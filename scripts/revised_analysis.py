"""Revised RQ3/RQ4. Historical exports live under history/, never overwritten."""
from pathlib import Path
import argparse, hashlib, json, time, platform
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import GroupShuffleSplit
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, silhouette_score, adjusted_rand_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering

COUNTRIES = ['DEU', 'ESP', 'EST', 'FRA', 'ITA', 'POL', 'QUR']
PVS = [f'PV{i}MATH' for i in range(1, 11)]
CORE = ['EDUSHORT', 'CLSIZE', 'PROATCE_10PP', 'ESCS']
SCHOOL = ['EDUSHORT', 'CLSIZE', 'PROATCE', 'SCH_ESCS']
EXPECTED_HASH = '2d1638ff15ba1a1dce592f0d5f67d6abc329e9e7155f4c6de340d615d8fb3bfb'

def weights(d, strategy):
    w = d.W_FSTUWT.astype(float).copy()
    if strategy == 'equal_country':
        w = w / w.groupby(d.CNT).transform('sum')
    return w.to_numpy()

class TrainingImputer:
    """Recover missingness from flags, fit medians on training records only.

    School medians use one row per school; student ESCS medians use students.
    School ESCS uses observed ESCS in the same school, independent of maths PV.
    Test school intake is assumed observable at prediction time.
    """
    @staticmethod
    def restore(d):
        x = d.copy()
        for col in ['ESCS', 'EDUSHORT', 'CLSIZE', 'PROATCE']:
            x.loc[x[col + '_imputed'].astype(bool), col] = np.nan
        means = x.groupby('SCHOOL_GROUP_ID').ESCS.mean()
        x['SCH_ESCS'] = x.SCHOOL_GROUP_ID.map(means)
        return x

    def fit(self, d):
        x = self.restore(d)
        self.medians = {}
        for col in ['ESCS'] + SCHOOL:
            u = x if col == 'ESCS' else x.drop_duplicates('SCHOOL_GROUP_ID')
            global_median = u[col].median()
            if not np.isfinite(global_median):
                raise ValueError(f'No observed training values for {col}')
            self.medians[col] = (u.groupby('CNT')[col].median().to_dict(), global_median)
        return self

    def transform(self, d):
        x = self.restore(d)
        for col, (by_country, fallback) in self.medians.items():
            x[col] = x[col].fillna(x.CNT.map(by_country)).fillna(fallback)
        x['PROATCE_10PP'] = x.PROATCE * 10
        if not np.isfinite(x[CORE + ['SCH_ESCS']].to_numpy(float)).all():
            raise ValueError('Unfilled/nonfinite predictors')
        return x


def design(d, features):
    countries = pd.get_dummies(pd.Categorical(d.CNT, categories=COUNTRIES), dtype=float)
    countries.columns = ['CNT_' + c for c in COUNTRIES]
    countries.index = d.index
    return pd.concat([d[features].astype(float), countries.iloc[:, 1:]], axis=1)


def permuted_design(b, features, feature, rng):
    x = b.copy()
    # School variables remain constant inside each school; swaps are within country.
    for c in COUNTRIES:
        mask = x.CNT == c
        if feature == 'ESCS':
            x.loc[mask, feature] = rng.permutation(x.loc[mask, feature].to_numpy())
        else:
            u = x.loc[mask].drop_duplicates('SCHOOL_GROUP_ID')
            shuffled = dict(zip(u.SCHOOL_GROUP_ID, rng.permutation(u[feature].to_numpy())))
            x.loc[mask, feature] = x.loc[mask, 'SCHOOL_GROUP_ID'].map(shuffled)
    return design(x, features)


def run_rq3(d, out, seeds, trees, repeats):
    rows, coefs, imps, split_rows, countries, medians = [], [], [], [], [], []
    variants = [('main', CORE + ['SCH_ESCS'], 'equal_country'),
                ('without_school_ESCS', CORE, 'equal_country'),
                ('population_sensitivity', CORE + ['SCH_ESCS'], 'population')]
    for seed in seeds:
        tr, te = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed).split(d, groups=d.SCHOOL_GROUP_ID))
        a0, b0 = d.iloc[tr], d.iloc[te]
        assert not set(a0.SCHOOL_GROUP_ID) & set(b0.SCHOOL_GROUP_ID)
        assert set(a0.CNT) == set(b0.CNT) == set(COUNTRIES)
        imputer = TrainingImputer().fit(a0)
        a, b = imputer.transform(a0), imputer.transform(b0)
        for col, (cm, gm) in imputer.medians.items():
            for c in COUNTRIES:
                medians.append(dict(seed=seed, feature=col, country=c, train_median=cm[c], fallback_median=gm))
        for part, sub in [('train', a), ('test', b)]:
            for c, g in sub.groupby('CNT'):
                split_rows.append(dict(seed=seed, partition=part, country=c, students=len(g), schools=g.SCHOOL_GROUP_ID.nunique()))
        for variant, features, weighting in variants:
            # Weighting sensitivity uses primary seed; both main specifications use all seeds.
            if variant == 'population_sensitivity' and seed != seeds[0]:
                continue
            wa, wb = weights(a, weighting), weights(b, weighting)
            xa, xb = design(a, features), design(b, features)
            mean = np.average(xa[features], axis=0, weights=wa)
            sd = np.sqrt(np.average((xa[features] - mean)**2, axis=0, weights=wa))
            for pi, pv in enumerate(PVS):
                y = b[pv].to_numpy()
                baselines = {
                    'TrainingWeightedMean': np.full(len(b), np.average(a[pv], weights=wa)),
                    'CountryTrainingMean': b.CNT.map(a.groupby('CNT').apply(lambda g: np.average(g[pv], weights=g.W_FSTUWT), include_groups=False)).to_numpy()}
                fitted = {}
                for name, model in [('LinearRegression', LinearRegression()),
                                    ('RandomForest', RandomForestRegressor(n_estimators=trees, min_samples_leaf=5, random_state=42, n_jobs=2))]:
                    model.fit(xa, a[pv], sample_weight=wa)
                    fitted[name] = model
                    baselines[name] = model.predict(xb)
                    if name == 'LinearRegression':
                        for j, f in enumerate(features):
                            coefs.append(dict(seed=seed, variant=variant, pv=pv, feature=f, coefficient=model.coef_[j], weighted_training_sd=sd[j], coefficient_per_sd=model.coef_[j]*sd[j]))
                for name, pred in baselines.items():
                    mae = mean_absolute_error(y, pred, sample_weight=wb)
                    rows.append(dict(seed=seed, variant=variant, weighting=weighting, pv=pv, model=name, mae=mae, r2=r2_score(y, pred, sample_weight=wb)))
                    if variant == 'main':
                        for c in COUNTRIES:
                            ix=(b.CNT == c).to_numpy()
                            countries.append(dict(seed=seed, pv=pv, model=name, country=c, n=int(ix.sum()), mae=mean_absolute_error(y[ix], pred[ix], sample_weight=wb[ix]), r2=r2_score(y[ix], pred[ix], sample_weight=wb[ix])))
                    if seed == seeds[0] and variant == 'main' and name in fitted:
                        # Same permutations for both models, all ten PVs; descriptive spread, not a confidence interval.
                        for fi, feature in enumerate(features):
                            for repeat in range(repeats):
                                xp = permuted_design(b, features, feature, np.random.default_rng(1000 + 100*fi + repeat))
                                delta = mean_absolute_error(y, fitted[name].predict(xp), sample_weight=wb) - mae
                                imps.append(dict(seed=seed, pv=pv, model=name, feature=feature, repeat=repeat, delta_mae=delta))
            print(f'RQ3 completed seed={seed} variant={variant}', flush=True)
    metrics=pd.DataFrame(rows); metrics.to_csv(out/'RQ3_metrics_all_PVs.csv', index=False)
    metrics.groupby(['seed','variant','weighting','model'])[['mae','r2']].mean().to_csv(out/'RQ3_model_comparison.csv')
    pd.DataFrame(coefs).to_csv(out/'RQ3_LR_coefficients_all_PVs.csv', index=False)
    pd.DataFrame(coefs).groupby(['seed','variant','feature'])[['coefficient','weighted_training_sd','coefficient_per_sd']].mean().to_csv(out/'RQ3_LR_coefficients.csv')
    pd.DataFrame(imps).to_csv(out/'RQ3_permutation_all_PVs.csv', index=False)
    pd.DataFrame(imps).groupby(['model','feature']).delta_mae.agg(['mean','std','min','max']).to_csv(out/'RQ3_permutation_importance.csv')
    pd.DataFrame(split_rows).to_csv(out/'RQ3_school_splits.csv', index=False)
    pd.DataFrame(countries).groupby(['seed','model','country']).agg(n=('n','first'),mae=('mae','mean'),r2=('r2','mean')).to_csv(out/'RQ3_country_metrics.csv')
    pd.DataFrame(medians).to_csv(out/'RQ3_training_imputation_parameters.csv', index=False)
    return metrics


def run_rq4(d, out):
    # Descriptive country means: imputed school fields are excluded variable by variable.
    features=['EDUSHORT','CLSIZE','PROATCE_10PP','ESCS']
    s=d.copy(); s['PROATCE_10PP']=s.PROATCE*10
    summaries=[]; missing=[]
    for c,g in s.groupby('CNT'):
        row={'CNT':c}
        for f in features:
            flag=('PROATCE' if f=='PROATCE_10PP' else f)+'_imputed'
            observed=g[flag].eq(0)
            assert observed.any(), (c,f,'entirely imputed')
            row[f]=np.average(g.loc[observed,f], weights=g.loc[observed,'W_FSTUWT'])
            missing.append(dict(country=c, feature=f, students=len(g), observed_students=int(observed.sum()), weighted_imputed_share=np.average(~observed,weights=g.W_FSTUWT)))
        summaries.append(row)
    country=pd.DataFrame(summaries).set_index('CNT');country.to_csv(out/'RQ4_country_features_observed.csv')
    pd.DataFrame(missing).to_csv(out/'RQ4_feature_coverage.csv', index=False)
    scores=[]; memberships=[]; stability=[]
    for coverage,ss in [('seven',country),('without_QUR',country.drop('QUR'))]:
        for omitted in [None]+features:
            fs=[f for f in features if f!=omitted]
            x=StandardScaler().fit_transform(ss[fs])
            for k in [2,3,4]:
                km=KMeans(n_clusters=k, random_state=42,n_init=50).fit(x)
                labs=km.labels_
                ward=AgglomerativeClustering(n_clusters=k,linkage='ward').fit_predict(x)
                variant='main' if omitted is None else 'without_'+omitted
                scores.append(dict(coverage=coverage,variant=variant,k=k,silhouette=silhouette_score(x,labs),ward_ARI=adjusted_rand_score(labs,ward)))
                for c,label in zip(ss.index,labs):
                    memberships.append(dict(coverage=coverage,variant=variant,k=k,country=c,cluster=int(label)))
                for seed in [7,2026]:
                    alt=KMeans(n_clusters=k,random_state=seed,n_init=50).fit_predict(x)
                    stability.append(dict(coverage=coverage,variant=variant,k=k,seed=seed,ARI=adjusted_rand_score(labs,alt)))
    pd.DataFrame(scores).to_csv(out/'RQ4_cluster_scores.csv',index=False)
    pd.DataFrame(memberships).to_csv(out/'RQ4_cluster_memberships.csv',index=False)
    pd.DataFrame(stability).to_csv(out/'RQ4_seed_stability.csv',index=False)
    main=pd.DataFrame(scores).query("coverage=='seven' and variant=='main'")
    best_k=int(main.loc[main.silhouette.idxmax(),'k'])
    selected=pd.DataFrame(memberships).query("coverage=='seven' and variant=='main' and k==@best_k").set_index('country').cluster
    clusters=country.join(selected);clusters.to_csv(out/'RQ4_selected_clusters.csv')
    clusters.groupby('cluster')[features].mean().to_csv(out/'RQ4_cluster_profiles.csv')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from scipy.cluster.hierarchy import linkage,dendrogram
    fig,ax=plt.subplots(figsize=(8,5))
    ax.scatter(clusters.CLSIZE,clusters.EDUSHORT,c=clusters.cluster,cmap='tab10',s=80)
    for c,row in clusters.iterrows():ax.annotate(c,(row.CLSIZE,row.EDUSHORT),xytext=(4,5),textcoords='offset points')
    ax.margins(x=.12, y=.1)
    ax.set(xlabel='Weighted class size (observed records)',ylabel='Weighted resource shortage (observed records)',title=f'Exploratory country profiles: k={best_k}; clustering uses four features')
    fig.tight_layout();fig.savefig(out/'RQ4_country_clusters.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5));dendrogram(linkage(StandardScaler().fit_transform(country),method='ward'),labels=country.index.tolist(),leaf_rotation=35,leaf_font_size=10,ax=ax)
    ax.set(title='Exploratory Ward dendrogram: seven systems',ylabel='Distance on standardized country features')
    fig.tight_layout();fig.savefig(out/'RQ4_dendrogram.png',dpi=180);plt.close(fig)
    return best_k


def main():
    p=argparse.ArgumentParser();p.add_argument('dataset',type=Path);p.add_argument('--output',type=Path,default=Path('results/revised'));p.add_argument('--seeds',nargs='+',type=int,default=[42,7,2026]);p.add_argument('--trees',type=int,default=100);p.add_argument('--permutation-repeats',type=int,default=3)
    args=p.parse_args();t=time.perf_counter();args.output.mkdir(parents=True,exist_ok=True)
    sha=hashlib.sha256(args.dataset.read_bytes()).hexdigest()
    if sha!=EXPECTED_HASH:raise ValueError('Dataset differs from reviewed version; do not silently mix versions.')
    full=pd.read_parquet(args.dataset);d=full[full.CNT.isin(COUNTRIES)].copy().reset_index(drop=True)
    assert len(d)==70517 and d.SCHOOL_GROUP_ID.nunique()==2449
    metrics=run_rq3(d,args.output,args.seeds,args.trees,args.permutation_repeats)
    k=run_rq4(d,args.output)
    info=dict(dataset_sha256=sha,students=len(d),schools=d.SCHOOL_GROUP_ID.nunique(),countries=COUNTRIES,seeds=args.seeds,trees=args.trees,min_samples_leaf=5,permutation_repeats=args.permutation_repeats,selected_k=k,elapsed_seconds=round(time.perf_counter()-t,2),python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,sklearn=sklearn.__version__,scope='Ten separate PV fits; predictive metrics and importance have no survey-design confidence intervals. Fixed untuned RF settings. RQ4 observed-only country means use variable-specific responding subsets; no stable population typology claim.')
    (args.output/'run_manifest.json').write_text(json.dumps(info,indent=2)+'\n')
    print(metrics.groupby(['seed','variant','model'])[['mae','r2']].mean().to_string(),flush=True)
    print(json.dumps(info,indent=2),flush=True)

if __name__=='__main__':main()

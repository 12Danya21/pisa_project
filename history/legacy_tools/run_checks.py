"""Historical specification checks only. Current analysis: revised_analysis.py.
Use --output outside results/revised/ to avoid mixing versions.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error,r2_score,silhouette_score,adjusted_rand_score
import sklearn,json
import argparse
parser=argparse.ArgumentParser(description='Independent PISA checks; does not modify source data.')
parser.add_argument('dataset',type=Path)
parser.add_argument('--output',type=Path,default=Path('pisa_check_results'))
args=parser.parse_args()
out=args.output;out.mkdir(exist_ok=True,parents=True)
d=pd.read_parquet(args.dataset)
d=d[d.CNT.isin(['DEU','FRA','POL','EST','ITA','ESP','QUR'])].copy()
d['group']=d.CNT.astype(str)+'_'+d.CNTSCHID.astype(str)
features=['CLSIZE','EDUSHORT','STAFFSHORT','SCH_ESCS','ESCS'];pvs=[f'PV{i}MATH' for i in range(1,11)]
d.groupby('CNT')[[c for c in d if c.endswith('_imputed')]].mean().mul(100).to_csv(out/'imputed_percent_by_country.csv')
rows=[];country=[]
for seed in [42,7,2026]:
 tr,te=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=seed).split(d,groups=d.group))
 a,b=d.iloc[tr],d.iloc[te]
 assert not set(a.group)&set(b.group)
 for variant,fs in [('original',features),('without_STAFFSHORT',[f for f in features if f!='STAFFSHORT'])]:
  for pv in pvs:
   models={'LinearRegression':LinearRegression()}
   if seed==42:models['RandomForest']=RandomForestRegressor(n_estimators=100,min_samples_leaf=5,random_state=42,n_jobs=-1)
   for name,m in models.items():
    m.fit(a[fs],a[pv],sample_weight=a.W_FSTUWT);pred=m.predict(b[fs])
    rows.append(dict(seed=seed,variant=variant,model=name,pv=pv,mae=mean_absolute_error(b[pv],pred,sample_weight=b.W_FSTUWT),r2=r2_score(b[pv],pred,sample_weight=b.W_FSTUWT)))
    if seed==42:
     for cnt in sorted(b.CNT.unique()):
      ix=(b.CNT==cnt).to_numpy();country.append(dict(country=cnt,variant=variant,model=name,pv=pv,n=int(ix.sum()),mae=mean_absolute_error(b.loc[ix,pv],pred[ix],sample_weight=b.loc[ix,'W_FSTUWT']),r2=r2_score(b.loc[ix,pv],pred[ix],sample_weight=b.loc[ix,'W_FSTUWT'])))
  print('Finished',seed,variant,flush=True)
 for pv in pvs:
  pred=np.full(len(b),np.average(a[pv],weights=a.W_FSTUWT))
  rows.append(dict(seed=seed,variant='baseline',model='TrainingWeightedMean',pv=pv,mae=mean_absolute_error(b[pv],pred,sample_weight=b.W_FSTUWT),r2=r2_score(b[pv],pred,sample_weight=b.W_FSTUWT)))
r=pd.DataFrame(rows);r.to_csv(out/'metrics_all_pvs.csv',index=False)
r.groupby(['seed','variant','model'])[['mae','r2']].mean().to_csv(out/'model_summary.csv')
c=pd.DataFrame(country);c.groupby(['country','variant','model']).agg(n=('n','first'),mae=('mae','mean'),r2=('r2','mean')).to_csv(out/'country_test_metrics.csv')
cf=['CLSIZE','EDUSHORT','STAFFSHORT','SCH_ESCS']
s=d.groupby('CNT').apply(lambda g:pd.Series({f:np.average(g[f],weights=g.W_FSTUWT) for f in cf}),include_groups=False)
cl=[];labels=[]
for variant,fs in [('original',cf),('without_STAFFSHORT',[f for f in cf if f!='STAFFSHORT'])]:
 for coverage,ss in [('seven',s),('without_QUR',s.drop('QUR'))]:
  x=StandardScaler().fit_transform(ss[fs])
  for k in [2,3,4]:
   lab=KMeans(n_clusters=k,random_state=42,n_init=20).fit_predict(x)
   cl.append(dict(variant=variant,coverage=coverage,k=k,silhouette=silhouette_score(x,lab)))
   for cnt,l in zip(ss.index,lab):labels.append(dict(variant=variant,coverage=coverage,k=k,country=cnt,cluster=int(l)))
pd.DataFrame(cl).to_csv(out/'cluster_scores.csv',index=False);pd.DataFrame(labels).to_csv(out/'cluster_membership.csv',index=False)
(out/'environment.json').write_text(json.dumps({'pandas':pd.__version__,'numpy':np.__version__,'sklearn':sklearn.__version__,'note':'All metrics average ten separate plausible-value analyses. No survey-design confidence intervals. Preprocessed supplied data; raw pipeline not rerun.'},indent=2))
print(r.groupby(['seed','variant','model'])[['mae','r2']].mean().to_string(),flush=True)
print(pd.DataFrame(cl).to_string(index=False),flush=True)
print(pd.DataFrame(labels).to_string(index=False),flush=True)

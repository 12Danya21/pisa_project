"""Descriptive country context and RQ4 imputation sensitivity; no inferential ranking."""
from pathlib import Path
import pandas as pd,numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score,adjusted_rand_score
from revised_analysis import COUNTRIES
r=Path(__file__).resolve().parents[1];o=r/'results/revised';o.mkdir(parents=True,exist_ok=True)
d=pd.read_parquet(r/'data/processed/pisa_cleaned_dataset.parquet');d=d[d.CNT.isin(COUNTRIES)].copy();d['PROATCE_10PP']=d.PROATCE*10
rows=[]
for c,g in d.groupby('CNT'):
    row={'CNT':c,'students':len(g),'schools':g.SCHOOL_GROUP_ID.nunique(),'maths_PV_mean':np.average(g[[f'PV{i}MATH' for i in range(1,11)]].mean(axis=1),weights=g.W_FSTUWT)}
    for f in ['ESCS','EDUSHORT','CLSIZE','PROATCE_10PP']:
        row[f+'_prepared']=np.average(g[f],weights=g.W_FSTUWT)
        flag=('PROATCE' if f=='PROATCE_10PP' else f)+'_imputed';obs=g[flag].eq(0)
        row[f+'_observed']=np.average(g.loc[obs,f],weights=g.loc[obs,'W_FSTUWT'])
        row[f+'_weighted_imputed_share']=np.average(~obs,weights=g.W_FSTUWT)
    rows.append(row)
s=pd.DataFrame(rows).set_index('CNT');s.to_csv(o/'country_context_summary.csv')
features=['EDUSHORT','CLSIZE','PROATCE_10PP','ESCS'];scores=[]
for coverage,ss in [('seven',s),('without_QUR',s.drop('QUR'))]:
    a=StandardScaler().fit_transform(ss[[f+'_observed' for f in features]])
    b=StandardScaler().fit_transform(ss[[f+'_prepared' for f in features]])
    for k in [2,3,4]:
        la=KMeans(n_clusters=k,n_init=50,random_state=42).fit_predict(a)
        lb=KMeans(n_clusters=k,n_init=50,random_state=42).fit_predict(b)
        scores.append({'coverage':coverage,'k':k,'observed_silhouette':silhouette_score(a,la),'prepared_silhouette':silhouette_score(b,lb),'ARI_observed_vs_prepared':adjusted_rand_score(la,lb)})
pd.DataFrame(scores).to_csv(o/'RQ4_observed_vs_prepared_sensitivity.csv',index=False)
print('Country context and observed/prepared clustering sensitivity exported.')

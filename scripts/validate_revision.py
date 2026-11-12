"""Focused invariants for the revised school split, imputation and saved artifacts."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from revised_analysis import TrainingImputer,weights,design,CORE,COUNTRIES,EXPECTED_HASH

root=Path(__file__).resolve().parents[1]
d=pd.read_parquet(root/'data/processed/pisa_cleaned_dataset.parquet')
d=d[d.CNT.isin(COUNTRIES)].reset_index(drop=True)
tr,te=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(d,groups=d.SCHOOL_GROUP_ID))
a,b=d.iloc[tr],d.iloc[te]
assert not set(a.SCHOOL_GROUP_ID)&set(b.SCHOOL_GROUP_ID)
p=TrainingImputer().fit(a);before=json.dumps(p.medians,sort_keys=True)
# Change all flagged held-out entries drastically: restored values must be identical.
changed=b.copy()
for f in ['ESCS','EDUSHORT','CLSIZE','PROATCE']:
    changed.loc[changed[f+'_imputed'].astype(bool),f]=999999
np.testing.assert_allclose(p.transform(b)[CORE+['SCH_ESCS']],p.transform(changed)[CORE+['SCH_ESCS']])
assert before==json.dumps(p.medians,sort_keys=True)
x=p.transform(b)
assert x.groupby('SCHOOL_GROUP_ID')[['EDUSHORT','CLSIZE','PROATCE_10PP','SCH_ESCS']].nunique().le(1).all().all()
w=weights(b,'equal_country')
np.testing.assert_allclose(pd.Series(w,index=b.index).groupby(b.CNT).sum(),np.ones(7))
assert design(p.transform(a),CORE).columns.equals(design(x,CORE).columns)
assert hashlib.sha256((root/'data/processed/pisa_cleaned_dataset.parquet').read_bytes()).hexdigest()==EXPECTED_HASH
hist=root/'history/pre_fix_49e71c4'
for f,expected in json.loads((hist/'SHA256.json').read_text()).items():
    assert hashlib.sha256((hist/f).read_bytes()).hexdigest()==expected,f
out=root/'results/revised'
if (out/'run_manifest.json').exists():
    m=pd.read_csv(out/'RQ3_metrics_all_PVs.csv')
    assert len(m)==280 and set(m.pv)=={f'PV{i}MATH' for i in range(1,11)}
    assert m[['mae','r2']].notna().all().all()
    for seed in [42,7,2026]:
        assert set(m.loc[(m.seed==seed)&(m.variant=='main'),'model'])=={'LinearRegression','RandomForest','TrainingWeightedMean','CountryTrainingMean'}
    c=pd.read_csv(out/'RQ4_country_features_observed.csv')
    assert len(c)==7 and 'STAFFSHORT' not in c and 'PROATCE_10PP' in c
    cv=pd.read_csv(out/'RQ4_feature_coverage.csv')
    assert cv.observed_students.gt(0).all()
    for f,expected in json.loads((out/'OUTPUT_SHA256.json').read_text()).items():
        assert hashlib.sha256((root/f).read_bytes()).hexdigest()==expected, f
    co=pd.read_csv(out/'RQ1_RQ2/RQ1_RQ2_coefficients.csv')
    got=co.loc[(co.model=='RQ2_ESCS_adjusted')&(co.term=='CLSIZE'),'coefficient'].iloc[0]
    np.testing.assert_allclose(got,1.01680374370473,atol=1e-9)
print('PASS: school isolation, training-only imputation invariance, school consistency, equal-country weights, schema, unchanged data and historical hashes; completed results checked when available.')

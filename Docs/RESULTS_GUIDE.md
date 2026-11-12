# Results guide — corrected analysis, not the final report

This guide explains what changed, how to read each result, and what the team can defend. Full original results remain in history/pre_fix_49e71c4; current exports are under results/revised/.

## Common sample and estimation targets

All RQs use the same seven systems and 70,517 students in 2,449 schools. The 121,564-row Parquet is an unchanged 14-system preparation file. Main analyses give each system equal influence. Population-weight sensitivity answers a different pooled question; compare models only within a common specification/weighting/split.

RQ1/RQ2 use all records for survey inference. RQ3 fits only training schools, with train-only preprocessing; held-out errors therefore need not reproduce the full-sample coefficients. RQ4 summarizes observed responding records within each country and does not use mathematics as a clustering feature.

## RQ1/RQ2: what survives socioeconomic adjustment?

| Term | RQ1 | RQ2: +student ESCS | RQ2b: +school ESCS |
|---|---:|---:|---:|
| EDUSHORT, points per index unit | −4.051 | −1.955 | +1.097 |
| CLSIZE, points per student | +1.532 | +1.017 | +0.241 |
| PROATCE_10PP, points per +10 percentage points | +0.575 | +0.406 | +0.176 |

RQ1/RQ2 estimates and standard errors reproduce the supplied notebook. In RQ2, shortage and certification intervals include zero; class size is positive. Adding SCH_ESCS reduces the class-size association to +0.241 (95% CI −0.018 to +0.500, p≈0.069), and none of the three policy terms is significant at 5%. Student/school background remains strongly associated with scores.

This does not prove resources have no effect or larger classes are useful. Intake selection and compensatory allocation are plausible explanations, not established mechanisms. No prior-achievement or experimental comparison identifies a spending effect. Without QUR, shortage and certification become significant in RQ2; population weighting also changes their significance. The conclusion must state that sensitivity.

## RQ3: do LR and RF agree?

Primary split seed=42; averages of ten separately fitted PV analyses. Main predictors: EDUSHORT, CLSIZE, PROATCE_10PP, ESCS, SCH_ESCS and country indicators. RF uses 100 trees, min_samples_leaf=5; settings were not tuned.

| Model | Weighted MAE | Weighted R² |
|---|---:|---:|
| CountryTrainingMean | 70.829 | 0.0506 |
| LinearRegression | 60.881 | 0.2787 |
| RandomForest | 61.771 | 0.2564 |
| TrainingWeightedMean | 72.699 | -0.0005 |

Across all three common school splits:

| Seed | LR MAE | RF MAE | LR R² | RF R² |
|---|---:|---:|---:|---:|
| 42 | 60.881 | 61.771 | 0.2787 | 0.2564 |
| 7 | 61.567 | 62.782 | 0.2992 | 0.2678 |
| 2026 | 60.661 | 61.898 | 0.2917 | 0.2641 |

LR has lower MAE and higher R² on each tested split. Both beat the overall and country training-mean baselines. Without school ESCS, errors increase for both models: intake information provides substantial predictive signal in these specified models. This is not an estimate of changing peer composition. RF losing this comparison does not prove the true relationships are linear or that every nonlinear model would lose.

### Which predictors do the models use?

Weighted held-out permutation importance at seed=42, three repetitions per PV. Positive delta means prediction error increased after disruption. Numerical school features are swapped by school within country; individual ESCS is swapped by student within country. Country dummies stay intact. The table describes numeric features conditional on country; it does not rank country indicators.

| Feature | LR delta MAE | RF delta MAE |
|---|---:|---:|
| SCH_ESCS | 13.269 | 13.114 |
| ESCS | 2.646 | 3.806 |
| PROATCE_10PP | -0.054 | 0.242 |
| CLSIZE | 0.047 | 0.155 |
| EDUSHORT | -0.002 | -0.208 |

Both models rely most on school ESCS, followed by individual ESCS among these numeric features. The policy variables have much smaller and sometimes negative permutation effects. Negative importance means that disrupting a feature improved held-out prediction in this exercise; it is not evidence that the underlying resource is harmful. Certification is slightly useful in RF here and not in LR; its scale is small beside background variables, and values vary over PVs/permutations. Correlated features can substitute for one another, and unrealistic shuffled combinations can affect the result. No causal or significance ranking follows.

### Why the new numbers differ from the old numbers

Old RQ3 used STAFFSHORT instead of certification, lacked country controls, used population weights and inherited imputation from the whole prepared sample. Current RQ3 changes all those elements and treats school ESCS availability explicitly. Several things changed together, so no exact share of the old/new MAE difference can be assigned to an individual fix. Historical old MAE 60.876/62.493 and current equal-country MAE must not be compared as a before/after improvement; the weighting targets differ. The population-sensitivity export provides an explicit like-target check, still with corrected predictors/preprocessing.

## RQ4: are there recognizable groups?

Current features are weighted observed-only means of EDUSHORT, CLSIZE, PROATCE_10PP and ESCS, standardized across countries. The ESCS level is used as a background indicator, not a segregation measure. Variable-specific responding subsets and missingness are recorded; observed/prepared sensitivity is exported.

| k | Silhouette |
|---|---:|
| 2 | 0.4057 |
| 3 | 0.3029 |
| 4 | 0.1746 |

The selected k=2 separates QUR from DEU/ESP/EST/FRA/ITA/POL. This primarily identifies an outlying resource/background profile; it does not establish two general institutional school-system types. QUR has higher reported shortage and lower certification/background in this selected sample. No causal explanation for that profile is identified.

At k=3 (secondary detail), EST/ITA group together, DEU/ESP/FRA/POL form another group, and QUR remains alone. This differs from the original STAFFSHORT-based grouping. Excluding QUR and restandardizing yields two groups DEU/EST/ITA and ESP/FRA/POL (silhouette 0.2967); the grouping depends on which country points define the feature scales.

The selected k=2 is stable to the tested K-means initialization seeds and agrees with Ward for this feature set. Observed vs prepared means produce the same k=2 and k=3 memberships, but not k=4. At k=4 even the seven-country main solution changes across initialization seeds (ARI≈0.488). These diagnostics do not establish sampling stability. See all leave-feature-out and without-QUR exports rather than selecting a convenient partition.

## What can be defended in discussion

- We corrected the comparison so certification, rather than staff shortage, represents the third policy proxy.
- Socioeconomic adjustment changes the interpretation, especially for class size; it does not transform the analysis into a causal study.
- In the tested matched specifications/splits, LR predicts better than the fixed RF and both use background information strongly.
- Seven-country clustering is exploratory. The strongest split isolates QUR; finer groupings depend on the specification.
- The data cannot identify the best return on ministry investment because intervention effects and costs are absent.

The first report draft and four-sentence recommendation are now in `report/PISA_report_draft.md`. Use the verified outputs and limitations below when revising it. Presentation slides remain to be assembled.

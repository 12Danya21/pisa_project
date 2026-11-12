# Data dictionary — reviewed preparation file and analytical subset

The unchanged preparation file contains 121,564 student records, 4,347 schools, 14 systems and 111 columns. All current RQ1–RQ4 use DEU, ESP, EST, FRA, ITA, POL and QUR: 70,517 students and 2,449 schools. Exact provenance and SHA-256 are in `data/DATA_MANIFEST.json`. Counts describe sampled records, not population sizes.

## Fields in plain language

| Field | Level | Meaning and interpretation |
|---|---|---|
| CNT | System | Education-system identifier. QUR represents the Ukrainian regions assessed, not all of Ukraine. |
| CNTSCHID | School | School identifier. Use together with CNT for joins and grouping. |
| SCHOOL_GROUP_ID | School | Composite CNT + school ID. All students in a school stay in the same training/test partition. |
| PV1MATH–PV10MATH | Student | Ten plausible draws for latent mathematics proficiency, not ten observed repeat test scores. Higher means higher proficiency. |
| EDUSHORT | School | Principal-reported index of educational material/infrastructure shortages hindering instruction. Higher means greater shortage; it is not equipment spending. |
| CLSIZE | School | Principal-reported class-size measure for the relevant modal grade/test-language class, represented by size-band values. It is not a direct measure of each student's mathematics class. |
| PROATCE | School | Proportion of teachers fully certified by the appropriate authority; in this file 0–1. Certification is not the quality of teaching or professional development. |
| PROATCE_10PP | School, derived | PROATCE × 10. One unit is ten percentage points of certification (e.g. 0.70→0.80). Current models create it; its absence in the original parquet is expected. |
| ESCS | Student | Economic, social and cultural status index based on family background/home resources. Higher values indicate greater socioeconomic advantage. |
| SCH_ESCS | School, derived | Mean of observed sampled students' ESCS in that school, computed before student ESCS imputation. Represents the level of school intake, not teaching quality, a causal peer effect, or the degree of segregation across schools. |
| W_FSTUWT | Student | Final survey weight: the represented population contribution of a sampled student. Used for within-country descriptive means and population sensitivity. |
| SENWT | Student | Pipeline weight rescaled to total 1,000 per system. Equal-country pooled comparisons are proportional to these weights on the common full subset. Training/testing normalize their own country totals. |
| W_FSTURWT1–80 | Student | Fay-BRR replicate weights for survey sampling uncertainty. RQ1/RQ2 uses all 80 per independent system, on the same scale as the main weights. |
| *_imputed | Respective level | 1 means the original value was missing and the pipeline replaced it; 0 means observed. Zero remaining nulls does not mean complete original observations. |
| STAFFSHORT | School, secondary only | Principal-reported staff-shortage index. It is not teacher qualification. Fully imputed in Estonia (and Belgium in the preparation sample); excluded from current main models and clustering. |
| STRATIO | School, unused in current main models | Student-to-teacher ratio across the school. Different from class size. |
| SCHLTYPE | School, unused in current main models | Categorical school governance/management variable. Do not treat its numeric labels as a continuous scale. Fully imputed in Austria in the preparation file; cannot substantiate an Austrian governance-share statement. |

## Plausible values and uncertainty

RQ1/RQ2 fits all ten PVs, combines coefficient estimates, averages sampling variance and adds (1+1/10) times the between-PV variance. Sampling variance uses 0.05 × sum of squared replicate deviations (80 replicates, Fay coefficient 0.5), applied one independent country at a time. Its p-values and intervals use normal approximations. Averaging PVs before a nonlinear model is not equivalent to fitting ten models; even for a fixed-design linear model where coefficients commute with averaging, the mean alone does not retain PV uncertainty.

RQ3 fits LR and RF separately for every PV and reports mean held-out MAE/R². It does not provide BRR confidence intervals. Across-PV or across-split spread is descriptive, not a design-based standard error. RQ4 uses resource/background features and no maths outcome, so it needs no PV aggregation.

## Missingness and predictor availability

RQ1/RQ2 preserves the reviewed pipeline data and reports complete-case sensitivity (56,287 records). In the seven-system subset, unweighted student shares flagged are 3.82% for ESCS, 8.96% for EDUSHORT, 8.85% for CLSIZE and 15.33% for PROATCE. These are not school shares or weighted population shares.

RQ3 restores missing values from the flags, calculates medians from training records only (one record per school for school fields), then applies those parameters to held-out schools. SCH_ESCS is recalculated from observed ESCS within each partition's schools. Prediction assumes background information about the new school's sampled intake is available; it is not an outcome leak. Individual missing ESCS is filled with the training country median; no missing-PV values are imputed.

RQ4 estimates each country's feature mean from observed records, weighted by W_FSTUWT, excluding imputed entries variable by variable. Consequently features can use different responding subsets. `RQ4_feature_coverage.csv` quantifies this limitation; `RQ4_observed_vs_prepared_sensitivity.csv` compares with the prepared data. Country means describe students' school environments, not an equally weighted census of schools.

No investment costs, previous achievement, direct teacher-training quality or experimental assignment are present. The model cannot calculate policy return on investment.

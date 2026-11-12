# Country context — seven-system analytical sample

The preparation file covers 14 systems; this document describes only the seven used in every current RQ. Historical 14-system context remains under history/. Country codes and regional coverage must be retained when communicating results.

## Descriptive sample summaries

Weights: W_FSTUWT within country. Mathematics means average the ten weighted PV means; they are descriptive, with no standard errors in this table. Resource means exclude flagged imputed values variable by variable and therefore describe responding subsets. No rank significance is implied. Certification is shown as a percentage, not in the model’s ten-point units.

| CNT | Students | Schools | Maths mean | ESCS observed | CLSIZE observed | EDUSHORT observed | Certified teachers observed (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| DEU | 6,116 | 257 | 474.8 | -0.137 | 24.68 | -0.067 | 85.9 |
| ESP | 30,800 | 966 | 473.1 | -0.033 | 26.10 | -0.295 | 87.1 |
| EST | 6,392 | 196 | 509.9 | 0.151 | 22.46 | -0.128 | 76.9 |
| FRA | 6,770 | 282 | 473.9 | 0.000 | 29.69 | -0.403 | 81.1 |
| ITA | 10,552 | 344 | 471.3 | -0.100 | 23.90 | -0.206 | 73.7 |
| POL | 6,011 | 240 | 489.0 | -0.105 | 28.28 | -0.366 | 88.1 |
| QUR | 3,876 | 164 | 440.8 | -0.351 | 24.69 | 0.910 | 68.6 |

Machine-readable values and coverage: `results/revised/country_context_summary.csv` and `RQ4_feature_coverage.csv`. Reproduce with `python scripts/country_summary.py`. Country-level resource means describe students’ school environments, not each school counted equally.

## Context supported by the supplied data and OECD sources

- QUR represents Ukrainian regions (18 of 27); do not label it as national Ukraine. It has a particularly high shortage mean and lower background/performance in this selected sample. These descriptive differences do not identify the cause of an outlying cluster.
- The [OECD Annex A2](https://www.oecd.org/en/publications/pisa-2022-results-volume-i_53f23881-en/full-report/the-pisa-target-population-the-pisa-samples-and-the-definition-of-schools_35666ed9.html) documents exclusion/coverage concerns; these must be distinguished from response-quality flags. See limitations_draft.md.
- The [OECD sampling caution list](https://www.oecd.org/en/publications/pisa-2022-results-volume-ii_a97db61c-en/full-report/component-11.html) does not list these seven among the systems marked with a response/sampling caution asterisk. Do not use an earlier draft’s guess about the Netherlands to describe this sample: NLD is not analysed here.
- Institutional tracking ages, governance shares and precise COVID closure durations in the initial draft were not verified for this revision. They have been removed from the active explanatory claims, rather than filled with guesses. They are not required cluster inputs.

## How to explain the clusters

Use actual resource/background profiles and sensitivity tables in RESULTS_GUIDE.md. A grouping by these four means is not evidence of a shared institutional system. ESCS is a country background level; it is not a measure of between-school segregation. Do not attach “early tracking”, “comprehensive”, “better funded” or policy-effect labels without independent supporting evidence.

## What this document does not claim

No experimental spending effect, exact ranking, all-Europe representation or verified institutional explanation is inferred. The original institutional hypotheses are preserved in history for provenance, not endorsed as findings.

# Limitations and what would change our conclusion

Updated for the seven-system analysis. The initial draft is preserved in history/. Quantitative results are in RESULTS_GUIDE.md and results/revised/.

## Causal interpretation

PISA is cross-sectional and observational. Country indicators, ESCS and SCH_ESCS adjust selected observed differences; they do not identify what would happen after changing equipment, classes or teacher qualifications. Prior achievement, school leadership, academic track, geography and allocation rules remain possible confounders. Reverse allocation is plausible: schools facing greater need may receive smaller classes or additional resources.

The positive CLSIZE association is attenuated from +1.02 in RQ2 to +0.24 in RQ2b (p≈0.069). This is consistent with confounding by intake, but does not prove a selection mechanism. Neither RQ1 nor RQ2 is an upper/lower causal bound. School composition may reflect selection and past decisions; controlling it changes the question and is not automatically a more accurate causal estimate. Student family background need not be a mediator of a school's resource policy; no such causal ordering is established here.

**What would change the policy conclusion:** a credible experiment or natural experiment for a specific investment, showing outcomes and costs in a comparable population. Null or imprecise certification associations do not demonstrate that teacher development is ineffective.

## Measurement and missingness

EDUSHORT measures perceived shortage, CLSIZE is a banded class-size proxy, and PROATCE measures certification, not teaching quality. Measurement limitations can distort associations in either direction; universal attenuation is not guaranteed for this multivariable observational model.

RQ1/RQ2 retains single median imputations. Its complete-case sensitivity has 56,287 records and similar coefficients, but may still select a nonrepresentative responding subset. Median imputation does not propagate missing-data uncertainty into the standard errors. RQ3 learns imputation only on training schools and restores original missingness from flags. Missingness flags identify overwritten data, not their original unobserved values. RQ4 uses observed-only feature means; different variables have different responding subsets, quantified in its coverage table. Its comparison against prepared means is a sensitivity check, not a correction for nonrandom missingness. STAFFSHORT is excluded from main analysis because it is not certification and is entirely imputed in EST.

**What would change the interpretation:** materially different conclusions under a justified missing-data model, measured teaching quality, or direct class-size/resource data.

## Coverage, pandemic and geography

The team selected seven systems; they are not a probability sample of Europe. QUR covers Ukrainian regions (18 of 27), not the whole country. The OECD retained systems with response difficulties in the exceptional 2022 cycle; the general warning does not mean all seven systems failed its standards. See [OECD database](https://www.oecd.org/en/data/datasets/pisa-2022-database.html).

The [OECD Annex A2](https://www.oecd.org/en/publications/pisa-2022-results-volume-i_53f23881-en/full-report/the-pisa-target-population-the-pisa-samples-and-the-definition-of-schools_35666ed9.html) reports exclusions above 5% in EST (5.9%) and QUR (14.9%), and a QUR population-coverage decline to 63.9%. These are coverage/exclusion issues, distinct from an OECD response-quality asterisk. The [Volume II caution list](https://www.oecd.org/en/publications/pisa-2022-results-volume-ii_a97db61c-en/full-report/component-11.html) contains none of the seven selected systems; that is not proof of absence of bias.

COVID disruption, war, non-response and coverage can influence the results. No country-specific school-closure durations or institutional tracking claims enter the current cluster labels. They should not be invented to explain a grouping. Non-response bias has no known uniform direction from these files alone.

**What would change the interpretation:** coverage-adjusted evidence, clear response-bias diagnostics or a change in the target population. Excluding QUR already changes shortage/certification significance in RQ2; the pooled result is not universally stable.

## Weighting, nesting and uncertainty

Main regression and prediction give each country equal influence. Population-weight sensitivity answers a different question and can change apparent significance or performance. Student-weighted country means describe students' exposure to school conditions; they do not describe the average school with equal school weights. School predictors vary across 2,449 schools, not 70,517 independently assigned policy units.

RQ1/RQ2 uses ten PVs and country-wise Fay-BRR sampling variance, with normal confidence intervals/p-values. Neither this design correction nor country fixed effects removes confounding. RQ3 averages test metrics across ten separate PV models without design-based confidence intervals. Predictive spread across school splits or permutation repeats is not inferential evidence that one model is universally better. The three splits overlap in sampled records; they are not three independent studies.

**What would change the interpretation:** changes under population weights, a different country mix, or credible heterogeneity. Per-country coefficients describe heterogeneity but are not a leave-one-country-out influence analysis. In-sample regression R² must not be compared directly with held-out prediction R².

## Prediction and feature importance

LR/RF use the same variables, weights, school partitions and all ten PVs. Fixed RF settings are inherited from the old model and are not tuned. Thus any result compares these specified models; it does not establish that linear models outperform every possible nonlinear model. Both are evaluated against overall and country training means.

Permutation importance measures the change in held-out weighted MAE after disrupting a variable within country. School variables are swapped at school level. Importance has no causal meaning or intrinsic sign. Correlated ESCS/SCH_ESCS can substitute for each other; values are not additive shares of explained variation and need not match standardized coefficients. Shuffled feature combinations can be unrealistic. See [scikit-learn permutation guidance](https://scikit-learn.org/1.3/modules/permutation_importance.html).

Prediction with SCH_ESCS assumes intake-background observations for the new school. This may not apply to a school before any intake data are available. A without-SCH_ESCS specification is reported separately.

## Clustering

Only seven country points are clustered. Features are selected resource/background summaries, not an exhaustive description of institutions. Silhouette selection over k=2–4 is a descriptive choice in this tiny sample, not independent validation. A QUR singleton indicates an outlying profile, not a general school-system type. Leave-feature-out, prepared-vs-observed, without-QUR, seed and Ward checks are exported. Seed stability does not establish sampling stability. No survey bootstrap or population uncertainty for clusters is claimed.

**What would change the conclusion:** material changes after omitting a feature/system, a different defensible set of indicators, or a different sample. Report such changes instead of selecting a convenient narrative.

## Outcome and scope

Only mathematics is analysed. No conclusions about wellbeing, reading/science or long-term outcomes follow. Policy ranking also requires intervention costs and evidence about how investments change the measured variables. Those inputs are absent.

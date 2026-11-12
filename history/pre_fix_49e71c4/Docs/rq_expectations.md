# Research Questions — Expectations Before the Results

**Owner:** Interpretation & Limitations Lead
**Purpose:** write down, *before* seeing the models, what each possible result would mean. When results arrive we compare against this file. This protects against the rubric's main failure mode: "restating the numbers in words."
**Policy question (from the brief):** A ministry can fund one of three things — school equipment, smaller classes, better-trained teachers. Which one actually moves results?

> Keep this file unchanged once results come in. Add a section "What we actually found" at the bottom instead. Showing that we predicted, tested and revised is part of what is marked ("how you adjust your modelling strategy in response to intermediate results").

---

## Correlations already visible in the data

Before modelling, the predictor correlations (student level, n = 121,564) already tell us something:

| | EDUSHORT | CLSIZE | STRATIO | PROATCE | STAFFSHORT | SCH_ESCS |
|---|---|---|---|---|---|---|
| **SCH_ESCS** | −0.16 | **+0.13** | +0.14 | +0.07 | −0.12 | 1 |

- Advantaged schools report **less equipment shortage** → part of any equipment "effect" may be intake.
- Advantaged schools have **slightly larger classes** → a naive model may show larger classes with higher scores (see RQ1, scenario C).
- The three levers barely correlate with each other (|r| ≤ 0.04) → multicollinearity between them is not a problem; between `CLSIZE` and `STRATIO` (0.19) and `EDUSHORT` and `STAFFSHORT` (0.35) it is moderate.

---

## RQ1 — Which school factors correlate with performance?

*Main model: weighted linear regression of maths (10 PVs) on the three policy levers only, `EDUSHORT`, `CLSIZE` and `PROATCE`, with no background controls.*

*Additional / robustness models: add `STRATIO`, `STAFFSHORT` and `SCHLTYPE` one at a time. They are kept out of the main model because some are fully imputed in certain countries (`STAFFSHORT` in Belgium and Estonia, `SCHLTYPE` in Austria), and because `STRATIO` and `STAFFSHORT` overlap with `CLSIZE` and `EDUSHORT`. Robustness models either exclude those countries or are flagged as including imputed values. If the coefficients of the three levers stay similar across these models, the main result is robust.*

| Scenario | What we would see | What it would mean |
|---|---|---|
| **A. Equipment matters** | `EDUSHORT` negative and significant | Schools whose principals report less shortage have higher-scoring students. Before RQ2, this cannot be separated from those schools also having advantaged students. |
| **B. Class size: small classes help** | `CLSIZE` negative | Consistent with the intuitive policy story, but likely to shrink once background is controlled. |
| **C. Class size: large classes "help"** | `CLSIZE` **positive** | **Most likely result.** Not evidence that large classes are good. Explanations: (1) *compensatory allocation* — struggling or disadvantaged students are deliberately placed in smaller classes, (2) academic tracks and urban schools are both larger and higher-achieving. |
| **D. Teacher certification matters** | `PROATCE` positive | Higher share of certified teachers is associated with higher scores. Check whether it comes from a few low-certification countries (QUR, ITA, EST). |
| **E. Teacher certification shows nothing** | `PROATCE` ≈ 0 | Do **not** conclude "teachers don't matter". With 36% of students in fully certified schools, the variable has little variation and measures legal status, not teaching quality. |
| **F. Low R²** | School factors explain only a few % of variance | Expected. Most score variation in PISA is *within* schools, between students. This puts the minister's options in proportion: none of the three is a big lever on its own. |

**Standard-error check:** with replicate weights, school-level coefficients will have much wider confidence intervals than naive OLS would suggest. Any coefficient that is "significant" only without replicate weights must not reach the recommendation.

---

## RQ2 — What happens once we control for family background?

*Model: RQ1 + `ESCS` (student) + `SCH_ESCS` (school intake) + `ESCS_imputed` flag.*

| Scenario | What we would see | What it would mean |
|---|---|---|
| **A. Coefficients shrink a lot** | `EDUSHORT` / `PROATCE` move toward zero | **Most likely.** Much of the RQ1 association was about which students attend well-resourced schools, not about the resources themselves. |
| **B. Coefficients survive** | Similar size, still significant | Stronger (still not causal) evidence that the factor matters independently of intake. This is the lever to put in the recommendation, with caveats. |
| **C. Sign flips** | e.g. `CLSIZE` goes from positive to zero/negative | Classic confounding: the RQ1 sign was driven by intake. Good material for interpretation. |
| **D. Coefficients grow** | Larger after control | Suppression: resources had been directed to disadvantaged schools (compensatory funding), masking their association. Policy-relevant. |
| **E. Student vs school ESCS** | `SCH_ESCS` coefficient large, comparable to or larger than student `ESCS` | Who your classmates are matters as much as your own background — a composition effect. Points toward sorting and tracking, not equipment, as the bigger policy issue. |

**Caveat to state explicitly:** ESCS may be partly a *mediator*, not only a confounder. If wealthier areas fund better schools, controlling for ESCS removes some of the genuine resource effect. We therefore report RQ1 as the **unadjusted** association and RQ2 as the association **adjusted for ESCS**, and compare the two. Neither should be read as a formal bound on the true effect: with observational data, we cannot claim that.

---

## RQ3 — Do the regression and the Random Forest agree?

*Random Forest on the same predictors (+ `CNT` possibly), train/test split by `SCHOOL_GROUP_ID`, compared via permutation importance and partial dependence plots.*

| Scenario | What we would see | What it would mean |
|---|---|---|
| **A. Same ranking** | RF importance order matches the size of standardised regression coefficients | Robust finding: the relationship is roughly linear and not an artefact of the model. |
| **B. RF ranks a lever higher than OLS** | e.g. `EDUSHORT` important in RF but small in OLS | **Non-linearity or threshold:** resources may matter only when severely lacking. Check the partial dependence plot — a flat line with a drop at the high-shortage end is a policy message ("target the worst-equipped schools"). |
| **C. RF ranks a lever lower** | Significant coefficient, low importance | The linear effect is real but small relative to other variables, or importance is shared with a correlated predictor (`CLSIZE`/`STRATIO`, `EDUSHORT`/`STAFFSHORT`). |
| **D. RF dominated by ESCS / SCH_ESCS / CNT** | School levers near the bottom | Consistent with RQ2-A: background and system explain much more than the three levers. |
| **E. RF barely beats baseline** | Test R² close to predicting the mean | School-level features have limited predictive power for individual students. Not a failure — an honest result. |

**Why they can disagree for reasons that are not substantive:**
- Importance shows how much the model *uses* a variable, not the direction or the size of its effect.
- Impurity-based importance favours continuous variables with many values over coarse ones like `CLSIZE` (9 values) → use **permutation importance**.
- Regression coefficients are conditional on all other variables; RF importance is not.
- The RF uses `SENWT` or no weights and only point estimates; the regression uses replicate weights and 10 PVs. Their uncertainty is not directly comparable.

---

## RQ4 — Do countries cluster into recognisable types of school system?

*Clustering of the 14 systems on country-level features (e.g. mean levers, SD of school ESCS, ESCS slope, private share, RQ2 coefficients per country).*

| Scenario | What we would see | What it would mean |
|---|---|---|
| **A. Clusters match known typologies** | Nordic/Baltic comprehensive vs Central European early-tracking vs Southern European | Policy implications differ by system type; a single recommendation for "a minister" must say which type of system it applies to. |
| **B. Clusters follow resources, not structure** | e.g. QUR alone, then high- vs low-shortage | Resource levels differ more than institutional design within Europe. |
| **C. No clear structure** | Low silhouette, unstable clusters | With 14 points this is quite possible. Report it honestly and do not over-interpret. |
| **D. Driven by one feature** | Clusters change completely when one variable is removed | Unstable; report the sensitivity. |

**Expected grouping** (see `country_context.md`, section C): {FIN, SWE, EST, POL?} · {DEU, AUT, CZE, NLD, BEL} · {ESP, ITA, PRT, FRA} · {QUR}.

**Constraints:** exclude 100%-imputed features for a country (Austria's school type, Belgium's and Estonia's staff shortage). Standardise features before clustering. Test 2–5 clusters and report the silhouette score; with 14 countries, also show a dendrogram, which is easier to read than k-means output.

---

## What would change our conclusion (link to limitations)

- Results that hold in pooled data but **reverse within most countries** → pooling artefact (Simpson's paradox). Run per-country models as a check.
- Results that **disappear when Spain or QUR is removed** → driven by one system.
- Results that **disappear when imputed rows are dropped** → driven by imputation.
- Results that are **significant only without replicate weights** → false precision.

---

## What we actually found

*(To be filled in after the models run. For each RQ: which scenario occurred, and the explanation.)*

# Data Dictionary — PISA 2022, Project A

**Owner:** Interpretation & Limitations Lead
**Dataset described:** `data/processed/pisa_cleaned_dataset.parquet` (121,564 students, 4,347 schools, 14 education systems, 111 columns)
**Source:** OECD PISA 2022 database (cycle CY08), student file `CY08MSP_STU_QQQ` and school file `CY08MSP_SCH_QQQ`
**Status:** Draft. Codings marked *(verify)* should be checked against the official codebook (`school_meta.variable_value_labels`) before the report is submitted.

> The brief asks us to "write down, in your own words, what ten of the fields actually mean." This file does that, and adds for each field **who reported it** and **what a high value means**, because both determine how a coefficient can be read.

---

## 1. Identifiers

| Field | Level | Meaning in plain words |
|---|---|---|
| `CNT` | Country | Three-letter code of the education system. `QUR` = Ukrainian regions (18 regions tested in 2022, not the whole country). |
| `CNTSCHID` | School | School ID, unique **only together with** `CNT`. Key used to merge students with their school. |
| `SCHOOL_GROUP_ID` | School | `CNT` + `CNTSCHID` joined as text (e.g. `AUT_4000006`). Use it to split train/test **by school** in the Random Forest. |

## 2. Outcome: mathematics performance

| Field | Level | Meaning in plain words | High value means |
|---|---|---|---|
| `PV1MATH` … `PV10MATH` | Student | Ten **plausible values** of the student's maths score. Each student answers only part of the test, so PISA does not give one score but ten equally plausible draws from the range of scores the student could have. The scale is set so the OECD mean is about 500 and the SD about 100. | Higher maths proficiency |

**How to use:** run every analysis 10 times (once per PV) and combine with Rubin's rules. Averaging the 10 PVs into one column before modelling gives correct point estimates but **understates the uncertainty**. Using only PV1 is what the brief explicitly calls wrong.

**Rough scale for interpretation:** in our sample the student SD is about 91 points. A difference of ~20 points is often described as roughly half to one school year of learning, but this rule of thumb is debated, so use it carefully in the minister's recommendation.

## 3. The three policy levers (research question 1)

| Field | Policy lever | Who reported it | What it measures | High value means | Distribution in our data |
|---|---|---|---|---|---|
| `EDUSHORT` | **Equipment** | School principal | Index of how much the principal thinks a lack or poor quality of educational material (textbooks, IT equipment, library, lab material) and physical infrastructure (building, heating, classrooms) hinders instruction. Standardised so the OECD mean is 0, SD 1. | **More shortage = worse equipment** | Mean −0.26. **26% of students are at the floor (−1.42)**, i.e. principal reports no shortage at all. |
| `CLSIZE` | **Class size** | School principal | Average size of the test-language class in the modal grade for 15-year-olds, taken from size **bands**, so values are band midpoints. | Larger classes | Only 9 possible values: 13, 18, 23, 28 … 53. Median 23. |
| `PROATCE` | **Teacher training** | School principal | Proportion of all teachers at the school who are **fully certified** by the appropriate authority. | More certified teachers | Mean 0.84. **36% of students are in schools with exactly 1.0** (all certified). |

**Interpretation warnings for this block**

- **Sign of `EDUSHORT`:** a *negative* coefficient means better-equipped schools score higher. Always rephrase as "less shortage" on slides.
- **`CLSIZE` is not the maths class.** It refers to the language-of-instruction class. Band midpoints also blur within-band differences, which attenuates the coefficient.
- **`PROATCE` ≠ "better-trained".** Certification is a legal status, not a measure of quality or in-service training. With so many schools at 1.0, there is little variation left to detect an effect.
- **All three are principal perceptions** (or principal-reported counts), answered once per school. Principals in different countries may interpret "hinders instruction" differently.

## 4. Additional school factors

| Field | Who reported it | Meaning | High value means | Note |
|---|---|---|---|---|
| `STRATIO` | Principal (derived from staff and enrolment counts) | Students per teacher in the whole school | More students per teacher | Overlaps conceptually with `CLSIZE` (correlation 0.19). 9 schools report values above 40, including some at 100 — likely reporting errors; check before modelling. |
| `STAFFSHORT` | Principal | Index of how much a lack of teaching or assisting staff hinders instruction (OECD mean 0, SD 1) | More staff shortage | Directly relevant to the teacher question. **Not available at all for Belgium and Estonia** (100% imputed) — see section 7. |
| `SCHLTYPE` | Principal / national centre | School management type. *(verify)* 1 = private independent, 2 = private government-dependent, 3 = public. | — | **Categorical, not numeric.** One-hot encode it. Not available for Austria (100% imputed as public). |

## 5. Family and school background (research question 2)

| Field | Level | Meaning in plain words | High value means |
|---|---|---|---|
| `ESCS` | Student | PISA index of **economic, social and cultural status**: built from parents' highest education, parents' highest occupation, and home possessions (including books at home). OECD mean 0, SD 1. | More advantaged family background |
| `SCH_ESCS` | School | Average `ESCS` of the sampled students in the school, computed by our pipeline. Captures the **social composition of the school's intake**. | More advantaged student intake |

**Why both are needed:** student `ESCS` controls for the individual's family. `SCH_ESCS` controls for the fact that advantaged students are concentrated in certain schools, and those schools may also have better resources. Correlation between the two is 0.51.

## 6. Weights

| Field | Meaning | When to use |
|---|---|---|
| `W_FSTUWT` | Final student weight: how many 15-year-olds in the country this student represents. Corrects for unequal selection chances and non-response. | Country-level estimates (country means, per-country regressions). |
| `W_FSTURWT1` … `W_FSTURWT80` | 80 **replicate weights** (BRR with Fay's adjustment, k = 0.5). Re-running a statistic with each one and measuring the spread gives correct standard errors that account for students being clustered in schools. | Standard errors and confidence intervals for every reported estimate. Variance = 0.05 × Σ (θᵣ − θ)². |
| `SENWT` | **Senate weight**: rescaled so every country sums to the same total (1,000 in our file). Every country counts equally in pooled analyses. | Pooled (all-countries) models, so Spain (25% of rows) does not dominate. |

**Consistency rule:** the replicate weights in the file are on the `W_FSTUWT` scale. If pooled models use `SENWT`, each replicate weight must be multiplied by the same per-country factor `SENWT / W_FSTUWT`; otherwise the standard errors do not belong to the estimates.

## 7. Imputation flags

Each `*_imputed` column is 1 if the original value was missing and replaced by the pipeline, otherwise 0.

| Flag | Overall share imputed | Countries where it is a concern |
|---|---|---|
| `ESCS_imputed` | 3% | **Germany 13%** |
| `PROATCE_imputed` | 16% | **Belgium 48%**, Netherlands 30%, France 28%, Germany 23% |
| `STAFFSHORT_imputed` | 20% | **Belgium 100%, Estonia 100%** (no real data) |
| `EDUSHORT_imputed`, `CLSIZE_imputed`, `STRATIO_imputed` | 9–12% | Netherlands, France, Germany ≈ 20–23% |
| `SCHLTYPE_imputed` | 11% | **Austria 100%**, Belgium 60%, Germany 17% |
| `SCH_ESCS_imputed` | <1% | — |

**Rules for interpretation:**

1. A variable that is 100% imputed in a country carries **no information** about that country. Austria's school type, and Belgium's and Estonia's staff shortage, must be excluded from any country-level statement and from clustering features.
2. Median imputation pulls values to the middle, which **weakens associations**. Run the main regression once with flagged rows excluded as a robustness check.

## 8. Fields we do not have (and why it matters)

- **Teacher questionnaire data** (teacher qualifications, professional development hours): would measure "training" better than `PROATCE`, but only some countries ran it.
- **Reading and science scores**: we analyse maths only.
- **Prior achievement**: PISA is cross-sectional, so we cannot control for how strong students were before entering their school.
- **Spending per student**: not in PISA at school level.

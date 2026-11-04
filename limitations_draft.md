# Limitations and What Would Change Our Conclusion — Draft

**Owner:** Interpretation & Limitations Lead
**Rubric weight:** 20% ("What the analysis does not show, who is missing, what would overturn you")
**Status:** Draft v1, written before final results. Sections marked **[update after results]** need numbers from the models.

---

## 1. Association is not causation

PISA is an observational, cross-sectional survey: each student is measured once, and schools were not randomly assigned their equipment, class sizes or teachers. Our models therefore show which school factors are **associated** with higher maths scores. They cannot show what would happen if a ministry changed one of them. Yet the ministry's question ("which one actually moves results?") is causal. Every result in this report should be read as "schools that have X also tend to have higher-scoring students", not as "giving schools X raises scores".

**What would overturn us:** evidence from experiments or natural experiments. The best-known example for class size, the Tennessee STAR experiment, found positive effects of smaller classes in early grades. If our observational results contradict such evidence, the experimental evidence should carry more weight.

## 2. Reverse causality and compensatory allocation

Resources are not distributed randomly; they often follow need. Many systems deliberately place struggling or disadvantaged students in smaller classes, or give additional funding and staff to schools with weaker results. In those cases low performance **causes** small classes or extra resources, not the other way round. This can make an effective policy look useless or even harmful in the data. In our sample, more advantaged schools have slightly *larger* classes (correlation between class size and school-average ESCS: +0.13), which is consistent with this mechanism.

**[update after results]** If the class-size coefficient is positive, state that this pattern most plausibly reflects allocation, not a benefit of larger classes.

## 3. Omitted variable bias

Even after controlling for student and school socio-economic status, many factors that affect both school resources and student results are absent from our models: teaching quality, school leadership, parental involvement, prior achievement, regional spending, urban versus rural location, and the academic track a student is in. In early-tracking systems (Germany, Austria, Czechia, Netherlands, Belgium), a "school effect" may largely be a **track effect**: academic-track schools differ in both resources and student intake. Any of these can make a school factor look more or less important than it is.

## 4. Controlling for ESCS: confounder or mediator?

We control for family background (ESCS) and school intake (school-average ESCS) to separate school resources from who attends the school. But if wealthier communities fund better-equipped schools, part of the true resource effect runs *through* socio-economic status, and controlling for it removes that part as well. We therefore present RQ1 as the **unadjusted** association and RQ2 as the association **adjusted for ESCS**. Comparing the two shows how much of each school factor's association travels with family background. Neither model gives a formal bound on the true effect, because with observational data other unmeasured factors can push the estimates in either direction.

## 5. Measurement: the variables do not measure exactly what the minister asked about

| Policy lever | What we actually measure | Problem |
|---|---|---|
| School equipment | `EDUSHORT`: principal's **perception** of whether material shortages hinder instruction | Subjective; principals in different countries may judge "hindrance" differently. 26% of students are in schools at the lowest possible value, so differences among well-equipped schools are invisible. |
| Smaller classes | `CLSIZE`: average size of the **language** class, reported in 5-student bands | Not the maths class; coarse bands blur real differences, biasing the coefficient towards zero. |
| Better-trained teachers | `PROATCE`: share of **legally certified** teachers | Certification is not training quality or professional development. 36% of students are in schools where every teacher is certified, leaving little variation. A null result means "we cannot detect it with this variable", not "teachers don't matter". |

All three levers are reported by the principal once per school and are identical for every student in it. Measurement error in such variables generally pushes estimated associations towards zero.

## 6. Missing data and imputation

The pipeline replaced missing school variables with country medians and flagged each imputed value. Imputed values make school factors look more similar than they are, which can weaken real associations. Missingness is not random:

- **Germany:** 13% of students lack ESCS, far more than any other country (others: 1–5%). Missing background data is typically more common among disadvantaged students, so German results may understate inequality.
- **Belgium and Estonia:** staff shortage (`STAFFSHORT`) is entirely missing; every value is imputed.
- **Austria:** school type (`SCHLTYPE`) is entirely missing; all schools were coded as public by imputation.
- **Belgium, Netherlands, France, Germany:** 20–48% of the teacher-certification values are imputed.

Fully imputed variables are excluded from any country-specific statement and from the country clustering. **[update after results]** Report whether the main results change when imputed rows are excluded.

## 7. Who is missing: sample coverage and COVID

- **Response rates in 2022.** PISA 2022 was conducted during the COVID-19 pandemic, and the OECD notes that its data files include all participating systems, even those with low response rates. Countries that did not meet sampling standards are marked with an asterisk in OECD tables. **[verify which of our 14 are flagged — likely the Netherlands]** If schools or students who did not take part are systematically weaker (e.g. disadvantaged schools under pandemic strain), country averages are biased upward and the relationship between resources and results may be distorted.
- **Ukrainian regions.** Only 18 regions were assessed, during the war. Results do not represent Ukraine as a whole, and the conditions of testing are not comparable to other systems. We report results with and without this system.
- **Who PISA excludes by design:** 15-year-olds not enrolled in school, students in schools excluded for practical reasons, and students with certain special needs. Systems with higher exclusion rates look better than they are.
- **Only 14 European systems.** Our conclusions apply to these systems and should not be extended to Europe as a whole or to the 80+ PISA participants.

## 8. COVID as a confounder, not just a response-rate issue

School closures in 2020–21 differed between and within countries. Schools with poorer equipment may also have been less able to teach remotely, so part of any equipment association in 2022 may reflect **pandemic learning loss** rather than the normal effect of equipment. The OECD itself found no simple relationship between closure length and performance trends across systems, so the direction of this bias is uncertain.

## 9. Pooling countries and the risk of misleading averages

Students are nested in schools, which are nested in countries. A relationship in the pooled data can differ from, or even reverse, the relationship within each country (Simpson's paradox). For example, a country with both large classes and high scores (Poland) can create a positive pooled association even if smaller classes help within every country. We use senate weights so each country counts equally, and **[update after results]** compare pooled coefficients with per-country coefficients.

## 10. Statistical method choices

- **Uncertainty.** Standard errors use the 80 replicate weights and the 10 plausible values (Rubin's rules). Ignoring either would understate uncertainty and make weak associations look significant.
- **Effective sample size.** Although we have 121,564 students, the three policy levers vary only between 4,347 schools. Precision for school factors is limited accordingly.
- **Random Forest.** It is trained on point estimates and evaluated on a held-out set of schools; it does not use replicate weights or all plausible values in the same way as the regression. Its feature importances indicate predictive usefulness, not direction or causal effect, and are not directly comparable to regression coefficients.
- **Clustering.** With only 14 countries, clusters are sensitive to which features and how many clusters are chosen. We report stability checks and treat clusters as descriptive.
- **Linearity.** The regression assumes each lever has the same effect at every level. Thresholds (e.g. equipment only mattering when severely lacking) are detected only by the Random Forest.

## 11. Scope of the outcome

We analyse mathematics only. Reading and science, student well-being, and longer-term outcomes are not considered. A lever that does little for maths scores could still matter for these.

---

## What would change our conclusion — summary

| If we found… | Our conclusion would change because… |
|---|---|
| The leading lever loses significance with replicate weights | The association was false precision. |
| The result disappears when one country (Spain, QUR) is dropped | It describes one system, not a general pattern. |
| Per-country models show opposite signs from the pooled model | The pooled result is a composition effect between countries. |
| The result disappears when imputed rows are excluded | It is an artefact of imputation. |
| Experimental evidence points the other way | Causal evidence outweighs observational association. |
| Teacher-questionnaire measures of training tell a different story than `PROATCE` | Certification was the wrong proxy for "better-trained teachers". |

---

## Implication for the minister's recommendation

The recommendation must use the language of association ("is linked to", "schools that… tend to…"), state which type of system it applies to, and name one concrete next step that would provide causal evidence (for example, a pilot with random or staggered allocation of the chosen investment, evaluated against comparable schools).

---

### Sources to cite
- OECD (2023), *PISA 2022 Results (Volume I)*, Reader's Guide and Annexes A2, A4 — sampling standards and flagged countries.
- OECD (2023), *PISA 2022 Results (Volume II): Learning During – and From – Disruption* — school closures and resources.
- OECD (2024), *PISA 2022 Technical Report* — weights, replicate weights, plausible values.
- OECD, *PISA Data Analysis Manual* — variance estimation with BRR and plausible values.
- Krueger, A. (1999), "Experimental Estimates of Education Production Functions", *Quarterly Journal of Economics* — Tennessee STAR class-size experiment.

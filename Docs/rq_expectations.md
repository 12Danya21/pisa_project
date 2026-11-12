# Initial hypotheses and what was actually found

The exact pre-result 14-system hypotheses are preserved in `history/pre_fix_49e71c4/Docs/rq_expectations.md`. They are not rewritten as though the results were known in advance. This current document records how the executed seven-system analysis differs from that plan.

| Historical idea | Executed analysis and interpretation |
|---|---|
| Less shortage may be associated with higher scores | Negative RQ1 coefficient, attenuated after ESCS; not significant in main RQ2 and changes sign in RQ2b. Not a stable causal spending effect. |
| Positive class-size coefficient may reflect selection | Positive in RQ1/RQ2, much smaller and not significant at 5% in RQ2b. Compatible with intake confounding; does not prove allocation mechanism. |
| Certification may be weak because it is an imperfect proxy | Small/imprecise pooled associations. It measures legal certification, not teacher-development quality. |
| Background adjustment may attenuate resource associations | RQ2 adds student ESCS; RQ2b separately adds school ESCS. An ESCS-imputation flag was planned historically but is not a predictor in the executed main model; a complete-case sensitivity is supplied instead. |
| RF and regression may prioritize background | Both prioritize school and student ESCS among numerical predictors under held-out permutation importance. RF need not win prediction; LR wins the tested comparisons. |
| Fourteen systems may resemble institutional types | Actual common scope is seven. Revised clustering uses resource/background means, with k=2 isolating QUR. Historical institutional group expectations are not established by this result. |

RQ1 contains country fixed effects even though the early plan described only policy terms. Main pooled weighting is equal-country; LR/RF also use country indicators. All ten PVs are fitted separately. Additional STRATIO/STAFFSHORT/SCHLTYPE models and partial-dependence plots were exploratory ideas, not compulsory course deliverables; they are not claimed as completed. No nonlinear threshold is claimed, so a threshold illustration is unnecessary to substantiate the current findings.

See `RESULTS_GUIDE.md` for numerical results and `limitations_draft.md` for what would change the interpretation. Identical importance rankings would not prove linearity, and mismatched rankings do not prove nonlinear policy thresholds.

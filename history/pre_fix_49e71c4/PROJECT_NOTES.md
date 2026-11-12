# Project A — PISA 2022 team notes

## Work in chronological order

| Date | Contribution and evidence |
|---|---|
| 18 Oct 2026 | 12Danya21 created the repository (b197a25). |
| 21 Oct | Danylo committed the student–school merge and data engineering pipeline (0a37bdc, 7bb9fe4). |
| 25 Oct | Danredko recorded the policy question, four research questions, seven target systems and plans for interpretation with Alex (db54a52). |
| 29–31 Oct | 12Danya21 uploaded revised exploration and pipeline notebooks and organised them under notebooks/ (bca7844, 16b7fd3, 2595d6b). The pipeline selects OECD 2022 student and school records, calculates school-average ESCS, flags and fills missing values, checks the many-to-one school merge and retains ten maths plausible values, final weights and 80 replicate weights. It also creates equal-country senate weights. The processed file contains 121,564 students, 4,347 schools and 111 columns across 14 systems. |
| 3–4 Nov | alexco-ro-nel organised the documentation and uploaded the data dictionary, country context, research expectations and limitations draft under Docs/ (8ae7f80 through b906665). These documents record initial hypotheses and measurement concerns. |
| Available by 11 Nov | The team supplied the cleaned Parquet, executed ML/clustering notebook and results archive. The notebook restricts the analysis to Germany, France, Poland, Estonia, Italy, Spain and the Ukrainian regions surveyed (18 of 27). Its individual author and completion date still need team confirmation. |
| 11 Nov | At the user's request, Codex inspected the files, reproduced the predictive and clustering results from the supplied Parquet and ran the additional checks below. The raw SAS pipeline was inspected. The independent rerun starts at the processed data. |

Git names identify the accounts that committed files. Before signing the work distribution statement, each member should confirm their full name, analytical contribution and how the group coordinated the handoffs.

## What the analysis found

**RQ1 and RQ2.** Awaiting the team's regression files. Compare associations for educational shortages (EDUSHORT), class size (CLSIZE) and teacher certification (PROATCE) before and after adjustment for student and school ESCS. Record the actual sample, weights, PV pooling and uncertainty method on receipt. The policy recommendation is pending.

**RQ3.** The original five predictors were CLSIZE, EDUSHORT, STAFFSHORT, SCH_ESCS and ESCS. The models trained on 56,029 students and tested on 14,488, with zero schools shared across sets. Both used W_FSTUWT and ten separate maths PV fits. Linear regression achieved mean MAE 60.88 and R² 0.2783. Random Forest achieved 62.49 and 0.2381. School and student ESCS ranked first and second in both models. RF importance has no sign and cannot measure the return on investment.

**RQ4.** K-means used four standardised country means weighted by student weights. Among k = 2, 3 and 4, k = 2 had the highest silhouette (0.3161) and isolated the Ukrainian regions. At k = 3 the original groups were DEU/EST/ITA, ESP/FRA/POL and QUR.

**Follow-up checks.** In Estonia every STAFFSHORT value was imputed. Removing it for all seven systems barely changed linear regression (MAE 60.87, R² 0.2787). RF reached MAE 62.98 and the training-mean baseline 72.82. Linear regression had lower MAE than RF in each system on the original split. Two additional school splits were checked for linear regression. Without STAFFSHORT, k = 2 retained the same country groups (silhouette 0.4127), while Spain moved into the DEU/EST/ITA group at k = 3. Use the grouping as exploratory. See results/checks/ for the country, PV and split details.

**Scope.** The pooled ML estimates use population weights. SENWT and replicate-weight standard errors are available options for further work. No design-based confidence intervals were calculated for RQ3. Preprocessing preceded the school split. Zero remaining missing values reflects imputation. The data measure associations and contain no investment costs.

## Submission checklist from the supplied course slides

The slides are titled FDA Hackathon. Confirm that this format applies to the PISA assignment.

- One group submission by email, due 5 December 2026 at 1 pm according to the slides.
- Submit the paper in Word and PDF, plus a separate .ipynb or .py file. Integrate RQ1–RQ2 into the submission code when received.
- Main text 2,250–2,750 words. Cover data collection, data analysis, results and interpretation. Place figures and tables within the relevant text.
- Times New Roman 12 pt, double spacing, justified paragraphs, APA 7 citations and references.
- Appendix excluded from main word count. Include a 315–385 word reflection on actual AI use, benefits and limitations. The documented AI assistance covered file review, reproducibility checks, sensitivity analysis and documentation. Team members should add their own usage.
- Include the work distribution and collaboration statement, signed by every member. The chronological log above is supporting evidence.

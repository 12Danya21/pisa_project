# Changes, provenance and rollback

## Baseline and branch

Reviewed upstream baseline: `49e71c400222f3f8e2d01f2492a11dfcb1af1ea2` (12 November 2026).
Correction branch: `fixes/pisa-consistency-2026-11-12`.

The original processed Parquet is unchanged. Its hash is in data/DATA_MANIFEST.json. Historical notebooks, Docs, exports/checks, README and PROJECT_NOTES are exact copies under `history/pre_fix_49e71c4/`, with SHA256.json. The received RQ1/RQ2 notebook is also retained there. These copies include historical mistakes solely to explain/undo the revision; they are not the active checklist or results.

## What changed and why

| Area | Original | Current | Consequence |
|---|---|---|---|
| Assignment | Hackathon submission checklist | Data Analytics briefing checklist; user-supplied presentation date | No invented word counts, format mandates or December deadline |
| RQ1/RQ2 | Received outside repo | Integrated, executed, common paths/pyarrow, full sensitivity exports | Numerical estimates are preserved; misleading summary statements corrected |
| Qualification | STAFFSHORT in RQ3, no certification | PROATCE_10PP; STAFFSHORT excluded | Now tests the requested teacher-certification proxy |
| Model alignment | Population weights, no country controls | Main equal-country weights, country indicators, with/without SCH_ESCS | Matches RQ2b/RQ2 specification families; does not make predictive coefficients identical to full-sample inference |
| Test preprocessing | Imputation before split | Restore flags; train-only medians, school ESCS based on own observed intake | Avoids using test schools to learn imputation rules |
| Predictive evaluation | One RF school split; impurity importance | LR and RF on three shared splits, ten PVs; two baselines; held-out weighted permutation importance | Supports a qualified predictive comparison, not causal importance or universal model superiority |
| RQ4 | Imputed EST staff shortage; export k=3 despite higher k=2 silhouette | No STAFFSHORT; qualification included; observed-only means; best silhouette k plus sensitivities | New profiles answer a different, documented descriptive specification |
| Explanations | Mostly 14-system hypotheses | Seven-system current context/results and explicit limitations | Initial expectations preserved as historical hypotheses |
| Outputs | Single old output set | history/ vs results/revised/ with manifests | Old results remain accessible and cannot be mistaken for current results |
| Raw pipeline | Machine-specific folder layout; overwrite risk | data/raw/ filenames; refuse overwrite of reviewed Parquet | Raw rebuild remains unexecuted because raw files were not supplied |

Changing variables, weights, preprocessing and controls together means the difference in old/new metrics cannot be attributed to one modification. In particular, population-weighted MAE and equal-country MAE describe different target populations; a lower number across those targets is not a measured improvement. Compare LR and RF within the same current variant/split, and use the population sensitivity explicitly.

## Safe rollback options

1. **Inspect originals without undoing anything:** open `history/pre_fix_49e71c4/`. Validation verifies every snapshot hash.
2. **Switch to a separate old checkout:** from a Git clone, `git worktree add ../pisa_before_fixes 49e71c4`. This leaves the corrected checkout intact. Copy the unchanged reviewed Parquet into the old checkout only if needed.
3. **Undo the correction commit on the correction branch:** after saving any later work, `git revert <correction_commit>`. Obtain the commit identifier from `git log --oneline`. This creates a visible reversal rather than rewriting history. Do not use reset --hard or force-push.
4. **ZIP recipient:** retain the complete review package, its history folder and manifest. To return to historical presentation of results, inspect the snapshots; do not overwrite revised exports. The companion Git bundle provides the commit history when available.

No original data were deleted and no force-push or main-branch overwrite is part of this workflow. A final report or slide deck has not been produced.

## Verification performed

- Sequential RQ1/RQ2 rerun; primary estimates and standard errors reproduce the received notebook.
- Historical file hashes and unchanged processed-data hash checked.
- School-isolated splits, consistent feature schema, equal-country weighting, train-only imputation invariance, school-level constancy and finite metrics checked.
- Revised RQ3 executes ten distinct PV fits per model/specification/split; current results record runtime and library versions.
- RQ4 exports observed/prepared and without-QUR/leave-feature/seed/Ward sensitivities; no claims of survey-bootstrap stability.
- Raw SAS reconstruction is not claimed; participants’ earlier AI prompts/configuration remain incompletely known.

## Follow-up cleanup and report draft

At the user’s request, a separate follow-up commit removes the obsolete active exploration notebook (its original remains in the historical snapshot), moves old-model checking code to history/legacy_tools/, removes the redundant requirements alias, eliminates three duplicate CSV aliases and renames the population-weight CSV consistently. RQ1/RQ2 exports were regenerated; its estimates remain unchanged. The initial report, contribution account and project lead’s presentation segment are now included. The original correction commit remains available for rollback of this cleanup without undoing the statistical corrections.

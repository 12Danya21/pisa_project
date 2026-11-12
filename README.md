# PISA 2022 — school characteristics and mathematics

Seven-system analysis: Germany, Estonia, Spain, France, Italy, Poland and the Ukrainian regions surveyed in PISA 2022. The question is which resource associations remain after socioeconomic adjustment, and whether linear and nonlinear models agree. These observational analyses do not identify investment returns.

## Current results and provenance

- `notebooks/RQ1_RQ2.ipynb`: executed survey regression, ten PVs and 80 Fay-BRR replicates per system. RQ2b adds school intake.
- `notebooks/PISA_2022_Final_ML_Clustering.ipynb`: revised RQ3/RQ4 entry point.
- `results/revised/`: current outputs only, with run manifests.
- `Docs/RESULTS_GUIDE.md`: explanations, old/new differences and limits of interpretation.
- `Docs/CHANGELOG_AND_ROLLBACK.md`: change inventory and rollback instructions.
- `history/pre_fix_49e71c4/`: exact pre-fix files, received RQ1/RQ2 and SHA-256 inventory. Historical material is not the current submission specification.

## Reproduce from the reviewed processed data

Use Python 3.12.4 to match the measured environment; numerical library versions are pinned below.

```sh
python -m pip install -r requirements.txt
python scripts/reproduce.py
```

Place the team's unchanged Parquet in `data/processed/pisa_cleaned_dataset.parquet`. The review package includes that file; Git excludes it. Its exact hash, source, dimensions and access instructions are in `data/DATA_MANIFEST.json`. Runners reject a different version to prevent silently mixed samples. A recipient without the package must obtain the reviewed file from the team, or rebuild and explicitly review/register the new hash; no public processed-data download URL has been invented.

For a partial rerun, execute the relevant script, then `python scripts/finalize_outputs.py` and `python scripts/validate_revision.py` to refresh/check the output inventory.

Both analytical notebooks may be run from the repository root or `notebooks/`. The revised ML notebook invokes the same script, so there is one implementation. RF settings are fixed at 100 trees and minimum leaf size 5, inherited from the original analysis; there is no tuning on the test data. Both LR and RF use seeds 42, 7 and 2026, ten separate PV fits and school-isolated tests. Population-weight sensitivity uses seed 42. Baselines are overall and country training means. Predictive metrics have no design-based confidence intervals; variation across PVs/permutations/splits is descriptive.

The main RQ3 includes EDUSHORT, CLSIZE, PROATCE_10PP, ESCS, SCH_ESCS and country indicators, with equal country weight separately in training and testing. Train-only medians replace flagged missing values. School ESCS uses observed background in that school, so prediction assumes that intake information is available. RQ4 uses observed-only weighted country means of EDUSHORT, CLSIZE, PROATCE_10PP and ESCS; coverage and leave-feature-out sensitivities are exported. It is exploratory, not a validated typology.

## Rebuild from OECD files

Download the PISA 2022 student and school SAS datasets from the [official OECD database](https://www.oecd.org/en/data/datasets/pisa-2022-database.html). Extract `CY08MSP_SCH_QQQ.SAS7BDAT` and `CY08MSP_STU_QQQ.SAS7BDAT` to `data/raw/` and run `notebooks/Data Engineering & Pipeline Lead_FINAL (3).ipynb`. The pipeline retains 14 systems and exports the processed Parquet; each analysis selects the agreed seven. Raw files were not available for this revision, so a raw rebuild and identity with the reviewed hash are not claimed. Do not overwrite the reviewed file without retaining its copy and provenance.

Initial exploration is retained only in `history/pre_fix_49e71c4/notebooks/01_initial_exploration.ipynb`. Old-model checks are in `history/legacy_tools/run_checks.py`; neither is part of the current reproduction route. Redundant CSV aliases and the old requirements alias have been removed. Use `requirements.txt` and the canonical results under `results/revised/`.

## Submission scope

See `PROJECT_NOTES.md` for the Data Analytics briefing checklist, team roles and dates. An initial report with the four-sentence recommendation is in `report/PISA_report_draft.md`; the editable Word copy is distributed in the review package. Slides remain to be assembled. Team contributions and the project lead’s integration role are documented in `Docs/TEAM_CONTRIBUTIONS.md`. Hackathon formatting/deadline rules do not apply to this project.

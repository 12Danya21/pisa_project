# PISA 2022 — school characteristics and mathematics

Read [the team log](PROJECT_NOTES.md) for contributions, findings and submission requirements. RQ3–RQ4 are available. RQ1–RQ2 are pending.

1. Start from the team's cleaned Parquet. Place it at `data/processed/pisa_cleaned_dataset.parquet` (remove the download suffix `(1)`). To rebuild from OECD PISA 2022 SAS data, use the school and student paths specified in the first cell of the data engineering notebook under `notebooks/`. The raw pipeline requires pyreadstat.
2. Install the numerical libraries with `python -m pip install -r requirements-checks.txt`. For notebooks also install Jupyter, matplotlib and seaborn.
3. Run `notebooks/PISA_2022_Final_ML_Clustering.ipynb` from the repository root or notebooks directory. Its exports appear in the working directory. The original team exports are in `results/`.
4. Reproduce the sensitivity tables from the repository root with `python scripts/run_checks.py data/processed/pisa_cleaned_dataset.parquet --output reproduced_checks`. Compare with `results/checks/`.

The final notebook uses seven systems from the 14-system preparation file. The original exports include STAFFSHORT. Use the sensitivity tables when interpreting the fully imputed Estonian values. Historical expectations under Docs/ describe planned analyses. PROJECT_NOTES records the methods actually run.

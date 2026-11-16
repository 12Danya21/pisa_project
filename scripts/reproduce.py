"""One-command reproduction from the reviewed processed dataset."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[1]
commands=[['run_regression.py'],['revised_analysis.py','data/processed/pisa_cleaned_dataset.parquet','--output','results/revised'],['country_summary.py'],['finalize_outputs.py'],['validate_revision.py']]
for script,*args in commands:
    subprocess.run([sys.executable,str(r/'scripts'/script),*args],cwd=r,check=True)

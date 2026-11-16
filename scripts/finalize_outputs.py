"""Refresh source provenance and output checksums after a full or partial rerun."""
from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[1];o=r/'results/revised'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=o/'run_manifest.json'
if p.exists():
    d=json.loads(p.read_text());d['source_scripts_sha256']={str(f.relative_to(r)):sha(f) for f in sorted((r/'scripts').glob('*.py'))}
    d['model_fit_count']={'LinearRegression':10*(2*len(d['seeds'])+1),'RandomForest':10*(2*len(d['seeds'])+1)}
    p.write_text(json.dumps(d,indent=2)+'\n')
files={str(f.relative_to(r)):sha(f) for f in sorted(o.rglob('*')) if f.is_file() and f.name!='OUTPUT_SHA256.json'}
(o/'OUTPUT_SHA256.json').write_text(json.dumps(files,indent=2)+'\n')
print('Refreshed provenance and output checksums.')

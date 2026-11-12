"""Run the RQ1/RQ2 notebook sequentially and retain executed outputs."""
from pathlib import Path
import contextlib,io,json,os,hashlib,time
import pandas as pd
import matplotlib
matplotlib.use('Agg')

def main():
    root=Path(__file__).resolve().parents[1]
    dataset=root/'data/processed/pisa_cleaned_dataset.parquet'
    expected='2d1638ff15ba1a1dce592f0d5f67d6abc329e9e7155f4c6de340d615d8fb3bfb'
    assert hashlib.sha256(dataset.read_bytes()).hexdigest()==expected, 'Dataset differs from reviewed version'
    os.chdir(root)
    path=root/'notebooks/RQ1_RQ2.ipynb';nb=json.loads(path.read_text());ns={'__name__':'__main__'}
    t=time.perf_counter();counter=0
    for c in nb['cells']:
        if c['cell_type']!='code':continue
        counter+=1; captured=[];stream=io.StringIO()
        def display(value):
            if isinstance(value,(pd.DataFrame,pd.Series)):
                captured.append({'output_type':'display_data','metadata':{},'data':{'text/plain':[value.to_string()], 'text/html':[value.to_frame().to_html() if isinstance(value,pd.Series) else value.to_html()]}})
            else:print(value)
        ns['display']=display
        with contextlib.redirect_stdout(stream):exec(''.join(c['source']),ns)
        c['execution_count']=counter
        c['outputs']=([{'output_type':'stream','name':'stdout','text':stream.getvalue().splitlines(keepends=True)}] if stream.getvalue() else [])+captured
    path.write_text(json.dumps(nb,indent=1,ensure_ascii=False)+'\n')
    out=root/'results/revised/RQ1_RQ2'
    (out/'run_manifest.json').write_text(json.dumps({'dataset_sha256':expected,'elapsed_seconds':round(time.perf_counter()-t,2),'execution':'All notebook code cells sequentially; figures exported as PNG; stdout and tables retained in executed notebook.','uncertainty':'80 Fay-BRR replicates per independent system; ten PVs, sampling variance + (1+1/10)*between-PV variance; normal intervals.'},indent=2)+'\n')
    print('Executed RQ1/RQ2 and exported all sensitivities.',flush=True)

if __name__=='__main__':main()

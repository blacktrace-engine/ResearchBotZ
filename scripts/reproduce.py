"""Verify source bytes, run both audits, compare all frozen result artifacts."""
import gzip
import hashlib
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]

def verify(directory,sums):
    for line in sums.read_text().splitlines():
        if not line.strip():continue
        expected,name=line.split(None,1)
        name=name.lstrip('*')
        path=directory/name
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=expected:raise RuntimeError('SHA256 mismatch: '+str(path))

def run(*args):
    subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,check=True)

def compare(bundle,output):
    checked=0
    with ZipFile(bundle) as z:
        for name in z.namelist():
            if not name.startswith('results/') or name.endswith('/'):continue
            actual=output/name.removeprefix('results/')
            if actual.read_bytes()!=z.read(name):raise RuntimeError('Frozen result mismatch: '+str(actual))
            checked+=1
    print(f'PASS: {checked} frozen result files match {bundle.name}',flush=True)

def main():
    verify(ROOT,ROOT/'SHA256SUMS')
    work=ROOT/'.work';corpus=work/'corpus';corpus.mkdir(parents=True,exist_ok=True)
    for p in sorted((ROOT/'data').glob('*.gz')):
        (corpus/p.name.removesuffix('.gz')).write_bytes(gzip.decompress(p.read_bytes()))
    verify(corpus,ROOT/'data/SHA256SUMS')
    print('PASS: repository artifacts and five expanded source checksums',flush=True)
    run('audits/functional/test_grouping.py')
    run('audits/write-states/test_states.py')
    run('audits/functional/analyze.py',corpus,work/'functional')
    run('audits/write-states/analyze_states.py',corpus,work/'functional/introductions.jsonl',work/'write-states')
    compare(ROOT/'bundles/functional-retry-audit.zip',work/'functional')
    compare(ROOT/'bundles/county-write-state-audit.zip',work/'write-states')
    print('PASS: complete offline reproduction',flush=True)

if __name__=='__main__':main()

"""Create a curated Git publication manifest; never package private reading copies."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'task3/screening559'
SKIP_SUFFIXES={'.log','.aux','.out','.toc','.bbl','.blg','.ndjson','.png','.pyc'}
ALLOWED_BINARY={'integrated_report/main.pdf','integrated_report/figures/Frozen_PRISMA.pdf','integrated_workbook/CEP_Task3_Working_Integrated_2026-10-23.xlsx'}
paths=[]
for p in sorted(D.rglob('*')):
    if not p.is_file() or p.is_symlink():continue
    rel=p.relative_to(D)
    if any(part in {'__pycache__','previews'} for part in rel.parts):continue
    if p.suffix in SKIP_SUFFIXES or p.name in {'PUBLICATION_MANIFEST.json','integrated_workbook_data.json'}:continue
    if p.suffix in {'.pdf','.xlsx'} and rel.as_posix() not in ALLOWED_BINARY:continue
    if p.suffix not in {'.md','.csv','.json','.py','.mjs','.tex','.bib','.pdf','.xlsx'}:continue
    paths.append(p)
for name in ['STATUS.md','FULL_TEXT_ACCESS_AND_NEXT_STEPS.md']:
    p=ROOT/name
    if p.exists():paths.append(p)
def entry(p):
    b=p.read_bytes()
    return {'bytes':len(b),'git_blob_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b,usedforsecurity=False).hexdigest()}
manifest={p.relative_to(ROOT).as_posix():entry(p) for p in paths}
(D/'PUBLICATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'files':len(manifest),'total_bytes':sum(x['bytes'] for x in manifest.values()),'licensed_primary_pdfs_included':False}))

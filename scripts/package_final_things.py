from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];F=R/'final things'
files=[p for p in F.rglob('*') if p.is_file() and not p.name.endswith('.inspect.ndjson') and p.name!='FILE_MANIFEST.json']
manifest={str(p.relative_to(F)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(files)}
(F/'FILE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(R/'GroupB_Final_Things.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[F/'FILE_MANIFEST.json']:z.write(p,'GroupB_Final_Things/'+str(p.relative_to(F)))
with zipfile.ZipFile(R/'GroupB_LaTeX_Report.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in (F/'02_Report_LaTeX').iterdir():
  if p.is_file():z.write(p,p.name)
for n in ['GroupB_Final_Things.zip','GroupB_LaTeX_Report.zip']:
 with zipfile.ZipFile(R/n) as z:assert z.testzip() is None
with zipfile.ZipFile(R/'GroupB_Final_Things.zip') as z:
 for name,v in manifest.items():assert hashlib.sha256(z.read('GroupB_Final_Things/'+name)).hexdigest()==v['sha256']
print('Full package files',len(files)+1,'all hashes PASS; LaTeX ZIP PASS')

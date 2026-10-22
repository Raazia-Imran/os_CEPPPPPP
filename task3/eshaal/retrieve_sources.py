from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import json,urllib.request,hashlib,fitz
root=Path(__file__).resolve().parents[1];out=Path(__file__).parent
ids=['P001','P002','P003','P004','P005','P006','P007','P023']
old=json.loads((root/'papers/retrieval.json').read_text());items=[x for x in old if x['report_id'] in ids]
def run(x):
 pid=x['report_id'];url=x.get('alternate_url',x['source_url']);now=datetime.now(timezone.utc).isoformat();row={'Report ID':pid,'URL':url,'Attempt UTC':now}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r:b=r.read()
  if not b.startswith(b'%PDF'):raise ValueError('Not a PDF')
  pdf=fitz.open(stream=b,filetype='pdf');f=root/'papers'/(pid+'.pdf');f.write_bytes(b)
  f.with_suffix('.txt').write_text('\n'.join('[PDF PAGE '+str(i+1)+']\n'+p.get_text() for i,p in enumerate(pdf)))
  row.update(status='PDF retrieved; pending source reading',pages=len(pdf),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),title_page=pdf[0].get_text()[:500])
 except Exception as e:row.update(status='Not retrieved',error=str(e))
 return row
with ThreadPoolExecutor(max_workers=8) as ex:r=list(ex.map(run,items))
(out/'retrieval_receipt.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

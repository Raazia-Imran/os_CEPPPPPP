from pathlib import Path
import json,csv,datetime,hashlib,subprocess,concurrent.futures
from zoneinfo import ZoneInfo
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'papers/manifest.json').read_text())
urls={'P001':'https://link.springer.com/content/pdf/10.1007/s11390-024-3773-5.pdf','P002':'https://arxiv.org/pdf/2201.08019','P018':'https://www.sciencedirect.com/science/article/pii/S0167739X23003187/pdfft','P019':'https://link.springer.com/content/pdf/10.1007/s42514-023-00154-y.pdf','P020':'https://link.springer.com/content/pdf/10.1007/s10586-025-05284-2.pdf','P023':'https://dl.acm.org/doi/pdf/10.1145/3768622'}
# P002 alternate is not established: retain publisher route until a matching manuscript is found.
urls['P002']='https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10018218'
def fetch(d):
 d=d.copy(); url=urls.get(d['report_id'],d['source_url']); p=root/'papers'/(d['report_id']+'.pdf'); t=datetime.datetime.now(datetime.timezone.utc)
 c=subprocess.run(['curl','-L','--max-time','50','--retry','1','-sS','-o',str(p),url],capture_output=True,text=True)
 valid=p.exists() and p.read_bytes().startswith(b'%PDF-')
 d.update(attempted_url=url,retrieved_utc=t.isoformat(),retrieved_pkt=t.astimezone(ZoneInfo('Asia/Karachi')).isoformat(),status='downloaded_pending_identity_check' if valid else 'not_retrieved',filename=p.name if valid else '',sha256=hashlib.sha256(p.read_bytes()).hexdigest() if valid else '',bytes=p.stat().st_size if valid else 0,note=c.stderr[:300])
 if valid:
  subprocess.run(['pdftotext',str(p),str(p.with_suffix('.txt'))],capture_output=True)
  print(d['report_id'],'PDF',flush=True)
 else:
  if p.exists(): p.unlink()
  print(d['report_id'],'not retrieved',flush=True)
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: results=list(ex.map(fetch,items))
(root/'papers/retrieval.json').write_text(json.dumps(results,indent=2))
with (root/'papers/retrieval.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)

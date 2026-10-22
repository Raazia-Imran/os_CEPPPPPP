"""Retrieve public author/publisher copies; never commit full texts or credentials."""
from pathlib import Path
import urllib.request, hashlib, json, datetime, concurrent.futures
import fitz
ROOT=Path(__file__).resolve().parents[1]
READING=ROOT/'papers'; READING.mkdir(exist_ok=True)
URLS={
 'P015':'https://www.usenix.org/system/files/osdi25-shen-weihang.pdf',
 'P018':'https://www.sciencedirect.com/science/article/pii/S0167739X23003187/pdfft',
 'P019':'https://link.springer.com/content/pdf/10.1007/s42514-023-00154-y.pdf',
 'P020':'https://link.springer.com/content/pdf/10.1007/s10586-025-05284-2.pdf',
 'P021':'https://danielwong.org/files/KRISP-HPCA2023.pdf',
 'P022':'https://arxiv.org/pdf/2410.07381v2',
 'RV01':'https://arxiv.org/pdf/2203.09040',
 'RV02':'https://www.cs.newpaltz.edu/~lik/publications/Jiahua-Huang-ACM-CSUR-2025',
 'RV03':'https://hal.science/hal-05429292v1/document',
}
def one(item):
 key,url=item; row={'report_id':key,'url':url,'attempt_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (academic source verification)'})
  with urllib.request.urlopen(req,timeout=40) as r: data=r.read(); row.update(http_status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
  row.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
  if not data.startswith(b'%PDF'): raise ValueError('Response is not a PDF')
  doc=fitz.open(stream=data,filetype='pdf'); text='\n'.join(p.get_text() for p in doc)
  if len(text)<1000: raise ValueError('Insufficient extractable text')
  (READING/(key+'.pdf')).write_bytes(data); (READING/(key+'.txt')).write_text(text)
  row.update(status='retrieved_pdf',pages=len(doc),text_chars=len(text))
 except Exception as e:row.update(status='unavailable',error=str(e))
 return row
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(one,URLS.items()))
 (Path(__file__).parent/'retrieval_attempts.json').write_text(json.dumps(rows,indent=2))
 print(json.dumps(rows,indent=2))

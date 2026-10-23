"""Secondary discovery metadata only; verify primary text before eligibility/extraction."""
from pathlib import Path
import csv,json,urllib.request,urllib.parse,datetime,hashlib,concurrent.futures,re
d=Path(__file__).resolve().parent;cache=Path('/workspace/scratch/8d52181bc639/research_metadata/openalex');cache.mkdir(parents=True,exist_ok=True)
q=[x for x in csv.DictReader((d/'Working_559_Queue.csv').open(newline='')) if not x['Recovered abstract']]
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
def fetch(url,name):
 req=urllib.request.Request(url,headers={'User-Agent':'CEP-SLR-metadata-audit/1.0'})
 with urllib.request.urlopen(req,timeout=25) as r:b=r.read();status=r.status
 (cache/name).write_bytes(b);return json.loads(b),hashlib.sha256(b).hexdigest(),status
def abstract(m):
 ix=m.get('abstract_inverted_index') or {};pairs=[(i,word) for word,positions in ix.items() for i in positions]
 return ' '.join(word for i,word in sorted(pairs))
def row(x,m,url,sha,status):
 title=m.get('title') or '';doi=(m.get('doi') or '').removeprefix('https://doi.org/');same=norm(title)==norm(x['Title']);match=not x['DOI'] or doi.lower()==x['DOI'].lower();txt=abstract(m)
 return {'Record ID':x['Record ID'],'Frozen DOI':x['DOI'],'Frozen title':x['Title'],'Metadata DOI':doi,'Metadata title':title,'Source URL':url,'OpenAlex ID':m.get('id',''),'Publication date':m.get('publication_date',''),'Type':m.get('type',''),'Identity match':'Exact normalized title and DOI where supplied' if same and match else 'Needs manual verification','Recovered abstract text':txt if same and match else '','Abstract available but not imported':bool(txt) and not(same and match),'Evidence SHA256':sha,'HTTP status':status,'Checked UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Status':'Recovered; individual reading pending' if txt and same and match else ('No indexed abstract' if same and match else 'No verified exact identity'),'Evidence role':'Secondary discovery metadata; primary text required for eligibility and extraction'}
def bulk(xs,k):
 url='https://api.openalex.org/works?'+urllib.parse.urlencode({'filter':'doi:'+'|'.join('https://doi.org/'+x['DOI'] for x in xs),'per-page':50})
 try:
  data,sha,status=fetch(url,f'batch_{k:03}.json');lookup={(m.get('doi') or '').removeprefix('https://doi.org/').lower():m for m in data.get('results',[])}
  return [row(x,lookup.get(x['DOI'].lower(),{}),url,sha,status) for x in xs]
 except Exception as e:return [row(x,{},url,'',str(e)[:120]) for x in xs]
def title(x):
 url='https://api.openalex.org/works?'+urllib.parse.urlencode({'search':x['Title'],'per-page':5})
 try:
  data,sha,status=fetch(url,x['Record ID']+'.json');m=next((m for m in data.get('results',[]) if norm(m.get('title') or '')==norm(x['Title'])),{})
  return row(x,m,url,sha,status)
 except Exception as e:return row(x,{},url,'',str(e)[:120])
withdoi=[x for x in q if x['DOI']];without=[x for x in q if not x['DOI']];chunks=[withdoi[i:i+25] for i in range(0,len(withdoi),25)];rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 fs=[pool.submit(bulk,xs,k) for k,xs in enumerate(chunks)]
 for future in concurrent.futures.as_completed(fs):rows.extend(future.result());print('DOI records checked',len(rows),flush=True)
 for result in pool.map(title,without):rows.append(result)
rows.sort(key=lambda x:x['Record ID'])
with (d/'OpenAlex_Metadata_Recovery.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'checked_records':len(rows),'abstracts_identity_matched':sum(bool(x['Recovered abstract text']) for x in rows),'individual_reading_pending':True,'frozen_queue_changed':False,'source_role':'Secondary metadata for discovery; primary verification remains required.'}
(d/'openalex_recovery_progress.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)

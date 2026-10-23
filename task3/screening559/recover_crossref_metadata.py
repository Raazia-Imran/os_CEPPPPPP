"""Recover publisher-deposited metadata; no eligibility or human decisions are changed."""
from pathlib import Path
import csv,json,urllib.request,urllib.parse,datetime,hashlib,concurrent.futures,re,html,time
d=Path(__file__).resolve().parent
cache=Path('/workspace/scratch/8d52181bc639/research_metadata/crossref');cache.mkdir(parents=True,exist_ok=True)
q=list(csv.DictReader((d/'Working_559_Queue.csv').open(newline='')))
todo=[x for x in q if not x['Recovered abstract'] and x['DOI']]
def get(x):
 doi=x['DOI'].strip();url='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')
 row={'Record ID':x['Record ID'],'Requested DOI':doi,'URL':url,'Checked UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'HTTP status':'','Metadata DOI':'','Metadata title':'','Title match':'','Recovered abstract text':'','Published date':'','Evidence SHA256':'','Result':'','Cache file':''}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'CEP-SLR-metadata-audit/1.0 (academic record verification)'})
  with urllib.request.urlopen(req,timeout=20) as r:b=r.read();row['HTTP status']=r.status
  m=json.loads(b)['message'];p=cache/(x['Record ID']+'.json');p.write_bytes(b)
  row.update({'Metadata DOI':m.get('DOI',''),'Metadata title':' '.join(m.get('title',[])),'Evidence SHA256':hashlib.sha256(b).hexdigest(),'Cache file':str(p)})
  norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
  same_doi=m.get('DOI','').lower()==doi.lower();same_title=norm(row['Metadata title'])==norm(x['Title'])
  row['Title match']='Exact normalized' if same_title else 'Needs manual identity check'
  raw=m.get('abstract','');txt=html.unescape(re.sub('<[^>]+>',' ',raw));txt=re.sub(r'\s+',' ',txt).strip()
  if same_doi and same_title and txt:row['Recovered abstract text']=txt;row['Result']='Abstract recovered; awaiting individual reading'
  elif txt:row['Result']='Abstract present but identity verification required; not imported'
  else:row['Result']='Metadata retrieved; no deposited abstract'
  row['Published date']=json.dumps(m.get('published',{}).get('date-parts',[]))
 except Exception as e:row['HTTP status']=getattr(e,'code','');row['Result']=type(e).__name__+': '+str(e)[:180]
 return row
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for row in pool.map(get,todo):
  rows.append(row)
  if len(rows)%30==0:print('Metadata checked',len(rows),'of',len(todo),flush=True)
rows.sort(key=lambda x:x['Record ID'])
with (d/'Crossref_Metadata_Recovery.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'checked_records':len(rows),'abstracts_identity_matched':sum(bool(x['Recovered abstract text']) for x in rows),'identity_checks_needed':sum('identity' in x['Result'] for x in rows),'missing_abstract_records_without_doi':sum(not x['Recovered abstract'] and not x['DOI'] for x in q),'note':'Recovered text has not been individually screened; original frozen queue unchanged.'}
(d/'metadata_recovery_progress.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)

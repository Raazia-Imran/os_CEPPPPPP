from pathlib import Path
import csv,json,urllib.request,datetime,hashlib,concurrent.futures,re,html
from html.parser import HTMLParser
d=Path(__file__).resolve().parent;cache=Path('/workspace/scratch/8d52181bc639/research_metadata/publisher');cache.mkdir(parents=True,exist_ok=True)
q=[x for x in csv.DictReader((d/'Working_559_Queue.csv').open(newline='')) if not(x['Recovered abstract'] or x.get('Supplemental abstract'))]
class Meta(HTMLParser):
 def __init__(self):super().__init__();self.meta={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
def clean(t):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',t))).strip()
def get(x):
 u=x['URL'] or ('https://doi.org/'+x['DOI'] if x['DOI'] else '')
 z={'Record ID':x['Record ID'],'Title':x['Title'],'DOI':x['DOI'],'Requested URL':u,'Final URL':'','HTTP status':'','Checked UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Response SHA256':'','Publisher title':'','Publisher DOI':'','Abstract or description text':'','Text type':'','Result':'','Final eligibility':'Pending'}
 if not u:z['Result']='No source URL supplied; targeted title lookup needed';return z
 try:
  req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (compatible; AcademicMetadataReader/1.0)'})
  with urllib.request.urlopen(req,timeout=12) as r:b=r.read(5000000);z['HTTP status']=r.status;z['Final URL']=r.url
  sha=hashlib.sha256(b).hexdigest();z['Response SHA256']=sha;(cache/(x['Record ID']+'.html')).write_bytes(b)
  t=b.decode('utf-8','replace');meta=Meta();meta.feed(t);z['Publisher title']=meta.meta.get('citation_title',meta.meta.get('dc.title',meta.meta.get('og:title','')));z['Publisher DOI']=meta.meta.get('citation_doi',meta.meta.get('dc.identifier',''))
  match=re.search(r'<section[^>]*(?:data-title=["\']Abstract["\']|\bid=["\']Abs1["\'])[^>]*>(.*?)</section>',t,re.S|re.I)
  if match:z['Abstract or description text']=clean(match.group(1));z['Text type']='Publisher abstract section; identity and completeness review pending'
  else:
   z['Abstract or description text']=meta.meta.get('citation_abstract',meta.meta.get('dc.description',meta.meta.get('description',meta.meta.get('og:description',''))))
   z['Text type']='Publisher meta description; may be truncated or generic, not automatically a complete abstract'
  z['Result']='Public page read; text needs individual identity/quality check' if z['Abstract or description text'] else 'Public page read; no abstract extracted'
 except Exception as e:z['HTTP status']=getattr(e,'code','');z['Result']=type(e).__name__+': '+str(e)[:150]
 return z
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for x in pool.map(get,q):
  rows.append(x)
  if len(rows)%25==0:print('Publisher abstract attempts',len(rows),'of',len(q),flush=True)
with (d/'Publisher_Abstract_Attempts.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'records_attempted':len(rows),'pages_with_text_to_verify':sum(bool(x['Abstract or description text']) for x in rows),'note':'Access errors are not scientific exclusions or final reports-not-retrieved; metadata snippets require quality review.'}
(d/'publisher_recovery_progress.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)

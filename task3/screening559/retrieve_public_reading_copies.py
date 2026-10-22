"""Inspect indexed public routes; retain PDFs locally, publish only access logs."""
from pathlib import Path
import csv, urllib.request, concurrent.futures, datetime, hashlib, fitz, json
d=Path(__file__).resolve().parent
reading=Path('/workspace/scratch/8d52181bc639/research_reading/queue');reading.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((d/'Full_Text_Discovery_Routes.csv').open(newline='')))
done={x['Record ID'] for x in csv.DictReader((d/'Final_Eligibility_Decisions.csv').open(newline=''))}
def get(x):
    events=[]
    for url in x['Public PDF routes'].split(' | '):
        if not url:continue
        event={'Record ID':x['Record ID'],'Expected title':x['Title'],'Attempt URL':url,
            'Attempted UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'HTTP status':'','Result':'','PDF pages':'','Source SHA256':'',
            'Content identity':'Not yet inspected','Eligibility':'Pending; access outcome alone is not an eligibility decision'}
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 CEP academic literature access'})
            with urllib.request.urlopen(req,timeout=15) as r:
                b=r.read(25_000_001);event['HTTP status']=r.status
            if len(b)>25_000_000: event['Result']='Response exceeds25MB limit; not retained'
            elif not b.startswith(b'%PDF'): event['Result']='Response is not a PDF; no reading copy claimed'
            else:
                doc=fitz.open(stream=b,filetype='pdf')
                text='\n'.join('PDF PAGE '+str(i+1)+'\n'+page.get_text() for i,page in enumerate(doc))
                (reading/(x['Record ID']+'.pdf')).write_bytes(b)
                (reading/(x['Record ID']+'.txt')).write_text(text)
                event.update({'Result':'PDF retrieved; identity/version and eligibility still require inspection',
                    'PDF pages':len(doc),'Source SHA256':hashlib.sha256(b).hexdigest()})
        except Exception as e:
            event['HTTP status']=getattr(e,'code','')
            event['Result']=str(e)[:220]
        events.append(event)
        if event['Source SHA256']:break
    return events
all_events=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    futures=[ex.submit(get,x) for x in rows if x['Public PDF routes'] and x['Record ID'] not in done]
    for f in concurrent.futures.as_completed(futures):
        all_events.extend(f.result())
        if len(all_events)%10==0:print('Access events',len(all_events),flush=True)
all_events.sort(key=lambda x:(x['Record ID'],x['Attempted UTC']))
with (d/'Public_Full_Text_Access_Attempts.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(all_events[0]));w.writeheader();w.writerows(all_events)
print(json.dumps({'access_events':len(all_events),'pdfs_retrieved':sum(bool(x['Source SHA256']) for x in all_events),
    'eligibility_not_inferred_from_download':True}),flush=True)

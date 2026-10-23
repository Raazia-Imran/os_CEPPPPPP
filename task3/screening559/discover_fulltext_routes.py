"""Discover public reading routes. Metadata matches are not eligibility decisions."""
from pathlib import Path
import csv, json, urllib.request, urllib.parse, concurrent.futures, datetime, hashlib, re
d = Path(__file__).resolve().parent
cache = Path('/workspace/scratch/8d52181bc639/research_metadata/fulltext_routes')
cache.mkdir(parents=True, exist_ok=True)
q = [x for x in csv.DictReader((d/'Working_559_Queue.csv').open(newline=''))
     if x['Preparation recommendation'] != 'propose_exclusion']
if (d/'Final_Screening_Decisions.csv').exists():
    advanced={x['Record ID'] for x in csv.DictReader((d/'Final_Screening_Decisions.csv').open(newline=''))
              if x['Final screening decision'].startswith('Advance')}
    q=[x for x in csv.DictReader((d/'Working_559_Queue.csv').open(newline='')) if x['Record ID'] in advanced]
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
def fetch(url, name):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'CEP-SLR-source-discovery/1.0'}), timeout=25) as r:
        data = r.read()
    (cache/name).write_bytes(data)
    return json.loads(data), hashlib.sha256(data).hexdigest()
def row(x, m, url, sha, error=''):
    doi = (m.get('doi') or '').removeprefix('https://doi.org/')
    matched = norm(m.get('title') or '') == norm(x['Title']) and (not x['DOI'] or doi.lower() == x['DOI'].lower())
    locs = m.get('locations') or []
    pdfs = list(dict.fromkeys(z['pdf_url'] for z in locs if z.get('pdf_url'))) if matched else []
    landings = list(dict.fromkeys(z['landing_page_url'] for z in locs if z.get('landing_page_url'))) if matched else []
    return {'Record ID':x['Record ID'], 'Title':x['Title'], 'Frozen DOI':x['DOI'],
        'Matched DOI':doi if matched else '', 'Identity verified':matched,
        'Indexed publication date':m.get('publication_date','') if matched else '',
        'Public PDF routes':' | '.join(pdfs), 'Landing routes':' | '.join(landings),
        'Discovery URL':url, 'Metadata SHA256':sha, 'Checked UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'Discovery result':error or ('Routes found; content inspection pending' if pdfs else 'No indexed PDF; further publisher/author lookup needed'),
        'Eligibility decision':'Pending primary inspection'}
def bulk(xs, k):
    url='https://api.openalex.org/works?'+urllib.parse.urlencode({'filter':'doi:'+'|'.join('https://doi.org/'+x['DOI'] for x in xs),'per-page':50})
    try:
        data, sha = fetch(url, f'batch_{k:03}.json')
        lookup={(m.get('doi') or '').removeprefix('https://doi.org/').lower():m for m in data.get('results',[])}
        return [row(x,lookup.get(x['DOI'].lower(),{}),url,sha) for x in xs]
    except Exception as e:
        return [row(x,{},url,'',str(e)[:180]) for x in xs]
def title(x):
    url='https://api.openalex.org/works?'+urllib.parse.urlencode({'search':x['Title'],'per-page':5})
    try:
        data,sha=fetch(url,x['Record ID']+'.json')
        m=next((m for m in data.get('results',[]) if norm(m.get('title') or '')==norm(x['Title'])),{})
        return row(x,m,url,sha)
    except Exception as e:return row(x,{},url,'',str(e)[:180])
withdoi=[x for x in q if x['DOI']]; without=[x for x in q if not x['DOI']]
chunks=[withdoi[i:i+25] for i in range(0,len(withdoi),25)]
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    fs=[pool.submit(bulk,xs,k) for k,xs in enumerate(chunks)]
    for f in concurrent.futures.as_completed(fs):rows.extend(f.result())
    rows.extend(pool.map(title,without))
rows.sort(key=lambda x:x['Record ID'])
with (d/'Full_Text_Discovery_Routes.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(json.dumps({'records':len(rows),'with_indexed_pdf_route':sum(bool(x['Public PDF routes']) for x in rows),'exact_identity_matches':sum(x['Identity verified'] for x in rows),'not_final_retrieval_outcomes':True}),flush=True)

"""Rebuild the attributed Group B import from immutable shared exports."""
import csv, json, re, hashlib, html, unicodedata
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'evidence'
def csvwrite(path,rows,fields=None):
    fields=fields or list(rows[0])
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def clean(v):return html.unescape(re.sub(r'\\([&%_{}])',r'\1',v)).replace('{','').replace('}','').strip()
def bib_entries(text):
    # Balanced-brace scanner: abstracts may contain nested TeX braces.
    pos=0
    while m:=re.search(r'@(\w+)\s*\{\s*([^,]+),',text[pos:]):
        typ,key=m.group(1).lower(),m.group(2);start=pos+m.end();i=start;depth=1
        while i<len(text) and depth:
            if text[i]=='{' and (i==0 or text[i-1]!='\\'):depth+=1
            if text[i]=='}' and (i==0 or text[i-1]!='\\'):depth-=1
            i+=1
        if depth:raise ValueError('Unbalanced entry '+key)
        body=text[start:i-1];fields={};j=0
        while fm:=re.search(r'(\w+)\s*=\s*',body[j:]):
            name=fm.group(1).lower();k=j+fm.end();vstart=k
            if k<len(body) and body[k]=='{':
                d=1;k+=1;vstart=k
                while k<len(body) and d:
                    if body[k]=='{' and body[k-1]!='\\':d+=1
                    if body[k]=='}' and body[k-1]!='\\':d-=1
                    k+=1
                value=body[vstart:k-1]
            elif k<len(body) and body[k]=='"':
                k+=1;vstart=k
                while k<len(body) and (body[k]!='"' or body[k-1]=='\\'):k+=1
                value=body[vstart:k];k+=1
            else:
                end=body.find(',',k);k=len(body) if end<0 else end;value=body[vstart:k]
            fields[name]=clean(value);j=k+1
        yield typ,key,fields
        pos=i
def doi_key(s):return re.sub(r'^https?://(?:dx\.)?doi.org/|^doi:\s*','',s.lower().strip()).rstrip(' .')
def title_key(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def main():
    records=[];manifest=[]
    def add(**kw):
        row=dict(record_id=f'GB-R{len(records)+1:05}',source_record_id='',database='',source_run='',source_file='',source_position='',title='',authors='',year='',venue='',doi='',url='',abstract='',source_hash='',route='',entry_type='')
        row.update(kw);records.append(row)
    for p in sorted((E/'imports/acm').glob('*.bib')):
        b=p.read_bytes();sha=hashlib.sha256(b).hexdigest();entries=list(bib_entries(b.decode('utf-8-sig')))
        manifest.append(dict(source_file=str(p.relative_to(ROOT)),sha256=sha,bytes=len(b),occurrences=len(entries),origin='User-supplied ACM Drive export',query_mapping='unknown'))
        for i,(typ,key,r) in enumerate(entries,1):
            add(database='ACM',source_run='ACM-UNMAPPED',source_file=str(p.relative_to(ROOT)),source_position=i,title=r.get('title',''),authors=r.get('author',''),year=r.get('year',''),venue=r.get('booktitle',r.get('journal',typ)),doi=doi_key(r.get('doi','')),url=r.get('url',''),abstract=r.get('abstract',''),source_hash=sha,route='supplied_database_export',entry_type=typ)
    p=E/'imports/group-a/imported_records.json';sha=hashlib.sha256(p.read_bytes()).hexdigest()
    for i,r in enumerate(json.loads(p.read_text()),1):
        add(source_record_id=r['record_id'],database=r['database'],source_run=r['run_id'],source_file=str(p.relative_to(ROOT)),source_position=i,title=r['title'],year=r.get('publication_date',''),doi=doi_key(r.get('doi','')),url=r.get('url',''),abstract=r.get('metadata',''),source_hash=sha,route='shared_database_search')
    manifest.append(dict(source_file=str(p.relative_to(ROOT)),sha256=sha,bytes=p.stat().st_size,occurrences=i,origin='Group A committed search capture',query_mapping='Original run IDs preserved'))
    p=E/'imports/group-a/supplementary_discovery.csv';sha=hashlib.sha256(p.read_bytes()).hexdigest()
    supplement=list(csv.DictReader(p.open()))
    ga_studies={r['record_id']:r for r in csv.DictReader((E/'imports/group-a/studies.csv').open())}
    for i,r in enumerate(supplement,1):
        s=ga_studies[r['record_id']]
        add(source_record_id=r['record_id'],database='Supplementary',source_run='GA-SUPPLEMENTARY',source_file=str(p.relative_to(ROOT)),source_position=i,title=s['title'],doi=doi_key(s.get('doi','')),url=r.get('source_url',''),year=s.get('publication_date',''),abstract=r.get('note',''),source_hash=sha,route='shared_supplementary_lead')
    manifest.append(dict(source_file=str(p.relative_to(ROOT)),sha256=sha,bytes=p.stat().st_size,occurrences=len(supplement),origin='Group A supplementary leads',query_mapping='Not database hits or newly completed snowballing'))
    seen={};duplicates=[];unique=[];titles={};possible=[]
    for r in records:
        d=doi_key(r['doi']);url=r['url'].rstrip('/').lower();key=('doi:'+d) if d else ('url:'+url if url else 'record:'+r['record_id'])
        # Crosswalk DOI and publisher URL so a DOI-less capture can match a DOI-bearing export.
        keys=[key]+(['url:'+url] if url else [])
        if not d and not url and r['authors'] and r['title']:
            keys.append('bibliographic:'+title_key(r['title'])+'|'+r['authors'].lower()+'|'+r['year'])
        match=next((seen[k] for k in keys if k in seen),None)
        r['canonical_record_id']=match or r['record_id']
        if match:
            duplicates.append(dict(record_id=r['record_id'],canonical_record_id=match,match_basis='Exact DOI/URL or exact title+authors+year without identifiers',resolution='Deterministic linkage; different DOI versions remain separate'))
            for k in keys:seen[k]=match
        else:
            unique.append(r)
            for k in keys:seen[k]=r['record_id']
            t=title_key(r['title'])
            if t in titles:possible.append(dict(record_id=r['record_id'],possible_match=titles[t],title=r['title'],status='Manual version/identity check required; not removed'))
            else:titles[t]=r['record_id']
    queue=[]
    for r in unique:
        s=(r['title']+' '+r['abstract']).lower()
        gpu=bool(re.search(r'\bgpu|graphics processing|cuda|nvidia',s));inf=bool(re.search(r'inferen|serving|\bdnn|\bllm|neural network',s));sharing=bool(re.search(r'shar|multi.?tenan|concurren|partition|\bmps\b|\bmig\b|preempt|remot|virtualiz|interferen|co.?locat|co.?execut|schedul',s))
        priority='high' if gpu and inf and sharing else ('uncertain' if gpu and (inf or sharing) else 'low')
        queue.append(dict(record_id=r['record_id'],database=r['database'],title=r['title'],doi=r['doi'],priority=priority,triage_basis=f'GPU={gpu}; inference={inf}; sharing={sharing}',screening_decision='pending',reviewer_1_vote='',reviewer_2_vote='',criterion='',reason='',fulltext_status='pending'))
    csvwrite(E/'records.csv',records);csvwrite(E/'duplicates.csv',duplicates);csvwrite(E/'possible_versions.csv',possible,['record_id','possible_match','title','status']);csvwrite(E/'screening.csv',queue);csvwrite(E/'import_manifest.csv',manifest)
    summary=dict(occurrences=len(records),database_occurrences=sum(r['database']!='Supplementary' for r in records),supplementary_occurrences=len(supplement),by_source=dict(Counter(r['database'] for r in records)),exact_duplicate_occurrences=len(duplicates),records_after_exact_linkage=len(unique),possible_version_pairs=len(possible),triage=dict(Counter(r['priority'] for r in queue)),final_screened=None,final_included=None)
    (E/'prisma_counts.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()

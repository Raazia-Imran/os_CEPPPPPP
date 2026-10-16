"""Append supplied ScienceDirect export occurrences; preserve existing review events.
Run once against the saved pre-import baseline. Subsequent runs validate and stop.
"""
import csv,json,re,hashlib,collections,sys
from pathlib import Path
from datetime import datetime,timezone
from import_shared import bib_entries,doi_key,title_key,csvwrite
R=Path(__file__).resolve().parents[1];E=R/'evidence';NOW=datetime.now(timezone.utc).isoformat(timespec='seconds')
def read(n):return list(csv.DictReader((E/n).open(encoding='utf-8-sig')))
def write(n,rs,fields=None):csvwrite(E/n,rs,fields)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ris(p):
 t=p.read_text(encoding='utf-8-sig');out=[];r=None;last=None
 for line in t.splitlines():
  m=re.match(r'^([A-Z0-9]{2})  - ?(.*)$',line)
  if m:
   k,v=m.groups()
   if k=='TY':assert r is None; r={}
   if k=='ER':
    assert r is not None;out.append(r);r=None;last=None;continue
   if r is not None:r.setdefault(k,[]).append(v);last=k
  elif line.strip() and r is not None and last:r[last][-1]+=' '+line.strip()
 assert r is None,'Unterminated RIS '+str(p)
 assert len(out)==len(re.findall(r'^TY  -',t,re.M))
 return out
if (E/'query_import_cycle_validation.json').exists():
 print('Existing import receipt found. Refusing to reassign IDs or repeat imports.');sys.exit(0)
rec=read('records.csv');screen=read('screening.csv');dup=read('duplicates.csv');manifest=read('import_manifest.csv')
base={n:sha(E/n) for n in ['records.csv','screening.csv','title_votes.csv','quality.csv','extraction.csv','study_extraction_form.csv','duplicates.csv','import_manifest.csv']}
(E/'query_import_cycle_baseline.json').write_text(json.dumps({'time_utc':NOW,'base_commit':'cb8251a1413da77b57a3df894e904c2f9f11bdd0','hashes':base,'counts':json.loads((E/'prisma_counts.json').read_text())},indent=2)+'\n')
# Exact reported log values remain separate from parsed exports.
text=(E/'incoming_shared/search_log_2026-10-16.txt').read_text();blocks=re.split(r'\n-+\s*\n',text);logs={}
for block in blocks:
 row={}
 for line in block.splitlines():
  if ': ' in line:
   k,v=line.split(': ',1);row[k]=v
 if 'Run ID' in row:logs[row['Run ID']]=row
files=list(sorted((E/'incoming_shared/sciencedirect_2026-10-16').glob('*.ris')))
assert len(files)==21
fileaudit=[];groups=collections.defaultdict(list);payload=[]
for p in files:
 family='SD-'+('MPS' if 'MPS' in p.name else 'MIG' if 'MIG' in p.name else 'API' if 'API' in p.name else 'TEMPORAL')
 rr=ris(p);groups[family]+=rr
 fileaudit.append(dict(filename=p.name,source_file=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size,parsed_occurrences=len(rr),run_id=family,mapping_status='family mapping supported by export name and supplied historical log; exact page order unverified',provenance='User supplied Drive citation export',import_status='active supplied partial search export'))
 payload.extend((p,family,i,r) for i,r in enumerate(rr,1))
write('query_export_audit.csv',fileaudit)
# DOI first; never collapse distinct DOIs by URL/title. Bibliographic fallback needs equal authors/year.
index={};titleindex=collections.defaultdict(list)
def keys(r):
 d=doi_key(r['doi']);u=r['url'].lower().rstrip('/');out=[]
 if d:out.append('doi:'+d)
 if u:out.append('url:'+u)
 if r['title'] and r['authors'] and r['year']:out.append('bib:'+title_key(r['title'])+'|'+title_key(r['authors'])+'|'+r['year'])
 return out
for r in rec:
 for k in keys(r):index.setdefault(k,r)
 titleindex[title_key(r['title'])].append(r)
nextid=max(int(r['record_id'].split('GB-R')[1]) for r in rec)+1;added=[];proposals=[];newqueue=[]
for p,family,pos,r in payload:
 val=lambda *ks: next((r[k][0] for k in ks if k in r),'')
 rid=f'GB-R{nextid:05}';nextid+=1
 x=dict.fromkeys(rec[0],'');x.update(record_id=rid,source_record_id=f'{p.name}:{pos}',database='ScienceDirect',source_run=family,source_file=str(p.relative_to(R)),source_position=str(pos),title=val('T1','TI'),authors=' and '.join(r.get('AU',r.get('A1',[]))),year=val('PY','Y1','DA'),venue=val('JO','JF','T2'),doi=doi_key(val('DO')),url=val('UR'),abstract=' '.join(r.get('AB',r.get('N2',[]))),source_hash=sha(p),route='supplied_partial_database_export;reported_historical_run',entry_type=val('TY'))
 # Missing titles remain blank as supplied; identity uses DOI/URL and metadata repair remains pending.
 match=None
 for k in keys(x):
  old=index.get(k)
  if old and not (x['doi'] and old['doi'] and doi_key(x['doi'])!=doi_key(old['doi'])):match=old;break
 x['canonical_record_id']=match['canonical_record_id'] if match else rid
 if match:dup.append(dict(record_id=rid,canonical_record_id=x['canonical_record_id'],match_basis='Exact DOI' if x['doi'] and doi_key(x['doi'])==doi_key(match['doi']) else 'Exact publisher URL or title+authors+year; no distinct DOI merged',resolution='Deterministic append-only linkage to preserved canonical ID'))
 else:
  ss=dict.fromkeys(screen[0],'');ss.update(record_id=rid,database='ScienceDirect',title=x['title'],doi=x['doi'],priority='not_prioritized',triage_basis='Imported this cycle; no screening performed',screening_decision='awaiting_first_recommendation',fulltext_status='not_sought',abstract_status='abstract supplied in RIS' if x['abstract'] else 'abstract unavailable',final_decision='pending',batch_id='QUERY-IMPORT-SD-2026-10-16');newqueue.append(ss)
  for old in (titleindex[title_key(x['title'])] if x['title'] else []):
   if old['canonical_record_id']!=rid:proposals.append(dict(record_id=rid,possible_match=old['canonical_record_id'],title=x['title'],status='same normalized title; distinct or absent identifiers; not merged'))
 for k in keys(x):index.setdefault(k,x)
 titleindex[title_key(x['title'])].append(x);rec.append(x);added.append(x)
for row in fileaudit:manifest.append(dict(source_file=row['source_file'],sha256=row['sha256'],bytes=row['bytes'],occurrences=row['parsed_occurrences'],origin='User supplied ScienceDirect partial export; historical run reported',query_mapping=row['run_id']+' family supported; page order unverified'))
write('records.csv',rec);write('screening.csv',screen+newqueue);write('duplicates.csv',dup);write('import_manifest.csv',manifest)
write('new_import_queue.csv',newqueue,list(screen[0]));write('new_version_candidates.csv',proposals,['record_id','possible_match','title','status'])
# Consolidated query table covers all four platforms while preserving original shared search logs.
queries=[]
for r in read('imports/group-a/search_runs.csv'):
 queries.append(dict(run_id=r['run_id'],platform=r['database'],status='attributed shared executed search; not rerun by Group B',query=r['query'],fields=r['fields'],filters=r['filters'],executed_date=r['date'],time_and_timezone='time not recorded; timezone unknown',displayed_hits_reported=r['hits'],exported_claimed=r['imported_occurrences'],parsed_or_captured_occurrences=sum(x['source_run']==r['run_id'] for x in rec),active_occurrences=sum(x['source_run']==r['run_id'] for x in rec),files='evidence/imports/group-a/imported_records.json',provenance='Group A source snapshot adf4a1e; shared search_runs.csv',gaps='Rendered metadata capture, not publisher export; exact time unavailable; different expressions from submitted protocol; full text indexed scope for Springer'))
for run,l in logs.items():
 rr=groups[run] if run.startswith('SD-') else []
 actual=len(rr) if rr else 1829
 paths=';'.join(r['source_file'] for r in fileaudit if r['run_id']==run) if rr else 'evidence/incoming_shared/acm_master/ACM_MASTER_01.bib;evidence/incoming_shared/acm_master/ACM_MASTER_02.bib'
 queries.append(dict(run_id=run,platform='ScienceDirect' if rr else 'ACM Digital Library',status='historical operator-reported; partial export reconciliation' if rr else 'reported master query; master and numbered exports not fully mapped',query=l.get('Exact query entered',''),fields=l.get('Search field(s)',''),filters=l.get('Filters (year, type, language, other)',''),executed_date='2026-10-14 (operator reported)',time_and_timezone=l.get('Search date/time (Pakistan time)','')+' Asia/Karachi',displayed_hits_reported=l.get('Displayed hit count','unknown'),exported_claimed=l.get('Number of records exported (if known)','unknown'),parsed_or_captured_occurrences=actual,active_occurrences=len(rr) if rr else 0,files=paths,provenance='Supplied search_log_2026-10-16.txt; actual bytes audited separately',gaps=('TEMPORAL URL has openaccess facet omitted from filter text; 1053 parsed agrees with reported count; exact pagination and operator unknown' if run=='SD-TEMPORAL' else '563 parsed versus 517 displayed; export claim 563; operator and exact pagination unknown' if run=='SD-MPS' else 'Parsed count agrees with reported count; identity and page completeness unverified; operator unknown' if rr else '1600 displayed and 1603 exported claimed; 1829 overlapping master entries with 1387 distinct DOI/title keys; 68 staged unmatched candidates; original 79-file mapping unresolved')))
queries.append(dict(run_id='ACM-NUMBERED-UNMAPPED',platform='ACM Digital Library',status='actual supplied exports; run mapping unknown',query='unknown',fields='unknown',filters='unknown',executed_date='unknown',time_and_timezone='unknown',displayed_hits_reported='unknown',exported_claimed='unknown',parsed_or_captured_occurrences=1582,active_occurrences=1582,files='evidence/imports/acm/*.bib; exact files in import_manifest.csv',provenance='79 user supplied originals, preserved hashes',gaps='Number 3 absent in names 1–80; this is not proof of missing search page; do not assign to master query without mapping evidence'))
write('database_query_audit.csv',queries)
# Report metadata defects without silently rewriting publisher values.
dates=[]
for r in rec:
 ys=re.findall(r'\b(?:19|20)\d{2}\b',r['year']);flag=''
 if not ys:flag='year unavailable or not parseable'
 elif int(ys[0])>2026:flag='publication year after protocol period; screen before eligibility'
 elif int(ys[0])<2020:flag='older study exception requires justification'
 elif ys[0]=='2026':flag='2026 publication day/cutoff not established from year alone'
 if flag:dates.append(dict(record_id=r['record_id'],canonical_record_id=r['canonical_record_id'],database=r['database'],year_as_imported=r['year'],title=r['title'],date_check=flag,final_decision='pending'))
write('publication_date_audit.csv',dates)
c=json.loads((E/'prisma_counts.json').read_text());c.update(occurrences=len(rec),database_occurrences=sum(x['database']!='Supplementary' for x in rec),by_source=dict(collections.Counter(x['database'] for x in rec)),exact_duplicate_occurrences=len(dup),records_after_exact_linkage=len(screen)+len(newqueue),first_recommendations_pending=len(newqueue),four_database_completeness='not established; supplied exports from four platforms represented',new_sciencedirect_occurrences=len(added),final_screened=None,final_included=None)
(E/'prisma_counts.json').write_text(json.dumps(c,indent=2)+'\n')
p=json.loads((E/'review_progress.json').read_text());p.update(unreviewed=len(newqueue),first_reviewer_fraction=2247/(len(screen)+len(newqueue)),cycle2_new_import_occurrences=len(added),cycle2_new_canonical_records=len(newqueue),cycle2_records_screened=0,cycle2_updated_at_utc=NOW,cycle2_report_status='Existing PDF predates database reconciliation; rebuild required before submission')
(E/'review_progress.json').write_text(json.dumps(p,indent=2)+'\n')
receipt=dict(checked_at_utc=NOW,scope='Cycle 2 database reconciliation, no screening',previous_occurrences=2291,added_sd_occurrences=len(added),new_canonical_records=len(newqueue),occurrences=len(rec),duplicate_links=len(dup),canonical_records=len(screen)+len(newqueue),by_source=c['by_source'],existing_recommendations=2247,preliminary_exclusions=1181,retain_or_uncertain=1066,first_recommendations_pending=len(newqueue),qa_items=50,outcomes=26,raw_manifest_rows=len(manifest),raw_hashes_match=all(sha(R/x['source_file'])==x['sha256'] for x in manifest),original_review_events_preserved=all(sha(E/n)==base[n] for n in ['title_votes.csv','quality.csv','extraction.csv','study_extraction_form.csv']),final_included_studies=None,masters_remain_staged=True,science_direct_family_counts={k:len(v) for k,v in groups.items()},four_database_complete=False,old_pdf_stale=True)
assert len(rec)-len(dup)==len(screen)+len(newqueue)
assert receipt['raw_hashes_match'] and receipt['original_review_events_preserved']
assert len({x['record_id'] for x in rec})==len(rec)
assert all(x['canonical_record_id'] in {s['record_id'] for s in screen+newqueue} for x in rec)
assert sum(int(x['occurrences']) for x in manifest)==len(rec)
(E/'query_import_cycle_validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))

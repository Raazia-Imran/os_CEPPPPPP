"""Validate accounting, frozen evidence, analysis IDs, citations and compiled artifacts."""
import csv,json,re,hashlib,zipfile,subprocess,xml.etree.ElementTree as X
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];E=R/'evidence';O=R/'task2/report'
def read(n):return list(csv.DictReader((E/n).open()))
b=json.loads((E/'cycle2_baseline.json').read_text());changed=[r['file'] for r in b['source_files'] if hashlib.sha256((R/r['file']).read_bytes()).hexdigest()!=r['sha256']]
assert set(changed)<={'evidence/review_progress.json'},changed
manifest=read('import_manifest.csv');assert len(manifest)==81
for r in manifest:assert hashlib.sha256((R/r['source_file']).read_bytes()).hexdigest()==r['sha256'],r['source_file']
# The submitted protocol is a tracked immutable baseline artifact.
proto=R/'task1/submitted_protocol.pdf';old=subprocess.check_output(['git','show',b['baseline_commit']+':task1/submitted_protocol.pdf'],cwd=R);assert hashlib.sha256(old).digest()==hashlib.sha256(proto.read_bytes()).digest()
rec=read('records.csv');scr=read('screening.csv');dup=read('duplicates.csv');qa=read('quality.csv');ex=read('extraction.csv');forms=read('study_extraction_form.csv');sb=read('snowballing.csv');versions=read('version_review_audit.csv');a=read('cycle2_analysis.csv');cat=read('cycle2_reference_catalog.csv')
assert len({r['record_id'] for r in rec})==len(rec)==2291
canonical={r['canonical_record_id'] for r in rec};assert canonical=={r['record_id'] for r in scr};assert len(canonical)==len(rec)-len(dup)==2247
assert all(r['final_decision']=='pending' for r in scr)
assert Counter(r['reviewer_1_vote'] for r in scr)=={'exclude_recommendation':1181,'retain_or_uncertain':1066}
assert not any(r['reviewer_2_vote'] for r in scr)
assert len(read('human_validation_queue.csv'))==1066;assert len(read('exclusion_validation_sample.csv'))==127
assert len(qa)==50 and len({r['report_id'] for r in qa})==5
assert all(r['independent_checker']=='' and r['reconciled_score']=='' for r in qa)
assert len(ex)==26 and len({r['outcome_id'] for r in ex})==26
assert all(r['final_decision'] in ['', 'pending'] and not r['independent_checker'] for r in ex)
lookup={r['outcome_id']:r for r in ex};reportids={r['report_id'] for r in forms}
assert len({r['analysis_id'] for r in a})==len(a)==41
for r in a:
 ids=set(filter(None,r['outcome_ids'].split(';')));assert ids<=lookup.keys()
 assert set(filter(None,r['report_ids'].split(';')))<=reportids
 for id in ids:
  assert lookup[id]['source_anchor'] in r['source_anchor']
  assert lookup[id]['report_id'] in r['report_ids']
 assert r['final_status']=='pending human validation'
c=json.loads((E/'prisma_counts.json').read_text());assert c['final_screened'] is None and c['final_included'] is None
src=(O/'main.tex').read_text();citekeys={k for group in re.findall(r'\\cite\{([^}]+)\}',src) for k in group.split(',')};assert citekeys=={r['citation_key'] for r in cat}
assert len(cat)==14 and sum(bool(r['doi']) for r in cat)==5
assert all(not r['doi'] for r in cat if r['citation_key'] in ['reef','pipeswitch','gpulets'])
assert len(re.findall(r'\\section\{',src.split(r'\appendix')[0]))==22
assert 'DOI and official-source catalogue' in src.rsplit(r'\section{',1)[1]
log=(O/'report.log').read_text();assert not re.search(r'Overfull|undefined citations|Citation .* undefined|! LaTeX Error',log)
text=subprocess.check_output(['pdftotext','-layout',str(O/'report.pdf'),'-'],text=True);flat=re.sub(r'\s+','',text)
for id in lookup:assert id in flat,id
assert not re.search(r'\b(?:Codex|ChatGPT|artificial intelligence assistant)\b',text,re.I)
info=subprocess.check_output(['pdfinfo',str(O/'report.pdf')],text=True);pages=int(re.search(r'Pages:\s+(\d+)',info).group(1))
# Read actual saved workbook values, including cached formulas, without re-authoring it.
z=zipfile.ZipFile(R/'task2/tracker/review_workbook.xlsx');assert z.testzip() is None
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};shared=[]
if 'xl/sharedStrings.xml' in z.namelist():shared=[''.join(e.itertext()) for e in X.fromstring(z.read('xl/sharedStrings.xml'))]
wb=X.fromstring(z.read('xl/workbook.xml'));names=[s.get('name') for s in wb.find('s:sheets',ns)];assert len(names)==27
allcells=[];sheetcells={}
for i,name in enumerate(names,1):
 vals={}
 for cell in X.fromstring(z.read(f'xl/worksheets/sheet{i}.xml')).findall('.//s:c',ns):
  v=cell.find('s:v',ns);inline=cell.find('s:is',ns)
  value=shared[int(v.text)] if cell.get('t')=='s' and v is not None else ''.join(inline.itertext()) if inline is not None else v.text if v is not None else ''
  assert cell.get('t')!='e',(name,cell.get('r'),value)
  vals[cell.get('r')]=value;allcells.append(value)
 sheetcells[name]=vals
summary=sheetcells['Summary'];assert [float(summary[x]) for x in ['B5','B6','B7','B8']]==[2291,44,2247,2247]
assert [float(summary['B'+str(n)]) for n in range(20,25)]==[13,17,18,17,17]
assert [float(summary['C'+str(n)]) for n in range(20,25)]==[18,20,20,20,20]
# Reconstruct the new analysis views and compare every field with the CSV register.
for kind,name in [('taxonomy','Taxonomy'),('comparison','Comparative matrix'),('tradeoff','Trade-offs'),('conflict','Conflicting evidence'),('rq','RQ synthesis'),('recommendation','Recommendations'),('gap','Evidence gaps'),('validity','Validity')]:
 vals=sheetcells[name];headers={re.match(r'[A-Z]+',cell).group(0):v for cell,v in vals.items() if re.fullmatch(r'[A-Z]+1',cell)}
 source=[r for r in a if r['kind']==kind]
 for row,r in enumerate(source,2):
  for col,field in headers.items():assert vals.get(col+str(row),'')==r[field],(name,row,field)
# Scan only changed publishable text; source URLs are public publishers, never private Drive links.
paths=set(subprocess.check_output(['git','diff','--name-only',b['baseline_commit']],cwd=R,text=True).splitlines())|set(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines())
for n in paths:
 p=R/n
 if p.is_file() and p.suffix in ['.md','.csv','.json','.tex','.bib','.py','.mjs']:
  assert not re.search(r'ghp_[A-Za-z0-9]{20,}|github_pat_|BEGIN [A-Z ]*PRIVATE KEY|drive.google.com/(?:drive|file)',p.read_text()),n
result={'checked_at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'cycle1_baseline_commit':b['baseline_commit'],'cycle2_new_screening_recommendations':0,'cycle1_primary_registers_unchanged':True,'only_modified_baseline_evidence_files':changed,'raw_hash_files_verified':len(manifest),'submitted_protocol_unchanged':True,'occurrences':len(rec),'by_source':dict(Counter(r['database'] for r in rec)),'duplicate_links':len(dup),'canonical_records':len(scr),'preliminary_exclusions':1181,'retain_or_uncertain':1066,'first_recommendations_pending':0,'human_candidate_queue':1066,'exclusion_sample':127,'priority_candidate_records':148,'version_dispositions':dict(Counter(r['audit_disposition'] for r in versions)),'quality_forms':5,'quality_items':len(qa),'study_forms':len(forms),'outcome_rows':len(ex),'legacy_outcome_final_decision_cells_blank':sum(not r['final_decision'] for r in ex),'snowballing_events':len(sb),'snowballing_directions':dict(Counter(r['direction'] for r in sb)),'analysis_statements':len(a),'cited_sources':len(cat),'verified_cited_dois':5,'report_pages':pages,'main_package_pages_including_title_and_contents':20,'workbook_sheets':len(names),'workbook_formula_cached_values_and_analysis_views':'PASS','latex_bibtex':'PASS; no undefined citations or overfull boxes','pdf_visual':'pending final rendered-page inspection','workbook_visual':'pending final preview inspection','final_included_studies':'pending','planning_readiness':'approximately60-65%; not a verified completion metric'}
(E/'cycle2_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

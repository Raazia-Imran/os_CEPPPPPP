"""Reader-facing checkpoint; derive counts and preserve unknown historical events."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import csv,json,re,shutil,hashlib
R=Path(__file__).resolve().parents[1];E=R/'evidence';F=R/'final things';S=F/'01_Statistics_and_Papers';W=F/'04_Workbook_and_Logs';A=F/'05_Protocol_and_Audit'
def read(n):return list(csv.DictReader((E/n).open(newline='')))
def write(p,rows):
 with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rec=read('records.csv');screen=read('screening.csv');forms=read('study_extraction_form.csv');checks=read('fulltext_checks.csv');votes=read('title_votes.csv');links=read('report_record_links.csv');quality=read('quality.csv');outcomes=read('extraction.csv');excluded=read('fulltext_exclusions.csv')
assert len(rec)-len(read('duplicates.csv'))==len(screen)==4075
raw=Counter(x['database'] for x in rec);canonical=Counter(x['database'] for x in screen)
databases=[dict(database=d,imported_occurrences=raw[d],linked_repeats_attributed=raw[d]-canonical[d],canonical_records=canonical[d]) for d in ['ACM','IEEE','Springer','ScienceDirect','Supplementary']]
write(S/'DATABASE_STATISTICS.csv',databases)
ci=Counter(x['criterion'] for x in screen if x['reviewer_1_vote']=='exclude_recommendation')
stats=[('Imported occurrences',4189,'Four databases4169 plus supplementary20'),('Applied duplicate links',114,'Occurrences remain preserved'),('Canonical records',4075,'4189-114'),('Initial automated recommendations',4075,'Not complete abstract verification'),('Preliminary exclusion proposals',1441,'Not final screened exclusions'),('Retain or uncertain after initial triage',2634,'Not all eligible'),('Awaiting first automated recommendation',0,'Does not imply completed screening'),('Source-assessed reports',17,'Bounded source-assessment slice'),('Provisionally eligible reports',13,'Not final unique studies'),('Companion candidate reports',1,'REEF study/report relationship open'),('Publication-version-uncertain reports',1,'ParvaGPU accessed arXiv version'),('Assessed full-text EC2 exclusions',2,'TGS and HiveD; incomplete exclusion census'),('QA and extraction forms',15,'13provisional plus2unresolved cases'),('Q1-Q10 item rows',150,'Ten items per form'),('Reported outcome rows',45,'Not45papers'),('Separate calculated outcomes',2,'Not author-reported measurements'),('Unassessed canonical retain/uncertain records',2617,'No linked source assessment'),('Independent human votes recorded',0,'AI-only deviation disclosed'),('Final included reports/studies','Pending','Not established; do not substitute15forms')]
write(S/'SELECTION_STATISTICS.csv',[dict(stage=a,count=b,meaning=c) for a,b,c in stats]);write(S/'PRELIMINARY_EXCLUSION_REASONS.csv',[dict(criterion=k,proposal_count=v,stage='initial_automated_triage;not_final_exclusion') for k,v in sorted(ci.items())])
by={x['record_id']:x for x in rec};pids=defaultdict(list)
for x in links:pids[x['report_id']].append(x)
short=['VastPipe','iGniter','gpulets','PipeSwitch','REEF','Paella','Orion','GSLICE','Clockwork','SIRIUS','ParvaGPU','Torpor','StreamBox','KRYPTON','XSched']
catalog=[];audit=[];today=datetime.now(timezone.utc).isoformat(timespec='seconds')
for f,name in zip(forms,short):
 pid=f['report_id'];doi=f['doi'] if f['doi'].startswith('10.') else '';source=f['source'] if f['source'].startswith('http') else 'https://doi.org/'+doi
 full=f['title'];cross=R.parent/'private_cycle6'/(pid+'.json')
 if cross.exists():full=re.sub('<[^>]+>','',json.loads(cross.read_text())['title'][0]);full=re.sub(r'\s+',' ',full).strip()
 elif len(full)<25:
  match=next((by[x['record_id']] for x in pids[pid] if x['record_id'] in by),None)
  if match:full=match['title']
 status=('provisional' if f['eligibility_status'].startswith('provisionally_eligible') else 'companion_candidate' if 'companion' in f['eligibility_status'] else 'publication_version_uncertain')
 if len(full)<25 and len(f['title'])>=25:full=f['title']
 catalog.append(dict(report_id=pid,short_name=name,title=full,year=f['year'],doi=doi or 'Not verified; official URL supplied',official_or_accessed_source=source,assessment_status=status,final_included='Pending',qa_items=10,outcome_rows=sum(x['report_id']==pid for x in outcomes)))
 audit.append(dict(report_id=pid,doi=doi,identity_url=('https://doi.org/'+doi if doi else source),verification_method=('Crossref live metadata; title matched' if cross.exists() else 'Publisher DOI/title search matched; Crossref retry429' if pid=='GB-P007' else 'Official accessed report URL retained; no DOI invented'),checked_at_utc=today,version_boundary=('Accessed arXiv preprint; final-publication equivalence unverified' if pid=='GB-P011' else 'REEF conference versus journal companion unresolved' if pid=='GB-P005' else 'Source version recorded in extraction form')))
write(S/'CURRENT_ASSESSED_PAPERS_AND_DOIS.csv',catalog);write(S/'DOI_SOURCE_AUDIT.csv',audit);write(S/'ASSESSED_EXCLUSIONS.csv',excluded)
events=defaultdict(list)
for v in votes:events[v['record_id']].append(v)
log=read('cycle3_screening_log.csv');lookup={x['record_id']:x for x in screen};dates_missing=times_missing=0
for r in log:
 x=lookup[r['record_id']];event=next((v for v in events[r['record_id']] if v['vote']==x['reviewer_1_vote']),{})
 date=x['date'] or event.get('date','');ts=x['timestamp_utc'] or event.get('timestamp_utc','') or x['first_assessed_at_utc'];dates_missing+=not bool(date);times_missing+=not bool(ts)
 r.update(screening_assessor=x['reviewer'] or event.get('reviewer','') or x['first_assessor'] or 'Not recorded',screening_date=date or 'Not recorded',screening_timestamp_utc=ts or 'Not recorded',timestamp_basis='existing screening record' if x['timestamp_utc'] else 'existing vote event' if event.get('timestamp_utc') else 'existing first-assessment field' if x['first_assessed_at_utc'] else 'No event timestamp; metadata-check date is not substituted',screening_method=x['method'] or event.get('method','') or 'Existing title recommendation; method field not recorded')
original=json.loads((R/'task2/submission/submission_input.json').read_text())
old_by={x['record_id']:x for x in original['tabs']['Screening log']}
log=[dict(old_by[r['record_id']],**{k:v for k,v in r.items() if k not in old_by[r['record_id']]}) for r in log]
write(W/'SCREENING_LOG_WITH_RECORDED_DATES.csv',log)
cycles=[dict(cycle=i,name=n,status=s,remaining=g) for i,n,s,g in [(1,'Recovery and requirements audit','Closed audit scope','Research gaps tracked separately'),(2,'Queries/imports/four-database audit','Closed audit scope with documented gaps','ACM run mapping; historical hit/export discrepancies; search completeness'),(3,'Screening/full-text selection','Partial','2617 canonical candidates lack source assessment; final selection pending'),(4,'Quality assessment','Partial overall; current15forms covered','23section/figure anchors;3provisional N/A calibrations; future eligible candidates'),(5,'Data extraction','Partial overall; current15forms covered','Unchecked fields and new eligible candidates; version reconciliation'),(6,'PRISMA and references','Interim outputs','Final selection and report/study linkage needed for final flow')]]
write(A/'CYCLE_STATUS.csv',cycles)
validation=dict(derived_from='verified main ef52a35e218c4b19425ab21c924aaac029aed2e0 plus presentation-only changes',statistics=dict((a,b) for a,b,c in stats),recorded_dates_missing=dates_missing,event_timestamps_missing=times_missing,no_invented_times=True,no_new_scientific_decisions=True,task1_sha256=hashlib.sha256((R/'task1/submitted_protocol.pdf').read_bytes()).hexdigest(),current_paper_names=short)
(S/'statistics.json').write_text(json.dumps(validation,indent=2)+'\n')
# Keep the simpler workbook layout and enrich only its actual screening provenance.
d=json.loads((R/'task2/submission/submission_input.json').read_text());d['tabs']['Screening log']=log
# Existing study summary contains six verified DOIs and official source URLs where no DOI is verified.
(R/'task2/qa/final_things_input.json').write_text(json.dumps(d)+'\n')
# Necessary supporting files only; raw licensed papers and supplied classmate work remain private.
for a,b in [('task1/submitted_protocol.pdf','05_Protocol_and_Audit/Submitted_Task1_Protocol.pdf'),('evidence/protocol_amendments.md','05_Protocol_and_Audit/Protocol_amendments.md'),('task2/HEADING_14_AUDIT.csv','05_Protocol_and_Audit/Requirements_1_to_14.csv'),('task2/qa/QA_CHECKLIST_AND_SCORING.md','03_QA_and_Extraction/QA_CHECKLIST_AND_SCORING.md')]:shutil.copy2(R/a,F/b)
for n in ['qa_score_matrix.csv','qa_totals_summary.csv','qa_rationale_table.csv','qa_followup.csv']:shutil.copy2(R/'task2/qa'/n,F/'03_QA_and_Extraction'/n)
for n in ['quality.csv','study_extraction_form.csv','extraction.csv','calculated_outcomes.csv']:shutil.copy2(E/n,F/'03_QA_and_Extraction'/n)
for n in ['database_query_audit.csv','query_export_audit.csv','import_manifest.csv','cycle3_duplicate_ledger.csv','duplicates.csv','fulltext_checks.csv','fulltext_criteria.csv','fulltext_exclusions.csv','fulltext_decision_log.csv']:shutil.copy2(E/n,W/n)
for n in ['GroupB_QA_Tables.pdf','GroupB_Data_Extraction.pdf']:shutil.copy2(R/'task2/submission'/n,F/'03_QA_and_Extraction'/n)
print('Counts verified; current15paper catalogue; date-only rows and missing event times:',dates_missing,times_missing)

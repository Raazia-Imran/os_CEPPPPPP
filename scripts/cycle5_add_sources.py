"""Append source-based AI assessments without overwriting earlier evidence."""
import csv,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];E=R/'evidence';TS=datetime.now(timezone.utc).isoformat(timespec='seconds')
def read(n):
 with (E/n).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def save(n,rows):
 fields=list(dict.fromkeys(k for x in rows for k in x))
 with (E/n).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
data=json.loads((E/'cycle5_source_assessments.json').read_text())
names=['study_extraction_form.csv','quality.csv','extraction.csv','fulltext_checks.csv','fulltext_criteria.csv','report_record_links.csv','report_validation_queue.csv','cycle3_retrieval.csv']
tables={n:read(n) for n in names};records=read('records.csv')
for p in data:
 rid=p['report_id']
 if any(x['report_id']==rid for x in tables['study_extraction_form.csv']):continue
 assert len(p['quality'])==10 and len(p['ic'])==6
 pdf=R.parent/'private_cycle5'/p['pdf_file'];assert pdf.read_bytes().startswith(b'%PDF')
 form={k:'not_extracted' for k in tables['study_extraction_form.csv'][0]}
 form.update(p['form'],report_id=rid,study_id='GB-PS'+rid[-3:],title=p['title'],doi=p['doi'],source=p['source_url'],source_anchor=p['anchor'],eligibility_status=p['eligibility'],reviewer='Codex-GroupB source assessment',independent_checker='',checked_at_utc=TS,field_status='Source-based AI extraction; unchecked fields explicitly marked; independent check pending',metric_outcomes_register='extraction.csv:'+rid)
 tables['study_extraction_form.csv'].append(form)
 for i,q in enumerate(p['quality'],1):
  score,reason,anchor=q
  tables['quality.csv'].append(dict(report_id=rid,criterion='Q'+str(i),score=str(score),maximum='0' if score=='NA' else '2',rationale=reason,anchor=anchor,reviewer='Codex-GroupB source assessment',second_score='',reconciled_score='',status='AI_first_review;independent_pending',checked_at_utc=TS,independent_checker='',reconciliation_status='pending',doi=p['doi'],source_url=p['source_url']))
 for x in p['outcomes']:
  oid='GB-O'+str(1+max(int(y['outcome_id'][4:]) for y in tables['extraction.csv'])).zfill(3)
  row={k:'' for k in tables['extraction.csv'][0]};row.update(x,report_id=rid,outcome_id=oid,mechanism=form['mechanism'],hardware=form['gpu_hardware'],reviewer='Codex-GroupB source assessment',check_status='AI_source_assessment;independent_pending',checked_at_utc=TS,independent_checker='',final_decision='pending',doi=p['doi'],source_url=p['source_url'],evidence_scope='within-one-GPU result; source version and caveats control interpretation')
  tables['extraction.csv'].append(row)
 tables['fulltext_checks.csv'].append(dict(report_id=rid,short_name=p['title'],doi=p['doi'],source=p['source_url'],anchor=p['anchor'],first_reviewer_recommendation=p['eligibility'],criterion_rationale='; '.join(p['ic']),remaining_checks=p['remaining'],reviewer='Codex-GroupB source assessment',date=TS[:10],second_vote='',final_decision='pending'))
 for i,reason in enumerate(p['ic'],1):
  tables['fulltext_criteria.csv'].append(dict(report_id=rid,criterion='IC'+str(i),source_anchor=p['anchor'],first_review_basis=reason,criterion_check_required=p['remaining'],reviewer='Codex-GroupB source assessment',status='AI_source_assessed;see_basis_for_uncertainty',independent_vote='',checker='',checked_at_utc=TS,final_decision='pending',doi=p['doi'],source_url=p['source_url']))
 for r in records:
  if r['canonical_record_id']==p['record_id']:tables['report_record_links.csv'].append(dict(report_id=rid,record_id=r['record_id'],canonical_record_id=p['record_id'],provisional_study_id=form['study_id'],doi=p['doi'],study_linkage_status=p['eligibility']))
 tables['report_validation_queue.csv'].append(dict(report_id=rid,title=p['title'],source=p['source_url'],eligibility_task=p['remaining'],outcome_task='Verify registered values, comparator and anchors',quality_task='Q1-Q10 independent check remains unperformed',checker='',checked_at_utc='',reconciliation_status='pending',final_decision='pending',doi=p['doi'],source_url=p['source_url']))
 tables['cycle3_retrieval.csv'].append(dict(candidate=p['pdf_file'].replace('.pdf',''),source_url=p['source_url'],checked_at_utc=TS,assessor='Codex-GroupB',retrieval_status='retrieved',sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),method='public primary conference/author PDF',assessment_status='AI_source_assessed;see_eligibility_and_version_status',licensed_source_in_git='no'))
for n,rows in tables.items():save(n,rows)
save('provisional_studies.csv',[{k:x[k] for k in ['report_id','title','doi','study_id','eligibility_status','source','source_anchor']}|{'final_decision':'pending'} for x in tables['study_extraction_form.csv']])
print(json.dumps(dict(report_forms=len(tables['study_extraction_form.csv']),qa_items=len(tables['quality.csv']),outcomes=len(tables['extraction.csv']))))

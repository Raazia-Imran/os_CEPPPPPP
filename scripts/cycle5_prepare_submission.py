"""Prepare compact submission views without silently finalizing selection."""
import csv,json,re,html,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R/'evidence';O=R/'task2/submission';O.mkdir(exist_ok=True)
def read(n):
 with (E/n).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def write(p,rows):
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
private=list(csv.DictReader((R.parent/'private_cycle3/records.csv').open()))
audit=[]
for r in private:
 a=r['abstract'];clean=re.sub(r'\s+',' ',html.unescape(a.replace('\x00',''))).strip()
 audit.append(dict(record_id=r['record_id'],canonical_record_id=r['canonical_record_id'],database=r['database'],original_characters=len(a),normalized_characters=len(clean),whitespace_or_entity_change=a!=clean,abstract_text_present=bool(a.strip()),completeness='unknown;snippet/full_abstract_not_verified',source_hash=r['source_hash']))
write(E/'abstract_cleaning_audit.csv',audit)
forms=read('study_extraction_form.csv');qa=read('quality.csv');ex=read('extraction.csv');s=read('screening.csv');rec=read('records.csv');du=read('duplicates.csv')
matrix=list(csv.DictReader((R/'task2/qa/qa_score_matrix.csv').open()));qmap={x['report_id']:x for x in matrix}
links=read('report_record_links.csv');study_map={}
for x in links:study_map.setdefault(x['canonical_record_id'],set()).add(x['provisional_study_id'])
log=read('cycle3_screening_log.csv')
for x in log:x['study_ids']=';'.join(sorted(study_map.get(x['record_id'],[]))) or 'not_assigned;selection_pending'
summary=[]
for f in forms:
 q=qmap[f['report_id']]
 summary.append(dict(report_id=f['report_id'],study_id=f['study_id'],title=f['title'],year=f['year'],doi=f['doi'],mechanism=f['mechanism'],gpu=f['gpu_hardware'],QA=q['raw_sum']+'/'+q['applicable_max'],outcome_rows=sum(x['report_id']==f['report_id'] for x in ex),eligibility=f['eligibility_status'],source=f['source'],anchor=f['source_anchor']))
issues=[dict(issue='Selection coverage',status='open',scope='2634 initial retain/uncertain records; 17 source-assessed reports, including 2 EC2 exclusions; final included studies pending',action='Complete source eligibility assessment; do not infer final study count from report forms.'),
 dict(issue='Reviewer method',status='documented deviation',scope='AI-only continuation authorized; human second fields blank',action='Disclose method and avoid claiming independent consensus.'),
 dict(issue='ParvaGPU version',status='open',scope='GB-P011 uses arXivv1; conference DOI identity recorded',action='Verify final publication text before included-study designation.'),
 dict(issue='REEF identity',status='open',scope='GB-P005 conference versus later journal companion',action='Map reports to study; do not substitute journal DOI.'),
 dict(issue='Missingness',status='explicit',scope='Unknown fields labelled not_extracted; absent reporting scoped to checked sections',action='Do not turn missing values into zeros or unqualified not_reported.'),
 dict(issue='Search gaps',status='open',scope='ACM79-file mapping;1600/1603 reported versus1582 imported;ScienceDirect MPS517displayed versus563exported',action='Keep both operator-reported and parsed counts; do not force agreement.'),
 dict(issue='Duplicate reconciliation',status='applied',scope='111 earlier links plus3 publisher-verified identity links=114',action='Preserve removed canonical screening rows and all vote events.'),
 dict(issue='Abstract cleaning',status='normalization audit complete; completeness not verified',scope=f'{sum(bool(x["abstract"].strip()) for x in private)}/{len(private)} occurrences have some abstract text',action='Originals preserved; whitespace/entity normalization does not establish complete abstracts.')]
tabs={'Search runs':read('database_query_audit.csv'),'Screening log':log,'Duplicates':read('cycle3_duplicate_ledger.csv'),
 'Study summary':summary,'Fulltext criteria':read('fulltext_criteria.csv'),'FT exclusions':read('fulltext_exclusions.csv'),'QA items':qa,'Study extraction':forms,'Outcomes':ex,'Calculations':read('calculated_outcomes.csv'),'Review issues':issues,'Abstract audit':audit}
for name,rows in tabs.items():write(O/(name.lower().replace(' ','_')+'.csv'),rows)
counts=dict(occurrences=len(rec),duplicate_links=len(du),canonical_records=len(s),preliminary_exclude=sum(x['reviewer_1_vote']=='exclude_recommendation' for x in s),retain_or_uncertain=sum(x['reviewer_1_vote']=='retain_or_uncertain' for x in s),source_assessed_reports=len(read('fulltext_checks.csv')),assessed_fulltext_exclusions=len(read('fulltext_exclusions.csv')),report_forms=len(forms),qa_items=len(qa),outcomes=len(ex),human_second_votes=sum(bool(x['reviewer_2_vote']) for x in s),final_included_studies=None)
(O/'submission_input.json').write_text(json.dumps(dict(counts=counts,tabs=tabs,qa_matrix=matrix),ensure_ascii=False)+'\n')
(O/'README.md').write_text('''# Group B submission files

Read GroupB_Review_Report.pdf first. GroupB_Submission_Workbook.xlsx contains the compact overview, executed search log, screening and duplicate logs, report summary, full-text criteria and assessed exclusions, Q1-Q10 items, study extraction, outcomes, calculations, issues and abstract audit. Separate GroupB_QA_Tables.pdf and GroupB_Data_Extraction.pdf contain paper-by-paper evidence. CSV copies are editable supporting registers.

The report is the current evidence checkpoint, not a completed final selection: all records have an automated first triage, but many remain uncertain and only the assessed source set has full-text forms. Seventeen reports have source assessments: two AI EC2 exclusions and fifteen QA/extraction forms. Fifteen report forms do not equal fifteen final included studies. ParvaGPU's accessed preprint remains version-uncertain. Final PRISMA stages are pending. Do not remove these limitations when submitting or describe unperformed independent review as complete.

The detailed audit workbook remains available separately. The compact workbook provides a simpler submission view; it does not discard the evidence history. Task1 remains unchanged. Raw licensed PDFs and full exported abstracts are deliberately outside the public repository.
''')
print(json.dumps(counts))

# Source queue excludes records already covered by a report assessment, without treating remaining records as eligible.
assessed_ids={x["canonical_record_id"] for x in links}
queue=[dict(record_id=x["record_id"],title=x["title"],doi=x["doi"],database=x["database"],recommendation=x["reviewer_1_vote"],status="awaiting_source_assessment;not_final_eligible") for x in s if x["reviewer_1_vote"]=="retain_or_uncertain" and x["record_id"] not in assessed_ids]
write(E/"source_assessment_queue.csv",queue)
print("Unassessed canonical retain/uncertain queue:",len(queue))

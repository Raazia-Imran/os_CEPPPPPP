"""Validate branch accounting, evidence joins and frozen integrity."""
from pathlib import Path
import csv,json,hashlib,datetime,collections
d=Path(__file__).resolve().parent;r=d.parents[1]
def rows(name):return list(csv.DictReader((d/name).open(newline='')))
baseline=list(csv.DictReader((r/'task3/logs/Remaining_559_Screening_Queue.csv').open(newline='')))
q=rows('Working_559_Queue.csv');lookup={x['Record ID']:x for x in q}
assert len(q)==len(lookup)==559
assert all(lookup[x['Record ID']][k]==v for x in baseline for k,v in x.items())
assert all(not x[k] for x in q for k in ['Independent decision','Independent criterion','Independent evidence anchor','Independent checked UTC','Adjudicated decision'])
screen=rows('Final_Screening_Decisions.csv');assert len(screen)==559
assert {x['Record ID'] for x in screen}==set(lookup)
excluded={x['Record ID'] for x in screen if x['Exclusion criterion']}
advanced=set(lookup)-excluded
assert len(excluded)==225 and len(advanced)==334
assert all(x['Missing abstract used as exclusion reason']=='No' for x in screen)
elig=rows('Final_Eligibility_Decisions.csv');inc=[x for x in elig if x['Final eligibility decision']=='Include'];exc=[x for x in elig if x['Final eligibility decision']=='Exclude']
assert len(inc)==7 and len(exc)==2 and len({x['Record ID'] for x in elig})==9
assert all(x['Record ID'] in advanced and x['Source SHA256'] and x['Source URL'].startswith('https://') and not x['Independent human vote'] for x in elig)
assert len({x['Study ID'] for x in inc})==7 and len({x['Report ID'] for x in inc})==7
qa=rows('Final_Candidate_QA.csv');outcomes=rows('Candidate_Outcomes_Prepared.csv');refs=rows('New_Included_References.csv');criteria=rows('Final_Eligibility_Criteria.csv')
assert len(qa)==70 and len(outcomes)==18 and len(refs)==7 and len(criteria)==42
for x in inc:
    rid=x['Record ID'];qq=[y for y in qa if y['Record ID']==rid]
    assert {y['Criterion'] for y in qq}=={'Q'+str(i) for i in range(1,11)}
    assert all(((y['Final source-based score']=='N/A' and int(y['Maximum'])==0) or (y['Final source-based score']!='N/A' and 0<=int(y['Final source-based score'])<=int(y['Maximum']))) and y['Rationale'] and y['PDF anchor'] for y in qq)
    assert {y['Criterion'] for y in criteria if y['Record ID']==rid}=={'IC'+str(i) for i in range(1,7)}
    ref=next(y for y in refs if y['Record ID']==rid)
    assert ref['DOI'].lower()==x['DOI'].lower() and ref['Primary evidence hash']==x['Source SHA256']
    assert any(y['Record ID']==rid and y['Anchor'] and y['Interpretation limit'] for y in outcomes)
snapshot=json.loads((d/'frozen_snapshot.json').read_text())
assert all(hashlib.sha256((r/path).read_bytes()).hexdigest()==sha for path,sha in snapshot['sha256'].items())
assert len(rows('Full_Text_Discovery_Routes.csv'))==334
audits=rows('methodology_corrections.csv');assert all(x['Evidence'] and x['Remaining gap'] for x in audits)
report=json.loads((d/'integrated_report/integration_summary.json').read_text())
workbook=json.loads((d/'integrated_workbook/workbook_validation.json').read_text())
assert report['working_studies']==27 and report['working_reports']==28 and report['QA_items']==270 and report['reported_outcomes']==70
assert workbook['counts']['studies']==27 and workbook['counts']['included_reports']==28 and workbook['live_QA_dependency_check']
assert all(x==0 for x in workbook['count_differences']+workbook['QA_differences'])
assert (d/'integrated_report/main.pdf').stat().st_size>100000
assert (d/'integrated_workbook/CEP_Task3_Working_Integrated_2026-10-23.xlsx').stat().st_size>100000
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'queue_records':559,'original_fields_unchanged':True,'human_votes_unchanged_and_empty':True,
    'final_screening_excluded':225,'final_screening_advanced':334,
    'new_final_inclusions':7,'new_full_text_exclusions':2,'advanced_records_open':325,
    'working_studies':27,'working_reports':28,'new_QA_rows':70,'new_outcomes':18,
    'new_references':7,'new_criteria':42,'frozen_hashes_unchanged':True,
    'whole_review_prisma_final':False,'new_report_workbook_integration_complete':True,
    'integration_scope':'Current27-study working snapshot;325advanced records still open'}
(d/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))

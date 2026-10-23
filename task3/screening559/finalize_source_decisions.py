"""Finalize inspected source decisions under the separately recorded process amendment.

This never fills independent human votes or modifies frozen artifacts.
"""
from pathlib import Path
import csv, json, datetime

d = Path(__file__).resolve().parent
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
mapping = {
    'R00080': ('S021', 'P024', 'LithOS'),
    'R00143': ('S022', 'P025', 'Abacus'),
    'R01089': ('S023', 'P026', 'Miriam'),
    'R00656': ('S024', 'P027', 'SGDRC'),
    'R00661': ('S025', 'P028', 'Pantheon'),
    'R00086': ('S026', 'P029', 'Oneiros'),
    'R00647': ('S027', 'P030', 'GACER'),
}
def read(name):
    return list(csv.DictReader((d / name).open(newline='')))
def write(name, rows):
    with (d / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

criteria = read('Full_Text_Eligibility_Prepared.csv')
sources = {x['Record ID']: x for x in read('Full_Text_Source_Register.csv')}
references=read('New_Included_References.csv')
mapping={x['Record ID']:(x['Study ID'],x['Report ID'],sources[x['Record ID']]['Candidate name']) for x in references}
qa = read('Candidate_QA_Prepared.csv')
outcomes = read('Candidate_Outcomes_Prepared.csv')
decisions = []
for rid, (sid, pid, name) in mapping.items():
    checks = [x for x in criteria if x['Record ID'] == rid]
    assert {x['Criterion'] for x in checks} == {'IC'+str(i) for i in range(1,7)}
    assert all(x['Prepared judgment'] == 'Meets criterion on inspected full text' for x in checks)
    assert len([x for x in qa if x['Record ID'] == rid]) == 10
    assert any(x['Record ID'] == rid for x in outcomes)
    source = sources[rid]
    decisions.append({'Record ID': rid, 'Study ID': sid, 'Report ID': pid,
        'Short name': name, 'Final eligibility decision': 'Include',
        'Basis': 'All IC1-IC6 met on inspected final primary text; see criterion-level source anchors',
        'DOI': source['DOI'], 'Source URL': source['Source URL'],
        'Source SHA256': source['Source SHA256'],
        'Decision method': 'Single automated source-based review; user-reported instructor permission; amendment M2026-10-23',
        'Independent human vote': '', 'Decided UTC': now,
        'Applied to frozen release': 'No',
        'Working integration status': 'Eligible addition; synthesis/report/workbook integration pending'})
exclusions=read('Full_Text_Exclusions.csv') if (d/'Full_Text_Exclusions.csv').exists() else []
write('Final_Eligibility_Decisions.csv', decisions+exclusions)
finalcriteria = []
for x in criteria:
    y = dict(x)
    y['Decision method'] = 'Single automated source-based review under M2026-10-23'
    y['Final criterion decision'] = 'Met'
    y['New study ID'] = mapping[x['Record ID']][0]
    y['Final checked UTC'] = now
    finalcriteria.append(y)
write('Final_Eligibility_Criteria.csv', finalcriteria)
finalqa = []
for x in qa:
    y = dict(x)
    y['Final source-based score'] = x['Prepared score']
    y['Decision method'] = 'Single automated source appraisal; no independent score asserted'
    y['Study ID'], y['Report ID'], _ = mapping[x['Record ID']]
    finalqa.append(y)
write('Final_Candidate_QA.csv', finalqa)
p = json.loads((d/'progress.json').read_text())
p.update({'final_source_based_eligibility_decisions': len(decisions)+len(exclusions),
    'final_full_text_exclusions':len(exclusions),
    'new_full_text_eligibility_assessments':len(decisions)+len(exclusions),
    'full_text_criteria_prepared':len(criteria),
    'candidate_QA_items_prepared':len(qa),
    'candidate_outcomes_prepared':len(outcomes),
    'candidate_studies_meeting_first_review_criteria':len(decisions),
    'candidate_QA_totals':{rid:sum(int(x['Prepared score']) for x in qa if x['Record ID']==rid and x['Prepared score']!='N/A') for rid in mapping},
    'new_included_studies': len(decisions), 'working_unique_studies': 20+len(decisions),
    'working_included_reports': 21+len(decisions), 'frozen_unique_studies': 20,
    'frozen_included_reports': 21, 'independent_human_votes': 0,
    'review_process_amendment': 'M2026-10-23',
    'prisma_changed': False, 'prisma_reconciliation_pending': True,
    'all_full_text_eligibility_closed': False})
(d/'progress.json').write_text(json.dumps(p, indent=2)+'\n')
print(f'{len(decisions)} final source-based inclusion decisions; working corpus{20+len(decisions)}studies/{21+len(decisions)}reports; frozen20/21 unchanged.')

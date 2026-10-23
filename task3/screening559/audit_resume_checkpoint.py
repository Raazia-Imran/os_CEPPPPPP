"""Reconcile the open queue and verify existing integration before status repair."""
from pathlib import Path
import csv, json, zipfile, hashlib, datetime

d = Path(__file__).resolve().parent
now = datetime.datetime.now(datetime.timezone.utc).isoformat()

def read(name):
    with (d / name).open(newline='') as f:
        return list(csv.DictReader(f))

def write(name, rows):
    with (d / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

queue = read('Working_559_Queue.csv')
screen = read('Final_Screening_Decisions.csv')
elig = read('Final_Eligibility_Decisions.csv')
excluded = {x['Record ID'] for x in screen if x['Exclusion criterion']}
closed = {x['Record ID'] for x in elig}
assert len(queue) == len({x['Record ID'] for x in queue}) == 559
assert not excluded & closed
open_rows = [x for x in queue if x['Record ID'] not in excluded | closed]
assert len(open_rows) == 321

report_text = '\n'.join(p.read_text() for p in (d / 'integrated_report').glob('*.tex'))
workbook = d / 'integrated_workbook/CEP_Task3_Working_Integrated_2026-10-23.xlsx'
with zipfile.ZipFile(workbook) as z:
    workbook_text = '\n'.join(z.read(n).decode() for n in z.namelist()
                              if n.endswith('.xml'))
verified = []
for row in elig:
    if row['Final eligibility decision'] != 'Include':
        continue
    assert row['Study ID'] in workbook_text and row['Report ID'] in workbook_text
    assert row['DOI'] in workbook_text and row['DOI'] in report_text
    row['Working integration status'] = 'Integrated in current working report and workbook; frozen release unchanged'
    verified.append(row['Record ID'])
write('Final_Eligibility_Decisions.csv', elig)

write('Open_Eligibility_Queue.csv', [{
    'Record ID': x['Record ID'], 'Database': x['Database'],
    'Title': x['Title'], 'DOI': x['DOI'], 'Year': x['Year'],
    'URL': x['URL'], 'Scope question': x['Preparation rationale'],
    'Next action': x['Preparation next action'],
    'Status': 'Open eligibility or report identity; not an exclusion',
} for x in open_rows])

result = {'checked_utc': now, 'screened': 559, 'screening_exclusions': len(excluded),
          'closed_eligibility': len(closed), 'open_eligibility_or_identity': len(open_rows),
          'integration_verified_by_report_DOI_and_workbook_ID_DOI': verified,
          'report_sha256': hashlib.sha256((d / 'integrated_report/main.pdf').read_bytes()).hexdigest(),
          'workbook_sha256': hashlib.sha256(workbook.read_bytes()).hexdigest(),
          'research_decisions_changed': False}
(d / 'RESUME_AUDIT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))

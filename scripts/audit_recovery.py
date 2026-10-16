"""Read-only research checks; writes a separate recovery audit receipt only."""
import csv, hashlib, json, subprocess, zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

R = Path(__file__).resolve().parents[1]
def rows(name):
    with (R / 'evidence' / (name + '.csv')).open() as f:
        return list(csv.DictReader(f))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
records, duplicates, screening = [rows(n) for n in ('records','duplicates','screening')]
manifest = rows('import_manifest')
by_id = {r['record_id']: r for r in records}
canonical = {r['canonical_record_id'] for r in records}
problems = []
if len(by_id) != len(records): problems.append('Repeated occurrence IDs')
if canonical != {r['record_id'] for r in screening}: problems.append('Canonical/screening ID mismatch')
for d in duplicates:
    if by_id[d['record_id']]['canonical_record_id'] != d['canonical_record_id']:
        problems.append('Duplicate link mismatch: ' + d['record_id'])
for m in manifest:
    if sha(R / m['source_file']) != m['sha256']: problems.append('Raw hash mismatch: '+m['source_file'])
    source = [r for r in records if r['source_file'] == m['source_file']]
    if len(source) != int(m['occurrences']): problems.append('Manifest count mismatch: '+m['source_file'])
votes = Counter(r['reviewer_1_vote'] or 'blank' for r in screening)
ns = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(R/'task2/tracker/review_workbook.xlsx') as z:
    bad = z.testzip()
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    sheets = [s.attrib['name'] for s in wb.find('s:sheets',ns)]
    errors=[]
    for n in z.namelist():
        if n.startswith('xl/worksheets/sheet') and n.endswith('.xml'):
            errors.extend((n,c.attrib['r']) for c in ET.fromstring(z.read(n)).findall('.//s:c',ns) if c.attrib.get('t')=='e')
from pypdf import PdfReader
pdf=PdfReader(R/'task2/report/report.pdf')
text='\n'.join(p.extract_text() or '' for p in pdf.pages)
baseline=json.loads((R/'evidence/cycle2_baseline.json').read_text())
original=subprocess.check_output(['git','show',baseline['baseline_commit']+':task1/submitted_protocol.pdf'],cwd=R)
result={
 'checked_at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),
 'inspected_main':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),
 'scope':'Cycle 1 recovery audit only; no import, screening, QA or extraction decisions changed',
 'occurrences':len(records),'database_split':dict(Counter(r['database'] for r in records)),
 'manifest_files':len(manifest),'manifest_occurrences':sum(int(m['occurrences']) for m in manifest),
 'applied_duplicate_links':len(duplicates),'canonical_records':len(canonical),
 'accounting_identity':len(records)-len(duplicates)==len(canonical),
 'recommendations':dict(votes),'final_decisions':dict(Counter(r['final_decision'] for r in screening)),
 'independent_title_votes_present':sum(bool(r['reviewer_2_vote']) for r in screening),
 'quality_forms':len({r['report_id'] for r in rows('quality')}),'quality_items':len(rows('quality')),
 'quality_criteria':sorted({r['criterion'] for r in rows('quality')}),
 'study_forms':len(rows('study_extraction_form')),'outcomes':len(rows('extraction')),
 'citation_events':len(rows('snowballing')),'version_pairs':len(rows('version_review_audit')),
 'version_dispositions':dict(Counter(r['audit_disposition'] for r in rows('version_review_audit'))),
 'submitted_protocol_unchanged':hashlib.sha256(original).hexdigest()==sha(R/'task1/submitted_protocol.pdf'),
 'cycle2_validation_exists_on_inspected_main':(R/'evidence/cycle2_validation.json').exists(),
 'published_report':{'pages':len(pdf.pages),'all_pages_text_readable':all(p.extract_text() for p in pdf.pages),'sha256':sha(R/'task2/report/report.pdf'),'contains_cycle2_taxonomy_heading':'Taxonomy of existing approaches' in text},
 'published_workbook':{'sheets':len(sheets),'names':sheets,'zip_integrity':bad is None,'stored_error_cells':errors,'sha256':sha(R/'task2/tracker/review_workbook.xlsx')},
 'problems':problems,
 'limitations':'File parsing verifies opening/structure, not a fresh Excel recalculation or complete visual QA. Missing final decisions remain pending.'
}
out=R/'task2/recovery_audit';out.mkdir(exist_ok=True)
(out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if problems or bad or errors or not result['accounting_identity']: raise SystemExit(1)

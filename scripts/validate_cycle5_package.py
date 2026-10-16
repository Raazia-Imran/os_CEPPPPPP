"""Verify joins, preservation, current artifacts and workbook caches; no research inference."""
import csv,json,hashlib,subprocess,io,zipfile,sys
from pathlib import Path
from collections import Counter
import lxml.etree as ET
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];E=R/'evidence';O=R/'task2/submission'
def read(p):return list(csv.DictReader(p.open(newline='',encoding='utf-8')))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rec=read(E/'records.csv');s=read(E/'screening.csv');du=read(E/'duplicates.csv');q=read(E/'quality.csv');ex=read(E/'extraction.csv');forms=read(E/'study_extraction_form.csv');checks=read(E/'fulltext_checks.csv');crit=read(E/'fulltext_criteria.csv');excl=read(E/'fulltext_exclusions.csv');queue=read(E/'source_assessment_queue.csv')
assert (len(rec),len(du),len(s))==(4189,114,4075)
assert len(rec)-len(du)==len(s)==len({r['record_id'] for r in s})
assert Counter(x['reviewer_1_vote'] for x in s)=={'exclude_recommendation':1441,'retain_or_uncertain':2634}
assert len(q)==150 and len(forms)==15 and len(ex)==45 and len(checks)==17 and len(crit)==102 and len(excl)==2 and len(queue)==2617
assert Counter(x['report_id'] for x in q)=={x['report_id']:10 for x in forms}
assert Counter(x['report_id'] for x in crit)=={x['report_id']:6 for x in checks}
assert all(not x['reviewer_2_vote'] for x in s)
assert all(not x['second_score'] and not x['reconciled_score'] for x in q)
assert len({x['outcome_id'] for x in ex})==45
assert all(x['source_anchor'] and x['value'] and x['units'] and x['baseline'] and x['workload'] for x in ex)
assert {x['criterion'] for x in excl}=={'EC2'}
assert sum(x['final_decision']=='AI_exclude_fulltext' for x in s)==2
baseline={}
for n,key in [('quality.csv',lambda x:(x['report_id'],x['criterion'])),('extraction.csv',lambda x:x['outcome_id']),('study_extraction_form.csv',lambda x:x['report_id'])]:
 old=list(csv.DictReader(io.StringIO(subprocess.check_output(['git','show','350fdc2:evidence/'+n],cwd=R,text=True))));idx={key(x):x for x in read(E/n)}
 assert all(all(x[k]==idx[key(x)].get(k) for k in x) for x in old),n
 baseline[n]=dict(rows=len(old),all_original_cells_preserved=True)
assert sha(R/'task1/submitted_protocol.pdf')=='cc1179c8f0e6656075e9d7e3f2b8da5d86e84f853af89a48f8dc7b87c39ac44d'
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def workbook(path):
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))] if 'xl/sharedStrings.xml' in z.namelist() else []
  rel={x.attrib['Id']:x.attrib['Target'].lstrip('/') for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
  sheets={};errors=[]
  for item in ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet',N):
   target=rel[item.attrib['{'+N['r']+'}id']];target=target if target.startswith('xl/') else 'xl/'+target
   root=ET.fromstring(z.read(target));cells={}
   for cell in root.findall('m:sheetData/m:row/m:c',N):
    val=cell.findtext('m:v','',N)
    if cell.attrib.get('t')=='s':val=strings[int(val)] if val else ''
    elif cell.attrib.get('t')=='inlineStr':val=''.join(cell.find('m:is',N).itertext())
    if cell.attrib.get('t')=='e':errors.append((item.attrib['name'],cell.attrib['r'],val))
    if val!='':cells[cell.attrib['r']]=val
   sheets[item.attrib['name']]=cells
  assert not errors,errors[:5]
  return sheets
checks_wb={}
workbook_paths=[('compact',O/'GroupB_Submission_Workbook.xlsx'),('public_detailed',R/'task2/tracker/review_workbook.xlsx')]
if '--public-only' not in sys.argv:workbook_paths.append(('private_detailed',R.parent/'private_cycle3/review_workbook.xlsx'))
for label,path in workbook_paths:
 b=workbook(path);assert len(b)==(13 if label=='compact' else 47)
 names={'Fulltext criteria':102,'FT exclusions':2,'QA items':150,'Study summary':15,'Outcomes':45,'Screening log':4075} if label=='compact' else {'Source checks':17,'Full-text criteria':102,'FT exclusions':2,'Quality':150,'Study extraction':15,'Extraction':45,'Screening log':4075}
 for n,expected in names.items():
  count=sum(k.startswith('A') and k[1:].isdigit() and int(k[1:])>1 for k in b[n]);assert count==expected,(label,n,count,expected)
 if label=='compact':
  assert [int(b['Overview']['B'+str(i)]) for i in range(4,12)]==[4189,114,4075,1441,2634,15,150,45]
  matrix={x['report_id']:x for x in read(R/'task2/qa/qa_score_matrix.csv')}
  for i in range(2,17):
   x=matrix[b['Study summary']['A'+str(i)]]
   assert float(b['Study summary']['H'+str(i)])==float(x['raw_sum'])
   assert float(b['Study summary']['M'+str(i)])==float(x['applicable_max'])
 else:
  assert int(b['Summary']['B11'])==17 and int(b['Summary']['B13'])==15
  abstract_col=next(k[:-1] for k,v in b['Records'].items() if k.endswith('1') and k[:-1].isalpha() and v=='abstract')
  abstracts=sum(k.startswith(abstract_col) and k[len(abstract_col):].isdigit() and int(k[len(abstract_col):])>1 for k in b['Records'])
  assert abstracts==(3658 if label=='private_detailed' else 0),(label,abstracts)
 checks_wb[label]=dict(sheets=len(b),formula_errors=0,sha256=sha(path),bytes=path.stat().st_size)
pdfs={}
for n,expected in [('GroupB_Review_Report.pdf',28),('GroupB_QA_Tables.pdf',17),('GroupB_Data_Extraction.pdf',37)]:
 p=O/n;doc=PdfReader(p);assert len(doc.pages)==expected,(n,len(doc.pages));text='\n'.join(x.extract_text() or '' for x in doc.pages);assert '[?]' not in text
 pdfs[n]=dict(pages=len(doc.pages),sha256=sha(p),bytes=p.stat().st_size)
assert sha(R/'task2/report/report.pdf')==sha(O/'GroupB_Review_Report.pdf')
r=dict(occurrences=4189,applied_duplicate_links=114,canonical_records=4075,initial_exclusion_proposals=1441,initial_retain_or_uncertain=2634,source_assessed_reports=17,assessed_EC2_exclusions=2,QA_extraction_forms=15,QA_items=150,reported_outcomes=45,separate_calculations=2,unassessed_canonical_candidate_queue=2617,independent_human_votes=0,final_included_studies=None,baseline_preservation=baseline,submitted_protocol_preserved=True,workbooks=checks_wb,pdfs=pdfs,limits=['Automated triage is not complete verified abstract screening.','15 forms are not 15 final included studies.','Final selection and PRISMA remain pending.','Visual previews inspected for changed workbook views and all PDF pages.'])
(E/'cycle5_package_validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))

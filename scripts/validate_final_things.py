from pathlib import Path
from collections import Counter
import csv,json,zipfile,hashlib,re,lxml.etree as ET
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];F=R/'final things'
def csvrows(p):return list(csv.DictReader(p.open(newline='')))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def workbook(p):
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None;strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))];rels={x.attrib['Id']:x.attrib['Target'].lstrip('/') for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))};tabs={}
  for item in ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet',N):
   target=rels[item.attrib['{'+N['r']+'}id']];target=target if target.startswith('xl/') else 'xl/'+target;cells={}
   for cell in ET.fromstring(z.read(target)).findall('m:sheetData/m:row/m:c',N):
    t=cell.attrib.get('t','');v=cell.findtext('m:v','',N);f=cell.findtext('m:f','',N)
    if t=='s':v=strings[int(v)] if v else ''
    assert t!='e',(item.attrib['name'],cell.attrib['r'],v)
    if v!='' or f:cells[cell.attrib['r']]=(v,f)
   tabs[item.attrib['name']]=cells
  return tabs
old=workbook(R/'task2/submission/GroupB_Submission_Workbook.xlsx');new=workbook(F/'04_Workbook_and_Logs/GroupB_Review_Workbook.xlsx');assert list(old)==list(new) and len(new)==13
# New date/method columns do not alter any pre-existing field, score, formula or value.
for tab,cells in old.items():
 for k,v in cells.items():assert new[tab].get(k)==v,(tab,k,v,new[tab].get(k))
log=new['Screening log'];headers={v[0]:k[:-1] for k,v in log.items() if k.endswith('1') and k[:-1].isalpha()}
assert 'study_ids' in headers and 'screening_timestamp_utc' in headers
missing=sum(v[0]=='Not recorded' for k,v in log.items() if re.fullmatch(headers['screening_timestamp_utc']+r'\d+',k));assert missing==798
assert [int(new['Overview']['B'+str(i)][0]) for i in range(4,12)]==[4189,114,4075,1441,2634,15,150,45]
cat=csvrows(F/'01_Statistics_and_Papers/CURRENT_ASSESSED_PAPERS_AND_DOIS.csv');assert len(cat)==15 and Counter(x['assessment_status'] for x in cat)=={'provisional':13,'companion_candidate':1,'publication_version_uncertain':1}
assert sum(x['doi'].startswith('10.') for x in cat)==6
assert digest(R/'task1/submitted_protocol.pdf')==digest(F/'05_Protocol_and_Audit/Submitted_Task1_Protocol.pdf')
for source in ['quality.csv','study_extraction_form.csv','extraction.csv','calculated_outcomes.csv']:assert digest(R/'evidence'/source)==digest(F/'03_QA_and_Extraction'/source)
pdfs={}
for rel,expected in [('01_Statistics_and_Papers/START_HERE_Statistics_and_Papers.pdf',3),('02_Report_LaTeX/GroupB_Review_Report.pdf',28),('03_QA_and_Extraction/GroupB_QA_Tables.pdf',17),('03_QA_and_Extraction/GroupB_Data_Extraction.pdf',37)]:
 p=F/rel;doc=PdfReader(p);assert len(doc.pages)==expected;assert '[?]' not in '\n'.join(x.extract_text() or '' for x in doc.pages);pdfs[rel]=dict(pages=len(doc.pages),sha256=digest(p))
report='\n'.join(x.extract_text() or '' for x in PdfReader(F/'02_Report_LaTeX/GroupB_Review_Report.pdf').pages);assert 'Group B mechanism taxonomy' in report and 'interim accounting' in report
source=(F/'02_Report_LaTeX/main.tex').read_text();assert source.count('begin{tikzpicture}')==2
r=dict(predecessor_main='5cb05fef5983707b79c25631c1e23105909debc7',scientific_registers_changed=False,existing_workbook_cells_and_formulas_preserved=True,workbook_tabs=13,missing_exact_event_times=missing,paper_forms=15,provisional_reports=13,unresolved_companion_or_version=2,assessed_exclusions=2,identified_dois=6,final_included_studies=None,source_qa_rows=150,reported_outcomes=45,separate_calculations=2,latex_undefined_citations=0,diagrams=2,pdfs=pdfs,all_final_selection_stages_complete=False)
(F/'05_Protocol_and_Audit/VALIDATION.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))

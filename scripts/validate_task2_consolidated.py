"""Technical validation of the consolidated interim package, not final eligibility."""
from pathlib import Path
import csv,json,re,hashlib,zipfile,xml.etree.ElementTree as ET,datetime,fitz
R=Path(__file__).resolve().parents[1];O=R/'final things/06_Task2_Submission';T=Path('/tmp/task2-consolidated-tex')
def read(p):return list(csv.DictReader(p.open(newline='')))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((R/'task2/qa/task2_consolidated_input.json').read_text());inv=json.loads((O/'table_inventory.json').read_text());qa=read(O/'data/qa_items.csv');forms=read(O/'data/study_extraction.csv');papers=read(O/'data/paper_list.csv');screen=read(O/'data/screening_log.csv');out=read(O/'data/outcomes.csv')
qaids=set(x['report_id'] for x in qa);formids=set(x['report_id'] for x in forms);expected={f'GB-P{i:03d}' for i in range(1,16)};assert qaids==formids==expected
assert len(papers)==17 and len(qa)==150 and len(forms)==15 and len(out)==45 and len(screen)==4075
assert len({x['record_id'] for x in screen})==4075
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(O/'GroupB_Task2_Workbook.xlsx') as z:
 wb=ET.fromstring(z.read('xl/workbook.xml'));sheets=wb.find('m:sheets',ns);names=[x.attrib['name'] for x in sheets];assert len(names)==13
 caches={};errors=[]
 for i,name in enumerate(names,1):
  root=ET.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'));cells={c.attrib['r']:c for c in root.findall('.//m:c',ns)};caches[name]=cells
  errors += [(name,k) for k,c in cells.items() if c.attrib.get('t')=='e']
 assert not errors
 def value(name,cell):return float(caches[name][cell].find('m:v',ns).text)
 for row,n in {4:4189,5:114,6:4075,8:1441,9:2634,10:17,11:15,12:150,13:45}.items():assert value('Overview',f'B{row}')==n
 for row,p in enumerate(papers[:15],2):
  qs=[x for x in qa if x['report_id']==p['report_id']];raw=sum(float(x['score']) for x in qs if x['score'] not in ['','N/A','NA']);maximum=sum(float(x['maximum']) for x in qs)
  assert value('Paper list',f'I{row}')==raw and value('Paper list',f'J{row}')==maximum
  assert abs(value('Paper list',f'K{row}')-raw/maximum)<1e-10
  assert value('Paper list',f'L{row}')==sum(x['report_id']==p['report_id'] for x in out)
log=(T/'main.log').read_text();assert not any(x in log for x in ['Overfull','Missing character','undefined','Fatal error'])
bib=(T/'main.bbl').read_text();assert len(re.findall(r'\\bibitem\{',bib))==23
aux=(T/'main.aux').read_text();assert re.search(r'newlabel\{core:end\}\{\{14\}\{24\}',aux)
doc=fitz.open(T/'main.pdf');joined=''.join(re.sub(r'\s+','',p.get_text()).replace('\u00ad','') for p in doc)
missing=[x['record_id'] for x in screen if x['record_id'] not in joined];assert not missing,missing[:5]
geometry=json.loads(Path('/tmp/task2-visual/geometry.json').read_text());assert geometry['pages']==len(doc) and not geometry['blank_pages'] and not geometry['outside_page_blocks']
assert sha(O/'Submitted_Task1_Protocol.pdf')=='cc1179c8f0e6656075e9d7e3f2b8da5d86e84f853af89a48f8dc7b87c39ac44d'
assert inv['source_cells_represented']==159545 and inv['bib_entries']==23
receipt=dict(checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Technical consolidation of an interim Task 2 record; not final eligibility validation',pdf_pages=len(doc),core_pdf_pages_including_cover_and_contents=25,headings='1-14',bibliography_entries=23,table_panels=inv['printed_panels'],source_cells_represented=inv['source_cells_represented'],glossary_values=inv['glossary_values'],workbook_tabs=names,workbook_formula_error_cells=errors,overview_cached_counts_reconciled=True,qa_totals_reconciled_reports=15,qa_extraction_id_sets_equal=True,canonical_ids_present_in_pdf=4075,missing_canonical_ids_in_pdf=missing,overfull_boxes=0,undefined_references=0,missing_characters=0,all_pages_rendered=True,blank_pages=[],outside_page_blocks=[],protocol_sha256=sha(O/'Submitted_Task1_Protocol.pdf'),initial_triage_coverage=1.0,independent_human_votes_recorded=0,final_included_studies=None,final_selection_complete=False,prisma_status='Interim adapted PRISMA 2020 categories; unfinished stages pending',scientific_counts_changed=False,remaining=['2617 retain/uncertain canonical candidates lack linked source assessment','Verified abstract/eligibility census and final report/study selection incomplete','REEF companion and ParvaGPU publication-version reconciliation','Search run mapping and historical hit/export provenance gaps','QA anchor and provisional N/A calibration follow-ups; unchecked extraction fields'])
(O/'VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:receipt[k] for k in ['pdf_pages','workbook_formula_error_cells','qa_extraction_id_sets_equal','canonical_ids_present_in_pdf','source_cells_represented','final_selection_complete']},indent=2))

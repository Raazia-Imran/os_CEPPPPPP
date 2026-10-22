from pathlib import Path
import json,zipfile,hashlib,datetime,csv
r=Path(__file__).resolve().parents[2];t=r/'task3';out=t/'team/Task3_Complete_First_Draft.zip';files={}
def add(p,name):
 if p.is_file():files[name]=p
 else:raise FileNotFoundError(p)
add(t/'report/main.pdf','01_Report/CEP_Task3_First_Draft.pdf');add(t/'report/CEP_Task3_First_Draft.docx','01_Report/CEP_Task3_First_Draft.docx');add(t/'workbook/CEP_Task3_Evidence_Workbook.xlsx','02_Master/CEP_Task3_Evidence_Workbook.xlsx')
for n in ['eshaal','raazia','rameen']:
 for p in (t/n).iterdir():
  if p.is_file() and p.suffix in ['.pdf','.docx','.xlsx','.csv','.json','.md','.bib','.py','.mjs'] and 'inspect' not in p.name:add(p,'03_Member_Reviews/'+n.capitalize()+'/'+p.name)
for fn in ['First_Draft_Team_Plan.pdf','First_Draft_Team_Plan.docx','First_Draft_Team_Plan.md','First_Draft_Status.json']:add(t/'team'/fn,'04_Team/'+fn)
for fn in ['methodology_corrections.csv','Remaining_559_Screening_Queue.csv','remaining_559_audit.json','integration_validation.json','export_archive_audit.json','final_first_draft_validation.json']:
 add(t/'logs'/fn,'05_Methodology/'+fn)
for p,name in [(r/'task1/submitted_protocol.pdf','Submitted_Task1_Protocol.pdf'),(t/'baseline/Instructor_Guideline.pdf','Instructor_Guideline.pdf'),(r/'docs/guidelines.md','guidelines.md'),(r/'docs/topics.md','topics.md'),(r/'evidence/protocol_amendments.md','protocol_amendments.md')]:add(p,'06_Protocol_and_Guidelines/'+name)
# Preserve the source-tree layout for audit/builds. Available raw exports are included; no missing archive is manufactured.
for subtree in ['logs','scripts','baseline','benchmark']:
 for p in (t/subtree).rglob('*'):
  if p.is_file() and p.suffix in ['.json','.csv','.md','.py','.mjs','.bib','.xlsx','.pdf','.png'] and not any(x in p.parts for x in ['previews','__pycache__']) and 'inspect' not in p.name:
   add(p,'07_Evidence_and_Reproducibility/source_tree/'+str(p.relative_to(r)))
for p in (t/'report').iterdir():
 if p.suffix in ['.tex','.bib']:add(p,'07_Evidence_and_Reproducibility/source_tree/'+str(p.relative_to(r)))
for p in (t/'papers').iterdir():
 if p.suffix in ['.json','.csv','.md']:add(p,'07_Evidence_and_Reproducibility/source_tree/'+str(p.relative_to(r)))
for p in (r/'evidence').rglob('*'):
 if p.is_file() and p.suffix in ['.csv','.json','.md','.ris','.bib','.txt']:
  add(p,'07_Evidence_and_Reproducibility/source_tree/'+str(p.relative_to(r)))
add(r/'task1/submitted_protocol.pdf','07_Evidence_and_Reproducibility/source_tree/task1/submitted_protocol.pdf')
for fn in ['guidelines.md','topics.md']:add(r/'docs'/fn,'07_Evidence_and_Reproducibility/source_tree/docs/'+fn)
readme='''# Complete Task 3 first-draft package

Open 01_Report/CEP_Task3_First_Draft.pdf first, then 04_Team/First_Draft_Team_Plan.pdf.

This ZIP contains the integrated CEP report (PDF/Word), current master workbook, all three individual packages, current team guide, methodology corrections, complete559-record work queue, preserved protocol/guidelines, frozen baseline, available search/export records and build sources. The original member-review-only ZIP is superseded.

Twenty unique primary studies meet the clarified20-study target. Twenty-one report copies include two REEF reports from one study. All200 included-study QA items,126 included-report inclusion checks and52 retained outcomes have source-review entries; source corrections are integrated.

Independent human source votes, the559 retained-record selection branch, historical search provenance and ParvaGPU final-text equivalence remain separately open. These are disclosed in the report and methodology_corrections.csv. Do not turn unknowns into exclusions or signatures.

Licensed third-party reading PDFs are excluded. Source identities, URLs, hashes and page anchors are included. Historical archive files that are missing from the checkout are explicitly recorded as unavailable; this package does not claim to contain them.

For reproducibility, source_tree preserves repository-relative paths. LaTeX sources are in source_tree/task3/report, and the unchanged protocol is in source_tree/task1. GitHub publication is proved by a verified publication receipt, not by this ZIP's existence. See the repository main-branch receipt for the latest commit.
'''
manifest=[{'file':n,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for n,p in sorted(files.items())]
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 z.writestr('START_HERE.md',readme);z.writestr('FILE_MANIFEST.json',json.dumps(manifest,indent=2))
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for expected in ['01_Report/CEP_Task3_First_Draft.pdf','02_Master/CEP_Task3_Evidence_Workbook.xlsx','03_Member_Reviews/Eshaal/Eshaal_Assigned_Review.pdf','03_Member_Reviews/Raazia/Raazia_Assigned_Review.pdf','03_Member_Reviews/Rameen/Rameen_Assigned_Review.pdf','05_Methodology/methodology_corrections.csv','06_Protocol_and_Guidelines/Submitted_Task1_Protocol.pdf']:assert expected in z.namelist()
 assert not any('/papers/P' in n and n.endswith(('.pdf','.txt')) for n in z.namelist())
receipt={'built_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'zip':str(out.relative_to(r)),'file_count':len(files)+2,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'required_artifacts_present':True,'third_party_reading_pdfs_excluded':True,'metadata':{'unique_studies':20,'included_reports':21,'qa_items':200,'outcomes':52,'retained_unassessed':559}}
(t/'logs/complete_package_validation.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))

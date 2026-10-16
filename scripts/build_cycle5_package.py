"""Assemble an organized checkpoint bundle; do not imply final study selection."""
from pathlib import Path
import json,csv,hashlib,zipfile,shutil
R=Path(__file__).resolve().parents[1];O=R/'task2/submission'
for name in ['taxonomy','comparative_matrix','trade_offs','conflicting_evidence','rq_synthesis','recommendations','evidence_gaps','validity','reference_catalog']:shutil.copy2(R/'evidence'/('cycle5_'+name+'.csv'),O/(name+'.csv'))
for a in ['qa_score_matrix.csv','qa_totals_summary.csv','qa_rationale_table.csv']:shutil.copy2(R/'task2/qa'/a,O/a)
for src,dest in [('evidence/cycle5_package_validation.json','validation.json'),('evidence/prisma_counts.json','prisma_counts.json'),('task2/HEADING_14_AUDIT.csv','requirements_audit.csv')]:shutil.copy2(R/src,O/dest)
files=[p for p in O.iterdir() if p.is_file() and p.suffix in ['.pdf','.xlsx','.csv','.md','.tex','.bib','.json'] and p.name not in ['submission_input.json','PACKAGE_MANIFEST.json']]
def category(p):
 n=p.name
 if n=='README.md':return n
 if n in ['GroupB_Review_Report.pdf','GroupB_Review_Report.tex','references.bib']:return '01_Report/'+n
 if n.endswith('.xlsx'):return '02_Workbook/'+n
 if n.startswith('qa_') or n.startswith('QA_') or n=='GroupB_QA_Tables.pdf':return '03_Quality_assessment/'+n
 if n in ['GroupB_Data_Extraction.pdf','study_summary.csv','study_extraction.csv','outcomes.csv','calculations.csv']:return '04_Data_extraction/'+n
 if n in ['GroupB_Submitted_Task1_Protocol.pdf','protocol_amendments.md']:return '06_Protocol/'+n
 if n in ['taxonomy.csv','comparative_matrix.csv','trade_offs.csv','conflicting_evidence.csv','rq_synthesis.csv','recommendations.csv','evidence_gaps.csv','validity.csv','reference_catalog.csv']:return '07_Synthesis/'+n
 if n in ['validation.json','requirements_audit.csv','review_issues.csv']:return '08_Validation/'+n
 return '05_Search_and_selection_logs/'+n
manifest={category(p):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(files)}
(O/'PACKAGE_MANIFEST.json').write_text(json.dumps(dict(status='Current evidence checkpoint; final selection incomplete',files=manifest),indent=2)+'\n')
p=O/'GroupB_Submission_Package.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(files):z.write(f,category(f))
 z.write(O/'PACKAGE_MANIFEST.json','PACKAGE_MANIFEST.json')
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 for name,entry in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==entry['sha256']
print('Verified package files',len(manifest)+1,'bytes',p.stat().st_size)

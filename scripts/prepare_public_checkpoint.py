"""Prepare a metadata-only publication view; retain full local originals unchanged."""
from pathlib import Path
import subprocess,csv,shutil,json
R=Path(__file__).resolve().parents[1];O=Path('/tmp/oscep-public')
changed=subprocess.check_output(['git','diff','--name-only','cb8251a','HEAD'],cwd=R,text=True).splitlines()
changed+=subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines()
changed+=['scripts/build_detailed_team_guide.py','scripts/prepare_public_checkpoint.py','task2/status_review/Task2_Detailed_Team_Guide.docx','task2/status_review/Task2_Detailed_Team_Guide.pdf','evidence/workbook_refresh_validation.json','task2/PUBLIC_CHECKPOINT.md']
for name in sorted(set(changed)):
 if 'incoming_shared/sciencedirect_' in name or name=='task2/tracker/review_workbook.xlsx':continue
 src=R/name
 if not src.is_file():continue
 dest=O/name;dest.parent.mkdir(parents=True,exist_ok=True)
 if name=='evidence/records.csv':
  rows=list(csv.DictReader(src.open()));fields=list(rows[0])
  for row in rows:row['abstract']=''
  with dest.open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 else:shutil.copy2(src,dest)
print('Metadata-only files prepared:',len(list(O.rglob('*'))))

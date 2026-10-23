"""Merge the dated assessed draft with preserved submission evidence."""
from pathlib import Path
import csv, json, zipfile, hashlib, shutil, datetime

d=Path(__file__).resolve().parent
repo=d.parents[1]
release=repo/'task3/release_2026-10-23'
release.mkdir(exist_ok=True)
public=release/'Task3_First_Draft_Public_2026-10-23.zip'
private=Path('/workspace/scratch/18d5426b12a3/Task3_Complete_First_Draft_2026-10-23.zip')
old=repo/'task3/team/Task3_Complete_First_Draft.zip'
oldsha=hashlib.sha256(old.read_bytes()).hexdigest()
artifacts={
 '01_Report/CEP_Task3_First_Draft.pdf':d/'integrated_report/main.pdf',
 '01_Report/CEP_Task3_First_Draft.docx':d/'integrated_report/CEP_Task3_Integrated_First_Draft.docx',
 '02_Master/CEP_Task3_Evidence_Workbook.xlsx':d/'integrated_workbook/CEP_Task3_Working_Integrated_2026-10-23.xlsx',
 '04_Team/Current_Handover.md':d/'RELEASE_HANDOVER.md',
 '04_Team/Team_Correction_Inbox.csv':d/'Team_Correction_Inbox.csv',
}
for name,p in list(artifacts.items()):
    dest=release/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
for p in d.iterdir():
    if p.suffix in ['.csv','.json'] and p.is_file():artifacts['05_Methodology/Current/'+p.name]=p
for p in d.rglob('*'):
    if p.is_file() and p.suffix in ['.py','.mjs','.csv','.json','.md','.tex','.bib','.xlsx'] and not any(x in p.parts for x in ['previews','__pycache__']) and p.name!='integrated_workbook_data.json':
        artifacts['07_Evidence_and_Reproducibility/source_tree/'+str(p.relative_to(repo))]=p
artifacts['07_Evidence_and_Reproducibility/source_tree/task3/workbook/CEP_Task3_Evidence_Workbook.xlsx']=repo/'task3/workbook/CEP_Task3_Evidence_Workbook.xlsx'
artifacts['07_Evidence_and_Reproducibility/source_tree/AGENTS.md']=repo/'AGENTS.md'
summary=json.loads((d/'integrated_report/integration_summary.json').read_text())
access=list(csv.DictReader((d/'Release_Reading_Copy_Access.csv').open()))
assert len(access)==10 and all(x['PDF available in private bundle']=='Yes' and x['Matches assessed source']=='Yes' for x in access)
for x in access:
    p=Path('/workspace/scratch/18d5426b12a3/private_reading/release')/(x['Study ID']+'_'+x['Report ID']+'.pdf')
    assert hashlib.sha256(p.read_bytes()).hexdigest()==x['Assessment source SHA256']
readme='''# Complete first draft 23 October 2026

Open 01_Report/CEP_Task3_First_Draft.pdf and use the matching Word companion and 02_Master workbook. This successor package integrates ten additions into the original frozen submission. The assessed corpus is 30 unique studies across 31 reports, with 300 QA items, 90 reported observations and two separate calculations.

All 559 continuation records have screening decisions. At the stated first-draft cutoff, 320 advanced records remain deferred for eligibility or identity. They are not exclusions or failed retrievals. Whole-review PRISMA and historical search-provenance limits remain explicit. This is the complete dated first-draft package, not a claim that the wider selection census is finished.

Use 04_Team/Current_Handover.md. Review the new master together. Transfer completed checks from older copies by paper ID. Earlier member packages and methodology snapshots are explicitly under Historical_Baseline and retain their original counts. They are evidence of previous work, not competing current masters. The previous frozen ZIP remains unchanged in the repository.

The public package contains source URLs, DOIs, hashes and assessment records. The private complete bundle additionally contains ten reading PDFs in 08_Added_Paper_PDFs, all hash-matched to the assessed sources. Do not publish those reading copies to the public repository. Original source copies for earlier studies retain the access status recorded in their source register; this package does not claim newly recovered PDFs for all original studies.

Reproducibility source_tree preserves the original report/workbook inputs and current build sources. Finalized CSV registers allow report/workbook rebuilding without the private reading files. Historical source builders may refer to their original local reading paths; source hashes and access URLs identify those inputs.
'''
(release/'START_HERE.md').write_text(readme)
manifest=[]
with zipfile.ZipFile(public,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.writestr('START_HERE.md',readme)
    with zipfile.ZipFile(old) as frozen:
        for item in frozen.infolist():
            n=item.filename
            if n in ['START_HERE.md','FILE_MANIFEST.json'] or n.startswith(('01_Report/','02_Master/','04_Team/')):continue
            if n.startswith('03_Member_Reviews/'):n=n.replace('03_Member_Reviews/','03_Member_Reviews/Historical_Baseline/',1)
            if n.startswith('05_Methodology/'):n=n.replace('05_Methodology/','05_Methodology/Historical_Baseline/',1)
            b=frozen.read(item);z.writestr(n,b)
            manifest.append({'file':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    for n,p in sorted(artifacts.items()):
        z.write(p,n);manifest.append({'file':n,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    z.writestr('FILE_MANIFEST.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(public) as z:assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
with zipfile.ZipFile(private,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    with zipfile.ZipFile(public) as pub:
        for item in pub.infolist():z.writestr(item,pub.read(item))
    for x in access:
        name=x['Study ID']+'_'+x['Report ID']+'.pdf'
        z.write('/workspace/scratch/18d5426b12a3/private_reading/release/'+name,'08_Added_Paper_PDFs/'+name)
with zipfile.ZipFile(private) as z:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if n.startswith('08_Added_Paper_PDFs/')])==10
assert hashlib.sha256(old.read_bytes()).hexdigest()==oldsha
receipt={'built_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'working_studies':30,'working_reports':31,'QA_items':300,'outcomes':90,'deferred_eligibility':320,'added_reading_PDFs':10,'all_added_PDF_hashes_match':True,'old_frozen_zip_unchanged':True,'public_reading_PDFs_excluded':True,'public_zip_sha256':hashlib.sha256(public.read_bytes()).hexdigest(),'private_zip_sha256':hashlib.sha256(private.read_bytes()).hexdigest(),'public_bytes':public.stat().st_size,'private_bytes':private.stat().st_size,'public_file_count':len(manifest)+2}
(release/'RELEASE_VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))

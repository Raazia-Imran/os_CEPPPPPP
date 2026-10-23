"""Create a current submission folder, portable LaTeX folder and team guide."""
from pathlib import Path
import csv, json, shutil, hashlib, datetime, zipfile
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

d=Path(__file__).resolve().parent
repo=d.parents[1]
submission=repo/'Task3_First_Draft_2026-10-24'
latex=repo/'Task3_LaTeX_2026-10-24'
for p in [submission,latex]:p.mkdir(exist_ok=True)
def write_csv(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def read(name):return list(csv.DictReader((d/name).open()))
def copy(p,to):to.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,to)
summary=json.loads((d/'integrated_report/integration_summary.json').read_text())
assert (summary['working_studies'],summary['working_reports'],summary['QA_items'],summary['reported_outcomes'])==(30,31,300,90)

# Repair stale navigation metadata without rewriting historical assessments.
p=d/'progress.json';v=json.loads(p.read_text())
v.update({'remaining_advanced_records':320,'integration_scope':'Current 30-study/31-report first draft; 320 advanced records deferred',
          'working_QA_items':300,'working_reported_outcomes':90,'reference_additions':10,
          'metadata_reconciled_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
p.write_text(json.dumps(v,indent=2)+'\n')
(d/'START_HERE.md').write_text('# Current first draft\n\nUse Task3_First_Draft_2026-10-24 for the PDF, Word report, Excel master and team guide. Use Task3_LaTeX_2026-10-24 for self-contained report sources. Current evidence: 30 studies / 31 reports, 300 QA items, 90 outcomes. All 559 continuation screening decisions are recorded; 320 advanced eligibility/identity records remain deferred. The full SLR is not complete. Older frozen packages are historical backups.\n')
rows=read('Heading_15_26_Integration_Checklist.csv')
for row in rows:
    for k in row:row[k]=row[k].replace('29-study','30-study').replace('323advanced','320 advanced').replace('323 advanced','320 advanced')
    if row['Heading']=='23':row['Remaining condition']='Team checking, final eligibility/PRISMA and historical search-provenance closure remain'
    if row['Heading']=='24':row['Current snapshot status']='All 13 sections present';row['Remaining condition']='Team review and any evidence corrections before submission'
write_csv(d/'Heading_15_26_Integration_Checklist.csv',rows)

copy(d/'integrated_report/main.pdf',submission/'01_Report/CEP_Task3_First_Draft.pdf')
copy(d/'integrated_report/CEP_Task3_Integrated_First_Draft.docx',submission/'01_Report/CEP_Task3_First_Draft.docx')
copy(d/'integrated_workbook/CEP_Task3_Working_Integrated_2026-10-23.xlsx',submission/'02_Master/CEP_Task3_Evidence_Workbook.xlsx')
copy(repo/'task1/submitted_protocol.pdf',submission/'06_Protocol_and_Guidelines/Submitted_Protocol.pdf')
copy(Path('/workspace/scratch/18d5426b12a3/upload/CEP_Operating_Systems_guideline(5).pdf'),submission/'06_Protocol_and_Guidelines/Instructor_Guideline.pdf')

payload=json.loads((d/'integrated_workbook/integrated_workbook_data.json').read_text())
for name,matrix in {**payload['data'],**payload['analysis']}.items():
    target=submission/'03_Data_and_Logs'/(''.join(c if c.isalnum() else '_' for c in name)+'.csv')
    target.parent.mkdir(exist_ok=True)
    with target.open('w',newline='') as f:csv.writer(f).writerows(matrix)
for n in ['Final_Screening_Decisions.csv','Final_Eligibility_Decisions.csv','Final_Eligibility_Criteria.csv',
          'Final_Candidate_QA.csv','Candidate_Outcomes_Prepared.csv','New_Included_References.csv',
          'Full_Text_Source_Register.csv','Release_Reading_Copy_Access.csv','Open_Eligibility_Queue.csv',
          'PRISMA_Branch_Accounting.json','Heading_15_26_Integration_Checklist.csv','methodology_corrections.csv',
          'VALIDATION.json','RESUME_AUDIT.json']:
    copy(d/n,submission/'03_Data_and_Logs'/n)

for p in (d/'integrated_report').iterdir():
    if p.suffix in ['.tex','.bib'] or p.name=='main.pdf':copy(p,latex/p.name)
for p in (d/'integrated_report/figures').iterdir():copy(p,latex/'figures'/p.name)
(latex/'build.sh').write_text('''#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
''')
(latex/'build.ps1').write_text('''$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
& pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) { throw "First LaTeX pass failed" }
& bibtex main
if ($LASTEXITCODE -ne 0) { throw "BibTeX failed" }
1..2 | ForEach-Object {
  & pdflatex -interaction=nonstopmode -halt-on-error main.tex
  if ($LASTEXITCODE -ne 0) { throw "LaTeX pass failed" }
}
''')
(latex/'.latexmkrc').write_text('$pdf_mode = 1;\n$bibtex_use = 2;\n')
(latex/'.gitignore').write_text('*.aux\n*.log\n*.out\n*.toc\n*.blg\n*.bbl\n*.fls\n*.fdb_latexmk\n')
(latex/'README.md').write_text('''# Task 3 LaTeX project

This self-contained project produces the 30-study/31-report first draft. Its evidence snapshot is dated 23 October; this portable folder was packaged on 24 October. The report explicitly retains 320 deferred eligibility/identity records.

## Overleaf
1. Download the separate LaTeX ZIP.
2. Open Overleaf, select New Project, then Upload Project and choose that ZIP.
3. Select main.tex as the main document and pdfLaTeX as compiler.
4. Click Recompile. Download the PDF after references and contents settle.

## Windows with MiKTeX or TeX Live
Install a LaTeX distribution first. Extract the ZIP, open a terminal in this folder and run the four commands below. The PowerShell helper build.ps1 runs the same sequence if your local execution policy permits scripts.

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

On Linux or macOS with TeX Live, run sh build.sh. No private reading PDF or workbook is required to compile the report. figures/Frozen_PRISMA.pdf is a generated historical review diagram, not a licensed research paper.

## Files to edit
main.tex contains the cover, abstract and document setup. body.tex contains the thirteen main sections and inputs the comparison files. taxonomy.tex, comparisons.tex, recommendations.tex and gaps.tex hold the corresponding tables and extensions. validity.tex holds the validity table. corpus.tex holds the study catalogue. counts.tex holds the selection table. appendices.tex holds detailed evidence cards. references.bib holds bibliography entries.

Edit citations in references.bib and cite their keys in the relevant TeX file. Rebuild the PDF after every accepted change. The report PDF is generated from LaTeX; editing Word does not update it. Send Word review comments to Raazia for application to these sources. Changing source code alone never establishes a new screening or eligibility decision.
''')

refs=read('New_Included_References.csv')
elig={x['Record ID']:x for x in read('Final_Eligibility_Decisions.csv')}
owner={'S021':'Eshaal','S022':'Rameen','S023':'Eshaal','S024':'Rameen','S025':'Eshaal',
       'S026':'Rameen','S027':'Eshaal','S028':'Rameen','S029':'Eshaal','S030':'Rameen'}
names={x['Study ID']:elig[x['Record ID']]['Short name'] for x in refs}
new=[]
for x in refs:
    new.append({'Study ID':x['Study ID'],'Report ID':x['Report ID'],'Paper':names[x['Study ID']],
                'DOI':x['DOI'],'Suggested checker':owner[x['Study ID']],
                'PDF in private bundle':'05_Added_Paper_PDFs/'+x['Study ID']+'_'+x['Report ID']+'.pdf',
                'QA rows':10,'Eligibility criteria':6,
                'Outcome rows':sum(y['Record ID']==x['Record ID'] for y in read('Candidate_Outcomes_Prepared.csv')),
                'Current decision':'Include; source assessed','Independent check':'Not recorded by this guide'})
write_csv(submission/'04_Team/New_Paper_Map.csv',new)
tasks=[]
for x in new:
    for category,items in [('Publication and DOI',['First page and DOI']),('Eligibility',['IC'+str(i) for i in range(1,7)]),('QA',['Q'+str(i) for i in range(1,11)]),('Report claim',['Main finding and its recommendation'])]:
        for item in items:tasks.append({'Checker':x['Suggested checker'],'Study ID':x['Study ID'],'Report ID':x['Report ID'],'Paper':x['Paper'],'Check type':category,'Item':item,'Status':'Not yet checked','Source page or table':'','Finding or correction':'','Checked by':'','Checked date':''})
    for y in read('Candidate_Outcomes_Prepared.csv'):
        if y['Record ID']==next(r['Record ID'] for r in refs if r['Study ID']==x['Study ID']):tasks.append({'Checker':x['Suggested checker'],'Study ID':x['Study ID'],'Report ID':x['Report ID'],'Paper':x['Paper'],'Check type':'Outcome','Item':y['Outcome ID'],'Status':'Not yet checked','Source page or table':y['Anchor'],'Finding or correction':'','Checked by':'','Checked date':''})
write_csv(submission/'04_Team/Independent_Check_Queue.csv',tasks)
for person in ['Eshaal','Rameen']:write_csv(submission/('04_Team/'+person+'_Checks.csv'),[x for x in tasks if x['Checker']==person])
copy(d/'Team_Correction_Inbox.csv',submission/'04_Team/Team_Correction_Inbox.csv')

requirements=[
 ('1','Final SLR report','01_Report PDF and Word','Draft prepared','Team review and wider selection limits remain'),
 ('2','Defined engineering problem','Report section 1','Present','Check the local single-GPU boundary'),
 ('3','Research objectives','Report section 1','Present','Check consistency with the protocol'),
 ('4','Three to five RQs','Report section 2','Present','Five RQs; each must have a synthesis answer'),
 ('5','SLR protocol','06_Protocol_and_Guidelines and methodology','Present','Original unchanged; deviations are separate'),
 ('6','Databases and justification','Report section 3 and Search_Log.csv','Present','Check named resources and actual coverage'),
 ('7','Exact search strings','Report appendix and search register','Partly closed','Historical fields and run/export mapping are incomplete'),
 ('8','Inclusion and exclusion criteria','Report section 3 and Eligibility.csv','Present','Apply the same six criteria to each added paper'),
 ('9','Database wise search results','Search_Log.csv and report section 4','Partly closed','Historical displayed/exported counts need evidence'),
 ('10','Search and screening log','Screening_Log.csv and Final_Screening_Decisions.csv','Partly closed','559 continuation screening decisions complete; 320 advanced eligibility/identity cases deferred'),
 ('11','Duplicate removal record','Duplicate_Removal.csv and identity audit','Documented with limits','114 links applied; unresolved companion/native identities remain'),
 ('12','PRISMA flow diagram','Report section 4 and counts.tex','Partly closed','Historical flow and current branch accounting are labelled; whole-review flow is not final'),
 ('13','QA checklist and scores','Master QA and Final_Candidate_QA.csv','Source appraisals present','300 items; independent checking must be recorded only when done'),
 ('14','Included primary studies','Master Studies and Source_Register.csv','Assessed set present','30 studies / 31 reports; ParvaGPU source-version condition and wider coverage remain'),
 ('15','Extraction sheet','Master Extraction and Evidence','Present','30 study forms; 90 observations plus two separate calculations'),
 ('16','Taxonomy','Report section 5 and Taxonomy.csv','Present','Classify mechanisms and implementation layers correctly'),
 ('17','Comparative evidence matrix','Report section 7 and Comparability.csv','Present','Preserve workload, hardware and baseline conditions'),
 ('18','Engineering trade offs','Report section 8','Present','Connect each benefit to a cost or limitation'),
 ('19','Conflicting evidence','Report section 9 and comparison tables','Present','Retain adverse results and explain unlike experiments'),
 ('20','Answers to all RQs','Report section 6','Present','Verify source support for each conclusion'),
 ('21','Engineering recommendation','Report section 10 and Recommendations.csv','Present','State choice, conditions, evidence, benefit, sacrifice and alternative'),
 ('22','Research gaps','Report section 11 and Research_Gaps.csv','Present','Scope gaps to reviewed evidence'),
 ('23','Threats to validity','Report section 12 and Validity.csv','Present','Retain incomplete selection and provenance limits'),
 ('24','Complete references','Report references and references.bib','Present with version limits','Ten added DOIs were found in their source PDFs; check original source-version cautions'),
 ('25','Supporting verification files','03_Data_and_Logs and repository history','Present with limits','Original exports and historic gaps retain their actual status')]
write_csv(submission/'04_Team/Guideline_23_Deliverables.csv',[dict(zip(['Deliverable','Requirement','Location','Status','Team action or remaining limit'],x)) for x in requirements])

doc=Document()
for sec in doc.sections:
    sec.page_width=Inches(8.5);sec.page_height=Inches(11)
    sec.top_margin=sec.bottom_margin=Inches(.7);sec.left_margin=sec.right_margin=Inches(.75)
for st in doc.styles:
    if st.type==1:
        st.font.name='Arial';st.font.size=Pt(11)
        st.font.color.rgb=RGBColor(0,0,0)
        st.paragraph_format.space_after=Pt(6);st.paragraph_format.line_spacing=1.05
doc.styles['Title'].font.size=Pt(23)
for name,size in [('Heading 1',16),('Heading 2',13)]:
    doc.styles[name].font.size=Pt(size);doc.styles[name].font.bold=True
def para(t,style=None):return doc.add_paragraph(t,style)
def head(t):doc.add_heading(t,1)
def table(headers,rows,widths=None):
    t=doc.add_table(rows=1,cols=len(headers));t.autofit=False
    for cell,text in zip(t.rows[0].cells,headers):cell.text=text
    for r in rows:
        for cell,text in zip(t.add_row().cells,r):cell.text=str(text)
    pr=t._tbl.tblPr;b=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        n=OxmlElement('w:'+edge);n.set(qn('w:val'),'single');n.set(qn('w:sz'),'4');n.set(qn('w:color'),'D9D9D9');b.append(n)
    pr.append(b)
    for i,row in enumerate(t.rows):
        if i==0:
            n=OxmlElement('w:tblHeader');row._tr.get_or_add_trPr().append(n)
        for j,c in enumerate(row.cells):
            if widths:c.width=Inches(widths[j])
            if i==0 or i%2==0:
                n=OxmlElement('w:shd');n.set(qn('w:fill'),'E8EDF2' if i==0 else 'F5F7F9');c._tc.get_or_add_tcPr().append(n)
            c.vertical_alignment=1
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(4)
                for r in p.runs:r.font.size=Pt(10);r.bold=(i==0)
    return t
para('Task 3 First Draft Team Guide','Title')
para('GPU sharing for multi-tenant inference | Prepared 24 October 2026')
para('Use the new 30-study package for all further checking. Keep the two older ZIPs as backups. We have assembled the report and supporting evidence, but we have not completed every full-text eligibility decision in the wider review. This guide explains what changed, where each file is, and exactly what to check before the Sunday 25 October submission.')
head('What is complete and what is still open')
table(['Measure','Verified position'],[
 ('Older shared package','20 unique studies, 21 reports, 200 QA items and 52 outcome rows'),
 ('Current assessed package','30 unique studies, 31 reports, 300 QA items and 90 outcome rows'),
 ('New papers','10 additions; each has six eligibility checks, ten QA items, extraction and a reference entry'),
 ('Source PDFs','All ten added PDFs recovered and matched to their assessment hashes'),
 ('Continuation screening','559 of 559 decisions recorded: 225 excluded and 334 advanced'),
 ('Continuation eligibility','14 of 334 advanced records closed: 10 included and four excluded; 320 deferred'),
 ('Full SLR completion','Incomplete eligibility, historical search provenance and independent checking remain')],[2.0,4.9])
para('The earlier 100% referred to assembling a bounded draft package. It did not mean that the entire SLR or every guideline requirement was fully closed. There is no defensible single percentage for all research work because the remaining records differ in effort and evidence availability.')
para('A record is a database entry. A report is a paper version. A study is the underlying investigation. The two linked REEF reports count as one study, which is why 31 reports represent 30 studies.')
para('Screening-stage completion does not mean that every abstract was available. The report identifies title or metadata-only decisions and 163 records without recovered abstract text. Evidence levels remain explicit in the screening log.')
doc.add_page_break();head('Which files to use now')
table(['File or folder','Use'],[
 ('01_Report/CEP_Task3_First_Draft.pdf','Read the current typeset report. Use its printed sections and study IDs for comments.'),
 ('01_Report/CEP_Task3_First_Draft.docx','Leave review comments or tracked edits. Word edits do not automatically update LaTeX.'),
 ('02_Master/CEP_Task3_Evidence_Workbook.xlsx','Use this database as the current master. The older database is a historical backup.'),
 ('03_Data_and_Logs','CSV copies of the main tables, screening decisions, criteria, QA, references and remaining queue.'),
 ('04_Team','This guide, paper map, deliverable checklist, individual check queues and correction inbox.'),
 ('05_Added_Paper_PDFs','Ten source PDFs in the private team ZIP. Public GitHub contains source links and hashes instead.'),
 ('06_Protocol_and_Guidelines','Original submitted protocol and the exact guideline PDF shared in this chat.'),
 ('Task3_LaTeX_2026-10-24','Separate runnable LaTeX project. Upload its ZIP to Overleaf or use the build commands in its README.')],[2.5,4.4])
para('The new folders supersede the two older ZIPs for editing. Previous checks are still useful: copy a correction by study/report ID into the current correction inbox. Do not silently replace the new master with an older workbook.')
head('How to open and start')
for step,s in enumerate(['Download and extract the new team ZIP. Keep its folders together.',
          'Open this guide, then open the report PDF and the master workbook.',
          'In Excel, open Studies. Search your study ID, for example S028. Read its report ID, DOI and QA denominator.',
          'Open the matching source PDF from 05_Added_Paper_PDFs using the paper map.',
          'Open your Eshaal_Checks.csv or Rameen_Checks.csv. These are blank check records; they are not claims that you already verified anything.',
          'Read the source anchor, compare it with the recorded claim and enter an actual finding. Return the completed CSV and any Word comments to Raazia.'],1):
    para(str(step)+'. '+s)
doc.add_page_break();head('The ten papers added after the frozen version')
table(['Study and report','Paper','Checker','Outcomes'],[(x['Study ID']+' / '+x['Report ID'],x['Paper'],x['Suggested checker'],x['Outcome rows']) for x in new],[1.4,3.3,1.2,1.0])
para('Each paper already has a source-based eligibility decision, ten QA items, extraction fields and cited findings in the draft. The ten additions contribute 60 eligibility checks, 100 QA items and 38 outcome rows. The older set contributes the other 200 QA items and 52 outcomes. These are item counts, not paper counts.')
para('The private bundle contains the ten new PDFs only. It does not claim to newly recover every original paper. Use earlier reading copies or the original source register for the older studies. Preserve any actual access/version limitation.')
head('What Eshaal and Rameen should do')
para('The suggested split gives each checker five added papers. First confirm the publication identity and eligibility. Next check the main reported finding and its use in the report. Then inspect the QA and other assigned outcome rows. The CSV assigns every item, but you must leave an item unverified if you have not checked it.')
para('Eshaal also checks Results, Comparison and Discussion. Look for percentages with the correct baseline, mean versus tail latency, and adverse results. Rameen also checks Methodology, Study Selection, QA and References. Check the 30/31 distinction, claim-specific N/A denominators and current counts.')
para('Use your previous completed reviews for the original studies. Give priority to source identity, the central numerical claims and recommendations. Cosmetic rewriting can follow. The new queues are suggested independent checks, not a replacement for actual protocol requirements.')
doc.add_page_break();head('How to check one paper step by step')
for title,body in [
 ('Publication identity','Compare the PDF first page with Studies and New_Paper_Map.csv. Check title, authors, year, venue and DOI. A preprint and a final paper can differ; record the actual version.'),
 ('Eligibility','Read IC1 to IC6 in the protocol and the recorded criterion anchors. Confirm a relevant sharing mechanism, separable inference evidence and a within-one-GPU result. A download or abstract alone is insufficient.'),
 ('Quality appraisal','Find Q1 to Q10 in the QA sheet. Read the rationale and cited page. Check the score against the scoring rule. N/A must mean that the paper does not make that type of claim; it must not conceal missing evidence for a claim.'),
 ('Data extraction','Compare mechanism, hardware, workload, tenant count, load, baseline and metric definition with the paper. Keep the source conditions attached to the result.'),
 ('Outcome and synthesis','Open Evidence and locate the outcome ID. Verify value, units, comparator and source anchor. Find the corresponding claim in the report, then check that its conclusion respects the source limits.'),
 ('Return a correction','Enter the item ID, source page, actual finding, checker name and date. Use Agree or Correction needed only after reading the relevant evidence. Put proposed changes in the correction inbox and let Raazia update the master once.')]:
    doc.add_heading(title,2);para(body)
para('Example: KACE reports 92.3% of an offline oracle throughput sum for its unseen GPT2-xl target. This is not a 92.3% latency reduction or a p99 guarantee. A correction must preserve the metric, target workload and oracle denominator.')
para('Example: SPLIT uses block-execution-time dispersion as a jitter measure. Do not rename it end-to-end request-tail jitter. Some splits add execution overhead; keep those adverse costs in the review.')
head('How Raazia should merge corrections')
para('Keep one master workbook and one LaTeX project. Check each proposed correction against its source, update the owning data row and any affected report claim, then rebuild the PDF. Update the Word companion after accepted changes. Recheck counts only when an eligibility or identity decision changes. Record the final Git commit and submitted file hashes.')
doc.add_page_break();head('Sir mandatory deliverables')
para('Heading 23 lists 25 deliverables. The following table maps every item. Present means that draft content exists; it does not certify that the associated research question or audit is fully closed. Guideline_23_Deliverables.csv contains the full actions and file locations.')
table(['No','Requirement','Location','Status'],[(x[0],x[1],x[2],x[3]) for x in requirements],[.35,2.1,2.7,1.75])
head('How headings 24 to 27 apply')
para('Heading 24 is the report structure. The current report has all thirteen main sections: Introduction; Research Questions; Methodology; Study Selection; Taxonomy; Results by RQ; Comparison; Trade-offs; Discussion; Recommendation; Research Gaps; Validity; Conclusion. References and evidence appendices follow. The appendix paper cards support the synthesis; they do not replace analysis across papers.')
para('Heading 25 asks for critical analysis. For each recommendation, explain which mechanism fits which workload, what evidence supports it and what cost must be accepted. Do not rank unrelated percentages as though the papers used one experiment. Mean latency, p99, batch completion, block dispersion and throughput sum remain distinct.')
para('Heading 26 asks for traceability and reproducibility. Every included study needs an identifiable source, every decision needs evidence, and every PRISMA count needs a real log. The current source/QA/extraction records are present. The 320 deferred records and historical search gaps mean that full compliance is still incomplete. They must remain visible.')
para('Heading 27 is the final engineering answer. Read the recommendation section and ask: what should an engineer select, under which conditions, why, with which benefit and sacrifice, and when is an alternative preferable? Every answer must point back to the reviewed evidence.')
head('Work before Sunday submission')
for step,s in enumerate(['Start with this current package and transfer any older corrections by paper ID.',
          'Eshaal and Rameen check their assigned sources and the report sections above. Return concrete corrections, not a blanket approval.',
          'Raazia reconciles corrections, regenerates affected outputs and checks the final report against the guideline matrix.',
          'Keep the 320-record queue separate. If further records are actually assessed, apply the criteria and rebuild the corpus-dependent outputs. Do not mark that queue complete merely because the draft minimum is met.',
          'Confirm cover details, submission instructions, required individual submissions and file opening. Record the exact final version before sending it to Sir.'],1):
    para(str(step)+'. '+s)
para('The current draft can be reviewed as a bounded first draft. Approval cannot be guaranteed, particularly while systematic selection and historical search reconstruction remain incomplete. The most useful work now is genuine source checking and correction of substantive claims, followed by a single consistent submission version.')
for sec in doc.sections:
    p=sec.footer.paragraphs[0];p.alignment=1
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');p._p.append(fld)
guide=submission/'04_Team/Team_Guide.docx';doc.save(guide)
readme='''# Start here

Use 04_Team/Team_Guide.pdf first. This is the current 30-study / 31-report team package. The two ZIPs previously shared with teammates are the older 20-study / 21-report version. The report/evidence snapshot is dated 23 October and this organized handover is dated 24 October 2026.

Read 01_Report/CEP_Task3_First_Draft.pdf. Use the matching Word file for comments and 02_Master/CEP_Task3_Evidence_Workbook.xlsx as the database. The private team ZIP includes ten added source PDFs. They are excluded from public GitHub; their exact sources, DOIs and hashes are in 03_Data_and_Logs.

The separate Task3_LaTeX_2026-10-24 folder is self-contained and can compile without the whole repository. All thirteen report sections are drafted. All 559 continuation screening decisions are recorded. Full-text eligibility/identity remains deferred for 320 advanced records; the whole SLR is not 100% complete. The deliverable matrix states the remaining limits.

Eshaal and Rameen have individual CSV check queues. Existing older checks transfer by stable IDs. Only actual completed source checks should receive a checker name and date. Raazia maintains the single master and applies accepted changes. Keep the older frozen ZIPs as historical backups.
'''
(submission/'START_HERE.md').write_text(readme)
(submission/'05_Added_Paper_PDFs').mkdir(exist_ok=True)
(submission/'05_Added_Paper_PDFs/README.md').write_text('The private team ZIP contains all ten added PDFs in this folder. The public repository provides URLs, DOIs and hashes in 03_Data_and_Logs/Release_Reading_Copy_Access.csv. Reading copies are excluded from public publication.\n')
print(json.dumps({'submission':str(submission),'latex':str(latex),'guide':str(guide),'new_papers':len(new),'suggested_checks':len(tasks),'guideline_deliverables':len(requirements)}))

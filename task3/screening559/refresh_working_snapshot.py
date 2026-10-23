"""Refresh current status from the actual eligibility, QA and outcome registers."""
from pathlib import Path
import csv,json,datetime
d=Path(__file__).resolve().parent;r=d.parents[1]
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(name):return list(csv.DictReader((d/name).open(newline='')))
def write(name,rows):
    with (d/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
elig=read('Final_Eligibility_Decisions.csv');inc=[x for x in elig if x['Final eligibility decision']=='Include'];exc=[x for x in elig if x['Final eligibility decision']=='Exclude']
n=len(inc);ne=len(exc);nst=20+n;nr=21+n;open_n=334-n-ne
qa=read('Final_Candidate_QA.csv');outcomes=read('Candidate_Outcomes_Prepared.csv');refs=read('New_Included_References.csv')
names=', '.join(x['Short name'] for x in inc)
p=json.loads((d/'progress.json').read_text());p.update({'final_source_based_eligibility_decisions':len(elig),'final_full_text_exclusions':ne,'new_full_text_eligibility_assessments':len(elig),'new_included_studies':n,'working_unique_studies':nst,'working_included_reports':nr,'remaining_advanced_records':open_n,'full_text_criteria_prepared':6*n,'candidate_QA_items_prepared':len(qa),'candidate_outcomes_prepared':len(outcomes),'reference_additions':len(refs),'integrated_working_report_and_workbook':True,'whole_review_final_prisma':False});(d/'progress.json').write_text(json.dumps(p,indent=2)+'\n')
account={'scope':'559-record continuation; not whole-review final PRISMA','records_screened':559,'records_excluded_at_screening':225,'records_advanced_to_retrieval':334,'new_included_reports':n,'full_text_excluded_reports':ne,'advanced_records_without_closed_eligibility_or_identity':open_n,'reconciliation':f'559=225+334;334={n}+{ne}+{open_n}','whole_review_final_prisma':False,'checked_utc':now};(d/'PRISMA_Branch_Accounting.json').write_text(json.dumps(account,indent=2)+'\n')
current=f'''# Current working snapshot

Updated UTC: {now}.

The working corpus contains **{nst}unique studies across{nr}reports**. The frozen20-study/21-report ZIP,report,workbook and submitted protocol remain unchanged.

## Selection

All559continuation records have final title/abstract-stage decisions:225excluded and334advanced.56earlier exclusion proposals were conservatively reopened.108screening exclusions are explicitly title/metadata-only; missing abstract text is never the exclusion reason.

Within the334advanced records,{n}new reports are included and{ne}are excluded at full text;{open_n}still require eligibility or report-identity closure. The newly included studies are {names}. A source PDF can be available while scope remains undecided: MIGER's supplied full text is recorded but its local-inference criterion remains pending. It is not counted as an added study or as unavailable.

## Integrated report and workbook

The new working PDF/LaTeX report is in integrated_report/. The expanded working master is integrated_workbook/CEP_Task3_Working_Integrated_2026-10-23.xlsx. It extends the frozen37-sheet master and retains source/version,eligibility,QA,extraction,comparison,recommendation and audit records. The current report integrates the additions into all13main sections and evidence appendices, with a headings23–26map. These are working artifacts; further eligibility can change the corpus.

The additions contribute{6*n}criterion checks,{len(qa)}QA items,{len(outcomes)}outcome rows and{len(refs)}DOI/reference/BibTeX entries. Working totals are{200+len(qa)}QA items,{52+len(outcomes)}reported observations and two inherited calculations. No independent human votes are asserted; the actual process is documented once in methodology and amendmentM2026-10-23.

## Remaining closure

The whole-review PRISMA is not final. Branch arithmetic and the working canonical partition are recorded separately; unresolved records are not relabeled exclusions or failed retrievals. Historical search-count/field/run gaps and ParvaGPU version limitations remain. Duplicate/companion hypotheses require native evidence; matching enrichment alone does not prove identity. Source PDFs are private reading copies and are not redistributed in the repository.

For submission, use the dated working report and workbook together, preserve the frozen backup, and retain the explicit remaining limits. Check VALIDATION.json and the artifact-specific validation files for the verified snapshot.
'''
(d/'CURRENT_STATUS.md').write_text(current)
(d/'START_HERE.md').write_text(f'''# Working evidence and integrated draft

Read CURRENT_STATUS.md. Current corpus:{nst}studies/{nr}reports;559screening decisions;{n}new inclusions,{ne}new full-text exclusions,{open_n}advanced records open. The new integrated PDF/LaTeX is in integrated_report/ and expanded master workbook in integrated_workbook/. Frozen20/21release preserved. References,source evidence,QA,outcomes and methodology corrections are included. Whole-review PRISMA and eligibility census remain open.
''')
(d/'README.md').write_text(f'''# Task3continued screening and integrated working draft

Current snapshot: **{nst}studies/{nr}reports**. Open CURRENT_STATUS.md for the distinction between completed work and remaining eligibility. Report:integrated_report/main.pdf; editable LaTeX:integrated_report/main.tex and references.bib. Master:integrated_workbook/CEP_Task3_Working_Integrated_2026-10-23.xlsx. All original37tabs are retained; current source and reference additions extend the master.

All559continuation records are screened(225excluded,334advanced). Full-text decisions add{n}eligible reports and{ne}exclusions;{open_n}advanced records remain open. Missing full text is not a scientific exclusion. MIGER is supplied but needs scope closure; no further copy is requested. ElasticRoom and SPLIT supplied copies are assessed and integrated.

The frozen submission is unchanged. The new report/workbook/CSVregisters share stable IDs. The whole-review PRISMA remains a working reconciliation. No licensed primary PDFs or independent human votes are invented or redistributed.
''')
issues=read('methodology_corrections.csv')
for x in issues:
    if x['Audit ID']=='MA04':x.update({'Finding':f'All559records have final screening decisions:225exclude,334advance. {n}new studies included and{ne}reports excluded at full text;{open_n}advanced records remain open.','Evidence':'Final_Screening_Decisions.csv;Final_Eligibility_Decisions.csv;PRISMA_Branch_Accounting.json','Remaining gap':'Full-text and identity census incomplete; whole-review final PRISMA remains open.','Checked UTC':now})
    if x['Audit ID']=='CONT05':x.update({'Finding':f'Frozen20studies/21reports unchanged. Working corpus{nst}/{nr}; additions supply{len(qa)}QA items,{len(outcomes)}outcomes and{len(refs)}references. New report and master workbook integrate this current snapshot.','Evidence':'integrated_report/integration_summary.json;integrated_workbook/workbook_validation.json;Final_Eligibility_Decisions.csv','Next action':'Complete unresolved eligibility/identity,then regenerate a coordinated final release.','Remaining gap':f'{open_n}advanced records and final PRISMA closure remain; no exhaustive final census claimed.','Checked UTC':now})
write('methodology_corrections.csv',issues)
req=read('Priority_PDF_Request.csv')
for x in req:
    rid=x['Record ID'];x['Current access status']='User-supplied final PDF received and inspected'
    if rid=='R00001':x['Action']='No further upload needed; close local-inference scope evidence before inclusion';x['Eligibility']='Pending criterionIC5/local inference scope; not an unavailable report'
    elif rid in {z['Record ID'] for z in inc}:x['Action']='No further upload needed; final source assessment integrated into working report/master';x['Eligibility']='Include; see Final_Eligibility_Decisions.csv'
write('Priority_PDF_Request.csv',req)
heading=read('Heading_15_26_Integration_Checklist.csv')
for x in heading:
    x['Integrated evidence']=x['Integrated evidence'].replace('27-study',f'{nst}-study').replace('325advanced',f'{open_n}advanced')
    x['Remaining condition']=x['Remaining condition'].replace('325advanced',f'{open_n}advanced')
    if x['Heading']=='19':x['Integrated evidence']='All five RQs updated with source-specific compiler/runtime,model-block,edge and memory evidence'
write('Heading_15_26_Integration_Checklist.csv',heading)
(d/'CHECKLIST.md').write_text(f'''# Current continuation checklist

- [x] All559screening decisions:225exclude,334advance.
- [x] {n}newinclusions and{ne}full-text exclusions supported by source evidence.
- [x] {nst}studies/{nr}reports integrated into PDF/LaTeX and38-sheet master.
- [x] {len(qa)}newQAitems,{len(outcomes)}newoutcomes,{len(refs)}newreferences.
- [x] Allthree requestedPDFs supplied;ElasticRoom/SPLITintegrated,MIGERscopepending.
- [ ] Close{open_n}advanced records and native identity evidence.
- [ ] Finalwhole-reviewPRISMA,remainingprovenanceandgenuine teammate corrections.

ReadCURRENT_STATUS.md andSUBMISSION_HANDOVER.md.
''')
(r/'STATUS.md').write_text('# Current CEP working status\n\n'+current+'\nSee task3/screening559/SUBMISSION_HANDOVER.md for teammate integration.\n')
print(json.dumps({'working_studies':nst,'working_reports':nr,'new_inclusions':n,'new_full_text_exclusions':ne,'advanced_open':open_n,'new_QA':len(qa),'new_outcomes':len(outcomes),'new_references':len(refs)}))

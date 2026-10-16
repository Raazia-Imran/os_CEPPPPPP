from pathlib import Path
from collections import Counter
import json,csv,shutil,re
R=Path(__file__).resolve().parents[1];E=R/'evidence';F=R/'final things';O=F/'06_Task2_Submission';D=O/'data'
def read(p):return list(csv.DictReader(p.open(newline='')))
def save(p,rows):
 with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
screen=read(E/'screening.csv');forms=read(E/'study_extraction_form.csv');checks=read(E/'fulltext_checks.csv');qa=read(E/'quality.csv');outs=read(E/'extraction.csv');fmap={x['report_id']:x for x in forms};cmap={x['report_id']:x for x in checks};matrix=read(R/'task2/qa/qa_score_matrix.csv');qm={x['report_id']:x for x in matrix};cat=read(F/'01_Statistics_and_Papers/CURRENT_ASSESSED_PAPERS_AND_DOIS.csv');cm={x['report_id']:x for x in cat};exc=read(E/'fulltext_exclusions.csv')
prior=json.loads((R/'task2/qa/final_things_input.json').read_text());papers=[]
for c in checks:
 pid=c['report_id'];f=fmap.get(pid,{});x=cm.get(pid,{});q=qm.get(pid);excluded=pid not in fmap
 papers.append(dict(report_id=pid,study_id=f.get('study_id','Not applicable: assessed exclusion'),paper=x.get('short_name',c['short_name']),title=x.get('title',next((z['title'] for z in exc if z['report_id']==pid),c['short_name'])),authors=f.get('authors','Bingyang Wu; Zili Zhang; Zhihao Bai; Xuanzhe Liu; Xin Jin' if pid=='GB-P016' else 'Hanyu Zhao; Zhenhua Han; Zhi Yang; Quanlu Zhang; Fan Yang; Lidong Zhou; Mao Yang; Francis C.M. Lau; Yuqi Wang; Yifan Xiong; Bin Wang'),year=f.get('year','2023' if pid=='GB-P016' else '2020'),doi_or_official_source=f.get('doi','') if f.get('doi','').startswith('10.') else c['source'],source_assessment=c['first_reviewer_recommendation'],qa_raw=int(q['raw_sum']) if q else 'Not applicable',qa_applicable_max=int(q['applicable_max']) if q else 'Not applicable',qa_percentage=float(q['raw_sum'])/float(q['applicable_max']) if q else 'Not applicable',reported_outcomes=sum(z['report_id']==pid for z in outs),source_anchor=c['anchor'],assessor=c['reviewer'],assessment_date=c['date'],final_status='Assessed EC2 exclusion' if excluded else 'Not established'))
assert len(papers)==17
reference=read(D/'REFERENCE_EXISTENCE_AUDIT.csv')
for row in reference:
 if row['citation_key']=='GB-P011':row['evidence_status']='Prior Crossref title/DOI match retained; fresh request429';row['limit']='Publication DOI identified; equivalence of accessed arXiv version remains open'
for pid,url,title in [('GB-P016','https://www.usenix.org/conference/nsdi23/presentation/wu','Transparent GPU Sharing in Container Clouds for Deep Learning Workloads'),('GB-P017','https://www.usenix.org/conference/osdi20/presentation/zhao-hanyu','HiveD: Sharing a GPU Cluster for Deep Learning with Guarantees')]:
 if not any(x['citation_key']==pid for x in reference):reference.append(dict(citation_key=pid,doi='',official_or_accessed_url=url,verification_url=url,checked_at_utc='',http_status='Registered full-text source',metadata_title=title,evidence_status='Official source/PDF identity from recorded assessment; excluded report',limit='',content_type=''))
save(D/'REFERENCE_EXISTENCE_AUDIT.csv',reference)
tabs={'Paper list':papers,'Search runs':prior['tabs']['Search runs'],'Screening log':prior['tabs']['Screening log'],'Duplicates':prior['tabs']['Duplicates'],'Fulltext criteria':prior['tabs']['Fulltext criteria'],'FT exclusions':prior['tabs']['FT exclusions'],'QA items':qa,'Study extraction':forms,'Outcomes':outs,'Calculations':prior['tabs']['Calculations'],'Review issues':prior['tabs']['Review issues'],'Reference audit':reference}
for name,rows in tabs.items():save(D/(name.lower().replace(' ','_')+'.csv'),rows)
# Preserve all earlier workbook data, including the abstract-normalization table, in the printed appendices.
save(D/'abstract_audit.csv',prior['tabs']['Abstract audit'])
extra={'Database statistics':F/'01_Statistics_and_Papers/DATABASE_STATISTICS.csv','Selection statistics':F/'01_Statistics_and_Papers/SELECTION_STATISTICS.csv','Discrepancy ledger':F/'01_Statistics_and_Papers/DISCREPANCY_LEDGER.csv','PRISMA accounting':F/'01_Statistics_and_Papers/PRISMA_INTERIM_COUNT_TABLE.csv','Current paper catalogue':F/'01_Statistics_and_Papers/CURRENT_ASSESSED_PAPERS_AND_DOIS.csv','QA checklist':R/'task2/qa/qa_checklist.csv','QA matrix':R/'task2/qa/qa_score_matrix.csv','QA totals':R/'task2/qa/qa_totals_summary.csv','QA follow-up':R/'task2/qa/qa_followup.csv','QA rationales':R/'task2/qa/qa_rationale_table.csv','Fulltext checks':E/'fulltext_checks.csv','Duplicate links':E/'duplicates.csv','Fulltext decision history':E/'fulltext_decision_log.csv','Import manifest':E/'import_manifest.csv','Export audit':E/'query_export_audit.csv','Protocol requirements audit':R/'task2/HEADING_14_AUDIT.csv','Cycle status':F/'05_Protocol_and_Audit/CYCLE_STATUS.csv'}
extras={name:read(p) for name,p in extra.items()}
for n,rows in extras.items():save(D/('support_'+n.lower().replace(' ','_')+'.csv'),rows)
counts=dict(occurrences=4189,duplicates=114,canonical=4075,preliminary_exclude=1441,retain_uncertain=2634,assessed_reports=17,qa_forms=15,qa_items=150,outcomes=45,calculations=2,unassessed_candidates=2617,missing_exact_timestamps=798,reference_entries=23,final_included=None)
(R/'task2/qa/task2_consolidated_input.json').write_text(json.dumps(dict(tabs=tabs,extras=extras,old_abstract_audit=prior['tabs']['Abstract audit'],counts=counts,qa_matrix=matrix),ensure_ascii=False)+'\n')
# Preserve the later CEP material outside Task2.
tex=(F/'02_Report_LaTeX/main.tex').read_text();a=tex.index(r'\section{Taxonomy and integration layers}');b=tex.index(r'\clearpage\bibliographystyle',a)
late=R/'task2/later_cep';late.mkdir(exist_ok=True);(late/'Sections_15_to_22.tex').write_text(tex[a:b])
print('Prepared17paper list,13-tab workbook sources and',len(extras),'supporting research tables; scientific registers unchanged')

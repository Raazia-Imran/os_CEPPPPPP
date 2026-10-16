"""Current synthesis views; retain Cycle2 tables as historical evidence."""
import csv,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R/'evidence'
def read(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def save(name,rows):
 with (E/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
forms=read(E/'study_extraction_form.csv');ex=read(E/'extraction.csv')
def row(i,kind,topic,text,reports='',outcomes='',anchor='',limit='Incomplete selection and first-AI assessment; no pooled ranking.'):
 return dict(analysis_id=i,kind=kind,topic=topic,interim_analysis=text,report_ids=reports,outcome_ids=outcomes,source_anchor=anchor,limitation_or_required_check=limit,confidence='Bounded source evidence;AI first assessment',final_status='interim;final_selection_pending')
views={}
views['Taxonomy']=[row('T'+f['report_id'][4:],'taxonomy',f['title'],f['mechanism'],f['report_id'],anchor=f['source_anchor'],limit=f['eligibility_status']) for f in forms]
views['Comparative matrix']=[row(x['outcome_id'],'comparison',x['metric'],x['value']+' '+x['units']+'; '+x['workload']+'; baseline: '+x['baseline'],x['report_id'],x['outcome_id'],x['source_anchor'],x['caveat']) for x in ex]
views['Trade-offs']=[row('TR'+f['report_id'][4:],'tradeoff',f['title'],f['tradeoffs'],f['report_id'],anchor=f['source_anchor'],limit=f['limitations']) for f in forms]
views['Conflicting evidence']=[row('CF01','conflict','Different metrics are not contradictions','GSLICE negative latency contrast versus TensorRT is configuration-specific; do not negate distinct throughput/GUE results.','GB-P008','GB-O032','p501 Table4'),row('CF02','conflict','Throughput versus latency','ParvaGPU preprint:354to446requests/s while11to27ms under one1-GPC/batch4configuration.','GB-P011','GB-O036;GB-O037','PDF p5/Figures3-4','Publication-version and quantile uncertainty; two calculations are separate from reported values.'),row('CF03','conflict','Density versus transfer cost','Torpor low-rate sharing benefit coexists with heavy-model transfer penalties; runtime/CPU/bandwidth paths differ.','GB-P012','GB-O038;GB-O039','pp605-606/Table4/Figure8')]
rq=[('RQ1','Mechanisms','Temporal/preemptive,MPS,APIremoting/interception,memory-sharing hybrids and MIG-integrating designs are represented. Prevalence cannot be inferred.'),('RQ2','Metrics','Keep throughput,requestP99/P98,SLOviolation rate,per-API overhead,host memory andGPUmemory distinct.'),('RQ3','Conditions','Hardware,model/batch/load,tenant mix,memory pressure and software integration govern applicability.'),('RQ4','Isolation and costs','Performance quotas are not security/fault guarantees; compiler/kernel/runtime changes impose different costs.'),('RQ5','Conditional choice','Choose candidates by service priority and validate on target conditions; no universal winner or final included-study synthesis established.')]
views['RQ synthesis']=[row(i,'rq',t,txt,';'.join(f['report_id'] for f in forms),anchor='Current study forms and outcome rows; report sections15-20') for i,t,txt in rq]
recs=[('MPS','Trusted concurrent models: test tuned quotas and tail interference.','GB-P001;GB-P002;GB-P003;GB-P008'),('Preemption','Foreground latency priority: test hardware/runtime preemption against target background mix.','GB-P005;GB-P006;GB-P007;GB-P015'),('Workflow sharing','Within-workflow density: test shared streams/runtime under an appropriate trust boundary.','GB-P013'),('Late binding','Low-rate functions: trade device memory against host bandwidth and CPU overhead.','GB-P012'),('Mixed inference/training','Use separable inferenceSLOs and explicit memory handover, not training gains as inference throughput.','GB-P004;GB-P010'),('MIG-aware deployment','Validate supported profiles/reconfiguration and final source before inferring quantitative MIG benefit.','GB-P011;GB-P014')]
views['Recommendations']=[row('RC'+str(i),'recommendation',t,txt,ids,anchor='Study forms and report section20') for i,(t,txt,ids) in enumerate(recs,1)]
issues=read(R/'task2/submission/review_issues.csv')
for name,kind in [('Evidence gaps','gap'),('Validity','validity')]:views[name]=[row(kind+str(i),kind,x['issue'],x['scope'],anchor='Current registers',limit=x['action']) for i,x in enumerate(issues,1)]
paths={}
for name,rows in views.items():
 namefile='cycle5_'+name.lower().replace(' ','_').replace('-','_')+'.csv';save(namefile,rows);paths[name]=namefile
catalog=read(E/'cycle2_reference_catalog.csv')
existing={x['doi'] for x in catalog if x['doi'].startswith('10.')}
for f in forms[5:]:
 if f['doi'] in existing:continue
 catalog.append(dict(citation_key=f['report_id'],short_title=f['title'],title=f['title'],doi=f['doi'],official_url=f['source'],status=f['eligibility_status'],role='assessed_source;not_final_study',source_identity_boundary='Exact accessed version in study form; no invented DOI'))
save('cycle5_reference_catalog.csv',catalog);paths['Reference catalogue']='cycle5_reference_catalog.csv'
(E/'cycle5_view_paths.json').write_text(json.dumps(paths)+'\n')
payload={}
for n,f in paths.items():
 rows=read(E/f);payload[n]=dict(fields=list(rows[0]),rows=rows)
rows=read(R/'task2/HEADING_14_AUDIT.csv')
for x in rows:
 if x['guideline_heading']=='13':x['evidence']='task2/qa/qa_score_matrix.csv; evidence/quality.csv';x['remaining']='15 assessed forms/150 first QA items; source/calibration/selection gaps retained';x['evidence_files']=x['evidence'];x['missing_work']=x['remaining']
 if x['guideline_heading']=='14':x['evidence']='15studyforms;45outcomes;2calculations; task2/submission/GroupB_Data_Extraction.pdf';x['remaining']='Expand beyond current assessed set; resolve source versions and unchecked fields';x['evidence_files']=x['evidence'];x['missing_work']=x['remaining']
with (R/'task2/HEADING_14_AUDIT.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
payload['Requirements audit']=dict(fields=list(rows[0]),rows=rows)
(R/'task2/qa/active_views_input.json').write_text(json.dumps(payload)+'\n')
print('Current synthesis rows',sum(len(x) for x in views.values()))
# Refresh source decisions and their dependent tabs from the same register checkpoint.
for n,f in {'Screening log':'cycle3_screening_log.csv','Screening':'screening.csv','Source checks':'fulltext_checks.csv','Full-text criteria':'fulltext_criteria.csv','FT exclusions':'fulltext_exclusions.csv','Retrieval log':'cycle3_retrieval.csv','QA followup':'../task2/qa/qa_followup.csv'}.items():
 rows=read(E/f);payload[n]=dict(fields=list(rows[0]),rows=rows)
(R/'task2/qa/active_views_input.json').write_text(json.dumps(payload)+'\n')

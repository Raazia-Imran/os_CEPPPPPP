"""Apply fresh source appraisals to user-provided P019/P020; preserve original columns."""
from pathlib import Path
import csv,json,hashlib,fitz
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
out=Path(__file__).parent;root=out.parent;d=json.loads((out/'review_data.json').read_text());now=datetime.now(timezone.utc).isoformat();pkt=datetime.now(ZoneInfo('Asia/Karachi')).isoformat()
notes={
'P019':[
(2,'Objective is QoS-preserving inference/training co-location.','PDF pp1-2; section1'),
(2,'NVML monitoring, CUDA API interception, predictor and adjustment are specified.','PDF pp6-11; sections4.1-4.3'),
(1,'Model pairs and measurements are described; repetitions and uncertainty remain unspecified.','PDF pp11-16; section5'),
(2,'V100, host, CentOS, CUDA and cuDNN plus five inference and six training models are given.','PDF pp4,11; Tables1-3'),
(1,'MPS/k8s comparators and workload pairs are relevant; exact MPS allocation quotas remain unresolved.','PDF pp11-12; section5.2; Figures14-17'),
(2,'QPS, query yield and goodput are distinguished with explicit definitions.','PDF pp12-14; sections5.2-5.3; equations2-3'),
(2,'Single-stream query size1, P99 and twice-solo QoS target are explicit.','PDF pp4,11-12; sections3.4,5.1-5.2'),
(2,'Thirty inference/training pairs and adjustment ablation directly test interference.','PDF pp11-16; Figures14-21'),
(1,'Performance restriction is tested, but stronger cross-context/error claims lack a direct fault/security experiment.','PDF pp2-3,10-11,15-16; sections4.3,5.4'),
(1,'Prediction/limiter overhead and limitations are discussed; data are on request and artifact/software details remain incomplete.','PDF pp15-16; sections5.5-5.6; data availability')],
'P020':[
(2,'Fragmentation, placement and dynamic partitioning objective is explicit.','PDF pp1-2; section1'),
(2,'Partition prediction, BnB scheduling, constraints and reconfiguration-cost model are described.','PDF pp5-11; section3; Algorithms1-3'),
(1,'Workload counts, comparators and metrics are given; repeated-run uncertainty is not established.','PDF pp11-16; section4'),
(2,'A30 system, driver, CUDA, DCGM, model variants and batch sizes are specified.','PDF pp11-13; Table2'),
(1,'MISO is adapted and ORACLE has prior knowledge; comparisons require those qualifications.','PDF p11; section4'),
(2,'STP is a normalized weighted partition-throughput sum; makespan and JCT are separate.','PDF p11; section4'),
(1,'Job completion, deadlines and queues are described; online request-tail measurements are not supplied.','PDF pp11-14; sections4.1-4.3'),
(2,'Single-A30 job/batch concurrency tests are distinguishable from the large-cluster simulation.','PDF pp13-16; sections4.2,4.3.1; Figures11-13'),
(1,'MIG placement boundaries are defined but no direct adversarial/fault-containment test is supplied.','PDF pp8-9,13-14; architectural constraints and local evaluation'),
(1,'Implementation and prediction/reconfiguration limits are disclosed; complete artifact/version details remain unresolved.','PDF pp11,18; sections3.2.5,6.4')]
}
ids={'P019':'1avJnG1rMh-XOq-28kM-vRSDLQO8GJfQ2','P020':'1UN94Gazed1uOUzn83BiMAMCaLImRctQz'}
receipt=[]
for s in d['sources']:
 pid=s['Report ID']
 if pid not in notes:continue
 f=root/'papers'/(pid+'.pdf');pdf=fitz.open(f);sha=hashlib.sha256(f.read_bytes()).hexdigest()
 s.update({'Version checked':'User-supplied publisher typeset PDF; title, DOI, year and journal matched on first page','Access status':'Full text inspected','PDF pages':len(pdf),'SHA256':sha,'Reviewed QA':sum(x[0] for x in notes[pid]),'Reviewed maximum':20,'Checked UTC':now,'Checked PKT':pkt})
 receipt.append({'Report ID':pid,'Drive file ID':ids[pid],'Retrieved UTC':now,'SHA256':sha,'Bytes':f.stat().st_size,'Pages':len(pdf),'Identity anchor':'PDF p1','Status':'Read and appraised; source PDF excluded from public Git'})
for q in d['qa']:
 if q['Report ID'] not in notes:continue
 score,note,anchor=notes[q['Report ID']][int(q['Item ID'][1:])-1]
 q.update({'Reviewed score':score,'Reviewed maximum':2,'Status':'Assessed','Rationale':note,'Source anchor':anchor,'Checked UTC':now})
basis={
'P019':[('Peer-reviewed journal article, English, published2023.','PDF p1'),('API-intercepted resource limiting among GPU co-tenants.','PDF pp10-11; section4.3'),('Five inference models share resources with six training models.','PDF pp4,11; Tables1-2; section5.1'),('P99, QPS and goodput results inspectable with comparator.','PDF pp11-15; section5'),('Thirty local co-location pairs; four-GPU app-mix totals kept separate.','PDF pp11-14; sections5.2-5.3'),('2023 is inside the submitted2020-2026 window.','PDF p1')],
'P020':[('English peer-reviewed Cluster Computing article published2025.','PDF p1'),('MIG placement and dynamic GPU partitioning are specified.','PDF pp8-11; section3.2'),('Small-language-model inference jobs and batch ranges are identified.','PDF pp11-12; Table2'),('Local JCT/STP and prediction-error sensitivity are inspectable; not online P99.','PDF pp11-14; sections4.1-4.2'),('Sections4.2/4.3.1 use a single A30; section4.3.2 simulation kept separate.','PDF pp13-14'),('2025 is inside the submitted2020-2026 window.','PDF p1')]}
for e in d['eligibility']:
 if e['Report ID'] in notes:
  b,a=basis[e['Report ID']][int(e['Item ID'][2:])-1];e.update({'Review decision':'Supported in accessed version','Rationale':b,'Source anchor':a,'Checked UTC':now})
for e in d['outcomes']:
 if e['Report ID'] not in notes:continue
 e.update({'Review status':'Value and context checked','Checked UTC':now})
 if e['Evidence ID']=='E048':e.update({'Evidence location':'PDF p11 / printed p314; section5.2; Figure14 on PDFp12','Review note':'Text confirms all30 tested pairs meet twice-solo P99 target; not a universal guarantee. Four-GPU app-mix goodput is separate.'})
 if e['Evidence ID']=='E049':e.update({'Evidence location':'PDF p12 / printed p315; section5.2; Figure16 on PDFp13','Review note':'Text reports about5% QPS loss in low-contention cases versus MPS; adverse outcome retained.'})
 if e['Evidence ID']=='E050':e.update({'Evidence location':'PDF pp13-14; section4.2; Figure12 on PDFp16','Review note':'15% prediction error gives8.09% longer makespan and two extra reconfigurations. This belongs to section4.2, not the section4.3.2 cluster simulation; job/makespan outcome, not request-tail latency.'})
new=[('RM13','P019 P020','Access','Unavailable fresh full text','Publisher PDFs supplied by user and appraised; P018 remains pending','PDF title pages; uploaded_source_receipt.json'),('RM14','P020 E050','Source section','Section4.3.2','Section4.2; PDFpp13-14; Figure12 onp16','Exact surrounding heading and paragraph verified'),('RM15','P019 E048 E049','Source anchors','Broad inherited page ranges','P99 pair count: PDFp11; QPS loss: PDFp12','Section5.2 and Figures14/16')]
for x in new:
 if not any(c['Change ID']==x[0] for c in d['changes']):d['changes'].append(dict(zip(['Change ID','Scope','Field','Original','Proposed treatment','Evidence'],x)))
for r in d['recommendations']:
 if r['Item']=='REC04':r.update({'Status':'Source checked; conditions retained','Finding':'ArkGPU local P99 and low-contention regression verified in supplied PDF.','Action':'Retain MPS comparator, thirty tested pairs and four-GPU/local distinction; no fault-isolation guarantee.'})
 if r['Item']=='REC05':r.update({'Status':'Source checked; job-level evidence','Finding':'Dyna-P sensitivity and local/cluster strata verified.','Action':'Correct E050 anchor to section4.2. Do not replace online request-tail evidence with makespan.'})
d['activity'].append({'UTC':now,'PKT':pkt,'Operator':d['reviewer'],'Action':'Read supplied ArkGPU and Dyna-P PDFs; ScienceDirect ZIP contains no InferFair; preserve P018 pending','Input commit':'5581282','Independent human signoff':False});d['built_utc']=now;d['built_pkt']=pkt
(out/'review_data.json').write_text(json.dumps(d,indent=2));(out/'uploaded_source_receipt.json').write_text(json.dumps(receipt,indent=2))
for name,key in [('Source_and_Identity_Review.csv','sources'),('QA_Source_Review.csv','qa'),('Eligibility_Source_Review.csv','eligibility'),('Outcome_Source_Review.csv','outcomes'),('Correction_Register.csv','changes'),('Recommendation_Audit.csv','recommendations'),('activity.csv','activity')]:
 with (out/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(d[key][0]),lineterminator='\n');w.writeheader();w.writerows(d[key])
combined=[]
for kind,key in [('identity','sources'),('eligibility','eligibility'),('QA','qa'),('outcome','outcomes')]:
 for r in d[key]:combined.append({'Reviewer':d['reviewer'],'Checked UTC':r.get('Checked UTC',now),'Study ID':next(s['Study ID'] for s in d['sources'] if s['Report ID']==r['Report ID']),'Report ID':r['Report ID'],'Record type':kind,'Item ID':r.get('Item ID',r.get('Evidence ID',r['Report ID'])),'Original value':r.get('Original score',r.get('Value',r.get('Original decision',r.get('Title','')))),'Source page/table/figure':r.get('Source anchor',r.get('Evidence location',r.get('Version checked',''))),'Status':r.get('Status',r.get('Review decision',r.get('Review status',r.get('Access status','')))),'Reviewed value':r.get('Reviewed score',r.get('Metric','')),'Rationale':r.get('Rationale',r.get('Review note','')),'Independent human vote':''})
with (out/'source_checks_Rameen.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(combined[0]),lineterminator='\n');w.writeheader();w.writerows(combined)
v=json.loads((out/'validation.json').read_text());v.update(sources_inspected=5,sources_pending_full_text=1,qa_assessed=50,qa_pending=10,eligibility_supported_in_accessed_versions=30,eligibility_pending=6,outcomes_checked=7,outcomes_pending=2)
v['sources']=[{'report':s['Report ID'],'original':s['Original QA'],'original_max':s['Original maximum'],'proposed':s['Reviewed QA'],'proposed_max':s['Reviewed maximum']} for s in d['sources']];(out/'validation.json').write_text(json.dumps(v,indent=2))
assert sum(q['Status']=='Assessed' for q in d['qa'])==50
print('Updated5/6 sources;50/60QA;30/36eligibility;7/9outcomes. InferFair pending.')

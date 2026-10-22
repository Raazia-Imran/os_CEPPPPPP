from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import csv,json,hashlib,fitz
out=Path(__file__).parent;root=out.parent;d=json.loads((out/'review_data.json').read_text());now=datetime.now(timezone.utc).isoformat();pkt=datetime.now(ZoneInfo('Asia/Karachi')).isoformat();pid='P018';f=root/'papers/P018.pdf';pdf=fitz.open(f)
notes=[
(2,'Performance fairness for heterogeneous inference models and goodput objectives are explicit.','PDF pp1-2; sections1.1-1.4'),
(2,'Online solo-run goodput estimator, model-state arrays, temporal scheduling and feedback controller are specified.','PDF pp5-8; section4; Algorithms1-3'),
(1,'Poisson load, sensitivity and trace duration are given; experiment repetitions and uncertainty remain unspecified.','PDF pp8-9; sections5.1-5.4'),
(1,'DellR740,V10032GB,models,load andSLO are supplied; precise CPU/OS/driver/CUDA/runtime versions remain unreported.','PDF pp2,8-9; Table1; section5'),
(2,'Clockwork,MPS+Clockwork and EDF conditions are explained; EDF intentionally lacks batching and is interpreted as a policy contrast.','PDF p8; section5.1'),
(2,'Goodput is successful requests per second withinSLO; unfairness is max/min solo-to-shared goodput slowdown.','PDF pp2,8-9; Eq1-2; Table3'),
(2,'SLO100ms,interval50ms,Poisson arrivals and saturation beyond1% deadline failures are specified; no numericalP99 latency is inferred.','PDF p9; sections5.2-5.3'),
(2,'Two- and three-model local co-running experiments are distinguishable from61-model,fourGPU trace replay.','PDF p9; sections5.3-5.4'),
(2,'Performance-isolation boundary is explicitly defined by unequal goodput slowdown and directly tested; no memory/security/fault guarantee is claimed.','PDF p2; Eq1-2; PDF p9; Table3'),
(1,'Algorithms and memory-management reliance onClockwork are explicit; versioned reproduction setup/artifact detail remains incomplete.','PDF pp5-8,10; section7')]
s=next(x for x in d['sources'] if x['Report ID']==pid);s.update({'Version checked':'User-supplied Elsevier typeset article;FGCS150(2024),10-20;DOI matched onPDFp1','Access status':'Full text inspected','PDF pages':len(pdf),'SHA256':hashlib.sha256(f.read_bytes()).hexdigest(),'Reviewed QA':sum(x[0] for x in notes),'Reviewed maximum':20,'Checked UTC':now,'Checked PKT':pkt})
for q in d['qa']:
 if q['Report ID']==pid:
  v,t,a=notes[int(q['Item ID'][1:])-1];q.update({'Reviewed score':v,'Reviewed maximum':2,'Status':'Assessed','Rationale':t,'Source anchor':a,'Checked UTC':now})
basis=[('English journal primary study;typeset DOI/title/year match.','PDFp1'),('TemporalSLO-aware scheduling with feedback goodput balancing.','PDFpp5-8;section4'),('Concurrent heterogeneous DNN inference;three-model Table3 workload.','PDFpp2,9;Tables1,3'),('InspectableSLO-compliant goodput and fairness with definitions.','PDFpp2,8-9;Eq1-2;Table3'),('Local co-location tests separately reported fromfourGPU realistictrace.','PDFp9;sections5.3-5.4'),('2024issue year within2020-2026window;online date18August2023 recorded separately.','PDFp1')]
for e in d['eligibility']:
 if e['Report ID']==pid:
  b,a=basis[int(e['Item ID'][2:])-1];e.update({'Review decision':'Supported in accessed version','Rationale':b,'Source anchor':a,'Checked UTC':now})
for e in d['outcomes']:
 if e['Report ID']==pid:e.update({'Review status':'Value and context checked','Review note':'Table3 row3:1:2 verifies524.29requests/s and unfairness1.05 versusClockwork457.24requests/s and1.50. Total600requests/s,SLO100ms,interval50ms. Not thefourGPU trace and not aP99 latency.','Evidence location':'PDFp9 / publishedp18;Table3;unfairness definitionPDFp2 / publishedp11;Eq2','Checked UTC':now})
for r in d['recommendations']:
 if r['Item']=='REC06':r.update({'Status':'Source checked;fairness-specific condition','Finding':'Local goodput andmax/min slowdown unfairness verified inInferFairTable3.','Action':'Retain600requests/s,three-model loadsplit3:1:2,SLO100ms and50ms interval;do not infer security/fault isolation.'})
for c in d['changes']:
 if c['Change ID']=='RM09':c['Proposed treatment']='Historical access gap closed:allthreepublisher PDFs now supplied andchecked;original unavailable status retained inhistory.';c['Evidence']='uploaded_source_receipt.json;inferfair_receipt.json'
 if c['Change ID']=='RM11':c['Proposed treatment']='REC04-REC06 primary-source checks completed;retain experiment-specificconditions andlimits.'
for row in [('RM16','P018','Full text and outcomes','Unavailable fresh source','Full11page article inspected;E046/E047 values andlocalcontext confirmed','PDFp9;Table3'),('RM17','P018 QA','Reporting appraisal','15/20baseline','17/20current source appraisal:Q4lowered for missingstackversions;Q5/Q7/Q9supported byexplicitcomparators,SLOmethod andfairnessboundary','QA_Source_Review.csv;submittedrubric')]:
 d['changes'].append(dict(zip(['Change ID','Scope','Field','Original','Proposed treatment','Evidence'],row)))
d['activity'].append({'UTC':now,'PKT':pkt,'Operator':d['reviewer'],'Action':'Read correct suppliedInferFair full text andclose allremaining primary-source checks inRameenpackage','Input commit':'7dddf17','Independent human signoff':False});d['built_utc']=now;d['built_pkt']=pkt
for name,key in [('Source_and_Identity_Review.csv','sources'),('QA_Source_Review.csv','qa'),('Eligibility_Source_Review.csv','eligibility'),('Outcome_Source_Review.csv','outcomes'),('Correction_Register.csv','changes'),('Recommendation_Audit.csv','recommendations'),('activity.csv','activity')]:
 with (out/name).open('w',newline='') as stream:w=csv.DictWriter(stream,fieldnames=list(d[key][0]),lineterminator='\n');w.writeheader();w.writerows(d[key])
(out/'review_data.json').write_text(json.dumps(d,indent=2));(out/'inferfair_receipt.json').write_text(json.dumps({'Report ID':pid,'Received filename':'1-s2.0-S0167739X23003187-main.pdf','Checked UTC':now,'Pages':len(pdf),'SHA256':s['SHA256'],'Identity':'FGCS150(2024),10-20;DOI10.1016/j.future.2023.08.020','Source PDF':'Kept privately;not published'},indent=2))
v=json.loads((out/'validation.json').read_text());v.update(sources_inspected=6,sources_pending_full_text=0,qa_assessed=60,qa_pending=0,eligibility_supported_in_accessed_versions=36,eligibility_pending=0,outcomes_checked=9,outcomes_pending=0);v['sources']=[{'report':s['Report ID'],'original':s['Original QA'],'original_max':s['Original maximum'],'proposed':s['Reviewed QA'],'proposed_max':s['Reviewed maximum']} for s in d['sources']];(out/'validation.json').write_text(json.dumps(v,indent=2));print('Rameen sourcechecks complete:6sources,60QA,36eligibility,9outcomes;human independentchecks separate.')

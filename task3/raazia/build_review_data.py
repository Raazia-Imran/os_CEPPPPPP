from pathlib import Path
import csv,json,hashlib,datetime,shutil
from zoneinfo import ZoneInfo
root=Path(__file__).resolve().parents[1];out=root/'raazia';now=datetime.datetime.now(datetime.timezone.utc);utc=now.isoformat();pkt=now.astimezone(ZoneInfo('Asia/Karachi')).isoformat()
# Preserve the damaged local reading copy separately; it is excluded from Git.
p=root/'papers/P008.pdf';old=p.with_suffix('.corrupt');
if not old.exists():shutil.copy2(p,old)
shutil.copy2('/tmp/GSLICE_verified_copy.pdf',p)
# Each record below is an AI source appraisal under the submitted Q1-Q10 rubric.
# Scores 1 denote a reporting/evidence limitation, not an unfinished assessment.
notes={
'P008':[
(2,'Inference sharing objective explicit.','PDF p1; printed p492; abstract/introduction'),
(2,'MPS allocation and adaptive batching described.','PDF pp4-8; section3'),
(1,'Confidence intervals shown; repeated-run count not specified for retained results.','PDF p9; printed p500; section4.1'),
(2,'V100 testbed, kernel, frameworks and concurrent models specified.','PDF pp8-9; section4 setup'),
(2,'TensorRT comparison matches GPU-ready batch execution and states excluded transport costs.','PDF p10; printed p501; section4.3'),
(2,'GUE defined as an efficacy metric; table values are not busy percentages.','PDF p3; printed p494; PDF p9 Table3'),
(1,'Median latency and SLO shown; request-tail quantile not established.','PDF p10; section4.4; Figures12a-12b'),
(2,'Two-to-four-function combinations evaluated.','PDF p9; section4.2; Figure10'),
(2,'Performance boundary evaluated under allocated GPU shares; no adversarial guarantee inferred.','PDF pp5-7,10-11; sections3.2,4.5'),
(1,'Implementation and sensitivity described; full reproduction package not established in accessed copy.','PDF pp8-13; sections4-6')],
'P009':[
(2,'Predictable multi-model inference objective and target behavior explicit.','PDF p2; printed p443; section1'),
(2,'Controller scheduling, worker actions and managed model runtime described.','PDF pp6-10; sections4-5'),
(1,'Section6.6 reports three scaling repetitions; repeated-run count for retained Figure5 is not specified.','PDF pp10-11,14; sections6.1,6.6'),
(2,'V100 hardware, TVM v0.7 compiler, model set and client configuration are reported.','PDF pp4,7,10; Table1; sections2,6'),
(1,'INFaaS uses different EC2 machines; authors restrict that contrast to qualitative interpretation.','PDF p10; printed p451; section6.1'),
(2,'Goodput counts successful requests within their deadline and excludes late requests.','PDF p11; printed p452; section6.1'),
(2,'SLO range, closed-loop load, latency CDF and batch scheduling explanation are explicit.','PDF pp10-11; Figure5; section6.1'),
(2,'Concurrent model demand and a protected minor workload tested.','PDF pp10-12; sections6.1-6.3; Figures5-7'),
(2,'Performance-isolation boundary is measured; dedicated-worker assumptions and security exclusions are explicit.','PDF pp11-12,14-15; sections6.2,7'),
(2,'Runtime, scheduling, model details and limitations support informed implementation appraisal; no local reproduction claimed.','PDF pp7-10,14-15; sections5,7')],
'P010':[
(2,'Inference-priority co-location objective and training progress goal explicit.','PDF p2; printed p1657; abstract/introduction'),
(2,'VMM pool, handover, memory mapping and SM allocation described.','PDF pp5-10; sections3-5'),
(1,'Trace distributions and 300-second window specified; repeated-run uncertainty not specified for Figure10.','PDF pp10-11; section6; Figure10'),
(2,'V100/A100 cases, CPU/RAM, software versions and model/batch table supplied.','PDF pp10-11,14; Table3; sections6,6.6'),
(1,'TaskSwitch is an adapted implementation; equivalence to unmodified PipeSwitch is not established.','PDF p10; comparing targets'),
(2,'Training samples/second and inference SLO compliance are defined separately.','PDF p11; metrics; Figure10'),
(2,'P99, arrivals, duration and four-times-solo SLO definition stated.','PDF p11; section6.1'),
(2,'Inference plus Swin-T training co-location evaluated on a single GPU.','PDF p11; Figure10'),
(1,'Handover correctness and priority boundary described; direct fault-injection validation not established.','PDF pp6-10; sections4-5'),
(2,'Artifact appendix reports availability, functionality and reproduction badges with artifact DOI.','PDF p20; artifact appendix; DOI10.5281/zenodo.15581800')],
'P011':[
(2,'SLO-constrained inference resource objective explicit.','arXiv v1 PDF pp1-2'),
(2,'MIG/MPS profiling, segment configuration and allocation algorithms described.','arXiv v1 PDF pp4-8; sectionIII'),
(1,'Profiler and six scenarios specified; repeated-run uncertainty not established.','arXiv v1 PDF pp5,8-10; sectionsIII-C,IV'),
(1,'A100, Ubuntu and CUDA reported; printed PyTorch1.14.0 string is an unresolved environment ambiguity.','arXiv v1 PDF p8; sectionIV-A'),
(1,'Local process-count contrast interpretable; fleet baseline variants and manuscript scope constrain comparison.','arXiv v1 PDF pp5,8; sectionsIII-B,IV-A'),
(2,'Local throughput values and metric units given.','arXiv v1 PDF pp4-5; Figure3; sectionIII-B'),
(1,'Local latency values given without a named tail quantile.','arXiv v1 PDF pp4-5; Figure4; sectionIII-B'),
(2,'One-to-three MPS processes measured inside a MIG segment.','arXiv v1 PDF pp4-5; Figures3-4'),
(1,'MIG/MPS boundary described; no dedicated fault or adversarial experiment established in reviewed manuscript.','arXiv v1 PDF pp2-4,8-10'),
(1,'Algorithms and reconfiguration limitation described; accessed manuscript has no verified final-version equivalence.','arXiv v1 PDF pp5-10; sectionIII-F; source/version record')],
'P012':[
(2,'Low-frequency serverless inference density and latency objectives explicit.','PDF p2; printed p597; section1'),
(2,'Remoting, swapping, memory manager, scheduler and two runtime modes described.','PDF pp5-9; sections4-6'),
(1,'Trace, rates and warm-up specified; repeated-run uncertainty not specified for retained Figure8.','PDF pp9-11; section7'),
(1,'Worker and model configuration supplied; exact OS/driver/framework version matrix not specified in setup.','PDF p9; printed p604; settings'),
(1,'Native and adapted INFless-KA baselines described; CPU execution paths and adaptations affect equality.','PDF pp10-11; sections7.1-7.3'),
(2,'Normalized single-GPU throughput and GPU busy-time definition supplied.','PDF pp10-11; metrics; Figure8'),
(2,'Default P98, per-function rates and deadlines stated.','PDF pp10-11; metrics; section7.2'),
(2,'Many low-frequency functions share one GPU; node-level results identified separately.','PDF pp10-11; Figure8; section7.2'),
(1,'Runtime-sharing and runtime-isolation modes plus recovery design stated; dedicated fault-injection evaluation not established.','PDF p7; section4.5; PDF p9 evaluation mode'),
(1,'Implementation and mode trade-offs explained; complete public replication recipe not established in paper.','PDF pp7-9,13; sections4.5,6,8')],
'P013':[
(2,'Workflow runtime-redundancy and spatial-sharing objective explicit.','PDF p2; printed p59; section1'),
(2,'API proxy, PTB transformation, stream sharing and memory pool described.','PDF pp5-10; sections3-8'),
(1,'Trace types, ablations and workloads stated; repeated-run uncertainty not specified for Figure13.','PDF pp10-13; section9'),
(2,'V100 hardware, CPU/RAM, framework versions, CUDA version and workflow descriptions reported.','PDF p10; printed p67; setup; Table2'),
(1,'Warm-up and common optimizations disclosed; adapted baselines and batch/concurrency choices constrain causal attribution.','PDF pp10-11; comparing targets; Figure13'),
(2,'Throughput, memory metrics and comparator-specific factors explicitly reported.','PDF p11; printed p68; Figures12-13'),
(1,'Traffic SLO and CDF supplied; exact scalar request-tail quantile not supplied for retained throughput result.','PDF p11; Figure14'),
(2,'Separate three- and six-user single-GPU tests supplied.','PDF p13; section9.4; Figure19'),
(2,'Mutual trust within workflow is explicit; separate proxies for users are distinguished from untested strong security.','PDF pp5-6,13; sections3-4,9.4,10'),
(2,'Implementation, preparation costs and multi-user limitations sufficiently detailed for informed appraisal.','PDF pp6-10,13; sections4-9')],
'P014':[
(2,'Compatibility, isolation and performance-control objectives explicit.','PDF p2; printed p1003; section1'),
(2,'Kernel interception, token control and MIG orchestration explained.','PDF pp5-10; sections3-4'),
(1,'Setup and workloads detailed; repeated-run uncertainty not specified for retained QoS result.','PDF pp10-13; section5'),
(2,'OS, kernel, driver, runtimes, GPUs and workloads explicitly tabulated.','PDF p10; printed p1011; Tables1-2'),
(1,'Isolation-capable baselines and MIG adaptations described; policy and allocation differences limit equivalence.','PDF pp10-11; section5.1'),
(2,'Throughput targets are solo-normalized and QoS violation is a request fraction.','PDF pp10,12-13; sections5.1,5.4-5.6'),
(2,'Solo-P99 threshold, Poisson load, subsequent rate halving and token sizes stated.','PDF pp12-13; section5.5; Figure17'),
(2,'Co-running inference relative-error and QoS experiments supplied.','PDF p13; sections5.5-5.6'),
(1,'Baseline fault propagation is tested; design/security argument does not directly establish universal KRYPTON containment.','PDF p4 Figure3; PDF p14 section7'),
(1,'Implementation and MIG limitation detailed; complete end-to-end replication package not established.','PDF pp10,14; sections4,7')]
}
def loadcsv(n):return list(csv.DictReader((root/'logs'/n).open()))
def dump(n,rows):
 with (out/n).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
oldqa={(x['Report ID'],x['Criterion']):x for x in loadcsv('baseline_QA.csv')};qas=[]
for report,items in notes.items():
 for i,(score,note,anchor) in enumerate(items,1):
  key=(report,'Q'+str(i));old=oldqa[key]
  qas.append({'Report ID':report,'Criterion':key[1],'Original score':int(old['Score']),'Reviewed score':score,'Maximum':2,'Assessment':'Source appraisal completed','Rationale':note,'Source anchor':anchor,'Source URL':('https://www.cse.iitb.ac.in/~puru/courses/spring2024-25/downloads/gslice.pdf' if report=='P008' else old['Source']),'Reviewer':'AI assistant under Raazia direction','Checked UTC':utc,'Independent human vote':''})
dump('QA_Source_Review.csv',qas)
evidence=[x for x in loadcsv('baseline_Evidence.csv') if x['Report ID'] in notes]
anchors={'E031':'GSLICE PDF p9; printed p500; Table3','E032':'GSLICE PDF p10; printed p501; Table4 and section4.3','E033':'USENIX PDF pp10-11; printed pp451-452; Figure5 and section6.1','E034':'USENIX PDF pp10-11; printed pp451-452; Figure5 and section6.1','E035':'USENIX PDF p11; printed p1666; Figure10 discussion','E036':'arXiv v1 PDF p5; sectionIII-B; Figures3-4 on p4','E037':'arXiv v1 PDF p5; sectionIII-B; Figures3-4 on p4','E038':'USENIX PDF pp10-11; printed pp605-606; Figure8 and section7.2','E039':'USENIX PDF pp10-11; printed pp605-606; default P98 metrics and section7.2','E040':'USENIX PDF p11; printed p68; section9.1; Figure13','E041':'USENIX PDF p13; printed p70; section9.3; Figure18','E042':'USENIX PDF pp12-13; printed pp1013-1014; section5.5; Figure17','E043':'USENIX PDF p13; printed p1014; section5.7'}
outs=[]
for e in evidence:
 x=dict(e);x['Original anchor']=x['Evidence location'];x['Evidence location']=anchors[x['Evidence ID']]
 x.update({'Review result':'Value verified in accessed source','Checked UTC':utc,'Reviewer':'AI assistant under Raazia direction'})
 if x['Evidence ID']=='E042':x['Workload']='Transformer-XL inference; batch8/16/32. Original rate is half solo maximum; shared test halves that rate again and assigns 50% time; tokens5-80ms.';x['Review result']='Value verified; offered-load context corrected'
 if x['Report ID']=='P008':x['Source']='https://www.cse.iitb.ac.in/~puru/courses/spring2024-25/downloads/gslice.pdf'
 outs.append(x)
dump('Outcome_Source_Review.csv',outs)
sources=[]
for s in loadcsv('baseline_Studies.csv'):
 if s['Report ID'] not in notes:continue
 pid=s['Report ID'];p=root/f'papers/{pid}.pdf'
 import fitz
 d=fitz.open(p)
 sources.append({'Study ID':s['Study ID'],'Report ID':pid,'Title':s['Title'],'Year':int(s['Year']),'Venue':s['Venue'],'DOI or proceedings':s['DOI'],'Source URL':('https://www.cse.iitb.ac.in/~puru/courses/spring2024-25/downloads/gslice.pdf' if pid=='P008' else s['Source']),'PDF pages':len(d),'SHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'Version checked':('arXiv2409.14447v1; SC24 publication identity confirmed from conference/author records; final text equivalence not established' if pid=='P011' else 'Conference paper; title and author identity matched in accessed PDF'),'Original QA':sum(x['Original score'] for x in qas if x['Report ID']==pid),'Reviewed QA':sum(x['Reviewed score'] for x in qas if x['Report ID']==pid),'Maximum':20,'Checked UTC':utc})
dump('Source_and_Identity_Review.csv',sources)
changes=[
('R01','P008','Reading copy','Saved local PDF unreadable','Recovered a readable 15-page academic-mirror copy; kept old bytes separately','File parsing and title/DOI checks'),
('R02','P009 E033/E034','Evidence anchor','Author-copy page10 inherited','Use accessed USENIX PDF pp10-11, printed451-452','Figure5 and section6.1'),
('R03','P009','Runtime extraction','Software versions not assessed','TVMv0.7 reported; preserve missing OS/driver distinctions','PDF pp4,7; Table1; section5'),
('R04','P009 Q3','QA rationale','Repetition count unclear','Scaling experiment has three repetitions; retained local Figure5 repetitions unspecified','PDF p14 section6.6; pp10-11 section6.1'),
('R05','P009 Q4/Q9','QA reappraisal','1/2 for both','2/2 for both: hardware/compiler/workload documented; performance isolation evaluated within explicit boundary','Submitted rubric Table8; source anchors in QA review'),
('R06','P013 Q4/Q9','QA reappraisal','1/2 for both','2/2 for both: hardware/framework/workload documented; trust assumptions and scope explicitly delimited','Submitted rubric Table8; source anchors in QA review'),
('R07','P012','Isolation/fault extraction','Not assessed in retained extract','Section4.5 describes two runtime modes and recovery; section7 uses sharing mode, section8 isolation mode; direct fault-test evidence not established','PDF pp7,9; sections4.5,7-8'),
('R08','P014 E042','Offered-load context','Poisson rate half maximum in shared test','Initial rate half solo maximum; shared test halves it again for50% allocation','PDF pp12-13 section5.5'),
('R09','P009/P012/P014 Q10','QA rationale','Artifact/reproduction wording used inconsistently','Appraise source replication information; do not penalize a paper merely because this review did not rerun it','Protocol Q10; revised QA rationales'),
('R10','P008-P014','Bibliography','Generic misc entries and abbreviated authors','Create full-author conference entries; label ParvaGPU accessed manuscript separately','Accessed PDF title pages and SC24/author record'),
('R11','P011','Version record','Published/preprint relationship uncertain','Publication identity confirmed; numerical check remains explicitly scoped to arXivv1','SC24 official record and accessed arXivv1'),
('R12','Review attribution','Reviewer identity','User requested assistant to do assigned work','Record AI assistant under Raazia direction; independent human vote left blank','Actual review method')]
changes=[dict(zip(['Change ID','Scope','Field','Original','Reviewed treatment','Evidence'],x)) for x in changes];dump('Correction_Register.csv',changes)
info={'checked_utc':utc,'checked_pkt':pkt,'scope':'S008-S014; source reading, AI appraisal and integration corrections','sources':sources,'qa':qas,'outcomes':outs,'changes':changes,'reviewer':'AI assistant under Raazia direction','independent_human_signoff_claimed':False,'global_scope':'559 retained records remain unassessed; unchanged by this seven-study source review'}
(out/'review_data.json').write_text(json.dumps(info,indent=2))
# Active processed data is an overlay; the frozen baseline is never rewritten.
data=json.loads((root/'logs/baseline_data.json').read_text())
qaidx={v:i for i,v in enumerate(data['QA'][0])};stidx={v:i for i,v in enumerate(data['Studies'][0])}
for row in data['QA'][1:]:
 if row[0] in notes:
  q=next(q for q in qas if q['Report ID']==row[0] and q['Criterion']==row[1]);row[2]=q['Reviewed score'];row[4]=q['Rationale'];row[5]=q['Source anchor'];row[6]=q['Source URL']
for row in data['Studies'][1:]:
 if row[1] in notes:
  new=next(s for s in sources if s['Report ID']==row[1]);row[6]=new['Reviewed QA'];row[8]=new['Reviewed QA']/20
for row in data['Evidence'][1:]:
 if row[1] in notes:
  e=next(e for e in outs if e['Evidence ID']==row[0]);row[data['Evidence'][0].index('Evidence location')]=e['Evidence location'];row[data['Evidence'][0].index('Workload')]=e['Workload'];row[data['Evidence'][0].index('Source')]=e['Source']
for row in data['Extraction'][1:]:
 if row[1]=='P009':row[5]='TVM v0.7 compiler and custom managed runtime reported (PDF pp4,7-8); exact OS/driver versions not established in setup.'
 if row[1]=='P012':
  row[12]='Section4.5 describes shared and isolated GPU runtimes; section7 evaluates runtime sharing, while section8 deployment uses isolation mode. No universal adversarial-security guarantee inferred.'
  row[13]='Section4.5 describes restart, migration and persisted-state recovery. Direct fault-injection validation is not established by the retained performance results.'
 if row[1]=='P014':row[8]='QoS: initial Poisson rate is half solo maximum; shared setting halves the input again and assigns50%time; tokens5/10/20/40/80ms; target original soloP99.'
(root/'logs/reviewed_data.json').write_text(json.dumps(data,indent=2))
print('Reviewed',len(sources),'sources;',len(qas),'QA items;',len(outs),'outcomes;',len(changes),'corrections')

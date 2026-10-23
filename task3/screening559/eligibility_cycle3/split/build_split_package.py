"""Full-text SPLIT assessment from the user-supplied final conference PDF.

No source PDF is copied into this publication folder. Original votes remain empty.
"""
from pathlib import Path
import csv,json,hashlib,datetime
d=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rid='R00877';sid='S029';pid='P032';doi='10.1145/3605573.3605627'
url='https://doi.org/'+doi
pdf=Path('/workspace/scratch/8d52181bc639/upload/3605573.3605627.pdf')
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
def write(name,rows):
    with (d/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
source={'Record ID':rid,'Reserved study ID':sid,'Reserved report ID':pid,'Candidate name':'SPLIT',
 'Title':'SPLIT: QoS-Aware DNN Inference on Shared GPU via Evenly-Sized Model Splitting',
 'Authors':'Diaohan Luo; Tian Yu; Yuewen Wu; Heng Wu; Tao Wang; Wenbo Zhang',
 'Venue':'52nd International Conference on Parallel Processing (ICPP2023)',
 'Conference year':2023,'Frozen indexed year':2023,'DOI':doi,'Source URL':url,'Source SHA256':sha,'PDF pages':10,
 'Access result':'User-supplied final ACM conference PDF inspected; uploaded file3605573.3605627.pdf; no public download success claimed',
 'Checked UTC':now,'Version caution':'Final typeset10page report, printed605-614. Author name is Diaohan Luo on primary first page; do not substitute secondary spelling.',
 'Final eligibility':'Include','Decision method':'Single automated source-based review under M2026-10-23; no independent human vote asserted'}
write('SPLIT_Source.csv',[source])
checks=[
 ('IC1','Met','English primary10-page final ICPP2023 conference report; first page carries exact DOI, copyright, full authors and venue.','PDF p1 / printed605'),
 ('IC2','Met','Five independently deployed model tasks share one Jetson Nano GPU through token-controlled, sequential block-level preemption. Model splitting plus a greedy response-ratio scheduler implements temporal sharing across live inference requests; parallel kernels are not required for temporal-sharing eligibility.','PDF pp5-8 / printed609-612; sections3.3-4.2,5.1,6'),
 ('IC3','Met','YOLOv2, GoogLeNet, ResNet50, VGG19 and GPT-2 inference tasks generate independent requests; task-level models are deployed separately. Training is not substituted for serving evidence.','PDF p7 / printed611; Table1 and section5.1'),
 ('IC4','Met','End-to-end response ratio and target-relative violation fraction are defined, with1000requests per scenario, six stated mean arrival intervals, target multiplier sweep2-20 and splitting-cost observations. Block-time SD is the stated jitter proxy and must remain distinct from request-tail latency.','PDF pp2,5,7-8 / printed606,609,611-612; sections2.1,3.4,5.1-5.5'),
 ('IC5','Met','Implementation and evaluation use one NVIDIA Jetson Nano with ONNX Runtime1.12.1 and Ubuntu18.04. Local temporal interference among independently arriving model requests is directly compared; results are not fleet-only aggregates.','PDF pp6-8 / printed610-612; sections4,5.1-5.5'),
 ('IC6','Met','August2023 final conference publication lies inside the submitted1January2020-to-actual-search window. No older-study exception is required.','PDF p1 / printed605; submitted protocol section6')]
write('SPLIT_Eligibility.csv',[{'Record ID':rid,'Study ID':sid,'Report ID':pid,'Criterion':q,'Final decision':dec,'Evidence':ev,'Anchor':anchor,'Source URL':url,'Source SHA256':sha,'Checked UTC':now,'Independent human vote':''} for q,dec,ev,anchor in checks])
qa=[
 ('Q1',2,2,'QoS objective, model-splitting mechanism and evaluation questions are explicit.','PDF pp1-2,7; abstract and section5'),
 ('Q2',2,2,'Genetic splitting objective, greedy preemption algorithm, token scheduler/assigner and ONNX-based thread implementation identify the layer and temporal-sharing boundary.','PDF pp4-7; sections3-4 and Algorithm1'),
 ('Q3',1,2,'Six mean arrival intervals,1000queries and target sweep are stated, but repeated trials, seeds, uncertainty intervals and warm-up are not established. The author-described Poisson generator parameter is an average interval, so a standard continuous-time Poisson process must not be assumed.','PDF pp7-8; sections5.1-5.5; Table2'),
 ('Q4',1,2,'Jetson Nano,Ubuntu18.04,ONNX Runtime1.12.1 and five evaluated models are reported. CUDA version,batch sizes,input shapes and complete device configuration are not reported. The earlier profiling passage says11models but its enumerated list contains10.','PDF p4 section3.1; pp6-7 sections4,5.1; Tables1-2'),
 ('Q5',1,2,'ClockWork,PREMA and runtime-aware baselines are named and applied to the six scenarios. The report does not fully document matched ports/configurations; PREMA is originally an NPU method, and baseline behavioral descriptions do not certify equivalence to original artifacts.','PDF pp7-8 sections5.3-5.5; p10 reference4'),
 ('Q6','N/A',0,'The primary evaluated objective is latency-target compliance and block-time dispersion. No quantitative utilization,throughput or density benefit is claimed; section6 explicitly accepts possible sacrifice of spatial utilization. This is a nonclaim N/A, not a substitute for missing support for a claimed throughput benefit.','PDF pp7-8 sections5.2,5.5,6; protocol section10 claim-specificN/A rule'),
 ('Q7',2,2,'End-to-end latency includes waiting/execution; response ratio and per-task alpha-times-isolated-time targets define violations.1000requests,six loads and alpha2-20sweep specify population and load. No p99 is claimed; jitter is explicitly a block-time SD proxy.','PDF p2 footnote1; p5 Eq3; p7 sections5.1-5.2'),
 ('Q8',2,2,'Independent requests from five separately deployed model tasks are compared under six increasing-load scenarios; short/long task effects and the adverse long-task stability trade-off are retained.','PDF pp7-8; Tables1-2,section5.5,Figures6-7'),
 ('Q9',2,2,'The claimed QoS/performance boundary is token-controlled temporal execution with preemption at model-block boundaries; violation and dispersion comparisons directly evaluate that limited claim. No security,memory protection or GPU-runtime fault-isolation guarantee is inferred.','PDF pp5-8; sections3.4-5.5 and section6 sequential-execution discussion'),
 ('Q10',1,2,'Algorithms,runtime,9000-lineC++implementation summary and limits for RNN/data-dependent execution and splitting overhead support informed reading; code artifact,exact profiling configuration and complete reproduction instructions are not supplied in the inspected report.','PDF pp5-8; sections3.3,4,5.1,6')]
write('SPLIT_QA.csv',[{'Record ID':rid,'Study ID':sid,'Report ID':pid,'Criterion':q,'Score':score,'Applicable maximum':maximum,'Rationale':reason,'Anchor':anchor,'Source URL':url,'Source SHA256':sha,'Checked UTC':now,'Independent score':''} for q,score,maximum,reason,anchor in qa])
context='One Jetson Nano; ONNX Runtime1.12.1; Ubuntu18.04; five independently deployed inference models;1000requests; author-described Poisson mean inter-arrival intervals160-110ms in six scenarios.'
outcomes=[
 ('SPLIT-01','Latency-target violation fraction','<10','percent','RT-A26percent in the accompanying prose','Target multiplier alpha beyond4; Figure6 and six-scenario discussion. '+context,'PDF p8 / printed612; section5.5 and Figure6 on p9','Author-stated threshold-relative result; prose does not isolate an exact panel/load for the26percent comparison. Do not convert into a precise paired effect or p99 value.'),
 ('SPLIT-02','Short-request block-execution-time SD reduction',68.9,'percent','Runtime-aware approach(RT-A)','Low workload,scenario1 mean interval160ms. '+context,'PDF p8 / printed612; section5.5,Figure7 on p9','Author-reported reduction in stated jitter proxy; not per-request end-to-end latency SD or a percentile.'),
 ('SPLIT-03','Short-request block-execution-time SD reduction',69.3,'percent','Runtime-aware approach(RT-A)','High-workload comparison in section5.5; six-scenario interval range retained. '+context,'PDF p8 / printed612; section5.5,Figure7 on p9','Source does not explicitly name one high-load panel in the sentence. Other comparators and long-request stability differ; no universal jitter reduction is inferred.'),
 ('SPLIT-04','Additional execution-time splitting overhead',15.4,'percent','Unsplit ResNet50 execution time','ResNet50 split into2blocks; offline optimal option in Table3. '+context,'PDF p8 / printed612; Table3; overhead definitionPDFp3footnote2','Additional sum-of-block execution time relative to vanilla model; not total service latency or scheduler-runtime overhead.'),
 ('SPLIT-05','Additional execution-time splitting overhead',50.3,'percent','Unsplit ResNet50 execution time;2-block option15.4percent','ResNet50 split into4blocks; Table3. '+context,'PDF p8 / printed612; Table3 and section5.4','Adverse configuration: extra splits can increase execution overhead and block dispersion; do not claim finer splitting always improves QoS.'),
 ('SPLIT-06','Additional execution-time splitting overhead',18.1,'percent','Unsplit VGG19 execution time','VGG19 split into3blocks; Table3. '+context,'PDF p8 / printed612; Table3 and section5.4','Different model and split count from ResNet50; not a shared global split setting or a throughput gain.')]
write('SPLIT_Outcomes.csv',[dict(zip(['Record ID','Study ID','Report ID','Outcome ID','Metric','Value','Unit','Baseline','Context','Anchor','Interpretation limit'],[rid,sid,pid,*x])) for x in outcomes])
ref={'Record ID':rid,'Study ID':sid,'Report ID':pid,'Authors':'Diaohan Luo and Tian Yu and Yuewen Wu and Heng Wu and Tao Wang and Wenbo Zhang','Title':source['Title'],'Venue':'Proceedings of the52ndInternational Conference on Parallel Processing(ICPP2023)','Year':2023,'Pages':'605-614','DOI':doi,'Primary URL':url,'Primary SHA256':sha,'Date basis':'ConferenceAugust7-10,2023; exactDOIandpage605firstpage','Version':'Final10page typesetACMconference report supplied by user'}
write('SPLIT_Reference.csv',[ref])
(d/'SPLIT.bib').write_text('@inproceedings{s029,\n author={'+ref['Authors']+'},\n title={{'+ref['Title']+'}},\n booktitle={Proceedings of the 52nd International Conference on Parallel Processing},\n year={2023},\n pages={605--614},\n doi={'+doi+'},\n url={'+url+'}\n}\n')
notes='''# SPLIT: synthesis and claim boundaries

SPLIT is eligible for the local GPU-sharing review. It adds model-aware temporal sharing, using offline genetic search for evenly sized blocks and online greedy block-boundary preemption. Independently arriving model tasks share one physical Jetson Nano; section6explicitly says execution is sequential to avoid interactions. Do not misclassify it as measured MPS/MIG spatial sharing merely because several model requests are live.

The engineering decision is lower short-request waiting and target-violation risk versus added model-splitting execution cost and reduced long-request stability. It supports static-DAGCNNs/Transformers; the authors identify input-dependent RNNexecution as unsuitable for offline splitting. The elastic mechanism suspends splitting at very dense loads or many same-type requests. Shorter90msintervals cause growing queues, while200msintervals make sequential processing sufficient; those loads are excluded from the six main scenarios rather than evidence that the method handles all regimes.

Keep these definitions separate: end-to-end latency includes waiting and execution; response ratio normalizes by isolated execution time; target multiplier alpha is swept2-20; reported jitter is the SDof block execution time. The block-dispersion objective is not identical to end-to-end request-latency jitter or p99. Figure7and prose provide short-request improvements while explicitly sacrificing stability for long requests. No throughput/utilization/fault-isolation benefit is inferred.

The abstract describes a43%latency-violation-rate reduction, whereas the conclusion describes a43%response-ratio reduction. These are different quantities, and the comparator/context is not unambiguous; the package does not use43%as a synthesized numerical effect. Likewise, the stated<10%versus26%threshold comparison does not identify a precise panel in its sentence; preserve that attribution rather than constructing an exact paired effect.

Other reporting cautions: the profiling section says11models but enumerates10; the request-generation parameterization calls lambda an average interval in ms, so do not silently convert it into a conventional Poisson arrival rate; PREMA/ClockWork descriptions are the authors' baselines and do not establish original artifact equivalence. Hardware/runtime setup lacks CUDAversion,batch,input-shape and repeated-trial details. No full reproduction is claimed.

QA:14/18applicable points(77.78%), with Q6reasonedN/A because no utilization/throughput/density benefit is claimed. This is reporting appraisal, not an inclusion gate, precision estimate or independent reviewer agreement. All initial human-vote fields remain blank.
'''
(d/'SPLIT_Synthesis.md').write_text(notes)
validation={'six_criteria_met':True,'QA_items':len(qa),'QA_raw_sum':sum(x[1] for x in qa if isinstance(x[1],int)),'QA_applicable_maximum':sum(x[2] for x in qa),'QA_percent':14/18*100,'outcome_rows':len(outcomes),'source_pages':10,'source_sha256':sha,'independent_human_vote':False,'IDs_reserved_by_root':True,'licensed_PDF_redistributed':False,'eligibility':'Include','classification':'Model-aware temporal block preemption; sequential execution of independently arriving tasks on one physical GPU'}
(d/'SPLIT_Validation.json').write_text(json.dumps(validation,indent=2)+'\n')
assert len(checks)==6 and len(qa)==10 and validation['QA_raw_sum']==14 and validation['QA_applicable_maximum']==18
print(json.dumps(validation))

from pathlib import Path
import csv,json,hashlib,datetime,collections
r=Path(__file__).resolve().parents[2];d=r/'task3/screening559';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
if (d/'Working_559_Queue.csv').exists():
 raise SystemExit('Working queue already exists. Initialization stopped to preserve later reviews; use apply_batch.py for new judgments.')
q=list(csv.DictReader((r/'task3/logs/Remaining_559_Screening_Queue.csv').open(newline='')))
# Explicit record-level reading judgments for the first25 supplied abstracts, not a keyword classifier.
judgments={
'R00001':('retain_for_full_text','IC2/IC3/IC5','MIG/MPS co-location of online and offline jobs is relevant; isolate per-GPU inference evidence from cluster JCT.','Verify venue/version and extract local co-tenant setup and inference QoS outcomes.'),
'R00002':('retain_for_full_text','IC2/IC3/IC5/IC6','Layout-aware MIG partitioning for LLM serving is relevant; final publication date and local comparisons need checking.','Verify2026 publication before the executed cutoff; inspect per-GPU serving outcomes.'),
'R00006':('retain_for_full_text','IC1/IC2/IC3','Deft studies GPU preemption for multiple DNN containers. Author institutional page identifies a2023 workshop paper, unlike frozen2024 metadata.','Resolve date, full-paper versus position/vision status, and protocol venue eligibility; no automatic inclusion.'),
'R00007':('uncertain_need_full_text','IC2','Inference compiler/scheduler is relevant, but the abstract does not establish distinct concurrent tenants.','Check whether experimental workloads actually share one physical GPU concurrently.'),
'R00008':('retain_for_full_text','IC2/IC3/IC5','Spatial GPU partitioning and inference-related real-time tasks are relevant; synthetic acceptance ratios alone would be insufficient.','Inspect empirical model-serving workload and per-GPU co-tenant configuration.'),
'R00010':('retain_for_full_text','IC3/IC4/IC5','MIG/MPS and kernel scheduling cover online/offline sharing; makespan and JCT do not establish separable inference outcomes.','Verify2026 date and look for interpretable inference measurements on one GPU.'),
'R00011':('retain_for_full_text','IC2/IC3/IC5','CPU escape is used to relieve multi-model GPU contention; local interference may be separable from the12-server aggregate.','Verify concurrent GPU models, local outcomes and migration overhead; do not exclude solely for server count.'),
'R00012':('uncertain_need_full_text','IC2','Layer caching/direct host access improves serving, but multiple model instances do not by themselves establish concurrent co-tenants.','Check temporal overlap, GPU residency/sharing policy and an eligible local experiment.'),
'R00013':('retain_for_full_text','IC2/IC3/IC6','Power-capped resource partitioning explicitly targets multi-tenant inference on named GPUs.','Verify2026 publication timing and local tenant mix; separate power and throughput outcomes.'),
'R00014':('retain_for_full_text','IC2/IC3/IC5','Inference/retraining resource competition and temporary GPU-space reallocation are relevant mixed-workload mechanisms.','Verify separable inference results and within-device allocation; do not relabel accuracy as latency.'),
'R00015':('retain_for_full_text','IC2/IC3/IC4','Concurrent single-GPU inference with MPS atop MIG and QoS-aware scheduling is directly relevant.','Verify report/version identity, publication date, hardware and local comparisons.'),
'R00016':('retain_for_full_text','IC2/IC3','Memory-aware serving of co-located models may be a classifiable runtime-sharing mechanism; scope is not decided by the merging label.','Check distinct concurrent model services, local GPU outcomes and accuracy/performance trade-off.'),
'R00018':('retain_for_full_text','IC2/IC3/IC5','GPU API remoting from CPU-only nodes can match the assigned remoting family; aggregate delay alone is insufficient.','Verify that distinct concurrent clients share the same GPU and local outcomes are extractable.'),
'R00019':('retain_for_full_text','IC2/IC3/IC5','The abstract explicitly describes two GPU processes to prevent heavy inference requests monopolizing the device.','Verify one-GPU setup, request/process concurrency and separate CPU extraction from GPU inference metrics.'),
'R00020':('retain_for_full_text','IC2/IC3/IC5','Kernel slicing for concurrent inference QoS is relevant; general accelerator statements must not replace GPU evidence.','Verify GPU-specific workload combinations, local measurements and report identity.'),
'R00021':('retain_for_full_text','IC2/IC3/IC5','Workflow scheduling treats shareable GPUs as a first-order factor; local sharing evidence may be separable from pipeline placement.','Inspect same-GPU co-tenants and distinguish local SLO outcomes from system cost.'),
'R00024':('retain_for_full_text','IC2/IC3/IC6','Concurrent GPU multitasking and resource isolation for DNN workloads appear relevant.','Verify2026 publication date and separable inference-serving results on V100/MI50.'),
'R00026':('propose_exclusion','EC4','The supplied abstract describes partitioning a target model across GPUs and topology-aware model/data-transfer parallelism, not local concurrent co-tenant evidence.','Independent reviewer must check this reason; reopen if the full text provides an eligible local sharing experiment.'),
'R00029':('uncertain_need_full_text','IC2','CPU fair-scheduler weighting improves GPU-fed inference pipelines; distinct tenants and a classifiable local GPU-sharing boundary remain unclear.','Check whether this is multi-tenant GPU sharing rather than only CPU-feeder optimisation; verify2026 date.'),
'R00030':('retain_for_full_text','IC2/IC3/IC4','Concurrency-aware compilation explicitly targets multiple DNN inference tasks on a shared GPU.','Verify final paper, configuration and concurrent model outcomes before QA/extraction.'),
'R00031':('uncertain_need_full_text','IC2','Data loading and serverless throughput are described, but concurrent sharing of one GPU is not established in the abstract.','Seek full text to check co-tenant execution and whether the intervention is a local sharing mechanism.'),
'R00032':('retain_for_full_text','IC2/IC3/IC5','Fine-grained GPU resourcing and inference/training outcomes may provide eligible local sharing evidence.','Separate local sharing from cluster elasticity and extract inference-specific results.'),
'R00033':('propose_exclusion','EC2','The abstract describes moving tasks within an emerging model data-flow graph from GPU to CPU; it does not describe distinct concurrent inference tenants.','Independent check required; reopen if full text demonstrates an eligible multi-tenant GPU-sharing experiment.'),
'R00035':('retain_for_full_text','IC2/IC3/IC5','The study explicitly predicts interference between co-located GPU training/inference workloads.','Verify separable inference results, report identity and local sharing configurations.'),
'R00037':('propose_exclusion','EC2','The described intervention monitors and terminates idle Slurm jobs; an evaluated concurrent inference-sharing mechanism/outcome is not established.','Check primary publication status and scope independently; this is not a final full-text exclusion.')}
rows=[];working=[]
for x in q:
 y=dict(x);y.update({'Preparation status':'Pending','Preparation recommendation':'','Preparation criterion':'','Preparation rationale':'','Preparation next action':'','Preparation checked UTC':''})
 if x['Record ID'] in judgments:
  rec,code,reason,nxt=judgments[x['Record ID']];assert x['Recovered abstract'];sha=hashlib.sha256(x['Recovered abstract'].encode()).hexdigest()
  row={'Batch':'B001','Record ID':x['Record ID'],'Title':x['Title'],'DOI':x['DOI'],'Frozen year':x['Year'],'Stage':'Abstract review of supplied recovered metadata','Recommendation':rec,'Criterion to check':code,'Rationale':reason,'Next action':nxt,'Evidence anchor':'Frozen Remaining_559_Screening_Queue.csv / '+x['Record ID']+' / Recovered abstract','Abstract SHA256':sha,'Reviewer role':'Prepared source-based first-pass assessment; not an independent human vote','Checked UTC':now,'Independent human vote':'','Final eligibility':'Pending','Full text assessed':False};rows.append(row)
  y.update({'Preparation status':'Abstract reviewed; independent/full-text checks pending','Preparation recommendation':rec,'Preparation criterion':code,'Preparation rationale':reason,'Preparation next action':nxt,'Preparation checked UTC':now})
 working.append(y)
def write(path,rr):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
write(d/'Batch_001_Abstract_Review.csv',rows);write(d/'Working_559_Queue.csv',working)
access=[{'Record ID':i,'URL':u,'Attempt type':typ,'Result':res,'Checked UTC':now,'Remaining action':nxt} for i,u,typ,res,nxt in [
('R00001','https://dl.acm.org/doi/fullHtml/10.1145/3673038.3673089','Publisher full text','403 Forbidden','Seek author/institutional copy; full text not yet assessed.'),
('R00035','https://dl.acm.org/doi/pdf/10.1145/3698038.3698555','Publisher PDF','403 Forbidden','Seek legitimate author/repository copy; do not mark report not retrieved after this attempt alone.'),
('R00030','https://dl.acm.org/doi/pdf/10.1145/3721145.3735113','Publisher PDF','403 Forbidden','Seek legitimate author/repository copy; detailed extraction pending.'),
('R00006','https://research.ibm.com/publications/towards-optimal-preemptive-gpu-time-sharing-for-edge-model-serving','Author institutional publication page','Read title,abstract,authors and11December2023/workshop label','Correct historical year only through version audit; inspect full text for IC1 eligibility.')]]
write(d/'Retrieval_and_Metadata_Checks.csv',access)
counts=dict(collections.Counter(x['Recommendation'] for x in rows));progress={'built_utc':now,'frozen_commit':'04271d77eae68f153d0682f951bd3cc1e9162a6b','queue_records':559,'abstracts_available_in_initial_queue':235,'abstracts_reviewed_this_batch':25,'recommendations':counts,'remaining_initial_abstract_reviews':534,'remaining_with_recovered_abstracts':210,'remaining_without_recovered_abstracts':324,'new_full_text_eligibility_assessments':0,'new_included_studies':0,'frozen_unique_studies':20,'independent_human_votes':0,'prisma_changed':False,'sampling':'First25records in frozen queue order; not representative and no yield extrapolation.'};(d/'progress.json').write_text(json.dumps(progress,indent=2)+'\n')
freeze={'commit':progress['frozen_commit'],'sha256':{f:hashlib.sha256((r/f).read_bytes()).hexdigest() for f in ['task3/team/Task3_Complete_First_Draft.zip','task3/report/main.pdf','task3/workbook/CEP_Task3_Evidence_Workbook.xlsx','task1/submitted_protocol.pdf']},'rule':'Do not rebuild or overwrite these frozen artifacts during queue work; integrate changes into a separately named improved release.'};(d/'frozen_snapshot.json').write_text(json.dumps(freeze,indent=2)+'\n')
assert len(rows)==25 and len(working)==559
assert all(not x[k] for x in working for k in ['Initial decision','Independent decision','Adjudicated decision'])
print(json.dumps(progress,indent=2))

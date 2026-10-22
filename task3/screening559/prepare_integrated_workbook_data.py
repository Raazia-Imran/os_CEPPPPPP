"""Join continuation evidence into a separate working master; frozen data stays intact."""
from pathlib import Path
import csv,json,datetime,collections
d=Path(__file__).resolve().parent;r=d.parents[1];out=d/'integrated_workbook';out.mkdir(exist_ok=True)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
data=json.loads((r/'task3/logs/integrated_data.json').read_text())
analysis=json.loads((r/'task3/logs/analysis.json').read_text())
def read(name):return list(csv.DictReader((d/name).open(newline='')))
elig=read('Final_Eligibility_Decisions.csv');inc=[x for x in elig if x['Final eligibility decision']=='Include']
refs={x['Record ID']:x for x in read('New_Included_References.csv')}
qa=read('Final_Candidate_QA.csv');outcomes=read('Candidate_Outcomes_Prepared.csv');checks=read('Final_Eligibility_Criteria.csv')
screen={x['Record ID']:x for x in read('Final_Screening_Decisions.csv')}
decisions={x['Record ID']:x for x in elig}
source={x['Record ID']:x for x in read('Full_Text_Source_Register.csv')}
cards={
'R00647':['Compiler/runtime hybrid: operator microbatch splitting and staged cross-model stream scheduling','One A100; separate P6000 and GTX1080Ti experiments','Native GPU streams; CPU/GPU synchronization; complete driver/software versions not supplied','Vision CNN, language and recommendation model inference batches','Two, four or five concurrent independent models on A100','Batch/image-size configurations in section5.1; no online tail-SLO population established','CuDNN-Seq,TVM-Seq,Stream-Parallel,Competitive-Sharing; AutoMT supports CNN only','Contextual batch-completion speedups and achieved SM occupancy; no serving-tail guarantee','Not established as a latency-isolation guarantee','No security-isolation claim; Q9 reasonedN/A','No fault-isolation guarantee claimed or tested','0.84-1.26seconds optimization; operator transformation/synchronization cost','Final9page/four-author paper differs from2023preprint; occupancy is not busy-time utilization; trials and software versions incomplete'],
'R00080':['TPC scheduling, atomization, dynamic right-sizing; MPS/driver interposition','One A100 SXM4 40GB108SM','Rust/CUDA-driver interposition; CUDA12.6; Ubuntu22.04','Vision/NLP inference; mixed training experiment separate','Two high-priority plus one best-effort inference app','Table2model-specific request rates and SLOs','MPS,TGS; MIG/Limits omit best-effort tenant','Fine-grained allocation improves contextual SLO outcomes; unequal tenant sets limit rankings','Measured SLO/p99 behavior, not universal guarantee','Not established by this source assessment','No adversarial/fault guarantee inferred','Atomization/driver support and kernel compatibility costs','Reimplemented baselines; persistent/cross-block kernel exceptions; source-version summaries differ'],
'R00143':['Deterministic overlapped operator groups; latency prediction and query control','Single A100 MPS; separate16GPU experiment','Segmental model executors; separate service processes','Seven vision/NLP models; variable batch/sequence','Pairwise and higher-order co-location','Poisson arrivals;50QPSlatency and100QPSthroughput analyses','FCFS,SJF,EDF; separate MIG comparisons','Contextual p99/throughput improvements; some saturated model pairs degrade','Prediction and admission control; dropped queries affect latency population','Separate processes do not establish a security guarantee','Not experimentally established here','Pair profiling about2h; CPU prediction/search overhead','A100SM-count discrepancy; queries/s not images/s; retain adverse pairs'],
'R01089':['Elastic-kernel transformation and criticality-aware runtime coordination','RTX2060 and edge device with inconsistent platform labels','CUDA benchmark and transformed kernels','Critical/normal AlexNet,CifarNet,SqueezeNet,GRU,ResNet,LSTM pairs','Critical plus normal inference','Closed/open-loop mixes and Table2arrival patterns','Sequential and source baselines by configuration','Throughput benefit has workload-specific critical-latency overhead','Critical-task coordination; reported overhead is not always under10percent','Not established','Not established','Kernel transformation and workload constraints','Intro/body latency-summary difference; platform identity discrepancy'],
'R00656':['Dynamic VRAM-bandwidth and SM control; page coloring/tidal SM masks','Local P40 and RTX A2000','TVM-generated kernels; shared CUDA context','Latency-sensitive and best-effort DNN inference; Apollo arrival traces','Multiple LS and BE services','SLO is concurrency-count times isolated p99; dynamic batching disabled','Multi-stream priority,TGS,MPS50/50,Orion reimplementation,static variant','Latency/goodput trade-offs; raw throughput can be lower than Multi-streaming','Measured queue-inclusive p99 and LS goodput','Shared address/runtime context; no security guarantee','Source explicitly says GPU-runtime errors cannot be isolated','Kernel compatibility and control implementation costs','11versus12model count discrepancy; unsupported libraries/architectures'],
'R00661':['Chunk-level preemption, model variants and early exits','Jetson Xavier NX384coreVolta; Nano128coreMaxwell separate','Python3.8/PyTorch offline; C++/LibTorch runtime','Nine real-time DNN task types in traffic/robot/UAV; BEAlexNet','Three/four RT tasks plus best-effort AlexNet','30fps with jitter;20-31msdeadlines; separate Poisson tests','RMS,DMS,RTm-DL with matched accuracy constraint','Lower deadline misses; similar utilization; model accuracy/memory/power costs','Deadline-adjusted accuracy treats late jobs as zero','Threads/streams do not establish tenant security','Not established','Early-exit memory and scheduling overhead; device power increase','Table/prose model-label discrepancies; no universal utilization dominance'],
'R00086':['Parameter-memory remapping; asynchronous CPU/GPU transfer; temporal/spatial sharing','One GH200 system; source H20096GBlabel needs clarification','vLLM0.7.3;CUDA12.4;PyTorch2.5.1;Linux5.14','OPT/Llama C1three-model and C2two-model combinations; ShareGPT/Alpaca/Azure traces','C1three,C2two local models','Bursty scaled arrival traces; TTFT includes queueing','vLLM and Pie on same system','Contextual P99TBT/TTFT and token-throughput gains; transfer trade-offs','MPS-like and MIG-like cases; captions need clarification','No adversarial isolation guarantee demonstrated','No fault-injection isolation test established','CPU-GPU bandwidth dependence; excessive remapping/transfer cost','Hardware description and isolation-caption inconsistencies; conference/index year distinct']}
for x in inc:
 rid=x['Record ID'];ref=refs[rid];pid=x['Report ID'];sid=x['Study ID'];itemqa=[y for y in qa if y['Record ID']==rid]
 score=sum(int(y['Final source-based score']) for y in itemqa if y['Final source-based score']!='N/A');maximum=sum(int(y['Maximum']) for y in itemqa)
 data['Studies'].append([sid,pid,ref['Title'],int(ref['Year']),ref['Venue'],ref['DOI'],score,maximum,score/maximum,x['Source URL'],'Final primary text; criterion and appraisal anchors in supporting source files'])
 for y in itemqa:data['QA'].append([pid,y['Criterion'],int(y['Final source-based score']) if y['Final source-based score']!='N/A' else 'N/A',int(y['Maximum']),y['Rationale'],y['PDF anchor'],x['Source URL'],y['Checked UTC']])
 card=cards.get(rid)
 if card is None:
  card=['See source package']*13
  card[0]=x['Short name']+'; see criterionIC2';card[1]=next((y['Evidence'] for y in checks if y['Record ID']==rid and y['Criterion']=='IC5'),'See source package')
 data['Extraction'].append([sid,pid,ref['Title'],*card,x['Source URL'],'; '.join(y['Anchor'] for y in checks if y['Record ID']==rid),now])
 for y in checks:
  if y['Record ID']==rid:data['Eligibility'].append([pid,sid,y['Criterion'],'eligible',y['Evidence'],y['Anchor'],x['Source URL']])
 data['Source Register'].append(['Report version',pid,sid,ref['Title'],'Included working addition; single source-based review under M2026-10-23',x['Source URL']])
 for y in outcomes:
  if y['Record ID']==rid:
   eid='E'+str(len(data['Evidence'])).zfill(3)
   data['Evidence'].append([eid,pid,y['Metric'],y['Value'],y['Unit'],y['Baseline'],card[1],y['Context'],y['Interpretation limit'],y['Anchor'],x['Source URL']])
for row in data['Screening Log'][1:]:
 rid=row[0]
 if rid not in screen:continue
 s=screen[rid];e=decisions.get(rid)
 row[5]=s['Exclusion criterion'];row[6]=s['Decision rationale'];row[7]=s['Evidence location']+'; '+s['Evidence level'];row[10]=s['Final checked UTC'];row[13]='Exclude' if s['Exclusion criterion'] else 'Advance'
 if s['Exclusion criterion']:
  row[4]='excluded_at_screening';row[14]='Not assessed (excluded at screening)';row[15]='Excluded at screening'
 elif e and e['Final eligibility decision']=='Include':
  row[4]='included_in_synthesis';row[9]=e['Report ID'];row[14]='Include; source-based eligibility';row[15]='Included working corpus';row[6]=e['Basis'];row[7]=e['Source URL'];row[5]='IC1-IC6'
 elif e and e['Final eligibility decision']=='Exclude':
  row[4]='excluded_after_source_assessment';row[14]='Exclude';row[15]='Excluded after full text';row[6]=e['Basis'];row[7]=e['Source URL'];row[5]='EC2'
 else:
  row[4]='full_text_eligibility_pending';row[14]='Pending retrieval/eligibility/identity';row[15]='Open; not an exclusion'
count=collections.Counter(row[4] for row in data['Screening Log'][1:]);n=len(inc);included=21+n;studies=20+n;assessed=23+len(elig)
summary={x[0]:x for x in data['Summary'][1:]}
for label,value,meaning in [
 ('Excluded at screening',count['excluded_at_screening'],'Historical3493plus225continuation decisions; source labels preserved'),
 ('Not advanced under stopping rule',count['full_text_eligibility_pending'],'Stopping rule removed for continued559branch; remaining retrieval/eligibility or identity open'),
 ('Source-assessed report versions',assessed,'Working included and excluded source assessments; unfinished records are not counted as assessed'),
 ('Included unique studies',studies,'Working eligible corpus; selection census still incomplete'),
 ('QA appraisals',len(data['QA'])-1,'Ten criteria per study; source evidence retained'),
 ('Evidence rows',len(data['Evidence'])-1,'Source-specific observations; no pooling of unlike metrics'),
 ('Independent human verification','No item-level independent human votes supplied','Single automated source review under user-reported instructor permission; amendmentM2026-10-23'),
 ('Task3 integrated status',f'{studies}studies;{included}reports;{len(data["QA"])-1}QAitems;{len(data["Evidence"])-1}outcomes','New working workbook; frozen20/21release unchanged; full-text scope remains open')]:
  summary[label][1:]=[value,meaning]
summary['Not advanced under stopping rule'][0]='Full-text eligibility or identity open'
data['Method & Deviations'].append([len(data['Method & Deviations']),'Review amendment M2026-10-23','User reports instructor permission for single automated final source eligibility. No independent votes are inferred.559stage decisions are complete; whole-review retrieval/eligibility census and historical search mapping remain open. Frozen artifacts unchanged.'])
data['PRISMA Counts']=[['Stage','Count','Accounting note'],['Records identified',4189,'Preserved historical count; run-provenance limitations remain'],['Duplicate links applied',114,'Existing duplicate links retained; new companion proposals pending'],['Canonical records screened',4075,'Working partition: screening exclusions + open + included report records + full-text exclusions'],['Excluded at record screening',count['excluded_at_screening'],'3493historical+225continuation; underlying evidence labels retained'],['Advanced after screening',4075-count['excluded_at_screening'],'Not all advanced reports are retrieved or assessed'],['Eligibility/identity open',count['full_text_eligibility_pending'],'Unresolved; not relabeled unavailable or excluded'],['Report versions assessed',assessed,'Historical23plus source-based continuation decisions'],['Excluded after source assessment',count['excluded_after_source_assessment'],'Historical2plus continuation exclusions'],['Included report versions',included,'REEF companion remains one study'],['Included unique studies',studies,'Working corpus; not an exhaustive final census']]
newpids=','.join(x['Report ID'] for x in inc)
analysis['Taxonomy'].extend([
 ['Fine-grained temporal/spatial control','TPC/kernel/operator and CUDA scheduling','P024,P025,P027','Transformable/supported kernels and predictable profiles','Deadline/SLO control with sharing','Driver/kernel compatibility; profiling and shared-runtime fault limits'],
 ['Edge mixed criticality','Elastic kernels, chunks, priorities and variants','P026,P028','Edge GPU and workload-specific real-time tasks','Deadline responsiveness with co-execution','Latency/accuracy/memory/power sacrifices; no hard security guarantee'],
 ['LLM memory virtualization','Parameter remapping and CPU-GPU transfers','P029','Sufficient interconnect bandwidth; multiple resident models','Tail latency and effective KV capacity','Transfer bottleneck; remapping policy and isolation-caption limits']])
for x in inc:
 card=cards.get(x['Record ID'],['See source criteria']*13)
 analysis['Comparability'].append(['CONT-'+x['Study ID'],x['Report ID'],card[8],'Within-study contextual comparison',card[12],'; '.join(y['PDF anchor'] for y in qa if y['Record ID']==x['Record ID'] and y['Criterion'] in ['Q4','Q5'])])
analysis['Recommendations'].extend([
 ['CONT-R4','Known heterogeneous multi-model batch mixes','GACER','P030; GACER-01--04','Lower batch-completion latency in source configurations','Optimization/search, transformations and incomplete replication details','Use latency-controlled serving mechanisms when online tail SLO is primary','Replicate workload; distinguish occupancy from utilization and batch latency from service tails'],
 ['CONT-R1','Latency-critical supported DNN co-location','LithOS/Abacus/SGDRC, depending on control layer','P024,P025,P027','Contextual SLO/p99 or goodput benefits','Compatibility/profiling/control cost; no inferred fault boundary','MIG when fault/security requirements dominate','Replicate target workload, baseline support and configuration'],
 ['CONT-R2','Real-time edge inference with model-variant flexibility','Miriam/Pantheon','P026,P028','Lower deadline misses or better mixed-criticality throughput','Accuracy, memory and latency/power costs','Unmodified models when output accuracy cannot be traded','Check task deadlines, arrival pattern and late-job metric'],
 ['CONT-R3','Memory-pressure multi-LLM serving with fast host link','Oneiros','P029','Contextual P99TBT/TTFT and token-throughput improvements','Transfer overhead and system bandwidth dependence','Avoid aggressive remapping when host transfer becomes bottleneck','Verify platform and MPS/MIG setting; no fault guarantee inferred']])
analysis['Research Gaps'].extend([
 ['CONT-G1','Supported tenant sets, reimplemented baselines and metric populations differ','P024-P029','RQ2/RQ3: which gains survive matched comparisons?','Same GPU/model/load/partition and late-request accounting'],
 ['CONT-G2','Performance isolation is often stronger than demonstrated fault/security evidence','P024-P029','RQ4: what failure boundaries are actually established?','Fault injection and adversarial co-tenancy with latency tests'],
 ['CONT-G3','Edge variants and LLM remapping shift costs beyond utilization','P026,P028,P029','RQ3/RQ5: when do accuracy/memory/transfer costs dominate?','Multi-metric sensitivity under deployment-specific constraints']])
analysis['Validity'].append(['Continuation incomplete','559screened;325advanced records open','Working corpus may change','Conservative reopening; staged evidence logs and explicit method amendment','Complete full text and identity audit; retain historical search limitations'])
for row in analysis['Requirements'][1:]:
 if row[0] in [10,12,14]:row[3]='Working integration updated; exhaustive eligibility/PRISMA closure pending'
counts={'canonical':4075,'screening_exclusions':count['excluded_at_screening'],'open':count['full_text_eligibility_pending'],'included_reports':included,'full_text_exclusions':count['excluded_after_source_assessment'],'studies':studies,'qa':len(data['QA'])-1,'outcomes':len(data['Evidence'])-1,'duplicates':114,'assessed':assessed}
assert counts['screening_exclusions']+counts['open']+counts['included_reports']+counts['full_text_exclusions']==4075
assert len(data['Extraction'])==len(data['Studies'])==studies+1
payload={'data':data,'analysis':analysis,'counts':counts,'final_decisions':elig,'references':list(refs.values()),'source_checks':list(source.values()),'methodology':read('methodology_corrections.csv'),'screening_stage':list(screen.values())}
(out/'integrated_workbook_data.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(counts))

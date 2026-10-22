from pathlib import Path
import csv,json,hashlib,fitz,collections
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
out=Path(__file__).parent;root=out.parent;now=datetime.now(timezone.utc).isoformat();pkt=datetime.now(ZoneInfo('Asia/Karachi')).isoformat();who='AI assistant preparing Eshaal assignment at Raazia request'
ids=['P001','P002','P003','P004','P005','P006','P007'];allids=ids+['P023']
def rows(n):return list(csv.DictReader((root/'logs'/('baseline_'+n+'.csv')).open()))
def save(n,r):
 with (out/n).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(r[0]),lineterminator='\n');w.writeheader();w.writerows(r)
smap={r['Report ID']:r for r in rows('Studies') if r['Report ID'] in ids};receipts={r['Report ID']:r for r in json.loads((out/'retrieval_receipt.json').read_text())}
notes={
'P001':[
('Local GPU portability and throughput objective are explicit; NPU cluster results are excluded from this extracted stratum.','PDF pp2,16-17; section6.7'),
('RL-tuned MPS allocation and MI100 CU-mask backend are described.','PDF pp16-17; sections6.7-6.8'),
('GPU throughput provenance is clear, but GPU-specific repeated-run uncertainty is not established.','PDF pp16-18'),
('A100/TensorRT and MI100/TVM/ROCm are named; exact versions, GPU batch/rate and tuned quotas remain incomplete.','PDF pp16-17'),
('Same A100 no/default/tuned MPS comparison; default means unspecified respective quotas.','PDF pp16-17; Figure14'),
('2.7x versus noMPS and1.5x versus defaultMPS are explicit for VGG16+GoogLeNet; not universal averages.','PDF p17 / printed459; Figure14 onp16'),
('No online latency claim in the retained local GPU outcomes; NPU results cannot fill this item.','PDF pp16-17; sections6.7-6.8'),
('Several paired CV/NLP model co-locations are measured.','PDF pp16-17; Figures14-16'),
('Performance sharing is measured; separate security/fault validation is not established. Q9 calibration remains flagged.','PDF pp16-17'),
('Stable-mix Q-table assumption and retuning for changed demand are explicit; GPU replication detail remains incomplete.','PDF p17; section6.9')],
'P002':[
('Predictable cost-efficient inference provisioning is the stated objective.','Final PDF p1'),
('MPS active-thread allocation, placement and shadow-Triton recovery are specified.','Final PDF pp8-10; section4.2'),
('Model validation repeats three times with SD bars; resource plan and P99 observation windows are described.','Final PDF pp10-12; sections5.2-5.3'),
('V100 instances, four models and batch/arrival settings are given; exact OS/driver coverage remains incomplete.','Final PDF p10; Table3; section5.1'),
('GSLICE+ and gpulets+ are modified; batch/allocation objectives differ and modifications must remain visible.','Final PDF p10; Baselines and Metrics'),
('Cost, allocation and throughput are separately defined; cluster cost is not local GPU throughput.','Final PDF pp10-13'),
('P99 over e.g.30seconds and first-second15.6ms versus10ms SLO, then shadow activation at1.5seconds are explicit.','Final PDF pp11-12; section5.3; Figure17'),
('Four co-located models with25% allocation and batch3 test local interference.','Final PDF p11; Figure13'),
('Resource/performance interference and recovery are measured; no independent memory/fault experiment established. Q9 calibration flagged.','Final PDF pp11-12'),
('Profiling cost and PCIe/prediction assumptions are disclosed; source code identified in final article.','Final PDF pp11,13-14; sections5.4,6')],
'P003':[
('SLO-aware spatio-temporal sharing objective is explicit.','PDF pp2-3'),
('MPS gpulet partitioning, scheduling, interference model and process replacement are described.','PDF pp7-10; sections4-5'),
('Poisson arrivals and three repetitions with median result are explicit.','PDF pp10-11; section5.1'),
('CPU,RTX2080Ti,OS,driver,CUDA,PyTorch and models are tabulated.','PDF p10; Tables2-3'),
('Ported SBP and greedy best-fit conditions, and why full Nexus is not compared, are explained.','PDF p10; section5.1'),
('SLO-preserved throughput is maximum rate with99% requests within SLO; multi-GPU results not substituted for local CDF.','PDF p11; section5.2'),
('17.66% is the90%-of-scenarios overhead threshold, not requestP90/P99.','PDF p6 / printed203; Figure7'),
('250 model/batch combinations across partition ratios test local interference.','PDF p6; section3.4'),
('MPS performance interference is tested; no memory/security/fault boundary experiment established. Q9 calibration flagged.','PDF p6; section3.4'),
('Reorganization cost and20second scheduling interval disclosed; exact reproduction of all preliminary CDF settings not performed.','PDF pp10,17-18; setup/appendix')],
'P004':[
('Time-sharing and fast context-switching between training/inference tasks are explicit.','PDF p2; abstract'),
('Pipelined transmission, controller, daemon and active/standby workers are specified.','PDF pp6-11; section4-5'),
('100-run means and Figure6 min/max are explicitly reported.','PDF p11; Metrics'),
('V100/T4,PCIe,memory,PyTorch1.3.0 andCUDA10.1 given; exact OS/kernel/driver unresolved.','PDF p11; Setup'),
('Ready-model baseline, same modified PyTorch and MPS full-memory/unified-memory swapping condition are explicit.','PDF pp11-12; section6.1'),
('Utilization is throughput relative to ready-model upper bound; eight-instance scheduling-cycle result kept distinct from local table.','PDF pp12-13; Figure6'),
('Table3 subtracts ready-model latency; it reports added mean overhead, not total latency or P99.','PDF pp11-12; Table3'),
('Single-GPU training-preempted-by-inference workload has separate inference latency; qualifies under mixed-workload rule.','PDF p11; Workloads and section6.1'),
('Process/memory control is described, but independent hostile-client/fault experiment is not established.','PDF pp8-11'),
('Stack versions, model registration and checkpoint dependence supplied; full reproduction configuration remains incomplete.','PDF pp10-11; sections5-6')],
'P005':[
('Concurrent RT/BE DNN inference with low latency and work conservation is explicit.','PDF p2'),
('Reset preemption, idempotent re-execution, queues and dynamic kernel padding are described.','PDF pp4-11; sections3-6'),
('DISB scenarios and baseline methods clear; end-to-end repeated-run/variance protocol not established.','PDF pp11-12; sections7.1-7.2'),
('MI50,CPU,16GB host RAM,Ubuntu18.04,ROCm4.3.0,TVM0.8.0 and clients supplied.','PDF p11; Table2'),
('RT-only,SEQ,GPUStreams and extended wait-based preemption conditions are explicit.','PDF pp11-12; sections7.1-7.3'),
('Figure11 throughput includes both RT and BE clients; benchmark/load is retained for each ratio.','PDF p12 / printed549; Figure11'),
('End-to-end RT overhead is stated with offered loads; request percentile for retained headline overheads unresolved.','PDF pp11-12; sections7.1-7.2'),
('Single/multiple RT and BE clients under uniform,Poisson and trace workloads are tested.','PDF pp11-12; Table2'),
('Performance-control evidence exists; security/fault isolation not established. Q9 calibration flagged.','PDF pp11-14'),
('Artifact,platform and idempotence constraints disclosed; conference REEF-N is distinct from later journal NVIDIA implementation.','PDF pp10-11,15-16; P023p1')],
'P006':[
('Fine-grained software scheduling for low-latency inference is explicit.','PDF p1'),
('Instrumented kernel placement/completion notifications,dispatcher and SRPT/deficit policy are described.','PDF pp5-9; sections4-6'),
('Stabilization before measurement stated; repetitions and uncertainty for headline curve not established.','PDF p10; Methodology'),
('T4,CPU,RAM,Linux4.15,CUDA11.7,TVM0.10 and model list supplied.','PDF pp9-10; Table2'),
('TritonTVM wrapper,omitted Clockwork curves and MPS process-count restriction require qualifications.','PDF p10; Table3; footnote3'),
('Average throughput versus P99 curves use increasing load until saturation.','PDF pp10-11; Figures11-12'),
('Up-to3x short-job P99 reduction is author-reported;6.6us is instrumentationP90 overhead, not request latency.','PDF pp10-12; Figures12,15'),
('Mixed short/long jobs and deficit threshold show latency/fairness trade-offs.','PDF pp10-12; Figures12-13'),
('No separately appraised resource/security/fault isolation guarantee; retain reasoned N/A.','PDF pp9-12; scheduling and discussion'),
('Compiler modifications,versioned setup,CPU dispatch and dynamic-batching limitations described.','PDF pp9-13; sections7-8')],
'P007':[
('Interference-aware fine-grained local GPU sharing is explicit.','PDF p1'),
('CUDA interception,per-client queues,resource profiling and throttling are specified.','PDF pp5-8; sections4-5'),
('Three experiment repetitions and interpretation of variance bars are specified.','PDF pp8-9,12; sections6.1,6.3'),
('V10016GB/A10040GB,VM,PyTorch1.12,Python3.9,CUDA10.2/11.3 and models supplied.','PDF pp4,8-9; Tables1,3'),
('REEF-N and Tick-Tock are reimplemented; Streams threads and MPS processes differ.','PDF p9; Baselines'),
('7.3x is aggregate throughput maximum versus GPU dedicated only to high-priority inference.','PDF p12; section6.2.3'),
('Poisson15% and Apollo22% overhead summaries are distinct; Figure12 averages across co-locations.','PDF pp9,12; Figures11-12'),
('Two-client tests and five-clientA100 experiment test interference at identified scales.','PDF pp9,12; sections6.2-6.3'),
('Same-trust-domain assumption explicitly limits isolation; direct performance evidence does not imply security.','PDF p13; Security'),
('Interception/profiling cost,cache interference and cluster co-design limits are explicit.','PDF p13; sections6.5,7')]
}
sources=[]
for pid in allids:
 old=smap.get(pid,smap['P005']);f=root/'papers'/('P002_final.pdf' if pid=='P002' else pid+'.pdf');pdf=fitz.open(f)
 version={'P001':'Journal typeset copy with cover; article startsPDFp2','P002':'Final IEEE TPDS34(3),812-827,2023 typeset copy; matched DOI and retained values','P003':'USENIX ATC2022 proceedings with cover','P004':'USENIX OSDI2020 proceedings with cover','P005':'USENIX OSDI2022 proceedings with cover; AMD results and restricted REEF-N','P006':'Author-hosted SOSP2023 copy with conference/DOI','P007':'Author-hosted EuroSys2024 copy with conference/DOI','P023':'Author-hosted42page journal typeset copy; publication footerNovember2025; extension statement onp1'}[pid]
 sources.append({'Study ID':old['Study ID'],'Report ID':pid,'Title':old['Title'] if pid!='P023' else 'Real-time, Work-conserving GPU Scheduling for Concurrent DNN Inference','Year':int(old['Year']) if pid!='P023' else 2025,'DOI':old['DOI'] if pid!='P023' else '10.1145/3768622','Source URL':json.loads((out/'igniter_final_receipt.json').read_text())['URL'] if pid=='P002' else receipts[pid]['URL'],'Version checked':version,'Access status':'Full text inspected','PDF pages':len(pdf),'SHA256':hashlib.sha256(f.read_bytes()).hexdigest(),'Original QA':int(old['QA score']) if pid!='P023' else None,'Original maximum':int(old['Applicable maximum']) if pid!='P023' else None,'Reviewed QA':int(old['QA score']) if pid!='P023' else None,'Reviewed maximum':int(old['Applicable maximum']) if pid!='P023' else None,'Reviewer':who,'Checked UTC':now,'Checked PKT':pkt,'Independent human vote':''})
qa=[]
for r in rows('QA'):
 pid=r['Report ID']
 if pid not in ids:continue
 note,anchor=notes[pid][int(r['Criterion'][1:])-1];qa.append({'Study ID':smap[pid]['Study ID'],'Report ID':pid,'Item ID':r['Criterion'],'Original score':r['Score'],'Original maximum':int(r['Maximum']),'Reviewed score':None if r['Score']=='NA' else int(r['Score']),'Reviewed maximum':int(r['Maximum']),'Status':'Assessed; N/A' if r['Score']=='NA' else 'Assessed','Rationale':note,'Source anchor':anchor,'Source URL':next(s['Source URL'] for s in sources if s['Report ID']==pid),'Reviewer':who,'Checked UTC':now,'Independent human score':''})
elig=[]
for r in rows('Eligibility'):
 pid=r['Report ID']
 if pid not in allids:continue
 s=next(s for s in sources if s['Report ID']==pid)
 basis=[('English peer-reviewed report identity matched to title,DOI/proceedings and year.',s['Version checked']),('Local sharing mechanism inspectable.',notes.get(pid,notes['P005'])[1][1]),('Inference workload identified; mixed training cases retained only for separable inference.',notes.get(pid,notes['P005'])[7][1]),('Relevant measured outcomes and methods inspectable.',notes.get(pid,notes['P005'])[5][1]),('Within-one-GPU evidence distinguishable from cluster outcomes.',notes.get(pid,notes['P005'])[7][1]),('Publication year lies in2020-2026 main window.','Title/metadata')]
 if pid=='P023':basis=[('Journal extension ofP005 explicitly identified; no new study.','PDF p1'),('Reset preemption and padding implemented on AMD and NVIDIA.','PDF pp9,15-23'),('TVM,PyTorch,TensorRT DNN/LLM inference workloads.','PDF pp23-24,31-33'),('Normalized latency/throughput metrics and comparisons inspectable.','PDF pp24-25,31-32'),('OneMI50 and oneGV100 configurations separately evaluated.','PDF p23; section6.2'),('Source footer givesNovember2025,within period; distinguish issue versus online dates.','PDF pp1-2')]
 b,a=basis[int(r['Criterion'][2:])-1];elig.append({'Study ID':s['Study ID'],'Report ID':pid,'Item ID':r['Criterion'],'Original decision':r['Decision'],'Review decision':'Supported in accessed version','Rationale':b,'Source anchor':a,'Source URL':s['Source URL'],'Reviewer':who,'Checked UTC':now,'Independent human decision':''})
outcomes=[]
for r in rows('Evidence'):
 pid=r['Report ID']
 if pid not in ids:continue
 x=dict(r);x.update({'Original metric':r['Metric'],'Original anchor':r['Evidence location'],'Review status':'Value and context checked','Reviewer':who,'Checked UTC':now,'Independent human vote':''})
 anchor,note={
 'P001':('PDF pp16-17 / printed458-459; Figure14; section6.7','2.7x and1.5x match paired-model prose. TensorRT and Poisson model-count description are available; exact rate,batch and tuned quotas remain unresolved. Abstract/global headline is not substituted.'),
 'P002':('Final PDF p11 / printed822; Figure13' if r['Evidence ID']=='E003' else 'Final PDF p12 / printed823; Figure17; section5.3','Prediction error range and transient P99 violation verified in final typeset copy; distinguish arXiv page offsets and final printed pages.'),
 'P003':('PDF p6 / printed203; Figure7; section3.4','90% refers to model/batch/partition scenarios, not request-tail percentile.17.66% plotted threshold matches retained value.'),
 'P004':('PDF pp11-12 / printed508-509; Table3; section6.1','All12 retained Table3 cells checked by model,GPU and mechanism.100-run added overhead after subtracting ready-model latency; MPS retains memory-full training and unified-memory swapping.'),
 'P005':('PDF pp11-12 / printed548-549; Table2; Figure11; section7.2','All nine values match scenario prose. RT+BE throughput,RT latency and load-specific denominator retained; journal results are not substituted.'),
 'P006':('PDF p10 / printed604; section7.1; Figure12 onPDFp11' if r['Evidence ID']=='E027' else 'PDF p12 / printed606; section7.3; Figure15','Up-to3x is short-job P99 claim;6.6us is added P90 instrumentation overhead for160blocks with aggregation,not request latency.'),
 'P007':('PDF p12 / printed1086; section6.2.3; Figure12','7.3x is maximum aggregate throughput;15% is authors’ Poisson high-priority latency summary over collocations,not worst-case/untrusted guarantee.')
 }[pid];x.update({'Evidence location':anchor,'Review note':note,'Source':next(s['Source URL'] for s in sources if s['Report ID']==pid) });outcomes.append(x)
changes=[
('ES01','P001 E001 E002','Source anchor','pp457-458','PDFpp16-17 / printed458-459; GPU-specific TensorRT/Poisson context retained','Figure14 and section6.7'),
('ES02','P002','Version and Xplore identifier','arXiv manuscript; earlier lookup10018218','Final typeset TPDS copy inspected; correct Xplore article identifier10002315; retain source URL/hash','Final DOI/title/page1 and IEEE metadata'),
('ES03','P004','Scope and metric','Mixed workload could be mistaken for training-only','Retain under separable single-GPU inference evidence; Table3 is added mean overhead,not P99/total latency','PDFpp11-12'),
('ES04','P005 P023','Report/study linkage','Two versions; possible double-count','SameS005 per explicit extension statement; conferenceAMD results distinct from journalNVIDIA/LLM additions','P023p1;pp23-24,31-33'),
('ES05','P023','Implementation generalization','ConferenceREEF-N equated with journal fullNVIDIAREEF','Keep implementations separate; TVM0.8/Ubuntu18.04/16GBhost versus TVM0.14/Ubuntu20.04/32GBhost','P005p11;P023p23'),
('ES06','P003 E006','Percentile meaning','Could be read as requestP90','CDF across co-location scenarios; no requestP90/P99 inference','PDFp6;Figure7'),
('ES07','P006 E028','Metric population','Could be read as request latency','Added empty-kernel instrumentationP90 overhead at160blocks with aggregation','PDFp12;Figure15'),
('ES08','P007','Trust and comparator','Performance isolation could imply untrusted isolation','Same trust domain; reconstructedREEF-N comparator and aggregate throughput conditions retained','PDFpp9,12-13'),
('ES09','All studies Q9','Calibration','Similar performance-control evidence has inconsistent inheritedQ9 treatment','Retain assessed scores in Eshaal package; flag team calibration before final master totals','SubmittedQ9;Raazia/Rameen proposals;source anchors'),
]
changes=[dict(zip(['Change ID','Scope','Field','Original','Proposed treatment','Evidence'],x)) for x in changes]
method=[
('MA01','Protocol preservation','Green','SubmittedTask1 preserved;later deviations separate','task1/submitted_protocol.pdf; evidence/protocol_amendments.md','Keep baseline hash unchanged; record amendments rather than replacing protocol'),
('MA02','Counting arithmetic','Green','4189-114=4075;3493+559+21+2=4075;21reports=20studies','baseline_PRISMA_Counts.csv; Screening_Log; Duplicate_Removal','Arithmetic verified; this does not validate every screening judgment'),
('MA03','Duplicate linkage','Green','114unique removed IDs;all114canonical targets exist in4075record register','baseline_Duplicate_Removal.csv;baseline_Screening_Log.csv','Keep original links;pairwise semantic validation is a separate task'),
('MA04','559-record stopping rule','Red','559retained records not source-assessed;no instructor acceptance evidence','baseline_Screening_Log.csv;Method_and_Deviations;rameen/novelty_scope_notes.md','Obtain dated scope decision or complete required screening;not automatic exclusions'),
('MA05','Abstract coverage','Yellow','2933records lack abstract;1142have abstract in export','baseline_Screening_Log.csv;Abstract available','Do not describe title/type-only decisions as full abstract reading;prioritize uncertain cases'),
('MA06','Independent review','Red','No separate human votes/signatures supplied for this review pass','Submittedprotocolsection9;teamworkdivision;reviewregisters','Perform rotation and preserve actual independent judgments/disagreements'),
('MA07','Shared search provenance','Yellow','IEEE/Springer shared metadata reuse attributed;actual historical time missing','baseline_Search_Log.csv;IMPORT_PROVENANCE.md','Retain collector attribution and missing-time status;no new GroupB search claim'),
('MA08','ACM provenance','Yellow','Numbered1582active records;master1829parsed but0active;display1600/exportclaim1603 unresolved','baseline_Search_Log.csv;ACM-MASTER;ACM-NUMBERED-UNMAPPED','Resolve original run/file mapping;do not add master to active occurrences'),
('MA09','ScienceDirect provenance','Yellow','1898registered active records;MPS517displayed versus563registered;full archive coverage unresolved','baseline_Search_Log.csv;Method_and_Deviations','Preserve discrepancy;new supplied six-articleZIP is reading material,not an executed search/export archive'),
('MA10','Search fields and synonyms','Yellow','Accepted shared strings differ from frozen protocol;Springer uses full-text indexed general search','baseline_Search_Log.csv;submittedprotocolsearchstrings','Document field/synonym deviations;current reading retrieval is not a search rerun'),
('MA11','Source versions','Yellow','iGniter final copy obtained;ParvaGPU final equivalence remains unresolved;REEF companions linked','eshaal/sources;raazia/README.md','Pin inspected versions and page offsets;do not assume version identity'),
('MA12','QA consistency','Yellow','70items source-appraised;NA preserved;Q9calibration issue remains acrossreviewpackages','QA_Source_Review.csv;submittedprotocolsection10','Adjudicate claim-specificQ9across allstudies before final aggregate scores'),
('MA13','Extraction','Green','30retained outcomes checked with hardware,baseline and statistic boundaries','Outcome_Source_Review.csv','Apply supported anchor corrections during master integration'),
('MA14','Minimum-study instruction','Yellow','Bounded corpus20unique studies;user reports newer minimum21','TEAM_WORK_DIVISION.md;POST_TASK2_CHECKLIST.md;userinstruction','If minimum21unique studies,assess at leastoneadditional eligible study;companions/surveys do not increase primarycount'),
]
method=[dict(zip(['Audit ID','Topic','Status','Finding','Evidence','Next action'],x)) for x in method]
# Independently computed controls from source registers.
screen=rows('Screening_Log');dups=rows('Duplicate_Removal');counter=collections.Counter(r['Decision'] for r in screen)
validation={'checked_utc':now,'sources_inspected':8,'unique_studies':7,'qa_items':len(qa),'qa_not_applicable':sum(r['Original score']=='NA' for r in qa),'eligibility_items':len(elig),'outcome_rows':len(outcomes),'canonical_records':len(screen),'unique_record_ids':len(set(r['Record ID'] for r in screen)),'duplicate_links':len(dups),'unique_removed_ids':len(set(r['Removed record ID'] for r in dups)),'duplicate_targets_exist':all(r['Canonical record ID'] in set(x['Record ID'] for x in screen) for r in dups),'screening_categories':dict(counter),'abstract_missing':sum(r['Abstract available']=='False' for r in screen),'qa_totals_unchanged':True,'independent_human_signoff':False,'master_integrated':False,'methodology_census_completed':False}
assert len(qa)==70 and len(elig)==48 and len(outcomes)==30 and len(screen)==4075 and len(dups)==114
assert 3493+559+21+2==4075 and 4189-114==4075
rotation=[{'Report IDs':'P008-P014','Assigned first reviewer':'Raazia','Assigned independent reviewer':'Eshaal','Status':'Pending actual independent human check','Actual reviewer':'','Checked UTC':'','Decision':'','Disagreement':''}]
d={'sources':sources,'qa':qa,'eligibility':elig,'outcomes':outcomes,'changes':changes,'methodology':method,'rotation':rotation,'reviewer':who,'built_utc':now,'built_pkt':pkt}
for name,k in [('Source_and_Identity_Review.csv','sources'),('QA_Source_Review.csv','qa'),('Eligibility_Source_Review.csv','eligibility'),('Outcome_Source_Review.csv','outcomes'),('Correction_Register.csv','changes'),('methodology_corrections.csv','methodology'),('Independent_Check_Queue.csv','rotation')]:save(name,d[k])
combined=[]
for kind,k in [('identity','sources'),('eligibility','eligibility'),('QA','qa'),('outcome','outcomes')]:
 for r in d[k]:combined.append({'Reviewer':who,'Checked UTC':now,'Study ID':r.get('Study ID',next(s['Study ID'] for s in sources if s['Report ID']==r['Report ID'])),'Report ID':r['Report ID'],'Type':kind,'Item ID':r.get('Item ID',r.get('Evidence ID',r['Report ID'])),'Original value':r.get('Original score',r.get('Value',r.get('Original decision',r.get('Title','')))),'Source page/table/figure':r.get('Source anchor',r.get('Evidence location',r.get('Version checked',''))),'Finding':r.get('Status',r.get('Review decision',r.get('Review status',r.get('Access status','')))),'Rationale':r.get('Rationale',r.get('Review note','')),'Independent human vote':''})
save('source_checks_Eshaal.csv',combined);(out/'review_data.json').write_text(json.dumps(d,indent=2));(out/'validation.json').write_text(json.dumps(validation,indent=2));print(json.dumps(validation,indent=2))

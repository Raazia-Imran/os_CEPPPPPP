"""Source-based ElasticRoom review from the supplied final publisher PDF.

Only extracted evidence is stored in this folder; the reading PDF is not copied.
"""
from pathlib import Path
import csv,json,hashlib,datetime
d=Path(__file__).resolve().parent
pdf=Path('/workspace/scratch/8d52181bc639/upload/3625549.3658654.pdf')
rid,sid,pid='R01093','S028','P031'
doi='10.1145/3625549.3658654';url='https://doi.org/'+doi
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
method='Single automated source-based review under M2026-10-23; no independent human vote asserted'
def write(name,rows):
    with (d/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

source={'Record ID':rid,'Study ID':sid,'Report ID':pid,'Short name':'ElasticRoom',
 'Title':'ElasticRoom: Multi-Tenant DNN Inference Engine via Co-design with Resource-constrained Compilation and Strong Priority Scheduling',
 'Authors':'Lixian Ma; Haoruo Chen; En Shao; Leping Wang; Quan Chen; Guangming Tan',
 'Venue':'International Symposium on High-Performance Parallel and Distributed Computing (HPDC2024)',
 'Year':2024,'DOI':doi,'Source URL':url,'Source SHA256':sha,'PDF pages':14,
 'Source provenance':'User supplied final publisher PDF; previous direct publisher access was blocked',
 'Version verification':'PDFp1 has exact title, six authors, HPDC2024date, ACM ISBN/copyright and exact DOI',
 'Access result':'Full14page PDF inspected; primary methods/results available',
 'Final eligibility decision':'Include','Decision method':method,'Independent human vote':'','Checked UTC':now}
write('Source.csv',[source])
checks=[
 ('IC1','Met','English final14page HPDC2024 primary conference paper; exact DOI, publication citation, ACM ISBN and copyright appear onp1.','PDF p1'),
 ('IC2','Met','TVM-based resource-constrained compilation generates kernel variants; runtime uses multi-stream, kernel-order and candidate scheduling across simultaneous RT/BE DNN requests.','PDF pp4-9; sections3-5 and6.1'),
 ('IC3','Met','Experiments use inference for AlexNet, MobileNet, ResNet50/101/152, DarkNet,VGG19 and BERT-Large, all batch1; RT/BE arrivals use Poisson patterns.','PDF pp9-10 sections6.1-6.2'),
 ('IC4','Met','Goodput is explicitly defined as QoS-satisfying requests divided by maximum batch inference latency. Mean end-to-end RT latency includes queuing; comparative and breakdown results are supplied.','PDF p4 equations1-2; pp10-12 sections6.2-6.4'),
 ('IC5','Met','NVIDIA experiments use one40GB A100, while AMD MI100 results are a separate device evaluation. LocalRT/BE co-location and ResNet50/MobileNet queueing experiments are extractable.','PDF p2 Figure1 caption; p9 section6.1; pp10-12 Figures8-9,13-14'),
 ('IC6','Met','HPDC2024conference publication falls within the original1January2020-to-final-search window.','PDF p1')]
write('Eligibility.csv',[{'Record ID':rid,'Study ID':sid,'Report ID':pid,'Criterion':c,
 'Final decision':v,'Evidence':e,'Anchor':a,'Source URL':url,'Source SHA256':sha,
 'Checked UTC':now,'Decision method':method,'Independent human vote':''} for c,v,e,a in checks])
qa=[
 ('Q1',2,2,'HighGPUutilization/goodput and lowRTlatency under mixed-priority inference are explicit objectives.','PDF pp1-2; section1'),
 ('Q2',2,2,'Compiler search constraints, block-to-SM mapping, lazy kernel ordering and two-stage candidate scheduling are described with algorithms.','PDF pp4-9; sections3-5 and Algorithms1-2'),
 ('Q3',1,2,'Poisson arrivals, model selection and QoSscales are specified, but repeated-trial uncertainty is not established. Scenario count/descriptions conflict with the listed three settings.','PDF p10 section6.2.1'),
 ('Q4',1,2,'A10040GB,MI100,CPU,systemRAM,CUDA/ROCm APIs and batch1workloads are specified. ExactMIGprofile and complete toolchain/model/input configurations are not fully stated.','PDF p9 section6.1; p10 section6.2.1'),
 ('Q5',1,2,'Comparator policies and tuning budgets are described, but KRISP is modified using ElasticRoom-generated kernels and REEF-like priorities; not a direct unchanged-original comparison. Baseline enumeration is inconsistent.','PDF p9 section6.1 Baselines'),
 ('Q6',2,2,'QoS-qualifiedGoodput has an explicit equation and requests/s results. Keep its batch-maximum-latency denominator distinct from ordinary throughput or measuredGPUbusy-time utilization.','PDF p4 equation2; p10 Figures8-9'),
 ('Q7',2,2,'Mean end-to-endRTlatency includes queueing; QoSscale and isolated-latency reference are defined. Queue and end-to-end breakdowns are provided. These are notp99results.','PDF pp10,12; section6.2.1 andFigure14'),
 ('Q8',2,2,'RT/BEco-location, variable arrival settings, heterogeneous models and isolated-versus-shared resource motivation test interference effects. MobileNet shows limited optimization scope.','PDF p3 Figure2; pp10-12 sections6.2,6.4'),
 ('Q9',1,2,'VirtualRoom makes a performance-isolation claim and is tested throughRT/BE latency/interference experiments. It does not establish security orGPUfault-containment guarantees under shared multi-stream execution.','PDF p2 virtualRoom contribution; pp7-8 section5.1; pp11-12 section6.4'),
 ('Q10',1,2,'Algorithms, implementation counts, compiler/API information and explicit framework/model/hardware limits aid informed reproduction. Complete artifact/versioned environment is not established; MI100slowdown is reported.','PDF pp2-3 Limitations; p9 section6.1; p10 section6.2; p12 conclusion')]
write('QA.csv',[{'Record ID':rid,'Study ID':sid,'Report ID':pid,'Criterion':c,'Score':s,
 'Applicable maximum':m,'Rationale':e,'Anchor':a,'Source URL':url,'Source SHA256':sha,
 'Checked UTC':now,'Independent score':''} for c,s,m,e,a in qa])

context_nvidia='OneA10040GB;batch1;randomly selected listedDNNs;PoissonRT/BE arrivals;three listed(RT,BE,QoSscale)settings:(0.4,1.0,1.2),(0.6,1.0,1.2),(0.6,1.0,1.4). Arrival-rate time unitNR; scenario narrative inconsistencies retained.'
context_amd='OneAMDMI100;batch1;same three scenario settings asNVIDIA according tosection6.2.2; hardware result kept separate fromA100; MI100slows down over sustained execution on authorsmachines.'
outcomes=[
 ('ELAST-01','Mean end-to-end RT latency reduction',22,'percent','REEF policy described insection6.1',context_nvidia,'PDF p10 section6.2.1 Figure8a','Author-reported average across scenarios; includesqueueing, notp99. Adapted baseline/configuration and scenario ambiguities prevent direct pooling withoriginalREEFresults.'),
 ('ELAST-02','QoS-qualified Goodput ratio',1.43,'times baseline','REEF policy described insection6.1',context_nvidia,'PDF p10 section6.2.1 Figure8b','Author-reported mean ratio; Goodput definition usesQoS-qualified requests over maximum batch inference latency. Do not call itordinary aggregate throughput or assumeBEQoSdetails.'),
 ('ELAST-03','Mean end-to-end RT latency speedup',1.08,'times baseline','Multi-Stream',context_amd,'PDF p10 section6.2.2 Figure9a','Author-reported average; scenario range1.05-1.10. Do not convert to8percent latency reduction; speedup and reduction differ.'),
 ('ELAST-04','QoS-qualified Goodput ratio',1.17,'times baseline','Multi-Stream',context_amd,'PDF p10 section6.2.2 Figure9b','Author-reported average; scenario range1.11-1.27. Not a matched cross-vendor hardware comparison.'),
 ('ELAST-05','Mean queueing-time speedup',1.8,'times baseline','REEF','OneA10040GB;ResNet50 andMobileNet co-located;RTarrival1.5-2.0 plotted;BEarrival1.0;arrival-rate time unitNR','PDF p12 section6.4.2 Figure14a','Source reports up to4.2times and mean1.8times versusREEF. This is queueing time, notkernel latency orp99.'),
 ('ELAST-06','Mean end-to-end RT latency reduction',19,'percent','REEF','SameA100ResNet50/MobileNet queueing experiment asELAST-05','PDF p12 section6.4.2 Figure14b','Keep separate from22percent average over thedifferentthree-scenario experimentELAST-01.'),
 ('ELAST-07','Kernel GFLOPS deficit','<8','percent below baseline','Ansor','OneMI100;Conv2atthread-block number56 andConv3at64;threeResNet50kernels;50ElasticRoomtuning attempts versus1000Ansor attempts inthisexperiment','PDF p11 section6.3.1 Figure11','Adverse result: ElasticRoom is slower for these kernel configurations. This is not anend-to-end serviceGoodput regression.'),
 ('ELAST-08','Sustained-execution stability','NR','qualitative','No quantitative comparator','AMDMI100on authorsmachines; speed decreases with elapsed execution','PDF p10 section6.2.1 closingparagraph','Adverse validity limitation reported byauthors; magnitude, cause and correction areNR. It may affectoffline generated kernel optimality.')]
write('Outcomes.csv',[dict(zip(['Record ID','Study ID','Report ID','Outcome ID','Metric','Value','Unit','Baseline','Context','Anchor','Interpretation limit'],[rid,sid,pid,*x])) for x in outcomes])
issues=[
 ('Baseline count','Section6.1 saysfivebaselines but namesMIG-FCFS,Multi-Stream,REEFandKRISP. Its wording mentionsKRISPtwice.','PDF p9 section6.1','Keep four named comparators; do notinvent a fifth.'),
 ('Modified baseline','KRISPusesElasticRoom-generated kernels andREEFpriority policy. MIG-FCFSdividesGPUinto twoequalinstances but exactprofile is not supplied.','PDF p9 section6.1','Describe actualevaluated policies; do notequate them to unchangedoriginalsystems orassume fullGPUallocation.'),
 ('Scenario count and description','Text saysfiveexperimentalsettings but lists three. Listedscenario2and3have equalRT0.6/BE1.0whileQoSchanges1.2to1.4; subsequent prose describes scenario2asmore relaxed andscenario3ashighestRTarrival.','PDF p10 section6.2.1','Retain numeric tuples exactly and label narrative conflict; no inferred scenario repair.'),
 ('Metric semantics','Goodput numeratorcountsQoS-qualified requests anddenominator ismaximum batch inference latency. BErequests have noexplicitlatencyrequirement insection6.2.1.','PDF p4 equations1-2;p10 section6.2.1','Do notpool withothergoodput definitions withoutmatchingdenominator/population; BEqualification detail remainsunclear.'),
 ('Arrival-rate units','Poissonarrival rates aregiven numerically withoutan explicit timeunit in theread experimentalsetup.','PDF p10 section6.2.1;p12 Figure14','Record timeunitNR; do notlabel themrequests/s byassumption.'),
 ('MI100 instability','Authors reportMI100slowdownwithlongerexecution, potentiallymakingofflinegeneratedkernels suboptimal.','PDF p10 closingparagraph','Retain avalidity limitation;do notdeclare genericAMDunreliability.'),
 ('Compiler tuningbudget','Servicecomparisonuses1000Ansorattempts versus100resource-constrained attempts;kernel-only comparisonuses1000versus50.','PDF p9 section6.1;p10 section6.3.1','Keep budgetsattached toappropriateexperiment;notoneuniversaltuningbudget.'),
 ('Adverse kernel cases','ElasticRoomunderperformsAnsoronMI100Conv2TB56andConv3TB64byless than8percent.','PDF p11 section6.3.1','Retain alongsideaveragekernelwins;do notstateuniversaldominance.'),
 ('Isolation boundary','VirtualRoomisperformance-prioritycoordinationovermulti-stream; noGPUfaultinjection/adversarialmemoryisolationtestisprovided.','PDF p2 contribution;pp7-8section5.1;pp11-12section6.4','Useperformanceisolationonly;neverinfersecurity/faultcontainmentfromlowlatency.'),
 ('Workload limit','Models arebatch1CNNsandBERT-Large;mainstreamlargegenerativeLLMsandframeworkadaptationarefuturework.','PDF pp2-3 limitations;p9workloads;p12conclusion','Do notgeneralizeobservedresultstoallLLMservingframeworks/hardware.'),
 ('Taxonomy caution','Source groupsMPSwithresource-exclusive mechanisms. That is thepaperclassification anddoesnotproveMPSoffersMIG-equivalenthardware/faultisolation.','PDF p3 section2.1','Retain corpus-wideprimitive/boundarydistinctions instead ofadoptingallsourcewordinguncritically.')]
write('Cautions.csv',[dict(zip(['Record ID','Issue','Evidence based limitation','Anchor','Required interpretation'],[rid,*x])) for x in issues])
write('Reference.csv',[{'Record ID':rid,'Study ID':sid,'Report ID':pid,
 'Authors':'Lixian Ma and Haoruo Chen and En Shao and Leping Wang and Quan Chen and Guangming Tan',
 'Title':source['Title'],'Venue':source['Venue'],'Year':2024,'DOI':doi,'Primary URL':url,
 'Primary SHA256':sha,'Version':'Supplied final14page publisherPDF; firstpageidentityverified','Date basis':'June2024conference'}])
(d/'ElasticRoom.bib').write_text('@inproceedings{s028,\n author={Lixian Ma and Haoruo Chen and En Shao and Leping Wang and Quan Chen and Guangming Tan},\n title={ElasticRoom: Multi-Tenant DNN Inference Engine via Co-design with Resource-constrained Compilation and Strong Priority Scheduling},\n booktitle={International Symposium on High-Performance Parallel and Distributed Computing (HPDC)},\n year={2024},\n doi={10.1145/3625549.3658654},\n url={https://doi.org/10.1145/3625549.3658654}\n}\n')
validation={'record':rid,'study':sid,'report':pid,'final_decision':'Include','all_six_IC_met':True,
 'QA_rows':10,'QA_raw_sum':sum(x[1] for x in qa),'QA_applicable_maximum':20,
 'QA_percent':sum(x[1] for x in qa)/20*100,'outcome_rows':len(outcomes),'caution_rows':len(issues),
 'source_sha256':sha,'source_pages':14,'independent_human_vote':False,
 'reading_PDF_copied_into_repository':False,'root_registers_modified_by_this_builder':False,
 'checked_utc':now}
(d/'Validation.json').write_text(json.dumps(validation,indent=2)+'\n')
assert validation['QA_raw_sum']==15 and validation['outcome_rows']==8
print(json.dumps(validation))

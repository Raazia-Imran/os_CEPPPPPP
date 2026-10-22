from pathlib import Path
import csv,datetime,json
d=Path(__file__).resolve().parent;now=datetime.datetime.now(datetime.timezone.utc).isoformat()
qa={
'R00080':[
(2,'Scheduling, efficiency and isolation objectives are explicit.','p1; section1'),
(2,'TPC scheduling, atomization, right-sizing and driver interposition are described.','pp6-10; sections5-6'),
(1,'Setup and outcome provenance are reported; repeated end-to-end trials and uncertainty need confirmation.','pp10-13; sections7-8'),
(2,'One A10040GB, software stack, model families and arrivals are specified.','pp10-11; Table2 and section7'),
(1,'Comparisons disclose reimplementation, unequal partition fractions and absence of BE for MIG/Limits; identical tenant capacity is not maintained.','pp10-11; sections7-8.1'),
(2,'Normalized throughput, app goodput and SLO-attainment axes are defined.','p11; Figures14-15'),
(2,'End-to-end p99, per-model constraints and request rates are stated.','pp10-12; Table2, Figure16'),
(2,'Multiple inference combinations and hybrid inference/training co-tenancy are tested.','pp11-12; section8.1'),
(2,'Performance-isolation boundary is tested through HP SLO attainment and BE progress; this is not a security/fault guarantee.','p11; Figures14-15'),
(1,'Implementation details and special-kernel limits aid replication; complete artifact execution has not been verified.','p10; section6')],
'R00143':[
(2,'Objective is predictable concurrent service latency with higher throughput.','p1'),
(2,'Operator-group prediction, segmental executors and headroom search are described.','pp4-8; sections4-6'),
(1,'Load, sampling and measurements are detailed; serving-run repeat variability remains to be verified.','pp6-10; sections5.4,7.1-7.3'),
(1,'Software, models and arrivals are documented but Table2 reports an unresolved A100128SM description.','p9 Table2; p15 artifact description'),
(2,'FCFS/SJF/EDF baselines use matched workload generation; query-drop treatment is disclosed.','p9 section7.1'),
(2,'Peak throughput is explicitly queries/s, distinguished from images/sequences per second.','p10 section7.3'),
(2,'p99 and QoS targets are defined with50QPS and separate100QPS peak experiment.','pp9-10; sections7.1-7.3'),
(2,'Pairwise21combinations plus triple/quadruple co-location are tested.','pp9-11 sections7.2-7.4'),
(1,'Performance interference is measured, but separate-process privacy/crash motivation is not a demonstrated GPU security/fault-isolation guarantee.','pp7,9-11; sections6.1,7'),
(2,'Artifact appendix and profiling/scheduling overhead discussion provide replication support and limits.','pp12,15; section7.8 and artifact appendix')],
'R01089':[
(2,'Mixed-criticality inference latency/throughput objective is explicit.','pp1-2'),
(2,'Elastic kernel generator and runtime coordination are explained.','pp5-8; sections5-8'),
(1,'Workloads and comparison metrics are described; repeated-run uncertainty is not established in inspected evaluation.','pp9-11; section9'),
(1,'Models, arrival patterns and CUDA stack are reported; edge GPU name/architecture/core count is internally inconsistent.','pp2,9; section9.1'),
(2,'Three baselines and operator-fusion settings are specified with reasons for exclusions.','p9 section9.1.3'),
(2,'Overall request throughput and achieved occupancy are defined.','p9 section9.1.4; p10 Figure9'),
(1,'Critical-task end-to-end latency is plotted, but run interval and quantile/repetition interpretation need confirmation.','pp9-10 Figure9'),
(2,'Critical and normal task pairs are evaluated under closed-loop, uniform and Poisson patterns.','pp9-10 Table2 and Figure9'),
(1,'Performance protection is measured but under10percent introductory summary does not cover all reported overheads; no security/fault guarantee is established.','pp1,9-10 Figure9'),
(2,'Source-code link, baseline details and compiler/runtime limitations aid replication.','pp2,9; sections8-9')],
'R00656':[
(2,'Responsiveness and throughput under inference co-location are explicit goals.','pp1-2'),
(2,'Page coloring, bimodal tensors and dynamic SM masks define the resource-control mechanism.','sections5-8'),
(1,'Trace scaling and metrics are specified; serving-run repetitions and uncertainty remain unconfirmed.','p10 section9.2'),
(1,'Devices, model list and arrivals are given, but text says12models while Table3 lists11.','p10 Table3 and section9.2'),
(1,'Baseline modifications and fixed MPS split are disclosed; Orion is a policy reimplementation, limiting equivalence.','p10 section9.2'),
(2,'Overall throughput combines LS goodput and BE samples/s; per-BE throughput is tracked.','pp10-11 section9.2 and Figure18'),
(2,'p99 includes queueing and SLO uses n times isolated p99; light/heavy trace conditions are stated.','p10 section9.2'),
(2,'Concurrent LS services and BE model combinations are evaluated on two device types.','pp10-11 Figure18'),
(2,'Performance allocation is tested and lack of fault isolation is explicitly acknowledged; no fault guarantee is inferred.','p11 section10'),
(1,'Implementation and limits are detailed, but complete executable artifact reproduction has not been verified.','p11 section10')]
}
rows=[]
for rid,items in qa.items():
 assert len(items)==10
 for i,(score,reason,anchor) in enumerate(items,1):rows.append({'Record ID':rid,'Criterion':'Q'+str(i),'Prepared score':score,'Maximum':2,'Rationale':reason,'PDF anchor':anchor,'Checked UTC':now,'Appraisal status':'Provisional source appraisal; calibration and independent vote pending','Independent score':'','Adjudicated score':''})
def write(name,rr):
 with (d/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
write('Candidate_QA_Prepared.csv',rows)
outcomes=[
('R00080','LITH-01','SLO attainment','100','percent','MPS45percent; TGS84percent in same plotted scenario','One A100; twoHP plusBE except MIG/Limits omitBE; model combinations and loads in Table2','p11 section8.1 Figure14','Scenario result, not universal hardware guarantee'),
('R00080','LITH-02','Normalized aggregate throughput','1','normalized','MPS1.11; MIG0.71; Limits0.58','Same scenario; normalized definition and unequal supported tenant sets retained','p11 section8.1 Figure14','Compare benefit with SLO attainment and BE availability'),
('R00143','ABA-01','Mean p99 latency reduction','23.1;34.1;23.8','percent','FCFS;SJF;EDF respectively','21pairwise model combinations at50QPS on A100/MPS; latency excludes baseline dropped queries','p9 section7.2 Figure14','QoS violation metric separately counts dropped requests'),
('R00143','ABA-02','Mean peak throughput improvement','25.7;38.1;25.7','percent','FCFS;SJF;EDF respectively','100QPS offered load; throughput is queries/s, not images/s','p10 section7.3 Figure17','VGG16/VGG19 slight degradation retained as adverse result'),
('R01089','MIR-01','Critical latency ratio','1.21;1.28','normalized to Sequential','Sequential1.0','MDTB-A closed-loop AlexNet/CifarNet; RTX2060 and platform labeledXavier respectively','p10 Figure9a-b','21percent and28percent overhead; contradicts universal under10percent reading'),
('R01089','MIR-02','Overall throughput ratio','1.64;1.83','normalized to Sequential','Sequential1.0','MDTB-A; RTX2060 and platform labeledXavier respectively','p10 Figure9c-d','Do not pair maximum throughput from a different workload with these latency values'),
('R00656','SGD-01','Overall throughput ratio','up to1.47;up to1.32','times','Orion policy reimplemented in SGDRC','P40 and RTX A2000 respectively; co-located inference; light/heavy Apollo trace settings','p11 section9.3 Figure18','Maxima are device-specific; MPS is unsupported on P40 in this evaluation'),
('R00656','SGD-02','Best-effort throughput ratio','up to2.36;up to1.79','times','Orion policy reimplemented in SGDRC','P40 and RTX A2000 respectively; LS goodput must be assessed alongside BE throughput','p11 section9.3 Figure18','Does not establish fault isolation; shared CUDA context cannot isolate runtime errors')]
write('Candidate_Outcomes_Prepared.csv',[dict(zip(['Record ID','Outcome ID','Metric','Value','Unit','Baseline','Context','Anchor','Interpretation limit'],x)) for x in outcomes])
progress=json.loads((d/'progress.json').read_text());progress['candidate_QA_items_prepared']=len(rows);progress['candidate_outcomes_prepared']=len(outcomes);progress['candidate_QA_totals']={rid:sum(x[0] for x in items) for rid,items in qa.items()};(d/'progress.json').write_text(json.dumps(progress,indent=2)+'\n')
print('Candidate QA items',len(rows),'outcome rows',len(outcomes),'totals',progress['candidate_QA_totals'])

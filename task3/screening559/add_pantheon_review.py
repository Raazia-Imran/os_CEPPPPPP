"""Explicit source reading of Pantheon; never derive judgments from download alone."""
from pathlib import Path
import csv,datetime,hashlib
d=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rid='R00661';url='https://zhouzimu.github.io/paper/mobisys24-han.pdf'
sha=hashlib.sha256(Path('/workspace/scratch/8d52181bc639/research_reading/Pantheon_MobiSys2024.pdf').read_bytes()).hexdigest()
def append(name, rows):
    p=d/name
    with p.open(newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames;old=list(reader)
    old=[x for x in old if x.get('Record ID')!=rid]
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(old+rows)
append('Full_Text_Source_Register.csv',[{'Record ID':rid,'Candidate name':'Pantheon','DOI':'10.1145/3643832.3661878','Source URL':url,
    'Access result':'HTTP200 PDF downloaded; methods, evaluation and discussion inspected',
    'Source SHA256':sha,'PDF pages':14,'Checked UTC':now,'Reading copy':'Local reading copy; not redistributed',
    'Stage':'Source-based eligibility assessed under M2026-10-23'}])
checks=[
('IC1','Final English MobiSys2024 primary14-page paper identifies exact DOI and conference on first page.','PDF p1'),
('IC2','Middleware schedules distinct concurrent DNN tasks with chunk-level preemption, model variants, and high/low-priority CUDA streams. Scheduler and worker are separate threads, not separate secure processes.','PDF pp3-8; sections3-4'),
('IC3','Nine real-time inference task types from smart traffic, service robot and UAV applications run with an additional best-effort AlexNet.','PDF p8; Table1 and section4'),
('IC4','Deadline miss rate and deadline-adjusted relative accuracy are defined; GPU utilization, best-effort interference and scheduling overhead are evaluated.','PDF pp8-11; sections5.1-5.5'),
('IC5','Main experiments use one Jetson Xavier NX GPU; a separate Nano deployment and NX car case study are identifiable local-device experiments.','PDF pp7-8,10; sections4 and5.3'),
('IC6','June2024 MobiSys publication is inside the original2020-to-search window.','PDF p1')]
append('Full_Text_Eligibility_Prepared.csv',[{'Record ID':rid,'Candidate name':'Pantheon','Criterion':c,
    'Prepared judgment':'Meets criterion on inspected full text','Evidence':e,'Anchor':a,
    'Source URL':url,'Source SHA256':sha,'Checked UTC':now,'Independent vote':'',
    'Adjudicated eligibility':'Pending','Assigned new study ID':''} for c,e,a in checks])
scores=[
('Q1',2,'Objective is timely concurrent DNN inference with acceptable accuracy and memory cost.','pp1-3'),
('Q2',2,'Chunk slicing, preemption, nested redundancy, variant selection and runtime architecture are described.','pp3-8; sections3-4'),
('Q3',1,'Arrival jitter, loads and some variance results are reported; broad repeated-trial and uncertainty reporting is incomplete.','pp8-10; sections4-5.3'),
('Q4',1,'Hardware and task table are detailed, but service-robot/UAV model labels differ between Table1 and following prose.','pp7-8; Table1 and application tasks'),
('Q5',2,'RMS, DMS and RTm-DL are specified; RTm-DL uses the same accuracy constraint and all methods fix the GPU frequency.','p8; section5'),
('Q6',2,'Utilization is compared under increasing concurrent tasks; values are contextual, not a universal efficiency gain.','p9; Figure11'),
('Q7',2,'Deadline miss definition, task deadlines, completion-time traces and nonperiodic arrivals are provided.','pp8-10; Table1, Figures9-10,15'),
('Q8',2,'Best-effort arrival load and increasing real-time task counts test co-tenant interference.','pp9-10; sections5.1,5.3'),
('Q9',1,'Stream-priority and scheduling isolation are described. Runtime uses shared memory/threads; no GPU fault or adversarial isolation guarantee is established.','pp7-8; section4; p10 best-effort load'),
('Q10',1,'Implementation stack, profiling limits and memory trade-offs are described; full reproducibility/calibration is not established by this review.','pp7-8,11-12; sections4,6')]
append('Candidate_QA_Prepared.csv',[{'Record ID':rid,'Criterion':q,'Prepared score':s,'Maximum':2,
    'Rationale':e,'PDF anchor':a,'Checked UTC':now,'Appraisal status':'Source appraisal under M2026-10-23; independent score absent',
    'Independent score':'','Adjudicated score':''} for q,s,e,a in scores])
metrics=[
('PANT-01','Deadline miss rate','0.39-1.10','percent','RMS; DMS; RTm-DL',
 'Three application mixes on Xavier NX; periodic30fps tasks plus best-effort AlexNet; variants constrain accuracy/memory',
 'PDF p9 section5.1 Figure9','Observed deadline performance; early exits alter models and late jobs count as zero accuracy.'),
('PANT-02','GPU utilization','50.85-78.50','percent','RTm-DL46.10-80.05percent',
 'Increasing service-robot task counts; Figure10-11 experiment','PDF p9 section5.1 Figure11',
 'Similar utilization accompanies lower deadline misses; no general utilization dominance.'),
('PANT-03','Mean device power','10.15','W','RTm-DL9.73W',
 'NX INA3221 power monitor; idle4.01W; added online scheduler computation','PDF p11 section5.5 Figure18',
 'Device power is not per-query energy; authors report4.3percent power increase.')]
append('Candidate_Outcomes_Prepared.csv',[dict(zip(['Record ID','Outcome ID','Metric','Value','Unit','Baseline','Context','Anchor','Interpretation limit'],[rid,*x])) for x in metrics])
print('Pantheon: six source criteria, ten QA items, three outcomes; QA16/20.')

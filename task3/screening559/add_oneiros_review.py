"""Source-based Oneiros review; author-hosted final conference PDF inspected."""
from pathlib import Path
import csv,datetime,hashlib
d=Path(__file__).resolve().parent; now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rid='R00086';url='https://lca.ece.utexas.edu/pubs/Li_SoCC_2025.pdf'
sha=hashlib.sha256(Path('/workspace/scratch/8d52181bc639/research_reading/Oneiros_SoCC2025.pdf').read_bytes()).hexdigest()
def append(name,rows):
    p=d/name
    with p.open(newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames;old=list(reader)
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows([x for x in old if x.get('Record ID')!=rid]+rows)
append('Full_Text_Source_Register.csv',[{'Record ID':rid,'Candidate name':'Oneiros','DOI':'10.1145/3772052.3772215',
    'Source URL':url,'Access result':'Author-hosted final conference PDF retrieved; methods, experiments and limitations inspected',
    'Source SHA256':sha,'PDF pages':14,'Checked UTC':now,'Reading copy':'Local copy; not redistributed',
    'Stage':'Source-based eligibility assessed under M2026-10-23'}])
checks=[
('IC1','English SoCC2025 final14-page primary conference paper; exact DOI and venue on p1; publisher proceeding independently confirms article identity.','PDF p1; publisher10.1145/3772052'),
('IC2','Parameter-memory remapping, controller and asynchronous transfer engine support temporal and spatial multi-model GPU sharing, including MPS and MIG scenarios.','PDF sections4-6; pp9-11 section7.2-7.3'),
('IC3','LLM inference workloads comprise distinct OPT and Llama model instances; C1 has three models and C2 has two.','PDF p9 Table1 and section7.1'),
('IC4','P99 TTFT/TBT and generated tokens/s are defined; per-configuration temporal and spatial comparisons are supplied. TTFT includes queuing.','PDF pp9-11 sections7.1-7.4; p11 footnote6'),
('IC5','Experiments use one GH200 system and concurrent local model combinations; CPU memory extends GPU capacity. Hardware labels require clarification.','PDF p9 section7.1 and Table1'),
('IC6','SoCC conference is November2025; the queue indexes2026. Both dates are within the submitted window. Preserve the distinction between venue year and publication/index date.','PDF p1; frozen queueR00086')]
append('Full_Text_Eligibility_Prepared.csv',[{'Record ID':rid,'Candidate name':'Oneiros','Criterion':c,
    'Prepared judgment':'Meets criterion on inspected full text','Evidence':e,'Anchor':a,'Source URL':url,
    'Source SHA256':sha,'Checked UTC':now,'Independent vote':'','Adjudicated eligibility':'Pending','Assigned new study ID':''} for c,e,a in checks])
qa=[
('Q1',2,'Memory pressure and latency/throughput objectives for multi-tenant serving are explicit.','p1; section1'),
('Q2',2,'Memory remapping, layer selection, asynchronous engine and controller policies are described.','sections4-6'),
('Q3',1,'Traces, datasets and load variations are reported; repeated-trial uncertainty and seeds are not established by this review.','p9 section7.1; pp9-12 evaluation'),
('Q4',1,'Versions, platform and model reservations are supplied; GH200/H20096GB description and Figure13 isolation caption need clarification.','p9 section7.1; p11 Figure13'),
('Q5',2,'vLLM and Pie baselines, runtime versions and same-platform comparisons are stated; outcome contexts retained.','pp9-11 sections7.1-7.4'),
('Q6',2,'Tokens/s and memory-reservation contexts are reported for temporal and spatial sharing.','p9 Table1; pp10-11 Figures8-14'),
('Q7',2,'P99 TTFT/TBT are defined; queuing inclusion and varying arrivals are explicit.','p9 section7.1; p11 footnote6'),
('Q8',2,'C1/C2, unequal arrival rates and input-length combinations test interactions between models.','pp9-10 Table1; Figures9-10'),
('Q9',1,'MPS and MIG boundaries are discussed, but isolation wording and Figure13 caption conflict; no fault/adversarial isolation test is demonstrated.','pp9-11 section7.3; Figure13'),
('Q10',2,'Source repository, software versions and transfer/idle-load trade-offs and ablations are supplied. Artifact was not executed here.','p1 repositoryURL; p9 section7.1; pp11-12 sections7.5-7.6')]
append('Candidate_QA_Prepared.csv',[{'Record ID':rid,'Criterion':q,'Prepared score':s,'Maximum':2,
    'Rationale':e,'PDF anchor':a,'Checked UTC':now,'Appraisal status':'Source appraisal under M2026-10-23; no independent score',
    'Independent score':'','Adjudicated score':''} for q,s,e,a in qa])
metrics=[('ONEI-01','P99 TBT reduction',65.5,'percent'),('ONEI-02','P99 TTFT reduction',20.7,'percent'),('ONEI-03','Throughput increase',6.6,'percent')]
append('Candidate_Outcomes_Prepared.csv',[{'Record ID':rid,'Outcome ID':oid,'Metric':metric,'Value':v,'Unit':unit,
    'Baseline':'vLLM','Context':'C1 three-model combination; Alpaca/ShareGPT and Azure coding traces; author-reported average across varied arrival rates under non-strict spatial sharing',
    'Anchor':'PDF pp9-10 Table1 and section7.3 Figure12','Interpretation limit':'Same-system contextual result; source calls this MPS-like non-strict isolation. Not a fault-isolation guarantee or general hardware result.'} for oid,metric,v,unit in metrics])
print('Oneiros: six source criteria, ten QA items(17/20), three outcomes.')

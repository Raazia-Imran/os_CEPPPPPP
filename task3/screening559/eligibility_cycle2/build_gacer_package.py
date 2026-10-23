"""Final-version GACER review; original2023preprint is not substituted."""
from pathlib import Path
import csv,json,hashlib,datetime
d=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rid='R00647';sid='S027';pid='P030';doi='10.1145/3676536.3676718'
url='https://par.nsf.gov/servlets/purl/10643398'
pdf=Path('/workspace/scratch/8d52181bc639/research_reading/cycle2/GACER_final.pdf')
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
def write(name,rows):
    with (d/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
source={'Record ID':rid,'Reserved study ID':sid,'Reserved report ID':pid,'Candidate name':'GACER',
 'Title':'GACER: Granularity-Aware ConcurrEncy Regulation for Multi-Tenant Deep Learning',
 'Authors':'Yongbo Yu; Fuxun Yu; Zhi Tian; Xiang Chen','Venue':'IEEE/ACM International Conference on Computer-Aided Design (ICCAD2024)',
 'Conference year':2024,'Frozen indexed year':2025,'DOI':doi,'Source URL':url,'Source SHA256':sha,'PDF pages':9,
 'Access result':'HTTP200; final typeset conference PDF inspected','Checked UTC':now,
 'Version caution':'The2023arXiv version has11pages and seven authors. Final9page report has four authors. Use final evidence only; retain queue/index year separately.',
 'Final eligibility':'Include','Decision method':'Single automated source-based review under M2026-10-23; no independent human vote asserted'}
write('GACER_Source.csv',[source])
checks=[
 ('IC1','Met','English final9page ICCAD2024 primary conference paper with exact DOI, copyright and venue citation.','PDF p1'),
 ('IC2','Met','Cross-stack runtime/compiler optimization splits microbatches and reorders operators across concurrent independent DNN model graphs using GPU streams and CPU/GPU synchronization.','PDF pp4-6; sections4.2-4.4'),
 ('IC3','Met','Section5.1 specifies model-inference batches and vision/language/recommendation workloads; training motivation is not substituted for inference results.','PDF p7 section5.1'),
 ('IC4','Met','Normalized batch-completion latency, achieved SM occupancy and optimization costs are reported with comparator descriptions and model settings.','PDF pp7-8; Figures7-8; Tables2-4'),
 ('IC5','Met','Section5.4 explicitly evaluates2,4and5concurrent models on one A100; Table2 provides within-device latencies. P6000/1080Ti outcomes are separate.','PDF p8 section5.4 and Tables2,4'),
 ('IC6','Met','ICCAD2024conference date and indexed2025date are both inside the2020-to-search window.','PDF p1; frozenR00647metadata')]
write('GACER_Eligibility.csv',[{'Record ID':rid,'Study ID':sid,'Report ID':pid,'Criterion':c,'Final decision':v,
 'Evidence':e,'Anchor':a,'Source URL':url,'Source SHA256':sha,'Checked UTC':now,'Independent human vote':''} for c,v,e,a in checks])
qa=[
 ('Q1',2,2,'Multi-tenant resource efficiency and execution-latency objectives are explicit.','PDF pp1-2'),
 ('Q2',2,2,'Operator splitting/fusion, stage pointers, stream synchronization and joint heuristic search are described.','PDF pp4-6; sections4.2-4.4'),
 ('Q3',1,2,'Workload sizes and profiling procedure are described, but trials/seeds, confidence intervals and warm-up details are not established.','PDF pp6-8; Algorithm1 and section5'),
 ('Q4',1,2,'GPU models, model types, datasets, batch/image sizes are stated; complete software/driver versions and device-memory configurations are not supplied.','PDF p7 section5.1; p8 Table4'),
 ('Q5',1,2,'Sequential, stream-parallel and MPS-style comparators are defined. Static FLOPS-based sharing and CNN-only AutoMT support constrain fairness across heterogeneous model mixes.','PDF p7 sections5.1-5.2 and Figure7'),
 ('Q6',2,2,'Achieved SM occupancy is measured by Nsight; latency speedups and tenant-count scaling are inspectable. Occupancy is not GPU busy-time utilization.','PDF pp7-8; Figure8 and Table2'),
 ('Q7',1,2,'Batch-completion latencies are extractable; per-tenant service tails/SLO/load-arrival measurements are not established.','PDF pp7-8 Figure7 and Table2'),
 ('Q8',2,2,'Concurrent model mixes,2/4/5tenants, batch variation and three GPU types test co-location behavior.','PDF pp7-8 sections5.1-5.6'),
 ('Q9','N/A',0,'No resource/security/fault-isolation guarantee is claimed. Stage synchronization and occupancy optimization do not establish such a boundary; protocol permits reasonedN/A for unclaimed criteria.','PDF sections4-6; no isolation claim/test identified'),
 ('Q10',1,2,'Algorithms, profiling and overhead dependence aid informed reproduction; complete artifact/environment and repeated-trial methodology are not provided.','PDF pp5-8 Algorithm1 and Tables3-4')]
write('GACER_QA.csv',[{'Record ID':rid,'Study ID':sid,'Report ID':pid,'Criterion':c,'Score':s,'Applicable maximum':m,
 'Rationale':e,'Anchor':a,'Source URL':url,'Source SHA256':sha,'Checked UTC':now,'Independent score':''} for c,s,m,e,a in qa])
outcomes=[
 ('GACER-01','Batch-completion latency',3.30,'ms','CuDNN-Seq4.32ms; TVM-Seq4.20ms; Stream-Parallel3.81ms; Competitive-Sharing3.89ms','OneA100; two concurrent modelsVGG16+LSTM; Table2 reports1.31x speedup versus sequential','PDF p8 Table2','Batch completion is not per-request p99 or a serviceSLO.'),
 ('GACER-02','Batch-completion latency',22.14,'ms','CuDNN-Seq37.86ms; TVM-Seq32.24ms; Stream-Parallel25.31ms; Competitive-Sharing27.22ms','OneA100; five concurrent modelsVGG+R18+R34+BERT+DLRM; source reports1.71x versus sequential','PDF p8 Table2','Table2labelsVGGwithoutversion; do not silently normalize it toVGG16.'),
 ('GACER-03','Optimization cost range','0.84-1.26','s','No comparator for this overhead table','Table3three model mixes, batch sizes4to128; heuristic/search optimization overhead','PDF p8 Table3 and section5.5','Seconds of optimization are not request latency; online suitability is conditional on tolerated reconfiguration delay.'),
 ('GACER-04','Batch-completion latency',8.51,'ms','CuDNN-Seq14.50ms; Stream-Parallel10.13ms','OneGTX1080Ti; R34+LSTM+BST; visionbatch8; source reports1.70x versus sequential','PDF p8 Table4 and section5.6','Different hardware and workload fromA100Table2; do not pool as matched comparison.')]
write('GACER_Outcomes.csv',[dict(zip(['Record ID','Study ID','Report ID','Outcome ID','Metric','Value','Unit','Baseline','Context','Anchor','Interpretation limit'],[rid,sid,pid,*x])) for x in outcomes])
write('GACER_Reference.csv',[{'Record ID':rid,'Study ID':sid,'Report ID':pid,'Authors':'Yongbo Yu and Fuxun Yu and Zhi Tian and Xiang Chen',
 'Title':source['Title'],'Venue':source['Venue'],'Year':2024,'DOI':doi,'Primary URL':url,'Primary SHA256':sha,
 'Date basis':'Conference2024; repository/index2025retained separately','Version':'Final9page conference report, not2023arXiv11page precursor'}])
(d/'GACER.bib').write_text('@inproceedings{s027,\n author={Yongbo Yu and Fuxun Yu and Zhi Tian and Xiang Chen},\n title={GACER: Granularity-Aware ConcurrEncy Regulation for Multi-Tenant Deep Learning},\n booktitle={IEEE/ACM International Conference on Computer-Aided Design (ICCAD)},\n year={2024},\n doi={10.1145/3676536.3676718},\n url={https://par.nsf.gov/servlets/purl/10643398}\n}\n')
(d/'GACER_Synthesis.md').write_text('''# GACER addition

Final source:GACERICCAD2024,9pages,fourauthors. The2023preprint differs in authorship and content and must not supply final numerical claims.

GACER adds a compiler/runtime hybrid using operator microbatch splitting and staged cross-model scheduling over native streams. This is resource-efficiency coordination rather than a demonstrated fault/security-isolation boundary. On oneA100,Table2reports3.30ms forVGG16+LSTM versus4.32ms sequential, and22.14ms for five models versus37.86ms sequential. These are batch-completion measurements, not tail serving latencies. The same paper measures achievedSMoccupancy; this is distinct fromGPUbusy-time utilization. Table3reports0.84-1.26seconds of optimization, creating an explicit adaptation-cost trade-off.

QA:13/18applicablepoints(72.2%);Q9reasonedN/A because no isolation guarantee is claimed. Do not force this into a20point denominator or replaceN/Awithzero. Lower score does not exclude an eligible study.

RQ1:cross-stack operator scheduling/microbatch granularity. RQ2:batch-completion latency, achievedSMoccupancy, optimization seconds. RQ3:effect depends on model heterogeneity, tenant count andGPU. RQ4:profiling/search and transformation/synchronization overhead, incomplete replication details, no demonstrated isolation boundary. RQ5:consider for known multi-model batch mixes when profiling/optimization cost is acceptable; it does not establish better online tail-SLOor fault isolation thanMIG/MPS.
''')
(d/'GACER_Validation.json').write_text(json.dumps({'six_criteria_met':True,'QA_items':10,'QA_raw_sum':13,'QA_applicable_maximum':18,'QA_percent':13/18*100,'outcome_rows':4,'source_pages':9,'source_sha256':sha,'independent_human_vote':False,'IDs_reserved_by_root':True},indent=2)+'\n')
print('GACER final package saved;13/18QA;4outcomes.')

from pathlib import Path
import csv,json,datetime,hashlib
d=Path(__file__).resolve().parent;r=d.parents[1];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sources={
'R00080':{'name':'LithOS','file':'LithOS_SOSP2025.pdf','doi':'10.1145/3731569.3764818','url':'https://www.pdl.cmu.edu/PDL-FTP/BigLearning/lithos_sosp25.pdf','pages':17},
'R00143':{'name':'Abacus','file':'Abacus_SC2021.pdf','doi':'10.1145/3458817.3476143','url':'https://www.microsoft.com/en-us/research/wp-content/uploads/2022/07/3458817.3476143.pdf','pages':15}}
evidence={
'R00080':[
('IC1','SOSP 2025 typeset English primary conference paper, DOI and 17-page citation on first page.','PDF p1'),
('IC2','TPC allocation, kernel atomization and CUDA-driver interposition schedule independent GPU contexts; implementation builds on MPS.','PDF pp6-10; sections5-6'),
('IC3','Inference-only setup has two high-priority model applications and one best-effort inference app; mixed training experiment is separate.','PDF pp10-11; section7, Table2 and section8.1'),
('IC4','SLO attainment, normalized throughput/goodput and end-to-end p99 latency are defined and compared under stated load.','PDF pp11-12; section8.1, Figures14-16'),
('IC5','Primary testbed is one A100 SXM4, 40GB, 108SM; local inference app combinations are evaluated.','PDF pp10-11; section7 and section8.1'),
('IC6','2025 final publication is within the submitted 2020-to-final-search window and predates the recorded October2026 search checkpoint.','PDF p1; submitted protocol section6')],
'R00143':[
('IC1','SC2021 typeset English primary conference paper identifies DOI, venue and 14-page main paper; supplied PDF also has an artifact appendix.','PDF p1 and p15'),
('IC2','Separate DNN service processes are coordinated through segmental executors and deterministic overlapped operator groups on a shared GPU.','PDF pp7-9; sections6.1-7.1'),
('IC3','Seven vision/NLP inference services are tested in pairwise and higher-order co-location.','PDF pp6,9-11; Table1 and sections7.1-7.4'),
('IC4','p99 latency, QoS violation and queries-per-second throughput are defined with load and baseline policies.','PDF pp9-10; sections7.1-7.3 and Figures14-17'),
('IC5','Local experiments run on one A100 with MPS; a separate 16-GPU cluster experiment is distinguishable.','PDF pp9,11; sections7.1,7.5-7.6'),
('IC6','2021 conference publication is within the submitted main window beginning1January2020.','PDF p1; submitted protocol section6')]}
sources.update({
'R01089':{'name':'Miriam','file':'Miriam_SenSys2023.pdf','doi':'10.1145/3625687.3625789','url':'https://neawhen.github.io/neiwen.github.io/assets/pdf/sensys23-miriam.pdf','pages':14},
'R00656':{'name':'SGDRC','file':'SGDRC_PPoPP2025.pdf','doi':'10.1145/3710848.3710863','url':'https://huaicheng.github.io/p/ppopp25-sgdrc.pdf','pages':15}})
evidence.update({
'R01089':[
('IC1','English SenSys2023 typeset14-page primary paper with exact DOI; frozen2024 year conflicts with first-page2023 publication and requires metadata correction.','PDF p1'),
('IC2','Elastic kernel transformation and runtime coordination control co-execution between critical and normal DNNs.','PDF pp5-8; sections5-8'),
('IC3','Mixed-critical DNN Task Benchmark explicitly uses concurrent critical and normal inference models.','PDF p9; section9.1.2 and Table2'),
('IC4','End-to-end critical latency, overall request throughput and achieved occupancy are defined and evaluated.','PDF pp9-11; sections9.1.4-9.3'),
('IC5','Per-device experiments compare co-running workloads on RTX2060 and an edge platform; platform-label inconsistency must remain flagged.','PDF p9; section9.1 and Table2'),
('IC6','Typeset SenSys2023 publication is inside2020-to-final-search window; no historical exception is needed.','PDF p1; submitted protocol section6')],
'R00656':[
('IC1','English typeset PPoPP2025 primary paper identifies the exact DOI and conference publication.','PDF p1'),
('IC2','Software page coloring, bimodal tensors and tidal SM masks dynamically allocate memory bandwidth and compute between services.','PDF sections5-8'),
('IC3','Latency-sensitive inference services are colocated with best-effort inference models; workloads and arrival trace are specified.','PDF p10; Table3 and section9.2'),
('IC4','p99 including queueing, SLO attainment, best-effort sample throughput and overall goodput/throughput are defined.','PDF pp10-11; sections9.2-9.3'),
('IC5','P40 and RTX A2000 are evaluated as local devices with clients/server on the same host; local co-tenant outcomes are inspectable.','PDF p10 section9.2'),
('IC6','March2025 conference publication predates recorded October2026 search and is in the main window.','PDF p1; submitted protocol section6')]})
rows=[];register=[]
for rid,s in sources.items():
 p=Path('/workspace/scratch/8d52181bc639/research_reading')/s['file'];sha=hashlib.sha256(p.read_bytes()).hexdigest()
 register.append({'Record ID':rid,'Candidate name':s['name'],'DOI':s['doi'],'Source URL':s['url'],'Access result':'HTTP200 PDF downloaded and relevant full-text methods/results inspected','Source SHA256':sha,'PDF pages':s['pages'],'Checked UTC':now,'Reading copy':'Private local reading copy; not redistributed in repository','Stage':'First full-text eligibility review prepared; independent review pending'})
 for ic,reason,anchor in evidence[rid]:rows.append({'Record ID':rid,'Candidate name':s['name'],'Criterion':ic,'Prepared judgment':'Meets criterion on inspected full text','Evidence':reason,'Anchor':anchor,'Source URL':s['url'],'Source SHA256':sha,'Checked UTC':now,'Independent vote':'','Adjudicated eligibility':'Pending','Assigned new study ID':''})
def write(name,rr):
 with (d/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
write('Full_Text_Source_Register.csv',register);write('Full_Text_Eligibility_Prepared.csv',rows)
notes=[
('R00080','Version','Author-hosted SOSP version used. The older arXiv abstract has different SOTA latency/throughput summaries; do not mix versions.','PDF p1 versus arXiv2504.15465 abstract'),
('R00080','Baseline fairness','Inference-only experiment has three applications for LithOS/MPS but no BE application for MIG/Limits; MIG uses3/7-4/7 rather than25/75 split. Comparisons are scenario dependent.','PDF p11 section8.1'),
('R00080','Implementation portability','REEF and Orion baselines were reimplemented and extended; persistent/cross-block kernels disable atomization and stealing. Functional support on other architectures is not a repeated performance evaluation.','PDF p10 sections6-7'),
('R00143','Hardware discrepancy','Table2 labels A100 as128SM, which needs verification against actual device configuration; do not silently copy or correct this hardware field.','PDF p9 Table2; artifact p15 A100-PCIE-40GB'),
('R00143','Measurement population','Baseline queries past QoS deadline are dropped and excluded from latency calculations, but dropped queries are counted in QoS violation. Throughput is queries/s, not images/s.','PDF pp9-10 sections7.1-7.3'),
('R00143','Adverse result','VGG16/VGG19 saturated operators can have slight performance degradation from scheduling overhead. Profiling cost and CPU prediction overhead must accompany benefit claims.','PDF pp10,12 sections7.3 and7.8'),
('R00062;R00145;R00299','Date scope clarification','The submitted protocol starts1January2020. These2020 records do not need a pre2020 seminal exception. Earlier batch notes asking to check an exception condition are resolved by protocol section6.','Submitted protocol PDF p8 section6'),
('R01089','Publication year','Frozen queue says2024, but the retrieved typeset paper identifies SenSys2023 and the exact DOI. Preserve old metadata and propose a2023 correction.','PDF p1'),
('R01089','Platform description','Section9.1.1 labels a Jetson AGX Xavier as Pascal256CUDA cores, while the background describes TX2. Verify actual platform identity before normalizing hardware; do not silently repair the source.','PDF pp2,9'),
('R01089','Claim boundary','Introductory summary says under10percent critical latency overhead, but the closed-loop result on p9 describes a21percent increase versus Sequential. Attach workload and baseline to each claim.','PDF pp1-2,9 section9.2'),
('R00656','Model count','Abstract and Table3 identify11models (8LS,3BE), while section9.2 says12. Preserve this internal reporting discrepancy.','PDF pp1,10'),
('R00656','Baseline/configuration','Orion policy is reimplemented within SGDRC, MPS uses a50/50compute split, and all systems disable dynamic batching. SLO threshold depends on number of concurrent services.','PDF p10 section9.2'),
('R00656','Adverse result','Overall throughput is lower than Multi-streaming in some cases although its LS goodput/latency is better. Do not state universal throughput dominance.','PDF pp10-11 section9.3')]
write('Full_Text_Review_Cautions.csv',[dict(zip(['Record IDs','Issue','Evidence based limitation or clarification','Anchor'],x)) for x in notes])
links=[('R00070','R00149','Matching title and abstract; different DOIs','Verify publication version relation; retain record provenance'),('R00300','R00336','NEPTUNE conference/journal titles and mechanism overlap','Compare authors and full texts before study linkage'),('R01567','R01570','HealthServe same title/abstract; different DOIs','Verify article/proceedings relation'),('R01524','R02180','WAGES exact title/abstract; second record lacks DOI','Check source metadata; likely duplicate import'),('R00645','R02185','DistMind exact title/abstract; second record lacks DOI','Check source metadata; likely duplicate import'),('R01087','R02186','MPS granularity paper same abstract; year/punctuation differ','Verify2024 proceeding identity and link imports'),('R00652','S012/P012','Torpor journal title differs from included USENIX report','Compare authors/experiments and link companion study if confirmed'),('R00038','R01098','Energy/carbon-sharing theme and modeling overlap only','Do not assume duplicate; check authors/content'),('R00643','R01082','Janus shared system name but substantially different work','Do not merge by system name alone')]
write('Report_Identity_Proposals.csv',[dict(zip(['Record A','Record B or existing study','Observed basis','Required resolution'],x)) for x in links])
p=json.loads((d/'progress.json').read_text());p.update({'new_full_text_eligibility_assessments':len(sources),'full_text_criteria_prepared':len(rows),'candidate_studies_meeting_first_review_criteria':len(sources),'new_included_studies':0,'independent_human_votes':0,'prisma_changed':False,'frozen_unique_studies':20});(d/'progress.json').write_text(json.dumps(p,indent=2)+'\n')
print(f'Saved{len(rows)}criterion judgments for{len(sources)}candidates; main corpus unchanged.')

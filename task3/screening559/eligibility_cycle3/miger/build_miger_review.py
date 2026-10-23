"""Preserve unresolved MIGER inference-scope evidence without forcing inclusion."""
from pathlib import Path
import csv,hashlib,json,datetime
d=Path(__file__).resolve().parent
pdf=Path('/workspace/scratch/8d52181bc639/upload/3673038.3673089.pdf')
sha=hashlib.sha256(pdf.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rid='R00001';doi='10.1145/3673038.3673089';url='https://doi.org/'+doi
def write(name,rows):
    with (d/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
write('Source.csv',[{'Record ID':rid,'Study ID':'','Report ID':'','Reserved identifiers if later eligible':'S030/P033; not assigned by this review',
 'Title':'MIGER: Integrating Multi-Instance GPU and Multi-Process Service for Deep Learning Clusters',
 'Authors':'Bowen Zhang; Shuxin Li; Zhuozhao Li','Venue':'53rd International Conference on Parallel Processing (ICPP2024)',
 'Year':2024,'DOI':doi,'Source URL':url,'Source SHA256':sha,'PDF pages':10,'Pages':'504-513',
 'Access result':'User supplied final publisher PDF; all methods/results inspected',
 'Final eligibility decision':'Pending scope clarification; not included and not excluded',
 'Decision method':'Single automated source-based review under M2026-10-23','Independent human vote':'','Checked UTC':now}])
checks=[
 ('IC1','Met','Final English ICPP2024 primary10page paper identifies exact DOI and three authors on p1.','PDF p1'),
 ('IC2','Met','MIGER proposes and evaluates a hierarchical scheduler combining MPS inside MIG partitions; at most one online inference and one offline training job share each partition.','PDF pp4-7 sections4.1-4.6 and5.1'),
 ('IC3','Pending joint inference evidence','Mixed training/inference workloads are explicit, but the main measured outcomes are aggregate offline job completion/makespan. The explicit local BERT latency test varies MIG allocation without an identified co-tenant. A separable inference outcome under the concurrent hybrid setup is not established.','PDF p3 Figure4; p7 Table3 and sections5.1-5.2'),
 ('IC4','Pending joint inference evidence','Local MPS/MIG throughput and prediction-error experiments are measured, but job mode is not identified for Figure2 and Figure3 results aggregate mixed model types. Figure4 reports inference allocation behavior, not a local concurrent hybrid result.','PDF pp2-3 Figures2-4 and Table2'),
 ('IC5','Pending concurrent-inference linkage','Figure4 gives one-A10080GB BERT-inference latency/utilization across MIG profiles. This is a local inference comparison, but its co-tenant setup is absent. Figure2 provides co-tenant measurements without identifying inference mode; the two experiments must not be combined into one invented concurrent-inference effect.','PDF pp2-3 section3.1-3.2; Figures2-4'),
 ('IC6','Met','August2024 conference publication is within the original2020-to-search window.','PDF p1')]
write('Eligibility.csv',[{'Record ID':rid,'Criterion':c,'Decision':v,'Evidence':e,'Anchor':a,'Source URL':url,
 'Source SHA256':sha,'Checked UTC':now,'Independent human vote':''} for c,v,e,a in checks])
observations=[
 ('MIGER-C01','BERT inference QoS outcome','3g.40gb and4g.40gb violate;7g.80gb satisfies','QoS threshold<150ms','MIG profile comparison on oneA10080GB','PDF p3 section3.2 Figure4','No concurrent co-tenant is specified; not a measured hybrid co-tenant inference effect. Local batch size and latency statistic areNR.'),
 ('MIGER-C02','GPU utilization underBERT inference','approximately50','percent','7g.80gb profile on oneA10080GB','PDF p3 section3.2 Figure4','Author text approximation retained; no graph digitization. This is not proof of shared-tenant inference utilization.'),
 ('MIGER-C03','Average job-completion-time reduction',46.6,'percent','MuxFlow; real8GPUcluster,150online/offlinejobs','PDF p7 section5.2 Figure8','Aggregate offline/cluster completion result; not a separable oneGPUinference latency outcome. Do not add to included-study quantitative synthesis while eligibility is unresolved.'),
 ('MIGER-C04','Small-job completion behavior','Higher JCT than comparators','qualitative','MISO andMuxFlow in realcluster jobCDF','PDF p7 section5.2 Figure9','Adverse result; magnitude and exact small-job thresholdNR. Do not omit if eventually integrated.')]
write('Candidate_Observations.csv',[dict(zip(['Record ID','Observation ID','Metric','Value','Unit','Context','Anchor','Interpretation limit'],[rid,*x])) for x in observations])
gaps=[
 ('Concurrent inference endpoint','Identify a measured online inference latency/QoS result for a specified online model sharing one GPU or one MIG partition with a named offline/online co-tenant.','Figures2-3do not identify job modes; Figure4has no namedco-tenant; aggregateJCTalone is insufficient.'),
 ('Modes in local experiments','Establish whetherResNet50/GAN/MLP inFigure2include an inference job, and which mixed train/inference combinations underpinFigure3.','Table2lists potential model modes but does not map individual Figure2/3observations to exact modes.'),
 ('Measured QoS versus design rule','Locate direct onlineQoS measurements, including violations/terminations, forMIGER local hybrid co-location.','Page6defines predictor-basedallocation and immediateofflinejobterminationonQoSviolation; a designresponse is not a reported measured latency distribution.'),
 ('Decision path','If no such evidence is available, adjudicate the protocol scope explicitly; do not invent per-GPUinference results or silently relax criteria.','User-reported permission changesreviewerprocess, notscientificeligibilitycriteria.')]
write('Evidence_Gaps.csv',[dict(zip(['Record ID','Issue','Exact evidence needed','Why current PDF does not close it'],[rid,*x])) for x in gaps])
write('Reference.csv',[{'Record ID':rid,'Authors':'Bowen Zhang and Shuxin Li and Zhuozhao Li',
 'Title':'MIGER: Integrating Multi-Instance GPU and Multi-Process Service for Deep Learning Clusters',
 'Venue':'53rd International Conference on Parallel Processing (ICPP2024)','Year':2024,'Pages':'504-513',
 'DOI':doi,'Primary URL':url,'Primary SHA256':sha,'Use':'Candidate/context reference; not a new included-study count'}])
(d/'MIGER_candidate.bib').write_text('@inproceedings{candidate_miger,\n author={Bowen Zhang and Shuxin Li and Zhuozhao Li},\n title={MIGER: Integrating Multi-Instance GPU and Multi-Process Service for Deep Learning Clusters},\n booktitle={53rd International Conference on Parallel Processing (ICPP)},\n year={2024},\n pages={504--513},\n doi={10.1145/3673038.3673089},\n url={https://doi.org/10.1145/3673038.3673089}\n}\n')
(d/'REVIEW.md').write_text('''# MIGER remains pending

The user-supplied final paper is fully available. Access is no longer the blocker. The open issue is whether the reported evidence jointly satisfies concurrent GPU sharing and separable inference outcomes under the submitted narrow protocol.

The paper clearly proposes MPS within MIG partitions and uses online inference plus offline training. Its explicit one-device BERT experiment compares MIG allocation sizes, but does not identify another concurrent tenant. Its local three-job throughput comparison does not label the exact jobs as training or inference. The mixed-workload prediction experiment aggregates possible training/inference modes. These separate experiments must not be assembled into an invented same-device concurrent-inference result.

The main benefits reported for MIGER concern cluster/job completion, makespan and offline throughput. They are useful context for a hybrid MPS/MIG design, but do not by themselves close the inference-specific selection criterion. Therefore this review neither includes nor excludes the record. Reserved identifiers S030/P033 remain unassigned. QA/extraction for an included study should not be manufactured before eligibility closes; Candidate_Observations.csv is explicitly provisional context.

If later evidence identifies a specified inference model's measured latency or QoS while sharing a physical GPU/partition with an identified co-tenant, revisit IC3/IC4/IC5. A clear source-based scope adjudication is an alternative, but it must be documented and consistently applied. It cannot be hidden as an access failure or automatic EC6 exclusion.

Keep adverse and contextual limits if eventually included: smaller jobs have higher JCT than MISO/MuxFlow; immediate offline-job termination protects online QoS when predictions fail; prediction-error sensitivity is simulated, not a measured online tail-latency result; MPS within a partition does not inherit the inter-partition MIG fault boundary. Page2 reverses the order of36%/46.6% in one summary sentence, whereas page7 and the conclusion consistently map46.6%toMuxFlow and36%toMISO. Preserve body comparator mapping and flag the source inconsistency.
''')
(d/'Validation.json').write_text(json.dumps({'record':rid,'eligibility':'Pending','included':False,'excluded':False,
 'criteria_rows':6,'source_pages':10,'source_sha256':sha,'context_observations':4,
 'new_study_ID_assigned':False,'independent_human_vote':False,'PDF_redistributed':False,
 'checked_utc':now},indent=2)+'\n')
print('MIGER pending scope package saved; no corpus-count change.')

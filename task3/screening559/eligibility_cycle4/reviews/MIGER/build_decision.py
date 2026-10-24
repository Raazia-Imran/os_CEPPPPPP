from pathlib import Path
import csv,json,datetime
D=Path(__file__).resolve().parent
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
source='11322073592686791f534c5528e01baf0dcf5dd06a86a9537044a819328605c8'
url='https://doi.org/10.1145/3673038.3673089'
checks=[
('IC1','Met','Final English ICPP2024 full paper identifies DOI,three authors and venue; supplied10-page publisher PDF.','PDF p1'),
('IC2','Met','MPS within MIG partitions explicitly co-locates online inference and offline training jobs on a physical GPU; mechanism and local scheduling rules are described.','PDF pp4-7 sections4.1-4.6'),
('IC3','Not demonstrated for joint eligibility','Inference workloads exist,but no separable measured inference endpoint is established under concurrent sharing. Figure4BERT latency varies allocation without a specified co-tenant; Table3online workloads do not supply measured per-tenant concurrent results.','PDF p3 Figure4;p7 Table3 and sections5.1-5.2'),
('IC4','Not demonstrated for joint eligibility','Figures2-3measure co-location behavior without separating inference modes. Sections5.2-5.5report mixed/offline JCT,makespan,queueing,monitor and scheduler costs rather than a separable inference-sharing outcome.','PDF pp2-3 Figures2-4;pp7-9 sections5.2-5.5'),
('IC5','Not demonstrated for joint eligibility','The isolated BERT allocation comparison is local inference evidence; the co-tenant throughput experiments are local sharing evidence. They cannot be combined into an unreported concurrent inference measurement.','PDF pp2-3 Figures2-4;pp7-9'),
('IC6','Met','ICPP2024 lies inside the protocol publication window.','PDF p1')]
def write(name,rows):
 with (D/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
write('Eligibility.csv',[{'Record ID':'R00001','Criterion':c,'Decision':v,'Evidence':e,'Anchor':a,'Source URL':url,'Source SHA256':source,'Checked UTC':stamp,'Independent human vote':''} for c,v,e,a in checks])
reason='EC2: The inspected full text does not establish a separable measured inference outcome under concurrent GPU sharing. Figure4is an isolated BERT-allocation comparison; Figure2does not identify inference modes and Figure3aggregates mixed modes. Main results measure cluster/mixed-or-offline job completion,queueing and makespan. These different experiments do not jointly demonstrate the inference-sharing endpoint required by conjunctive IC3-IC5. Secondary scope boundary: EC4 aggregate main evaluation. Evidence: PDF pp2-3 Figures2-4;pp6-9 sections4.5,5.1-5.5.'
write('Final_Exclusions.csv',[{'Record ID':'R00001','Study ID':'','Report ID':'','Short name':'MIGER','Final eligibility decision':'Exclude','Basis':reason,'DOI':'10.1145/3673038.3673089','Source URL':url,'Source SHA256':source,'Decision method':'Source-anchored full-text assessment under submitted conjunctive criteria','Independent human vote':'','Decided UTC':stamp,'Applied to frozen release':'No','Working integration status':'Completed full-text scope exclusion; context retained separately'}])
(D/'ADJUDICATION.md').write_text('''# MIGER full text scope decision

Decision: exclude from the primary-study synthesis under EC2. This completes the assessment previously held open; it does not assert that the paper has no inference workload or no useful GPU-sharing evidence.

The source is fully available and was rechecked across the mechanism and results sections. The conjunctive protocol requires inference evidence under the concurrent sharing setup. The explicit BERT comparison varies MIG size without a specified co-tenant. The local co-running throughput examples do not identify separable inference modes. The principal evaluation reports mixed/offline job completion, queueing and makespan across the cluster. The required combination is therefore not demonstrated in the assessed text. The secondary EC4 boundary explains why aggregate cluster benefits cannot substitute for the local inference endpoint.

No p99 distribution, new experiment or dedicated single-GPU-only study is required by this decision. An interpretable mean, throughput or interference result for an identified inference workload under same-device co-tenancy could satisfy the protocol. The exclusion is not based on source access, GPU count, paper quality, absence of tail latency, or a desired corpus size.

Preserve the earlier reading observations as context outside included-study outcomes. A new version or explicit source clarification can trigger a documented reassessment, as with any review decision; this is a completed decision for the inspected report, not an invented experiment or a claim about unreported author data.
''')
(D/'Validation.json').write_text(json.dumps({'record':'R00001','decision':'Exclude','primary_reason':'EC2','secondary_scope_note':'EC4','criteria_rows':6,'full_text_available':True,'source_sha256':source,'source_pages':10,'no_study_id_assigned':True,'prior_pending_decision_preserved':'eligibility_cycle3/miger/','independent_human_vote_asserted':False},indent=2)+'\n')
print(reason)

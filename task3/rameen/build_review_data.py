"""Build attributed review records without replacing inherited assessments."""
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import csv,json,hashlib
import fitz
ROOT=Path(__file__).resolve().parents[1]; OUT=Path(__file__).parent
NOW=datetime.now(timezone.utc).isoformat(); PKT=datetime.now(ZoneInfo('Asia/Karachi')).isoformat()
REVIEWER='AI assistant preparing Rameen assignment at Raazia request'
IDS=['P015','P018','P019','P020','P021','P022']
def rows(name): return list(csv.DictReader((ROOT/'logs'/('baseline_'+name+'.csv')).open()))
def save(name,data):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
studies={r['Report ID']:r for r in rows('Studies') if r['Report ID'] in IDS}
notes={
'P015':[
(2,'Portable preemptive scheduling objective and GPU-serving case are explicit.','PDF pp2-3; section1'),
(2,'XQueue, XShim and three preemption levels specify the mechanism.','PDF pp4-10; sections3-6'),
(1,'Setup and policies are described; repeated-run uncertainty for Figure15 is not specified.','PDF pp11-14; sections7-8'),
(1,'GV100, BERT-large and client rates are explicit; exact Triton/CUDA versions and batch sizes for case3 remain unresolved.','PDF p14; section8 case3'),
(2,'Same-GPU standalone, native and priority Triton cases use the stated client conditions.','PDF p14; Figure15a'),
(2,'Throughput in requests/s and normalized P99 comparisons are distinguished.','PDF p14; Figure15'),
(2,'P99, latency CDF, high-priority 10 requests/s and continuous background load are explicit.','PDF p14; section8 case3; Figure15a'),
(2,'Two BERT-large clients share one GV100 in the retained experiment.','PDF p14; section8 case3'),
(2,'Direct foreground performance-control evidence is delimited; malicious bypass is explicitly a limitation, not a security guarantee.','PDF pp14-15; Figure15a; section9 Untrusted tenants'),
(2,'Artifact instructions, hardware-dependent preemption limits and sufficient-memory assumption are documented.','PDF pp15,23; section9; Artifact Appendix')],
'P021':[
(2,'Kernel-wise spatial right-sizing for concurrent inference is explicit.','PDF p1; abstract; sectionI'),
(2,'Kernel-scoped partition proposal and emulation through CU masks are described.','PDF pp5-9; sectionsIV-V'),
(1,'Emulation correction is transparent; repeated-run uncertainty for headline results is not established.','PDF pp9-11; sectionsV-B,VI'),
(2,'MI50, host, Ubuntu/kernel, ROCm and model/worker/batch settings are supplied.','PDF pp9-10; sectionVI-A; TableIII'),
(1,'Model-wise policy permits CU overlap beyond prior isolation constraints; these cases are flagged and limit equivalence.','PDF pp9-10; sectionVI-A'),
(2,'RPS normalization and energy-per-inference measurement are defined; adjusted results estimate native support.','PDF pp9-11; sectionsV-B,VI-B'),
(2,'P95 latency and SLO evaluation are explicit under maximum-load inference.','PDF pp10-11; TablesIII-IV; Figure13b'),
(2,'One, two and four workers plus mixed-model pairs exercise contention.','PDF pp10-12; Figures13-15'),
(2,'KRISP-I prevents CU overlap and is compared with oversubscribed KRISP-O; this tests a compute-resource/performance boundary only.','PDF pp10-12; KRISP-I/O definitions; Figures13,16'),
(2,'Emulation calibration, adjusted latency formula and proposed hardware changes permit informed appraisal of implementation limits.','PDF pp7-9; sectionsIV-D,V-B')],
'P022':[
(2,'Performance isolation for high-priority inference with best-effort co-tenants is explicit.','arXiv v3 PDF pp1-2'),
(2,'Slicing, preemption, API mediation and profile-guided priority scheduling are described.','arXiv v3 PDF pp5-8; section4'),
(1,'Profiler averages repeated measurements, but end-to-end repetitions and uncertainty remain unspecified.','arXiv v3 PDF pp8-11; sections4.2,5.1-5.3'),
(2,'A100 SXM, host, runtime versions and six training/six inference models are explicit.','arXiv v3 PDF p9; Table2; section5.1'),
(2,'Common workloads, adapted trace, load, hardware and normalized metrics are documented for the four comparison mechanisms.','arXiv v3 PDF pp9-11; sections5.1-5.3'),
(2,'System throughput sums normalized throughput of all concurrent workloads; it is not background throughput alone.','arXiv v3 PDF pp9-10; sections5.1,5.3'),
(2,'P99 latency, 50% end-to-end load and 10%-90% idle-time sensitivity are specified.','arXiv v3 PDF pp9-11; Figures5-6'),
(2,'Inference/training pairs and scaling to multiple inference workloads are evaluated on a shared GPU.','arXiv v3 PDF pp9-11; sections5.2-5.4'),
(2,'P99 and workload-pair tests directly assess performance isolation; no adversarial memory or cross-tenant fault guarantee is inferred.','arXiv v3 PDF pp9-13; sections5-6'),
(2,'Artifact setup, virtualization/kernel-transformation overhead and CUDA cooperative-kernel limitations are documented.','arXiv v3 PDF pp12-14; sections5.7,6; AppendixA')]
}
sources=[]
for pid in IDS:
 s=studies[pid]; path=ROOT/'papers'/('P022_v3.pdf' if pid=='P022' else pid+'.pdf'); available=pid in notes
 url=('https://arxiv.org/pdf/2410.07381v3' if pid=='P022' else s['Source'])
 version={'P015':'USENIX proceedings PDF with cover; printed pp671-692', 'P021':'Author-hosted 14-page HPCA manuscript; IEEE DOI identity confirmed; exact publisher-byte equivalence unverified', 'P022':'arXiv v3, 28 February 2025; ASPLOS 2025 DOI/ISBN/conference footer present; publisher-byte equivalence not asserted'}.get(pid,'Publisher abstract/metadata plus inherited source assessment; no fresh full text')
 sources.append({'Study ID':s['Study ID'],'Report ID':pid,'Title':s['Title'],'Year':int(s['Year']),'DOI':s['DOI'],'Source URL':url,'Version checked':version,'Access status':'Full text inspected' if available else 'Full text unavailable','PDF pages':len(fitz.open(path)) if available else None,'SHA256':hashlib.sha256(path.read_bytes()).hexdigest() if available else '', 'Original QA':int(s['QA score']),'Original maximum':int(s['Applicable maximum']),'Reviewed QA':sum(x[0] for x in notes[pid]) if available else None,'Reviewed maximum':20 if available else None,'Reviewer':REVIEWER,'Checked UTC':NOW,'Checked PKT':PKT,'Independent human vote':''})
oldqa={(r['Report ID'],r['Criterion']):r for r in rows('QA')}; qa=[]
for pid in IDS:
 for i in range(1,11):
  old=oldqa[pid,'Q'+str(i)]; available=pid in notes
  score,note,anchor=notes[pid][i-1] if available else (None,'Original judgment retained without fresh validation. Full text is required to reassess this item.','Not inspected; inherited anchor: '+old['Evidence location'])
  qa.append({'Study ID':studies[pid]['Study ID'],'Report ID':pid,'Item ID':'Q'+str(i),'Original score':old['Score'],'Original maximum':int(old['Maximum']),'Reviewed score':score,'Reviewed maximum':2 if available else None,'Status':'Assessed' if available else 'Pending full text','Rationale':note,'Source anchor':anchor,'Source URL':next(s['Source URL'] for s in sources if s['Report ID']==pid),'Reviewer':REVIEWER,'Checked UTC':NOW,'Independent human score':''})
elig=[]
anchors={
'P015':['PDF cover and pp2,23','PDF pp4-10; sections3-6','PDF p14; section8 case3','PDF p14; Figure15a','PDF p14; single GV100 experiment','PDF cover: OSDI2025'],
'P021':['PDF p1; title/authors; IEEE DOI metadata','PDF pp5-9; sectionsIV-V','PDF pp9-10; sectionVI-A; TableIII','PDF pp10-11; Figure13; TableIII','PDF pp9-10; one MI50, multiple workers','IEEE HPCA2023 DOI metadata'],
'P022':['arXiv v3 PDF p1; ASPLOS2025 DOI/conference/ISBN','arXiv v3 PDF pp5-8; section4','arXiv v3 PDF pp9-11; Table2; Figures5-6','arXiv v3 PDF pp9-10; sections5.1,5.3','arXiv v3 PDF p11; shared-GPU co-location discussion','arXiv v3 PDF p1; ASPLOS2025']}
basis={
'P015':['English final USENIX proceedings identity verified.','Temporal/API scheduling among concurrent GPU inference clients.','Two BERT-large inference clients; non-GPU cases excluded from extraction.','P99 ratio and throughput-latency evidence inspectable.','Single-GV100 inference case is separately reported.','2025 lies within the main publication window.'],
'P021':['Peer-reviewed HPCA2023 identity established; evidence version is author manuscript.','Kernel-wise spatial partitioning among inference workers.','Concurrent homogeneous and mixed-model inference workloads.','P95 latency and throughput are inspectable, subject to emulation calibration.','One MI50 supports separately extractable co-tenant tests.','2023 lies within the main publication window.'],
'P022':['ASPLOS2025 identity matches the v3 manuscript title/authors/DOI; exact publisher-byte equivalence unverified.','API interception and thread-block priority scheduling share a GPU.','High-priority inference plus training, and multi-inference tests, are separable.','P99 and normalized total-system-throughput results are inspectable.','Same-GPU workload results are distinct from the eight-GPU host inventory.','2025 lies within the main publication window.']}
for old in rows('Eligibility'):
 pid=old['Report ID']
 if pid not in IDS:continue
 i=int(old['Criterion'][2:])-1; available=pid in notes
 elig.append({'Study ID':old['Study ID'],'Report ID':pid,'Item ID':old['Criterion'],'Original decision':old['Decision'],'Review decision':'Supported in accessed version' if available else 'Pending full text','Rationale':basis[pid][i] if available else 'Inherited criterion decision is not independently revalidated from abstract or metadata.','Source anchor':anchors[pid][i] if available else 'Inherited: '+old['Evidence location'],'Source URL':next(s['Source URL'] for s in sources if s['Report ID']==pid),'Reviewer':REVIEWER,'Checked UTC':NOW,'Independent human decision':''})
outcomes=[]
for old in rows('Evidence'):
 pid=old['Report ID']
 if pid not in IDS:continue
 x=dict(old);x.update({'Original metric':old['Metric'],'Original anchor':old['Evidence location'],'Review status':'Value and context checked' if pid in notes else 'Pending full text','Review note':'','Reviewer':REVIEWER,'Checked UTC':NOW,'Independent human vote':''})
 if pid=='P015': x['Evidence location']='PDF p14; printed p683; section8 case3; Figure15a';x['Review note']='1.07x standalone and author-rounded 30.0% decrease are textual results; section7.4 label in inherited anchor corrected.'
 if pid=='P021':x['Evidence location']='Author PDF pp9-11; sectionVI; TableIII and Figure13b';x['Review note']='95 denotes P95, not effect size. MPS Default is an AMD unrestricted-concurrency analogue. Emulation correction preserves right-sizing/allocation overhead.'
 if pid=='P022':
  x['Metric']='Normalized total system throughput';x['Evidence location']='arXiv v3 PDF p10; section5.3; Figure6a on p11';x['Source']='https://arxiv.org/pdf/2410.07381v3'
  x['Hardware']='Shared A100 SXM 40GB; eight-GPU EC2 p4d host inventory is not an eight-GPU outcome; Ubuntu20.04/CUDA12.2/PyTorch2.2.0/ONNX Runtime GPU1.17.0/Hidet0.3.0'
  x['Interpretation']='Sum of normalized throughput of all concurrent workloads: Tally1.19 versus TGS1.65 at10% idle time. Not background throughput alone.';x['Review note']='Values verified in v3; metric label corrected and version pinned.'
 if pid not in notes:x['Review note']='Numeric value and inherited source anchor retained; publisher metadata/abstract does not verify this detailed outcome.'
 outcomes.append(x)
changes=[
('RM01','P015','Source anchor','section7.4 case3','section8 case3; PDFp14/printedp683','Printed source heading'),
('RM02','P015 Q9','Applicability and score','NA/0','Proposed2/2; compute/performance control is claimed and tested','PDFpp14-15; Figure15a; section9. Submitted Q9 is not restricted to security/fault guarantees.'),
('RM03','P021 Q9','QA score','1/2 because no security/fault test','Proposed2/2 for delimited compute-resource boundary','PDFpp10-12; KRISP-I/O; Figures13,16. No stronger security claim inferred.'),
('RM04','P021 Q10','QA score','1/2 because emulation limits deployability','Proposed2/2 for transparent replication and limitation details','PDFpp7-9; emulation calibration and formula. Emulation alone is not a failure of reporting.'),
('RM05','P022','Source version','Unpinned arXiv URL','Pin arXiv2410.07381v3; 17pages; DOI-matched ASPLOS manuscript','v3PDFp1 and arXiv version history'),
('RM06','P022 E052','Metric','Normalized background throughput','Normalized total system throughput','v3PDFpp9-10; sections5.1,5.3'),
('RM07','P022 Q5','QA score','1/2 due policy throughput trade-off','Proposed2/2; stated policies and common conditions support interpretable comparison','v3PDFpp9-11. Different policy objectives alone do not invalidate a benchmark comparison.'),
('RM08','P022 Q9','QA score','1/2 because no hostile isolation','Proposed2/2 for directly measured performance isolation','v3PDFpp9-13; no security/fault equivalence inferred'),
('RM09','P018 P019 P020','Fresh validation','Inherited scores/eligibility/outcomes','Keep pending; retain baseline without new validation claim','Fresh publisher PDF responses are HTML; retrieval_attempts.json'),
('RM10','Novelty','Contribution wording','Broad taxonomy/trade-offs could be described as novel','Position as bounded, source-audited, condition-specific update; no first-review claim','Yu2022; Huang2025; Ye2024; supplementary search receipt'),
('RM11','Recommendations REC04-REC06','Evidence strength','Missing-reading sources cited without local review distinction','Mark P019/P020/P018 dependent recommendations provisional pending source reacquisition','Scope/recommendation audit'),
('RM12','P022','Runtime label','ONNX1.17','ONNX Runtime GPU1.17.0','v3PDFp9; section5.1')]
changes=[dict(zip(['Change ID','Scope','Field','Original','Proposed treatment','Evidence'],x)) for x in changes]
novelty=[
{'ID':'RV01','Title':'A Survey of Multi-Tenant Deep Learning Inference on GPU','Authors':'Fuxun Yu; Di Wang; Longfei Shangguan; Minjia Zhang; Chenchen Liu; Xiang Chen','Year':2022,'Identifier':'arXiv:2203.09040','Access':'Full text inspected, 8 pages; contextual survey','Scope':'Full-stack multi-tenant DL inference, GPU streams/MPS/MIG and software/hardware scheduling.','Anchor':'PDFpp1-3; sectionsI-II; pp5-7 sectionsIII-IV','Overlap':'High topical overlap; taxonomy and hybrid scheduling are already established discussion topics.','Implication':'Differentiate by current source-anchored, single-physical-GPU outcome comparability and conditional recommendations; no first survey claim.','URL':'https://arxiv.org/abs/2203.09040'},
{'ID':'RV02','Title':'On Efficiency, Fairness and Security in AI Accelerator Resource Sharing: A Survey','Authors':'Jiahua Huang; Weiwei Lin; Wentai Wu; Yang Wang; Haocheng Zhong; Xinhua Wang; Keqin Li','Year':2025,'Identifier':'10.1145/3721427','Access':'Full text inspected, 35 pages; ACM Computing Surveys57(9),Article221','Scope':'2016-2024 sharing research across GPUs and other AI accelerators; efficiency, fairness, interference and security.','Anchor':'PDFpp1-4; abstract; sections1.1-1.3; taxonomy and later discussion','Overlap':'Strong overlap with performance/isolation trade-offs; these themes are not novel in themselves.','Implication':'Use as direct comparator and cite prior coverage. Narrower single-GPU inference audit and 2025 studies may add value; exhaustive novelty remains unproven.','URL':'https://doi.org/10.1145/3721427'},
{'ID':'RV03','Title':'Deep Learning Workload Scheduling in GPU Datacenters: A Survey','Authors':'Zhisheng Ye; Wei Gao; Qinghao Hu; Peng Sun; Xiaolin Wang; Yingwei Luo; Tianwei Zhang; Yonggang Wen','Year':2024,'Identifier':'10.1145/3638757','Access':'Publisher/index and author metadata; final full-text attempt unsuccessful. Related2022preprint separately identified.','Scope':'Training and inference scheduling in GPU datacenters.','Anchor':'Publisher/author title and abstract metadata; final body not inspected','Overlap':'Broader scheduler objectives and resource utilization; detailed methodological overlap remains pending.','Implication':'Do not assert absence of equivalent RQs or methods without full-text comparison. Do not silently equate the differently titled2022preprint with final text.','URL':'https://doi.org/10.1145/3638757'},
{'ID':'RV04','Title':'A comprehensive review of GPU virtualization and sharing methods','Authors':'Petr Mandrik','Year':2025,'Identifier':'HAL:hal-05429292v1','Access':'Repository-index lead dated22December2025; January2026 author-upload date also surfaced; direct repository access blocked','Scope':'GPU virtualization/sharing in VMs and containers; remoting, scheduling and related capabilities (indexed abstract only).','Anchor':'Repository-index metadata; full text not inspected','Overlap':'Potentially high mechanism overlap, including API mediation.','Implication':'Treat as an unresolved recent technical-report comparator, not a peer-reviewed primary study or a verified novel-scope exclusion.','URL':'https://hal.science/hal-05429292v1'}]
recommendations=[
{'Item':'REC02','Status':'Supported conditionally','Finding':'XSched and Tally source checks support foreground latency versus total throughput trade-off.','Action':'Keep workload, offered load, shared GPU and comparator visible; correct E052 metric.'},
{'Item':'REC04','Status':'Partial source coverage','Finding':'ArkGPU-specific evidence has not been freshly rechecked.','Action':'Keep as a candidate recommendation supported by inherited extraction; resolve P019 before final acceptance.'},
{'Item':'REC05','Status':'Partial source coverage','Finding':'Dyna-P prediction and reconfiguration outcomes remain inherited.','Action':'Do not use makespan as online request-tail evidence; resolve P020 and keep local versus cluster strata separate.'},
{'Item':'REC06','Status':'Pending primary source','Finding':'InferFair is the sole report directly cited by this recommendation.','Action':'Mark recommendation provisional; no unconditional fairness recommendation until P018 text and definitions are verified.'},
{'Item':'G01-G06','Status':'Corpus observations, not worldwide absences','Finding':'Existing surveys already discuss efficiency, fairness, security and LLM integration.','Action':'Phrase gaps as missing matched evidence in this reviewed corpus; do not imply the whole literature has no solution.'}]
rotation=[]
for pid in ['P001','P002','P003','P004','P005','P006','P007','P023']:
 rotation.append({'Report ID':pid,'Assigned first reviewer':'Eshaal','Assigned independent reviewer':'Rameen','Status':'Awaiting Eshaal first-review return and actual independent human check','Required items':'Identity/version, IC1-IC6, all linked QA/outcomes; P023 linked to S005, not a new study','Actual reviewer':'','Checked UTC':'','Decision':'','Disagreement resolution':''})
activity=[{'UTC':NOW,'PKT':PKT,'Operator':REVIEWER,'Action':'Prepare item-level review from accessed PDFs and protocol; preserve inaccessible items as pending','Input commit':'feeabc8e9a73b7ced7c4f4628e570d4eae000080','Independent human signoff':False}]
combined=[]
for kind,items in [('identity',sources),('eligibility',elig),('QA',qa),('outcome',outcomes)]:
 for r in items:
  pid=r['Report ID']; status=r.get('Status',r.get('Review decision',r.get('Review status',r.get('Access status',''))))
  combined.append({'Reviewer':REVIEWER,'Checked UTC':NOW,'Checked PKT':PKT,'Study ID':studies[pid]['Study ID'],'Report ID':pid,'Record type':kind,'Item ID':r.get('Item ID',r.get('Evidence ID',pid)),'Current value':r.get('Original score',r.get('Value',r.get('Original decision',r.get('Title','')))),'Source page/table/figure':r.get('Source anchor',r.get('Evidence location',r.get('Version checked',''))),'Status':status,'Proposed correction':r.get('Reviewed score',r.get('Metric','')),'Rationale':r.get('Rationale',r.get('Review note','')),'Independent human vote':''})
for name,data in [('Source_and_Identity_Review.csv',sources),('QA_Source_Review.csv',qa),('Eligibility_Source_Review.csv',elig),('Outcome_Source_Review.csv',outcomes),('Correction_Register.csv',changes),('Novelty_Comparison.csv',novelty),('Recommendation_Audit.csv',recommendations),('Independent_Check_Queue.csv',rotation),('source_checks_Rameen.csv',combined),('activity.csv',activity)]:save(name,data)
data={'sources':sources,'qa':qa,'eligibility':elig,'outcomes':outcomes,'changes':changes,'novelty':novelty,'recommendations':recommendations,'rotation':rotation,'activity':activity,'reviewer':REVIEWER,'built_utc':NOW,'built_pkt':PKT}
(OUT/'review_data.json').write_text(json.dumps(data,indent=2))
validation={'sources_inspected':3,'sources_pending_full_text':3,'qa_assessed':sum(r['Status']=='Assessed' for r in qa),'qa_pending':sum(r['Status']!='Assessed' for r in qa),'eligibility_supported_in_accessed_versions':sum(r['Review decision']=='Supported in accessed version' for r in elig),'eligibility_pending':sum(r['Review decision']!='Supported in accessed version' for r in elig),'outcomes_checked':sum(r['Review status']=='Value and context checked' for r in outcomes),'outcomes_pending':sum(r['Review status']!='Value and context checked' for r in outcomes),'scope_records_unassessed':559,'instructor_scope_accepted':False,'independent_human_signoff':False,'score_treatment':'Proposals for teammate adjudication; master and frozen baseline unchanged','sources':[{'report':s['Report ID'],'original':s['Original QA'],'original_max':s['Original maximum'],'proposed':s['Reviewed QA'],'proposed_max':s['Reviewed maximum']} for s in sources]}
assert len(qa)==60 and len(elig)==36 and len(outcomes)==9
assert len({(r['Report ID'],r['Item ID']) for r in qa})==60
assert all(r['Reviewed score'] is None for r in qa if r['Report ID'] not in notes)
(OUT/'validation.json').write_text(json.dumps(validation,indent=2));print(json.dumps(validation,indent=2))

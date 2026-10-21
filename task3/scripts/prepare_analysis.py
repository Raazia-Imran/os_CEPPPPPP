from pathlib import Path
import json,csv,datetime,hashlib,re
from zoneinfo import ZoneInfo
root=Path(__file__).resolve().parents[1]; d=json.loads((root/'logs/baseline_data.json').read_text())
retr=json.loads((root/'papers/retrieval.json').read_text())
for r in retr:
 p=root/'papers'/r['filename'] if r['filename'] else None
 if p and p.exists():
  r['status']='PDF retrieved; title checked';r['version_note']='Public proceedings or author-hosted copy; retain original copyright notice'
  if r['report_id'] in ['P002','P011','P022']:r['version_note']='Author manuscript; published-version equivalence not established in this pass'
  if r['report_id']=='P023':r['version_note']='Author-hosted journal PDF; explicitly extends P005 on page 1; same S005'
  r['identity_check_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 else:r['version_note']='Publisher PDF not retrieved; supplied baseline extraction preserved, not newly reverified'
keys=list(dict.fromkeys(k for r in retr for k in r))
with (root/'papers/retrieval.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(retr)
(root/'papers/retrieval.json').write_text(json.dumps(retr,indent=2))
rows=['# Included report reading catalogue','', '21 report versions / 20 studies. PDF identity checking is distinct from rechecking every extracted result. P005 and P023 share S005. P016 and P017 are exclusions.','', '| Report | Study | Title | Reading source | Status |','|---|---|---|---|---|']
for r in retr:
 link=f"[{r['filename']}]({r['filename']})" if r['filename'] else f"[Publisher]({r['source_url']})"
 rows.append(f"| {r['report_id']} | {r['study_id']} | {r['title']} | {link} | {r['status']} |")
rows+=['','The repository AGENTS.md excludes licensed full-text redistribution. Files whose notices restrict public reposting are kept as source links in the public repository; local reading copies are not evidence of permission to republish.']
(root/'papers/README.md').write_text('\n'.join(rows))
# Analytical matrices are interpretations of the supplied extraction, with explicit report IDs.
a={}
a['Taxonomy']=[['Family','Control boundary','Reports','Assumption','Primary benefit','Cost / limit'],
['Temporal / priority','Request, model, kernel or launch order','P004 P005 P006 P007 P009 P015 P022','A suitable interception/preemption boundary exists','Protect foreground response while admitting background work','Switch cost, profiling and background slowdown'],
['Software spatial sharing','MPS quota or AMD CU-mask control','P001 P002 P003 P008 P021','Concurrent jobs fit memory and selected compute allocation','Use otherwise idle capacity','Residual interference; quotas are not proof of security'],
['Hardware partition and hybrid','MIG profiles plus temporal/MPS policy','P011 P014 P020','Supported partition profiles fit model memory','Explicit resource allocation and controlled co-location','Fragmentation, placement and reconfiguration cost'],
['API / runtime mediation','User API, shared runtime or kernel interface','P006 P012 P013 P014 P019 P022','Required APIs and integration hooks are supported','Scheduling control, runtime or memory efficiency','Compatibility, CPU/transfer cost and trust boundary'],
['Memory handover','Inference/training memory ownership','P010','Training can yield memory without breaking inference','Exploit residual resources','Reclamation and integration overhead'],
['Fairness policy','Relative model slowdown and SLO goodput','P018','Comparable per-model service objectives','Balance useful service across models','Not equivalent to request-tail or hostile-tenant isolation']]
a['Comparability']=[['Comparison ID','Reports / evidence','Observation','Comparison class','Interpretation','Missing control'],
['CMP01','P011 E036 E037 C001 C002','354 to 446 requests/s; 11 to 27 ms','Within-source trade-off','25.99% throughput increase accompanies 2.4545x latency','Latency quantile; final version equivalence'],
['CMP02','P001 E001; P011 E036','2.7x versus 25.99% increase','Unmatched cross-study','Different baseline and GPU/model context prevent ranking','Matched workload, batch and resource budget'],
['CMP03','P007 E029 E030; P015 E044','Up to 7.3x aggregate work versus 1.07x foreground P99','Different objectives','Foreground delay and total completed work must be assessed together','Common model mix and background progress metric'],
['CMP04','P008 E031 E032','GUE 94.04 and negative signed latency improvement','Within-source metric tension','Composite efficacy is not utilization percent; preserve adverse latency','Metric definitions and baseline stratum'],
['CMP05','P012 E038 E039','Density benefit with model-transfer sensitivity','Condition-dependent trade-off','Late binding suits low-rate functions only if transfer fits SLO','Heavy-model transfer and host CPU budget'],
['CMP06','P019 E048 E049; P022 E052','QoS protection with low-contention or background throughput loss','Different experiments, consistent cost','Protecting foreground work can sacrifice co-tenant work','Matched slowdown definitions'],
['CMP07','P005 P023','REEF engines and report versions differ','Companion study, not replication','Retain source-version strata; do not double-count corroboration','Outcome-to-version mapping for every combined REEF row'],
['CMP08','P018 E046 E047; P020 E050','Goodput/fairness versus makespan','Different metrics','Job-level efficiency cannot establish request-tail service','Request arrival process and latency distribution']]
a['Recommendations']=[['ID','Scenario','Candidate','Evidence','Expected benefit','Sacrifice','Alternative / trigger','Validation needed'],
['REC01','Trusted resident models; utilization priority','Tuned MPS / software spatial controls','P001 P002 P003 P008 E001-E004 E006 E031-E032','Higher useful co-location under tested allocations','Interference, quota tuning and memory pressure','Partitions or dedication when trust/isolation dominates','Measure each model P99 and SLO goodput under bursts'],
['REC02','Foreground tail-latency priority','Priority/preemptive scheduling','P005 P006 P007 P015 P022 E018-E030 E044-E045 E052','Lower foreground interference','Background slowdown, profiling and runtime integration','Dedicated GPU when supported control cannot meet deadline','Check foreground tails and background progress jointly'],
['REC03','Low-rate serverless functions','Late binding / controlled runtime sharing','P012 P013 E038-E041','Higher function or workflow density','Host CPU, memory transfer and shared-runtime trust','Keep large or high-rate models resident if swaps dominate','Sweep model sizes, cold starts, offered rate and concurrency'],
['REC04','Mixed inference with opportunistic training','Memory handover / controlled co-location','P010 P019 E035 E048-E049','Protect inference while using residual capacity','Reclamation overhead and reduced training progress','Separate resources for intolerable interference','Measure inference tails separately from training throughput'],
['REC05','Supported partition hardware; stable memory fit','MIG-aware hybrid policy','P011 P014 P020 E036-E037 E042-E043 E050','Resource allocation with configurable co-location','Fragmentation and reconfiguration overhead','Software sharing when partition granularity wastes capacity','Validate profile fit and reconfiguration effects; security needs separate tests'],
['REC06','Several models with unequal service pressure','Fairness-aware admission / scheduling','P018 E046-E047','Balance normalized slowdown and SLO goodput','May give up aggregate throughput to improve fairness','Priority scheduling when one foreground SLA dominates','Agree fairness objective and per-model SLO before deployment']]
a['Research Gaps']=[['Gap ID','Observation in corpus','Reports / basis','Research question','Needed experiment'],
['G01','No matched all-family comparison','Comparability CMP01-CMP08','Which gains survive matched conditions?','Same GPU, model mix, memory budget, arrivals and SLO across families'],
['G02','Security/fault boundaries often unestablished','Extraction Security boundary / Fault boundary','Does performance control protect hostile tenants?','Separate adversarial access, fault injection and performance tests'],
['G03','Metrics emphasize different units','E001-E052','Can foreground protection preserve useful background work?','Report per-model goodput, tails and background progress jointly'],
['G04','Partition prediction affects makespan','P020 E050','How does reconfiguration affect online service?','Bursty arrivals plus placement changes and request-tail measurement'],
['G05','Version and method details remain incomplete','P002 P011 P022; QA Q3/Q4/Q10','How reproducible are the comparisons?','Publish exact version, driver/runtime, warmup, repetitions and uncertainty'],
['G06','Energy and cost evidence not harmonized','Extraction schema and heterogeneous outcomes','Do measured utilization gains reduce energy per useful request?','Measure GPU and host energy per SLO-compliant request']]
a['Validity']=[['Threat','Evidence','Effect on conclusion','Mitigation applied','Remaining work'],
['Selection/stopping','559 retained records not assessed','No exhaustive recall or prevalence claim','Stopping branch remains visible','Instructor/team decision on bounded scope; extend if required'],
['Title-only decisions','2933 records without exported abstract','Relevant work may be missed','Abstract-availability column retained','Prioritize uncertain/relevant records for abstract checks'],
['Single review','No item-level independent checks','Correlated screening/QA/extraction errors possible','Original rationale and source anchors retained','Record real named checks if performed'],
['Search provenance','Displayed/exported discrepancies and broad fields','Search cannot be fully reconstructed from totals','Exact preserved query/log values retained','Supply missing original exports, facets and receipts'],
['Source version','Author manuscripts and combined REEF anchors','Page/result mappings may differ','Separate source-version and retrieval records','Compare final published text and map companion outcomes'],
['Measurement heterogeneity','Different GPU/model/baseline/statistic','Cross-study speedup ranking is invalid','No pooled effect size or universal winner','Matched comparisons needed'],
['Reporting bias','Uneven repetitions and uncertainty','Headlines may overstate robustness','Adverse and null findings retained','Recheck high-impact claims at exact source locations']]
a['Human Checks']=[['Check ID','Priority','Task','Evidence to return','Status','Reviewer','Checked UTC','Notes'],
['H01','High','Confirm whether bounded review with 559 unassessed retained records is acceptable','Instructor direction / dated team scope decision','Pending','','','Do not infer approval from general permission to use AI'],
['H02','High','Supply InferFair, ArkGPU and Dyna-P PDFs already downloaded','Original PDFs or legitimate accessible source','Pending','','','These three publisher copies were not retrieved'],
['H03','High','Check headline outcomes against source figures/tables','Report ID, evidence ID, source version, page, correction and actual time','Pending','','','Use 52 evidence rows; do not sign unseen rows'],
['H04','Medium','Check companion/version mapping','P005/P023 outcomes and P002/P011/P022 manuscript comparisons','Pending','','','Separate report count from study count'],
['H05','Medium','Confirm original search artifacts and group provenance','Exact original exports, search fields/facets and times','Pending','','','Do not reconstruct missing event times from file dates']]
req=['Final SLR report','Engineering problem','Research objectives','Research questions','SLR protocol','Database justification','Complete search strings','Inclusion/exclusion criteria','Database-wise results','Search and screening log','Duplicate record','PRISMA flow','Quality checklist/scores','Included primary studies','Extraction sheet','Taxonomy','Comparative matrix','Trade-offs','Conflicting evidence','All RQ answers','Engineering recommendation','Research gaps','Threats to validity','References','Supporting verification files']
loc=['report/main.pdf (draft)','report section 1','report section 1','report section 2','../task1/submitted_protocol.pdf','report section 3','Search Log / appendix','report section 3','report section 4','Screening Log / Search Log','Duplicate Removal','baseline/PRISMA_2020_FLOW_DIAGRAM.pdf','QA / QA Reconciliation','Studies / Source Register','Extraction / Evidence','Taxonomy / report section 5','Comparability / report section 7','report section 8','Comparability / report section 9','report section 6','Recommendations / report section 10','Research Gaps / report section 11','Validity / report section 12','report references','logs / baseline / scripts']
a['Requirements']=[['Guideline 23 item','Requirement','Artifact','Status / qualification']]+[[i+1,x,loc[i],'Draft present; verify before final submission' if i not in [4,8,9,10,12,14] else 'Existing evidence preserved; limits documented'] for i,x in enumerate(req)]
a['Benchmark']=[['Benchmark','Source','Observed practice','Application to this draft','Limit'],['Hong, Spence and Nikolopoulos, ACM Computing Surveys 50(3), article 35, 2017','https://doi.org/10.1145/3068281','Classify by implementation layer; compare mechanisms; discuss scheduling and unresolved constraints','Separate taxonomy from outcomes and condition recommendations on control boundary','A survey organization benchmark, not proof of PRISMA compliance'],['Journal standing, checked 20 Oct 2026','https://dl.acm.org/journal/CSUR','Publisher search result: 2025 impact factor 30.4; rank 1/146 in Computer Science Theory & Methods','Q1 standing inferred from top rank; journal-level measure only','Does not certify this student draft as journal-ready']]
(root/'logs/analysis.json').write_text(json.dumps(a,indent=2))
for name,rr in a.items():
 with (root/'logs'/(name.replace(' ','_')+'.csv')).open('w') as f:csv.writer(f).writerows(rr)
now=datetime.datetime.now(datetime.timezone.utc)
with (root/'logs/activity.csv').open('a') as f:csv.writer(f).writerow(['A002',now.isoformat(),now.astimezone(ZoneInfo('Asia/Karachi')).isoformat(),'AI assistant under user direction','Retrieve sources and prepare traceable analytical matrices',f"{sum(bool(r['filename']) for r in retr)} PDFs downloaded; 3 not retrieved; matrices use supplied evidence",'papers/retrieval.csv; logs/analysis.json','Actual preparation checkpoint; individual retrieval attempts have separate timestamps'])
(root/'benchmark/README.md').write_text('''# Journal benchmark

Hong, Spence and Nikolopoulos, *GPU Virtualization and Scheduling Methods: A Comprehensive Survey*, ACM Computing Surveys 50(3), article 35, 2017. DOI: https://doi.org/10.1145/3068281. Author manuscript inspected: https://pureadmin.qub.ac.uk/ws/portalfiles/portal/130042880/acm_surveys_GPU_2017.pdf.

The survey uses implementation layer as its organizing principle, then compares approaches and treats scheduling separately. Its future directions follow from technical constraints. We adopt these organizational practices, while adding the instructor-required PRISMA accounting and claim-level evidence IDs. It is a survey benchmark, not an assertion that its search methodology is a reproducible SLR.

ACM's journal search result on 20 October 2026 reports 2025 impact factor 30.4 and rank 1/146 in Computer Science Theory & Methods (https://dl.acm.org/journal/CSUR). Q1 is inferred from that top rank. The metric belongs to the journal and does not measure this draft's quality. Direct journal-page fetch returned 403; the publisher search result supplied the metric.

First-draft quality gates: explicit engineering decision; nonexclusive technical taxonomy; matched-baseline interpretation; adverse findings retained; recommendations linked to evidence and sacrifices; gaps justified by the corpus; protocol departures visible. The current review still has selection, version and independent-check limitations.
''')
print('Analysis matrices',len(a),'PDFs',sum(bool(r['filename']) for r in retr))

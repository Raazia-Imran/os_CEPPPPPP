# Scope and recent-survey overlap audit

Prepared on 22 October 2026 Pakistan time by the AI assistant at Raazia's request for Rameen's assignment. This is a supplementary audit, not a rerun of the protocol's four formal database searches. Exact instrumented queries, time, source and returned references are in novelty_search_receipt.json. Search-result counts are not added to PRISMA identification totals.

## Scope question for the instructor

Our Topic 23 first draft uses the supplied bounded corpus of 20 unique studies represented by 21 report versions. The inherited register records 4,189 occurrences, 114 duplicate links, 4,075 canonical records, 3,493 screening exclusions and 559 retained records that were not advanced for assessment. Twenty-three reports were source-assessed in the supplied baseline, with two report exclusions. The 559 records are unassessed; they are not technical exclusions or evidence that no further eligible studies exist.

**Question:** May we submit the first draft as an explicitly bounded review with this limitation while completing source verification, or must all 559 retained records undergo the remaining screening and full-text process before final submission? If bounded scope is acceptable, please confirm the permitted boundary and whether any particular mechanism, workload or date coverage must be added.

Instructor decision: **Pending**. Date, exact response and evidence location: **Not supplied**. No approval, waiver, exclusion decision or final corpus closure is implied by this prepared question. The question has not been sent.

## Consequences of the decision

If bounded scope is accepted, preserve the dated response, state the coverage restriction in the abstract/methods/PRISMA/validity sections, and retain the ordered unassessed register. Continue to distinguish inherited assessments from fresh source verification. Acceptance of a first draft does not establish exhaustive final SLR coverage.

If full assessment is required, freeze the actual retained/unassessed IDs before allocating 187 to Eshaal, 186 to Raazia and 186 to Rameen. These are prospective workloads, not completed decisions. Apply the submitted criteria and real independent votes; obtain full text, QA and extraction for new eligible studies; recalculate the study/report mapping and PRISMA from actual records. Do not turn the 559 into automatic exclusions to keep the 20-study count.

## Survey comparison

**Yu et al., 2022, A Survey of Multi-Tenant Deep Learning Inference on GPU, arXiv:2203.09040.** The eight-page full text was inspected. Its full-stack view includes service, graph, runtime, kernel and resource layers and discusses streams, MPS, MIG and hybrid scheduling. This is a directly overlapping contextual survey, not a primary study in our set. Source: PDF pp1-3 and sectionsIII-IV; https://arxiv.org/abs/2203.09040.

**Huang et al., 2025, On Efficiency, Fairness and Security in AI Accelerator Resource Sharing: A Survey, ACM Computing Surveys57(9),Article221, DOI10.1145/3721427.** The35-page author-hosted publication copy was inspected. It reviews2016-2024 work across AI accelerators and already organizes discussion around efficiency, fairness, interference and security. Those themes cannot independently establish novelty for our review. Its wider accelerator/workload remit differs from our single-physical-GPU inference boundary. Source: PDFpp1-4; https://www.cs.newpaltz.edu/~lik/publications/Jiahua-Huang-ACM-CSUR-2025 and https://doi.org/10.1145/3721427.

**Ye et al., 2024, Deep Learning Workload Scheduling in GPU Datacenters: A Survey, DOI10.1145/3638757.** Publisher, institutional and author metadata were identified. The final full text was not retrieved in this pass; the related2022preprint has a different title and author order, so it is not silently treated as the final article. Available abstract metadata covers training and inference scheduling and resource utilization. Author-hosted40-page text now confirms broad inference scheduling and hybrid co-location coverage (Figure1,Section4,Section5.2); placeholder citation metadata is not final publisher pagination. Source: https://doi.org/10.1145/3638757 and https://scholar.pku.edu.cn/yezhisheng/publications/deep-learning-workload-scheduling-gpu-datacenters-survey.

**Mandrik, A comprehensive review of GPU virtualization and sharing methods, HALhal-05429292v1.** Repository-index results date the technical report22December2025; aJanuary2026author-upload date also appears. Direct repository access was blocked. Treat it as a recent contextual lead with potentially strong mechanism overlap. Its exact full-text coverage and peer-review status are not verified. Source: https://hal.science/hal-05429292v1.

## Contribution wording supported by this audit

The defensible contribution is a bounded, source-audited comparison of single-GPU inference-sharing evidence that keeps workload, metric, baseline, resource boundary and implementation cost attached to each recommendation, and incorporates relevant2025systems. This is a narrower analytical emphasis and update, not evidence that no prior review has asked similar questions. The novelty comparison remains qualified by the unavailable Mandrik technical-report full text and the unverified final publisher pagination of the Ye author copy and by supplementary-search coverage.

Proposed text for integration: "Prior surveys already cover multi-tenant GPU inference and accelerator-sharing efficiency, fairness and security. This review therefore focuses on the traceability and comparability of within-one-physical-GPU inference outcomes, distinguishing performance control from security and fault containment and linking engineering recommendations to their measured conditions. Its contribution is bounded by the supplied corpus and does not establish exhaustive novelty."

## Recommendation and research-gap checks

REC02 has freshly inspectable XSched/Tally support for foreground latency versus total system throughput, subject to source conditions. REC04 includes ArkGPU and REC05 includes Dyna-P; their local findings were checked against the user-supplied publisher PDFs on22October2026. REC06 now includes the checked InferFair Table3 goodput524.29requests/s and unfairness1.05 under600requests/s,3:1:2mix,SLO100ms and50msperiod. These are conditional source outcomes, not a universal recommendation.

G01-G06 should remain observations about this reviewed corpus. Existing surveys discuss several of the same issues, and lack of a matched experiment in this set is not proof of absence throughout the literature. Dyna-P job completion and makespan are not substitutes for online request-tail measurements. KRISP's calibrated emulation is not a measured deployable NVIDIA MPS implementation. Tally'sE052quantity sums normalized throughput across concurrent workloads, rather than measuring background throughput alone.

## Outstanding human review and access

All six assigned sources,60QAitems,36eligibility checks and9outcomes have been source-checked. InferFair was closed using the correct supplied publisher copy. Original forms remain frozen; the master now integrates the supported corrections.

Rameen's independent check of Eshaal'sP001-P007plusP023 awaits Eshaal's first-review return and actual separate human judgments. Rameen's own six-study work is to be independently checked by Raazia. AI preparation in this package is not either person's signature. Source-based scores are integrated in the current master; actual teammate adjudication remains pending.

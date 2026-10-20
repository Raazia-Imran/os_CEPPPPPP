# Opening draft: guideline headings 1–3

Drafted UTC: 2026-10-20T20:47:14.776Z. Status: editorial first draft, not a newly verified full-text synthesis. This file begins the report's Introduction under guideline heading 24; guideline numbers are a requirements map, not necessarily the final report's section numbers.

## 1. Background and scope
Multi-tenant inference serving requires a system to allocate GPU capacity among applications whose response-time requirements and resource demands differ. The engineering objective is not simply to keep the device busy. Useful service depends on whether each tenant receives responses within its latency target, while the operator seeks to serve more work with the available hardware. A configuration that increases aggregate throughput can therefore be unsuitable if it causes an unacceptable increase in one tenant's tail latency.

The assigned Topic 23 frames this problem around temporal sharing, process-level concurrency such as MPS, hardware partitioning such as MIG, and API interception or remoting. These categories describe different points of control. Scheduling determines when work runs; resource allocation determines which work may coexist; interception or remoting determines where requests can be observed and controlled. The final taxonomy should therefore permit a system to combine categories rather than forcing every study into one exclusive class.

This review is bounded at the single-node operating-system and runtime layer. Cluster-level placement is relevant only when evidence about a local sharing mechanism is separable. Training-only scheduling is outside the inference-focused question; mixed inference and background workloads are relevant when the inference outcome is reported distinctly. The supplied report catalogue and eligibility decisions govern the actual included set; this prose does not amend them.

## 2. Engineering problem
The decision is to select an appropriate local GPU-sharing mechanism for a specified workload, hardware platform and service objective. Four requirements must be evaluated together: useful throughput, per-tenant latency, resource efficiency, and isolation. Implementation effort, compatibility, profiling cost and runtime overhead determine whether a promising mechanism is feasible in the intended deployment.

The comparison must distinguish several meanings of success. Aggregate requests per second measures completed work, whereas goodput counts work meeting a stated service criterion. Mean latency does not establish tail-latency behavior. A reported p95 result cannot be treated as p99 evidence, and an internal switching delay is not an end-to-end request latency. Likewise, performance isolation is not evidence of protection against memory faults or security attacks. A recommendation must identify which property was actually evaluated.

The central conflict is that admitting additional concurrent work can improve capacity use while increasing contention or scheduling delay. Restricting concurrency or assigning a more stable resource share may protect a priority tenant, but can leave capacity unused or constrain background progress. Dynamic adjustment introduces another dependency: the decision must remain suitable when arrivals, model mixes or performance estimates change. These relationships motivate a conditional comparison rather than a universal ranking.

The final evidence matrix will retain the hardware, model or workload, offered load, batch size, sharing configuration, comparator, metric definition and measurement location for each supported claim. Missing fields will be marked as not reported or not yet verified. Numerical improvements will remain tied to their original comparator; ratios from incompatible experiments will not be pooled into a headline winner.

## 3. Review objective and intended contribution
The review aims to determine which categories of GPU-sharing mechanisms are suitable under different inference-serving conditions, what benefits are supported by the available evidence, and which sacrifices accompany those benefits. Each recommendation must state the relevant workload and hardware conditions, the service objective, the evidence supporting the recommendation, its implementation or performance cost, and the circumstances in which an alternative becomes preferable.

The intended contribution is an evidence-based selection framework: a mechanism taxonomy, a context-preserving comparison, an explanation of trade-offs and apparent disagreements, and a set of conditional engineering recommendations. The original protocol's research questions will organize the synthesis and must be copied faithfully before drafting their answers.

## Evidence boundary for subsequent sections
The supplied later baseline identifies 21 reports representing 20 studies, including two linked REEF reports. This describes the supplied synthesis corpus; it does not establish exhaustive coverage of all eligible literature. The unassessed retained pool, review provenance, unavailable reading copies and report-version uncertainties must be disclosed in methods and threats to validity. No new experiment or independent reviewer check is claimed by this draft.

## Integration notes
- Governing topic and requirements: docs/topics.md and docs/guidelines.md.
- Baseline evidence: task3/baseline/CEP_EVIDENCE_WORKBOOK.xlsx and task3/papers/manifest.json.
- Add verified primary-paper citations and source anchors during the comparison and synthesis pass. No numerical result is newly asserted in this opening draft.
- Preserve submitted Task 1 and document changes separately.

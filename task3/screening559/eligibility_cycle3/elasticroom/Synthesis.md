# ElasticRoom: integration into the analytical headings

Record R01093; study S028; report P031. Source: the supplied final HPDC 2024 paper, DOI 10.1145/3625549.3658654, 14 pages. All six eligibility criteria are met. The source-based QA result is 15/20. No independent human vote is asserted.

## Taxonomy and RQ1

ElasticRoom adds a compiler/runtime hybrid over native GPU multi-stream execution. A TVM-based compiler generates alternative implementations with constrained thread-block resource demands. At runtime, kernel ordering prioritizes real-time requests, while candidate selection adjusts the resources used by co-located kernels. This is finer-grained software scheduling and resource coordination. It must not be classified as a new MIG-like hardware partition or as demonstrated fault isolation. The paper evaluates NVIDIA A100 and AMD MI100 devices separately. Its broader portability claim remains bounded by those experiments and the framework-adaptation limits acknowledged on pages 2–3.

## Metrics, comparison and RQ2

The paper's Goodput is the number of QoS-satisfying requests divided by the maximum inference latency in the batch (page 4, equations 1–2). It is not automatically interchangeable with another system's token throughput, completed-query throughput or GPU busy-time utilization. The main latency endpoint is mean end-to-end real-time latency, including queueing, rather than p99. The reviewed request workloads have batch size one. Arrival-rate values and QoS scales should be copied with their original context; the arrival-rate time unit is not explicit in the inspected setup.

On A100, the paper reports 22% lower mean end-to-end real-time latency and 1.43 times Goodput relative to its described REEF policy, averaged across the three scenarios (page 10, Figure 8). These results should accompany the actual comparator implementation and workload. KRISP is also modified using ElasticRoom-generated kernels and a REEF-like priority strategy (page 9). Therefore, cross-paper statements that these results reproduce unchanged original KRISP or REEF experiments are unsupported.

On MI100, the unambiguous Multi-Stream comparison reports an average latency speedup of 1.08 and a Goodput ratio of 1.17 (page 10, Figure 9). A speedup of 1.08 must not be rewritten as an 8% latency reduction. NVIDIA and AMD results should remain separate rather than being pooled into a single hardware-independent effect.

## Conditions, adverse results and RQ3

Resource-constrained compilation and priority scheduling help when real-time and best-effort requests would otherwise contend for resources or queue behind one another. The scheduler breakdown finds little improvement for MobileNet because its computational load and interference are already low (page 11). This qualifies the benefit: finer-grained scheduling has more room to help some model/resource mixes than others.

Retain two adverse findings. First, on MI100, ElasticRoom-generated kernels perform worse than Ansor in the specified Conv2/thread-block-56 and Conv3/thread-block-64 cases, by less than 8% (page 11). Second, the authors report that their MI100 slows down during sustained execution, potentially making offline-generated kernel choices suboptimal (page 10). These statements concern the reported configuration and must not become general claims about all AMD hardware.

## Trade-offs, conflicting evidence and RQ4

ElasticRoom and GACER both connect compilation choices with runtime co-location, but they optimize different reported workloads and outcomes. GACER's batch-completion latency and achieved SM occupancy should not be treated as matched counterparts to ElasticRoom's QoS-qualified Goodput and mean real-time request latency. Likewise, an average-latency improvement does not establish a contradiction with another paper reporting a different p99 outcome.

The software design requires kernel variants, offline tuning and a runtime scheduler. Its lazy scheduling relies on predictable resource occupancy and kernel execution time (pages 7–8), which makes the reported execution drift a material validity concern. Strong real-time priority can trade capacity available to best-effort traffic, but the paper does not provide a general per-tenant fairness or starvation guarantee. Its virtual-room claim is performance coordination, not a demonstrated security or fault-containment boundary.

Preserve source-reporting ambiguities in the comparison notes: the setup says five baselines but names four comparator systems; it says five scenario settings but lists three; its prose describing scenarios 2 and 3 conflicts with their numeric tuples. The AMD text also changes comparator naming between a CU-masking description and the figure labels. The extracted Multi-Stream contrasts avoid that ambiguous mapping. These issues limit precision; they do not justify inventing corrected configurations or discarding all eligible evidence.

## Conditional recommendation, gaps and RQ5

Consider this compiler/runtime approach for known CNN/BERT inference mixes where priority-aware co-location, kernel recompilation and offline tuning are feasible. It adds evidence that hardware partitioning is not the only route to controlling real-time interference. It does not establish universal superiority over MPS, MIG, time-slicing or API remoting. Retain hardware partitioning's separately supported isolation role when the engineering requirement includes fault containment, and retain the source's limited framework and large-language-model coverage as research gaps. Completing the remaining eligible corpus may change the final recommendation.

## Deliverable updates

The eligibility register gains six criterion rows; QA gains ten items; extraction gains eight outcomes, including adverse evidence; bibliography gains one verified DOI entry. Integrate these rows into the new working report and workbook using S028/P031 without renumbering frozen IDs. Recompute selection counts only after the root register adopts this decision. The frozen release must remain unchanged.

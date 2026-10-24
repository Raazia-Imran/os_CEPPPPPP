# QLLM synthesis

Include S032/P035. Logical LS/BE inference workload classes are separately admitted, queued and prioritized on one GPU, with individual state and preempt/resume across MoE experts. This satisfies the protocol workload-based tenant definition without assuming process-level separation. Merely splitting prefill/decode into workers or tracking sequences would not alone establish that boundary.

For priority-differentiated MoE serving, QLLM provides evidence that fine-grained preemption can trade BE response time for LS responsiveness. At the studied20percentLS Poisson mix,the results body reports65.2xaverage/max101.6xTTFTspeedup and compliance with its3secondtarget through7offeredrequests/s; BE slowdown1.38xreported aggregate and2.04xpeak must accompany those gains. These source-specific ratios cannot be pooled with unlike DNN preemption latencies or treated as hardware-independent guarantees.

The abstract65.5x versus body65.2x discrepancy is preserved,with body chosen for extraction. TTFT quantile/window and SLO violation population are not stated. The source offers an initial evaluation,one model,one GPU and one LS fraction; memory cost and possible starvation remain unresolved. No request-p99,security boundary,fault isolation,energy gain or dense-model performance is inferred.

Conditional recommendation: consider expert-level priority scheduling where one MoE model serves independently managed priority workloads and extra sequence-state/cache management is acceptable. Prefer an alternative or add fairness controls where BE starvation is unacceptable; validate the actual class mix,software version,output lengths and response SLO first.

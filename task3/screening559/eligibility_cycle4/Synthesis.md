# KACE source assessment

Include as S030/P033. KACE chooses MPS colocations using offline kernel and system metrics. Figure 5 and section 5.2.3 separately identify inference targets, meeting the narrow inference requirement. The model training in the predictor must not be confused with the application workloads, which include both training and inference.

Choose this policy family when throughput-oriented colocation is the objective and offline profiling is feasible. Memory footprint or GPU busy rate alone can select a poor inference partner. The ViT batch-2 case explains how compute-intensive BERT batch-2 inference can interfere despite its small memory footprint. No latency target, tail guarantee, security or fault boundary is established.

The reported averages over all 21 target cases mix training and inference. They are contextual observations, not inference-only treatment effects. KACE is not uniformly best: the adapted Xu and MEMCAP policies win six and two cases respectively. Preserve those adverse cases. No figure values were digitized or reconstructed. Three/four-job results are reported without underlying plots. A single V100 platform and missing OS/driver details limit transfer.

QA is 14/16 applicable points. Q7 and Q9 are reasoned N/A because the paper makes no corresponding measured latency/isolation claim. No independent reproduction or reviewer vote is asserted.

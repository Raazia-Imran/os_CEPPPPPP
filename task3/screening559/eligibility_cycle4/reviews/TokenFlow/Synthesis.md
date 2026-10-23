# TokenFlow synthesis

Include S033/P036 as logical client-stream sharing. Each client specifies a required output rate; independently tracked buffers and execution state drive admission,preemption,offloading and resumption. The workload-management boundary is explicit; one shared model or process does not by itself establish or defeat eligibility.

TokenFlow adds evidence for consumption-aware temporal scheduling and proactive host/device KV movement. Keep timeliness-weighted effective throughput separate from raw tokens/sec and GPU utilization. Source-reported maximum gains depend on burst/Poisson load,hardware and token lengths. Lower TTFT is achieved by pausing streams with adequate client buffers and resuming urgent streams; the cost includes more scheduling work and host-transfer coordination.

Lower buffer conservativeness improves agility but risks stuttering;shorter0.5-1.5secondreschedule intervals improve responsiveness marginally with overhead. The reported scheduling cost is approximately0.4ms versus0.07msSGLang. Figure/table details contain model-label variation(Qwen2/Qwen2.5 and8B/32B) andTable2ablation times lack a clearly named endpoint,so those times are not recast as request mean/P99latency. Ascend910B results remain context outside GPU-only comparisons.

Conditional recommendation: consider per-client consumption-aware preemption for bursty streaming applications that can specify their output-rate requirement and support coordinated KV offload. Validate host-link bandwidth,buffer thresholds,fairness and actual rate distribution;retain a simpler scheduler when transfer/scheduler cost outweighs responsiveness gains. No fault-isolation or universal strictQoSguarantee is inferred.

Source-version boundary: the inspected17-pageauthor-endorsedacceptedscientificreport is linked by the authors'EuroSys2026implementation. Publisher PDF access returned403; no byte-identicalcopyeditedequivalence is claimed. The acceptedpaperidentity and scientificcopy are recorded distinctly.

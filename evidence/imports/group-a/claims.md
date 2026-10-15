# Group A — provisional claim and RQ matrix

All recommendations are reviewer interpretations of heterogeneous published experiments, not deployments validated by this group. The full-text set is current, not a final systematic selection. No pooled numerical effect is calculated.

| ID / RQ | Provisional interpretation | Primary support | Counterevidence / condition | Strength |
|---|---|---|---|---|
| C1 / RQ1,3 | Temporal scheduling is a candidate for priority inference when co-tenant work can be controlled. | GA-S001,003,004,008,014,015; extraction anchors | Memory handover, context and runtime differ; no universal bound | Direct within each study; indirect across studies |
| C2 / RQ1,3 | MPS provisioning can support density goals, with workload-specific tuning. | GA-S002,012,017,020 | Loading/reconfiguration and interference matter; density is not security | Direct within study; conditional interpretation |
| C3 / RQ1,3 | MIG and MPS can be combined; slice memory pressure must be checked. | GA-S010,016,019 | Parva author manuscript; Fermilab local-slice evidence only | Direct within each study; indirect comparison |
| C4 / RQ2 | Goodput, throughput, busy time, GUE and occupancy require distinct columns. | GA-S004,005,010,012 | Different denominators and percentiles prevent raw pooling | Measurement interpretation |
| C5 / RQ4 | Protecting priority latency can reduce lower-priority throughput. | GA-S009 section5.3 Fig6 | Tally does not dominate TGS on BE throughput in that stratum | Direct counterexample |
| C6 / RQ4,5 | API remoting is a candidate when transfer costs fit the SLO budget. | GA-S005,006,007,009,011 | PCIe/NVLink path, runtime compatibility, process boundary and scheduler overhead | Conditional, indirect across systems |
| C7 / RQ1,4,5 | Performance protection does not establish security or fault containment. | GA-S007 section2.2; all isolation columns | Most extracted results do not test adversarial isolation; GhostWriter remains inaccessible, with no further user download requested | Insufficient comparative security evidence |

RQ-to-final-output: RQ1 → mechanism/control boundary taxonomy; RQ2 → definitions and comparability table; RQ3 → hardware/workload/configuration strata; RQ4 → trade-offs/counterexamples/operating cost; RQ5 → conditional decision matrix. Required field groups are preserved in extraction.csv; untranscribed parameters are explicitly NOT EXTRACTED rather than marked absent in the paper.

Sensitivity: all current QA totals are at least6.5, so dropping QA<6 removes none and provides no discriminating test. Removing author-manuscript ParvaGPU and Tally weakens the hybrid MIG and negative-throughput evidence. Removing AMD-only KRISP and the main AMD REEF stratum leaves NVIDIA temporal/API/MPS evidence but does not validate AMD-to-NVIDIA transfer. Dropping incomplete environment profiles would remove much of the set; current recommendations are therefore provisional. Do not convert a high rubric total into high causal confidence or complete search coverage.

Next extraction pass: finish driver/runtime versions, MIG profile names, MPS quotas, batching, exact arrival rates, warm-up/windows/variance and measured-vs-claimed isolation fields before final recommendations. Check all newer/related reports and repeat synthesis after resolving the access queue. No experiments or code artifacts have been rerun.


Six-paper update: GA-S017 VastPipe supplies local A100 MPS and separate MI100 CU-mask throughput strata; its 1000-NPU cluster results are outside the local GPU comparison. GA-S018 ArkGPU supplies mixed inference/training p99/QPS evidence; its four-GPU goodput gains are separate. GA-S019 Dyna-P supplies local MIG inference-job results and a concurrency/JCT trade-off; cluster simulations and makespan are not online p99 measurements. GA-S020 iGniter supplies local MPS interference and transient p99 failure/recovery evidence; fleet cost savings are not local utilization. GA-S021 InferFair supplies local fairness/SLO goodput with distinct unfairness definition. Updated GA-S001 journal REEF supplies NVIDIA comparisons and a throughput cost of latency protection; the OSDI report is a linked E8 companion, never an additional study.

Reporting sensitivity: the four newly included moderate-QA studies (VastPipe6.5, ArkGPU7, Dyna-P7, InferFair7.5) are removed by a stricter QA>=8 sensitivity stratum; iGniter and journal REEF score8.5. Removing these moderate rows weakens dynamic-MIG placement, API-throttled inference/training and relative-goodput fairness evidence. QA<6 removes none. Scores do not resolve missing full-text plot data. No universal or pooled percentage improvement is defensible.

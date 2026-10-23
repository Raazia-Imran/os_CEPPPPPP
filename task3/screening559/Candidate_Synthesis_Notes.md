# Candidate additions for the next report version

These notes concern four newly inspected candidates. They are not integrated into the frozen20-study report. First full-text eligibility, provisional QA and extraction are prepared; independent review and adjudication remain pending. No study identifiers in the frozen corpus have been renumbered.

## RQ1 mechanisms

LithOS adds transparent CUDA-driver interposition, TPC-level spatial scheduling, TPC stealing and temporal kernel atomization. Its implementation builds on MPS rather than constituting a hardware-independent replacement for it. Right-sizing and power management are additional mechanisms and are disabled in the scheduling-only comparison (SOSP2025, DOI10.1145/3731569.3764818, sections5-8).

Abacus adds headroom-based operator-group scheduling and latency prediction across separate model-service processes. The relevant mechanism is deterministic overlap of selected operators, not simply deploying more models. Its local MPS and MIG experiments are separable from a later cluster experiment (SC2021, DOI10.1145/3458817.3476143, sections4-7).

Miriam adds source-to-source elastic-kernel transformation and runtime coordination for mixed-criticality DNNs. It targets fine-grained resource contention without relying on the MPS/MIG support assumed by server systems. The exact edge platform identity is inconsistent in the inspected report and must remain unresolved pending verification (SenSys2023, DOI10.1145/3625687.3625789, sections5-9).

SGDRC adds software-defined compute and VRAM-bandwidth control using learned channel mapping, page coloring, bimodal tensors and dynamic SM masks. It specifically evaluates inference on P40 and RTX A2000. Its TVM-generated kernels and common CUDA context constrain transparency and fault isolation (PPoPP2025, DOI10.1145/3710848.3710863, sections5-10).

## RQ2 measurement context

Do not combine normalized aggregate throughput with queries/s or image samples/s without preserving each definition. Abacus separates50QPS latency and100QPS peak-throughput experiments; baseline deadline-dropped requests are excluded from latency but included in violation counts. SGDRC combines LS goodput with BE sample throughput and defines SLO as the concurrent-service count times isolated p99. LithOS uses app-specific latency and throughput-oriented SLOs and unequal supported tenant sets for some baselines. Miriam reports normalized critical-task latency and total throughput across workload patterns; its figure does not justify treating an introductory under10percent overhead statement as universal.

## RQ3 context dependence and adverse evidence

Abacus reports slight degradation for saturated VGG16/VGG19 co-location because little overlap opportunity remains while scheduling still costs time. LithOS comparisons with MIG/Limits omit a BE app on those baselines, and MIG cannot implement the same75/25partition fractions; this is a deployment-capability comparison, not evidence of identical allocation conditions. SGDRC is not universally fastest in raw throughput: Multi-streaming wins some cases at the cost of LS latency/goodput. Miriam's MDTB-A data show21percent and28percent critical latency overhead versus Sequential on the two reported platforms, paired with64percent and83percent throughput improvements; do not pair a best-case throughput from another workload with these latencies.

## RQ4 isolation and engineering costs

These additions reinforce the distinction between performance management and security/fault isolation. SGDRC explicitly cannot isolate co-located DNN GPU runtime errors in its shared CUDA context. Abacus uses separate service processes, which does not itself establish GPU memory or fault isolation. LithOS and Miriam show measured performance protection under stated tasks; neither result should be rewritten as a general security guarantee. Implementation costs include reverse-engineered driver/resource behavior, transformed kernels, offline profiling, CPU prediction/scheduling and limited support for special or closed-source kernels.

## RQ5 conditional recommendation changes to consider

For transparent multi-model datacenter inference on the evaluated A100 stack, LithOS merits comparison with the existing recommendation, conditional on compatibility, special-kernel handling and local reproduction. When low-end NVIDIA devices lack MIG, SGDRC provides an empirically evaluated compute-plus-memory-control candidate, conditional on TVM kernel generation and acceptance of its fault boundary. On edge devices, Miriam is a candidate when source kernel transformation is feasible and measured critical-task overhead fits the application budget. Abacus is a candidate when workloads are known sufficiently for operator profiling and prediction, with saturated pairs avoided when overlap provides no benefit.

These are review inferences from the cited papers, not new reproduced experiments or a cross-paper ranking. The recommendation must be reconsidered after all newly eligible studies, independent corrections and sensitivity checks are integrated.

# Six supplied papers — full-text review, 11 October 2026

This completes the six-paper review stage under the adopted Group A protocol. AI-CODEX is the sole reviewer. Source files are user-supplied Markdown conversions of published journal articles; their filenames and SHA-256 hashes are in uploaded_paper_receipts.csv. No licensed full text is committed. Assessments and source locations are reproducible from uploaded_review_assessments.json; the originals remain private.

Five new studies are included. The more complete REEF journal version replaces the OSDI2022 preferred report within GA-S001. The conference record remains a full-text E8 companion, not an eligibility rejection of REEF itself. companion_report_extraction.csv and companion_report_quality.csv preserve the former assessment. Six pending reports resolved plus the superseded conference classification increase full-text assessments from22 to28; unique studies rise16 to21, full-text exclusions6 to7, and pending cases102 to96. Discovery counts remain689 formal occurrences,10 duplicates and20 selected supplementary records.

| Record | Study | Paper | Decision | QA /10 |
|---|---|---|---|---:|
| GA-R0006 | GA-S017 | vastpipe | Include | 6.5 |
| GA-R0037 | GA-S018 | arkgpu | Include | 7 |
| GA-R0014 | GA-S019 | dynap | Include | 7 |
| GA-X005 | GA-S020 | igniter | Include | 8.5 |
| GA-X006 | GA-S021 | inferfair | Include | 7.5 |
| GA-X007 | GA-S001 | reef | Preferred journal version; same study | 8.5 |

The six conversions contain readable evidence for eligibility, but do not preserve original plot pixels. Missing chart points, CDF percentiles, damaged equations and uncertain labels are not reconstructed. Source line numbers refer to the supplied conversion; printed pages/sections/figure identifiers are preferred for later checking. NOT EXTRACTED is different from not reported in the original. No experimental code has been rerun.

## GA-S017 — vastpipe

Protocol7.2: explicit pairs of inference services share an A100 using MPS, with local throughput comparators. NPU/cluster scope alone would not qualify.

**Source:** https://doi.org/10.1007/s11390-024-3773-5; Published pp457-459; sections6.7-6.9; Figs14-16; uploaded Markdown lines1150-1290.

**Setup:** Local NVIDIA A100: TensorRT serving, MPS; AMD MI100: TVM/ROCm with hipExtStreamCreateWithCUMask. GPU memory, OS, driver and runtime versions NOT EXTRACTED for these GPU experiments. NPU Table3 is not the GPU configuration.

**Workload:** Co-located CV pairs (VGG16/GoogLeNet, VGG19/GoogLeNet, ResNet101/InceptionV3, VGG19/ResNet50); NLP/CV pairs with BERT/GPT2; Poisson-generated request mixes. Exact GPU batch sizes and rates NOT EXTRACTED.

**Comparators:** No MPS; default MPS without per-service quotas; RL-selected MPS quotas. AMD no/default CU mask separately.

**Bounded outcome:** A100 VGG16+GoogLeNet: throughput 2.7x no MPS and 1.5x default MPS; not a universal average or p99 result. NLP/CV mean 2.43x no MPS, 1.45x default MPS. MI100 mean 1.89x no mask, 1.24x default mask.

**Limits:** Include only local GPU inference evidence, not the main 1000-NPU cluster results. Offline Q-table assumes relatively stable request mix; GPU-specific quotas, repetitions and variance unresolved. Chart bars are not preserved in Markdown. Preliminary ICCD2021 report is linked as an unassessed version lead.

**Isolation:** Performance: Throughput/interference comparison only; no extracted tail-latency or SLO protection measurement. Resource/memory: MPS quotas/CU masks described; no separate memory-capacity enforcement test extracted.. Security: Not established. Fault containment: Not tested in extracted GPU results.

QA: Q1=1: Local model co-location question explicit in6.7/6.8; Q2=1: Per-model MPS control and CU-mask API specified; Q3=0.5: GPU models/backends known; GPU OS/driver/version/memory unresolved; Q4=1: Named co-located models and request distribution; exact load incomplete; Q5=0.5: No/default/tuned sharing compares same platform; exact quotas incomplete; Q6=1: Throughput ratios and requests/s labelled; no tail-latency inference; Q7=0: GPU-specific warm-up, run duration, repetitions and variance not recoverable from supplied text; Q8=0.5: Figures/captions and numerical prose survive; chart bars do not; Q9=0.5: Stable-mix/Q-table assumptions stated; GPU threats incompletely discussed; Q10=0.5: GPU results interpretable with caveats; insufficient configuration for replication.

## GA-S018 — arkgpu

Protocol7.2 mixed-workload exception: LC inference-specific outcomes from local inference/training co-location test API control of BE resource interference. Transfer limited to this priority mix.

**Source:** https://doi.org/10.1007/s42514-023-00154-y; Published pp313-319; sections4.3,5.1-5.4; Table3; Figs14-21; Markdown lines920-1360.

**Setup:** Machine with four V100s; Xeon Platinum8163; CentOS7.9.2009; driver460.106.00; CUDA11.1; cuDNN7.6.5. Per-GPU memory/framework versions NOT EXTRACTED.

**Workload:** Five MLPerf inference LC models (ResNet50, SSD-MobileNet, SSD-ResNet34, DLRM, BERT), each paired locally with six BE training models (30 pairs). Single-stream query size1; p99 QoS threshold twice solo. Separate four-GPU app-mixes are not local occupancy evidence.

**Comparators:** MPS (Non-ArkGPU); k8s-native for QPS/utilization; GaiaGPU and adjustment-unit ablation. MPS quota settings NOT EXTRACTED.

**Bounded outcome:** Section5.2 reports all30 tested pairs satisfy the 2x-solo p99 QoS target with ArkGPU. Low-contention pairs can lose about5% QPS from throttling. Four-GPU app-mix goodput gains94.98% vs k8s-native and38.65% vs MPS are separate system-level results.

**Limits:** Mixed inference/training qualifies via explicit inference p99/QPS and workload transfer rationale; it does not establish inference-only performance. Polling/API sleeps can add delay; BE checkpoint/restart affects costs. Huge goodput ratios can have near-zero baseline yield. Repetitions/variance and chart coordinates unresolved.

**Isolation:** Performance: p99 tested against twice-solo QoS; average latency, QPS and goodput separately Resource/memory: API usage throttling/monitoring described; no hostile memory-enforcement experiment extracted. Security: Not established by API interception. Fault containment: Background discussion of MPS faults is not an ArkGPU fault test.

QA: Q1=1: LC protection during BE co-location explicit; Q2=1: CUDA interception, NVML polling, sleep and adjustment described in4.3; Q3=1: Table3 specifies GPU/CPU/OS/driver/CUDA/cuDNN; memory not transcribed; Q4=1: MLPerf single-stream, query size1,30 pairs and QoS rule explicit; Q5=0.5: MPS/native/GaiaGPU compared; quotas and baseline implementation incomplete; Q6=1: p99, average, QPS and yield-based goodput distinguished; Q7=0: Warm-up/window/repetitions/uncertainty not recoverable in supplied text; Q8=0.5: Tables and numerical prose readable; plot data unavailable; Q9=0.5: Throttling overhead and low-contention regressions discussed; limited threats analysis; Q10=0.5: Algorithm and data-on-request statement; workload/configuration gaps restrict replication.

## GA-S019 — dynap

Protocol7.2: identifiable concurrent inference jobs on MIG partitions; single-A30 local sensitivity/scalability strata in4.2/4.3.1 independently support inclusion.

**Source:** https://doi.org/10.1007/s10586-025-05284-2; PDF pp11-16; sections4.1-4.3.2; Table2; Figs8-13; Markdown lines700-865.

**Setup:** Two A30s,24GB each; CUDA12.2; driver535.171.04; DCGM3.1.3. Local sections4.2/4.3.1 use one A30. StaCon profiles2g.12gb+1g.6gb+1g.6gb. OS/backend versions NOT EXTRACTED.

**Workload:** 50 SLM inference jobs; batch1-64; DistilGPT, Codegen, Flan-T5-Large, Codellama and Phi-1 as labelled in Table2. Local batch sensitivity:10 inference jobs, batches1-8 vs32-64 on one A30. Later160-A100 cluster study is simulation.

**Comparators:** Full-GPU sequential baseline; fixed StaCon MIG; pre-profiled MISO adapted to A30; ORACLE with future job/size/time knowledge.

**Bounded outcome:** Single-A30 batch experiments: smaller partitions increase concurrency but can increase mean JCT; not online p99 evidence. Fig8 broader job set reports39.03% lower makespan vs StaCon,12.14% vs MISO and14.7% higher normalized STP vs StaCon. Prediction-error sensitivity:15% perturbation adds8.09% makespan.

**Limits:** Retain one-GPU inference strata separately from two-GPU aggregate and cluster simulation. JCT/makespan/STP cannot replace request-tail latency or goodput. Reconfiguration can stop/restart active jobs; neither architectural MIG claims nor OOM avoidance prove hostile isolation. Model labels/parameter counts and corrupted overhead fraction require caution.

**Isolation:** Performance: Job completion/makespan/STP and prediction sensitivity; no extracted online p99 guarantee Resource/memory: OOM failures for fixed StaCon reported; profiling/placement avoids them in tested set. Security: Architectural isolation discussed, no adversarial test. Fault containment: OOM observation is not cross-tenant fault containment validation.

QA: Q1=1: Fragmentation/concurrent inference question explicit; Q2=1: MIG profiles, merge/split and placement algorithms described; Q3=0.5: GPU/memory/CUDA/driver/DCGM clear; OS/backend unresolved; Q4=1: SLMs,50 jobs,batch ranges and local10-job strata explicit; Q5=0.5: MISO pre-profiled and adapted; ORACLE privileged information disclosed; Q6=1: JCT/makespan/normalized STP distinct; avoid p99 interpretation; Q7=0.5: Prediction perturbation and power-cap sensitivities; repetitions/variance unresolved; Q8=0.5: Table2 and numeric prose readable; plot coordinates missing; Q9=0.5: Reconfiguration cost/architecture and prediction limits discussed; incomplete threats treatment; Q10=0.5: Implementation described but missing runtime/control detail restricts replication.

## GA-S020 — igniter

Protocol7.2: local co-located MPS inference measurements and quota configurations identifiable; fleet allocation/cost is a distinct engineering outcome.

**Source:** https://doi.org/10.1109/TPDS.2022.3232715; Published pp820-824; sections4.2,5.1-5.4; Figs13-18; Markdown lines938-1245.

**Setup:** Ten EC2 p3.2xlarge instances,one V100 each,8vCPU/61GB; Triton2.12.0,TensorRT8.0.1.6. MPS active-thread percentage; allocation unit2.5%. Heterogeneous extension adds20 T4 instances. OS/driver/CUDA version NOT EXTRACTED.

**Workload:** AlexNet,ResNet50,VGG19(ImageNet),SSD(VOC2012);12 workload/SLO configurations; constant arrivals. Local experiment co-locates four models at25% quota,batch3. p99 provisioning measured over windows e.g.30s; model-validation experiments repeated3 times with SD bars.

**Comparators:** FFD+; GSLICE+ with iGniter placement; gpu-lets+ modified batch strategy and best-fit placement. These are adapted baselines.

**Bounded outcome:** Local four-model latency prediction error1.53%-5.02%(Fig13). Fig14 deployment: iGniter6 GPUs/0 SLO violations vs gpu-lets+8/3,FFD+5/10,GSLICE+6/3;25% lower hourly instance cost vs gpu-lets+, not25% higher local utilization. Fig17 shows an initial p99 violation before shadow-process recovery.

**Limits:** Constant arrivals and four vision models limit bursty/LLM transfer. Negligible PCIe contention assumption can underpredict AlexNet; baselines modified. Steady-state/post-correction SLO success is not an unconditional guarantee; shadow standby incurs capacity/memory costs. Chart bars/latency traces unavailable in Markdown.

**Isolation:** Performance: Local interference prediction and p99/SLO checks; transient prediction failure explicitly retained Resource/memory: MPS quotas/shadow process provisioned; no separate hostile-memory test. Security: Not established. Fault containment: Not tested in extracted results.

QA: Q1=1: Inference interference and SLO provisioning explicit; Q2=1: Active-thread quotas,batching,placement and shadow recovery described; Q3=0.5: EC2 GPU/CPU/memory and serving versions clear; OS/driver missing; Q4=1: Models,datasets,constant arrivals,quotas and local batch3 clear; Q5=0.5: Three adapted baselines and modifications disclosed; effect confounded with placement/batching; Q6=1: p99,SLO throughput,cost and prediction error distinguished; Q7=1: Model validation three repetitions/SD; p99 windows and update rule explicit; not all experiments have same controls; Q8=0.5: Figure captions/numeric prose survive; error bars and full traces not digitizable; Q9=1: PCIe assumption,model error and recovery described; Q10=1: Public code URL,algorithm and coefficients aid interpretation; code not rerun.

## GA-S021 — inferfair

Protocol7.2: local heterogeneous inference scheduling and sharing comparators provide measurable goodput/fairness outcomes, independent of four-GPU replay.

**Source:** https://www.sciencedirect.com/science/article/pii/S0167739X23003187; Published pp17-18; sections5.1-5.4; Table3; Eq2; Markdown lines718-899.

**Setup:** Dell PowerEdgeR740; V10032GB; local synthetic co-running experiment and separate four-GPU realistic trace. OS/driver/CUDA/backend versions NOT EXTRACTED.

**Workload:** Local GoogLeNet/ResNet152 Poisson arrivals; three-model test adds Mobile_Pose_MobileNetv3;600req/s distributed in six ratios; SLO100ms and interval50ms. Separate61-model,90min MAF replay on four GPUs.

**Comparators:** Clockwork; MPS plus Clockwork SLO scheduling with two worker processes/GPU; EDF without batching (not a like-for-like batching baseline).

**Bounded outcome:** Local Table3 load3:1:2: unfairness1.05 vs Clockwork1.50; SLO goodput524.29 vs457.24req/s. Other load ratios give smaller differences. Local unfairness is max/min model slowdown(Eq2), not p99 or security. Four-GPU MAF outcome kept separate.

**Limits:** Two-column Markdown interleaves algorithms/prose; use labelled Table3 rows and sections, not scrambled formulas. Repetitions/variance and software versions unresolved. MAF trace has minute-level invocation counts; cross-study batching and isolation definitions differ.

**Isolation:** Performance: Relative goodput/slowdown fairness and SLO-compliant goodput; no extracted p99 bound Resource/memory: Memory management identified as future work; no extracted enforcement test. Security: Not established by performance-isolation terminology. Fault containment: Not tested in extracted results.

QA: Q1=1: Heterogeneous model-sharing fairness explicit; Q2=1: Estimator,feedback controller and temporal scheduling described; Q3=0.5: Server/GPU/memory clear; OS/driver/backend unresolved; Q4=1: Models,Poisson load,SLO,interval,load ratios and replay duration explicit; Q5=0.5: Clockwork and adapted MPS; EDF lacks batching and is less directly comparable; Q6=1: Goodput requests/s and unfairness ratio distinguish outcome definitions; Q7=0.5: 90min replay and parameter sensitivity clear; local repetitions/variance unresolved; Q8=1: Table3 rows/labels unambiguous in Markdown; plot coordinates absent; Q9=0.5: Future work/memory and heterogeneity discussed; incomplete validity treatment; Q10=0.5: Algorithms interpretable despite column interleaving; software/control gaps restrict replication.

## GA-S001 — reef

Protocol7.2/9: complete peer-reviewed extension explicitly links OSDI2022; new NVIDIA implementation/evaluation and limitations justify preferred version without adding a study.

**Source:** https://doi.org/10.1145/3768622; Article pp1:23-1:24,1:31-1:34; sections6.2,6.6,7; Figs28-29; Markdown lines1111-1180,1600-1820.

**Setup:** One MI50,16GB/60CUs;i7-10700,32GB RAM;Ubuntu20.04,ROCm4.3.0,TVM0.14.0. Separate one GV100,32GB/80SMs;CUDA11.4,PyTorch1.12.0,TensorRT8.5.1. Driver version NOT EXTRACTED.

**Workload:** DISB A-E,uniform RT except Poisson E; closed-loop BE; ResNet152,VGG19,YOLOv3,BERT-base,GPT2 (128 tokens,GPT2 prefill). RT rates50%,100% or10% solo-throughput according to workload; Apollo/SVL trace. Separate LLM case batch1,100 decode tokens,MLC-LLM.

**Comparators:** RT-only; sequential priority; GPU streams. NVIDIA closed-source strata compare priority-enabled Triton/TensorRT and Orion/PyTorch without dynamic padding.

**Bounded outcome:** GV100 PyTorch DISB-C: Orion p99 normalized latency1.17x vs Reef below1.05x; normalized total throughput0.97x vs1.14x(Fig29). TensorRT comparison trades throughput: mean1.21x Triton vs1.11x Reef(Fig28). All ratios retain model-solo normalization; do not mix engines/AMD strata.

**Limits:** Explicit OSDI2022 extension; select journal as preferred report and retain GA-S001 once. Requires deterministic/stateless kernels; closed-source comparison omits padding. Memory assumed sufficient; bandwidth contention and input-shape profiling limits. Printed publication date differs from some issue-year indexing; recorded2025 follows supplied copy and is in cutoff either way.

**Isolation:** Performance: Per-request normalized RT distributions/p99 and separately normalized total throughput; engine/stratum retained Resource/memory: All models assumed to fit GPU memory; no enforced-memory-isolation experiment. Security: Not established by scheduler priority. Fault containment: Kernel killing/restart is a scheduling mechanism, not adversarial fault containment.

QA: Q1=1: RT and BE sharing question explicit; Q2=1: Reset/preemption,padding and NVIDIA implementation described; Q3=0.5: GPU/CPU/RAM/OS/frameworks clear; driver missing; Q4=1: DISB mix,RT relative rates,arrivals and model/token configurations explicit; Q5=1: Same-engine closed-source comparisons and priority settings disclosed; Q6=1: Latency and throughput denominators explicit; p99 prose anchored toFig29; Q7=0.5: Solo reference averaged1000 runs; repeats/duration for all serving tests unresolved; Q8=0.5: Captions/numerical comparisons survive; full CDF/plot data absent; Q9=1: Section7 details statelessness,determinism,graphs,bandwidth and memory limits; Q10=1: Implementation and explicit engine constraints permit interpretation; experiments not rerun.

## What remains

The original shortlisting/report checkpoint was merged through PR3. This update completes the six supplied full-text decisions, QA, extraction and report-version assessment. The intermediate deliverable is updated; it is not the final CEP report. No remaining-four or replacement download batch is requested. Unavailable records stay pending/deferred.

Next work: recover formal ACM/ScienceDirect query exports through accessible routes, document unrecoverable coverage, continue already identified public manuscript leads, check relevant publication dates and versions, fill configuration/measurement gaps where readable, perform systematic citation chasing and transparent sensitivity synthesis. Then produce the final20-30-page CEP report with RQ answers, decision matrix, reconciled flow and appendices. Human audit remains useful for the disclosed single-AI-reviewer bias. The21-study eligible checkpoint exceeds the15-20 target; retain eligible evidence and justify any later narrowing rather than silently dropping papers.

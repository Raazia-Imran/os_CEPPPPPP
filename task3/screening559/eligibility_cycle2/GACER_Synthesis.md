# GACER addition

Final source:GACERICCAD2024,9pages,fourauthors. The2023preprint differs in authorship and content and must not supply final numerical claims.

GACER adds a compiler/runtime hybrid using operator microbatch splitting and staged cross-model scheduling over native streams. This is resource-efficiency coordination rather than a demonstrated fault/security-isolation boundary. On oneA100,Table2reports3.30ms forVGG16+LSTM versus4.32ms sequential, and22.14ms for five models versus37.86ms sequential. These are batch-completion measurements, not tail serving latencies. The same paper measures achievedSMoccupancy; this is distinct fromGPUbusy-time utilization. Table3reports0.84-1.26seconds of optimization, creating an explicit adaptation-cost trade-off.

QA:13/18applicablepoints(72.2%);Q9reasonedN/A because no isolation guarantee is claimed. Do not force this into a20point denominator or replaceN/Awithzero. Lower score does not exclude an eligible study.

RQ1:cross-stack operator scheduling/microbatch granularity. RQ2:batch-completion latency, achievedSMoccupancy, optimization seconds. RQ3:effect depends on model heterogeneity, tenant count andGPU. RQ4:profiling/search and transformation/synchronization overhead, incomplete replication details, no demonstrated isolation boundary. RQ5:consider for known multi-model batch mixes when profiling/optimization cost is acceptable; it does not establish better online tail-SLOor fault isolation thanMIG/MPS.

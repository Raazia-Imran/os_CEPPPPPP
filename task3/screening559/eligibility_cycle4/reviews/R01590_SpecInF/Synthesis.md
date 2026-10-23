# SpecInF synthesis

Classify as temporal CUDA API interception/kernel gating with training-bubble detection, notMIG. The key inference result is separable from distributedtraining: inferenceinstances share each physicalGPU with a primarytrainingworker. This adds evidence for exploiting idle intervals under mixed workloads and for the limits of fixedMPSallocation.

Recommendations must require sufficient residualGPUmemory and an inference request short enough to fit a trainingbubble. Benefits shrink for pipelineparallelmicrobatches; multiinstanceinference can still reduce primarytrainingthroughput. Keepoffline14xvsTGS andonline67%p95vsMPS distinct and retain Exclusive's additionalGPU cost. Noformaltrainingperformance or security/faultisolation guarantee is inferred.

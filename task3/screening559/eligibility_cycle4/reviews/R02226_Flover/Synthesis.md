# Flover synthesis

The qualifying local evidence is its controlled comparison against separately launched concurrent model instances on oneA100. The proposed implementation fuses autoregressive requests into a common generation stream; this is a remedy for measured baseline contention, not a claim that arbitrary same-model request batching always satisfies tenant eligibility.

Use GPTJ6B andLlama13B oneGPU outcomes for the local comparison. Keep33B/65B tensor-parallel results separately labelled. Fusion reduces launch and context overhead and can sharply improve aggregate completion time, while mean per-request latency still increases relative to an isolated request. No per-tenant isolation or tail-SLO guarantee is established.

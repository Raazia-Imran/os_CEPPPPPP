# HarmonyBatch synthesis

The local mechanism is cGPU temporal sharing. Separate applications may share the same model while retaining distinct SLOs, arrival rates and per-application batching timeouts; this satisfies the protocol management-based tenant definition. Time-slice-induced jitter in partial GPU allocations motivates separate average and maximum latency models.

The recommendation is conditional on cloud pricing, request rates, SLOs and batching tolerance. CPU functions can be preferable in an intermediate SLO regime; GPU functions become cost-effective for sufficiently strict or relaxed SLOs with suitable load. Do not compare cost reductions directly with hardware utilisation, and disclose that modified MBS+ includes the proposed predictor.

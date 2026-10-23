# EdgeServing synthesis

Classify as explicit temporal batch scheduling with separate model queues and scheduler-controlled early exits. The per-model queue management establishes distinct tenants even when homogeneous repeated-model combinations are evaluated. This adds a strong quality–latency tradeoff absent from simple throughput-only recommendations.

Under increasing load the system lowers tail latency partly by exiting at shallower classifiers. Expected accuracy drops from76.75% to60.38% on RTX3080 and can approach9% on the weakerGTX platform. Recommend only where these accuracy sacrifices are acceptable; do not call all experiments SLO-guaranteed. Retain profile-statistic and hardware-variant ambiguities and final DOI/page gap.

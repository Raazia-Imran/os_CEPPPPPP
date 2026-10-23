# MIGER remains pending

The user-supplied final paper is fully available. Access is no longer the blocker. The open issue is whether the reported evidence jointly satisfies concurrent GPU sharing and separable inference outcomes under the submitted narrow protocol.

The paper clearly proposes MPS within MIG partitions and uses online inference plus offline training. Its explicit one-device BERT experiment compares MIG allocation sizes, but does not identify another concurrent tenant. Its local three-job throughput comparison does not label the exact jobs as training or inference. The mixed-workload prediction experiment aggregates possible training/inference modes. These separate experiments must not be assembled into an invented same-device concurrent-inference result.

The main benefits reported for MIGER concern cluster/job completion, makespan and offline throughput. They are useful context for a hybrid MPS/MIG design, but do not by themselves close the inference-specific selection criterion. Therefore this review neither includes nor excludes the record. Reserved identifiers S030/P033 remain unassigned. QA/extraction for an included study should not be manufactured before eligibility closes; Candidate_Observations.csv is explicitly provisional context.

If later evidence identifies a specified inference model's measured latency or QoS while sharing a physical GPU/partition with an identified co-tenant, revisit IC3/IC4/IC5. A clear source-based scope adjudication is an alternative, but it must be documented and consistently applied. It cannot be hidden as an access failure or automatic EC6 exclusion.

Keep adverse and contextual limits if eventually included: smaller jobs have higher JCT than MISO/MuxFlow; immediate offline-job termination protects online QoS when predictions fail; prediction-error sensitivity is simulated, not a measured online tail-latency result; MPS within a partition does not inherit the inter-partition MIG fault boundary. Page2 reverses the order of36%/46.6% in one summary sentence, whereas page7 and the conclusion consistently map46.6%toMuxFlow and36%toMISO. Preserve body comparator mapping and flag the source inconsistency.

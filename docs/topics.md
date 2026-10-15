Topic Details

Topic 23. GPU sharing mechanisms for multi-tenant inference serving: time-slicing versus
MPS versus MIG versus API remoting, utilization against latency isolation

Standard SLR title

GPU Sharing Mechanisms for Multi-Tenant Inference Serving: A Systematic
Literature Review of Utilization and Latency Isolation Trade-offs

OS subdomain

OS support for GPUs and ML workloads

Central trade-off

GPU utilization and tenant density against predictable per-tenant inference
latency and fault isolation

Taxonomy categories

Temporal sharing and time-slicing; process-level concurrency (MPS); hardware
partitioning (MIG); API interception and remoting or virtualization

IEEE Xplore search string

("All Metadata":"GPU sharing" OR "All Metadata":"multi-tenant
GPU" OR "All Metadata":"GPU virtualization") AND ("All
Metadata":inference OR "All Metadata":"deep learning") AND ("All
Metadata":utilization OR "All Metadata":interference)

Literature estimate

Estimated 50 to 85 candidates. Confidence: high. Very active since 2021. The
main risk is scope creep into cluster scheduling, so bound the review at the
single-node OS and runtime layer.

Target venues

IEEE Transactions on Parallel and Distributed Systems (stretch for a review);
Future Generation Computer Systems (Elsevier)

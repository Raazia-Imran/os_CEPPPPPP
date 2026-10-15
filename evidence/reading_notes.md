# Public full-text checks | Group B, 15 October 2026

These notes are **preliminary source checks**, not a final included-study set or independent second-reviewer decision. Link each later numerical extraction to the final peer-reviewed publication and verify against its figures/tables.

## B-LEAD-0014: Naranjo et al., *Accelerated serverless computing based on GPU virtualization*

- User RIS DOI: `10.1016/j.jpdc.2020.01.004`. [Author-hosted manuscript, 30 pages](https://www.grycap.upv.es/gmolto/publications/preprints/Diana2020asc.pdf); [publisher record](https://www.sciencedirect.com/science/article/pii/S0743731519303533). The manuscript is an accessible version, not automatically identical in pagination to the publisher's final PDF.
- The abstract on PDF p. 1 describes local and remote GPU virtualization and deep-learning inference on echocardiography images. Section 3.2 (PDF pp. 7–8) describes rCUDA clients and a remote GPU server that can be shared by several applications.
- The results discussion on PDF pp. 20–21, Fig. 9, compares simultaneous processing of up to four videos under rCUDA and native-GPU settings. It explicitly links the concurrency comparison to a single shared GPU. The setup on PDF p. 17 mentions a Tesla V100 with 32 GB and a 10 GbE network connection.
- **Provisional fit:** promising API remoting primary study with separable inference-sharing evidence. Verify that its measured time is an appropriate inference outcome, distinguish end-to-end video processing from per-request GPU latency, check the final journal article/version, and apply the submitted IC/EC and Q1–Q10 rubric before inclusion.

## B-LEAD-0020: Liang et al., *Lilou: Resource-aware model-driven latency prediction for GPU-accelerated model serving*

- User RIS DOI: `10.1016/j.peva.2025.102539`. [Author-hosted manuscript](https://lass.cs.umass.edu/papers/pdf/lilou_gpu_prediction.pdf); [publisher record](https://www.sciencedirect.com/science/article/pii/S0166531625000732).
- PDF p. 2, Fig. 1 discusses MPS resource limits and an inference latency example; p. 6 says the evaluation uses MPS to constrain GPU capacity. The main system predicts inference latency under resource allocations; the text examined so far does not establish concurrent tenants or a direct isolation/interference comparison.
- **Provisional fit:** useful context or baseline; do not count as a Group B primary study until the full methods show an eligible shared-GPU inference contrast.

## B-LEAD-0022: Prades, Reaño and Silla, *NGS: A network GPGPU system for orchestrating remote and virtual accelerators*

- User RIS DOI: `10.1016/j.sysarc.2024.103138`. [Peer-reviewed final publisher version at the university repository](https://pure.qub.ac.uk/en/publications/ngs-a-network-gpgpu-system-for-orchestrating-remote-and-virtual-a/).
- The repository abstract describes cross-node access to remote GPUs; it does not mention inference. **Provisional fit:** likely context rather than primary inclusion under the submitted single-GPU concurrent-inference rule. Check the full text before a final reasoned exclusion.

## Other leads with public copies

- B-LEAD-0039, Gilman and Walls, *Characterizing concurrency mechanisms for NVIDIA GPUs under deep learning workloads*: [author preprint record](https://arxiv.org/abs/2110.00459), [journal publisher record](https://www.sciencedirect.com/science/article/pii/S0166531621000511). The abstract explicitly mentions training **and** inference. Match the peer-reviewed version and separable inference results.
- B-LEAD-0024, *Using remote GPU virtualization techniques to enhance edge computing devices*: [publisher record](https://www.sciencedirect.com/science/article/pii/S0167739X22004423), [public author version](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4273555). Check whether remote processing evaluates several tenants of the **same physical GPU**, instead of only a single offloaded application.
- B-LEAD-0008, *SpaceFlow*: [publisher record](https://www.sciencedirect.com/science/article/pii/S0743731526000894). Its abstract documents spatial partition enforcement; concurrent **inference** measurement remains to verify from full text.
- B-LEAD-0042, *Optimum*: [publisher record](https://www.sciencedirect.com/science/article/pii/S1383762123000802), [author preprint record](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4305614). Determine whether model deployment tests a submitted GPU-sharing mechanism, rather than only model placement or batching.

The first usable full-text candidate requires final peer-review/version and quality verification; no headline comparative numerical result is copied from an unchecked PDF into the report.


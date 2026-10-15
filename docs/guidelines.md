OPERATING SYSTEMS
Complex Engineering Problem (CEP)

Title
Evidence-Based Analysis of a Contemporary Operating Systems Engineering Problem
Using a Systematic Literature Review

-  Group size: Three students per group
-  Submission deadline (week): 13th
-  Minimum primary studies (final included set): 15 to 20
-  Referencing style: IEEE
-  Report format: min 20 to 30 pages, font 12, submitted as hard copy and soft copy

1. Background
Modern operating systems must make engineering decisions under multiple and often conflicting
requirements. A solution that performs well for one workload, hardware configuration, or system
requirement may perform poorly under another. For example, improving throughput may
increase response time, stronger security may introduce performance overhead, improved
resource utilization may reduce isolation, and energy savings may affect application
performance.

For many Operating Systems problems, several algorithms, mechanisms, policies, architectures,
and system designs have been proposed. However, results reported in the research literature may
differ because of variations in workloads, hardware platforms, operating-system configurations,
evaluation metrics, experimental methodologies, and assumptions.

Therefore, selecting an appropriate solution requires systematic collection and critical evaluation
of available research evidence rather than relying on a single study or a simple comparison of
techniques.

2. Generic Complex Engineering Problem Statement
For the assigned Operating Systems topic, multiple algorithms, mechanisms, policies,
techniques, architectures, or system-level solutions have been proposed in the research literature.
These alternatives differ in their assumptions, implementation complexity, performance
characteristics, resource requirements, scalability, reliability, security, energy consumption, and
suitability for different workloads and operating environments.

There is no single solution that can be assumed to be universally optimal. Selecting an
appropriate solution requires consideration of several interacting and sometimes conflicting
engineering requirements. Furthermore, existing research may report incomplete, heterogeneous,
or contradictory findings because studies are conducted using different hardware platforms,

operating-system versions, workloads, datasets, configurations, baselines, and evaluation
metrics.

Your task is to investigate the assigned problem through a Systematic Literature Review
(SLR) using a predefined and reproducible review protocol and reporting the study-selection
process according to PRISMA 2020.

You are required to identify and critically evaluate the major existing solutions, analyze their
strengths and limitations, investigate the engineering trade-offs among them, explain conflicting
evidence where it exists, and determine the conditions under which different approaches are
appropriate.

The final objective is to produce an evidence-based engineering recommendation for the
assigned Operating Systems problem.

A descriptive literature review or paper-by-paper summary will not satisfy the requirements of
this CEP.

3. CEP Objective
The objective of this task is to determine:

Which existing approach, or category of approaches, is most appropriate for
the assigned Operating Systems problem under different system requirements,
workload characteristics, constraints, and operating conditions, and what
engineering trade-offs must be accepted when selecting that approach?

Your recommendation must be supported by systematically collected research evidence.

4. Required SLR Methodology
You must conduct a structured Systematic Literature Review using a predefined SLR protocol
and report the review in accordance with PRISMA 2020.

PRISMA 2020 provides a checklist and flow-diagram framework for transparently reporting the
identification, screening, eligibility assessment, exclusion, and inclusion of studies.

5. Required Activities
Activities 1�3 below cover the initial phase: defining the problem, scoping the literature, and
framing the research questions. They are not the whole assignment. The remaining required work
is specified in Sections 6�22 (protocol, systematic search, PRISMA screening, quality

assessment, data extraction, taxonomy, comparison, trade-off analysis, evidence synthesis, and
the final recommendation). Treat the entire sequence as the set of activities you must complete.
Activity 1: Understand and Define the Engineering Problem
Clearly define your assigned Operating Systems problem.

Your discussion should identify:

the system or application context;
the technical problem being addressed;

-
-
-  why the problem requires an engineering decision;
-
-
-  major conflicting engineering requirements;
-  workloads or operating conditions that may influence the decision.

the major competing solutions;
relevant system constraints;

You must clearly explain why one approach cannot automatically be considered the best under
all conditions.

Activity 2: Conduct a Preliminary Literature Investigation
Perform an initial search to understand:

existing terminology;

-
-  major approaches;
-
-
-
-  potential research gaps.

important authors and studies;
commonly used evaluation metrics;
recent surveys and systematic reviews;

You should also determine whether a recent SLR has already answered exactly the same research
question.

If such a review exists, refine your scope, research questions, comparison dimensions, workload
context, or publication period so that your study provides a meaningful contribution.

Activity 3: Formulate Research Questions
Develop approximately 3�5 focused Research Questions (RQs).

Your RQs should require analysis and evaluation rather than simple description.

A generic structure may include:

RQ1. What algorithms, mechanisms, techniques, policies, architectures, or approaches have been
proposed to address the assigned Operating Systems problem?

RQ2. Which metrics and experimental conditions are used to evaluate these approaches?

RQ3. What strengths, limitations, and engineering trade-offs are reported for the identified
approaches?

RQ4. Under which workloads, hardware configurations, system requirements, or operating
conditions do different approaches perform better or worse?

RQ5. Based on the available evidence, which approaches are most appropriate for different
system requirements and why?

You may modify these RQs according to your assigned problem.

6. Prepare the SLR Protocol
Before final study selection, prepare a review protocol containing:

1.  research objective;
2.  research questions;
3.  selected academic databases;
4.  search keywords;
5.  search strings;
6.  publication period;
7.  inclusion criteria;
8.  exclusion criteria;
9.  screening procedure;
10. quality-assessment criteria;
11. data-extraction fields;
12. evidence-synthesis strategy.

Major changes made to the protocol after searching should be documented and justified.

7. Selection of Academic Databases
Database selection must be based on the resources available through the E-Databases section of
the NED University E.A. Khan Library E-Resources page. The library provides access to
scholarly resources relevant to engineering, computing, science, and related disciplines.

NED University E.A. Khan Library E-Resources
Requirements
You must:

-
-
-
-
-

examine the E-Databases section;
identify databases relevant to your assigned problem;
select preferably at least four suitable academic databases;
justify the selection of each database;
apply a systematic search strategy across the selected databases.

Where appropriate, citation-indexing resources may also be used for citation tracking and
validation.

Google Scholar should only be used as a supplementary source, for example for
backward/forward citation searching or discovering additional studies. It should not replace
systematic searching of appropriate scholarly databases.

8. Develop the Search Strategy
Identify keywords from:

-
-
-
-
-
-

the assigned problem;
relevant Operating Systems concepts;
competing approaches;
alternative terminology;
synonyms;
application/workload context.

Construct search strings using Boolean operators where supported:

AND, OR, NOT

For example:

("container isolation" OR "container security") AND ("performance overhead" OR latency OR
throughput)

This is only an example. Your actual search string must correspond to your topic and RQs.

Record the exact search string used in each database.

9. Literature Period
Give priority to recent peer-reviewed literature, preferably covering approximately:

2020�2026

Older studies may be included where they:

introduced an important algorithm or mechanism;
-
represent seminal work;
-
-  define an important baseline;
-

remain directly relevant to the problem.

Any substantial use of older literature should be justified.

10. Inclusion and Exclusion Criteria
Define explicit criteria before screening.
Possible Inclusion Criteria
Studies may be included if they:

are peer-reviewed journal or conference papers;

-
-  directly address the assigned problem;
-  propose, evaluate, compare, or analyze relevant approaches;
-
-
-
-

contain sufficient technical detail;
report relevant experimental or analytical evidence;
are written in English;
fall within the selected publication period.

Possible Exclusion Criteria
Studies may be excluded if they:

-
-
-

are duplicates;
are unrelated to the research questions;
contain insufficient technical information;

are editorials, presentations, posters, or unsupported opinion articles;
contain only an abstract without sufficient study details;

-
-
-  do not evaluate relevant OS mechanisms or engineering requirements.

Topic-specific criteria should be added where necessary.

11. PRISMA 2020 Study-Selection Process
Document the study-selection process using PRISMA 2020.

The screening process should include, where applicable:
Stage 1: Identification
Record studies retrieved from each database.
Stage 2: Duplicate Removal
Identify and remove duplicate records.
Stage 3: Title and Abstract Screening
Screen titles and abstracts against the predefined inclusion/exclusion criteria.
Stage 4: Full-Text Assessment
Retrieve potentially relevant studies and assess their complete text.
Stage 5: Final Inclusion
Identify the final set of primary studies used for evidence synthesis.

Prepare a PRISMA 2020 flow diagram showing the actual numbers at every stage.

The official PRISMA templates provide fields for records identified, records removed before
screening, records screened, reports assessed, reports excluded and reasons for exclusion, and
studies finally included.

All values in your PRISMA diagram must be traceable to your search and screening records.

12. Maintain a Search and Screening Log
Maintain a complete record of your SLR process.

At minimum, record:

Study ID

Database

Title

Year

Duplicate?  Title/

Abstract
Decision

Full-Text
Decision

Exclusion
Reason

Final
Status

This record must be submitted as supporting evidence.

13. Quality Assessment
Develop a suitable quality-assessment checklist for evaluating the final candidate studies.

Possible criteria include:

Is the proposed methodology sufficiently described?
Is the experimental setup appropriate?

-  Are the research objectives clearly defined?
-
-
-  Are hardware/software configurations described?
-  Are workloads or datasets adequately explained?
-  Are appropriate evaluation metrics used?
Is the comparison with baselines fair?
-
-  Are limitations or threats to validity discussed?
-  Are conclusions supported by evidence?
-

Is sufficient information provided to understand or reproduce the experiment?

Develop a scoring scheme and justify it.

Do not automatically treat every included paper as equally reliable.

14. Data Extraction
Develop a structured data-extraction form.

Depending on the topic, consider extracting:

Category

Possible Data

Bibliographic information

Authors, year, venue

Approach

Environment

Hardware

Workload

Baseline

Performance

Resource usage

Algorithm/mechanism/policy

OS, kernel, platform

CPU, memory, storage, accelerator

Application/workload characteristics

Compared techniques

Throughput, latency, execution time

CPU, memory, storage

Category

Scalability

Energy

Reliability

Security

Overhead

Advantages

Limitations

Trade-offs

Possible Data

Cores, users, processes, nodes

Power/energy measurements

Failure/recovery characteristics

Protection/isolation properties

Runtime or implementation cost

Reported strengths

Reported weaknesses

Conflicting engineering requirements

Modify the extraction form according to your assigned problem.

15. Develop a Taxonomy of Existing Approaches
Do not structure your review as:

-  Paper 1 did this.
-  Paper 2 did this.
-  Paper 3 did this.

Instead, classify studies according to meaningful technical categories.

Develop a taxonomy of the major solution approaches and organize the literature around those
categories.

Your taxonomy should help answer questions such as:

-  What major categories of solutions exist?
-  How do they differ?
-  Which assumptions do they make?
-  Which problems do they solve?
-  Under what conditions are they appropriate?

16. Comparative Analysis
Develop one or more evidence matrices comparing approaches using common criteria.

For example:

Approach

Performance

Latency

Resource
Overhead

Scalability

Security  Limitations

Suitable
Conditions

The actual comparison dimensions must be selected according to your topic.

Simple counting of how many papers use a technique is insufficient.

You must analyze what the research evidence says about the technique.

17. Analyze Engineering Trade-offs
This is a major requirement of the CEP.

Identify the conflicting engineering requirements associated with your problem.

Examples include:

throughput vs. latency;

fairness vs. throughput;
security vs. performance overhead;
resource utilization vs. isolation;

-
-  performance vs. energy consumption;
-
-
-
-  memory savings vs. CPU cost;
reliability vs. performance;
-
scalability vs. implementation complexity;
-
responsiveness vs. power consumption;
-
locality vs. load balancing.
-

Explain how each competing solution handles these trade-offs.

18. Analyze Conflicting Evidence
You are expected to identify situations where published studies reach different conclusions.

For example:

-  Study A reports that an approach improves performance.
-  Study B reports little improvement.
-  Study C reports degradation for another workload.

Do not simply state that the studies disagree.

Investigate possible reasons, including:

-  workload characteristics;
-  hardware differences;
-  number of CPU cores;
-  memory capacity;
-  OS/kernel version;
storage technology;
-
configuration;
-
-  baseline implementation;
-  measurement methodology;
-

evaluation metrics.

Explaining conflicting results is an important part of this CEP.

19. Evidence Synthesis
Synthesize findings across the selected primary studies to answer every RQ.

Your synthesis should identify:

consistently reported findings;
conflicting findings;
effective solutions;
ineffective solutions;

-  dominant approaches;
-
-
-
-
-  operating conditions affecting results;
-  major engineering trade-offs;
-
-  gaps in existing research.

limitations of current solutions;

Tables and figures should be used where they improve the analysis.

20. Evidence-Based Engineering Recommendation
The final objective is to make a defensible engineering recommendation.

Your recommendation must specify:

What should be selected?
Identify the recommended approach or approaches.
Under what conditions?
Specify workload, system, hardware, application, or operating conditions.
Why?
Provide evidence from the SLR.
What benefits are expected?
For example:

lower latency;
improved throughput;
reduced memory usage;

-
-
-
-  better isolation;
lower energy;
-
improved reliability.
-

What must be sacrificed?
Identify the associated engineering cost or disadvantage.
When should an alternative be selected?
Identify conditions where another approach becomes preferable.

A conclusion such as:

�Approach X is the best approach.�

is normally inadequate.

A stronger conclusion would take the following form:

�Approach X is more appropriate for workload category A when latency is the
primary requirement; however, Approach Y is preferable for workload
category B when resource utilization and scalability are prioritized.�

The exact recommendation must emerge from your collected evidence.

21. Research Gaps
Identify unresolved problems such as:

-
-
-

insufficient evaluation;
lack of standardized benchmarks;
limited scalability studies;

inconsistent findings;
inadequate security analysis;
limited evaluation on recent hardware;
lack of real-world experiments;

-
-
-
-
-  unexplored workloads;
limited reproducibility.
-

Research gaps must follow logically from your evidence.

22. Threats to Validity and SLR Limitations
Discuss limitations of your own review, including where applicable:

language restrictions;

-  database-selection bias;
search-string limitations;
-
-  publication bias;
-
-  publication-period restrictions;
-
-
-

reviewer judgment during screening;
inconsistent metrics among studies;
limited availability of full-text papers.

Explain how you attempted to reduce these threats.

23. Mandatory Deliverables
Each group must submit:

1.  Final SLR report
2.  Defined engineering problem
3.  Research objectives
4.  3�5 research questions
5.  SLR protocol
6.  Selected databases and justification
7.  Complete search strings for every database
8.  Inclusion and exclusion criteria
9.  Database-wise search results
10. Search and screening log
11. Duplicate-removal record
12. PRISMA 2020 flow diagram
13. Quality-assessment checklist and scores
14. Final list of included primary studies

15. Data-extraction sheet
16. Taxonomy/classification of approaches
17. Comparative evidence matrix
18. Engineering trade-off analysis
19. Analysis of conflicting evidence
20. Answers to all research questions
21. Evidence-based engineering recommendation
22. Research gaps
23. Threats to validity
24. Complete references
25. Supporting tables/files required to verify the SLR process

24. Suggested Final Report Structure
Your final report should approximately follow this structure:
1. Introduction

-  Background
-  Engineering problem
-  Motivation
-  Objectives
-  Contribution of the review

2. Research Questions
3. Research Methodology
-  SLR protocol
-  Database selection
-  Search strategy
-  Search strings
Inclusion/exclusion criteria
-
-  Study-selection procedure
-  Quality assessment
-  Data extraction
-  Data synthesis

4. PRISMA 2020 Study Selection

-  Search results
-  Screening
-  Eligibility
-  Final studies
-  PRISMA flow diagram

5. Classification/Taxonomy of Existing Approaches
6. Results and Evidence Synthesis
Organized according to the RQs rather than individual papers.

7. Comparative Analysis
8. Engineering Trade-off Analysis
9. Discussion

Interpretation of results

-
-  Conflicting evidence
-  Conditions influencing performance

10. Evidence-Based Engineering Recommendation
11. Research Gaps and Future Research Directions
12. Threats to Validity
13. Conclusion
References
Appendices

-  Search log
-  Quality assessment
-  Data-extraction sheet
-  Supporting evidence

25. Expected Level of Work
This assignment is not a conventional literature review.

A submission that primarily summarizes papers individually will receive limited credit.

A strong submission should demonstrate:

Systematic Evidence Collection ? Critical Evaluation ? Classification ? Comparison ?
Trade-off Analysis ? Synthesis ? Engineering Decision

Your final recommendation should be traceable to evidence contained in the reviewed primary
studies.

26. Research Quality Expectation

every included paper must be traceable;
-
every PRISMA count must be verifiable;
-
-  database searches must be reproducible;
-
-
-
-

inclusion/exclusion decisions must be documented;
evidence should not be fabricated or selectively reported;
claims must be supported by cited studies;
limitations and contradictory evidence must be reported transparently.

The quality of analysis is more important than simply collecting a large number of papers.

27. Final Expected Outcome
At the completion of the CEP, your group should be able to answer:

Based on systematically collected research evidence, what solution or category
of solutions should an engineer select for the assigned Operating Systems
problem under specified conditions, and what technical trade-offs accompany
that decision?

Your answer must be supported by the evidence obtained through your SLR.



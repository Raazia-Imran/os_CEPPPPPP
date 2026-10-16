# OS CEP Group B Task 2 Status and Team Checklist

Checked 16 October 2026 against published main 014b14c. Topic 23 is GPU sharing for multi tenant inference. Task 2 through guideline Heading 14 is not ready for final submission. The evidence framework and preliminary pass exist; final selection, independent checks and synchronized outputs remain open.


## Cycle check

| Requested cycle | Verified standing |

|---|---|

| Cycle 1 Recover and audit | cd3f1e0 and its child 014b14c are on main. Audit and continuation files exist, but cycle2_validation.json does not. This document supplies a fresh audit and continuation checklist; research remains unchanged. |

| Cycle 2 Queries imports and four database coverage | Not complete. Active records cover ACM, IEEE and Springer plus supplementary leads. ScienceDirect remains deferred and unintegrated. Historical query and export reconciliation is unresolved. |

| Earlier Cycle 2 Interim report build | Partially published. main.tex has Sections 1–22 and 41 analysis statements, but report.pdf is still the 24 page Heading 14 build. The 19 sheet workbook lacks the new analysis views. A builder or source file is not proof of a completed build. |


## Verified evidence baseline

| Measure | Current value |

|---|---|

| Occurrences and source split | 2,291 = ACM 1,582 + IEEE 102 + Springer 587 + supplementary 20 |

| Applied duplicate links and canonical records | 44 links; 2,247 records; manifest sum and record IDs reconcile |

| Preliminary recommendations | 1,181 exclude + 1,066 retain or uncertain = 2,247; none awaiting first recommendation |

| Final screening and inclusion | All 2,247 final decisions pending; final included count unknown |

| Full text QA and extraction | 5 bounded report checks; 5 preliminary QA forms and 50 Q1–Q10 items; 5 study forms and 26 outcomes |

| Validation and citation work | 1,066 candidate checks; 127 sampled exclusion checks; 10 citation events |

All 81 import manifest hashes match the preserved source files. The submitted protocol matches the uploaded protocol byte for byte. These checks establish integrity, not search completeness or final eligibility.


## Heading 1 to 7 requirements audit


### 1 Background

Prepared. Required: Explain shared GPU inference, context and competing requirements.

Evidence and remaining work: Protocol and report Section 1; check final wording against evidence.


### 2 Engineering problem

Prepared. Required: Define one device scope, tenants, alternatives, constraints and conditional choice.

Evidence and remaining work: Protocol and report Section 2; keep local contrasts separate from cluster results.


### 3 Objective

Prepared. Required: State the decision objective and utilization latency isolation focus.

Evidence and remaining work: Protocol and report Section 3; retain the approved scope.


### 4 SLR methodology

Partial execution. Required: Describe reproducible protocol based review and PRISMA reporting.

Evidence and remaining work: Protocol and amendments exist; complete recorded review actions before claiming execution.


### 5 Required activities

Prepared with checks open. Required: Problem definition, preliminary investigation, terminology, competing reviews and five RQs.

Evidence and remaining work: RQs are present; verify novelty against relevant reviews and retain a citation linked comparison.


### 6 SLR protocol

Prepared. Required: Preserve all 12 protocol elements and justified later amendments.

Evidence and remaining work: task1/submitted_protocol.pdf unchanged; evidence/protocol_amendments.md records deviations.


### 7 Academic databases

Partial. Required: Justify preferably four suitable NED resources and actual coverage.

Evidence and remaining work: ACM plus shared IEEE and Springer active. ScienceDirect is staged; complete and reconcile it or explicitly justify the coverage deviation.

Prepared means the content or plan exists. It does not certify that all review actions were completed. The guideline prefers four databases; the submitted protocol specifically plans four, so any departure must remain explicit.


## Heading 8 to 14 requirements audit


### 8 Search strategy

Partial. Required: Provide keyword and database query tables with exact executed strings, fields, filters, dates, hits and exports.

Evidence and remaining work: planned_queries.csv, search_runs.csv, shared logs and import_manifest.csv; reconcile 79 ACM files, overlapping masters and reported totals. Check planned serving synonyms and older MPS lanes.


### 9 Literature period

Partial. Required: State actual cutoff and justified older exceptions.

Evidence and remaining work: Protocol and report Section 9; verify publication dates and distinguish shared 11 October and ACM reported 14 October coverage.


### 10 Inclusion and exclusion

Partial. Required: Provide criteria tables and record keyed title abstract and full text decisions with reasons.

Evidence and remaining work: screening.csv, title_votes.csv, fulltext_criteria.csv; independent votes and adjudication pending. Snippets are not full abstracts.


### 11 PRISMA 2020

Interim diagram exists. Required: Show identification, duplicate removal, screening, retrieval, full text rejection reasons, eligible reports and unique studies.

Evidence and remaining work: prisma_counts.json and prisma_flow.pdf; current flow labels final stages pending. Replace with final reconciled flow only after actual decisions.


### 12 Search and screening log

Partial. Required: Submit Study ID, database, title, year, duplicate status, title abstract decision, full text decision, exclusion reason and final status.

Evidence and remaining work: Records, duplicate links, votes, search logs and workbook exist. Complete missing provenance, second votes and final decisions.


### 13 Quality assessment

Partial. Required: Use Group B Q1–Q10, scores 0–2, rationales and anchors; preserve justified N/A and applicable maximum.

Evidence and remaining work: quality.csv has 50 items across five reports. Independently verify and expand to final candidates. Below 60 percent is a sensitivity analysis, not an automatic exclusion.


### 14 Data extraction

Partial. Required: Provide study identity and outcome tables with conditions, units, baseline, page or figure, missingness, limits and trade offs.

Evidence and remaining work: study_extraction_form.csv and extraction.csv contain five forms and 26 outcomes. Verify all anchors and expand to every eligible study; outcome rows are not study counts.


## Work split and exact return files

Suggested allocation follows the existing project handoff. Teammates should return completed rows keyed to existing IDs, not screenshots or a statement that everything was checked. Preserve their independent judgment before reconciliation.

- Eshaal: return existing ACM decisions matched to record IDs. Check the 148 priority candidates first, then the remaining assigned candidate rows and 127 sampled exclusions. Record include for full text, exclude with criterion and reason, or uncertain; add reviewer and date. Return the completed human_validation_queue.csv and exclusion_validation_sample.csv, or equivalent workbook tabs.

- Eshaal: reconcile the historical ACM log against the 79 numbered exports. Return a run to export mapping with exact accepted query, field, collection, filters, date and timezone, displayed and exported counts, filename and operator. Leave unknown historical details unknown.

- Rameen: independently check the five priority reports against IC1–IC6, all 26 extracted outcomes and all 50 QA items. Record exact page, table or figure and corrections. Return report_validation_queue.csv, fulltext_criteria.csv, extraction.csv and quality.csv with independent fields completed. Resolve PipeSwitch scope and the REEF conference versus journal relationship.

- Raazia with automation: reconcile returned votes, adjudicate differences, resolve the five remaining paper identity pairs and approved duplicate proposals, expand retrieval QA and extraction, and regenerate record report study accounting. Do not count a source as eligible merely because Group A accepted it.


## Automation checklist for the next authorized work

- Compare staged exports by hash and DOI or title; preserve originals and do not blindly add overlapping master files or the 68 staged identifiers.

- Prepare source located first review QA and extraction for additional candidates and trace every change to IDs. Humans independently check the required votes and headline results.

- Rebuild the recovered PDF, separate interim flow and workbook without rerunning destructive legacy import or screening scripts. Follow task2/report/BUILD.md.

- Validate the output files, citation resolution, spreadsheet formulas and counts; visually inspect final pages and sheet previews; create a truthful cycle2_validation.json only after the checks run.

- For submission through Heading 14, reconcile final decisions and retrieval reasons, update the flow and included study table, and attach the workbook and underlying logs. The guideline target of 15–20 final primary studies is not established by five report checks. Do not force eligibility to meet a quota.


## Continuation and submission gate

Next step is output synchronization and search provenance reconciliation, followed by wider eligibility QA and extraction. No new searches, imports, screening, QA scoring or report rebuilds were performed in this status review. Resume from the newest remote main and preserve newer valid work.

The attached query reports and query workbooks describe Group A checkpoints; their 21 provisional studies and 0–1 scores are not Group B results. The data extraction sample concerns GPU memory oversubscription and uses QA1–QA8; use its layout only. The uploaded Group B workbook is older, with 20 QA rows and six outcomes. Current registers supersede those copies.

Both supplied Drive folders were listed. One contains 79 ACM bibliography files; the other leads to 24 items including two ACM masters, a search log and ScienceDirect RIS batches. Listing establishes availability only; no new file contents were imported in this audit.

The instructor guideline gives a final CEP report format of 20–30 pages and font 12, IEEE references, and a final primary study target of 15–20. A separate Task 2 marking sheet was not supplied. Page count alone does not establish completion through Heading 14.

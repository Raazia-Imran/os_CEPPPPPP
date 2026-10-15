# Group A Task 2: the simple, complete checklist

**Topic:** GPU sharing for multi-tenant inference. **Use the submitted** `report/SLR_protocol.pdf` **and its Group A amendments as the rules.** This is the search, selection, appraisal and extraction report that comes before the final CEP paper. The instructor's separate Task 2 marking sheet has not been supplied here, so verify its exact cutoff and deadline before submission.

## What the words mean

- A **search hit/record** is one item shown by a database. It is not a paper we have accepted or read. The same paper can appear in several searches.
- **Deduplication** links repeated hits and keeps one copy for screening without losing where it came from.
- **Screening** checks the title/abstract, then the available full paper, against the protocol. Every rejection needs a stage and reason. An inaccessible paper remains *pending retrieval*; it is not a full-text rejection.
- An **included study** is a unique, eligible piece of research after full-text checking. Two publications of the same experiment count as one study.
- **PRISMA** is a flow of the actual numbers through search, duplicates, screening, retrieval, exclusion and inclusion. It does not generate the numbers for us.
- **Extraction** copies the facts we need from each eligible study into a table, with its page/table/figure and conditions. Later, the final CEP paper uses that table to compare mechanisms and answer the RQs.

## Phase 1: lock the rules and collect search results

- [x] Read the submitted protocol and record the approved changes (Group A, 11 October 2026 cutoff, one AI reviewer). Keep the original protocol intact.
- [x] Search IEEE Xplore and Springer Nature Link with the recorded queries and retain 102 + 587 displayed occurrences. **Limit:** prior runs captured public result-page metadata, not original publisher exports; their time-of-day was not recorded.
- [ ] Finish ACM Digital Library and ScienceDirect using the protocol's master Boolean query, or the four family queries if the master is rejected. Record *exact* text accepted by the site, collection/field, filters, date/time, URL, displayed total, every export filename, and the number actually exported. See `groups/group-a/evidence/search_runs.csv`.
- [ ] Verify that all result pages were exported. The four newly supplied ScienceDirect RIS files contain 25 records each, but their search log has unfilled fields. Keep them as a **partial incoming batch** until the site totals, fields, query strings, timestamps and any missing pages are known. Do not call them complete runs or silently replace the missing counts with 25.
- [ ] If a website denies access, record the failed attempt and unknown hit count. Use Google Scholar only for supplementary discovery or citation chasing, not to stand in for the missing formal database.

**Who does what:** I can inspect public pages, import/export records, maintain the logs, check metadata and prepare decisions. Only the VPN-connected laptop can prove subscription access that this workspace does not inherit. The manual action is to export full result lists and the short run log, not to read hundreds of PDFs. No new PDF downloads are requested now.

## Phase 2: clean and decide

- [ ] Import all original records, preserve their database/run and immutable ID, then link DOI/title duplicates. Count raw occurrences and unique records separately.
- [ ] Screen each unique title/abstract against the protocol. Record `include for full-text check`, `exclude` plus reason, or `uncertain`. A paper about MIG welding or MPS meaning microplastics is a false match, not GPU sharing evidence.
- [ ] Retrieve promising full texts through open publisher/author versions first. Keep paywalled candidates pending instead of guessing their findings. The user's earlier limit was ten requested downloads; six supplied conversions have already been assessed, and no further downloads are currently requested.
- [ ] Apply the protocol's full-text criteria (especially concurrent inference tenants on one physical GPU, or a separately extractable local contrast). Assign one primary `E1`–`E10` code to each assessed rejection. Link conference/journal versions to one study.
- [ ] Check the AI decisions and a sample of title exclusions with a human teammate if possible. The existing report correctly says there was one AI reviewer; do not later describe it as independent dual screening unless that actually happens.

## Phase 3: judge and capture the evidence

- [ ] Score every included study using the protocol's ten-question quality checklist. Keep the score and a source-located explanation; a score alone is not enough.
- [ ] Extract each measured outcome with GPU model, software/runtime, model and co-tenant mix, batch/request load, baseline, metric/units, latency quantile, figure/table/page, limitations and whether isolation was tested or just claimed. Mark missing data as `not reported` or `not extracted`, as appropriate; never enter a guessed zero.
- [ ] Keep the `query_references.bib` bibliography for the included primary reports in sync with the included-study list. Contextual surveys and vendor documentation must not be counted as primary studies.
- [ ] Do citation chasing from eligible papers and record the seed paper, direction (references or citing papers), date, source, discovered ID and screening decision. This is a separate discovery route, not an unlogged increase to database totals.

## Phase 4: assemble and submit Task 2

- [ ] Recalculate the PRISMA flow from the logs: database records, duplicates removed, records screened/excluded, reports sought/not retrieved/assessed, full-text rejections by reason, eligible reports, and **unique** studies. Explain any incomplete database coverage. Do not issue a final four-database PRISMA diagram while ACM/ScienceDirect are unknown.
- [ ] Update `report/query_report.tex`, compile `report/query_report.pdf`, and attach or link the evidence workbook and logs. Report the *executed* search, actual decisions, QA and extraction. Do not turn planned actions into past-tense results.
- [ ] Before submission, open the PDF and check tables, 12-point text, references, citation links, dates, figures, included count and all arithmetic. Validate `groups/group-a/scripts/validate_evidence.py`. Ask a teammate to read the summary and key decisions. The instructor's final CEP page requirement does not automatically establish a separate Task 2 page requirement.

## What the instructor can check through the Data Extraction heading

The assignment guideline's sections 1–14 lead into the final-report deliverables. This table is an audit of the **Task 2 checkpoint**, not a claim that the later research paper is finished. The instructor's separate Task 2 marking sheet was not supplied.

| What must be visible | Current source | State |
|---|---|---|
| Problem, objective, 3–5 RQs, frozen SLR protocol and amendment | Submitted `report/SLR_protocol.pdf`; `groups/group-a/protocol.md` | Prepared |
| Four justified databases; accepted database-specific query text, fields, filters and hit totals | `groups/group-a/evidence/search_runs.csv` | IEEE and Springer logged; ACM unavailable here; ScienceDirect incoming metadata has no run log |
| Dated inclusion/exclusion rules | Group A protocol §§6–8 | Prepared |
| Every imported record's title/abstract decision and rejection reason | `studies.csv`, `rejected.csv`; incoming ScienceDirect ledger separately | Captured subset done; four-database set incomplete |
| Deduplication and linked versions | `duplicates.csv`, `version_links.csv`; incoming duplicate IDs separately | Captured subset done; new exports not yet reconciled |
| Actual PRISMA record → report → study counts, including not retrieved | `prisma_counts.json`, search/decision logs | Intermediate subset only |
| Quality rubric and score with evidence for each included study | Protocol §10 and `quality.csv` | Initial scores done; verify remaining anchors |
| List of unique eligible primary studies and accurate citations | `accepted.csv`, `report/query_references.bib` | 21 provisional, subject to full coverage/eligibility audit |
| Study-level extraction sheet with exact source locations and missingness | `extraction.csv`, companion rows, source assessments | Started; technical fields and some outcome anchors unfinished |
| LaTeX report, readable PDF, evidence workbook and underlying logs | `report/query_report.tex`, `.pdf`, `.xlsx`; evidence directory | Reviewable checkpoint; regenerate after verified changes |

The guideline's later taxonomy, trade-offs, conflicting evidence, answers to all RQs and final recommendation belong to the **final CEP report**. We can draft them as evidence matures, but they cannot be declared complete from this shortlisting checkpoint.

### Current checkpoint, not the final answer

The merged repository reports **689 formal occurrences** from IEEE and Springer, **10 duplicate occurrences**, **20 selected supplementary candidates**, **21 provisionally included unique studies**, **28 assessed full texts**, **7 full-text exclusions**, **575 earlier-stage exclusions**, and **96 pending retrieval cases**. These counts describe the captured subset. ACM and ScienceDirect totals remain **unknown**. Four user-supplied ScienceDirect RIS files separately contain **100 entries**, including **10 repeats within the batch**; the separate incoming ledger has preliminary reasons for all 90 distinct items and one author-manuscript full-text check. The current 14-page search/selection report is a useful reviewed checkpoint; it is not yet a completed four-database Task 2 search. The instructor's 15–20 target concerns *final unique primary studies*, not 600 hits. More than 20 currently qualify provisionally; a final included set needs transparent coverage and eligibility review, never a quota-based cut.

### Software in one sentence

Use the **publisher websites in a browser** to search and export citations (the VPN-connected laptop if needed), the **CSV/Excel workbook** to record search and screening decisions, **PRISMA 2020's official flow diagram** to display reconciled counts, and **LaTeX/Overleaf** to edit the report and `.bib` bibliography. Zotero or Rayyan can help manage citations or reviewer votes, but neither is required and neither decides eligibility for us.

**Submission gate:** Every number in the PDF must lead back to a recorded database run, record decision or study row. Every extracted factual claim must lead back to an accessible paper and page/table/figure. Remaining access and coverage gaps must be stated openly.

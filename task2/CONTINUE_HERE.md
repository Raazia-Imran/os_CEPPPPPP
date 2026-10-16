# Cycle 5 screening batch: first automated triage covers all 4,078 records

Added1,591 automated recommendations:91 explicit exclusion proposals and1,500 uncertain. Current first-pass split1,441 exclude and2,637 retain/uncertain. This is not complete abstract verification or final selection; all final decisions remain pending. Original2,487 recommendations preserved. Nine assessed reports,90 QA items and34 outcomes unchanged while new full texts are assessed. User authorizes AI-only continuation; see protocol_amendments.md. Workbook/report rebuilding follows source batches.

# Cycle 4 initial QA outputs and workbook synchronized

Published QA-table checkpoint: 1e75a465d922a66cca2ff0bdf17f04f6abe0d2b4. Current artifacts: 47-sheet public/private review workbooks and 35-page interim QA/extraction appendix; 9 provisional reports, 90 initial QA items, 34 outcomes. All original workbook cells/formulas preserved; all QA totals and saved caches checked. Drive workbook replacement verified. No new final eligibility or human validation. Twenty QA page mappings, two N/A calibrations, independent checks and wider source coverage remain open. Active first recommendations remain 2,487/4,078; 1,591 pending. Continue with task2/qa/CONTINUATION.md and task2/NEXT_24_HOURS.md. Final SLR report/PRISMA remain historical/pending.

# Cycle 4 QA tables prepared; source checks remain open

Nine assessed provisional reports have 90 Q1-Q10 rows and 34 outcomes. Derived QA matrix, totals, checklist, rationales and follow-up tasks reconcile to unchanged source registers. Twenty legacy QA items need printed PDF-page mapping; two N/A judgments require calibration; independent scoring remains pending for all reports. Incoming Claude opinions preserved separately: 1,831 rows; 50 disagreements among 240 overlaps. Active screening remains 2,487/4,078 preliminary recommendations (61.0%), with 1,591 awaiting first recommendation. See task2/qa and task2/NEXT_24_HOURS.md. Current QA/extraction appendix and workbook synchronization are being verified; final SLR PDF/PRISMA remain historical/pending.

# Continue Cycle 3 from the saved batches

Read task2/CYCLE3_PROGRESS.md and evidence/cycle3_validation.json. Preserve2487 preliminary recommendations,90 QA rows,34 outcomes and9 report forms. First recommendations still pending for1591 records. Next candidate IDs/DOIs are in evidence/cycle3_next_batch.csv;1137 retain/uncertain records need the remaining retrieval/eligibility work. Do not rerun import scripts or overwrite real human returns. Source PDFs stay private. Final inclusion/PRISMA remain pending; the existing report PDF is historical. Continue Cycle 3 only when requested; do not begin Cycle4 automatically.

# Cycle 3 in progress

Resume source assessments for Paella, Orion, GSLICE and Clockwork. Do not rerun imports or overwrite baseline votes. Raw sources stay private. Save each batch; update registers and full/private and public workbook views at the end. All independent human votes remain pending.

# Next: Cycle 3, only on request

Read task2/PUBLIC_CHECKPOINT.md and evidence/workbook_refresh_validation.json first. The workbook is current for the reconciled queue; the report PDF is not. Original new RIS sources and the full abstract-bearing workbook are private in supplied Drive. Public records/workbook omit abstracts intentionally. Retrieve and hash-check originals before raw-source validation. Do not rerun old frozen-baseline report validators against expanded counts. Preserve all existing recommendations and real reviewer work.

## Preserved published recovery audit

# Continue after recovery/audit Cycle 1

Start with task2/recovery_audit/README.md and receipt.json. Inspected main cb8251a has a 24-page report and 18-sheet workbook; do not confuse these with local recovery 1aa970c (38 pages/27 sheets). cycle2_validation.json is absent from inspected main. Source Sections 1-22 do not prove the compiled report is current. All 2247 final decisions remain pending. Next, when requested, perform Cycle 2 queries/imports/four-database coverage; do not start Cycle 3 automatically. Older build commands below are historical and must not overwrite the recovery. Preserve the new cb8251a team checklist and submitted protocol.

---
Historical notes follow; the latest audit above controls publication status.

# Continue after Cycle 2

Use the newest STATUS.md checkpoint and evidence/cycle2_validation.json. The report through22is an interim draft; do not restart screening or treat recommendations as final decisions. Cycle1 canonical counts remain frozen. First recommendations:2,247complete;1,181exclude;1,066retain/uncertain. Final included studies:pending.

Next: follow COMPLETION_AND_TEAM.md for actual human screening/source/QA validation, expand full-text extraction beyond5reports, reconcile search/version gaps and only then finalize studies and PRISMA. Rebuild Cycle2 using build_cycle2_evidence.py,build_cycle2_references.py andbuild_cycle2_report.py after justified evidence updates. The references builder uses evidence/cycle2_reference_metadata.json as its durable verification cache; reverify metadata if citation identities change. Do not run cycle1_finalize.py or legacy import/checkpoint scripts on the completed queue.

## Historical Cycle1 continuation

# Continue after Cycle 1

Use STATUS.md for current measured counts. The source CSV/JSON registers are authoritative; regenerate workbook/report after any decision changes. Run `python3 scripts/cycle1_screen.py --refresh`, then rebuild outputs with the scripts saved in this repository. Do not rerun the older import/advance_review builders over the current registers: they initialize or overwrite earlier state.

## Completed preparation

All2,247 active canonical records have first recommendations. Cycle1 added1,447. Current split:1,181 preliminary exclusions and1,066 retain/uncertain; no final decision is inferred. All41 version pairs have a detailed audit. There are5 bounded source checks,50 QA item rows across5 reports,26 outcome rows,5 expanded study forms and10 targeted citation events. Report/workbook remain interim evidence outputs through heading14. No final CEP synthesis has been written.

## Next, in order

1. Eshaal: align already completed human ACM decisions with immutable record IDs. Preserve that existing work and do not duplicate it. Reconcile the recovered search log with79 numbered exports; the two additional masters contain829+1000 overlapping entries and do not reproduce the claimed1603 total. The68 unmatched candidate identifiers remain staged outside active counts until a justified import/reconciliation checkpoint.
2. Validate `evidence/human_validation_queue.csv` (all1066 candidate records) and `evidence/exclusion_validation_sample.csv` (127 sampled exclusions). Priority1 items come first. Review independently with first-vote columns hidden where practical. A sample is not already checked.
3. Rameen: use `evidence/report_validation_queue.csv` for5 priority reports. Check26 outcome IDs (GB-O001 onward),50 Q1-Q10 items and30 criterion-specific IC1-IC6 rows. Preserve your own votes/scores before comparing. Record anchors,actual dates and any corrections.
4. Raazia: reconcile3 verified identity proposals and3 proposed companion-report relationships;resolve5 unresolved paper identities. Apply justified links in a separate count-reconciled checkpoint; current44/2247 accounting is unchanged.
5. Extend full-text checks,QA and complete extraction to all provisionally eligible reports. Use not extracted for unchecked fields and not reported only after checking. Expand backward/forward searches and log each event separately.
6. Only after actual eligibility validation: freeze report-to-study mapping,derive final PRISMA and prepare Cycle2 taxonomy/comparisons/RQ synthesis/engineering recommendation.

## Rebuild and verify

`python3 scripts/cycle1_finalize.py` refreshes metadata-status labels,validation tasks and count checks. `python3 scripts/build_cycle1_report.py` writes LaTeX/flow from current registers. Compile main.tex with BibTeX and two additional LaTeX passes from task2/report;compile prisma_flow.tex separately. The workbook uses scripts/build_workbook.mjs with the bundled artifact runtime and OS_CEP_ROOT set to the absolute repository path. Render/check outputs before publishing.

Original raw files and submitted protocol must remain byte-for-byte unchanged. Final included studies stays pending until genuinely validated. ScienceDirect remains deferred. Keep private source PDFs and access credentials out of this public repository. Publish small checkpoints with verified remote commits;record preceding commit hashes/times in STATUS.md.

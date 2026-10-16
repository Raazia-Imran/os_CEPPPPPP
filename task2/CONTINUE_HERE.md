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

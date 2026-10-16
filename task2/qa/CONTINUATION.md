# Current QA checkpoint and continuation

The current nine-report appendix, QA tables and 47-sheet workbook supersede the seven-report handoff output. This cycle audited and presented existing first-review evidence; it did not claim a fresh full-source reappraisal, new final decisions or human validation. Source scores, source outcomes and active screening were unchanged.

## Completed

- Ten Q1-Q10 items per assessed provisional report: 90 items across 9 reports, with matrix, totals, rationales, checklist and source-check queue.
- Thirty-four outcome rows and nine study forms printed in the current 35-page QA/extraction appendix. This is supporting evidence, not the final SLR report.
- Incoming 1,831 AI opinions preserved separately. Of 240 overlapping recommendations, 190 agree broadly and 50 disagree. The other 1,591 were not previously recommended in the active register. No incoming title-only opinion was silently promoted into a final decision.
- Public and private workbooks each have 47 sheets. All populated cells/formulas in the 43 original sheets were preserved; four QA/reconciliation views and Summary notes were added. No saved error cells; all nine formula totals match the register. A temporary score change propagated correctly and was restored. Native Excel opening was not performed.
- Existing full workbook replaced in Drive at the same file ID; metadata readback confirmed size 5,627,418 bytes and modified time 2026-10-16T12:06:25.368Z. Full abstracts remain in the private copy; public copy has none.

## Unresolved

All 90 independent QA scores and reconciled scores are blank. Twenty legacy items need exact printed PDF-page mapping; VastPipe Q7 and Paella Q9 need actual N/A calibration. Resolve PipeSwitch scope and REEF conference/journal relationship. Continue full-text/eligibility coverage beyond nine provisional reports; complete unextracted fields and independently verify numerical outcomes. No currently assessed report lacks initial QA, but this does not establish QA coverage for unassessed candidates.

Active baseline remains 4,189 occurrences minus 111 links equals 4,078 canonical records; 2,487 active preliminary recommendations (61.0%) and 1,591 pending first recommendations. Final included reports/studies remain pending. Do not count provisional report forms or outcomes as unique studies. The final SLR PDF and final-stage PRISMA were not regenerated in this cycle.

## Rebuild without changing research decisions

1. Run `python3 scripts/cycle4_quality.py` to derive QA CSVs and ignored workbook_update.json from the authoritative registers and preserved incoming opinions.
2. Build the appendix with the bundled Python running `scripts/build_cycle4_appendix.py`; render and inspect all PDF pages.
3. For the current workbook, copy `scripts/update_cycle4_workbook.mjs` to a conversation-specific temporary directory with node_modules linked to the bundled runtime. Set OS_CEP_ROOT, OS_CEP_WORKBOOK and OS_CEP_PREVIEW_PREFIX. Run with the primary Node runtime and sufficient heap (6 GB worked). Repeat on the separate private workbook, preserving abstract cells. The updater targets the four owned QA/reconciliation tabs and Summary additions.
4. If rebuilding the entire older 43-sheet baseline with build_workbook.mjs, run the Cycle 4 updater afterwards to restore the four QA/reconciliation views. The generic builder alone does not yet contain these additions.
5. Validate saved files with scripts/validate_cycle4_artifacts.py and the original workbook baselines used for comparison; the current script defaults to /tmp/c4-wb baseline snapshots. Recheck register hashes, PDF IDs, workbook values/formulas, rendered views and publication.

Read task2/NEXT_24_HOURS.md. Next work: finish prioritized Cycle 3 full-text screening while humans independently check Cycle 4 evidence; then expand extraction and regenerate cross-study synthesis/report from genuine decisions. Do not begin another cycle automatically.

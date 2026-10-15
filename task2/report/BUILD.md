# Build current outputs

From the repository root:

1. `python scripts/import_shared.py` rebuilds the original import and resets the work queue. Do not run this over unsaved reviewer edits. Preserve independent vote files separately and reapply them by record ID.
2. `python scripts/advance_review.py` reproduces this checkpoint's bounded first-review events, source checks and extraction/QA drafts. It is not a general automated full-text screener.
3. `python scripts/build_checkpoint.py` rebuilds report sources and workbook input from registers.
4. In `task2/report`, run `pdflatex main.tex`, `bibtex main`, then `pdflatex main.tex` twice; copy main.pdf to report.pdf. Run `pdflatex prisma_flow.tex` for the standalone flow.
5. The saved `scripts/build_workbook.mjs` uses the Codex bundled artifact runtime and `task2/tracker/workbook_input.json`. Set `OS_CEP_ROOT` to this repository root before running it from a temporary directory linked to the bundled node modules. Preserve the required artifact-tool dependency.

After changes, verify counts, source anchors, references, PDF layout, workbook formulas and image previews. The report is explicitly interim until final screening and independent review are closed.

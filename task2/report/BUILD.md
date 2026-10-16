# Resume and build Cycle 2

Read STATUS.md and task2/CONTINUE_HERE.md first. CSV/JSON registers control outputs; preserve Task 1 and raw imports.

1. Run `python3 scripts/build_cycle2_input.py` from the repository root. It recreates the ignored workbook input without screening, importing or resetting evidence.
2. Run `python3 scripts/build_cycle2_report.py` to regenerate the interim report and accounting flow.
3. From `task2/report`, run `pdflatex -interaction=nonstopmode -halt-on-error -jobname=report main.tex`, `bibtex report`, then the same LaTeX command twice. Compile `prisma_flow.tex` separately.
4. Run `scripts/build_workbook.mjs` with the bundled artifact runtime from a temporary directory linked to its node modules. Set `OS_CEP_ROOT` to the absolute repository path and create `OS_CEP_PREVIEW_DIR` first.
5. Run `python3 scripts/validate_cycle2.py`. Inspect rendered PDF pages and worksheet previews, then record actual visual results before publishing.

Analysis and references are already recovered. Rerun `build_cycle2_evidence.py` only after justified evidence changes, and `build_cycle2_references.py` only when bibliographic metadata needs regeneration. Cached historical checks must retain their verification dates.

Do not run legacy import, screening, finalize or checkpoint scripts merely to rebuild outputs: they can replace current state. Final screening, independent Q1-Q10 appraisal/extraction and inclusion remain pending.

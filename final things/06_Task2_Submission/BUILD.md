# Build the complete Task 2 report

Use a TeX Live installation with pdfLaTeX and BibTeX. Keep these files in the same directory:

- main.tex
- references.bib
- Submitted_Task1_Protocol.pdf

Run from that directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The resulting `main.pdf` is the complete document, delivered here as `GroupB_Task2_Through14.pdf`. No shell escape, network connection, Python scripts or CSV imports are needed to compile it. The source includes every displayed table row. Standard packages include geometry, lmodern, microtype, booktabs, longtable, array, graphicx, enumitem, xcolor, fancyhdr, tikz, pdflscape, pdfpages, amsmath, amssymb and hyperref; required TikZ libraries are declared in the source.

The core report occupies the first 25 PDF pages (cover, contents, Headings 1–14 and references). Full log appendices make the electronic document much longer. Main text uses 12-point type; detailed landscape tables use 9-point type. Repeated long values in large logs use reversible V-codes with a complete glossary; CSVs and the workbook retain original values.

The embedded protocol is the original submitted file. Its pagination and content are preserved. Later CEP Sections 15–22 are not part of this Task 2 build.

Repository regeneration, after the source registers have been updated, uses `scripts/prepare_task2_consolidated.py`, `scripts/build_task2_consolidated.py` and `scripts/build_task2_workbook.mjs`. The workbook builder requires the artifact-tool runtime. Do not run older initialization/import scripts or replace final-stage pending values with preliminary triage counts.

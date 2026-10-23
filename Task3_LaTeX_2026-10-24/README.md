# Task 3 LaTeX project

This self-contained project produces the 30-study/31-report first draft. Its evidence snapshot is dated 23 October; this portable folder was packaged on 24 October. The report explicitly retains 320 deferred eligibility/identity records.

## Overleaf
1. Download the separate LaTeX ZIP.
2. Open Overleaf, select New Project, then Upload Project and choose that ZIP.
3. Select main.tex as the main document and pdfLaTeX as compiler.
4. Click Recompile. Download the PDF after references and contents settle.

## Windows with MiKTeX or TeX Live
Install a LaTeX distribution first. Extract the ZIP, open a terminal in this folder and run the four commands below. The PowerShell helper build.ps1 runs the same sequence if your local execution policy permits scripts.

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

On Linux or macOS with TeX Live, run sh build.sh. No private reading PDF or workbook is required to compile the report. figures/Frozen_PRISMA.pdf is a generated historical review diagram, not a licensed research paper.

## Files to edit
main.tex contains the cover, abstract and document setup. body.tex contains the thirteen main sections and inputs the comparison files. taxonomy.tex, comparisons.tex, recommendations.tex and gaps.tex hold the corresponding tables and extensions. validity.tex holds the validity table. corpus.tex holds the study catalogue. counts.tex holds the selection table. appendices.tex holds detailed evidence cards. references.bib holds bibliography entries.

Edit citations in references.bib and cite their keys in the relevant TeX file. Rebuild the PDF after every accepted change. The report PDF is generated from LaTeX; editing Word does not update it. Send Word review comments to Raazia for application to these sources. Changing source code alone never establishes a new screening or eligibility decision.

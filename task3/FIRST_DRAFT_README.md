# Task 3 first draft submission

Open report/main.pdf to read the 107-page draft. Open workbook/CEP_Task3_Evidence_Workbook.xlsx for the 27-tab evidence workbook. report/CEP_Task3_First_Draft.docx is the editable Word companion. FIRST_DRAFT_CHECKLIST.pdf shows completed, partial and remaining tasks.

## Build LaTeX
From the task3/report directory run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Keep the folder structure intact. All included TeX tables and references.bib are required. The PRISMA figure is in task3/baseline. The protocol is in task1/submitted_protocol.pdf at package root. Instructor guidance is in docs/guidelines.md and task3/baseline/Instructor_Guideline.pdf.

## Draft boundaries
The supplied bounded corpus contains 20 studies represented by 21 reports. There are 559 retained records without source assessment, three missing reading PDFs, unresolved source-version checks and no independent item-level signoff. Draft sections and matrices exist; their presence is not proof of complete scientific verification. Page count does not establish quality or guarantee marks.

Third-party reading copies are excluded from this public-repository package. Source URLs and retrieval hashes remain in task3/papers. Hong et al. DOI 10.1145/3068281 is a journal survey used as a structural benchmark, not a primary study or evidence of novelty.

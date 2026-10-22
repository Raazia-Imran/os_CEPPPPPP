# Task 3: integrated first draft — 22 October 2026

Start with [the main report](report/main.pdf), [master workbook](workbook/CEP_Task3_Evidence_Workbook.xlsx), and [team handover](team/First_Draft_Team_Plan.pdf).

The complete handover ZIP is `team/Task3_Complete_First_Draft.zip`. It supersedes the earlier member-review-only ZIP.

Current source-review coverage: 20 unique studies, 21 report copies (REEF is one study), 200 QA items, 126 included-report inclusion checks, and 52 retained outcomes. The correct InferFair copy is checked and all three member packages are integrated. Sir’s clarified 20-study target is met. No additional three studies are needed merely for the count.

Independent named human source checks remain pending. The 559 retained records have not been advanced to complete eligibility assessment. Historical search-provenance gaps and ParvaGPU final-text equivalence remain explicit limitations. Do not relabel these records exclusions or manufacture votes, abstracts or search events.

## Exact files
- `report/main.pdf`: integrated CEP first draft with audit appendices.
- `report/CEP_Task3_First_Draft.docx`: editable report companion.
- `workbook/CEP_Task3_Evidence_Workbook.xlsx`: current 37-tab master.
- `eshaal/`, `raazia/`, `rameen/`: individual source-review returns.
- `team/First_Draft_Team_Plan.pdf`: headings 15–26 crosswalk, mandatory deliverables and teammate instructions.
- `logs/methodology_corrections.csv`: justified audit resolutions and remaining limitations.
- `logs/Remaining_559_Screening_Queue.csv`: all 559 records, recoverable abstracts, different first/independent reviewers and blank decision fields.
- `logs/publication_receipt.json`: verified remote publication checkpoint; check its timestamp/commit rather than inferring publication from a local file.

## Real teammate return
Rameen independently checks Eshaal’s P001–P007 plus P023; Eshaal checks Raazia’s P008–P014; Raazia checks Rameen’s P015 and P018–P022. Record actual names, times, initial judgments, page/table anchors and disagreements before adjudication. Then review the main CEP draft together.

## Reproducibility and boundaries
The submitted Task1 protocol and frozen Task2 evidence workbook are preserved. Current CSVs and source-review appraisals are separate. Build the report with `python task3/scripts/build_report.py`, then pdflatex/bibtex in `task3/report`; `build_word.py` creates Word from those sources. Workbook authoring scripts use the documented artifact-tool runtime.

Third-party reading PDFs are excluded from Git and the ZIP. Source identities, URLs, hashes and versions are retained. Available search artifacts are included; missing historical archive bytes are explicitly documented, not claimed recovered.

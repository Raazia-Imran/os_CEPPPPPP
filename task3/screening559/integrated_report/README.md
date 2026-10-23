# Integrated first draft 23 October 2026

Use main.pdf, CEP_Task3_Integrated_First_Draft.docx and the matching integrated workbook together. The assessed corpus is 30 unique studies across 31 reports, with 300 QA items, 90 outcome rows and two inherited calculations.

All 559 continuation records have screening decisions. At the first-draft cutoff, 320 advanced records remain deferred for eligibility or report identity. They are retained in Open_Eligibility_Queue.csv and are not exclusions or failed retrievals. The whole-review PRISMA is not final. Historical search provenance and source-version limits remain in the methodology.

Build main.tex with pdflatex, bibtex, then two pdflatex passes. The report builder reads final source registers and the preserved original report. build_word.py derives the editable companion from the compiled citation order. The previous frozen 20-study package remains a versioned backup.

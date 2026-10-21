# Raazia assigned source review

Open Raazia_Assigned_Review.pdf for the17-page review. Raazia_Assigned_Review.docx is editable. Raazia_Source_Review.xlsx contains seven tabs with source identities,42 eligibility assessments,70 QA appraisals,13 checked outcomes, original/reviewed score comparisons and corrections. CSV files provide the same records for merging. Reviewed_References.bib contains the seven reviewed bibliography entries.

The integrated master is ../workbook/CEP_Task3_Evidence_Workbook.xlsx (31 tabs). The updated report is ../report/main.pdf (109 pages), with editable main.tex, included TeX files, references.bib and Word companion in that directory. Frozen baseline files remain in ../baseline. ../logs/reviewed_data.json is the processed overlay used by the report builder.

The source review is attributed to the AI assistant under Raazia's direction. It is not an independent human vote or a local rerun of paper experiments. ParvaGPU numerical checks concern arXivv1; publication identity is confirmed but final-text equivalence is not established. The global559-record coverage limitation is preserved.

## Main findings
All13 retained numerical values were found in the accessed sources. Clockwork page offsets and TVM information, Torpor runtime-mode/recovery descriptions and KRYPTON offered-load context were clarified. Clockwork Q4/Q9 and StreamBox Q4/Q9 each change from1 to2 under the claim-specific protocol; the seven-study sum becomes114/140 rather than110/140. Original scores remain in the review records and frozen baseline.

## Rebuild order
Run build_review_data.py only when the restored GSLICE reading copy and other local reading PDFs are available. It depends on legitimate local reading copies, excluded from Git. It creates the processed overlay. Run build_review_report.py for the personal Word document and eligibility records. Use the bundled document renderer to produce its PDF.

To reconstruct workbooks from scratch, first run ../scripts/build_workbook.mjs to restore the27-tab baseline-derived workbook, then build_review_workbooks.mjs, add_eligibility.mjs and finalize_master.mjs. Do not repeatedly append review tabs to an already integrated workbook. Build the main report using ../scripts/build_report.py, then pdflatex/bibtex/pdflatex/pdflatex in ../report; build_word.py regenerates the Word companion.

Independent team reviewers should record separate actual judgments. Corrections in this folder are review findings for teammate review, not a substitute signature.

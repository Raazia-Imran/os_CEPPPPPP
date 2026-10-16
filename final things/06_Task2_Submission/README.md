# Group B Task 2: start here

Open **GroupB_Task2_Through14.pdf** first. Its first 25 PDF pages contain the cover, contents, Headings 1–14 and references. The remaining pages are the complete research tables, value glossary, amendments and unchanged submitted Task 1 protocol. Use the contents/bookmarks to jump to a table. These appendices are intended for electronic use; printing the full logs is unnecessary.

Open **GroupB_Task2_Workbook.xlsx** for the shorter editable view. Start with Overview, then Paper list. The same report ID joins eligibility, QA and extraction. Outcome rows are measurements, not extra papers. Exact dates are retained when recorded; missing event times are not reconstructed.

## How many papers?

**QA and extraction cover the same 15 reports, GB-P001–GB-P015. There are not 21 final included studies.**

| ID | Short name | Current position |
| --- | --- | --- |
| GB-P001 | VastPipe | Provisional |
| GB-P002 | iGniter | Provisional |
| GB-P003 | gpulets | Provisional |
| GB-P004 | PipeSwitch | Provisional |
| GB-P005 | REEF | Companion-report relationship unresolved |
| GB-P006 | Paella | Provisional |
| GB-P007 | Orion | Provisional |
| GB-P008 | GSLICE | Provisional |
| GB-P009 | Clockwork | Provisional |
| GB-P010 | SIRIUS | Provisional |
| GB-P011 | ParvaGPU | Accessed preprint versus final publication unresolved |
| GB-P012 | Torpor | Provisional |
| GB-P013 | StreamBox | Provisional |
| GB-P014 | KRYPTON | Provisional |
| GB-P015 | XSched | Provisional |

TGS (GB-P016) and HiveD (GB-P017) are the two separately recorded source-assessed exclusions. Thus **17 reports have assessments; 15 have QA/extraction forms**. The previous bibliography had 21 entries: 15 paper references plus six background/method references. This consolidated bibliography adds the two excluded-paper references, giving 23 entries. Reference counts are not included-study counts.

DOIs or official source URLs appear in `data/paper_list.csv`. Six of the 15 form-covered reports have identified DOIs; official URLs are retained for the other nine. ParvaGPU's DOI exists, but that does not establish that its accessed preprint is identical to the final paper.

## What do the large counts mean?

- Four databases supplied 4,169 occurrences; supplementary discovery supplied 20: **4,189 occurrences** in total.
- Removing 114 linked duplicate occurrences leaves **4,075 canonical records**.
- Every canonical record has initial automated triage: **1,441 exclusion proposals and 2,634 retain/uncertain**. This is not complete verified abstract screening.
- Seventeen candidate records link to source assessments; **2,617 retain/uncertain records have no linked source assessment**.
- The 15 forms contain **150 Q1–Q10 items, 45 reported outcomes and two separate calculations**.
- **Final included reports and unique studies are not established.** The adapted PRISMA 2020 diagram therefore marks unfinished stages as pending.

## Files and submission boundaries

- `main.tex`, `references.bib`, `Submitted_Task1_Protocol.pdf`: compile the complete report using BUILD.md. All table rows are already in the TeX source; compilation does not require CSV-reading scripts.
- `GroupB_Task2_Workbook.xlsx`: 13 readable tabs with cached formulas and recorded-date provenance.
- `separate_tables/`: standalone QA and extraction PDFs preserved from the current assessed set.
- `data/`: unabridged research CSVs, including screening, duplicate, search, eligibility, QA, extraction and reference evidence.
- `table_inventory.json`, `VALIDATION.json`, `FILE_MANIFEST.json`: technical checks and file identity.

The full research tables belong in the appendices as requested. Build scripts, file hashes and publication receipts support reproducibility; they are not scientific findings that need to be pasted into the body. Later CEP Sections 15–22 remain separately preserved in `task2/later_cep/Sections_15_to_22.tex` in the repository.

This is a technically consolidated **interim Task 2 submission**, not a completed systematic selection. Cycles 1 and 2 have closed audit scopes (Cycle 2 retains documented gaps); Cycles 3–5 remain partial overall; Cycle 6 has interim accounting/reference outputs; Cycle 7 supplies this consolidated package. No reliable overall marks/completion percentage can be inferred from initial triage coverage.

# Cycle 1: recovery and requirements audit

Inspected published main `cb8251a1413da77b57a3df894e904c2f9f11bdd0` on 16 October 2026. This cycle changes audit and continuation material only. No search, import, screening, appraisal or extraction decision was added.

## Publication and recovery

| Item | Verified position |
| --- | --- |
| `cd3f1e0` and `014b14c` | Ancestors of inspected main; published |
| Newer `cb8251a` checklist | Published and preserved |
| Local `1aa970c` recovery checkpoint | Not an ancestor of inspected main; recovered files preserved locally |
| Report source | Published source has Sections 1-22 and interim analysis |
| Published report | Opens, 24 pages; later taxonomy heading absent from extracted PDF text |
| Published workbook | ZIP/XML opens, 18 actual worksheet entries, no stored error cells |
| Local recovered artifacts | 38-page PDF and 27-sheet workbook; not the files currently published |
| `evidence/cycle2_validation.json` | Absent on inspected main (GitHub also returned 404); exists in local recovery |

The earlier published checklist says 19 workbook sheets. Reading `xl/workbook.xml` establishes **18**. Historical references to a completed 38-page/27-sheet publication are not supported by inspected main. Do not run an old builder over the recovered files or overwrite newer valid work.

Previous publication attempts for the recovered full PDF were rejected by automatic approval review because it contains identifiable student details. This cycle does not retry that payload. The raw data and submitted protocol remain unchanged. Local recovered validation describes the local artifacts, not the published ones; its existence must not be represented as publication.

## Recalculated baseline

| Measure | Register-derived value |
| --- | --- |
| Imported occurrences | 2,291 |
| Sources | ACM 1,582; Springer 587; IEEE 102; supplementary 20 |
| Database-only occurrences | 2,271 |
| Raw manifest | 81 files; sum 2,291; all hashes and per-file row counts match |
| Applied duplicate links | 44 |
| Canonical record IDs | 2,247 = 2,291 - 44; exactly match screening IDs |
| First recommendations | 1,181 exclude + 1,066 retain/uncertain = 2,247 |
| Final decisions | All 2,247 pending; no final included-study count |
| Independent title votes | None populated in the register; this does not deny unimported human work |
| Appraisal/extraction | 5 report forms; 50 Q1-Q10 items; 5 study forms; 26 outcomes |
| Versions | 41 pairs: 30 containers; 3 identity proposals; 3 companion proposals; 5 unresolved |
| Citation events | 10 targeted events; not exhaustive |

No discrepancy in the requested baseline required a numerical correction. Identity/version proposals remain unapplied. Supplementary discoveries are separate from database occurrences. Staged ACM identifiers and ScienceDirect files are outside these active counts.

## Heading 1-14 deliverables

`../HEADING_14_AUDIT.csv` is the concise 14-row crosswalk. Each row identifies the required section, table/diagram, evidence files and missing work. Prepared content does not certify completed review execution. The guideline explicitly requires a PRISMA diagram; it does not require a separate invented diagram for every heading.

The governing sources are `docs/guidelines.md`, `docs/topics.md` and the unchanged `task1/submitted_protocol.pdf`. Main-window dates, older MPS searches, IC1-IC6/EC1-EC7, independent review and Q1-Q10 scoring remain controlling. The attached GPU-memory-oversubscription sample was inspected for tabular presentation only. Its QA1-QA8 scale and results are inapplicable to Group B.

Missing work is concentrated in reproducible query/export coverage, actual independent decisions, final full-text eligibility, wider primary-report QA/extraction and final PRISMA. The guideline expectation of 15-20 final primary studies is not met by calling 26 outcomes or 5 checked reports included studies.

## Verification and continuation

`receipt.json` records actual file hashes and checks. `scripts/audit_recovery.py` recomputes counts and file-opening checks without hard-coding the expected baseline. Opening/ZIP parsing and cached-error checks are not a fresh Excel recalculation or a new complete visual inspection.

Next authorized cycle is **Cycle 2: queries, imports and four-database coverage**, only when separately requested. Audit each database, reconcile exported occurrences versus displayed hits and overlapping files, inspect staged ScienceDirect evidence, preserve supplementary discoveries separately and amend the protocol only for actual deviations. Do not begin screening Cycle 3 or silently replace current artifacts with older builds.

# Integration of teammate checks and continued screening

Frozen baseline: commit `04271d77eae68f153d0682f951bd3cc1e9162a6b`. Never overwrite its ZIP, report, workbook or submitted protocol during screening.

## One working master

1. Preserve each teammate's returned file unchanged with the actual date and reviewer identity. Match by report ID, study ID, item ID and source version. A screenshot or report reading does not establish an independent item-level source vote.
2. Log every proposed change with its origin, evidence anchor, old value, proposed value, affected files and resolution. If screening creates a newer value, flag a conflict for source-based adjudication; do not automatically choose the most recent file.
3. Keep initial independent judgments separate from the prepared review and the adjudicated value. Name the real reviewer only when actually supplied. Record unresolved items explicitly.
4. Validate eligibility and report-to-study linkage before counting a new study. Assign new stable IDs without renumbering the frozen P/S IDs. Maintain a mapping for duplicate or companion reports. Do not assume a different DOI means a different study.
5. For each eligible addition complete source appraisal, extraction and claim-to-source anchors. Update taxonomy, comparisons, RQ synthesis, recommendations, references and validity where the new evidence changes them.
6. Recompute selection accounting from actual stage events. Abstract-review recommendations are not final full-text exclusions, independent votes or PRISMA closure. Preserve historical search gaps unless recovered evidence resolves them.
7. Generate a new dated report, integrated workbook and supporting ZIP. Check study/report counts, reference resolution, formula consistency, artifact hashes and frozen baseline integrity. Preserve the exact submitted release and change log.

## Working change log schema

Change ID | Origin | Received/assessed UTC | Reviewer or preparer role | Study/report/item ID | Source version | Old value | Proposed value | Evidence anchor | Resolution | Affected artifacts | Applied release

## Publication authorization

On22October2026the user explicitly requested that this screening continuation, including recovered abstract text and derived assessments, be saved in a separate folder in the public Raazia-Imran/os_CEPPPPPP repository. Publish checkpoints on the task3-screening-559 branch under task3/screening559. Preserve the frozen submission artifacts and integrate scientific changes into the final report/workbook only after eligibility and review closure. Licensed reading PDFs and private access links are excluded.

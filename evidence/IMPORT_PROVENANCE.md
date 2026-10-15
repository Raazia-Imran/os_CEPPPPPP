# Shared-source provenance and counting

The user explicitly authorized reuse of Group A's IEEE/Springer searches and assessments on 15 October 2026 and supplied the ACM Drive folder. Source snapshot: `AliRazaDev241/OS_CEP` commit `adf4a1e827f71610eba21785fbf5cbac8793fbfc`. Group A is the originating collector; Group B is the reusing review team. These are not newly executed Group B searches.

`imports/group-a/` preserves the original committed evidence files byte-for-byte. Its nested README/status statements describe Group A, not the current Group B review. Original Group A IDs, QA meanings and decisions stay intact. `shared_candidate_review.csv` maps prior accepted studies to new Group B records; its acceptance field remains pending.

`imports/acm/` preserves all 79 supplied BibTeX files. The Drive listing contains numbered names 1-80 except 3. This filename gap does not prove a missing search page; completeness must be checked against the actual run/export log. BibTeX holds 686 inproceedings, 609 proceedings, 264 articles, 15 inbook items, 7 books and 1 technical report (1,582 occurrences). Publication type is used only as an explicit first-review recommendation, with independent audit pending.

No ACM query, date, displayed count, field or page mapping is inferred from a batch name or upload timestamp. The private Drive folder URL is not committed. `import_manifest.csv` records each file's hash and count. `records.csv` retains source membership, original record ID, file and position. New record numbering uses deterministic filename order and source position; preserve raw names and this order when rebuilding.

Deduplication normalizes DOI, then matches exact publisher URL; identifier-free copies may match identical normalized title+author+year. Different DOIs remain separate for version checks. This conservative reconstruction yields 44 linked repeated occurrences and 41 unresolved title pairs. It supersedes the unverified 74/2,217 figures in the pasted interrupted-session update. Do not mix counts from the two runs.

The 20 shared supplementary leads remain distinct from database exports. A new targeted four-reference backward pilot is recorded in `snowballing.csv`; three unimported candidate leads are not added to identification totals until resolved. Existing GSLICE references point to existing records. No forward citation census has been completed.

`screening.csv` is a mutable work queue. `title_votes.csv` preserves actual first-review events; final decisions remain pending. Automated priority flags are not exclusions. A later first-pass decision does not override a distinct independent vote. Changes to CSVs require rebuilding derived report/workbook outputs.

Licensed full texts, Markdown conversions of licensed articles, VPN details and private access links are not committed. Source-anchored extracted facts and assessment notes may be committed. Original full texts remain in their authorized private locations.

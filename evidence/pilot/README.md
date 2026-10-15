# Pilot full-text evidence checks

Three public source versions were downloaded and their substantive methods/results inspected on 15 October 2026. These are single-AI-reviewer pilot checks; final publisher-version comparison and a second independent protocol vote remain pending. No candidate here is counted as a final included Group B study.

- `publication_checks.csv`: Crossref DOI registration metadata checked against incoming RIS. A DOI's embedded year is not necessarily its issue-publication year: Lilou's DOI contains 2025, but its registered issue is March 2026.
- `fulltext_receipts.csv`: public copy URLs and hashes, so the examined version can be identified. Full-text PDFs remain outside the public repository.
- `eligibility_checks.csv`: provisional IC/EC recommendations with source anchors and unresolved checks.
- `extraction.csv`: pilot facts and chart labels only. Naranjo Fig. 9 labels were visually checked. Values describe end-to-end processing of video batches, not p95/p99 request latency. Gilman and Walls use training completion time as a utilization proxy; do not relabel it GPU busy percentage.
- `candidate_references.bib`: DOI-checked journal citations for candidates, separate from the final included-study bibliography.

These checks reduce later reading effort but do not close the four database searches, independent screening, quality assessment or final data-extraction milestones.

Version cautions: the Naranjo author copy retains template/footer and text artifacts; the Lilou author copy includes a placeholder running header, “Trovato et al.” These do not change the independently checked journal identities, but they make final-version comparison essential before treating the extracted source as the definitive published text.


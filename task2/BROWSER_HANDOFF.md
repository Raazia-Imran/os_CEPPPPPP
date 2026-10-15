# Minimum browser handoff for the four database searches

I prepared every Group B query in `evidence/planned_queries.csv`. A connected VPN icon alone does not establish that a library page recognizes your institution. Desktop Commander's available controls run terminal commands and manage files; its direct requests met site protection on three publishers and a client challenge on the Springer search page. It cannot presently click the already signed-in browser's search/export controls. Those terminal probes did not execute protocol searches.

For the part that requires a person's authenticated browser, use the same short routine for each platform:

1. In your VPN-connected browser, enter the NED library's E-Resources page and follow the database link. Check whether you can actually search and export. No passwords or VPN files need to be shared.
2. Open `evidence/planned_queries.csv`. Copy the **submitted_expression** for one platform/query ID. The ID (for example `I1`) is only a label. Set the protocol's field and publication years; record any search expression the website changes or rejects.
3. Note the result count displayed **before** exporting and the exact field, filters, date/time with timezone and collection. Export *every result page/batch* with at least title, authors, abstract, year, venue, DOI and URL where available. Keep original files. If the site limits batch size, record each batch and whether any results remain unexported.
4. Fill one line of `evidence/search_runs.csv` per executed query and send/upload the original export(s). A screenshot of the result count and applied filters can help but does not replace the export.
5. Repeat the three current-period searches and one historical MPS search per platform (four searches × four platforms = sixteen planned). If a platform has no institutional access, record the precise error; an alternative database would need a justified protocol amendment.

| Platform | IDs | Submitted scope to check in the live interface |
| --- | --- | --- |
| IEEE Xplore Command Search | I1, I2, I3, H1 | All Metadata; current period or pre-2020 historical lane |
| ACM Digital Library Advanced Search | A1, A2, A3, H2 | Record whether the ACM Guide to Computing Literature or ACM full-text collection was searched |
| ScienceDirect Advanced Search | D1, D2, D3, H3 | Title/abstract/author keywords field; avoid silently using body-wide search |
| Springer Nature Link Advanced Search | S1, S2, S3, H4 | Keywords includes document body; record noise and actual scope, and any precision search separately |

**Simplest handoff:** one platform at a time, send the four export files and the four filled log lines. I can then import records, check duplicates, organize title/abstract votes and prepare the evidence report. Download requests for individual full texts are a later, short list; the public copies in `evidence/reading_notes.md` already reduce that burden.

**What to send additionally:** the instructor's separate Task 2 statement/rubric and exact deadline, if there is one. The course guideline specifies the whole CEP through Data Extraction but does not define a separate Task 2 length or grading checklist.


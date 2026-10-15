"""Initialize non-claiming Group B CSV registers from the submitted protocol."""

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"


def write_csv(name, fields, rows=()):
    with (EVIDENCE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    tex = (ROOT / "task1/search_strings.tex").read_text(encoding="utf-8")
    rows = []
    platform = None
    current = None
    for line in tex.splitlines():
        if "IEEE Xplore Command Search" in line:
            platform = "IEEE Xplore"
        elif "ACM Digital Library Advanced Search" in line:
            platform = "ACM Digital Library"
        elif "ScienceDirect Advanced Search" in line:
            platform = "ScienceDirect"
        elif "Springer Nature Link Advanced Search" in line:
            platform = "Springer Nature Link"
        match = re.match(r"^(I[1-3]|A[1-3]|D[1-3]|S[1-3]|H[1-4])\s*=\s*(.*)$", line)
        if match:
            if current:
                rows.append(current)
            qid, expression = match.groups()
            current = dict(query_id=qid, platform=platform, lane="pre_2020_MPS" if qid.startswith("H") else "main_2020_to_run_date", submitted_expression=expression)
        elif current and (not line.strip() or line.startswith(r"\end{Verbatim}")):
            rows.append(current)
            current = None
        elif current:
            current["submitted_expression"] += " " + line.strip()
    if current:
        rows.append(current)
    ids = {r["query_id"] for r in rows}
    expected = {f"{prefix}{n}" for prefix in "IADS" for n in range(1, 4)} | {f"H{n}" for n in range(1, 5)}
    assert ids == expected and len(rows) == 16, (len(rows), sorted(ids ^ expected))
    write_csv("planned_queries.csv", ["query_id", "platform", "lane", "submitted_expression"], rows)
    write_csv("search_runs.csv", ["run_id", "query_id", "platform", "collection", "interface_url", "access_route", "executed_at_local", "timezone", "exact_accepted_query", "field_scope", "date_range", "language_filter", "document_filter", "displayed_hits", "exported_occurrences", "batch_or_page_range", "export_file", "sha256", "operator", "status", "syntax_error_or_amendment", "notes"])
    write_csv("access_tests.csv", ["date_utc", "platform", "route", "tested_url", "observed_outcome", "can_search_browser", "can_export", "formal_query_executed", "notes"], [
        dict(date_utc="2026-10-15 (exact time not captured)", platform="NED E-Resources", route="Remote Desktop Commander PowerShell web request on connected device", tested_url="https://eaklibrary.neduet.edu.pk/eakl/E-Resources.html", observed_outcome="Timeout after 15 seconds", can_search_browser="unknown", can_export="unknown", formal_query_executed="no", notes="Terminal test only; VPN/session entitlement unverified"),
        dict(date_utc="2026-10-15 (exact time not captured)", platform="IEEE Xplore", route="Remote Desktop Commander PowerShell web request on connected device", tested_url="https://ieeexplore.ieee.org/", observed_outcome="HTTP 418 from direct request", can_search_browser="unknown", can_export="unknown", formal_query_executed="no", notes="Direct request response is not proof browser access fails"),
        dict(date_utc="2026-10-15 (exact time not captured)", platform="ACM Digital Library", route="Remote Desktop Commander PowerShell web request on connected device", tested_url="https://dl.acm.org/", observed_outcome="HTTP 403 from direct request", can_search_browser="unknown", can_export="unknown", formal_query_executed="no", notes="Direct request response is not proof browser access fails"),
        dict(date_utc="2026-10-15 (exact time not captured)", platform="ScienceDirect", route="Remote Desktop Commander PowerShell web request on connected device", tested_url="https://www.sciencedirect.com/", observed_outcome="Connection closed on direct request", can_search_browser="unknown", can_export="unknown", formal_query_executed="no", notes="Direct request response is not proof browser access fails"),
        dict(date_utc="2026-10-15 (exact time not captured)", platform="Springer Nature Link", route="Remote Desktop Commander PowerShell web request on connected device", tested_url="https://link.springer.com/", observed_outcome="HTTP 200 homepage; later simple search URL showed JavaScript client challenge", can_search_browser="unknown", can_export="unknown", formal_query_executed="no", notes="No protocol expression executed; no hit count; shell access not browser login"),
    ])
    templates = EVIDENCE / "templates"
    write_csv("templates/records.csv", ["record_id", "run_id", "database", "raw_export_file", "source_position", "title", "authors", "year", "venue", "doi", "url", "abstract", "source_hash"])
    write_csv("templates/duplicates.csv", ["record_id", "canonical_record_id", "match_basis", "checked_by", "checked_date", "resolution_notes"])
    write_csv("templates/screening.csv", ["record_id", "stage", "reviewer_id", "independent_vote", "criterion", "reason", "date", "resolved_vote", "adjudicator", "adjudication_notes"])
    write_csv("templates/reports.csv", ["report_id", "canonical_record_id", "study_id", "retrieval_status", "retrieval_attempts", "full_text_criterion", "first_decisive_exclusion_reason", "report_version", "reviewer_id", "date"])
    write_csv("templates/quality.csv", ["study_id", "criterion_Q1_to_Q10", "reviewer_id", "score_0_1_2_or_NA", "justification", "source_page_or_table", "date"])
    write_csv("templates/extraction.csv", ["study_id", "report_id", "doi", "source_page_table_figure", "mechanism_configuration", "gpu_hardware", "driver_runtime_os", "model_workload", "tenant_count", "batch_load_slo", "baseline", "metric", "value_and_units", "uncertainty", "method", "reported_limitations", "reviewer_interpretation", "RQ_tag", "extracted_by", "checked_by"])
    print("Initialized", len(rows), "planned expressions and blank Group B review registers")


if __name__ == "__main__":
    main()

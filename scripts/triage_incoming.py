"""Conservative, single-reviewer *preliminary* triage of supplied RIS only.

This is not the submitted protocol's independent two-reviewer screening or a
formal PRISMA stage. Decisions are deliberately reversible on full-text review.
"""

import csv
import re
from pathlib import Path

from prepare_leads import first, key, parse_ris


ROOT = Path(__file__).resolve().parents[1]
ADVANCE = {8, 14, 20, 22, 24, 39, 42}
UNCERTAIN = {1, 11, 13, 15, 27, 28, 84, 92}


def disposition(position, rec):
    title = first(rec, "T1", "TI").lower()
    abstract = first(rec, "N2", "AB").lower()
    if position in ADVANCE:
        return "read_full_text", "Potential single-GPU inference sharing/remoting evidence; mechanism and separability require full-text verification"
    if position in UNCERTAIN:
        return "uncertain_recheck", "Metadata leave inference tenants, device-level contrast or mechanism evaluation unresolved"
    if title.startswith("chapter") or "survey" in title or " review" in title:
        return "likely_out_of_scope", "Secondary work or book chapter; can inform background, not primary included set"
    if "welding" in title or "microplastic" in title or "crop" in title or "defect" in title:
        return "likely_out_of_scope", "Different application; no evaluated concurrent inference GPU-sharing mechanism in supplied metadata"
    if "training" in title and "inference" not in title and "inference" not in abstract:
        return "likely_out_of_scope", "Training-oriented record; no separable inference-sharing evaluation identified in supplied metadata"
    return "likely_out_of_scope", "Title and supplied abstract do not establish evaluated concurrent tenants on one GPU; reopen if later evidence changes this"


def main():
    seen = {}
    rows = []
    count = 0
    for path in sorted((ROOT / "evidence/incoming_shared").glob("*.ris")):
        for local_no, rec in enumerate(parse_ris(path), 1):
            count += 1
            lead = dict(lead_id=f"B-LEAD-{count:04d}", doi=first(rec, "DO"), title=first(rec, "T1", "TI"))
            identity = key(lead)
            if identity in seen:
                decision, reason = "exact_key_duplicate", "Same DOI or normalized title as earlier incoming RIS record; manual verification still required"
            else:
                seen[identity] = lead["lead_id"]
                decision, reason = disposition(count, rec)
            rows.append(dict(lead_id=lead["lead_id"], source_file=path.name, source_position=local_no, title=lead["title"], doi=lead["doi"], exact_key_canonical=seen[identity], preliminary_disposition=decision, reason=reason, basis="rules_assisted_metadata_triage_not_full_independent_screening", reviewed_date_utc="2026-10-15", formal_group_b_screening="no"))
    assert count == 100
    with (ROOT / "evidence/preliminary_triage.csv").open("w", newline="", encoding="utf-8") as out:
        w = csv.DictWriter(out, rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    from collections import Counter

    print("Preliminary triage only:", dict(Counter(row["preliminary_disposition"] for row in rows)))


if __name__ == "__main__":
    main()

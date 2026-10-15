"""Inventory supplied candidate metadata without deciding Group B eligibility."""

import csv
import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_A = ROOT.parent / "OS_CEP/groups/group-a/evidence/accepted.csv"
RIS_DIR = ROOT / "evidence/incoming_shared"


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_ris(path):
    record = {}
    last = None
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        match = re.match(r"^([A-Z0-9]{2})  - (.*)$", line)
        if match:
            tag, value = match.groups()
            if tag == "TY":
                record = {}
            elif tag == "ER":
                yield record
                record, last = {}, None
                continue
            else:
                record.setdefault(tag, []).append(value)
            last = tag
        elif line.startswith(" ") and last and record.get(last):
            record[last][-1] += " " + line.strip()


def first(rec, *tags):
    return next((rec[tag][0].strip() for tag in tags if rec.get(tag)), "")


def key(row):
    doi = row["doi"].lower().removeprefix("https://doi.org/").strip()
    if doi:
        return "doi:" + doi
    title = re.sub(r"[^a-z0-9]+", "", row["title"].lower())
    return "title:" + title if title else "unknown:" + row["lead_id"]


def main():
    leads, inventories = [], []
    for path in sorted(RIS_DIR.glob("*.ris")):
        records = list(parse_ris(path))
        inventories.append((path.name, len(records), hashlib.sha256(path.read_bytes()).hexdigest()))
        for idx, record in enumerate(records, 1):
            leads.append(dict(lead_id=f"B-LEAD-{len(leads)+1:04d}", source_kind="user_supplied_ScienceDirect_RIS_unverified_run", source_id=f"{path.name}#{idx:03d}", title=first(record, "T1", "TI"), doi=first(record, "DO"), year=first(record, "PY", "Y1")[:4], url=first(record, "UR", "L1"), group_b_decision="", review_status="unassessed_candidate"))
    if SOURCE_A.exists():
        with SOURCE_A.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            leads.append(dict(lead_id=f"B-LEAD-{len(leads)+1:04d}", source_kind="Group_A_shared_accepted_list_not_B_decision", source_id=row["study_id"], title=row["title"], doi=row["doi"], year=row["publication_date"][:4], url=row["url"], group_b_decision="", review_status="unassessed_candidate"))
    fields = ["lead_id", "source_kind", "source_id", "title", "doi", "year", "url", "group_b_decision", "review_status"]
    write_csv(ROOT / "evidence/shared_leads.csv", fields, leads)
    keys = Counter(map(key, leads))
    exact_duplicate_occurrences = sum(count - 1 for count in keys.values())
    print(f"incoming RIS occurrences: {sum(n for _, n, _ in inventories)}")
    print(f"Group A lead occurrences: {len(leads)-sum(n for _, n, _ in inventories)}")
    print(f"all lead occurrences: {len(leads)}, exact DOI/title key duplicates: {exact_duplicate_occurrences}, key-distinct leads: {len(keys)}")
    for filename, count, digest in inventories:
        print(f"{filename}: {count} records; sha256 {digest}")


if __name__ == "__main__":
    main()

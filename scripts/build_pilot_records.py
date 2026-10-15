"""Build pilot records from locally retrieved public manuscripts and Crossref JSON.

Run with the directory containing the receipt filenames below. No final Group B
inclusion or independent reviewer agreement is inferred by this script.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/pilot"
SOURCES = [
    ("B-LEAD-0014", "naranjo2020", "naranjo2020.pdf", "https://www.grycap.upv.es/gmolto/publications/preprints/Diana2020asc.pdf", "author_hosted_manuscript", 30),
    ("B-LEAD-0020", "lilou", "lilou.pdf", "https://lass.cs.umass.edu/papers/pdf/lilou_gpu_prediction.pdf", "author_hosted_manuscript", 12),
    ("B-LEAD-0039", "gilman2021", "concurrency2021.pdf", "https://arxiv.org/pdf/2110.00459", "arxiv_v1_author_manuscript", 21),
]


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    source_dir = parser.parse_args().source_dir
    publications, receipts, bib = [], [], []
    for lead, stem, filename, url, version, pages in SOURCES:
        metadata_path = source_dir / (stem + "_crossref.json")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))["message"]
        date_parts = metadata["published"]["date-parts"][0]
        year = date_parts[0]
        publications.append(dict(lead_id=lead, doi=metadata["DOI"], title=metadata["title"][0], journal=metadata["container-title"][0], volume=metadata.get("volume", ""), pages_or_article=metadata.get("page", ""), issue_date="-".join(map(str, date_parts)), metadata_source="https://api.crossref.org/works/" + metadata["DOI"], metadata_sha256=hashlib.sha256(metadata_path.read_bytes()).hexdigest(), checked_date_utc="2026-10-15", final_text_version_compared="no"))
        pdf = source_dir / filename
        receipts.append(dict(lead_id=lead, source_url=url, source_version=version, source_pages=pages, file_bytes=pdf.stat().st_size, sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(), retrieved_date_utc="2026-10-15", repository_pdf_uploaded="no", screening_status="single_AI_pilot_only"))
        authors = " and ".join(a.get("family", "") + ", " + a.get("given", "") for a in metadata["author"])
        page = metadata.get("page", "").replace("-", "--")
        title = metadata["title"][0].replace("NVIDIA", "{NVIDIA}").replace("GPU", "{GPU}").replace("Lilou", "{Lilou}")
        bib.append("@article{candidate_" + stem + ",\n  author = {" + authors + "},\n  title = {" + title + "},\n  journal = {" + metadata["container-title"][0] + "},\n  year = {" + str(year) + "},\n  volume = {" + metadata.get("volume", "") + "},\n  pages = {" + page + "},\n  doi = {" + metadata["DOI"] + "},\n  url = {https://doi.org/" + metadata["DOI"] + "}\n}\n")
    write("publication_checks.csv", publications)
    write("fulltext_receipts.csv", receipts)
    (OUT / "candidate_references.bib").write_text("% Verified journal identities; candidates, not final included studies.\n\n" + "\n".join(bib), encoding="utf-8")
    write("eligibility_checks.csv", [
        dict(lead_id="B-LEAD-0014", reviewer="Codex_single_pilot", recommendation="provisionally_eligible", criterion="IC2_IC3_IC4_IC5", source_anchor="Author manuscript sections 4.2-4.3 and 5; PDF pp14-22; Fig9 p21", reason="Concurrent inference video-processing functions share one V100 through rCUDA; inspectable batch completion outcomes", pending="Final journal text equivalence; second independent vote; QA; exact inference model/software versions", final_included="no"),
        dict(lead_id="B-LEAD-0020", reviewer="Codex_single_pilot", recommendation="context_only_or_exclude_pending_final_version", criterion="EC2_IC2", source_anchor="Author manuscript sections 3.3, 4, 5.1 and 5.4; PDF pp5-9", reason="MPS limits resource allocation for prediction experiments; examined evaluation does not establish concurrent co-tenant inference contrast", pending="Compare final 2026 journal version before final EC2 decision; second independent vote", final_included="no"),
        dict(lead_id="B-LEAD-0039", reviewer="Codex_single_pilot", recommendation="provisionally_eligible", criterion="IC2_IC3_IC4_IC5", source_anchor="arXiv v1 sections 3.1, 4.2-4.3 and discussion O10; PDF pp4,9-13,17", reason="One training and one inference workload share RTX3090; inference outcomes separable for time-slicing and MPS", pending="Compare final Performance Evaluation version; second independent vote; QA; distinguish proxy utilization from busy-percent", final_included="no"),
    ])
    extraction = []
    for videos, remote, native in [(1,52,24),(2,67,49),(3,74,73),(4,86,98)]:
        extraction.append(dict(lead_id="B-LEAD-0014", source_version="author_manuscript", anchor="PDF p21 Fig9 (labels visually checked); methods pp14-18; explanation p22", mechanism="OSCAR+rCUDA API remoting", hardware="Tesla V100 32GB; 10GbE; virtualized serverless setting", workload=f"{videos} video(s), each 180 frames; pretrained echocardiography image classification", comparator="OSCAR+Native GPU with platform access bottleneck", metric="end-to-end video-batch completion time", candidate_value=remote, comparator_value=native, units="seconds", limitations="Includes environment and processing overhead; exclusive/native vs shared/remote scheduling differs; not per-request p95/p99; several repetitions but exact n/uncertainty NR", reviewer="Codex", check_status="visual_labels_checked_single_reviewer; final_version_and_independent_check_pending"))
    extraction.append(dict(lead_id="B-LEAD-0039", source_version="arxiv_v1", anchor="PDF p4 section3.1; pp12-13 section4.3; p17 O10", mechanism="MPS vs time-slicing; priority streams supplementary comparator", hardware="One NVIDIA GeForce RTX3090 Ampere; MIG not evaluated", workload="One continuous training task and one inference task; 500 Poisson or 5000 single-stream inference requests", comparator="Each workload executed alone", metric="mean/variation of inference turnaround; training completion time as utilization proxy", candidate_value="NR_in_this_pilot_row", comparator_value="NR_in_this_pilot_row", units="ms for inference turnaround; seconds for training completion", limitations="Training time is a proxy, not directly comparable to GPU busy-percent; MPS clients configured at 100%; framework coverage differs across mechanisms", reviewer="Codex", check_status="methods_checked_single_reviewer; numerical_effects_and_final_version_pending"))
    write("extraction.csv", extraction)
    assert len(publications) == 3 and len(extraction) == 5
    print("Saved three DOI checks, three source receipts, three pilot eligibility recommendations, five extraction rows and candidate BibTeX")


if __name__ == "__main__":
    main()

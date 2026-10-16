"""Refresh workbook inputs without screening or import mutations."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evidence'

def read(name):
    with (E / name).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))

paths = [
    ("Screening log","cycle3_screening_log.csv"),("Title votes","title_votes.csv"),
    ("Duplicate ledger","cycle3_duplicate_ledger.csv"),("Metadata audit","cycle3_metadata_audit.csv"),
    ("Retrieval log","cycle3_retrieval.csv"),("Access attempts","cycle3_access_attempts.csv"),
    ("Identity rechecks","cycle3_version_audit.csv"),("Provisional studies","provisional_studies.csv"),
    ("Validated studies","validated_studies.csv"),("FT exclusions","fulltext_exclusions.csv"),
    ("Query audit", "database_query_audit.csv"), ("Export audit", "query_export_audit.csv"),
    ("Date audit", "publication_date_audit.csv"), ("New import queue", "new_import_queue.csv"), ("New version proposals", "new_version_candidates.csv"),
    ("Requirements audit", "../task2/HEADING_14_AUDIT.csv"),

    ('Screening', 'screening.csv'), ('Records', 'records.csv'),
    ('Duplicates', 'duplicates.csv'), ('Version checks', 'possible_versions.csv'),
    ('Source checks', 'fulltext_checks.csv'), ('Quality', 'quality.csv'),
    ('Extraction', 'extraction.csv'), ('Snowballing', 'snowballing.csv'),
    ('Shared candidates', 'shared_candidate_review.csv'), ('Import manifest', 'import_manifest.csv'),
    ('Version audit', 'version_review_audit.csv'), ('Study extraction', 'study_extraction_form.csv'),
    ('Human validation', 'human_validation_queue.csv'), ('Exclusion sample', 'exclusion_validation_sample.csv'),
    ('Metadata enrichment', 'metadata_enrichment.csv'), ('Report validation', 'report_validation_queue.csv'),
    ('Full-text criteria', 'fulltext_criteria.csv'),
    ('Taxonomy', 'cycle2_taxonomy.csv'), ('Comparative matrix', 'cycle2_comparison.csv'),
    ('Trade-offs', 'cycle2_tradeoff.csv'), ('Conflicting evidence', 'cycle2_conflict.csv'),
    ('RQ synthesis', 'cycle2_rq.csv'), ('Recommendations', 'cycle2_recommendation.csv'),
    ('Evidence gaps', 'cycle2_gap.csv'), ('Validity', 'cycle2_validity.csv'),
    ('Reference catalogue', 'cycle2_reference_catalog.csv'),
]
payload = {
    'counts': json.loads((E / 'prisma_counts.json').read_text()),
    'progress': json.loads((E / 'review_progress.json').read_text()),
    'sheets': {name: read(path) for name, path in paths},
    'fields': {name: next(csv.reader((E/path).open())) for name,path in paths},
}
(ROOT / 'task2/tracker/workbook_input.json').write_text(json.dumps(payload, ensure_ascii=False) + '\n')
print(f'Workbook input: {len(paths)} register views plus Summary; no evidence registers modified.')

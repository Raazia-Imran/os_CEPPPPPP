"""Preserve incoming AI opinions without promoting title-only exclusions."""
import csv, hashlib, json, shutil
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
U = R.parent / 'upload'
O = R / 'task2/reconciliation'
O.mkdir(exist_ok=True)
def read(p):
    with p.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))
def write(p, rows):
    with p.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
incoming = read(U / 'cycle3_new_import_ai_prelim(1).csv')
current = {x['record_id']: x for x in read(R/'evidence/screening.csv')}
assert len(incoming) == len({r['record_id'] for r in incoming})
comparison = []
for x in incoming:
    y = current[x['record_id']]
    assert x['doi'].strip().lower() == y['doi'].strip().lower()
    old = y['reviewer_1_vote']
    normalized = 'exclude' if old == 'exclude_recommendation' else 'retain_or_uncertain' if old == 'retain_or_uncertain' else 'pending'
    new = 'exclude' if x['ai_prelim_recommendation'] == 'exclude' else 'retain_or_uncertain'
    comparison.append(dict(record_id=x['record_id'], doi=x['doi'], current_ai_vote=old,
        incoming_ai_vote=x['ai_prelim_recommendation'], incoming_basis=x['basis'],
        comparison='not_previously_recommended' if normalized == 'pending' else 'agree_broad_recommendation' if normalized == new else 'disagree',
        action='preserve_both_AI_opinions;source_check_pending;no_human_vote', final_decision='pending'))
shutil.copyfile(U/'cycle3_new_import_ai_prelim(1).csv', O/'claude_ai_opinions.csv')
write(O/'ai_comparison.csv', comparison)
summary = dict(source_bundle_head='53d558faa73ebedc8cec67e349f49e98c38b6b1b',
    compared_main='f45c72bb5ccf2afb865fb77a1ecad14900ecd14e', incoming_rows=len(incoming),
    comparison_counts=dict(Counter(x['comparison'] for x in comparison)),
    incoming_basis=dict(Counter(x['basis'] for x in incoming)),
    incoming_votes=dict(Counter(x['ai_prelim_recommendation'] for x in incoming)),
    screening_register_modified=False, independent_human_reviews_added=0,
    attachments_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in U.iterdir() if p.name in ['groupB(1).bundle','all_groupB_changes(1).patch','cycle3_new_import_ai_prelim(1).csv']})
(O/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
(O/'CLAUDE_HANDOFF_AUDIT.md').write_text('''# Incoming AI handoff audit

Latest published main was f45c72b. The bundle has four extra commits ending 53d558f, based on the earlier seven-report checkpoint. Its seven-report QA tables and PDF are historical, not replacements for current nine-report evidence. GSLICE and Clockwork were already assessed. The current workbook has 90 QA items, not 50.

The 1,831 incoming recommendations are preserved here under their original AI assessor. Record IDs and DOI fields match the active register. Compare ai_comparison.csv before reconciling any recommendation. Two AI opinions do not satisfy the submitted independent human-review requirement.

No incoming opinion was promoted to a final decision. Most incoming exclusions rely on titles; absence of a GPU-sharing signal in a title does not establish EC2. The README explicitly says that only partial abstracts were read for 19 records. Source-level abstract checks remain necessary, including for disagreements. Existing first opinions remain unchanged; incoming-only opinions remain a separate unverified pass. No duplicate links or PRISMA counts changed.

The alleged ff9cd88 discrepancy-ledger commit is not among the four bundled commits. Do not report it as merged. Existing database discrepancy evidence remains authoritative. The bundle and patch remain preserved in the supplied attachments; this checkpoint publishes only the relevant incoming opinions, comparison and provenance.

Measured baseline: 4,189 occurrences minus 111 linked duplicates equals 4,078 canonical records. 2,487/4,078 (61.0%) have an active preliminary recommendation; 1,591 await one. This is recommendation coverage, not final review completion. There are 9 provisional report forms, 90 QA items and 34 outcome rows. Final included studies remain pending. Existing report source, references and interim PRISMA already exist; the compiled report is historical and needs regeneration.
''')
print(json.dumps(summary,indent=2))

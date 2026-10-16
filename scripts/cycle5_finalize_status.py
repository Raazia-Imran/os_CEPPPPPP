"""Current artifact status, distinct from historical run/reviewer snapshots."""
import csv,json
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];E=R/'evidence'
def read(n):return list(csv.DictReader((E/n).open()))
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
s=read('screening.csv');du=read('duplicates.csv');checks=read('fulltext_checks.csv');forms=read('study_extraction_form.csv');q=read('quality.csv');ex=read('extraction.csv');excluded=read('fulltext_exclusions.csv');links=read('report_record_links.csv');mapped={x['canonical_record_id'] for x in links}
c=json.loads((E/'prisma_counts.json').read_text())
# Preserve the historical priority/disposition snapshots, then state the current ledger status.
c.setdefault('historical_import_triage_snapshot',c['triage']);c['triage']=dict(Counter(x['priority'] for x in s))
c.setdefault('historical_version_pair_dispositions',c['version_pair_dispositions'])
c['version_pair_dispositions_note']='Legacy 41-pair audit snapshot retained; three verified identity proposals are now applied. Other proposals remain unapplied.'
c['proposed_duplicate_links_applied']=True;c['applied_proposed_identity_links']=3
c.update(assessed_fulltext_exclusions=len(excluded),complete_fulltext_exclusion_census=None,unassessed_canonical_candidate_records=sum(x['reviewer_1_vote']=='retain_or_uncertain' and x['record_id'] not in mapped for x in s))
save('prisma_counts.json',c)
p=json.loads((E/'review_progress.json').read_text());p.update(current_report_status='Current 28-page evidence checkpoint; final selection/PRISMA pending',current_synthesis_rows=105,source_checked_reports=len(checks),appraised_reports=len(forms),quality_item_rows=len(q),new_outcome_rows=len(ex),assessed_fulltext_exclusions=len(excluded),final_decisions='Two source-assessed AI EC2 exclusions; remaining final screening/inclusion pending',unassessed_canonical_candidate_records=c['unassessed_canonical_candidate_records'],human_candidate_records_note='Historical human-return queue size; not the active candidate or completed-review count',updated_at_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'))
save('review_progress.json',p)
v=json.loads((E/'cycle3_validation.json').read_text());v['limitations']='Selected source sections assessed; no complete retrieval census or final included-study count. Three verified identity links applied; other version/companion proposals remain unapplied. Current PDFs and workbooks are verified separately in cycle5_package_validation.json.';save('cycle3_validation.json',v)
print('Current status updated; historical run/reviewer snapshots retained')

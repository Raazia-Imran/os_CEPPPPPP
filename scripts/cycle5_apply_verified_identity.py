"""Apply only the three documented publisher-identity proposals; preserve all votes."""
import csv,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];E=R/'evidence';TS=datetime.now(timezone.utc).isoformat(timespec='seconds')
def read(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def write(p,rows,fields=None):
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
records=read(E/'records.csv');by={x['record_id']:x for x in records};du=read(E/'duplicates.csv');s=read(E/'screening.csv');versions=read(E/'cycle3_version_audit.csv')
history=read(E/'screening_merged_history.csv') if (E/'screening_merged_history.csv').exists() else []
applied=[]
for v in versions:
 if v['applied'].startswith('yes'):continue
 a,b=v['record_id'],v['possible_match'];assert by[a]['canonical_record_id']==a and by[b]['canonical_record_id']==b
 doi=v['left_doi'] or v['right_doi'];m=json.loads((R.parent/'private_cycle3'/(doi.replace('/','_')+'.json')).read_text())
 if v['left_doi']:assert any(x['id'].lower()==by[b]['doi'].lower() for x in m['relation']['is-identical-to'])
 else:assert by[a]['url'].lower().rstrip('/')==m['resource']['primary']['URL'].lower().rstrip('/')
 history.extend(x for x in s if x['record_id']==a);s=[x for x in s if x['record_id']!=a]
 for x in records:
  if x['canonical_record_id']==a:x['canonical_record_id']=b
 du.append(dict(record_id=a,canonical_record_id=b,match_basis=v['verified_basis']+'; '+v['metadata_url'],resolution='Applied by AI after explicit user authorization for autonomous reconciliation; preserve initial votes in screening_merged_history.csv'))
 v.update(applied='yes_cycle5',remaining='Applied publisher-identity link; metadata receipts from earlier verification retained; no new search or human action claimed')
 applied.append(dict(removed_canonical_id=a,surviving_canonical_id=b,metadata_url=v['metadata_url'],basis=v['verified_basis'],applied_at_utc=TS,assessor='Codex-GroupB'))
if not applied:print('Already applied');raise SystemExit
assert len(records)-len(du)==len(s)==len({x['canonical_record_id'] for x in records})
write(E/'records.csv',records);write(E/'duplicates.csv',du);write(E/'screening.csv',s);write(E/'screening_merged_history.csv',history);write(E/'cycle3_version_audit.csv',versions);write(E/'cycle5_applied_identity_links.csv',applied)
# Keep the private abstract-bearing metadata view aligned, without changing raw exports.
private=R.parent/'private_cycle3/records.csv';original=read(private)
for x in original:x['canonical_record_id']=by[x['record_id']]['canonical_record_id']
write(private,original)
c=json.loads((E/'prisma_counts.json').read_text());c.update(exact_duplicate_occurrences=len(du),records_after_exact_linkage=len(s),cycle5_new_identity_links=len(applied),duplicate_note='111 earlier exact links plus3 publisher-verified identity links; original export occurrences unchanged')
(E/'prisma_counts.json').write_text(json.dumps(c,indent=2)+'\n')
print(json.dumps(dict(occurrences=len(records),applied_duplicate_links=len(du),canonical_records=len(s),new_identity_links=len(applied))))

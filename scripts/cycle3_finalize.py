"""Derive Cycle3 views and validate preservation without inventing final stages."""
import csv,json,hashlib,subprocess,os
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];E=R/'evidence';TS=datetime.now(timezone.utc).isoformat(timespec='seconds')
def read(n):return list(csv.DictReader((E/n).open()))
def write(n,rs,fields=None):
 with (E/n).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(dict.fromkeys(k for r in rs for k in r)));w.writeheader();w.writerows(rs)
records=read('records.csv');screen=read('screening.csv');du=read('duplicates.csv');forms=read('study_extraction_form.csv');checks=read('fulltext_checks.csv');by={r['record_id']:r for r in records}
assert len(records)-len(du)==len(screen)==len({x['canonical_record_id'] for x in records})
# Preserve earlier actual field values. Newly added DOI/source columns are enrichment only.
import io
for name,key in [('title_votes.csv',None),('quality.csv',None),('extraction.csv','outcome_id'),('screening.csv','record_id')]:
 old=list(csv.DictReader(io.StringIO(subprocess.check_output(['git','show','aa20346:evidence/'+name],cwd=R,text=True))));new=read(name)
 if name=='screening.csv':
  now={x['record_id']:x for x in new}
  if (E/'screening_merged_history.csv').exists():now.update({x['record_id']:x for x in read('screening_merged_history.csv')})
  for x in old:
   if x['reviewer_1_vote']:assert all(now[x['record_id']].get(k,'')==v for k,v in x.items()),x['record_id']
 else:
  assert all(all(new[i].get(k,'')==v for k,v in x.items()) for i,x in enumerate(old)),name
lookup={r['report_id']:r for r in forms}
assessment={r['report_id']:r['first_reviewer_recommendation'] for r in checks}
for name in ['quality.csv','extraction.csv','fulltext_criteria.csv','report_validation_queue.csv']:
 rs=read(name)
 for r in rs:r.update(doi=lookup[r['report_id']]['doi'],source_url=lookup[r['report_id']]['source'])
 write(name,rs)
# Record-keyed screening view supplements original recommendations; do not overwrite them.
links=read('report_record_links.csv')
legacy_aliases={'GB-P003':'Serving Heterogeneous Machine Learning Models','GB-P004':'PipeSwitch:','GB-P005':'Microsecond-scale Preemption'}
for f in forms[:5]:
 for r in records:
  doi=f['doi'].lower()
  match=(doi.startswith('10.') and r['doi'].lower()==doi) or (f['report_id'] in legacy_aliases and legacy_aliases[f['report_id']].lower() in r['title'].lower() and r['year']==f['year'])
  if match and not any(x['report_id']==f['report_id'] and x['record_id']==r['record_id'] for x in links):links.append(dict(report_id=f['report_id'],record_id=r['record_id'],canonical_record_id=r['canonical_record_id'],provisional_study_id=f['study_id'],doi=f['doi'],study_linkage_status='record identity supported;study linkage provisional'))
write('report_record_links.csv',links)
mapped={}
for x in links:mapped.setdefault(x['canonical_record_id'],[]).append(x['report_id'])
log=[]
for s in screen:
 r=by[s['record_id']];pids=mapped.get(s['record_id'],[])
 log.append(dict(record_id=s['record_id'],database=r['database'],title=r['title'],year=r['year'],doi=r['doi'],duplicate_status='canonical',title_abstract_recommendation=s['reviewer_1_vote'] or 'awaiting_first_recommendation',title_abstract_reason=s['reason'],report_ids=';'.join(pids),fulltext_first_assessment=';'.join(assessment[p] for p in pids) if pids else s['fulltext_status'],fulltext_assessor='Codex-GroupB' if pids else '',fulltext_source=';'.join(lookup[p]['source'] for p in pids),fulltext_anchor=';'.join(lookup[p]['source_anchor'] for p in pids),independent_vote=s['reviewer_2_vote'],final_status=s['final_decision']))
write('cycle3_screening_log.csv',log)
ledger=[dict(record_id=r['record_id'],canonical_record_id=r['canonical_record_id'],doi=r['doi'],source_file=r['source_file'],duplicate_status='linked_repeat' if r['record_id']!=r['canonical_record_id'] else 'canonical',link_basis=next((d['match_basis'] for d in du if d['record_id']==r['record_id']),'')) for r in records]
write('cycle3_duplicate_ledger.csv',ledger)
versions=[]
private=Path(os.environ.get('OS_CEP_PRIVATE_DIR',R.parent/'private_cycle3'))
for v in read('version_review_audit.csv'):
 if v['audit_disposition']!='identity_verified_linkage_proposed':continue
 doi=v['left_doi'] or v['right_doi'];m=json.loads((private/(doi.replace('/','_')+'.json')).read_text());a=by[v['record_id']];b=by[v['possible_match']]
 relation=m.get('relation',{}).get('is-identical-to',[]);u=m.get('resource',{}).get('primary',{}).get('URL','')
 verified=any(x['id'].lower()==b['doi'].lower() for x in relation) if v['left_doi'] else a['url'].lower().rstrip('/')==u.lower().rstrip('/')
 assert verified
 versions.append(dict(record_id=v['record_id'],possible_match=v['possible_match'],left_doi=v['left_doi'],right_doi=v['right_doi'],metadata_url='https://api.crossref.org/works/'+doi,verified_basis='Crossref is-identical-to relation' if v['left_doi'] else 'Exact publisher primary URL matches DOI-less occurrence',checked_at_utc=TS,assessor='Codex-GroupB',applied='no',remaining='Independent reconciliation/application pending; no counts changed'))
if not (E/'cycle3_version_audit.csv').exists():write('cycle3_version_audit.csv',versions)
if not (E/'cycle3_access_attempts.csv').exists():
 failure=json.loads((private/'failed_attempt.json').read_text());write('cycle3_access_attempts.csv',[dict(failure,assessor='Codex-GroupB',report_status='not_retrieved_this_attempt;alternate_routes_not_exhausted')])
ex=sum(x['reviewer_1_vote']=='exclude_recommendation' for x in screen);retain=sum(x['reviewer_1_vote']=='retain_or_uncertain' for x in screen);pending=sum(not x['reviewer_1_vote'] for x in screen)
c=json.loads((E/'prisma_counts.json').read_text());c.update(preliminary_recommendations=ex+retain,preliminary_exclusion_recommendations=ex,preliminary_retain_or_uncertain=retain,first_recommendations_pending=pending,cycle3_assessed_reports=len(checks),cycle3_provisionally_eligible_reports=sum(x['first_reviewer_recommendation'].startswith('provisionally_eligible') for x in checks),final_screened=None,final_included=None,cycle3_note='Bounded first-review assessments; source-version uncertainty is not provisional eligibility; no final PRISMA completion inferred')
(E/'prisma_counts.json').write_text(json.dumps(c,indent=2)+'\n')
p=json.loads((E/'review_progress.json').read_text());p.update(first_reviewer_records=ex+retain,first_reviewer_fraction=(ex+retain)/len(screen),exclude_recommendations=ex,retained_or_uncertain=retain,unreviewed=pending,source_checked_reports=len(checks),appraised_reports=len(forms),quality_item_rows=len(read('quality.csv')),new_outcome_rows=len(read('extraction.csv')),human_candidate_records=len(read('human_validation_queue.csv')),cycle3_new_recommendations=sum(v.get('batch_id')=='C3-METADATA-01' for v in read('title_votes.csv')),cycle3_new_report_assessments=4,updated_at_utc=TS,cycle3_status='Batches1-2 saved; remaining screening and independent validation open',cycle2_report_status='Historical PDF predates expanded Cycle3 evidence')
(E/'review_progress.json').write_text(json.dumps(p,indent=2)+'\n')
validation=dict(checked_at_utc=TS,occurrences=len(records),duplicate_links=len(du),canonical_records=len(screen),recommendations=ex+retain,exclude_recommendations=ex,retain_or_uncertain=retain,first_recommendations_pending=pending,source_checked_reports=len(checks),quality_items=len(read('quality.csv')),outcome_rows=len(read('extraction.csv')),preserved_baseline_reviews=True,duplicate_links_changed=len(du)!=111,independent_human_votes_created=False,final_included_studies=None,limitations='Selected source sections assessed; no complete systematic retrieval census. Three publisher-verified identity links applied; other version/companion proposals remain unapplied. Existing PDF historical.')
assert validation['quality_items']==10*len(forms) and len({x['outcome_id'] for x in read('extraction.csv')})==validation['outcome_rows'] and ex+retain+pending==len(screen)
(E/'cycle3_validation.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps(validation,indent=2))

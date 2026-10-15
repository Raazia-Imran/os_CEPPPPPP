"""Refresh explicit missing-data labels, validation tasks and reproducible counts."""
import csv,json
from pathlib import Path
from datetime import datetime,timezone
from import_shared import csvwrite,title_key,doi_key
from cycle1_screen import read,now,metadata,refresh,validate
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence';TS=now()
def write(n,rows):csvwrite(E/n,rows,list(dict.fromkeys(k for r in rows for k in r)))
rec={r['record_id']:r for r in read('records.csv')};en={r['record_id']:r for r in read('metadata_enrichment.csv')}
q=read('screening.csv');votes=read('title_votes.csv');byvote={r['record_id']:r for r in votes}
for r in q:
    rr=rec[r['record_id']];f,a,full=metadata(rr,en)
    status='abstract available' if full else 'abstract unavailable'+('; search-result snippet only' if a else '')
    r['abstract_status']=status;r.setdefault('final_decision','pending')
    if not r.get('final_decision'):r['final_decision']='pending'
    if not r.get('publication_type_checked'):r['publication_type_checked']=rr['entry_type'] or f.get('entry_type','') or 'unknown'
    if not r.get('venue_checked'):r['venue_checked']=rr['venue'] or f.get('venue','') or 'unknown'
    if not r.get('doi_metadata'):r['doi_metadata']=rr['doi'] or f.get('doi','') or 'not resolved'
    if not r.get('evidence_excerpt'):r['evidence_excerpt']=a[:400] if full else rr['title']
    v=byvote.get(r['record_id'])
    if v:
        v['abstract_status']=status;v.setdefault('fulltext_status',r['fulltext_status']);v['metadata_status_checked_at_utc']=TS
        # No historical timestamp or more precise historical vote is invented.
        if not v.get('recommendation'):v['recommendation']='exclude' if v['vote']=='exclude_recommendation' else 'uncertain'
write('screening.csv',q);write('title_votes.csv',votes)
outcomes=read('extraction.csv')
for i,r in enumerate(outcomes,1):
    r['outcome_id']=r.get('outcome_id') or f'GB-O{i:03d}'
    r.setdefault('independent_checker','');r.setdefault('independent_checked_at_utc','');r.setdefault('final_decision','pending')
write('extraction.csv',outcomes)
forms=read('study_extraction_form.csv')
shared=json.loads((E/'imports/group-a/included_studies.json').read_text())
for r in forms:
    match=next((s for s in shared if r['doi'] and doi_key(s.get('doi',''))==doi_key(r['doi'])),None)
    if match:
        for dest,key in [('authors','authors'),('year','year'),('venue','venue')]:
            if not r.get(dest) and match.get(key):r[dest]=str(match[key])
    for k,v in list(r.items()):
        if not v and k not in ['independent_checker']:r[k]='not resolved' if k=='doi' else 'not extracted'
write('study_extraction_form.csv',forms)
checks=read('fulltext_checks.csv');tasks=[];criteria=[]
for r in checks:
    rid=r['report_id'];n=sum(x['report_id']==rid for x in outcomes)
    tasks.append(dict(report_id=rid,title=r['short_name'],source=r['source'],eligibility_task='Independently check IC1-IC6, report version and within-one-GPU evidence',outcome_task=f'Verify {n} registered outcomes against exact baseline/unit/anchor',quality_task='Independently score Q1-Q10 using0-2 rubric; preserve own scores',checker='',checked_at_utc='',reconciliation_status='pending',final_decision='pending'))
    for code,reason in [('IC1','Verify final English peer-reviewed report and companion/version relationship.'),('IC2','Check mechanism classification,distinct tenants and single-device sharing.'),('IC3','Check inference workload;PipeSwitch mixed training/inference relevance needs explicit decision.'),('IC4','Check evaluable outcome,configuration and baseline against extraction anchors.'),('IC5','Confirm separable same-device result and sufficient full text.'),('IC6','Verify publication date versus documented cutoff;older exception if needed.')]:
        criteria.append(dict(report_id=rid,criterion=code,source_anchor=r['anchor'],first_review_basis=r['criterion_rationale'],criterion_check_required=reason,reviewer='Codex-GroupB',status='bounded source evidence available; criterion-specific independent validation pending',independent_vote='',checker='',checked_at_utc='',final_decision='pending'))
write('report_validation_queue.csv',tasks);write('fulltext_criteria.csv',criteria)
p=refresh();validate();print(json.dumps(p,indent=2))

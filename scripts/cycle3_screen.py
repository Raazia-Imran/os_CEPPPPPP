"""Conservative metadata-assisted recommendations, not final decisions."""
import csv,json,re,hashlib,os
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];E=R/'evidence';TS=datetime.now(timezone.utc).isoformat(timespec='seconds')
def read(p):return list(csv.DictReader(p.open()))
def write(p,rows,fields=None):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
private=Path(os.environ['OS_CEP_PRIVATE_RECORDS']);raw=read(private);public=read(E/'records.csv')
assert [(r['record_id'],r['canonical_record_id']) for r in raw]==[(r['record_id'],r['canonical_record_id']) for r in public]
by={r['record_id']:r for r in raw};screen=read(E/'screening.csv');votes=read(E/'title_votes.csv');human=read(E/'human_validation_queue.csv');audit=read(E/'cycle3_metadata_audit.csv') if (E/'cycle3_metadata_audit.csv').exists() else [];added=0
gpu=re.compile(r'\bgpus?\b|graphics processing|cuda|nvidia|rocm',re.I)
inf=re.compile(r'inferen|model.serv|deep.learn|neural.network|\bdnn\b|\bllm\b',re.I)
review=re.compile(r'\bsurvey\b|systematic (?:literature )?review|\breview of\b|\ba review\b|bibliometric',re.I)
for s in screen:
 if s['reviewer_1_vote']:continue
 r=by[s['record_id']];text=r['title']+' '+r['abstract'];vote='';criterion='';reason=''
 if r['entry_type']=='CHAP' and not re.search('conference|proceedings',r['venue'],re.I):
  vote='exclude_recommendation';criterion='EC1';reason='Imported book-chapter type rather than the required full conference/journal primary report. Preliminary publication-type check; independent confirmation pending.'
 elif review.search(r['title']):
  vote='exclude_recommendation';criterion='EC1';reason='Title explicitly identifies a survey/review, not an eligible primary report. Retain separately for context/citation leads; independent confirmation pending.'
 elif gpu.search(text) and inf.search(text):
  vote='retain_or_uncertain';reason='Exported title/abstract contains GPU and ML/inference context. Sharing scope, concurrent tenants and separable inference still require assessment; not final eligibility.'
 audit.append(dict(record_id=s['record_id'],doi=r['doi'],title=r['title'],gpu_context_present=bool(gpu.search(text)),ml_context_present=bool(inf.search(text)),abstract_available=bool(r['abstract']),source_file=r['source_file'],source_position=r['source_position'],action=vote or 'left_awaiting_first_recommendation',assessor='Codex-GroupB rules-assisted',checked_at_utc=TS))
 if not vote:continue
 s.update(reviewer_1_vote=vote,screening_decision='preliminary_exclude' if criterion else 'preliminary_retain_or_uncertain',criterion=criterion,reason=reason,fulltext_status='not_sought',final_decision='pending',batch_id='C3-METADATA-01',priority='high' if not criterion else 'low',triage_basis='Exported title/abstract or publication-type rule; independent review pending')
 # Add assessor fields without overwriting existing real reviewer data.
 s.update(first_assessor='Codex-GroupB rules-assisted',first_assessed_at_utc=TS)
 votes.append(dict(record_id=s['record_id'],stage='title_abstract_metadata',reviewer='Codex-GroupB rules-assisted',date=TS[:10],vote=vote,criterion=criterion,reason=reason,source=r['source_file']+':record'+r['source_position']+':title/abstract/type',second_vote='',final_decision='pending',recommendation='exclude' if criterion else 'uncertain',timestamp_utc=TS,abstract_status='publisher RIS abstract' if r['abstract'] else 'unavailable',fulltext_status='not_sought',batch_id='C3-METADATA-01',method='Conservative explicit-publication-type or positive-context rules; no exclusion from absent keyword'))
 if not criterion and not any(x['record_id']==s['record_id'] for x in human):human.append(dict(record_id=s['record_id'],priority=2,title=r['title'],doi=r['doi'],recommendation='',abstract_status='publisher RIS abstract' if r['abstract'] else 'unavailable',fulltext_status='not_sought',reason=reason,assigned_role='human screening checker',independent_vote='',criterion='',checked_at_utc='',final_decision='pending'))
 added+=1
write(E/'screening.csv',screen);write(E/'title_votes.csv',votes);write(E/'human_validation_queue.csv',human)
write(E/'cycle3_metadata_audit.csv',list({x['record_id']:x for x in audit}.values()))
write(E/'new_import_queue.csv',[s for s in screen if not s['reviewer_1_vote']],list(screen[0]))
print(json.dumps(dict(new_recommendations=added,remaining_first_recommendations=sum(not s['reviewer_1_vote'] for s in screen),existing_recommendations_untouched=True)))

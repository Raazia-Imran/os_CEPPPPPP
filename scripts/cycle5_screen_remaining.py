"""Finish the first automated triage pass; uncertainty is never final inclusion."""
import csv,json,re,hashlib
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];E=R/'evidence';TS=datetime.now(timezone.utc).isoformat(timespec='seconds')
def read(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def write(p,rows,fields):
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
raw=read(R.parent/'private_cycle3/records.csv');by={x['record_id']:x for x in raw}
screen=read(E/'screening.csv');votes=read(E/'title_votes.csv');audit=[]
baseline=hashlib.sha256((E/'screening.csv').read_bytes()).hexdigest()
for s in screen:
 if s['reviewer_1_vote']:continue
 r=by[s['record_id']];title=r['title'];text=title+' '+r['abstract'];criterion=''
 gpu=bool(re.search(r'\bGPU\b|\bGPUs\b|graphics processing|\bCUDA\b|\bNVIDIA\b|\bROCm\b',text,re.I))
 review=bool(re.search(r'\bsurvey\b|\breview\b|bibliometric',title,re.I))
 nongpu=re.search(r'\b(FPGA|FPGAs|ASIC|ASICs|microcontroller|microcontrollers|CPU-only|TPU|TPUs|photonic|quantum computing|DNA computing|neuromorphic)\b',title,re.I)
 unrelated=re.search(r'\b(soil|irrigation|wastewater|concrete|corrosion|catalyst|catalysts|photocatalytic|electrochemical|lithium-ion|lithium ion|crop|crops|seismic|pharmacokinetic|drug delivery|molecular dynamics|blood glucose|tumor segmentation|tumour segmentation)\b',title,re.I)
 if review:criterion='EC1';reason='Title explicitly identifies a review/survey; context source rather than primary eligible report.'
 elif nongpu and not gpu:criterion='EC5';reason='Title explicitly targets '+nongpu.group(0)+'; exported abstract contains no GPU evidence. Automated exclusion proposal; source verification not final.'
 elif unrelated and not gpu:criterion='EC5';reason='Title explicitly concerns '+unrelated.group(0)+' application/domain; supplied title/abstract has no GPU-platform evidence. Automated exclusion proposal, not final eligibility.'
 else:reason='Automated pass cannot establish conjunctive IC1-IC6 from supplied metadata. Retain as uncertain for source assessment; absence of keywords is not an exclusion.'
 vote='exclude_recommendation' if criterion else 'retain_or_uncertain'
 s.update(reviewer_1_vote=vote,screening_decision='AI_preliminary_exclude' if criterion else 'AI_uncertain_source_assessment_pending',criterion=criterion or 'IC1-IC6 pending',reason=reason,first_assessor='Codex-GroupB automated triage',first_assessed_at_utc=TS,batch_id='C5-TRIAGE-01',final_decision='pending')
 v={k:'' for k in votes[0]};v.update(record_id=s['record_id'],stage='title_abstract_automated_triage',reviewer='Codex-GroupB automated triage',date=TS[:10],vote=vote,criterion=s['criterion'],reason=reason,source=r['source_file']+':record'+r['source_position'],final_decision='pending',timestamp_utc=TS,method='Explicit review/non-GPU-domain rules; all other records uncertain; no final full-text decision',batch_id='C5-TRIAGE-01');votes.append(v)
 audit.append(dict(record_id=s['record_id'],doi=r['doi'],basis='title plus exported abstract text' if r['abstract'] else 'title only; abstract absent',abstract_text_characters=len(r['abstract']),abstract_completeness='not_verified',source_file=r['source_file'],source_position=r['source_position'],source_hash=r['source_hash'],recommendation=vote,criterion=s['criterion'],reason=reason,assessor='Codex-GroupB automated triage',checked_at_utc=TS,final_decision='pending'))
write(E/'screening.csv',screen,list(screen[0]));write(E/'title_votes.csv',votes,list(votes[0]));write(E/'cycle5_triage_audit.csv',audit,list(audit[0]));write(E/'new_import_queue.csv',[],list(screen[0]))
from collections import Counter
counts=dict(Counter(x['reviewer_1_vote'] for x in screen))
(E/'cycle5_triage_validation.json').write_text(json.dumps(dict(new_automated_triage_rows=len(audit),baseline_screening_sha256=baseline,total_records=len(screen),recommendations=counts,final_decisions=dict(Counter(x['final_decision'] for x in screen)),note='100% first automated triage coverage is not 100% abstract verification or final screening.'),indent=2)+'\n')
print(json.dumps(dict(new=len(audit),counts=counts)))

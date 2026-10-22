"""Apply explicitly read record judgments without filling human votes or final decisions."""
from pathlib import Path
import csv,json,datetime,hashlib,collections,sys
d=Path(__file__).resolve().parent
batch=sys.argv[1]; judgments=json.loads((d/f'batch{batch}_judgments.json').read_text())
q=list(csv.DictReader((d/'Working_559_Queue.csv').open(newline='')))
now=datetime.datetime.now(datetime.timezone.utc).isoformat();rows=[]
for x in q:
 if x['Record ID'] not in judgments:continue
 rec,code,reason,nxt=judgments[x['Record ID']]
 abstract=x['Recovered abstract'] or x.get('Supplemental abstract','')
 assert abstract and not x['Preparation recommendation'],x['Record ID']
 sha=hashlib.sha256(abstract.encode()).hexdigest()
 anchor=('Frozen Remaining_559_Screening_Queue.csv / '+x['Record ID']+' / Recovered abstract') if x['Recovered abstract'] else (x['Supplemental abstract source']+' / '+x['Record ID']+' / identity-matched abstract; primary verification pending')
 rows.append({'Batch':'B'+batch,'Record ID':x['Record ID'],'Title':x['Title'],'DOI':x['DOI'],'Frozen year':x['Year'],'Stage':'Abstract review of recovered metadata','Recommendation':rec,'Criterion to check':code,'Rationale':reason,'Next action':nxt,'Evidence anchor':anchor,'Abstract SHA256':sha,'Reviewer role':'Prepared source-based first-pass assessment; not an independent human vote','Checked UTC':now,'Independent human vote':'','Final eligibility':'Pending','Full text assessed':False})
 x.update({'Preparation status':'Abstract reviewed; independent/full-text checks pending','Preparation recommendation':rec,'Preparation criterion':code,'Preparation rationale':reason,'Preparation next action':nxt,'Preparation checked UTC':now})
def write(path,rr):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
assert len(rows)==len(judgments)
write(d/f'Batch_{batch}_Abstract_Review.csv',rows);write(d/'Working_559_Queue.csv',q)
assert all(not x[k] for x in q for k in ['Initial decision','Independent decision','Adjudicated decision'])
snap=json.loads((d/'frozen_snapshot.json').read_text())
for p,sha in snap['sha256'].items():assert hashlib.sha256((d.parents[1]/p).read_bytes()).hexdigest()==sha,p
reviewed=[x for x in q if x['Preparation recommendation']];remaining=[x for x in q if not x['Preparation recommendation']]
prior=json.loads((d/'progress.json').read_text())
progress={'built_utc':now,'frozen_commit':snap['commit'],'queue_records':len(q),'abstracts_available_in_initial_queue':sum(bool(x['Recovered abstract']) for x in q),'supplemental_abstracts_recovered':sum(bool(x.get('Supplemental abstract')) for x in q),'abstracts_reviewed_total':len(reviewed),'latest_batch':batch,'latest_batch_size':len(rows),'recommendations':dict(collections.Counter(x['Preparation recommendation'] for x in reviewed)),'remaining_initial_abstract_reviews':len(remaining),'remaining_with_recovered_abstracts':sum(bool(x['Recovered abstract'] or x.get('Supplemental abstract')) for x in remaining),'remaining_without_recovered_abstracts':sum(not(x['Recovered abstract'] or x.get('Supplemental abstract')) for x in remaining),'new_full_text_eligibility_assessments':prior.get('new_full_text_eligibility_assessments',0),'new_included_studies':0,'frozen_unique_studies':20,'independent_human_votes':0,'prisma_changed':False,'frozen_artifact_hashes_unchanged':True}
(d/'progress.json').write_text(json.dumps(progress,indent=2)+'\n');print(json.dumps(progress,indent=2))

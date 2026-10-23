"""Record title-only recommendations without treating missing abstracts as exclusions."""
from pathlib import Path
import csv,json,datetime,hashlib,collections,sys
d=Path(__file__).resolve().parent;b=sys.argv[1];j=json.loads((d/f'title_batch{b}_judgments.json').read_text());q=list(csv.DictReader((d/'Working_559_Queue.csv').open(newline='')));now=datetime.datetime.now(datetime.timezone.utc).isoformat();rows=[]
for x in q:
 if x['Record ID'] not in j:continue
 assert not x['Preparation recommendation'] and not(x['Recovered abstract'] or x.get('Supplemental abstract')),x['Record ID']
 rec,criterion,reason=j[x['Record ID']];anchor='Frozen queue title/DOI/year/URL only; no abstract or full text assessed for this recommendation'
 evidence=json.dumps({k:x[k] for k in ['Record ID','Title','DOI','Year','URL']},sort_keys=True,ensure_ascii=False)
 rows.append({'Batch':'T'+b,'Record ID':x['Record ID'],'Title':x['Title'],'DOI':x['DOI'],'Recommendation':rec,'Criterion to check':criterion,'Rationale':reason,'Evidence kind':'Title and metadata only','Evidence anchor':anchor,'Title metadata SHA256':hashlib.sha256(evidence.encode()).hexdigest(),'Checked UTC':now,'Next action':'Retrieve primary abstract or full text; verify criterion and identity. Independent review and final eligibility pending.','Independent human vote':'','Final eligibility':'Pending'})
 x.update({'Preparation status':'Title-only assessment; abstract/full-text and independent checks pending','Preparation recommendation':rec,'Preparation criterion':criterion,'Preparation rationale':reason,'Preparation next action':'Retrieve primary abstract or full text and verify scope/identity; missing abstract is not an exclusion.','Preparation checked UTC':now})
def write(path,rr):
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
assert len(rows)==len(j);assert all(not x[k] for x in q for k in ['Initial decision','Independent decision','Adjudicated decision'])
write(d/f'Title_Batch_{b}_Review.csv',rows);write(d/'Working_559_Queue.csv',q)
p=json.loads((d/'progress.json').read_text());reviewed=[x for x in q if x['Preparation recommendation']];p.update({'built_utc':now,'initial_record_recommendations_total':len(reviewed),'title_only_assessments_prepared':sum(x['Preparation status'].startswith('Title-only') for x in q),'recommendations_all_evidence_levels':dict(collections.Counter(x['Preparation recommendation'] for x in reviewed)),'records_without_preparation_recommendation':len(q)-len(reviewed),'title_abstract_stage_closed':False,'all_full_text_eligibility_closed':False});(d/'progress.json').write_text(json.dumps(p,indent=2)+'\n');print({k:p[k] for k in ['initial_record_recommendations_total','title_only_assessments_prepared','records_without_preparation_recommendation','recommendations_all_evidence_levels']})

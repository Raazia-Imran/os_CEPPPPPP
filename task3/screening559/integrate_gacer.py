from pathlib import Path
import csv
d=Path(__file__).resolve().parent;p=d/'eligibility_cycle2';rid='R00647'
def read(path):return list(csv.DictReader(path.open(newline='')))
def append(name, rr):
 path=d/name;old=read(path);fields=list(old[0]);old=[x for x in old if x.get('Record ID')!=rid]
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(old+rr)
s=read(p/'GACER_Source.csv')[0]
append('Full_Text_Source_Register.csv',[{'Record ID':rid,'Candidate name':'GACER','DOI':s['DOI'],'Source URL':s['Source URL'],'Access result':s['Access result'],'Source SHA256':s['Source SHA256'],'PDF pages':s['PDF pages'],'Checked UTC':s['Checked UTC'],'Reading copy':'Local private reading copy; not redistributed','Stage':'Final source eligibility under M2026-10-23'}])
append('Full_Text_Eligibility_Prepared.csv',[{'Record ID':rid,'Candidate name':'GACER','Criterion':x['Criterion'],'Prepared judgment':'Meets criterion on inspected full text','Evidence':x['Evidence'],'Anchor':x['Anchor'],'Source URL':s['Source URL'],'Source SHA256':s['Source SHA256'],'Checked UTC':x['Checked UTC'],'Independent vote':'','Adjudicated eligibility':'Pending','Assigned new study ID':''} for x in read(p/'GACER_Eligibility.csv')])
append('Candidate_QA_Prepared.csv',[{'Record ID':rid,'Criterion':x['Criterion'],'Prepared score':x['Score'],'Maximum':x['Applicable maximum'],'Rationale':x['Rationale'],'PDF anchor':x['Anchor'],'Checked UTC':x['Checked UTC'],'Appraisal status':'Final source appraisal; reasonedN/A retained; no independent vote','Independent score':'','Adjudicated score':''} for x in read(p/'GACER_QA.csv')])
append('Candidate_Outcomes_Prepared.csv',[{k:x[k] for k in read(d/'Candidate_Outcomes_Prepared.csv')[0]} for x in read(p/'GACER_Outcomes.csv')])
ref=read(p/'GACER_Reference.csv')[0]
append('New_Included_References.csv',[{'Record ID':rid,'Study ID':'S027','Report ID':'P030','Authors':ref['Authors'],'Title':ref['Title'],'Venue':ref['Venue'],'Year':ref['Year'],'Pages':'1-9','DOI':ref['DOI'],'Primary text URL':ref['Primary URL'],'Primary evidence hash':ref['Primary SHA256'],'Metadata URL':'https://doi.org/'+ref['DOI'],'Verification':'Final first page; four authors and9pages; differs from2023preprint; venue/index year distinct'}])
allrefs=read(d/'New_Included_References.csv')
(d/'New_Included_References.bib').write_text('\n\n'.join('@inproceedings{'+x['Study ID'].lower()+',\n author={'+x['Authors']+'},\n title={'+x['Title']+'},\n booktitle={'+x['Venue']+'},\n year={'+x['Year']+'},\n pages={'+x['Pages'].replace('-','--')+'},\n doi={'+x['DOI']+'},\n url={'+x['Primary text URL']+'}\n}' for x in allrefs)+'\n')
print('GACER source, six criteria, ten QA items and four outcomes integrated.')

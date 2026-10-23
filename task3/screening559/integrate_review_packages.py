"""Adopt complete, explicitly assessed source packages using stable IDs.

Package existence alone is not eligibility: all six checks and ten appraisal rows
must have source evidence. Frozen reports, workbook and protocol are not edited.
"""
from pathlib import Path
import csv,json
d=Path(__file__).resolve().parent
def read(p):return list(csv.DictReader(p.open(newline='')))
def replace_rows(name,rid,rows):
    path=d/name;old=read(path);fields=list(old[0]);old=[x for x in old if x.get('Record ID')!=rid]
    assert all(not set(x)-set(fields) for x in rows),(name,'Unexpected fields')
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(old+rows)

configs=[('eligibility_cycle3/elasticroom','Source.csv','Eligibility.csv','QA.csv','Outcomes.csv','Reference.csv','ElasticRoom'),
         ('eligibility_cycle3/split','SPLIT_Source.csv','SPLIT_Eligibility.csv','SPLIT_QA.csv','SPLIT_Outcomes.csv','SPLIT_Reference.csv','SPLIT'),
         ('eligibility_cycle4','Source.csv','Eligibility.csv','QA.csv','Outcomes.csv','Reference.csv','KACE')]
adopted=[]
for folder,sn,en,qn,on,rn,name in configs:
    root=d/folder;s=read(root/sn)[0];ref=read(root/rn)[0];ec=read(root/en);qa=read(root/qn);out=read(root/on)
    rid=s['Record ID'];sid=ref['Study ID'];pid=ref['Report ID'];now=s['Checked UTC']
    assert {x['Criterion'] for x in ec}=={'IC'+str(i) for i in range(1,7)}
    assert all(x['Final decision']=='Met' and x['Evidence'] and x['Anchor'] for x in ec)
    assert {x['Criterion'] for x in qa}=={'Q'+str(i) for i in range(1,11)}
    assert all(x['Rationale'] and x['Anchor'] and (x['Score']=='N/A' and x['Applicable maximum']=='0' or 0<=int(x['Score'])<=int(x['Applicable maximum'])<=2) for x in qa)
    assert out and all(x['Anchor'] and x['Interpretation limit'] for x in out)
    assert all(x['Source SHA256']==s['Source SHA256'] for x in ec+qa)
    replace_rows('Full_Text_Source_Register.csv',rid,[{'Record ID':rid,'Candidate name':name,'DOI':s['DOI'],'Source URL':s['Source URL'],'Access result':s['Access result'],'Source SHA256':s['Source SHA256'],'PDF pages':s['PDF pages'],'Checked UTC':now,'Reading copy':'Private reading copy; access route recorded above; PDF not redistributed','Stage':'Final source eligibility under M2026-10-23'}])
    replace_rows('Full_Text_Eligibility_Prepared.csv',rid,[{'Record ID':rid,'Candidate name':name,'Criterion':x['Criterion'],'Prepared judgment':'Meets criterion on inspected full text','Evidence':x['Evidence'],'Anchor':x['Anchor'],'Source URL':s['Source URL'],'Source SHA256':s['Source SHA256'],'Checked UTC':x['Checked UTC'],'Independent vote':'','Adjudicated eligibility':'Pending','Assigned new study ID':''} for x in ec])
    replace_rows('Candidate_QA_Prepared.csv',rid,[{'Record ID':rid,'Criterion':x['Criterion'],'Prepared score':x['Score'],'Maximum':x['Applicable maximum'],'Rationale':x['Rationale'],'PDF anchor':x['Anchor'],'Checked UTC':x['Checked UTC'],'Appraisal status':'Final source appraisal; reasoned N/A retained; no independent vote','Independent score':'','Adjudicated score':''} for x in qa])
    replace_rows('Candidate_Outcomes_Prepared.csv',rid,[{k:x[k] for k in read(d/'Candidate_Outcomes_Prepared.csv')[0]} for x in out])
    replace_rows('New_Included_References.csv',rid,[{'Record ID':rid,'Study ID':sid,'Report ID':pid,'Authors':ref['Authors'],'Title':ref['Title'],'Venue':ref['Venue'],'Year':ref['Year'],'Pages':ref.get('Pages','1-'+s['PDF pages']),'DOI':ref['DOI'],'Primary text URL':ref['Primary URL'],'Primary evidence hash':ref['Primary SHA256'],'Metadata URL':'https://doi.org/'+ref['DOI'],'Verification':ref['Version']+'; '+ref['Date basis']}])
    adopted.append({'Record ID':rid,'Study ID':sid,'Report ID':pid,'Name':name,'QA points':sum(int(x['Score']) for x in qa if x['Score']!='N/A'),'QA maximum':sum(int(x['Applicable maximum']) for x in qa),'Outcomes':len(out)})
allrefs=read(d/'New_Included_References.csv')
(d/'New_Included_References.bib').write_text('\n\n'.join('@inproceedings{'+x['Study ID'].lower()+',\n author={'+x['Authors']+'},\n title={{'+x['Title']+'}},\n booktitle={'+x['Venue']+'},\n year={'+x['Year']+'},\n pages={'+x['Pages'].replace('-','--')+'},\n doi={'+x['DOI']+'},\n url={'+x['Primary text URL']+'}\n}' for x in allrefs)+'\n')
print(json.dumps(adopted))

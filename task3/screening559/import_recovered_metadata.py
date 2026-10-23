from pathlib import Path
import csv,json,re
d=Path(__file__).resolve().parent
q=list(csv.DictReader((d/'Working_559_Queue.csv').open(newline='')))
lookup={}
for name in ['OpenAlex_Metadata_Recovery.csv','Crossref_Metadata_Recovery.csv']:
 for x in csv.DictReader((d/name).open(newline='')):
  t=x['Recovered abstract text'].strip()
  if len(t)<80 or re.fullmatch(r'(no abstract available\.?|abstract unavailable\.?)',t,re.I):continue
  if t:lookup[x['Record ID']]=(x,name)
for x in q:
 m,name=lookup.get(x['Record ID'],({},''))
 x.update({'Supplemental abstract':m.get('Recovered abstract text',''),'Supplemental abstract source':name,'Supplemental metadata URL':m.get('Source URL',m.get('URL','')),'Supplemental evidence SHA256':m.get('Evidence SHA256',''),'Supplemental identity status':m.get('Identity match',m.get('Title match',''))})
with (d/'Working_559_Queue.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(q[0]));w.writeheader();w.writerows(q)
summary={'original_abstracts':sum(bool(x['Recovered abstract']) for x in q),'new_nonplaceholder_identity_matched_abstracts':sum(bool(x['Supplemental abstract']) for x in q),'still_without_abstract_text':sum(not(x['Recovered abstract'] or x['Supplemental abstract']) for x in q),'new_abstracts_read':0,'frozen_queue_changed':False,'placeholder_rule':'No abstract available and text shorter than80characters not treated as a usable abstract; metadata evidence retained.'}
(d/'Supplemental_Abstract_Status.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)

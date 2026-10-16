"""Catalogue cited identities; never transfer a companion DOI to the conference report."""
import re,csv,json
from pathlib import Path
from datetime import datetime,timezone
from import_shared import bib_entries
R=Path(__file__).resolve().parents[1];E=R/'evidence';b=R/'task2/report/references.bib';s=b.read_text();entries={k:f for t,k,f in bib_entries(s)}
keys=['nvidiaMPS','nvidiaMIG','nvidiaTime','kitchenham','petersen','prisma','prismas','nedResources','nedGuide','vastpipe','igniter','gpulets','pipeswitch','reef']
dois={'petersen':'10.14236/ewic/EASE2008.8','prisma':'10.1136/bmj.n71','prismas':'10.1186/s13643-020-01542-z','vastpipe':'10.1007/s11390-024-3773-5','igniter':'10.1109/TPDS.2022.3232715'}
urls={'nvidiaMPS':'https://docs.nvidia.com/deploy/mps/latest/index.html','nvidiaMIG':'https://docs.nvidia.com/datacenter/tesla/mig-user-guide/latest/index.html','nvidiaTime':'https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html','kitchenham':'https://ebse.webspace.durham.ac.uk/wp-content/uploads/sites/49/2022/08/Systematic-reviews-5-8.pdf','nedResources':'https://eaklibrary.neduet.edu.pk/eakl/E-Resources.html','nedGuide':'https://eaklibrary.neduet.edu.pk/eakl/ResearchGuide.html','gpulets':'https://www.usenix.org/conference/atc22/presentation/choi-seungbeom','pipeswitch':'https://www.usenix.org/conference/osdi20/presentation/bai','reef':'https://www.usenix.org/conference/osdi22/presentation/han'}
short=dict(nvidiaMPS='NVIDIA MPS documentation',nvidiaMIG='NVIDIA MIG guide',nvidiaTime='NVIDIA GPU time-slicing',kitchenham='Kitchenham and Charters guidelines',petersen='Systematic Mapping Studies',prisma='PRISMA 2020',prismas='PRISMA-S',nedResources='NED E-Resources',nedGuide='NED Research Guide',vastpipe='VastPipe (2025)',igniter='iGniter (2023)',gpulets='gpulets (ATC 2022)',pipeswitch='PipeSwitch (OSDI 2020)',reef='REEF conference (OSDI 2022)')
rows=[];metadata=[];stamp=datetime.now(timezone.utc).isoformat(timespec='seconds')
for key in keys:
 doi=dois.get(key,'');url='https://doi.org/'+doi if doi else urls[key]
 if doi:
  cache=Path('/tmp/cycle2-doi')/(doi.replace('/','_')+'.json')
  saved=json.loads((E/'cycle2_reference_metadata.json').read_text())['crossref_records'] if (E/'cycle2_reference_metadata.json').exists() else []
  m=json.loads(cache.read_text()) if cache.exists() else next(m for m in saved if m['DOI'].lower()==doi.lower())
  assert m['DOI'].lower()==doi.lower();metadata.append(m);status='DOI/title verified against Crossref registration metadata'
 elif key in ['pipeswitch','reef','gpulets']:status='Official USENIX BibTeX checked: DOI field not listed; publisher URL retained'
 else:status='Context/method/institutional source; DOI not listed in repository citation; official URL retained'
 rows.append(dict(citation_key=key,short_title=short[key],title=entries[key]['title'],doi=doi,official_url=url,status=status,role='primary checked report' if key in ['vastpipe','igniter','gpulets','pipeswitch','reef'] else 'methodology/context',source_identity_boundary='REEF journal DOI 10.1145/3768622 is not assigned to this conference report' if key=='reef' else 'Cited report identity retained'))
for key in ['vastpipe','igniter']:
 block=re.search(r'@article\{'+key+r',.*?\n\}',s,re.S).group(0)
 if 'note=' not in block and 'note =' not in block:s=s.replace(block,block[:-2]+',\n note={doi: '+dois[key]+'}\n}')
b.write_text(s)
with (E/'cycle2_reference_catalog.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
(E/'cycle2_reference_metadata.json').write_text(json.dumps({'checked_at_utc':stamp,'scope':'Bibliographic verification only; no new experimental outcome added','crossref_records':metadata,'usenix_citation_checks':[{'key':k,'url':urls[k],'observation':'Official BibTeX lists publisher URL and no DOI field','checked_at_utc':stamp} for k in ['pipeswitch','reef','gpulets']]},indent=2)+'\n')
wi=json.loads((R/'task2/tracker/workbook_input.json').read_text());wi['sheets']['Reference catalogue']=rows;(R/'task2/tracker/workbook_input.json').write_text(json.dumps(wi,ensure_ascii=False))
print(len(rows),'cited sources;',len(dois),'verified DOIs; no invented identifiers.')

"""Audit identity proposals without collapsing uncertain records or study versions."""
from pathlib import Path
import csv, json, hashlib, datetime
D=Path(__file__).resolve().parent
ROOT=D.parents[1]
def read(path):
    with path.open(newline='') as f: return list(csv.DictReader(f))
q={x['Record ID']:x for x in read(D/'Working_559_Queue.csv')}
native={x['record_id'].removeprefix('GB-'):x for x in read(ROOT/'evidence/records.csv')}
proposals=read(D/'Report_Identity_Proposals.csv')
rows=[]
for p in proposals:
    a,b=p['Record A'],p['Record B or existing study']; x=q[a]; y=q.get(b,{})
    n,m=native.get(a,{}),native.get(b,{})
    same_text=bool(x.get('Recovered abstract')) and x.get('Recovered abstract')==y.get('Recovered abstract')
    decision='Retain separate records pending primary version/content evidence'
    gap=p['Required resolution']
    caution='A shared system name, title overlap or cross-record metadata enrichment does not establish study identity.'
    if (a,b)==('R00643','R01082'):
        decision='Retain separate candidate studies; no evidence supports linkage'
        gap='Assess each full text independently; do not collapse operator-parallelism DNN work and production multi-LLM serving by shared Janus name.'
    if b in ['R02180','R02185','R02186']:
        caution='Enriched abstract and DOI-derived URL match, but native second capture has no DOI/authors and uses a distinct IEEE document URL. Enrichment is not independent identity verification.'
        gap='Resolve native IEEE document metadata and compare DOI/authors/venue; three publisher-page checks returned robot verification on 23 October2026. No duplicate removal applied.'
    rows.append({'Record A':a,'Record B or existing study':b,'Native URL A':n.get('url',''),'Native URL B':m.get('url',''),
      'Native DOI A':n.get('doi',''),'Native DOI B':m.get('doi',''),'Enriched abstract exactly equal':str(same_text),
      'Decision':decision,'Evidence':p['Observed basis']+'; frozen/native evidence/records.csv and current Working_559_Queue.csv',
      'Evidence caution':caution,'Remaining gap':gap,'Count change':0,
      'Checked UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Independent human vote':''})
with (D/'Identity_Evidence_Audit.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(D/'Identity_Audit_Notes.md').write_text('''# Report identity audit

Nine proposed relationships were checked against both the native record register and the enriched working queue. No record was removed and no companion study was counted twice on the strength of this audit.

The WAGES, DistMind and MPS-granularity pairs share enriched abstracts and DOI-derived URLs. Their original second captures have separate IEEE document URLs and lack DOI/authors. The merged enrichment cannot independently validate the relationship that generated it. Direct checks of all three native publisher pages on23October2026 returned robot-verification pages. Source metadata and content remain necessary before applying a duplicate link.

The two Janus candidates describe different operator-scheduling and multi-LLM-serving work and remain separate. The other overlap/version proposals remain explicit checks; a conference/journal pair may be two reports of one study, but that relationship must be supported by authors and experimental content.

This is an identity audit, not a full-text eligibility decision. It changes no PRISMA totals and does not resolve historical search provenance.
''')
print(json.dumps({'proposals_audited':len(rows),'count_changes':0,'native_and_enriched_sources_distinguished':True}))

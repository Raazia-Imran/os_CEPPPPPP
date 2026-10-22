from pathlib import Path
import csv,json,re,hashlib,datetime,collections
root=Path(__file__).resolve().parents[2]; t=root/'task3'; now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def csvwrite(p,rows):
 if isinstance(rows[0],dict):
  keys=list(dict.fromkeys(k for r in rows for k in r)); rows=[keys]+[[r.get(k,'') for k in keys] for r in rows]
 with p.open('w',newline='') as f:csv.writer(f).writerows(rows)
mem={n:load(t/n/'review_data.json') for n in ['raazia','rameen','eshaal']}
e=mem['eshaal']
# A single claim-specific calibration is applied across all three packages, with separate original values.
notes={'P002':('PDF pp8-10; interference/provisioning evaluation','Q9=2 for direct measured performance-interference evaluation within the stated service scope; this does not establish security or fault isolation.'),'P003':('PDF pp3-4,8-12; sections3 and5','Q9=2 for direct measured interference and allocation-boundary evaluation; no hostile-tenant security guarantee is inferred.'),'P005':('Conference PDF pp2-3,8-11; sections2 and5','Q9=2 for explicitly defined priority/performance protection and direct latency-interference tests; journal-only NVIDIA results remain separate.')}
for q in e['qa']:
 pid=q['Report ID'];item=q['Item ID']
 if item=='Q9' and pid in notes:q.update({'Reviewed score':2,'Reviewed maximum':2,'Rationale':notes[pid][1],'Source anchor':notes[pid][0]})
 if pid=='P003' and item=='Q10':q.update({'Reviewed score':2,'Reviewed maximum':2,'Rationale':'Artifact appendix provides versioned dependencies, Docker/build/run instructions and limitations; availability/replicability reporting is scored without claiming a local replication. Zenodo 10.5281/zenodo.6544909 and casys-kaist/glet are supplied.','Source anchor':'PDF pp17-18; artifact appendix: Ubuntu18.04/kernel4.15, LibTorch1.10, CUDA>=10.2, cuDNN>=7.6, Boost>=1.6, OpenCV>=4, CMake>=3.19'})
for src in e['sources']:
 qa=[q for q in e['qa'] if q['Report ID']==src['Report ID']]
 if qa:src['Reviewed QA']=sum(q['Reviewed score'] for q in qa if isinstance(q['Reviewed score'],(int,float)));src['Reviewed maximum']=sum(q['Reviewed maximum'] for q in qa if isinstance(q['Reviewed maximum'],(int,float)))
e['changes'].append({'Change ID':'ES10','Scope':'P002 P003 P005','Field':'QA Q9 / P003 Q10','Original':'Inherited scores retained pending common calibration','Proposed treatment':'Q9=2 for direct claim-specific performance interference tests; P003 Q10=2 for versioned artifact appendix. Original scores remain visible.','Evidence':'Source anchors in QA rows; common Q9 rubric applied without extrapolating to security/fault isolation'})
# Remove duplicate audit entry if rerun.
e['changes']=list({r['Change ID']:r for r in e['changes']}.values())
# Verify recoverable metadata and prepare an honest, unvoted queue.
d=load(t/'logs/reviewed_data.json');base=load(t/'logs/baseline_data.json');a=load(t/'logs/analysis.json')
records=list(csv.DictReader((root/'evidence/records.csv').open()))
def norm(v):return re.sub(r'[^a-z0-9]','',str(v).lower())
def doi(v):return str(v).lower().replace('https://doi.org/','').strip()
bydoi=collections.defaultdict(list);bytitle=collections.defaultdict(list)
for r in records:
 if r['doi']:bydoi[doi(r['doi'])].append(r)
 bytitle[norm(r['title'])].append(r)
for r in csv.DictReader((root/'evidence/metadata_enrichment.csv').open()):
 r.setdefault('url','https://doi.org/'+r['doi'] if r['doi'] else '');r['record_id']='enrichment:'+r['record_id'];
 if r['doi']:bydoi[doi(r['doi'])].append(r)
 bytitle[norm(r['title'])].append(r)
queue=[];sh=d['Screening Log'][0]
for row in d['Screening Log'][1:]:
 if row[4]!='retained_not_advanced_under_stopping_rule':continue
 r=dict(zip(sh,row));hits=bydoi.get(doi(row[3]),[]) if row[3] else []
 if not hits:hits=bytitle.get(norm(row[2]),[])
 abstracts={h['abstract'].strip() for h in hits if h['abstract'].strip()}; abstract=max(abstracts,key=len) if abstracts else ''
 i=len(queue);names=['Eshaal','Raazia','Rameen']
 queue.append({'Record ID':row[0],'Database':row[1],'Title':row[2],'DOI':row[3],'Year':row[11],'Baseline abstract available':row[8],'Recovered abstract':abstract,'Abstract metadata match':'DOI/title exact normalized match' if hits else 'Unmatched; verify before use','Abstract variants':len(abstracts),'Source record IDs':'; '.join(h['record_id'] for h in hits),'URL':hits[0]['url'] if hits else '', 'First reviewer':names[i%3],'Independent reviewer':names[(i+1)%3],'Initial decision':'','Initial criterion':'','Initial evidence anchor':'','Initial checked UTC':'','Independent decision':'','Independent criterion':'','Independent evidence anchor':'','Independent checked UTC':'','Adjudicated decision':'','Reason / access attempts':'','Full-text stage':'Not sought in frozen baseline'})
csvwrite(t/'logs/Remaining_559_Screening_Queue.csv',queue)
qstats={'records':len(queue),'baseline_with_abstract':sum(str(r['Baseline abstract available']).lower()=='true' for r in queue),'metadata_abstract_recovered':sum(bool(r['Recovered abstract']) for r in queue),'first_assignment':dict(collections.Counter(r['First reviewer'] for r in queue)),'decisions_entered':0,'note':'Metadata availability is not a completed screening vote. The frozen selection partition is unchanged.'};save(t/'logs/remaining_559_audit.json',qstats)
# Methodology audit: resolutions include explicit limitations, not invented events.
methods=e['methodology']
updates={
'MA01':('Resolution documented','Frozen protocol preserved; all later amendments and execution deviations are separate.','Keep submitted protocol unchanged; source hash verified in integrated validation.'),
'MA04':('Explicit limitation','559 retained records were not advanced; their full eligibility is unknown. The 20-study count does not close this branch.','Use Remaining_559_Screening_Queue.csv for two actual votes, abstract retrieval where needed, full-text attempts and IC/EC decisions. Otherwise submit a clearly bounded first draft and retain the deviation; instructor acceptance has not been evidenced.'),
'MA05':('Explicit limitation','Frozen canonical register: 2933 without abstracts and 1142 with abstracts. Current 559-row queue separately audits recoverable metadata; availability does not prove reading.','Use actual source abstracts where recoverable; request abstract/full text for uncertain records; exclude only on a supported IC/EC reason. Title-only decisions remain a limitation. See remaining_559_audit.json.'),
'MA06':('Explicit limitation','All 200 included-study QA items and 52 outcome rows have source-review entries; separate named human votes are absent.','Use teammate rotation; preserve initial independent judgments, real names/times, disagreements and adjudication. Do not copy prepared appraisals into independent-vote fields.'),
'MA07':('Explicit limitation','IEEE/Springer shared searches are attributed. Historical exact execution times and complete operator receipts remain unavailable.','Disclose reuse and missing times; recorded dates do not establish within-day times. No retrospective rerun is claimed.'),
'MA08':('Explicit limitation','ACM numbered files contribute 1582 active occurrences. Two master BibTeX files parse to 1829 entries and are not active additional occurrences. Display1600/claimed1603 versus parsed1829 and exact run mapping remain unresolved.','Retain count fields separately; do not add master records to PRISMA. Verify raw-file mapping with original collector if available.'),
'MA09':('Explicit limitation','ScienceDirect active register has1898 occurrences. MPS displayed517 versus registered563 remains unresolved. A historical full-export manifest exists, but its named archive files are absent from this checkout; four standalone samples do not replace the full archive.','Preserve manifest as historical evidence; do not assert current byte verification or export completeness. Missing archive and field/facet uncertainty remain disclosed.'),
'MA10':('Explicit limitation','Accepted query/field deviations from the submitted protocol are documented. Broad indexed fields and missing run/facet mapping cannot be reconstructed from reading copies.','Report actual preserved strings; distinguish planned versus executed searches and supplementary retrieval. No unseen run or missing filter is invented.'),
'MA11':('Explicit limitation','All20 study copies plus REEF companion are inspected. iGniter final copy is checked; REEF E018-E026 belong to conferenceP005; Tally is pinned to arXivv3. ParvaGPU final-text equivalence remains unverified.','Retain ParvaGPU manuscript-only quantitative status and IC1 version condition; no false final-version certification.'),
'MA12':('Resolution documented','Claim-specific Q9 calibration and applicable-denominator review are applied across20 forms. P003 artifact appendix supports Q10=2. Original scores remain frozen and item-level changes are logged.','Use integrated current scores; human calibration/signoff remains a separate pending step. N/A only P001Q7 and P006Q9.'),
'MA13':('Resolution documented','All52 retained outcomes source-checked across the three packages; corrected anchors, metric meanings and source-version boundaries integrated.','Do not treat reporting verification as experiment replication; named independent checks remain pending.'),
'MA14':('Resolution documented','User clarified Sir requires20 studies; docs/guidelines.md states minimum15to20. Corpus has20 unique studies/21reports because REEF conference+journal is one study.','No count-driven extra studies are required for this draft. If completing the retained queue identifies more eligible studies, include them under the predefined criteria rather than stopping at20.')}
for r in methods:
 if r['Audit ID'] in updates:r['Status'],r['Finding'],r['Next action']=updates[r['Audit ID']]
 r['Evidence']=r['Evidence']+'; integrated source-review registers / remaining_559_audit.json' if r['Audit ID'] in ['MA05','MA06','MA11','MA12','MA13'] else r['Evidence']
 r['Remaining gap']=r['Next action'] if r['Status']=='Explicit limitation' else ('Independent human confirmation remains pending' if r['Audit ID'] in ['MA12','MA13'] else 'None for the stated factual correction')
 r['Checked UTC']=now
csvwrite(t/'logs/methodology_corrections.csv',methods);csvwrite(t/'eshaal/methodology_corrections.csv',methods)
# Current overlay; preserve frozen baseline without any edits.
for name,member in mem.items():
 if name!='raazia':
  save(t/name/'review_data.json',member)
  for key,filename in [('sources','Source_and_Identity_Review.csv'),('qa','QA_Source_Review.csv'),('eligibility','Eligibility_Source_Review.csv'),('outcomes','Outcome_Source_Review.csv'),('changes','Correction_Register.csv')]:csvwrite(t/name/filename,member[key])
 for q in member['qa']:
  pid=q['Report ID'];item=q.get('Item ID',q.get('Criterion'));row=next(x for x in d['QA'][1:] if x[0]==pid and x[1]==item)
  row[2]=q['Reviewed score'];row[3]=q.get('Reviewed maximum',q.get('Maximum'));row[4]=q['Rationale'];row[5]=q['Source anchor'];row[6]=q['Source URL'];row[7]=q.get('Checked UTC',member.get('checked_utc',now))
 for o in member['outcomes']:
  row=next(x for x in d['Evidence'][1:] if x[0]==o['Evidence ID'])
  for i,key in enumerate(['Evidence ID','Report ID','Metric','Value','Units','Baseline','Hardware','Workload','Interpretation','Evidence location','Source']):row[i]=o[key]
 for el in member['eligibility']:
  pid=el['Report ID'];ic=el.get('Item ID',el.get('Criterion'));row=next(x for x in d['Eligibility'][1:] if x[0]==pid and x[2]==ic)
  # Keep original eligibility decision and qualification; replace supporting rationale/anchor only.
  row[4]=el.get('Rationale',el.get('Basis'));row[5]=el.get('Source anchor',el.get('Anchor'));row[6]=el.get('Source URL',next(s['Source URL'] for s in member['sources'] if s['Report ID']==pid))
 for src in member['sources']:
  pid=src['Report ID'];study=next((r for r in d['Studies'][1:] if r[1]==pid),None)
  if study:
   qs=[r for r in d['QA'][1:] if r[0]==pid];study[6]=sum(r[2] for r in qs if isinstance(r[2],(float,int)));study[7]=sum(r[3] for r in qs if isinstance(r[3],(float,int)));study[8]=study[6]/study[7];study[9]=src['Source URL'];study[10]=src['Version checked']
# Technical corrections integrated into study-level cards.
ex={r[1]:r for r in d['Extraction'][1:]}
for pid,membername in [(s['Report ID'],n) for n,m in mem.items() for s in m['sources'] if s['Report ID']!='P023']:
 member=mem[membername];src=next(s for s in member['sources'] if s['Report ID']==pid);row=ex[pid];row[16]=src['Source URL'];outs=[o for o in member['outcomes'] if o['Report ID']==pid];row[17]='; '.join(dict.fromkeys(o['Evidence location'] for o in outs))
ex['P018'][4]='Dell R740 host; NVIDIA V10032GB; precise CPU,OS,driver/CUDA versions not established.';ex['P018'][5]='Clockwork-based engine and InferFair estimator/feedback scheduling; no local replication claimed.';ex['P018'][6]='Table3 local example: three models R2,R3,R4; evaluated 2/3-model local experiments are separate from 4-GPU61-modelMAF trace.';ex['P018'][7]='3models in retained Table3 example';ex['P018'][8]='600requests/s total; per-model ratio3:1:2; Poisson arrivals; SLO100ms; scheduler period50ms.';ex['P018'][9]='Clockwork; MPS+Clockwork; EDF, with no-batching comparators explicitly justified.';ex['P018'][10]='524.29SLO-compliant requests/s versus Clockwork457.24; max/min slowdown unfairness1.05 versus1.50 in Table3row3:1:2.';ex['P018'][11]='Performance fairness measured as maximum/minimum model slowdown (Eq2); value near1 means more equal slowdown.';ex['P018'][12]='Security not established by fairness results';ex['P018'][13]='Fault isolation not directly tested';ex['P018'][15]='Repetition/uncertainty and exact software versions unreported; fairness is not throughput maximization or a hostile-tenant guarantee.'
ex['P019'][10]='30tested co-location pairs meet twice-soloP99 deadline; approximately5%QPS regression in low-contention cases is retained.'
ex['P020'][10]='15%prediction error causes8.09%longer makespan and2additional reconfigurations; Section4.2 local experiment, distinct from Section4.3.2simulation.'
ex['P021'][4]='AMD MI50 CU-mask emulation for kernel right-sizing; not a deployable NVIDIA MPS measurement.'
ex['P022'][5]='ONNXRuntimeGPU1.17.0; inspected arXivv3 copy';ex['P022'][10]='At10%idle-time setting, normalized total system throughput1.19 versus TGS1.65; this is not background-only throughput.'
# Avoid overwriting entire reviewed extraction cards; append precise source-context corrections.
for pid,txt in {'P003':'Pairwise90%threshold describes a distribution across tested model pairs, not P90request latency. Artifact appendix provides a versioned environment.','P005':'All retained E018-E026 values are conferenceP005/AMD-stratum outcomes. P023 is linked companion context; no journal-only NVIDIA/LLM results are spliced into these rows.','P007':'P99effect is source-described about2x; do not claim graph-extracted precision.','P001':'GPU-specific throughput only; exact rate,batch and selected quotas remain unresolved.','P015':'XSched GPU Triton case3 is Section8, PDFp14/printed683; NPU/ASIC/FPGA outcomes excluded.'}.items():ex[pid][15]+=' '+txt
for r in a['Comparability'][1:]:
 if r[0]=='CMP06':r[2]='ArkGPU ~5%low-contention QPS regression; Tally total normalized throughput1.19 versusTGS1.65';r[4]='Foreground protection can carry aggregate or co-tenant costs; Tally outcome is total system throughput.'
 if r[0]=='CMP07':r[5]='No current combined numerical rows: E018-E026 explicitly assigned to conferenceP005; journal experiments remain separate.'
for r in a['Recommendations'][1:]:
 if r[0]=='REC04':r[5]='Memory/reclamation costs and possible co-tenant regression; ArkGPU ~5%QPS loss under low contention.'
 if r[0]=='REC05':r[7]='Validate profile fit and online request tails; Dyna-P8.09%makespan penalty at15%prediction perturbation is local, not Section4.3.2simulation.'
 if r[0]=='REC06':r[4]='In Table3ratio3:1:2,total600requests/s: goodput524.29 versusClockwork457.24; unfairness1.05 versus1.50.';r[7]='Validate intended SLO/arrival mix; source uses100msSLO,50msperiod and max/min slowdown unfairness. No universal throughput advantage is inferred.'
for r in a['Research Gaps'][1:]:
 if r[0]=='G05':r[2]='ParvaGPU final-text equivalence; source Q3/Q4/Q10 reporting limits. iGniter final checked; Tallyv3 pinned.'
for r in a['Validity'][1:]:
 if r[0]=='Source version':r[1]='ParvaGPU author manuscript not compared with final text';r[3]='iGniter final checked; Tallyv3 pinned; REEF conference/journal mapping resolved';r[4]='Confirm ParvaGPU final equivalence or retain version condition.'
 if r[0]=='Reporting bias':r[3]='All52 retained outcome values/context checked; adverse findings retained';r[4]='Independent high-impact claim checks; reporting uncertainty still missing in some sources.'
a['Human Checks']=[a['Human Checks'][0],['H01','High','Close559-record scope','Dated scope decision or completed screening/full-text logs','Pending','','','20study target satisfied; bounded selection still disclosed'],['H02','Closed','Complete20study source access','All20primary copies plus REEFcompanion inspected','Completed in source-review pass','',now,'InferFair source gap closed; no missing assigned study copy'],['H03','High','Independent check of prepared claims/forms','Actual name,time,initial judgment,source anchor and adjudication','Pending','','','All200QAitems,126included-reportICitems,52outcomes have first-pass source entries'],['H04','Medium','Check final-version condition','ParvaGPU final text comparison or explicit version limitation','Pending','','','REEF mapping and iGniter final-copy checks complete; Tallyv3 pinned'],['H05','Medium','Close search evidence gaps','Original run/file/facet receipts or retained explicit limitations','Limitations documented','','','No manufactured exact times or archive byte checks']]
for r in d['Method & Deviations'][1:]:
 r[2]=r[2].replace('Three items are N/A','Two items are N/A') if isinstance(r[2],str) else r[2]
d['Method & Deviations']=[r for r in d['Method & Deviations'] if r[1]!='Task3 integrated correction']
d['Summary']=[r for r in d['Summary'] if r[0]!='Task3 integrated status']
for rr in d['Method & Deviations'][1:]:
 if rr[1]=='Quality assessment':rr[2]='Current justified N/A: P001Q7 andP006Q9; XSchedQ9 applies to directly evaluated performance protection. Original baseline unchanged; independent human votes pending.'
d['Method & Deviations'].append([len(d['Method & Deviations']),'Task3 integrated correction','20unique studies/21reports satisfy clarified20-study target. All200QAitems and52outcomes source-reviewed. Original baseline unchanged. Independent human votes,559selection branch and historical search gaps remain separately unresolved. methodology_corrections.csv gives resolutions/limitations.'])
d['Summary'].append(['Task3 integrated status','20studies;21reports;200QAitems;52outcomes source-reviewed','First draft complete as an artifact; independent signoff and exhaustive screening are not claimed.'])
for k,v in a.items():csvwrite(t/'logs'/(k.replace(' ','_')+'.csv'),v)
for k,v in d.items():csvwrite(t/'logs'/('current_'+k.replace(' ','_').replace('&','and')+'.csv'),v)
save(t/'logs/analysis.json',a);save(t/'logs/integrated_data.json',d)
# Keep reviewed_data consistent for legacy consumers; frozen baseline remains untouched.
save(t/'logs/reviewed_data.json',d)
qa_totals={r[1]:[r[6],r[7]] for r in d['Studies'][1:]}
validation={'built_utc':now,'studies':len(d['Studies'])-1,'reports':21,'qa_items':len(d['QA'])-1,'outcomes':len(d['Evidence'])-1,'included_report_criteria_source_reviewed':sum(len(m['eligibility']) for m in mem.values()),'qa_totals':qa_totals,'qa_sum':sum(v[0] for v in qa_totals.values()),'qa_max':sum(v[1] for v in qa_totals.values()),'na':[[r[0],r[1]] for r in d['QA'][1:] if r[2] is None and r[3]==0],'independent_human_signoffs':0,'queue':qstats,'protocol_sha256':hashlib.sha256((root/'task1/submitted_protocol.pdf').read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256((t/'logs/baseline_data.json').read_bytes()).hexdigest()}
assert validation['studies']==20 and validation['qa_items']==200 and validation['outcomes']==52
assert validation['included_report_criteria_source_reviewed']==126 and len(queue)==559
save(t/'logs/integration_validation.json',validation)
# Raw export audit only claims bytes currently available.
manifest=list(csv.DictReader((root/'evidence/query_export_audit.csv').open()));available=[]
for r in manifest:
 p=root/r['source_file'];available.append({'path':r['source_file'],'present':p.exists(),'historical_hash':r['sha256'],'current_hash_matches':hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'] if p.exists() else None})
save(t/'logs/export_archive_audit.json',{'checked_utc':now,'manifest_rows':len(manifest),'present':sum(x['present'] for x in available),'files':available,'limitation':'Historical manifest is retained; absent files cannot be current byte-verified. Standalone sample exports are different artifacts.'})
print(json.dumps(validation,indent=2))

from pathlib import Path
import csv,json,datetime,hashlib
r=Path('/workspace/scratch/18d5426b12a3/os_CEPPPPPP');d=r/'task3/screening559';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return list(csv.DictReader(p.open()))
def write(p,rows):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
queue={x['Record ID']:x for x in read(d/'Open_Eligibility_Queue.csv')}
all_records={x['Record ID']:x for x in read(d/'Working_559_Queue.csv')}
for rid in ['R00284','R00875']:
 if rid not in queue:queue[rid]=all_records[rid]
access=read(d/'Public_Full_Text_Access_Attempts_2026-10-24.csv');sources={x['Record ID']:x for x in access if x['Source SHA256']}
notes={
'R00284':('FreeRide','EC2: The evaluated sharing system harvests pipeline-training bubbles for model-training, graph-analytics and image-resize/watermark tasks. Section 6.1.4 enumerates the actual side workloads; section 6.2 and Tables 1-2 evaluate those workloads and training overhead/cost. No evaluated inference-serving tenant is present. MPS is used, but a GPU sharing mechanism alone does not meet the inference-serving scope. Evidence: PDF pp8-10 sections 6.1.1-6.1.5 and 6.2, Tables 1-2; p11 sections 6.3-6.5. Final ACM DOI/venue/copyright appear on p1.'),
'R00875':('Helios workload characterization','EC2: The intervention is cluster job scheduling and node power management rather than within-GPU sharing for concurrent inference tenants. Section 2.1 explicitly disables GPU oversubscription and assigns each node exclusively to one virtual cluster; section 4.2.3 evaluates trace-driven whole-job scheduling; sections 4.3.2-4.3.3 evaluate node sleep/wakeup. Inference is listed among supported workloads, but this does not establish an evaluated local inference sharing comparison. Evidence: PDF p2 sections 2.1-2.2; pp9-11 sections 4.2.3 and 4.3, Tables 3-5. Final SC2021 DOI/venue/copyright appear on p1.')}
rows=read(d/'Full_Text_Exclusions.csv');old={x['Record ID'] for x in rows};new=[]
for rid,(name,basis) in notes.items():
 src=sources[rid];p=Path('/workspace/scratch/18d5426b12a3/private_reading/queue')/(rid+'.pdf');assert hashlib.sha256(p.read_bytes()).hexdigest()==src['Source SHA256']
 if rid not in old:
  row=dict.fromkeys(rows[0],'');row.update({'Record ID':rid,'Short name':name,'Final eligibility decision':'Exclude','Basis':basis,'DOI':queue[rid]['DOI'],'Source URL':src['Attempt URL'],'Source SHA256':src['Source SHA256'],'Decision method':'Source-based eligibility assessment under M2026-10-23; no independent vote inferred','Decided UTC':now,'Applied to frozen release':'No','Working integration status':'Final full-text exclusion; no added study/report ID assigned'});rows.append(row);new.append(row)
write(d/'Full_Text_Exclusions.csv',rows)
c=d/'eligibility_cycle5';c.mkdir(exist_ok=True);write(c/'Final_Exclusions.csv',new or [x for x in rows if x['Record ID'] in notes])
checks=[]
for row in rows:
 if row['Record ID'] in notes:
  for i in range(1,7):checks.append({'Record ID':row['Record ID'],'Criterion':f'IC{i}','Judgment':'Not met' if i==2 else ('Met: English final primary conference paper' if i==1 else ('Met: publication in review window' if i==6 else 'Not used: first decisive failure IC2')),'Evidence':row['Basis'] if i==2 else ('PDF p1 publication block' if i in [1,6] else 'No inclusion/QA/extraction asserted after scope failure'),'Source URL':row['Source URL'],'Source SHA256':row['Source SHA256']})
write(c/'Eligibility.csv',checks)
(c/'README.md').write_text('# Eligibility cycle 5\n\nTwo source-based EC2 exclusions: R00284 FreeRide and R00875 Helios workload characterization. Final conference identity is printed in each retrieved PDF. Decisions use inspected methods and results, not download status or titles. The six-criterion audit stops after the first decisive scope failure; no included-study IDs, QA scores or outcome rows are assigned. PDFs are retained privately. Other retrieved texts remain open until their identities, versions and eligibility are assessed.\n')
# Describe retrieval state for every open record; absence of a route is not a failed retrieval.
status=[]
for rid,x in queue.items():
 ev=[v for v in access if v['Record ID']==rid];src=sources.get(rid)
 status.append({'Record ID':rid,'Title':x['Title'],'DOI':x['DOI'],'Retrieval this cycle':('PDF retrieved; identity/version inspection required' if src else ('Indexed routes attempted; no readable PDF recovered this cycle' if ev else 'No indexed PDF route attempted this cycle; author/publisher discovery remains')),'Attempts this cycle':len(ev),'PDF pages':src['PDF pages'] if src else '', 'Source SHA256':src['Source SHA256'] if src else '', 'Eligibility':('Closed: Exclude EC2' if rid in notes else 'Open; retrieval status is not an eligibility decision')})
write(c/'Queue_Access_Status.csv',status)
print(json.dumps({'new_exclusions':len(new),'retrieval_events':len(access),'retrieved_pdfs':len(sources),'existing_open_queue':len(queue),'expected_open_after_merge':len(queue)-len(notes)}))

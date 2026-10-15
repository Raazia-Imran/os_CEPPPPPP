"""Source-anchored Cycle 1 additions; no final eligibility or synthesis."""
import csv,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from import_shared import csvwrite,doi_key,title_key
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence'
TS=datetime.now(timezone.utc).isoformat(timespec='seconds');DATE=TS[:10]
def read(n):return list(csv.DictReader((E/n).open()))
def write(n,rows):csvwrite(E/n,rows,list(dict.fromkeys(k for r in rows for k in r)))
records=read('records.csv');by={r['record_id']:r for r in records}
# Preserve the 41-pair input. Audit decisions do not silently remove occurrence rows.
audit=read('version_review_audit.csv')
for r in audit:
    a,b=by[r['record_id']],by[r['possible_match']]
    r.update(left_authors=a['authors'] or 'unavailable in capture',right_authors=b['authors'] or 'unavailable in capture',left_venue=a['venue'] or 'unavailable in capture',right_venue=b['venue'] or 'unavailable in capture',left_year=a['year'],right_year=b['year'],reviewer='Codex-GroupB',checked_at_utc=TS,independent_checker='',linkage_applied='no',count_change='0')
    if r['review_priority']=='container_scope_audit':
        r.update(audit_disposition='container_pair_scope_classified',assessment='Both imported entry types are proceedings and titles identify whole proceedings. EC1 container recommendations remain preliminary. Different editions/identifiers are preserved; no study-level merge required.',remaining_action='Human audit of publication type; identity linkage unnecessary unless reconstructing container-level exports.')
    elif r['record_id'] in ['GB-R00149','GB-R00150','GB-R01570']:
        r.update(audit_disposition='companion_report_relationship_proposed',assessment='Same normalized title and same named authors; abstract/SIGMETRICS companion venue versus PACM full journal venue. Preserve separate report identities; prefer full PACM report only after content comparison. Different DOIs are not deterministic duplicates.',remaining_action='Compare complete report and abstract/companion content; confirm study linkage and preferred report.')
    elif r['record_id']=='GB-R01568':
        r.update(audit_disposition='identity_verified_linkage_proposed',assessment='Crossref for 10.1145/3820171.3806868 explicitly asserts is-identical-to DOI 10.1145/3801489.3806868. Authors and title match. Original occurrence identities preserved; linkage proposal awaits register reconciliation.',remaining_action='Validate metadata relation, then apply duplicate link in a separately reconciled checkpoint.')
    elif r['record_id'] in ['GB-R02190','GB-R02256']:
        doi=b['doi'];meta=Path('/tmp/oscep-metadata')/(doi.replace('/','_')+'.json');m=json.loads(meta.read_text())['message'];url=m['resource']['primary']['URL']
        assert url.rstrip('/')==a['url'].rstrip('/')
        r.update(audit_disposition='identity_verified_linkage_proposed',assessment='Registered DOI resource URL exactly equals the DOI-less IEEE capture URL; title matches. Bibliographic publication year is '+str(m['published']['date-parts'][0])+'. Year discrepancy in one export is metadata, not evidence of another study.',remaining_action='Validate primary URL identity and apply duplicate link with counts reconciled; raw metadata unchanged.')
    else:r.update(audit_disposition='unresolved_paper_identity',assessment='Compared DOI, title, available authors, venue and year. Exact title is insufficient where capture lacks authors or metadata lookup was rate limited. No merge applied.',remaining_action='Retrieve missing publisher metadata; compare authors/version/content. Keep both records pending.')
    r['status']=r['audit_disposition']+'; originals retained'
write('version_review_audit.csv',audit)
# Retain bounded primary metadata receipts, not full papers.
metadir=E/'metadata_checks';metadir.mkdir(exist_ok=True)
receipts=[]
for p in sorted(Path('/tmp/oscep-metadata').glob('*.json')):
    m=json.loads(p.read_text())['message'];d=m['DOI'];small={k:m.get(k) for k in ['DOI','title','author','container-title','type','published','relation','resource']};small.update(checked_at_utc=TS,metadata_source='https://api.crossref.org/works/'+d)
    (metadir/p.name).write_text(json.dumps(small,indent=2)+'\n')
# Re-download receipts: source PDFs remain private/local, factual extraction is public.
urls={'gpulets':'https://www.usenix.org/system/files/atc22-choi-seungbeom.pdf','pipeswitch':'https://www.usenix.org/system/files/osdi20-bai.pdf','reef':'https://www.usenix.org/system/files/osdi22-han.pdf'}
for key,url in urls.items():
    p=Path('/tmp/oscep-sources')/(key+'.pdf');assert p.is_file()
    import subprocess
    pages=subprocess.check_output(['pdfinfo',str(p)],text=True);n=int(next(l.split(':')[1] for l in pages.splitlines() if l.startswith('Pages:')))
    receipts.append(dict(report_id={'gpulets':'GB-P003','pipeswitch':'GB-P004','reef':'GB-P005'}[key],source_url=url,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),pdf_pages=n,retrieved_date_utc=DATE,receipt_checked_at_utc=TS,version='published conference PDF',local_only='yes; source PDF not committed',reviewer='Codex-GroupB'))
write('cycle1_source_receipts.csv',receipts)
ex=read('extraction.csv');existing={(x['report_id'],x['hardware'],x['workload'],x['metric'],x['value']) for x in ex}
def add(rid,mech,hw,work,base,metric,value,unit,anchor,caveat):
    key=(rid,hw,work,metric,value)
    if key in existing:return
    ex.append(dict(report_id=rid,mechanism=mech,hardware=hw,workload=work,baseline=base,metric=metric,value=value,units=unit,source_anchor=anchor,caveat=caveat,reviewer='Codex-GroupB',check_status='source_checked_first_reviewer; independent_check_pending',checked_at_utc=TS,independent_checker='',final_decision='pending',evidence_scope='one physical GPU' if rid in ['GB-P004','GB-P005'] else 'see source-specific caveat'));existing.add(key)
for hw,vals,mps in [('NVIDIA V10016GB',['6.01','5.40','10.27'],['307.02','232.25','204.52']),('NVIDIA T416GB',['5.57','7.66','34.56'],['259.20','193.05','338.25'])]:
    for model,val,mval in zip(['ResNet152','Inception_v3','Bert_base'],vals,mps):
        work=model+' inference batch8 + training batch32'
        # Preserve the already extracted V100/ResNet152 row instead of duplicating it.
        if not (hw=='NVIDIA V10016GB' and model=='ResNet152'):
            add('GB-P004','Temporal switching',hw,work,'Ready-model latency subtracted','Additional end-to-end latency',val,'ms','p509 Table3; setup p508 section6','Mean of100 runs; overhead not total latency or tail statistic; mixed training/inference workload.')
        add('GB-P004','NVIDIA MPS with unified-memory swapping',hw,work,'Ready-model latency subtracted','Additional end-to-end latency',mval,'ms','p509 Table3; setup p508 section6','Training task occupies GPU memory and continues. Baseline condition matters; not a universal MPS comparison.')
for work,metric,value,unit,caveat in [
    ('DISB A:1 VGG19 RT client100req/s uniform +1 ResNet152 BE','Overall throughput ratio','1.60','x','Includes RT and BE requests; RT-only reference dedicates GPU to RT tasks.'),
    ('DISB A:1 VGG19 RT client100req/s uniform +1 ResNet152 BE','RT end-to-end latency overhead','0.5','percent','Described as negligible; not a p99 value or worst-case guarantee.'),
    ('DISB B:1 VGG19 RT client220req/s uniform +1 ResNet152 BE','Overall throughput ratio','1.14','x','High RT load; differs from low-load DISB A.'),
    ('DISB B:1 VGG19 RT client220req/s uniform +1 ResNet152 BE','RT end-to-end latency overhead','1','percent','About60 microseconds in prose; not a tail percentile.'),
    ('DISB C-E:multiple BE clients','RT end-to-end latency overhead','<1.5','percent','Authors also state0.1ms; keep inequality and scenario range.'),
    ('DISB D:5 RT model clients20req/s uniform +5 BE model clients','Overall throughput ratio','3.00','x','About25% lower throughput than GPUStreams; latency trade-off preserved.'),
    ('DISB E:5 RT model clients20req/s Poisson +5 BE model clients','Overall throughput ratio','2.96','x','About25% lower throughput than GPUStreams; latency trade-off preserved.'),
    ('Apollo REAL trace about43 RTreq/s +5 BE model clients','Overall throughput ratio','7.7','x','Real-world trace mapped to representative DNN models; not production deployment measurement.'),
    ('Apollo REAL trace about43 RTreq/s +5 BE model clients','RT end-to-end latency overhead','<2','percent','Not a p99 latency claim or security/fault isolation test.')]:
    add('GB-P005','Reset-based kernel preemption + dynamic kernel padding','AMD MI5016GB',work,'RT-Only dedicated GPU',metric,value,unit,'p549 section7.2 Fig11 prose; setup p548 Table2',caveat)
write('extraction.csv',ex)
forms=read('study_extraction_form.csv')
updates={
'GB-P003':dict(authors='Seungbeom Choi et al.',year='2022',venue='USENIX ATC22',mechanism='MPS spatial partitions plus temporal batching; interference-aware gpulet scheduler',gpu_hardware='RTX2080Ti11GB; two GPUs/server, two servers; local pair measurements separated',cpu_memory='20-core Xeon E5-2630v4;192GB DRAM (Table2)',os_kernel='Ubuntu18.04; kernel not extracted',driver_runtime='NVIDIA440.64;CUDA10.2;PyTorch1.10 (p207 Table2)',models='GoogLeNet,LeNet,ResNet50,SSD-MobileNet,VGG16,MnasNet,MobileNetv2,DenseNet,BaseBERT (Table3)',tenant_mix='paired local inferences; system scenarios contain several models',batch_load_slo='Poisson inter-arrivals; model SLO5-202ms;99% requests within SLO; median of3 runs (pp207-208)',baseline='Solo latency for local Fig7; SBP and greedy best-fit for system scheduling',latency='Fig7 across-pair CDF threshold17.66%; not request-p90',scalability='8 logical backend servers with additional GPUs; system-level result (pp208-209)',overhead='20-second reorganization interval; overlap new proxy preparation with active serving (p207 Fig11)',limitations='Original Nexus not directly comparable; SBP ported; cross-model interference remains; no extracted security/fault test',tradeoffs='Partition and batch jointly selected; throughput numbers at system scale cannot be assigned to one GPU',source_anchor='pp201-203 local mechanism/Fig7; p207 Tables2-3;pp208-209 system methodology'),
'GB-P004':dict(authors='Zhihao Bai;Zhen Zhang;Yibo Zhu;Xin Jin',year='2020',venue='USENIX OSDI20',mechanism='Temporal task switching; pipelined model transfer; active/standby workers and shared memory daemon',gpu_hardware='V10016GB PCIe3x16;T416GB PCIe3x8',cpu_memory='V100 instance:8vCPU Xeon E5-2686v4/61GB;T4 instance:8vCPU Platinum8259CL/32GB (p508)',driver_runtime='CUDA10.1;PyTorch1.3.0;torchvision0.4.2;scipy1.3.2;driver not extracted',models='ResNet152;Inception_v3;Bert_base',tenant_mix='one training task preempted for one inference task; separable inference latency',batch_load_slo='training32;inference8;100-run averages;Fig6 reports minimum/maximum (p508)',baseline='Ready model;stop-and-start;MPS using unified memory',latency='Additional total latency versus ready model;Table3;not p99',overhead='Table3 total extra latency;Table4 first-layer startup overhead;kept separate',advantages='Reduced switching overhead for checked workloads; see extraction.csv',limitations='Mixed training/inference applicability;MPS benchmark swaps memory;modified PyTorch for all comparators;no extracted OS/driver/security/fault evidence',tradeoffs='Pipelined transfers and registered resident host models require runtime integration;inference-only multi-tenant relevance needs human eligibility check',source_anchor='p508 section6/6.1; p509 Tables3-4'),
'GB-P005':dict(authors='Mingcong Han;Hanze Zhang;Rong Chen;Haibo Chen',year='2022',venue='USENIX OSDI22',mechanism='Reset-based preemption;idempotent inference kernels;dynamic kernel padding;runtime/driver changes',gpu_hardware='AMD Radeon Instinct MI50:60CUs/16GB;REEF-N extension NVIDIA V100',cpu_memory='Intel Corei7-10700:8cores;16GB host DRAM (p548)',os_kernel='Ubuntu18.04;kernel not extracted',driver_runtime='ROCm4.3.0;ApacheTVM0.8.0;NVIDIA extension CUDA10.2',models='ResNet152;DenseNet201;VGG19;Inceptionv3;DistilBERT',tenant_mix='DISB A/B:1RT+1BE;C:1RT+5BE;D/E:5RT+5BE',batch_load_slo='Table2 RT100/220/100/20/20req/s;D uniform,E Poisson;BE closed-loop;batch not extracted',baseline='RT-Only;SEQ;GPUStreams;separate wait-based preemption microbenchmark',latency='RT end-to-end overhead below2% in REAL;no request percentile extracted',throughput='RT+BE total normalized to RT-Only;not RT-only throughput',advantages='Checked workloads retain near RT-only latency while using idle capacity for BE inference',limitations='Reset requires idempotent kernels;model-pair padding incompatibilities;conference/journal report linkage open;not security/fault isolation',tradeoffs='DISB D/E throughput about25% below GPUStreams while limiting RT latency;implementation differs on closed-source GPUs',source_anchor='p548 section7.1 Table2;p549 section7.2 Fig11;section8 idempotence limitation')}
for r in forms:
    if r['report_id'] in updates:r.update(updates[r['report_id']],field_status='Source-checked selected fields; remaining not_extracted; final eligibility and independent verification pending',checked_at_utc=TS)
    # Existing anchored outcomes support filling selected fields without rereading licensed originals.
    elif r['report_id']=='GB-P001':r.update(mechanism='tuned/default MPS comparison; prior source check only',gpu_hardware='NVIDIA A100 (existing source-check register)',models='VGG16+GoogLeNet (existing extraction rows)',baseline='No MPS / default MPS;exact quotas not extracted',checked_at_utc=TS)
    elif r['report_id']=='GB-P002':r.update(mechanism='MPS quota allocation and shadow process recovery;prior source check',gpu_hardware='NVIDIA V100 (existing source-check register)',models='AlexNet;ResNet50;VGG19;SSD',batch_load_slo='batch3 for prediction check;W1 SLO10ms for recovery example',baseline='Measured latency for prediction error;10ms SLO for recovery',checked_at_utc=TS)
write('study_extraction_form.csv',forms)
qa=read('quality.csv')
sets={
'GB-P003':[(2,'Clear SLO-aware co-location objective','p199 abstract;section1'),(2,'MPS partitions and temporal batching described','pp201-207 sections2-4'),(2,'Poisson requests;median of3 repeats;throughput/SLO procedure','pp207-208 section5.1-5.2'),(2,'Full GPU/CPU/OS/driver/runtime and model tables','p207 Tables2-3'),(2,'Ported SBP comparator and Nexus incompatibility justified','p207 section5.1'),(2,'Maximum throughput with99%SLO definition;system scale explicit','p208 section5.2'),(2,'SLO99% procedure;local overhead CDF population explicit','p203 Fig7;p208 section5.2'),(2,'Paired model interference and scheduler interference comparison','p203 Fig7;p208 Fig14'),(1,'Performance interference checked;security/fault boundary not extracted','p203 Fig7;section5.2'),(1,'Prototype and appendix setup available;replication not attempted','p207 Table2;appendixA')],
'GB-P004':[(2,'Fine-grained task-switching problem and design explicit','p499 abstract;section1'),(2,'Controller,memory daemon,workers and pipeline described','pp504-508 sections4-5'),(2,'100-run mean;min/max forFig6;setup described','p508 section6'),(1,'Hardware/software specified;OS/kernel/driver not extracted','p508 section6'),(2,'Same modified PyTorch;ready-model and swapping conditions explicit','p508 section6.1'),(2,'Inference throughput and utilization denominator defined','p509 section6.1 Fig6'),(2,'End-to-end overhead defined;mean and extrema identified','pp508-509 Table3'),(2,'Training/inference co-location;inference metric separated','pp508-509 section6.1'),(1,'Process/memory control described;security/fault testing not extracted','pp507-508 implementation'),(1,'Versioned stack described;limitations documented;replication not attempted','p508 section6;section7')],
'GB-P005':[(2,'Concurrent real-time/best-effort inference objective explicit','p539 abstract;section1'),(2,'Reset preemption,queues and padding implementation described','sections3-6;pp547-548'),(1,'Benchmark arrivals and baseline methods detailed;repeat/variance protocol not extracted','p548 section7.1'),(2,'CPU,GPU,host RAM,OS,runtime,models andclients specified','p548 section7.1 Table2'),(2,'RT-only and GPUStreams/SEQ conditions;extensions disclosed','p548 section7.1;p549 section7.3'),(2,'Total RT+BE throughput and denominator explicit','p549 section7.2 Fig11'),(1,'End-to-end latency and load specified;request percentile not extracted','pp548-549 Table2/Fig11'),(2,'MultipleRT/BE clients and multiple mixes directly tested','p548 Table2;p549 section7.2'),(1,'Performance isolation tested;no extracted memory/security/fault boundary test','pp548-549 section7.2'),(2,'Artifact and idempotence/platform limitations explicit','p540 repository;section8;appendixA')]}
present={r['report_id'] for r in qa}
for rid,items in sets.items():
    if rid in present:continue
    for i,(score,reason,anchor) in enumerate(items,1):qa.append(dict(report_id=rid,criterion='Q'+str(i),score=score,maximum=2,rationale=reason,anchor=anchor,reviewer='Codex-GroupB',second_score='',reconciled_score='',status='first_review_only',checked_at_utc=TS,independent_checker='',reconciliation_status='pending'))
write('quality.csv',qa)
# Each event is an observed reference edge, not a newly imported unique study.
sb=read('snowballing.csv')
events=[('GB-P003 gpulets','backward','Serving DNNs like Clockwork: Performance Predictability from the Bottom Up','Clockwork','p211 references[21]'),('GB-P003 gpulets','backward','Cocktail: A Multidimensional Optimization for Model Serving in Cloud','Cocktail','p211 references[22]'),('GB-P003 gpulets','backward','INFaaS: Automated Model-less Inference Serving','INFaaS','p212 references[36]'),('GB-P003 gpulets','backward','Nexus: A GPU Cluster Engine for Accelerating DNN-Based Video Analysis','Nexus','p212 references[38]'),('GB-P005 REEF','backward','PipeSwitch: Fast Pipelined Context Switching for Deep Learning Applications','PipeSwitch','p555 references[6]'),('GB-P004 PipeSwitch','forward','Microsecond-scale Preemption for Concurrent GPU-accelerated DNN Inferences','Microsecond','REEF p555 references[6] verifies later paper cites PipeSwitch;bounded forward edge, not index census')]
for i,(seed,direction,title,term,anchor) in enumerate(events,1):
    eid='C1-SB'+str(i).zfill(3)
    if any(x['event_id']==eid for x in sb):continue
    hits=[r['record_id'] for r in records if term.lower() in r['title'].lower()]
    sb.append(dict(event_id=eid,date=DATE,seed_report=seed,direction=direction,source=urls['reef'] if seed!='GB-P003 gpulets' else urls['gpulets'],anchor=anchor,candidate_title=title,existing_record_ids=';'.join(hits),status='existing record lead; eligibility pending' if hits else 'unimported lead; screening pending',coverage='Targeted citation edge; no exhaustive backward/forward coverage claimed',reviewer='Codex-GroupB',checked_at_utc=TS,doi='not resolved',final_decision='pending',screening_status='pending Group B validation',counted_as_new_database_record='no'))
write('snowballing.csv',sb)
print(json.dumps(dict(version_dispositions=dict(__import__('collections').Counter(r['audit_disposition'] for r in audit)),quality_reports=len({r['report_id'] for r in qa}),quality_items=len(qa),outcome_rows=len(ex),study_forms=len(forms),snowballing_events=len(sb)),indent=2))

"""Persist the actual bounded Group B reviewer checks; never copy final GA decisions."""
import csv,json
from pathlib import Path
from import_shared import csvwrite
E=Path(__file__).resolve().parents[1]/'evidence'
DATE='2026-10-15'
def main():
    records=list(csv.DictReader((E/'records.csv').open()));queue=list(csv.DictReader((E/'screening.csv').open()))
    # These identifiers were individually inspected in the printed high-priority title list.
    ec1={67,234,329,876,1097}
    ec2={65,99,111,135,153,180,195,260,271,302,370,382,445,448,526,617,863,1530}
    ec3={50,56,169,181,377,420}
    ec5={92,115,225,322,446,1533}
    votes=[];byid={r['record_id']:r for r in records}
    for r in queue:
        typ=byid[r['record_id']]['entry_type']
        if r['priority']!='high' and typ not in {'proceedings','book','techreport'}:continue
        n=int(r['record_id'].split('R')[1]);code=next((c for c,ids in [('EC1',ec1),('EC2',ec2),('EC3',ec3),('EC5',ec5)] if n in ids),'')
        reason={'EC1':'Title explicitly identifies a survey, poster or extended abstract; primary full report must be located separately.', 'EC2':'Title explicitly addresses training/post-training rather than separable concurrent inference evidence. Recheck abstract if mixed-workload evidence appears.', 'EC3':'Title identifies hardware/kernel/communication optimization without an identifiable tenant-sharing mechanism; abstract verification needed.', 'EC5':'Title targets CPU, FPGA, NPU or non-GPU processor; verify abstract before final exclusion.'}.get(code,'Title plausibly concerns GPU inference/sharing or is ambiguous; retain for abstract/full-text checking. No eligibility inferred from title alone.')
        if typ in {'proceedings','book','techreport'}:
            code='EC1';reason='Original BibTeX entry type '+typ+' identifies a whole container/book/report rather than an eligible full conference or journal primary paper. Metadata-based first-review recommendation; independent audit pending.'
        # All exclusions are recommendations pending abstract verification and second review.
        vote='exclude_recommendation' if code else 'retain_or_uncertain'
        r.update(reviewer_1_vote=vote,criterion=code,reason=reason,screening_decision='awaiting_abstract_and_second_review')
        votes.append(dict(record_id=r['record_id'],stage='title',reviewer='Codex-GroupB',date=DATE,vote=vote,criterion=code,reason=reason,source='records.csv:title',second_vote='',final_decision='pending'))
    csvwrite(E/'screening.csv',queue);csvwrite(E/'title_votes.csv',votes)
    ga=json.loads((E/'imports/group-a/included_studies.json').read_text())
    cross=[]
    for a in ga:
        hits=[r for r in records if r['title'].lower()==a['title'].lower() or (a.get('doi') and r['doi'].lower()==a['doi'].lower())]
        cross.append(dict(group_a_study_id=a['study_id'],title=a['title'],doi=a.get('doi',''),group_b_record_ids=';'.join(r['record_id'] for r in hits),mechanism_prior=a.get('mechanism',''),group_a_acceptance='prior assessment only',group_b_final_decision='pending',next_action='Verify IC1-IC6 and original source; score Group B Q1-Q10 independently'))
    csvwrite(E/'shared_candidate_review.csv',cross)
    # Actual source checks performed during this continuation. No second reviewer is invented.
    checks=[
      ('GB-P001','VastPipe','10.1007/s11390-024-3773-5','s11390-024-3773-5.md','pp457-459, sections6.7-6.9, Figs14-16','provisionally_eligible','Local A100 inference model pairs use tuned/default/no MPS; local GPU outcomes are separable from NPU cluster results.','Original chart check, second reviewer, exact quotas/batches, all source sections'),
      ('GB-P002','iGniter','10.1109/TPDS.2022.3232715','iGniter user-supplied Markdown','pp820-824, sections4.2,5.1-5.4, Figs13-17','provisionally_eligible','Four inference models co-located on one V100, MPS quotas and local latency prediction are explicit; fleet costs kept distinct.','Second reviewer; OS/driver extraction; full-source verification of remaining fields'),
      ('GB-P003','gpulets','','https://www.usenix.org/system/files/atc22-choi-seungbeom.pdf','pp201-203,207; sections2,3,5.1; Figs4,7; Tables2-3','provisionally_eligible','One-device paired inference interference and MPS partitioning are separable from multi-GPU scheduler results.','Second reviewer, complete outcome extraction and QA'),
      ('GB-P004','PipeSwitch','','https://www.usenix.org/system/files/osdi20-bai.pdf','pp508-509, section6.1, Tables3-4','provisionally_eligible','Separable inference latency under local training/inference co-location; temporal switching and MPS comparator.','Second reviewer; mixed training/inference scope sensitivity; complete QA'),
      ('GB-P005','REEF conference','','https://www.usenix.org/system/files/osdi22-han.pdf','p548 section7.1 Table2; pp539-542','eligible_companion_candidate','Concurrent RT/BE inference tenants on MI50; later journal report must be linked as the same study.','Verify journal equivalence before preferred-report choice; second reviewer; no double counting')
    ]
    fields=['report_id','short_name','doi','source','anchor','first_reviewer_recommendation','criterion_rationale','remaining_checks','reviewer','date','second_vote','final_decision']
    csvwrite(E/'fulltext_checks.csv',[dict(zip(fields,list(x)+['Codex-GroupB',DATE,'','pending'])) for x in checks],fields)
    extracts=[
      ('GB-P001','MPS tuned quotas','NVIDIA A100','VGG16+GoogLeNet','No MPS','Throughput ratio','2.7','x','pp457-458 Fig14 and accompanying prose','Batch/rate/quotas unresolved; not tail-latency evidence'),
      ('GB-P001','MPS tuned quotas','NVIDIA A100','VGG16+GoogLeNet','Default MPS','Throughput ratio','1.5','x','pp457-458 Fig14 and accompanying prose','Same comparison family; not a universal average'),
      ('GB-P002','MPS 25% per model','NVIDIA V100','AlexNet/ResNet50/VGG19/SSD; batch3','Measured local latency','Prediction error range','1.53-5.02','percent','p822 section5.2 Fig13','Prediction accuracy, not utilization or latency speedup'),
      ('GB-P002','MPS shadow-process recovery','NVIDIA V100','W1 with W5 and W11','W1 latency SLO10ms','Initial p99 latency','15.6','ms','p823 section5.3 Fig17 prose','Transient violation precedes recovery; no unconditional guarantee'),
      ('GB-P004','Temporal switching','NVIDIA V10016GB','ResNet152 inference batch8 + training batch32','Ready-model latency subtracted; MPS overhead307.02ms','Additional end-to-end latency','6.01','ms','p509 Table3; setup p508 section6','Mean100 runs; overhead, not total latency or p99; MPS uses unified-memory swapping'),
      ('GB-P003','MPS spatial co-location','RTX2080Ti11GB','Paired model inferences','Solo-running latency','Distribution threshold:90% of measured pairs','17.66','percent overhead below threshold','p203 Fig7','Across-pair CDF, not request-p90/p99; no hostile-memory/fault test')
    ]
    fields=['report_id','mechanism','hardware','workload','baseline','metric','value','units','source_anchor','caveat','reviewer','check_status']
    csvwrite(E/'extraction.csv',[dict(zip(fields,list(x)+['Codex-GroupB','source_checked_first_reviewer; independent_check_pending'])) for x in extracts],fields)
    # Calibration uses the Group B 0-2 meanings, never a multiplied Group A score.
    scores={
      'GB-P001':[(2,'Objective and local GPU portability question explicit','sections1,6.7'),(2,'Tuned MPS quotas and CU masking described','sections6.7-6.8'),(1,'GPU-specific repeats and variance unresolved in conversion','sections6.7-6.9'),(1,'GPU/backend named; precise GPU loads and versions incomplete','sections6.7-6.8'),(1,'Same hardware and no/default/tuned MPS; quotas incomplete','Fig14'),(2,'Throughput ratios and baseline named in prose','Fig14 and prose'),('NA','GPU-portability extraction makes no latency claim; do not score NPU latency as GPU evidence','sections6.7-6.8'),(2,'Multiple named co-located inference pairs evaluated','Figs14-16'),(1,'Performance interference considered; no separate security/fault validation extracted','sections6.7-6.8'),(1,'Stable-mix Q-table constraint; GPU replication settings incomplete','section6.9')],
      'GB-P002':[(2,'Interference-aware inference provisioning objective explicit','abstract,section1'),(2,'MPS allocation and shadow implementation described','section4.2'),(2,'Model checks repeated three times with SD; metric windows specified','sections5.1-5.3'),(1,'GPU/workloads/backend detailed; OS/driver unresolved','sections4.2,5.1'),(1,'Adapted baselines and allocation/batch differences disclosed','section5.1'),(2,'Cost, throughput, resource-allocation metrics distinguished','sections5.1,5.3'),(2,'P99 windows, SLO and recovery timing explicit','section5.3 Fig17'),(2,'Four co-located models and quota configuration specified','section5.2 Fig13'),(1,'Performance interference measured; security/fault boundaries not tested in checked portion','sections5.2-5.3'),(2,'Code, prediction limitations and PCIe caveat explicit','sections4.2,5.2')]
    }
    qa=[]
    for rid,items in scores.items():
        for i,(score,reason,anchor) in enumerate(items,1):qa.append(dict(report_id=rid,criterion='Q'+str(i),score=score,maximum=0 if score=='NA' else 2,rationale=reason,anchor=anchor,reviewer='Codex-GroupB',second_score='',reconciled_score='',status='first_review_calibration_only'))
    csvwrite(E/'quality.csv',qa)
    sb=[]
    for ref,term,title,status in [(4,'Prophet','Prophet: Precise QoS Prediction on Non-Preemptive Accelerators','older candidate; seminal justification and full text required'),(5,'Baymax','Baymax: QoS Awareness and Increased Utilization for Non-Preemptive Accelerators','older candidate; seminal justification and full text required'),(15,'Clipper','Clipper: A Low-Latency Online Prediction Serving System','context candidate; sharing eligibility unresolved'),(17,'GSLICE','GSLICE: Controlled Spatial Sharing of GPUs for a Scalable Inference Platform','already exported candidate; do not count as a new unique study')]:
        matches=[r['record_id'] for r in records if term.lower() in r['title'].lower()]
        sb.append(dict(event_id='GB-SB'+str(ref),date=DATE,seed_report='GB-P003 gpulets',direction='backward',source='https://www.usenix.org/system/files/atc22-choi-seungbeom.pdf',anchor='pp210-211 References ['+str(ref)+']',candidate_title=title,existing_record_ids=';'.join(matches),status=status,coverage='Targeted four-reference pilot; remaining bibliography and forward citation chasing pending',reviewer='Codex-GroupB'))
    csvwrite(E/'snowballing.csv',sb)
    print('Recorded',len(votes),'title votes,',len(checks),'source checks,',len(extracts),'extractions,',len(qa),'QA item scores and',len(sb),'citation links')
if __name__=='__main__':main()

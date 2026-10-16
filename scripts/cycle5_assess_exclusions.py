"""Two source-based exclusions; not a claim of complete full-text screening."""
import csv,hashlib
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R/'evidence';TS=datetime.now(timezone.utc).isoformat(timespec='seconds')
def read(n):
 with (E/n).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def save(n,rows,fields=None):
 with (E/n).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(dict.fromkeys(k for x in rows for k in x)));w.writeheader();w.writerows(rows)
checks=read('fulltext_checks.csv');criteria=read('fulltext_criteria.csv');links=read('report_record_links.csv');retrieval=read('cycle3_retrieval.csv');screen=read('screening.csv');excluded=read('fulltext_exclusions.csv');records={x['record_id']:x for x in read('records.csv')}
events=read('fulltext_decision_log.csv') if (E/'fulltext_decision_log.csv').exists() else []
cases=[('GB-P016','GB-R02285','TGS: Transparent GPU Sharing in Container Clouds for Deep Learning Workloads','tgs','https://www.usenix.org/system/files/nsdi23-wu.pdf','printed p69 abstract; evaluation pp75-80; p81 discussion; PDF pp2,8-14','Training-focused GPU container sharing; evaluation concerns production/opportunistic training jobs. Discussion explicitly places inference optimization outside this paper; no separable inference-sharing result identified.'),('GB-P017','GB-R02286','HiveD: Sharing a GPU Cluster for Deep Learning with Guarantees','hived','https://www.usenix.org/system/files/osdi20-zhao_hanyu.pdf','printed p515 abstract; section6 evaluation pp521-525; PDF pp2,8-12','GPU-cluster resource reservation and affinity for deep-learning training; evaluated queueing/completion-time behavior is not concurrent local inference serving. EC2 decisive; aggregate cluster scope is a secondary limitation.')]
for rid,record,title,key,url,anchor,reason in cases:
 if any(x['report_id']==rid for x in checks):continue
 pdf=R.parent/'private_cycle5'/(key+'.pdf');assert pdf.read_bytes().startswith(b'%PDF')
 canonical=records[record]['canonical_record_id']
 checks.append(dict(report_id=rid,short_name=title,doi='',source=url,anchor=anchor,first_reviewer_recommendation='exclude_recommendation',criterion_rationale='EC2: '+reason,remaining_checks='AI-only assessment; no independent human review claimed',reviewer='Codex-GroupB source assessment',date=TS[:10],second_vote='',final_decision='AI_exclude_fulltext'))
 for i in range(1,7):
  basis={1:'English peer-reviewed official conference PDF.',2:'GPU sharing exists, but concurrent inference-serving scope is not demonstrated.',3:'FAIL: '+reason,4:'No eligible local inference outcome identified; training/cluster results not substituted.',5:'Cluster/training scope does not establish the required local inference evidence.',6:'Within2020-2026 publication period.'}[i]
  criteria.append(dict(report_id=rid,criterion='IC'+str(i),source_anchor=anchor,first_review_basis=basis,criterion_check_required='No independent check performed',reviewer='Codex-GroupB source assessment',status='AI_assessed;IC3_failed;EC2_exclusion',independent_vote='',checker='',checked_at_utc=TS,final_decision='AI_exclude_fulltext',doi='',source_url=url))
 links.append(dict(report_id=rid,record_id=record,canonical_record_id=canonical,provisional_study_id='not_applicable_excluded_report',doi='',study_linkage_status='AI_fulltext_excluded_EC2'))
 retrieval.append(dict(candidate=key,source_url=url,checked_at_utc=TS,assessor='Codex-GroupB',retrieval_status='retrieved',sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),method='official open-access primary PDF',assessment_status='AI_fulltext_excluded_EC2',licensed_source_in_git='no'))
 excluded.append(dict(report_id=rid,record_id=record,title=title,criterion='EC2',reason=reason,source_url=url,source_anchor=anchor,assessor='Codex-GroupB source assessment',checked_at_utc=TS,decision_status='AI_fulltext_exclusion;independent_not_performed'))
 for x in screen:
  if x['record_id']==canonical:
   events.append(dict(record_id=canonical,report_id=rid,old_fulltext_status=x['fulltext_status'],new_fulltext_status='AI_assessed_exclusion_EC2',old_final_decision=x['final_decision'],new_final_decision='AI_exclude_fulltext',criterion='EC2',reason=reason,source_anchor=anchor,assessor='Codex-GroupB',checked_at_utc=TS))
   x.update(fulltext_status='AI_assessed_exclusion_EC2',final_decision='AI_exclude_fulltext')
for n,rows in [('fulltext_checks.csv',checks),('fulltext_criteria.csv',criteria),('report_record_links.csv',links),('cycle3_retrieval.csv',retrieval),('screening.csv',screen),('fulltext_exclusions.csv',excluded)]:save(n,rows)
save('fulltext_decision_log.csv',events)
print('Full-text assessments',len(checks),'source-based exclusion rows',len(excluded))

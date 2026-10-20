from pathlib import Path
import openpyxl,json,csv,hashlib,datetime
from zoneinfo import ZoneInfo
root=Path(__file__).resolve().parents[1]
w=openpyxl.load_workbook(root/'baseline/CEP_EVIDENCE_WORKBOOK.xlsx',read_only=True,data_only=True)
data={s.title:[list(r) for r in s.values if any(x is not None for x in r)] for s in w}
(root/'logs/baseline_data.json').write_text(json.dumps(data,indent=2,default=str))
for name,rows in data.items():
 with (root/'logs'/('baseline_'+name.replace(' ','_').replace('&','and')+'.csv')).open('w') as f: csv.writer(f).writerows(rows)
now=datetime.datetime.now(datetime.timezone.utc)
with (root/'logs/activity.csv').open('w') as f:
 csv.writer(f).writerows([['Activity ID','UTC time','Pakistan time','Actor','Action','Result','Evidence','Timestamp meaning'],['A001',now.isoformat(),now.astimezone(ZoneInfo('Asia/Karachi')).isoformat(),'AI assistant under user direction','Reconcile uploaded Task 2 package against GitHub main','Uploaded baseline: 21 reports / 20 studies; GitHub historical status: 15 forms. Baseline retained separately.','baseline/; GitHub a92cc23','Actual checkpoint recording time; not historical screening time']])
manifest=[]
for r in data['Source Register'][1:]:
 if r[0]=='Report version' and r[2]!='n/a': manifest.append(dict(zip(['type','report_id','study_id','title','relationship','source_url'],r)))
(root/'papers/manifest.json').write_text(json.dumps(manifest,indent=2))
(root/'README.md').write_text('''# Task 3: first full CEP draft

The supplied 18 October workbook/report supersede the older GitHub status for this Task 3 branch of work. Original Task 1 and Task 2 files remain unchanged.

## Corpus
21 included report versions map to 20 unique studies. P005 and P023 are REEF companion versions of S005. P016 (TGS) and P017 (HiveD) are excluded and do not belong in the included-paper folder. 559 retained records were not advanced under the bounded stopping rule. This is a bounded rapid review, not a completed exhaustive eligibility census.

## Phases
1. Preserve baseline and reconcile IDs/counts.
2. Retrieve the 21 reports, validate PDF identity, and record source/version/hash/access outcome.
3. Extend the workbook with activity, retrieval, provenance, synthesis, sensitivity and requirement records.
4. Benchmark journal survey argumentation; draft the full report through guideline 22, organized using 24 and audited against 23.
5. Verify files, publish and record outstanding team actions.

New activity times describe actual actions/checkpoints in UTC and Asia/Karachi. Historical batch/build times remain explicitly labeled. No second reviewer is invented.

See papers/ for the report catalogue and accessible copies, logs/ for machine-readable records, workbook/ for the expanded Excel, report/ for the first draft, and benchmark/ for the journal comparison.
''')
print('Baseline saved',len(manifest),'reports')

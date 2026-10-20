from pathlib import Path
import json, csv, datetime, hashlib
from zoneinfo import ZoneInfo

root=Path(__file__).resolve().parents[1]
now=datetime.datetime.now(datetime.timezone.utc)
activity=json.loads((root/'logs/activity.json').read_text())
activity.append(['A003',now.isoformat(),now.astimezone(ZoneInfo('Asia/Karachi')).isoformat(),'AI assistant under user direction','Recover workspace and compare repeated attachments; resume synchronized deliverables','Original sources and 18 reading PDFs recovered. New attachments match earlier SHA256 values. Rebuilding PDF and adding Word from the same source.','report/; workbook/; benchmark/README.md','Actual recovery checkpoint, not a screening event'])
(root/'logs/activity.json').write_text(json.dumps(activity,indent=2))
with (root/'logs/activity.csv').open('w',newline='') as f: csv.writer(f).writerows(activity)
body=root/'report/body.tex'
s=body.read_text()
start=s.index('The five questions retain')
end=s.index('\\section{Research methodology}',start)
questions=[
'What time-slicing, MPS, MIG and API remoting mechanisms are evaluated for concurrent inference on one GPU, and how do sharing granularity, layer and isolation boundary classify them?',
'How do studies measure utilization, throughput, density, average/tail latency, predictability and interference, and how comparable are their experimental methods?',
'Under what GPU, workload, batch, tenant mix and configuration conditions are changes in utilization, throughput, density and latency reported?',
'What resource and fault isolation properties, trade-offs, implementation costs and conflicting results are reported, and what limits the evidence?',
'Which approach or combination is supported for specified inference-serving conditions and priorities, with what confidence and alternatives?']
s=s[:start]+'The following research questions reproduce the submitted Task 1 protocol (Table 3).\n\\begin{description}\n'+''.join('\\item[RQ%d] %s\n'%(i+1,q) for i,q in enumerate(questions))+'\\end{description}\n\n'+s[end:]
body.write_text(s)
builder=root/'scripts/build_report.py'
s=builder.read_text().replace('K. Ramakrishnan','K. K. Ramakrishnan').replace('20 October 2026','21 October 2026')
builder.write_text(s)
wb=root/'scripts/build_workbook.mjs'
s=wb.read_text().replace("const root='/workspace/scratch/c8625892f6af/repo/task3';", "const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');")
s=s.replace("g.format.rowHeight=100;", "g.format.rowHeight=100;")
wb.write_text(s)
data=json.loads((root/'logs/analysis.json').read_text())
data['Benchmark'].append(['Verified journal status','2025 JIF 30.4; rank 1/146 (Q1), Computer Science Theory & Methods','https://dl.acm.org/journal/csur/indexing','Publisher search result checked '+now.isoformat()+'; journal metric, not article quality certification'])
(root/'logs/analysis.json').write_text(json.dumps(data,indent=2))
print('Restored verbatim protocol RQs and recorded recovery')

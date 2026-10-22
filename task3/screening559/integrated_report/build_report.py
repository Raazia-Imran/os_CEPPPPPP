"""Build a distinct six-addition working report; never modify the frozen report."""
from pathlib import Path
import csv, json, shutil, hashlib, re

out=Path(__file__).resolve().parent
screen=out.parent
repo=out.parents[2]
frozen=repo/'task3/report'
for name in ['main.tex','body.tex','appendices.tex','taxonomy.tex','comparisons.tex','recommendations.tex','gaps.tex','validity.tex','corpus.tex','references.bib']:
    shutil.copyfile(frozen/name,out/name)
(out/'figures').mkdir(exist_ok=True)
shutil.copyfile(repo/'task3/baseline/PRISMA_2020_FLOW_DIAGRAM.pdf',out/'figures/Frozen_PRISMA.pdf')

def read(name):return list(csv.DictReader((screen/name).open(newline='')))
elig=[x for x in read('Final_Eligibility_Decisions.csv') if x['Final eligibility decision']=='Include']
assert len(elig)==7
refs=read('New_Included_References.csv')
qa=read('Final_Candidate_QA.csv')
criteria=read('Final_Eligibility_Criteria.csv')
outcomes=read('Candidate_Outcomes_Prepared.csv')
assert len(qa)==70 and len(criteria)==42 and len(outcomes)==18

def patch(name,old,new):
    p=out/name;s=p.read_text()
    assert s.count(old)==1,(name,old[:100],s.count(old))
    p.write_text(s.replace(old,new))
def before(name,anchor,new):patch(name,anchor,new+'\n\n'+anchor)
def table(headers, rows, widths):
    spec=''.join('>{\\raggedright\\arraybackslash}p{'+str(w)+'\\textwidth}' for w in widths)
    return '\\begin{longtable}{'+spec+'}\n\\toprule\n'+' & '.join('\\textbf{'+h+'}' for h in headers)+'\\\\\\midrule\\endhead\n'+'\n'.join(' & '.join(r)+'\\\\\\addlinespace' for r in rows)+'\n\\bottomrule\\end{longtable}\n'
def tex(s):
    s=str(s)
    if re.fullmatch(r'[a-f0-9]{64}',s):return r'\nolinkurl{'+s+'}'
    if s.startswith('https://'):return r'\url{'+s+'}'
    return ''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in s)

patch('main.tex','Task 3: First Complete Draft','Task 3: Integrated Working Draft')
patch('main.tex','22 October 2026','23 October 2026')
patch('main.tex','Based on the supplied Task 2 corpus: 21 report versions, 20 unique studies.','Working corpus: 27 report versions, 26 unique studies.\\\\Frozen submission: 21 reports, 20 studies, preserved separately.')
start=(out/'main.tex').read_text();a=start.index('GPU sharing for multi-tenant inference requires');b=start.index('\\end{abstract}')
start=start[:a]+r'''GPU sharing for multi-tenant inference requires a choice among resource efficiency, request latency, isolation and implementation cost. This working review synthesizes 26 studies represented by 27 reports. The imported search register contains 4,189 occurrences and 4,075 canonical records after 114 duplicate links. In the continued 559-record branch, title/abstract screening excluded 225 records and advanced 334; six additional studies met full-text eligibility, two reports were excluded at full text, and 326 advanced records await eligibility or identity closure. These branch counts do not constitute a reconciled final whole-review PRISMA flow. The analysis uses 260 appraisal items, 66 reported observations and two transparent calculations. It combines temporal scheduling, software spatial sharing, hardware partitions, runtime/API mediation, model-memory management and hybrid controls. The evidence supports conditional selection: fine-grained control can protect request latency, while model modification, profiling, transfer bandwidth and shared-context faults constrain its use. No pooled effect or universal winner is supported. The conclusions remain limited by incomplete selection, historical search-provenance gaps, title-only screening and source-version uncertainty.
'''+start[b:];(out/'main.tex').write_text(start)

patch('body.tex','This first draft synthesizes the supplied bounded corpus of 20 studies represented by 21 reports.','This working draft integrates the frozen 20-study/21-report corpus with six source-eligible additions, giving 26 studies represented by 27 reports.')
patch('body.tex','The review is not an exhaustive census of the search results. The supplied record contains 559 retained records that were not advanced to source assessment. The first draft therefore supports candidate selection under observed conditions, while leaving the wider coverage question open. This boundary is part of the research method and must remain visible in the abstract, selection accounting and recommendations.','The review is not an exhaustive census of the search results. All 559 records in the continuation branch now have a title/abstract-stage decision: 225 exclusions and 334 advancements. Six additions and two full-text exclusions are resolved; 326 advanced records still await eligibility or report-identity closure. This draft supports candidate selection under observed conditions while the wider coverage question remains open.')
patch('body.tex',"The implemented review used a single consolidated AI-assisted assessment under team direction. The uploaded materials refer to team checking, but contain no named independent item-level votes or signed verification record. This draft therefore does not claim completion of the protocol's independent second review or report inter-rater agreement. Activity records preserve preparation provenance and actual checkpoint times. Historical batch or workbook-build times are not evidence of when a person screened a particular record.","The implemented review uses a single automated source-based assessment under team direction. For the continuation, the user reported instructor permission to rely fully on this process; amendment M2026-10-23 records that oral permission as user-reported, rather than independently inspected written approval. No independent human item-level votes or calibration are inferred. Activity records preserve actual preparation and decision times, which do not establish when a person reviewed a record.")
patch('body.tex','The source-review packages cover all 20 included studies and the REEF companion report:','The frozen source-review packages cover the original 20 studies and the REEF companion report:')
patch('body.tex','Current scores sum to 338/396 applicable points;','The original 20-study scores sum to 338/396 applicable points;')
before('body.tex',r'\subsection{Databases, search fields and period}',r'''The continuation adds 36 source-anchored inclusion-criterion judgments, 60 Q1--Q10 items and 14 outcome rows for LithOS, Abacus, Miriam, SGDRC, Pantheon and Oneiros. Their appraisal totals are respectively 17, 17, 16, 16, 16 and 17 out of 20. Combined with the original forms, the working corpus has 260 appraisal items, 162 included-report inclusion checks and 66 outcome rows. The study-level appraisal sum is 437/516 applicable points. This accounting describes reporting quality, not independent replication or a certainty-weighted effect. The six additions and their anchors appear in Appendix~\ref{app:additions} \cite{s021,s022,s023,s024,s025,s026}.''')
patch('body.tex','There are 200 appraisal items for 20 study-level forms.','There are 260 appraisal items for 26 study-level forms: 200 inherited items and 60 new source-based items.')
patch('body.tex','The 52 outcome rows and two calculations are not 54 studies.','The 66 outcome rows and two calculations are not 68 studies.')
a=(out/'body.tex').read_text();i=a.index('The supplied logs reconcile arithmetically');j=a.index('\\input{counts.tex}',i)
a=a[:i]+r'''The frozen selection logs reconcile 4,189 occurrences minus 114 duplicate links to 4,075 canonical records. Their historical partition is 3,493 screening exclusions, 559 retained records not advanced, 21 included reports and two source-assessed exclusions. That snapshot is preserved separately and is not overwritten by the continuation.

The 559-record branch now has final title/abstract-stage decisions: 225 excluded and 334 advanced. A conservative scope audit reopened 56 earlier proposed exclusions. Of the screening exclusions, 108 explicitly use title/metadata evidence alone. No record is excluded because an abstract is missing. The queue contains 235 original abstract texts plus 161 supplemental recovered texts; 163 records still lack abstract text, and five recovered texts have quality flags.

Of the 334 advanced records, six new reports met all inclusion criteria and two were excluded at full text under EC2. In-Mig evaluates cross-venue agent reasoning and routing without an extractable GPU-sharing intervention; ALL-RP evaluates social-media repost prediction, with GPU use for model training rather than concurrent inference sharing. The remaining 326 records require eligibility or identity closure. They are neither full-text exclusions nor reports declared unavailable. Duplicate and companion-report proposals remain separate identity checks.

The working included set is therefore 27 reports representing 26 studies, preserving the REEF P005/P023-to-S005 linkage. These counts do not by themselves finalize whole-review PRISMA: historical record/report mapping, source-assessment events and pending identities must be reconciled before a complete final flow is claimed. Later retrieval dates do not change the original search cutoffs. The minimum-study target is met; it is not a cap or a reason to omit further eligible studies.
'''+a[j:]
a=a.replace('{../baseline/PRISMA_2020_FLOW_DIAGRAM.pdf}','{figures/Frozen_PRISMA.pdf}')
a=a.replace('Supplied bounded-review selection flow, preserved from Task 2. Current PDF download attempts are a separate activity.','Frozen Task 2 selection flow, shown as historical provenance only. The adjacent branch table records later decisions; a reconciled final whole-review PRISMA flow remains pending.')
(out/'body.tex').write_text(a)
(out/'counts.tex').write_text(table(['Accounting scope / stage','Count'],[
('Historical identified occurrences','4,189'),('Historical duplicate links','114'),('Historical canonical records','4,075'),
('Historical original included reports / studies','21 / 20'),('Continuation records screened','559'),('Continuation screening exclusions','225'),
('Continuation advanced to retrieval / eligibility','334'),('Continuation full-text inclusions / exclusions','6 / 2'),('Advanced records with unresolved eligibility or identity','326'),
('Working included reports / unique studies','27 / 26')],[.7,.15])+r'\textbf{Stage distinctions:} $559=225+334$ and $334=6+2+326$. Advancement does not mean that all 334 reports have been retrieved or assessed. This is branch accounting, not a completed whole-review PRISMA flow.'+'\n')

before('body.tex',r'\subsection{Spatial allocation and partitions}',r'''LithOS extends temporal control with transparent kernel atomization and TPC allocation; Abacus makes operator overlap deterministic so a controller can predict concurrent-service latency. Miriam and Pantheon target edge inference, but at different intervention boundaries: elastic kernels versus chunk preemption combined with early-exit variants. They are not interchangeable implementations of the same scheduler \cite{s021,s022,s023,s025}.''')
before('body.tex',r'\input{taxonomy.tex}',r'''SGDRC dynamically controls compute and VRAM-bandwidth contention through software mechanisms, while Oneiros remaps model-parameter memory and overlaps CPU/GPU transfers to relieve multi-model memory pressure. Oneiros evaluates temporal and spatial configurations; its memory-management benefit is not a new fault-containment guarantee. SGDRC explicitly reports that its shared CUDA context cannot isolate DNN GPU-runtime failures \cite{s024,s026}.''')

rq_add={
r'\subsection{RQ2: measurements and comparability}':r'''The six additions reinforce the layered taxonomy. LithOS coordinates TPC scheduling and atomization, Abacus coordinates operator overlap, Miriam transforms kernels, Pantheon combines chunk preemption with model adaptation, SGDRC controls compute and memory bandwidth, and Oneiros controls parameter-memory residency. The enforcement point and shared state explain which mechanisms can be composed and which integration assumptions must be checked \cite{s021,s022,s023,s024,s025,s026}.''',
r'\subsection{RQ3: conditions affecting results}':r'''Pantheon's deadline-adjusted relative accuracy treats a late job as zero accuracy; it is not ordinary classification accuracy. Abacus excludes deadline-dropped queries from latency calculations while including them in QoS violations, so latency must be read with the violation population. Oneiros separates P99 time-to-first-token (TTFT), including queuing, from time-between-token (TBT), and reports throughput in generated tokens/s. None is directly interchangeable with DNN requests/s or an unspecified latency statistic \cite{s022,s025,s026}.''',
r'\subsection{RQ4: isolation and implementation cost}':r'''Miriam's RTX2060 and edge-device results differ by workload and arrival mode; the introductory latency-overhead summary is not a universal bound for the body experiments. Pantheon reports 0.39--1.10\% deadline misses for three stated application mixes, but does so with model-variant, memory and accuracy constraints. Oneiros's C1 spatial-sharing comparison reports author-averaged reductions of 65.5\% in P99 TBT and 20.7\% in P99 TTFT, with 6.6\% higher tokens/s, under the stated trace and model mix. These are within-source conditions, not transferable service guarantees \cite{s023,s025,s026}.''',
r'\subsection{RQ5: conditional selection}':r'''SGDRC's shared-context execution provides performance control without DNN runtime-fault isolation. Pantheon prioritizes deadlines by trading some model accuracy and memory residency for schedulability, and adds device power relative to its comparator. Abacus incurs profiling and predictor work. LithOS requires compatible interception and kernel behavior; Oneiros relies on high CPU/GPU transfer bandwidth and must cap remapping to avoid extra latency. These costs should be compared to the deployment's constraint, not collapsed into a single isolation or overhead score \cite{s021,s022,s024,s025,s026}.''',
r'\section{Comparative analysis}':r'''The added evidence broadens the candidate set without changing the selection rule. For predictable co-located DNN service, deterministic overlap or fine-grained priority control is a candidate when profiling and compatible kernels are acceptable. For an edge deadline objective, model-changing approaches require an explicit accuracy budget. For memory-constrained multi-LLM service on a high-bandwidth CPU/GPU system, parameter remapping is a candidate while transfer cost remains tolerable. Fault-sensitive or mutually untrusted tenants require a separately established boundary \cite{s021,s022,s023,s024,s025,s026}.'''}
for anchor,para in rq_add.items():before('body.tex',anchor,para)
patch('body.tex','The evidence table in Appendix~\\ref{app:evidence} retains all 52 supplied observations.','The evidence tables in Appendices~\\ref{app:evidence} and \\ref{app:additions} retain 52 inherited and 14 new observations, respectively.')
before('body.tex',r'\subsection{Partition control versus flexibility}',r'''\subsection{Deadlines versus model accuracy and memory}
Pantheon gives a different trade-off from a scheduler that preserves the original model unchanged: its early-exit variants reduce work when needed to protect deadlines. The reported deadline-adjusted accuracy therefore couples model quality and timeliness. Its similar utilization to RTm-DL does not establish universal utilization superiority. Miriam likewise requires workload-specific reading of throughput and critical-task latency rather than importing its introductory summary as a hard bound \cite{s023,s025}.

\subsection{Memory capacity versus transfer bandwidth}
Oneiros trades parameter residency for KV-cache capacity and asynchronous transfer. Its spatial-sharing gains occur in a stated GH200 setup and model mix; more aggressive remapping can increase average latency, and halting remapping at low load can help. This complements, rather than directly supersedes, Torpor's low-rate late-binding evidence because model scale, transfer path and metrics differ \cite{P012,s026}.''')
before('body.tex',r'\subsection{Version and engine effects}',r'''The added papers supply further within-source tensions. LithOS's plotted SLO advantage must be read with an unequal supported tenant set for some comparators. SGDRC can trade raw aggregate throughput for latency-sensitive goodput; it does not dominate every throughput baseline. Pantheon's lower deadline-miss rate coexists with model/memory changes, and its power experiment reports 10.15 W versus RTm-DL's 9.73 W. These are conditional costs, not mutually contradictory claims across unmatched systems \cite{s021,s024,s025}.''')
patch('body.tex','The 559-record unassessed branch makes that distinction essential.','The 326 unresolved advanced records make that distinction essential.')
patch('body.tex','The bounded 20-study corpus supports a conditional approach','The working 26-study corpus supports a conditional approach')
patch('body.tex',"The principal outcome is therefore a traceable selection framework, not a universal ranking. The first draft covers the instructor's analytical requirements through Section 22 and follows the suggested final-report sequence. It remains a draft: the 559-record selection branch, ParvaGPU final-version condition, historical search gaps and independent item-level checking remain open before the work is represented as a fully verified final SLR.","The principal outcome is a traceable selection framework. The 13 main report sections now integrate the six confirmed additions into taxonomy, metric interpretation, trade-offs and conditional recommendations. The work remains an evolving draft: 326 advanced records await eligibility or identity closure, whole-review PRISMA requires reconciliation, and historical search and source-version limitations remain explicit. Further eligible studies must be integrated using the same criteria, rather than stopping at the current count.")

def append_table_rows(name,rows):
    p=out/name;s=p.read_text();assert s.count('\\bottomrule\\end{longtable}')==1
    p.write_text(s.replace('\\bottomrule\\end{longtable}','\n'.join(' & '.join(row)+'\\\\\\addlinespace' for row in rows)+'\n\\bottomrule\\end{longtable}'))
append_table_rows('taxonomy.tex',[
('Fine-grained temporal / spatial control; P024 P025 P026','TPC/atomization, deterministic operator overlap and elastic kernels; compatibility and profiled workload assumptions','Kernel support, profiling, latency versus throughput'),
('Software compute/bandwidth control; P027','SM allocation and software VRAM-bandwidth control; shared CUDA context','No DNN runtime-fault isolation'),
('Model-adaptive edge preemption; P028','Chunk preemption plus early-exit variants; permitted accuracy/memory budget','Deadline behavior changes both model work and scheduler cost'),
('Parameter-memory virtualization; P029','Temporal/spatial multi-model service with asynchronous transfer; high CPU/GPU bandwidth','Transfer overhead, memory policy and isolation claims separate')])
append_table_rows('comparisons.tex',[
('CMP09 P024 / LITH-01--02. Within-source tenant-set limitation','LithOS SLO attainment100\%; normalized throughput1.0 versus MPS1.11 in the logged scenario','MIG/Limits omit BE while LithOS/MPS include it; no matched all-family ranking'),
('CMP10 P025 / ABAC rows. Population distinction','p99 improvement and peak query throughput use distinct load/settings','Deadline-dropped queries excluded from latency but counted in violations'),
('CMP11 P026 P028. Unmatched edge experiments','Elastic kernels versus model-variant/chunk preemption','Different models, platforms and accuracy semantics; not a direct winner comparison'),
('CMP12 P027 / SGDRC rows. Goodput versus raw throughput','Latency-sensitive protection with BE progress; adverse raw throughput retained','Shared context lacks runtime-fault isolation; baseline reimplementation matters'),
('CMP13 P029 / ONEI-01--03. Within-source spatial case','65.5\%lowerP99TBT;20.7\%lowerP99TTFT;6.6\%higher tokens/s','C1 model mix and traces; source averages, not a general hardware effect')])
append_table_rows('gaps.tex',[
('Model-adaptive versus model-preserving schedules','P028 changes exit/variant; P026 transforms kernels','Hold accuracy budget and input distribution constant; jointly report deadline and task quality'),
('Multi-model memory remapping and protection','P029 capacity/latency results; no fault guarantee','Measure transfer, tenant progress, tail latency and fault behavior with explicit isolation boundaries'),
('Source configuration/report inconsistencies','P025 A100 SM label; P026 platform label; P029 platform/isolation caption','Publish exact device identifiers and corrected experiment manifests')])
patch('validity.tex','Selection/stopping: No exhaustive recall or prevalence claim & Stopping branch remains visible & Instructor/team decision on bounded scope; extend if required','Incomplete eligibility: No exhaustive recall or prevalence claim & 559screening decisions preserved;56borderline proposals reopened & Close326advanced records and report identities; reconcile whole-review flow')
patch('validity.tex','All52 retained outcome values/context checked; adverse findings retained','52inherited plus14new source-anchored outcomes; adverse findings retained')
append_table_rows('validity.tex',[
('New-source reporting discrepancies','Primary labels and adverse contexts preserved in appraisal/source cautions','Clarify hardware, version and isolation-caption inconsistencies; do not silently repair source claims')])

recs=r'''
\subsubsection*{REC07: Predictable multi-model DNN co-location}
Abacus and LithOS broaden the candidate set where deterministic overlap or fine-grained resource control is compatible with the workload. Evaluate inference-only results separately from mixed training, preserve co-tenant sets, and measure profiling, host and kernel-support costs. Use a more conservative allocation when the protected service cannot tolerate the measured tail or unsupported kernels \cite{s021,s022}.

\subsubsection*{REC08: Edge deadlines with an explicit accuracy budget}
Consider Miriam for elastic-kernel coordination and Pantheon when chunk preemption and early-exit model variants are acceptable. The expected benefit is lower deadline interference under the evaluated mix; the sacrifice can include altered accuracy, extra resident variants, scheduling work and power. Prefer a model-preserving alternative when early exits violate task-quality requirements. Test nonperiodic arrivals, background progress and the actual platform rather than importing a single reported percentage \cite{s023,s025}.

\subsubsection*{REC09: Compute/bandwidth contention under a shared trust context}
SGDRC is a candidate for controlling compute and VRAM-bandwidth contention when its generated-kernel environment and shared CUDA context are acceptable. The expected benefit is latency-sensitive goodput with best-effort progress. It cannot be selected as a DNN runtime-fault boundary: that isolation is explicitly absent. Preserve cases where another baseline has greater raw throughput \cite{s024}.

\subsubsection*{REC10: Memory-constrained multi-LLM serving}
Oneiros is a candidate when a high-bandwidth CPU/GPU transfer path makes parameter remapping feasible. Its stated spatial-sharing case reports lower P99TBT/TTFT and higher tokens/s than vLLM. The sacrifice is transfer and remapping overhead; aggressive remapping can worsen average delay. Retain resident parameters or reduce remapping at low load or when transfers dominate, and establish required protection separately \cite{s026}.
'''
with (out/'recommendations.tex').open('a') as f:f.write(recs)

corpus=(out/'corpus.tex').read_text();rows=[]
for e in elig:
    ref=next(x for x in refs if x['Record ID']==e['Record ID'])
    score=sum(int(x['Final source-based score']) for x in qa if x['Record ID']==e['Record ID'] and x['Final source-based score']!='N/A')
    maximum=sum(int(x['Maximum']) for x in qa if x['Record ID']==e['Record ID'])
    rows.append((e['Study ID']+' / '+e['Report ID'],tex(e['Short name'])+' ('+str(ref['Year'])+')',str(score)+'/'+str(maximum)))
corpus=corpus.replace('\\bottomrule\\end{longtable}','\n'.join(' & '.join(row)+'\\\\\\addlinespace' for row in rows)+'\n\\bottomrule\\end{longtable}');(out/'corpus.tex').write_text(corpus)
with (out/'references.bib').open('a') as f:f.write('\n\n'+(screen/'New_Included_References.bib').read_text())

appendix=(out/'appendices.tex').read_text()
appendix=appendix.replace('\\section{Complete study appraisal and extraction cards}','\\section{Original 20-study appraisal and extraction cards}\nThe following inherited cards preserve the original source package. The six new cards are in Appendix~\\ref{app:additions}; together they cover the working 26-study corpus.')
appendix=appendix.replace('\\section{Complete outcome register}\\label{app:evidence}','\\section{Original 52-outcome register}\\label{app:evidence}\nThese inherited observations remain unchanged. The 14new observations are in Appendix~\\ref{app:additions}.')
# Replace the obsolete closing task table; keep the original exact search archive.
i=appendix.index('\\section{Files, timestamps and remaining checks}')
appendix=appendix[:i]+r'''\section{Files, timestamps and remaining checks}
The frozen report, workbook, ZIP and submitted protocol remain separate immutable artifacts. This dated working report integrates the six confirmed additions. Original timestamps retain their historical meaning. The electronic CSV registers carry the full559screening decisions,326open advanced records, eligibility evidence, access attempts and methodology corrections. The priority is to finish eligibility/identity closure, then reconcile whole-review PRISMA and regenerate a consistently dated submission package. No reviewer name or vote is inferred.
'''
appendix+=r'\clearpage\section{Six added source-based study packages}\label{app:additions}'+'\n'
for e in elig:
    rid=e['Record ID'];ref=next(x for x in refs if x['Record ID']==rid)
    appendix+='\\clearpage\\subsection{'+e['Study ID']+' / '+e['Report ID']+' '+tex(e['Short name'])+'}\n\\cite{'+e['Study ID'].lower()+'}\n'
    appendix+=table(['Field','Source-based record'],[(tex(k),tex(v)) for k,v in [
        ('Record ID',rid),('Title',ref['Title']),('Venue/year',ref['Venue']+'; '+str(ref['Year'])),('DOI',ref['DOI']),
        ('Source',e['Source URL']),('Version evidence hash',e['Source SHA256']),('Eligibility','Include; all IC1-IC6 met on inspected primary text'),('Decision date UTC',e['Decided UTC'])]],[.21,.71])
    cc=[x for x in criteria if x['Record ID']==rid]
    appendix+=table(['Criterion','Evidence and anchor'],[(tex(x['Criterion']),tex(x['Evidence']+' '+x['Anchor'])) for x in cc],[.13,.77])
    qq=[x for x in qa if x['Record ID']==rid]
    appendix+=table(['QA','Score','Rationale and source anchor'],[(tex(x['Criterion']),'N/A' if x['Final source-based score']=='N/A' else tex(x['Final source-based score'])+'/'+x['Maximum'],tex(x['Rationale']+' '+x['PDF anchor'])) for x in qq],[.08,.08,.72])
    for x in [x for x in outcomes if x['Record ID']==rid]:
        appendix+='\\subsubsection*{'+tex(x['Outcome ID']+' '+x['Metric'])+'}\n'
        appendix+=table(['Field','Extracted value/context'],[(tex(k),tex(x[k])) for k in ['Metric','Value','Unit','Baseline','Context','Anchor','Interpretation limit']],[.21,.71])
appendix+=r'''\section{Continuation full-text exclusions}
Only assessed reports enter this table. Pending or inaccessible records are not relabeled as scientific exclusions.
'''
ex=[x for x in read('Final_Eligibility_Decisions.csv') if x['Final eligibility decision']=='Exclude']
appendix+=table(['Record / DOI','Decisive reason'],[(tex(x['Record ID']+'; '+x['DOI']),tex(x['Basis'])) for x in ex],[.26,.64])

crosswalk=[
('23','25mandatory deliverables','The inherited crosswalk plus the current inclusion/QA/extraction appendices and separate electronic registers','Prepared report/evidence; final whole-review PRISMA and eligibility closure remain open'),
('24','13main report sections','Introduction;RQs;Method;Selection;Taxonomy;RQ synthesis;Comparison;Trade-offs;Discussion;Recommendation;Gaps;Validity;Conclusion','All13sections retained and six additions integrated'),
('25','Analytical standard','Mechanism taxonomy; contextual comparative matrix; adverse outcomes; trade-offs; fiveRQ answers; conditional recommendations','Analysis integrated; systematic selection remains incomplete at full text'),
('26','Research quality','Stable IDs, primary URLs/hashes, DOI references, eligibility reasons, QA/extraction anchors and explicit limits','Traceability prepared; historical search reconstruction and326advanced records remain open')]
appendix+=r'\section{Headings 23--26 completion map}'+'\n'+table(['Heading','Requirement','Current evidence','Remaining qualification'],[(tex(a),tex(b),tex(c),tex(d)) for a,b,c,d in crosswalk],[.07,.17,.39,.25])
(out/'appendices.tex').write_text(appendix)

(out/'README.md').write_text('''# Integrated working report,23October2026

This separate draft integrates six source-eligible additions into the original13-section report. It is26studies/27reports,260QA items,66outcomes and two inherited calculations. All559continuation records have screening decisions;326advanced records still need eligibility or identity closure. Whole-review PRISMA is not final.

Build: `pdflatex main.tex`, `bibtex main`, `pdflatex main.tex`, `pdflatex main.tex`.

The inherited PRISMA figure is explicitly historical. The current branch table reports actual later-stage counts without pretending all334advanced records were retrieved. Frozen report/workbook/ZIP/protocol are unchanged. The source PDFs are not redistributed. Six added study cards include36ICchecks,60QAitems,14outcomes and primary source anchors. Further eligible additions require the same integration process and new counts.
''')
summary={'working_studies':26,'working_reports':27,'QA_items':260,'applicable_QA_points':516,'awarded_QA_points':437,'reported_outcomes':66,'calculations':2,'added_IC_checks':36,'added_QA_items':60,'added_outcomes':14,'added_citations':6,'screening_excluded':225,'advanced':334,'full_text_added_include':6,'full_text_added_exclude':2,'advanced_open':326,'whole_review_PRISMA_final':False,'frozen_report_unchanged':hashlib.sha256((frozen/'main.pdf').read_bytes()).hexdigest()=='c29ce1502390454412de07978683a850286d5e657562a322968ec4f443ce355e'}
(out/'integration_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))

# Refresh current-corpus phrases after the inherited six-addition template has
# been built. Original20-study snapshot statements and original52rows stay intact.
replacements={
 '26 studies':'27 studies','26 unique studies':'27 unique studies','26-study':'27-study','26studies':'27studies',
 '27 reports':'28 reports','27 report versions':'28 report versions','27reports':'28reports',
 '260 appraisal':'270 appraisal','260QA':'270QA','66 reported':'70 reported','66 outcome':'70 outcome','66outcomes':'70outcomes',
 '326 advanced':'325 advanced','326open':'325open','326advanced':'325advanced','Close326':'Close325','six additional studies':'seven additional studies','six new reports':'seven new reports',
 'six source-eligible additions':'seven source-eligible additions','six confirmed additions':'seven confirmed additions',
 'Six additions':'Seven additions','six additions':'seven additions','Six added':'Seven added','six new cards':'seven new cards','Six added study cards':'Seven added study cards',
 '36 source-anchored':'42 source-anchored','36IC':'42IC','60 Q1--Q10':'70 Q1--Q10','60 new source-based':'70 new source-based','60QA':'70QA',
 '14 outcome rows for':'18 outcome rows for','14new observations':'18new observations','14outcomes':'18outcomes',
 '162 included-report':'168 included-report','437/516':'450/534',
 'Miriam, SGDRC, Pantheon and Oneiros. Their appraisal totals are respectively 17, 17, 16, 16, 16 and 17 out of 20.':'Miriam, SGDRC, Pantheon, Oneiros and GACER. The first six appraisal totals are17,17,16,16,16and17out of20; GACER scores13/18with a reasonedN/A isolation item.',
 '6 / 2':'7 / 2','27 / 26':'28 / 27','334=6+2+326':'334=7+2+325',
 'seven new source-based items':'seven new source-based items',
}
for path in [*out.glob('*.tex'),out/'README.md']:
    text=path.read_text()
    for old,new in replacements.items():text=text.replace(old,new)
    text=text.replace('60 new source-based items','70 new source-based items').replace('26 study-level forms','27 study-level forms')
    text=text.replace('52inherited plus14new','52 inherited plus18 new')
    if path.name=='comparisons.tex':text=text.replace(r'65.5\%lowerP99TBT;20.7\%lowerP99TTFT;6.6\%higher',r'65.5\% lower P99 TBT; 20.7\% lower P99 TTFT; 6.6\% higher')
    if path.name=='appendices.tex':
        text=text.replace('Introduction;RQs;Method;Selection;Taxonomy;RQ synthesis;Comparison;Trade-offs;Discussion;Recommendation;Gaps;Validity;Conclusion','Introduction; RQs; Method; Selection; Taxonomy; RQ synthesis; Comparison; Trade-offs; Discussion; Recommendation; Gaps; Validity; Conclusion')
        text=text.replace(r'p{0.07\textwidth}>{\raggedright\arraybackslash}p{0.17\textwidth}>{\raggedright\arraybackslash}p{0.39\textwidth}',r'p{0.11\textwidth}>{\raggedright\arraybackslash}p{0.17\textwidth}>{\raggedright\arraybackslash}p{0.35\textwidth}')
        for doi in ['10.32604/cmc.2026.077259','10.32604/cmc.2025.059528']:text=text.replace('; '+doi+' &','; '+r'\nolinkurl{'+doi+'} &')
    path.write_text(text)
gacer=r'''\subsection{Compiler/runtime coordination and batch-latency evidence}
GACER extends the fine-grained compiler/runtime family through microbatch splitting and staged cross-model operator scheduling over GPU streams. Its final ICCAD2024 report evaluates heterogeneous inference models on one A100 and separately on P6000 and GTX1080Ti devices. Table2 reports3.30ms for VGG16+LSTM versus4.32ms sequential and22.14ms for five models versus37.86ms sequential. These are batch-completion measurements, not per-request tail latencies or online SLO attainment. Achieved SM occupancy is likewise distinct from GPU busy-time utilization. Table3 reports0.84--1.26seconds of optimization across the stated mixes and batches. This supports a conditional choice for known multi-model batch workloads when optimization and transformation costs are tolerable; it does not establish fault isolation or superiority on online tail-SLO objectives. The final report has four authors and nine pages, differing from the older seven-author preprint, which does not supply the extracted final results \cite{s027}.
'''
path=out/'comparisons.tex';path.write_text(path.read_text()+gacer)
path=out/'taxonomy.tex';path.write_text(path.read_text()+r'\paragraph{Cross-stack extension.} GACER belongs to compiler/runtime coordination: spatial microbatch splitting and temporal cross-model scheduling complement native streams. This resource-efficiency control does not assert a fault/security boundary \cite{s027}.'+'\n')
path=out/'recommendations.tex';path.write_text(path.read_text()+r'\paragraph{Known heterogeneous batch mixes.} Consider GACER when batch-completion efficiency is the objective and profiling/optimization delay is acceptable. Its reported0.84--1.26second optimization cost and absent serving-tail/fault evidence limit transfer to online SLO-sensitive or mutually untrusted tenants \cite{s027}.'+'\n')
summary.update({'working_studies':27,'working_reports':28,'QA_items':270,'applicable_QA_points':534,'awarded_QA_points':450,'reported_outcomes':70,'added_IC_checks':42,'added_QA_items':70,'added_outcomes':18,'added_citations':7,'full_text_added_include':7,'advanced_open':325})
(out/'integration_summary.json').write_text(json.dumps(summary,indent=2)+'\n')

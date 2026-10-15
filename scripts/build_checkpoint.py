"""Build a traceable interim report and workbook input, not a final selection claim."""
import csv,json,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence';OUT=ROOT/'task2/report'
def read(name):return list(csv.DictReader((E/name).open(encoding='utf-8')))
def esc(s):
    s=str(s)
    return ''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in s).replace('–','--').replace('—','---').replace('×',r'$\times$')
def para(s):return esc(s)+'\n\n'
def table(headers,rows,widths):
    spec=''.join('p{'+str(w)+r'\linewidth}' for w in widths)
    return '\\begin{longtable}{'+spec+'}\n\\toprule\n'+' & '.join(map(esc,headers))+r'\\\midrule'+'\n\\endhead\n'+'\n'.join(' & '.join(map(esc,row))+r'\\' for row in rows)+'\n\\bottomrule\n\\end{longtable}\n'
def main():
    counts=json.loads((E/'prisma_counts.json').read_text());votes=read('title_votes.csv');vc=Counter(r['vote'] for r in votes)
    checks=read('fulltext_checks.csv');ex=read('extraction.csv');qa=read('quality.csv');runs=read('imports/group-a/search_runs.csv');runs=[r for r in runs if r['status']=='executed']
    count_rejected=vc['exclude_recommendation'];count_retained=vc['retain_or_uncertain']
    progress=dict(first_reviewer_records=len(votes),first_reviewer_fraction=len(votes)/counts['records_after_exact_linkage'],exclude_recommendations=count_rejected,retained_or_uncertain=count_retained,unreviewed=counts['records_after_exact_linkage']-len(votes),source_checked_reports=len(checks),new_outcome_rows=len(ex),appraised_reports=2,final_decisions='pending',final_included_studies='pending')
    (E/'review_progress.json').write_text(json.dumps(progress,indent=2)+'\n')
    wb={'counts':counts,'progress':progress,'sheets':{}}
    for name,path in [('Screening','screening.csv'),('Records','records.csv'),('Duplicates','duplicates.csv'),('Version checks','possible_versions.csv'),('Source checks','fulltext_checks.csv'),('Quality','quality.csv'),('Extraction','extraction.csv'),('Snowballing','snowballing.csv'),('Shared candidates','shared_candidate_review.csv'),('Import manifest','import_manifest.csv')]:wb['sheets'][name]=read(path)
    (ROOT/'task2/tracker/workbook_input.json').write_text(json.dumps(wb,ensure_ascii=False)+'\n')
    intro=r'''\documentclass[12pt,a4paper]{article}
\usepackage[margin=0.85in]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern,microtype,booktabs,longtable,array,enumitem,xcolor,graphicx,tikz,fancyhdr}
\usetikzlibrary{arrows.meta,positioning}
\usepackage[hidelinks]{hyperref}
\usepackage{seqsplit}
\setlength{\emergencystretch}{3em}
\setlength{\headheight}{15pt}
\setlength{\parskip}{5pt}
\setlength{\parindent}{0pt}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{Group B: GPU sharing review}\fancyhead[R]{Interim evidence checkpoint}\fancyfoot[C]{\thepage}
\begin{document}
\begin{titlepage}\centering
{\large NED University of Engineering and Technology\\Department of Software Engineering\par}\vspace{1.5cm}
{\LARGE\bfseries GPU Sharing for Multi-Tenant Inference\par}\vspace{0.5cm}
{\Large Search, Screening and Extraction Checkpoint\par}\vspace{0.7cm}
{\large Operating Systems CEP, Topic 23\\Work through guideline Section 14\par}\vspace{1cm}
Eshaal Faisal\\Raazia Imran Reshamwala\\Rameen Siddiqui\vspace{1cm}
\begin{quote}Status: interim research evidence. Selection, independent review and final inclusion remain open. The submitted 27 September 2026 protocol is preserved.\end{quote}
\vfill 15 October 2026
\end{titlepage}
\tableofcontents\newpage
'''
    parts=[intro,r'\section{Purpose and engineering problem}',para('This checkpoint continues Group B\'s submitted protocol toward guideline Sections 7-14. The decision concerns how one physical GPU can support concurrent inference tenants through time-slicing, MPS, MIG and API interception/remoting while balancing utilization, latency and isolation. Multi-GPU papers qualify only when a within-device inference-sharing result is separable. This report documents actual imported data and bounded source checks; it does not claim a completed systematic review.'),r'The review method follows software-engineering SLR guidance and transparent PRISMA reporting \cite{kitchenham,prisma,prismas}.',r'\section{Research questions}',table(['RQ','Preserved focus'],[
      ('RQ1','Mechanism families, sharing granularity, implementation layer and isolation boundary.'),('RQ2','Metric definitions and comparability of hardware, workload, baselines and methods.'),('RQ3','Conditions under which utilization, throughput, density and latency change.'),('RQ4','Resource/fault isolation, implementation costs, trade-offs and conflicting evidence.'),('RQ5','Conditional engineering choices, confidence and alternatives.')],[.08,.84]),
      r'\section{Sources and shared-data provenance}',para('The user explicitly authorized reuse of Group A\'s searches and findings with attribution. We imported its committed IEEE/Springer metadata and preserved its assessments as prior assessments. Group B does not claim to have re-executed those searches. Group A source snapshot: adf4a1e827f71610eba21785fbf5cbac8793fbfc. The shared materials remain under evidence/imports/group-a. ACM bibliography exports supplied through Drive remain untouched under evidence/imports/acm. The import manifest records SHA-256 hashes and counts.'),
      table(['Source','Rows','Evidence status'],[('Other sources' if k=='Supplementary' else k,v,{'ACM':'79 original BibTeX files; exact query-to-batch mapping unresolved','IEEE':'Group A executed metadata capture; five-run shared log includes four IEEE runs','Springer':'Group A master search; broad full-text indexed scope','Supplementary':'20 selected shared leads; not a systematic citation census'}[k]) for k,v in counts['by_source'].items()],[.15,.14,.62]),
      para('Database occurrences total 2,271. The 20 supplementary leads are a separate route, giving 2,291 total imported occurrences. These counts are export/capture counts, not a claim that ACM displayed exactly 1,582 hits. ScienceDirect\'s earlier 100 incoming RIS occurrences remain preserved separately and are excluded from this active checkpoint by the user\'s instruction. No source was deleted.'),
      r'\section{Search strategy and deviations}',para('Group B\'s submitted protocol specifies 12 main-window expressions and four older-MPS expressions. The imported Group A search design uses a different master/family vocabulary and broad Springer field. Reuse saves collection effort but does not establish equivalence to every Group B planned query. Appendix A preserves the exact shared executed expressions and settings. The ACM files do not establish their original query, field, date filters, displayed hits or pagination. Those unknowns remain unknown.'),
      table(['Run','Shared count','Field and coverage'],[(r['run_id'],r['hits'],r['fields']+'; '+r['filters']) for r in runs],[.19,.13,.59]),
      para('Search-coverage gaps: ACM run mapping and completeness; missing prespecified older-MPS lanes; unexecuted Group B expressions; broad Springer body-search noise; ScienceDirect deferred. The shared search cutoff is 11 October 2026; ACM export upload/modified times cannot substitute for search timestamps. Publication-date eligibility for ACM candidates must use the documented actual run date, or a clearly adopted and recorded common cutoff.'),
      r'\section{Eligibility and screening rules}',table(['Criterion','Operational rule'],[('IC1','Final English peer-reviewed full journal or conference primary study.'),('IC2-IC3','Distinct concurrent tenants share one physical GPU through an assigned mechanism, with separable inference evidence.'),('IC4-IC5','Inspectable relevant outcome and sufficient methods/configuration; separable local result permitted in larger systems.'),('IC6','Main date window or individually justified older seminal exception.'),('EC1','Non-primary/non-peer-reviewed, survey, poster, abstract-only or container item.'),('EC2-EC5','Training-only/no concurrent inference; hardware-only; aggregate cluster-only; non-GPU-only.'),('EC6-EC7','Insufficient assessed full-text detail; outside date/language criteria.')],[.16,.76]),
      para('Missing full text is a retrieval status, not EC6. Title uncertainty is retained. Multiple reports are linked to a study rather than counted as separate studies. The existing REEF conference/journal versions require a preferred-report decision. Original independent votes must be preserved; there is currently one Group B AI reviewer, not two human reviewers.'),
      r'\section{Duplicate linkage and payload}',para(f"Deterministic linkage identifies {counts['exact_duplicate_occurrences']} repeated occurrences, leaving {counts['records_after_exact_linkage']} canonical records for review. The keys use normalized DOI or exact publisher URL; identifier-free ACM copies additionally require identical normalized title, authors and year. Different DOIs are not silently collapsed. There are {counts['possible_version_pairs']} title-match pairs still requiring identity/version review. These are not removed from the active counts."),para('The earlier pasted checkpoint reported 74 duplicates and 2,217 records. Those figures were not recovered as a committed row-level log. This reconstruction deliberately reports its own reproducible result instead of repeating an unverified total. Identity linkage remains subject to review of the 41 pairs. The imported ACM payload also contains 609 proceedings containers, seven books and one technical report; these explain many low-relevance hits and require distinct EC1 recommendations.'),
      r'\section{Current screening results}',table(['Measure','Observed state'],[('Canonical records',2247),('Recorded first-review decisions',len(votes)),('Exclude recommendations',count_rejected),('Retain/uncertain recommendations',count_retained),('Awaiting first review',2247-len(votes)),('Independent second-review and final decisions','Pending'),('Source-checked priority reports',5),('Final included primary-study count','Not established')],[.57,.34]),
      para('The 800 first-review rows comprise 183 individually inspected high-priority titles and 617 explicit BibTeX container/book/report type checks. Recommendations are preliminary, with abstract verification where needed and independent checking still open. The remaining triage labels are automated prioritization signals, not exclusion decisions. No 1,813-record automated triage category is reported as a final exclusion.'),
      r'\section{Interim PRISMA 2020 accounting}',para('The following diagram is a pending-stage accounting view using PRISMA categories, not a completed official PRISMA result. Final screening, reports sought/not retrieved, assessed exclusions and included-study totals require resolved record/report/study links and independent review. Four targeted backward-reference links are logged separately; three are unimported candidate leads and do not inflate current identification counts.'),r'\input{prisma.tex}',
      r'\section{Citation chasing}',para('A targeted backward pilot inspected four references from gpulets: Prophet [4], Baymax [5], Clipper [15] and GSLICE [17], on printed pages 210-211. GSLICE already occurs in the imported payload. The other three are candidate leads awaiting metadata/full-text eligibility checks; their older dates require individual justification if retained. This is a four-reference pilot, not exhaustive backward/forward snowballing. The remaining references and forward citations remain to be searched and logged.'),
      r'\section{Priority full-text checks}',table(['Report','Group B first-review finding'],[(r['short_name'],r['criterion_rationale']+' Remaining: '+r['remaining_checks']+'. Source: '+r['anchor']) for r in checks],[.16,.76]),
      r'\section{Quality appraisal and calibration}',para('Group A\'s ten-item 0-1 scale has different criterion meanings from Group B\'s submitted Q1-Q10 0-2 rubric. Multiplying the totals would be invalid. Two fresh first-review appraisals are recorded with rationale and source anchors; the second reviewer and reconciliation columns remain blank. N/A is used only for an outcome claim genuinely outside the bounded evidence being appraised. The VastPipe appraisal is explicitly restricted to its local GPU evidence, not the NPU experiments.'),
      table(['Report','First-review sum','Applicable max','Normalized'],[(rid,sum(float(r['score']) for r in qa if r['report_id']==rid and r['score']!='NA'),sum(int(r['maximum']) for r in qa if r['report_id']==rid),f"{sum(float(r['score']) for r in qa if r['report_id']==rid and r['score']!='NA')/sum(int(r['maximum']) for r in qa if r['report_id']==rid):.1%}") for rid in ['GB-P001','GB-P002']],[.2,.22,.22,.18]),
      para('Scores do not establish final inclusion, nor do they replace the source check. No final synthesis sensitivity conclusion is yet supported. Each appraisal retains ten separate criterion rows so the team can challenge a score without losing its original rationale.'),
      r'\section{Data extraction through guideline Section 14}',para('The active register contains six newly checked outcomes across four priority reports. Five older pilot rows remain in evidence/pilot/extraction.csv with their original manuscript/version caveats. They are not added to final included-study counts. The full extraction category specification A-M remains in the submitted protocol. Use not-extracted for fields not yet transcribed, NR only when the source was checked and does not report the item, and an empty checker field until an independent check occurs.'),
      table(['Report / metric','Checked result and interpretation'],[(r['report_id']+' / '+r['metric'],r['value']+' '+r['units']+'; '+r['hardware']+'; '+r['workload']+'. Baseline: '+r['baseline']+'. Anchor: '+r['source_anchor']+'. '+r['caveat']) for r in ex],[.27,.65]),
      r'Checked source reports are VastPipe, iGniter, gpulets and PipeSwitch \cite{vastpipe,igniter,gpulets,pipeswitch}. REEF\textquotesingle s conference report has a bounded configuration check \cite{reef}; a later journal extension is already a shared version lead.',
      r'\section{Interpretation limits}',para('The extracted quantities are deliberately kept distinct. Prediction error is not a utilization gain. A p99 recovery example does not prove an unconditional SLO guarantee. Additional end-to-end latency is not total response time. A CDF across model-pair overheads is not a request-latency percentile. Fleet cost/GPU-count benefits cannot be attributed to local GPU utilization without a valid denominator. Performance interference does not prove memory, security or fault containment.'),
      r'\section{Work to close before submission}',table(['Owner / task','Concrete output'],[('Eshaal: source and abstract review','Recover ACM query-to-file mapping from search history/screenshots: exact strings, field, date, hit count and exported pages. Then review assigned screening rows without seeing first-review votes initially.'),('Rameen: priority paper checks','Independently check the five priority reports, six outcomes and 20 QA items. Enter own vote/score and exact page/table. Check the remaining 21 shared candidates in priority order.'),('Raazia / AI: registers and report','Resolve version pairs, continue abstracts and full texts, complete citation chasing, reconcile PRISMA and rebuild report/workbook from the same logs.')],[.27,.65]),
      para(f"Measured progress: {len(votes)}/2247 ({len(votes)/2247:.1%}) canonical records have a first-review recommendation. Five reports have bounded source checks; two have first-review appraisals. Final protocol-compliant screening and inclusion are pending. These are activity-specific measures, not a claim of 50% or 100% overall completion. The final CEP additionally needs Sections 15-22: taxonomy, comparison, trade-offs, conflicts, synthesis, recommendation, gaps and limitations."),
      r'\appendix\section{Exact imported Group A executed searches}']
    for r in runs:
        parts += [r'\subsection{'+esc(r['run_id'])+'}',para('Database: '+r['database']+'. Date: '+r['date']+'; time UTC: '+r['time_utc']+'. Reviewer/operator: '+r['reviewer']+'. Collection: '+r['collection']+'.'),r'{\small\ttfamily\raggedright '+esc(r['query'])+r'\par}',para('Field: '+r['fields']+'. Filters: '+r['filters']+'. Displayed hits: '+r['hits']+'. Captured occurrences: '+r['imported_occurrences']+'. Export method: '+r['export_method']+'.')]
    parts += [r'\section{Evidence-file guide}',table(['File','Purpose'],[('records.csv','One immutable occurrence per row; source hash and original identity.'),('duplicates.csv / possible_versions.csv','Resolved deterministic repeats / unresolved title pairs.'),('screening.csv / title_votes.csv','Editable review queue / preserved first-review events.'),('fulltext_checks.csv','Five source checks with outstanding criteria/version work.'),('quality.csv / extraction.csv','Fresh Group B first-review appraisal / six outcome records.'),('snowballing.csv','Four backward-reference events; no invented citation census.'),('imports/group-a','Original attributed search data and prior assessments.'),('imports/acm / import_manifest.csv','Untouched bibliography batches and hash inventory.')],[.38,.54]),r'\input{heading14_audit.tex}\clearpage\bibliographystyle{ieeetr}\bibliography{references}\end{document}']
    (OUT/'main.tex').write_text('\n'.join(parts))
    flow=r'''\begin{center}
\begin{tikzpicture}[box/.style={draw=blue!55!black,rounded corners,align=center,text width=5.4cm,minimum height=1.1cm,font=\small},side/.style={box,draw=orange!70!black,text width=4.1cm},>=Latex,node distance=0.9cm]
\node[box] (db) {Database records: 2,271\\ACM 1,582; Springer 587; IEEE 102};
\node[side,right=0.6cm of db] (other) {Other-source records: 20\\ACM query mapping unresolved};
\node[box,below=of db] (all) {Imported records: 2,291};
\node[side,right=0.6cm of all] (dup) {Duplicates linked: 44\\41 version pairs pending};
\node[box,below=of all] (queue) {Review queue: 2,247};
\node[box,below=of queue] (first) {First review: 800\\Awaiting first review: 1,447};
\node[side,right=0.6cm of first] (votes) {Exclude votes: 647\\Retain/uncertain: 153\\Second review pending};
\node[box,below=1.5cm of first] (ft) {Priority source checks: 5\\Final assessment count pending};
\node[side,right=0.6cm of ft] (retr) {Reports sought / not retrieved\\Final exclusions and reasons\\Counts pending};
\node[box,below=of ft] (inc) {Final inclusion: pending\\Six checked outcome rows; two QA drafts};
\draw[->] (db)--(all);\draw[->] (other)--(all);\draw[->] (all)--(queue);\draw[->] (all)--(dup);\draw[->] (queue)--(first);\draw[->] (first)--(votes);\draw[->] (first)--(ft);\draw[->] (ft)--(retr);\draw[->] (ft)--(inc);
\end{tikzpicture}
\end{center}
'''
    # Actual vote counts are generated, not hand-entered in the rendered diagram.
    flow=flow.replace('votes: 647','votes: '+str(count_rejected)).replace('uncertain: 153','uncertain: '+str(count_retained))
    (OUT/'prisma.tex').write_text(flow)
    (OUT/'prisma_flow.tex').write_text(r'\documentclass[12pt,a4paper]{article}\usepackage[margin=0.8in]{geometry}\usepackage{tikz}\usetikzlibrary{arrows.meta,positioning}\pagestyle{empty}\begin{document}\section*{Group B interim record accounting}\input{prisma.tex}\noindent Pending-stage PRISMA accounting. Recommendations are not final exclusions; final inclusion is not established.\end{document}')
    # Reuse verified bibliographic identities while retaining existing method keys.
    refs=(ROOT/'task1/references.bib').read_text()
    studies=json.loads((E/'imports/group-a/included_studies.json').read_text())
    for key in ['vastpipe','igniter']:
        r=next(s for s in studies if s['key']==key)
        refs+='\n@article{'+key+',\n title={'+r['title']+'},\n author={'+r['authors']+'},\n journal={'+r['venue']+'},\n year={'+str(r['year'])+'},\n doi={'+r['doi']+'}\n}\n'
    (OUT/'references.bib').write_text(refs)
    print(json.dumps(progress,indent=2))
if __name__=='__main__':main()

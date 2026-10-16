"""Build an interim Cycle 2 report from frozen Cycle 1 registers and traced claims."""
import csv,json,re,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
from build_checkpoint import esc as base_esc
R=Path(__file__).resolve().parents[1];E=R/'evidence';O=R/'task2/report'
def read(n):return list(csv.DictReader((E/n).open()))
def esc(s):
 s=re.sub(r'[,;](?=[A-Za-z])',lambda m:m.group(0)+' ',str(s)).replace('not_extracted','not extracted')
 return base_esc(s).replace('/',r'/\allowbreak{}')
def para(s):return esc(s)+'\n\n'
def table(headers,rows,widths):
 return '\\begin{longtable}{'+''.join('p{'+str(w)+r'\linewidth}' for w in widths)+'}\n\\toprule\n'+' & '.join(map(esc,headers))+r'\\\midrule'+'\n\\endhead\n'+'\n'.join(' & '.join(map(esc,row))+r'\\' for row in rows)+'\n\\bottomrule\n\\end{longtable}\n'
# Reuse the already reviewed through-14 rendering, then reorganize its full detail as appendices.
subprocess.run([sys.executable,str(R/'scripts/build_cycle1_report.py')],check=True)
s=(O/'main.tex').read_text();head,tail=s.split(r'\appendix\section{Exact attributed shared executed searches}',1)
before,quality=head.split(r'\section{Quality assessment}',1);quality,extract=quality.split(r'\section{Data extraction}',1)
qintro,qdetail=quality.split(r'\subsection{',1);qdetail=r'\subsection{'+qdetail
eintro,edetail=extract.split(r'\subsection{',1);edetail=r'\subsection{'+edetail
queries=tail.split(r'\section{Validation and continuation}',1)[0]
# Preserve raw operator provenance in registers; print the attributed source in the report.
queries=queries.replace('Originating operator: AI-CODEX.', 'Source attribution: Group A shared executed search.')
# All observations keep their outcome identity in the printed detail.
ex=read('extraction.csv')
for r in ex:edetail=edetail.replace(esc(r['metric'])+': '+esc(r['value']),esc(r['outcome_id']+' '+r['metric'])+': '+esc(r['value']),1)
before=before.replace('Task 2 Cycle 1','Task 2 Cycle 2').replace('Task 2, Cycle 1','Task 2, Cycle 2').replace('Task 2: Working Evidence Report through Guideline Section 14','Task 2 and CEP: Interim Evidence and Analysis').replace('Search, Screening, Quality Assessment and Data Extraction','Systematic Review Evidence and Conditional Engineering Analysis').replace('Later CEP synthesis is outside this cycle.','The analysis is interim and limited to the checked evidence; final selection and independent validation remain pending.').replace('This cycle strengthens the evidence registers; it does not select a universal winner or answer the final CEP synthesis questions.','This cycle interprets the current evidence and gives cautious interim answers to the five protocol RQs. No universal winner or final included-study synthesis is established.')
# Keep a single unambiguous first-review total; historic Cycle 1 additions remain attributed.
before=before.replace('New Cycle 1 recommendations','Cycle 1 added recommendations')
before=before.replace(r'\tableofcontents',r'\begingroup\setlength{\parskip}{0pt}\makeatletter\renewcommand\l@section{\@dottedtocline{1}{0em}{2.5em}}\makeatother\tableofcontents\endgroup')
parts=[before,r'\section{Quality assessment}',qintro,para('Full item-by-item rationales and anchors for all 50 Q1-Q10 entries are retained in Appendix B. Applicable-score normalization preserves justified N/A items. None of the five preliminary forms falls below the protocol 60% sensitivity threshold, so removing below-threshold forms leaves this provisional set unchanged; that arithmetic does not demonstrate robust conclusions or establish eligibility. Unreconciled appraisal and missing family coverage still constrain confidence.'),r'\section{Data extraction}',eintro]
forms=read('study_extraction_form.csv')
parts += [table(['Report / platform','Workload and interpretation boundary'],[(f['report_id']+' / '+f['gpu_hardware'],f['models']+'; '+f['tenant_mix']+'; '+f['latency']+'; '+f['field_status']) for f in forms],[.25,.64]),para('Appendix C preserves all five detailed study forms and every one of the 26 outcome rows. Sections 15-22 organize the analysis by mechanism, engineering question and decision condition. An observed outcome is not an independent study, and the current five-report evidence slice is not a final included-study set.')]
analysis=read('cycle2_analysis.csv')
sourcecite=r'Checked primary-report sources: \cite{vastpipe,igniter,gpulets,pipeswitch,reef}. '
sections=[('taxonomy','Taxonomy of existing approaches'),('comparison','Comparative evidence matrix'),('tradeoff','Engineering trade-offs'),('conflict','Conflicting and apparently conflicting evidence'),('rq','Interim answers to RQ1-RQ5'),('recommendation','Conditional engineering recommendations'),('gap','Research gaps in the current evidence'),('validity','Threats to validity and review limitations')]
for kind,title in sections:
 parts += [r'\section{'+title+'}']
 if kind=='taxonomy':parts += [para('Classification separates sharing granularity from implementation layer. Temporal execution, concurrent MPS allocation and spatial hardware partitions describe different resource-sharing choices; interception or remoting describes where calls are mediated. A hybrid can occupy more than one category. Mechanism definitions are contextual; only registered primary outcomes support experimental claims.'),r'Context references: \cite{nvidiaMPS,nvidiaMIG,nvidiaTime}. '+sourcecite]
 elif kind=='comparison':parts += [para('The matrix juxtaposes five source-specific configurations; it does not rank their numerical effects. Within-paper contrasts retain their own denominator and statistic. Hardware, workload, memory and software conditions are retained in Appendix C. Across-paper evidence is descriptive unless those dimensions match.'),sourcecite]
 elif kind=='tradeoff':parts += [para('A throughput gain is not automatically a utilization percentage, latency guarantee, energy saving or isolation result. The trade-off analysis retains costs and failure conditions alongside each potential benefit.'),sourcecite]
 elif kind=='conflict':parts += [para('A direct contradiction requires comparable questions and experimental conditions. The current register shows apparent cross-study disagreement and explicit within-study objective trade-offs, but does not establish a matched cross-study contradiction. The following explanations use observed configuration differences rather than untested causal attribution.'),sourcecite]
 elif kind=='rq':parts += [para('Answers follow the submitted protocol questions. Confidence is limited by preliminary eligibility, first-review extraction and heterogeneous metrics. No effect is pooled, no family is declared dominant by publication counts, and no conclusion is generalized to the full candidate queue.'),sourcecite]
 elif kind=='recommendation':parts += [para('These are conditional candidates for controlled engineering evaluation. Each requires workload replay, per-tenant measurements and an explicit acceptance threshold set by the deployment owner. Final evidence-based selection must be revisited after human validation and broader extraction.'),sourcecite]
 elif kind=='gap':parts += [para('A missing result here identifies a gap in this extracted evidence slice. It does not establish that the entire research field lacks such work. The next research steps should target these missing comparisons and properties.')]
 else:parts += [para('The review exposes provenance, uncertainty and missing decisions so that they can be corrected. Mitigation reduces some risks; it does not erase incomplete searches, unvalidated judgments or configuration heterogeneity.')]
 selected=[r for r in analysis if r['kind']==kind]
 parts += [table(['Analysis / condition','Interim finding, evidence and boundary'],[(r['analysis_id']+' '+r['topic'],r['interim_analysis']+' Evidence: '+(r['outcome_ids'] or r['report_ids'] or r['source_anchor'])+'. Boundary: '+r['limitation_or_required_check']) for r in selected],[.24,.65])]
parts += [r'\section*{Interim conclusion}\addcontentsline{toc}{section}{Interim conclusion}',para('The engineering choice is conditional: adaptive concurrency can improve useful throughput in a suitable trusted co-inference setting, while preemption or pipelined switching may better address particular latency and memory constraints. The evidence does not support a universal best mechanism, a security/fault-isolation winner, a pooled speedup or a remoting recommendation. These conclusions are candidates for validation against the final eligible study set, not final deployment guarantees.'),para('The report now addresses guideline Sections 1-22 as an interim package. Search provenance, final screening, full-text eligibility, independent appraisal/extraction and study-level identity remain open. The instructor target of 15-20 eligible primary studies is not established by five bounded report checks. Final PRISMA and the final included-study count remain pending.'),r'\label{maintextend}\clearpage\appendix\section{Exact attributed shared executed searches}',queries,r'\clearpage\section{Detailed quality-assessment forms}',qdetail,r'\clearpage\section{Detailed study forms and extracted outcomes}',edetail,r'\clearpage\section{Validation and continuation}',para('This Cycle 2 analysis uses the committed Cycle 1 results as its quantitative baseline. No new screening recommendation, outcome measurement, quality vote or citation event was added during report preparation. The complete analysis-to-outcome mapping is retained in cycle2_analysis.csv and the workbook. Final selection remains pending.'),table(['Person','Next action'],[('Eshaal','Align existing human ACM work to record IDs; validate148priority candidates, then the1066candidate queue and127sampled exclusions; reconcile query/export provenance.'),('Rameen','Validate IC1-IC6 for all5priority reports, all26outcomes and50quality items independently; record exact anchors and disagreements; resolve PipeSwitch applicability and REEF source version.'),('Raazia','Reconcile verified human decisions and proposed version links; extend full-text eligibility, QA and extraction to every included study; then freeze final PRISMA and revise conclusions.')],[.15,.74]),para('First recommendations are complete, while final screening, QA and extraction remain incomplete. Continue wider retrieval and citation chasing, resolve staged search identifiers and study identities, then re-evaluate the recommendations. A DOI/official-source catalogue closes this PDF; USENIX reports without a DOI in their official citation retain their publisher URLs.'),r'\clearpage\bibliographystyle{ieeetr}\bibliography{references}',r'\clearpage\section{DOI and official-source catalogue}']
cat=read('cycle2_reference_catalog.csv')
parts += [para('This catalogue covers every work cited in the report. A DOI is printed where verified in publisher or registration metadata. Where the official citation does not list a DOI, its stable publisher or institutional URL is supplied; an identifier from a different version is never substituted.'),table(['Citation key / work','DOI or official source; identity status'],[(r['citation_key']+' / '+r['short_title'],('DOI: '+r['doi'] if r['doi'] else 'DOI not listed in checked official citation')+'; '+r['official_url']+'; '+r['status']) for r in cat],[.27,.62]),r'\end{document}']
(O/'main.tex').write_text('\n'.join(parts))
# Recalculate all flow nodes from the active registers; final stages deliberately remain pending.
c=json.loads((E/'prisma_counts.json').read_text());p=json.loads((E/'review_progress.json').read_text())
flow=(O/'prisma.tex').read_text()
replacements={
 'Database occurrences: 2,271':f"Database occurrences: {c['database_occurrences']:,}",
 'ACM1,582; Springer587; IEEE102':f"ACM {c['by_source']['ACM']:,}; Springer {c['by_source']['Springer']}; IEEE {c['by_source']['IEEE']}",
 'Other-source occurrences:20':f"Other-source occurrences: {c['supplementary_occurrences']}",
 'Active imported occurrences:2,291':f"Active imported occurrences: {c['occurrences']:,}",
 'Applied duplicate links:44':f"Applied duplicate links: {c['exact_duplicate_occurrences']}",
 'Additional identity proposals:3':f"Additional identity proposals: {c['version_pair_dispositions']['identity_verified_linkage_proposed']}",
 'Canonical record queue:2,247':f"Canonical record queue: {c['records_after_exact_linkage']:,}",
 'First recommendations:2247':f"First recommendations: {c['preliminary_recommendations']:,}",
 'Not yet recommended:0':f"Not yet recommended: {c['first_recommendations_pending']}",
 'Preliminary exclude:1181':f"Preliminary exclude: {c['preliminary_exclusion_recommendations']:,}",
 'Retain/uncertain:1066':f"Retain/uncertain: {c['preliminary_retain_or_uncertain']:,}",
 'Bounded priority source checks:5':f"Bounded priority source checks: {len(read('fulltext_checks.csv'))}",
 'Final included studies:pending':'Final included studies: pending',
 '26 outcomes;5 preliminary appraisals':f"{len(ex)} outcomes; {len(forms)} preliminary appraisals"}
for a,b in replacements.items():
 assert a in flow,a
 flow=flow.replace(a,b)
(O/'prisma.tex').write_text(flow)
(O/'prisma_flow.tex').write_text(r"\documentclass[12pt,a4paper]{article}\usepackage[margin=0.8in]{geometry}\usepackage{tikz}\usetikzlibrary{arrows.meta,positioning}\pagestyle{empty}\begin{document}\section*{Group B interim record accounting: Cycle 2}\input{prisma.tex}\noindent Register-derived interim accounting. Preliminary recommendations are not final exclusions. Reports sought, not retrieved, finally assessed/excluded and final included studies remain pending human validation.\end{document}")
print('Cycle 2 main.tex: guideline1-22, source appendices, DOI catalogue; all flow nodes register-derived.')

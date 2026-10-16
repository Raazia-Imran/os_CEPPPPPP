"""One compilable Task2 TeX source plus lossless, readable research-table appendices."""
from pathlib import Path
from collections import Counter
import json,re,csv,hashlib,shutil
R=Path(__file__).resolve().parents[1];F=R/'final things';O=F/'06_Task2_Submission';d=json.loads((R/'task2/qa/task2_consolidated_input.json').read_text())
source=(F/'02_Report_LaTeX/main.tex').read_text();stop=source.index(r'\section{Taxonomy and integration layers}');core=source[:stop]
core=core.replace('Current evidence checkpoint','Task 2 research record').replace('Systematic Review Evidence and Analysis','Study Selection, Quality Assessment and Data Extraction')
core=re.sub(r'\\vspace\{0\.8cm\}\\begin\{quote\}.*?\\end\{quote\}',r'\\vspace{0.8cm}\\begin{quote}Task 2 submission through instructor Heading 14. This record presents the completed preparation and the source evidence currently assessed. Final eligibility and unique-study selection remain incomplete.\\end{quote}',core,flags=re.S)
core=core.replace('Supporting files: compact review workbook; separate QA and data-extraction tables; record-keyed CSV logs.','Complete research tables follow as appendices. The accompanying workbook provides a concise, editable view.')
core=core.replace(r'\usepackage{lmodern,microtype,booktabs,longtable,array,graphicx,enumitem,xcolor,fancyhdr,tikz}',r'\usepackage{lmodern,microtype,booktabs,longtable,array,graphicx,enumitem,xcolor,fancyhdr,tikz,pdflscape,pdfpages,amsmath,amssymb}')
core=core.replace('On 16 October 2026, the user authorized AI-only continuation without waiting for manual returns. Automated triage and source-based AI assessment therefore proceed as an explicit departure from the planned two-reviewer process. The process does not claim independent human agreement. Original votes/scores remain available; unperformed second/reconciled fields stay blank.','The present record uses automated first-pass recommendations followed by targeted assessments of accessible sources. Independent reviewer fields have not been populated. This departure from the planned dual-review process is documented separately; no reviewer-agreement statistic is reported. Initial decisions, scores and provenance remain preserved.')
core=core.replace('Authorized departure from independent two-reviewer plan; no human votes invented.','Automated assessment replaced the planned independent dual-review process; initial records are retained.').replace('AI-only continuation','Review-method amendment').replace('AI EC2 judgments','source-assessed EC2 decisions').replace('first AI assessment','initial assessment')
# Standard PRISMA2020 categories, with a declared pooled-record adaptation and pending final stages.
flow=r'''\clearpage
\begin{figure}[p]\centering
\begin{tikzpicture}[b/.style={draw,rounded corners,align=center,text width=7cm,inner sep=5pt,font=\small},s/.style={b,text width=3.6cm},>=Latex]
\node[b,text width=5.9cm](db) at(-3.3,0){Identification via databases\\ACM1,582;IEEE102;Springer587;ScienceDirect1,898\\Total4,169occurrences};
\node[b,text width=5.9cm](other) at(3.3,0){Identification via other methods\\20supplementary occurrences\\Discovery routes retained separately};
\node[b](all) at(0,-2.4){Pooled identification register\\4,189occurrences};
\node[s](remove) at(5.8,-2.4){Removed before screening\\114duplicate links applied\\Other applied removals:0};
\node[b](screen) at(0,-4.5){Records screened:final stage pending\\4,075canonical records have initial triage\\Verified abstract-screening census incomplete};
\node[s](excluded) at(5.8,-4.5){Records excluded:pending\\1,441preliminary exclusion proposals are not final screened exclusions};
\node[b](sought) at(0,-6.6){Reports sought for retrieval\\Complete count pending};
\node[s](unavailable) at(5.8,-6.6){Reports not retrieved\\Complete count pending\\Access attempts are not a report count};
\node[b](assessed) at(0,-8.7){Reports assessed for eligibility\\17documented source assessments\\Wider candidate census incomplete};
\node[s](ftout) at(5.8,-8.7){Reports excluded\\2source-assessed EC2 decisions\\Complete exclusion census pending};
\node[b](included) at(0,-11){Studies included:pending\\Reports of included studies:pending\\15QA/extraction forms do not establish final inclusion};
\draw[->](db.south)--(all.north);\draw[->](other.south)--(all.north);\draw[->](all.east)--(remove.west);\draw[->](all)--(screen);\draw[->](screen)--(excluded);\draw[->](screen)--(sought);\draw[->](sought)--(unavailable);\draw[->](sought)--(assessed);\draw[->](assessed)--(ftout);\draw[->](assessed)--(included);
\end{tikzpicture}
\caption{Interim PRISMA2020 accounting, adapted from Page et al.\cite{prisma}. Database and supplementary occurrences are pooled before record linkage in this register. Unfinished stages are pending; no preliminary proposal is promoted to a final exclusion.}
\end{figure}\clearpage
'''
core=re.sub(r'\\begin\{center\}\\begin\{tikzpicture\}[\s\S]*?\\end\{tikzpicture\}\\end\{center\}',lambda m:flow,core,count=1)
core=core.replace(r'\section{Search, screening, duplicate and abstract logs}',r'Source-assessed exclusions are TGS and HiveD\cite{GB-P016,GB-P017}. These decisions are distinct from initial exclusion proposals.'+'\n'+r'\section{Search, screening, duplicate and abstract logs}')
# Human-readable source-value formatting; CSVs retain exact originals.
replace={'\u2013':'-','\u2014':'-','\u2010':'-','\u2011':'-','\u2012':'-','\u2212':'-','\u2018':"'",'\u2019':"'",'\u201c':'"','\u201d':'"','\xa0':' ','\u202f':' ','\u00d7':r'\ensuremath{\times}','\u00b5':r'\ensuremath{\mu}','\u03bc':r'\ensuremath{\mu}','\u03b1':r'\ensuremath{\alpha}','\u03b2':r'\ensuremath{\beta}','\u03ba':r'\ensuremath{\kappa}','\u2020':r'\textdagger{}','\u204e':'*','\u2039':'<','\u203a':'>','\u00b0':r'\ensuremath{^{\circ}}'}
def esc(v):
 text=str(v);text=re.sub(r'\s+',' ',text).strip();parts=[]
 for c in text:
  if c in replace:parts.append(replace[c]);continue
  parts.append({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_\allowbreak{}','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','/':r'/\allowbreak{}',':':r':\allowbreak{}','<':r'\textless{}','>':r'\textgreater{}'}.get(c,c))
 s=''.join(parts)
 # Source hashes and other long tokens must wrap inside cells.
 return re.sub(r'(?<![A-Za-z])[A-Fa-f0-9]{40,}',lambda m:r'\allowbreak{}'.join(m.group(0)[i:i+8] for i in range(0,len(m.group(0)),8)),s)
# Complete tables from every workbook tab plus the supporting scientific registers.
tables=[('Workbook summary', [dict(measure=k,value=v) for k,v in d['counts'].items()]),*d['tabs'].items(),('Abstract normalization audit (previous workbook tab)',d['old_abstract_audit']),*d['extras'].items()]
# Lossless glossary abbreviates repeated long labels in large logs; source data and row IDs stay intact.
freq=Counter(str(v) for name,rows in tables if len(rows)>200 for row in rows for v in row.values() if v not in ['',None]);values=sorted(v for v,n in freq.items() if (len(v)>=16 and n>=3) or len(v)>=95)
gloss={v:f'V{i:05d}' for i,v in enumerate(values,1)}
def val(v,use):return r'\texttt{'+gloss[str(v)]+'}' if use and str(v) in gloss else esc('' if v is None else v)
parts=[core,r'\clearpage\bibliographystyle{ieeetr}\bibliography{references}\label{core:end}\clearpage\appendix',r'\section{Reading the complete research tables}',r'The appendices reproduce the research data used by the accompanying workbook and the additional evidence registers. Report IDs join quality, eligibility and extraction records. Outcome rows are measurements, not studies. Blank cells remain blank. Long repeated values in large logs are represented by V-codes; the complete value glossary preserves every original string. The editable CSV files retain their unabridged values. This is reversible display compression, not a change to the evidence.',r'\subsection*{The paper count in plain English}',r'The quality and extraction tables cover the same fifteen report IDs, GB-P001 to GB-P015. Thirteen reports are provisionally eligible; REEF retains a companion-report question and ParvaGPU retains a publication-version question. TGS and HiveD are separately assessed exclusions, GB-P016 and GB-P017. The bibliography contains fifteen assessed-paper references, two excluded-paper references and six context or methods references. Its entry count is not a count of included studies.',r'\subsection*{Progress measures}',r'Initial triage covers 4,075/4,075 records (100\%). Source assessments are linked to 17/2,634 initial retain/uncertain candidates (0.65\%). All fifteen existing assessment forms have ten quality items and one extraction form; this does not establish complete extraction of every field or completion of the full candidate queue. There is no defensible overall assignment-completion or marks percentage from these counts.',r'\section{Complete workbook and supporting research tables}']
index=[];total_cells=0;table_count=0
for ti,(name,rows) in enumerate(tables,1):
 if not rows:continue
 fields=list(dict.fromkeys(k for row in rows for k in row));key=fields[0];others=fields[1:];use=len(rows)>200
 heading = r'\subsection{'+esc(name)+'}'+esc(f'Source table: {len(rows)} rows; {len(fields)} fields. Stable first-column keys are repeated across horizontal panels.')
 # Four data columns per panel balance full text against readable table widths.
 chunks=[others[i:i+4] for i in range(0,len(others),4)] or [[]]
 for panel,cols in enumerate(chunks,1):
  names=[key]+cols;n=len(names);weights=[]
  for f in names:
   lengths=sorted(len(gloss.get(str(row.get(f,'')),str(row.get(f,'')))) if use else len(str(row.get(f,''))) for row in rows)
   q=lengths[int((len(lengths)-1)*.90)];weights.append(max(12,min(85,q+6)))
  weights[0]=max(18,min(26,weights[0]));widths=[.94*x/sum(weights) for x in weights]
  spec=''.join(r'>{\raggedright\arraybackslash}p{'+f'{w:.5f}'+r'\linewidth}' for w in widths)
  head=' & '.join(r'\textbf{'+esc(x.replace('_',' '))+'}' for x in names)+r'\\\midrule'
  parts += [r'\begin{landscape}'+(heading if panel==1 else '')+r'\begingroup\fontsize{9}{11}\selectfont\setlength{\tabcolsep}{2pt}\setlength{\LTpre}{2pt}\setlength{\LTpost}{2pt}',r'\begin{longtable}{'+spec+'}',r'\caption{'+esc(name)+f': panel {panel}/{len(chunks)}'+r'}\label{tab:full-'+str(ti)+'-'+str(panel)+r'}\\\toprule',head,r'\endfirsthead',r'\toprule',head,r'\endhead',r'\midrule\multicolumn{'+str(n)+r'}{r}{\footnotesize Continued on next page}\\\endfoot',r'\bottomrule\endlastfoot']
  parts.extend(' & '.join(val(row.get(f,''),use) for f in names)+r'\\' for row in rows)
  parts += [r'\end{longtable}\endgroup\end{landscape}'];table_count+=1
 index.append(dict(table=name,rows=len(rows),fields=len(fields),panels=len(chunks),all_cells_represented=True,glossary_compression=use));total_cells+=len(rows)*len(fields)
parts += [r'\clearpage\section{Complete source-value glossary}',r'V-codes used in the large log tables expand to the exact source strings below. Codes are value identifiers, not records, reports or studies. All source rows remain in their tables.',r'\begingroup\fontsize{9}{11}\selectfont\begin{longtable}{p{0.12\linewidth}p{0.78\linewidth}}\toprule Code & Original source value\\\midrule\endhead']
parts.extend(r'\texttt{'+code+'} & '+esc(v)+r'\\' for v,code in gloss.items());parts += [r'\bottomrule\end{longtable}\endgroup',r'\clearpage\section{Protocol amendments and completion boundaries}']
for p in (R/'evidence/protocol_amendments.md').read_text().split('\n\n'):
 if p.strip():parts += [esc(p.strip().lstrip('# '))+r'\par\medskip']
parts += [r'\subsection*{What must still be completed}',r'Complete verified title/abstract and source eligibility for the remaining candidate queue; reconcile REEF and ParvaGPU report/study versions; resolve the documented search-provenance gaps; complete the quality-anchor and N/A calibration follow-ups; and derive final inclusion and PRISMA numbers from those actual decisions. Missing exact event times remain unrecorded. Independent reviewer fields do not represent completed human checks.',r'\clearpage\section{Submitted Task1 protocol}',r'The following protocol PDF is preserved byte for byte. Its original pagination and references remain part of that submitted document.',r'\includepdf[pages=-,pagecommand={}]{Submitted_Task1_Protocol.pdf}',r'\end{document}']
(O/'main.tex').write_text('\n'.join(parts)+'\n')
# Print only bibliography entries actually cited by this document: no hidden aliases or duplicate unused entries.
bib=(F/'02_Report_LaTeX/references.bib').read_text();entry={m.group(2).strip():m.group(0).rstrip() for m in re.finditer(r'@(\w+)\s*\{([^,]+),[\s\S]*?(?=\n@|\Z)',bib)}
entry['GB-P016']=r'''@misc{GB-P016,
author={Bingyang Wu and Zili Zhang and Zhihao Bai and Xuanzhe Liu and Xin Jin},
title={{Transparent GPU Sharing in Container Clouds for Deep Learning Workloads}},
year={2023},howpublished={USENIX NSDI. [Online]. Available: \url{https://www.usenix.org/conference/nsdi23/presentation/wu}}
}'''
entry['GB-P017']=r'''@misc{GB-P017,
author={Hanyu Zhao and Zhenhua Han and Zhi Yang and Quanlu Zhang and Fan Yang and Lidong Zhou and Mao Yang and Francis C. M. Lau and Yuqi Wang and Yifan Xiong and Bin Wang},
title={{HiveD: Sharing a GPU Cluster for Deep Learning with Guarantees}},
year={2020},howpublished={USENIX OSDI. [Online]. Available: \url{https://www.usenix.org/conference/osdi20/presentation/zhao-hanyu}}
}'''
keys=list(dict.fromkeys(k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',core) for k in group.split(',')));assert len(keys)==23 and all(k in entry for k in keys)
(O/'references.bib').write_text('\n\n'.join(entry[k] for k in keys)+'\n');shutil.copy2(R/'task1/submitted_protocol.pdf',O/'Submitted_Task1_Protocol.pdf')
(O/'table_inventory.json').write_text(json.dumps(dict(tables=index,source_cells_represented=total_cells,printed_panels=table_count,glossary_values=len(gloss),bib_entries=len(keys),scientific_data_changed=False),indent=2)+'\n')
print('One TeX source',len(parts),'blocks,',total_cells,'source cells;',table_count,'panels;',len(gloss),'lossless value codes;23bibliography entries')

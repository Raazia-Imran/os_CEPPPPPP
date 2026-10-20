from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]; out=root/'report';d=json.loads((root/'logs/baseline_data.json').read_text());a=json.loads((root/'logs/analysis.json').read_text())
def esc(v):
 s=str(v or '').replace('≥','>=').replace('≤','<=').replace('×','x').replace('–','-').replace('—','-').replace('’',"'").replace('“','"').replace('”','"')
 escaped = ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}.get(x,x) for x in s)
 return re.sub(r'[^\s]{25,}',lambda m: r'\nolinkurl{'+m[0].replace(r'\_', '_').replace(r'\&','&').replace(r'\%','%')+'}',escaped)
def table(head,rows,widths):
 spec=''.join(r'>{\raggedright\arraybackslash}p{'+str(x)+r'\textwidth}' for x in widths)
 return '\n'.join([r'\begin{longtable}{'+spec+'}',r'\toprule',' & '.join(r'\textbf{'+esc(h)+'}' for h in head)+r'\\\midrule\endhead',*[' & '.join(esc(c) for c in r)+r'\\\addlinespace' for r in rows],r'\bottomrule\end{longtable}'])
def cards(name,header,rows):
 txt=[]
 for row in rows:
  txt.append(r'\subsubsection*{'+esc(row[0])+': '+esc(row[1])+ '}')
  txt.append(table(['Dimension','Assessment'],[[header[i],row[i]] for i in range(2,len(header))],[.22,.70]))
 return '\n'.join(txt)
(out/'counts.tex').write_text(table(['Stage','Count'],[r[:2] for r in d['PRISMA Counts'][1:]],[.70,.15]))
(out/'corpus.tex').write_text(table(['Study / report','System / source identity','QA'],[[r[0]+' / '+r[1],r[2]+' ('+str(r[3])+')',str(r[6])+'/'+str(r[7])] for r in d['Studies'][1:]],[.16,.62,.10]))
(out/'taxonomy.tex').write_text(table(['Family / reports','Control and condition','Cost'],[[r[0]+'; '+r[2],r[1]+'. '+r[3],r[5]] for r in a['Taxonomy'][1:]],[.25,.35,.28]))
(out/'comparisons.tex').write_text(table(['Evidence / class','Observation','Interpretation and missing control'],[[r[0]+' '+r[1]+'. '+r[3],r[2],r[4]+'. Missing: '+r[5]] for r in a['Comparability'][1:]],[.26,.28,.34]))
(out/'recommendations.tex').write_text(cards('Recommendations',a['Recommendations'][0],a['Recommendations'][1:]))
(out/'gaps.tex').write_text(table(['Corpus gap','Basis','Next experiment'],[[r[1],r[2],r[4]] for r in a['Research Gaps'][1:]],[.28,.22,.38]))
(out/'validity.tex').write_text(table(['Threat / consequence','Mitigation','Remaining work'],[[r[0]+': '+r[2],r[3],r[4]] for r in a['Validity'][1:]],[.32,.26,.30]))
# IEEE-style numerical bibliography, identities taken from supplied report and workbook.
authors=['L.-X. Ma et al.','F. Xu et al.','S. Choi et al.','Z. Bai et al.','M. Han, H. Zhang, R. Chen, and H. Chen','K. K. W. Ng, H. M. Demoulin, and V. Liu','F. Strati, X. Ma, and A. Klimovic','A. Dhakal, S. G. Kulkarni, and K. K. Ramakrishnan','A. Gujarati et al.','J. Wang, Y. Wang, M. Han, and R. Chen','M. Lee et al.','M. Yu et al.','H. Wu et al.','S. Zhang et al.','W. Shen et al.','Y. Peng and H. Peng','J. Lou et al.','T. Adufu and Y. Kim','M. Chow, A. Jahanshahi, and D. Wong','W. Zhao, A. Jayarajan, and G. Pekhimenko']
full={'P001':'VastPipe: A High-Throughput Inference System via Adaptive Space-Division Multiplexing for Diverse Accelerators','P002':'iGniter: Interference-Aware GPU Resource Provisioning for Predictable DNN Inference in the Cloud','P003':'Serving Heterogeneous Machine Learning Models on Multi-GPU Servers with Spatio-Temporal Sharing','P004':'PipeSwitch: Fast Pipelined Context Switching for Deep Learning Applications','P005':'Microsecond-scale Preemption for Concurrent GPU-accelerated DNN Inferences'}
bib=[]
for i,r in enumerate(d['Studies'][1:]):
 title=full.get(r[1],r[2]);bib.append('@misc{'+r[1]+',\n author={'+authors[i].replace(', and ',' and ').replace(', ',' and ').replace(' et al.',' and others')+'},\n title={{'+title+'}},\n year={'+str(r[3])+'},\n howpublished={'+r[4]+'},\n note={Report '+r[1]+', study '+r[0]+'. Source: \\url{'+r[9]+'}}\n}')
bib.append('@article{P023,author={Mingcong Han and Rong Chen and Weihang Shen and Hanze Zhang and Jinrong Yang and Haibo Chen},title={Real-time, Work-conserving GPU Scheduling for Concurrent DNN Inference},journal={ACM Transactions on Computer Systems},volume={44},number={1},year={2025},note={Article 1, pp. 1--42. Online publication 2025; issue indexed 2026. Companion of P005},doi={10.1145/3768622}}')
bib+=['@article{prisma,author={Matthew J. Page and others},title={The PRISMA 2020 statement: An updated guideline for reporting systematic reviews},journal={BMJ},volume={372},pages={n71},year={2021},doi={10.1136/bmj.n71}}','@article{prismas,author={Melissa L. Rethlefsen and others},title={PRISMA-S: An extension to the PRISMA statement for reporting literature searches in systematic reviews},journal={Systematic Reviews},volume={10},pages={39},year={2021},doi={10.1186/s13643-020-01542-z}}','@techreport{kitchenham,author={Barbara Kitchenham and Stuart Charters},title={Guidelines for performing systematic literature reviews in software engineering},institution={Keele University and University of Durham},number={EBSE-2007-01},year={2007},note={Version 2.3}}','@article{benchmark,author={Cheol-Ho Hong and Ivor Spence and Dimitrios S. Nikolopoulos},title={GPU Virtualization and Scheduling Methods: A Comprehensive Survey},journal={ACM Computing Surveys},volume={50},number={3},year={2017},note={Article 35},doi={10.1145/3068281}}']
(out/'references.bib').write_text('\n\n'.join(bib))
append=[r'\appendix\section{Exact search register}\label{app:search}','The following entries are preserved from the supplied workbook. Date precision, provenance and count discrepancies remain as recorded.']
for r in d['Search Log'][1:]:
 append += [r'\subsection{'+esc(r[0])+'}',table(['Field','Recorded value'],list(zip(d['Search Log'][0][1:],r[1:])),[.25,.65])]
append += [r'\section{Complete study appraisal and extraction cards}', 'These cards preserve the 20 supplied study forms. They are an audit appendix; the main text is organized by mechanism and RQ. Scores are not a claim of independent verification.']
for r in d['Extraction'][1:]:
 append += [r'\clearpage\subsection{'+esc(r[0]+' / '+r[1]+' '+r[2])+'}',r'\cite{'+r[1]+'}',table(['Field','Extracted content'],list(zip(d['Extraction'][0][3:18],r[3:18])),[.23,.67])]
 qr=[x for x in d['QA'][1:] if x[0]==r[1]]
 append += [table(['QA','Score / maximum','Rationale and anchor'],[[x[1],str(x[2])+' / '+str(x[3]),str(x[4])+'. '+str(x[5])] for x in qr],[.07,.13,.68])]
append += [r'\clearpage\section{Complete outcome register}\label{app:evidence}','Reported observations remain attached to their baseline, hardware, workload and source. Values are preserved as supplied, including ranges, approximate values and maxima.']
for r in d['Evidence'][1:]:
 append += [r'\subsection*{'+esc(r[0]+' / '+r[1]+' '+r[2])+'}',table(['Field','Evidence'],list(zip(d['Evidence'][0][3:],r[3:])),[.22,.68])]
append += [r'\section{Calculated quantities}',table(['Calculation','Formula and input','Value / limit'],[[r[0]+' '+r[1],r[3]+': '+r[4],r[5]+' '+r[6]+'. '+r[8]] for r in d['Calculations'][1:]],[.15,.43,.30]),r'\section{Guideline deliverable crosswalk}',table(['Item','Requirement','Artifact','Status / qualification'],a['Requirements'][1:],[.07,.26,.32,.22]),r'\section{Journal benchmark and drafting standard}',r'The organizational benchmark is Hong et al.\ \cite{benchmark}. Its layer-based taxonomy and comparison structure inform the draft. The current review adds the instructor-required search, selection and appraisal records. Journal standing is contextual and does not certify the draft as publishable. See the separate benchmark note for the dated publisher-metric check.',r'\section{Files, timestamps and remaining checks}','The Excel workbook preserves the original 14 tabs and adds analytical and audit tabs. The complete 4,075-row screening log and 114 duplicate links remain electronically accessible rather than being expanded into hundreds of print pages. New activity timestamps are in UTC and Pakistan time; historical batch/build values retain their original meaning.',table(['Priority task','Evidence required'],[[r[2],r[3]+'. '+r[7]] for r in a['Human Checks'][1:]],[.39,.51])]
(out/'appendices.tex').write_text('\n\n'.join(append))
(out/'main.tex').write_text(r'''\documentclass[12pt,a4paper]{article}
\usepackage[margin=24mm]{geometry}
\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage{lmodern,microtype}
\usepackage{graphicx,longtable,booktabs,array,amsmath,hyperref,fancyhdr,xurl}
\hypersetup{colorlinks=true,linkcolor=black,citecolor=black,urlcolor=blue}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}\setlength{\emergencystretch}{3em}
\renewcommand{\arraystretch}{1.18}\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small GPU sharing for multi-tenant inference}\fancyhead[R]{\small Task 3 draft}\fancyfoot[C]{\thepage}\setlength{\headheight}{15pt}
\begin{document}
\begin{titlepage}\centering
{\large NED University of Engineering and Technology\\Department of Software Engineering\par}\vspace{28mm}
{\LARGE\bfseries GPU Sharing for Multi-Tenant Inference\par}\vspace{6mm}
{\Large A Bounded Systematic Evidence Synthesis of Performance, Isolation and Engineering Trade-offs\par}\vspace{20mm}
{\large Operating Systems CEP -- Topic 23\\Task 3: First Complete Draft\par}\vspace{16mm}
Eshaal Faisal (SE-24008)\\Raazia Imran Reshamwala (SE-24009)\\Rameen Siddiqui (SE-24016)
\vfill 21 October 2026\\[6mm]
\small Based on the supplied Task 2 corpus: 21 report versions, 20 unique studies.\\The bounded selection and remaining verification work are explicitly reported.
\end{titlepage}
\begin{abstract}
GPU sharing for multi-tenant inference requires a choice among resource efficiency, request latency, isolation and implementation cost. This bounded review synthesizes 20 studies represented by 21 reports using the supplied search, screening, appraisal and extraction records. The register contains 4,189 occurrences and 4,075 canonical records after 114 duplicate links. It records 3,493 screening exclusions, 559 retained records not advanced under the stopping rule, and 23 source-assessed reports, of which two are excluded. The analysis classifies temporal scheduling, software spatial sharing, hardware partitions, runtime/API mediation and hybrid controls. It uses 200 appraisal items, 52 reported observations and two transparent calculations. The evidence supports conditional selection: increased concurrency can improve throughput while increasing latency; foreground protection can reduce background progress; and higher model density can introduce transfer, compatibility or trust costs. No pooled effect or universal winning mechanism is supported. Recommendations are linked to source conditions and remain limited by bounded selection, title-only screening, a single assessment pass and source-version uncertainty.
\end{abstract}
\tableofcontents\clearpage
\input{body.tex}
\clearpage\bibliographystyle{ieeetr}\bibliography{references}
\clearpage\input{appendices.tex}
\end{document}
''')
print('Report sources generated')

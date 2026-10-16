"""Separate, source-linked QA and extraction documents for the current report set."""
import csv,json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,PageBreak,Spacer,KeepTogether
R=Path(__file__).resolve().parents[1];E=R/'evidence';O=R/'task2/submission'
def read(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
forms=read(E/'study_extraction_form.csv');qa=read(R/'task2/qa/qa_rationale_table.csv');matrix=read(R/'task2/qa/qa_score_matrix.csv');outcomes=read(E/'extraction.csv')
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'));pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'));pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB')
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyX',fontName='DV',fontSize=10.5,leading=14.5,spaceAfter=8));styles.add(ParagraphStyle(name='CellX',parent=styles['BodyX'],fontSize=8.5,leading=11.5,spaceAfter=0));styles.add(ParagraphStyle(name='HeadX',fontName='DVB',fontSize=15,leading=19,spaceAfter=12,keepWithNext=True));styles.add(ParagraphStyle(name='SubX',parent=styles['HeadX'],fontSize=11,leading=15,spaceBefore=9,spaceAfter=7))
def p(x,style='BodyX'):return Paragraph(escape(str(x)).replace('\n','<br/>'),styles[style])
def table(rows,widths):
 t=Table([[p(v,'CellX') for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E7EEF5')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#C7D4E1'))]));return t
def footer(canvas,doc):
 canvas.setFont('DV',8);canvas.drawString(50,28,'Group B | Source-based AI assessment | Final selection incomplete');canvas.drawRightString(A4[0]-50,28,str(doc.page))
def build(name,story):SimpleDocTemplate(str(O/name),pagesize=A4,leftMargin=50,rightMargin=50,topMargin=45,bottomMargin=48).build(story,onFirstPage=footer,onLaterPages=footer)
story=[p('Group B Quality Assessment','HeadX'),p(f'{len(forms)} assessed report forms | {len(qa)} Q1-Q10 item rows | 16 October2026'),p('Use the submitted0-2rubric. Justified N/A removes its maximum. Below60% is sensitivity only. These are first AI assessments; original scores and unperformed independent fields are preserved. ParvaGPU source-version uncertainty and REEF companion identity prevent treating every form as a final study.'),table([['Report','Title','Score / max','Status']]+[[x['report_id'],x['title'],x['raw_sum']+'/'+x['applicable_max'],x['eligibility_status']] for x in matrix],[65,230,70,130]),PageBreak(),p('Q1-Q10 checklist','HeadX')]
rules=read(R/'task2/qa/qa_checklist.csv');story.append(table([['Item','Criterion','Score2requires']]+[[x['criterion'],x['label'],x['score_2_requires']] for x in rules],[35,130,330]))
for f in forms:
 rid=f['report_id'];rows=[x for x in qa if x['report_id']==rid]
 story += [PageBreak(),p(rid+' | '+f['title'],'HeadX'),p('Source: '+f['source']+' | '+f['source_anchor']),p('Status: '+f['eligibility_status']+'. Independent scoring unperformed.'),table([['Q','Score / max','Rationale','Exact source anchor / precision']]+[[x['criterion'],x['score']+'/'+x['maximum'],x['rationale'],x['anchor']+' | '+x['anchor_precision']] for x in rows],[28,55,247,165]),p('Assessor: '+'; '.join(sorted({x['reviewer'] for x in rows}))),p('Original dates: '+'; '.join(sorted({x['checked_at_utc'] for x in rows if x['checked_at_utc']})) if any(x['checked_at_utc'] for x in rows) else 'Original item dates were not populated; no retrospective date invented.')]
build('GroupB_QA_Tables.pdf',story)
story=[p('Group B Topic-Specific Data Extraction','HeadX'),p(f'{len(forms)} report forms | {len(outcomes)} reported outcome rows | 2 separately calculated outcomes'),p('Report forms are not final included studies. Units, conditions, baselines and source anchors control every interpretation. Not extracted means unchecked; not reported is limited to the checked section stated in the cell. Source preprints, cluster-only results, training results and non-GPU results are not silently converted into eligible local inference evidence.'),table([['Report','Study linkage','Title','Eligibility']]+[[f['report_id'],f['study_id'],f['title'],f['eligibility_status']] for f in forms],[65,80,220,130])]
fields=['authors','year','venue','doi','source','source_anchor','mechanism','gpu_hardware','cpu_memory','os_kernel','driver_runtime','models','tenant_mix','batch_load_slo','baseline','latency','throughput','resource_usage','scalability','energy','reliability','security_fault_isolation','overhead','advantages','limitations','tradeoffs']
for f in forms:
 rid=f['report_id'];story += [PageBreak(),p(rid+' | '+f['title'],'HeadX'),table([['Field','Registered evidence']]+[[k.replace('_',' '),f[k] or 'not resolved'] for k in fields],[125,370]),p('Reported outcomes','SubX')]
 for x in outcomes:
  if x['report_id']!=rid:continue
  rows=[['Outcome ID',x['outcome_id']],['Metric / value / unit',x['metric']+' | '+x['value']+' | '+x['units']],['Hardware / mechanism',x['hardware']+' | '+x['mechanism']],['Workload / conditions',x['workload']],['Baseline',x['baseline']],['Source anchor',x['source_anchor']],['Limit / interpretation',x['caveat']],['Assessor / status',x['reviewer']+' | '+x['check_status']]]
  story += [KeepTogether(table(rows,[125,370])),Spacer(1,9)]
story += [PageBreak(),p('Calculated outcomes: formulas and inputs','HeadX')]
for x in read(E/'calculated_outcomes.csv'):story += [table([['Field','Calculation evidence']]+[[k,v] for k,v in x.items()],[125,370]),Spacer(1,12)]
build('GroupB_Data_Extraction.pdf',story)
print('Saved separate QA and extraction PDFs')

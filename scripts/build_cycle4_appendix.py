"""Publish the current register as an explicitly interim QA/extraction appendix."""
import csv, json, re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

R=Path(__file__).resolve().parents[1]; O=R/'task2/qa'; E=R/'evidence'
def read(p):
    with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='B',fontName='DV',fontSize=10,leading=14,spaceAfter=7))
styles.add(ParagraphStyle(name='SmallB',parent=styles['B'],fontSize=8,leading=11,spaceAfter=0,splitLongWords=True))
styles.add(ParagraphStyle(name='H',fontName='DVB',fontSize=16,leading=21,textColor=colors.HexColor('#243B53'),spaceAfter=12,keepWithNext=True))
styles.add(ParagraphStyle(name='SH',parent=styles['H'],fontSize=12,leading=16,spaceBefore=10,spaceAfter=7))
def p(text,style='B'):
    return Paragraph(escape(str(text)).replace('\n','<br/>').replace('\u2011','-'),styles[style])
def table(rows,widths):
    t=Table([[p(v,'SmallB') for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E7EEF5')),('FONTNAME',(0,0),(-1,0),'DVB'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LINEBELOW',(0,0),(-1,0),.8,colors.HexColor('#829AB1')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#D9E2EC'))]))
    return t
forms=read(E/'study_extraction_form.csv');qa=read(O/'qa_rationale_table.csv');outcomes=read(E/'extraction.csv')
matrix=read(O/'qa_score_matrix.csv');checklist=read(O/'qa_checklist.csv');followup={x['report_id']:x for x in read(O/'qa_followup.csv')}
story=[p('GPU sharing for multi-tenant inference','H'),p('Quality assessment and data extraction','H'),
    p('Group B | Interim evidence appendix | 16 October 2026'),
    p('Nine provisional reports; 90 Q1-Q10 items; 34 registered outcome rows. Initial AI assessments only. Independent checks, final eligibility, report-to-study reconciliation and final PRISMA remain pending.'),
    p('This appendix replaces the older seven-report handoff tables for current QA/extraction coverage. It is supporting material for the SLR, not the final synthesis report. Paper-by-paper tables must feed cross-study comparison, trade-off analysis and conditional recommendations.'),
    p('What has been checked','SH'),
    p('Register keys, ten-item coverage, permitted scores, N/A denominators and totals were recalculated. Existing source scores and outcomes were preserved. This pass does not represent a new full-source appraisal or a real second reviewer.'),
    p('What remains open','SH'),
    p('Twenty legacy QA items have section/figure anchors without printed PDF pages. Both provisional N/A judgments require calibration. All nine reports need independent checks; PipeSwitch scope and REEF conference/journal identity need resolution. Unchecked extraction fields remain not_extracted, rather than being converted to absent findings.'),
    p('Measured review progress','SH'),
    table([['Measure','Verified register state'],['Identification','4,189 occurrences; 111 applied duplicate links; 4,078 canonical records'],['Preliminary screening','2,487 active recommendations (61.0%); 1,591 awaiting first recommendation'],['Incoming AI opinions','1,831 preserved separately; 50 disagreements within 240 overlapping recommendations'],['Study selection','9 provisional report forms; final eligible reports and unique studies pending']], [130,365]),
    PageBreak(),p('Group B QA checklist and scoring','H'),
    p('Authority: submitted protocol section 10, Table 8, printed pp11-12. Score 0 = absent/unclear, 1 = partly addressed, 2 = sufficiently supported. Full maximum 20. Use justified N/A only for a claim the paper does not make; subtract its maximum from the applicable denominator.'),
    p('Normalized percentage = applicable score / applicable maximum x 100. Below 60% is a sensitivity analysis, not an exclusion gate. No initial report is below that line; calibration and source verification remain pending.'),
    table([['Item','Criterion','Requirements for score 2']]+[[x['criterion'],x['label'],x['score_2_requires']] for x in checklist],[36,126,333]),
    PageBreak(),p('Study-by-criterion matrix','H'),
    p('Report IDs are not unique-study counts. Scores remain preliminary; no human validation is implied. NA = justified provisional N/A, not a zero score.'),
    table([['ID']+[f'Q{i}' for i in range(1,11)]+['Total','%']]+[[x['report_id'].replace('GB-','')]+[x[f'Q{i}'] for i in range(1,11)]+[x['raw_sum']+'/'+x['applicable_max'],x['normalized_pct']] for x in matrix],[49]+[29]*10+[69,87]),
    p('Report key','SH'),table([['Report','Title / initial QA status']]+[[x['report_id'],x['title']+' | '+x['qa_status']] for x in matrix],[75,420]),
    p('N/A calibration','SH'),p('GB-P001 VastPipe Q7 and GB-P006 Paella Q9 are provisional N/A judgments. They are preserved, not ratified. The protocol requires a two-study calibration; no completed independent calibration is recorded.')]
for form in forms:
    rid=form['report_id']; m=next(x for x in matrix if x['report_id']==rid)
    story += [PageBreak(),p(rid+' | '+form['title'],'H'),p('Identity and assessment status','SH')]
    assessors='; '.join(sorted({x['reviewer'] for x in qa if x['report_id']==rid}))
    recorded_dates='; '.join(sorted({x['checked_at_utc'] for x in qa if x['report_id']==rid and x['checked_at_utc']})) or 'Item-level dates not populated in original register'
    ident=[['Field','Registered evidence'],['Authors / year / venue',' / '.join(form[k] for k in ['authors','year','venue'])],['DOI',form['doi'] or 'No DOI resolved; retain official conference URL'],['Study linkage',form['study_id']],['Source / anchor',form['source']+' | '+form['source_anchor']],['Assessor / recorded date',assessors+' | '+recorded_dates],['Eligibility',m['eligibility_status']+'; final and independent decisions pending'],['QA total',m['raw_sum']+'/'+m['applicable_max']+' ('+m['normalized_pct']+'%); AI first review'],['Required follow-up',followup[rid]['calibration_or_scope_task']]]
    story += [table(ident,[110,385]),p('Detailed QA rationales','SH'),p('Initial assessor, status and evidence anchors come from evidence/quality.csv. Source-page precision is an audit flag, not a claim that this cycle independently verified the cited page.')]
    story.append(table([['Q','Score / max','Rationale','Source anchor']]+[[x['criterion'],x['score']+'/'+x['maximum'],x['rationale'],x['anchor']] for x in qa if x['report_id']==rid],[28,57,254,156]))
    story += [p('Study-level extraction and missingness','SH')]
    fields=['mechanism','gpu_hardware','cpu_memory','os_kernel','driver_runtime','models','tenant_mix','batch_load_slo','baseline','resource_usage','scalability','energy','reliability','security_fault_isolation','overhead','advantages','limitations','tradeoffs']
    story.append(table([['Field','Registered value']]+[[k.replace('_',' '),form[k]] for k in fields],[125,370]))
    story += [p('Registered quantitative outcomes','SH'),p('These are outcome rows, not separate studies. Preserve baseline, statistic, units and limitations. Not_extracted means unchecked; do not read it as not reported. Headline values require a real independent source check.')]
    for x in outcomes:
        if x['report_id']!=rid:continue
        story.append(KeepTogether(table([['Outcome ID',x['outcome_id']],['Metric / value / unit',x['metric']+' | '+x['value']+' | '+x['units']],['Configuration',x['mechanism']+' | '+x['hardware']+' | '+x['workload']],['Baseline',x['baseline']],['Exact registered anchor',x['source_anchor']],['Limits / interpretation',x['caveat']],['Review status',x['reviewer']+' | '+x['check_status']+'; independent check pending']],[125,370])))
        story.append(Spacer(1,10))
def footer(canvas,doc):
    canvas.setFont('DV',8);canvas.setFillColor(colors.HexColor('#52667A'))
    canvas.drawString(50,28,'Group B | Interim QA / extraction | Independent checks pending')
    canvas.drawRightString(A4[0]-50,28,str(doc.page))
doc=SimpleDocTemplate(str(O/'GroupB_Current_QA_and_Extraction.pdf'),pagesize=A4,leftMargin=50,rightMargin=50,topMargin=45,bottomMargin=47,title='Group B: current QA and extraction evidence',author='Group B; AI-assisted interim register export')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Saved current QA and extraction appendix')

from pathlib import Path
import csv,json,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("DejaVu","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
R=Path(__file__).resolve().parents[1];F=R/'final things';S=F/'01_Statistics_and_Papers'
def rows(p):return list(csv.DictReader(p.open()))
styles=getSampleStyleSheet();
for n in ['Title','Heading1','Heading2']:styles[n].fontName='DejaVuBold'
styles.add(ParagraphStyle(name='CellX',fontName='DejaVu',fontSize=9,leading=12,spaceAfter=0));styles.add(ParagraphStyle(name='BodyX',fontName='DejaVu',fontSize=10,leading=14,spaceAfter=7))
def p(x,style='CellX'):return Paragraph(html.escape(str(x)),styles[style])
def table(headers,data,widths):
 allrows=[[p(x) for x in headers]]+[[p(x) for x in row] for row in data]
 t=Table(allrows,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCE6EF')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#425466')),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#D9E0E7')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));return t
def footer(c,d):c.setFont('DejaVu',8);c.setFillColor(colors.HexColor('#52616B'));c.drawString(40,23,'Group B | Current evidence checkpoint | Final study selection pending');c.drawRightString(A4[0]-40,23,str(d.page))
story=[p('Group B: statistics and paper list','Title'),p('GPU sharing for multi-tenant inference | 16 October 2026','BodyX'),p('Read this first. The research is not fully screened yet. The current 15 QA/extraction forms are not a final list of 15 included studies.','BodyX')]
db=rows(S/'DATABASE_STATISTICS.csv');story+=[p('Starting records by source','Heading2'),table(['Source','Occurrences','Linked repeats','Canonical'],[[x['database'],x['imported_occurrences'],x['linked_repeats_attributed'],x['canonical_records']] for x in db]+[['TOTAL',4189,114,4075]],[190,90,100,130])]
statistics=rows(S/'SELECTION_STATISTICS.csv');take=[0,1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,18]
story+=[Spacer(1,9),p('Narrowing and assessment coverage','Heading2'),table(['Stage','Count'],[[statistics[i]['stage'],statistics[i]['count']] for i in take],[410,100]),p('Preliminary exclusion proposals: EC1=851; EC2=453; EC3=6; EC5=131. These 1,441 proposals are not final screened exclusions. The two source-assessed EC2 exclusions belong to the assessed report slice.','BodyX'),PageBreak()]
cat=rows(S/'CURRENT_ASSESSED_PAPERS_AND_DOIS.csv');paperrows=[]
for x in cat:
 identifier=x['doi'] if x['doi'].startswith('10.') else 'Official PDF; DOI not verified'
 paperrows.append([x['report_id']+' '+x['short_name']+' ('+x['year']+')',identifier,x['assessment_status'].replace('_',' ')])
story+=[p('The 15 reports currently carrying QA/extraction','Heading1'),p('Six conference/journal DOIs are identified below. For the other nine reports, use the official/accessed PDF links in CURRENT_ASSESSED_PAPERS_AND_DOIS.csv. An unverified DOI is not invented.','BodyX'),table(['Report / paper','DOI or source identifier','Current status'],paperrows,[170,190,150]),Spacer(1,8),p('Source-assessed exclusions','Heading2'),table(['Report','Decision / reason'],[[x['report_id']+' '+x['title'],x['criterion']+': '+x['reason']] for x in rows(S/'ASSESSED_EXCLUSIONS.csv')],[210,300]),p('REEF: conference/journal study relationship is unresolved. ParvaGPU: the conference DOI is identified, but extracted evidence comes from the accessed arXiv version; final-publication equivalence is unresolved. Other assessments remain provisional.','BodyX'),PageBreak()]
story+=[p('What is complete, and what is pending?','Heading1'),table(['Cycle','Current state','Remaining'],[[x['cycle']+' '+x['name'],x['status'],x['remaining']] for x in rows(F/'05_Protocol_and_Audit/CYCLE_STATUS.csv')],[165,145,200]),Spacer(1,10),p('Through instructor Heading 14','Heading2')]
audit=rows(F/'05_Protocol_and_Audit/Requirements_1_to_14.csv');story+=[table(['Heading','State','Specific remaining work'],[[x['guideline_heading']+' '+x['requirement'],x['state'],x['remaining']] for x in audit if int(x['guideline_heading'])>=8],[155,60,295])]
info=json.loads((S/'statistics.json').read_text());story+=[Spacer(1,9),p('Recorded dates and timestamps','Heading2'),p('All 4,075 screening rows have a recorded date after matching existing vote events. Exact event timestamps remain unrecorded for '+str(info['event_timestamps_missing'])+' rows. These stay “Not recorded”. A metadata-check timestamp is not substituted for an actual screening event. No searches, reviewer actions or times were fabricated.','BodyX')]
SimpleDocTemplate(str(S/'START_HERE_Statistics_and_Papers.pdf'),pagesize=A4,rightMargin=40,leftMargin=40,topMargin=35,bottomMargin=40).build(story,onFirstPage=footer,onLaterPages=footer)
print('Statistics PDF built')

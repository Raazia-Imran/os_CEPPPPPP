import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const r=process.env.OS_CEP_ROOT,d=JSON.parse(await fs.readFile(r+'/task2/qa/task2_consolidated_input.json','utf8'));const wb=Workbook.create(),ov=wb.worksheets.add('Overview');
const xl=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const numberFields=new Set(['qa_raw','qa_applicable_max','qa_percentage','reported_outcomes','score','maximum','original_characters','normalized_characters','calculated_value']);
for(const [name,rows] of Object.entries(d.tabs)){
 const sh=wb.worksheets.add(name),fields=Object.keys(rows[0]),end=xl(fields.length-1),last=rows.length+1;sh.showGridLines=false;
 const vals=[fields,...rows.map(x=>fields.map(k=>{const v=x[k]??'';if(['screening_date','screening_timestamp_utc','assessment_date'].includes(k)&&/^\d{4}-\d{2}-\d{2}(T.*)?$/.test(v))return new Date(v);if(numberFields.has(k)&&v!==''&&!isNaN(Number(v)))return Number(v);return typeof v==='string'&&v.startsWith('=')?"'"+v:v;}))];
 sh.getRange(`A1:${end}${last}`).values=vals;sh.getRange(`A1:${end}${last}`).format={font:{name:'Arial',size:10},columnWidth:25,rowHeight:35,wrapText:true};
 sh.getRange(`A1:${end}1`).format={fill:'#243B53',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true};
 for(let i=0;i<fields.length;i++){
  const k=fields[i],range=sh.getRange(`${xl(i)}1:${xl(i)}${last}`);
  if(/title|source|anchor|reason|rationale|method|basis|query|filters|fields|authors|limits|gaps|scope|action/.test(k))range.format.columnWidth=58;
  if(['screening_date','assessment_date'].includes(k)){sh.getRange(`${xl(i)}2:${xl(i)}${last}`).setNumberFormat('yyyy-mm-dd');range.format.horizontalAlignment='center';}
  if(k==='screening_timestamp_utc'){sh.getRange(`${xl(i)}2:${xl(i)}${last}`).setNumberFormat('yyyy-mm-dd hh:mm:ss');range.format.horizontalAlignment='center';}
 }
 sh.getRange(`A2:${end}${last}`).format.autofitRows();sh.freezePanes.freezeRows(1);sh.freezePanes.freezeColumns(1);
}
const papers=wb.worksheets.getItem('Paper list');
for(let i=0;i<15;i++){const row=i+2;papers.getRange(`I${row}`).formulas=[[`=SUMIF('QA items'!A2:A151,A${row},'QA items'!C2:C151)`]];papers.getRange(`J${row}`).formulas=[[`=SUMIF('QA items'!A2:A151,A${row},'QA items'!D2:D151)`]];papers.getRange(`K${row}`).formulas=[[`=I${row}/J${row}`]];papers.getRange(`L${row}`).formulas=[[`=COUNTIF(Outcomes!A2:A46,A${row})`]];}
papers.getRange('K2:K16').setNumberFormat('0.0%');
ov.showGridLines=false;ov.getRange('A1').values=[['Group B Task2: start here']];ov.getRange('A1').format.font={name:'Arial',size:16,bold:true};
const metrics=[['Imported occurrences',4189,'Four databases: 4,169; supplementary: 20'],['Applied duplicate links',114,'Original occurrences remain preserved'],['Canonical records',4075,'4,189 - 114'],['Initial automated triage',4075,'Not complete verified abstract screening'],['Preliminary exclude proposals',1441,'Not final screened exclusions'],['Retain / uncertain',2634,'Not all eligible'],['Source-assessed reports',17,'15 forms and 2 assessed EC2 exclusions'],['QA/extraction forms',15,'13 provisional and 2 unresolved cases'],['Q1-Q10 items',150,'Ten per form'],['Reported outcomes',45,'Not 45 papers'],['Separate calculations',2,'Not author-reported measurements'],['Unassessed candidate records',2617,'No linked source assessment'],['Final included studies','Not established','Selection and report-to-study reconciliation unfinished'],['Reference entries',23,'15 assessed-paper refs; 2 excluded-paper refs; 6 context/method refs'],['Missing exact event times',798,'Not recorded; actual dates preserved']];
ov.getRange('A3:C3').values=[['Measure','Count/status','Meaning']];ov.getRange('A4:C18').values=metrics;
ov.getRange('B4').formulas=[['=COUNTA(Duplicates!A2:A4190)']];ov.getRange('B5').formulas=[['=COUNTIF(Duplicates!E2:E4190,"linked_repeat")']];ov.getRange('B6').formulas=[['=COUNTA(\'Screening log\'!A2:A4076)']];ov.getRange('B8').formulas=[['=COUNTIF(\'Screening log\'!G2:G4076,"exclude_recommendation")']];ov.getRange('B9').formulas=[['=COUNTIF(\'Screening log\'!G2:G4076,"retain_or_uncertain")']];
ov.getRange('B10').formulas=[['=COUNTA(\'Paper list\'!A2:A18)']];ov.getRange('B11').formulas=[['=COUNTA(\'Study extraction\'!A2:A16)']];ov.getRange('B12').formulas=[['=COUNTA(\'QA items\'!A2:A151)']];ov.getRange('B13').formulas=[['=COUNTA(Outcomes!A2:A46)']];
ov.getRange('A21:C24').values=[['How to read','Paper list','All 17 assessed reports; QA/extraction use the same 15 IDs, GB-P001–GB-P015'],['Main PDF','GroupB_Task2_Through14.pdf','Core report plus complete research tables as appendices'],['QA and extraction','QA items / Study extraction / Outcomes','Paper IDs join all tables; outcome rows are separate measurements'],['Authorship / method','Three project authors; automated initial assessment','No unperformed human votes or final decisions are claimed']];
ov.getRange('A27:D27').values=[['Measured coverage','Numerator','Denominator','Coverage']];ov.getRange('A28:C31').values=[['Initial triage records',4075,4075],['Candidates linked to source assessment',17,2634],['QA items for current 15 forms',150,150],['Extraction forms for current 15 QA reports',15,15]];
for(let row=28;row<=31;row++)ov.getRange(`D${row}`).formulas=[[`=B${row}/C${row}`]];
ov.getRange('D28:D31').setNumberFormat('0.00%');ov.getRange('A33').values=[['These are coverage measures, not an overall assignment or grading percentage.']];
ov.getRange('A3:D33').format={font:{name:'Arial',size:11},wrapText:true,rowHeight:45};ov.getRange('A1:A33').format.columnWidth=38;ov.getRange('B1:B33').format.columnWidth=30;ov.getRange('C1:C33').format.columnWidth=84;ov.getRange('D1:D33').format.columnWidth=18;
ov.getRange('A3:C3').format={fill:'#243B53',font:{color:'#FFFFFF',bold:true},rowHeight:35};ov.getRange('A27:D27').format={fill:'#243B53',font:{color:'#FFFFFF',bold:true},rowHeight:35};ov.getRange('B4:B18').format.horizontalAlignment='center';ov.getRange('B4:B15').setNumberFormat('#,##0');
wb.recalculate();const actual=[4,5,6,8,9,10,11,12,13].map(n=>ov.getRange('B'+n).values[0][0]);if(actual.join(',')!==[4189,114,4075,1441,2634,17,15,150,45].join(','))throw Error('Counts mismatch:'+actual);
for(let i=0;i<15;i++){const row=i+2,q=d.qa_matrix[i];if(papers.getRange('I'+row).values[0][0]!==Number(q.raw_sum)||papers.getRange('J'+row).values[0][0]!==Number(q.applicable_max))throw Error('QA mismatch');}
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:10},maxChars:1000})).ndjson);
for(const name of ['Overview',...Object.keys(d.tabs)]){const img=await wb.render({sheetName:name,range:name==='Overview'?'A1:C24':'A1:D5',format:'png',scale:1.1});await fs.writeFile(process.env.OS_CEP_PREVIEW_DIR+'/'+name.replaceAll(' ','_')+'.png',new Uint8Array(await img.arrayBuffer()));}
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(r+'/final things/06_Task2_Submission/GroupB_Task2_Workbook.xlsx');console.log('Saved13-tab Task2 workbook;counts and15QA totals reconcile');

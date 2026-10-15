import fs from 'node:fs/promises';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';
const root=process.env.OS_CEP_ROOT;
if(!root)throw new Error('Set OS_CEP_ROOT to the absolute repository root');
const d=JSON.parse(await fs.readFile(root+'/task2/tracker/workbook_input.json','utf8'));
const wb=Workbook.create();const summary=wb.worksheets.add('Summary');
function col(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
summary.showGridLines=false;
summary.getRange('A2:D2').values=[['Group B evidence checkpoint',null,null,null]];
summary.getRange('A2').format.font={name:'Arial',size:16,bold:true};
summary.getRange('A4:C4').values=[['Metric','Count / status','Meaning']];
summary.getRange('A5:C16').values=[
['Imported occurrences',null,'Original source rows'],
['Exact linked repeats',null,'Title/version pairs remain separate'],
['Canonical review queue',null,'Records requiring selection decisions'],
['First-review recommendations',null,'Title or explicit publication-type check'],
['First-review coverage',null,'Recommendations divided by canonical queue'],
['Final independent decisions','Pending','Do not substitute first votes for final exclusions'],
['Priority reports source-checked',d.progress.source_checked_reports,'Bounded source checks; final inclusion pending'],
['New checked outcome rows',d.progress.new_outcome_rows,'Independent numerical checks pending'],
['First-review QA reports',d.progress.appraised_reports,'Group B 0-2 rubric; no copied scores'],
['Original possible version pairs',41,'See Version audit for current dispositions'],
['ScienceDirect','Deferred','Earlier RIS originals preserved outside active counts'],
['ACM run mapping','Partly recovered','Search log recovered; 79-file mapping and counts unresolved']];
summary.getRange('A19:C19').values=[['First-review quality calibration','Raw score','Applicable maximum']];
summary.getRange('A20:A21').values=[['GB-P001 VastPipe (local GPU evidence)'],['GB-P002 iGniter']];
summary.getRange('D19').values=[['Normalized']];
for(const [name,rows] of Object.entries(d.sheets)){
 const sh=wb.worksheets.add(name);sh.showGridLines=false;
 let fields=[...new Set(rows.flatMap(r=>Object.keys(r)))];
 if(name==='Screening') fields=[...new Set(['record_id','database','title','priority','reviewer_1_vote','reviewer_2_vote','screening_decision','criterion','reason','doi','fulltext_status',...fields])];
 if(name==='Records') fields=['record_id','canonical_record_id','database','title','authors','year','doi','url','entry_type','source_run','source_file','source_position','source_hash','abstract'];
 const vals=[fields,...rows.map(r=>fields.map(k=>{
 let v=r[k]??'';
 if(name==='Quality' && ['score','maximum'].includes(k) && v!=='' && v!=='NA')return Number(v);
 if(name==='Import manifest' && ['bytes','occurrences'].includes(k))return Number(v);
 return typeof v==='string'&&v.startsWith('=')?"'"+v:v;
 }))];
 if(!fields.length)continue;
 const end=col(fields.length-1);sh.getRange(`A1:${end}${vals.length}`).values=vals;
 sh.getRange(`A1:${end}${vals.length}`).format.font={name:'Arial',size:10};
 sh.getRange(`A1:${end}1`).format={fill:'#243B53',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:38,wrapText:true};
 sh.getRange(`A2:${end}${vals.length}`).format.rowHeight=48;
 sh.getRange(`A1:${end}${vals.length}`).format.columnWidth=24;
 sh.getRange(`A2:${end}${vals.length}`).format.wrapText=true;
 sh.freezePanes.freezeRows(1);sh.freezePanes.freezeColumns(name==='Screening'||name==='Records'?2:1);
 for(let i=0;i<fields.length;i++){
  const k=fields[i];if(/title|reason|rationale|caveat|remaining_checks|abstract|criterion_rationale|basis|assessment|check_required|eligibility_task|outcome_task|quality_task|remaining_action|evidence_excerpt/.test(k))sh.getRange(`${col(i)}1:${col(i)}${vals.length}`).format.columnWidth=64;
  if(/source_hash|sha256/.test(k))sh.getRange(`${col(i)}1:${col(i)}${vals.length}`).format.columnWidth=68;
 }
 sh.getRange(`A2:${end}${vals.length}`).format.autofitRows();
 if(name==='Screening'){
  sh.getRange(`F2:F${vals.length}`).format.fill='#FFF2CC';
  sh.getRange(`F2:F${vals.length}`).dataValidation={rule:{type:'list',values:['retain','exclude','uncertain']}};
 }
}
const n=d.sheets.Records.length+1,q=d.sheets.Screening.length+1,v=d.sheets.Duplicates.length+1;
summary.getRange('B5').formulas=[[`=COUNTA(Records!A2:A${n})`]];
summary.getRange('B6').formulas=[[`=COUNTA(Duplicates!A2:A${v})`]];
summary.getRange('B7').formulas=[['=B5-B6']];
summary.getRange('B8').formulas=[[`=COUNTIF(Screening!E2:E${q},"exclude_recommendation")+COUNTIF(Screening!E2:E${q},"retain_or_uncertain")`]];
summary.getRange('B9').formulas=[['=B8/B7']];summary.getRange('B9').setNumberFormat('0.0%');
for(let i=0;i<2;i++){
 const row=20+i,rid='GB-P00'+(i+1);
 summary.getRange(`B${row}`).formulas=[[`=SUMIF(Quality!A2:A21,"${rid}",Quality!C2:C21)`]];
 summary.getRange(`C${row}`).formulas=[[`=SUMIF(Quality!A2:A21,"${rid}",Quality!D2:D21)`]];
 summary.getRange(`D${row}`).formulas=[[`=B${row}/C${row}`]];
}summary.getRange('D20:D21').setNumberFormat('0.0%');
summary.getRange('A4:C4').format={fill:'#243B53',font:{name:'Arial',size:10,color:'#FFFFFF',bold:true},rowHeight:30};
summary.getRange('A19:D19').format={fill:'#243B53',font:{name:'Arial',size:10,color:'#FFFFFF',bold:true},rowHeight:40,wrapText:true};
summary.getRange('A5:D21').format.font={name:'Arial',size:11};
summary.getRange('A5:C16').format.rowHeight=36;
summary.getRange('A1:A21').format.columnWidth=51;
summary.getRange('B1:B21').format.columnWidth=20;
summary.getRange('C1:C21').format.columnWidth=65;
summary.getRange('D1:D21').format.columnWidth=18;
summary.getRange('A5:C16').format.wrapText=true;
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Summary!A4:D21',include:'values,formulas',tableMaxRows:21,tableMaxCols:4,maxChars:4500})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},summary:'formula errors'})).ndjson);
for(const name of ['Summary',...Object.keys(d.sheets)]){
 const preview=await wb.render({sheetName:name,range:name==='Summary'?'A2:C16':'A1:D5',scale:1.2,format:'png'});
 await fs.writeFile((process.env.OS_CEP_PREVIEW_DIR || '/tmp/oscep-wb')+'/'+name.replaceAll(' ','_')+'.png',new Uint8Array(await preview.arrayBuffer()));
}
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(root+'/task2/tracker/review_workbook.xlsx');
console.log('Workbook exported');

import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile,FileBlob} from '@oai/artifact-tool';
const dir=path.dirname(new URL(import.meta.url).pathname),root=path.resolve(dir,'..');
const d=JSON.parse(await fs.readFile(dir+'/review_data.json','utf8'));
const overlay=JSON.parse(await fs.readFile(root+'/logs/reviewed_data.json','utf8'));
function matrix(rows){let keys=Object.keys(rows[0]);return [keys,...rows.map(r=>keys.map(k=>r[k]??''))];}
function add(w,name,rows,widths){const s=w.worksheets.add(name),cols=rows[0].length,n=rows.length;s.getRangeByIndexes(0,0,n,cols).values=rows;s.showGridLines=false;s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(2);const g=s.getRangeByIndexes(0,0,n,cols);g.format.font={name:'Arial',size:10};g.format.wrapText=true;g.format.verticalAlignment='top';g.format.rowHeight=80;g.format.columnWidth=24;s.getRangeByIndexes(0,0,1,cols).format={fill:'#193E5C',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:42,wrapText:true};for(let c=0;c<cols;c++)s.getRangeByIndexes(0,c,n,1).format.columnWidth=widths?.[c]??28;s.tables.add(s.getRangeByIndexes(0,0,n,cols).address.split('!').pop(),true,'T'+name.replace(/[^a-z]/gi,''));return s;}
const review=Workbook.create();
const ov=add(review,'Overview',[
['Task','Value','Meaning'],['Study source reviews',7,'S008-S014'],['QA item appraisals',70,'10 criteria per study'],['Outcome checks',13,'Values and contexts checked against accessed full text'],['Original QA total',null,'Sum across the seven studies'],['Reviewed QA total',null,'AI reappraisal, not a human independent vote'],['Applicable maximum',140,'7 studies x20'],['Attribution',d.reviewer,'Actual reviewer role'],['Scope','Seven-study source review','Other team assignments and the559-record coverage question remain outside this task'],['Source versions','See Study Review','ParvaGPU numbers are scoped to accessed arXivv1'],['Historical data','Frozen baseline preserved','Corrections are stored in a processed overlay']],[30,34,80]);
const ss=add(review,'Study Review',matrix(d.sources),[13,13,65,12,44,38,65,12,70,75,15,15,15,30]);
const qa=add(review,'QA Review',matrix(d.qa),[13,13,13,13,13,29,78,52,65,42,30,25]);qa.getRange('C2:E71').setNumberFormat('0');
const os=add(review,'Outcome Review',matrix(d.outcomes),[13,13,53,20,20,55,70,72,76,60,65,58,48,30,42]);
add(review,'Corrections',matrix(d.changes),[13,22,28,65,95,65]);
const summaryRows=[['Study ID','Report ID','Original QA','Reviewed QA','Maximum','Change','Checked outcomes'],...d.sources.map(s=>[s['Study ID'],s['Report ID'],s['Original QA'],null,20,null,null])];
const sums=add(review,'QA Summary',summaryRows,[14,14,18,18,18,18,22]);sums.getRange('A2:G8').format.rowHeight=30;
for(let r=2;r<=8;r++){sums.getRange(`D${r}`).formulas=[[`=SUMIF('QA Review'!$A$2:$A$71,B${r},'QA Review'!$D$2:$D$71)`]];sums.getRange(`F${r}`).formulas=[[`=D${r}-C${r}`]];sums.getRange(`G${r}`).formulas=[[`=COUNTIF('Outcome Review'!$B$2:$B$14,B${r})`]];}
ov.getRange('B5').formulas=[['=SUM(\'QA Summary\'!C2:C8)']];ov.getRange('B6').formulas=[['=SUM(\'QA Summary\'!D2:D8)']];
review.recalculate();
console.log((await review.inspect({kind:'table',range:'QA Summary!A1:G8',include:'values,formulas',maxChars:2000,tableMaxRows:8,tableMaxCols:7})).ndjson);
console.log((await review.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20},maxChars:1200})).ndjson);
await fs.mkdir(dir+'/previews',{recursive:true});
for(const name of ['Overview','Study Review','QA Review','Outcome Review','Corrections','QA Summary']){const p=await review.render({sheetName:name,range:name==='QA Summary'?'A1:G8':(name==='QA Review'?'A1:H4':'A1:D4'),scale:1});await fs.writeFile(dir+'/previews/'+name.replaceAll(' ','_')+'.png',new Uint8Array(await p.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(review)).save(dir+'/Raazia_Source_Review.xlsx');
const master=await SpreadsheetFile.importXlsx(await FileBlob.load(root+'/workbook/CEP_Task3_Evidence_Workbook.xlsx'));
for(const name of ['QA','Studies','Evidence','Extraction']){
 const s=master.worksheets.getItem(name),rows=overlay[name];
 for(let i=1;i<rows.length;i++){
  const report=rows[i][name==='QA'?0:1];
  if(d.sources.some(x=>x['Report ID']===report)){
   let a=rows[i].map(v=>v??null);if(name==='QA')for(const c of [2,3])if(a[c]!==''&&!isNaN(Number(a[c])))a[c]=Number(a[c]);
   s.getRangeByIndexes(i,0,1,a.length).values=[a];
  }
 }
}
const rec=master.worksheets.getItem('QA Reconciliation');
for(let i=0;i<20;i++){const report=overlay.Studies[i+1][1];if(d.sources.some(x=>x['Report ID']===report))rec.getCell(i+1,2).values=[[overlay.Studies[i+1][6]]];}
add(master,'Raazia QA Review',matrix(d.qa),[13,13,13,13,13,29,78,52,65,42,30,25]);
add(master,'Raazia Outcomes',matrix(d.outcomes),[13,13,53,20,20,55,70,72,76,60,65,58,48,30,42]);
add(master,'Raazia Corrections',matrix(d.changes),[13,22,28,65,95,65]);
master.recalculate();
console.log((await master.inspect({kind:'table',range:'QA Reconciliation!A8:J15',include:'values,formulas',maxChars:1800,tableMaxRows:8,tableMaxCols:10})).ndjson);
console.log((await master.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20},maxChars:1000})).ndjson);
await(await SpreadsheetFile.exportXlsx(master)).save(root+'/workbook/CEP_Task3_Evidence_Workbook.xlsx');
console.log('Saved personal six-tab review and integrated30-tab master workbook');

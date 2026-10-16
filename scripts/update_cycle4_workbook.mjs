import fs from 'node:fs/promises';
import {FileBlob, SpreadsheetFile} from '@oai/artifact-tool';
const file=process.env.OS_CEP_WORKBOOK, root=process.env.OS_CEP_ROOT;
const d=JSON.parse(await fs.readFile(root+'/task2/qa/workbook_update.json','utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));
const prefix=process.env.OS_CEP_PREVIEW_PREFIX;
if(process.env.OS_CEP_INSPECT_ONLY==='1'){
 const img=await wb.render({sheetName:'Summary',range:'A2:D16',format:'png',scale:1.2});
 await fs.writeFile(prefix+'-before.png',new Uint8Array(await img.arrayBuffer()));
 console.log((await wb.inspect({kind:'table',range:'Summary!A19:D28',include:'values,formulas',maxChars:1800,tableMaxRows:10,tableMaxCols:4})).ndjson);
 process.exit(0);
}
// Zero-based column index to Excel label.
function xl(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
function add(name,headers,rows){
 let sh;
 try{sh=wb.worksheets.getItem(name);}catch{}
 if(!sh)sh=wb.worksheets.add(name);
 sh.showGridLines=false;
 const clean=v=>typeof v==='string'&&v.startsWith('=')?"'"+v:v;
 const vals=[headers,...rows.map(r=>headers.map(k=>clean(r[k]??'')))];
 const end=xl(headers.length-1);sh.getRange(`A1:${end}${vals.length}`).values=vals;
 sh.getRange(`A1:${end}${vals.length}`).format={font:{name:'Arial',size:10},columnWidth:24,wrapText:true};
 sh.getRange(`A1:${end}1`).format={fill:'#243B53',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true};
 sh.getRange(`A2:${end}${vals.length}`).format.rowHeight=44;
 sh.freezePanes.freezeRows(1);sh.freezePanes.freezeColumns(1);
 for(let i=0;i<headers.length;i++){
  if(/title|reason|rationale|return|task|basis|status|action/.test(headers[i]))sh.getRange(`${xl(i)}1:${xl(i)}${vals.length}`).format.columnWidth=58;
  if(/_at_utc$/.test(headers[i]))sh.getRange(`${xl(i)}2:${xl(i)}${vals.length}`).setNumberFormat('yyyy-mm-dd hh:mm:ss');
 }
 sh.getRange(`A2:${end}${vals.length}`).format.autofitRows();
 return sh;
}
const h=['report_id','title',...Array.from({length:10},(_,i)=>'Q'+(i+1)),'Raw score','Applicable maximum','Normalized','Sensitivity below 60%','QA status'];
const sh=add('QA matrix',h,d.matrix);
const n=d.matrix.length+1;
for(let i=0;i<d.matrix.length;i++){
 const row=i+2,rid=d.matrix[i].report_id;
 for(let j=0;j<10;j++){
  const source=d.quality.findIndex(x=>x.report_id===rid&&x.criterion==='Q'+(j+1))+2;
  sh.getRange(`${xl(j+2)}${row}`).formulas=[[`=Quality!C${source}`]];
 }
 sh.getRange(`M${row}`).formulas=[[`=SUM(C${row}:L${row})`]];
 sh.getRange(`N${row}`).formulas=[[`=SUMIF(Quality!A2:A${d.quality.length+1},A${row},Quality!D2:D${d.quality.length+1})`]];
 sh.getRange(`O${row}`).formulas=[[`=M${row}/N${row}`]];
 sh.getRange(`P${row}`).formulas=[[`=IF(O${row}<0.6,"yes","no")`]];
 sh.getRange(`Q${row}`).values=[['AI first review; independent check pending']];
}
sh.getRange(`C1:L${n}`).format.columnWidth=8;
sh.getRange(`M1:P${n}`).format.columnWidth=19;
sh.getRange(`O2:O${n}`).setNumberFormat('0.0%');
sh.getRange(`A2:Q${n}`).format.rowHeight=68;
const ch=['criterion','label','score_2_requires','score_1','score_0','protocol_anchor'];
add('QA followup',Object.keys(d.followup[0]),d.followup);
const rules=add('QA checklist',ch,d.checklist);rules.getRange('C1:C11').format.columnWidth=85;rules.getRange('C2:C11').format.autofitRows();
add('AI opinions',Object.keys(d.opinions[0]),d.opinions);
const summary=wb.worksheets.getItem('Summary');
summary.getRange(`A${19+d.matrix.length+10}:C${19+d.matrix.length+12}`).values=[['Cycle 4 QA view',`${d.matrix.length} reports / ${d.quality.length} items`,'Initial scores preserved; independent source checks pending'],['Incoming AI opinions',1831,'Separate pass; 50 disagreements within 240 overlaps; no final decisions'],['QA follow-up','See current QA followup','See QA followup; current paper-by-paper appendix in task2/qa']];
summary.getRange(`A${19+d.matrix.length+10}:C${19+d.matrix.length+12}`).format={wrapText:true,rowHeight:48,font:{name:'Arial',size:11}};
wb.recalculate();
const expected=d.matrix.map(x=>[Number(x.raw_sum),Number(x.applicable_max)]);
const got=sh.getRange(`M2:N${n}`).values;
if(JSON.stringify(got)!==JSON.stringify(expected))throw Error('QA formula totals mismatch '+JSON.stringify(got));
// Test a non-N/A input in the same calculation engine, then restore it.
const q=wb.worksheets.getItem('Quality');const original=q.getRange('C2').values;
q.getRange('C2').values=[[1]];wb.recalculate();
if(sh.getRange('M2').values[0][0]!==expected[0][0]-1)throw Error('QA recalculation did not propagate');
q.getRange('C2').values=original;wb.recalculate();
if(JSON.stringify(sh.getRange(`M2:N${n}`).values)!==JSON.stringify(expected))throw Error('QA restoration failed');
for(const [name,range] of [['Summary','A19:D39'],['QA matrix','A1:H10'],['QA matrix','I1:Q10'],['QA followup','A1:F4'],['QA checklist','A1:C5'],['AI opinions','A1:D4']]){
 const img=await wb.render({sheetName:name,range,format:'png',scale:1.2});
 await fs.writeFile(prefix+'-'+name.replaceAll(' ','_')+'-'+range.replaceAll(':','_')+'.png',new Uint8Array(await img.arrayBuffer()));
}
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:1500,summary:'QA workbook error scan'})).ndjson);
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(file);
console.log(JSON.stringify({saved:file,qaRows:d.quality.length,matrixReports:d.matrix.length,totals:got,recalculationTest:'passed; input restored'}));

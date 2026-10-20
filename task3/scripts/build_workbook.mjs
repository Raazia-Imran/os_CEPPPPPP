import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.env.TASK3_ROOT || path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const d=JSON.parse(await fs.readFile(root+'/logs/baseline_data.json','utf8'));
const a=JSON.parse(await fs.readFile(root+'/logs/analysis.json','utf8'));
const retr=JSON.parse(await fs.readFile(root+'/papers/retrieval.json','utf8'));
const w=await SpreadsheetFile.importXlsx(await FileBlob.load(root+'/baseline/CEP_EVIDENCE_WORKBOOK.xlsx'));
function add(name,rows){const s=w.worksheets.add(name), cols=Math.max(...rows.map(r=>r.length));const rr=rows.map(r=>Array.from({length:cols},(_,i)=>r[i]??null));s.getRangeByIndexes(0,0,rr.length,cols).values=rr;s.showGridLines=false;s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(1);const g=s.getRangeByIndexes(0,0,rr.length,cols);g.format.font={name:'Arial',size:10};g.format.columnWidth=34;g.format.wrapText=true;g.format.verticalAlignment='top';g.format.rowHeight=100;s.getRangeByIndexes(0,0,1,cols).format={fill:'#193E5C',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true};s.getRangeByIndexes(1,0,rr.length-1,1).format.columnWidth=20;s.tables.add(s.getRangeByIndexes(0,0,rr.length,cols).address.split('!').pop(),true,'T'+name.replace(/[^a-z]/gi,''));return s;}
for(const [name,rows] of Object.entries(a))add(name,rows);
const keys=['report_id','study_id','title','status','filename','source_url','alternate_url','retrieved_utc','retrieved_pkt','version_note','sha256','bytes','identity_check_utc'];
add('PDF Retrieval',[keys,...retr.map(r=>keys.map(k=>r[k]??''))]);
const activity=JSON.parse(await fs.readFile(root+'/logs/activity.json','utf8'));
const act=add('Activity Log',activity);
act.getRange('B2:C'+activity.length).setNumberFormat('yyyy-mm-dd hh:mm:ss');
act.getRange('A2:H'+activity.length).format.rowHeight=80;
w.worksheets.getItem('PDF Retrieval').getRange('H2:I22').setNumberFormat('yyyy-mm-dd hh:mm:ss');
w.worksheets.getItem('PDF Retrieval').getRange('M2:M22').setNumberFormat('yyyy-mm-dd hh:mm:ss');
const q=add('QA Reconciliation',[['Study ID','Report ID','Recorded score','Item total','Recorded maximum','Item maximum','Normalized score','Below 60%','Score difference','Maximum difference'],...d.Studies.slice(1).map(r=>[r[0],r[1],r[6],null,r[7],null,null,null,null,null])]);
// Convert source score cells to numbers without changing their mathematical values. N/A stays text.
const qa=w.worksheets.getItem('QA');
for(let i=1;i<d.QA.length;i++)for(const c of [2,3]){let v=d.QA[i][c];if(v!==null&&v!==''&&!Number.isNaN(Number(v)))qa.getCell(i,c).values=[[Number(v)]];}
for(let r=2;r<=21;r++){
 q.getRange(`D${r}`).formulas=[[`=SUMIF(QA!$A$2:$A$201,B${r},QA!$C$2:$C$201)`]];
 q.getRange(`F${r}`).formulas=[[`=SUMIF(QA!$A$2:$A$201,B${r},QA!$D$2:$D$201)`]];
 q.getRange(`G${r}`).formulas=[[`=D${r}/F${r}`]];
 q.getRange(`H${r}`).formulas=[[`=IF(G${r}<0.6,"Yes","No")`]];
 q.getRange(`I${r}`).formulas=[[`=D${r}-C${r}`]];q.getRange(`J${r}`).formulas=[[`=F${r}-E${r}`]];
}
q.getRange('G2:G21').setNumberFormat('0.0%');q.getRange('A2:J21').format.rowHeight=28;q.getRange('A1:J21').format.columnWidth=18;
const c=add('Count Reconciliation',[['Metric','Computed count','Baseline count','Difference'],['Canonical records',null,4075,null],['Screening exclusions',null,3493,null],['Not advanced',null,559,null],['Included reports',null,21,null],['Full-text exclusions',null,2,null],['Unique studies',null,20,null],['QA items',null,200,null],['Outcome rows',null,52,null],['Duplicate links',null,114,null],['Source-assessed reports',null,23,null],['Partition total',null,4075,null]]);
const ff=['=COUNTA(\'Screening Log\'!A2:A4076)', '=COUNTIF(\'Screening Log\'!E2:E4076,"excluded_at_screening")','=COUNTIF(\'Screening Log\'!E2:E4076,"retained_not_advanced_under_stopping_rule")','=COUNTIF(\'Screening Log\'!E2:E4076,"included_in_synthesis")','=COUNTIF(\'Screening Log\'!E2:E4076,"excluded_after_source_assessment")','=COUNTA(Studies!A2:A21)','=COUNTA(QA!A2:A201)','=COUNTA(Evidence!A2:A53)','=COUNTA(\'Duplicate Removal\'!A2:A115)','=B5+B6','=B3+B4+B5+B6'];
ff.forEach((v,i)=>{c.getCell(i+1,1).formulas=[[v]];c.getCell(i+1,3).formulas=[[`=B${i+2}-C${i+2}`]]});c.getRange('A2:D12').format.rowHeight=30;
const read=add('Task 3 Guide',[['Topic','How to use'],['Baseline','Original 14 tabs retain supplied evidence. QA numeric strings become numeric values for reconciliation; no score is changed.'],['Reading','PDF Retrieval distinguishes available copy, source URL and manuscript version. Check the source before signing off a claim.'],['Timestamps','Activity Log contains new actual actions. Historical source times remain batch/entry/build times where labeled.'],['Human checks','Enter real reviewer name, actual UTC time and evidence in Human Checks. Pending does not mean completed.'],['Synthesis','Taxonomy, Comparability, Recommendations, Research Gaps and Validity contain new interpretations linked to report/evidence IDs.'],['Sensitivity','Every current study scores at least 60%. Removing below-60% studies removes none: this is not evidence of robustness to selection bias.'],['Scope','559 retained records remain unassessed. The bounded scope needs acceptance; do not rename these records technical exclusions.']]);read.getRange('B1:B8').format.columnWidth=95;
w.recalculate();
console.log((await w.inspect({kind:'table',range:'QA Reconciliation!A1:J5',include:'values,formulas',tableMaxRows:5,tableMaxCols:10,maxChars:2000})).ndjson);
console.log((await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:1000})).ndjson);
await fs.mkdir(root+'/workbook/previews',{recursive:true});
for(const name of [...Object.keys(a),'PDF Retrieval','Activity Log','QA Reconciliation','Count Reconciliation','Task 3 Guide']){const b=await w.render({sheetName:name,range:name==='QA Reconciliation'?'A1:J6':'A1:D5',scale:1});await fs.writeFile(root+'/workbook/previews/'+name.replaceAll(' ','_')+'.png',new Uint8Array(await b.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(w)).save(root+'/workbook/CEP_Task3_Evidence_Workbook.xlsx');
console.log('Saved',root+'/workbook/CEP_Task3_Evidence_Workbook.xlsx');

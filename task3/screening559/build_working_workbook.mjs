import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const root=await fs.realpath(process.cwd());
const dir=await fs.realpath(path.join(root,'task3','screening559'));
if(path.relative(root,dir)!==path.join('task3','screening559')){throw Error('Unexpected repository/source directory');}
const out=await fs.realpath(path.join(dir,'integrated_workbook'));
if(path.relative(dir,out)!=='integrated_workbook'){throw Error('Output directory escapes the continuation folder');}
await fs.access(path.join(root,'AGENTS.md'));
const p=JSON.parse(await fs.readFile(out+'/integrated_workbook_data.json','utf8'));
const w=await SpreadsheetFile.importXlsx(await FileBlob.load(root+'/task3/workbook/CEP_Task3_Evidence_Workbook.xlsx'));
const baselineNames=w.worksheets.items.map(s=>s.name);const get=n=>w.worksheets.getItem(n);
const before=await w.render({sheetName:'Studies',range:'A1:I4',scale:1,format:'png'});
await fs.writeFile(out+'/baseline_preview.png',new Uint8Array(await before.arrayBuffer()));
const changes=[];
function put(name,rows){
 let s=w.worksheets.items.find(x=>x.name===name),fresh=!s;if(fresh)s=w.worksheets.add(name);
 const oldRows=fresh?0:s.getUsedRange().values.length,n=rows.length,m=Math.max(...rows.map(x=>x.length));
 // Extend native tables through their documented row API before replacing values.
 if(!fresh&&n>oldRows&&s.tables.items.length===1)s.tables.items[0].rows.add(null,Array.from({length:n-oldRows},()=>Array(m).fill(null)));
 s.getRangeByIndexes(0,0,n,m).values=rows.map(x=>Array.from({length:m},(_,i)=>x[i]??null));
 if(n>oldRows){const g=s.getRangeByIndexes(Math.max(1,oldRows),0,n-Math.max(1,oldRows),m);g.format.font={name:'Arial',size:10};g.format.wrapText=true;g.format.verticalAlignment='top';g.format.rowHeight=100;}
 if(fresh){s.showGridLines=false;s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(2);s.getRangeByIndexes(0,0,n,m).format.columnWidth=32;s.getRangeByIndexes(0,0,1,m).format={fill:'#193E5C',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:42};s.tables.add(s.getRangeByIndexes(0,0,n,m).address.split('!').pop(),true,'Continuation'+name.replace(/[^a-z]/gi,''));}
 changes.push(name);return s;
}
const matrix=rr=>[Object.keys(rr[0]),...rr.map(x=>Object.values(x))];
for(const [n,rows] of Object.entries(p.data))put(n,rows);
for(const [n,rows] of Object.entries(p.analysis))put(n,rows);
put('Methodology Corrections',matrix(p.methodology));
put('Reference Additions',matrix(p.references));
const sources=get('Source Checks').getUsedRange().values;
for(const e of p.final_decisions.filter(x=>x['Final eligibility decision']==='Include'))sources.push([e['Study ID'],e['Report ID'],'Final primary copy; single source-based review',e['Source URL'],e['Source SHA256'],Number(p.source_checks.find(s=>s['Record ID']===e['Record ID'])['PDF pages']),'Full text inspected',e['Decided UTC'],'']);
put('Source Checks',sources);
const retrieval=get('PDF Retrieval').getUsedRange().values;
for(const e of p.final_decisions.filter(x=>x['Final eligibility decision']==='Include')){
 const ref=p.references.find(x=>x['Record ID']===e['Record ID']);
 retrieval.push([e['Report ID'],e['Study ID'],ref.Title,'Full text inspected','Private local reading copy',e['Source URL'],'',e['Decided UTC'],new Date(new Date(e['Decided UTC']).getTime()+5*3600000).toISOString().replace('Z','+05:00'),'Final primary source; no licensed PDF redistributed',e['Source SHA256'],'Not recorded in workbook',e['Decided UTC']]);
}
put('PDF Retrieval',retrieval);
const activity=get('Activity Log').getUsedRange().values,clock=new Date();
activity.push(['CONT-INTEGRATE',clock.toISOString(),new Date(clock.getTime()+5*3600000).toISOString().replace('Z','+05:00'),'Assistant under team direction','Integrate confirmed source-based additions',`${p.counts.studies}studies/${p.counts.included_reports}reports;${p.counts.open}advanced records open`,'screening559/final decision,QA,outcome and reference logs','Actual working integration time; not an independent human vote']);
put('Activity Log',activity);
const guide=get('Task 3 Guide');guide.getRange('B2').values=[['New working master; frozen20-study/21-report release is preserved separately.']];guide.getRange('B3').values=[['Source Checks and Reference Additions include the new source versions and bibliography.']];guide.getRange('B5').values=[['Single automated source review under user-reported instructor permission; independent human votes remain blank.']];guide.getRange('B8').values=[[`${p.counts.open}advanced records remain open after559screening decisions. The working included corpus is${p.counts.studies}studies/${p.counts.included_reports}reports. Whole-review PRISMA is not final.`]];
changes.push('Task 3 Guide');
const nq=p.counts.qa+1,ns=p.counts.studies+1;
for(let i=1;i<p.data.Studies.length;i++){
 const rr=i+1,s=get('Studies');s.getRange(`G${rr}:I${rr}`).formulas=[[`=SUMIF(QA!$A$2:$A$${nq},B${rr},QA!$C$2:$C$${nq})`,`=SUMIF(QA!$A$2:$A$${nq},B${rr},QA!$D$2:$D$${nq})`,`=G${rr}/H${rr}`]];
}
get('Studies').getRange(`I2:I${ns}`).setNumberFormat('0.0%');
const rec=[['Study ID','Report ID','Recorded score','Item total','Recorded maximum','Item maximum','Normalized score','Below60%','Score difference','Maximum difference'],...p.data.Studies.slice(1).map(x=>[x[0],x[1],x[6],null,x[7],null,null,null,null,null])];
put('QA Reconciliation',rec);
for(let i=2;i<=ns;i++){
 get('QA Reconciliation').getRange(`D${i}`).formulas=[[`=SUMIF(QA!$A$2:$A$${nq},B${i},QA!$C$2:$C$${nq})`]];
 get('QA Reconciliation').getRange(`F${i}:J${i}`).formulas=[[`=SUMIF(QA!$A$2:$A$${nq},B${i},QA!$D$2:$D$${nq})`,`=D${i}/F${i}`,`=IF(G${i}<0.6,"Yes","No")`,`=D${i}-C${i}`,`=F${i}-E${i}`]];
}
get('QA Reconciliation').getRange(`G2:G${ns}`).setNumberFormat('0.0%');
const c=p.counts,control=[['Metric','Computed count','Expected working count','Difference'],['Canonical records',null,4075,null],['Screening exclusions',null,c.screening_exclusions,null],['Eligibility/identity open',null,c.open,null],['Included reports',null,c.included_reports,null],['Full-text exclusions',null,c.full_text_exclusions,null],['Unique studies',null,c.studies,null],['QA items',null,c.qa,null],['Outcome rows',null,c.outcomes,null],['Duplicate links',null,114,null],['Source-assessed reports',null,c.assessed,null],['Partition total',null,4075,null]];
put('Count Reconciliation',control);
const ff=["=COUNTA('Screening Log'!A2:A4076)",'=COUNTIF(\'Screening Log\'!E2:E4076,"excluded_at_screening")','=COUNTIF(\'Screening Log\'!E2:E4076,"full_text_eligibility_pending")','=COUNTIF(\'Screening Log\'!E2:E4076,"included_in_synthesis")','=COUNTIF(\'Screening Log\'!E2:E4076,"excluded_after_source_assessment")',`=COUNTA(Studies!A2:A${ns})`,`=COUNTA(QA!A2:A${nq})`,`=COUNTA(Evidence!A2:A${c.outcomes+1})`,"=COUNTA('Duplicate Removal'!A2:A115)",'=B5+B6','=B3+B4+B5+B6'];
for(let i=2;i<=12;i++){get('Count Reconciliation').getRange(`B${i}`).formulas=[[ff[i-2]]];get('Count Reconciliation').getRange(`D${i}`).formulas=[[`=B${i}-C${i}`]];}
w.recalculate();
const diff=get('Count Reconciliation').getRange('D2:D12').values.flat(),qdiff=get('QA Reconciliation').getRange(`I2:J${ns}`).values.flat();
if(diff.some(x=>x!==0)||qdiff.some(x=>x!==0))throw Error('Reconciliation failed '+JSON.stringify({diff,qdiff}));
// A meaningful live dependency check on a newly integrated numeric appraisal.
const row=202,old=get('QA').getCell(row-1,2).values[0][0],beforeScore=get('Studies').getRange('G22').values[0][0];
if(typeof old!=='number'){throw Error('Numeric appraisal test unavailable');}
get('QA').getCell(row-1,2).values=[[old-1]];
if(get('Studies').getRange('G22').values[0][0]!==beforeScore-1){throw Error('New study formula did not respond');}
get('QA').getCell(row-1,2).values=[[old]];
w.recalculate();
const errors=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:30},maxChars:3000});
console.log(errors.ndjson);
await fs.mkdir(out+'/previews',{recursive:true});
for(const n of [...new Set(changes)]){
 const s=get(n),nrows=s.getUsedRange().values.length,range=n==='Studies'?`A22:I${ns}`:n==='QA Reconciliation'?`A22:J${ns}`:n==='Count Reconciliation'?'A1:D12':n==='Summary'?'A1:C9':n==='Screening Log'?'A1:G3':`A${Math.max(1,nrows-2)}:F${nrows}`;
 const b=await w.render({sheetName:n,range,scale:1,format:'png'});await fs.writeFile(out+'/previews/'+n.replaceAll(' ','_')+'.png',new Uint8Array(await b.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(w)).save(out+'/CEP_Task3_Working_Integrated_2026-10-23.xlsx');
await fs.writeFile(out+'/workbook_validation.json',JSON.stringify({counts:c,preserved_original_tabs:baselineNames.every(n=>w.worksheets.items.some(s=>s.name===n)),tabs:w.worksheets.items.map(s=>s.name),count_differences:diff,QA_differences:qdiff,live_QA_dependency_check:true,error_scan:errors.ndjson,frozen_input_not_overwritten:true},null,2));
console.log('Working workbook exported',JSON.stringify(c));

import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const dir=process.argv[2];
const data=JSON.parse(await fs.readFile(dir+'/review_data.json','utf8'));
const receipt=JSON.parse(await fs.readFile(dir+'/novelty_search_receipt.json','utf8'));
const wb=Workbook.create();
function matrix(rows){const k=Object.keys(rows[0]);return [k,...rows.map(r=>k.map(c=>r[c]??null))];}
function sheet(name,rows,widths){
 const s=wb.worksheets.add(name),n=rows.length,m=rows[0].length;
 s.showGridLines=false;s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(2);
 const r=s.getRangeByIndexes(0,0,n,m);r.values=rows;r.format.font={name:'Arial',size:10};r.format.verticalAlignment='top';r.format.wrapText=true;r.format.rowHeight=90;
 s.getRangeByIndexes(0,0,1,m).format={fill:'#183A56',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:42,wrapText:true,horizontalAlignment:'center'};
 for(let c=0;c<m;c++)s.getRangeByIndexes(0,c,n,1).format.columnWidth=widths[c]??30;
 s.tables.add(s.getRangeByIndexes(0,0,n,m).address.split('!').pop(),true,'Rameen'+name.replace(/[^a-z]/gi,''));
 return s;
}
const overview=wb.worksheets.add('Overview');overview.showGridLines=false;
overview.getRange('A2').values=[['Rameen source review']];overview.getRange('A2:H2').format.font={name:'Arial',size:15,bold:true};
overview.getRange('A3').values=[['S015-S020. Proposed appraisals and corrections await teammate adjudication.']];
overview.getRange('A5:H5').values=[['Study','Full-text status','QA assessed','QA pending','Original QA','Proposed QA','Proposed max','Human signoff']];
overview.getRange('A6:H11').values=data.sources.map(s=>[s['Study ID']+' / '+s['Report ID'],s['Access status'],null,null,s['Original QA'],null,null,'Pending']);
overview.getRange('J5:K5').values=[['Item','Count']];
overview.getRange('J6:K11').values=[['Sources inspected',null],['Sources pending',null],['Eligibility checked',null],['Eligibility pending',null],['Outcomes checked',null],['Outcomes pending',null]];
overview.getRange('A14:B19').values=[['Review boundary','Status'],['Independent human signoff','Pending'],['Instructor scope acceptance','Pending'],['Retained records unassessed',559],['Master workbook','Source corrections integrated; human signoff pending'],['Attribution',data.reviewer]];
overview.getRange('A2:K19').format.font={name:'Arial',size:10};overview.getRange('A2:K2').format.font={name:'Arial',size:15,bold:true};
overview.getRange('A5:K19').format.rowHeight=30;overview.getRange('A5:K19').format.verticalAlignment='center';
overview.getRange('A5:H5').format={fill:'#183A56',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:38,wrapText:true};
overview.getRange('J5:K5').format={fill:'#183A56',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:38};
overview.getRange('A:A').format.columnWidth=22;overview.getRange('B:B').format.columnWidth=34;overview.getRange('C:H').format.columnWidth=15;overview.getRange('I:I').format.columnWidth=3;overview.getRange('J:J').format.columnWidth=24;overview.getRange('K:K').format.columnWidth=14;
overview.getRange('B18:B19').format.wrapText=true;overview.getRange('A18:H19').format.rowHeight=48;
const src=sheet('Sources',matrix(data.sources),[14,13,70,12,40,68,82,29,12,70,17,18,18,18,65,30,30,25]);
const qa=sheet('QA',matrix(data.qa),[14,13,13,15,16,16,18,24,90,65,72,65,30,25]);
// Preserve numeric types without coercing unassessed blanks or genuine N/A.
for(let i=0;i<data.qa.length;i++){const old=data.qa[i]['Original score'];if(old!=='NA')qa.getCell(i+1,3).values=[[Number(old)]];}
qa.getRange('D2:G61').setNumberFormat('0');qa.getRange('F2:G61').format.font={name:'Arial',size:10,color:'#134A7C'};
qa.getRange('N2:N61').format.fill='#FFF2CC';qa.getRange('N2:N61').dataValidation={rule:{type:'list',values:['0','1','2','NA']}};
sheet('Eligibility',matrix(data.eligibility),[14,13,13,22,36,100,72,72,65,30,30]);
sheet('Outcomes',matrix(data.outcomes),[14,13,55,20,20,60,90,76,85,70,70,55,60,26,90,65,30,24]);
sheet('Corrections',matrix(data.changes),[14,24,26,70,100,90]);
sheet('Survey overlap',matrix(data.novelty),[14,80,75,12,35,90,95,75,95,110,75]);
const searches=receipt.queries.map((q,i)=>({'Query ID':'NS'+String(i+1).padStart(2,'0'),'Source':receipt.source,'Query':q.q,'Recency days':q.recency??null,'Started UTC':receipt.started_utc,'Completed UTC':receipt.completed_utc,'Purpose':receipt.purpose,'Coverage':'Supplementary search; no displayed total captured; no PRISMA identification change'}));
sheet('Search log',matrix(searches),[14,36,100,16,30,30,105,95]);
sheet('Review queue',matrix(data.rotation),[14,25,28,100,105,28,30,30,70]);
for(let i=0;i<6;i++){
 const r=i+6,pid=data.sources[i]['Report ID'];
 overview.getRange(`C${r}`).formulas=[[`=COUNTIFS(QA!$B$2:$B$61,"${pid}",QA!$H$2:$H$61,"Assessed")`]];
 overview.getRange(`D${r}`).formulas=[[`=COUNTIFS(QA!$B$2:$B$61,"${pid}",QA!$H$2:$H$61,"Pending full text")`]];
 overview.getRange(`F${r}`).formulas=[[`=IF(C${r}=0,"",SUMIF(QA!$B$2:$B$61,"${pid}",QA!$F$2:$F$61))`]];
 overview.getRange(`G${r}`).formulas=[[`=IF(C${r}=0,"",SUMIF(QA!$B$2:$B$61,"${pid}",QA!$G$2:$G$61))`]];
}
const f=[`=COUNTIF(Sources!$H$2:$H$7,"Full text inspected")`,`=COUNTIF(Sources!$H$2:$H$7,"Full text unavailable")`,`=COUNTIF(Eligibility!$E$2:$E$37,"Supported in accessed version")`,`=COUNTIF(Eligibility!$E$2:$E$37,"Pending full text")`,`=COUNTIF(Outcomes!$N$2:$N$10,"Value and context checked")`,`=COUNTIF(Outcomes!$N$2:$N$10,"Pending full text")`];
overview.getRange('K6:K11').formulas=f.map(x=>[x]);
overview.getRange('B6:B11').conditionalFormats.add('containsText',{text:'unavailable',format:{fill:'#FCE4D6',font:{color:'#9C2B15'}}});
qa.getRange('H2:H61').conditionalFormats.add('containsText',{text:'Pending',format:{fill:'#FCE4D6',font:{color:'#9C2B15'}}});
// Meaningful live-formula check in a disposable edit, then restore.
const old=qa.getRange('F2').values[0][0];qa.getRange('F2').values=[[old-1]];
if(overview.getRange('F6').values[0][0]!==17)throw new Error('QA summary failed to react');
qa.getRange('F2').values=[[old]];wb.recalculate();
const overviewCheck=overview.getRange('C6:G11').values;
if(overviewCheck[0][3]!==18||overviewCheck[4][3]!==18||overviewCheck[5][3]!==19)throw new Error('QA totals mismatch');
if(overviewCheck[1][3]!==17)throw new Error('InferFair QA mismatch');
const counts=overview.getRange('K6:K11').values.flat();
if(JSON.stringify(counts)!==JSON.stringify([6,0,36,0,9,0]))throw new Error('Summary counts mismatch: '+JSON.stringify(counts));
console.log((await wb.inspect({kind:'table',range:'Overview!A5:H11',include:'values,formulas',maxChars:2500,tableMaxRows:7,tableMaxCols:8})).ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:30},maxChars:2000});console.log(errors.ndjson);
await fs.mkdir(dir+'/previews',{recursive:true});
for(const s of wb.worksheets.items){const range=s.name==='Overview'?'A2:K19':s.name==='QA'?'A1:J4':s.name==='Sources'?'A1:H3':s.name==='Survey overlap'?'A1:F3':s.name==='Review queue'?'A1:E3':s.name==='Outcomes'?'A1:H3':'A1:F3';const p=await wb.render({sheetName:s.name,range,scale:1,format:'png'});await fs.writeFile(dir+'/previews/'+s.name.replaceAll(' ','_')+'.png',new Uint8Array(await p.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(wb)).save(dir+'/Rameen_Source_Review.xlsx');
await fs.writeFile(dir+'/workbook_validation.json',JSON.stringify({tabs:wb.worksheets.items.map(s=>s.name),counts,qa_totals:[18,17,16,15,18,19],live_qa_formula_test:true,unavailable_scores_blank:true,error_scan:errors.ndjson},null,2));
console.log('Saved Rameen_Source_Review.xlsx');

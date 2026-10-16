import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.env.OS_CEP_ROOT;
const d=JSON.parse(await fs.readFile(root+'/task2/submission/submission_input.json','utf8'));
const wb=Workbook.create();const overview=wb.worksheets.add('Overview');
const xl=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const numeric=new Set(['score','maximum','outcome_rows','original_characters','normalized_characters','calculated_value']);
for(const [name,rows] of Object.entries(d.tabs)){
 const sh=wb.worksheets.add(name);sh.showGridLines=false;const fields=Object.keys(rows[0]);const end=xl(fields.length-1);
 const values=[fields,...rows.map(r=>fields.map(k=>{
  const v=r[k]??'';if(numeric.has(k)&&v!==''&&v!=='NA'&&!isNaN(Number(v)))return Number(v);
  return typeof v==='string'&&v.startsWith('=')?"'"+v:v;
 }))];
 sh.getRange(`A1:${end}${values.length}`).values=values;
 sh.getRange(`A1:${end}${values.length}`).format={font:{name:'Arial',size:10},wrapText:true,columnWidth:23,rowHeight:40};
 sh.getRange(`A1:${end}1`).format={fill:'#243B53',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:40};
 for(let i=0;i<fields.length;i++){
  if(/title|query|reason|basis|mechanism|workload|limitations|tradeoff|status|action|scope|fields|filters|provenance|gaps|rationale|anchor|source/.test(fields[i]))sh.getRange(`${xl(i)}1:${xl(i)}${values.length}`).format.columnWidth=58;
 }
 sh.getRange(`A2:${end}${values.length}`).format.autofitRows();sh.freezePanes.freezeRows(1);sh.freezePanes.freezeColumns(1);
}
const qa=wb.worksheets.getItem('QA items'),summary=wb.worksheets.getItem('Study summary');
const nr=d.tabs['QA items'].length+1;
summary.getRange('H1').values=[['QA raw score']];summary.getRange('M1:N1').values=[['Applicable maximum','QA normalized']];
summary.getRange('M1:N16').format={font:{name:'Arial',size:10},columnWidth:22,wrapText:true};summary.getRange('M1:N1').format={fill:'#243B53',font:{color:'#FFFFFF',bold:true},rowHeight:40};
for(let i=2;i<=d.tabs['Study summary'].length+1;i++){
 summary.getRange(`H${i}`).formulas=[[`=SUMIF('QA items'!A2:A${nr},A${i},'QA items'!C2:C${nr})`]];
 summary.getRange(`M${i}`).formulas=[[`=SUMIF('QA items'!A2:A${nr},A${i},'QA items'!D2:D${nr})`]];
 summary.getRange(`N${i}`).formulas=[[`=H${i}/M${i}`]];
}summary.getRange('N2:N16').setNumberFormat('0.0%');
overview.showGridLines=false;overview.getRange('A1:D1').values=[['Group B review: submission overview','','','']];overview.getRange('A1').format.font={name:'Arial',size:17,bold:true};
const metrics=[['Imported occurrences',d.counts.occurrences,'Four databases plus supplementary sources'],['Applied duplicate links',d.counts.duplicate_links,'111 original plus3 publisher-verified identities'],['Canonical screening records',d.counts.canonical_records,'All have initial automated triage; not all abstracts verified'],['Preliminary exclude proposals',d.counts.preliminary_exclude,'Not final full-text exclusions'],['Retain / uncertain',d.counts.retain_or_uncertain,'Initial triage; source decisions logged separately'],['Assessed report forms',d.counts.report_forms,'Includes version-uncertain/companion cases; not final studies'],['QA items',d.counts.qa_items,'Q1-Q10,0-2,justified N/A; first AI assessment'],['Reported outcomes',d.counts.outcomes,'Outcome rows are not studies'],['Final included studies','Pending','Final selection incomplete'],['Reviewer method','AI-only deviation','No independent human review claimed']];
overview.getRange('A3:C3').values=[['Metric','Count / status','Interpretation']];overview.getRange('A4:C13').values=metrics;
overview.getRange('B4').formulas=[[`=COUNTA(Duplicates!A2:A${d.tabs.Duplicates.length+1})`]];
overview.getRange('B5').formulas=[[`=COUNTIF(Duplicates!E2:E${d.tabs.Duplicates.length+1},"linked_repeat")`]];
overview.getRange('B6').formulas=[[`=COUNTA('Screening log'!A2:A${d.tabs['Screening log'].length+1})`]];
overview.getRange('B7').formulas=[[`=COUNTIF('Screening log'!G2:G${d.tabs['Screening log'].length+1},"exclude_recommendation")`]];
overview.getRange('B8').formulas=[[`=COUNTIF('Screening log'!G2:G${d.tabs['Screening log'].length+1},"retain_or_uncertain")`]];
overview.getRange('B9').formulas=[[`=COUNTA('Study summary'!A2:A${d.tabs['Study summary'].length+1})`]];
overview.getRange('B10').formulas=[[`=COUNTA('QA items'!A2:A${nr})`]];
overview.getRange('B11').formulas=[[`=COUNTA(Outcomes!A2:A${d.tabs.Outcomes.length+1})`]];
overview.getRange('A21:C22').values=[['Source-assessed reports',d.counts.source_assessed_reports,'Includes assessed exclusions and reports with forms'],['Assessed EC2 exclusions',d.counts.assessed_fulltext_exclusions,'TGS and HiveD; AI source judgments, not a complete exclusion census']];
overview.getRange('A21:C22').format={font:{name:'Arial',size:11},wrapText:true,rowHeight:50};
overview.getRange('A16:C19').values=[['How to read','Start with Study summary','Report IDs link full-text criteria, QA, extraction and outcomes'],['Search / selection','Search runs, Screening log, Duplicates','All rows retain provenance and current decision status'],['Paper-by-paper evidence','QA items, Study extraction, Outcomes','Do not mix percentile/mean, training/inference, GPU/NPU or local/fleet results'],['Remaining work','Review issues and Abstract audit','Uncertain fields/cases remain explicit; original detailed audit workbook retained']];
overview.getRange('A3:C19').format={font:{name:'Arial',size:11},rowHeight:48,wrapText:true};overview.getRange('A3:C3').format={fill:'#243B53',font:{color:'#FFFFFF',bold:true},rowHeight:34};overview.getRange('A1:A19').format.columnWidth=34;overview.getRange('B1:B19').format.columnWidth=32;overview.getRange('C1:C19').format.columnWidth=83;
wb.recalculate();
if(overview.getRange('B4:B11').values.map(r=>r[0]).join(',')!==[4189,114,4075,1441,2634,15,150,45].join(','))throw Error('Overview/source count mismatch');
for(let i=0;i<d.qa_matrix.length;i++){
 const a=summary.getRange(`H${i+2}`).values[0][0],b=summary.getRange(`M${i+2}`).values[0][0];
 if(a!==Number(d.qa_matrix[i].raw_sum)||b!==Number(d.qa_matrix[i].applicable_max))throw Error('QA mismatch '+d.qa_matrix[i].report_id);
}
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:1000})).ndjson);
for(const name of ['Overview',...Object.keys(d.tabs)]){
 const range=name==='Overview'?'A1:C22':'A1:D5';const img=await wb.render({sheetName:name,range,scale:1.2,format:'png'});
 await fs.writeFile(process.env.OS_CEP_PREVIEW_DIR+'/'+name.replaceAll(' ','_')+'.png',new Uint8Array(await img.arrayBuffer()));
}
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(root+'/task2/submission/GroupB_Submission_Workbook.xlsx');
console.log('Saved13-tab compact workbook; counts and QA totals checked');

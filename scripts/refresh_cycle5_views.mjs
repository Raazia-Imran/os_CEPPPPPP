import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.env.OS_CEP_ROOT,file=process.env.OS_CEP_WORKBOOK;
const data=JSON.parse(await fs.readFile(root+'/task2/qa/active_views_input.json','utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));
const xl=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
for(const [name,d] of Object.entries(data)){
 const sh=wb.worksheets.getItem(name);const end=xl(d.fields.length-1),last=d.rows.length+1;
 // Existing large screening tabs keep their dimensions; overwrite the complete current block.
 if(last<300)sh.getRange('A1:AZ300').clear();
 sh.getRange(`A1:${end}${last}`).values=[d.fields,...d.rows.map(r=>d.fields.map(k=>r[k]??''))];
 sh.getRange(`A1:${end}${last}`).format.font={name:'Arial',size:10};
 sh.getRange(`A1:${end}1`).format={fill:'#243B53',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true};
 sh.getRange(`A2:${end}${last}`).format.wrapText=true;sh.getRange(`A2:${end}${last}`).format.autofitRows();
}
const s=wb.worksheets.getItem('Summary');
s.getRange('A6').values=[['Applied duplicate links']];s.getRange('C6').values=[['111 earlier links plus3 publisher-verified identities']];
s.getRange('B11').values=[[17]];
s.getRange('C11').values=[['17 source assessments: 2 EC2 exclusions;15 QA/extraction forms']];
s.getRange('C8').values=[['First automated triage; not full-abstract verification or final screening']];
s.getRange('A37:C37').values=[['Current synthesis rows',105,'Current source-linked views; Cycle2 tables remain preserved in evidence history']];
s.getRange('A40:C40').values=[['Current report PDF','Current 22-section checkpoint','Updated through22sections; final eligibility/PRISMA stages pending']];
s.getRange('A37:C40').format.wrapText=true;s.getRange('A37:C40').format.rowHeight=50;
wb.recalculate();
for(const [name,d] of Object.entries(data)){
 const img=await wb.render({sheetName:name,range:'A1:D4',format:'png',scale:1.2});
 await fs.writeFile(process.env.OS_CEP_PREVIEW_PREFIX+'-'+name.replaceAll(' ','_')+'.png',new Uint8Array(await img.arrayBuffer()));
}
const img=await wb.render({sheetName:'Summary',range:'A31:D46',format:'png',scale:1.2});await fs.writeFile(process.env.OS_CEP_PREVIEW_PREFIX+'-Summary.png',new Uint8Array(await img.arrayBuffer()));
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:1000})).ndjson);
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(file);console.log('Current synthesis,reference catalogue,requirements and Summary refreshed');

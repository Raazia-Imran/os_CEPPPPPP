import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const file=process.env.OS_CEP_WORKBOOK;
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));
function col(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
const data=JSON.parse(await fs.readFile(process.env.OS_CEP_ROOT+'/task2/tracker/workbook_input.json','utf8'));
const audit=wb.worksheets.getItem('Requirements audit');
const af=data.fields['Requirements audit'];
const av=[af,...data.sheets['Requirements audit'].map(r=>af.map(k=>r[k]??''))];
audit.getRange(`A1:${col(af.length-1)}${av.length}`).values=av;
audit.getRange(`A2:${col(af.length-1)}${av.length}`).format.autofitRows();
for(const [name,rows] of Object.entries(data.sheets)){
 if(!rows.length)continue;const sh=wb.worksheets.getItem(name);
 const headers=sh.getRange('A1:CB1').values[0];
 for(let i=0;i<headers.length;i++){
  if(typeof headers[i]!=='string')continue;
  if(/(_at_utc|timestamp_utc)$/.test(headers[i]))sh.getRange(`${col(i)}2:${col(i)}${rows.length+1}`).setNumberFormat('yyyy-mm-dd hh:mm:ss');
  if(/^(date|checked_date)$/.test(headers[i]))sh.getRange(`${col(i)}2:${col(i)}${rows.length+1}`).setNumberFormat('yyyy-mm-dd');
 }
}
wb.recalculate();
const img=await wb.render({sheetName:'Retrieval log',range:'A1:D5',format:'png',scale:1.2});
await fs.writeFile(process.env.OS_CEP_DATE_PREVIEW,new Uint8Array(await img.arrayBuffer()));
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(file);
console.log('Date display formats applied; workbook saved');

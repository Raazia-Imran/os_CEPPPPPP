import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.env.OS_CEP_ROOT,file=process.env.OS_CEP_WORKBOOK;
const input=JSON.parse(await fs.readFile(root+'/task2/qa/active_views_input.json','utf8'));const d=input['Requirements audit'];
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));const sh=wb.worksheets.getItem('Requirements audit');
const xl=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
sh.getRange(`A1:${xl(d.fields.length-1)}${d.rows.length+1}`).values=[d.fields,...d.rows.map(r=>d.fields.map(k=>r[k]??''))];
wb.recalculate();const image=await wb.render({sheetName:'Requirements audit',range:'A10:D15',format:'png',scale:1.2});await fs.writeFile(process.env.OS_CEP_PREVIEW_PREFIX+'-requirements.png',new Uint8Array(await image.arrayBuffer()));
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(file);console.log('Requirements audit synchronized');

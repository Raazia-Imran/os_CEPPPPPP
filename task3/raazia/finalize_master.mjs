import fs from 'node:fs/promises';import path from 'node:path';import {SpreadsheetFile,FileBlob} from '@oai/artifact-tool';
const dir=path.dirname(new URL(import.meta.url).pathname),root=path.resolve(dir,'..'),data=JSON.parse(await fs.readFile(dir+'/review_data.json','utf8'));
const w=await SpreadsheetFile.importXlsx(await FileBlob.load(root+'/workbook/CEP_Task3_Evidence_Workbook.xlsx'));
const guide=w.worksheets.getItem('Task 3 Guide');guide.getRange('B2').values=[['Frozen14-tab baseline preserved separately. Active data applies the documented seven-study AI review; original and reviewed QA scores appear in Raazia QA Review.']];
const rec=w.worksheets.getItem('PDF Retrieval'),rows=rec.getUsedRange().values;const src=data.sources.find(x=>x['Report ID']==='P008');
for(let i=1;i<rows.length;i++)if(rows[i][0]==='P008'){
 rec.getCell(i,5).values=[[src['Source URL']]];rec.getCell(i,9).values=[['Readable15-page academic-mirror copy installed during current source review; original retrieval times remain historical. See Raazia Source and Identity Review for current check timestamp.']];rec.getCell(i,10).values=[[src.SHA256]];rec.getCell(i,11).values=[[(await fs.stat(root+'/papers/P008.pdf')).size]];rec.getCell(i,12).values=[[data.checked_utc]];
}
w.recalculate();await(await SpreadsheetFile.exportXlsx(w)).save(root+'/workbook/CEP_Task3_Evidence_Workbook.xlsx');
console.log('Master guide and reading-copy metadata updated');

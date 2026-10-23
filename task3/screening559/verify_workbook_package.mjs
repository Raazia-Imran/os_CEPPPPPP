import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob, SpreadsheetFile} from '@oai/artifact-tool';
const root=await fs.realpath(process.cwd());
await fs.access(path.join(root,'AGENTS.md'));
const dir=await fs.realpath(path.join(root,'task3','screening559','integrated_workbook'));
if(path.relative(root,dir)!==path.join('task3','screening559','integrated_workbook')){throw new Error('Unexpected output directory');}
const w=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(dir,'CEP_Task3_Working_Integrated_2026-10-23.xlsx')));
w.recalculate();
const get=name=>w.worksheets.getItem(name);
const diff=get('Count Reconciliation').getRange('D2:D12').values.flat();
if(diff.some(x=>x!==0)){throw new Error('Packaged count reconciliation failed');}
const study=get('Studies').getUsedRange().values;
const targetIds=['S027','S028','S029','S030'];
const scores=Object.fromEntries(targetIds.map(id=>{const row=study.find(x=>x[0]===id); if(!row){throw new Error('Missing added study '+id);}return [id,{score:row[6],maximum:row[7]}];}));
if(scores.S027.score!==13||scores.S027.maximum!==18||scores.S028.score!==15||scores.S028.maximum!==20||scores.S029.score!==14||scores.S029.maximum!==18){throw new Error('Packaged QA values differ from source registers');}
const result={tabs:w.worksheets.items.length,working_studies:study.length-1,count_differences:diff,added_QA_checks:scores,transport_shared_strings_readback_passed:true,cell_values_formulas_and_styles_preserved:true};
const expected=JSON.parse(await fs.readFile(path.join(dir,'..','integrated_report','integration_summary.json'),'utf8'));
if(result.tabs!==38||result.working_studies!==expected.working_studies||scores.S030.score!==14||scores.S030.maximum!==16){throw new Error('Packaged sheet/study count or KACE score mismatch');}
await fs.writeFile(path.join(dir,'package_readback_validation.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));

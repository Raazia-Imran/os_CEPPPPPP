"""Read saved XLSX XML and PDF text; never author spreadsheets here."""
import hashlib, json, math, re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader

R=Path(__file__).resolve().parents[1]
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def book(path):
    result={}
    with zipfile.ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(t.itertext()) for t in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',NS)]
        rel={x.attrib['Id']:x.attrib['Target'] for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',NS):
            key=sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target=rel[key]; name=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            cells={}
            for c in ET.fromstring(z.read(name)).findall('.//s:sheetData/s:row/s:c',NS):
                value=c.find('s:v',NS);v=value.text if value is not None else ''
                if c.attrib.get('t')=='s':v=strings[int(v)] if v else ''
                elif c.attrib.get('t')=='inlineStr':v=''.join(c.find('s:is',NS).itertext())
                f=c.find('s:f',NS)
                if v or f is not None:cells[c.attrib['r']]={'value':v or '', 'formula':f.text if f is not None else '', 'type':c.attrib.get('t','n')}
            result[sheet.attrib['name']]=cells
    return result
def same(a,b):
    if a['formula']!=b['formula']:return False
    if a['value']==b['value']:return True
    if a['type'] in ('n','') and b['type'] in ('n',''):
        try:return math.isclose(float(a['value']),float(b['value']),rel_tol=1e-12,abs_tol=1e-12)
        except ValueError:return False
    return False
def validate(before,after,private=False):
    old,new=book(before),book(after)
    assert len(old)==43 and len(new)==47,(len(old),len(new))
    differences=[]
    for sheet,cells in old.items():
        assert sheet in new
        for addr,c in cells.items():
            if not same(c,new[sheet].get(addr,{'value':'','formula':'','type':'n'})):
                differences.append((sheet,addr,c,new[sheet].get(addr)))
    assert not differences, differences[:5]
    errors=[(s,a,c['value']) for s,cells in new.items() for a,c in cells.items() if c['type']=='e']
    assert not errors,errors[:5]
    qa=json.loads((R/'task2/qa/workbook_update.json').read_text())['matrix']
    for i,row in enumerate(qa,2):
        for col,k in [('M','raw_sum'),('N','applicable_max')]:
            assert float(new['QA matrix'][f'{col}{i}']['value'])==float(row[k])
        assert math.isclose(float(new['QA matrix'][f'O{i}']['value']),float(row['raw_sum'])/float(row['applicable_max']),rel_tol=1e-12)
    abstracts=sum(bool(c['value']) for a,c in new['Records'].items() if re.fullmatch(r'N\d+',a) and a!='N1')
    assert abstracts>0 if private else abstracts==0
    return dict(sheets=len(new),preserved_original_sheets=len(old),original_cell_differences=len(differences),saved_error_cells=len(errors),
        qa_formula_totals='matched all nine source totals',abstract_cells=abstracts,sha256=hashlib.sha256(Path(after).read_bytes()).hexdigest())
public=validate('/tmp/c4-wb/public-baseline.xlsx',R/'task2/tracker/review_workbook.xlsx')
private=validate('/tmp/c4-wb/private-baseline.xlsx',R.parent/'private_cycle3/review_workbook.xlsx',True)
pdf=R/'task2/qa/GroupB_Current_QA_and_Extraction.pdf'
reader=PdfReader(pdf);text='\n'.join(p.extract_text() for p in reader.pages)
for i in range(1,10):assert f'GB-P{i:03}' in text
for i in range(1,35):assert f'GB-O{i:03}' in text
receipt=dict(public_workbook=public,private_workbook=private,pdf=dict(pages=len(reader.pages),all_9_report_ids=True,all_34_outcome_ids=True,sha256=hashlib.sha256(pdf.read_bytes()).hexdigest()),
    recalculation='Artifact Tool test: changed first score 2 to 1, total decreased by 1, original restored and totals rechecked',
    native_excel_opening='not performed',independent_human_checks_added=0)
(R/'task2/qa/artifact_validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))

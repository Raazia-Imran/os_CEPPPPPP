"""Losslessly compact artifact-tool OOXML shared strings for Git transport.

This changes serialization only. Resolved worksheet values, formulas and style
indices are verified identical before replacing the generated workbook.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
import json, hashlib, os
BASE = Path(__file__).resolve().parent / 'integrated_workbook'
TARGET = BASE / 'CEP_Task3_Working_Integrated_2026-10-23.xlsx'
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
T = lambda tag: '{' + NS + '}' + tag
with ZipFile(TARGET) as z:
    parts = {name: z.read(name) for name in z.namelist()}
original_size = TARGET.stat().st_size
sst = E.fromstring(parts['xl/sharedStrings.xml']) if 'xl/sharedStrings.xml' in parts else E.Element(T('sst'), nsmap={None: NS})
strings = [''.join(si.itertext()) for si in sst]
lookup = {value: i for i, value in enumerate(strings)}
def snapshot(root, values):
    cells = []
    for c in root.iter(T('c')):
        v, f = c.find(T('v')), c.find(T('f'))
        value = v.text if v is not None else None
        if c.get('t') == 's' and value is not None:
            value = values[int(value)]
        cells.append((c.get('r'), value, E.tostring(f) if f is not None else None, c.get('s')))
    return cells
changed = 0
for name in sorted(parts):
    if not (name.startswith('xl/worksheets/') and name.endswith('.xml')):
        continue
    root = E.fromstring(parts[name])
    before = snapshot(root, strings)
    for c in root.iter(T('c')):
        v = c.find(T('v'))
        if c.get('t') != 'str' or c.find(T('f')) is not None or v is None or v.text is None:
            continue
        value = v.text or ''
        if value not in lookup:
            lookup[value] = len(strings)
            strings.append(value)
            si = E.SubElement(sst, T('si'))
            text = E.SubElement(si, T('t'))
            text.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            text.text = value
        c.set('t', 's')
        v.text = str(lookup[value])
        changed += 1
    assert before == snapshot(root, strings), name
    parts[name] = E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
sst.set('uniqueCount', str(len(strings)))
sst.set('count', str(int(sum(E.fromstring(data).xpath('count(//*[local-name()="c"][@t="s"])') for name, data in parts.items() if name.startswith('xl/worksheets/') and name.endswith('.xml')))))
parts['xl/sharedStrings.xml'] = E.tostring(sst, xml_declaration=True, encoding='UTF-8', standalone=True)
temp = TARGET.with_suffix('.compact.xlsx')
try:
    with ZipFile(temp, 'w', compression=ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in parts.items():
            z.writestr(name, data)
    with ZipFile(temp) as z:
        assert z.testzip() is None
    os.replace(temp, TARGET)
finally:
    temp.unlink(missing_ok=True)
result = {'original_bytes': original_size, 'compact_bytes': TARGET.stat().st_size,
          'converted_string_cells': changed, 'resolved_values_formulas_styles_identical': True,
          'sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest()}
(BASE / 'transport_serialization_validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))

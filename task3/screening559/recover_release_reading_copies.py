"""Recover private reading copies; record access separately from eligibility."""
from pathlib import Path
import csv, hashlib, urllib.request, concurrent.futures, datetime, shutil

d=Path(__file__).resolve().parent
private=Path('/workspace/scratch/18d5426b12a3/private_reading/release')
private.mkdir(exist_ok=True)
refs=list(csv.DictReader((d/'New_Included_References.csv').open()))
library=Path('/workspace/scratch/18d5426b12a3/private_reading/library_copies')

def fetch(x):
    dest=private/(x['Study ID']+'_'+x['Report ID']+'.pdf')
    row={'Study ID':x['Study ID'],'Report ID':x['Report ID'],'Title':x['Title'],'DOI':x['DOI'],
         'Source URL':x['Primary text URL'],'Assessment source SHA256':x['Primary evidence hash'],
         'Recovered SHA256':'','Matches assessed source':'','PDF available in private bundle':'No',
         'Access result':'','Checked UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        supplied=list(library.rglob(x['DOI'].split('/')[-1]+'.pdf'))
        if supplied:
            b=supplied[0].read_bytes();route='Previously supplied reading copy recovered'
        elif x['Study ID']=='S030':
            b=private.parent.joinpath('KACE.pdf').read_bytes();route='Author-hosted copy recovered'
        else:
            req=urllib.request.Request(x['Primary text URL'],headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=25) as f:b=f.read()
            route='Public author/repository PDF downloaded'
        assert b.startswith(b'%PDF'), 'Response is not a PDF'
        dest.write_bytes(b);sha=hashlib.sha256(b).hexdigest()
        row.update({'Recovered SHA256':sha,'Matches assessed source':'Yes' if sha==x['Primary evidence hash'] else 'No; version check required',
                    'PDF available in private bundle':'Yes','Access result':route})
    except Exception as e:row['Access result']=type(e).__name__+': '+str(e)[:160]
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(fetch,refs))
with (d/'Release_Reading_Copy_Access.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for r in rows:print(r['Study ID'],r['PDF available in private bundle'],r['Matches assessed source'],r['Access result'])

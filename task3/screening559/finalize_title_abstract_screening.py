"""Conservative stage decisions; advancement is not final inclusion.

Adopts explicit recorded assessments after a conservative scope audit. Reopens
borderline systems papers instead of treating absent tenant detail as exclusion.
"""
from pathlib import Path
import csv,datetime,hashlib,json,collections
d=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
q=list(csv.DictReader((d/'Working_559_Queue.csv').open(newline='')))
# Explicitly reviewed records whose positive topic/type evidence supports exclusion.
early_exclude=set('''R00050 R00051 R00055 R00065 R00092 R00099 R00100 R00102
R00106 R00115 R00119 R00154 R00165 R00176 R00180 R00191 R00194 R00221
R00225 R00239 R00322 R00335 R00344 R00348 R00356 R00377 R00382 R00398
R00415 R00416 R00422 R00446 R00449 R00455 R00468 R00475 R00479 R00489
R00519 R00540 R00571 R00580 R00649 R00653 R00691 R00959 R01099 R01115
R01318 R01530 R01567 R01570 R01577 R01578 R01581 R01652 R01674 R01951
R02105 R02115 R02219 R02237 R02238 R02245 R02292 R02299'''.split())
# These otherwise proposed exclusions require primary clarification or have data
# quality concerns. Uncertainty advances a record; it does not exclude it.
late_reopen=set('''R02358 R02372 R02596 R02660 R03098 R03153 R03671 R03811 R04108'''.split())
out=[];changes=[]
for x in q:
    rid=x['Record ID']
    proposed=x['Preparation recommendation']=='propose_exclusion'
    excluded=proposed and (rid in early_exclude or (rid>='R02300' and rid not in late_reopen))
    text=x['Recovered abstract'] or x['Supplemental abstract']
    titleonly=not bool(text)
    decision='Exclude at title/abstract stage' if excluded else 'Advance to report retrieval/full-text eligibility'
    reason=x['Preparation rationale'] if excluded else (
        'Conservative reopening: existing metadata does not justify a decisive exclusion; inspect primary scope/version.' if proposed else
        'Potentially eligible or uncertain; inspect primary scope/version and all IC1-IC6. Advancement is not inclusion.')
    payload=json.dumps({'Record ID':rid,'Title':x['Title'],'DOI':x['DOI'],'Text':text},ensure_ascii=False,sort_keys=True).encode()
    out.append({'Record ID':rid,'Title':x['Title'],'DOI':x['DOI'],
        'Final screening decision':decision,'Exclusion criterion':x['Preparation criterion'] if excluded else '',
        'Decision rationale':reason,'Evidence level':'Title and metadata only' if titleonly else 'Recorded title and abstract/recovered text',
        'Evidence location':'Working_559_Queue.csv: '+rid+'; corresponding Batch/Title_Batch review',
        'Evidence SHA256':hashlib.sha256(payload).hexdigest(),
        'Method':'Single automated screening; adopts recorded assessment with conservative scope audit; M2026-10-23',
        'Independent human vote':'','Final checked UTC':now,
        'Missing abstract used as exclusion reason':'No','Final full-text eligibility':'Separate stage'})
    if proposed and not excluded:
        changes.append({'Record ID':rid,'Earlier recommendation':'propose_exclusion','Final screening decision':decision,
            'Reason':reason,'Earlier rationale retained':x['Preparation rationale'],'Checked UTC':now})
for name,rows in [('Final_Screening_Decisions.csv',out),('Conservative_Screening_Reopenings.csv',changes)]:
    with (d/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
counts=collections.Counter(x['Final screening decision'] for x in out)
assert len(out)==559 and len({x['Record ID'] for x in out})==559
summary={'records_screened':559,'excluded_at_screening':counts['Exclude at title/abstract stage'],
    'advanced_to_report_retrieval':counts['Advance to report retrieval/full-text eligibility'],
    'earlier_proposed_exclusions_reopened':len(changes),'title_only_exclusions':sum(x['Evidence level']=='Title and metadata only' and x['Exclusion criterion']!='' for x in out),
    'missing_abstract_exclusions':0,'duplicate_report_linkage_pending':True,
    'meaning':'Branch stage accounting only; not a reconciled whole-review PRISMA flow',
    'checked_utc':now}
(d/'Screening_Stage_Accounting.json').write_text(json.dumps(summary,indent=2)+'\n')
p=json.loads((d/'progress.json').read_text());p.update({'title_abstract_stage_closed':True,
    'final_screening_complete':True,'final_screening_decisions':559,
    'final_screening_excluded':summary['excluded_at_screening'],
    'final_screening_advanced':summary['advanced_to_report_retrieval'],
    'screening_reopened_prior_proposals':len(changes),
    'all_full_text_eligibility_closed':False,'prisma_reconciliation_pending':True})
(d/'progress.json').write_text(json.dumps(p,indent=2)+'\n')
print(json.dumps(summary))

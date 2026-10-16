"""Derive QA deliverables from unchanged first-review evidence; never fabricate checks."""
import csv, hashlib, json, re
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
E = R/'evidence'
O = R/'task2/qa'
O.mkdir(exist_ok=True)
def read(p):
    with p.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def write(p, rows, fields=None):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
qa=read(E/'quality.csv'); forms=read(E/'study_extraction_form.csv')
checks={x['report_id']:x for x in read(E/'fulltext_checks.csv')}
outcomes=read(E/'extraction.csv')
assert len(qa)==len({(x['report_id'],x['criterion']) for x in qa})
matrix=[]; details=[]; followup=[]
for form in forms:
    rid=form['report_id']; rows=[x for x in qa if x['report_id']==rid]
    assert {x['criterion'] for x in rows}=={f'Q{i}' for i in range(1,11)}, rid
    byq={x['criterion']:x for x in rows}
    for x in rows:
        assert x['rationale'].strip() and x['anchor'].strip()
        assert (x['score']=='NA' and x['maximum']=='0') or (x['score'] in ['0','1','2'] and x['maximum']=='2')
        details.append(dict(x,anchor_precision='printed_page_and_section_or_figure' if re.search(r'\bp{1,2}\d',x['anchor']) else 'section_or_figure_only;PDF_page_mapping_pending',
            cycle4_action='preserved_initial_score;register_consistency_checked;not_a_new_source_review',
            independent_check_status='pending' if not x['independent_checker'] else 'see_original_fields'))
    total=sum(int(x['score']) for x in rows if x['score']!='NA')
    maximum=sum(int(x['maximum']) for x in rows)
    matrix.append(dict(report_id=rid,title=form['title'],doi=form['doi'],
        **{f'Q{i}':byq[f'Q{i}']['score'] for i in range(1,11)},
        raw_sum=total,applicable_max=maximum,normalized_pct=round(100*total/maximum,2),
        below_60_sensitivity_flag='yes' if total/maximum<.6 else 'no',
        na_criteria=';'.join(x['criterion'] for x in rows if x['score']=='NA'),
        qa_status='AI_first_review;independent_check_pending;not_final',
        eligibility_status=checks[rid]['first_reviewer_recommendation']))
    missing_pages=sum(not re.search(r'\bp{1,2}\d',x['anchor']) for x in rows)
    special={'GB-P001':'Calibrate Q7 N/A against complete source; map section/figure anchors to original PDF pages.',
        'GB-P002':'Map section/figure anchors to original PDF pages; verify software/workload reporting.',
        'GB-P004':'Resolve mixed training/inference scope using separable local inference measurements.',
        'GB-P005':'Resolve conference/journal report relationship before study counting; do not substitute journal DOI.',
        'GB-P006':'Independently calibrate Q9 N/A: distinguish performance fairness from claimed resource/security/fault isolation.'}.get(rid,'Recheck all criterion rationales against the exact source version.')
    if rid=='GB-P011':special='Accessed source is arXivv1; establish equivalence to final SC24 report before inclusion.'
    if rid=='GB-P015':special='Check claim-specific Q9 N/A; GPU case only, not NPU/ASIC/FPGA gains.'
    followup.append(dict(report_id=rid,title=form['title'],doi=form['doi'],qa_rows=len(rows),
        outcome_rows=sum(x['report_id']==rid for x in outcomes),
        items_without_printed_page=missing_pages,calibration_or_scope_task=special,
        required_return='Independent Q1-Q10 scores, rationale, exact PDF page/section/table/figure; preserve initial scores; verify registered outcomes and IC1-IC6.',
        independent_checker='',checked_at_utc='',reconciliation_status='pending',final_decision='pending'))
write(O/'qa_score_matrix.csv',matrix)
write(O/'qa_totals_summary.csv',[{k:x[k] for k in ['report_id','title','raw_sum','applicable_max','normalized_pct','below_60_sensitivity_flag','na_criteria','qa_status','eligibility_status']} for x in matrix])
write(O/'qa_rationale_table.csv',details)
write(O/'qa_followup.csv',followup)
write(O/'qa_corrections.csv',[],['report_id','criterion','original_score','proposed_score','original_maximum','proposed_maximum','reason','source_anchor','assessor','assessor_type','checked_at_utc','independent_status','reconciliation_status'])
rubric=[
('Q1','Clarity of objective','Problem, proposed mechanism and evaluated questions are clear.'),
('Q2','Technical description','Sharing primitive, configuration and implementation layer permit classification.'),
('Q3','Experimental transparency','Setup, measurement procedure, repetitions or analytical method and result provenance are clear.'),
('Q4','Hardware/workload description','GPU model/generation, software and concurrent inference workload/tenant characteristics are reported.'),
('Q5','Baseline fairness','Relevant baseline and comparable workload, resources and measurements are documented or justified.'),
('Q6','Utilization/throughput','Claimed benefit has defined metric, unit and method; otherwise alternate outcome is explained.'),
('Q7','Latency measurement','Claimed latency specifies interval, load, statistic and method; claimed tail/SLO results state a quantile.'),
('Q8','Multi-tenant interference','Concurrent tenants/co-tenants are tested and evidence supports interference conclusions.'),
('Q9','Isolation evaluation','Claimed resource, security or fault isolation has a defined boundary and direct test or delimited evidence.'),
('Q10','Replication/limits','Details/artifacts support informed replication; threats, limits or configuration dependence are discussed.')]
write(O/'qa_checklist.csv',[dict(criterion=q,label=label,score_2_requires=text,score_1='Partly addressed',score_0='Absent or unclear',protocol_anchor='Submitted protocol section 10, Table 8, printed pp11-12') for q,label,text in rubric])
summary=dict(report_forms=len(forms),reports_with_all_10_items=len(matrix),qa_items=len(qa),outcomes=len(outcomes),
    na_items=[x['report_id']+':'+x['criterion'] for x in qa if x['score']=='NA'],
    below_60_reports=[x['report_id'] for x in matrix if x['below_60_sensitivity_flag']=='yes'],
    source_scores_changed=0,new_independent_human_checks=0,
    second_score_populated=sum(bool(x['second_score']) for x in qa),
    reconciled_score_populated=sum(bool(x['reconciled_score']) for x in qa),
    assessed_reports_without_qa=sorted({rid for rid,x in checks.items() if x['first_reviewer_recommendation']!='exclude_recommendation'}-{x['report_id'] for x in matrix}),
    excluded_reports_without_qa_by_design=sorted(rid for rid,x in checks.items() if x['first_reviewer_recommendation']=='exclude_recommendation'),
    anchor_precision=dict(Counter(x['anchor_precision'] for x in details)),
    source_sha256={n:hashlib.sha256((E/n).read_bytes()).hexdigest() for n in ['quality.csv','extraction.csv','study_extraction_form.csv','screening.csv']},
    limitations=['Register audit and derivation, not a new full-source reappraisal.','N/A calibration and human independent scoring pending.','No final included-study count or overall completion percentage inferred.'])
(O/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
(O/'QA_CHECKLIST_AND_SCORING.md').write_text('''# Group B quality assessment: current nine-report checkpoint

Authority: submitted protocol section 10, Table 8, printed pp11-12. Use Q1-Q10, 0-2: 0 absent/unclear, 1 partial, 2 sufficiently supported. The full maximum is 20. qa_checklist.csv records every criterion. The other group's QA1-QA8 /8 and VRAM-oversubscription exclusion codes do not apply.

N/A is only for a claim the paper genuinely does not make, with rationale. Missing reporting is not N/A. Exclude the item's maximum from the denominator. Display raw sum, applicable maximum and normalized percentage. Below 60% is a sensitivity view, never an eligibility gate. There are two provisional N/A judgments: VastPipe Q7 and Paella Q9; the required independent two-study calibration is not recorded as complete.

All nine assessed provisional report forms have ten QA items: 90 total. The score matrix and detailed rationale table are derived from unchanged evidence/quality.csv. This cycle checks keys, completeness, ranges, N/A denominators and arithmetic. It does not assert a fresh reading or verification of every source. Initial scores, assessors and independent fields are preserved. qa_corrections.csv is empty because no source-justified score correction was made in this pass.

Twenty legacy items for VastPipe and iGniter have section/figure anchors but no printed PDF page mapping; 70 items have printed page anchors. Exact pages and all rationales still need source verification. Source pointers naming supplied Markdown are provenance, not downloadable URLs. Do not invent a DOI for USENIX conference reports or replace REEF's conference identity with its journal version.

qa_followup.csv assigns the remaining source/independent checks for every report. No currently assessed report lacks initial QA; unassessed candidates are not automatically eligible or scored. All 90 second and reconciled score fields remain blank. No paper is below 60% on the preserved initial scores; this does not establish that conclusions are robust to unresolved eligibility, calibration or reporting gaps.

For an independent check: hide initial score/rationale columns; open the exact source version; score each Q with a page/table/figure and your rationale; enter your name and actual date. Preserve your scores before comparing. Log disagreements as proposed corrections, then record the actual adjudicator and reconciled score. Leave final decisions pending until the review process genuinely resolves them.
''')
incoming=read(R/'task2/reconciliation/claude_ai_opinions.csv')
comparison={x['record_id']:x for x in read(R/'task2/reconciliation/ai_comparison.csv')}
opinions=[dict(x,**{k:comparison[x['record_id']][k] for k in ['current_ai_vote','comparison','action']}) for x in incoming]
(O/'workbook_update.json').write_text(json.dumps(dict(matrix=matrix,quality=qa,followup=followup,
    checklist=read(O/'qa_checklist.csv'),opinions=opinions))+'\n')
(O/'QA_CHECKLIST_AND_SCORING.md').write_text(f'''# Current Group B Q1-Q10 assessment

Authority: submitted protocol section10/Table8, printed pp11-12. Score0 absent/unclear;1 partial;2 supported. Full maximum20. Justified N/A excludes its maximum from the denominator; missing reporting is not N/A. Below60% is sensitivity analysis, not exclusion.

There are {len(matrix)} assessed report forms and {len(qa)} item rows. Original scores and fields were preserved; Cycle5 adds source-based AI assessments. None is claimed to be independent human review. Second/reconciled fields remain blank unless genuinely supplied. Source-version uncertainty is not eligibility: ParvaGPU is explicitly uncertain; REEF companion identity remains open.

Provisional N/A items: {', '.join(summary['na_items'])}. Required calibration remains unperformed. Items without printed-page precision: {sum(x['items_without_printed_page'] for x in followup)}. Detailed anchors and rationales are in qa_rationale_table.csv; remaining checks in qa_followup.csv. Section-only anchors are not fabricated PDF pages. Source pointers naming supplied Markdown are provenance rather than downloadable URLs.

All matrix totals are recalculated from source rows. No score changes to the earlier reports are claimed in this batch. Empty correction tables are not evidence of independent agreement. No report falls below60% on current first scores; this does not establish robustness to incomplete selection, source versions or missing evidence. Study/report/outcome counts remain distinct.
''')
print(json.dumps(summary,indent=2))

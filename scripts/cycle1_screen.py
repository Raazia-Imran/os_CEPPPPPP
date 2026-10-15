"""Append conservative, auditable preliminary recommendations; never final decisions.

Original votes and raw imports are preserved. Shared search-result snippets are
explicitly distinguished from abstracts. Metadata enrichment does not identify
additional occurrences or establish full-text access.
"""
import argparse, csv, hashlib, json, re, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from import_shared import bib_entries, doi_key, title_key, csvwrite
ROOT=Path(__file__).resolve().parents[1]; E=ROOT/'evidence'
def read(n): return list(csv.DictReader((E/n).open(encoding='utf-8-sig')))
def now():return datetime.now(timezone.utc).isoformat(timespec='seconds')
def overlay():
    if (E/'metadata_enrichment.csv').is_file() and (E/'incoming_shared/acm_master/reconciliation.json').is_file():
        prior=json.loads((E/'incoming_shared/acm_master/reconciliation.json').read_text())
        if all(hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256'] for a in prior['files']):
            return read('metadata_enrichment.csv')
    rows=[]; ix={}; tx={}
    old=read('records.csv'); oldkeys={doi_key(r['doi']) or title_key(r['title']) for r in old}
    extras=[]; audit=[]
    for p in sorted((E/'incoming_shared/acm_master').glob('*.bib')):
        raw=p.read_bytes(); entries=list(bib_entries(raw.decode('utf-8-sig')))
        audit.append(dict(file=str(p.relative_to(ROOT)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),parsed_entries=len(entries)))
        for typ,key,f in entries:
            f=dict(f,entry_type=typ,source=str(p.relative_to(ROOT)),source_sha256=audit[-1]['sha256'])
            if f.get('doi'):ix.setdefault(doi_key(f['doi']),f)
            tx.setdefault(title_key(f.get('title','')),[]).append(f)
            if (doi_key(f.get('doi','')) or title_key(f.get('title',''))) not in oldkeys:
                extras.append(dict(title=f.get('title',''),doi=f.get('doi',''),year=f.get('year',''),venue=f.get('booktitle',f.get('journal','')),source=f['source'],status='staged_not_in_active_counts',final_decision='pending'))
    for r in old:
        f=ix.get(doi_key(r['doi'])) if r['doi'] else None
        match='exact DOI'
        if not f and not r['doi']:
            candidates=tx.get(title_key(r['title']),[])
            ds={doi_key(c.get('doi','')) for c in candidates}
            if len(ds)==1 and candidates:f=candidates[0];match='exact normalized title; one distinct DOI in recovered masters; identity still pending'
        if f and f.get('abstract'):
            rows.append(dict(record_id=r['record_id'],match_basis=match,title=f.get('title',''),doi=f.get('doi',''),authors=f.get('author',''),year=f.get('year',''),venue=f.get('booktitle',f.get('journal','')),entry_type=f['entry_type'],abstract=f['abstract'],source_file=f['source'],source_sha256=f['source_sha256'],checked_at_utc=now()))
    csvwrite(E/'metadata_enrichment.csv',rows)
    unique={r['doi'] or title_key(r['title']):r for r in extras}
    csvwrite(E/'incoming_shared/acm_master/staged_new_candidates.csv',list(unique.values()))
    (E/'incoming_shared/acm_master/reconciliation.json').write_text(json.dumps(dict(files=audit,claimed_displayed=1600,claimed_exported=1603,actual_combined_occurrences=sum(a['parsed_entries'] for a in audit),actual_distinct_doi_or_title=len(ix),new_distinct_candidates=len(unique),metadata_enriched_occurrences=len(rows),active_counts_changed=False,conclusion='Two overlapping exports; teammate claimed total is not reproduced. Existing numbered exports not automatically mapped to this run.'),indent=2)+'\n')
    return rows
GPU=r'\bgpus?\b|graphics processing|\bcuda\b|\bnvidia\b|\btesla\b'
INF=r'inferen|model.?serv|\bserving\b|prediction serving'
SHARE=r'multi.?tenan|co.?locat|co.?execut|concurren|gpu.shar|spatial.shar|time.slic|multi.instance|multi.process service|\bmps\b|\bmig\b|preempt|interferen|cuda remot|api remot|gpu virtual|gpu partition|multiplex|multi.model|multi.dnn|multitask'
def rx(p,t):return bool(re.search(p,t,re.I))
def metadata(r,enrich):
    f=enrich.get(r['record_id'],{});a=r['abstract'].strip()
    is_full=bool(a) and r['database']=='ACM'
    if not is_full and f.get('abstract'):a=f['abstract'];is_full=True
    return f,a,is_full
def recommend(r,enrich):
    f,a,full=metadata(r,enrich); t=r['title'];s=t+' '+a
    venue=r['venue'] or f.get('venue','');typ=r['entry_type'] or f.get('entry_type','')
    abst='abstract available' if full else 'abstract unavailable'
    source=f.get('source_file',r['source_file']) if f and not r['abstract'].strip() else r['source_file']
    if not full and a:abst+='; search-result snippet only'
    # Explicit secondary publication identity is sufficient for a recommendation.
    if rx(r'\bsurvey\b|\bsystematic (?:literature )?review\b|\ba review\b|\btutorial\b|^poster[: ]|\bextended abstract\b',t) or rx(r'^Abstracts of',venue):
        return 'exclude','EC1','Title/venue explicitly identifies a secondary, poster or abstract-only report; locate full primary version separately.',abst,typ,venue,a,full,source
    if rx(r'\btrain(?:ing)?\b|fine.tun|hyperparameter',t) and not rx(INF,s) and not rx(r'co.?locat|multi.?tenan.*inferen',s):
        return 'exclude','EC2','Title and available metadata describe training/tuning; no separable concurrent inference outcome identified at this preliminary stage.',abst,typ,venue,a,full,source
    if rx(r'\bFPGA|\bNPU|\bTPU|\bCPU|\bDSP|quantum|qubit',t) and not rx(GPU,s):
        return 'exclude','EC5','Named non-GPU platform in title; available metadata does not identify an evaluated GPU-sharing mechanism. Verify before any final exclusion.',abst,typ,venue,a,full,source
    if full and rx(GPU,s) and rx(INF,s) and rx(SHARE,s):
        return 'retain','IC2-IC5 pending','Abstract indicates GPU, inference and a sharing/interference mechanism. Same-device outcomes, publication and configuration require full-text confirmation.',abst,typ,venue,a,full,source
    if full and not rx(GPU,s) and not rx(SHARE,s):
        return 'exclude','EC2','Available abstract describes the named application or algorithm without an identifiable concurrent GPU-inference-sharing evaluation; recommendation requires human validation.',abst,typ,venue,a,full,source
    return 'uncertain','IC1-IC6 pending','Available title/metadata cannot establish all conjunctive criteria. Preserve for abstract/identity or within-device full-text review.',abst,typ,venue,a,full,source
def refresh():
    records=read('records.csv');q=read('screening.csv');votes=read('title_votes.csv');c=Counter(r['reviewer_1_vote'] for r in q);checks=read('fulltext_checks.csv');quality=read('quality.csv')
    p=dict(first_reviewer_records=sum(bool(r['reviewer_1_vote']) for r in q),first_reviewer_fraction=sum(bool(r['reviewer_1_vote']) for r in q)/len(q),exclude_recommendations=c['exclude_recommendation'],retained_or_uncertain=c['retain_or_uncertain'],unreviewed=c[''],source_checked_reports=len(checks),new_outcome_rows=len(read('extraction.csv')),appraised_reports=len({r['report_id'] for r in quality if r['score'] not in ('','not assessed','not_extracted')}),quality_item_rows=len(quality),snowballing_events=len(read('snowballing.csv')),final_decisions='pending',final_included_studies='pending',updated_at_utc=now(),cycle1_new_recommendations=sum(r.get('batch_id','').startswith('C1-') for r in votes))
    (E/'review_progress.json').write_text(json.dumps(p,indent=2)+'\n')
    by={r['record_id']:r for r in records};queue=[]
    for r in q:
        if r['reviewer_1_vote']!='exclude_recommendation':queue.append(dict(record_id=r['record_id'],priority='1' if r['priority']=='high' else '2',title=r['title'],doi=r['doi'],recommendation=r.get('recommendation','retain/uncertain' if r['reviewer_1_vote'] else 'not yet recommended'),abstract_status=r.get('abstract_status','needs assessment'),fulltext_status=r['fulltext_status'],reason=r['reason'],assigned_role='human screening checker',independent_vote='',criterion='',checked_at_utc='',final_decision='pending'))
    # A deterministic stratified sample of exclusions is additional work, never a completed vote.
    excluded=[r for r in q if r['reviewer_1_vote']=='exclude_recommendation'];sample=[]
    groups={}
    for r in excluded:groups.setdefault((r['database'],r['criterion']),[]).append(r)
    for (db,code),g in sorted(groups.items()):
        chosen=sorted(g,key=lambda r:hashlib.sha256(r['record_id'].encode()).hexdigest())[:max(2,(len(g)+9)//10)]
        for r in chosen:sample.append(dict(record_id=r['record_id'],database=db,criterion=code,title=r['title'],first_reason=r['reason'],sampling='SHA256 record-ID ordering, 10% rounded up, minimum 2 per source/criterion (bounded by stratum size)',independent_vote='',checker='',checked_at_utc='',final_decision='pending'))
    csvwrite(E/'human_validation_queue.csv',sorted(queue,key=lambda x:(x['priority'],x['record_id'])))
    csvwrite(E/'exclusion_validation_sample.csv',sample)
    p['human_candidate_records']=len(queue);p['exclusion_sample_records']=len(sample)
    (E/'review_progress.json').write_text(json.dumps(p,indent=2)+'\n')
    paths=[('Screening','screening.csv'),('Records','records.csv'),('Duplicates','duplicates.csv'),('Version checks','possible_versions.csv'),('Source checks','fulltext_checks.csv'),('Quality','quality.csv'),('Extraction','extraction.csv'),('Snowballing','snowballing.csv'),('Shared candidates','shared_candidate_review.csv'),('Import manifest','import_manifest.csv'),('Version audit','version_review_audit.csv'),('Study extraction','study_extraction_form.csv'),('Human validation','human_validation_queue.csv'),('Exclusion sample','exclusion_validation_sample.csv'),('Metadata enrichment','metadata_enrichment.csv')]
    for name,path in [('Report validation','report_validation_queue.csv'),('Full-text criteria','fulltext_criteria.csv')]:
        if (E/path).is_file():paths.append((name,path))
    wb=dict(counts=json.loads((E/'prisma_counts.json').read_text()),progress=p,sheets={name:read(path) for name,path in paths})
    (ROOT/'task2/tracker/workbook_input.json').write_text(json.dumps(wb,ensure_ascii=False)+'\n')
    return p
def validate():
    rec=read('records.csv');q=read('screening.csv');v=read('title_votes.csv');du=read('duplicates.csv');ids={r['record_id'] for r in rec};qi={r['record_id'] for r in q}
    assert len(ids)==len(rec)==2291 and len(qi)==len(q)==2247 and len(du)==44
    assert len({r['record_id'] for r in v})==len(v) and all(r['record_id'] in qi for r in v)
    assert all(r['final_decision']=='pending' for r in v)
    assert len(v)==sum(bool(r['reviewer_1_vote']) for r in q)
    bad=[]
    for r in read('import_manifest.csv'):
        if hashlib.sha256((ROOT/r['source_file']).read_bytes()).hexdigest()!=r['sha256']:bad.append(r['source_file'])
    assert not bad,bad
    for path in ['evidence/imports','task1/submitted_protocol.pdf']:
        import subprocess
        assert not subprocess.check_output(['git','diff','07085c4','--',path]),'Original changed '+path
    result=dict(checked_at_utc=now(),record_rows=len(rec),canonical_queue_rows=len(q),linked_duplicate_rows=len(du),first_recommendations=len(v),raw_manifest_files_verified=len(read('import_manifest.csv')),original_protocol_unchanged=True,original_imports_unchanged=True,all_final_votes_pending=True,checks='PASS: ID uniqueness/references, arithmetic, final-state guard, original hashes')
    (E/'checkpoint_validation.json').write_text(json.dumps(result,indent=2)+'\n');return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--batch',default='C1-01');ap.add_argument('--limit',type=int,default=400);ap.add_argument('--refresh',action='store_true');args=ap.parse_args()
    enrich={r['record_id']:r for r in overlay()}
    if not args.refresh:
        rec={r['record_id']:r for r in read('records.csv')};q=read('screening.csv');v=read('title_votes.csv');done=0
        for r in q:
            if r['reviewer_1_vote'] or done>=args.limit:continue
            rr=rec[r['record_id']];vote,code,reason,abst,typ,venue,a,full,source=recommend(rr,enrich)
            ts=now();fullstatus='not checked this cycle; existing full-text register takes precedence'
            r.update(reviewer_1_vote='exclude_recommendation' if vote=='exclude' else 'retain_or_uncertain',criterion=code,reason=reason,screening_decision='awaiting_human_validation',recommendation=vote,reviewer='Codex-GroupB',date=ts[:10],timestamp_utc=ts,abstract_status=abst,publication_type_checked=typ or 'unknown',venue_checked=venue or 'unknown',fulltext_status=fullstatus,final_decision='pending',batch_id=args.batch,method='conservative rules-assisted preliminary recommendation; not independent human screening',evidence_excerpt=a[:400] if full else rr['title'],doi_metadata=rr['doi'] or enrich.get(rr['record_id'],{}).get('doi','not resolved'))
            fields=list(v[0])
            new={k:'' for k in fields};new.update(record_id=r['record_id'],stage='title_abstract' if full else 'title_metadata',reviewer='Codex-GroupB',date=ts[:10],vote=r['reviewer_1_vote'],criterion=code,reason=reason,source=source,second_vote='',final_decision='pending',recommendation=vote,timestamp_utc=ts,abstract_status=abst,fulltext_status=fullstatus,batch_id=args.batch,method=r['method']);v.append(new);done+=1
        # Extend old rows without changing their original values or inventing dates.
        vf=list(dict.fromkeys(k for r in v for k in r));qf=list(dict.fromkeys(k for r in q for k in r))
        csvwrite(E/'screening.csv',q,qf);csvwrite(E/'title_votes.csv',v,vf)
    print(json.dumps(refresh(),indent=2));print(json.dumps(validate()))
if __name__=='__main__':main()

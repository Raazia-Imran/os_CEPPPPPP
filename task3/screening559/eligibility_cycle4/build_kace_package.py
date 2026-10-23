"""KACE source assessment. Reading PDF stays outside the repository."""
from pathlib import Path
import csv, hashlib, datetime, json

d = Path(__file__).resolve().parent
d.mkdir(exist_ok=True)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
rid, sid, pid = 'R00035', 'S030', 'P033'
url = 'https://www3.cs.stonybrook.edu/~anshul/socc24_kace.pdf'
doi = '10.1145/3698038.3698555'
pdf = Path('/workspace/scratch/18d5426b12a3/private_reading/KACE.pdf')
sha = hashlib.sha256(pdf.read_bytes()).hexdigest()

def write(name, rows):
    with (d/name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

source = {'Record ID':rid, 'Candidate name':'KACE', 'DOI':doi, 'Source URL':url,
          'Source SHA256':sha, 'PDF pages':10, 'Checked UTC':now,
          'Access result':'Author-hosted typeset SoCC 2024 full text downloaded and inspected; first-page DOI/title/authors match'}
write('Source.csv', [source])
checks = [
 ('IC1','English ten-page primary SoCC 2024 conference paper; first page gives venue, authors and exact DOI. Institutional publication record confirms pages 460-469.','PDF p1; Stony Brook institutional publication record'),
 ('IC2','Application-level predictor chooses colocated jobs executed through NVIDIA MPS on one V100. Offline kernel profiling disables MPS; actual colocated execution starts the MPS daemon.','PDF pp3-4, sections 3.1-3.4 and 4'),
 ('IC3','Table 1 labels training and inference modes. Figure 5 separately reports BERT, ViT, Whisper and Wav2Vec2 inference target cases. These separable inference cases establish scope without treating aggregate mixed-mode gains as inference-only effects.','PDF p4 Table 1; p7 Figure 5 and section 5.2.3'),
 ('IC4','Defines normalized sum of colocated throughput relative to an offline oracle and tests inference-target interference under five repeated runs with standard-deviation bars. The metric is pair throughput, not per-request latency.','PDF p4 section 4 Eq. 1; p7 Figure 5'),
 ('IC5','Evaluation uses one 32GB NVIDIA V100; individual inference-target colocations are identifiable in Figure 5, including ViT batch 2 versus BERT batch 2 interference discussion.','PDF p4 setup; p7 section 5.2.3'),
 ('IC6','November 2024 conference publication lies within the submitted 2020-to-search window.','PDF p1; protocol section 6')]
write('Eligibility.csv', [{'Record ID':rid,'Study ID':sid,'Report ID':pid,'Criterion':q,'Final decision':'Met','Evidence':ev,'Anchor':a,'Source URL':url,'Source SHA256':sha,'Checked UTC':now,'Independent human vote':''} for q,ev,a in checks])
qa = [
 ('Q1',2,2,'Explicit goal is selecting a colocated workload to improve normalized throughput while accounting for contention.','PDF pp1-2'),
 ('Q2',2,2,'Offline system/kernel profiling, features, prediction models and online MPS execution are explained; classify as MPS colocation policy, not a new hardware boundary.','PDF pp3-4 sections 3.1-3.4'),
 ('Q3',2,2,'181 feasible pairings, train/test proportions, five runs, standard-deviation bars and oracle normalization are specified. Random seeds are not identified; uncertainty is SD, not confidence intervals.','PDF pp4-7 sections 4-5.2.3'),
 ('Q4',2,2,'V100 32GB, two Xeon Gold 6230 CPUs, 128GB RAM, PyTorch 1.13, CUDA 12.3 and workload modes/batches are stated. Preserve reported software versions without assuming compatibility validation. OS/driver versions are absent.','PDF p4 Table 1 and section 4'),
 ('Q5',1,2,'Oracle and rule policies are defined. Xu et al. is an author-implemented adaptation of a VM-oriented approach with a different original objective, limiting matched-baseline interpretation.','PDF pp4-5 comparison baselines; p7'),
 ('Q6',2,2,'Throughput sum is explicitly defined and normalized against oracle on the same colocations, with five-run averages/SD. Mixed-mode aggregate results must not become inference-only estimates.','PDF p4 Eq. 1; pp6-7 Figures 3-5'),
 ('Q7','N/A',0,'No request latency, tail-latency or SLO benefit is measured. Latency-sensitive motivation is not a measured claim. No p99 or response-time protection is inferred.','PDF pp4-8 evaluation; protocol claim-specific N/A rule'),
 ('Q8',2,2,'Inference-target cases expose candidate-dependent compute/memory contention, with training/inference labels and batch-dependent adverse comparisons.','PDF p7 Figure 5 and section 5.2.3'),
 ('Q9','N/A',0,'KACE selects efficient colocations. It does not claim or demonstrate memory protection, adversarial security, fault containment or bounded latency isolation.','PDF pp3-8 mechanism/evaluation; protocol claim-specific N/A rule'),
 ('Q10',1,2,'Public artifact is cited and features/method are described. Evaluation uses one GPU generation; three/four-job results lack plotted detail and request-latency validation is absent. No independent artifact execution was performed.','PDF p2 artifact note; pp7-8 sections 5.2.5-7')]
write('QA.csv',[{'Record ID':rid,'Study ID':sid,'Report ID':pid,'Criterion':q,'Score':v,'Applicable maximum':m,'Rationale':ev,'Anchor':a,'Source URL':url,'Source SHA256':sha,'Checked UTC':now,'Independent score':''} for q,v,m,ev,a in qa])
context='One V100 32GB; NVIDIA MPS; PyTorch 1.13 and CUDA 12.3 as reported; inference-target colocation discussion in Figure 5.'
outcomes = [
 ('KACE-05','Oracle-normalized throughput sum for unseen GPT2-xl target',92.3,'percent of oracle','Offline-optimal oracle; adapted Xu policy reaches 57.8 percent of oracle','One V100 32GB; GPT2-xl 1.5B unseen autoregressive inference target; output lengths 10, 20 and 214 tokens; training data exclude GPT2-xl.','PDF p8 section 5.2.6','Pair-throughput result for specified unseen inference target, not tokens per second or per-request tail latency. The prose does not give a per-length breakdown or confidence interval.'),
 ('KACE-06','Adapted Xu oracle-normalized throughput sum for unseen GPT2-xl target',57.8,'percent of oracle','KACE reaches 92.3 percent of the same offline oracle','One V100 32GB; same unseen GPT2-xl target experiment in section 5.2.6.','PDF p8 section 5.2.6','Author-implemented baseline, not an independent reproduction of Xu et al. No ratio of these percentages is reported as a new effect.'),
 ('KACE-01','SM busy rate of BERT batch-2 inference candidate',92,'percent','ViT batch-2 target has 29 percent SM busy rate',context+' BERT batch-2 has small memory footprint but high compute demand.','PDF p7 section 5.2.3','Exclusive workload busy-rate diagnostic explaining colocation interference; not a KACE utilization gain or request-latency effect.'),
 ('KACE-02','SM busy rate of ViT batch-2 inference target',29,'percent','BERT batch-2 inference candidate has 92 percent SM busy rate',context+' Identified inference-target case.','PDF p7 section 5.2.3','Source contrasts resource profiles; busy rate is not achieved occupancy, useful-work throughput or a latency percentile.'),
 ('KACE-03','Cases where adapted Xu policy outperforms KACE',6,'cases','21 mixed training/inference target cases in Figure 5',context+' Author reports 7 percent mean and 14 percent maximum advantage in this subset.','PDF p7 section 5.2.3','Adverse mixed-mode contextual result; not six inference-only cases or an overall 7 percent effect. Individual inference-target cases establish eligibility separately.'),
 ('KACE-04','Cases where MEMCAP outperforms KACE',2,'cases','21 mixed training/inference target cases in Figure 5',context+' Author reports 6 percent mean and 7 percent maximum advantage in this subset.','PDF p7 section 5.2.3','Adverse mixed-mode context. Do not generalize to all inference workloads or compare unnormalized batch-throughput sums across papers.')]
write('Outcomes.csv',[dict(zip(['Record ID','Study ID','Report ID','Outcome ID','Metric','Value','Unit','Baseline','Context','Anchor','Interpretation limit'],[rid,sid,pid,*x])) for x in outcomes])
ref={'Record ID':rid,'Study ID':sid,'Report ID':pid,'Authors':'Bing-Shiun Han and Tathagata Paul and Zhenhua Liu and Anshul Gandhi','Title':'KACE: Kernel-Aware Colocation for Efficient GPU Spatial Sharing','Venue':'Proceedings of the 2024 ACM Symposium on Cloud Computing','Year':2024,'Pages':'460-469','DOI':doi,'Primary URL':url,'Primary SHA256':sha,'Version':'Author-hosted typeset ten-page final conference text with matching DOI','Date basis':'SoCC November 20-22, 2024; first page and institutional publication metadata'}
write('Reference.csv',[ref])
(d/'Synthesis.md').write_text('''# KACE source assessment

Include as S030/P033. KACE chooses MPS colocations using offline kernel and system metrics. Figure 5 and section 5.2.3 separately identify inference targets, meeting the narrow inference requirement. The model training in the predictor must not be confused with the application workloads, which include both training and inference.

Choose this policy family when throughput-oriented colocation is the objective and offline profiling is feasible. Memory footprint or GPU busy rate alone can select a poor inference partner. The ViT batch-2 case explains how compute-intensive BERT batch-2 inference can interfere despite its small memory footprint. No latency target, tail guarantee, security or fault boundary is established.

The reported averages over all 21 target cases mix training and inference. They are contextual observations, not inference-only treatment effects. KACE is not uniformly best: the adapted Xu and MEMCAP policies win six and two cases respectively. Preserve those adverse cases. No figure values were digitized or reconstructed. Three/four-job results are reported without underlying plots. A single V100 platform and missing OS/driver details limit transfer.

QA is 14/16 applicable points. Q7 and Q9 are reasoned N/A because the paper makes no corresponding measured latency/isolation claim. No independent reproduction or reviewer vote is asserted.
''')
assert sum(v for _,v,_,_,_ in qa if isinstance(v,int)) == 14
(d/'Validation.json').write_text(json.dumps({'record':rid,'study':sid,'report':pid,'criteria_met':6,'QA_items':10,'QA_score':14,'QA_maximum':16,'outcomes':len(outcomes),'source_sha256':sha,'PDF_redistributed':False},indent=2)+'\n')
print('KACE: six criteria met; QA 14/16; six observations with explicit scope limits.')

# Evidence-Grounded Opportunity Clustering — Research Plan v0.1

Status: proposed, **not empirically validated**. Scope: Opportunity Discovery and Exploration only.

## Research question
Does an evidence-aware, problem-centric relationship model recover meaningful user needs more accurately than conventional text/topic clustering, while retaining source traceability and uncertainty?

## Units and relation types
- Raw signal: source URL, precise locator, observed/event date, provenance class, quoted claim, review state.
- Problem instance: user segment, job-to-be-done, context, friction, current workaround, outcome.
- Product: product ID, positioning, mechanism, publicly documented alternatives.
- Relation labels: SAME_PROBLEM, RELATED_PROBLEM, SOLUTION_FOR, ALTERNATIVE_TO, CONTRADICTS, INSUFFICIENT_EVIDENCE.
- Do not infer that common domain/topic means the same user problem.
- Provisional observations are not promoted to approved facts.

## Baselines to run before inventing a new algorithm
B0: lexical TF-IDF cosine + agglomerative grouping.
B1: multilingual sentence embeddings cosine + threshold grouping.
B2: embeddings + HDBSCAN; report outlier fraction.
B3: BERTopic for topic discovery; evaluate whether its topics really correspond to jobs-to-be-done.
B4: pairwise problem extraction + explicit same-problem classifier; no graph constraints.
B5 (candidate): combine semantic similarity, job-to-be-done equivalence, user/context compatibility and typed provenance-aware graph edges. A hard contradiction in user/task identity may prohibit same-problem merging even when similarity is high.

## Falsifiable hypotheses
H1: B5 improves SAME_PROBLEM pairwise F1 against B1 by a preregistered margin.
H2: B5 lowers false-merges for superficially related but operationally distinct problems.
H3: B5 improves source-traceable opportunity retrieval precision@5 without materially reducing recall@20.
H4: Removing job/context features worsens SAME_PROBLEM performance (ablation).
H5: Source type weighting reduces apparent corroboration from multiple copies of the same promotional claim.

If hypotheses fail, prefer the simpler baseline.

## Gold dataset and split
- Start with 100–200 independently labeled pairs covering same problem, related-but-distinct, different problem, and ambiguous.
- Two reviewers blinded to algorithm results; adjudicate disagreements; track inter-annotator agreement.
- Group train/test by source thread and product, and add an explicit future time split to reduce leakage.
- Dedupe syndication and copied content before counting independently sourced observations.
- Include Chinese/English paraphrases, hard negatives, low-data needs and adversarial near-misses.

## Metrics
Pairwise precision/recall/F1 for SAME_PROBLEM; false-merge rate on hard negatives; Adjusted Rand Index and NMI for clustered labels when ground truth exists; retrieval precision@5 / recall@20; abstention/noise rate; citation traceability; contradiction retrieval coverage; stability under bootstrap/subsampling.

Do not optimize only silhouette score: geometric cluster cohesion does not establish product usefulness. Avoid reporting a single aggregate accuracy as a measure of startup viability.

## Experiment order
1. Freeze annotation guidance and small gold dataset; establish split rules.
2. Run B0/B1 with simple transparent thresholds; archive predictions and error cases.
3. Run B2/B3, observe outliers and cross-language issues.
4. Implement B4/B5 only if baseline errors justify additional complexity.
5. Perform feature ablations, bootstrap intervals, source robustness tests and blinded qualitative review.
6. Link useful clusters to Opportunity Explorer. Show source citations and unknowns, never a synthetic market-demand confidence score.

## Literature and reference implementations
- Sentence Transformers: https://www.sbert.net/docs/quickstart.html
- Sentence Transformers community detection: https://www.sbert.net/docs/package_reference/util/retrieval.html
- BERTopic: https://bertopic.readthedocs.io/en/latest/
- HDBSCAN: https://hdbscan.readthedocs.io/en/latest/
- scikit-learn clustering evaluation: https://scikit-learn.org/stable/modules/clustering.html

These references establish mature components, not empirical validation of B5 on this task.

# Roadmap — From Research Archive to Developer Toolkit

Status: hypothesis-driven; ordering matters more than fixed deadlines. No tools in this plan are claimed as implemented.

## Phase 0 — Foundations (now)
**Outputs:** README, public research policy, VISION.md, ROADMAP.md, schemas, report and insight conventions.
**Acceptance:** public files have citations/provenance fields, stable IDs, and pass schema validation; no confidential content.

## Phase 1 — Reliable evidence base
**Build:** normalize products, user needs, source claims, VC funding signals and dated observations. Create a small, hand-audited seed set. Deduplicate by canonical URL and stable IDs. Record both confirming and contradicting evidence.
**Acceptance:** 20 independently verified product profiles; 30 evidence records; 10 user-need hypotheses spanning at least three categories. Sample audit: all factual assertions linked to inspectable sources; unknowns left unknown.
**Stop/go:** if citation quality or legal reuse is inadequate, narrow source scope.

## Phase 2 — Useful discovery/search
**Build:** minimal static site or CLI over versioned JSON/Markdown. Filter by target user, job-to-be-done, sector, first seen date, evidence strength and funding/bootstrapped status. Link every result to evidence.
**Acceptance:** an automated suite of at least 20 documented search tasks returns source-linked relevant results, with measured precision and failure cases.

## Phase 3 — User Pain Explorer (first analysis tool)
**Build:** user segment/task input → candidate need clusters → cited examples, workarounds, competitive alternatives, counterevidence, unknowns and falsifiable tests. Use retrieval with citations and a deterministic evidence ledger before introducing optional LLM synthesis.
**Acceptance:** a versioned benchmark of at least 20 hypotheses checks attribution, relevant opposing evidence, alternative products, reproducibility and falsifiable next steps. Record disagreement and failures rather than hiding them.
**Decision:** if the tool produces generic suggestions without supporting evidence, improve the dataset rather than add more agent complexity.

## Phase 4 — Idea Validation workspace
**Build:** input an idea, identify riskiest assumptions, compare alternatives, design 1–2-week experiments, maintain outcomes and revised beliefs. Do not confuse hypothetical plans with actual customer interviews.
**Acceptance:** the engine produces reproducible test plans and executes automated evidence-based checks and clearly labeled scenario/sensitivity tests; real demand remains unverified unless supported by independent observations.

## Phase 5 — Community contributions and longitudinal research
**Build:** contributor guide, source submissions, dispute resolution, provenance checks, stable versions and retrospective prediction review.
**Acceptance:** evidence contributions reviewed against written criteria; reversals or corrections are traceable.

## Engineering sequence
1. Define schema and validation rules.
2. Extract structured records from existing public research.
3. Write a deterministic local validator and CI check.
4. Prototype a read-only browse/search UX.
5. Add evidence-grounded analysis.
6. Add contribution/experiment workflows only after direct user feedback.

## Risks & mitigations
- Survivorship/funding bias → sample bootstrapped, failed and low-visibility products.
- LLM hallucination → cite specific observation IDs and show unknowns.
- Scraping and rights → prioritize permitted public APIs, original links and short paraphrases.
- Data staleness → store observed_at and review_by; never present old snapshots as current.
- Scope creep → one useful workflow before building an all-purpose agent suite.

## First two-week experiment (proposed)
Create a reproducible benchmark with ten varied startup hypotheses (including promising, weak, and deliberately unsupported examples). For each, specify reference evidence, market alternatives, likely counterexamples, testable assumptions and expected uncertainty. Run the tool against these cases and log citation accuracy, false-confidence errors, retrieval gaps and consistency across repeated runs. No participant recruitment is required.

## Automated Startup Hypothesis Testing Lab
Modules in order: (1) evidence retrieval and provenance checks; (2) competitor coverage and differentiation test; (3) counterevidence / contradiction audit; (4) cost, pricing and acquisition sensitivity scenarios; (5) hypothesis-level experiment planner. A report must distinguish verified, claimed, inferred and unknown outcomes. Never equate synthetic personas or model-generated opinions with genuine user feedback.

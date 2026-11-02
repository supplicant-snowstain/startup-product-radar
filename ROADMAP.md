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
**Acceptance:** five external testers can locate and compare relevant products and state why at least one result matters. Collect task completion time and qualitative feedback.

## Phase 3 — User Pain Explorer (first analysis tool)
**Build:** user segment/task input → candidate need clusters → cited examples, workarounds, competitive alternatives, counterevidence, unknowns and falsifiable tests. Use retrieval with citations and a deterministic evidence ledger before introducing optional LLM synthesis.
**Acceptance:** 5–10 independent builders attempt a real idea-discovery task; at least 4 find a plausible pain worth investigating, can retrieve its sources, and identify a concrete next validation action. Record disagreement and failures rather than hiding them.
**Decision:** if the tool produces generic suggestions without supporting evidence, improve the dataset rather than add more agent complexity.

## Phase 4 — Idea Validation workspace
**Build:** input an idea, identify riskiest assumptions, compare alternatives, design 1–2-week experiments, maintain outcomes and revised beliefs. Do not confuse hypothetical plans with actual customer interviews.
**Acceptance:** at least three documented experiments conducted by consenting external builders; record observed outcomes, including rejected ideas.

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
Interview five independent builders about the last idea they evaluated. Ask for the evidence they searched, abandoned alternatives and time spent. Present a manually curated example of User Pain Explorer and have them complete the same task. Capture whether it changes their next action. This is a research plan, not a claim that interviews occurred.

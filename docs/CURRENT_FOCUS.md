# Current Product Focus: Discover → Explore

Status: active scope decision (2026-11-03).

## Mission
Help independent builders discover real-world unmet needs and explore why those opportunities may exist. Support original thinking rather than outputting confident startup success predictions.

## Stage 1: Opportunity Discovery (in scope now)
User input: broad interest, user segment, task, geography or no prompt (browse).

Output: sourced opportunity cards with user segment, job-to-be-done, repeated pain signal, products addressing it, current alternatives, recency, evidence links, conflicting observations and unanswered questions.

Minimum experience: browse by domain; search a specific need; inspect original sources; save a shortlist. No fabricated market statistics and no declaring PMF.

Acceptance: deterministic reference set of 20 needs with annotated evidence links; ability to locate relevant needs and trace each factual statement to an observation. Measure query precision@5, source traceability, duplicates, stale evidence and unsupported assertions. Benchmarks should include negative and low-evidence cases.

## Stage 2: Opportunity Exploration (in scope now)
User input: a selected need or product family.

Output: comparative map of user groups, substitutes, product mechanisms, adoption signals, business models, competitive boundaries, credible counterexamples, hidden assumptions, related unmet jobs and research questions.

Minimum experience: select a need → compare 3–5 relevant products when evidence permits → inspect claim-level citations → see conflicts and unknowns → export an evidence-backed exploration brief.

Acceptance: a small time-bounded reference corpus with sourced expected comparisons; metrics include competitor relevance, coverage of known alternatives, counterevidence recall, temporal leakage, and unsupported assertion rate. A useful brief may conclude "insufficient evidence."

## Deferred (not discarded)
Stage 3: Idea Evaluation — assesses a builder's concrete product proposal and its risks.
Stage 4: Hypothesis Testing — constructs experiments and sensitivity tests; no fake user demand.
Keep existing evaluator code as a supporting utility, not the primary product workflow. No new work on complex agent orchestration until Stage 1–2 have a usable end-to-end path.

## Implementation order
1. Define source-to-need relations and curated need records, retaining exact citations.
2. Produce an initial small corpus from publicly available daily research and explicit review; do not auto-approve extraction.
3. Build a read-only discovery CLI/API with filters and evidence-linked output.
4. Build need-to-product exploration comparisons.
5. Make a simple browsable interface only after end-to-end evidence navigation works.
6. Compare with a baseline keyword search and record limitations.

## Data quality safeguards
Public independent research only; no privileged employer information or employer-specific work recommendations. VC funding is a lead, not evidence of demand. Do not conflate promotional claims with independent user observations. Store timestamps and negative evidence. Unknown is a legitimate output.

## Out-of-scope for now
User recruitment experiments, automated startup investment ratings, synthetic user personas as demand evidence, market size prediction, autonomous pivot recommendations or overbuilt multi-agent infrastructure.

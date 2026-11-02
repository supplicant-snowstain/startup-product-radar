# Vision — Startup Product Radar

Status: exploratory product thesis (2026-11-03). Not a claim of product-market fit.

## One-line mission
An open-source, evidence-driven startup discovery and validation toolkit for independent builders.

## Why
Independent developers often see new products and funding news but struggle to understand which **real user problems** are underserved, how to distinguish adoption evidence from hype, and which assumptions to test before building.

## Intended users
1. **Explorers:** independent developers without a defined idea, looking for recurring user pains and novel product patterns.
2. **Validators:** builders with an idea, seeking alternatives, evidence, counterarguments and an actionable low-cost validation plan.

## Value proposition
Move from product discovery to evidence-backed decisions:
**Observe → Structure evidence → Synthesize cross-product needs → Form hypotheses → Design experiments → Reassess**.

## Product principles
- User needs and behavior first; AI is not a criterion for inclusion.
- Sources, timestamps and limitations are visible; marketing or VC investment is not verified demand.
- Clearly separate fact, first-party claims, inference and unknowns.
- Surface competing explanations and counterexamples, including failures and unfunded products.
- Assist human judgment rather than output an authoritative idea score.
- Small, useful tools before building an agent platform or social network.
- Public-only independent research; no privileged workplace material, private data or credentials.
- Preserve provenance and respect source licenses, robots rules and rate limits.

## Candidate experiences (not yet implemented)
**Discover:** Browse newly observed products, the user jobs they address and verified change histories.
**Understand:** Compare product mechanics and discover repeated needs across unrelated categories.
**Evaluate:** Enter an idea and receive competitors, evidence, assumptions and falsifiable questions.
**Validate:** Turn the highest-risk assumption into a 1–2-week customer-discovery or MVP experiment.

## First wedge: User Pain Explorer
Input: a user segment, task or category (e.g., independent consultants managing invoices).
Output: dated, sourced problem statements, workarounds, representative examples, existing alternatives, missing evidence and 2–3 testable hypotheses.
Success is measured by whether real builders discover relevant, previously unrecognized pains and can run a sensible validation test—not by the quantity of generated ideas.

## Explicit non-goals for the first release
No autonomous startup investment advice, no definitive market-size estimates from scraped mentions, no guaranteed PMF scores, no paywalled scraping, no automatic claims of user interviews, and no employer-specific consulting.

## Open questions
- Which evidence is both legally reusable and representative enough for publication?
- Do developers value discovering pains, assessing their own ideas or preparing interviews most?
- Can analysis cite opposing evidence instead of producing persuasive but weak narratives?
- Can a lightweight, file-based evidence store stay trustworthy as records accumulate?

## Decision gates
Advance from curated knowledge base to a working tool only after observing users complete real discovery or validation tasks. Each gate and its outcome should be recorded in ROADMAP.md and the evidence ledger.

# Opportunity Explorer — first usable release checklist

## Target user journey
A solo builder who has no specific idea can browse recent publicly observed problems by domain, open a need, inspect original reports and products, and leave with one or two clearly phrased *questions worth investigating*. The product does not score startup success.

## P0 deliverables, in order
1. **Data availability:** publish 10–20 distinct, attributed public problem signals from multiple domains, each including precise original URL, observation date, source type, limits, and review status. Only promote to approved evidence after review.
2. **Discover view:** simple category and keyword filters; cards show user, problem, source count and recency. Empty and ambiguous results are explicit.
3. **Explore view:** a selected problem exposes primary quotations/links, adjacent products or substitutes, possible workarounds, conflicting reports, and outstanding questions. If none are known, show unknown, not generic AI synthesis.
4. **Read-only demo:** a minimal web or static browsing interface hosted from repository data, without external API keys or cloud infrastructure.
5. **Regression suite:** sample navigation paths for three domains, missing/duplicate evidence, citations and abstention. Record bugs before considering embedding search.

## Acceptance criteria
- A fresh visitor can go from homepage to a source-backed problem in no more than three navigation steps.
- Each factual claim has a resolvable original source or is clearly marked hypothesis; no synthetic test fixtures in public market data.
- No opportunity is labeled validated solely on founder marketing, funding or product launch.
- At least 10 distinct sourced signals and 3 exploratory groupings exist before declaring the first dataset release; no invented count or live date.
- The interface visibly separates sourced observation, interpretation and unknown.
- CI must pass on the actual commit and navigation be manually smoke-tested before declaring the release ready.

## Explicit non-goals
Custom clustering algorithms, learned opportunity scores, success forecasting, user recruitment, multi-agent orchestration, speculative market sizing and ranking founders. Existing research plan is deferred.

## Current limitation
Initial provisional signals are only a seed. The repository does not yet meet the above release criteria.

# 2026-11-22 — Context contamination and local control

Source: https://www.producthunt.com/leaderboard/daily/2026/11/21

AI Context Flow offers shared memory and rollback; its maker says conflict notifications are still being developed (https://www.producthunt.com/products/ai-context-flow). Glassmail limits agent mail operations and uses on-device AI (https://www.producthunt.com/products/glassmail). Codemany claims per-job sandboxing to isolate self-hosted CI (https://www.producthunt.com/products/codemany). These are public product claims, not independently measured outcomes.

**Hypothesis:** independent developers using multiple agents need a local memory-contamination audit. MVP: Python/SQLite synthetic scenarios and an HTML report; interview 8 developers, trial with 5; pass if 3 complete and 2 repeat use in 7 days, fail if fewer than 2 repeat or existing logs suffice. Avoid real confidential data. No proof of willingness to pay, retention or PMF.

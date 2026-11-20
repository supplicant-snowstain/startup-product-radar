# Cross-Client Promise Check — 2026-11-20

Evidence: https://www.producthunt.com/products/stripo-email ; https://www.producthunt.com/products/testsprite ; https://www.producthunt.com/products/manufact .

Hypothesis (not validated): solo developers need a compact, reproducible cross-client behavior comparison rather than another general-purpose agent.

MVP: Python + Playwright + YAML; 3 browsers; public demo pages only; static HTML screenshots, expected vs observed, fallback checks. Week 1: interview 8; week 2: recruit 5 tests. Success: 3 real completions, 2 repeat within 7 days, 2 specific integration or payment intents, median debugging time 25% lower. Failure: fewer than 2 repeats or existing tools solve it adequately. Avoid collecting production credentials.

Counterevidence: existing Playwright tests may be sufficient; email clients differ from browsers; vendor claims are not verified demand.

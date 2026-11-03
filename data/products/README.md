# Public product observations

Add one reviewed or provisional public product per JSON file. Required: id, name, description, category, source_url, source_type, observed_at, date_precision, verification_status.

Dates: **observed_at is the date the research team observed the product**, never automatically its launch date. Only set launch_date if independently sourced; date_precision may be day, month or unknown.

Optional: website, differentiator, problem_ids, limitations. Never infer user demand from a launch announcement. Product-to-need links must point to existing need IDs and be explicitly justified. Founder or vendor claims must remain attributed.

Generate `web/products.json` with `PYTHONPATH=tools/startup_lab python -m startup_lab.product_feed`. Empty state is expected until real sources are checked and product records added.

## Optional human-readable story

A product may include `story.en`, `story.zh`, and `story.fr` with five fields: `who`, `pain`, `solution`, `benefit`, `uncertainty`. The story must not invent a founder's personal motivation or attribute imagined quotations to customers. Frame unproven benefits as possibilities. If a story is missing, the web page states that the origin is not yet known instead of inventing one.

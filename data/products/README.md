# Public product observations

Add one reviewed or provisional public product per JSON file. Required: id, name, description, category, source_url, source_type, observed_at, date_precision, verification_status.

Dates: **observed_at is the date the research team observed the product**, never automatically its launch date. Only set launch_date if independently sourced; date_precision may be day, month or unknown.

Optional: website, differentiator, problem_ids, limitations. Never infer user demand from a launch announcement. Product-to-need links must point to existing need IDs and be explicitly justified. Founder or vendor claims must remain attributed.

Generate `web/products.json` with `PYTHONPATH=tools/startup_lab python -m startup_lab.product_feed`. Empty state is expected until real sources are checked and product records added.

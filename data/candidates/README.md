# Candidate evidence queue

Daily research outputs can propose **candidate** records, but they are not automatically trusted. A reviewer checks the original public source and supplies a precise source locator, review date, limitations and an explicit approval.

Only explicitly reviewed candidates may be promoted into data/evidence/. Do not invent a reviewer or mark source_checked automatically.

Candidate required fields: statement, source_url, source_locator, observed_at, limitations, evidence_type, direction, dimension, review_status, source_checked, reviewed_by. Optional: product_id, source_published_at, event_date, confidence, reviewed_at.

Run from repository root:

```bash
PYTHONPATH=tools/startup_lab python -m startup_lab promote path/to/candidate.json
```

Promotion produces data/evidence/ev-<hash>.json. It never verifies web content itself; source_checked reflects the curator's externally completed review. Retain the source URL and locator. Synthetic sample URLs are not publishable.

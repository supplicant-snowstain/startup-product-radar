# Repository integration v0.2

The offline adapter reads index/products.csv and validated-curator candidate files from data/evidence/*.json. It makes no network calls, does not scrape third-party websites and does not pretend Markdown narratives are structured evidence.

Example programmatic usage:

```python
from startup_lab.repository import audit_repository,idea_from_repository
print(audit_repository("."))
print(idea_from_repository(".", "idea.json"))
```

idea.json has an id and evidence_ids array referencing records in data/evidence/. Missing evidence IDs cause an invalid-input result; an empty evidence directory is explicitly reported as awaiting verified evidence.

Integration next steps: explicit extraction and review of source-backed claims from reports, canonical product matching, verified fetch timestamps, retrieval ranking and automatic contradiction discovery.

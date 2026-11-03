# Product research staging

Candidate records generated from public discoveries are **not** published automatically. A curator must inspect original sources, confirm claims, check duplicates beyond URL matching, and only then create a `data/products/*.json` record. Launch dates require a precise dated source. No credentials or private information.

Run: `PYTHONPATH=tools/startup_lab python -m startup_lab.product_candidates incoming.json --root .`. Input is a JSON array of objects with `name`, `source_url`, `observed_at`, and optional `description`/`source_type`. URL deduplication is a conservative first pass, not entity-level deduplication.

## Automated checks

On each change to the staging directory, GitHub Actions runs the `Validate Daily Product Candidates` workflow. It checks each candidate's ID against the canonical source URL, requires a pending/unverified state, validates observation dates, and detects duplicate canonical source URLs. This workflow does not open original web pages, verify launch claims, or authorize publication. Run locally:

```bash
PYTHONPATH=tools/startup_lab python -m startup_lab.validate_candidates --root .
```

The daily automation instructions have been updated to **attempt** writing candidate records, but no successful automated GitHub archive has been verified. GitHub Actions success only proves local schema checks, not independent research accuracy.

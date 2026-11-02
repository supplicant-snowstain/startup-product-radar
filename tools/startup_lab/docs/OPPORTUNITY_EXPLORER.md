# Opportunity Explorer v0.6

The first end-to-end **data navigation** slice covers two active product stages:

- Discovery: search and browse needs linked to source-backed evidence and products.
- Exploration: select a need to see supporting/opposing/context observations, related products, missing links and uncertainty.

Commands (from repository root):

```bash
PYTHONPATH=tools/startup_lab python -m startup_lab discover "invoice" --root .
PYTHONPATH=tools/startup_lab python -m startup_lab discover --root .
PYTHONPATH=tools/startup_lab python -m startup_lab explore need-001 --root .
```

Canonical records live in `data/needs/*.json` (schema: `schema/need.schema.json`), `data/evidence/*.json` and `index/products.csv`. Use stable IDs and source citations; needs cannot manufacture or auto-approve evidence. Missing references are shown as warnings rather than silently discarded.

Current limitations: keyword-only discovery; no market-wide crawling, no automatic demand ranking or actual proof that a customer pain is unmet. Empty output is expected until curated, reviewed need and evidence records are added. Test fixtures are synthetic.

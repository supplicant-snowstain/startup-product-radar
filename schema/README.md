# Data contracts (draft v0.1)

JSON Schemas describe canonical research records. Markdown reports are human-readable views, not a substitute for provenance. Objects may be stored in data/ as JSON with stable IDs. These schemas do not imply an operational ingestion pipeline.

- product.schema.json: product identity, stage and verification timestamps
- evidence.schema.json: dated assertion, source, evidence type, confidence and limitations
- insight.schema.json: cross-product need hypothesis with supporting and contradicting evidence IDs
- experiment.schema.json: proposal or real experiment, outcomes and evidence

Core relations:
Product → Evidence IDs; Insight → Product IDs + Evidence IDs; Experiment → Insight ID.
Use ISO dates, stable slug-like IDs, canonical URLs, and explicit null/unknown values. Claims about adoption, revenue or retention require independent evidence.

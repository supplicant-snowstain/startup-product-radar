# Relationship evidence contract (v1)

A relationship is **not** created merely because two products share keywords, a date, or a category. The global graph currently shows co-observation, which is a research-index association only.

For future editorially reviewed relationships, use `data/relationships.json`:

```json
{
  "schema_version": 1,
  "relationships": [
    {
      "id": "unique-stable-id",
      "from": "product-slug-a",
      "to": "product-slug-b",
      "type": "alternative_to",
      "assertion": {"en": "Documented comparison", "zh": "有来源的比较", "fr": "Comparaison documentée"},
      "source_url": "https://example.org/source",
      "evidence_kind": "independent_comparison",
      "review_status": "approved",
      "reviewed_at": "YYYY-MM-DD"
    }
  ]
}
```

Allowed relation types: `alternative_to`, `same_audience`, `same_problem`, `shared_maker`, `integrates_with`. Allowed evidence kinds: `first_party_claim`, `independent_comparison`, `direct_user_report`, `primary_documentation`. Only `review_status: approved` can be shown as an asserted cross-product link; this is an editorial gate, not proof of commercial success. All endpoints must resolve to products already in the public research feed. Never use observation dates as launch dates, and never invent a maker, user segment, relation, or source URL.

The public UI must display the original source, relationship type, and evidence kind. Unknown or provisional relationships are omitted. This data contract is intentionally independent of a visualization library.

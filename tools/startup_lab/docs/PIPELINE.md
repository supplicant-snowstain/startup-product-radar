# Evidence pipeline v0.3

1. **Discover**: daily report records product and candidate insights with original links.
2. **Propose**: optional structured JSON in data/candidates/; records default to pending.
3. **Review**: source inspection by a curator, distinguish official announcements, investor claims, first-hand users and independent sources. Record exact locator, date, limitations and reviewer.
4. **Promote**: deterministic validator creates one immutable identity per source/locator/statement under data/evidence/.
5. **Audit**: offline evaluator checks missing citations, competing evidence, duplicates and incomplete inputs.
6. **Revisit**: contradictory new observations are new records, not replacements of history.

The pipeline intentionally does not claim to scrape, fetch, verify links, perform human review or establish product-market fit automatically. Never automatically set review_status=approved or source_checked=true from an LLM response. Real records remain absent until verified and committed.

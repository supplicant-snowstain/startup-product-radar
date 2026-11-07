# Public social-source discovery policy

Goal: discover **product-level public evidence**, not track private individuals.

## Source priority
1. Product website links to an official X account, GitHub, Product Hunt, founder blog, or announcement.
2. Public product launch posts and original announcements, with permalinks and observation timestamps.
3. Independent user discussions, preserving context and separating praise, criticism and unresolved questions.
4. Optional Sherlock username lookup for **public brands or explicitly public professional handles only**, after direct-source discovery fails.

## Sherlock is a candidate generator, not identity verification
A matching username does not establish account ownership. Never automatically connect a candidate handle to a maker, founder or product. Require an official cross-link, a verifiable primary-source statement, or manual review with documented corroboration. Respect X and other services' terms, rate limits, access controls and robots rules. Do not attempt to bypass login, access private posts, enumerate personal accounts in bulk or store unrelated personal profiles.

## Suggested candidate record
```json
{
  "product_slug": "example",
  "platform": "x",
  "profile_url": "https://x.com/example",
  "discovery_method": "official_website_link",
  "identity_status": "candidate",
  "identity_evidence_url": "https://example.com",
  "observed_at": "YYYY-MM-DD",
  "review_status": "pending_review"
}
```
Statuses: candidate → verified / rejected; review is required before public graph inclusion. A verified brand profile is distinct from a verified founder identity. Product claims, founder claims and independent user evidence remain separate.

## Recommended rollout
First implement official-site X links and source permalinks. Then add public launch/discussion references and editorial review. Only consider an opt-in Sherlock enrichment job if repeated missing-handle cases justify its operational cost. Do not run Sherlock in the browser or in a default daily bulk crawl.

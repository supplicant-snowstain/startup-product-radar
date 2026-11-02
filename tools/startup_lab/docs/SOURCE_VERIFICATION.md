# Source Verification v0.5 (safe prototype)

This module validates candidate URL syntax and DNS addresses, checks a quoted excerpt against **provided HTML snapshots**, and records uncertainty. It does not yet fetch live websites.

Why remote fetch is disabled: standard Python URL opening re-resolves DNS after validation and may reach private network addresses, so pre-fetch checks alone do not prevent SSRF/DNS rebinding. A production fetcher must use a pinned-IP connection, block redirects or revalidate each hop, enforce content-size limits and timeouts, and comply with site terms and robots policies.

Usage:

```python
from startup_lab.source_verify import match_snapshot,verify_source
result = match_snapshot('<p>Example public text ...</p>', 'Example public text')
```

A text match confirms only presence of exact wording in supplied content. It does not establish the claim as true, independent, representative or current. All approved entries still require a curator's explicit review. No internal/private sources are permitted.

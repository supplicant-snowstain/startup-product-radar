# Evidence Retrieval v0.4

This module retrieves **previously curated JSON evidence**, not arbitrary assertions from raw Markdown. Searches are local lexical overlap, including Chinese two-character terms. Relevance is not learned or independently verified.

From repository root:

```bash
PYTHONPATH=tools/startup_lab python -m startup_lab search "invoice workflow" --root .
PYTHONPATH=tools/startup_lab python -m startup_lab sides "invoice workflow" --root .
PYTHONPATH=tools/startup_lab python -m startup_lab candidates reports/YYYY/MM/YYYY-MM-DD.md
```

The candidates command discovers Markdown hyperlinks for curator review; it never invents claims or approves sources. To promote one, manually provide a bounded statement, date, evidence type, exact source locator and reviewer details, then run the existing promote command.

The sides command lists records tagged support or contradict; it does not prove actual logical contradiction. The system never concludes there is no market demand because no matching evidence was found. If the repository lacks curated JSON evidence, results are empty by design.

## Next engineering checks
- Robust claim-level source resolution and document snapshots with permission awareness
- Duplicate detection at canonical URL and claim level
- Source freshness and revalidation scheduling
- Measured precision/recall on a genuinely annotated, rights-compliant dataset
- Explicit uncertainty and adversarial evaluation

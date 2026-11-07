#!/usr/bin/env python3
"""Validate reviewed product relations before publication. Standard library only."""
import argparse
import json
import pathlib
import sys
from urllib.parse import urlparse

TYPES = {"alternative_to", "same_audience", "same_problem", "shared_maker", "integrates_with"}
KINDS = {"first_party_claim", "independent_comparison", "direct_user_report", "primary_documentation"}
STATUSES = {"draft", "pending_review", "approved", "rejected"}

def validate(data, known):
    errors = []
    if data.get("schema_version") != 1 or not isinstance(data.get("relationships"), list):
        return ["expected schema_version=1 and relationships array"]
    ids = set()
    for i, r in enumerate(data["relationships"]):
        prefix = f"relationships[{i}]"
        if not isinstance(r, dict):
            errors.append(f"{prefix}: must be object")
            continue
        rid = r.get("id")
        if not isinstance(rid, str) or not rid.strip() or rid in ids:
            errors.append(f"{prefix}: missing or duplicate id")
        else:
            ids.add(rid)
        status = r.get("review_status")
        if status not in STATUSES:
            errors.append(f"{prefix}: invalid review_status")
        if r.get("type") not in TYPES:
            errors.append(f"{prefix}: invalid relation type")
        if r.get("from") == r.get("to") or r.get("from") not in known or r.get("to") not in known:
            errors.append(f"{prefix}: endpoints must be distinct known product slugs")
        if status == "approved":
            url = r.get("source_url")
            if not isinstance(url, str) or urlparse(url).scheme != "https" or not urlparse(url).netloc:
                errors.append(f"{prefix}: approved relationship requires https source_url")
            if r.get("evidence_kind") not in KINDS:
                errors.append(f"{prefix}: approved relationship requires valid evidence_kind")
            assertion = r.get("assertion")
            if not isinstance(assertion, dict) or not isinstance(assertion.get("en"), str) or not assertion["en"].strip():
                errors.append(f"{prefix}: approved relationship requires an English assertion")
            if not isinstance(r.get("reviewed_at"), str) or len(r["reviewed_at"]) != 10:
                errors.append(f"{prefix}: approved relationship requires YYYY-MM-DD reviewed_at")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--relations", default="data/relationships.json")
    parser.add_argument("--research", default="web/research.json")
    parser.add_argument("--output", default="web/relationships.json")
    args = parser.parse_args()
    relations = json.loads(pathlib.Path(args.relations).read_text(encoding="utf-8"))
    feed = json.loads(pathlib.Path(args.research).read_text(encoding="utf-8"))
    known = {p["slug"] for report in feed.get("reports", []) for p in report.get("products", []) if isinstance(p.get("slug"), str)}
    errors = validate(relations, known)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    approved = [r for r in relations["relationships"] if r["review_status"] == "approved"]
    payload = {"schema_version": 1, "relationships": approved}
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Validated {len(relations['relationships'])} relationships; published {len(approved)} approved.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

"""Validate a Review Studio export and prepare a human-reviewed intelligence update.

This CLI never pushes to GitHub, opens PRs, or bypasses maintainer approval.
"""
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("job", "workflow", "alternatives", "evidence", "counterevidence", "experiment")
LANGUAGES = ("zh", "en", "fr")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REPORT = re.compile(r"^reports/(\d{4})/(\d{2})/(\d{4}-\d{2}-\d{2})\.md$")

def validate_export(payload, root=ROOT):
    errors = []
    if not isinstance(payload, dict):
        return ["Export must be a JSON object"]
    slug = payload.get("slug")
    if not isinstance(slug, str) or not SLUG.fullmatch(slug):
        errors.append("Invalid slug")
    if payload.get("review_status") != "requires_maintainer_approval":
        errors.append("Export must require maintainer approval")
    path = payload.get("source_report")
    m = REPORT.fullmatch(path) if isinstance(path, str) else None
    if not m or m.group(3)[:4] != m.group(1) or m.group(3)[5:7] != m.group(2):
        errors.append("Invalid source report path")
    elif not (root/path).is_file():
        errors.append("Source report not found in repository")
    indexed = {}
    with (root/"index/products.csv").open(encoding="utf-8", newline="") as f:
        indexed = {row["slug"]: row for row in csv.DictReader(f)}
    if slug not in indexed:
        errors.append("Product slug is not in research index")
    elif isinstance(path, str) and indexed[slug].get("first_observed") != Path(path).stem:
        errors.append("Source report does not match first observation date")
    entry = payload.get("intelligence")
    if not isinstance(entry, dict):
        errors.append("Missing intelligence object")
    else:
        for field in FIELDS:
            translations = entry.get(field)
            if not isinstance(translations, dict):
                errors.append(field+": missing translations")
                continue
            for lang in LANGUAGES:
                value = translations.get(lang)
                if not isinstance(value, str) or not value.strip() or len(value)>1500:
                    errors.append(field+"."+lang+": must contain 1–1500 characters")
        if entry.get("source_status") != "editorial_review_pending":
            errors.append("Source status must remain editorial_review_pending")
        if set(entry) != set(FIELDS)|{"source_status"}:
            errors.append("Unexpected intelligence fields")
    if set(payload) != {"slug", "source_report", "review_status", "intelligence"}:
        errors.append("Unexpected export fields")
    return errors

def prepare(payload, root=ROOT):
    errors = validate_export(payload, root)
    if errors:
        raise ValueError("; ".join(errors))
    target = root/"data/research_intelligence.json"
    result = json.loads(target.read_text(encoding="utf-8"))
    if payload["slug"] in result["products"]:
        raise ValueError("Product already has curated intelligence; manual conflict resolution required")
    result["products"][payload["slug"]] = payload["intelligence"]
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    review = json.loads(args.review.read_text(encoding="utf-8"))
    target = (root/"data/research_intelligence.json").resolve()
    output = args.output.resolve()
    if output == target:
        parser.error("Refusing to overwrite canonical intelligence. Generate a candidate file and review the diff first.")
    result = prepare(review, root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Prepared candidate intelligence JSON for manual diff and PR:", output)

if __name__ == "__main__":
    main()

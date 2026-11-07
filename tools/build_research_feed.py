"""Generate public research navigation from dated reports and the existing product index.

This feed is a research directory, NOT a product-launch feed or candidate approval.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://github.com/supplicant-snowstain/startup-product-radar/blob/main/"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def build(root=ROOT):
    intelligence_path = root / "data/research_intelligence.json"
    intelligence = json.loads(intelligence_path.read_text(encoding="utf-8"))["products"] if intelligence_path.is_file() else {}
    products = {}
    with (root / "index/products.csv").open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            day = row.get("first_observed", "")
            if DATE.fullmatch(day):
                products.setdefault(day, []).append({"slug": row["slug"], "name": row["name"], "category": row.get("category", "Unknown"), "ai_role": row.get("ai_role", "unknown"), "website": row.get("website", ""), "profile_url": BASE + row["profile_path"], "intelligence": intelligence.get(row["slug"])})
    items = []
    for path in sorted((root / "reports").glob("????/??/????-??-??.md"), reverse=True):
        day = path.stem
        if not DATE.fullmatch(day):
            continue
        content = path.read_text(encoding="utf-8")
        heading = next((line.lstrip("# ").strip() for line in content.splitlines() if line.startswith("# ")), "")
        items.append({"observed_at": day, "title": heading[:200], "report_url": BASE + path.relative_to(root).as_posix(), "products": products.get(day, [])[:8], "evidence_status": "research_provisional"})
    return {"schema_version": 1, "kind": "research_observations", "disclaimer": "Observation date is not launch date. Research does not imply verified demand, retention or PMF.", "reports": items[:30]}


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--output", type=Path, default=Path("web/research.json"))
    args = p.parse_args()
    out = args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build(args.root), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

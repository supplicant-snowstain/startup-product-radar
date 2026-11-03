"""Create a verifiable build manifest from the exact feeds shipped to Pages."""
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

def build(web, commit=None, built_at=None):
    web=Path(web)
    products=json.loads((web/"products.json").read_text(encoding="utf-8"))
    signals=json.loads((web/"signals.json").read_text(encoding="utf-8"))
    items=products["products"]
    if products["count"]!=len(items) or signals["count"]!=len(signals["signals"]):
        raise ValueError("Feed count mismatch")
    if not all(p.get("collection") in ("new_launch","case_study") for p in items):
        raise ValueError("Product collection missing")
    stamp=built_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {"schema_version":1,"generated_at_utc":stamp,
            "commit_sha":commit or None,"products":len(items),
            "dated_launches":sum(p["collection"]=="new_launch" for p in items),
            "case_studies":sum(p["collection"]=="case_study" for p in items),
            "problem_signals":len(signals["signals"]),
            "explanation":"Build timestamp is not a product launch date, research observation date, or proof of daily archival."}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--web",default="web")
    parser.add_argument("--output",default="web/site-status.json")
    parser.add_argument("--commit",default=os.getenv("GITHUB_SHA"))
    args=parser.parse_args()
    result=build(args.web,commit=args.commit)
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Site manifest:",result)

if __name__=="__main__":main()

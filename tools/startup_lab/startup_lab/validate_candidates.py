"""Validate the entire unreviewed product candidate queue before publishing."""
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from .product_candidates import canonical_url

def validate(root):
    root=Path(root)
    folder=root/"data"/"product_candidates"
    failures=[]
    seen={}
    for path in sorted(folder.glob("*.json")):
        if path.name=="README.md":continue
        try:
            obj=json.loads(path.read_text(encoding="utf-8"))
            url=canonical_url(obj["source_url"])
            expected="candidate-"+hashlib.sha256(url.encode()).hexdigest()[:16]
            if obj.get("id")!=expected or path.stem!=expected:
                raise ValueError("Candidate ID or file name mismatches canonical source URL")
            if obj.get("review_state")!="pending" or obj.get("source_checked") is not False:
                raise ValueError("Unreviewed candidate must remain pending")
            if obj.get("launch_date") is not None or obj.get("launch_date_verified") is not False:
                raise ValueError("Candidate must not claim verified launch date")
            if not isinstance(obj.get("name"),str) or not obj["name"].strip():
                raise ValueError("Missing candidate name")
            date.fromisoformat(obj["observed_at"])
            if url in seen:raise ValueError("Duplicate source URL also in "+seen[url])
            seen[url]=str(path)
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as exc:
            failures.append(str(path)+": "+str(exc))
    return {"checked":len(list(folder.glob("*.json"))),"errors":failures}

def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument("--root",default=".")
    args=parser.parse_args()
    report=validate(args.root)
    print(json.dumps(report,indent=2))
    if report["errors"]:raise SystemExit(1)

if __name__=="__main__":main()

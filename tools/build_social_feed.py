#!/usr/bin/env python3
"""Publish only verified, reviewed official product profiles. Never scrape private accounts."""
import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlparse

PLATFORMS={"x","github","producthunt"}
def build(registry, known):
    if registry.get("schema_version") != 1 or not isinstance(registry.get("profiles"),list):
        raise ValueError("invalid social profiles registry")
    out=[]
    for p in registry["profiles"]:
        if p.get("review_status")!="approved":
            continue
        url=p.get("profile_url","")
        evidence=p.get("identity_evidence_url","")
        if (p.get("product_slug") not in known or p.get("platform") not in PLATFORMS
            or p.get("identity_status")!="verified" or
            not all(isinstance(u,str) and urlparse(u).scheme=="https" and urlparse(u).netloc for u in [url,evidence])):
            raise ValueError("approved profile lacks identity verification or known product: "+str(p.get("product_slug")))
        out.append({k:p[k] for k in ["product_slug","platform","profile_url","identity_status","identity_evidence_url","review_status"]})
    return {"schema_version":1,"profiles":out}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--registry",default="data/social_profiles.json")
    ap.add_argument("--products",default="index/products.csv")
    ap.add_argument("--output",default="web/social-profiles.json")
    args=ap.parse_args()
    known={r["slug"] for r in csv.DictReader(Path(args.products).open(encoding="utf-8",newline=""))}
    payload=build(json.loads(Path(args.registry).read_text(encoding="utf-8")),known)
    Path(args.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Published",len(payload["profiles"]),"reviewed social profiles")

if __name__=="__main__":
    main()

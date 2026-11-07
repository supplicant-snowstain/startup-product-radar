"""Validate curated intelligence without treating editorial content as verified demand."""
import argparse
import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIELDS=("job","workflow","alternatives","evidence","counterevidence","experiment")
LANGS=("zh","en","fr")
def check(root=ROOT):
    errors=[]
    with (root/"index/products.csv").open(encoding="utf-8",newline="") as f:
        index={row["slug"]:row for row in csv.DictReader(f)}
    data=json.loads((root/"data/research_intelligence.json").read_text(encoding="utf-8"))
    products=data.get("products")
    if not isinstance(products,dict):
        return ["products must be an object"]
    for slug,entry in products.items():
        if slug not in index:
            errors.append(slug+": not indexed")
        if not isinstance(entry,dict):
            errors.append(slug+": invalid entry")
            continue
        for field in FIELDS:
            values=entry.get(field)
            if not isinstance(values,dict):
                errors.append(slug+"."+field+": missing language object")
                continue
            for lang in LANGS:
                value=values.get(lang)
                if not isinstance(value,str) or not value.strip() or len(value)>1500:
                    errors.append(slug+"."+field+"."+lang+": missing or invalid")
        if not isinstance(entry.get("source_status"),str) or not entry["source_status"].strip():
            errors.append(slug+": missing source status")
        if "source_links" in entry:
            from urllib.parse import urlparse
            links=entry["source_links"]
            if not isinstance(links,list) or not links or any(not isinstance(link,str) or urlparse(link).scheme!="https" or not urlparse(link).hostname for link in links):
                errors.append(slug+": invalid source links")
        if "evidence_level" in entry and entry["evidence_level"] not in ("public_claims","observed_public_feedback","independent_user_evidence"):
            errors.append(slug+": invalid evidence level")
        if entry.get("source_status") in ("verified_demand","proven_pmf","approved"):
            errors.append(slug+": unsupported evidence certification")
    return errors

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    args=p.parse_args()
    errors=check(args.root)
    if errors:
        for err in errors: print("FAIL:",err)
        raise SystemExit(1)
    print("Curated intelligence schema and index linkage validated.")
if __name__=="__main__":main()

"""Stage candidate product research without automatically publishing claims."""
import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

def canonical_url(url):
    parsed=urlsplit(url.strip())
    if parsed.scheme!="https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Public source must be a valid HTTPS URL")
    query=urlencode(sorted((k,v) for k,v in parse_qsl(parsed.query) if not k.lower().startswith("utm_")))
    return urlunsplit(("https",parsed.hostname.lower(),parsed.path.rstrip("/") or "/",query,""))

def stage(root, incoming):
    root=Path(root)
    if not isinstance(incoming,list):raise ValueError("Input must be a JSON array")
    folder=root/"data"/"product_candidates";folder.mkdir(parents=True,exist_ok=True)
    published=root/"data"/"products"
    known=set()
    for path in list(folder.glob("*.json"))+list(published.glob("*.json") if published.exists() else []):
        record=json.loads(path.read_text(encoding="utf-8"))
        try:known.add(canonical_url(record["source_url"]))
        except (KeyError,ValueError):pass
    result={"created":[],"duplicates":[],"errors":[]}
    for i,item in enumerate(incoming):
        try:
            if not isinstance(item,dict):raise ValueError("Entry must be an object")
            name=item.get("name","").strip()
            if not name or len(name)>200:raise ValueError("Product name missing or too long")
            url=canonical_url(item.get("source_url",""))
            observed=item.get("observed_at","")
            if not isinstance(observed,str):raise ValueError('Invalid observation date')
            date.fromisoformat(observed)
            if url in known:
                result["duplicates"].append({"index":i,"name":name,"source_url":url});continue
            key=hashlib.sha256(url.encode()).hexdigest()[:16]
            record={"id":"candidate-"+key,"name":name,"source_url":url,
                    "observed_at":observed,"description":item.get("description",""),
                    "source_type":item.get("source_type","unverified_public_source"),
                    "review_state":"pending","source_checked":False,
                    "launch_date":None,"launch_date_verified":False,
                    "notes":"Candidate only. Do not automatically publish as new launch or confirmed user demand."}
            destination=folder/(record["id"]+".json")
            destination.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            known.add(url);result["created"].append(str(destination.relative_to(root)))
        except (TypeError,ValueError) as error:result["errors"].append({"index":i,"error":str(error)})
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("input",help="JSON file containing an array of publicly observed products")
    parser.add_argument("--root",default=".")
    args=parser.parse_args()
    incoming=json.loads(Path(args.input).read_text(encoding="utf-8"))
    print(json.dumps(stage(args.root,incoming),ensure_ascii=False,indent=2))
if __name__=="__main__":main()

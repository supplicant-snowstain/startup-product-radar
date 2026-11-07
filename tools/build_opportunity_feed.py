#!/usr/bin/env python3
"""Publish reviewed opportunity research; never auto-promote hypotheses to facts."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

SECTIONS={"founding","feedback","growth","future","timeline"}
def build(data, known):
    if data.get("schema_version")!=1 or not isinstance(data.get("products"),dict):
        raise ValueError("invalid opportunity schema")
    published={}
    for slug,sections in data["products"].items():
        if slug not in known or not isinstance(sections,dict):
            raise ValueError("unknown product or invalid section: "+slug)
        for key,record in sections.items():
            if key not in SECTIONS or not isinstance(record,dict):
                raise ValueError("invalid opportunity section: "+key)
            if record.get("review_status")!="approved":
                continue
            if record.get("claim_status") not in {"documented","hypothesis"}:
                raise ValueError("approved section needs claim_status: "+slug+"/"+key)
            summary=record.get("summary")
            if not isinstance(summary,dict) or not all(isinstance(summary.get(l),str) and summary[l].strip() for l in ["zh","en","fr"]):
                raise ValueError("approved section requires three languages: "+slug+"/"+key)
            sources=record.get("sources")
            if not isinstance(sources,list) or not sources:
                raise ValueError("approved section requires source: "+slug+"/"+key)
            for src in sources:
                u=src.get("url") if isinstance(src,dict) else None
                if not isinstance(u,str) or urlparse(u).scheme!="https" or not urlparse(u).netloc:
                    raise ValueError("invalid source: "+slug+"/"+key)
            published.setdefault(slug,{})[key]={k:record[k] for k in ["summary","evidence","counterevidence","next_test","sources","claim_status"] if k in record}
    return {"schema_version":1,"products":published}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--registry",default="data/opportunity.json")
    p.add_argument("--research",default="web/research.json")
    p.add_argument("--output",default="web/opportunity.json")
    a=p.parse_args()
    feed=json.loads(Path(a.research).read_text(encoding="utf-8"))
    known={p["slug"] for report in feed["reports"] for p in report.get("products",[]) if p.get("slug")}
    output=build(json.loads(Path(a.registry).read_text(encoding="utf-8")),known)
    Path(a.output).write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Published",sum(map(len,output["products"].values())),"reviewed opportunity sections")
if __name__=="__main__":
    main()

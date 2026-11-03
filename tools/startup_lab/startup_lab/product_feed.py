"""Generate a product discovery feed without inventing products or launch dates."""
import json
from pathlib import Path

def build(root):
    base=Path(root)/"data"/"products"
    products=[]
    for path in sorted(base.glob("*.json")) if base.exists() else []:
        item=json.loads(path.read_text(encoding="utf-8"))
        required=("id","name","description","category","source_url","source_type","observed_at","date_precision","verification_status")
        if any(not item.get(k) for k in required):raise ValueError("Incomplete product record: "+str(path))
        if item["verification_status"] not in ("provisional","source_checked","reviewed"):
            raise ValueError("Unknown verification state: "+str(path))
        if item["date_precision"] not in ("day","month","unknown"):
            raise ValueError("Unknown date precision: "+str(path))
        products.append({k:item.get(k) for k in ("id","name","description","category","website","source_url","source_type","observed_at","launch_date","date_precision","verification_status","problem_ids","differentiator","limitations","story")})
    ids=[x["id"] for x in products]
    if len(set(ids))!=len(ids):raise ValueError("Duplicate product IDs")
    products.sort(key=lambda x:(x["observed_at"],x["id"]),reverse=True)
    return {"schema_version":1,"status":"research_feed","count":len(products),"products":products,"warning":"Observed-at is the research observation date, not necessarily the launch date. Product listing does not prove demand or product-market fit."}

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--root",default=".")
    p.add_argument("--output",default="web/products.json")
    args=p.parse_args()
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    feed=build(args.root)
    out.write_text(json.dumps(feed,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Published",feed["count"],"products")

if __name__=="__main__":main()

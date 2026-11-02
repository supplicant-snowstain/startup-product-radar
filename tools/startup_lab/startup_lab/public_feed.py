"""Generate a static, public, provisional opportunity feed from repository records."""
import json
from pathlib import Path

def build(root):
    root=Path(root)
    folder=root/"data"/"provisional"
    items=[]
    for path in sorted(folder.glob("*.json")):
        item=json.loads(path.read_text(encoding="utf-8"))
        if item.get("review_state")!="ai_source_read_only" or item.get("human_reviewed") is not False:
            raise ValueError("Unexpected provisional record review state: "+str(path))
        required=("id","title","domain","problem","source_url","source_locator","observed_at","limitations")
        if any(not item.get(field) for field in required):
            raise ValueError("Missing provisional field: "+str(path))
        items.append({"id":item["id"],"title":item["title"],"domain":item["domain"],
                      "user_segment":item.get("user_segment","Not specified"),
                      "problem":item["problem"],"source_url":item["source_url"],
                      "source_locator":item["source_locator"],"observed_at":item["observed_at"],
                      "source_type":item.get("source_type","unknown"),
                      "review_state":"provisional_not_human_reviewed",
                      "limitations":item["limitations"],"questions":item.get("questions",[])})
    ids=[i["id"] for i in items]
    if len(ids)!=len(set(ids)):raise ValueError("Duplicate provisional IDs")
    return {"schema_version":1,"dataset_status":"provisional_only","count":len(items),"signals":items,
            "disclaimer":"Public source leads. Not independently corroborated or validated customer demand."}

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",default=".")
    parser.add_argument("--output",default="web/signals.json")
    args=parser.parse_args()
    feed=build(args.root)
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(feed,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Generated",path,"with",feed["count"],"signals")

if __name__=="__main__":main()

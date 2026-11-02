"""Browse attributed public opportunity signals WITHOUT treating them as reviewed evidence."""
import json
from pathlib import Path
from .retrieval import tokens

def load_signals(root):
    folder=Path(root)/"data"/"provisional"
    records=[]
    if not folder.exists(): return records
    seen=set()
    for file in sorted(folder.glob("*.json")):
        r=json.loads(file.read_text(encoding="utf-8"))
        required=("id","kind","title","domain","user_segment","problem","source_url","source_locator","review_state","human_reviewed","limitations")
        if any(key not in r for key in required):raise ValueError("Missing required fields in "+str(file))
        if r["id"] in seen:raise ValueError("Duplicate signal id: "+r["id"])
        if r["human_reviewed"] is not False or r["review_state"]!="ai_source_read_only":
            raise ValueError("Unexpected approval state for provisional signal "+r["id"])
        seen.add(r["id"]);records.append(r)
    return records

def discover_public(root,query="",limit=20):
    if not 1<=limit<=100:raise ValueError("limit must be 1..100")
    q=tokens(query)
    cards=[]
    for r in load_signals(root):
        matched=sorted(q & tokens(" ".join(str(r.get(k,"")) for k in ("title","domain","user_segment","problem","statement"))))
        if q and not matched:continue
        cards.append({"id":r["id"],"title":r["title"],"domain":r["domain"],"kind":r["kind"],
                      "user_segment":r["user_segment"],"problem":r["problem"],
                      "source_url":r["source_url"],"source_locator":r["source_locator"],
                      "review_state":"provisional_not_human_reviewed","matched_terms":matched})
    cards.sort(key=lambda r:(-len(r["matched_terms"]),r["id"]))
    return {"total":len(cards),"cards":cards[:limit],
            "warning":"Public sources were read by AI; independent corroboration and human review are pending. No validated market-demand claims."}

def explore_public(root,signal_id):
    r=next((r for r in load_signals(root) if r["id"]==signal_id),None)
    if r is None:raise ValueError("Unknown provisional signal "+signal_id)
    return {"signal":r,"review_state":"provisional_not_human_reviewed",
            "warning":"A public comment or founder claim is not proof of unmet demand. Never merge into reviewed evidence automatically."}

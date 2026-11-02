"""Opportunity Discovery and Exploration over reviewed local records.

No market conclusions are generated without associated evidence.
"""
import json
from pathlib import Path
from .retrieval import tokens
from .repository import load_evidence, load_products

def load_needs(root):
    folder=Path(root)/"data"/"needs"
    results=[]
    if not folder.exists(): return []
    seen=set()
    for path in sorted(folder.glob("*.json")):
        row=json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(row,dict): raise ValueError(f"Invalid need: {path}")
        required=("id","title","domain","user_segment","problem","evidence_ids","product_ids")
        if any(k not in row for k in required):raise ValueError(f"Missing need fields: {path}")
        if row["id"] in seen:raise ValueError(f"Duplicate need ID: {row['id']}")
        if not isinstance(row["evidence_ids"],list) or not isinstance(row["product_ids"],list):
            raise ValueError(f"Invalid need links: {path}")
        seen.add(row["id"])
        results.append(row)
    return results

def _corpus(root):
    needs=load_needs(root)
    evidence=load_evidence(root)
    products=load_products(root)
    evidence_by_id={e["id"]:e for e in evidence}
    product_by_id={p.get("slug"):p for p in products}
    return needs,evidence_by_id,product_by_id

def discover(root,query="",limit=20):
    if limit<1 or limit>100:raise ValueError("limit must be between 1 and 100")
    needs,ev,products=_corpus(root)
    query_words=tokens(query)
    cards=[]
    for need in needs:
        description=" ".join(str(need.get(k,"")) for k in ("title","domain","user_segment","problem"))
        overlap=query_words & tokens(description)
        if query_words and not overlap: continue
        linked=[ev[i] for i in need["evidence_ids"] if i in ev]
        missing=sorted(set(need["evidence_ids"])-set(ev))
        listed=[products[i] for i in need["product_ids"] if i in products]
        independent=[e for e in linked if e["evidence_type"] in ("primary","independent","user-report")]
        cards.append({"id":need["id"],"title":need["title"],"domain":need["domain"],
            "user_segment":need["user_segment"],"problem":need["problem"],
            "matched_terms":sorted(overlap),"evidence_count":len(linked),
            "independent_evidence_count":len(independent),"missing_evidence_ids":missing,
            "related_products":[{"slug":p["slug"],"name":p["name"]} for p in listed],
            "status":"unverified_links" if missing else ("evidence_linked" if independent else "limited_evidence")})
    cards.sort(key=lambda c:(-len(c["matched_terms"]),-c["independent_evidence_count"],c["id"]))
    return {"query":query,"total":len(cards),"cards":cards[:limit],
            "limitations":["Counts are not proof of unmet demand or product success.",
                           "Unlinked records and absent sources may indicate an incomplete corpus."]}

def explore(root,need_id):
    needs,ev,products=_corpus(root)
    need=next((n for n in needs if n["id"]==need_id),None)
    if need is None:raise ValueError("Unknown need ID: "+need_id)
    grouped={"support":[],"contradict":[],"context":[],"unknown":[]}
    missing=[]
    for eid in need["evidence_ids"]:
        e=ev.get(eid)
        if e is None:
            missing.append(eid);continue
        direction=e.get("direction","unknown")
        if direction not in grouped:direction="unknown"
        grouped[direction].append({"id":eid,"statement":e["statement"],
            "source_url":e["source_url"],"observed_at":e["observed_at"],
            "evidence_type":e["evidence_type"]})
    relevant=[products[i] for i in need["product_ids"] if i in products]
    return {"need":need,"evidence":grouped,"missing_evidence_ids":missing,
            "missing_product_ids":sorted(set(need["product_ids"])-set(products)),
            "related_products":[{"slug":p["slug"],"name":p["name"],"website":p.get("website",""),
                                  "category":p.get("category","")} for p in relevant],
            "assessment":"needs_source_review" if missing else ("linked_evidence_available" if any(grouped.values()) else "no_evidence"),
            "limitations":["This is a sourced exploration view, not an automatic finding of market opportunity.",
                           "Evidence direction is metadata, not proof of logical contradiction."]}

"""Offline, citation-preserving retrieval over curated evidence records."""
import re
from .repository import load_evidence

STOP={"the","and","for","with","this","that","from","into","have","will","用户","产品","市场","一个","以及"}
def tokens(text):
    english=re.findall(r"[a-z0-9]+",text.lower())
    han=re.findall(r"[\u4e00-\u9fff]{2,}",text)
    grams=[segment[i:i+2] for segment in han for i in range(len(segment)-1)]
    return set(t for t in english+han+grams if t not in STOP)

def retrieve(root,query,limit=10):
    if not query.strip(): raise ValueError("query cannot be blank")
    if not 1 <= limit <= 100: raise ValueError("limit must be 1..100")
    q=tokens(query)
    results=[]
    for e in load_evidence(root):
        document=" ".join(str(e.get(k,"")) for k in ("statement","dimension","product_id"))
        matched=sorted(q & tokens(document))
        if not matched: continue
        # Transparent lexical overlap; does not claim semantic relevance.
        score=len(matched)/max(len(q),1)
        results.append({"id":e["id"],"score":round(score,4),"matched_tokens":matched,
                        "statement":e["statement"],"source_url":e["source_url"],
                        "direction":e.get("direction","unknown"),
                        "dimension":e.get("dimension","unknown"),
                        "evidence_type":e["evidence_type"],
                        "observed_at":e["observed_at"]})
    results.sort(key=lambda e:(-e["score"],e["id"]))
    return {"query":query,"total_matches":len(results),"results":results[:limit],
            "limitations":["Lexical search only; no source verification or completeness guarantee.",
                           "Missing records do not establish absence of demand."]}

def evidence_sides(root,query,limit=20):
    found=retrieve(root,query,limit)
    grouped={"support":[],"contradict":[],"context":[],"unknown":[]}
    for e in found["results"]:
        direction=e["direction"]
        grouped[direction if direction in grouped else "unknown"].append(e)
    return {"query":query,"sides":grouped,"potential_disagreement":
            bool(grouped["support"] and grouped["contradict"]),
            "warning":"Opposing labels are candidates for manual review, not verified logical contradictions.",
            "total_matches":found["total_matches"]}

"""Fail-closed conversion of reviewed research candidates into evidence records.

No LLM extraction or web fetch is performed. Each candidate explicitly quotes a
short claim and links it to a public source; promotion is manual.
"""
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ALLOWED_TYPES = {"primary","user-report","independent","founder-claim","investor-claim","analyst-inference"}
DIMENSIONS = {"user_need","competitor","differentiation","distribution","pricing","feasibility"}
DIRECTIONS = {"support","contradict","context","unknown"}

def canonical_url(value):
    p=urlsplit(value.strip())
    if p.scheme not in ("https","http") or not p.hostname:
        raise ValueError("source_url must be an absolute HTTP(S) URL")
    host=p.hostname.lower()
    if host in {"example.org","example.com","example.net"}:
        raise ValueError("example domains are synthetic and cannot be published")
    # Avoid changing meaningful paths or query parameters.
    netloc=host + ((":"+str(p.port)) if p.port else "")
    return urlunsplit((p.scheme.lower(),netloc,p.path or "/",p.query,""))

def review_candidate(candidate):
    problems=[]
    def require_text(field):
        val=candidate.get(field)
        if not isinstance(val,str) or not val.strip():
            problems.append("missing "+field)
            return ""
        return val.strip()
    claim=require_text("statement")
    url=require_text("source_url")
    observed=require_text("observed_at")
    limitations=require_text("limitations")
    source_locator=require_text("source_locator")
    for field in ("observed_at","source_published_at","event_date"):
        if candidate.get(field) is not None:
            try: date.fromisoformat(candidate[field])
            except (ValueError,TypeError): problems.append("invalid "+field)
    if candidate.get("evidence_type") not in ALLOWED_TYPES: problems.append("invalid evidence_type")
    if candidate.get("direction") not in DIRECTIONS: problems.append("invalid direction")
    if candidate.get("dimension") not in DIMENSIONS: problems.append("invalid dimension")
    if candidate.get("review_status") != "approved": problems.append("candidate not approved")
    if candidate.get("source_checked") is not True: problems.append("source not checked")
    if not candidate.get("reviewed_by") or not str(candidate["reviewed_by"]).strip():
        problems.append("reviewer not identified")
    try: normalized=canonical_url(url)
    except (ValueError,TypeError) as ex:
        normalized=""
        problems.append(str(ex))
    if len(claim)>800: problems.append("statement too long")
    if problems:
        return {"accepted":False,"problems":problems}
    # Stable identity for same observation; citations with differing claims remain distinct.
    fingerprint="|".join((normalized,source_locator,claim))
    identifier="ev-"+hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:16]
    record={k:candidate[k] for k in ("statement","observed_at","evidence_type","direction","limitations","dimension")}
    record.update({"id":identifier,"source_url":normalized,"confidence":candidate.get("confidence","unassessed"),
                   "source_locator":source_locator,"reviewed_by":candidate["reviewed_by"].strip(),
                   "reviewed_at":candidate.get("reviewed_at",observed)})
    for key in ("source_published_at","event_date","product_id"):
        if key in candidate: record[key]=candidate[key]
    return {"accepted":True,"record":record}

def promote(candidate_file,output_dir):
    candidate=json.loads(Path(candidate_file).read_text(encoding="utf-8"))
    decision=review_candidate(candidate)
    if not decision["accepted"]: return decision
    output=Path(output_dir)/ (decision["record"]["id"]+".json")
    output.parent.mkdir(parents=True,exist_ok=True)
    serialized=json.dumps(decision["record"],ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if output.exists() and output.read_text(encoding="utf-8") != serialized:
        return {"accepted":False,"problems":["record ID collision or attempted modification"]}
    output.write_text(serialized,encoding="utf-8")
    return {"accepted":True,"path":str(output),"record":decision["record"]}

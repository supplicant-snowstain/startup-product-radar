"""Read public research records from repository files; fail closed on missing evidence."""
import csv
import json
from pathlib import Path
from .evaluator import evaluate

def load_products(root):
    path=Path(root)/"index"/"products.csv"
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))

def load_evidence(root):
    folder=Path(root)/"data"/"evidence"
    records=[]
    if not folder.exists():
        return records
    for path in sorted(folder.glob("*.json")):
        record=json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(record,dict):
            raise ValueError(f"evidence must be an object: {path}")
        for key in ("id","source_url","statement","observed_at","evidence_type"):
            if not record.get(key):
                raise ValueError(f"missing {key}: {path}")
        records.append(record)
    return records

def audit_repository(root):
    products=load_products(root)
    evidence=load_evidence(root)
    seen=set()
    duplicates=[]
    for record in evidence:
        if record["id"] in seen:
            duplicates.append(record["id"])
        seen.add(record["id"])
    return {"product_rows":len(products),"evidence_records":len(evidence),
            "duplicate_evidence_ids":duplicates,
            "readiness":"data_available" if evidence else "awaiting_verified_evidence",
            "note":"Product index rows and public evidence are counted, not independently authenticated."}

def idea_from_repository(root,idea_path):
    idea=json.loads(Path(idea_path).read_text(encoding="utf-8"))
    evidence=load_evidence(root)
    ids=set(idea.get("evidence_ids",[]))
    selected=[e for e in evidence if e["id"] in ids]
    mapped=[]
    for e in selected:
        kinds={"primary":"primary","user-report":"user_report","independent":"independent",
               "founder-claim":"founder_claim","investor-claim":"investor_claim",
               "analyst-inference":"analyst_inference"}
        mapped.append({"id":e["id"],"url":e["source_url"],"observed_at":e["observed_at"],
                       "type":kinds.get(e["evidence_type"],"invalid"),
                       "dimension":e.get("dimension","unknown"),
                       "stance":e.get("stance","context"),"claim":e["statement"]})
    result=evaluate({"id":idea.get("id"),"evidence":mapped})
    result["missing_evidence_ids"]=sorted(ids-{e["id"] for e in selected})
    result["repository_audit"]=audit_repository(root)
    if result["missing_evidence_ids"]:
        result["status"]="invalid_input"
    result["limitations"].append("Repository citations and claims are not independently verified by this offline audit.")
    return result

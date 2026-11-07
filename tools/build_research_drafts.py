"""Create reviewable research-intelligence drafts; never publish or approve them.

Only deterministic evidence snippets are extracted. A human must independently
verify, translate, and merge drafts into data/research_intelligence.json.
"""
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("job", "workflow", "alternatives", "evidence", "counterevidence", "experiment")
MAX_CHARS = 500
PATTERNS = {
    "job": r"(?:JTBD|用户问题|用户任务|目标用户)\s*[:：]\s*([^\n]+)",
    "workflow": r"(?:CLAIMED 工作流|工作流|使用流程)\s*[:：]\s*([^\n]+)",
    "alternatives": r"(?:替代方案)\s*[:：]\s*([^\n]+)",
    "counterevidence": r"(?:CONTRADICTED|反面证据|限制)\s*[:：]\s*([^\n]+)",
    "experiment": r"(?:可证伪假设|可证伪实验|验证实验)\s*[:：]\s*([^\n]+)",
}
def extract(report, name):
    # Restrict extraction to a heading that explicitly names the product.
    pattern = re.compile(r"^#{2,4}\s+[^\n]*"+re.escape(name)+r"[^\n]*$", re.I|re.M)
    match = pattern.search(report)
    if not match:
        return {}
    following = re.search(r"^#{2,4}\s+", report[match.end():], re.M)
    section = report[match.end():match.end()+following.start()] if following else report[match.end():]
    result = {}
    for field, pat in PATTERNS.items():
        m = re.search(pat, section, re.I)
        if m:
            result[field] = m.group(1).strip().strip("-* ")[:MAX_CHARS]
    return result

def build(root=ROOT):
    reviewed = json.loads((root/"data/research_intelligence.json").read_text(encoding="utf-8")).get("products", {})
    drafts = []
    with (root/"index/products.csv").open(encoding="utf-8",newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        slug = row.get("slug","")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",slug) or slug in reviewed:
            continue
        day = row.get("first_observed","")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}",day):
            continue
        report_path = root/"reports"/day[:4]/day[5:7]/(day+".md")
        if not report_path.is_file():
            continue
        snippets = extract(report_path.read_text(encoding="utf-8"), row.get("name",""))
        if not snippets:
            continue
        drafts.append({
            "slug":slug,"name":row["name"],"observed_at":day,
            "review_status":"needs_human_review",
            "source_report":report_path.relative_to(root).as_posix(),
            "extracted_zh":snippets,
            "missing_fields":[key for key in FIELDS if key not in snippets],
            "required_checks":["Verify each claim against primary sources","Distinguish observed, claimed and inferred","Translate zh/en/fr manually","Review counterevidence and falsification criteria"],
        })
    return {"schema_version":1,"kind":"editorial_drafts_not_publication","policy":"These are unverified extraction drafts, not approved product intelligence or verified demand.","drafts":drafts}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--output",type=Path,default=Path("data/research_drafts.json"))
    args=p.parse_args()
    result=build(args.root)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Generated",len(result["drafts"]),"review-only drafts")

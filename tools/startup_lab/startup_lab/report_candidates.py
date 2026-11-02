"""Extract Markdown link references as UNREVIEWED source candidates.

No factual assertion is inferred and no item is automatically approved.
"""
import re
from pathlib import Path
from urllib.parse import urlsplit

LINK=re.compile(r"(?<!!)\[([^\]\n]{1,140})\]\((https?://[^)\s]+)\)")
def report_candidates(path):
    p=Path(path)
    content=p.read_text(encoding="utf-8")
    candidates=[]
    seen=set()
    for match in LINK.finditer(content):
        title,url=match.groups()
        if not urlsplit(url).hostname or url in seen: continue
        seen.add(url)
        line=content.count("\n",0,match.start())+1
        candidates.append({"source_url":url,"source_locator":str(p)+":"+str(line),
                           "link_label":title,"review_status":"pending",
                           "source_checked":False,"statement":None,
                           "notice":"A link is not evidence; a curator must check the source and formulate a bounded claim."})
    return {"report":str(p),"candidates":candidates,
            "warning":"No claims, review flags or evidence scores are automatically generated."}

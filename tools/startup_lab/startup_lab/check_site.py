"""Verify a generated static-site artifact before GitHub Pages deployment."""
import json
from html.parser import HTMLParser
from pathlib import Path

WEB=Path(__file__).resolve().parents[3]/"web"

class References(HTMLParser):
    def __init__(self):
        super().__init__();self.scripts=[];self.styles=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="script" and a.get("src"):self.scripts.append(a["src"])
        if tag=="link" and a.get("rel")=="stylesheet" and a.get("href"):self.styles.append(a["href"])

def check():
    errors=[]
    for page in ("index.html","explore.html","product.html"):
        parser=References()
        parser.feed((WEB/page).read_text(encoding="utf-8"))
        for asset in parser.scripts+parser.styles:
            if asset.startswith(("http://","https://")):continue
            if not (WEB/asset).is_file():errors.append(page+": missing "+asset)
    for file in ("signals.json","products.json","idea-stories.json","opportunity-map.json"):
        try:json.loads((WEB/file).read_text(encoding="utf-8"))
        except (OSError,ValueError) as e:errors.append(file+": "+str(e))
    products=json.loads((WEB/"products.json").read_text(encoding="utf-8"))
    if products.get("count")!=len(products.get("products",[])):errors.append("products.json: count mismatch")
    if products.get("count",0)==0:errors.append("products.json: no products to showcase")
    if not (WEB/"locales"/"en.json").is_file():errors.append("Missing fallback English language pack")
    return errors

def main():
    problems=check()
    if problems:
        for problem in problems:print("FAIL:",problem)
        raise SystemExit(1)
    print("Static artifact verified: HTML references, data files and product records.")

if __name__=="__main__":main()

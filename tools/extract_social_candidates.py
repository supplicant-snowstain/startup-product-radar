#!/usr/bin/env python3
"""Extract candidate official social links from an explicitly supplied product homepage HTML.
No network requests; output is an unverified review queue, never public identity assertions.
"""
import argparse
from html.parser import HTMLParser
import json
from urllib.parse import urljoin, urlparse

HOSTS = {"x.com": "x", "twitter.com": "x", "github.com": "github",
         "producthunt.com": "producthunt"}
BLOCKED_PATHS = {"share", "intent", "search", "home", "login", "signup", "hashtag", "i"}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        values = dict(attrs)
        if values.get("href"):
            self.hrefs.append(values["href"])

def candidates(product_slug, website, html):
    parser = Links()
    parser.feed(html)
    results, seen = [], set()
    for href in parser.hrefs:
        url = urljoin(website, href)
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower().removeprefix("www.")
        platform = HOSTS.get(host)
        path = parsed.path.strip("/")
        if parsed.scheme != "https" or not platform or not path:
            continue
        if path.split("/")[0].lower() in BLOCKED_PATHS:
            continue
        if platform == "x" and len(path.split("/")) != 1:
            continue
        canonical = f"https://{host}/{path}"
        if canonical in seen:
            continue
        seen.add(canonical)
        results.append({"product_slug": product_slug, "platform": platform,
                        "profile_url": canonical, "discovery_method": "product_website_link",
                        "identity_status": "candidate", "identity_evidence_url": website,
                        "review_status": "pending_review"})
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-slug", required=True)
    parser.add_argument("--website", required=True)
    parser.add_argument("--html-file", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if urlparse(args.website).scheme != "https":
        parser.error("--website must be an HTTPS product homepage")
    from pathlib import Path
    html = Path(args.html_file).read_text(encoding="utf-8")
    records = candidates(args.product_slug, args.website, html)
    Path(args.output).write_text(json.dumps({"schema_version":1,"candidates":records},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Extracted {len(records)} candidate public profiles; none verified.")

if __name__ == "__main__":
    main()

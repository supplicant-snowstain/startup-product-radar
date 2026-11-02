"""Bounded public HTML verification, with SSRF protections and explicit uncertainty.

Optional network action, invoked only by the operator. No automatic promotion.
"""
import hashlib
import html
import ipaddress
import json
import re
import socket
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlsplit, urljoin

MAX_BYTES=1024*1024
class ExtractText(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in {"script","style","noscript"}: self.skip+=1
    def handle_endtag(self,tag):
        if tag in {"script","style","noscript"} and self.skip:self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)
def normalized(text):
    return " ".join(html.unescape(text).split()).casefold()

def validate_public_url(url):
    p=urlsplit(url)
    if p.scheme not in ("http","https") or not p.hostname or p.username or p.password:
        raise ValueError("Only public HTTP(S) URLs without credentials are permitted")
    if p.port not in (None,80,443):
        raise ValueError("Nonstandard ports are not permitted")
    host=p.hostname
    if host in {"localhost","localhost.localdomain"} or host.endswith(".local"):
        raise ValueError("Local hostnames are blocked")
    addresses=socket.getaddrinfo(host,p.port or (443 if p.scheme=="https" else 80),type=socket.SOCK_STREAM)
    if not addresses: raise ValueError("DNS did not return addresses")
    for result in addresses:
        ip=ipaddress.ip_address(result[4][0])
        if not ip.is_global:
            raise ValueError("Non-public IP address blocked")
    return url

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise ValueError("Redirect blocked; inspect the destination separately")

def match_snapshot(content,needle):
    if not isinstance(needle,str) or len(needle.strip())<12:
        raise ValueError("Provide a quoted source excerpt of at least 12 characters")
    parser=ExtractText();parser.feed(content)
    text=normalized(" ".join(parser.parts))
    snippet=normalized(needle)
    return {"excerpt_present":snippet in text,"text_chars":len(text)}

def verify_source(url,excerpt,timeout=8):
    validate_public_url(url)
    request=urllib.request.Request(url,headers={"User-Agent":"StartupProductRadarResearch/0.5","Accept":"text/html"})
    opener=urllib.request.build_opener(NoRedirect)
    try:
        # DNS resolution and address validation occur before the fetch, but standard
        # urllib does not pin the TCP destination IP: not safe for untrusted URLs.
        # Disable remote fetching until a pinned-IP transport is implemented.
        return {"status":"requires_secure_fetch_backend","url":url,
                "checked_at":datetime.now(timezone.utc).isoformat(),
                "excerpt_present":None,
                "warning":"Remote fetch disabled: DNS rebinding remains possible without pinned-IP connections."}
    except (OSError,ValueError) as exc:
        return {"status":"fetch_error","url":url,"error":str(exc),"excerpt_present":None}

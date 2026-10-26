#!/usr/bin/env python3
"""Lightweight on-page SEO checker based on Google's SEO Starter Guide.

Usage:
  python seo_audit.py <file.html | folder | https://url> [--format text|json]

Standard library only. Checks only what the guide supports; it deliberately does
NOT flag heading counts/order, content length, meta keywords as an opportunity,
or TLD choice, because the guide says those are not worth focusing on.
"""
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

GENERIC_ANCHORS = {"click here", "here", "read more", "more", "link", "this",
                   "learn more", "click", "this link", "page"}
BAD_ALT = {"image", "img", "photo", "picture", "image1", "untitled"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.meta = {}
        self.canonical = None
        self.images = []
        self.links = []
        self._link = None
        self._link_text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
            self.title = ""
        elif tag == "meta" and a.get("name"):
            self.meta[a["name"].lower()] = a.get("content", "") or ""
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower():
            self.canonical = a.get("href")
        elif tag == "img":
            self.images.append(a)
        elif tag == "a" and a.get("href"):
            self._link = a
            self._link_text = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "a" and self._link is not None:
            self.links.append((self._link, " ".join("".join(self._link_text).split())))
            self._link = None

    def handle_data(self, data):
        if self._in_title and self.title is not None:
            self.title += data
        if self._link is not None:
            self._link_text.append(data)


def audit_html(html, source):
    p = Page()
    p.feed(html)
    out = []

    def add(sev, msg, fix):
        out.append({"severity": sev, "issue": msg, "fix": fix})

    # Indexability
    robots = p.meta.get("robots", "").lower()
    if "noindex" in robots:
        add("high", "robots meta contains noindex: page is excluded from search",
            "Remove noindex if this page should appear in Google.")

    # Title
    title = (p.title or "").strip()
    if not title:
        add("high", "Missing or empty <title>",
            "Add a unique, concise title that accurately describes the page.")
    elif len(title) > 70:
        add("low", f"Title is long ({len(title)} chars) and may be shortened in results (heuristic)",
            "Put the most important words first; keep it concise.")

    # Meta description
    desc = p.meta.get("description", "").strip()
    if not desc:
        add("medium", "Missing meta description",
            "Add a short, unique 1-2 sentence summary of this page.")

    # Canonical
    if not p.canonical:
        add("info", "No canonical link",
            "Optional. Only needed if the same content is reachable under multiple URLs.")

    # Images
    for img in p.images:
        src = img.get("src", "(no src)")
        if "alt" not in img:
            add("medium", f"Image without alt attribute: {src}",
                "Add descriptive alt text (alt=\"\" only if purely decorative).")
        elif img["alt"].strip().lower() in BAD_ALT:
            add("low", f"Non-descriptive alt text '{img['alt']}': {src}",
                "Describe what the image shows and how it relates to the page.")

    # Link text
    for a, text in p.links:
        if text.strip().lower() in GENERIC_ANCHORS:
            add("low", f"Generic link text '{text}' -> {a.get('href')}",
                "Use anchor text that says what the linked page contains.")

    # URL
    if source.startswith("http"):
        path = urlparse(source).path
        for seg in [s for s in path.split("/") if s]:
            if re.fullmatch(r"[0-9a-fA-F]{12,}|\d+", seg):
                add("low", f"URL segment '{seg}' is an opaque identifier",
                    "Prefer readable words in URLs where practical (long-term, low urgency).")

    return out


def load(target):
    if target.startswith("http"):
        req = urllib.request.Request(target, headers={"User-Agent": "seo-audit/1.0"})
        return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    return Path(target).read_text(encoding="utf-8", errors="replace")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fmt = "json" if "json" in sys.argv else "text"
    if not args:
        sys.exit(__doc__)
    target = args[0]
    sources = []
    if not target.startswith("http") and Path(target).is_dir():
        sources = [str(f) for f in sorted(Path(target).rglob("*.htm*"))]
    else:
        sources = [target]

    results = {}
    for s in sources:
        try:
            results[s] = audit_html(load(s), s)
        except Exception as e:  # report and continue
            results[s] = [{"severity": "error", "issue": f"Could not load: {e}", "fix": ""}]

    if fmt == "json":
        print(json.dumps(results, indent=2))
        return
    order = {"error": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    for s, issues in results.items():
        print(f"\n== {s}")
        if not issues:
            print("  No issues found by automated checks.")
        for i in sorted(issues, key=lambda x: order.get(x["severity"], 9)):
            print(f"  [{i['severity'].upper()}] {i['issue']}\n      -> {i['fix']}")


if __name__ == "__main__":
    main()

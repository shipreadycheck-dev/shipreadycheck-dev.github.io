#!/usr/bin/env python3
"""Build guide pages (_build/guides/*.md -> <slug>.html at the repo root), guides.html,
sitemap.xml and robots.txt. Run from the website repo root: python3 _build/build_guides.py
Folders starting with "_" are not published by GitHub Pages."""
import markdown, re, pathlib, json, html, datetime

BUILD = pathlib.Path(__file__).resolve().parent
ROOT = BUILD.parent
SITE = "https://shipreadycheck-dev.github.io"
TODAY = datetime.date.today().isoformat()

CSS = """:root{--paper:#EEF1F4;--panel:#fff;--ink:#1C2433;--soft:#4A5568;--rule:#C9D1DB;--tag:#F2C230;--focus:#2457C5}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#141A24;--panel:#1C2433;--ink:#E8ECF2;--soft:#A7B1C0;--rule:#2F3A4C;--tag:#E6B422;--focus:#7AA2F7}}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Archivo,system-ui,sans-serif;font-size:18px;line-height:1.65}
a{color:inherit}:focus-visible{outline:3px solid var(--focus);outline-offset:3px}
.wrap{max-width:740px;margin:0 auto;padding:24px 20px 80px}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:36px;font-size:16px}
.brand{font-weight:800;font-stretch:115%;text-decoration:none;display:flex;gap:10px;align-items:center}
.brand i{width:12px;height:12px;border-radius:50%;background:var(--tag);box-shadow:0 0 0 3px var(--ink);display:inline-block}
.top a.cta{text-decoration:none;font-weight:700;border:2px solid var(--ink);border-radius:9px;padding:7px 14px}
h1{font-stretch:118%;font-weight:900;font-size:clamp(30px,5vw,44px);line-height:1.08;margin:0 0 18px}
h2{font-stretch:110%;font-weight:850;font-size:26px;margin:44px 0 10px}
h3{font-size:20px;margin:30px 0 6px}
blockquote{margin:16px 0;padding:16px 20px;background:var(--tag);color:#2A2100;border-radius:12px}
blockquote p{margin:0}
table{border-collapse:collapse;width:100%;font-size:16px;margin:12px 0}
th,td{border:1px solid var(--rule);padding:8px 10px;text-align:left;vertical-align:top}
code{font-family:"JetBrains Mono",monospace;font-size:.84em;background:var(--panel);padding:1px 5px;border-radius:4px}
pre{background:var(--panel);border:1px solid var(--rule);border-radius:10px;padding:16px;overflow-x:auto}
pre code{background:none;padding:0}
.meta{color:var(--soft);font-size:15px;margin:-6px 0 28px}
.box{margin-top:48px;padding:26px;border:2px solid var(--ink);border-radius:14px;background:var(--panel)}
.box h2{margin-top:0}
.list a{display:block;padding:18px 0;border-bottom:1px solid var(--rule);text-decoration:none}
.list a strong{display:block;font-size:20px}.list a span{color:var(--soft);font-size:16px}
footer{margin-top:56px;color:var(--soft);font-size:15px}"""

HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="{ogtype}"><meta property="og:url" content="{url}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
{ld}
<style>{css}</style></head><body><div class="wrap">
<header class="top"><a class="brand" href="./"><i aria-hidden="true"></i>Ship-Ready Check</a><a class="cta" href="./#pricing">Check my app</a></header>
<main>
"""
FOOT = """</main>
<footer><a href="guides.html">More guides</a> · <a href="./">Ship-Ready Check</a> · <a href="terms.html">Terms</a></footer>
</div></body></html>"""


def parse(md_text):
    m = re.match(r"---\n(.*?)\n---\n", md_text, re.S)
    meta = dict(line.split(": ", 1) for line in m.group(1).splitlines())
    return meta, md_text[m.end():]


guides = []
for f in sorted((BUILD / "guides").glob("*.md")):
    meta, body = parse(f.read_text())
    url = f"{SITE}/{meta['slug']}.html"
    body_html = markdown.markdown(body, extensions=["tables", "fenced_code"])
    # turn the closing section into a highlighted box
    body_html = re.sub(r"(<h2>Want (?:someone to check it for you\?|a second pair of eyes\?)</h2>.*)$",
                       r'<div class="box">\1</div>', body_html, flags=re.S)
    # add a dated byline under the H1
    upd = datetime.date.fromisoformat(meta["updated"])
    body_html = body_html.replace("</h1>", f'</h1>\n<p class="meta">Ship-Ready Check · Updated {upd.strftime("%B %-d, %Y")}</p>', 1)
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": meta["title"],
          "description": meta["description"], "dateModified": meta["updated"],
          "author": {"@type": "Organization", "name": "Ship-Ready Check", "url": SITE},
          "mainEntityOfPage": url}
    page = HEAD.format(title=html.escape(meta["title"]), desc=html.escape(meta["description"]), url=url,
                       ogtype="article", css=CSS,
                       ld=f'<script type="application/ld+json">{json.dumps(ld)}</script>') + body_html + FOOT
    (ROOT / f"{meta['slug']}.html").write_text(page)
    guides.append((meta, url))
    print("wrote", meta["slug"])

# index
items = "\n".join(f'<a href="{m["slug"]}.html"><strong>{html.escape(m["title"])}</strong><span>{html.escape(m["description"])}</span></a>' for m, _ in guides)
idx = HEAD.format(title="Security guides for AI-built apps | Ship-Ready Check",
                  desc="Plain-English guides to the security mistakes AI coding tools make: exposed keys, open Supabase databases, unverified Stripe payments.",
                  url=f"{SITE}/guides.html", ogtype="website", css=CSS, ld="") + \
      '<h1>Security guides for AI-built apps</h1>\n<p class="meta">Plain-English fixes for the mistakes Lovable, Bolt, Cursor and Claude Code make most.</p>\n<div class="list">' + items + "</div>" + FOOT
(ROOT / "guides.html").write_text(idx)

# sitemap + robots
latest = max(m["updated"] for m, _ in guides)
pages = [("", latest), ("guides.html", latest), ("checklist.html", "2026-10-15"), ("sample-report.html", "2026-10-15")] + [(f"{m['slug']}.html", m["updated"]) for m, _ in guides]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
     "\n".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{d}</lastmod></url>" for p, d in pages) + "\n</urlset>\n"
(ROOT / "sitemap.xml").write_text(sm)
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /thanks.html\n\nSitemap: {SITE}/sitemap.xml\n")
print("wrote guides.html, sitemap.xml, robots.txt")

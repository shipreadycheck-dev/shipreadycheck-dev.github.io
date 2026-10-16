#!/usr/bin/env python3
"""Quality gate. Run from the website repo root AFTER building:
    python3 _build/check_site.py
Exits non-zero (and prints every failure) if anything is wrong. Nothing publishes on failure."""
import pathlib, re, sys, html.parser, xml.dom.minidom

BUILD = pathlib.Path(__file__).resolve().parent
ROOT = BUILD.parent
fails, warns = [], []


def fail(msg): fails.append(msg)
def warn(msg): warns.append(msg)


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.h1 = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and "href" in a: self.links.append(a["href"])
        if tag == "h1": self.h1 += 1


# 1. Guide sources
slugs, titles = set(), set()
for f in sorted((BUILD / "guides").glob("*.md")):
    text = f.read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail(f"{f.name}: missing front matter"); continue
    meta = dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l)
    body = text[m.end():]
    for k in ("title", "description", "slug", "updated"):
        if not meta.get(k): fail(f"{f.name}: front matter missing '{k}'")
    slug = meta.get("slug", "")
    if f.stem != slug: fail(f"{f.name}: file name must equal slug '{slug}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug or "x"): fail(f"{f.name}: slug must be lowercase-with-dashes")
    if slug in slugs: fail(f"{f.name}: duplicate slug")
    slugs.add(slug)
    t = meta.get("title", "")
    if t.lower() in titles: fail(f"{f.name}: duplicate title")
    titles.add(t.lower())
    if len(t) > 90: fail(f"{f.name}: title too long ({len(t)} > 90)")
    d = meta.get("description", "")
    if not 90 <= len(d) <= 200: fail(f"{f.name}: description should be 90-200 chars (is {len(d)})")
    words = len(re.findall(r"\b\w+\b", body))
    if not 600 <= words <= 1800: fail(f"{f.name}: {words} words (need 600-1800)")
    if "—" in text: fail(f"{f.name}: contains an em dash")
    if "{{" in text or "TODO" in text or "lorem" in text.lower(): fail(f"{f.name}: placeholder text left in")
    ext = set(re.findall(r"\]\((https?://[^)\s]+)\)", body))
    ext = {u for u in ext if "shipreadycheck-dev" not in u}
    if len(ext) < 2: fail(f"{f.name}: needs at least 2 external sources (has {len(ext)})")
    if "shipreadycheck-dev.github.io/#pricing" not in body: fail(f"{f.name}: missing link to the paid check")
    if not re.search(r"^## Want ", body, re.M): fail(f"{f.name}: missing the closing 'Want ...' section")
    if not body.lstrip().startswith("# "): fail(f"{f.name}: must start with a single H1")
    if len(re.findall(r"^# ", body, re.M)) != 1: fail(f"{f.name}: must have exactly one H1")
    if re.search(r"\b(guarantee[sd]?|100% secure|bulletproof|unhackable)\b", body, re.I) and "not a guarantee" not in body.lower() and "does not mean" not in body.lower():
        warn(f"{f.name}: check wording around guarantees")

# 2. Built HTML pages: every internal link must resolve, one H1, no placeholders
pages = [p for p in ROOT.glob("*.html") if not p.name.startswith("google")]
for p in pages:
    s = p.read_text()
    lp = LinkParser(); lp.feed(s)
    if p.name not in ("thanks.html",) and lp.h1 != 1: fail(f"{p.name}: has {lp.h1} H1 tags (need 1)")
    if "{{" in s: fail(f"{p.name}: unfilled placeholder")
    for href in lp.links:
        if href.startswith(("http://", "https://", "mailto:", "#")): continue
        target = href.split("#")[0]
        if target in ("", "./"): continue
        if not (ROOT / target).exists(): fail(f"{p.name}: broken link -> {href}")
for slug in slugs:
    if not (ROOT / f"{slug}.html").exists(): fail(f"{slug}.html was not built")
    elif f'href="{slug}.html"' not in (ROOT / "guides.html").read_text(): fail(f"{slug} missing from guides.html")

# 3. Sitemap
try:
    sm = xml.dom.minidom.parse(str(ROOT / "sitemap.xml"))
    locs = [n.firstChild.data for n in sm.getElementsByTagName("loc")]
    for slug in slugs:
        if not any(l.endswith(f"/{slug}.html") for l in locs): fail(f"sitemap.xml missing {slug}")
except Exception as e:
    fail(f"sitemap.xml invalid: {e}")

# 4. Never touch these
for must in ("index.html", "thanks.html", "terms.html", "checklist.html", "sample-report.html", "starter-kit.zip", "robots.txt"):
    if not (ROOT / must).exists(): fail(f"{must} is missing from the site")
if not list(ROOT.glob("google*.html")): fail("Google verification file is missing (never delete it)")

for w in warns: print("WARN:", w)
if fails:
    print(f"FAILED {len(fails)} check(s):")
    for x in fails: print(" -", x)
    sys.exit(1)
print(f"PASSED: {len(slugs)} guides, {len(pages)} pages checked.")

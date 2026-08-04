#!/usr/bin/env python3
"""
Phase 1b — turn the raw WordPress dump into the S3 database layout.

Reads  ./raw/*.json          (produced by fetch_wp.py)
Writes ./out/db/lovemesomecoding/{env}/...
       ./out/reports/*.json  (verification artifacts)

Transformations applied to post/page HTML:
  1. EnlighterJS <pre class="EnlighterJSRAW" data-enlighter-language="java">
       -> <pre><code class="language-java">   (Prism/Shiki-compatible)
  2. wp-content/uploads URLs -> media CDN, with WordPress' auto-generated resized
     variants (foo-300x200.png) collapsed back to the original (foo.png).
  3. Absolute lovemesomecoding.com post links -> site-relative.
  4. Sanitize: drop <script> and on* handlers that sit OUTSIDE <pre>. Everything
     inside <pre> is a code sample and is preserved verbatim.
  5. Stable ids injected on h2/h3 so a table of contents can deep-link.

    python3 transform.py [--env prod]
"""

import argparse
import html
import json
import os
import re
import unicodedata
from collections import Counter, defaultdict

from bs4 import BeautifulSoup, NavigableString

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "out")

SITE = "lovemesomecoding.com"
APP = "lovemesomecoding"

# Filled from --media-cdn; placeholder until the CloudFront distro exists (Phase 0).
MEDIA_BASE = "{{MEDIA_CDN}}"

# EnlighterJS language ids -> Prism language ids
LANG_MAP = {
    "java": "java", "python": "python", "shell": "bash", "bash": "bash",
    "html": "markup", "xml": "markup", "sql": "sql", "js": "javascript",
    "javascript": "javascript", "css": "css", "powershell": "powershell",
    "yaml": "yaml", "json": "json", "markdown": "markdown", "groovy": "groovy",
    "kotlin": "kotlin", "dockerfile": "docker", "generic": "plaintext",
    "raw": "plaintext", "": "plaintext",
}

# WordPress resize suffix: foo-1024x463.jpeg -> foo.jpeg
VARIANT_RE = re.compile(r"-\d+x\d+(?=\.\w+$)")
UPLOADS_RE = re.compile(
    r"https?://(?:www\.)?" + re.escape(SITE) + r"/wp-content/uploads/([^\s\"'\)\\]+)"
)
INTERNAL_RE = re.compile(r"https?://(?:www\.)?" + re.escape(SITE) + r"(/[^\s\"'\)\\]*)?")

stats = Counter()


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text) or "section"


def media_key(path):
    """uploads-relative path -> key under the storage bucket, variants collapsed."""
    return "media/" + VARIANT_RE.sub("", path)


def rewrite_urls(text):
    def _upload(m):
        stats["url_media_rewritten"] += 1
        return f"{MEDIA_BASE}/{media_key(m.group(1))}"

    text = UPLOADS_RE.sub(_upload, text)

    def _internal(m):
        stats["url_internal_rewritten"] += 1
        return m.group(1) or "/"

    return INTERNAL_RE.sub(_internal, text)


PRE_RE = re.compile(r"<pre\b([^>]*)>(.*?)</pre>", re.S | re.I)
LANG_ATTR_RE = re.compile(r'data-enlighter-language="([^"]*)"', re.I)
CODE_WRAP_RE = re.compile(r"^\s*<code\b[^>]*>(.*)</code>\s*$", re.S | re.I)
COMMENT_BANNER_RE = re.compile(r"<!--.*?-->", re.S)


def extract_code_blocks(raw_html):
    """Pull <pre> regions out BEFORE any HTML parsing.

    Post bodies contain raw, unescaped HTML/CSS samples inside <pre> (e.g. a Java
    text block holding <button onclick=...> and <script>). An HTML parser treats
    those as real elements and get_text() then silently deletes the markup, so the
    sample renders as bare words. Stashing the regions verbatim and reinserting
    them escaped is the only way to preserve them.
    """
    blocks = []

    def _stash(m):
        attrs, inner = m.group(1), m.group(2)
        lang = (LANG_ATTR_RE.search(attrs) or [None, ""])[1] if LANG_ATTR_RE.search(attrs) else ""
        # peel a wrapping <code> so we don't double-nest
        cw = CODE_WRAP_RE.match(inner)
        if cw:
            inner = cw.group(1)
        blocks.append((LANG_MAP.get(lang.lower(), "plaintext"), html.unescape(inner)))
        return f"<pre data-codeblock=\"{len(blocks) - 1}\"></pre>"

    return PRE_RE.sub(_stash, raw_html), blocks


def restore_code_blocks(text, blocks):
    def _put(m):
        prism, source = blocks[int(m.group(1))]
        stats["code_blocks"] += 1
        stats[f"code_block_{prism}"] += 1
        return (f'<pre class="language-{prism}"><code class="language-{prism}">'
                f"{html.escape(source, quote=False)}</code></pre>")

    return re.sub(r'<pre data-codeblock="(\d+)"></pre>', _put, text)


TITLE_ATTR_RE = re.compile(r'(\stitle=")([^"]*)(")')


def repair_attributes(text):
    """Escape raw angle brackets inside title="..." values.

    One post (css-applying-css) has MDN tooltip text pasted in with unescaped tags
    — title="The HTML <style> element ...". That terminates attribute parsing, so
    the parser treats <style> as real and eats the following prose. WordPress
    mis-renders it today for the same reason.
    """
    def _fix(m):
        val = m.group(2)
        if "<" not in val and ">" not in val:
            return m.group(0)
        stats["attr_repaired"] += 1
        return m.group(1) + val.replace("<", "&lt;").replace(">", "&gt;") + m.group(3)

    return TITLE_ATTR_RE.sub(_fix, text)


def transform_html(raw_html):
    """Returns (clean_html, toc, plain_text)."""
    stashed, blocks = extract_code_blocks(raw_html)
    stashed = COMMENT_BANNER_RE.sub("", stashed)  # drop authoring banner comments
    stashed = repair_attributes(stashed)
    soup = BeautifulSoup(stashed, "lxml")

    # --- 4. sanitize (code blocks are already stashed out of reach) ------
    for tag in soup.find_all("script"):
        if not tag.find_parent("pre"):
            tag.decompose()
            stats["script_stripped"] += 1
    for tag in soup.find_all(True):
        if tag.find_parent("pre"):
            continue
        for attr in [a for a in tag.attrs if a.lower().startswith("on")]:
            del tag[attr]
            stats["onevent_stripped"] += 1

    # --- 5. heading ids + table of contents ------------------------------
    toc, seen = [], set()
    for h in soup.find_all(["h2", "h3"]):
        title = h.get_text(strip=True)
        if not title:
            continue
        base = slugify(title)
        hid, n = base, 2
        while hid in seen:
            hid, n = f"{base}-{n}", n + 1
        seen.add(hid)
        h["id"] = hid
        toc.append({"id": hid, "text": title, "level": int(h.name[1])})

    # --- responsive tables ----------------------------------------------
    for table in soup.find_all("table"):
        classes = set(table.get("class") or [])
        table["class"] = list(classes | {"table", "table-bordered"})
        stats["tables"] += 1

    body = soup.body or soup
    clean = "".join(str(c) for c in body.children)
    # URL rewriting runs while code blocks are still stashed, so sample code is
    # never touched — only real links and images are.
    clean = rewrite_urls(clean)
    clean = restore_code_blocks(clean, blocks)

    prose = soup.get_text(" ", strip=True)
    code_text = " ".join(src for _, src in blocks)
    return clean, toc, f"{prose} {code_text}".strip()


def plain(text, limit=None):
    text = html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()
    text = re.sub(r"\s+", " ", text)
    if limit and len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text


def write_json(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="prod", choices=["local", "prod"])
    ap.add_argument("--media-cdn", default="{{MEDIA_CDN}}",
                    help="media CloudFront base URL (default: placeholder token)")
    args = ap.parse_args()

    globals()["MEDIA_BASE"] = args.media_cdn.rstrip("/")

    load = lambda n: json.load(open(os.path.join(RAW, f"{n}.json"), encoding="utf-8"))
    posts, pages = load("posts"), load("pages")
    cats = {c["id"]: c for c in load("categories")}
    tags = {t["id"]: t for t in load("tags")}

    db = os.path.join(OUT, "db", APP, args.env)
    index, by_cat, search, manifest = [], defaultdict(list), [], []

    for p in posts:
        url_path = p["link"].split(SITE, 1)[1].strip("/")
        cat_slug, slug = url_path.split("/", 1)

        content, toc, text = transform_html(p["content"]["rendered"])
        words = len(text.split())

        record = {
            "slug": slug,
            "wpId": p["id"],
            "title": html.unescape(p["title"]["rendered"]),
            "category": cat_slug,
            "categories": [cats[c]["slug"] for c in p["categories"] if c in cats],
            "tags": [tags[t]["slug"] for t in p["tags"] if t in tags],
            "date": p["date"],
            "modified": p["modified"],
            "excerpt": plain(p["excerpt"]["rendered"], 300),
            "url": f"/{cat_slug}/{slug}",
            "contentHtml": content,
            "toc": toc,
            "wordCount": words,
            "readingMinutes": max(1, round(words / 220)),
            "status": "published",
        }
        write_json(os.path.join(db, "posts", f"{slug}.json"), record)

        summary = {k: record[k] for k in
                   ("slug", "title", "category", "tags", "date", "modified",
                    "excerpt", "url", "readingMinutes")}
        index.append(summary)
        by_cat[cat_slug].append(summary)
        search.append({"u": record["url"], "t": record["title"],
                       "c": cat_slug, "x": record["excerpt"][:180]})
        manifest.append({"old": p["link"], "new": record["url"]})
        stats["posts"] += 1

    for pg in pages:
        slug = pg["link"].split(SITE, 1)[1].strip("/")
        content, toc, text = transform_html(pg["content"]["rendered"])
        write_json(os.path.join(db, "pages", f"{slug.replace('/', '__')}.json"), {
            "slug": slug,
            "wpId": pg["id"],
            "title": html.unescape(pg["title"]["rendered"]),
            "url": f"/{slug}",
            "date": pg["date"], "modified": pg["modified"],
            "contentHtml": content, "toc": toc, "status": "published",
        })
        manifest.append({"old": pg["link"], "new": f"/{slug}"})
        stats["pages"] += 1

    index.sort(key=lambda r: r["date"], reverse=True)
    write_json(os.path.join(db, "index", "posts.json"), index)

    cat_index = []
    for cid, c in cats.items():
        items = sorted(by_cat.get(c["slug"], []), key=lambda r: r["date"], reverse=True)
        if not items:
            stats["empty_categories"] += 1
            continue
        write_json(os.path.join(db, "index", "by-category", f"{c['slug']}.json"), items)
        cat_index.append({
            "slug": c["slug"],
            "name": html.unescape(c["name"]),
            "description": plain(c.get("description", "")),
            "count": len(items),
            "url": f"/{c['slug']}",
        })
    cat_index.sort(key=lambda c: -c["count"])
    write_json(os.path.join(db, "index", "categories.json"), cat_index)
    write_json(os.path.join(db, "search", "index.json"), search)
    write_json(os.path.join(db, "redirects.json"), {
        "/wp-sitemap.xml": "/sitemap.xml",
        "/feed": "/rss.xml",
        "/feed/": "/rss.xml",
    })

    # ---- verification artifacts ----
    reports = os.path.join(OUT, "reports")
    write_json(os.path.join(reports, "url_manifest.json"), manifest)
    write_json(os.path.join(reports, "transform_stats.json"), dict(stats))

    referenced = set()
    for p in posts + pages:
        for m in UPLOADS_RE.finditer(p["content"]["rendered"]):
            referenced.add(VARIANT_RE.sub("", m.group(1)))
    write_json(os.path.join(reports, "media_needed.json"), sorted(referenced))

    print(f"posts:      {stats['posts']}")
    print(f"pages:      {stats['pages']}")
    print(f"categories: {len(cat_index)} non-empty ({stats['empty_categories']} empty skipped)")
    print(f"code blocks:{stats['code_blocks']}  tables:{stats['tables']}")
    print(f"urls rewritten: media={stats['url_media_rewritten']} internal={stats['url_internal_rewritten']}")
    print(f"sanitized: scripts={stats['script_stripped']} on*={stats['onevent_stripped']}")
    print(f"distinct original images needed: {len(referenced)}")
    print(f"\nwrote -> {db}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Prove the normaliser round-trips every code sample byte-for-byte.

The migration nearly shipped corrupted code blocks because an HTML parser ate the
raw <script>/<style>/onclick= that legitimately appear *inside* code samples, and
the damage barely changed the character count — so length checks passed. Compare
sources, not lengths. No AWS access needed.

Also checks the things that are cheap here and expensive to notice on the live
site: duplicate slugs, ascending dates, and cross-post links that point at a slug
nothing in this track defines.

    python projects/leetcode/check_content.py
"""

import html
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent.parent / "lovemesomecoding_backend"

os.environ.setdefault("env", "test")
os.environ.setdefault("data_env", "test")
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(HERE))

import manifest  # noqa: E402
from app.services import content as content_service  # noqa: E402

SOURCE_PRE = re.compile(r'<pre\b([^>]*)>(.*?)</pre>', re.S | re.I)
OUT_PRE = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-[\w-]+">(.*?)</code></pre>', re.S)
INNER_CODE = re.compile(r'^\s*<code\b[^>]*>(.*)</code>\s*$', re.S | re.I)
INTERNAL_LINK = re.compile(r'href="(/[^"#]*)', re.I)

# Exactly what the frontend's build-time highlighter matches. If the shape
# changes on either side, highlighting silently stops.
FRONTEND_SHAPE = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-\1">', re.S)

CATEGORY = manifest.CATEGORY["slug"]
KNOWN_SLUGS = {e["slug"] for e in manifest.POSTS}

failures = []
total_blocks = 0

# Manifest-level checks first — a duplicate slug silently overwrites a post.
if len(KNOWN_SLUGS) != len(manifest.POSTS):
    failures.append("duplicate slug in the manifest")

# Ordering only applies to the LeetCode track itself. Legacy rewrites have no
# number and keep their original 2018/2019 dates, so they are exempt: upsert_post
# never reapplies `date` to an existing post, and their position in the archive is
# already fixed.
tracked = [e for e in manifest.POSTS if "number" in e]

dates = [e["date"] for e in tracked]
if dates != sorted(dates):
    failures.append("dates do not ascend with the manifest order; prev/next would zig-zag")

numbers = [e["number"] for e in tracked]
if numbers != sorted(numbers):
    failures.append("LeetCode numbers are out of order in the manifest")

for entry in manifest.POSTS:
    raw = (HERE / "posts" / entry["file"]).read_text(encoding="utf-8")

    # The code samples as authored.
    authored = []
    for attrs, inner in SOURCE_PRE.findall(raw):
        wrapped = INNER_CODE.match(inner)
        if wrapped:
            inner = wrapped.group(1)
        authored.append(html.unescape(inner))

    result = content_service.normalize(raw)
    emitted = [html.unescape(body) for _lang, body in OUT_PRE.findall(result["contentHtml"])]
    langs = [lang for lang, _ in OUT_PRE.findall(result["contentHtml"])]

    total_blocks += len(authored)

    if len(authored) != len(emitted):
        failures.append(f"{entry['slug']}: {len(authored)} blocks in, {len(emitted)} out")
        continue

    for i, (before, after) in enumerate(zip(authored, emitted)):
        if before != after:
            failures.append(
                f"{entry['slug']} block {i} ({langs[i]}) changed:\n"
                f"    in : {before[:160]!r}\n    out: {after[:160]!r}")

    unsupported = [l for l in langs if l == "plaintext"]
    shaped = len(FRONTEND_SHAPE.findall(result["contentHtml"]))
    if shaped != len(emitted):
        failures.append(f"{entry['slug']}: {len(emitted)} blocks but {shaped} match "
                        "the shape the frontend highlighter expects")

    # A heading with no id would break the table of contents' deep links.
    missing_ids = [t for t in result["toc"] if not t.get("id")]
    if missing_ids:
        failures.append(f"{entry['slug']}: {len(missing_ids)} heading(s) with no anchor")

    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")

    # A link into this track must name a post this track actually defines.
    # The frontend build fails on a dead post URL, but only for indexed ones —
    # a typo here would ship a 404 nobody notices.
    for href in INTERNAL_LINK.findall(raw):
        if href.startswith(f"/{CATEGORY}/"):
            target = href[len(CATEGORY) + 2:].rstrip("/")
            if target not in KNOWN_SLUGS:
                failures.append(f"{entry['slug']}: links to {href}, which this track "
                                "does not define")

    print(f"{entry['slug']:46} {result['wordCount']:>5} words  "
          f"{result['readingMinutes']:>2} min  {len(result['toc']):>2} headings  "
          f"{len(emitted):>2} code blocks ({len(emitted) - len(unsupported)} highlighted)")

print(f"\n{len(manifest.POSTS)} posts, {total_blocks} code blocks")
if failures:
    print("\nFAILED:")
    for f in failures:
        print(f"  x {f}")
    sys.exit(1)
print("every code sample round-trips byte-for-byte")

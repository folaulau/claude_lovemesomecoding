#!/usr/bin/env python3
"""Prove the normaliser round-trips every code sample byte-for-byte.

The migration nearly shipped corrupted code blocks because an HTML parser ate the
raw <script>/<style>/onclick= that legitimately appear *inside* code samples, and
the damage barely changed the character count — so length checks passed. Compare
sources, not lengths. No AWS access needed.

JSX makes this sharper than it was for plain TypeScript: a post body is full of
`<Pressable onPress={…}>` and `{items.map(…)}` inside <pre> blocks, and one
missed &lt; is invisible until it renders.

While the track is being authored, posts with no file yet are reported as
`not written` and do not fail the run. Once every file exists this becomes a
plain pass/fail.

    python projects/react_native/check_content.py
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

# Exactly what the frontend's build-time highlighter matches. If the shape
# changes on either side, highlighting silently stops.
FRONTEND_SHAPE = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-\1">', re.S)

failures = []
missing = []
total_blocks = 0
written = 0

for entry in manifest.POSTS:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        missing.append(entry["slug"])
        print(f"{entry['slug']:44} not written")
        continue
    written += 1
    raw = path.read_text(encoding="utf-8")

    # The code samples as authored.
    authored = []
    for _attrs, inner in SOURCE_PRE.findall(raw):
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

    print(f"{entry['slug']:44} {result['wordCount']:>5} words  "
          f"{result['readingMinutes']:>2} min  {len(result['toc']):>2} headings  "
          f"{len(emitted):>2} code blocks ({len(emitted) - len(unsupported)} highlighted)")

# ------------------------------------------------------- manifest invariants
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest.POSTS")

dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend — the prev/next pager would read out of order")

for entry in manifest.POSTS:
    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")

# The five 2018 URLs are indexed. Their replacements must stay in the manifest,
# or the redirect map generated from OLD_SLUG_REDIRECTS points at nothing.
for old, new in manifest.OLD_SLUG_REDIRECTS.items():
    if new not in slugs:
        failures.append(
            f"{old} redirects to {new}, which is no longer in the manifest — "
            "that would 404 a URL indexed since 2018")

if manifest.CATEGORY["slug"] == manifest.OLD_CATEGORY_SLUG:
    failures.append("CATEGORY slug is still the old typo")

# `sources` is what makes the topic table reviewable. A lesson with none is
# either prose-only on purpose or an oversight; say which.
no_sources = [e["slug"] for e in manifest.POSTS if not e["sources"]]
if no_sources:
    print(f"\nnote: {len(no_sources)} lesson(s) name no demo-app source: "
          f"{', '.join(no_sources)}")

print(f"\n{len(manifest.POSTS)} posts in the manifest, {written} written, "
      f"{len(missing)} still to write, {total_blocks} code blocks")

if failures:
    print("\nFAILED:")
    for f in sorted(set(failures)):
        print(f"  x {f}")
    sys.exit(1)

if missing:
    print("manifest is consistent; every written post round-trips byte-for-byte")
    print(f"NOT READY TO SEED — {len(missing)} post(s) have no file yet")
    sys.exit(0)

print("every code sample round-trips byte-for-byte")

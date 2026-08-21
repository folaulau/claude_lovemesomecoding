#!/usr/bin/env python3
"""Prove the normaliser round-trips every code sample byte-for-byte.

The migration nearly shipped corrupted code blocks because an HTML parser ate the
raw <script>/<style>/onclick= that legitimately appear *inside* code samples, and
the damage barely changed the character count — so length checks passed. Compare
sources, not lengths. No AWS access needed.

A Docker track makes this sharper still. Post bodies quote nginx config full of
`location / { … }`, compose YAML with `${VAR}` interpolation, and shell pipelines
with `<` redirects — all inside <pre> blocks, and one missed &lt; is invisible
until it renders.

While the track is being authored, posts that have no file yet are reported as
`not written` and do not fail the run — the whole track is blocked on the Docker
artifacts being added to the pizza demo app. Once every file exists this becomes
a plain pass/fail.

    python projects/docker_tutorial/check_content.py
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

    print(f"{entry['slug']:44} {result['wordCount']:>5} words  "
          f"{result['readingMinutes']:>2} min  {len(result['toc']):>2} headings  "
          f"{len(emitted):>2} code blocks ({len(emitted) - len(unsupported)} highlighted)")

# Manifest-level invariants worth catching before anything is written.
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest.POSTS")

dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend — the prev/next pager would read out of order")

for frozen in manifest.FROZEN_SLUGS:
    if frozen not in slugs:
        failures.append(f"frozen slug {frozen} is no longer in the manifest — that URL is indexed")

# Lesson 1 carries the track index. A lesson added to the manifest but never
# linked from there is unreachable except through the category archive, and
# nothing else would notice.
INDEX_POST = HERE / "posts" / manifest.POSTS[0]["file"]
if INDEX_POST.exists():
    index_html = INDEX_POST.read_text(encoding="utf-8")
    unlinked = [s for s in slugs
                if f'href="/{manifest.CATEGORY["slug"]}/{s}"' not in index_html]
    if unlinked:
        failures.append(
            f"{manifest.POSTS[0]['slug']} does not link: {', '.join(unlinked)} "
            "— every lesson must appear in the track index")

for entry in manifest.POSTS:
    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")

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

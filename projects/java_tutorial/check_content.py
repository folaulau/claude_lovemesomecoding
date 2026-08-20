#!/usr/bin/env python3
"""Prove the normaliser round-trips every code sample byte-for-byte.

The migration nearly shipped corrupted code blocks because an HTML parser ate the
raw <script>/<style>/onclick= that legitimately appear *inside* code samples, and
the damage barely changed the character count — so length checks passed. Compare
sources, not lengths. No AWS access needed.

    python projects/java_tutorial/check_content.py
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
total_blocks = 0

written = 0
for entry in manifest.POSTS:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        print(f"{entry['slug']:36} .. not written yet")
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

    # The reason this project exists. The track averaged 6,362 words before the
    # trim and README asks twice for posts to be kept to the point, so drifting
    # back over the band is a failure, not a style note.
    lo, hi = manifest.WORD_TARGET
    words = result["wordCount"]
    if words > hi:
        failures.append(f"{entry['slug']}: {words} words, over the {hi} ceiling "
                        f"— cut {words - hi} more")
    elif words < lo:
        failures.append(f"{entry['slug']}: {words} words, under the {lo} floor "
                        f"— thin by {lo - words}")

    # A 59-entry table of contents is a second scroll bar, not a navigation aid.
    # The pre-trim posts ran to 78 headings; 4-10 h2 sections is the shape.
    h2s = [t for t in result["toc"] if t.get("level") == 2]
    if not 4 <= len(h2s) <= 10:
        failures.append(f"{entry['slug']}: {len(h2s)} h2 sections, want 4-10")

    if not entry.get("tags"):
        failures.append(f"{entry['slug']}: no tags (all 28 old posts had none — that is the bug)")

    print(f"{entry['slug']:44} {result['wordCount']:>5} words  "
          f"{result['readingMinutes']:>2} min  {len(result['toc']):>2} headings  "
          f"{len(emitted):>2} code blocks ({len(emitted) - len(unsupported)} highlighted)")

print(f"\n{written}/{len(manifest.POSTS)} posts written, {total_blocks} code blocks, "
      f"target {manifest.WORD_TARGET[0]}-{manifest.WORD_TARGET[1]} words")
if failures:
    print("\nFAILED:")
    for f in failures:
        print(f"  x {f}")
    sys.exit(1)
print("every code sample round-trips byte-for-byte")

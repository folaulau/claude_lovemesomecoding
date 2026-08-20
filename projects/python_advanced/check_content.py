#!/usr/bin/env python3
"""Prove the normaliser round-trips every code sample, and hold the length gates.

Two jobs.

1. **Round-trip.** The migration nearly shipped corrupted code blocks because an
   HTML parser ate the raw <script>/<style>/onclick= that legitimately appear
   *inside* code samples, and the damage barely changed the character count — so
   length checks passed. Compare sources, not lengths.

2. **The gates this track exists for.** Before the rework these eight posts
   averaged 1,889 prose words — over the ceiling — with 22 to 48 code blocks
   each and up to 16 headings, several of them numbered "1." ... "8.", which is
   an index rather than a narrative. All three gates bite on this track.

No AWS access needed.

    python3 projects/python_advanced/check_content.py
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

# Migration residue. One wrapper per post on all 17 today; they carry no styling.
BOLDGRID = re.compile(r'boldgrid|col-md-12 col-xs-12 col-sm-12', re.I)

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

    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")

    # --- the gates ------------------------------------------------------
    lo, hi = manifest.WORD_TARGET
    words = result["wordCount"]
    if words > hi:
        failures.append(f"{entry['slug']}: {words} words, over the {hi} ceiling "
                        f"— cut {words - hi} more")
    elif words < lo:
        failures.append(f"{entry['slug']}: {words} words, under the {lo} floor "
                        f"— thin by {lo - words}")

    # THE check for this track. `python-advanced-virtual-environments-pip`
    # shipped 48 blocks and `python-advanced-numpy-arrays` 37 on 1,210 words of
    # prose. The reworked /python posts run 4-12 blocks.
    if len(emitted) > manifest.CODE_BLOCK_MAX:
        failures.append(
            f"{entry['slug']}: {len(emitted)} code blocks, over the "
            f"{manifest.CODE_BLOCK_MAX} cap — cut {len(emitted) - manifest.CODE_BLOCK_MAX}. "
            "A block per method is the symptom; merge them.")

    # Before the rework: 6 to 16 h2 per post.
    h2_lo, h2_hi = manifest.H2_RANGE
    h2s = [t for t in result["toc"] if t.get("level") == 2]
    if not h2_lo <= len(h2s) <= h2_hi:
        failures.append(f"{entry['slug']}: {len(h2s)} h2 sections, want {h2_lo}-{h2_hi}")

    # Numbered headings are an index, not a narrative — the shape the pre-rework
    # posts had ("1. Creating Lists" ... "11. Stacks and Queues").
    numbered = [t["text"] for t in h2s if re.match(r'^\s*\d+[.)]\s', t.get("text", ""))]
    if numbered:
        failures.append(f"{entry['slug']}: {len(numbered)} numbered h2(s) — "
                        f"name the section instead: {numbered[:3]}")

    # Every post had exactly one tag, the literal string "python". Not zero like
    # /java, but not useful either.
    tags = entry.get("tags") or []
    if len(tags) < 2:
        failures.append(f"{entry['slug']}: {len(tags)} tag(s) — all 8 old posts had "
                        "just \"python\", which is the bug")

    if BOLDGRID.search(raw):
        failures.append(f"{entry['slug']}: boldgrid wrapper survived — strip it")

    print(f"{entry['slug']:36} {result['wordCount']:>5} words  "
          f"{result['readingMinutes']:>2} min  {len(h2s):>2} h2  "
          f"{len(emitted):>2}/{manifest.CODE_BLOCK_MAX} blocks "
          f"({len(emitted) - len(unsupported)} highlighted)  {len(tags)} tags")

print(f"\n{written}/{len(manifest.POSTS)} posts written, {total_blocks} code blocks")
print(f"gates: {manifest.WORD_TARGET[0]}-{manifest.WORD_TARGET[1]} words, "
      f"<={manifest.CODE_BLOCK_MAX} code blocks, "
      f"{manifest.H2_RANGE[0]}-{manifest.H2_RANGE[1]} h2, >=2 tags")
if failures:
    print("\nFAILED:")
    for f in failures:
        print(f"  x {f}")
    sys.exit(1)
print("every code sample round-trips byte-for-byte and every gate holds")

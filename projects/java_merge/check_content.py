#!/usr/bin/env python3
"""Round-trip + length + shape checks for the rewritten posts in this merge.

Only posts that have been rewritten (a file in posts/) are checked. The rest are
moving as-is and are not this project's content.

    python projects/java_merge/check_content.py
"""
import html, os, re, sys
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
FRONTEND_SHAPE = re.compile(r'<pre class="language-([\w-]+)"><code class="language-\1">', re.S)

failures, written, total_blocks, total_words = [], 0, 0, 0

for entry in manifest.POSTS:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        continue
    written += 1
    raw = path.read_text(encoding="utf-8")

    authored = []
    for _attrs, inner in SOURCE_PRE.findall(raw):
        m = INNER_CODE.match(inner)
        authored.append(html.unescape(m.group(1) if m else inner))

    result = content_service.normalize(raw)
    emitted = [html.unescape(b) for _l, b in OUT_PRE.findall(result["contentHtml"])]
    langs = [l for l, _ in OUT_PRE.findall(result["contentHtml"])]
    total_blocks += len(authored)
    total_words += result["wordCount"]

    if len(authored) != len(emitted):
        failures.append(f"{entry['slug']}: {len(authored)} blocks in, {len(emitted)} out")
        continue
    for i, (before, after) in enumerate(zip(authored, emitted)):
        if before != after:
            failures.append(f"{entry['slug']} block {i} ({langs[i]}) changed:\n"
                            f"    in : {before[:160]!r}\n    out: {after[:160]!r}")

    if len(FRONTEND_SHAPE.findall(result["contentHtml"])) != len(emitted):
        failures.append(f"{entry['slug']}: a block does not match the highlighter's shape")

    if any(not t.get("id") for t in result["toc"]):
        failures.append(f"{entry['slug']}: heading with no anchor")

    lo, hi = manifest.WORD_TARGET
    w = result["wordCount"]
    if w > hi:
        failures.append(f"{entry['slug']}: {w} words, over the {hi} ceiling — cut {w - hi} more")
    elif w < lo:
        failures.append(f"{entry['slug']}: {w} words, under the {lo} floor — thin by {lo - w}")

    h2s = [t for t in result["toc"] if t.get("level") == 2]
    if not 4 <= len(h2s) <= 10:
        failures.append(f"{entry['slug']}: {len(h2s)} h2 sections, want 4-10")

    if 'boldgrid' in raw:
        failures.append(f"{entry['slug']}: still carries WordPress boldgrid wrappers")

    if not entry.get("tags"):
        failures.append(f"{entry['slug']}: no tags")

    print(f"{entry['slug']:52} {result['wordCount']:>5}w {result['readingMinutes']:>2}m "
          f"{len(h2s):>2}h2 {len(emitted):>2} code")

remaining = len(manifest.POSTS) - written
print(f"\n{written} rewritten ({total_words:,} words, {total_blocks} code blocks); "
      f"{remaining} not yet rewritten")
if failures:
    print(f"\nFAILED ({len(failures)}):")
    for f in failures:
        print(f"  x {f}")
    sys.exit(1)
print("every rewritten post round-trips and fits the band")

#!/usr/bin/env python3
"""Prove every post round-trips through the content pipeline, and enforce this track's rules.

Adapted from projects/system_design/check_content.py, minus the parts that only apply to code
tracks (snippet provenance, measured figures, language support). What stays:

  1. Every <pre> block survives normalisation byte for byte, in the shape the frontend
     highlighter expects. Compare sources, not lengths (see the root CLAUDE.md).
  2. Every heading gets an anchor, so the table of contents works.
  3. Every post fits the 6-12 minute budget. The pipeline counts prose AND code together.
  4. Every post has at least one plaintext block (a skeleton, worksheet or question list).
  5. Manifest dates ascend and no excerpt is over 500 characters.
  6. Every story fact a post states is in STORY_FACTS. The sample answers are built from real
     projects, and a number that drifted in retelling is how a true story becomes a false one.

    python projects/behavioral_questions/check_content.py
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

SOURCE_PRE = re.compile(r"<pre\b([^>]*)>(.*?)</pre>", re.S | re.I)
OUT_PRE = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-[\w-]+">(.*?)</code></pre>', re.S)
INNER_CODE = re.compile(r"^\s*<code\b[^>]*>(.*)</code>\s*$", re.S | re.I)
FRONTEND_SHAPE = re.compile(r'<pre class="language-([\w-]+)"><code class="language-\1">')
TAGS = re.compile(r"<[^>]+>")

# Rule 6. Each key is a figure the sample answers quote; each value is where it is recorded. A post
# that contains the key must be telling the story the source records, and check_content cannot
# judge that, but it CAN make sure every quoted figure is one of these and that the source file
# still contains it.
REPO = HERE.parent.parent
STORY_FACTS = {
    # projects/rewrite/progress_report.md
    "512": "projects/rewrite/progress_report.md",
    "568": "projects/rewrite/progress_report.md",
    "5,152": "projects/rewrite/progress_report.md",
    "336": "projects/rewrite/progress_report.md",
    "$25": "projects/rewrite/progress_report.md",
    # projects/oracle/progress_report.md
    "12 tutorials": "projects/oracle/progress_report.md",
    "4101 bytes": "projects/oracle/progress_report.md",
    # the root CLAUDE.md (current monthly cost)
    "$0.60": "CLAUDE.md",
    # projects/system_design/manifest.py (the rule that was wrong)
    "2,871": "projects/system_design/manifest.py",
    "5,742": "projects/system_design/manifest.py",
    # stories/sidecar-health.md (Folau's own account of the Sidecar Health project)
    "40%": "projects/behavioral_questions/stories/sidecar-health.md",
    "MySQL 5.7": "projects/behavioral_questions/stories/sidecar-health.md",
    "team of three": "projects/behavioral_questions/stories/sidecar-health.md",
    # projects/rds-mysql-84-upgrade/progress_report.md
    "8.0.43": "projects/rds-mysql-84-upgrade/progress_report.md",
    "8.4.10": "projects/rds-mysql-84-upgrade/progress_report.md",
    "48 parameters": "projects/rds-mysql-84-upgrade/progress_report.md",
}
# The source files store some figures unformatted ("5152", "4101 bytes"). Map the post's
# spelling to the string the source actually contains.
SOURCE_SPELLING = {"5,152": "5152"}

failures, missing, written = [], [], 0

print(f"{'slug':<40} {'words':>6} {'min':>4} {'hd':>3} {'blk':>4}")
print("-" * 64)

for entry in manifest.POSTS:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        missing.append(entry["slug"])
        continue
    written += 1
    raw = path.read_text(encoding="utf-8")

    authored = []
    for _attrs, inner in SOURCE_PRE.findall(raw):
        wrapped = INNER_CODE.match(inner)
        authored.append(html.unescape(wrapped.group(1) if wrapped else inner))

    result = content_service.normalize(raw)
    body = result["contentHtml"]
    pairs = OUT_PRE.findall(body)
    emitted = [html.unescape(b) for _lang, b in pairs]
    langs = [lang for lang, _ in pairs]

    if len(authored) != len(emitted):
        failures.append(f"{entry['slug']}: {len(authored)} blocks in, {len(emitted)} out")
        continue
    for i, (before, after) in enumerate(zip(authored, emitted)):
        if before != after:
            failures.append(f"{entry['slug']} block {i} changed:\n    in : {before[:120]!r}\n"
                            f"    out: {after[:120]!r}")
    if len(FRONTEND_SHAPE.findall(body)) != len(emitted):
        failures.append(f"{entry['slug']}: a block does not match the highlighter's shape")

    if any(not t.get("id") for t in result["toc"]):
        failures.append(f"{entry['slug']}: a heading has no anchor")

    words = result["wordCount"]
    if words > manifest.TOTAL_WORDS_MAX:
        failures.append(f"{entry['slug']}: {words} words = {result['readingMinutes']} min, over "
                        f"the {manifest.TOTAL_WORDS_MAX}-word cap")
    elif words < manifest.TOTAL_WORDS_MIN:
        failures.append(f"{entry['slug']}: {words} words, under the "
                        f"{manifest.TOTAL_WORDS_MIN}-word floor")

    if langs.count("plaintext") < manifest.MIN_PLAINTEXT_BLOCKS:
        failures.append(f"{entry['slug']}: no plaintext block (skeleton, worksheet or list)")

    text = html.unescape(TAGS.sub(" ", body))
    for fact, source in STORY_FACTS.items():
        if fact in text:
            source_text = (REPO / source).read_text(encoding="utf-8")
            if SOURCE_SPELLING.get(fact, fact) not in source_text:
                failures.append(f"{entry['slug']}: quotes {fact!r}, which {source} no longer "
                                "contains — check the story against the record")

    print(f"{entry['slug']:<40} {words:>6} {result['readingMinutes']:>4} "
          f"{len(result['toc']):>3} {len(emitted):>4}")

dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend")
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest")
for entry in manifest.POSTS:
    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")

for slug in missing:
    print(f"  not written: {slug}")
if failures:
    print(f"\n{len(failures)} FAILURE(S):")
    for f in failures:
        print(f"  ✗ {f}")
    sys.exit(1)
print(f"\nall {written} written post(s) pass" + (f"; {len(missing)} to write." if missing else "."))

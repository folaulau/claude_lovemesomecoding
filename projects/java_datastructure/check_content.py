#!/usr/bin/env python3
"""Prove the normaliser round-trips every code sample byte-for-byte.

The migration nearly shipped corrupted code blocks because an HTML parser ate the
raw <script>/<style>/onclick= that legitimately appear *inside* code samples, and
the damage barely changed the character count — so length checks passed. Compare
sources, not lengths. No AWS access needed.

    python projects/java_datastructure/check_content.py
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

    print(f"{entry['slug']:44} {result['wordCount']:>5} words  "
          f"{result['readingMinutes']:>2} min  {len(result['toc']):>2} headings  "
          f"{len(emitted):>2} code blocks ({len(emitted) - len(unsupported)} highlighted)")


# ---------------------------------------------------------------- snippet fidelity
#
# Every Java snippet in an implementation post has to come from a real file under src/dsa/,
# because those are what tests/run.sh actually compiles and runs. A snippet that has drifted
# from its source is a published sample nothing verifies - the exact failure this track exists
# to avoid.
#
# Posts with `source: None` are conceptual (Big O, memory, and so on). Their Java is small and
# illustrative rather than lifted from an implementation, so it cannot be checked this way.
# Those lines are COUNTED AND REPORTED rather than silently skipped, so "unverified" stays
# visible instead of quietly reading as "verified".
#
# Comments are ignored - a post often carries a tighter comment than the source - and so are
# elided or very short lines. What is compared is the substantive code.
SRC = HERE / "src" / "dsa"
JAVA_OUT = re.compile(
    r'<pre class="language-java"><code class="language-java">(.*?)</code></pre>', re.S)

# Checked against EVERY source, not just the post's named one: posts legitimately quote a
# neighbour to make a comparison (greedy against dynamic programming, for instance).
CORPUS = " ".join(
    re.sub(r"\s+", " ", re.sub(r"//.*$", "", f.read_text(encoding="utf-8"), flags=re.M))
    for f in sorted(SRC.glob("*.java")))


def substantive(line):
    stripped = re.sub(r"//.*$", "", line).strip()
    if len(stripped) < 25 or stripped.startswith(("*", "/*", "#")) or "..." in stripped:
        return None
    return re.sub(r"\s+", " ", stripped)


verified_lines = 0
illustrative_lines = 0
illustrative_posts = []

for entry in manifest.POSTS:
    source_name = entry.get("source")
    raw = (HERE / "posts" / entry["file"]).read_text(encoding="utf-8")
    java_blocks = JAVA_OUT.findall(content_service.normalize(raw)["contentHtml"])
    if not java_blocks:
        continue

    if source_name and not (SRC / f"{source_name}.java").exists():
        failures.append(f"{entry['slug']}: source {source_name}.java does not exist")
        continue

    allowed = {re.sub(r"\s+", " ", line.strip()) for line in entry.get("illustrative", ())}
    allowed_used = set()

    for block in java_blocks:
        for line in html.unescape(block).splitlines():
            needle = substantive(line)
            if needle is None:
                continue
            if not source_name:
                illustrative_lines += 1
                continue
            if needle in allowed:
                # Declared in the manifest as deliberately not from src/dsa - a generic
                # one-liner used to make a point, not an implementation. Listing them
                # explicitly keeps the exception auditable instead of letting the check
                # quietly weaken.
                allowed_used.add(needle)
                illustrative_lines += 1
                continue
            verified_lines += 1
            if needle not in CORPUS:
                failures.append(
                    f"{entry['slug']}: Java line is not in src/dsa/ and is not declared "
                    f"in `illustrative` -> {needle[:90]}")

    # A stale allowance is a check that has quietly stopped checking something.
    for unused in sorted(allowed - allowed_used):
        failures.append(
            f"{entry['slug']}: `illustrative` lists a line that is not in the post -> {unused[:80]}")

    if not source_name:
        illustrative_posts.append(entry["slug"])

print()
print(f"{verified_lines} Java lines verified against src/dsa/")
if illustrative_lines:
    print(f"{illustrative_lines} illustrative Java lines NOT source-checked, in: "
          + ", ".join(illustrative_posts))
print(f"{len(manifest.POSTS)} posts, {total_blocks} code blocks")
if failures:
    print("\nFAILED:")
    for f in failures:
        print(f"  x {f}")
    sys.exit(1)
print("every code sample round-trips byte-for-byte and matches src/dsa/")

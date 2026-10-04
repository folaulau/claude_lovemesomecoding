#!/usr/bin/env python3
"""Prove every code sample round-trips, and enforce this track's own rules.

Code blocks are compared byte-for-byte against what the content pipeline emits, not by length:
the migration nearly shipped corrupted samples because an HTML parser ate raw <script>/<style>
inside code, with almost no change in character count. This track quotes diffs and session
transcripts full of `<`, `>` and generics, which is exactly what a parser reinterprets.

Track rules on top of the round-trip:

  1. 5-8 reading minutes. ⚠️ The pipeline counts PROSE AND CODE together.
  2. Prose is at least manifest.MIN_PROSE_SHARE of the words. This is a practice track; a post
     that is mostly transcript has stopped arguing anything.
  3. The LAST h2 is manifest.REQUIRED_HEADING ("Before you accept"). It is the series' core theme,
     and every post closes with it.
  4. No block falls back to plaintext by accident. `plaintext` on purpose is fine (a terminal
     transcript is not a language); a mistyped class is not.
  5. Every language used is supported on both halves: backend SUPPORTED_LANGUAGES decides the
     class, the frontend's Prism imports supply the grammar.
  6. The manifest is coherent: unique slugs, ascending dates, excerpts under 500 chars.

Posts with no file yet are reported as `not written` and do not fail the run. No AWS needed.

    python projects/ai_engineering/check_content.py
"""

import html
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BACKEND = ROOT / "lovemesomecoding_backend"

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
AUTHORED_LANG = re.compile(r"language-([\w-]+)")
FRONTEND_SHAPE = re.compile(r'<pre class="language-([\w-]+)"><code class="language-\1">')
H2 = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.S | re.I)
TAG = re.compile(r"<[^>]+>")

# Prism component per language, for rule 5. `markup` is built into prism core.
PRISM_IMPORTS = {
    "java": "prism-java", "bash": "prism-bash", "typescript": "prism-typescript",
    "tsx": "prism-tsx", "json": "prism-json", "markdown": "prism-markdown",
    "yaml": "prism-yaml", "sql": "prism-sql", "properties": "prism-properties",
    "diff": "prism-diff", "markup": None, "plaintext": None,
    # Built into prism core, alongside markup, css and clike: imported by no line of its own.
    "javascript": None,
}


def prose_and_code_words(result: dict) -> tuple[int, int]:
    """Split the pipeline's wordCount the way the pipeline builds it, from its own output."""
    blocks = OUT_PRE.findall(result["contentHtml"])
    code_words = len(html.unescape(" ".join(b for _lang, b in blocks)).split())
    return result["wordCount"] - code_words, code_words


failures: list[str] = []
warnings: list[str] = []
missing: list[str] = []
used_langs: set[str] = set()
written = 0

print(f"{'slug':<44} {'prose':>6} {'code':>6} {'total':>6} {'min':>4} {'prose%':>7}  "
      f"{'hd':>3} {'blk':>4}")
print("-" * 96)

for entry in manifest.POSTS:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        missing.append(entry["slug"])
        continue
    written += 1
    raw = path.read_text(encoding="utf-8")
    slug = entry["slug"]

    authored, authored_langs = [], []
    for attrs, inner in SOURCE_PRE.findall(raw):
        wrapped = INNER_CODE.match(inner)
        if wrapped:
            inner = wrapped.group(1)
        authored.append(html.unescape(inner))
        claimed = AUTHORED_LANG.search(attrs)
        authored_langs.append(claimed.group(1) if claimed else None)
    used_langs.update(lang for lang in authored_langs if lang)

    result = content_service.normalize(raw)
    body = result["contentHtml"]
    pairs = OUT_PRE.findall(body)
    emitted = [html.unescape(b) for _lang, b in pairs]
    langs = [lang for lang, _ in pairs]

    if len(authored) != len(emitted):
        failures.append(f"{slug}: {len(authored)} blocks in, {len(emitted)} out")
        continue

    # THE check. Byte-for-byte, not length.
    for i, (before, after) in enumerate(zip(authored, emitted)):
        if before != after:
            failures.append(f"{slug} block {i} ({langs[i]}) changed:\n"
                            f"    in : {before[:160]!r}\n    out: {after[:160]!r}")

    if len(FRONTEND_SHAPE.findall(body)) != len(emitted):
        failures.append(f"{slug}: not every block matches the shape the highlighter expects")

    # (4) plaintext by accident
    for i, lang in enumerate(langs):
        if lang == "plaintext" and authored_langs[i] != "plaintext":
            failures.append(f"{slug} block {i}: claims {authored_langs[i]!r} but rendered as "
                            "plaintext — unsupported language, renders grey silently")

    if [t for t in result["toc"] if not t.get("id")]:
        failures.append(f"{slug}: a heading has no anchor")

    # (3) the closing section
    h2s = [html.unescape(TAG.sub("", h)).strip() for h in H2.findall(raw)]
    if not h2s or h2s[-1] != manifest.REQUIRED_HEADING:
        failures.append(f"{slug}: last h2 is {h2s[-1] if h2s else None!r}, must be "
                        f"{manifest.REQUIRED_HEADING!r}")

    # (1) and (2)
    words = result["wordCount"]
    prose, code = prose_and_code_words(result)
    share = prose / words if words else 0
    if words > manifest.TOTAL_WORDS_MAX:
        failures.append(f"{slug}: {words} words = {result['readingMinutes']} min, over the "
                        f"{manifest.TOTAL_WORDS_MAX}-word cap ({code} of them are code)")
    elif words < manifest.TOTAL_WORDS_MIN:
        warnings.append(f"{slug}: {words} words = {result['readingMinutes']} min, under the "
                        f"{manifest.TOTAL_WORDS_MIN}-word floor")
    if share < manifest.MIN_PROSE_SHARE:
        failures.append(f"{slug}: prose is {share:.0%} of the words, floor is "
                        f"{manifest.MIN_PROSE_SHARE:.0%} ({prose} prose vs {code} code)")

    print(f"{slug:<44} {prose:>6} {code:>6} {words:>6} {result['readingMinutes']:>4} "
          f"{share:>6.0%}  {len(result['toc']):>3} {len(emitted):>4}")

# ------------------------------------------------------------------ manifest rules
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest.POSTS")
dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend — prev/next would read out of order")
for entry in manifest.POSTS:
    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")
    if not entry["tags"]:
        failures.append(f"{entry['slug']}: no tags")

app = ROOT / manifest.DEMO_APP
for slug, sources in manifest.SNIPPET_SOURCES.items():
    for rel in sources:
        if not (app / rel).exists():
            failures.append(f"{slug}: SNIPPET_SOURCES names {rel!r}, which does not exist")

# (5) language support, both halves — only for languages actually used
prism_src = (ROOT / "lovemesomecoding_frontend/src/lib/content.ts").read_text(encoding="utf-8")
for lang in sorted(used_langs - {"plaintext"}):
    if lang not in content_service.SUPPORTED_LANGUAGES:
        failures.append(f"backend SUPPORTED_LANGUAGES is missing {lang!r}")
    component = PRISM_IMPORTS.get(lang, f"prism-{lang}")
    if component and component not in prism_src:
        failures.append(f"frontend content.ts does not import prismjs/components/{component}")

nav = (ROOT / "lovemesomecoding_frontend/src/lib/nav.ts").read_text(encoding="utf-8")
if f"'{manifest.CATEGORY['slug']}'" not in nav:
    warnings.append(f"nav.ts does not mention {manifest.CATEGORY['slug']!r} — the category will "
                    f"publish but never appear in the {manifest.NAV_GROUP} dropdown")

# ------------------------------------------------------------------------ report
print("-" * 96)
print(f"written {written}/{len(manifest.POSTS)}; budget {manifest.TOTAL_WORDS_MIN}-"
      f"{manifest.TOTAL_WORDS_MAX} words, prose floor {manifest.MIN_PROSE_SHARE:.0%}")
for slug in missing:
    print(f"  not written: {slug}")
if warnings:
    print(f"\n{len(warnings)} warning(s):")
    for w in warnings:
        print(f"  ! {w}")
if failures:
    print(f"\n{len(failures)} FAILURE(S):")
    for f in failures:
        print(f"  ✗ {f}")
    sys.exit(1)
print(f"\nno failures in {written} written post(s)." if missing else f"\nall {written} pass.")

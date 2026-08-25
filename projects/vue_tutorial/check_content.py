#!/usr/bin/env python3
"""Prove the normaliser round-trips every code sample byte-for-byte.

The migration nearly shipped corrupted code blocks because an HTML parser ate the
raw <script>/<style>/onclick= that legitimately appear *inside* code samples, and
the damage barely changed the character count — so length checks passed. Compare
sources, not lengths. No AWS access needed.

VUE IS THE WORST CASE THIS PIPELINE HAS FACED. A single-file component is the
unit of work in Vue, so most snippets in this track are one — and every one
contains a literal <template>, a literal <script setup> and often a literal
<style scoped>, all inside a <pre>. That is precisely the input that made an HTML
parser delete code during the migration. The ordering in
`app/services/content.py` (extract <pre> with a regex BEFORE parsing) is what
saves it, and this checker is the thing that proves the ordering still holds.

It also guards the second Vue-specific hazard: Prism ships NO `vue` grammar, and
an unsupported language is silently normalised to plaintext rather than
rejected. Any block that asks for a language the backend does not support shows
up here as an unhighlighted block, and `language-vue` reaching plaintext is a
hard failure — see PLAINTEXT_IS_A_FAILURE below.

While the track is being authored, posts that have no file yet are reported as
`not written` and do not fail the run. Once every file exists this becomes a
plain pass/fail.

    python projects/vue_tutorial/check_content.py
"""

import datetime
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

# Languages a Vue post is expected to ask for. Anything else that lands on
# plaintext is almost certainly a typo in a class attribute rather than a
# deliberate choice, and plaintext is what an unsupported language degrades to
# SILENTLY -- which is the whole reason this list exists.
EXPECTED_LANGUAGES = {
    "vue", "javascript", "markup", "css", "scss", "json", "bash", "yaml", "plaintext",
    "nginx", "docker",
}

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

    # `language-vue` degrading to plaintext means the backend's SUPPORTED_LANGUAGES
    # no longer lists "vue" -- the single failure this track is most exposed to,
    # and one that is invisible on the page (the code is all still there, just
    # grey). Catch it here rather than after 28 posts are published.
    for i, (lang, (attrs, _inner)) in enumerate(zip(langs, SOURCE_PRE.findall(raw))):
        asked = re.search(r'language-([\w-]+)', attrs)
        asked = asked.group(1) if asked else ""
        if asked and asked != lang and lang == "plaintext":
            failures.append(
                f"{entry['slug']} block {i}: authored as language-{asked} but normalised to "
                f"plaintext. Add {asked!r} to SUPPORTED_LANGUAGES in "
                f"lovemesomecoding_backend/app/services/content.py, and register the grammar "
                f"in lovemesomecoding_frontend/src/lib/content.ts.")
        if lang not in EXPECTED_LANGUAGES:
            failures.append(f"{entry['slug']} block {i}: unexpected language {lang!r}")
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

# Post dates must fall between 2023 and 2025, and must never be in the future.
#
# The first publish of this track was stamped 2026-09-01..2026-11-21: outside the
# range AND dated after the day it shipped. A future-dated post sorts to the top
# of every archive and the sitemap while claiming to have been written on a day
# that has not happened. Nothing else in the pipeline checks this.
#
# Re-basing is one edit to START_DATE in manifest.py — but a post that already
# exists keeps its stored date, so republishing after a re-base needs
# `seed.py --force-dates`.
DATE_MIN, DATE_MAX = "2023-01-01", "2025-12-31"
_today = datetime.date.today().isoformat()
for entry in manifest.POSTS:
    day = entry["date"][:10]
    if not (DATE_MIN <= day <= DATE_MAX):
        failures.append(
            f"{entry['slug']}: date {day} is outside {DATE_MIN}..{DATE_MAX}. "
            "Re-base START_DATE in manifest.py, then seed with --force-dates.")
    if day > _today:
        failures.append(f"{entry['slug']}: date {day} is in the future (today is {_today})")

for frozen in manifest.FROZEN_SLUGS:
    if frozen not in slugs:
        failures.append(f"frozen slug {frozen} is no longer in the manifest — that URL is indexed")

# The whole track is worthless if the backend cannot keep a `vue` code block.
# Assert it directly rather than inferring it from a post, so this fails even
# when no post has been written yet.
if content_service.normalize_language("vue") != "vue":
    failures.append(
        "the backend normalises language 'vue' to "
        f"{content_service.normalize_language('vue')!r}. Every SFC snippet in this track would "
        "render as unhighlighted grey text. Add \"vue\" to SUPPORTED_LANGUAGES in "
        "lovemesomecoding_backend/app/services/content.py.")

for entry in manifest.POSTS:
    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")

# Internal links. The track cross-references itself constantly -- every lesson
# ends with a "Next:" link and the interview questions link back to all 27 --
# so one renamed slug silently produces a page of 404s. Code blocks are excluded:
# a quoted index.html legitimately contains href="/favicon.svg".
_slugs = {e["slug"] for e in manifest.POSTS}
_links = 0
for entry in manifest.POSTS:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        continue
    prose = SOURCE_PRE.sub("", path.read_text(encoding="utf-8"))
    for m in re.finditer(r'href="(/[^"#]*)"', prose):
        _links += 1
        href = m.group(1)
        target = href[len("/vue/"):] if href.startswith("/vue/") else None
        if target is None:
            failures.append(f"{entry['slug']}: link to {href} leaves the track")
        elif target not in _slugs:
            failures.append(f"{entry['slug']}: link to {href} is not a slug in the manifest")

print(f"\n{_links} internal links checked")

# Lesson 1 carries the index of all 28 lessons, and it is GENERATED from the
# manifest (gen_index.py). A lesson added or renamed without re-running the
# generator leaves an index that is quietly wrong -- every link still resolves,
# it is just the wrong list. Compare rather than trust.
_lesson_one = HERE / "posts" / manifest.POSTS[0]["file"]
if _lesson_one.exists():
    import gen_index  # noqa: E402

    _text = _lesson_one.read_text(encoding="utf-8")
    if gen_index.START not in _text or gen_index.END not in _text:
        failures.append(
            f"{manifest.POSTS[0]['slug']}: the lesson-index markers are missing — "
            "gen_index.py cannot maintain the index")
    else:
        _have = gen_index.START + _text.partition(gen_index.START)[2].partition(gen_index.END)[0] \
            + gen_index.END
        if _have.strip() != gen_index.render().strip():
            failures.append(
                f"{manifest.POSTS[0]['slug']}: the lesson index does not match the manifest. "
                "Run: python projects/vue_tutorial/gen_index.py --write")

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

#!/usr/bin/env python3
"""Prove every code sample round-trips, and enforce this track's own rules.

The migration nearly shipped corrupted code blocks because an HTML parser ate the
raw <script>/<style>/onclick= that legitimately appear *inside* code samples, and
the damage barely changed the character count — so length checks passed. Compare
sources, not lengths. No AWS access needed.

A Hasura track sharpens that in its own way. GraphQL bodies are almost entirely
`{`, `}`, `$` and `!`, permission rules are JSON full of `_eq` and `_and`, and
HML is YAML where indentation IS the meaning. One swallowed character in any of
them is invisible until it renders wrong.

On top of the round-trip check this enforces four things specific to this track:

  1. Every one of the ELEVEN frozen slugs is still in the manifest. Those URLs
     are indexed and losing one is a 404 on a live page.
  2. A "rewrite" post must actually be longer than what that URL serves today.
     Rewriting `hasura-metadata` — an empty page — into 200 words is not the job.
  3. Every post covers v3, because the README requires v2 AND v3 in each one.
     Checked by looking for a v3/DDN heading, not a passing mention.
  4. Any post that talks about v3 states the date the v3 docs were read. The v3
     half of this track was NOT run locally, and that admission is the thing
     keeping it honest — see progress_report.md.

While the track is being authored, posts with no file yet are reported as
`not written` and do not fail the run. Once every file exists this becomes a
plain pass/fail.

    python projects/hasura_tutorial/check_content.py
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

# A heading that introduces the v3 half of a post. "In v3 (DDN)", "Hasura v3",
# "DDN" — any h2/h3 naming the other product counts. A mention buried in a
# paragraph does not, which is the point: the requirement is a section.
#
# Match the heading's whole inner HTML and strip tags before testing, rather than
# testing the raw markup. The normaliser adds an `id` attribute to every heading
# and post bodies routinely wrap terms in <code>, so a regex that assumes the
# text runs uninterrupted from `>` to `<` silently matches nothing.
HEADING = re.compile(r'<h[23]\b[^>]*>(.*?)</h[23]>', re.S | re.I)
TAGS = re.compile(r'<[^>]+>')
V3_TERM = re.compile(r'\bv3\b|\bDDN\b', re.I)
MENTIONS_V3 = re.compile(r'\bDDN\b|\bv3\b', re.I)


def has_v3_heading(body: str) -> bool:
    return any(V3_TERM.search(TAGS.sub(" ", inner)) for inner in HEADING.findall(body))

# The minimum a rewritten post has to reach regardless of its baseline. Four of
# the eleven frozen URLs serve zero words, so "longer than today" alone would
# accept almost anything.
MIN_REWRITE_WORDS = 600

failures = []
missing = []
total_blocks = 0
total_graphql = 0
written = 0

for entry in manifest.POSTS:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        missing.append(entry["slug"])
        print(f"{entry['slug']:34} not written")
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
    body = result["contentHtml"]
    emitted = [html.unescape(b) for _lang, b in OUT_PRE.findall(body)]
    langs = [lang for lang, _ in OUT_PRE.findall(body)]

    total_blocks += len(authored)
    total_graphql += langs.count("graphql")

    if len(authored) != len(emitted):
        failures.append(f"{entry['slug']}: {len(authored)} blocks in, {len(emitted)} out")
        continue

    for i, (before, after) in enumerate(zip(authored, emitted)):
        if before != after:
            failures.append(
                f"{entry['slug']} block {i} ({langs[i]}) changed:\n"
                f"    in : {before[:160]!r}\n    out: {after[:160]!r}")

    plain = [l for l in langs if l == "plaintext"]
    shaped = len(FRONTEND_SHAPE.findall(body))
    if shaped != len(emitted):
        failures.append(f"{entry['slug']}: {len(emitted)} blocks but {shaped} match "
                        "the shape the frontend highlighter expects")

    # A heading with no id would break the table of contents' deep links.
    missing_ids = [t for t in result["toc"] if not t.get("id")]
    if missing_ids:
        failures.append(f"{entry['slug']}: {len(missing_ids)} heading(s) with no anchor")

    # --- this track's own rules ------------------------------------------
    words = result["wordCount"]

    # (2) a rewrite has to beat the page it replaces
    if entry["state"] == "rewrite":
        baseline = manifest.EXISTING_WORDS[entry["slug"]]
        if words < MIN_REWRITE_WORDS:
            failures.append(
                f"{entry['slug']}: rewrite is {words} words, minimum {MIN_REWRITE_WORDS} "
                f"(the live page it replaces has {baseline})")
        elif words <= baseline:
            failures.append(
                f"{entry['slug']}: rewrite is {words} words but the live page "
                f"already has {baseline} — that is not a rewrite")

    # (3) every post must carry a v3 section, per the README
    if not has_v3_heading(body):
        failures.append(
            f"{entry['slug']}: no v3/DDN heading. The README requires v2 AND v3 "
            "in every post.")

    # (4) anything discussing v3 must state when the v3 docs were read
    if MENTIONS_V3.search(body) and manifest.V3_DOCS_READ not in body:
        failures.append(
            f"{entry['slug']}: talks about v3 but never states the docs-read date "
            f"({manifest.V3_DOCS_READ}). The v3 half was not run locally and has "
            "to say so.")

    gql = langs.count("graphql")
    print(f"{entry['slug']:34} {words:>5} words  "
          f"{result['readingMinutes']:>2} min  {len(result['toc']):>2} headings  "
          f"{len(emitted):>2} blocks ({gql} graphql"
          f"{', ' + str(len(plain)) + ' PLAINTEXT' if plain else ''})")

# Manifest-level invariants worth catching before anything is written.
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest.POSTS")

dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend — the prev/next pager would read out of order")

# (1) the eleven indexed URLs
for frozen in manifest.FROZEN_SLUGS:
    if frozen not in slugs:
        failures.append(f"frozen slug {frozen} is no longer in the manifest — that URL is indexed")

for entry in manifest.POSTS:
    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")
    if not entry["tags"]:
        failures.append(f"{entry['slug']}: no tags — every post in the old collection had none")

# The README requires a v2/v3 comparison table on the getting started page, and
# names each item and how it differs in v3. The table is data in manifest.py, so
# what is checkable — and what actually goes wrong — is whether the post renders
# ALL of it. A table that quietly loses its awkward rows is the failure mode:
# "Admin access" and "On a schedule" are the two nobody wants to write down.
_home = HERE / "posts" / next(
    e["file"] for e in manifest.POSTS if e["slug"] == manifest.COMPARISON_HOME)
if _home.exists():
    home_body = _home.read_text(encoding="utf-8")
    if "<table" not in home_body:
        failures.append(f"{manifest.COMPARISON_HOME}: the README requires a v2/v3 "
                        "comparison TABLE on the getting started page, and there is no <table>")
    absent_rows = [item
                   for _group, items in manifest.V2_V3_COMPARISON
                   for item, *_ in items
                   if item not in home_body]
    if absent_rows:
        failures.append(
            f"{manifest.COMPARISON_HOME}: comparison table is missing "
            f"{len(absent_rows)} of "
            f"{sum(len(i) for _g, i in manifest.V2_V3_COMPARISON)} rows: "
            + ", ".join(absent_rows[:6]) + ("…" if len(absent_rows) > 6 else ""))

# Lesson 1 carries a short cut of the same table, so a reader knows v2 and v3 are
# two products before reading nineteen posts that assume it.
_intro = HERE / "posts" / next(
    e["file"] for e in manifest.POSTS if e["slug"] == "hasura-introduction")
if _intro.exists():
    intro_body = _intro.read_text(encoding="utf-8")
    absent_teaser = [r for r in manifest.COMPARISON_TEASER if r not in intro_body]
    if absent_teaser:
        failures.append("hasura-introduction: orientation table is missing "
                        + ", ".join(absent_teaser))

# `graphql` support is what this track lives on, and it is a two-sided change:
# the backend decides the class, the frontend supplies the grammar. Either one
# alone renders every query grey. Check both here rather than discovering it in
# a built page.
if "graphql" not in content_service.SUPPORTED_LANGUAGES:
    failures.append("backend SUPPORTED_LANGUAGES is missing 'graphql'")
prism = (HERE.parent.parent / "lovemesomecoding_frontend/src/lib/content.ts")
if prism.exists() and "prism-graphql" not in prism.read_text():
    failures.append("frontend content.ts does not import prismjs/components/prism-graphql")

print(f"\n{len(manifest.POSTS)} posts in the manifest, {written} written, "
      f"{len(missing)} still to write, {total_blocks} code blocks "
      f"({total_graphql} graphql)")

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

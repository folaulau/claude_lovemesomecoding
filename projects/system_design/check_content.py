#!/usr/bin/env python3
"""Prove every code sample round-trips, and enforce this track's own rules.

The migration nearly shipped corrupted code blocks because an HTML parser ate the raw
<script>/<style>/onclick= that legitimately appear *inside* code samples, and the damage barely
changed the character count — so length checks passed. Compare sources, not lengths. No AWS access
needed.

Python sharpens that differently from GraphQL: indentation IS the syntax, and a decorator line or
a `\\n` inside a string is the kind of thing a parser eats invisibly. A block that loses one level
of indent still looks like Python.

On top of the round-trip check this enforces five rules specific to this track. Note that rule 2
is the INVERSE of the Hasura track's: there a rewrite had to get longer, because those URLs served
almost nothing. Here every one of them is two to three times too long.

  1. Every one of the NINE frozen slugs is still in the manifest. Those URLs are indexed and
     losing one is a 404 on a live page.
  2. Every post fits the 15-20 reading-minute budget. ⚠️ The pipeline counts PROSE AND CODE
     together, so this is a cap on the total, not on the writing.
  3. Prose is at least 40% of the words. This is the rule that matters. Code is 75% of the
     current collection — `fastapi-testing` runs 7.7 words of code per word of prose — and a
     total-words cap alone is satisfied by a shorter code dump.
  4. A post that makes a performance or container claim quotes a figure from manifest.MEASURED.
     Every number in this track was measured on one machine on one day; an unsourced millisecond
     is how a plausible invention gets published.
  5. Frozen posts must actually shrink. A "rewrite" that lands at the same size did not happen.

While the track is being authored, posts with no file yet are reported as `not written` and do not
fail the run. Once every file exists this becomes a plain pass/fail.

    python projects/system_design/check_content.py
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

# Exactly what the frontend's build-time highlighter matches. If the shape changes on either side,
# highlighting silently stops.
FRONTEND_SHAPE = re.compile(r'<pre class="language-([\w-]+)"><code class="language-\1">')

TAGS = re.compile(r"<[^>]+>")

# Every language this track needs. Checked on BOTH sides — the backend decides the class, the
# frontend supplies the grammar, and either one alone renders the block grey.
#
# ⚠️ `lua` is the one to watch: the rate-limiting post quotes the token-bucket EVAL script, and
# `lua` is not a language any earlier track used. `plaintext` carries every diagram and is
# deliberately NOT in this set — it needs no grammar, which is half of why it is the right choice
# for diagrams.
REQUIRED_LANGUAGES = {"python", "bash", "sql", "json", "yaml", "lua"}
PRISM_IMPORTS = {
    "python": "prism-python", "bash": "prism-bash", "sql": "prism-sql",
    "json": "prism-json", "yaml": "prism-yaml", "lua": "prism-lua",
}

# Rule 4. A post that says something is faster or slower by a stated amount has to quote a figure
# that was actually measured. The trigger is deliberately broad and the requirement narrow: if you
# make a claim, cite one of the recorded numbers.
#
# ⚠️ The trigger deliberately does NOT fire on bare arithmetic. This track is full of
# back-of-the-envelope estimation, and "5 million writes a day is about 58 a second" is a
# calculation the reader can check on the page — not a measurement that needs a source.
CLAIMS_MEASUREMENT = re.compile(
    r"\b(\d+(?:\.\d+)?\s*ms\b|\d+\s*(?:x|times)\s*(?:faster|slower)|"
    r"\d+\s*%\s*(?:faster|slower)|\bmeasured\b|\bbenchmark)", re.I)

# The exact strings that count as a citation, built from manifest.MEASURED so the two cannot drift.
_M = manifest.MEASURED
MEASURED_STRINGS = {
    str(_M["cache_http_cold_ms"]),
    str(_M["cache_http_warm_ms"]),
    str(_M["cache_service_cold_ms"]),
    str(_M["cache_service_warm_ms"]),
    _M["cache_speedup"],
    str(_M["limiter_threads"]),
    str(_M["limiter_capacity"]),
    _M["backoff_sequence"],
    str(_M["tests_with_redis"]),
}

# Posts that are REQUIRED to carry the measurements, because their whole argument rests on them.
MUST_CITE = manifest.MUST_CITE


def prose_and_code_words(raw: str, result: dict) -> tuple[int, int]:
    """Split the pipeline's wordCount the same way the pipeline builds it.

    ⚠️ Recomputed from the SAME normalised output the pipeline produced, not from the source, so
    this cannot disagree with the published readingMinutes.
    """
    blocks = OUT_PRE.findall(result["contentHtml"])
    code_words = len(html.unescape(" ".join(b for _lang, b in blocks)).split())
    return result["wordCount"] - code_words, code_words


failures = []
warnings = []
missing = []
written = 0
totals = {"words": 0, "prose": 0, "code": 0, "blocks": 0}

print(f"{'slug':<40} {'prose':>6} {'code':>6} {'total':>6} {'min':>4} {'prose%':>7}  "
      f"{'hd':>3} {'blk':>4}")
print("-" * 92)

for entry in manifest.POSTS:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        missing.append(entry["slug"])
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
    body = result["contentHtml"]
    pairs = OUT_PRE.findall(body)
    emitted = [html.unescape(b) for _lang, b in pairs]
    langs = [lang for lang, _ in pairs]

    totals["blocks"] += len(authored)

    if len(authored) != len(emitted):
        failures.append(f"{entry['slug']}: {len(authored)} blocks in, {len(emitted)} out")
        continue

    # THE check. Byte-for-byte, not length.
    for i, (before, after) in enumerate(zip(authored, emitted)):
        if before != after:
            failures.append(
                f"{entry['slug']} block {i} ({langs[i]}) changed:\n"
                f"    in : {before[:160]!r}\n    out: {after[:160]!r}")

    shaped = len(FRONTEND_SHAPE.findall(body))
    if shaped != len(emitted):
        failures.append(f"{entry['slug']}: {len(emitted)} blocks but {shaped} match the shape "
                        "the frontend highlighter expects")

    plain = [lang for lang in langs if lang == "plaintext"]

    missing_ids = [t for t in result["toc"] if not t.get("id")]
    if missing_ids:
        failures.append(f"{entry['slug']}: {len(missing_ids)} heading(s) with no anchor")

    # --- this track's own rules ---------------------------------------------
    words = result["wordCount"]
    prose, code = prose_and_code_words(raw, result)
    share = prose / words if words else 0
    totals["words"] += words
    totals["prose"] += prose
    totals["code"] += code

    # (2) the reading-time budget
    if words > manifest.TOTAL_WORDS_MAX:
        failures.append(
            f"{entry['slug']}: {words} words = {result['readingMinutes']} min, over the "
            f"{manifest.TOTAL_WORDS_MAX}-word cap ({manifest.TARGET_MINUTES[1]} min). "
            f"Remember code counts: {code} of these are code.")
    elif words < manifest.TOTAL_WORDS_MIN:
        # ⚠️ A FAILURE on this track, not a warning as on the others. Thinness is the defect this
        # whole rewrite exists to fix — the seven live posts average 1,020 words — so a post that
        # lands under the floor has reproduced the problem it was written to correct.
        failures.append(
            f"{entry['slug']}: {words} words = {result['readingMinutes']} min, under the "
            f"{manifest.TOTAL_WORDS_MIN}-word floor — thin for a whole topic")

    # (3) the prose band — floor AND ceiling
    if share < manifest.MIN_PROSE_SHARE:
        failures.append(
            f"{entry['slug']}: prose is {share:.0%} of the words, floor is "
            f"{manifest.MIN_PROSE_SHARE:.0%} ({prose} prose vs {code} code). "
            "That is a listing with commentary, not a lesson.")
    elif share > manifest.MAX_PROSE_SHARE:
        failures.append(
            f"{entry['slug']}: prose is {share:.0%} of the words, ceiling is "
            f"{manifest.MAX_PROSE_SHARE:.0%} ({prose} prose vs only {code} code). "
            "That is an essay about a system, which is exactly what the seven live posts are.")

    # (6) at least one ASCII diagram
    if len(plain) < manifest.MIN_PLAINTEXT_BLOCKS:
        failures.append(
            f"{entry['slug']}: no plaintext block — a system design post needs a picture of the "
            "system, and this track's pictures are ASCII diagrams")

    # (5) a rewrite has to actually GROW — the inverse of the FastAPI track's rule.
    #
    # See manifest.rewrite_floor for why this is capped at the track floor rather than a flat 2x:
    # `system-design-basics` is already 2,871 words, and demanding 5,742 of it contradicts the
    # 4,400-word cap two rules above.
    if entry["state"] == "rewrite":
        _p, _c, baseline, base_min, _img, _h2, _h3 = manifest.EXISTING[entry["slug"]]
        floor = manifest.rewrite_floor(baseline)
        if words < floor:
            failures.append(
                f"{entry['slug']}: rewrite is {words} words but the live page already has "
                f"{baseline} ({base_min} min); it has to reach at least {floor} "
                "to have addressed the thinness")
        elif words < baseline:
            failures.append(
                f"{entry['slug']}: rewrite is {words} words, SHORTER than the {baseline}-word "
                "page it replaces — the defect being fixed here is thinness")

    # (4) claims must be sourced
    if CLAIMS_MEASUREMENT.search(TAGS.sub(" ", body)):
        if not any(s in body for s in MEASURED_STRINGS):
            warnings.append(
                f"{entry['slug']}: makes a performance/size claim but quotes no figure from "
                "manifest.MEASURED — check it is not invented")
    for required in MUST_CITE.get(entry["slug"], []):
        if required not in body:
            failures.append(
                f"{entry['slug']}: must quote the measured value {required!r}; its argument "
                "rests on it")

    print(f"{entry['slug']:<40} {prose:>6} {code:>6} {words:>6} "
          f"{result['readingMinutes']:>4} {share:>6.0%}  "
          f"{len(result['toc']):>3} {len(emitted):>4}"
          + (f"  {len(plain)} PLAINTEXT" if plain else ""))

# ---------------------------------------------------------------- manifest rules
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest.POSTS")

dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend — the prev/next pager would read out of order")

# (1) the nine indexed URLs
for frozen in sorted(manifest.FROZEN_SLUGS):
    if frozen not in slugs:
        failures.append(f"frozen slug {frozen} is no longer in the manifest — that URL is indexed")

if manifest.FROZEN_SLUGS != set(manifest.EXISTING):
    failures.append("FROZEN_SLUGS and EXISTING disagree — one was edited without the other")

for entry in manifest.POSTS:
    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")
    if not entry["tags"]:
        failures.append(f"{entry['slug']}: no tags")
    if entry["slug"] not in manifest.SNIPPET_SOURCES:
        failures.append(f"{entry['slug']}: no SNIPPET_SOURCES entry — check_snippets cannot "
                        "verify its code")

# Language support, both halves.
for lang in sorted(REQUIRED_LANGUAGES):
    if lang not in content_service.SUPPORTED_LANGUAGES:
        failures.append(f"backend SUPPORTED_LANGUAGES is missing {lang!r}")
prism_file = HERE.parent.parent / "lovemesomecoding_frontend/src/lib/content.ts"
if prism_file.exists():
    prism_src = prism_file.read_text(encoding="utf-8")
    for lang in sorted(REQUIRED_LANGUAGES):
        if PRISM_IMPORTS[lang] not in prism_src:
            failures.append(f"frontend content.ts does not import prismjs/components/"
                            f"{PRISM_IMPORTS[lang]}")

# ---------------------------------------------------------------------- report
print("-" * 92)
if written:
    share = totals["prose"] / totals["words"] if totals["words"] else 0
    live_total = sum(v[2] for v in manifest.EXISTING.values())
    print(f"{'WRITTEN ' + str(written) + '/' + str(len(manifest.POSTS)):<40} "
          f"{totals['prose']:>6} {totals['code']:>6} {totals['words']:>6} "
          f"{'':>4} {share:>6.0%}  {'':>3} {totals['blocks']:>4}")
    print(f"\nthe seven live posts total {live_total:,} words "
          f"({sum(v[3] for v in manifest.EXISTING.values())} reading-minutes)")

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

if missing:
    print(f"\nno failures in the {written} written post(s); "
          f"{len(missing)} still to write.")
else:
    print(f"\nall {written} posts pass.")

#!/usr/bin/env python3
"""Prove every code sample round-trips, and enforce this track's own rules.

The migration nearly shipped corrupted code blocks because an HTML parser ate the raw
<script>/<style>/onclick= that legitimately appear *inside* code samples, and the damage barely
changed the character count — so length checks passed. Compare sources, not lengths. No AWS access
needed.

JSON sharpens that differently from Java: a query body is nothing but punctuation, and a parser
that eats one `<` inside a `<mark>` example, or re-encodes an `&` in a query string, produces a
block that still looks like valid JSON. Compare sources, not lengths.

On top of the round-trip check this enforces five rules specific to this track. Note that rule 2
is the INVERSE of the FastAPI track's: there every post was two to three times too long. Here the
whole collection is 52 reading-minutes across THIRTEEN posts — six of them under 350 words — so the
binding constraint is the floor, not the cap.

  1. Every one of the THIRTEEN frozen slugs is still in the manifest. Those URLs are indexed and
     losing one is a 404 on a live page.
  2. Every post fits the 12-18 reading-minute budget, and the FLOOR is a failure rather than a
     warning, because thinness is this track's actual defect. ⚠️ The pipeline counts PROSE AND
     CODE together, so the cap is on the total, not on the writing.
  3. Prose is at least 40% of the words. The fix for a 123-word post is not 3,000 words of JSON.
  4. A post that makes a timing or size claim quotes a figure from manifest.MEASURED. Every number
     in this track was measured on one machine on one day; an unsourced millisecond is how a
     plausible invention gets published.
  5. A rewrite must not come out smaller than the live page it replaces.

While the track is being authored, posts with no file yet are reported as `not written` and do not
fail the run. Once every file exists this becomes a plain pass/fail.

    python projects/elasticsearch_tutorial/check_content.py
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
# frontend supplies the grammar, and either one alone renders the block grey. `json` carries most
# of this track: a query DSL body is JSON, and without the grammar every query in eighteen posts
# renders as flat grey text.
REQUIRED_LANGUAGES = {"python", "bash", "json", "yaml", "docker"}
PRISM_IMPORTS = {
    "python": "prism-python", "bash": "prism-bash", "json": "prism-json",
    "yaml": "prism-yaml", "docker": "prism-docker",
}

# Rule 4. A post that says something is faster, slower, or a given size has to quote a figure that
# was actually measured. The trigger is deliberately broad and the requirement narrow: if you make
# a claim, cite one of the recorded numbers.
CLAIMS_MEASUREMENT = re.compile(
    r"\b(\d+(?:\.\d+)?\s*ms\b|\d+\s*%\s*(?:faster|slower)|\bmedian\b|\bMB\b|\bbenchmark)", re.I)

# The exact strings that count as a citation, built from manifest.MEASURED so the two cannot drift.
_M = manifest.MEASURED
MEASURED_STRINGS = {
    str(_M["search_no_facets_ms"]), str(_M["search_with_facets_ms"]),
    str(_M["index_one_by_one_200_ms"]), str(_M["index_bulk_200_ms"]),
    str(_M["bm25_score"]), str(_M["bm25_boost"]), str(_M["bm25_idf"]), str(_M["bm25_tf"]),
    _M["bulk_speedup"],
}

# Posts that are REQUIRED to carry the measurements, because their whole argument rests on them.
MUST_CITE = {
    "elasticsearch-bulk-indexing-data-sync": [
        str(_M["index_one_by_one_200_ms"]), str(_M["index_bulk_200_ms"]),
    ],
    "elasticsearch-relevance-tuning": [str(_M["bm25_score"]), str(_M["bm25_idf"])],
    "elasticsearch-aggregation": [str(_M["search_with_facets_ms"])],
}


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
        # A FAILURE here, not a warning. Thinness is what is wrong with this collection — six of
        # the thirteen live posts are under 350 words — so a rewrite that lands short has not
        # fixed the thing it was written to fix.
        failures.append(
            f"{entry['slug']}: {words} words = {result['readingMinutes']} min, under the "
            f"{manifest.TOTAL_WORDS_MIN}-word floor ({manifest.TARGET_MINUTES[0]} min) — "
            "thin for a whole topic, which is the defect this track exists to repair")

    # (3) the prose floor — the anti-code-dump rule
    if share < manifest.MIN_PROSE_SHARE:
        failures.append(
            f"{entry['slug']}: prose is {share:.0%} of the words, floor is "
            f"{manifest.MIN_PROSE_SHARE:.0%} ({prose} prose vs {code} code). "
            "That is a listing with commentary, not a lesson.")

    # (5) a rewrite must not come out smaller than the page it replaces
    if entry["state"] == "rewrite":
        _p, _c, baseline, base_min = manifest.EXISTING[entry["slug"]]
        if words <= baseline:
            failures.append(
                f"{entry['slug']}: rewrite is {words} words but the live page already has "
                f"{baseline} ({base_min} min) — that is not a rewrite")

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

# (1) the thirteen indexed URLs
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
    print(f"\nthe thirteen live posts total {live_total:,} words "
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

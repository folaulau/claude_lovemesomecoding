#!/usr/bin/env python3
"""Prove every code sample round-trips, and enforce this track's own rules.

The migration nearly shipped corrupted code blocks because an HTML parser ate the raw
<script>/<style>/onclick= that legitimately appear *inside* code samples, and the damage barely
changed the character count — so length checks passed. Compare sources, not lengths. No AWS access
needed.

SQL sharpens that differently from Python: a `<` inside a comparison and an `&` inside a string are
exactly the characters an HTML round-trip mangles, and a WHERE clause that lost its `<` still looks
like SQL.

On top of the round-trip check this enforces the rules specific to this track. Rules 4 and 5 exist
because **nothing in this track was executed** — there is no Snowflake account on this machine (see
manifest.VERIFIED and progress_report.md). A track that cannot measure must not sound like it did.

  1. The frozen slug is still in the manifest. `/snowflake/snowflake-introduction` is indexed and
     losing it is a 404 on a live page.
  2. Every post fits the 6-10 reading-minute budget. ⚠️ The pipeline counts PROSE AND CODE
     together, so this is a cap on the total, not on the writing.
  3. Prose is at least 40% of the words. SQL is terse; a Snowflake post that is mostly code is
     usually a post that forgot to explain anything.
  4. NO POST PRINTS A DOLLAR FIGURE. Credit consumption per warehouse size is documented and
     stable; the price per credit varies by edition, cloud and region, so a dollar amount is wrong
     somewhere and stale everywhere.
  5. NO POST CLAIMS A MEASUREMENT. No timings, no "N% faster", no benchmark language. Nothing here
     was run, and an unsourced millisecond is how a plausible invention gets published.
  6. The rewrite must GROW. ⚠️ This is the inverse of the FastAPI and Postgres rule — those tracks
     were cutting bloated posts down, this one replaces a 624-word marketing blurb with a lesson.
  7. Every code block declares a real language. A block that normalises to `plaintext` renders
     grey, and in this track it is usually a result dump that should have been an HTML table.
  8. Posts only name the two databases the track uses, and only real TPCH schemas. A query against
     an invented schema is one the reader cannot run, which is the entire point of decision 2.
  9. Images point at the media CDN. Anything else is a hotlink or a dead file.

While the track is being authored, posts with no file yet are reported as `not written` and do not
fail the run. Once every file exists this becomes a plain pass/fail.

    python projects/snowflake_tutorial/check_content.py
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
IMG_SRC = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"', re.I)
INLINE_CODE = re.compile(r"<code\b[^>]*>(.*?)</code>", re.S | re.I)

# Every language this track needs. Checked on BOTH sides — the backend decides the class, the
# frontend supplies the grammar, and either one alone renders the block grey. All of these already
# exist on both sides, so this guards against a regression, not a gap.
REQUIRED_LANGUAGES = {"sql", "bash", "json", "python", "yaml"}
PRISM_IMPORTS = {
    "sql": "prism-sql", "bash": "prism-bash", "json": "prism-json",
    "python": "prism-python", "yaml": "prism-yaml",
}

# ---------------------------------------------------------------------------
# Rule 4 — no dollar figures
# ---------------------------------------------------------------------------
# `$2.00 per credit`, `$23/TB`, `costs $40 a month`. Also catches "USD 2.00".
#
# ⚠️ Two patterns, not one, and the split is load-bearing. In PROSE any `$` followed by a digit is
# a price. In CODE it is almost always a positional column reference — `COPY INTO ... SELECT $1,
# $2 FROM @stage` — so the code pattern has to insist on something that only money has: a decimal
# cents part, or a per-unit phrase after it.
DOLLARS_PROSE = re.compile(r"(\$\s?\d|\bUSD\s?\d|\bdollars?\s+per\b)", re.I)
DOLLARS_CODE = re.compile(
    r"(\$\s?\d+\.\d{2}\b|\$\s?\d[\d,]*\s*(?:per\b|/\s*(?:credit|TB|GB|month|year|hour)|"
    r"a\s+(?:month|year|day)))", re.I)

# ---------------------------------------------------------------------------
# Rule 5 — no invented measurements
# ---------------------------------------------------------------------------
# Deliberately narrow: it must catch a claim, not a configuration value. `AUTO_SUSPEND = 60` is a
# setting; "ran in 60 ms" is a measurement. So durations only trip it when they are attached to
# timing language, and comparatives only when they carry a number.
MEASUREMENT_CLAIMS = [
    (re.compile(r"\b\d+(?:\.\d+)?\s*(?:ms|milliseconds)\b", re.I), "a millisecond timing"),
    (re.compile(r"\b(?:ran|took|completed|finished|returned|executed|elapsed)\s+in\s+"
                r"[~<>]?\s*\d", re.I), "a stated runtime"),
    (re.compile(r"\b\d+(?:\.\d+)?\s*(?:x|times|%)\s+(?:faster|slower|cheaper|quicker)\b", re.I),
     "a quantified speedup"),
    # ⚠️ Narrow on purpose: TPC-H is legitimately called "benchmark data" throughout this
    # track. The verb and the appeal-to-results are the claims; the noun is a dataset name.
    (re.compile(r"\b(?:benchmark(?:ed|ing)\b|benchmarks?\s+(?:show|showed|prove|confirm)|"
                r"we measured|i measured|on my machine|median (?:of )?\d)", re.I),
     "benchmark language"),
]

# The two databases this track is allowed to name, plus the sample schemas that really exist.
# Anything matching DB_NAMED that is not one of these is an invented object.
DB_NAMED = re.compile(r"\b([A-Z][A-Z0-9_]{4,})\.(?:[A-Z][A-Z0-9_]*)\.", re.M)
ALLOWED_DBS = {manifest.SAMPLE_DB, manifest.LAB_DB}
TPCH_SCHEMA = re.compile(r"\bTPCH_[A-Z0-9]+\b")


def prose_and_code_words(result: dict) -> tuple[int, int]:
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

print(f"{'slug':<48} {'prose':>6} {'code':>6} {'total':>6} {'min':>4} {'prose%':>7}  "
      f"{'hd':>3} {'blk':>4}")
print("-" * 100)

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

    missing_ids = [t for t in result["toc"] if not t.get("id")]
    if missing_ids:
        failures.append(f"{entry['slug']}: {len(missing_ids)} heading(s) with no anchor")

    # --- this track's own rules ---------------------------------------------
    words = result["wordCount"]
    prose, code = prose_and_code_words(result)
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
    elif result["readingMinutes"] < manifest.TARGET_MINUTES[0]:
        # ⚠️ The floor is on the PUBLISHED reading time, not on the raw word count. readingMinutes
        # rounds, so a 1,270-word post publishes as 6 minutes and is inside the budget even though
        # it is under 6 × 220. Warning on the word count instead flagged posts that were fine.
        warnings.append(
            f"{entry['slug']}: {words} words = {result['readingMinutes']} min, under the "
            f"{manifest.TARGET_MINUTES[0]}-minute floor — thin for a whole topic")

    # (3) the prose floor — the anti-code-dump rule
    if share < manifest.MIN_PROSE_SHARE:
        failures.append(
            f"{entry['slug']}: prose is {share:.0%} of the words, floor is "
            f"{manifest.MIN_PROSE_SHARE:.0%} ({prose} prose vs {code} code). "
            "That is a listing with commentary, not a lesson.")

    # (4) no dollar figures. Prose is checked broadly, code narrowly — see DOLLARS_CODE.
    # ⚠️ Inline <code> counts as CODE, not prose. Post 7 explains COPY INTO's positional column
    # references in a sentence — "referenced positionally as <code>$1</code>" — and the broad
    # prose pattern reads that as a price.
    without_blocks = OUT_PRE.sub(" ", body)
    inline_code = INLINE_CODE.findall(without_blocks)
    prose_only = TAGS.sub(" ", INLINE_CODE.sub(" ", without_blocks))
    code_only = " ".join([b for _lang, b in pairs] + inline_code)
    priced = DOLLARS_PROSE.findall(prose_only) + DOLLARS_CODE.findall(code_only)
    if priced:
        failures.append(
            f"{entry['slug']}: prints a price ({priced[0].strip()!r}). Credit CONSUMPTION is "
            "stable and safe to state; the dollar price per credit varies by edition, cloud and "
            "region. Link https://www.snowflake.com/en/pricing-options/ instead.")

    # (5) no invented measurements — prose only, so a SQL literal cannot trip it
    text = TAGS.sub(" ", body)
    for pattern, what in MEASUREMENT_CLAIMS:
        hit = pattern.search(text)
        if hit:
            failures.append(
                f"{entry['slug']}: makes {what} ({hit.group(0).strip()!r}), but nothing in this "
                "track was executed — there is no Snowflake account. Cut it or attribute it to "
                "the docs. See manifest.VERIFIED.")

    # (6) the rewrite has to actually grow
    if entry["state"] == "rewrite":
        _p, _c, baseline, base_min = manifest.EXISTING[entry["slug"]]
        if words <= baseline * 1.5:
            failures.append(
                f"{entry['slug']}: rewrite is {words} words against the live page's {baseline} "
                f"({base_min} min). That page is a stub — the rewrite is supposed to replace it "
                "with a lesson, not reword it.")

    # (7) every block declares a real language
    plain = [i for i, lang in enumerate(langs) if lang == "plaintext"]
    if plain:
        failures.append(
            f"{entry['slug']}: block(s) {plain} normalised to plaintext — they render grey. "
            "Give them a supported language, or make them an HTML <table> if they are results.")

    # (8) only the two real databases, only real TPCH schemas
    for db in set(DB_NAMED.findall(body)):
        if db not in ALLOWED_DBS:
            warnings.append(
                f"{entry['slug']}: names a database {db!r} that is neither "
                f"{manifest.SAMPLE_DB} nor {manifest.LAB_DB} — check the reader can run this")
    for schema in set(TPCH_SCHEMA.findall(body)):
        if schema not in manifest.SAMPLE_SCHEMAS:
            failures.append(
                f"{entry['slug']}: queries {schema}, which does not exist. Real ones: "
                + ", ".join(manifest.SAMPLE_SCHEMAS))

    # (9) images live on the media CDN
    for src in IMG_SRC.findall(body):
        if manifest.MEDIA_HOST not in src:
            failures.append(f"{entry['slug']}: <img> src is not on {manifest.MEDIA_HOST}: {src}")

    print(f"{entry['slug']:<48} {prose:>6} {code:>6} {words:>6} "
          f"{result['readingMinutes']:>4} {share:>6.0%}  "
          f"{len(result['toc']):>3} {len(emitted):>4}")

# ---------------------------------------------------------------- manifest rules
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest.POSTS")

dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend — the prev/next pager would read out of order")

# (1) the indexed URL
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
print("-" * 100)
if written:
    share = totals["prose"] / totals["words"] if totals["words"] else 0
    print(f"{'WRITTEN ' + str(written) + '/' + str(len(manifest.POSTS)):<48} "
          f"{totals['prose']:>6} {totals['code']:>6} {totals['words']:>6} "
          f"{'':>4} {share:>6.0%}  {'':>3} {totals['blocks']:>4}")
    live_total = sum(v[2] for v in manifest.EXISTING.values())
    print(f"\nthe live collection is ONE post totalling {live_total:,} words "
          f"({sum(v[3] for v in manifest.EXISTING.values())} reading-minutes)")

if not manifest.VERIFIED:
    print("\n⚠️  manifest.VERIFIED is False — no sample in this track was executed. Rules 4 and 5 "
          "are the only thing standing between that and an invented benchmark.")

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

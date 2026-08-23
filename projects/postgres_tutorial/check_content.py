#!/usr/bin/env python3
"""Prove every code sample round-trips, and enforce this track's own rules.

The migration nearly shipped corrupted code blocks because an HTML parser ate the raw
<script>/<style>/onclick= that legitimately appear *inside* code samples, and the damage barely
changed the character count — so length checks passed. Compare sources, not lengths. No AWS access
needed.

SQL sharpens that in its own way. A code sample here is frequently *psql output* — a table drawn
with `-`, `|` and `+` — and an HTML parser that decides `<` starts a tag will happily eat half of
a `WHERE created_at < now()`. Byte-for-byte is the only check worth running.

On top of the round-trip check this enforces six rules specific to this track:

  1. Both frozen slugs are still in the manifest. `/postgre/postgres-introduction` and
     `/postgre/postgres-installation` are indexed and losing one is a 404 on a live page.
  2. Every post fits the 6-10 reading-minute budget. ⚠️ The pipeline counts PROSE AND CODE
     together, so this is a cap on the total, not on the writing.
  3. Prose is at least 40% of the words. SQL is the easiest language in the world to fill a word
     budget with — paste a longer query — and the result is a listing with captions.
  4. A rewrite has to actually GROW. ⚠️ This is the INVERSE of the FastAPI track's rule, and the
     reason is the opposite situation: those nine posts were 40-minute monsters that had to be
     cut, while these two are 176-word and 112-word stubs. A "rewrite" that lands near the stub's
     size did not happen.
  5. Any row count a post quotes about the lab database matches manifest.LAB_ROWS. Every figure
     in this track came from one build of stayhub_lab; a plausible-looking round number that
     nobody ran is exactly what this catches.
  6. A post that shows a query plan is one of the posts allowed to. `EXPLAIN` output is the most
     tempting thing in the track to invent, because it looks authoritative and nobody checks. The
     posts that quote it are declared here and verified by check_sql.py.

While the track is being authored, posts with no file yet are reported as `not written` and do not
fail the run. Once every file exists this becomes a plain pass/fail.

    python projects/postgres_tutorial/check_content.py
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
# frontend supplies the grammar, and either one alone renders the block grey. All of these already
# exist; this guards against a regression, not a gap.
#
# `plaintext` is not in here and is not a defect in this track: psql's table output has no grammar
# worth applying, so a result set is deliberately plaintext. The count is printed per post so a
# sudden jump gets noticed.
REQUIRED_LANGUAGES = {"sql", "bash", "python", "yaml", "docker", "json"}
PRISM_IMPORTS = {
    "sql": "prism-sql", "bash": "prism-bash", "python": "prism-python",
    "yaml": "prism-yaml", "docker": "prism-docker", "json": "prism-json",
}

# Rule 6. Only these posts may print a query plan, and check_sql.py re-runs every plan they show.
PLAN_POSTS = {
    "postgres-indexes",
    "postgres-explain-and-query-performance",
    "postgres-transactions-and-locking",
    "postgres-schema-migrations",
    "postgres-in-production",
}
SHOWS_A_PLAN = re.compile(r"\b(Seq Scan|Index Scan|Index Only Scan|Bitmap Heap Scan|Hash Join|"
                          r"Nested Loop|Merge Join|Gather Merge|QUERY PLAN)\b")

# Rule 5. Row counts from manifest.LAB_ROWS, in every spelling a post might use them.
_R = manifest.LAB_ROWS
LAB_NUMBERS = set()
for _key, _value in _R.items():
    if isinstance(_value, int):
        LAB_NUMBERS |= {f"{_value:,}", str(_value)}
for _status, _value in _R["bookings_by_status"].items():
    LAB_NUMBERS |= {f"{_value:,}", str(_value)}
# Round spellings that are honest shorthand for the exact figure.
LAB_NUMBERS |= {"400,000", "400k", "20,000", "50,000"}

# A number with a thousands separator, in prose, IN THE SAME SENTENCE as the name of a lab table.
#
# Both halves of that are needed. Small unseparated integers are everywhere in SQL ("LIMIT 10",
# "5432") so the separator is what marks a figure. And the table name is what separates a claim
# about the data ("400,000 bookings") from ordinary arithmetic in an explanation ("10,000 rows in
# 10,000 transactions") — the first has to be true of stayhub_lab, the second is a sentence.
# "rows" and "users" are deliberately NOT in the list: both are ordinary English here.
LAB_TABLES = r"(?:bookings?|properties|reviews|payments)"
BIG_NUMBER = re.compile(
    r"\b(\d{1,3}(?:,\d{3})+)\b(?=[^.!?]*\b" + LAB_TABLES + r"\b)")


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

    # Characters outside the house set. Caught a stray CJK character sitting mid-sentence in the
    # indexes post ("most applications query one 状態 of a workflow"), which reads as a normal word
    # at a glance and would have shipped. Punctuation the posts use on purpose is allowed; anything
    # else is a slip.
    ALLOWED_NON_ASCII = set("—–’‘“”…×→±⚠️✓✗‹›°éíóúñ")
    stray = sorted({c for c in raw if ord(c) > 127} - ALLOWED_NON_ASCII)
    if stray:
        failures.append(
            f"{entry['slug']}: unexpected character(s) {stray} — a typo, or add it to "
            "ALLOWED_NON_ASCII if it is deliberate")

    if not result["toc"]:
        failures.append(f"{entry['slug']}: no h2/h3 at all — no table of contents, no deep links. "
                        "That is the defect the two live stubs have.")

    # --- this track's own rules ---------------------------------------------
    words = result["wordCount"]
    prose, code = prose_and_code_words(result)
    share = prose / words if words else 0
    totals["words"] += words
    totals["prose"] += prose
    totals["code"] += code

    # (2) the reading-time budget
    #
    # Tested on readingMinutes, not on the word count, because readingMinutes is the number the
    # reader sees and it is ROUNDED: 1,278 words is 5.8, published as "6 min". Comparing words
    # against TARGET_MINUTES * 220 flags a post that already reads as being inside the band.
    minutes = result["readingMinutes"]
    low, high = manifest.TARGET_MINUTES
    if minutes > high:
        failures.append(
            f"{entry['slug']}: {minutes} min ({words} words), over the {high}-minute cap. "
            f"Remember code counts: {code} of these words are code.")
    elif minutes < low:
        warnings.append(
            f"{entry['slug']}: {minutes} min ({words} words), under the {low}-minute floor — "
            "thin for a whole topic")

    # (3) the prose floor — the anti-code-dump rule
    if share < manifest.MIN_PROSE_SHARE:
        failures.append(
            f"{entry['slug']}: prose is {share:.0%} of the words, floor is "
            f"{manifest.MIN_PROSE_SHARE:.0%} ({prose} prose vs {code} code). "
            "That is a listing with commentary, not a lesson.")

    # (4) a rewrite has to actually grow — the inverse of the FastAPI rule
    if entry["state"] == "rewrite":
        _p, _c, baseline, base_min = manifest.EXISTING[entry["slug"]]
        if words < baseline * 4:
            failures.append(
                f"{entry['slug']}: rewrite is {words} words against a {baseline}-word stub. "
                "A rewrite of a stub that is not several times longer did not replace anything.")

    # (5) quoted row counts have to be real
    for number in set(BIG_NUMBER.findall(TAGS.sub(" ", body))):
        if number not in LAB_NUMBERS:
            warnings.append(
                f"{entry['slug']}: quotes the figure {number} — not one of manifest.LAB_ROWS. "
                "If it came from a query, add it to the manifest; if not, it is invented.")

    # (6) query plans only where they are verified
    if SHOWS_A_PLAN.search(TAGS.sub(" ", body)) and entry["slug"] not in PLAN_POSTS:
        failures.append(
            f"{entry['slug']}: shows a query plan but is not in PLAN_POSTS, so check_sql.py "
            "never re-runs it. An unverified EXPLAIN is the most authoritative-looking thing "
            "you can invent.")

    print(f"{entry['slug']:<44} {prose:>6} {code:>6} {words:>6} "
          f"{result['readingMinutes']:>4} {share:>6.0%}  "
          f"{len(result['toc']):>3} {len(emitted):>4}"
          + (f"  {len(plain)} plaintext" if plain else ""))

# ---------------------------------------------------------------- manifest rules
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest.POSTS")

dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend — the prev/next pager would read out of order")

# (1) the two indexed URLs
for frozen in sorted(manifest.FROZEN_SLUGS):
    if frozen not in slugs:
        failures.append(f"frozen slug {frozen} is no longer in the manifest — that URL is indexed")

if manifest.FROZEN_SLUGS != set(manifest.EXISTING):
    failures.append("FROZEN_SLUGS and EXISTING disagree — one was edited without the other")

if not PLAN_POSTS <= set(slugs):
    failures.append(f"PLAN_POSTS names slugs not in the manifest: "
                    f"{', '.join(sorted(PLAN_POSTS - set(slugs)))}")

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
print("-" * 96)
if written:
    share = totals["prose"] / totals["words"] if totals["words"] else 0
    live_total = sum(v[2] for v in manifest.EXISTING.values())
    print(f"{'WRITTEN ' + str(written) + '/' + str(len(manifest.POSTS)):<44} "
          f"{totals['prose']:>6} {totals['code']:>6} {totals['words']:>6} "
          f"{'':>4} {share:>6.0%}  {'':>3} {totals['blocks']:>4}")
    print(f"\nthe two live posts total {live_total} words "
          f"({sum(v[3] for v in manifest.EXISTING.values())} reading-minutes) between them")

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
    print(f"\nno failures in the {written} written post(s); {len(missing)} still to write.")
else:
    print(f"\nall {written} posts pass.")

#!/usr/bin/env python3
"""Prove every code sample round-trips, and enforce this track's own rules.

The migration nearly shipped corrupted code blocks because an HTML parser ate the raw
<script>/<style>/onclick= that legitimately appear *inside* code samples, and the damage barely
changed the character count — so length checks passed. Compare sources, not lengths. No AWS access
and no database needed.

SQL sharpens that in its own way. A code sample here is frequently *mysql client output* — a table
drawn with `+`, `-` and `|` — and an HTML parser that decides `<` starts a tag will happily eat
half of a `WHERE created_at < NOW()`. Byte-for-byte is the only check worth running.

On top of the round-trip check this enforces the rules specific to this track:

  1. All 42 frozen slugs are still in the manifest. Every one is an indexed URL and losing one
     is a 404 on a page that has ranked since 2019.
  2. Every post fits its reading-minute band. ⚠️ The pipeline counts PROSE AND CODE together, so
     this is a cap on the total, not on the writing. Unlike the Postgres track this cuts BOTH
     ways — `mysql-transaction` is a 0-word stub that has to grow and
     `sql-interview-fundamentals` is a 27-minute monster that has to shrink.
  3. Prose is at least 40% of the words. SQL is the easiest language in the world to fill a word
     budget with — paste a longer query — and the result is a listing with captions.
  4. NO IMAGES. Not one <img>, <figure> or external image URL. See the docstring on RULE 4.
  5. No WordPress leftovers — `boldgrid-section`, `col-md-*`, `class=""`.
  6. Any lab figure a post quotes matches manifest.LAB_ROWS.
  7. A post that shows a query plan is one of the posts allowed to, so check_sql.py re-runs it.

While the track is being authored, posts with no file yet are reported as `not written` and do not
fail the run. Once every file exists this becomes a plain pass/fail.

    lovemesomecoding_backend/.venv/bin/python projects/mysql_tutorial/check_content.py
"""

import datetime as _dt
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
# `plaintext` is not in here and is not a defect: the mysql client's table output has no grammar
# worth applying, so a result set is deliberately plaintext. The count is printed per post so a
# sudden jump gets noticed.
REQUIRED_LANGUAGES = {"sql", "bash", "java", "properties", "yaml", "docker"}
PRISM_IMPORTS = {
    "sql": "prism-sql", "bash": "prism-bash", "java": "prism-java",
    "properties": "prism-properties", "yaml": "prism-yaml", "docker": "prism-docker",
}

# RULE 4 — NO IMAGES.
#
# The 42 posts being replaced carry 99 <img> tags across 30 of them, almost all WordPress
# screenshots of query output. A screenshot of a result set is the worst available form for it:
# not searchable, not copyable, not selectable, invisible to a screen reader, and — the reason
# that decides it here — IMPOSSIBLE FOR check_sql.py TO VERIFY. Every one becomes a real
# plaintext block holding the actual output, which the checker then re-derives.
#
# Three of them additionally hotlink miro.medium.com / i.stack.imgur.com / interviewbit, which is
# a broken-link risk and a licensing problem at once.
IMAGE_MARKERS = re.compile(
    r"<img\b|<figure\b|<picture\b|<svg\b|background-image\s*:|\.(?:png|jpe?g|gif|webp|svg)\b",
    re.I)

# RULE 5 — WordPress leftovers. 36 of the 42 live posts still carry these.
WORDPRESS_MARKERS = re.compile(
    r"boldgrid|col-md-|col-xs-|col-sm-|wp-block|wp-image|enlighter|class=\"\"", re.I)

# RULE 7. Only these posts may print a query plan, and check_sql.py re-runs every plan they show.
SHOWS_A_PLAN = re.compile(
    r"\b(?:EXPLAIN\s+ANALYZE|possible_keys|key_len|filtered|Using\s+filesort|"
    r"Using\s+temporary|Using\s+index\s+condition|const_row_not_found|"
    r"-> Table scan on|-> Index lookup on|-> Nested loop)\b", re.I)

# RULE 6. Row counts from manifest.LAB_ROWS, in every spelling a post might use them.
_R = manifest.LAB_ROWS
LAB_NUMBERS = set()
for _key, _value in _R.items():
    if isinstance(_value, int):
        LAB_NUMBERS |= {f"{_value:,}", str(_value)}
for _status, _value in _R["orders_by_status"].items():
    LAB_NUMBERS |= {f"{_value:,}", str(_value)}
# Round spellings that are honest shorthand for the exact figure.
LAB_NUMBERS |= {"400,000", "400k", "1,000,000", "1m", "50,000", "80,000"}

# A number with a thousands separator, in prose, IN THE SAME SENTENCE as the name of a lab table.
#
# Both halves are needed. Small unseparated integers are everywhere in SQL ("LIMIT 10", "3308") so
# the separator is what marks a figure. And the table name is what separates a claim about the data
# ("400,000 orders") from ordinary arithmetic in an explanation — the first has to be true of
# pizza_lab, the second is a sentence.
LAB_TABLES = r"(?:orders?|items?|users?|toppings?|customers?)"
BIG_NUMBER = re.compile(r"\b(\d{1,3}(?:,\d{3})+)\b(?=[^.!?]*\b" + LAB_TABLES + r"\b)")

ALLOWED_NON_ASCII = set("—–’‘“”…×→±⚠️✓✗‹›°éíóúñ§")


def prose_and_code_words(result: dict) -> tuple[int, int]:
    """Split the pipeline's wordCount the same way the pipeline builds it.

    ⚠️ Recomputed from the SAME normalised output the pipeline produced, not from the source, so
    this cannot disagree with the published readingMinutes.
    """
    blocks = OUT_PRE.findall(result["contentHtml"])
    code_words = len(html.unescape(" ".join(b for _lang, b in blocks)).split())
    return result["wordCount"] - code_words, code_words


failures: list[str] = []
warnings: list[str] = []
missing: list[str] = []
written = 0
totals = {"words": 0, "prose": 0, "code": 0, "blocks": 0, "was": 0}

print(f"{'slug':<38} {'was':>5} {'prose':>6} {'code':>6} {'total':>6} {'min':>4} {'prose%':>7}  "
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

    plain = [lang for lang in langs if lang == "plaintext"]

    if [t for t in result["toc"] if not t.get("id")]:
        failures.append(f"{entry['slug']}: heading(s) with no anchor")

    if not result["toc"]:
        failures.append(f"{entry['slug']}: no h2/h3 at all — no table of contents, no deep links. "
                        "That is one of the defects being fixed.")

    # Prose only — a `.png` inside a code sample is a filename, not an image.
    prose_html = OUT_PRE.sub(" ", body)

    # (4) no images
    hits = IMAGE_MARKERS.findall(prose_html)
    if hits:
        failures.append(
            f"{entry['slug']}: image markup found ({', '.join(sorted(set(hits))[:4])}). "
            "This track ships no images — query output goes in a plaintext block so "
            "check_sql.py can re-derive it. See RULE 4.")

    # (5) WordPress leftovers
    wp = WORDPRESS_MARKERS.findall(raw)
    if wp:
        failures.append(f"{entry['slug']}: WordPress leftover markup "
                        f"({', '.join(sorted(set(wp))[:4])})")

    stray = sorted({c for c in raw if ord(c) > 127} - ALLOWED_NON_ASCII)
    if stray:
        failures.append(
            f"{entry['slug']}: unexpected character(s) {stray} — a typo, or add it to "
            "ALLOWED_NON_ASCII if it is deliberate")

    # --- this track's own size rules ----------------------------------------
    words = result["wordCount"]
    prose, code = prose_and_code_words(result)
    share = prose / words if words else 0
    was = manifest.EXISTING.get(entry["slug"], (0, 0, 0, 0))[2]
    totals["words"] += words
    totals["prose"] += prose
    totals["code"] += code
    totals["was"] += was

    # (2) the reading-time budget, tested on readingMinutes because that is the number the reader
    # sees and it is ROUNDED.
    minutes = result["readingMinutes"]
    low, high = manifest.target_minutes(entry["slug"])
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

    # (6) quoted lab figures have to be real
    if entry["slug"] in manifest.LAB_POSTS:
        for number in set(BIG_NUMBER.findall(TAGS.sub(" ", prose_html))):
            if number not in LAB_NUMBERS:
                warnings.append(
                    f"{entry['slug']}: quotes the figure {number} — not one of "
                    "manifest.LAB_ROWS. If it came from a query, add it; if not, it is invented.")
    else:
        for number in set(BIG_NUMBER.findall(TAGS.sub(" ", prose_html))):
            if number in LAB_NUMBERS:
                warnings.append(
                    f"{entry['slug']}: quotes the lab figure {number} but is not in LAB_POSTS, "
                    "so check_sql.py never runs it against pizza_lab.")

    # (7) query plans only where they are verified.
    #
    # Searched in the PLAINTEXT BLOCKS ONLY, not the whole body. A quoted plan is by
    # definition output, and output lives in a plaintext block; naming `Using filesort` in
    # a sentence is discussing a concept, not asserting a result. Searching the whole body
    # failed `sql-order-by` for a prose mention, which is the rule crying wolf — and a rule
    # that cries wolf is one that gets switched off.
    quoted_output = "\n".join(b for lang, b in pairs if lang == "plaintext")
    if SHOWS_A_PLAN.search(quoted_output) and entry["slug"] not in manifest.LAB_POSTS:
        failures.append(
            f"{entry['slug']}: shows a query plan but is not in LAB_POSTS, so check_sql.py "
            "never re-runs it. An unverified EXPLAIN is the most authoritative-looking thing "
            "you can invent.")

    print(f"{entry['slug']:<38} {was:>5} {prose:>6} {code:>6} {words:>6} "
          f"{minutes:>4} {share:>6.0%}  {len(result['toc']):>3} {len(emitted):>4}"
          + (f"  {len(plain)} plaintext" if plain else ""))

# ---------------------------------------------------------------- manifest rules
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest.POSTS")

dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend — the prev/next pager would read out of order")

# A future-dated post is the real failure. There is NO site-wide date window — the
# LeetCode track retired its own on 2026-08-24 — so the only hard rules are that dates
# ascend (checked above) and that none is in the future. The Vue track's first publish
# shipped 2026-09-01, which was both future-dated and invisible until someone looked.
_today = _dt.date.today().isoformat()
for _e in manifest.POSTS:
    if _e["date"][:10] > _today:
        failures.append(
            f"{_e['slug']}: dated {_e['date'][:10]}, which is in the future (today is {_today}). "
            "Move START_DATE back.")
        break

# (1) the 42 indexed URLs
for frozen in sorted(manifest.FROZEN_SLUGS):
    if frozen not in slugs:
        failures.append(f"frozen slug {frozen} is no longer in the manifest — that URL is indexed")

if manifest.FROZEN_SLUGS != set(manifest.EXISTING):
    failures.append("FROZEN_SLUGS and EXISTING disagree — one was edited without the other")

_declared_new = {e["slug"] for e in manifest.POSTS if e["new"]}
if _declared_new & manifest.FROZEN_SLUGS:
    failures.append(f"marked new but actually live: {', '.join(sorted(_declared_new & manifest.FROZEN_SLUGS))}")

if not manifest.LAB_POSTS <= set(slugs):
    failures.append("LAB_POSTS names slugs not in the manifest: "
                    f"{', '.join(sorted(manifest.LAB_POSTS - set(slugs)))}")

if not manifest.LONG_POSTS <= set(slugs):
    failures.append("LONG_POSTS names slugs not in the manifest")

if not manifest.SHORT_POSTS <= set(slugs):
    failures.append("SHORT_POSTS names slugs not in the manifest: "
                    f"{', '.join(sorted(manifest.SHORT_POSTS - set(slugs)))}")

if manifest.SHORT_POSTS & manifest.LONG_POSTS:
    failures.append("a post is in both SHORT_POSTS and LONG_POSTS")

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
    print(f"{'WRITTEN ' + str(written) + '/' + str(len(manifest.POSTS)):<38} "
          f"{totals['was']:>5} {totals['prose']:>6} {totals['code']:>6} {totals['words']:>6} "
          f"{'':>4} {share:>6.0%}  {'':>3} {totals['blocks']:>4}")
    print(f"\nthe 42 live posts total {sum(v[2] for v in manifest.EXISTING.values()):,} words "
          f"between them today")

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

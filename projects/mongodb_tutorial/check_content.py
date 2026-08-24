#!/usr/bin/env python3
"""Prove every code sample round-trips, and enforce this track's own rules.

The migration nearly shipped corrupted code blocks because an HTML parser ate the raw
<script>/<style>/onclick= that legitimately appear *inside* code samples, and the damage barely
changed the character count — so length checks passed. Compare sources, not lengths. No AWS access
needed.

MongoDB sharpens that differently from Python: a mongosh snippet is mostly braces, dollar-prefixed
operator names and quoted keys. `$group`, `$lookup`, `$inc` all start with a character a template
engine may treat as special, and `{$gt: 5}` is one stray unescape away from being valid-looking
nonsense. A block that loses a brace still looks like JavaScript.

On top of the round-trip check this enforces six rules specific to this track. Note that rule 5 is
the INVERSE of the FastAPI track's: there every rewrite had to get SHORTER, because those nine
posts were each three times too long. Here the three live posts serve 193, 106 and ZERO words, so a
rewrite that does not grow substantially has not happened.

  1. Every one of the THREE frozen slugs is still in the manifest. Those URLs are indexed and
     losing one is a 404 on a live page.
  2. Every post fits the 6-9 reading-minute budget. ⚠️ The pipeline counts PROSE AND CODE
     together, so this is a cap on the total, not on the writing.
  3. Prose is at least 45% of the words. At this length it matters more, not less: 1,980 words is
     about a dozen modest code blocks, and a post that spends 70% of them on listings has
     explained nothing.
  4. A post that makes a storage, timing or count claim quotes a figure from manifest.MEASURED.
     Every number in this track was measured on one machine on one day; an unsourced megabyte is
     how a marketing claim gets published as fact.
  5. Frozen posts must actually GROW. See above.
  6. Every post date falls inside the agreed 2024-2025 window, and every post carries tags —
     not one of the three live posts has any, so the tag pages for this category are empty.

While the track is being authored, posts with no file yet are reported as `not written` and do not
fail the run. Once every file exists this becomes a plain pass/fail.

    python projects/mongodb_tutorial/check_content.py
"""

import html
import os
import re
import sys
from datetime import datetime
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

# The language as AUTHORED, read off the source <pre>/<code> before normalisation.
LANG_IN_ATTRS = re.compile(r'language-([\w-]+)')


class _NoLang:
    @staticmethod
    def group(_n):
        return "plaintext"


_NO_LANG = _NoLang()

# Every language this track needs, checked on BOTH sides — the backend decides the class, the
# frontend supplies the grammar, and either one alone renders the block grey.
#
# All seven already exist on both sides, verified 2026-08-24:
#   backend  app/services/content.py SUPPORTED_LANGUAGES
#   frontend src/lib/content.ts      static prism imports
# `javascript` needs no frontend import — Prism core ships it. So unlike the Hasura track (which
# had to ADD `graphql` to both), this track needs NO content-pipeline change. This guards against
# a regression, not a gap.
REQUIRED_LANGUAGES = {"javascript", "java", "bash", "json", "yaml", "properties", "xml"}
BACKEND_HAS = content_service.SUPPORTED_LANGUAGES
# xml maps onto Prism's `markup`, which the backend spells "markup".
LANGUAGE_ALIAS = {"xml": "markup"}

# Rule 4. A post that says something is a given size, faster, or a given count has to quote a
# figure that was actually measured. The trigger is deliberately broad and the requirement narrow:
# if you make a claim, cite one of the recorded numbers.
CLAIMS_MEASUREMENT = re.compile(
    r"\b(\d+(?:\.\d+)?\s*(?:MB|GB|ms)\b|\d+\s*%\s*(?:faster|slower|smaller|larger)"
    r"|\bbenchmark|\bmeasured\b|\bkeysExamined\b|\bdocsExamined\b)", re.I)

_M = manifest.MEASURED
MEASURED_STRINGS = {
    str(_M["ts_random_mb"]), str(_M["ts_sorted_mb"]), str(_M["ts_plain_mb"]),
    str(_M["ts_ratio"]), str(_M["ts_buckets"]), f"{_M['ts_buckets']:,}",
    str(_M["ts_per_bucket"]), str(_M["ts_metadata_combos"]),
    str(_M["ts_measurements"]), f"{_M['ts_measurements']:,}",
    str(_M["feed_keys_examined"]), str(_M["feed_docs_examined"]), str(_M["feed_returned"]),
    _M["feed_plan_index"], _M["creator_index_stored"],
    str(_M["docs_view_events"]), f"{_M['docs_view_events']:,}",
    str(_M["tests_backend"]), str(_M["tests_e2e"]),
}

# Documented server limits, not measurements. Quoting "the 16 MB document cap" is citing the
# MongoDB manual, and demanding it be backed by our own benchmark would be nonsense — the rule
# exists to stop UNSOURCED numbers, not to stop well-known constants.
DOCUMENTED_LIMITS = {"16 MB", "32 MB", "100 MB", "16MB", "32MB", "100MB"}

# Posts REQUIRED to carry a measurement, because their whole argument rests on one.
MUST_CITE = {
    "mongodb-indexes": [str(_M["feed_keys_examined"]), _M["feed_plan_index"]],
    "mongodb-change-streams": [str(_M["ts_per_bucket"])],
}


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
totals = {"words": 0, "prose": 0, "code": 0, "blocks": 0}
seen_languages: set[str] = set()

# --- rule 1: the frozen slugs are all still here ----------------------------
manifest_slugs = {e["slug"] for e in manifest.POSTS}
lost = [s for s in manifest.FROZEN_SLUGS if s not in manifest_slugs]
if lost:
    failures.append(
        "frozen slug dropped from the manifest: " + ", ".join(lost) +
        " — these are live indexed URLs and removing one is a 404")

# --- rule 6a: dates inside the agreed window -------------------------------
low, high = manifest.DATE_WINDOW
for entry in manifest.POSTS:
    when = datetime.fromisoformat(entry["date"])
    if not (low <= when <= high):
        failures.append(
            f"{entry['slug']}: date {entry['date'][:10]} is outside the agreed "
            f"{low:%Y}-{high:%Y} window")

print(f"{'slug':<42} {'prose':>6} {'code':>6} {'total':>6} {'min':>4} {'prose%':>7}  "
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
    seen_languages.update(langs)

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

    # A block that SILENTLY normalised to plaintext is a language the backend does not support.
    #
    # Authoring `language-plaintext` on purpose is legitimate — a server error message or a
    # command transcript has no grammar worth applying. So compare what was ASKED FOR against
    # what came out, and only complain when they differ. Warning on every plaintext block makes
    # the deliberate ones noise, and noise is how a real downgrade gets scrolled past.
    authored_langs = [
        (LANG_IN_ATTRS.search(attrs) or LANG_IN_ATTRS.search(inner[:200]) or _NO_LANG).group(1)
        for attrs, inner in SOURCE_PRE.findall(raw)
    ]
    downgraded = [
        (i, want) for i, (want, got) in enumerate(zip(authored_langs, langs))
        if got == "plaintext" and want != "plaintext"
    ]
    if downgraded:
        detail = ", ".join(f"block {i} asked for {want!r}" for i, want in downgraded)
        failures.append(f"{entry['slug']}: {len(downgraded)} block(s) silently downgraded to "
                        f"plaintext — {detail}. Add the language to SUPPORTED_LANGUAGES, or the "
                        "block renders grey.")

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
        # Compare MINUTES, not raw words. The budget Folau agreed was 6-9 reading minutes, and
        # readingMinutes is what the site actually displays. A post at 1,298 words shows as 6 min
        # and is on target; failing it against a 1,320-word floor is the check disagreeing with
        # the spec it is meant to enforce.
        warnings.append(
            f"{entry['slug']}: {words} words = {result['readingMinutes']} min, under the "
            f"{manifest.TARGET_MINUTES[0]}-minute floor — thin for a whole topic")

    # (3) the prose floor — the anti-code-dump rule
    if share < manifest.MIN_PROSE_SHARE:
        failures.append(
            f"{entry['slug']}: prose is {share:.0%} of the words, floor is "
            f"{manifest.MIN_PROSE_SHARE:.0%} ({prose} prose vs {code} code). "
            "That is a listing with commentary, not a lesson.")

    # (5) a rewrite has to actually GROW — the inverse of the FastAPI rule
    if entry["frozen"]:
        _p, _c, baseline, base_min = manifest.EXISTING[entry["slug"]]
        if words <= baseline:
            failures.append(
                f"{entry['slug']}: rewrite is {words} words but the live page already has "
                f"{baseline} — the whole point was to replace an empty or near-empty page")

    # (4) claims must be sourced
    text = TAGS.sub(" ", body)
    # Strip the documented constants before testing, so a post that only mentions those is not
    # asked to cite a benchmark for them.
    claim_text = text
    for limit in DOCUMENTED_LIMITS:
        claim_text = claim_text.replace(limit, "")
    if CLAIMS_MEASUREMENT.search(claim_text) and not any(s in body for s in MEASURED_STRINGS):
        warnings.append(
            f"{entry['slug']}: makes a measurement claim but quotes no figure from "
            "manifest.MEASURED")
    for required in MUST_CITE.get(entry["slug"], []):
        if required not in body:
            failures.append(
                f"{entry['slug']}: must quote the measured value {required!r} — its argument "
                "rests on it")

    # (6b) tags — the existing three have none, and that is one of the defects being fixed
    if not entry.get("tags"):
        failures.append(f"{entry['slug']}: no tags. The 2019 posts had none and the tag pages "
                        "for this category are empty because of it.")

    print(f"{entry['slug']:<42} {prose:>6} {code:>6} {words:>6} "
          f"{result['readingMinutes']:>4} {share:>6.0%}  "
          f"{len(result['toc']):>3} {len(emitted):>4}")

# --- language support, both sides ------------------------------------------
for lang in sorted(seen_languages):
    if lang == "plaintext":
        continue
    if lang not in BACKEND_HAS:
        failures.append(f"language {lang!r} is used but not in the backend's SUPPORTED_LANGUAGES "
                        "— it will normalise to plaintext")

print("-" * 96)
if written:
    share = totals["prose"] / totals["words"] if totals["words"] else 0
    print(f"{'TOTAL ' + str(written) + ' post(s)':<42} {totals['prose']:>6} {totals['code']:>6} "
          f"{totals['words']:>6} {round(totals['words'] / 220):>4} {share:>6.0%}  "
          f"{'':>3} {totals['blocks']:>4}")

    baseline_total = sum(v[2] for v in manifest.EXISTING.values())
    print(f"\nthe three live posts total {baseline_total} words today; "
          f"this track's frozen rewrites are the replacement")

if missing:
    print(f"\nnot written yet ({len(missing)}): " + ", ".join(missing))

if warnings:
    print(f"\n⚠️  {len(warnings)} warning(s):")
    for w in warnings:
        print("   - " + w)

if failures:
    print(f"\n❌ {len(failures)} failure(s):")
    for f in failures:
        print("   - " + f)
    sys.exit(1)

if missing:
    print(f"\n✅ {written} written post(s) pass. {len(missing)} still to write.")
else:
    print(f"\n✅ all {written} posts pass every rule.")

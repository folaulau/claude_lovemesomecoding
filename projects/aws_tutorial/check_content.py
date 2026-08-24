#!/usr/bin/env python3
"""Prove every code sample round-trips, and enforce this track's own rules.

The migration nearly shipped corrupted code blocks because an HTML parser ate the raw
<script>/<style>/onclick= that legitimately appear *inside* code samples, and the damage barely
changed the character count — so length checks passed. Compare sources, not lengths.

This track sharpens that in its own way: a code sample here is frequently a JSON policy document
full of `"Resource": "arn:aws:s3:::bucket/*"`, or a shell line containing `2>&1`, or a JMESPath
query full of `[]` and `?`. Every one of those has a character an HTML parser can decide to
interpret. Byte-for-byte is the only check worth running. No AWS access needed.

On top of the round-trip check this enforces the rules specific to the AWS track:

  1. All 33 FROZEN slugs are still in the manifest. Each is a live indexed URL, and losing one is
     a 404 on a page Google already has. `aws-ecr` is the one post that is genuinely new, so it
     has no indexed URL to protect and is exempt from this rule but not from any other.
  2. Every post fits the 4-6 reading-minute budget, unless it is in manifest.LENGTH_EXEMPT —
     a declared table with a reason per entry, so an exemption is a decision on the record rather
     than the cap being quietly dropped. The FLOOR still applies to an exempt post.
     ⚠️ The pipeline counts PROSE AND CODE together, so a 40-line IAM policy can blow the budget
     without a single extra sentence.
  3. Prose is at least 45% of the words. JSON is even easier than SQL to fill a word budget with —
     one pasted policy is 400 words of `"Effect": "Allow"` — and the result is a listing with
     captions rather than a lesson.
  4. A rewrite has to be a REWRITE, proved two ways: every post clears the word floor, and no
     post shares a long verbatim run with the body it replaced.
     ⚠️ This is NOT the Postgres track's "grew by 4x" rule, and the difference is the whole point.
     That rule assumes the original is a stub. Here `aws-elasticache` is 2,184 words and
     `aws-s3` is 1,584 — of copied AWS product-page marketing — so "must grow" is not only wrong,
     it is unsatisfiable: 8 of the 26 non-blank posts cannot be twice their original AND fit the
     4-6 minute cap. For those, the correct rewrite is SHORTER. What actually distinguishes a
     rewrite from a light edit is whether the text is new, so that is what gets measured, against
     originals/prose.json.gz. See progress_report.md.
  5. No AWS account number. A 12-digit run of digits in a post is almost certainly a real account
     id pasted out of a console, and it is not something to publish. ARNs in samples use a
     placeholder. This is the one rule here that is about safety rather than quality.
  6. No dead WordPress markup. `boldgrid-section`, `col-md-*`, `class=""` and `/index.php?name=`
     are the exact defects being rewritten away; a post that reintroduces one has been
     copy-pasted out of the old body rather than written.
  7. A post about a service a reader cannot adopt has to say so above the fold. `aws-codecommit`
     and `aws-alexa` are declared `closed` in the manifest, and the warning has to be in the
     first heading-to-heading section, not buried at the end.
  8. Images are not hotlinked to AWS. 12 of the 36 images in the current collection point at
     docs.aws.amazon.com or d1.awsstatic.com, which AWS reorganizes without notice.

While the track is being authored, posts with no file yet are reported as `not written` and do not
fail the run. Once every file exists this becomes a plain pass/fail.

    lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/check_content.py
"""

import gzip
import html
import json
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
REQUIRED_LANGUAGES = {"bash", "json", "yaml", "python"}
PRISM_IMPORTS = {
    "bash": "prism-bash", "json": "prism-json", "yaml": "prism-yaml", "python": "prism-python",
}

# Rule 5. A 12-digit number is an AWS account id. Checked on the raw source so it catches one in
# an attribute or a comment too, not only in rendered text.
ACCOUNT_ID = re.compile(r"(?<!\d)\d{12}(?!\d)")
# The placeholder the track uses instead. Declared so the rule has an answer, not just a refusal.
ACCOUNT_PLACEHOLDER = "111122223333"  # the id AWS's own docs use for examples

# ⚠️ The last group of a UUID is twelve hex characters, so an all-numeric one — which is exactly
# what an example id like `amzn1.ask.skill.00000000-0000-0000-0000-000000000000` contains — trips
# the account-id rule. That is a false positive, and a false positive on a safety rule is how a
# safety rule gets switched off. So a match sitting inside a UUID-shaped token is skipped.
#
# Deliberately NOT solved by requiring no adjacent hyphen: `my-bucket-123456789012` is a genuine
# way an account id leaks, and that spelling has to keep failing.
UUID_TOKEN = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")

# Rule 6. The markup this rewrite exists to remove.
WORDPRESS_CRUFT = {
    "boldgrid": re.compile(r"boldgrid"),
    "col-md-/col-xs-": re.compile(r"col-(?:md|xs|sm)-\d"),
    'class=""': re.compile(r'class=""'),
    "/index.php?name=": re.compile(r"/index\.php\?name="),
}

# Rule 8. Images we must not hotlink.
FOREIGN_IMAGE = re.compile(r'<img[^>]+src="https?://(?!d2q2snz6diubfd\.cloudfront\.net)([^"/]+)')

# Rule 7. Wording that counts as declaring a service closed.
#
# ⚠️ Matched against WHITESPACE-COLLAPSED text, not the raw rendered text. The post bodies are
# hard-wrapped at about 100 characters, so a phrase like "you cannot\ncreate one" carries a
# newline in the middle and a pattern expecting a literal space silently misses it. That is a
# false NEGATIVE on a rule whose whole job is to catch a missing warning — the worst direction for
# this particular rule to fail in. Caught on aws-codecommit, whose first sentence says exactly the
# right thing and was reported as saying nothing.
CLOSED_MARKER = re.compile(
    r"closed \S*\s*to new customers|closed to new customers|no longer accepting new|"
    r"not an AWS service|stopped onboarding|ceased onboarding|"
    r"cannot create (?:a |an )?(?:new )?(?:repositor|one|cluster)", re.I)


# Rule 4b. The original prose of all 33 live posts, captured by originals/snapshot.py.
ORIGINALS_PATH = HERE / "originals" / "prose.json.gz"
if not ORIGINALS_PATH.exists():
    raise SystemExit(
        f"missing {ORIGINALS_PATH}\n"
        "Rule 4 compares each rewrite against the body it replaces. Regenerate it with:\n"
        "  lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/originals/snapshot.py")
with gzip.open(ORIGINALS_PATH, "rt", encoding="utf-8") as _fh:
    ORIGINALS = json.load(_fh)

# The longest run of words a rewrite may share with the old content.
#
# Tuned, not guessed. Technical writing about one service legitimately repeats short phrases —
# "the AWS Management Console", "a dead-letter queue", "you are charged for provisioned storage" —
# and a threshold low enough to catch those is a threshold that gets switched off. Twelve
# consecutive identical words is well past coincidence and reliably means a paragraph was pasted.
MAX_SHARED_RUN = 12

WORD = re.compile(r"[A-Za-z0-9]+")


def _shingles(words, size):
    """Every run of `size` consecutive words, as (index, tuple)."""
    return [(i, tuple(words[i:i + size])) for i in range(len(words) - size + 1)]


def _build_original_index(originals, size):
    """shingle -> the slug(s) it appears in, across ALL 33 original bodies.

    ⚠️ Checked against EVERY original, not just the post's own.

    The first version compared each rewrite only with the body at the same slug, which misses the
    obvious cheat and the likely accident: pasting AWS product-page prose that happens to sit in a
    sibling post. Verified by planting the original `aws-lambda` marketing paragraph into the
    Kinesis post — the same-slug rule passed it, because Kinesis's own original is blank.

    Also deliberately NOT difflib. SequenceMatcher over 33 x 33 bodies is hundreds of millions of
    comparisons; hashing shingles once makes the whole check linear and instant, and "12+
    consecutive shared words" is exactly a shingle match.
    """
    index = {}
    for slug, text in originals.items():
        words = [w.lower() for w in WORD.findall(text)]
        for _i, shingle in _shingles(words, size):
            index.setdefault(shingle, set()).add(slug)
    return index


def shared_runs(new_text, index, size):
    """Yield (run_text, source_slugs) for each maximal pasted run in `new_text`.

    Overlapping shingle hits are merged so one pasted paragraph is reported once, at its real
    length, rather than as forty near-identical findings.
    """
    words = [w.lower() for w in WORD.findall(new_text)]
    hits = [(i, index[sh]) for i, sh in _shingles(words, size) if sh in index]
    if not hits:
        return []
    runs, start, end, sources = [], hits[0][0], hits[0][0] + size, set(hits[0][1])
    for i, slugs in hits[1:]:
        if i <= end:                      # overlaps the run being built — extend it
            end = i + size
            sources |= slugs
        else:
            runs.append((" ".join(words[start:end]), sources))
            start, end, sources = i, i + size, set(slugs)
    runs.append((" ".join(words[start:end]), sources))
    return runs


ORIGINAL_INDEX = _build_original_index(ORIGINALS, MAX_SHARED_RUN)


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

print(f"{'slug':<40} {'prose':>6} {'code':>6} {'total':>6} {'min':>4} {'prose%':>7}  "
      f"{'hd':>3} {'blk':>4}   was")
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

    missing_ids = [t for t in result["toc"] if not t.get("id")]
    if missing_ids:
        failures.append(f"{entry['slug']}: {len(missing_ids)} heading(s) with no anchor")

    # Characters outside the house set — a stray CJK character mid-sentence reads as a normal word
    # at a glance and would otherwise ship.
    # Box-drawing characters are deliberate: several posts draw a small architecture diagram in a
    # plaintext block, and that is a better fit than an image we would then have to host.
    ALLOWED_NON_ASCII = set("—–’‘“”…×→±⚠️✓✗‹›°éíóúñ" "─│┌┐└┘├┤┬┴┼")
    stray = sorted({c for c in raw if ord(c) > 127} - ALLOWED_NON_ASCII)
    if stray:
        failures.append(
            f"{entry['slug']}: unexpected character(s) {stray} — a typo, or add it to "
            "ALLOWED_NON_ASCII if it is deliberate")

    if not result["toc"]:
        failures.append(f"{entry['slug']}: no h2/h3 at all — no table of contents, no deep links. "
                        "That is the defect this whole track exists to fix: 33 posts and 2 "
                        "headings between them.")

    # --- this track's own rules ---------------------------------------------
    words = result["wordCount"]
    prose, code = prose_and_code_words(result)
    share = prose / words if words else 0
    totals["words"] += words
    totals["prose"] += prose
    totals["code"] += code
    text = TAGS.sub(" ", body)

    # (2) the reading-time budget
    #
    # Tested on readingMinutes, not on the word count, because readingMinutes is the number the
    # reader sees and it is ROUNDED: 1,378 words is 6.3, published as "6 min".
    minutes = result["readingMinutes"]
    low, high = manifest.TARGET_MINUTES
    high = manifest.LENGTH_EXEMPT.get(entry["slug"], high)
    if minutes > high:
        failures.append(
            f"{entry['slug']}: {minutes} min ({words} words), over the {high}-minute cap. "
            f"Remember code counts: {code} of these words are code.")
    elif minutes < low:
        warnings.append(
            f"{entry['slug']}: {minutes} min ({words} words), under the {low}-minute floor — "
            "thin for a whole service")

    # (3) the prose floor — the anti-policy-dump rule
    if share < manifest.MIN_PROSE_SHARE:
        failures.append(
            f"{entry['slug']}: prose is {share:.0%} of the words, floor is "
            f"{manifest.MIN_PROSE_SHARE:.0%} ({prose} prose vs {code} code). "
            "That is a listing with commentary, not a lesson.")

    # (4a) every post clears the word floor, blank or not
    #
    # ⚠️ Deliberately NOT "must be bigger than the original". Eight of the 26 non-blank posts are
    # already longer than the 4-6 minute cap allows, because they are padded marketing copy —
    # aws-elasticache is 2,184 words. For those the correct rewrite is SHORTER, and a growth rule
    # would forbid the right answer. The floor is absolute; the cap in rule 2 is the other side.
    if words < manifest.TOTAL_WORDS_MIN:
        blank_note = (" This post is BLANK on the live site, so the floor is the only bar."
                      if entry["slug"] in manifest.BLANK else
                      " This post is new, so the floor is the only bar."
                      if entry["state"] == "new" else "")
        failures.append(
            f"{entry['slug']}: {words} words, under the track floor of "
            f"{manifest.TOTAL_WORDS_MIN}.{blank_note}")

    # (4b) and it has to be NEW TEXT, which is what actually separates a rewrite from an edit
    for run, sources in shared_runs(text, ORIGINAL_INDEX, MAX_SHARED_RUN):
        where = "its own old body" if sources == {entry["slug"]} else \
            "the old " + ", ".join(sorted(sources))
        failures.append(
            f"{entry['slug']}: shares a {len(run.split())}-word verbatim run with {where} — "
            f"\"{run[:110]}…\". That was pasted, not rewritten. The copied AWS product-page prose "
            "is the defect this track exists to remove.")

    # (5) no account numbers
    uuid_spans = [m.span() for m in UUID_TOKEN.finditer(raw)]
    for match in ACCOUNT_ID.finditer(raw):
        if match.group() == ACCOUNT_PLACEHOLDER:
            continue
        start, end = match.span()
        if any(u_start <= start and end <= u_end for u_start, u_end in uuid_spans):
            continue  # the tail of a UUID, not an account id
        failures.append(
            f"{entry['slug']}: contains the 12-digit number {match.group()}, which is the shape "
            f"of an AWS account id. Use the documentation placeholder {ACCOUNT_PLACEHOLDER}.")

    # (6) no resurrected WordPress markup
    for label, pattern in WORDPRESS_CRUFT.items():
        if pattern.search(raw):
            failures.append(
                f"{entry['slug']}: contains `{label}` — dead WordPress markup. This post was "
                "copy-pasted out of the old body rather than rewritten.")

    # (7) a closed service has to say so early
    if entry["closed"]:
        head = " ".join(text.split())[:900]
        if not CLOSED_MARKER.search(head):
            failures.append(
                f"{entry['slug']}: declared `closed` in the manifest but the first 900 characters "
                "do not say so. A reader who stops after the intro must not be left thinking "
                "they can adopt this.")

    # (8) no hotlinked images
    for host in set(FOREIGN_IMAGE.findall(raw)):
        failures.append(
            f"{entry['slug']}: hotlinks an image from {host}. Host it on the media CDN or drop "
            "it — AWS reorganizes those paths without notice.")

    was = manifest.EXISTING.get(entry["slug"])
    was_col = f"{was[2]:>5}w/{was[3]}m" if was else f"{'new':>9}"
    print(f"{entry['slug']:<40} {prose:>6} {code:>6} {words:>6} "
          f"{result['readingMinutes']:>4} {share:>6.0%}  "
          f"{len(result['toc']):>3} {len(emitted):>4}   {was_col}"
          + (f"  {len(plain)} plaintext" if plain else ""))

# ---------------------------------------------------------------- manifest rules
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest.POSTS")

dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend — the prev/next pager would read out of order")

# (1) every one of the 33 indexed URLs
for frozen in sorted(manifest.FROZEN_SLUGS):
    if frozen not in slugs:
        failures.append(f"frozen slug {frozen} is no longer in the manifest — that URL is indexed")

if manifest.FROZEN_SLUGS != set(manifest.EXISTING):
    failures.append("FROZEN_SLUGS and EXISTING disagree — one was edited without the other. "
                    "EXISTING holds the measured 'before' for every rewrite; a NEW slug must be "
                    "in neither.")

# A new slug with a baseline means someone added it to EXISTING, which would make it look like a
# rewrite of something. A frozen slug without one means a live post lost its measured baseline.
for entry in manifest.POSTS:
    if entry["state"] not in ("rewrite", "new"):
        failures.append(f"{entry['slug']}: state is {entry['state']!r}, expected rewrite or new")
    if entry["state"] == "new" and entry["slug"] in manifest.EXISTING:
        failures.append(f"{entry['slug']}: marked new but has an EXISTING baseline")
    if entry["state"] == "rewrite" and entry["slug"] not in manifest.EXISTING:
        failures.append(f"{entry['slug']}: marked rewrite but has no EXISTING baseline")
    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")
    if not entry["tags"]:
        failures.append(f"{entry['slug']}: no tags")
    if "aws" not in entry["tags"]:
        warnings.append(f"{entry['slug']}: tags do not include 'aws'")

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
    live_total = sum(v[2] for v in manifest.EXISTING.values())
    print(f"{'WRITTEN ' + str(written) + '/' + str(len(manifest.POSTS)):<40} "
          f"{totals['prose']:>6} {totals['code']:>6} {totals['words']:>6} "
          f"{'':>4} {share:>6.0%}  {'':>3} {totals['blocks']:>4}")
    print(f"\nthe live collection totals {live_total} words across all 33 posts, "
          f"with {sum(1 for v in manifest.EXISTING.values() if v[2] == 0)} of them blank")

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

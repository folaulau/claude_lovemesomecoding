#!/usr/bin/env python3
"""Prove every code sample round-trips, and enforce this track's own rules.

The migration nearly shipped corrupted code blocks because an HTML parser ate the raw
<script>/<style>/onclick= that legitimately appear *inside* code samples, and the damage barely
changed the character count — so length checks passed. Compare sources, not lengths. No AWS access
needed.

A NestJS track has its own version of that hazard, and it is worse than the TypeScript track's.
Nearly every block here is decorated TypeScript, which means the blocks are full of `<`:
generics (`ConfigService<AppConfig>`, `Observable<unknown>`, `Repository<User>`), and the arrow
functions inside `@OneToMany('Project', (p: Project) => p.homeowner)`. An HTML parser is entitled
to read `<AppConfig>` as a tag. A block that has quietly lost `<AppConfig>` still looks like
perfectly good Nest code — and `ConfigService<AppConfig>` silently becoming `ConfigService` is
exactly the damage a length check waves through.

On top of the round-trip check this enforces the rules specific to this track:

  1. Every post fits the 8-10 reading-minute budget. ⚠️ The pipeline counts PROSE AND CODE
     together, so this is a cap on the total, not on the writing.
  2. Prose is at least 40% of the words. Lower than the TypeScript track's 45% because a
     framework post legitimately quotes a whole guard or a whole module — see
     manifest.MIN_PROSE_SHARE for why that follows rather than being a concession.
  3. No block renders as `plaintext` by accident. Every language this track uses is supported on
     both halves, so an unexpected plaintext block is a typo in a class attribute — and it fails
     silently, because an unsupported language is normalised rather than rejected.
  4. A block showing the WRONG way sits near manifest.ANTIPATTERN_MARKER. Almost every block here
     is quoted from a file that runs, so an unmatched block is a stale quote unless it says
     otherwise; without the marker check_snippets.py cannot tell those two apart.
  5. The manifest is coherent: unique slugs, ascending dates, every post declaring the files it
     may quote, and every declared file actually existing.

While the track is being authored, posts with no file yet are reported as `not written` and do not
fail the run. Once every file exists this becomes a plain pass/fail.

    python projects/nestjs_tutorial/check_content.py
"""

import html
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
BACKEND = REPO_ROOT / "lovemesomecoding_backend"

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

# The language as AUTHORED, read off the source <pre>'s class attribute — as opposed to the
# language the pipeline settled on. The two differ exactly when the authored one is unsupported,
# which is what rule 3 is looking for.
AUTHORED_LANG = re.compile(r"language-([\w-]+)")

# Exactly what the frontend's build-time highlighter matches. If the shape changes on either side,
# highlighting silently stops.
FRONTEND_SHAPE = re.compile(r'<pre class="language-([\w-]+)"><code class="language-\1">')

# Every language this track needs. Checked on BOTH sides — the backend decides the class, the
# frontend supplies the grammar, and either one alone renders the block grey. All four already
# exist (verified 2026-09-05), so this guards against a regression rather than filling a gap.
REQUIRED_LANGUAGES = {"typescript", "json", "bash", "sql"}
PRISM_IMPORTS = {
    "typescript": "prism-typescript", "json": "prism-json",
    "bash": "prism-bash", "sql": "prism-sql",
}

# Rule 4. What a block showing the WRONG way looks like.
#
# ⚠️ This track uses the marker far less than the TypeScript track did, and the difference is
# structural rather than stylistic. There, half the job was showing code the compiler rejects, and
# none of it could live in the app. Here almost every block is lifted from a file that compiles
# and runs — so an unmatched block is a stale quote by default, and the marker is the only way to
# say "this one is unmatched on purpose".
#
# The house style is a comment naming what is wrong, because a block that merely looks different
# from the app teaches nothing about why the app is not written that way.
WRONG_WAY = re.compile(
    r"(// ✗|// Wrong|// WRONG|// BUG|// Never|// Do not|// Don't|// Bad|"
    r"// This is the bug|// looks fine, and is not)", re.I)

ANTIPATTERN = re.compile(re.escape(manifest.ANTIPATTERN_MARKER), re.I)

# How far back to look for the marker. Far enough to cover a heading plus an intro paragraph,
# short enough not to leak in from the previous section. Same window check_snippets.py uses, and
# they must agree — that is the entire point of this rule.
MARKER_WINDOW = 400


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

    # The code samples as authored, and the language each one CLAIMED.
    authored = []
    authored_langs = []
    for attrs, inner in SOURCE_PRE.findall(raw):
        wrapped = INNER_CODE.match(inner)
        if wrapped:
            inner = wrapped.group(1)
        authored.append(html.unescape(inner))
        claimed = AUTHORED_LANG.search(attrs)
        authored_langs.append(claimed.group(1) if claimed else None)

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

    # (3) plaintext by ACCIDENT is a typo; plaintext on purpose is fine.
    #
    # ⚠️ The distinction is the whole rule. `plaintext` is the right language for a stack trace or
    # a Nest startup log — neither is TypeScript and Prism has no grammar for either — so banning
    # it outright would be wrong. But an unsupported language is NORMALISED to plaintext rather
    # than rejected, so `language-typescrpt` also lands here, silently, rendering grey.
    mistyped = [(i, authored_langs[i]) for i, lang in enumerate(langs)
                if lang == "plaintext" and authored_langs[i] != "plaintext"]
    if mistyped:
        detail = ", ".join(f"block {i} claims {claimed!r}" for i, claimed in mistyped)
        failures.append(
            f"{entry['slug']}: {len(mistyped)} block(s) fell back to plaintext because the "
            f"language is not supported — {detail}. That renders grey without complaining.")

    if not emitted:
        failures.append(f"{entry['slug']}: no code blocks at all")

    missing_ids = [t for t in result["toc"] if not t.get("id")]
    if missing_ids:
        failures.append(f"{entry['slug']}: {len(missing_ids)} heading(s) with no anchor")

    # (4) a wrong-way demonstration has to be marked as one
    for i, match in enumerate(OUT_PRE.finditer(body)):
        if match.group(1) not in ("typescript", "json"):
            continue
        block_text = html.unescape(match.group(2))
        if not WRONG_WAY.search(block_text):
            continue
        window = body[max(0, match.start() - MARKER_WINDOW):match.start()]
        if not (ANTIPATTERN.search(window) or ANTIPATTERN.search(match.group(0))):
            warnings.append(
                f"{entry['slug']} block {i}: shows the wrong way but no "
                f"{manifest.ANTIPATTERN_MARKER!r} within {MARKER_WINDOW} chars before it — "
                "check_snippets.py will treat it as a stale quote")

    # --- the length budget --------------------------------------------------
    words = result["wordCount"]
    prose, code = prose_and_code_words(result)
    share = prose / words if words else 0
    totals["words"] += words
    totals["prose"] += prose
    totals["code"] += code

    # (1) the reading-time budget
    if words > manifest.TOTAL_WORDS_MAX:
        failures.append(
            f"{entry['slug']}: {words} words = {result['readingMinutes']} min, over the "
            f"{manifest.TOTAL_WORDS_MAX}-word cap ({manifest.TARGET_MINUTES[1]} min). "
            f"Remember code counts: {code} of these are code.")
    elif words < manifest.TOTAL_WORDS_MIN:
        warnings.append(
            f"{entry['slug']}: {words} words = {result['readingMinutes']} min, under the "
            f"{manifest.TOTAL_WORDS_MIN}-word floor — thin for a whole topic")

    # (2) the prose floor — the anti-repository-tour rule
    if share < manifest.MIN_PROSE_SHARE:
        failures.append(
            f"{entry['slug']}: prose is {share:.0%} of the words, floor is "
            f"{manifest.MIN_PROSE_SHARE:.0%} ({prose} prose vs {code} code). "
            "That is a tour of a repository, not an explanation of one.")

    print(f"{entry['slug']:<44} {prose:>6} {code:>6} {words:>6} "
          f"{result['readingMinutes']:>4} {share:>6.0%}  "
          f"{len(result['toc']):>3} {len(emitted):>4}")

# ---------------------------------------------------------------- manifest rules
slugs = [e["slug"] for e in manifest.POSTS]
if len(set(slugs)) != len(slugs):
    failures.append("duplicate slug in manifest.POSTS")

files = [e["file"] for e in manifest.POSTS]
if len(set(files)) != len(files):
    failures.append("duplicate file in manifest.POSTS")

dates = [e["date"] for e in manifest.POSTS]
if dates != sorted(dates):
    failures.append("manifest dates do not ascend — the prev/next pager would read out of order")

# FROZEN_SLUGS is empty today and that is correct — nothing is published under /nestjs. But
# anything in it must still be in the track, or the URL it protects has silently gone.
for frozen in sorted(manifest.FROZEN_SLUGS):
    if frozen not in slugs:
        failures.append(f"frozen slug {frozen} is no longer in the manifest — that URL is indexed")

for entry in manifest.POSTS:
    if len(entry["excerpt"]) > 500:
        failures.append(f"{entry['slug']}: excerpt is {len(entry['excerpt'])} chars, max 500")
    if not entry["tags"]:
        failures.append(f"{entry['slug']}: no tags")
    if entry["slug"] not in manifest.SNIPPET_SOURCES:
        failures.append(f"{entry['slug']}: no SNIPPET_SOURCES entry — check_snippets cannot "
                        "verify its code")

# Every declared snippet source must exist, or check_snippets silently verifies against nothing.
app = REPO_ROOT / manifest.DEMO_APP
for slug, sources in manifest.SNIPPET_SOURCES.items():
    for rel in sources:
        if not (app / rel).exists():
            failures.append(f"{slug}: SNIPPET_SOURCES names {rel!r}, which does not exist")

# ⚠️ The files this track ADDED to the demo app. They are the only source for lessons 7 and 10-12,
# so if one is deleted those posts quietly become unverifiable rather than failing.
for rel in manifest.ADDED_FOR_THIS_TRACK:
    if not (app / rel).exists():
        failures.append(f"ADDED_FOR_THIS_TRACK names {rel!r}, which does not exist — a lesson "
                        "depends on it")

# Language support, both halves.
for lang in sorted(REQUIRED_LANGUAGES):
    if lang not in content_service.SUPPORTED_LANGUAGES:
        failures.append(f"backend SUPPORTED_LANGUAGES is missing {lang!r}")
prism_file = REPO_ROOT / "lovemesomecoding_frontend/src/lib/content.ts"
if prism_file.exists():
    prism_src = prism_file.read_text(encoding="utf-8")
    for lang in sorted(REQUIRED_LANGUAGES):
        if PRISM_IMPORTS[lang] not in prism_src:
            failures.append(f"frontend content.ts does not import prismjs/components/"
                            f"{PRISM_IMPORTS[lang]}")

# The nav. This track's category is brand new, so the dropdown entry is a real task — and one that
# is invisible when forgotten: the posts publish and resolve perfectly, they are just unreachable
# from the menu.
nav_file = REPO_ROOT / "lovemesomecoding_frontend/src/lib/nav.ts"
if nav_file.exists():
    if f"'{manifest.CATEGORY['slug']}'" not in nav_file.read_text(encoding="utf-8"):
        warnings.append(
            f"nav.ts does not mention {manifest.CATEGORY['slug']!r} — the category will publish "
            f"but never appear in the {manifest.NAV_GROUP} dropdown")

# ---------------------------------------------------------------------- report
print("-" * 96)
if written:
    share = totals["prose"] / totals["words"] if totals["words"] else 0
    print(f"{'WRITTEN ' + str(written) + '/' + str(len(manifest.POSTS)):<44} "
          f"{totals['prose']:>6} {totals['code']:>6} {totals['words']:>6} "
          f"{'':>4} {share:>6.0%}  {'':>3} {totals['blocks']:>4}")
    print(f"\nbudget {manifest.TOTAL_WORDS_MIN}-{manifest.TOTAL_WORDS_MAX} words per post "
          f"({manifest.TARGET_MINUTES[0]}-{manifest.TARGET_MINUTES[1]} min), "
          f"prose floor {manifest.MIN_PROSE_SHARE:.0%}")

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

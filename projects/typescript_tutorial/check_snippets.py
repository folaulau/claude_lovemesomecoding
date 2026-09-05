#!/usr/bin/env python3
"""Prove every code sample still matches the pizza file it was copied from.

`check_content.py` proves a post's HTML survives the normaliser. It says NOTHING about whether a
quoted snippet is still true — a post can round-trip perfectly while quoting a module that was
rewritten a month ago. This is the check for that, and it is the one that goes stale on its own.

⚠️ READ THIS BEFORE JUDGING THE MATCH RATE. It is deliberately much lower here than in the FastAPI
track, and a low number is NOT a finding.

A framework tutorial quotes whole modules, so nearly every block should match the app and a miss
is drift. A LANGUAGE tutorial is not like that. Most blocks in this track are three or four lines
demonstrating one rule — `let x = 'a'` widening to `string` — and they belong in no repository,
because no repository contains code written to illustrate widening. On top of that, half of
teaching a type system is showing the code it REJECTS, and none of that compiles at all.

So the check that earns its keep here is not "did it match" but the NEAR-MISS detector: a block
whose opening lines ARE in the app but whose body is not. That is the signature of a real quote
that has gone stale, and it is what makes this exit non-zero.

Matching ignores indentation (a fragment lifted out of a class body is dedented when quoted) and
comments (the house style quotes the app verbatim MINUS its teaching comments — the pizza files
are heavily commented and repeating them would say everything twice). A line that is exactly `...`
or `// ...` marks a deliberate elision and splits the block into chunks that must each match,
though they need not be adjacent.

`manifest.SNIPPET_SOURCES` declares which files each post may quote, so a block is checked against
THAT file, not merely against the app somewhere. A snippet that drifts in from an unrelated module
is reported.

    python projects/typescript_tutorial/check_snippets.py
    python projects/typescript_tutorial/check_snippets.py --show-illustrative
"""

import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

APP = HERE.parent.parent / manifest.DEMO_APP

SKIP_DIRS = {"node_modules", "dist", "build", ".git", ".angular", "coverage", ".vite",
             "out-tsc", "__pycache__", ".next", "test-results", "playwright-report"}

BLOCK = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-[\w-]+">(.*?)</code></pre>', re.S)

# Languages that could plausibly have come out of the app as a FILE.
#
# `bash` is deliberately absent: every bash block is a command typed at a prompt, so checking it
# against file contents would report the whole track as drift. `markup` likewise — those are HTML
# fragments and Angular template snippets shown inline.
SOURCE_LANGS = {"typescript", "tsx", "json"}

SOURCE_SUFFIXES = {".ts", ".tsx", ".json", ".mjs", ".js"}

# How many opening lines must match before a near-miss counts as drift rather than an invented
# example that happens to start with a common line.
#
# ⚠️ This is the LONGEST MATCHING PREFIX, not a fixed-length lead, and the difference is the whole
# check. A fixed lead fails on the most common drift there is — a changed line INSIDE the lead:
#
#     export class ApiError extends Error {     <- still true
#       readonly status: number;                <- still true
#       readonly body: ApiErrorBody;            <- CHANGED (lost its `| null`)
#
# The fixed lead does not match, so the block gets filed as "illustrative" — the one bucket that
# never fails a build. Drift detection that silently reclassifies drift as fine is worse than none.
DRIFT_LEAD = 2

# A section deliberately showing code the compiler REJECTS. Those blocks must not match the app —
# that is the point of them — so they are excluded rather than reported.
#
# This track leans on the marker far harder than any other, because "here is what does not
# compile" is half the syllabus. check_content.py enforces the other direction: a block that shows
# a compiler error and is NOT marked gets a warning there.
ANTIPATTERN = re.compile(re.escape(manifest.ANTIPATTERN_MARKER), re.I)

# How far back to look for the marker. Must agree with check_content.py's MARKER_WINDOW.
MARKER_WINDOW = 400

BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


def strip_line_comment(line: str) -> str:
    """Cut a trailing `// ...`, but only when the `//` is not inside a string.

    ⚠️ Naively cutting at the first `//` corrupts real code, and this app is full of the reason:
    `'http://localhost:8085'` in api.ts, `'https://…'` in the Stripe helpers. The scan tracks
    quote state — including template literals — and only cuts at a `//` outside any string.
    """
    quote = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'`":
            quote = ch
        elif ch == "/" and line[i + 1:i + 2] == "/":
            return line[:i]
        i += 1
    return line


def strip_comments(text: str) -> str:
    text = BLOCK_COMMENT.sub("", text)
    text = HTML_COMMENT.sub("", text)
    return "\n".join(strip_line_comment(ln) for ln in text.splitlines())


def lines(text: str) -> list[str]:
    """Non-blank lines, indentation and comments stripped."""
    return [ln.strip() for ln in strip_comments(text).splitlines() if ln.strip()]


def contains(haystack: list[str], needle: list[str]) -> bool:
    if not needle:
        return True
    return any(haystack[i:i + len(needle)] == needle
               for i in range(len(haystack) - len(needle) + 1))


# Characters that carry no identity — brackets, quotes and separators. A line made only of these
# says nothing about WHICH file it came from.
STRUCTURAL = str.maketrans("", "", "{}[]()<>,:;\"'` \t")


def substantive(line: str) -> bool:
    """Does this line identify anything, or is it just punctuation?

    ⚠️ This exists because of a false positive that would otherwise fire on every invented JSON
    example in the track. DRIFT_LEAD counts matching opening lines, and a tsconfig opens

        {
        "compilerOptions": {

    which is the opening of EVERY tsconfig in the app. A hand-written config illustrating
    `allowJs`/`checkJs` — which is in no repository, and should not be — therefore matched two
    lines, cleared DRIFT_LEAD, and got reported as a drifted quote.

    Counting only lines that name something fixes it without weakening the check: a genuinely
    drifted quote still opens with real declarations, and those all survive this filter.
    """
    return len(line.translate(STRUCTURAL)) >= 3


def longest_prefix(haystack: list[str], needle: list[str]) -> int:
    """How many of `needle`'s opening lines appear in `haystack` as one contiguous run.

    Used to tell drift from invention: a quote that has drifted still opens with several real
    lines, while an invented example usually shares at most one common line like `interface Props {`.
    """
    best = 0
    for n in range(1, len(needle) + 1):
        if contains(haystack, needle[:n]):
            best = n
        else:
            break
    return best


def longest_suffix(haystack: list[str], needle: list[str]) -> int:
    """The same, from the other end.

    ⚠️ Both ends are needed, and a prefix-only check is what the FastAPI track ships. Measured
    against a deliberately drifted fixture on 2026-09-05: renaming `crustPriceDelta` in a quoted
    interface was NOT reported, because the renamed field was the FIRST line of its chunk. The
    prefix matched nothing, depth was 0, and the block was filed as `illustrative` — the bucket
    that never fails a build.

    Reading from the end catches it: the three lines after the rename are still contiguous in the
    app, so the chunk is clearly a real quote with one line changed.
    """
    best = 0
    for n in range(1, len(needle) + 1):
        if contains(haystack, needle[-n:]):
            best = n
        else:
            break
    return best


def drift_evidence(haystack: list[str], part: list[str]) -> tuple[str, str] | None:
    """Does this non-matching chunk look like a real quote that has gone stale?

    Returns (description, the line it diverges at), or None if the chunk looks invented.
    """
    pre = longest_prefix(haystack, part)
    if sum(1 for ln in part[:pre] if substantive(ln)) >= DRIFT_LEAD and pre < len(part):
        return (f"the first {pre} of {len(part)} lines ARE in the app", part[pre])

    suf = longest_suffix(haystack, part)
    if sum(1 for ln in part[len(part) - suf:] if substantive(ln)) >= DRIFT_LEAD and suf < len(part):
        return (f"the last {suf} of {len(part)} lines ARE in the app",
                part[len(part) - suf - 1])

    return None


def chunks_of(block: str) -> list[list[str]]:
    """Split on lines that are exactly `...` or `// ...`, the elision markers.

    ⚠️ Split BEFORE stripping comments, or `// ...` would already have been erased. And splitting
    on the bare substring rather than the whole line would break every spread and rest parameter
    in the app — `...opts`, `...product.sizes` — which is most of them.
    """
    out, current = [], []
    for ln in block.splitlines():
        if ln.strip() in ("...", "// ...", "/* ... */"):
            if current:
                out.append(lines("\n".join(current)))
            current = []
        else:
            current.append(ln)
    if current:
        out.append(lines("\n".join(current)))
    return [c for c in out if c]


def load_sources() -> dict[str, list[str]]:
    """Every quotable file in the app, as stripped lines, keyed by path relative to APP."""
    sources = {}
    for path in APP.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix not in SOURCE_SUFFIXES:
            continue
        try:
            sources[str(path.relative_to(APP))] = lines(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, OSError):
            continue
    return sources


def flagged_blocks(raw_html: str) -> set[int]:
    """Indices of blocks sitting inside a section marked as deliberately non-compiling."""
    flagged = set()
    for i, match in enumerate(BLOCK.finditer(raw_html)):
        window = raw_html[max(0, match.start() - MARKER_WINDOW):match.start()]
        if ANTIPATTERN.search(window) or ANTIPATTERN.search(match.group(0)):
            flagged.add(i)
    return flagged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-illustrative", action="store_true",
                        help="list the blocks that matched nothing in the app")
    args = parser.parse_args()

    if not APP.exists():
        raise SystemExit(f"demo app not found: {APP}")

    sources = load_sources()
    print(f"scanned {len(sources)} quotable files under {APP.relative_to(HERE.parent.parent)}\n")

    all_lines: list[str] = []
    for body in sources.values():
        all_lines.extend(body)

    drift, undeclared, illustrative = [], [], []
    checked = matched = skipped_lang = antipattern = written = 0

    print(f"{'slug':<44} {'blocks':>7} {'matched':>8} {'illus':>6} {'anti':>5}")
    print("-" * 74)

    for entry in manifest.POSTS:
        path = HERE / "posts" / entry["file"]
        if not path.exists():
            continue
        written += 1
        raw = path.read_text(encoding="utf-8")
        flagged = flagged_blocks(raw)

        declared = manifest.SNIPPET_SOURCES.get(entry["slug"], [])
        declared_lines: list[str] = []
        for rel in declared:
            if rel in sources:
                declared_lines.extend(sources[rel])
            else:
                # check_content.py fails on this too, from the filesystem side. Kept here so this
                # script is usable on its own.
                undeclared.append(
                    f"{entry['slug']}: SNIPPET_SOURCES names {rel!r}, which does not exist "
                    "in the app")

        post_blocks = post_matched = post_illus = post_anti = 0

        for i, (lang, escaped) in enumerate(BLOCK.findall(raw)):
            block = html.unescape(escaped)
            if lang not in SOURCE_LANGS:
                skipped_lang += 1
                continue
            if i in flagged:
                antipattern += 1
                post_anti += 1
                continue

            post_blocks += 1
            checked += 1
            parts = chunks_of(block)

            if all(contains(declared_lines, part) for part in parts):
                matched += 1
                post_matched += 1
                continue

            # Not in the files this post declared. Is it anywhere in the app?
            if all(contains(all_lines, part) for part in parts):
                undeclared.append(
                    f"{entry['slug']} block {i} ({lang}): matches the app but NOT any file in "
                    f"SNIPPET_SOURCES ({', '.join(declared) or 'none declared'})")
                matched += 1
                post_matched += 1
                continue

            # Near-miss detection — the check that actually matters in this track.
            #
            # ⚠️ EVERY chunk, not just the first. A block split by `// ...` whose opening chunk
            # still matches is exactly where a stale quote hides.
            evidence = None
            for part in parts:
                if contains(all_lines, part):
                    continue
                evidence = drift_evidence(all_lines, part)
                if evidence:
                    break

            if evidence:
                description, diverges_at = evidence
                drift.append(
                    f"{entry['slug']} block {i} ({lang}): {description} but the block as a whole "
                    f"is not — the quote has drifted.\n"
                    f"      diverges at : {diverges_at[:88]!r}")
            else:
                illustrative.append(f"{entry['slug']} block {i} ({lang}): "
                                    f"{(parts[0][0][:80] if parts and parts[0] else '(empty)')!r}")
                post_illus += 1

        print(f"{entry['slug']:<44} {post_blocks:>7} {post_matched:>8} "
              f"{post_illus:>6} {post_anti:>5}")

    print("-" * 74)
    if not written:
        print("no posts written yet — nothing to check.")
        return 0

    print(f"{'TOTAL':<44} {checked:>7} {matched:>8} {len(illustrative):>6} {antipattern:>5}")
    print(f"\n{skipped_lang} block(s) skipped as non-source languages (bash, markup, plaintext)")
    print(f"{antipattern} block(s) excluded as deliberate non-compiling examples")
    if checked:
        print(f"{matched}/{checked} checked blocks ({matched / checked:.0%}) are quoted from "
              "code that runs")
        print("⚠️  a low share is EXPECTED here — see the docstring. The drift count below is "
              "the number that matters.")

    if args.show_illustrative and illustrative:
        print(f"\nillustrative ({len(illustrative)}) — matched nothing in the app:")
        for item in illustrative:
            print(f"  · {item}")

    if undeclared:
        print(f"\n{len(undeclared)} block(s) quoted from an undeclared file:")
        for item in undeclared:
            print(f"  ! {item}")

    if drift:
        print(f"\n{len(drift)} DRIFTED QUOTE(S):")
        for item in drift:
            print(f"  ✗ {item}")
        return 1

    print("\nno drift.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Prove every code sample still matches the demo app it was copied from.

`check_content.py` proves a post's HTML survives the normaliser. It says NOTHING
about whether a quoted snippet is still true — a post can round-trip perfectly
while quoting a permission rule that was rewritten a month ago. This is the check
for that, and it is the one that goes stale on its own.

Every code block in every post is searched for, contiguously, in
lovemesomecoding_demo_project/stayhub. Indentation is ignored, because a fragment
lifted out of a nested compose service or a Python list is dedented when quoted,
and that is fine. A line that is exactly `...` marks a deliberate elision and
splits the block into chunks that must each match (but need not be adjacent).

⚠️ This track has a second source of truth the Docker track did not: roughly half
its content is v3 (DDN), which was written from the docs and has NO demo app
behind it. Those blocks are `yaml` HML and can never match StayHub. They are
counted separately and never reported as drift — see V3_MARKERS below.

Blocks that match nothing are reported as `illustrative` rather than failing:
plenty of this track is GraphQL typed into a console and `hasura` command lines
written for the lesson, which never existed in the app as files. The number is
printed so a sudden jump gets noticed — that is what a drifted quote looks like.

    python projects/hasura_tutorial/check_snippets.py
    python projects/hasura_tutorial/check_snippets.py --show-illustrative

Exits non-zero only when a block ALMOST matches — its opening lines are found in
the app but the whole block is not. That is the signature of real drift, as
opposed to an invented example that merely starts with a common line.
"""

import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parent.parent / "lovemesomecoding_demo_project/stayhub"

# Everything under APP is scanned EXCEPT these. All the sub-projects are in
# scope — the track quotes hasura/metadata.py, the compose file, the FastAPI
# app and both React frontends' GraphQL documents.
SKIP_DIRS = {"node_modules", "dist", "build", ".git", "__pycache__", ".venv",
             "venv", ".pytest_cache", "test-results", "playwright-report",
             "screenshots", "uploads", ".mypy_cache", "coverage"}

sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

BLOCK = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-[\w-]+">(.*?)</code></pre>', re.S)

# Languages that could plausibly have come out of the app as a FILE.
#
# `python` is in here and matters more than anything else: StayHub's Hasura
# metadata IS a Python module, so the permission rules this track quotes most
# often live in hasura/metadata.py rather than in YAML.
#
# `graphql` is in here because the frontends' queries live in gql`` template
# literals inside .ts files — indentation is stripped before matching, so a
# quoted document lines up with the literal's body.
#
# `bash` is deliberately absent: every bash block is a command typed at a prompt,
# so checking it against file contents would report the whole track as drift.
SOURCE_LANGS = {"python", "yaml", "json", "graphql", "typescript", "tsx", "sql", "properties"}

SOURCE_SUFFIXES = {".py", ".yml", ".yaml", ".json", ".ts", ".tsx", ".sql",
                   ".properties", ".conf", ".env", ".example"}
SOURCE_NAMES = {"Dockerfile", ".dockerignore", "Makefile"}

# How many opening lines must match before a near-miss counts as drift rather
# than an invented example that happens to start with a common line.
DRIFT_LEAD = 3

# A block belonging to the v3 half of the track. DDN metadata is HML — YAML with
# a `kind:` at the top — and there is no DDN project in this repo to check it
# against, by decision (see progress_report.md). Matching these against StayHub
# would report every one of them as illustrative and bury the signal.
V3_MARKERS = re.compile(
    r'^\s*kind:\s*(?:' + "|".join(manifest.V3_METADATA_KINDS) + r')\b', re.M)


COMMENTS = [
    re.compile(r"/\*.*?\*/", re.S),         # /* ... */
    re.compile(r"<!--.*?-->", re.S),        # xml/html comments
    re.compile(r"^\s*//.*$", re.M),         # // line comments
    re.compile(r"^\s*#.*$", re.M),          # python, compose, graphql, properties
]


def strip_trailing_comment(line: str) -> str:
    """Cut a trailing ` # ...` comment, but only when the `#` is not in a string.

    Whole-line comments are handled by the COMMENTS patterns; this is for the
    other half, and StayHub is full of them:

        NOTHING_HIDDEN = {}  # an empty filter means "every row"

    A post quotes that line without its comment, so a line-start-anchored regex
    leaves the two sides unequal and the whole block reads as drift. That is not
    hypothetical — it is the first thing this script got wrong.

    ⚠️ Naively cutting at the first `#` is wrong and would corrupt real code:
    a URL fragment, a CSS colour, or `{"tag": "#hasura"}` all contain one. So the
    scan tracks quote state and only cuts at a `#` that is outside any string AND
    preceded by whitespace — which is what a comment looks like in Python, YAML,
    GraphQL and properties files alike.
    """
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote and line[i - 1:i] != "\\":
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1].isspace()):
            return line[:i]
    return line


def strip_comments(text: str) -> str:
    """Remove comments before matching.

    The house style is to quote the app verbatim MINUS its teaching comments —
    repeating those in the post says everything twice. StayHub's compose file and
    hasura/metadata.py are both more than half comment, so without this every
    quote reads as drift.

    ⚠️ `#` is stripped from both sides, so a Python comment and a GraphQL comment
    both vanish. That is fine — they vanish from the app text too, so the
    comparison stays honest.
    """
    for pattern in COMMENTS:
        text = pattern.sub("", text)
    return "\n".join(strip_trailing_comment(ln) for ln in text.splitlines())


def lines(text: str) -> list[str]:
    """Non-blank lines, indentation and comments stripped."""
    return [ln.strip() for ln in strip_comments(text).splitlines() if ln.strip()]


def contains(haystack: list[str], needle: list[str]) -> bool:
    if not needle:
        return True
    return any(haystack[i:i + len(needle)] == needle
               for i in range(len(haystack) - len(needle) + 1))


def chunks_of(block: str) -> list[list[str]]:
    """Split on lines that are exactly `...`, the elision marker.

    Splitting on the bare substring would break every YAML flow sequence and
    Python's own `...`, which is a false positive that costs a real minute.
    """
    out, current = [], []
    for ln in block.splitlines():
        if ln.strip() == "...":
            if current:
                out.append(lines("\n".join(current)))
            current = []
        else:
            current.append(ln)
    if current:
        out.append(lines("\n".join(current)))
    return [c for c in out if c]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-illustrative", action="store_true",
                        help="list the blocks that matched nothing in the app")
    args = parser.parse_args()

    if not APP.is_dir():
        raise SystemExit(f"demo app not found at {APP}")

    sources = {}
    for path in APP.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in SOURCE_SUFFIXES and path.name not in SOURCE_NAMES:
            continue
        if SKIP_DIRS & set(path.relative_to(APP).parts):
            continue
        try:
            sources[path] = lines(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue

    if not sources:
        raise SystemExit(f"scanned {APP} and found no source files — check SKIP_DIRS")

    matched = illustrative = v3 = 0
    suspects = []
    per_post = []

    for entry in manifest.POSTS:
        path = HERE / "posts" / entry["file"]
        if not path.exists():
            continue
        post_matched = post_illustrative = post_v3 = 0

        for lang, raw in BLOCK.findall(path.read_text(encoding="utf-8")):
            block = html.unescape(raw)

            # v3 first: an HML block is YAML, so without this it would be
            # scanned against StayHub and always come back illustrative.
            if V3_MARKERS.search(block):
                v3 += 1
                post_v3 += 1
                continue

            if lang not in SOURCE_LANGS:
                continue
            parts = chunks_of(block)
            if not parts:
                continue
            hit = next((p for p, src in sources.items()
                        if all(contains(src, c) for c in parts)), None)
            if hit:
                matched += 1
                post_matched += 1
                continue

            illustrative += 1
            post_illustrative += 1

            # A LEAD-IN of several lines matching somewhere, while the whole
            # block does not, is drift. Matching only the first line is not:
            # `PUBLISHED_ONLY = {` opens the real rule and every fragment
            # quoting it alike.
            #
            # ⚠️ The lead must be strictly SHORTER than the chunk it came from.
            # Taking a flat DRIFT_LEAD lines means that on a 3-line block the
            # lead IS the block — it cannot match when the block does not, so
            # the shortest drifted quotes, which is most of them, slip through.
            lead = parts[0][:min(DRIFT_LEAD, len(parts[0]) - 1)]
            if len(lead) >= 2:
                for p, src in sources.items():
                    if contains(src, lead):
                        suspects.append((entry["slug"], p.relative_to(APP), lead[0]))
                        break
            if args.show_illustrative:
                print(f"  illustrative  {entry['slug']}: {parts[0][0][:78]}")

        per_post.append((entry["slug"], post_matched, post_illustrative, post_v3))

    print(f"scanned {len(sources)} source file(s) under {APP.name}/\n")
    for slug, m, i, t in per_post:
        print(f"{slug:34} {m:>2} from the app, {i:>2} illustrative, {t:>2} v3/HML")

    print(f"\n{matched} block(s) matched the demo app, {illustrative} illustrative, "
          f"{v3} v3/HML (not checkable — no DDN project, by decision)")

    if suspects:
        print("\nPOSSIBLE DRIFT — the opening lines exist in the app but the block does not:")
        for slug, rel, first in suspects:
            print(f"  x {slug}: {first[:70]}\n      cf. {rel}")
        return 1

    print("every quoted block is either verbatim from the app, v3, or clearly illustrative")
    return 0


if __name__ == "__main__":
    sys.exit(main())

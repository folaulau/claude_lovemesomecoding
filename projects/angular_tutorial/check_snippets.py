#!/usr/bin/env python3
"""Prove every code sample still matches the demo app it was copied from.

`check_content.py` proves a post's HTML survives the normaliser. It says NOTHING
about whether a quoted snippet is still true — a post can round-trip perfectly
while quoting a component that was refactored a month ago. This is the check for
that, and it is the one that goes stale on its own.

Every code block in every post is searched for, contiguously, in
pizza-angular-frontend. Indentation is ignored, because a fragment lifted out of
a deeply nested template is dedented when quoted, and that is fine. A line that
is exactly `...` marks a deliberate elision and splits the block into chunks that
must each match (but need not be adjacent to one another).

Blocks that match nothing are reported as `illustrative` rather than failing:
plenty of them are three-line examples written for the lesson and never existed
in the app. The number is printed so a sudden jump gets noticed — that is what a
drifted quote looks like.

    python projects/angular_tutorial/check_snippets.py
    python projects/angular_tutorial/check_snippets.py --show-illustrative

Exits non-zero only when a block ALMOST matches — its opening lines are found in
the app but the whole block is not. That is the signature of real drift, as
opposed to an invented example that merely starts with a common import.
"""

import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parent.parent / "lovemesomecoding_demo_project/pizza/pizza-angular-frontend"

# Everything under APP is scanned EXCEPT these. The project root has to be in
# scope, not just src/ — posts quote angular.json and package.json, and scanning
# only src/ silently reported those as "illustrative" rather than verifying them.
SKIP_DIRS = {"node_modules", "dist", ".angular", ".git", "out-tsc", "test-results",
             "playwright-report", "screenshots"}

sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

BLOCK = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-[\w-]+">(.*?)</code></pre>', re.S)

# Languages that could plausibly have come out of the app at all.
SOURCE_LANGS = {"typescript", "markup", "scss", "css", "json"}

# How many opening lines must match before a near-miss counts as drift rather
# than an invented example that happens to start with a common import.
DRIFT_LEAD = 3


COMMENTS = [
    re.compile(r"/\*.*?\*/", re.S),        # /* ... */, including the ANGULAR CONCEPT blocks
    re.compile(r"<!--.*?-->", re.S),        # template comments
    re.compile(r"^\s*//.*$", re.M),         # // line comments
]


def strip_comments(text: str) -> str:
    """Remove comments before matching.

    The house style is to quote the app verbatim MINUS its teaching comments —
    repeating those in the post says everything twice. So a post's version of
    spinner.ts is the import followed immediately by @Component, while the file
    has a 12-line comment between them. Without this, every such quote reads as
    drift.
    """
    for pattern in COMMENTS:
        text = pattern.sub("", text)
    return text


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

    Splitting on the bare substring would break `Math.min(...xs)` and every
    other spread operator, which is a false positive that cost a real minute.
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
        if not path.is_file() or path.suffix not in {".ts", ".html", ".scss", ".css", ".json"}:
            continue
        if SKIP_DIRS & set(path.relative_to(APP).parts):
            continue
        sources[path] = lines(path.read_text(encoding="utf-8"))

    matched = illustrative = 0
    suspects = []
    per_post = []

    for entry in manifest.POSTS:
        path = HERE / "posts" / entry["file"]
        if not path.exists():
            continue
        post_matched = post_illustrative = 0

        for lang, raw in BLOCK.findall(path.read_text(encoding="utf-8")):
            block = html.unescape(raw)
            if lang not in SOURCE_LANGS:
                continue
            parts = chunks_of(block)
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
            # "import { Component } from '@angular/core';" opens half the app
            # and every invented example alike.
            lead = parts[0][:DRIFT_LEAD]
            if len(lead) >= DRIFT_LEAD:
                for p, src in sources.items():
                    if contains(src, lead):
                        suspects.append((entry["slug"], p.relative_to(APP), lead[0]))
                        break
            if args.show_illustrative:
                print(f"  illustrative  {entry['slug']}: {parts[0][0][:78]}")

        per_post.append((entry["slug"], post_matched, post_illustrative))

    for slug, m, i in per_post:
        print(f"{slug:34} {m:>2} from the app, {i:>2} illustrative")

    print(f"\n{matched} block(s) matched the demo app, {illustrative} illustrative")

    if suspects:
        print("\nPOSSIBLE DRIFT — the opening lines exist in the app but the block does not:")
        for slug, rel, first in suspects:
            print(f"  x {slug}: {first[:70]}\n      cf. {rel}")
        return 1

    print("every quoted block is either verbatim from the app or clearly illustrative")
    return 0


if __name__ == "__main__":
    sys.exit(main())

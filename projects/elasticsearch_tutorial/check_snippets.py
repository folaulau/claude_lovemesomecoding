#!/usr/bin/env python3
"""Prove every code sample still matches the StayHub file it was copied from.

`check_content.py` proves a post's HTML survives the normaliser. It says NOTHING about whether a
quoted snippet is still true — a post can round-trip perfectly while quoting a dependency that was
rewritten a month ago. This is the check for that, and it is the one that goes stale on its own.

⚠️ THIS IS THE CHECK THAT JUSTIFIES THE WHOLE TRACK. The thirteen posts being replaced quote
`curl` against invented `movies` and `students` indexes copied out of tutorialspoint, which is
exactly why they cannot be trusted and exactly what this rewrite is for. Every python block here
should be traceable to a file that runs and is covered by StayHub's 193-test suite.

⚠️ `json` blocks are expected to be `illustrative`, and that is correct rather than a gap. A query
DSL body is typed at a console or built as a Python dict — `queries.py` holds
`{"range": {"price_per_night": {...}}}` as Python, not as a .json file — so a JSON block matches no
file. What IS checked is the python that builds it.

Stronger than the Hasura track's equivalent in one way: `manifest.SNIPPET_SOURCES` declares which
files each post is allowed to quote, so a block is checked against THAT file, not merely against
the app somewhere. A snippet that drifts into the post from an unrelated module is a finding, not
a pass.

Matching ignores indentation (a fragment lifted out of a class body is dedented when quoted) and
comments (the house style quotes the app verbatim MINUS its teaching comments — repeating them
says everything twice). A line that is exactly `...` marks a deliberate elision and splits the
block into chunks that must each match, though they need not be adjacent.

Blocks that match nothing are reported as `illustrative` rather than failing: shell commands,
`before` snippets showing the wrong way, and small invented fragments are legitimate. The count is
printed so a sudden jump gets noticed — that is what drift looks like.

Exits non-zero when a block ALMOST matches: its opening lines are found in the app but the whole
block is not. That is the signature of real drift, as opposed to an invented example that happens
to start with a common line.

    python projects/elasticsearch_tutorial/check_snippets.py
    python projects/elasticsearch_tutorial/check_snippets.py --show-illustrative
"""

import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# The whole StayHub tree, not just the backend: this track quotes `docker-compose.yml` too, and
# manifest.SNIPPET_SOURCES names files relative to here.
APP = HERE.parent.parent / "lovemesomecoding_demo_project/stayhub"

SKIP_DIRS = {"node_modules", "dist", "build", ".git", "__pycache__", ".venv", "venv",
             ".pytest_cache", ".ruff_cache", ".mypy_cache", "test-results", "uploads",
             "notifications", "htmlcov"}

sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

BLOCK = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-[\w-]+">(.*?)</code></pre>', re.S)

# Languages that could plausibly have come out of the app as a FILE.
#
# `bash` is deliberately absent: every bash block is a command typed at a prompt, so checking it
# against file contents would report the whole track as drift.
SOURCE_LANGS = {"python", "yaml", "json", "docker", "properties", "sql"}

SOURCE_SUFFIXES = {".py", ".yml", ".yaml", ".json", ".ini", ".cfg", ".txt", ".env", ".example"}
SOURCE_NAMES = {"Dockerfile", ".dockerignore", "Makefile", "alembic.ini", "pytest.ini"}

# How many opening lines must match before a near-miss counts as drift rather than an invented
# example that happens to start with a common line.
#
# ⚠️ This is the LONGEST MATCHING PREFIX, not a fixed-length lead, and the difference is the whole
# check. The first version took the first 3 lines and asked whether that exact run appeared in the
# app — which fails on the most common drift there is, a changed line INSIDE those three:
#
#     def require_host(user: CurrentUser) -> User:      <- still true
#         if not user.is_host:                          <- still true
#             raise ForbiddenException("Hosts only!")   <- CHANGED
#
# The fixed lead does not match, so the block was filed as "illustrative" — the one bucket that
# never fails a build. Drift detection that silently reclassifies drift as fine is worse than
# none. Measured against a deliberately drifted fixture on 2026-08-21.
DRIFT_LEAD = 2

# A section deliberately showing the WRONG way. Those blocks must not match the app — that is the
# point of them — so they are excluded rather than reported.
ANTIPATTERN = re.compile(re.escape(manifest.ANTIPATTERN_MARKER), re.I)

COMMENTS = [
    re.compile(r"/\*.*?\*/", re.S),
    re.compile(r"<!--.*?-->", re.S),
    re.compile(r"^\s*//.*$", re.M),
    re.compile(r"^\s*#.*$", re.M),
]

# Docstrings. StayHub's files are heavily docstringed and posts quote the code without them, so
# without this nearly every python block reads as drift.
DOCSTRING = re.compile(r'("""|\'\'\')(?:.|\n)*?\1')


def strip_trailing_comment(line: str) -> str:
    """Cut a trailing ` # ...` comment, but only when the `#` is not inside a string.

    ⚠️ Naively cutting at the first `#` would corrupt real code: a URL fragment, a colour, or
    `{"tag": "#python"}` all contain one. The scan tracks quote state and only cuts at a `#` that
    is outside any string AND preceded by whitespace.
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
    text = DOCSTRING.sub("", text)
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


def longest_prefix(haystack: list[str], needle: list[str]) -> int:
    """How many of `needle`'s opening lines appear in `haystack` as one contiguous run.

    Used to tell drift from invention: a quote that has drifted still opens with several real
    lines, while an invented example usually shares at most one common line like `class Foo:`.
    """
    best = 0
    for n in range(1, len(needle) + 1):
        if contains(haystack, needle[:n]):
            best = n
        else:
            break
    return best


def chunks_of(block: str) -> list[list[str]]:
    """Split on lines that are exactly `...`, the elision marker.

    Splitting on the bare substring would break Python's own `...` and every YAML flow sequence.
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


def load_sources() -> dict[str, list[str]]:
    """Every quotable file in the backend, as stripped lines, keyed by path relative to APP."""
    sources = {}
    for path in APP.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix not in SOURCE_SUFFIXES and path.name not in SOURCE_NAMES:
            continue
        try:
            sources[str(path.relative_to(APP))] = lines(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, OSError):
            continue
    return sources


def split_antipattern_blocks(raw_html: str) -> set[int]:
    """Indices of blocks that sit inside a section marked as a deliberate antipattern."""
    flagged = set()
    for i, match in enumerate(BLOCK.finditer(raw_html)):
        # Look back at the 400 characters before the block for the marker — far enough to cover a
        # heading or an intro paragraph, short enough not to leak into the next section.
        window = raw_html[max(0, match.start() - 400):match.start()]
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
    checked = matched = skipped_lang = antipattern = 0
    written = 0

    print(f"{'slug':<40} {'blocks':>7} {'matched':>8} {'illus':>6} {'anti':>5}")
    print("-" * 70)

    for entry in manifest.POSTS:
        path = HERE / "posts" / entry["file"]
        if not path.exists():
            continue
        written += 1
        raw = path.read_text(encoding="utf-8")
        flagged = split_antipattern_blocks(raw)

        declared = manifest.SNIPPET_SOURCES.get(entry["slug"], [])
        declared_lines: list[str] = []
        for rel in declared:
            if rel in sources:
                declared_lines.extend(sources[rel])
            else:
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

            # Near-miss detection: how much of the opening actually appears in the app? A quote
            # that has drifted still opens with several real lines; an invented example shares at
            # most one common line.
            head = parts[0] if parts else []
            depth = longest_prefix(all_lines, head) if head else 0
            if depth >= DRIFT_LEAD and depth < len(head):
                drift.append(
                    f"{entry['slug']} block {i} ({lang}): the first {depth} of {len(head)} lines "
                    f"ARE in the app but the block as a whole is not — the quote has drifted.\n"
                    f"      last good : {head[depth - 1][:88]!r}\n"
                    f"      drifts at : {head[depth][:88]!r}")
            else:
                illustrative.append(f"{entry['slug']} block {i} ({lang}): "
                                    f"{(parts[0][0][:80] if parts and parts[0] else '(empty)')!r}")
                post_illus += 1

        print(f"{entry['slug']:<40} {post_blocks:>7} {post_matched:>8} "
              f"{post_illus:>6} {post_anti:>5}")

    print("-" * 70)
    if not written:
        print("no posts written yet — nothing to check.")
        return 0

    print(f"{'TOTAL':<40} {checked:>7} {matched:>8} {len(illustrative):>6} {antipattern:>5}")
    print(f"\n{skipped_lang} block(s) skipped as non-source languages (bash, plaintext, markup)")
    if checked:
        print(f"{matched}/{checked} checked blocks ({matched / checked:.0%}) are quoted from "
              "code that runs")

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

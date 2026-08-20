#!/usr/bin/env python3
"""Prove that every snippet claiming to come from the bank app really does.

Folau's requirement (2026-08-20): draw examples from
`lovemesomecoding_demo_project/bank/bank-python-console`. A snippet that says it is
real code has to BE real code, or the claim rots the first time the app changes.

A block opts in by naming its source file immediately above the <pre>:

    <!-- from: bank/money.py -->
    <pre class="language-python"><code class="language-python">...

Every substantial line of that block must then appear in that file. Posts are
allowed to elide and adapt, so these are normalised away before comparing:

  * an elided body — a bare `...`, a `# ...` line, or a `pass`
  * comments, which posts routinely rewrite for their own context — and which
    this app has a LOT of, since it was written to be quoted
  * indentation, which necessarily changes when a method is lifted out of its
    class, and Python is the language where that is not a cosmetic difference
  * a trailing comma, added or dropped when a call is rewrapped
  * a `>` that was `&gt;` in the HTML

`check_snippets.py` deliberately does NOT run these blocks: a method lifted out
of its module refers to the collaborators it had there. They are covered instead
by this check plus the app's own 398-line test suite, which `check.sh` runs.

    python projects/python_advanced/check_provenance.py
    python projects/python_advanced/check_provenance.py --list   # coverage per post
"""

import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
APP = REPO / "lovemesomecoding_demo_project" / "bank" / "bank-python-console"

sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

BLOCK = re.compile(
    r'(?P<markers>(?:<!--[^>]*-->\s*)*)'
    r'<pre\b[^>]*>(?:\s*<code\b[^>]*>)?(?P<body>.*?)(?:</code>\s*)?</pre>',
    re.S | re.I)
FROM_MARKER = re.compile(r'<!--\s*from:\s*(?P<path>[^\s>]+?)\s*-->', re.I)

# Lines a post is allowed to introduce or drop without breaking the claim: an
# elided body, a comment line, or the `pass` that stands in for one.
ELISION = re.compile(r'^(\.\.\.|#\s*\.\.\..*|#.*|pass)$')


def strip_comment(line: str) -> str:
    """Drop a trailing `#` comment, but only a real one.

    A naive `line.split("#")[0]` truncates `re.sub(r'#\\w+', ...)` and
    `f"{value:#>8}"` mid-string. Truncating makes a line SHORTER, which makes it
    MORE likely to match something in the source file — so getting this wrong
    fails in the direction of a false pass, which is the direction that matters.
    Track quote state instead.
    """
    out = []
    quote = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            if ch == "\\":
                out.append(ch)
                if i + 1 < len(line):
                    out.append(line[i + 1])
                    i += 2
                    continue
            elif ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def normalise(line: str) -> str:
    """Whitespace, indentation and comments are all things a post may change."""
    line = strip_comment(line)
    line = re.sub(r'\s+', ' ', line).strip()
    # A trailing comma is routinely added or dropped when a call is rewrapped
    # from one line to several.
    return line.rstrip(",")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="show coverage per post")
    args = ap.parse_args()

    if not APP.exists():
        print(f"demo app not found: {APP}")
        return 1

    sources = {}
    failures = []
    claimed = 0
    posts_with_claims = 0

    for entry in manifest.POSTS:
        path = HERE / "posts" / entry["file"]
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8")
        in_post = 0

        for i, m in enumerate(BLOCK.finditer(raw)):
            marker = FROM_MARKER.search(m.group("markers") or "")
            if not marker:
                continue
            claimed += 1
            in_post += 1
            rel = marker.group("path")
            src = APP / rel

            if not src.exists():
                failures.append(f"{entry['slug']} block {i}: no such file in the app — {rel}")
                continue
            if rel not in sources:
                sources[rel] = [normalise(l) for l in
                                src.read_text(encoding="utf-8").splitlines()]
            haystack = sources[rel]

            code = html.unescape(m.group("body"))
            missing = []
            for line in code.splitlines():
                stripped = line.strip()
                if not stripped or ELISION.match(stripped):
                    continue
                needle = normalise(line)
                if not needle:
                    continue
                if needle not in haystack:
                    missing.append(needle)

            if missing:
                failures.append(
                    f"{entry['slug']} block {i} claims {rel} but {len(missing)} line(s) "
                    f"are not in it:\n      " + "\n      ".join(repr(x) for x in missing[:5]))

        if in_post:
            posts_with_claims += 1
            if args.list:
                print(f"  {entry['slug']:36} {in_post} block(s) from the app")

    print(f"\n{claimed} blocks claim the bank app, across {posts_with_claims} posts")
    print(f"{len(sources)} source files referenced")
    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for f in failures:
            print(f"  x {f}")
        return 1
    print("every claimed snippet really is in the app")
    return 0


if __name__ == "__main__":
    sys.exit(main())

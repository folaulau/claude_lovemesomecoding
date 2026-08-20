#!/usr/bin/env python3
"""Prove that every snippet claiming to come from the bank app really does.

Folau's requirement (2026-08-20): draw examples from
`lovemesomecoding_demo_project/bank/bank-java-console`. A snippet that says it is
real code has to BE real code, or the claim rots the first time the app changes.

A block opts in by naming its source file immediately above the <pre>:

    <!-- from: src/com/bank/model/Money.java -->
    <pre class="language-java"><code class="language-java">...

Every substantial line of that block must then appear in that file. Posts are
allowed to elide and adapt, so these are normalised away before comparing:

  * an elided body — `{ ... }` or a bare `// ...` line
  * comments, which posts routinely rewrite for their own context
  * whitespace and indentation
  * a `>` that was `&gt;` in the HTML

`check_snippets.py` still compiles every block. This one only answers "is it
really from there", which compilation cannot tell you.

    python projects/java_tutorial/check_provenance.py
    python projects/java_tutorial/check_provenance.py --list   # coverage per post
"""

import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
APP = REPO / "lovemesomecoding_demo_project" / "bank" / "bank-java-console"

sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

BLOCK = re.compile(
    r'(?P<markers>(?:<!--[^>]*-->\s*)*)'
    r'<pre\b[^>]*>(?:\s*<code\b[^>]*>)?(?P<body>.*?)(?:</code>\s*)?</pre>',
    re.S | re.I)
FROM_MARKER = re.compile(r'<!--\s*from:\s*(?P<path>[^\s>]+?)\s*-->', re.I)

# Lines a post is allowed to introduce or drop without breaking the claim.
ELISION = re.compile(r'^(\{?\s*(//\s*)?\.\.\.\s*\}?|//.*|/\*.*|\*.*|\*/)$')


def normalise(line: str) -> str:
    line = line.split("//")[0]                 # posts rewrite trailing comments
    line = re.sub(r'\s+', ' ', line).strip()
    return line


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

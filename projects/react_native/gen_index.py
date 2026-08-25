#!/usr/bin/env python3
"""Regenerate the lesson index that lives in lesson 1.

The index is GENERATED from manifest.POSTS rather than hand-maintained, because a
hand-written list of 25 links drifts the first time a lesson is inserted or
renamed — and it drifts silently, since a wrong link still renders.

Prints the HTML block. `--write` splices it into the post between the
<!-- LESSON-INDEX --> markers, replacing whatever is there.

    python projects/react_native/gen_index.py
    python projects/react_native/gen_index.py --write
"""

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

START = "<!-- LESSON-INDEX -->"
END = "<!-- /LESSON-INDEX -->"

# Where each section starts, by 1-based lesson number.
SECTIONS = {
    1: "Getting started",
    6: "Layout and UI",
    11: "Navigation",
    13: "Architecture",
    17: "Platform and native",
    21: "Quality and shipping",
}


def build() -> str:
    cat = manifest.CATEGORY["slug"]
    out = []
    open_list = False

    for i, entry in enumerate(manifest.POSTS, 1):
        if i in SECTIONS:
            if open_list:
                out.append("</ol>")
            out.append(f"<h3>{SECTIONS[i]}</h3>")
            out.append(f'<ol start="{i}">')
            open_list = True
        # The lesson index reads better without the "React Native – " prefix that
        # every title carries for the archive and the browser tab.
        short = entry["title"].replace("React Native – ", "")
        out.append(f'  <li><a href="/{cat}/{entry["slug"]}">{short}</a></li>')

    if open_list:
        out.append("</ol>")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    block = build()
    if not args.write:
        print(block)
        return 0

    path = HERE / "posts" / manifest.POSTS[0]["file"]
    if not path.exists():
        raise SystemExit(f"lesson 1 is not written yet: {path}")

    body = path.read_text(encoding="utf-8")
    if START not in body or END not in body:
        raise SystemExit(f"{path.name} has no {START} / {END} markers")

    updated = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        f"{START}\n{block}\n{END}",
        body,
        flags=re.S,
    )
    path.write_text(updated, encoding="utf-8")
    print(f"index rewritten into {path.name} ({len(manifest.POSTS)} lessons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

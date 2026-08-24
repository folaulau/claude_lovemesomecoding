#!/usr/bin/env python3
"""Generate lesson 1's lesson index from manifest.POSTS.

A hand-written index of 28 links drifts the first time a lesson is inserted or
renamed, and it drifts silently — every link still resolves, it is just the
wrong list. Generating it means `manifest.py` is the only place the track order
exists.

The generated block is written between two marker comments in
`posts/01-vue-get-started.html`, so the rest of that post is hand-written and
left alone:

    <!-- LESSON-INDEX:START --> ... <!-- LESSON-INDEX:END -->

    python projects/vue_tutorial/gen_index.py            # print it
    python projects/vue_tutorial/gen_index.py --write    # splice it into lesson 1

Run it after adding, removing, renaming or reordering a lesson. `check_content.py`
fails if lesson 1's index no longer matches the manifest, so a forgotten run is
caught rather than published.
"""

import argparse
import sys
from itertools import groupby
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

START = "<!-- LESSON-INDEX:START -->"
END = "<!-- LESSON-INDEX:END -->"

# The lesson title as it reads in a list, without the "Vue – " prefix every
# manifest title carries for the archive and the browser tab.
PREFIX = "Vue – "


def short_title(title: str) -> str:
    return title[len(PREFIX):] if title.startswith(PREFIX) else title


def render() -> str:
    out = [START]
    position = 1
    for part, group in groupby(manifest.POSTS, key=lambda p: p["part"]):
        entries = list(group)
        out.append(f"<h3>{part}</h3>")
        out.append(f'<ol start="{position}">')
        for entry in entries:
            url = f"/{manifest.CATEGORY['slug']}/{entry['slug']}"
            out.append(f'  <li><a href="{url}">{short_title(entry["title"])}</a></li>')
        out.append("</ol>")
        position += len(entries)
    out.append(END)
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true",
                        help="splice into posts/01-vue-get-started.html between the markers")
    args = parser.parse_args()

    block = render()
    if not args.write:
        print(block)
        return 0

    path = HERE / "posts" / manifest.POSTS[0]["file"]
    if not path.exists():
        raise SystemExit(f"{path} does not exist yet — write lesson 1 first")

    text = path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(
            f"{path.name} has no {START} / {END} markers. Add them where the index belongs.")

    head, _, rest = text.partition(START)
    _, _, tail = rest.partition(END)
    path.write_text(head + block + tail, encoding="utf-8")
    print(f"spliced {len(manifest.POSTS)} lessons into {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

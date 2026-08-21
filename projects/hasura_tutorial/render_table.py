#!/usr/bin/env python3
"""Render the v2 -> v3 comparison table from manifest.V2_V3_COMPARISON.

The README asks for a comparison table on the getting started page showing each
item and how it differs in v3. The rows live in `manifest.py` as data; this turns
them into the HTML that goes into a post.

Posts in this repo are plain static HTML files — nothing templates them at build
time — so the workflow is: run this, paste the output into the post body. That
sounds like a step you could skip by hand-writing the table once, and it is
exactly the step whose absence lets a 33-row table rot. `check_content.py`
asserts every row name still appears in the post, so a hand-edit that drops a row
fails the build rather than quietly shipping.

    python projects/hasura_tutorial/render_table.py            # the full table
    python projects/hasura_tutorial/render_table.py --teaser   # lesson 1's cut
    python projects/hasura_tutorial/render_table.py --markdown # for the report
"""

import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import manifest  # noqa: E402

# `backticks` and **bold** are how the rows are written, because they read fine
# in the source. Convert rather than asking every row to be authored in HTML.
CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")


def cell(text: str) -> str:
    """Escape, then re-introduce the two bits of markup the rows use.

    Order matters: escape FIRST, so a row containing a literal `<` or `&` — and
    several do, `_eq` filters and `->` arrows among them — cannot inject markup.
    Then convert the markers, whose delimiters survive escaping untouched.
    """
    out = html.escape(text)
    out = CODE.sub(r"<code>\1</code>", out)
    out = BOLD.sub(r"<strong>\1</strong>", out)
    return out


def rows_for(teaser: bool):
    """Every row, or just the ones lesson 1 shows, keeping table order."""
    wanted = set(manifest.COMPARISON_TEASER)
    for group, items in manifest.V2_V3_COMPARISON:
        selected = [i for i in items if not teaser or i[0] in wanted]
        if selected:
            yield group, selected


def render_html(teaser: bool) -> str:
    out = ['<table>', '<thead>', '<tr>',
           '<th>Item</th><th>Hasura v2</th><th>Hasura v3 (DDN)</th>'
           '<th>What actually changes</th>',
           '</tr>', '</thead>', '<tbody>']
    for group, items in rows_for(teaser):
        if not teaser:
            # A group header row, so 33 rows read as six sections rather than a
            # wall. colspan=4 keeps it inside the same table, which matters:
            # six separate tables would each scroll independently on a phone.
            out.append(f'<tr><th colspan="4">{html.escape(group)}</th></tr>')
        for item, v2, v3, note in items:
            out.append(
                f'<tr><td>{cell(item)}</td><td>{cell(v2)}</td>'
                f'<td>{cell(v3)}</td><td>{cell(note)}</td></tr>')
    out += ['</tbody>', '</table>']
    return "\n".join(out)


def render_markdown(teaser: bool) -> str:
    out = ["| Item | Hasura v2 | Hasura v3 (DDN) | What actually changes |",
           "|---|---|---|---|"]
    for group, items in rows_for(teaser):
        if not teaser:
            out.append(f"| **{group}** | | | |")
        for item, v2, v3, note in items:
            # A literal pipe would split the cell; none of the rows has one
            # today, and this makes sure that stays true silently.
            cells = [c.replace("|", "\\|") for c in (item, v2, v3, note)]
            out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--teaser", action="store_true",
                        help="only the rows lesson 1 shows")
    parser.add_argument("--markdown", action="store_true",
                        help="markdown instead of HTML, for the progress report")
    args = parser.parse_args()

    print(render_markdown(args.teaser) if args.markdown else render_html(args.teaser))

    total = sum(len(i) for _g, i in manifest.V2_V3_COMPARISON)
    shown = sum(len(i) for _g, i in rows_for(args.teaser))
    print(f"\n<!-- {shown} of {total} rows, "
          f"from manifest.V2_V3_COMPARISON (docs read {manifest.V3_DOCS_READ}) -->",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

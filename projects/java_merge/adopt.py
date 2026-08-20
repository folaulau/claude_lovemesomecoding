#!/usr/bin/env python3
"""Bring the 29 posts written in projects/java_tutorial into the merged track.

21 survive under their own slug. The other 8 lose their slug to an incoming
duplicate (plan.RETIRE_IN_FAVOUR_OF) but their CONTENT is the trimmed, compiled,
bank-app-sourced version, so it is adopted under the winning slug rather than
thrown away. That is what "consolidate" means here: the incoming URL wins, the
better body wins.

Two rewrites are applied to every adopted file:
  1. links to a retired slug are repointed at its survivor, so no post relies on
     a 301 to reach its neighbour
  2. "post 14" link text becomes the post's name — see titles.py

    python projects/java_merge/adopt.py            # report
    python projects/java_merge/adopt.py --write
"""
import argparse, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "java_tutorial" / "posts"
DEST = HERE / "posts"
sys.path.insert(0, str(HERE))
import plan, titles, manifest  # noqa: E402

# my slug -> the file that holds it, from the java_tutorial manifest order
sys.path.insert(0, str(HERE.parent / "java_tutorial"))


def source_files() -> dict:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "jt_manifest", HERE.parent / "java_tutorial" / "manifest.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return {e["slug"]: e["file"] for e in m.POSTS}


LINK = re.compile(r'<a href="/java/([a-z0-9-]+)">([^<]*)</a>')

# The 8 posts that change slug also change neighbours: they land in a sectioned
# 64-post track rather than the 29-post sequence they were written for, so their
# closing "next" paragraph names a post that no longer follows them. Replaced
# wholesale, because the sentence has to change, not just the href.
# check_flow.py is what proves this map is complete and correct.
CLOSING = {
    "java-8-lambda-expression": (
        "<p>A lambda needs an interface with one abstract method to implement. "
        "<a href=\"/java/java-8-functional-interfaces\">Functional Interfaces</a> is next — the "
        "ones the JDK already gives you, and how they compose.</p>"),
    "java-8-streams": (
        "<p>Most pipelines end in a collector. "
        "<a href=\"/java/java-8-collectors-class\">Collectors</a> is next — grouping, joining, "
        "partitioning, and building a map without tripping on duplicate keys.</p>"),
    "java-8-optional": (
        "<p>Next: <a href=\"/java/java-8-foreach\">forEach</a> — iterating a collection the "
        "functional way, and the two things it cannot do that a loop can.</p>"),
    "java-8-date-time-api": (
        "<p>Next: <a href=\"/java/java-8-stringjoiner\">StringJoiner</a> — a small class for "
        "the very common job of building a delimited string.</p>"),
    "java-8-completablefuture": (
        "<p>That closes the Java 8 shift. The next section walks each LTS release since, starting "
        "with <a href=\"/java/java-11-string-methods\">the Java 11 String methods</a>.</p>"),
    "java-17-records": (
        "<p>Records pair with the other Java 17 addition for modelling data. "
        "<a href=\"/java/java-17-sealed-classes\">Sealed Classes</a> is next — saying these are "
        "the only kinds, and getting the compiler to hold you to it.</p>"),
    "java-17-sealed-classes": (
        "<p>Sealed types are what make an exhaustive switch possible. "
        "<a href=\"/java/java-17-switch-expressions\">Switch Expressions</a> is next.</p>"),
    "java-exception-handling": (
        "<p>That completes the fundamentals. The next section covers the functional style Java 8 "
        "introduced, starting with "
        "<a href=\"/java/java-8-lambda-expression\">Lambda Expressions</a>.</p>"),
}
# Deliberately NOT a regex. An earlier version used one and its inner group
# backtracked across the whole document, replacing every paragraph from the first
# <p> onward — the files still parsed, so only the word-count check caught it.
# The last <p> is unambiguous; find it directly.
def replace_closing(body: str, paragraph: str) -> str:
    i = body.rfind("<p>")
    if i == -1:
        raise SystemExit("no closing paragraph to replace")
    return body[:i] + paragraph + "\n"
NUMBERED = re.compile(r'^(?:[Pp]ost|[Pp]osts)\s+[\d\s,and–\-to]+$')


def rewrite(html: str) -> tuple[str, int, int]:
    repointed = renamed = 0

    def fix(m):
        nonlocal repointed, renamed
        slug, text = m.group(1), m.group(2)
        if slug in plan.RETIRE_IN_FAVOUR_OF:
            slug = plan.RETIRE_IN_FAVOUR_OF[slug]
            repointed += 1
        if NUMBERED.match(text.strip()) and slug in titles.INLINE:
            text = titles.INLINE[slug]
            renamed += 1
        return f'<a href="/java/{slug}">{text}</a>'

    return LINK.sub(fix, html), repointed, renamed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    files = source_files()
    adopted = {**{s: s for s in files if s not in plan.RETIRE_IN_FAVOUR_OF},
               **plan.RETIRE_IN_FAVOUR_OF}   # my slug -> destination slug

    if args.write:
        DEST.mkdir(exist_ok=True)
    total_rp = total_rn = 0
    for mine, dest_slug in sorted(adopted.items()):
        src = SOURCE / files[mine]
        if not src.exists():
            print(f"  x missing {src}")
            return 1
        body, rp, rn = rewrite(src.read_text(encoding="utf-8"))
        if dest_slug in CLOSING:
            # Replace the final paragraph — the "next" pointer — outright.
            body = replace_closing(body.rstrip() + "\n", CLOSING[dest_slug])
        total_rp += rp
        total_rn += rn
        note = "" if mine == dest_slug else f"  (was /java/{mine})"
        print(f"  {dest_slug:52} {rp} link(s) repointed, {rn} renamed{note}")
        if args.write:
            (DEST / f"{dest_slug}.html").write_text(body, encoding="utf-8")

    print(f"\n{len(adopted)} posts adopted; {total_rp} links repointed, "
          f"{total_rn} 'post N' references renamed")
    if not args.write:
        print("nothing written. Re-run with --write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

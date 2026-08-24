#!/usr/bin/env python3
"""Prove every Java block in this track was copied from ReelCMS, not invented.

This is the rule that separates this track from the three posts it replaces. Those quote nothing
at all — between them they carry zero code blocks. Everything here has to come from
`lovemesomecoding_demo_project/reelcms`, an app that runs and whose 66 backend tests pass.

The check is deliberately fuzzy about whitespace and strict about everything else. A post quotes an
excerpt, not a whole file: leading indentation is stripped, blank lines collapse, and a `// ...`
elision is allowed. What may NOT differ is the code itself — identifiers, operators, string
literals, argument order.

    python projects/mongodb_tutorial/check_snippets.py

WHAT IS AND IS NOT CHECKED

  java        checked against manifest.SNIPPET_SOURCES
  yaml        checked, when the source is docker-compose.yml
  properties  checked, when the source is application.properties
  javascript  NOT checked — mongosh snippets are typed at a shell, not compiled into the app.
              check_content.py still proves they round-trip byte-for-byte.
  bash/json   NOT checked — shell transcripts and API payloads.

Two escape hatches, both narrow:

  data-antipattern  a block deliberately showing the WRONG way. Without it the only way to show a
                    mistake would be to commit the mistake to ReelCMS.
  data-generic      a block illustrating a FRAMEWORK feature this app does not use. Without it the
                    only way to mention one would be to add unused code to ReelCMS so the snippet
                    has somewhere to point.

Neither may be used for a claim about what ReelCMS does.
"""

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

import manifest  # noqa: E402

DEMO = REPO_ROOT / manifest.DEMO_BACKEND
DEMO_ROOT = REPO_ROOT / manifest.DEMO_APP

PRE = re.compile(r"<pre\b([^>]*)>(.*?)</pre>", re.S | re.I)
INNER_CODE = re.compile(r"^\s*<code\b[^>]*>(.*)</code>\s*$", re.S | re.I)
LANG = re.compile(r'language-([\w-]+)')

CHECKED_LANGUAGES = {"java", "yaml", "properties"}
ELISION = re.compile(r"^\s*(//|#)\s*\.\.\.\s*$")


def normalise(code: str) -> list[str]:
    """Collapse a block to the lines that carry meaning.

    Strips indentation and blank lines so an excerpt lifted out of a method body still matches the
    file it came from. Keeps everything else exactly.
    """
    out = []
    for line in code.splitlines():
        stripped = line.strip()
        if not stripped or ELISION.match(line):
            continue
        out.append(re.sub(r"\s+", " ", stripped))
    return out


def source_text(rel: str) -> str | None:
    """Resolve a snippet source. Backend paths are relative to the backend module; a couple of
    files (docker-compose.yml) live at the app root instead."""
    for base in (DEMO, DEMO_ROOT):
        path = base / rel
        if path.exists():
            return path.read_text(encoding="utf-8")
    return None


failures: list[str] = []
warnings: list[str] = []
checked = 0
skipped = 0
missing_posts: list[str] = []

# Fail loudly if the demo app is not where the manifest says it is — otherwise every block
# "matches nothing" and the run reads as a content problem.
if not DEMO.exists():
    raise SystemExit(f"demo backend not found at {DEMO}\nmanifest.DEMO_BACKEND is wrong.")

# Every declared source must exist. A typo here silently weakens the check to "matches nothing in
# an empty haystack", which fails in a way that looks like the post is wrong.
for slug, sources in manifest.SNIPPET_SOURCES.items():
    for rel in sources:
        if source_text(rel) is None:
            failures.append(f"{slug}: declared source does not exist: {rel}")

for entry in manifest.POSTS:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        missing_posts.append(entry["slug"])
        continue

    raw = path.read_text(encoding="utf-8")
    sources = manifest.SNIPPET_SOURCES.get(entry["slug"], [])
    haystacks = {rel: normalise(source_text(rel) or "") for rel in sources}

    for index, (attrs, inner) in enumerate(PRE.findall(raw)):
        lang_match = LANG.search(attrs) or LANG.search(inner[:200])
        lang = lang_match.group(1) if lang_match else "plaintext"
        if lang not in CHECKED_LANGUAGES:
            continue
        if manifest.ANTIPATTERN_MARKER in attrs or manifest.GENERIC_MARKER in attrs:
            skipped += 1
            continue

        wrapped = INNER_CODE.match(inner)
        if wrapped:
            inner = wrapped.group(1)
        lines = normalise(html.unescape(inner))
        if not lines:
            continue
        checked += 1

        if not sources:
            failures.append(
                f"{entry['slug']} block {index} ({lang}): the post declares no snippet sources "
                "in manifest.SNIPPET_SOURCES, so this block is untraceable")
            continue

        # Every line of the excerpt has to appear in ONE source file, in order.
        matched_in = None
        for rel, hay in haystacks.items():
            if not hay:
                continue
            positions = []
            cursor = 0
            ok = True
            for line in lines:
                try:
                    found = hay.index(line, cursor)
                except ValueError:
                    ok = False
                    break
                positions.append(found)
                cursor = found + 1
            if ok:
                matched_in = rel
                break

        if matched_in is None:
            # Report the first line that could not be found anywhere — that is almost always the
            # edited one.
            everything = {line for hay in haystacks.values() for line in hay}
            culprit = next((line for line in lines if line not in everything), lines[0])
            failures.append(
                f"{entry['slug']} block {index} ({lang}): not found in "
                f"{', '.join(sources)}\n      first unmatched line: {culprit[:120]!r}")

print(f"checked {checked} block(s) against ReelCMS"
      + (f", skipped {skipped} marked block(s)" if skipped else ""))

if missing_posts:
    print(f"not written yet ({len(missing_posts)}): " + ", ".join(missing_posts))

if warnings:
    print(f"\n⚠️  {len(warnings)} warning(s):")
    for w in warnings:
        print("   - " + w)

if failures:
    print(f"\n❌ {len(failures)} failure(s):")
    for f in failures:
        print("   - " + f)
    sys.exit(1)

print("✅ every checked block is traceable to a file that runs.")

#!/usr/bin/env python3
"""Check that code snippets really come from the demo app.

Snippets are edited for the page — comments reflowed, bodies elided with `...`,
JSDoc turned into line comments, JSX attributes pulled onto one line — so this
cannot diff them. Instead it takes every substantial line of code from every
block and asks whether that line exists anywhere in the demo app source. A line
that does not is either invented, mistyped, or illustrative; each one has to be
looked at by hand.

    python projects/frontend_dev/check_snippets.py
"""

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
APP = REPO / "lovemesomecoding_demo_project" / "pizza" / "pizza-react-frontend"
sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

# Every source file the snippets could have come from. Note `e2e/` is inside the
# app directory, so the Playwright specs quoted by the testing post are covered
# by the same sweep.
corpus = []
for pattern in ("*.ts", "*.tsx", "*.scss", "*.css", "*.html", "*.json"):
    for path in APP.rglob(pattern):
        # node_modules is somebody else's code; dist/ and test-results/ are build output.
        if {"node_modules", "dist", "test-results", "playwright-report"} & set(path.parts):
            continue
        corpus.append(path.read_text(encoding="utf-8", errors="replace"))
if not corpus:
    raise SystemExit(f"no demo-app sources found under {APP} — is the path right?")
haystack = "\n".join(corpus)
# Compare on collapsed whitespace so reindenting a snippet does not register as a change.
flat = re.sub(r"\s+", " ", haystack)

BLOCK = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-[\w-]+">(.*?)</code></pre>', re.S)

# Languages whose blocks are prose-like, hand-built for the page, or quoted from
# somewhere other than the app source: shell commands, HTTP traces, config the
# post invents to make a point, and plain output.
# `tsx` and `typescript` are the ones that carry app-specific claims, so those are
# the two that get verified. html/css blocks in this track are illustrative teaching
# markup rather than quotes from the app, and Prism ships no scss grammar anyway.
SKIP_LANGS = {"bash", "shell", "http", "text", "plaintext", "diff", "yaml", "json",
              "html", "markup", "css", "scss", "properties"}

# Lines written for the page rather than lifted, each checked by hand once.
# Keep this list short and justified — it is the escape hatch, not the norm.
ALLOWED = {
    # Post 4 teaches the three immutable-update idioms in the abstract, over a
    # generic `items`, before showing the app's real `upsert` helper that uses
    # them. Deliberately not tied to a domain type.
    "const next = [...items, newItem];",
    "const added   = [...items, newItem];",
    "const updated = items.map((i) => (i.id === target.id ? { ...i, quantity: 2 } : i));",
    "const removed = items.filter((i) => i.id !== target.id);",
    # Post 4's `Remote<T>` union is the shape being ARGUED FOR as an alternative
    # to three independent fields. The app models loading state per-context
    # rather than with this generic, so it exists only on the page.
    "| { status: 'error'; message: string }",
    "| { status: 'ready'; data: T };",
    # Post 7 shows this as the ANTI-pattern — fetch does not reject on 404, so
    # this renders an error body as if it were data. It must not appear in the
    # app, and finding it there would be the bug.
    "const data = await fetch(url).then((r) => r.json());",
}


def normalise(line: str, lang: str) -> str:
    """Undo the edits a snippet is allowed to make without changing what it claims."""
    # An elided body: `function foo() { ... }` stands for the real `function foo() {`.
    line = re.sub(r"\{\s*\.\.\.\s*\}\s*$", "{", line)
    # A trailing explanatory comment added for the page. Guarded so it does not
    # eat the `//` inside a string literal such as 'http://localhost:8085'.
    if "//" in line and "://" not in line:
        line = re.sub(r"\s*//.*$", "", line)
    if lang in ("scss", "css"):
        line = re.sub(r"\s*/\*.*?\*/\s*$", "", line)
    return re.sub(r"\s+", " ", line).strip()


unmatched = []
checked = 0

for entry in manifest.POSTS:
    raw = (HERE / "posts" / entry["file"]).read_text(encoding="utf-8")
    for lang, body in BLOCK.findall(raw):
        if lang in SKIP_LANGS:
            continue
        for line in html.unescape(body).splitlines():
            line = line.strip()
            # Skip comments, elisions, braces and short fragments — they carry no claim.
            if (not line or len(line) < 25
                    or line.startswith(("//", "#", "*", "/*", "--", "...", "}", "{", "<!--"))
                    or line in ("*/",)):
                continue
            if line in ALLOWED:
                continue
            checked += 1
            needle = normalise(line, lang)
            if len(needle) >= 25 and needle not in flat:
                unmatched.append((entry["slug"], lang, line))

print(f"{checked} code lines checked against {len(corpus)} demo-app files")
if unmatched:
    print(f"\n{len(unmatched)} line(s) NOT found in the demo app — inspect each:")
    for slug, lang, line in unmatched:
        print(f"  {slug} [{lang}]\n      {line}")
    sys.exit(1)
print("every code line appears in the demo app source")

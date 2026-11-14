#!/usr/bin/env python3
"""Expand src/NN-slug.src.html into posts/NN-slug.html.

A lesson's source is ordinary HTML except for code fences, which this script HTML-escapes and wraps
in the exact `<pre class="language-X"><code class="language-X">` shape the site's highlighter
expects:

    @@kotlin
    any code, written raw — no &lt; by hand
    @@

Inside a fence, a line of the form

    <<K/feature/cart/CartStore.kt | fun flushPendingWrites | ^    }$ | nc>>

is replaced by lines lifted from the demo app: from the first line containing the START text to
the first line after it matching END, inclusive, dedented. END is a regex when anchored with `^` or
`$`, otherwise a plain substring. `nc` drops whole-line
comments, so a lesson can quote the code without repeating the essay in its KDoc. Quoting from the
file is what keeps a post from drifting at the moment it is written; check_snippets.py is what
catches drift afterwards.

Path prefixes: A = the app, K = main sources, T = test sources, RES = res/, IOS = the SwiftUI app,
P = the pizza directory.

    python projects/android_tutorial/build_posts.py            # every src file
    python projects/android_tutorial/build_posts.py 05 06       # only lessons 05 and 06
"""

import html
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

PIZZA = HERE.parent.parent / manifest.DEMO_APP
PREFIXES = {
    "A": PIZZA / manifest.A,
    "K": PIZZA / manifest.K,
    "T": PIZZA / manifest.T,
    "RES": PIZZA / manifest.RES,
    "IOS": PIZZA / manifest.IOS,
    "P": PIZZA,
}

FENCE = re.compile(r"^@@([\w-]+)\n(.*?)^@@$", re.S | re.M)
QUOTE = re.compile(r"^\s*<<(.+?)>>\s*$")
COMMENT_LINE = re.compile(r"^\s*(//|/\*|\*|\*/|<!--|-->|#)")


def resolve(path: str) -> Path:
    head, _, rest = path.partition("/")
    return PREFIXES[head] / rest if head in PREFIXES else PIZZA / path


def extract(spec: str) -> str:
    parts = [p.strip() for p in spec.split("|")]
    path, start, end = parts[0], parts[1], parts[2]
    flags = set(parts[3:])
    lines = resolve(path).read_text(encoding="utf-8").splitlines()

    # START follows the same rule as END: anchored means regex, otherwise a substring.
    start_re = re.compile(start if start.startswith("^") or start.endswith("$") else re.escape(start))
    try:
        # A start never lands inside a comment unless it is itself one: `@Parcelize` must find the
        # annotation, not the KDoc sentence above it that mentions `@Parcelize`.
        start_is_comment = bool(COMMENT_LINE.match(start))
        first = next(i for i, ln in enumerate(lines)
                     if start_re.search(ln) and (start_is_comment or not COMMENT_LINE.match(ln)))
    except StopIteration:
        raise SystemExit(f"quote start not found: {start!r} in {path}")
    # An END anchored with ^ or $ is a regex (`^    }$` — the closing brace at that indent);
    # anything else is a plain substring, so `PizzaButton(text = "Order now"` needs no escaping.
    end_re = re.compile(end if end.startswith("^") or end.endswith("$") else re.escape(end))
    try:
        last = next(i for i in range(first, len(lines)) if end_re.search(lines[i]))
    except StopIteration:
        raise SystemExit(f"quote end not found: {end!r} after {start!r} in {path}")

    chunk = lines[first:last + 1]
    if "nc" in flags:
        out, in_block = [], False
        for ln in chunk:
            stripped = ln.strip()
            if in_block:
                if "*/" in stripped:
                    in_block = False
                continue
            if stripped.startswith("/*") and "*/" not in stripped:
                in_block = True
                continue
            if COMMENT_LINE.match(ln):
                continue
            out.append(ln)
        chunk = out
    return textwrap.dedent("\n".join(chunk))


def expand_fence(match: re.Match) -> str:
    lang, body = match.group(1), match.group(2)
    out = []
    for ln in body.splitlines():
        q = QUOTE.match(ln)
        out.append(extract(q.group(1)) if q else ln)
    code = "\n".join(out).rstrip("\n") + "\n"
    return (f'<pre class="language-{lang}"><code class="language-{lang}">'
            f"{html.escape(code, quote=False)}</code></pre>")


def build(src: Path) -> Path:
    text = src.read_text(encoding="utf-8")
    rendered = FENCE.sub(expand_fence, text)
    if "@@" in rendered or "<<" in re.sub(r"<pre.*?</pre>", "", rendered, flags=re.S):
        raise SystemExit(f"{src.name}: an unclosed fence or stray quote directive")
    out = HERE / "posts" / src.name.replace(".src.html", ".html")
    out.write_text(rendered, encoding="utf-8")
    return out


def main() -> int:
    wanted = set(sys.argv[1:])
    for src in sorted((HERE / "src").glob("*.src.html")):
        if wanted and src.name[:2] not in wanted:
            continue
        print("built", build(src).relative_to(HERE))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Helpers for writing post bodies. Import this, never hand-escape a code block.

The README's hardest-won rule is that you do not hand-escape code inside a
<pre>. Vue makes it worse than it was for React: a single-file component snippet
contains a literal <template>, a literal <script setup> and often a literal
<style scoped>, and ONE missed &lt; is invisible until it renders — the browser
opens a real element and everything after it disappears into it.

So code blocks are written as raw source and escaped here, once, correctly.

    from authoring import code, post

    post("03-vue-sfc.html", f'''
    <p>Prose.</p>
    {code("vue", open("....vue").read())}
    ''')
"""

import html
from pathlib import Path

POSTS = Path(__file__).resolve().parent / "posts"

# Kept in step with EXPECTED_LANGUAGES in check_content.py. Asking for a
# language the backend does not support degrades to plaintext SILENTLY, so a
# typo here is caught at authoring time instead of in review.
LANGUAGES = {"vue", "javascript", "markup", "css", "scss", "json", "bash", "yaml", "plaintext"}


def code(lang: str, source: str) -> str:
    """One code block, in exactly the shape the frontend highlighter matches.

    `<pre class="language-X"><code class="language-X">` — the build-time Prism
    pass matches that literally, so the two classes must agree and there must be
    no whitespace between the tags.
    """
    if lang not in LANGUAGES:
        raise ValueError(f"unsupported language {lang!r}; expected one of {sorted(LANGUAGES)}")
    escaped = html.escape(source.strip("\n"), quote=False)
    return f'<pre class="language-{lang}"><code class="language-{lang}">{escaped}</code></pre>'


def from_app(lang: str, relative_path: str, *, start: str = None, end: str = None,
             count: int = None, pad: int = 0, to_end: bool = False) -> str:
    """A code block quoted verbatim from the demo app.

    Reading the file rather than retyping it is what makes check_snippets.py
    meaningful — a snippet copied by hand drifts the moment the app changes, and
    this cannot.

    Slicing, all by SINGLE-LINE substring match (a multi-line `start` matches
    nothing and raises):

        start=          first line containing this
        end=            through the next line containing this, inclusive.
                        A plain SUBSTRING, not a regex.
        count=          exactly this many lines from `start`
        pad=            extra lines after `end`, for a trailing `);` or `}`
        to_end=         from `start` to the end of the file, said deliberately

    Giving neither `end` nor `count` quotes to the end of the file, which is
    correct for a whole file and almost never what you meant for a fragment — so
    it raises unless `start` was also omitted.
    """
    root = Path(__file__).resolve().parent.parent.parent
    path = root / "lovemesomecoding_demo_project/reelcms/reelcms-vue-frontend" / relative_path
    lines = path.read_text(encoding="utf-8").splitlines()

    if start is None:
        if end is not None or count is not None:
            raise ValueError("end/count need a start")
        return code(lang, "\n".join(lines))

    if "\n" in start:
        raise ValueError(f"start must be a single line, got {start!r}")

    try:
        first = next(i for i, ln in enumerate(lines) if start in ln)
    except StopIteration:
        raise ValueError(f"{relative_path}: no line contains {start!r}") from None

    if to_end:
        last = len(lines)
    elif count is not None:
        last = first + count
    elif end is not None:
        try:
            last = next(i for i, ln in enumerate(lines) if i > first and end in ln) + 1 + pad
        except StopIteration:
            raise ValueError(f"{relative_path}: no line after {start!r} contains {end!r}") from None
    else:
        raise ValueError(
            f"{relative_path}: quoting from {start!r} to the end of the file. Pass `end`, "
            "`count`, or `to_end=True` if that is really what you meant — an unbounded "
            "fragment is almost always a mistake.")

    return code(lang, "\n".join(lines[first:last]))


def post(filename: str, body: str) -> Path:
    """Write a post body, normalising the blank-line noise f-strings leave behind."""
    lines = [ln.rstrip() for ln in body.strip().splitlines()]
    out = []
    for ln in lines:
        if ln == "" and out and out[-1] == "":
            continue  # collapse runs of blank lines
        out.append(ln)
    path = POSTS / filename
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return path

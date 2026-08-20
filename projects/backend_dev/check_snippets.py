#!/usr/bin/env python3
"""Check that code snippets really come from the demo app.

Snippets are edited for the page — comments reflowed, bodies elided with `...`,
javadoc turned into line comments — so this cannot diff them. Instead it takes
every substantial line of code from every block and asks whether that line
exists anywhere in the demo app source. A line that does not is either invented,
mistyped, or illustrative; each one has to be looked at by hand.

    python projects/backend_dev/check_snippets.py
"""

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
APP = REPO / "lovemesomecoding_demo_project" / "pizza" / "pizza-springboot-backend"
sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

# Every source file the snippets could have come from.
corpus = []
for pattern in ("*.java", "*.properties", "*.sql", "*.xml", "*.yml"):
    for path in APP.rglob(pattern):
        if "target" in path.parts:
            continue
        corpus.append(path.read_text(encoding="utf-8", errors="replace"))
haystack = "\n".join(corpus)
# Compare on collapsed whitespace so reindenting a snippet does not register as a change.
flat = re.sub(r"\s+", " ", haystack)

BLOCK = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-[\w-]+">(.*?)</code></pre>', re.S)

# Languages whose blocks are prose-like or hand-built for the page.
SKIP_LANGS = {"json"}

# Lines written for the page rather than lifted, each checked by hand once.
# Keep this list short and justified — it is the escape hatch, not the norm.
ALLOWED = {
    # ServiceTimingAspect's javadoc carries this illustration with "timed"; post 4 makes the
    # same point about every proxied annotation, so it says "advised".
    "public void a() { b(); }   // b() is NOT advised - internal call, no proxy involved",
    "public void b() { ... }    // advised only when some OTHER bean calls it",
    # RestExceptionHandler does not import HttpStatus, so the real source spells these
    # org.springframework.http.HttpStatus.*. Shortened for the page; the import is implied.
    'ApiError error = new ApiError(HttpStatus.BAD_REQUEST, "Validation failed", request.getRequestURI());',
    "ApiError error = new ApiError(HttpStatus.INTERNAL_SERVER_ERROR,",
    'ApiError error = new ApiError(HttpStatus.UNAUTHORIZED, "Invalid email or password", request.getRequestURI());',
    # OrderPlacedEvent really has a static factory in its body; elided to `{}` here because
    # the point being made is the component list.
    "UUID orderPublicId, String contactEmail, BigDecimal total, OrderType orderType) {}",
    # Reflowed by the formatter across two lines in OrderApiIntegrationTest.
    '.content(plainLargePepperoni("""',
}


def normalise(line: str, lang: str) -> str:
    """Undo the edits a snippet is allowed to make without changing what it claims."""
    # An elided body: `... foo(bar) { ... }` stands for the real `... foo(bar) {`.
    line = re.sub(r"\{\s*\.\.\.\s*\}\s*$", "{", line)
    # A trailing explanatory comment added for the page.
    line = re.sub(r"\s*//.*$", "", line)
    if lang == "sql":
        line = re.sub(r"\s*--.*$", "", line)
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
            if (not line or len(line) < 25 or line.startswith(("//", "#", "*", "/*", "--", "...", "}", "{"))
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

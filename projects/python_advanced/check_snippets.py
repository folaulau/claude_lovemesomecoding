#!/usr/bin/env python3
"""Run every Python code block in the track. Nothing ships unexecuted.

/java verifies its standalone snippets by compiling them. Python can do better:
compiling proves a sample is well-formed, running proves it is *right*. A post
that says a line prints `[1, 2, 3]` when it prints `[3, 2, 1]` is wrong in the
way that actually costs a reader an hour, and only execution catches it.

So every block gets, in order:

  1. **Parsed** under both interpreters (3.12 baseline, 3.14 current).
  2. **Executed** under both, in a temp directory, with a timeout.
  3. Its **`# Output:` claims verified** against what it really printed.

The existing posts already annotate 37 blocks with `# Output:`, so the convention
is established — this makes it load-bearing rather than decorative.

Markers, written as HTML comments immediately above the <pre>. They are comments
because the content normaliser rewrites <pre> attributes to class="language-X"
and would drop anything else:

    <!-- py:3.14 -->        3.14 only. For t-strings and anything else that is a
                            SyntaxError on 3.12. Never sent to 3.12.
    <!-- norun -->          Parse only. For blocks needing a network, a real
                            file, input(), or a long-running loop.
    <!-- expect-error -->   Must fail. Verifies the post's claim that something
                            breaks — and fails if it quietly starts working.
    <!-- needs: numpy -->   Needs a third-party package. Runs in this project's
                            .venv under 3.12 ONLY — those packages are not
                            installed for 3.14 and several do not support it.
                            Half this track is about libraries, so `norun` here
                            would leave four of eight posts unverified.
    <!-- from: bank/x.py -->  Lifted from the demo app. Not run here; a method
                            lifted out of its module refers to collaborators it
                            had there. check_provenance.py covers those.

THE AUTHORING RULE, which is the point: an unmarked block must run on its own.
That is a constraint on how posts are written, and a deliberate one — a reader
can paste any block and have it work. Where that is genuinely impossible, mark it
`norun` rather than leaving it broken.

Output claims: a comment of the form `# Output: <value>` claims that `<value>` is
one of the lines the block prints. Claims must appear in the same ORDER as the
output, but need not be exhaustive — annotate the interesting prints and leave
the rest. A bare `# Output:` with nothing after it is documentation and ignored.

A block written as a REPL session (first line starts with `>>>`) is run through
doctest instead, which compares every result exactly.

    python3 projects/python_advanced/check_snippets.py
    python3 projects/python_advanced/check_snippets.py --show python-tuples:3
    python3 projects/python_advanced/check_snippets.py --baseline-only
"""

import argparse
import concurrent.futures
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

BASELINE = manifest.VERSIONS["python"]   # "3.12"
LATEST = manifest.VERSIONS["latest"]     # "3.14"


def find_python(version: str) -> str | None:
    """Locate a specific interpreter, without depending on PATH order."""
    found = shutil.which(f"python{version}")
    if found:
        return found
    for candidate in (f"/usr/local/bin/python{version}",
                      f"/opt/homebrew/bin/python{version}",
                      f"/usr/bin/python{version}"):
        if Path(candidate).exists():
            return candidate
    return None


# A <pre>, optionally preceded by the HTML comments that mark it.
BLOCK = re.compile(
    r'(?P<markers>(?:<!--[^>]*-->\s*)*)'
    r'<pre\b[^>]*>(?:\s*<code\b[^>]*>)?(?P<body>.*?)(?:</code>\s*)?</pre>',
    re.S | re.I)
PY_MARKER = re.compile(r'<!--\s*py:([\d.]+)\s*-->', re.I)
NORUN = re.compile(r'<!--\s*norun\s*-->', re.I)
EXPECT_ERROR = re.compile(r'<!--\s*expect-error\s*-->', re.I)
FROM_MARKER = re.compile(r'<!--\s*from:\s*[^\s>]+\s*-->', re.I)
NEEDS = re.compile(r'<!--\s*needs:\s*([\w, ]+?)\s*-->', re.I)

# Top-level module of every import in a block, so an unmarked third-party import
# can be refused. Without this the `needs:` marker is only INCIDENTALLY enforced:
# numpy happens to be absent from 3.14 today, so forgetting the marker fails
# there — but it passed on bare 3.12, where numpy sits in the interpreter's own
# site-packages. Install numpy for 3.14 and a missing marker would start passing
# silently. Checking the imports makes the marker required rather than lucky.
IMPORTED = re.compile(r'^\s*(?:import|from)\s+([A-Za-z_]\w*)', re.M)

# The interpreter inside this project's .venv, with the pinned third-party
# packages installed. Built by:  python3.12 -m venv .venv &&
# .venv/bin/pip install -r requirements-check.txt
VENV_PYTHON = HERE / ".venv" / "bin" / "python"

# Only Python blocks run. The track also carries shell, text and console samples.
NON_PYTHON = re.compile(
    r'language-(bash|shell|sh|console|text|plaintext|json|yaml|yml|toml|ini|xml|sql|diff)',
    re.I)
PRE_TAG = re.compile(r'<pre\b[^>]*>', re.I)

# `# Output: value` — the claim. A bare `# Output:` is documentation, not a
# claim, so the value group requires at least one non-space character.
OUTPUT_CLAIM = re.compile(r'#\s*(?:Output|Outputs|Prints)\s*:\s*(\S.*?)\s*$',
                          re.I | re.M)


def claims(code: str) -> list[str]:
    return OUTPUT_CLAIM.findall(code)


def is_repl(code: str) -> bool:
    for line in code.splitlines():
        if line.strip():
            return line.lstrip().startswith(">>>")
    return False


def extract(entry, lifted: list) -> list[dict]:
    """Every runnable Python block in one post."""
    raw = (HERE / "posts" / entry["file"]).read_text(encoding="utf-8")
    out = []
    for i, m in enumerate(BLOCK.finditer(raw)):
        tag = PRE_TAG.search(m.group(0))
        if tag and NON_PYTHON.search(tag.group(0)):
            continue
        code = html.unescape(m.group("body")).strip()
        if not code:
            continue
        markers = m.group("markers") or ""
        if FROM_MARKER.search(markers):
            lifted.append(entry["slug"])
            continue
        pinned = PY_MARKER.search(markers)
        needs = NEEDS.search(markers)
        out.append({
            "needs": [n.strip() for n in needs.group(1).split(",")] if needs else [],
            "slug": entry["slug"],
            "index": i,
            "code": code,
            "pin": pinned.group(1) if pinned else None,
            "norun": bool(NORUN.search(markers)),
            "expect_error": bool(EXPECT_ERROR.search(markers)),
            "repl": is_repl(code),
            "claims": claims(code),
            "line": raw[:m.start()].count("\n") + 1,
        })
    return out


# doctest is the right tool for a REPL block: it already knows how to match a
# session's expected output exactly, including tracebacks and blank-line markers.
DOCTEST_DRIVER = """\
import doctest, sys
source = open({src!r}, encoding="utf-8").read()
runner = doctest.DocTestRunner(optionflags=doctest.ELLIPSIS | doctest.IGNORE_EXCEPTION_DETAIL)
parser = doctest.DocTestParser()
test = parser.get_doctest(source, {{}}, "snippet", "snippet", 0)
if not test.examples:
    print("NO-EXAMPLES", file=sys.stderr); sys.exit(2)
runner.run(test, out=lambda s: sys.stderr.write(s))
sys.exit(1 if runner.failures else 0)
"""


def run_one(block: dict, python: str, workdir: Path) -> str | None:
    """None on success, the complaint otherwise."""
    d = workdir / f"{block['slug']}_{block['index']}_{Path(python).name}"
    d.mkdir(parents=True, exist_ok=True)
    src = d / "snippet.py"
    src.write_text(block["code"] + "\n", encoding="utf-8")

    # Step 1 — parse. Always, even for `norun`; a syntax error is never allowed.
    #
    # A REPL block is skipped here and only here: `>>> sorted(xs)` is not valid
    # Python source, so ast.parse rejects the whole block. doctest compiles each
    # example itself and reports a syntax error in one just as loudly, so nothing
    # is lost — but forgetting this exemption failed every REPL block in the
    # track, which is how it was found.
    parsed = subprocess.run(
        [python, "-c", f"import ast,sys; ast.parse(open({str(src)!r},encoding='utf-8').read())"],
        capture_output=True, text=True, timeout=60) if not block["repl"] else None
    if parsed is not None and parsed.returncode != 0:
        if block["expect_error"]:
            return None  # the post claims it does not even parse. Fair.
        tail = [l for l in parsed.stderr.splitlines() if l.strip()][-3:]
        return "does not parse:\n      " + "\n      ".join(tail)

    if block["norun"]:
        if block["repl"]:
            return "a REPL block cannot be `norun` — nothing would check it at all"
        return None

    # Step 2 — execute. `-s -E` isolates the run from this machine's user
    # site-packages and from PYTHONPATH, so a sample cannot pass because of
    # something only installed here. cwd is the temp dir, so a block that writes
    # a file cannot escape it.
    #
    # NOT `-I`, which would be the obvious choice: -I additionally refuses to put
    # the script's own directory on sys.path, so `import money` fails for a
    # snippet that just wrote money.py beside itself. That broke every import
    # example in python-modules-packages while being nothing to do with the post.
    # -s -E keeps the isolation that matters and leaves normal import behaviour
    # intact.
    if block["repl"]:
        driver = d / "driver.py"
        driver.write_text(DOCTEST_DRIVER.format(src=str(src)), encoding="utf-8")
        cmd = [python, "-s", "-E", str(driver)]
    else:
        cmd = [python, "-s", "-E", str(src)]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=d)
    except subprocess.TimeoutExpired:
        return "ran for over 30s — infinite loop, or it wants input(). Mark it norun."

    if block["expect_error"]:
        # The post claims this breaks. Verify the claim: a sample that quietly
        # started working is a sample whose lesson has evaporated.
        if proc.returncode == 0:
            return ("marked expect-error but it RAN CLEAN — either the post's claim "
                    "is now wrong or the marker is stale")
        return None

    if proc.returncode != 0:
        if block["repl"]:
            # doctest writes the Expected/Got comparison to stderr. Show more of
            # it than a traceback needs, and do not call it "raised" — the
            # session ran fine, it just printed something else.
            tail = [l for l in proc.stderr.splitlines() if l.strip()][-8:]
            return "REPL session does not match:\n      " + "\n      ".join(tail)
        tail = [l for l in proc.stderr.splitlines() if l.strip()][-4:]
        return "raised:\n      " + "\n      ".join(tail)

    # Step 3 — verify the output claims. The reason this checker exists.
    if block["repl"]:
        return None  # doctest already compared every result exactly.
    expected = block["claims"]
    if not expected:
        return None
    # stdout first, then stderr. Several things a post legitimately demonstrates
    # write to stderr rather than stdout — `logging` does by default, and so do
    # warnings — and a claim about one of those is not a wrong claim. Order is
    # still enforced within each stream; a block that interleaves the two must
    # claim its stdout lines before its stderr lines.
    actual = ([l.rstrip() for l in proc.stdout.splitlines()]
              + [l.rstrip() for l in proc.stderr.splitlines()])
    remaining = list(actual)
    for want in expected:
        for i, got in enumerate(remaining):
            if got.strip() == want.strip():
                remaining = remaining[i + 1:]
                break
        else:
            return (f"claims `# Output: {want}` but that line is not in what it printed"
                    f" (in order).\n      printed: {actual[:8]}")
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", metavar="SLUG:INDEX",
                    help="print one block with its markers and exit")
    ap.add_argument("--baseline-only", action="store_true",
                    help=f"skip the {LATEST} pass (use when only one interpreter is installed)")
    args = ap.parse_args()

    py_base = find_python(BASELINE)
    py_latest = None if args.baseline_only else find_python(LATEST)
    venv = VENV_PYTHON if VENV_PYTHON.exists() else None
    if not py_base:
        print(f"no python{BASELINE} found — install it or use --baseline-only with it on PATH")
        return 1

    blocks, lifted = [], []
    for entry in manifest.POSTS:
        if not (HERE / "posts" / entry["file"]).exists():
            print(f"  .. {entry['slug']:36} not written yet, skipped")
            continue
        blocks.extend(extract(entry, lifted))

    if not blocks:
        print("no post bodies written yet — nothing to run")
        return 0

    marker_failures = []
    for b in blocks:
        used = set(IMPORTED.findall(b["code"])) & manifest.THIRD_PARTY
        if used and not b["needs"] and not b["norun"]:
            marker_failures.append(
                f"{b['slug']} block {b['index']} (line {b['line']}): imports "
                f"{sorted(used)} but has no `<!-- needs: ... -->` marker, so it would be "
                f"run on the bare interpreters where those packages do not belong")
        stale = set(b["needs"]) - used
        if stale:
            marker_failures.append(
                f"{b['slug']} block {b['index']} (line {b['line']}): marked "
                f"`needs: {', '.join(sorted(stale))}` but never imports it — stale marker")

    if args.show:
        slug, _, idx = args.show.partition(":")
        for b in blocks:
            if b["slug"] == slug and str(b["index"]) == idx:
                marks = [k for k in ("norun", "expect_error", "repl") if b[k]]
                if b["pin"]:
                    marks.append(f"py:{b['pin']}")
                print(f"# {slug} block {idx}  ({', '.join(marks) or 'plain'}; "
                      f"{len(b['claims'])} output claims)\n")
                print(b["code"])
                return 0
        print(f"no such block: {args.show}")
        return 1

    print(f"python {BASELINE}: {py_base}")
    print(f"python {LATEST}: {py_latest or '(skipped)'}")
    print(f"venv {BASELINE}: {venv or '(missing — run: python3.12 -m venv .venv && '
                                     '.venv/bin/pip install -r requirements-check.txt)'}")
    print(f"{len(blocks)} python blocks in {len(set(b['slug'] for b in blocks))} posts\n")

    jobs = []
    for b in blocks:
        if b["needs"]:
            # Third-party blocks run in the venv, under 3.12 only. Never sent to
            # the bare interpreters, where the import would fail for reasons that
            # have nothing to do with whether the sample is correct.
            if venv:
                jobs.append((b, str(venv), f"{BASELINE}+venv"))
            continue
        if b["pin"] == LATEST:
            # Never send a 3.14-pinned block to 3.12 — that it fails there is the
            # entire reason the callout exists.
            if py_latest:
                jobs.append((b, py_latest, LATEST))
        else:
            jobs.append((b, py_base, BASELINE))
            if py_latest:
                jobs.append((b, py_latest, LATEST))

    failures = list(marker_failures)
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            futures = {pool.submit(run_one, b, py, workdir): (b, label)
                       for b, py, label in jobs}
            for f in concurrent.futures.as_completed(futures):
                b, label = futures[f]
                try:
                    err = f.result()
                except Exception as e:  # a checker bug must not read as a pass
                    err = f"checker error: {e!r}"
                if err:
                    failures.append(f"{b['slug']} block {b['index']} "
                                    f"(line {b['line']}, python {label}):\n      {err}")

    by_post = {}
    for b in blocks:
        by_post.setdefault(b["slug"], []).append(b)
    verified = 0
    for entry in manifest.POSTS:
        bs = by_post.get(entry["slug"])
        if not bs:
            continue
        needy = sum(1 for b in bs if b["needs"])
        pinned = sum(1 for b in bs if b["pin"])
        skipped = sum(1 for b in bs if b["norun"])
        expected = sum(1 for b in bs if b["expect_error"])
        checked = sum(len(b["claims"]) for b in bs)
        verified += checked
        bad = sum(1 for f in failures if f.startswith(entry["slug"] + " "))
        bits = ([f"{needy} need the venv"] if needy else []) + \
               ([f"{pinned} pinned to {LATEST}"] if pinned else []) + \
               ([f"{skipped} norun"] if skipped else []) + \
               ([f"{expected} must fail"] if expected else []) + \
               ([f"{checked} output claims"] if checked else [])
        note = f"  ({', '.join(bits)})" if bits else ""
        print(f"  {'x' if bad else 'ok':>2}  {entry['slug']:36} {len(bs):>2} blocks{note}")

    unrunnable = [b for b in blocks if b["needs"]] if not venv else []
    if unrunnable:
        failures.append(
            f"{len(unrunnable)} block(s) need third-party packages but .venv is missing — "
            "they were NOT verified. Build it: python3.12 -m venv .venv && "
            ".venv/bin/pip install -r requirements-check.txt")

    print(f"\n{len(jobs)} runs across {len(blocks)} blocks, {verified} output claims verified")
    if lifted:
        print(f"{len(lifted)} block(s) quoted from the demo app were not run here — "
              f"check_provenance.py and the app's own suite cover those")
    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for f in sorted(failures):
            print(f"  x {f}")
        print("\n  re-run with --show SLUG:INDEX to see the block")
        return 1
    print("every code sample runs and prints what the post says it prints")
    return 0


if __name__ == "__main__":
    sys.exit(main())

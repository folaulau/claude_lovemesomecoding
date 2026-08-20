#!/usr/bin/env python3
"""Compile every Java code block in the track with javac. Nothing ships uncompiled.

The sibling tracks verify snippets by requiring every line to exist in the demo
app. That rule is wrong here — `int count = 0;` has no business being traced back
to a pizza ordering API — so this track writes standalone samples instead and
pays for the exception with a real compiler. See progress_report.md.

Two JDKs, because the track is Java 21 with callouts for 25:

  * a block marked `<!-- jdk:25 -->` immediately before its <pre> compiles under
    25 ONLY. The Java 25 compact-source form is a preview feature under 21 and
    would fail there, which is the whole point of the callout.
  * every other block must compile under BOTH 21 and 25. Compiling under 25 as
    well is what catches a sample that quietly relies on something removed or
    changed after 21.

Most samples are fragments, not compilation units — a few statements, or one
method. A fragment is wrapped before compiling:

  bare statements   -> wrapped in a method, in a class
  member decls      -> wrapped in a class
  a full class/etc. -> compiled as-is

The wrapper is chosen by inspection, and `--show` prints the wrapped unit for any
block so a failure is debuggable rather than mysterious.

    python projects/java_tutorial/check_snippets.py
    python projects/java_tutorial/check_snippets.py --show java-stream:3
    python projects/java_tutorial/check_snippets.py --jdk21-only   # skip the 25 pass
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

# Resolved once. JAVA_21 is whatever `javac` on PATH is, which is what the rest of
# the toolchain uses; JAVA_25 is located through java_home so the check does not
# depend on PATH order.
def find_jdk(version: str) -> str | None:
    try:
        out = subprocess.run(["/usr/libexec/java_home", "-v", version],
                             capture_output=True, text=True, timeout=20)
        if out.returncode == 0:
            javac = Path(out.stdout.strip()) / "bin" / "javac"
            if javac.exists():
                return str(javac)
    except (OSError, subprocess.SubprocessError):
        pass
    return None


# A <pre>, optionally preceded by HTML comments that pin its JDK or mark it as a
# deliberate compile error. Order between the two markers does not matter.
BLOCK = re.compile(
    r'(?P<markers>(?:<!--\s*(?:jdk:\d+|expect-error)\s*-->\s*)*)'
    r'<pre\b[^>]*>(?:\s*<code\b[^>]*>)?(?P<body>.*?)(?:</code>\s*)?</pre>',
    re.S | re.I)
JDK_MARKER = re.compile(r'<!--\s*jdk:(\d+)\s*-->', re.I)
EXPECT_ERROR = re.compile(r'<!--\s*expect-error\s*-->', re.I)

# Only Java blocks are compiled. A block is Java unless its class says otherwise
# — the track also carries shell, xml and plaintext samples.
NON_JAVA = re.compile(r'language-(bash|shell|sh|xml|properties|yaml|yml|json|text|plaintext|console|sql)',
                      re.I)
PRE_TAG = re.compile(r'<pre\b[^>]*>', re.I)

# --- deciding how to wrap a fragment -----------------------------------------

# A complete compilation unit: has a top-level type declaration at column 0.
TOP_LEVEL_TYPE = re.compile(
    r'^\s*(?:(?:public|final|abstract|sealed|non-sealed|static)\s+)*'
    r'(?:class|interface|enum|record|@interface)\s+\w', re.M)

# A Java 25 compact source file: a method declared at column 0 with no enclosing
# type. It IS a complete compilation unit, but it has no top-level type
# declaration, so TOP_LEVEL_TYPE misses it and the statement wrapper would then
# nest `void main()` inside a method body. Caught by check_snippets.py on the
# first Java 25 callout ever written, which is exactly what it is for.
# No access modifier is allowed here on purpose: `private int helper()` is a class
# member, not a compact source file, and hoisting it to top level would be a false
# failure. MEMBER_DECL is therefore tested FIRST — see wrap().
COMPACT_SOURCE = re.compile(
    r'^(?:void|[A-Za-z_]\w*(?:<[^>]*>)?(?:\[\])?)\s+\w+\s*\([^)]*\)\s*(?:throws [\w, .]+\s*)?\{',
    re.M)

# Looks like class members rather than statements: a method or field declaration
# with a modifier, or a constructor.
# `default` is deliberately NOT in the main modifier list. In an arrow switch,
# `    default -> ...` would match it and the whole block would be wrapped as a
# class body, where bare statements are illegal. It is allowed only in the shape
# it takes on an interface method — `default` followed by a return type.
MEMBER_DECL = re.compile(
    r'^\s{0,4}(?:'
    r'(?:public|private|protected|static|final|abstract|synchronized|native|transient|volatile)\s+'
    r'|default\s+[\w<]'
    r')+',
    re.M)

# `final` is legal on BOTH a field and a local variable, so MEMBER_DECL alone
# cannot tell `final int MAX = 3;` (a field) from `final int max = 3;` followed by
# `list.add(x);` (locals plus statements). These two settle it: if the block
# declares no method but does contain a bare call statement, it is statements.
METHOD_DECL = re.compile(
    r'^\s{0,4}(?:(?:public|private|protected|static|final|abstract|synchronized|default)\s+)*'
    r'(?:void|[A-Za-z_]\w*(?:<[^>]*>)?(?:\[\])?)\s+\w+\s*\([^)]*\)\s*(?:throws [\w, .]+\s*)?\{',
    re.M)
BARE_CALL = re.compile(r'^\s{0,4}[A-Za-z_][\w.]*\s*\([^;]*\)\s*;', re.M)

# Fragments routinely reference types the sample never imports. Rather than make
# every post carry an import block that is noise for the reader, the wrapper
# imports the packages a Java sample realistically touches.
PREAMBLE = """import java.util.*;
import java.util.function.*;
import java.util.stream.*;
import java.time.*;
import java.time.format.*;
import java.math.*;
import java.io.*;
import java.nio.file.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
"""

# Statements that only make sense at class level would break the method wrapper,
# and a `package` line breaks the fixed file name. Detect and handle.
PACKAGE_LINE = re.compile(r'^\s*package\s+[\w.]+\s*;\s*$', re.M)
# Group 1 captures everything after `import` so it can be re-emitted above the
# wrapper class. It MUST capture — without the group, findall returns whole lines
# and the wrapper emits `import import java.util.List;;`.
IMPORT_LINE = re.compile(r'^[ \t]*import[ \t]+((?:static[ \t]+)?[\w.*]+)[ \t]*;[ \t]*$', re.M)


def wrap(code: str, index: int, jdk: str | None = None) -> tuple[str, str]:
    """Return (compilation unit, how it was wrapped).

    `jdk` is the block's pin. It matters because a bare `void foo() { ... }` is
    ambiguous: at top level it is a Java 25 compact source file, but in a Java 21
    post it is just a method fragment that wants a class around it. Compiling the
    second as the first fails under javac 21 with "unnamed classes are a preview
    feature", which is a false alarm about the checker rather than the post. So
    only a block explicitly pinned to 25 is allowed to be a compact source file.
    """
    # A sample's own imports have to move above the wrapper's class.
    own_imports = IMPORT_LINE.findall(code)
    body = IMPORT_LINE.sub("", code)
    # A package line cannot coexist with a fixed output path; drop it, it never
    # affects whether the rest compiles.
    body = PACKAGE_LINE.sub("", body)
    imports = PREAMBLE + "".join(f"import {i};\n" for i in own_imports) if own_imports else PREAMBLE

    if TOP_LEVEL_TYPE.search(body) and COMPACT_SOURCE.search(body):
        # A type declaration AND loose methods alongside it. javac 25 reads that
        # as a compact source file and demands a main method; javac 21 rejects the
        # loose methods outright. Nesting the lot inside a class is legal in both
        # — nested records and classes are fine — and preserves what the sample
        # is demonstrating.
        return (imports + "abstract class Snippet" + str(index) + " {\n" + body + "\n}\n",
                "class body (type + loose methods)")

    if TOP_LEVEL_TYPE.search(body):
        # Already a compilation unit. Every top-level type must be non-public or
        # match the file name, so strip `public` from top-level declarations.
        body = re.sub(r'^(\s*)public(\s+(?:final\s+|abstract\s+|sealed\s+|non-sealed\s+)*'
                      r'(?:class|interface|enum|record|@interface)\s)', r'\1\2', body, flags=re.M)
        return imports + body, "as-is"

    # Before COMPACT_SOURCE: a modifier means it is a member, and `static void
    # main()` wrapped in a class compiles just as well as it would standalone.
    # But a `final` local followed by loose statements is NOT a class body.
    if MEMBER_DECL.search(body) and not METHOD_DECL.search(body) and BARE_CALL.search(body):
        return (imports + "abstract class Snippet" + str(index) + " {\n"
                "  void run() throws Exception {\n" + body + "\n  }\n}\n",
                "statements (final locals)")

    if MEMBER_DECL.search(body):
        return (imports + "abstract class Snippet" + str(index) + " {\n" + body + "\n}\n",
                "class body")

    if jdk == "25" and COMPACT_SOURCE.search(body):
        # A Java 25 compact source file. Compile untouched — wrapping it in
        # anything is precisely what breaks it.
        return imports + body, "compact source (as-is)"

    if COMPACT_SOURCE.search(body):
        # A bare method with no modifier: a fragment. Give it a class to live in.
        return (imports + "abstract class Snippet" + str(index) + " {\n" + body + "\n}\n",
                "class body")

    # Bare statements. `void m()` rather than `main` so a `return;` is legal and
    # a sample declaring its own main does not collide.
    return (imports + "abstract class Snippet" + str(index) + " {\n"
            "  void run() throws Exception {\n" + body + "\n  }\n}\n", "statements")


def extract(entry) -> list[dict]:
    """Every Java code block in one post, with its pinned JDK if it has one."""
    raw = (HERE / "posts" / entry["file"]).read_text(encoding="utf-8")
    out = []
    for i, m in enumerate(BLOCK.finditer(raw)):
        tag = PRE_TAG.search(m.group(0))
        if tag and NON_JAVA.search(tag.group(0)):
            continue
        code = html.unescape(m.group("body")).strip()
        if not code:
            continue
        markers = m.group("markers") or ""
        jdk = JDK_MARKER.search(markers)
        out.append({"slug": entry["slug"], "index": i, "code": code,
                    "jdk": jdk.group(1) if jdk else None,
                    "expect_error": bool(EXPECT_ERROR.search(markers)),
                    "line": raw[:m.start()].count("\n") + 1})
    return out


# A module declaration is a compilation unit of its own kind: it only compiles in
# a file literally named module-info.java, and every package it `exports` has to
# actually exist. Rather than exempt it from checking, build the tiny source tree
# it needs — a module-info plus one placeholder class per exported package.
MODULE_DECL = re.compile(r'^\s*(?:open\s+)?module\s+[\w.]+\s*\{', re.M)
EXPORTS = re.compile(r'^\s*exports\s+([\w.]+)', re.M)


def compile_module(code: str, javac: str, d: Path) -> str | None:
    src = d / "src"
    (src).mkdir(parents=True, exist_ok=True)
    (src / "module-info.java").write_text(code, encoding="utf-8")
    for pkg in EXPORTS.findall(code):
        pkg_dir = src / Path(*pkg.split("."))
        pkg_dir.mkdir(parents=True, exist_ok=True)
        (pkg_dir / "Placeholder.java").write_text(
            f"package {pkg};\npublic class Placeholder {{ }}\n", encoding="utf-8")
    files = [str(f) for f in src.rglob("*.java")]
    try:
        r = subprocess.run([javac, "-nowarn", "-d", str(d / "out")] + files,
                           capture_output=True, text=True, timeout=120)
    except subprocess.SubprocessError as e:
        return f"javac did not run: {e}"
    if r.returncode == 0:
        return None
    lines = [l for l in r.stderr.splitlines() if l.strip()]
    return "(module declaration)\n      " + "\n      ".join(lines[:6])


def compile_one(block: dict, javac: str, workdir: Path) -> str | None:
    """None on success, the compiler's complaint otherwise."""
    if MODULE_DECL.search(block["code"]):
        d = workdir / f"{block['slug']}_{block['index']}_{Path(javac).parent.parent.name}_mod"
        d.mkdir(parents=True, exist_ok=True)
        return compile_module(block["code"], javac, d)

    unit, how = wrap(block["code"], block["index"], block["jdk"])
    d = workdir / f"{block['slug']}_{block['index']}_{Path(javac).parent.parent.name}"
    d.mkdir(parents=True, exist_ok=True)
    src = d / "Snippet.java"
    src.write_text(unit, encoding="utf-8")
    try:
        r = subprocess.run([javac, "-nowarn", "-d", str(d), str(src)],
                           capture_output=True, text=True, timeout=120)
    except subprocess.SubprocessError as e:
        return f"javac did not run: {e}"
    if block.get("expect_error"):
        # The post claims this does not compile. Verify the claim: a sample that
        # started compiling is a sample whose lesson has silently evaporated.
        if r.returncode == 0:
            return ("marked expect-error but it COMPILED — either the post's claim "
                    "is now wrong or the marker is stale")
        return None

    if r.returncode == 0:
        return None
    # Trim to the first few real diagnostics; a cascade after one error is noise.
    lines = [l for l in r.stderr.splitlines() if l.strip()]
    return f"(wrapped {how})\n      " + "\n      ".join(lines[:6])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", metavar="SLUG:INDEX",
                    help="print the wrapped compilation unit for one block and exit")
    ap.add_argument("--jdk21-only", action="store_true",
                    help="skip the Java 25 pass (use when only one JDK is installed)")
    args = ap.parse_args()

    javac21 = find_jdk("21") or shutil.which("javac")
    javac25 = None if args.jdk21_only else find_jdk("25")
    if not javac21:
        print("no JDK 21 found — install one or point PATH at javac")
        return 1

    blocks = []
    for entry in manifest.POSTS:
        path = HERE / "posts" / entry["file"]
        if not path.exists():
            print(f"  .. {entry['slug']:36} not written yet, skipped")
            continue
        blocks.extend(extract(entry))

    if not blocks:
        print("no post bodies written yet — nothing to compile")
        return 0

    if args.show:
        slug, _, idx = args.show.partition(":")
        for b in blocks:
            if b["slug"] == slug and str(b["index"]) == idx:
                unit, how = wrap(b["code"], b["index"], b["jdk"])
                print(f"# {slug} block {idx}  (wrapped: {how})\n")
                print(unit)
                return 0
        print(f"no such block: {args.show}")
        return 1

    print(f"javac 21: {javac21}")
    print(f"javac 25: {javac25 or '(skipped)'}")
    print(f"{len(blocks)} java code blocks in {len(set(b['slug'] for b in blocks))} posts\n")

    # (block, javac, label) for every compile that has to happen.
    jobs = []
    for b in blocks:
        if b["jdk"] == "25":
            if javac25:
                jobs.append((b, javac25, "25"))
            # With --jdk21-only a 25-pinned block is simply not checked; it must
            # never be sent to javac 21, which is the reason the marker exists.
        else:
            jobs.append((b, javac21, "21"))
            if javac25:
                jobs.append((b, javac25, "25"))

    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            futures = {pool.submit(compile_one, b, jc, workdir): (b, label)
                       for b, jc, label in jobs}
            for f in concurrent.futures.as_completed(futures):
                b, label = futures[f]
                err = f.result()
                if err:
                    failures.append(f"{b['slug']} block {b['index']} "
                                    f"(line {b['line']}, javac {label}):\n      {err}")

    by_post = {}
    for b in blocks:
        by_post.setdefault(b["slug"], []).append(b)
    for entry in manifest.POSTS:
        bs = by_post.get(entry["slug"])
        if not bs:
            continue
        pinned = sum(1 for b in bs if b["jdk"])
        expected = sum(1 for b in bs if b["expect_error"])
        bad = sum(1 for f in failures if f.startswith(entry["slug"] + " "))
        bits = ([f"{pinned} pinned to 25"] if pinned else []) + \
               ([f"{expected} must fail"] if expected else [])
        note = f"  ({', '.join(bits)})" if bits else ""
        print(f"  {'x' if bad else 'ok':>2}  {entry['slug']:36} {len(bs):>2} blocks{note}")

    print(f"\n{len(jobs)} compilations across {len(blocks)} blocks")
    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for f in sorted(failures):
            print(f"  x {f}")
        print("\n  re-run with --show SLUG:INDEX to see the wrapped unit")
        return 1
    print("every code sample compiles")
    return 0


if __name__ == "__main__":
    sys.exit(main())

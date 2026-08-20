"""The Python Tutorial track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and post 26 is the newest.

17 of these 26 slugs are LIVE AND INDEXED. They are being reworked in place,
never replaced: changing any one of them changes a URL Google already has. Nine
are new. Do not renumber a slug to match a reordered `file`.

Every existing post carries its original 2020-2021 publication date, and
`upsert_post` never overwrites an existing date, so seeding this track needs
`seed.py --force-dates` for the reading order to come out right. Without it the
archive keeps the old scatter and the prev/next pager walks the track in
publication order rather than teaching order. See progress_report.md.

The 13:00 stamps are deliberate. Five other tracks date their posts over an
overlapping range — /spring-boot, /react and /oracle at 09:00, the DS&A track at
10:00, /backend-dev at 11:00, /java and /frontend-dev at 12:00 and
/spring-study-guide at 14:00 — and an exact tie makes the archive order
arbitrary. 13:00 was the free hour.
"""

CATEGORY = {
    "slug": "python",
    "name": "Python",
    "description": (
        "Python from your first script to the things you will actually reach for at work — data "
        "types and strings, lists, dicts and sets, functions, comprehensions and generators, "
        "classes and dataclasses, exceptions, files, modules and async. Written against Python "
        "3.12, kept short on purpose, and every code sample is executed before it ships."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, which already maps this slug
# to the display name "Python" under the "Python" group. The stored category name
# is currently the lowercase "python"; upserting CATEGORY fixes that.
NAV_GROUP = "Python"

# Snippets in this track are NOT lifted from the demo app by default. Same
# exception /java took and for the same reason: `total = 0` has no business being
# traced back to a console banking app, and forcing it there would make every
# basics post read like application code. The trade is that nothing external
# vouches for the samples, so `check_snippets.py` RUNS every block instead.
#
# A block may still opt in to the demo app with a `<!-- from: path -->` marker,
# which check_provenance.py verifies against this tree.
DEMO_APP = "lovemesomecoding_demo_project/bank/bank-python-console"

# Stated on the get-started page and assumed by every other post.
#
# Folau's call (2026-08-20): baseline Python 3.12 — what bank-python-console
# targets and what the site says elsewhere — but where 3.14 changed something a
# beginner would actually meet, the post shows it in a callout. So
# check_snippets.py runs every block under BOTH interpreters, and a block marked
# `<!-- py:3.14 -->` runs under 3.14 only.
VERSIONS = {
    "python": "3.12",       # the baseline every post assumes
    "latest": "3.14",       # flagged in callouts, never assumed
}

# The release table on the get-started page. README asks for the major Python 3
# releases and what each added, so this is the source of truth for that table —
# edit here, then regenerate the section in post 01.
#
# Python has no LTS releases. Every 3.x gets two years of bugfixes and three more
# of security fixes, then goes end-of-life, so "which one is supported" is a
# different question from Java's and the table says so.
#
# `features` names only what a reader of THIS track would recognise. The full
# what's-new page for each release is a different document and not what was
# asked for.
#
# TODO before publish: re-check the `status` column against
# https://devguide.python.org/versions/ — the support phases move with the
# calendar and this table was written on 2026-08-20.
RELEASES = [
    {"version": "3.9",  "released": "2020-10", "status": "end of life",
     "features": "Dict merge with `|` and `|=`, `str.removeprefix` / `removesuffix`, "
                 "builtin generics (`list[int]`, no `typing.List`), `zoneinfo`"},
    {"version": "3.10", "released": "2021-10", "status": "security fixes only",
     "features": "Structural pattern matching (`match` / `case`), `X | Y` union types, "
                 "much better syntax error messages, parenthesised context managers"},
    {"version": "3.11", "released": "2022-10", "status": "security fixes only",
     "features": "10-60% faster than 3.10, exception groups and `except*`, tracebacks that "
                 "point at the exact expression, `tomllib` in the standard library"},
    {"version": "3.12", "released": "2023-10", "status": "**this track's baseline**",
     "features": "f-strings that can nest and reuse quotes, `type` aliases and the "
                 "`def fn[T](...)` type-parameter syntax, sharper error suggestions"},
    {"version": "3.13", "released": "2024-10", "status": "widely deployed",
     "features": "A new interactive REPL with colour and multiline editing, the "
                 "free-threaded (no-GIL) build as an experiment, an experimental JIT"},
    {"version": "3.14", "released": "2025-10", "status": "current release",
     "features": "Template strings (t-strings), annotations evaluated lazily so type "
                 "hints stop costing import time, free-threading officially supported"},
]

# Target length for every post in this track, measured on the normaliser's
# wordCount (which counts code as well as prose).
#
# Unlike /java, this track's prose is NOT the problem — the 17 existing posts
# already average 1,438 prose words, inside the band. The problem is CODE: 9 to
# 53 blocks per post, pushing four posts past a 16-minute read on under 1,000
# words of actual explanation. So the ceiling that matters here is CODE_BLOCK_MAX,
# not WORD_TARGET. See progress_report.md.
WORD_TARGET = (900, 1800)

# The cap this project exists to enforce. `python-modules-packages` ships 53 code
# blocks and `python-iterationfor-while-loops` 47; that is a reference sheet, not
# a tutorial. For calibration, the 29 authored /java posts run 2-12 blocks and
# average 8. Python samples are shorter, so the cap is a little looser.
CODE_BLOCK_MAX = 14

# A 53-entry table of contents is a second scroll bar, not a navigation aid. Four
# posts currently have NO headings at all and therefore an empty TOC, which is the
# other half of the same bug.
H2_RANGE = (4, 10)

POSTS = [
    # ---- Getting started -------------------------------------------------
    {
        "slug": "python-get-started",
        "title": "Python – Get Started",
        "file": "01-python-get-started.html",
        "date": "2026-06-30T13:00:00",
        "tags": ["python", "getting-started", "pip", "venv"],
        "excerpt": (
            "Start here. Install Python, run your first script, and understand the difference "
            "between the REPL and a file. Which Python version this track uses and why, every "
            "major 3.x release and what each one added, virtual environments and pip, and the "
            "map of the other 25 posts with the order to read them in."
        ),
    },
    {
        "slug": "python-introduction",
        "title": "Python – Introduction",
        "file": "02-python-introduction.html",
        "date": "2026-07-02T13:00:00",
        "tags": ["python", "beginner", "getting-started", "interpreter"],
        "excerpt": (
            "What Python actually is — a language and an interpreter, which is two things people "
            "use one word for. Why indentation is syntax rather than style, what dynamic typing "
            "buys you and costs you, where Python is used in 2026, and how its releases work."
        ),
    },

    # ---- The language ----------------------------------------------------
    {
        "slug": "python-data-types",
        "title": "Python – Data Types",
        "file": "03-python-data-types.html",
        "date": "2026-07-04T13:00:00",
        "tags": ["python", "data-types", "variables", "beginner"],
        "excerpt": (
            "The types you will use every day — int, float, str, bool, None — plus what a variable "
            "really is in Python, why `is` and `==` are not the same question, and the integer "
            "division and float rounding traps that bite everyone once."
        ),
    },
    {
        "slug": "python-string-methods",
        "title": "Python – String Methods",
        "file": "04-python-string-methods.html",
        "date": "2026-07-06T13:00:00",
        "tags": ["python", "strings", "text", "beginner"],
        "excerpt": (
            "The string methods worth memorising — strip, split, join, replace, startswith, and "
            "the case pair — plus slicing, why strings are immutable, and why building one in a "
            "loop with `+=` is the wrong tool."
        ),
    },
    {
        "slug": "python-f-strings",
        "title": "Python – f-strings and Formatting",
        "file": "05-python-f-strings.html",
        "date": "2026-07-08T13:00:00",
        "tags": ["python", "strings", "f-strings", "formatting"],
        "excerpt": (
            "Formatting text the modern way. f-strings, the format spec that lines up currency and "
            "columns, `=` for debugging, what changed in 3.12, and the two older styles you will "
            "still meet in real code and should not write."
        ),
    },
    {
        "slug": "python-conditional-statements",
        "title": "Python – Conditional Statements",
        "file": "06-python-conditional-statements.html",
        "date": "2026-07-10T13:00:00",
        "tags": ["python", "control-flow", "conditionals", "match"],
        "excerpt": (
            "if, elif and else, what Python considers falsy and why that surprises people, the "
            "conditional expression, chained comparisons, and when `match` is genuinely clearer "
            "than a chain of elifs."
        ),
    },
    {
        "slug": "python-iterationfor-while-loops",
        "title": "Python – Iteration (for / while loops)",
        "file": "07-python-iteration-for-while-loops.html",
        "date": "2026-07-12T13:00:00",
        "tags": ["python", "control-flow", "loops", "iteration"],
        "excerpt": (
            "The for loop that walks a sequence rather than an index, when a while loop is the "
            "right shape, range, enumerate and zip, break and continue, and the loop-else clause "
            "almost nobody knows is there."
        ),
    },

    # ---- Collections -----------------------------------------------------
    {
        "slug": "python-lists-list-comprehensions",
        "title": "Python – Lists & List Comprehensions",
        "file": "08-python-lists-list-comprehensions.html",
        "date": "2026-07-14T13:00:00",
        "tags": ["python", "lists", "comprehensions", "collections"],
        "excerpt": (
            "Lists, the operations you actually use on them, sorting with a key, and list "
            "comprehensions — what they replace, when they are clearer than a loop, and the "
            "point past which they stop being readable."
        ),
    },
    {
        "slug": "python-tuples",
        "title": "Python – Tuples",
        "file": "09-python-tuples.html",
        "date": "2026-07-16T13:00:00",
        "tags": ["python", "tuples", "collections", "unpacking"],
        "excerpt": (
            "Tuples and why an immutable sequence earns its place next to the list. Unpacking, "
            "returning more than one value, the starred target, named tuples, and the one-element "
            "tuple that catches everybody."
        ),
    },
    {
        "slug": "python-dictionaries-sets",
        "title": "Python – Dictionaries & Sets",
        "file": "10-python-dictionaries-sets.html",
        "date": "2026-07-18T13:00:00",
        "tags": ["python", "dictionaries", "sets", "collections"],
        "excerpt": (
            "The dict, which is the data structure Python is built on, and the set, which answers "
            "membership and de-duplication in one line. get and setdefault, iteration, dict and "
            "set comprehensions, and what makes a key hashable."
        ),
    },

    # ---- Functions -------------------------------------------------------
    {
        "slug": "python-function",
        "title": "Python – Functions",
        "file": "11-python-function.html",
        "date": "2026-07-20T13:00:00",
        "tags": ["python", "functions", "arguments", "scope"],
        "excerpt": (
            "Defining and calling functions, positional and keyword arguments, defaults, *args and "
            "**kwargs, returning values, docstrings, and the mutable-default-argument bug that is "
            "still the most common Python gotcha there is."
        ),
    },
    {
        "slug": "python-lambda-functions",
        "title": "Python – Lambda Functions",
        "file": "12-python-lambda-functions.html",
        "date": "2026-07-22T13:00:00",
        "tags": ["python", "functions", "lambda", "functional"],
        "excerpt": (
            "The one-expression anonymous function. Where it belongs — a sort key, a small "
            "callback — where it does not, and why `sorted(xs, key=lambda p: p.name)` is the "
            "example that justifies the whole feature."
        ),
    },
    {
        "slug": "python-generators-iterators",
        "title": "Python – Generators & Iterators",
        "file": "13-python-generators-iterators.html",
        "date": "2026-07-24T13:00:00",
        "tags": ["python", "generators", "iterators", "yield"],
        "excerpt": (
            "What the for loop is really doing, and how `yield` lets you produce a sequence "
            "without building it. Generator expressions, laziness and why it matters on a large "
            "file, and the one rule about consuming a generator twice."
        ),
    },
    {
        "slug": "python-decorators",
        "title": "Python – Decorators",
        "file": "14-python-decorators.html",
        "date": "2026-07-26T13:00:00",
        "tags": ["python", "decorators", "functions", "functools"],
        "excerpt": (
            "Decorators, built up from the one fact that makes them possible: functions are "
            "objects. Writing one, passing arguments through it, why `functools.wraps` is not "
            "optional, and the built-in decorators you already use."
        ),
    },

    # ---- Objects ---------------------------------------------------------
    {
        "slug": "python-class",
        "title": "Python – Class",
        "file": "15-python-class.html",
        "date": "2026-07-28T13:00:00",
        "tags": ["python", "classes", "objects", "oop"],
        "excerpt": (
            "Writing a class: `__init__`, what `self` actually is, instance versus class "
            "attributes, methods, and `__repr__` — the dunder that pays for itself the first time "
            "you print a list of your objects."
        ),
    },
    {
        "slug": "python-oop",
        "title": "Python – OOP",
        "file": "16-python-oop.html",
        "date": "2026-07-30T13:00:00",
        "tags": ["python", "oop", "inheritance", "polymorphism"],
        "excerpt": (
            "Inheritance, composition and polymorphism in a language with duck typing, where an "
            "interface is a set of methods rather than a declaration. `super()`, properties, "
            "abstract base classes, and when to prefer composition."
        ),
    },
    {
        "slug": "python-dataclasses-type-hints",
        "title": "Python – Dataclasses & Type Hints",
        "file": "17-python-dataclasses-type-hints.html",
        "date": "2026-08-01T13:00:00",
        "tags": ["python", "dataclasses", "type-hints", "typing"],
        "excerpt": (
            "`@dataclass` writes the constructor, the repr and the equality you were about to "
            "write by hand. Plus type hints: what they do and do not do at runtime, the syntax "
            "worth knowing, and what a checker like mypy adds."
        ),
    },

    # ---- Everyday Python -------------------------------------------------
    {
        "slug": "python-exception-handling",
        "title": "Python – Exception Handling",
        "file": "18-python-exception-handling.html",
        "date": "2026-08-03T13:00:00",
        "tags": ["python", "exceptions", "errors", "try-except"],
        "excerpt": (
            "try, except, else and finally, catching the exception you meant rather than all of "
            "them, raising your own, chaining with `raise ... from`, and why a bare `except:` is "
            "the line that hides the bug you are looking for."
        ),
    },
    {
        "slug": "python-fileread-write",
        "title": "Python – File (read/write)",
        "file": "19-python-file-read-write.html",
        "date": "2026-08-05T13:00:00",
        "tags": ["python", "files", "io", "pathlib"],
        "excerpt": (
            "Reading and writing files with `with open(...)`, why the context manager is not "
            "optional, reading a large file a line at a time, `pathlib` instead of string paths, "
            "and the CSV and JSON modules you will reach for straight afterwards."
        ),
    },
    {
        "slug": "python-user-input",
        "title": "Python – User Input",
        "file": "20-python-user-input.html",
        "date": "2026-08-07T13:00:00",
        "tags": ["python", "input", "cli", "argparse"],
        "excerpt": (
            "`input()` always hands you a string, which is where most beginner bugs start. "
            "Validating and converting it, looping until the answer is usable, hidden input for "
            "passwords, and `argparse` when the input is command-line arguments instead."
        ),
    },
    {
        "slug": "python-modules-packages",
        "title": "Python – Modules & Packages",
        "file": "21-python-modules-packages.html",
        "date": "2026-08-09T13:00:00",
        "tags": ["python", "modules", "packages", "imports"],
        "excerpt": (
            "Splitting code across files. What import really does, the search path, packages and "
            "`__init__.py`, the `if __name__ == \"__main__\"` guard, and why a circular import is "
            "a design problem rather than a syntax one."
        ),
    },
    {
        "slug": "python-async",
        "title": "Python – Async & Await",
        "file": "22-python-async.html",
        "date": "2026-08-11T13:00:00",
        "tags": ["python", "async", "asyncio", "concurrency"],
        "excerpt": (
            "async and await, and the one question that decides whether they help you at all: is "
            "the work waiting or computing. Coroutines, `asyncio.run`, running things at the same "
            "time with `gather`, and the blocking call that quietly ruins it."
        ),
    },

    # ---- Working like a professional -------------------------------------
    {
        "slug": "python-testing",
        "title": "Python – Testing",
        "file": "23-python-testing.html",
        "date": "2026-08-13T13:00:00",
        "tags": ["python", "testing", "pytest", "unittest"],
        "excerpt": (
            "Writing tests with pytest — plain asserts, arranging and asserting, fixtures, "
            "parametrising instead of copy-pasting, and testing that something raises. What "
            "unittest looks like for when you meet it, and what is worth testing at all."
        ),
    },
    {
        "slug": "python-debugging",
        "title": "Python – Debugging",
        "file": "24-python-debugging.html",
        "date": "2026-08-15T13:00:00",
        "tags": ["python", "debugging", "pdb", "logging"],
        "excerpt": (
            "Reading a traceback properly — it is the answer, not the noise — then `breakpoint()` "
            "and the handful of pdb commands worth knowing, logging instead of print, and the "
            "half-dozen error messages that mean something specific."
        ),
    },
    {
        "slug": "python-best-practices",
        "title": "Python – Best Practices",
        "file": "25-python-best-practices.html",
        "date": "2026-08-17T13:00:00",
        "tags": ["python", "best-practices", "pep8", "code-quality"],
        "excerpt": (
            "The conventions that make Python read like Python — PEP 8 and the formatter that "
            "enforces it, naming, EAFP over LBYL, comprehensions over loops over map, and the "
            "handful of habits that separate working code from code someone else can maintain."
        ),
    },
    {
        "slug": "python-code-snippets",
        "title": "Python – Code Snippets",
        "file": "26-python-code-snippets.html",
        "date": "2026-08-19T13:00:00",
        "tags": ["python", "snippets", "recipes", "reference"],
        "excerpt": (
            "The short answers you keep looking up — read a file into a list, sort a dict by "
            "value, flatten a nested list, count occurrences, chunk a list, merge dicts, retry a "
            "call, time a block. Copy, paste, move on."
        ),
    },
]

# Sanity: catch a hand-edit that duplicates a slug, file or date.
for _key in ("slug", "file", "date"):
    _seen = [p[_key] for p in POSTS]
    if len(_seen) != len(set(_seen)):
        _dupes = sorted({v for v in _seen if _seen.count(v) > 1})
        raise SystemExit(f"manifest: duplicate {_key}: {_dupes}")

# The 17 slugs that are already live. Renaming one of these is a URL change and
# check_content.py refuses it, which is the point of writing them down.
EXISTING_SLUGS = {
    "python-introduction", "python-data-types", "python-conditional-statements",
    "python-iterationfor-while-loops", "python-lists-list-comprehensions",
    "python-dictionaries-sets", "python-string-methods", "python-function",
    "python-lambda-functions", "python-class", "python-oop",
    "python-exception-handling", "python-fileread-write", "python-modules-packages",
    "python-decorators", "python-user-input", "python-testing",
}

_manifest_slugs = {p["slug"] for p in POSTS}
if not EXISTING_SLUGS <= _manifest_slugs:
    raise SystemExit(
        "manifest: these live, indexed slugs were dropped from POSTS — that is a URL "
        f"change, not a rename: {sorted(EXISTING_SLUGS - _manifest_slugs)}"
    )

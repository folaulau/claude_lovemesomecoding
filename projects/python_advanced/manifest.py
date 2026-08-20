"""The Python Advanced track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and post 8 is the newest.

ALL EIGHT of these slugs are LIVE AND INDEXED, some since 2019. Every one is
being reworked in place, never replaced: changing any of them changes a URL
Google already has. No post in this track is new.

Every existing post carries its original 2019-2023 publication date, and
`upsert_post` never overwrites an existing date, so seeding this track needs
`seed.py --force-dates` for the reading order to come out right.

The 15:00 stamps are deliberate. Seven other tracks date their posts over an
overlapping range — 09:00 (/spring-boot, /react, /oracle), 10:00 (DS&A),
11:00 (/backend-dev), 12:00 (/java, /frontend-dev), 13:00 (/python) and
14:00 (/spring-study-guide) — and an exact tie makes the archive order
arbitrary. 15:00 was the free hour.
"""

CATEGORY = {
    "slug": "python-advanced",
    "name": "Python Advanced",
    "description": (
        "Where the Python track stops. The iterator and coroutine protocols underneath "
        "generators, functools and operator, serialization and its sharp edges, packaging and "
        "publishing, then NumPy, databases and a first machine learning model. Written against "
        "Python 3.12, and every code sample is executed — including the library ones."
    ),
}

NAV_GROUP = "Python"

# The basics track. This one assumes it and links back to it constantly rather
# than re-explaining anything it covers. See OVERLAP below.
PREREQUISITE = "python"

# Snippets are standalone and RUN, same contract as /python. A block may still
# quote the demo app with `<!-- from: path -->`, which check_provenance.py
# verifies.
DEMO_APP = "lovemesomecoding_demo_project/bank/bank-python-console"

VERSIONS = {
    "python": "3.12",
    "latest": "3.14",
}

# Third-party packages the checker can execute, from `.venv`. A block marked
# `<!-- needs: numpy -->` runs in that venv under 3.12 ONLY — these packages are
# not installed for 3.14 and several do not support it yet.
#
# The venv exists because half of this track is ABOUT libraries. Marking every
# library block `norun` would have left four of the eight posts unverified, and
# a stale API call in the NumPy or MySQL post is exactly the failure this
# tooling is meant to prevent. Versions are pinned in requirements-check.txt.
THIRD_PARTY = {
    "numpy", "pandas", "sklearn", "yaml", "marshmallow", "sqlalchemy",
    "mysql", "matplotlib",
}

# Same band as /python. This track measured 1,889 mean prose words before the
# rework, with three posts over the ceiling and code blocks running to 48.
WORD_TARGET = (900, 1800)

# The cap that matters. Before the rework: 22-48 blocks per post.
CODE_BLOCK_MAX = 14

# Before the rework: 6-16 h2, several with numbered "1." ... "8." headings,
# which is an index rather than a narrative.
H2_RANGE = (4, 10)

# Three of these eight posts duplicated /python once that track was expanded to
# 26 posts on 2026-08-20. Folau's call: keep every slug (all indexed) and
# repoint the content deeper rather than redirect it away. This table records
# what each of the three now covers and what it defers, so the boundary does not
# quietly erode the next time either track is edited.
OVERLAP = {
    "python-advanced-generators-iterators": {
        "duplicated": "/python/python-generators-iterators",
        "now_covers": "the iterator protocol by hand, generators as coroutines "
                      "(send/throw/close), contextlib, and itertools beyond the basics",
        "defers": "what yield is and why laziness matters",
    },
    "python-advanced-map-reduce-and-filter": {
        "duplicated": "/python/python-lambda-functions",
        "now_covers": "functools — reduce, partial, cache, singledispatch — and the "
                      "operator module",
        "defers": "lambda syntax, and why a comprehension beats map/filter",
    },
    "python-advanced-virtual-environments-pip": {
        "duplicated": "/python/python-get-started, /python/python-modules-packages",
        "now_covers": "packaging: pyproject.toml, editable installs, lockfiles and "
                      "reproducible builds, publishing to PyPI",
        "defers": "creating a venv, activating it, and pip install",
    },
}

POSTS = [
    # ---- Language depth ---------------------------------------------------
    {
        "slug": "python-advanced-generators-iterators",
        "title": "Python Advanced – Generators & Iterators",
        "file": "01-python-advanced-generators-iterators.html",
        "date": "2026-08-05T15:00:00",
        "tags": ["python", "generators", "iterators", "coroutines"],
        "excerpt": (
            "Past yield. The iterator protocol written out by hand, generators used as coroutines "
            "with send and throw, why contextlib turns one into a context manager, and the "
            "itertools functions worth knowing by name."
        ),
    },
    {
        "slug": "python-advanced-map-reduce-and-filter",
        "title": "Python Advanced – functools, operator, and reduce",
        "file": "02-python-advanced-map-reduce-and-filter.html",
        "date": "2026-08-07T15:00:00",
        "tags": ["python", "functools", "operator", "functional"],
        "excerpt": (
            "The functional toolkit that survives the comprehension argument: reduce where it is "
            "genuinely the right shape, partial for pre-filling arguments, cache and "
            "singledispatch, and the operator module that replaces most small lambdas."
        ),
    },
    {
        "slug": "python-advanced-serialization",
        "title": "Python Advanced – Serialization",
        "file": "03-python-advanced-serialization.html",
        "date": "2026-08-09T15:00:00",
        "tags": ["python", "serialization", "json", "pickle"],
        "excerpt": (
            "Turning objects into bytes and back. Custom JSON encoders for the types json refuses, "
            "why pickle is a remote code execution risk rather than a file format, YAML's safe_load "
            "rule, and round-tripping dataclasses without writing the mapping by hand."
        ),
    },

    # ---- Shipping it ------------------------------------------------------
    {
        "slug": "python-advanced-virtual-environments-pip",
        "title": "Python Advanced – Packaging & Publishing",
        "file": "04-python-advanced-virtual-environments-pip.html",
        "date": "2026-08-11T15:00:00",
        "tags": ["python", "packaging", "pyproject", "pypi"],
        "excerpt": (
            "From a folder of scripts to something people can install. pyproject.toml, editable "
            "installs, why a lockfile is not requirements.txt, building a wheel, and publishing to "
            "PyPI without breaking anyone's build."
        ),
    },

    # ---- Data -------------------------------------------------------------
    {
        "slug": "python-advanced-numpy-arrays",
        "title": "Python Advanced – NumPy Arrays",
        "file": "05-python-advanced-numpy-arrays.html",
        "date": "2026-08-13T15:00:00",
        "tags": ["python", "numpy", "arrays", "vectorization"],
        "excerpt": (
            "The array that made Python a data language. Why it is faster than a list, shape and "
            "dtype, vectorised operations instead of loops, broadcasting, boolean masks, and the "
            "view-versus-copy distinction that causes the confusing bugs."
        ),
    },
    {
        "slug": "python-advanced-mysql",
        "title": "Python Advanced – Databases",
        "file": "06-python-advanced-mysql.html",
        "date": "2026-08-15T15:00:00",
        "tags": ["python", "database", "sql", "mysql"],
        "excerpt": (
            "Talking to a database from Python. The DB-API every driver implements, parameterised "
            "queries and the injection they prevent, transactions and context managers, connection "
            "pooling, and where an ORM earns its place."
        ),
    },
    {
        "slug": "python-advanced-machine-learning",
        "title": "Python Advanced – Machine Learning",
        "file": "07-python-advanced-machine-learning.html",
        "date": "2026-08-17T15:00:00",
        "tags": ["python", "machine-learning", "scikit-learn", "pandas"],
        "excerpt": (
            "A first model, end to end and actually run: load the data, split it properly, fit a "
            "classifier, and measure it with something better than accuracy. What the workflow is, "
            "what the vocabulary means, and the leakage mistake that flatters every beginner."
        ),
    },

    # ---- Interviews -------------------------------------------------------
    {
        "slug": "python-advanced-interview-questions",
        "title": "Python Advanced – Interview Questions",
        "file": "08-python-advanced-interview-questions.html",
        "date": "2026-08-19T15:00:00",
        "tags": ["python", "interview", "gil", "career"],
        "excerpt": (
            "The questions that actually get asked, with answers that show understanding rather "
            "than recall. Mutable defaults, is versus ==, the GIL and what it does not mean, "
            "shallow copies, decorators, generators, and how to answer when you do not know."
        ),
    },
]

for _key in ("slug", "file", "date"):
    _seen = [p[_key] for p in POSTS]
    if len(_seen) != len(set(_seen)):
        _dupes = sorted({v for v in _seen if _seen.count(v) > 1})
        raise SystemExit(f"manifest: duplicate {_key}: {_dupes}")

# Every slug here is already live. Dropping one is a URL change, not a rename.
EXISTING_SLUGS = {
    "python-advanced-generators-iterators", "python-advanced-map-reduce-and-filter",
    "python-advanced-serialization", "python-advanced-virtual-environments-pip",
    "python-advanced-numpy-arrays", "python-advanced-mysql",
    "python-advanced-machine-learning", "python-advanced-interview-questions",
}

_manifest_slugs = {p["slug"] for p in POSTS}
if EXISTING_SLUGS != _manifest_slugs:
    raise SystemExit(
        "manifest: POSTS must be exactly the eight live slugs — no additions, no removals. "
        f"missing: {sorted(EXISTING_SLUGS - _manifest_slugs)} "
        f"unexpected: {sorted(_manifest_slugs - EXISTING_SLUGS)}"
    )

if set(OVERLAP) - EXISTING_SLUGS:
    raise SystemExit(f"manifest: OVERLAP names unknown slugs: {sorted(set(OVERLAP) - EXISTING_SLUGS)}")

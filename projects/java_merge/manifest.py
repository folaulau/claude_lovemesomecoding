"""The merged `/java` track: 64 posts in reading order.

21 survive from projects/java_tutorial (29 minus the 8 retired in favour of an
incoming duplicate — see plan.RETIRE_IN_FAVOUR_OF). 43 arrive from `/java-8` and
`/java-advanced`.

Every slug here is LIVE AND INDEXED. The 43 incoming ones change category and
therefore change URL, which is why plan.py builds a redirect for each. Do not
rename a slug to tidy it up: that is another URL change and another redirect.

Dates are restamped in reading order, 1 day apart at 12:00, so the archive sorts
newest-first into reverse reading order and the prev/next pager walks 1 -> 64.
12:00 keeps this track clear of /spring-boot (09:00), the DS&A track (10:00),
/backend-dev (11:00) and /spring-study-guide (14:00).
"""

from datetime import datetime, timedelta

TARGET_CATEGORY = "java"
WORD_TARGET = (900, 1800)

CATEGORY = {
    "slug": "java",
    "name": "Java",
    "description": (
        "Everything Java, in one place — from your first program through the language "
        "fundamentals and object orientation, then the functional style Java 8 introduced, "
        "what each LTS release since has added, and the advanced topics you meet at work: "
        "generics, threads, regex, JDBC, logging and encryption."
    ),
}

# (slug, section, tags). Order IS the reading order.
# `origin`: "java" = already in /java, "java-8"/"java-advanced" = moving in.
TRACK = [
    # ---- 1. Getting started ------------------------------------------------
    ("java-get-started",            "Getting started", "java", ["java", "getting-started", "jdk", "java-lts"]),
    ("introduction-to-java",        "Getting started", "java", ["java", "jvm", "beginner", "getting-started"]),

    # ---- 2. The language ---------------------------------------------------
    ("java-variables",              "The language", "java", ["java", "variables", "beginner", "scope"]),
    ("java-data-types",             "The language", "java", ["java", "data-types", "primitives", "beginner"]),
    ("java-operators",              "The language", "java", ["java", "operators", "beginner"]),
    ("java-string",                 "The language", "java", ["java", "string", "immutability", "beginner"]),
    ("java-conditional-statements", "The language", "java", ["java", "control-flow", "switch", "beginner"]),
    ("java-for-loop",               "The language", "java", ["java", "loops", "control-flow", "beginner"]),
    ("java-arrays",                 "The language", "java", ["java", "arrays", "beginner", "collections"]),
    ("java-method",                 "The language", "java", ["java", "methods", "beginner", "overloading"]),

    # ---- 3. Object orientation ---------------------------------------------
    ("java-class",                  "Object orientation", "java", ["java", "class", "oop", "constructor"]),
    ("java-oop",                    "Object orientation", "java", ["java", "oop", "inheritance", "polymorphism"]),
    ("java-interface",              "Object orientation", "java", ["java", "interface", "oop", "abstraction"]),
    ("java-static-and-final-keywords", "Object orientation", "java", ["java", "static", "final", "immutability"]),
    ("java-packages",               "Object orientation", "java", ["java", "packages", "access-modifiers", "project-structure"]),

    # ---- 4. Everyday Java --------------------------------------------------
    ("java-collections",            "Everyday Java", "java", ["java", "collections", "list", "map"]),
    ("java-exception-handling",     "Everyday Java", "java", ["java", "exceptions", "error-handling", "try-catch"]),

    # ---- 5. Functional Java (the Java 8 shift) -----------------------------
    ("java-8-lambda-expression",    "Functional Java", "java-8", ["java", "lambda", "functional", "java-8"]),
    ("java-8-functional-interfaces","Functional Java", "java-8", ["java", "functional-interface", "lambda", "java-8"]),
    ("java-8-method-references",    "Functional Java", "java-8", ["java", "method-reference", "lambda", "java-8"]),
    ("java-8-streams",              "Functional Java", "java-8", ["java", "stream", "functional", "java-8"]),
    ("java-8-collectors-class",     "Functional Java", "java-8", ["java", "collectors", "stream", "java-8"]),
    ("java-8-optional",             "Functional Java", "java-8", ["java", "optional", "null-safety", "java-8"]),
    ("java-8-foreach",              "Functional Java", "java-8", ["java", "foreach", "iteration", "java-8"]),
    ("java-8-interface-default-methods-and-static-methods", "Functional Java", "java-8",
     ["java", "interface", "default-methods", "java-8"]),
    ("java-8-date-time-api",        "Functional Java", "java-8", ["java", "date-time", "java-8", "timezone"]),
    ("java-8-stringjoiner",         "Functional Java", "java-8", ["java", "string", "stringjoiner", "java-8"]),
    ("java-8-array-parallel-sort",  "Functional Java", "java-8", ["java", "arrays", "sorting", "parallel"]),
    ("java-8-completablefuture",    "Functional Java", "java-8", ["java", "concurrency", "async", "completablefuture"]),

    # ---- 6. Java 11 --------------------------------------------------------
    ("java-11-string-methods",      "Java 11", "java-8", ["java", "java-11", "string", "api"]),
    ("java-11-api-improvements",    "Java 11", "java-8", ["java", "java-11", "collections", "files"]),
    ("java-11-httpclient",          "Java 11", "java-8", ["java", "java-11", "http", "api"]),
    ("java-11-single-file-execution","Java 11", "java-8", ["java", "java-11", "tooling", "getting-started"]),
    ("java-11-migration-guide",     "Java 11", "java-8", ["java", "java-11", "migration", "upgrade"]),

    # ---- 7. Java 17 --------------------------------------------------------
    ("java-17-records",             "Java 17", "java-8", ["java", "java-17", "record", "immutability"]),
    ("java-17-sealed-classes",      "Java 17", "java-8", ["java", "java-17", "sealed-class", "pattern-matching"]),
    ("java-17-switch-expressions",  "Java 17", "java-8", ["java", "java-17", "switch", "control-flow"]),
    ("java-17-text-blocks",         "Java 17", "java-8", ["java", "java-17", "text-blocks", "string"]),
    ("java-17-pattern-matching-instanceof", "Java 17", "java-8", ["java", "java-17", "pattern-matching", "instanceof"]),
    ("java-17-other-improvements",  "Java 17", "java-8", ["java", "java-17", "api", "features"]),
    ("java-17-migration-guide",     "Java 17", "java-8", ["java", "java-17", "migration", "upgrade"]),

    # ---- 8. Java 21 --------------------------------------------------------
    ("java-21-virtual-threads",     "Java 21", "java-8", ["java", "java-21", "virtual-threads", "concurrency"]),
    ("java-21-pattern-matching-switch", "Java 21", "java-8", ["java", "java-21", "pattern-matching", "switch"]),
    ("java-21-record-patterns",     "Java 21", "java-8", ["java", "java-21", "record", "pattern-matching"]),
    ("java-21-sequenced-collections", "Java 21", "java-8", ["java", "java-21", "collections", "api"]),
    ("java-21-unnamed-variables",   "Java 21", "java-8", ["java", "java-21", "syntax", "features"]),
    ("java-21-other-improvements",  "Java 21", "java-8", ["java", "java-21", "api", "features"]),
    ("java-21-migration-guide",     "Java 21", "java-8", ["java", "java-21", "migration", "upgrade"]),

    # ---- 9. Java 25 --------------------------------------------------------
    ("java-25-simplified-java",     "Java 25", "java-8", ["java", "java-25", "getting-started", "syntax"]),
    ("java-25-stream-gatherers",    "Java 25", "java-8", ["java", "java-25", "stream", "gatherers"]),
    ("java-25-flexible-constructors","Java 25", "java-8", ["java", "java-25", "constructor", "syntax"]),
    ("java-25-other-improvements",  "Java 25", "java-8", ["java", "java-25", "api", "features"]),
    ("java-25-migration-guide",     "Java 25", "java-8", ["java", "java-25", "migration", "upgrade"]),

    # ---- 10. Advanced ------------------------------------------------------
    ("java-advanced-generics",      "Advanced", "java-advanced", ["java", "generics", "type-safety", "advanced"]),
    ("java-advanced-multithreading","Advanced", "java-advanced", ["java", "concurrency", "threads", "advanced"]),
    ("java-advanced-regex",         "Advanced", "java-advanced", ["java", "regex", "string", "advanced"]),
    ("java-advanced-database",      "Advanced", "java-advanced", ["java", "jdbc", "database", "sql"]),
    ("java-advanced-log4j",         "Advanced", "java-advanced", ["java", "logging", "log4j", "advanced"]),
    ("java-advanced-encryption-and-decryption", "Advanced", "java-advanced", ["java", "security", "encryption", "advanced"]),
    ("java-advanced-eclipse-hot-keys", "Advanced", "java-advanced", ["java", "eclipse", "ide", "productivity"]),

    # ---- 11. Working like a professional -----------------------------------
    ("java-debugging",              "Working like a professional", "java", ["java", "debugging", "stack-trace", "tools"]),
    ("how-to-solve-java-problems",  "Working like a professional", "java", ["java", "debugging", "problem-solving", "beginner"]),
    ("java-best-practices",         "Working like a professional", "java", ["java", "best-practices", "clean-code", "conventions"]),
    ("java-code-snippets",          "Working like a professional", "java", ["java", "snippets", "reference", "how-to"]),
]

# Newest post lands today; the rest step back one day each, in reading order.
_LAST = datetime(2026, 8, 20, 12, 0, 0)
_START = _LAST - timedelta(days=len(TRACK) - 1)

POSTS = [
    {
        "slug": slug,
        "file": f"{slug}.html",
        "section": section,
        "origin": origin,
        "tags": tags,
        "date": (_START + timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%S"),
        "moves": origin != TARGET_CATEGORY,
    }
    for i, (slug, section, origin, tags) in enumerate(TRACK)
]

BY_SLUG = {p["slug"]: p for p in POSTS}

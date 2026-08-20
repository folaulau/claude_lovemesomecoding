"""The Java Tutorial track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and post 29 is the newest.

28 of these 29 slugs are LIVE AND INDEXED. They are being rewritten in place,
never replaced: changing any one of them changes a URL Google already has. Only
`java-get-started` is new. Do not renumber a slug to match a reordered `file`.

Every existing post carries its original 2018-2023 publication date, and
`upsert_post` never overwrites an existing date, so seeding this track needs
`seed.py --force-dates` for the reading order to come out right. Without it the
archive keeps the old scatter and the prev/next pager walks the track in
publication order rather than teaching order. See progress_report.md.

The 12:00 stamps are deliberate. Four other tracks date their posts over an
overlapping range — /spring-boot at 09:00, the DS&A track at 10:00, /backend-dev
at 11:00 and /spring-study-guide at 14:00 — and an exact tie makes the archive
order arbitrary.
"""

CATEGORY = {
    "slug": "java",
    "name": "Java",
    "description": (
        "Java from your first program to the features you will actually use at work — variables "
        "and types, control flow, classes and interfaces, collections and exceptions, then "
        "lambdas, streams, Optional, records and sealed classes. Written against Java 21, kept "
        "short on purpose, and every code sample compiles."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, which already maps this slug
# to the display name "Java" under the "Java" group.
NAV_GROUP = "Java"

# Folau, 2026-08-20: draw examples from the console bank app. He first pointed at
# `bank/bank-python-console` — the Python twin — and confirmed the Java one is
# what a Java tutorial should quote. The two are kept at parity over the same CSV
# files by `bank/parity.sh`.
#
# This app is a far better fit than the pizza Spring Boot backend the sibling
# tracks use: it is plain Java 21 with no framework, no build tool and no
# database, and its own README says teachability outranks cleverness. A basics
# post can quote it without the result reading like framework code.
DEMO_APP = "lovemesomecoding_demo_project/bank/bank-java-console"

# Which posts quote it, and which deliberately do not. The app has NO interfaces
# and NO sealed types, so posts 13 and 24 are standalone by necessity, not choice
# — do not go looking for source to cite there. The pure-syntax posts (variables,
# operators, loops, packages) are standalone because a banking domain would add
# noise to `i++`, not insight.
#
# A quoted block is marked `<!-- from: <path relative to DEMO_APP> -->` and is
# verified by check_provenance.py rather than compiled by check_snippets.py — a
# method lifted out of its class cannot compile alone. See progress_report.md.
QUOTES_DEMO_APP = [
    "java-data-types", "java-string", "java-conditional-statements", "java-class",
    "java-oop", "java-static-and-final-keywords", "java-collections",
    "java-exception-handling", "java-date", "java-stream", "java-method-reference",
    "java-optional", "java-record", "java-best-practices",
]

# Stated on the get-started page and assumed by every other post.
#
# Folau's call (2026-08-20): baseline Java 21, but where 25 changed something a
# beginner would actually meet — the first program, most obviously — the post
# shows the 25 form in a callout. So check_snippets.py compiles every block under
# BOTH JDKs, and a block marked `<!-- jdk:25 -->` is compiled under 25 only.
VERSIONS = {
    "java": "21",           # the baseline every post assumes
    "latest-lts": "25",     # flagged in callouts, never assumed
}

# The LTS table on the get-started page. README asks for "major LTS java releases
# and new features that came out on each release", so this is the source of truth
# for that table — edit here, then regenerate the section in post 01.
#
# `features` names only what a reader of THIS track would recognise. The full JEP
# list for each release is a different document and not what was asked for.
LTS_RELEASES = [
    {"version": "8",  "released": "2014-03", "status": "legacy, still widespread",
     "features": "Lambdas, Stream API, Optional, method references, "
                 "default methods on interfaces, java.time"},
    {"version": "11", "released": "2018-09", "status": "legacy",
     "features": "`var` for local variables, new String methods (isBlank, strip, "
                 "lines, repeat), HttpClient, run a .java file without compiling it"},
    {"version": "17", "released": "2021-09", "status": "still common in production",
     "features": "Records, sealed classes, switch expressions, text blocks, "
                 "instanceof pattern matching, helpful NullPointerExceptions"},
    {"version": "21", "released": "2023-09", "status": "**this track's baseline**",
     "features": "Virtual threads, pattern matching for switch, record patterns, "
                 "sequenced collections"},
    {"version": "25", "released": "2025-09", "status": "current LTS",
     "features": "Compact source files and instance main methods (hello world with "
                 "no class and no static), the IO class, module import declarations, "
                 "flexible constructor bodies, scoped values"},
]

# Target length for every post in this track. The 2026-02-28 pass left the track
# averaging 6,362 words — 19 of 28 posts were 30-44 minute reads. README asks
# twice for posts to be kept to the point, so check_content.py enforces this band.
#
# The CEILING is the point of this project. The floor is only a thinness guard,
# and it is 900 rather than 1200 because that is what the track this band was
# matched to actually measures: /backend-dev's ten posts run 926-1464 words. An
# 1,050-word post that has said everything it needs to say is finished, not thin.
WORD_TARGET = (900, 1800)

POSTS = [
    # ---- Getting started -------------------------------------------------
    {
        "slug": "java-get-started",
        "title": "Java – Get Started",
        "file": "01-java-get-started.html",
        "date": "2026-06-24T12:00:00",
        "tags": ["java", "getting-started", "jdk", "java-lts"],
        "excerpt": (
            "Start here. Install a JDK, run your first program, and understand the three commands "
            "that turn a text file into something the computer executes. Which Java version this "
            "track uses and why, every major LTS release and what each one added, and the map of "
            "the other 28 posts with the order to read them in."
        ),
    },
    {
        "slug": "introduction-to-java",
        "title": "Introduction to Java",
        "file": "02-introduction-to-java.html",
        "date": "2026-06-26T12:00:00",
        "tags": ["java", "jvm", "beginner", "getting-started"],
        "excerpt": (
            "What Java actually is — a language, a compiler and a virtual machine, which is three "
            "things people use one word for. Why write once run anywhere still matters, what the "
            "JVM buys you, where Java is used in 2026, and how versions and LTS releases work."
        ),
    },

    # ---- The language ----------------------------------------------------
    {
        "slug": "java-variables",
        "title": "Java Variables",
        "file": "03-java-variables.html",
        "date": "2026-06-28T12:00:00",
        "tags": ["java", "variables", "beginner", "scope"],
        "excerpt": (
            "A variable is a named box with a type. Declaring and assigning, the three kinds — "
            "local, instance and static — and the scope rules that decide where each one is "
            "visible and when it dies. Plus `var`, and the one place it hurts readability."
        ),
    },
    {
        "slug": "java-data-types",
        "title": "Java Data Types",
        "file": "04-java-data-types.html",
        "date": "2026-06-30T12:00:00",
        "tags": ["java", "data-types", "primitives", "beginner"],
        "excerpt": (
            "Eight primitives and everything else. What each primitive costs and what it can "
            "hold, why `int` overflows silently, why `double` cannot represent 0.1, when to reach "
            "for `BigDecimal`, and what autoboxing does behind your back."
        ),
    },
    {
        "slug": "java-operators",
        "title": "Java Operators",
        "file": "05-java-operators.html",
        "date": "2026-07-02T12:00:00",
        "tags": ["java", "operators", "beginner"],
        "excerpt": (
            "Arithmetic, comparison, logical and assignment operators, plus the ternary. The "
            "traps that actually catch people: integer division truncating, `==` on objects "
            "comparing identity, and short-circuit evaluation you should be relying on."
        ),
    },
    {
        "slug": "java-string",
        "title": "Java String",
        "file": "06-java-string.html",
        "date": "2026-07-04T12:00:00",
        "tags": ["java", "string", "immutability", "beginner"],
        "excerpt": (
            "Strings are immutable and that single fact explains most of their behaviour. The "
            "methods worth memorising, why `==` is the classic bug, when concatenation in a loop "
            "becomes a performance problem, text blocks, and formatting."
        ),
    },
    {
        "slug": "java-conditional-statements",
        "title": "Java Conditional Statements",
        "file": "07-java-conditional-statements.html",
        "date": "2026-07-06T12:00:00",
        "tags": ["java", "control-flow", "switch", "beginner"],
        "excerpt": (
            "`if`, `else if`, `else`, the ternary, and `switch` — including the arrow form and "
            "switch expressions, which removed the fall-through bug that made the old syntax "
            "dangerous. When a guard clause beats nesting."
        ),
    },
    {
        "slug": "java-for-loop",
        "title": "Java For Loop",
        "file": "08-java-for-loop.html",
        "date": "2026-07-08T12:00:00",
        "tags": ["java", "loops", "control-flow", "beginner"],
        "excerpt": (
            "The classic `for`, the enhanced for-each, `while` and `do-while`, and how to choose. "
            "`break` and `continue`, nested loops, and the two errors everyone writes at least "
            "once: the off-by-one and modifying a collection while iterating it."
        ),
    },
    {
        "slug": "java-arrays",
        "title": "Java Arrays",
        "file": "09-java-arrays.html",
        "date": "2026-07-10T12:00:00",
        "tags": ["java", "arrays", "beginner", "collections"],
        "excerpt": (
            "Fixed-size, typed, zero-indexed. Declaring and initialising, iterating, "
            "multi-dimensional arrays, the `Arrays` utility methods that save you writing loops, "
            "and the moment you should stop using an array and reach for a `List`."
        ),
    },
    {
        "slug": "java-method",
        "title": "Java Method",
        "file": "10-java-method.html",
        "date": "2026-07-12T12:00:00",
        "tags": ["java", "methods", "beginner", "overloading"],
        "excerpt": (
            "Signatures, parameters and return values. Overloading and the rules that decide "
            "which overload wins, varargs, static versus instance methods, and the thing that "
            "confuses everyone: Java is pass-by-value, even for objects."
        ),
    },

    # ---- Object orientation ----------------------------------------------
    {
        "slug": "java-class",
        "title": "Java Class",
        "file": "11-java-class.html",
        "date": "2026-07-14T12:00:00",
        "tags": ["java", "class", "oop", "constructor"],
        "excerpt": (
            "Fields, constructors and methods, and what `new` actually does. Constructor "
            "chaining, `this`, why you write getters instead of public fields, and the two "
            "methods you inherit from Object and will eventually have to override."
        ),
    },
    {
        "slug": "java-oop",
        "title": "Java OOP",
        "file": "12-java-oop.html",
        "date": "2026-07-16T12:00:00",
        "tags": ["java", "oop", "inheritance", "polymorphism"],
        "excerpt": (
            "Encapsulation, inheritance, polymorphism and abstraction — the four ideas, each in "
            "code rather than in a definition. Overriding versus overloading, abstract classes, "
            "and why composition is usually the better answer to “I want to reuse this”."
        ),
    },
    {
        "slug": "java-interface",
        "title": "Java Interface",
        "file": "13-java-interface.html",
        "date": "2026-07-18T12:00:00",
        "tags": ["java", "interface", "oop", "abstraction"],
        "excerpt": (
            "An interface is a contract with no state. Implementing one, why a class can "
            "implement many but extend only one, default and static methods and what they were "
            "added for, functional interfaces, and interface versus abstract class."
        ),
    },
    {
        "slug": "java-static-and-final-keywords",
        "title": "Static and Final Keywords",
        "file": "14-java-static-and-final-keywords.html",
        "date": "2026-07-20T12:00:00",
        "tags": ["java", "static", "final", "immutability"],
        "excerpt": (
            "`static` belongs to the class, `final` cannot be reassigned — and both are "
            "misunderstood in the same way. Static fields, methods and blocks, constants, final "
            "parameters, final classes, and why a `final` reference is not an immutable object."
        ),
    },
    {
        "slug": "java-packages",
        "title": "Packages",
        "file": "15-java-packages.html",
        "date": "2026-07-22T12:00:00",
        "tags": ["java", "packages", "access-modifiers", "project-structure"],
        "excerpt": (
            "How Java organises code into namespaces. Declaring a package, how it maps to "
            "directories, imports and why the wildcard is discouraged, the four access modifiers "
            "including the default nobody names, and how to lay out a real project."
        ),
    },

    # ---- Everyday Java ---------------------------------------------------
    {
        "slug": "java-collections",
        "title": "Collections",
        "file": "16-java-collections.html",
        "date": "2026-07-24T12:00:00",
        "tags": ["java", "collections", "list", "map"],
        "excerpt": (
            "List, Set, Map and Queue, and how to pick one in about five seconds. ArrayList "
            "versus LinkedList, HashMap versus TreeMap, why HashSet needs equals and hashCode to "
            "work, iteration, and the immutable factory methods."
        ),
    },
    {
        "slug": "java-exception-handling",
        "title": "Exception Handling",
        "file": "17-java-exception-handling.html",
        "date": "2026-07-26T12:00:00",
        "tags": ["java", "exceptions", "error-handling", "try-catch"],
        "excerpt": (
            "try, catch, finally and try-with-resources. Checked versus unchecked and when each "
            "is the right choice, writing your own exception, and the four ways to handle one "
            "badly — starting with the empty catch block that swallows the evidence."
        ),
    },
    {
        "slug": "java-date",
        "title": "Java Date",
        "file": "18-java-date.html",
        "date": "2026-07-28T12:00:00",
        "tags": ["java", "date-time", "java-8", "timezone"],
        "excerpt": (
            "Use `java.time` and never `Date` or `Calendar`. LocalDate, LocalDateTime, Instant "
            "and ZonedDateTime and which one your field should be, formatting and parsing, doing "
            "arithmetic on dates, and storing timestamps so time zones cannot hurt you."
        ),
    },

    # ---- Modern Java -----------------------------------------------------
    {
        "slug": "java-lambda-expression",
        "title": "Java – Lambda Expression",
        "file": "19-java-lambda-expression.html",
        "date": "2026-07-30T12:00:00",
        "tags": ["java", "lambda", "functional", "java-8"],
        "excerpt": (
            "A lambda is a function you can pass around, and it works because of one rule: it "
            "implements an interface with a single abstract method. The syntax, the built-in "
            "functional interfaces worth knowing, and effectively-final capture."
        ),
    },
    {
        "slug": "java-stream",
        "title": "Java – Stream",
        "file": "20-java-stream.html",
        "date": "2026-08-01T12:00:00",
        "tags": ["java", "stream", "functional", "java-8"],
        "excerpt": (
            "Describe what you want instead of looping. Source, intermediate operations, "
            "terminal operation — and why nothing runs until the terminal one. filter, map, "
            "collect, the Collectors worth knowing, and when a plain for loop is still better."
        ),
    },
    {
        "slug": "java-method-reference",
        "title": "Java – Method Reference",
        "file": "21-java-method-reference.html",
        "date": "2026-08-03T12:00:00",
        "tags": ["java", "method-reference", "lambda", "functional"],
        "excerpt": (
            "`String::toUpperCase` is a lambda with the noise removed. The four forms — static, "
            "bound instance, unbound instance and constructor — what each one desugars to, and "
            "the rule for when a method reference is clearer than the lambda it replaces."
        ),
    },
    {
        "slug": "java-optional",
        "title": "Java – Optional",
        "file": "22-java-optional.html",
        "date": "2026-08-05T12:00:00",
        "tags": ["java", "optional", "null-safety", "java-8"],
        "excerpt": (
            "A return type that says “there might be nothing here” in the signature "
            "instead of in a comment. Creating one, map and flatMap and filter, getting a value "
            "out safely — and the three places Optional does not belong."
        ),
    },
    {
        "slug": "java-record",
        "title": "Java Record",
        "file": "23-java-record.html",
        "date": "2026-08-07T12:00:00",
        "tags": ["java", "record", "immutability", "java-16"],
        "excerpt": (
            "One line replaces the sixty you used to write for a data carrier. What the compiler "
            "generates, compact constructors for validation, what records deliberately cannot do, "
            "and why shallow immutability is a trap worth knowing about."
        ),
    },
    {
        "slug": "java-sealed-class",
        "title": "Java Sealed Class",
        "file": "24-java-sealed-class.html",
        "date": "2026-08-09T12:00:00",
        "tags": ["java", "sealed-class", "pattern-matching", "java-17"],
        "excerpt": (
            "`sealed` lets you say these are the only subtypes, and the compiler holds you to it. "
            "permits, the sealed/final/non-sealed rule, and the payoff — a switch over a sealed "
            "type that the compiler proves you have covered exhaustively."
        ),
    },
    {
        "slug": "java-completablefuture",
        "title": "Java – CompletableFuture",
        "file": "25-java-completablefuture.html",
        "date": "2026-08-11T12:00:00",
        "tags": ["java", "concurrency", "async", "completablefuture"],
        "excerpt": (
            "Run work off the calling thread and chain what happens next. supplyAsync, thenApply "
            "versus thenCompose, running several in parallel and waiting for all, handling "
            "exceptions in a chain, and why you should pass your own executor."
        ),
    },

    # ---- Working like a professional -------------------------------------
    {
        "slug": "java-debugging",
        "title": "Debugging",
        "file": "26-java-debugging.html",
        "date": "2026-08-13T12:00:00",
        "tags": ["java", "debugging", "stack-trace", "tools"],
        "excerpt": (
            "Reading a stack trace properly — which line is yours, what “Caused by” "
            "means, and why the top frame is rarely the bug. Breakpoints, stepping, conditional "
            "breakpoints, watches, and logging that is still useful in production."
        ),
    },
    {
        "slug": "how-to-solve-java-problems",
        "title": "How to Solve Java Problems",
        "file": "27-how-to-solve-java-problems.html",
        "date": "2026-08-15T12:00:00",
        "tags": ["java", "debugging", "problem-solving", "beginner"],
        "excerpt": (
            "A method for getting unstuck. Read the error before you search for it, reproduce it "
            "smaller, change one thing at a time, and check your assumptions in that order. Plus "
            "the errors every Java beginner hits and what each one actually means."
        ),
    },
    {
        "slug": "java-best-practices",
        "title": "Java Best Practices",
        "file": "28-java-best-practices.html",
        "date": "2026-08-17T12:00:00",
        "tags": ["java", "best-practices", "clean-code", "conventions"],
        "excerpt": (
            "The habits that separate code people can maintain from code they rewrite. Naming, "
            "small methods, immutability by default, failing fast, avoiding null, handling "
            "exceptions honestly, and the conventions every Java team already expects."
        ),
    },
    {
        "slug": "java-code-snippets",
        "title": "Java Code Snippets",
        "file": "29-java-code-snippets.html",
        "date": "2026-08-19T12:00:00",
        "tags": ["java", "snippets", "reference", "how-to"],
        "excerpt": (
            "The lookups you will make over and over, in one place. Reading a file, parsing and "
            "formatting a date, sorting a list, grouping with streams, string to number, random "
            "values, and copying a collection safely. Every one compiles as written."
        ),
    },
]

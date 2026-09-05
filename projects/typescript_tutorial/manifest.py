"""The TypeScript track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend
with the track and lesson 21 is the newest.

Unlike the React and FastAPI tracks, **every slug here is new**. There is no `typescript` category
in the content DB (checked 2026-09-05 against the 42 in `content/index/categories.json`), so no
indexed URL is at risk and `seed.py` never needs `--force-dates`. If that ever stops being true —
if a `typescript` post is published by hand before this track seeds — add it to FROZEN_SLUGS and
the seed guard will start protecting it.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, so re-basing the whole
track is one edit.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "typescript",
    "name": "TypeScript",
    "description": (
        "TypeScript from the first annotation to a codebase that holds together — the type "
        "system itself, then what changes when you point it at a real project: unions instead of "
        "enums, generics that earn their place, the tsconfig flags that decide what compiles, "
        "decorators, and React. Every example is lifted from a working marketplace app, so the "
        "code in these posts is code that runs."
    ),
}

# Where the category sits in the site navigation. Unlike every other track's, this one is a REAL
# task, not a note: `typescript` is a brand-new slug, so it does not appear in
# lovemesomecoding_frontend/src/lib/nav.ts at all yet and the dropdown will not show it until it
# is added to the JavaScript group. See progress_report.md.
NAV_GROUP = "JavaScript"

# The app every code sample is taken from.
#
# ⚠️ NOT the contractor app, even though ITS readme says the TypeScript track would come from it.
# That project was still being written when this track started — its whole source tree was created
# inside one 35-minute window on 2026-09-05, `api/client.ts` was split into `queries.ts` and then
# restored while this manifest was being drafted, and nothing in it is committed. A tutorial that
# quotes a tree changing every thirty seconds is a tutorial that ships stale code.
#
# Pizza is the opposite: last touched 2026-08-24, committed, and it typechecks. Folau's call,
# 2026-09-05. If the contractor app ever settles, the NestJS half would strengthen lesson 19 —
# but Angular already supplies decorators, so nothing is actually missing.
DEMO_APP = "lovemesomecoding_demo_project/pizza"

# The two halves of it, both TypeScript. They are quoted for DIFFERENT things and the split is
# deliberate — see the tsconfig note below.
RA = "pizza-react-frontend"
NG = "pizza-angular-frontend"

# ---------------------------------------------------------------------------
# Versions — READ OFF THIS MACHINE, not chosen
# ---------------------------------------------------------------------------
# `npx tsc --version` in both app directories and `node --version`, 2026-09-05.
#
# ⚠️ The two apps are on DIFFERENT TypeScript versions, and that is a feature rather than an
# oversight to tidy up. Angular 21 pins its own compiler and had not moved to 6.x, so:
#
#   pizza-react-frontend    TS 6.0.3, `erasableSyntaxOnly: true`   -> no enums, no parameter
#                                                                     properties, no decorators
#   pizza-angular-frontend  TS 5.9.3, `experimentalDecorators: true` -> decorators everywhere
#
# One repository, two legitimate configurations, and each one forbids something the other relies
# on. Lessons 9 (enums), 12 (classes), 18 (tsconfig) and 19 (decorators) are all built on that
# contrast — it turns "should you use X?" into "under this flag X does not compile, so here is
# what the app does instead", which is a much better lesson than a preference.
VERSIONS = {
    "typescript (react)": "6.0.3",
    "typescript (angular)": "5.9.3",
    "node": "22.23.2",
    "react": "19.2.8",
    "vite": "8.2.0",
    "redux-toolkit": "2.12.0",
    "angular": "21.2.0",
    "ngrx": "21.1.1",
    "rxjs": "7.8",
}

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together, then
# `readingMinutes = max(1, round(words / 220))`. See lovemesomecoding_backend/app/services/
# content.py. Budgeting prose alone silently doubles the published reading time.
#
# Folau asked for 8-10 reading-minutes (2026-09-05) — deeper than the React track's 4-7, half of
# FastAPI's 13-16.
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (8, 10)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 1,760
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 2,200

# ⚠️ The prose floor is 45% here, HIGHER than the FastAPI track's 40%, and the reason is specific
# to a language tutorial.
#
# A framework post quotes whole modules, so code legitimately dominates. A TypeScript post's
# snippets are three or four lines demonstrating one rule — so when code takes over the word count
# in THIS track, it is not because the examples are substantial. It is because the post has become
# a syntax reference with captions, which is the exact failure mode w3schools has and the reason
# the README says to use it for the topic list rather than the treatment.
MIN_PROSE_SHARE = 0.45

# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------
# 21 posts, 3 days apart, landing the last one on 2026-09-05.
START_DATE = datetime(2026, 7, 7, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=index * STEP_DAYS)).strftime("%Y-%m-%dT%H:%M:%S")


# ---------------------------------------------------------------------------
# Which files each post is allowed to quote
# ---------------------------------------------------------------------------
# Paths are relative to DEMO_APP. check_snippets.py checks a post's blocks against THESE files
# first, and reports a block that matches the app but not the declared list — a snippet that has
# drifted in from an unrelated module is a finding, not a pass.
SNIPPET_SOURCES = {
    "typescript-get-started": [
        f"{RA}/package.json", f"{NG}/package.json",
        # The landing page opens on the money helpers and the cart line, because "rename a field
        # and watch what happens" is the argument for the whole track.
        f"{RA}/src/lib/money.ts", f"{RA}/src/types/index.ts",
    ],
    "typescript-set-up": [
        f"{RA}/package.json", f"{RA}/tsconfig.json", f"{RA}/tsconfig.app.json",
        f"{RA}/tsconfig.node.json", f"{RA}/vite.config.ts",
        f"{NG}/package.json", f"{NG}/tsconfig.json", f"{NG}/tsconfig.app.json",
    ],
    "typescript-basic-types": [
        f"{RA}/src/types/index.ts", f"{RA}/src/lib/money.ts",
    ],
    "typescript-special-types": [
        # `toApiFailure` and `failureMessage` both take `unknown` and prove what they have before
        # touching it — the whole lesson, already written and running.
        f"{RA}/src/store/apiFailure.ts", f"{RA}/src/lib/api.ts",
        f"{NG}/src/app/core/api-error.ts",
    ],
    "typescript-arrays-and-tuples": [
        f"{RA}/src/types/index.ts", f"{RA}/src/lib/money.ts",
        # for the spread example — Math.min over a mapped price list
        f"{RA}/src/components/ProductCard.tsx",
    ],
    "typescript-object-types": [
        f"{RA}/src/types/index.ts",
        # for Record<string, string> — the index-signature section
        f"{RA}/src/lib/api.ts",
    ],
    "typescript-interfaces-vs-type-aliases": [
        f"{RA}/src/types/index.ts", f"{RA}/src/lib/money.ts",
        f"{NG}/src/app/admin/store/outcome.ts",
        # MoneyPipe is quoted as the `implements` example — an interface satisfied by a class,
        # which is the myth this lesson kills.
        f"{NG}/src/app/core/money.pipe.ts",
        # the `interface Props` example in the component-props section
        f"{RA}/src/components/ProductCard.tsx",
    ],
    "typescript-union-and-intersection-types": [
        f"{RA}/src/types/index.ts", f"{NG}/src/app/admin/store/outcome.ts",
    ],
    "typescript-enums": [
        # No `enum` anywhere in either app: the React half forbids it with erasableSyntaxOnly and
        # uses string-literal unions instead. That IS the lesson.
        f"{RA}/src/types/index.ts", f"{RA}/tsconfig.app.json",
        f"{NG}/src/app/core/models.ts",
        # `const RANGES = [7, 30, 90] as const` — the runtime-values replacement for an enum,
        # and the only `as const` in the React app that is not a one-off cast.
        f"{RA}/src/pages/admin/AdminReportsPage.tsx",
    ],
    "typescript-narrowing": [
        f"{RA}/src/store/apiFailure.ts", f"{NG}/src/app/core/api-error.ts",
        f"{NG}/src/app/admin/store/outcome.ts",
    ],
    "typescript-functions": [
        f"{RA}/src/lib/money.ts", f"{RA}/src/lib/api.ts",
        f"{NG}/src/app/core/money.pipe.ts",
        # the callback-prop type, quoted as the canonical `(x: T) => void`
        f"{RA}/src/components/ProductCard.tsx",
    ],
    "typescript-classes": [
        f"{RA}/src/lib/api.ts", f"{NG}/src/app/core/api-error.ts",
        f"{NG}/src/app/core/money.pipe.ts", f"{RA}/tsconfig.app.json",
    ],
    "typescript-generics": [
        # `request<T>` plus the `api` object that fixes the method and forwards T.
        f"{RA}/src/lib/api.ts", f"{RA}/src/types/index.ts",
    ],
    "typescript-utility-types": [
        # Omit<RequestOptions,…> in api.ts, Record<string,string> in both ApiErrors, and
        # ReturnType<typeof store.getState> in the store.
        f"{RA}/src/lib/api.ts", f"{RA}/src/store/index.ts",
        f"{RA}/src/store/apiFailure.ts",
    ],
    "typescript-mapped-and-conditional-types": [
        f"{RA}/src/store/index.ts", f"{RA}/src/types/index.ts",
        # `const RANGES = [7, 30, 90] as const` — the typeof/indexed-access worked example
        f"{RA}/src/pages/admin/AdminReportsPage.tsx",
    ],
    "typescript-type-assertions": [
        f"{RA}/src/lib/api.ts", f"{NG}/src/app/core/api-error.ts",
        f"{NG}/src/app/admin/store/outcome.ts",
        # the two real `as const` uses in the apps
        f"{RA}/src/pages/admin/AdminReportsPage.tsx",
        f"{NG}/src/app/core/cart.service.ts",
    ],
    "typescript-modules": [
        f"{RA}/src/types/index.ts", f"{RA}/src/lib/api.ts",
        f"{RA}/tsconfig.app.json", f"{NG}/src/app/core/api-error.ts",
    ],
    "typescript-tsconfig": [
        f"{RA}/tsconfig.json", f"{RA}/tsconfig.app.json", f"{RA}/tsconfig.node.json",
        f"{NG}/tsconfig.json", f"{NG}/tsconfig.app.json",
    ],
    "typescript-decorators": [
        f"{NG}/src/app/core/money.pipe.ts", f"{NG}/src/app/core/autofocus.directive.ts",
        f"{NG}/src/app/core/auth.service.ts",
        f"{NG}/src/app/shared/product-card/product-card.ts",
        f"{NG}/tsconfig.json", f"{RA}/tsconfig.app.json",
    ],
    "typescript-with-react": [
        f"{RA}/src/components/ProductCard.tsx", f"{RA}/src/context/AuthContext.tsx",
        f"{RA}/src/lib/api.ts", f"{RA}/src/types/index.ts",
        f"{RA}/src/store/index.ts",
    ],
    "typescript-interview-questions": [
        f"{RA}/src/types/index.ts", f"{RA}/src/lib/api.ts",
        f"{RA}/src/store/apiFailure.ts", f"{NG}/src/app/admin/store/outcome.ts",
    ],
}

# A section deliberately showing the WRONG way. check_snippets.py excludes blocks near this marker
# from the "must match the app" rule, because not matching is the entire point of them.
#
# This track leans on that harder than any other: half of teaching a type system is showing the
# code it REJECTS, and none of that code can compile, let alone live in the app.
ANTIPATTERN_MARKER = "does not compile"

# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
_TRACK = [
    # ------------------------------------------------------------ start here
    {
        "slug": "typescript-get-started",
        "title": "TypeScript – Get Started",
        "tags": ["typescript", "javascript"],
        "excerpt": (
            "Start here. What TypeScript actually is — a type checker that erases itself, not a "
            "language that runs — the three kinds of bug it catches and the one class it cannot, "
            "the exact versions this track is written against, the marketplace app every example "
            "is taken from, and the full lesson index in reading order."
        ),
    },
    {
        "slug": "typescript-set-up",
        "title": "TypeScript – Setting Up a Project",
        "tags": ["typescript", "tsconfig", "vite"],
        "excerpt": (
            "Two projects, two setups, and the difference matters. A Node service where tsc emits "
            "the JavaScript, and a Vite app where tsc only checks and the bundler strips the "
            "types. What tsc --init actually gives you, why noEmit is not a downgrade, and the "
            "four commands you will run every day."
        ),
    },
    {
        "slug": "typescript-basic-types",
        "title": "TypeScript – The Basic Types",
        "tags": ["typescript", "types"],
        "excerpt": (
            "string, number, boolean and the annotations you do not need to write. Where "
            "inference is better than an explicit type and where it quietly gives up, why let and "
            "const infer differently, literal types, and the one place a return type is worth "
            "writing by hand even though TypeScript could work it out."
        ),
    },
    {
        "slug": "typescript-special-types",
        "title": "TypeScript – any, unknown, never and void",
        "tags": ["typescript", "types"],
        "excerpt": (
            "The four types that are not values. any switches the checker off and spreads; "
            "unknown is the safe version and forces you to prove what you have; never is what a "
            "function that does not return has, and the trick behind exhaustive switches; void is "
            "not undefined. With the catch (err: unknown) block that made the case."
        ),
    },
    # ----------------------------------------------------- shaping data
    {
        "slug": "typescript-arrays-and-tuples",
        "title": "TypeScript – Arrays and Tuples",
        "tags": ["typescript", "types"],
        "excerpt": (
            "string[] versus Array<string>, arrays of unions versus unions of arrays, and readonly "
            "arrays that stop a helper mutating its argument. Then tuples: fixed length, typed per "
            "position, and the one in this app's date formatter that would be Array<string | "
            "number> without them — which is to say, useless."
        ),
    },
    {
        "slug": "typescript-object-types",
        "title": "TypeScript – Object Types",
        "tags": ["typescript", "types", "interface"],
        "excerpt": (
            "Optional properties and why `string | null` is not the same as `?`, readonly and "
            "exactly how shallow it is, index signatures for genuinely open-ended objects, nested "
            "shapes, and excess property checks — the rule that rejects an extra key on a literal "
            "but waves the same object through when it arrives in a variable."
        ),
    },
    {
        "slug": "typescript-interfaces-vs-type-aliases",
        "title": "TypeScript – Interfaces vs Type Aliases",
        "tags": ["typescript", "interface", "types"],
        "excerpt": (
            "They overlap almost completely, which is why the question keeps coming up. The three "
            "real differences — declaration merging, what each can name, and the error messages "
            "you get back — and the rule this app follows: interface for a shape with a name, "
            "type for everything a shape cannot express."
        ),
    },
    {
        "slug": "typescript-union-and-intersection-types",
        "title": "TypeScript – Unions and Intersections",
        "tags": ["typescript", "types"],
        "excerpt": (
            "A union is a value that is one of these; an intersection is a value that is all of "
            "these at once. Why you can only reach the members a union has in common, why an "
            "intersection of two conflicting properties gives you never rather than an error, and "
            "how a union of string literals replaces a validation function."
        ),
    },
    {
        "slug": "typescript-enums",
        "title": "TypeScript – Enums, and What to Use Instead",
        "tags": ["typescript", "enum", "types"],
        "excerpt": (
            "TypeScript's enum is the one feature in the language that emits runtime JavaScript, "
            "and everything awkward about it follows from that: reverse mappings that put numbers "
            "in your object, const enum breaking under isolatedModules, and a build flag that "
            "rejects it outright. Then the `as const` object this app uses in both halves instead."
        ),
    },
    {
        "slug": "typescript-narrowing",
        "title": "TypeScript – Narrowing and Type Guards",
        "tags": ["typescript", "types", "narrowing"],
        "excerpt": (
            "Narrowing is what makes unions usable: typeof, instanceof, the in operator, truthiness "
            "and equality all teach the checker something. Then the two you write yourself — a "
            "predicate returning `x is Thing`, and the discriminated union — plus the never trick "
            "that turns a forgotten case into a build failure instead of a blank badge."
        ),
    },
    # ----------------------------------------------------- behaviour
    {
        "slug": "typescript-functions",
        "title": "TypeScript – Functions",
        "tags": ["typescript", "functions"],
        "excerpt": (
            "Parameter and return types, optional and default and rest parameters, and the "
            "function type itself — the thing you annotate a callback with. Then overloads, when "
            "one signature genuinely cannot describe two call shapes, and why a union return type "
            "is usually the better answer than a second overload."
        ),
    },
    {
        "slug": "typescript-classes",
        "title": "TypeScript – Classes",
        "tags": ["typescript", "classes", "oop"],
        "excerpt": (
            "public, private and protected, and why TypeScript's private is a compile-time promise "
            "while #private is a runtime one. readonly, parameter properties and the build flag "
            "that bans them, abstract classes, implements versus extends, and subclassing Error "
            "so the UI can tell a rejected write from a server that fell over."
        ),
    },
    {
        "slug": "typescript-generics",
        "title": "TypeScript – Generics",
        "tags": ["typescript", "generics"],
        "excerpt": (
            "A generic is a function's type argument, and the point is preserving a relationship "
            "the checker would otherwise lose. Constraints with extends, defaults, generic "
            "interfaces and classes, and the rule for when NOT to reach for one — with a data "
            "loading hook that would return `any` without them."
        ),
    },
    {
        "slug": "typescript-utility-types",
        "title": "TypeScript – The Utility Types Worth Knowing",
        "tags": ["typescript", "types", "utility-types"],
        "excerpt": (
            "Partial, Required, Readonly, Pick, Omit, Record, Exclude, Extract, NonNullable, "
            "ReturnType and Awaited — what each one is for, in the order you will actually need "
            "them. Including the Record in this app that turns adding a status to a union into a "
            "build error until somebody writes the label for it."
        ),
    },
    {
        "slug": "typescript-mapped-and-conditional-types",
        "title": "TypeScript – keyof, Mapped and Conditional Types",
        "tags": ["typescript", "types", "advanced"],
        "excerpt": (
            "The machinery the utility types are built from. keyof and typeof and what they mean "
            "together, indexed access, mapped types with their modifiers, conditional types and "
            "infer. Ending with the expression this app uses in two files — "
            "`(typeof UserRole)[keyof typeof UserRole]` — read one piece at a time."
        ),
    },
    {
        "slug": "typescript-type-assertions",
        "title": "TypeScript – Assertions, as const and satisfies",
        "tags": ["typescript", "types"],
        "excerpt": (
            "`as` is you overruling the checker, and it is the one construct here that can make a "
            "program crash. When it is legitimate, the double-assertion escape hatch and why "
            "needing it is a warning, non-null `!`, and then `satisfies` — the operator that "
            "checks a value against a type without widening it, which is what you usually wanted."
        ),
    },
    # ----------------------------------------------------- real projects
    {
        "slug": "typescript-modules",
        "title": "TypeScript – Modules and Type-Only Imports",
        "tags": ["typescript", "modules", "esm"],
        "excerpt": (
            "import type and why a bundler needs you to say it, verbatimModuleSyntax, and the "
            "reason the NestJS half of this app writes `.js` in an import that points at a `.ts` "
            "file. Module resolution in one page, declaration files, and what to do about a "
            "package that ships no types."
        ),
    },
    {
        "slug": "typescript-tsconfig",
        "title": "TypeScript – tsconfig, the Flags That Matter",
        "tags": ["typescript", "tsconfig"],
        "excerpt": (
            "Most of tsconfig you set once. These are the ones that change what compiles: the "
            "strict family one flag at a time, target and lib and how they differ, "
            "moduleResolution, noEmit, erasableSyntaxOnly, and path aliases. Read off the two real "
            "configs in this app — which disagree with each other, correctly."
        ),
    },
    {
        "slug": "typescript-decorators",
        "title": "TypeScript – Decorators",
        "tags": ["typescript", "decorators", "nestjs"],
        "excerpt": (
            "A decorator is a function that runs when the class is defined. What @Injectable, "
            "@Column and @Post are really doing, the metadata reflection that lets a framework "
            "read your parameter types at runtime, writing your own, and the split between the "
            "legacy experimentalDecorators and the standard ones — with which this app uses."
        ),
    },
    {
        "slug": "typescript-with-react",
        "title": "TypeScript – With React",
        "tags": ["typescript", "react"],
        "excerpt": (
            "Typing props and children, useState where inference is enough and where it is not, "
            "useRef's two different types, event handlers, and generic components. Plus the "
            "context pattern that removes the `| undefined` every consumer would otherwise have to "
            "handle, taken from this app's auth provider."
        ),
    },
    {
        "slug": "typescript-interview-questions",
        "title": "TypeScript – Interview Questions",
        "tags": ["typescript", "interview"],
        "excerpt": (
            "The questions a TypeScript role actually asks, answered against the twenty lessons "
            "before this one. any versus unknown, interface versus type, why enum is contentious, "
            "what structural typing means in practice, how narrowing works, what erases at build "
            "time and what does not. Short answers, with the reasoning behind them."
        ),
    },
]

# Slug -> filename, and the dates, are derived so a reorder is one edit.
POSTS = [
    {
        "slug": entry["slug"],
        "title": entry["title"],
        "file": f"{i + 1:02d}-{entry['slug']}.html",
        "date": _date(i),
        "tags": entry["tags"],
        "excerpt": entry["excerpt"],
    }
    for i, entry in enumerate(_TRACK)
]

# Nothing is frozen: this category does not exist on the live site yet, so no slug here is an
# indexed URL. Kept as an empty set rather than deleted so seed.py's guard stays wired up — the
# day a typescript post is published outside this track, adding it here is the whole fix.
FROZEN_SLUGS: set[str] = set()

NEW_SLUGS = {e["slug"] for e in _TRACK}

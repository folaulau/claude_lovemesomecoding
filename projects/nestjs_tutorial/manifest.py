"""The NestJS track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend
with the track and lesson 20 is the newest.

**Every slug here is new.** There is no `nestjs` category in the content DB (checked 2026-09-05
against the 43 in `content/index/categories.json`), so no indexed URL is at risk and `seed.py`
never needs `--force-dates`. If that ever stops being true — if a `nestjs` post is published by
hand before this track seeds — add it to FROZEN_SLUGS and the seed guard starts protecting it.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, so re-basing the whole
track is one edit.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "nestjs",
    "name": "NestJS",
    "description": (
        "NestJS from your first controller to an API you would put in front of real users — "
        "modules and dependency injection, then the request pipeline in the order it actually "
        "runs: pipes, guards, interceptors, middleware and exception filters. Then the parts a "
        "real service needs: typed configuration, TypeORM with transactions, JWT authentication, "
        "role-based authorization, uploads and tests. Every example is lifted from a working "
        "contractor marketplace API, so code in these posts is code that runs."
    ),
}

# Where the category sits in the site navigation.
#
# ⚠️ A REAL TASK, not a note. `nestjs` is a brand-new slug, so it does not appear in
# lovemesomecoding_frontend/src/lib/nav.ts at all and the JavaScript dropdown will not show it
# however many times this track is seeded. `navTree()` filters against `allCategories()`, so the
# entry is inert until the category exists — add both. See progress_report.md.
NAV_GROUP = "JavaScript"

# ---------------------------------------------------------------------------
# The app every code sample is taken from
# ---------------------------------------------------------------------------
# The contractor marketplace, named by the README:
#     "Use this project …/contractor/contractor-nestjs-backend to provide examples"
#
# ⚠️ The TypeScript track REJECTED this same app on 2026-09-05 and used pizza instead. That was
# correct then and does not apply now. The objection was CHURN — the whole source tree appeared
# inside one 35-minute window and `api/client.ts` was split and restored twenty seconds before the
# check ran. Re-checked before this track started: nothing in the tree had moved for seven hours,
# and `npx tsc --noEmit` exits 0.
#
# (It is not committed, and never will be: `lovemesomecoding_demo_project` is in .gitignore line
# 14. `git status` calling it untracked was never evidence of anything.)
DEMO_APP = "lovemesomecoding_demo_project/contractor"
BE = "contractor-nestjs-backend"

# ---------------------------------------------------------------------------
# What this track ADDED to the app
# ---------------------------------------------------------------------------
# README, updated 2026-09-05: "add to the project if a teaching material is not there yet but make
# sure the project still runs."
#
# The app already had modules, controllers, providers, DTOs behind a global ValidationPipe, two
# guards, a param decorator, SetMetadata + Reflector, TypeORM, config, JWT and file upload. It had
# no middleware, no filter, no interceptor of its own, no custom pipe and no unit tests.
#
# ⚠️ Every addition had to be something the app SHOULD HAVE HAD, not a demo bolted on for a
# lesson. Two of them fixed real defects:
#   - the filter turns a `QueryFailedError` into a 409 instead of the bare 500 that
#     `uq_one_accepted_quote_per_project` used to produce;
#   - the pipe fixes `@Length(1, 80)` passing three spaces that the service then stored as "".
#
# Gates after the change: tsc exit 0, `nest build` exit 0, `npm test` 17 passed (was: no test files
# at all), `npm run test:e2e` 19 passed with no assertion edited. Then run for real and exercised
# with curl. See progress_report.md for the table.
ADDED_FOR_THIS_TRACK = [
    f"{BE}/src/common/middleware/request-id.middleware.ts",
    f"{BE}/src/common/interceptors/logging.interceptor.ts",
    f"{BE}/src/common/filters/all-exceptions.filter.ts",
    f"{BE}/src/common/pipes/trim.pipe.ts",
    f"{BE}/src/common/pipes/trim.pipe.spec.ts",
    f"{BE}/src/common/guards/roles.guard.spec.ts",
    f"{BE}/src/auth/auth.service.spec.ts",
]

# ---------------------------------------------------------------------------
# Versions — READ OFF THIS MACHINE, not chosen
# ---------------------------------------------------------------------------
# `node --version`, `npx tsc --version`, and the installed package.json versions under
# node_modules, 2026-09-05.
VERSIONS = {
    "@nestjs/core": "12.0.1",
    "@nestjs/common": "12.0.1",
    "@nestjs/typeorm": "12.0.1",
    "typeorm": "1.1.1",
    "class-validator": "0.15.1",
    "typescript": "6.0.3",
    "node": "22.23.2",
    "vitest": "4.1.11",
    "postgres": "16-alpine",
}

# ⚠️ The single most important thing to say about this codebase, and it is said in lesson 2 and
# then never quietly dropped: the Nest scaffold is ESM. `"type": "module"` with
# `moduleResolution: nodenext` means EVERY relative import carries a `.js` extension even though
# the file next to it is `.ts` — the specifier has to name the file that exists at RUNTIME.
#
# Leave it off and it compiles fine, then dies at startup with ERR_MODULE_NOT_FOUND. Every snippet
# in this track keeps the extension, because a reader copying one out is the person this bites.
ESM_NOTE = True

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together, then
# `readingMinutes = max(1, round(words / 220))`. See lovemesomecoding_backend/app/services/
# content.py. Budgeting prose alone silently doubles the published reading time.
#
# Folau asked for 8-10 reading-minutes (2026-09-05), the same budget as the TypeScript track.
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (8, 10)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 1,760
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 2,200

# ⚠️ 40%, LOWER than the TypeScript track's 45%, and the difference is not sloppiness.
#
# A language tutorial's snippets are three lines demonstrating one rule, so when code takes over
# the word count there it means the post has become a syntax reference with captions. A FRAMEWORK
# tutorial legitimately quotes a whole guard, a whole module, a whole DTO — the shape of the file
# IS the lesson, and cutting it to fragments to protect a ratio would make the post worse.
#
# 40% still bites: it is roughly "for every line of code, a line about it", which is the floor
# below which a post is a tour of a repository rather than an explanation of one.
MIN_PROSE_SHARE = 0.40

# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------
# 20 posts, 3 days apart, landing the last one on 2026-09-05.
START_DATE = datetime(2026, 7, 10, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=index * STEP_DAYS)).strftime("%Y-%m-%dT%H:%M:%S")


# ---------------------------------------------------------------------------
# Slugs that already exist and must be rewritten in place, never re-minted
# ---------------------------------------------------------------------------
# Empty, and correct: nothing is published under /nestjs. Kept wired up because the day somebody
# publishes a nestjs post by hand, adding the slug here is the whole fix.
FROZEN_SLUGS: set[str] = set()

# ---------------------------------------------------------------------------
# Which files each post is allowed to quote
# ---------------------------------------------------------------------------
# Paths are relative to DEMO_APP. check_snippets.py checks a post's blocks against THESE files
# first, and reports a block that matches the app but not the declared list — a snippet that has
# drifted in from an unrelated module is a finding, not a pass.
SNIPPET_SOURCES = {
    "nestjs-get-started": [
        f"{BE}/package.json", f"{BE}/src/app.module.ts",
        f"{BE}/src/auth/auth.controller.ts", f"{BE}/src/common/enums.ts",
    ],
    "nestjs-project-setup": [
        f"{BE}/package.json", f"{BE}/tsconfig.json", f"{BE}/tsconfig.build.json",
        f"{BE}/nest-cli.json", f"{BE}/src/main.ts", f"{BE}/.env.example",
        f"{BE}/src/database/entities/user.entity.ts",
    ],
    "nestjs-modules": [
        f"{BE}/src/app.module.ts", f"{BE}/src/auth/auth.module.ts",
        f"{BE}/src/projects/projects.module.ts", f"{BE}/src/quotes/quotes.module.ts",
    ],
    "nestjs-controllers": [
        f"{BE}/src/auth/auth.controller.ts", f"{BE}/src/projects/projects.controller.ts",
        f"{BE}/src/contractors/contractors.controller.ts",
        f"{BE}/src/quotes/quotes.controller.ts",
    ],
    "nestjs-providers-and-dependency-injection": [
        f"{BE}/src/auth/auth.service.ts", f"{BE}/src/auth/auth.module.ts",
        f"{BE}/src/projects/projects.module.ts", f"{BE}/src/quotes/quotes.service.ts",
        f"{BE}/src/app.module.ts",
    ],
    "nestjs-dtos-and-validation": [
        f"{BE}/src/auth/dto/auth.dto.ts", f"{BE}/src/projects/dto/project.dto.ts",
        f"{BE}/src/main.ts", f"{BE}/src/common/serializers.ts",
    ],
    "nestjs-pipes": [
        f"{BE}/src/common/pipes/trim.pipe.ts", f"{BE}/src/main.ts",
        f"{BE}/src/projects/projects.controller.ts", f"{BE}/src/projects/dto/project.dto.ts",
    ],
    "nestjs-guards": [
        f"{BE}/src/common/guards/jwt-auth.guard.ts", f"{BE}/src/common/guards/roles.guard.ts",
        f"{BE}/src/projects/projects.controller.ts",
        f"{BE}/src/contractors/contractors.controller.ts",
    ],
    "nestjs-custom-decorators": [
        f"{BE}/src/common/decorators/current-user.decorator.ts",
        f"{BE}/src/common/decorators/roles.decorator.ts",
        f"{BE}/src/common/guards/roles.guard.ts", f"{BE}/src/auth/auth.controller.ts",
    ],
    "nestjs-interceptors": [
        f"{BE}/src/common/interceptors/logging.interceptor.ts", f"{BE}/src/app.module.ts",
        f"{BE}/src/contractors/contractors.controller.ts",
    ],
    "nestjs-middleware": [
        f"{BE}/src/common/middleware/request-id.middleware.ts", f"{BE}/src/app.module.ts",
        f"{BE}/src/common/interceptors/logging.interceptor.ts",
    ],
    "nestjs-exception-filters": [
        f"{BE}/src/common/filters/all-exceptions.filter.ts", f"{BE}/src/app.module.ts",
        f"{BE}/src/quotes/quotes.service.ts", f"{BE}/src/projects/projects.service.ts",
    ],
    "nestjs-request-lifecycle": [
        f"{BE}/src/app.module.ts", f"{BE}/src/main.ts",
        f"{BE}/src/common/middleware/request-id.middleware.ts",
        f"{BE}/src/common/interceptors/logging.interceptor.ts",
        f"{BE}/src/common/guards/jwt-auth.guard.ts",
        f"{BE}/src/common/pipes/trim.pipe.ts",
        f"{BE}/src/common/filters/all-exceptions.filter.ts",
        f"{BE}/src/projects/projects.controller.ts",
    ],
    "nestjs-configuration": [
        f"{BE}/src/config/configuration.ts", f"{BE}/src/app.module.ts",
        f"{BE}/src/auth/auth.module.ts", f"{BE}/src/main.ts", f"{BE}/.env.example",
    ],
    "nestjs-database-typeorm": [
        f"{BE}/src/database/entities/base.entity.ts",
        f"{BE}/src/database/entities/user.entity.ts",
        f"{BE}/src/database/data-source.ts", f"{BE}/src/app.module.ts",
        f"{BE}/src/projects/projects.service.ts", f"{BE}/src/projects/projects.module.ts",
        f"{BE}/package.json",
    ],
    "nestjs-authentication-jwt": [
        f"{BE}/src/auth/auth.service.ts", f"{BE}/src/auth/jwt-payload.ts",
        f"{BE}/src/auth/auth.module.ts", f"{BE}/src/common/guards/jwt-auth.guard.ts",
        f"{BE}/src/auth/auth.controller.ts",
    ],
    "nestjs-authorization-roles": [
        f"{BE}/src/common/decorators/roles.decorator.ts",
        f"{BE}/src/common/guards/roles.guard.ts", f"{BE}/src/common/enums.ts",
        f"{BE}/src/projects/projects.controller.ts", f"{BE}/src/projects/projects.service.ts",
        f"{BE}/src/auth/dto/auth.dto.ts",
    ],
    "nestjs-file-upload": [
        f"{BE}/src/contractors/contractors.controller.ts",
        f"{BE}/src/contractors/contractors.service.ts",
        f"{BE}/src/contractors/image-validation.ts", f"{BE}/src/main.ts",
    ],
    "nestjs-testing": [
        f"{BE}/src/common/pipes/trim.pipe.spec.ts", f"{BE}/src/common/guards/roles.guard.spec.ts",
        f"{BE}/src/auth/auth.service.spec.ts", f"{BE}/test/rules.e2e-spec.ts",
        f"{BE}/vitest.config.ts", f"{BE}/package.json",
    ],
    "nestjs-interview-questions": [
        f"{BE}/src/app.module.ts", f"{BE}/src/common/guards/roles.guard.ts",
        f"{BE}/src/common/middleware/request-id.middleware.ts",
        f"{BE}/src/common/interceptors/logging.interceptor.ts",
        f"{BE}/src/auth/auth.module.ts", f"{BE}/src/main.ts",
    ],
}

# A section deliberately showing the WRONG way. check_snippets.py excludes blocks near this marker
# from the "must match the app" rule, because not matching is the entire point of them.
#
# ⚠️ A framework track needs this LESS than the TypeScript track did and uses it differently.
# There, half of teaching a type system was showing code the compiler rejects, and none of it
# could live in the app. Here almost every block is quoted from a file that runs — so a block that
# does not match is a stale quote unless it is explicitly marked, and the marker is rare on
# purpose. Where it appears it is nearly always the same shape: the plausible version of something
# the app deliberately does not do (`decode` instead of `verifyAsync`, `origin: true`, the guards
# in the wrong order).
ANTIPATTERN_MARKER = "the wrong way"

# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
_TRACK = [
    # ------------------------------------------------------------ foundations
    {
        "slug": "nestjs-get-started",
        "title": "NestJS – Get Started",
        "tags": ["nestjs", "typescript", "nodejs"],
        "excerpt": (
            "Start here. What NestJS actually is — a structure for a Node server, not a runtime — "
            "why it looks like Angular and Spring, when the structure earns its cost and when it "
            "does not, the exact versions this track is written against, the contractor "
            "marketplace API every example is taken from, and the full lesson index in reading "
            "order."
        ),
    },
    {
        "slug": "nestjs-project-setup",
        "title": "NestJS – Setting Up a Project",
        "tags": ["nestjs", "typescript", "nodejs"],
        "excerpt": (
            "Creating a project with the Nest CLI, what each generated file is for, and the "
            "tsconfig flags Nest actually needs — experimentalDecorators and "
            "emitDecoratorMetadata are not style settings, they are what makes injection work. "
            "Plus the ESM trap that costs everyone an afternoon: why every relative import in "
            "this codebase ends in .js even though the file is .ts."
        ),
    },
    {
        "slug": "nestjs-modules",
        "title": "NestJS – Modules",
        "tags": ["nestjs", "typescript", "architecture"],
        "excerpt": (
            "The unit Nest is organised around. What imports, providers, controllers and exports "
            "each mean, why a provider is private to its module until you export it, when "
            "@Global() is right and why it is used exactly once in this app, and how "
            "forRoot/forFeature dynamic modules differ from ordinary ones."
        ),
    },
    {
        "slug": "nestjs-controllers",
        "title": "NestJS – Controllers",
        "tags": ["nestjs", "typescript", "rest-api"],
        "excerpt": (
            "Routing, and the line between HTTP and everything else. Route decorators, @Body, "
            "@Param and @Query, why POST answers 201 by default and when that is wrong, choosing "
            "204 over an empty 200, and the rule that keeps controllers thin — a controller that "
            "decides who may do something is in the wrong layer."
        ),
    },
    {
        "slug": "nestjs-providers-and-dependency-injection",
        "title": "NestJS – Providers and Dependency Injection",
        "tags": ["nestjs", "typescript", "architecture"],
        "excerpt": (
            "How Nest builds your object graph. @Injectable, constructor injection and what the "
            "emitted metadata is actually doing, provider tokens beyond the class — useValue, "
            "useFactory and useClass, why an async factory is the only way to configure a module "
            "from config, injection scopes and the reason singletons are the right default."
        ),
    },
    # ------------------------------------------------------ the request pipeline
    {
        "slug": "nestjs-dtos-and-validation",
        "title": "NestJS – DTOs and Validation",
        "tags": ["nestjs", "typescript", "validation"],
        "excerpt": (
            "class-validator, the global ValidationPipe, and the failure mode that ships more "
            "often than any other in Nest: an app with beautifully annotated DTOs and no global "
            "pipe is completely unvalidated, and nothing about it looks wrong. Plus whitelist, "
            "forbidNonWhitelisted, and why the response DTO is a separate idea from the request "
            "one."
        ),
    },
    {
        "slug": "nestjs-pipes",
        "title": "NestJS – Pipes",
        "tags": ["nestjs", "typescript", "validation"],
        "excerpt": (
            "What a pipe is — transform, validate, or both — the built-in ones worth knowing, and "
            "writing your own PipeTransform. Built around a real bug this app had: @Length(1, 80) "
            "happily passed three spaces that the service then stored as an empty string, because "
            "the validator and the service disagreed about what the value was."
        ),
    },
    {
        "slug": "nestjs-guards",
        "title": "NestJS – Guards",
        "tags": ["nestjs", "typescript", "security"],
        "excerpt": (
            "CanActivate, and the one question a guard answers: may this request proceed? A real "
            "JWT guard in about thirty lines, why verifyAsync and never decode, why guard order "
            "in @UseGuards is load-bearing, and where a guard stops being the right tool — the "
            "check that needs to read the row belongs in the service."
        ),
    },
    {
        "slug": "nestjs-custom-decorators",
        "title": "NestJS – Custom Decorators",
        "tags": ["nestjs", "typescript", "architecture"],
        "excerpt": (
            "The two kinds worth writing. createParamDecorator for pulling the current user out "
            "of a request, and SetMetadata plus Reflector for attaching data to a route that a "
            "guard reads back — the indirection that lets one guard serve every controller "
            "instead of each one writing its own check."
        ),
    },
    {
        "slug": "nestjs-interceptors",
        "title": "NestJS – Interceptors",
        "tags": ["nestjs", "typescript", "architecture"],
        "excerpt": (
            "The only part of the pipeline that sees both sides of a request. Wrapping a handler "
            "in an RxJS stream, why tap and not map when you are only observing, logging an "
            "outcome you cannot get from middleware, and the three ways to bind one — including "
            "the provider token that makes globals injectable and testable."
        ),
    },
    {
        "slug": "nestjs-middleware",
        "title": "NestJS – Middleware",
        "tags": ["nestjs", "typescript", "architecture"],
        "excerpt": (
            "The outermost layer, and the only one that is not really Nest — it is Express, with "
            "a class around it. What that buys and what it costs, why there is no APP_MIDDLEWARE "
            "token, and the question that decides between middleware and an interceptor: does "
            "this need to run even when a guard rejects the request?"
        ),
    },
    {
        "slug": "nestjs-exception-filters",
        "title": "NestJS – Exception Filters",
        "tags": ["nestjs", "typescript", "error-handling"],
        "excerpt": (
            "HttpException and the built-in subclasses, throwing from a service without importing "
            "anything HTTP-shaped, and writing a @Catch() filter that turns a database constraint "
            "violation into a 409 instead of the bare 500 it would otherwise be. Plus the rule "
            "that keeps a filter from being a breaking change: add to the body, never reshape it."
        ),
    },
    {
        "slug": "nestjs-request-lifecycle",
        "title": "NestJS – The Request Lifecycle",
        "tags": ["nestjs", "typescript", "architecture"],
        "excerpt": (
            "The order everything runs in, traced through one real request from the contractor "
            "API. Middleware, guards, interceptors, pipes, the handler, then interceptors and "
            "filters on the way back out — and the practical consequences of that order, which "
            "is where most of the confusing bugs in a Nest app come from."
        ),
    },
    # -------------------------------------------------------- real applications
    {
        "slug": "nestjs-configuration",
        "title": "NestJS – Configuration",
        "tags": ["nestjs", "typescript", "configuration"],
        "excerpt": (
            "@nestjs/config, and why the useful pattern is not reading process.env through "
            "ConfigService but parsing every variable once into a typed object. Validating at "
            "startup so a bad value is an error that names it, isGlobal, getOrThrow, and "
            "registerAsync for the modules that need a value config has not produced yet."
        ),
    },
    {
        "slug": "nestjs-database-typeorm",
        "title": "NestJS – Databases with TypeORM",
        "tags": ["nestjs", "typescript", "typeorm", "postgres"],
        "excerpt": (
            "Entities, repositories, migrations and transactions. forRoot and forFeature, why "
            "synchronize must stay false, the column types that bite — bigint and numeric come "
            "back as strings — and a real transaction with a pessimistic row lock, which is the "
            "reason this app's writes go through NestJS rather than through a generated mutation."
        ),
    },
    {
        "slug": "nestjs-authentication-jwt",
        "title": "NestJS – Authentication with JWT",
        "tags": ["nestjs", "typescript", "security", "jwt"],
        "excerpt": (
            "Register and login end to end: bcrypt with a cost that is slow on purpose, what goes "
            "in a token and what must never, signing with @nestjs/jwt, and the two defences that "
            "keep a login form from confirming which addresses are registered — one message for "
            "every failure, and a dummy hash comparison so they take the same time."
        ),
    },
    {
        "slug": "nestjs-authorization-roles",
        "title": "NestJS – Authorization and Roles",
        "tags": ["nestjs", "typescript", "security"],
        "excerpt": (
            "Role-based access with @Roles and a RolesGuard, and the harder half nobody shows: "
            "ownership. Why the role never comes from a request body, why a foreign resource "
            "returns 404 rather than 403, and why the route whose rules depend on the row "
            "deliberately has no @Roles decorator at all."
        ),
    },
    {
        "slug": "nestjs-file-upload",
        "title": "NestJS – File Upload",
        "tags": ["nestjs", "typescript", "security"],
        "excerpt": (
            "FileInterceptor and multer, and the fact that decides everything else about an "
            "upload endpoint: the Content-Type is whatever the client typed. Memory storage "
            "versus disk and why it is a security choice, stopping a 2 GB request at 5 MB, "
            "sniffing magic bytes, and generating the stored filename rather than sanitising one."
        ),
    },
    {
        "slug": "nestjs-testing",
        "title": "NestJS – Testing",
        "tags": ["nestjs", "typescript", "testing"],
        "excerpt": (
            "Test.createTestingModule, mocking a provider with useValue, and getting the token "
            "right — @InjectDataSource does not ask for the class, so overriding the class leaves "
            "your test talking to the real database. Then e2e with supertest, and the trap that "
            "makes a whole suite pass vacuously: forgetting the global pipe."
        ),
    },
    {
        "slug": "nestjs-interview-questions",
        "title": "NestJS – Interview Questions",
        "tags": ["nestjs", "typescript", "interview"],
        "excerpt": (
            "The questions that actually get asked, with answers drawn from the nineteen lessons "
            "before this one — module scope and why a provider is not global, guards versus "
            "middleware versus interceptors, how Nest resolves a dependency, why the global "
            "ValidationPipe matters, and what happens to an exception on its way out."
        ),
    },
]

POSTS = [
    {**entry, "file": f"{index + 1:02d}-{entry['slug']}.html", "date": _date(index)}
    for index, entry in enumerate(_TRACK)
]

# Every slug in this track is new. Kept as its own name because seed.py's collision guard reads it
# — a slug marked new that already exists in ANOTHER category would be an accidental overwrite,
# since post slugs are global across the site.
NEW_SLUGS = {entry["slug"] for entry in POSTS} - FROZEN_SLUGS

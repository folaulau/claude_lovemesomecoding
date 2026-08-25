"""The FastAPI track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend
with the track and the last lesson is the newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because this track is
authored before it is published: when the publish date is finally known, move START_DATE and every
lesson re-bases in order.

⚠️ NINE of these nineteen slugs are not new. The whole /fastapi collection was published in June
2023 and every one of its URLs is indexed. They are being rewritten IN PLACE, not replaced:
changing one of those slugs changes a live URL, and `verify-build.mjs` fails the frontend build
when an indexed post URL stops resolving.

Because all nine carried 2023 dates and `upsert_post` never overwrites an existing date, seeding
needs `seed.py --force-dates` or the archive interleaves nine 2023 posts with nine 2025 ones and
the pager reads nonsense. The same applies to any later re-base of START_DATE: once a post is
published its stored date is sticky, so moving the whole track means --force-dates again. See
progress_report.md.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "fastapi",
    # ⚠️ The stored record currently says "fastapi" in lowercase with an EMPTY description.
    # upsert_category rewrites both from here, which is the only reason the archive page gets a
    # display name and a standfirst at all.
    "name": "FastAPI",
    "description": (
        "FastAPI from a first endpoint to something you can put in front of users — routing and "
        "validation, project structure, dependency injection, SQLAlchemy and migrations, auth, "
        "uploads, background work, middleware, testing, observability and Docker. Every example "
        "is taken from a real short-let booking API, and the performance claims are measured on "
        "the machine that wrote them rather than repeated."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself lives in
# lovemesomecoding_frontend/src/lib/nav.ts, which already lists `fastapi` under the Python group
# with the display name "FastAPI" — nothing to add there.
NAV_GROUP = "Python"

# The app every code sample is taken from.
DEMO_APP = "lovemesomecoding_demo_project/stayhub/stayhub-fastapi-backend"

# ---------------------------------------------------------------------------
# Versions — READ OFF THIS MACHINE, not chosen
# ---------------------------------------------------------------------------
# `pip show`, `python -V`, `docker --version`, `postgres --version`, taken while the StayHub
# stack was up and its 100 tests passing.
VERSIONS = {
    "python": "3.12.4",
    "fastapi": "0.115.5",
    "starlette": "0.41.3",
    "pydantic": "2.10.3",
    "pydantic-settings": "2.6.1",
    "sqlalchemy": "2.0.36 (installed as SQLAlchemy[asyncio] — see below)",
    "alembic": "1.14.0",
    "uvicorn": "0.32.1 ([standard] extra)",
    "psycopg": "3.2.3 ([binary] extra)",
    "postgres": "16.15",
    "docker engine": "27.4.0",
    "host": "Docker Desktop on aarch64 (Apple Silicon)",
}

# ---------------------------------------------------------------------------
# Length budget — the whole point of this rewrite
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together, then
# `readingMinutes = max(1, round(words / 220))`. See lovemesomecoding_backend/app/services/
# content.py:161. Budgeting prose alone silently doubles the published reading time.
#
# Folau asked for 15-20 reading-minutes, so:
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (15, 20)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 3,300
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 4,400

# ⚠️ AND a floor on the prose share, which matters more than the cap.
#
# Measured across the nine live posts on 2026-08-21: CODE IS 75% OF THE COUNTED WORDS.
# `fastapi-testing` carries 10,647 words of code against 1,383 of prose — 7.7 to 1. These posts
# are not wordy; they are code dumps with captions, and a total-words cap alone would be satisfied
# by a shorter code dump.
#
# 40% is the floor, not the goal. A lesson should read as an explanation illustrated by code, not
# a listing with commentary.
MIN_PROSE_SHARE = 0.40

# What the collection looks like TODAY, measured off the prod tree on 2026-08-21. This is the
# baseline the rewrite has to beat, and check_content.py reports against it.
EXISTING = {
    #                                        prose,   code,  total, minutes
    "fastapi-testing":                      (1383, 10647, 12030, 55),
    "fastapi-authentication-authorization": (2540,  9074, 11614, 53),
    "fastapi-database-integration":         (2293,  8605, 10898, 50),
    "fastapi-rest-api":                     (2592,  8191, 10783, 49),
    "fastapi-pydantic-models-validation":   (1427,  8088,  9515, 43),
    "fastapi-introduction":                 (4657,  4097,  8754, 40),
    "fastapi-routes-request-handling":      (1629,  6303,  7932, 36),
    "fastapi-deployment":                   (1965,  5348,  7313, 33),
    "fastapi-interview-questions":          (2814,  4231,  7045, 32),
}

# ---------------------------------------------------------------------------
# Measured facts — quoted by posts, held here so they cannot drift
# ---------------------------------------------------------------------------
# Every number a post states about performance or the container comes from this block. Written
# down once because a figure repeated in prose in three posts is a figure that disagrees with
# itself within a month, and because check_content.py can then assert a post that CLAIMS a
# measurement quotes one of these.
MEASURED = {
    # scripts/bench_stats.py, 30 runs each after warm-up, 2026-08-21.
    "stats_sync_median_ms": 7.9,
    "stats_async_median_ms": 19.8,
    # 8 queries, median of 7 runs, varying only per-query wait via pg_sleep.
    # (wait_ms, sync_serial_ms, async_gather_ms)
    "async_crossover": [
        (0, 4.0, 15.5),
        (5, 59.1, 22.2),
        (50, 444.9, 76.2),
        (200, 1654.7, 232.9),
    ],
    "async_breakeven_ms": "1-2ms of wait per call",
    # `docker build` + `docker images` + `docker run`, 2026-08-21.
    "image_size": "304MB",
    "image_user": "stayhub (non-root)",
    "build_seconds": 45,
    # pytest -q, before and after this track's app work.
    "tests_before": 58,
    "tests_after": 100,
}

# ---------------------------------------------------------------------------
# Snippet sources
# ---------------------------------------------------------------------------
# Which StayHub files each post is allowed to quote. check_snippets.py reads these and verifies
# that the python blocks in a post actually appear in the named source.
#
# ⚠️ This is the rule that separates this track from the nine posts it replaces. Those quote
# invented `Product` and `Order` models that exist nowhere. Every python block here must be
# traceable to a file that runs and is covered by the 100-test suite.
#
# The one exception is a block deliberately showing the WRONG way — those carry
# `class="language-python"` inside a section flagged by ANTIPATTERN_MARKER and are excluded.
ANTIPATTERN_MARKER = "data-antipattern"

SNIPPET_SOURCES = {
    "fastapi-introduction": ["app/main.py", "app/api/v1/routes/bookings.py"],
    "fastapi-routes-request-handling": [
        "app/api/v1/routes/properties.py", "app/api/v1/routes/search.py",
        "app/api/v1/routes/bookings.py", "app/api/v1/routes/payments.py",
        "app/api/v1/router.py", "app/core/deps.py", "app/schemas/booking.py",
        "app/main.py", "app/models/enums.py", "app/api/v1/routes/admin.py",
    ],
    "fastapi-pydantic-models-validation": [
        "app/schemas/common.py", "app/schemas/property.py", "app/schemas/booking.py",
        "app/api/v1/routes/properties.py", "app/services/booking_service.py",
    ],
    "fastapi-project-structure": [
        "app/main.py", "app/api/v1/router.py", "app/core/config.py",
        "app/repositories/base.py", "app/services/booking_service.py",
        "app/api/v1/routes/bookings.py", "app/models/booking.py",
        "tests/test_booking_service.py", "app/models/property.py",
        "app/models/enums.py", "app/services/pricing_service.py",
        "app/services/cancellation_policy.py", "app/api/v1/routes/admin.py",
    ],
    "fastapi-dependency-injection": [
        "app/core/deps.py", "app/db/session.py", "app/schemas/common.py",
        "tests/test_api_admin.py", "app/api/v1/routes/properties.py",
        "app/api/v1/routes/admin.py", "app/core/security.py",
        "app/db/async_session.py",
    ],
    "fastapi-database-integration": [
        "app/db/base.py", "app/db/session.py", "app/models/booking.py",
        "app/models/property.py", "app/repositories/base.py",
        "app/repositories/booking_repository.py", "alembic/env.py",
        "app/services/booking_service.py", "app/models/enums.py",
        "app/api/v1/routes/admin.py",
        "alembic/versions/73d982de7a7a_initial_schema.py",
    ],
    "fastapi-rest-api": [
        "app/api/v1/routes/properties.py", "app/api/v1/routes/admin.py",
        "app/schemas/common.py", "app/schemas/property.py",
        "tests/test_api_admin.py", "app/main.py", "app/api/v1/routes/search.py",
        "app/api/v1/routes/bookings.py", "app/schemas/search.py",
    ],
    "fastapi-error-handling": [
        "app/core/exceptions.py", "app/core/middleware.py",
        "tests/test_api_middleware.py", "app/services/booking_service.py",
        "app/schemas/common.py", "app/main.py", "app/api/v1/routes/search.py",
    ],
    "fastapi-authentication-authorization": [
        "app/core/security.py", "app/core/deps.py",
        "app/services/auth_service.py", "app/api/v1/routes/auth.py",
        "app/services/booking_service.py", "app/models/user.py",
        "tests/test_security.py", "tests/test_api_admin.py",
    ],
    "fastapi-file-uploads": [
        "app/api/v1/routes/uploads.py", "app/core/config.py",
        "tests/test_api_uploads.py", "app/models/property.py",
    ],
    "fastapi-background-tasks": [
        "app/services/notification_service.py", "app/api/v1/routes/bookings.py",
        "app/api/v1/routes/admin.py",
    ],
    "fastapi-async-vs-sync": [
        "app/db/async_session.py", "app/api/v1/routes/admin.py",
        "app/api/v1/routes/uploads.py", "scripts/bench_stats.py", "requirements.txt",
    ],
    "fastapi-middleware-cors": [
        "app/core/middleware.py", "app/main.py", "tests/test_api_middleware.py",
        "app/core/logging.py", "app/core/config.py",
    ],
    "fastapi-testing": [
        "tests/conftest.py", "tests/test_api_admin.py", "tests/test_api_middleware.py",
        "tests/test_booking_service.py", "pytest.ini", "app/core/logging.py",
        "tests/test_api_uploads.py", "app/core/config.py", "app/main.py",
        "app/services/notification_service.py",
    ],
    "fastapi-observability": [
        "app/core/logging.py", "app/core/middleware.py", "app/main.py",
        "app/core/config.py", "app/api/v1/routes/uploads.py", "app/db/session.py",
    ],
    "fastapi-docker": ["Dockerfile", ".dockerignore", "requirements.txt"],
    "fastapi-deployment": ["Dockerfile", "app/core/config.py", "app/main.py",
                           "app/core/security.py"],
    # Quotes across the whole track by design. Listed anyway so the blocks that ARE verbatim get
    # checked; the deliberately-wrong "what is wrong with this?" blocks carry ANTIPATTERN_MARKER
    # and are excluded.
    "fastapi-oauth2": [
        "app/core/oauth.py", "app/services/oauth_service.py",
        "app/api/v1/routes/oauth.py", "app/api/v1/routes/auth.py",
        "app/models/oauth_account.py", "app/core/deps.py", "tests/test_oauth.py",
    ],
    "fastapi-interview-questions": [
        "app/api/v1/routes/admin.py", "app/core/deps.py", "app/schemas/common.py",
        "tests/test_api_admin.py",
    ],
}

# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later, so the archive
# reads as a course rather than a pile.
START_DATE = datetime(2025, 9, 2, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=STEP_DAYS * index)).strftime("%Y-%m-%dT%H:%M:%S")


# Authored in reading order. `state` is documentation, not data: "rewrite" means the slug already
# exists on the live site and must not change.
_TRACK = [
    # -------------------------------------------------------------- foundations
    {
        "slug": "fastapi-introduction",
        "title": "FastAPI – What It Is and Why It Exists",
        "state": "rewrite",
        "tags": ["fastapi", "python"],
        "excerpt": (
            "Start here. What FastAPI actually gives you — validation, serialisation and "
            "OpenAPI docs derived from ordinary type hints — and what it does not. Installing "
            "it, a first endpoint, what /docs is really reading, and how a request travels "
            "through the ASGI stack. Then the lesson index in reading order, the versions this "
            "track is written against, and the booking API every example is taken from."
        ),
    },
    {
        "slug": "fastapi-routes-request-handling",
        "title": "FastAPI – Routes, Parameters and Status Codes",
        "state": "rewrite",
        "tags": ["fastapi", "python", "rest"],
        "excerpt": (
            "Everything that turns an HTTP request into typed Python arguments. Path and query "
            "parameters, constraints with Query(), why Annotated is the form to learn, header "
            "and cookie parameters, choosing a status code, and splitting an API across routers "
            "with APIRouter. Including the repeated query parameter that needs no parsing, and "
            "the alias that lets a Python snake_case argument read as camelCase on the wire."
        ),
    },
    {
        "slug": "fastapi-pydantic-models-validation",
        "title": "FastAPI – Pydantic Models and Validation",
        "state": "rewrite",
        "tags": ["fastapi", "python", "pydantic"],
        "excerpt": (
            "Pydantic v2 as FastAPI actually uses it. Field constraints, field and model "
            "validators, computed fields for values that change at midnight, and separating the "
            "model you store from the model you return. Includes the snake_case-to-camelCase "
            "boundary that lets Python and TypeScript each keep their own conventions, and a "
            "field named `property` that breaks the `property` builtin twenty lines later."
        ),
    },
    # ---------------------------------------------------------------- structure
    {
        "slug": "fastapi-project-structure",
        "title": "FastAPI – Project Structure That Survives Growth",
        "state": "new",
        "tags": ["fastapi", "python", "architecture"],
        "excerpt": (
            "The question the official docs answer least well. How a single main.py becomes "
            "routes, services, repositories, schemas and models — what belongs in each layer, "
            "and the rules that keep them apart: routes own HTTP, services own the rules, and "
            "repositories never commit because only the caller knows where a transaction ends. "
            "Plus typed settings read once, so a misspelt variable is a startup error."
        ),
    },
    {
        "slug": "fastapi-dependency-injection",
        "title": "FastAPI – Dependency Injection in Practice",
        "state": "new",
        "tags": ["fastapi", "python", "testing"],
        "excerpt": (
            "The feature FastAPI is built on. Depends(), dependencies that yield so setup and "
            "teardown live together, sub-dependencies, and collapsing the whole thing into one "
            "readable Annotated alias so a route signature states its own security rules. Then "
            "dependency_overrides, which is what makes any of it testable — and the reason an "
            "override keyed on the wrong function object silently does nothing."
        ),
    },
    # ------------------------------------------------------------------ data
    {
        "slug": "fastapi-database-integration",
        "title": "FastAPI – SQLAlchemy, Sessions and Migrations",
        "state": "rewrite",
        "tags": ["fastapi", "python", "sqlalchemy", "postgres"],
        "excerpt": (
            "A real data layer. The engine and one session per request, typed SQLAlchemy 2.0 "
            "models, the repository pattern, and who owns the transaction. Then Alembic: naming "
            "constraints so a downgrade can refer to them, and never editing an applied "
            "migration. Includes the N+1 problem, eager loading, and why expire_on_commit=False "
            "matters specifically in FastAPI."
        ),
    },
    {
        "slug": "fastapi-rest-api",
        "title": "FastAPI – Designing the REST API",
        "state": "rewrite",
        "tags": ["fastapi", "python", "rest"],
        "excerpt": (
            "Turning endpoints into an API someone else can use. Resource naming, PATCH versus "
            "PUT, response_model and what it hides, and giving a state change its own endpoint "
            "instead of making it a writable field. Then pagination done properly — a generic "
            "Page[T] envelope, bounded page sizes, and the ORDER BY that stops page two "
            "repeating rows from page one."
        ),
    },
    {
        "slug": "fastapi-error-handling",
        "title": "FastAPI – One Error Shape for the Whole API",
        "state": "new",
        "tags": ["fastapi", "python"],
        "excerpt": (
            "Every failure leaving as the same JSON body, so a client needs one error parser. "
            "Custom exception classes raised from the service layer, handlers that turn them "
            "into responses, and flattening pydantic's nested validation errors into field "
            "messages a form can render. Plus the trap that cost this project a real bug: a "
            "handler registered for bare Exception does NOT run where the others do."
        ),
    },
    {
        "slug": "fastapi-authentication-authorization",
        "title": "FastAPI – Authentication and Authorization",
        "state": "rewrite",
        "tags": ["fastapi", "python", "security", "jwt"],
        "excerpt": (
            "Hashing passwords with bcrypt, issuing a JWT, and verifying it on every request. "
            "Then the half everyone skips: authorization as dependencies, so a route signature "
            "declares who may call it and the OpenAPI schema documents it for free. Includes "
            "why the user is re-read from the database each request, and why a foreign-owned "
            "resource returns 404 rather than 403."
        ),
    },
    # ------------------------------------------------------------ doing work
    {
        "slug": "fastapi-oauth2",
        "title": "FastAPI \u2013 OAuth2 and Sign in with Google",
        "state": "new",
        "tags": ["fastapi", "python", "oauth2", "security"],
        "excerpt": (
            "The authorization code flow with PKCE, built end to end: why OAuth2 is not a login "
            "protocol, what state actually defends against, and the one if statement that stands "
            "between a sign-in button and an account takeover. Plus the token endpoint that makes "
            "the Authorize button on /docs work, and how to test a flow that leaves your network."
        ),
    },
    {
        "slug": "fastapi-file-uploads",
        "title": "FastAPI – File Uploads Without the Holes",
        "state": "new",
        "tags": ["fastapi", "python", "security"],
        "excerpt": (
            "UploadFile, streamed in chunks rather than read into memory, with a size limit "
            "enforced during the write because there is no trustworthy length beforehand. Then "
            "the three guards an upload endpoint needs: content sniffed from the bytes rather "
            "than trusted from a header the client typed, a generated filename because "
            "\"../../app/main.py\" is a valid one, and no partial file left behind on failure."
        ),
    },
    {
        "slug": "fastapi-background-tasks",
        "title": "FastAPI – Background Tasks and Their Limits",
        "state": "new",
        "tags": ["fastapi", "python"],
        "excerpt": (
            "BackgroundTasks runs work after the response is sent, which is the entire feature. "
            "What that buys, what it emphatically is not — no retry, no persistence, no "
            "visibility — and when to reach for a real queue instead. Then the trap that makes "
            "it dangerous: a yield dependency closes BEFORE the task runs, so passing an ORM "
            "object half-works, and the half that fails is the half you add later."
        ),
    },
    {
        "slug": "fastapi-async-vs-sync",
        "title": "FastAPI – async def or def, and How to Tell",
        "state": "new",
        "tags": ["fastapi", "python", "performance"],
        "excerpt": (
            "The most consequential one-word decision in the framework. What FastAPI does with "
            "a def route versus an async def one, why a blocking call inside async def stalls "
            "every other request, and the threadpool that makes plain def safe. Then the same "
            "eight queries run serially and concurrently and MEASURED — where async wins by 86%, "
            "where it loses by 289%, and roughly where the line between them sits."
        ),
    },
    {
        "slug": "fastapi-middleware-cors",
        "title": "FastAPI – Middleware, Ordering and CORS",
        "state": "new",
        "tags": ["fastapi", "python"],
        "excerpt": (
            "Middleware for the things every request needs: a correlation id, a timing header, "
            "one access log line. Then ordering, which reads backwards — add_middleware inserts "
            "at the front, so the last call is the outermost layer. Getting that wrong shipped a "
            "real bug here: every 500 reached the browser without CORS headers, so the frontend "
            "reported a CORS failure and never saw the error body."
        ),
    },
    # --------------------------------------------------------------- shipping
    {
        "slug": "fastapi-testing",
        "title": "FastAPI – Testing the Whole Stack",
        "state": "rewrite",
        "tags": ["fastapi", "python", "testing"],
        "excerpt": (
            "TestClient against the real ASGI stack, dependency_overrides to swap the database "
            "and the current user, and a fixture that runs every test inside a transaction it "
            "rolls back. Which tests belong at the service layer and which can only be written "
            "through HTTP — including the class of bug that lives entirely in configuration and "
            "is invisible to everything below TestClient."
        ),
    },
    {
        "slug": "fastapi-observability",
        "title": "FastAPI – Logging, Health Checks and Request Tracing",
        "state": "new",
        "tags": ["fastapi", "python", "observability"],
        "excerpt": (
            "Making a running API explainable. Structured JSON logs with a correlation id "
            "carried by a ContextVar so it survives both async routes and the threadpool, a "
            "health check that reports each dependency separately, and what to log per request. "
            "Includes two things that bite in a container: uvicorn quietly replacing your log "
            "config, and a test that asserted on log content while reading another handler's work."
        ),
    },
    {
        "slug": "fastapi-docker",
        "title": "FastAPI – Containerising It Properly",
        "state": "new",
        "tags": ["fastapi", "python", "docker"],
        "excerpt": (
            "A multi-stage Dockerfile that leaves the compiler behind, a .dockerignore that cuts "
            "the build context from hundreds of megabytes and keeps .env out of a layer, and a "
            "non-root user. Then the settings that decide whether it works: --host 0.0.0.0, "
            "PYTHONUNBUFFERED, how many workers, and a healthcheck. With the resulting image "
            "size and build time measured rather than estimated."
        ),
    },
    {
        "slug": "fastapi-deployment",
        "title": "FastAPI – Getting It Into Production",
        "state": "rewrite",
        "tags": ["fastapi", "python", "deployment"],
        "excerpt": (
            "From a working image to something serving users. Workers and what they cost in "
            "database connections, a reverse proxy in front, configuration and secrets from the "
            "environment, running migrations as a step rather than at boot, and rolling out "
            "without dropping requests. Plus what to check first when it works locally and not "
            "in the cluster."
        ),
    },
    {
        "slug": "fastapi-interview-questions",
        "title": "FastAPI – Interview Questions",
        "state": "rewrite",
        "tags": ["fastapi", "python", "interview"],
        "excerpt": (
            "The questions a FastAPI role actually asks, answered against the eighteen lessons "
            "before this one. Why type hints do the validating, def versus async def and what "
            "happens to each, how dependency injection is tested, where a transaction begins and "
            "ends, what BackgroundTasks does not promise, and how a request is traced in "
            "production. Short answers, with the reasoning behind them."
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
        "state": entry["state"],
    }
    for i, entry in enumerate(_TRACK)
]

# Slugs that already exist on the live site and must never change. All nine were published in
# June 2023; check_content.py fails if one leaves the manifest, and seed.py refuses to write to
# prod if one is missing from the target tree.
FROZEN_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "rewrite"}

NEW_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "new"}

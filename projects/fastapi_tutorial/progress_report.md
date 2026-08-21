# FastAPI tutorial track — progress report

**Status:** WRITTEN AND SEEDED TO **local** — all 18 post bodies exist, pass every check, and are
in the local content tree with the category record fixed. NOT published to prod.
**Started:** 2026-08-21
**Where it lands:** https://lovemesomecoding.com/fastapi

---

## What this is

Unlike the Hasura track, `/fastapi` is **not empty**. It holds nine posts, all published
2023-06-01…09, and every one of them is long. Measured off the **prod** content tree on
2026-08-21:

| slug | prose words | code blocks | h2 | h3 | reading | languages |
|---|---:|---:|---:|---:|---:|---|
| `fastapi-introduction` | 4,657 | 52 | 16 | 44 | 40m | bash, python |
| `fastapi-routes-request-handling` | 1,629 | 65 | 15 | 60 | 36m | bash, python |
| `fastapi-rest-api` | 2,592 | 55 | 13 | 64 | 49m | bash, python |
| `fastapi-pydantic-models-validation` | 1,427 | 63 | 16 | 62 | 43m | bash, python |
| `fastapi-database-integration` | 2,293 | 63 | 14 | 68 | 50m | bash, python |
| `fastapi-testing` | 1,383 | 57 | 17 | 44 | 55m | bash, python, yaml |
| `fastapi-authentication-authorization` | 2,540 | 59 | 14 | 68 | 53m | bash, python |
| `fastapi-deployment` | 1,965 | 79 | 16 | 55 | 33m | bash, plaintext, python |
| `fastapi-interview-questions` | 2,814 | 52 | 5 | 36 | 32m | bash, python |
| **total** | **21,300** | **545** | **126** | **501** | **391m** | |

So the problem here is the opposite of Hasura's. Nothing is thin. Three things are wrong instead:

1. **They are not "to the point."** 391 reading-minutes across nine posts, an average of 43
   minutes each. `fastapi-database-integration` carries 14 `<h2>` and 68 `<h3>` and finishes with
   a section called *"Complete Project: E-Commerce Data Layer."* That is a book chapter, not a
   tutorial post.
2. **Every example is invented.** Products, orders, carts, a generic e-commerce data layer. The
   README asks for StayHub, and none of it is StayHub.
3. **The category record is broken** — `{"slug": "fastapi", "name": "fastapi", "description": ""}`.
   Lowercase display name, no description. Exactly the defect the Hasura track had to fix.

Every post carries `tags: ["fastapi"]`, which at least is not the Hasura situation (no tags at all).

### The nine slugs are frozen

All nine are live, indexed URLs, and the frontend runs `trailingSlash: false` with a build guard
(`scripts/verify-build.mjs`) that **fails the build** if an indexed post URL stops resolving. They
are rewritten **in place**. Renaming one is not a refactor, it is a dead link — see the migration
notes in `projects/rewrite/progress_report.md`.

They also all carry 2023 dates. `upsert_post` never overwrites an existing date, so seeding this
track needs `seed.py --force-dates` exactly once per tree or the archive interleaves nine 2023
posts with nine 2026 ones and the pager reads nonsense. Same trap the Hasura track documented.

---

## Decisions — 2026-08-21

Three questions were put to Folau; all three answered.

| Question | Decision |
|---|---|
| Post length | **Medium — 15–20 reading-minutes**, ~2,500–3,000 prose words. Roughly half of what is there now. Each post still covers one whole area end to end. |
| Track size | **18 posts** — the 9 rewritten in place plus 9 new. |
| StayHub gaps | **Build the additions first, then write.** Quote only code that has actually run. |

The third decision is the important one. The Hasura track's own progress report records what
happens when it is skipped: four posts were written describing StayHub surfaces that were never
built, and they remain the four least-verified posts in that track. Not repeating it here.

---

## The topic table — 18 posts

Derived from the official FastAPI *Tutorial – User Guide* and *Advanced User Guide*
(fastapi.tiangolo.com/learn, read 2026-08-21) filtered to the README's bar: **what you actually
need to get a project developed and released to production**, not every feature that exists.

Ordering is teaching order. Dates ascend with the track so the archive reads as a course.

### Rewritten in place — slugs frozen

| # | slug | what it becomes |
|---|---|---|
| 1 | `fastapi-introduction` | Why FastAPI, install, first app, `/docs`, the ASGI request cycle. Currently 4,657 words and duplicates half of posts 2, 4 and 10 — the biggest cut in the track. |
| 2 | `fastapi-routes-request-handling` | Path/query/header/cookie params, `Annotated`, status codes, `APIRouter`. |
| 3 | `fastapi-rest-api` | Resource design, PATCH vs PUT, `response_model`, pagination, filtering. StayHub's `/properties` is the worked example. |
| 4 | `fastapi-pydantic-models-validation` | Pydantic v2: field constraints, validators, `computed_field`, the snake_case↔camelCase alias boundary. |
| 5 | `fastapi-database-integration` | Engine, session-per-request, the repository layer, transactions, Alembic, N+1. |
| 6 | `fastapi-testing` | `TestClient`, `dependency_overrides`, the rollback fixture, async tests. |
| 7 | `fastapi-authentication-authorization` | Password hashing, JWT, `HTTPBearer`, role gates via dependencies. |
| 8 | `fastapi-deployment` | Uvicorn/Gunicorn workers, reverse proxy, env config, zero-downtime, health checks. |
| 9 | `fastapi-interview-questions` | Rewritten against the other seventeen. |

### New

| # | slug | why it earns a post |
|---|---|---|
| 10 | `fastapi-project-structure` | The single most-asked question and the one the docs answer worst. StayHub's `api/ core/ db/ models/ repositories/ schemas/ services/` layout, and why each layer exists. |
| 11 | `fastapi-dependency-injection` | `Depends`, `yield`, sub-dependencies, `Annotated` type aliases, `dependency_overrides`. FastAPI's defining feature; currently scattered across three posts. |
| 12 | `fastapi-error-handling` | One error shape for the whole API. Custom exception classes, handlers, flattening `RequestValidationError` into field errors a form can render. |
| 13 | `fastapi-async-vs-sync` | `def` vs `async def`, the threadpool, when async actually helps, blocking calls in async routes. The most common production mistake in the framework. |
| 14 | `fastapi-middleware-cors` | Middleware order, request IDs, timing, and why `allow_credentials=True` forbids `allow_origins=["*"]`. |
| 15 | `fastapi-background-tasks` | `BackgroundTasks`, what it is not, and when you need a real queue instead. |
| 16 | `fastapi-file-uploads` | `UploadFile`, streaming vs `bytes`, size limits, storage. |
| 17 | `fastapi-docker` | Multi-stage Dockerfile, worker count, compose, image size. |
| 18 | `fastapi-observability` | Structured logging, health checks that name what is broken, metrics, request tracing. |

**Deliberately left out** (README: *"We don't need to create a post for every single small thing"*):
WebSockets and SSE, OpenAPI callbacks/webhooks, sub-application mounts, templates, WSGI
inclusion, dataclasses, OAuth2 scopes, SDK generation. None of them block shipping a REST API.

---

## The demo app

`lovemesomecoding_demo_project/stayhub/stayhub-fastapi-backend` — the **write** side of an
Airbnb-style app. Reads come from Hasura; `GET /api/v1/search` from Elasticsearch.

### Verified running, 2026-08-21

```
GET http://localhost:8000/health -> {"status":"ok","database":true,"elasticsearch":true}
pytest -q                        -> 58 passed in 2.27s
```

Containers up and healthy: `stayhub-postgres` (5433), `stayhub-hasura` (8081),
`stayhub-elasticsearch` (9200). The **API itself is not containerised** — it runs on the host under
uvicorn. That is a gap post 17 has to fix, not just describe.

### Versions — read off this machine, not chosen

| | |
|---|---|
| python | 3.12.4 |
| fastapi | 0.115.5 |
| starlette | 0.41.3 |
| pydantic | 2.10.3 |
| pydantic-settings | 2.6.1 |
| sqlalchemy | 2.0.36 |
| alembic | 1.14.0 |
| uvicorn | 0.32.1 (`[standard]`) |
| postgres | 16.15 |
| docker engine | 27.4.0 |
| host | Docker Desktop on aarch64 (Apple Silicon) |

### What StayHub already does well — quote this, do not invent it

The app is densely commented with real *why* reasoning. These are the strongest teaching moments
already sitting in the tree:

| file | what it teaches |
|---|---|
| `app/core/security.py` | JWT shared with Hasura; **the Hasura role cannot be called `admin`** — it is reserved, bypasses every permission, and metadata refuses to define rules for it. Also: every `x-hasura-*` claim must be a *string*, and bcrypt silently truncates at 72 **bytes**. |
| `app/core/deps.py` | `Annotated` dependency aliases (`CurrentUser`, `HostUser`, `AdminUser`); `HTTPBearer(auto_error=False)` so an absent header reaches our handler instead of FastAPI's; the user re-read from the DB every request because a token proves *who*, not *what they currently are*. |
| `app/core/exceptions.py` | One error body for the entire API; `RequestValidationError` flattened to `field -> message`; stack traces never returned. |
| `app/schemas/common.py` | The snake_case↔camelCase boundary via `alias_generator=to_camel` + `populate_by_name`; `EmailStr` rejecting `.test` and why that is correct. |
| `app/schemas/booking.py` | `@computed_field` for values that change at midnight; and the `property` field shadowing the `property` builtin inside a class body — a `TypeError` that points twenty lines away from its cause. |
| `app/repositories/base.py` | **Repositories never commit.** `flush()` where an id is needed; the caller owns the transaction boundary. |
| `app/db/session.py` | `pool_pre_ping=True`; `expire_on_commit=False` and why it matters *specifically* for FastAPI — serialisation happens after the route returns, sometimes after the session is gone. |
| `app/services/booking_service.py` | The friendly overlap check loses the race and the Postgres exclusion constraint wins it; `IntegrityError` translated into a 409. |
| `app/main.py` | `lifespan`; a failing search index must not stop the app booting; a health check that names *which* dependency is down. |
| `tests/conftest.py` | Rollback bound to an **outer** transaction on the connection, so code under test can call `commit()` and still leave no trace. |

### ✅ What StayHub was missing — all eight built, 2026-08-21

| gap | needed by | what was added | status |
|---|---|---|---|
| custom middleware | 14, 18 | `app/core/middleware.py` — request id + timing + access log | ✅ |
| structured logging | 18 | `app/core/logging.py` — JSON formatter, ContextVar request id | ✅ |
| `TestClient` | 6 | `tests/test_api_{middleware,admin,uploads}.py` | ✅ 42 tests |
| pagination helper | 3 | `Page[T]` + `PageParams` in `schemas/common.py`; two new admin list endpoints use it | ✅ |
| `BackgroundTasks` | 15 | `app/services/notification_service.py`, wired into booking create + cancel | ✅ |
| `UploadFile` | 16 | `app/api/v1/routes/uploads.py` — sniffed, streamed, size-capped | ✅ |
| `Dockerfile` | 17, 8 | multi-stage + `.dockerignore` + `api` compose service behind a profile | ✅ |
| async SQLAlchemy | 13 | `app/db/async_session.py` + `GET /admin/stats-async` + `scripts/bench_stats.py` | ✅ |

`pytest -q`: **58 → 100 passing.** The app boots, `/health` is green, and the database is
unchanged after a run (4 users / 12 properties / 3 bookings, same as the seed).

Nothing existing was rewritten. `/admin/stats` is still sync, `GET /bookings/mine` still returns a
bare list, and `docker compose up -d` still starts backing services only — every addition is
additive so no frontend breaks.

---

## What the app work turned up — this is the material the posts are made of

Building before writing was the right call. Four of these could not have been written from the
docs, and two were bugs.

### 🐛 A real bug: a 500 reached the browser with no CORS headers

`register_exception_handlers` registers a handler for bare `Exception`. Starlette does **not** put
that handler where the others go — the specific handlers live in `ExceptionMiddleware`, the
innermost layer, while a bare-`Exception` handler becomes `ServerErrorMiddleware`'s handler, the
**outermost** layer of the whole stack. A response built out there has already skipped every user
middleware on the way back.

Measured before the fix:

```
unhandled 500 ->  X-Request-ID absent   Access-Control-Allow-Origin absent
handled   404 ->  X-Request-ID present  Access-Control-Allow-Origin present
```

So the React frontend saw a CORS failure instead of `{"message": "Something went wrong on our
end."}` — its single error parser never got the body. **Fix:** `RequestContextMiddleware` sits
*inside* CORS and converts unhandled exceptions itself, so CORS still sees a normal response.
Locked in by `test_a_500_still_carries_cors_headers`, which was test-fired: reversing the two
`add_middleware` calls fails that test and nothing else in the suite.

Feeds posts **12** (error handling) and **14** (middleware).

### 🐛 A second bug, found by reading `docker logs`

The access log line — the one line whose entire purpose is correlation — came out as
`"request_id": "-"` while every other line in the same request carried the real id. The
`ContextVar` was reset in a `finally:` that ran *before* the logging call below it.

No test caught it because no test asserted on log **content**. The first replacement test was
itself wrong: it used pytest's `caplog` and passed even with the bug reintroduced, because a
`LogRecord` is one object shared by every handler — the app's root handler (carrying
`RequestIdFilter`) mutated it before caplog's handler saw it, so the test was reading the filter's
work and reporting it as the middleware's. The real test replaces the root handlers and asserts on
the emitted JSON.

Feeds post **18** (observability), and is a genuinely good "your test is lying to you" story.

### 📐 `BackgroundTasks` — the trap is that it half-works

A `yield` dependency's cleanup runs **before** background tasks. Measured, FastAPI 0.115.5:

```
1. dep: open
2. route body
3. dep: CLOSED        <- get_db's finally: db.close()
4. background task ran
```

So the request's session is closed by the time the task runs. What makes it dangerous is that
passing the ORM object *mostly* works:

```
booking.total          -> OK, Decimal('797.40')     (expire_on_commit=False keeps it)
booking.property.title -> DetachedInstanceError
```

A loaded column survives; the first unvisited relationship raises. The version that passes the
object passes a test that checks the total, and breaks in production the day someone adds the
property name to the email — after a 200 has already gone out, where nobody is looking.
`notification_service` therefore takes a **UUID** and opens its own session.

Feeds post **15**.

### 📊 Async measured, and it lost

`/admin/stats-async` runs the same eight aggregates concurrently with `asyncio.gather`. Against
this Postgres, 30 runs each:

```
/admin/stats        (8 serial)      median   7.9ms
/admin/stats-async  (8 concurrent)  median  19.8ms     <- 2.5x WORSE
```

Varying only the per-query wait shows exactly why (8 queries, median of 7 runs):

| per-query wait | sync serial | async gather | |
|---:|---:|---:|---|
| 0 ms | 4.0 ms | 15.5 ms | async **289% slower** |
| 5 ms | 59.1 ms | 22.2 ms | async 63% faster |
| 50 ms | 444.9 ms | 76.2 ms | async 83% faster |
| 200 ms | 1654.7 ms | 232.9 ms | async 86% faster |

Break-even is roughly **1–2 ms of wait per call**. A database on the same machine is below it; a
third-party HTTP API, an S3 upload or a cross-network database is far above it. `/admin/stats`
stays sync because it is the faster endpoint.

This is the empirical backbone of post **13**, and it directly contradicts the "async is faster"
framing the existing `fastapi-introduction` post leans on.

### 🔧 `SQLAlchemy[asyncio]`, not `SQLAlchemy`

`create_async_engine` needs `greenlet`, which the bare install does not pull in. Everything
imports fine and the first async query dies **at close time** with `ValueError: the greenlet
library is required to use this function`, pointing at `sqlalchemy/util/concurrency.py` rather
than at anything you wrote. `requirements.txt` now says `SQLAlchemy[asyncio]==2.0.36`.

### 🔧 Uvicorn overwrites your logging config

Uvicorn installs its own handlers on `uvicorn.access` / `uvicorn.error` when it starts — *after*
`configure_logging` has run — so its lines bypass the formatter entirely. Observed in `docker
logs`: two lines per request, one JSON and one not, in a stream something is trying to parse.
`uvicorn.access` is now disabled outright (the middleware already logs every request, with a
duration and an id uvicorn's line lacks) and the others propagate to root.

Feeds posts **17** and **18**.

### 🔒 Upload guards, each one test-fired

`Content-Type` in a multipart part is whatever the client typed — `curl -F 'file=@shell.php;
type=image/png'` sets it to anything. The route sniffs magic bytes and requires them to **match**
the declared type; generates the stored filename instead of trusting `file.filename`
(`"../../app/main.py"` is a valid string); caps size *during* the stream (there is no trustworthy
length up front — `Content-Length` is a claim and a chunked upload sends none); and deletes the
partial file on failure. 13 tests, one per guard.

Feeds post **16**.

### 🐳 Container facts, verified not assumed

```
image size          304 MB
runs as             stayhub (non-root)
.env in the image   absent
gcc in the runtime  absent
healthcheck         healthy
```

`--host 0.0.0.0` is the one that catches everyone: uvicorn's default binds the container's own
loopback, the bind succeeds, the app logs that it is running, `docker ps` shows the port
published, and every request from the host is refused with nothing anywhere saying why.

Feeds post **17**.

---

## Where it stands

| | |
|---|---|
| Survey of `/fastapi` | ✅ 9 posts, prod tree read directly |
| Topic table | ✅ 18 lessons, agreed 2026-08-21 |
| Decisions | ✅ length, size, build-first — all three answered |
| Demo app runs | ✅ health ok, 58 tests pass, versions captured |
| StayHub additions | ✅ **all eight done**, 100 tests passing |
| `manifest.py` | ✅ 18 posts, 9 frozen slugs cross-checked against prod — exact match |
| `check_content.py` | ✅ built, all five track rules test-fired |
| `check_snippets.py` | ✅ built; matching, drift, undeclared-source and antipattern all fired |
| `seed.py` | ✅ built; dry-runs clean, all three guards fired |
| Post bodies | ✅ **18 of 18**, 54,300 words, 357 code blocks |
| Category record fixed | ✅ `"FastAPI"` + a real description |
| Seeded to `local` | ✅ archive holds 18, dates in reading order, 9 frozen URLs preserved |
| Published to `prod` | ⬜ **not done** — awaiting review |

---

## Notes and traps carried over

- **`seed.py --force-dates` exactly once per tree.** Nine slugs carry 2023 dates that
  `upsert_post` will not overwrite.
- **Never rename a frozen slug.** `verify-build.mjs` fails the build, which is the point.
- **`python` is already a supported language** in the content pipeline, unlike `graphql` before the
  Hasura track. Confirm `dockerfile` and `ini` before post 17 needs them.
- Code blocks must render as `<pre class="language-X"><code class="language-X">` — the build-time
  Prism highlighter matches that exact shape.
- Extract `<pre>` blocks with regex **before** any HTML parsing. Post bodies contain raw
  unescaped tags inside code samples.


---

## The tooling — built and test-fired 2026-08-21

Four scripts, modelled on the Hasura track's but with this track's rules.

### `manifest.py`

18 posts in reading order, dates computed from `START_DATE + STEP_DAYS` so a reorder is one edit.
Cross-checked against the live prod index:

```
live on /fastapi     : 9
manifest frozen      : 9
exact match          : True
orphans / phantoms   : none
new slugs colliding  : none
```

It also holds `MEASURED` — every performance and container figure this track quotes, recorded
once so three posts cannot disagree about the same number.

### ⚠️ The length budget was wrong in the first draft of this report

The decision was "15–20 reading minutes", and this report originally translated that to
"~2,500–3,000 prose words". **That was wrong**, and it would have shipped 25–30 minute posts.

`readingMinutes` is computed in `lovemesomecoding_backend/app/services/content.py:161` as
`max(1, round(words / 220))` — where `words` counts **prose and code text together**. So the
budget is a cap on the TOTAL:

```
15-20 min  =  3,300 - 4,400 words, prose + code
```

Re-measuring the live posts with that split changes what the problem even is:

| slug | prose | code | total | min | code share |
|---|---:|---:|---:|---:|---:|
| `fastapi-testing` | 1,383 | 10,647 | 12,030 | 55 | 88% |
| `fastapi-authentication-authorization` | 2,540 | 9,074 | 11,614 | 53 | 78% |
| `fastapi-database-integration` | 2,293 | 8,605 | 10,898 | 50 | 79% |
| `fastapi-rest-api` | 2,592 | 8,191 | 10,783 | 49 | 76% |
| `fastapi-pydantic-models-validation` | 1,427 | 8,088 | 9,515 | 43 | 85% |
| `fastapi-introduction` | 4,657 | 4,097 | 8,754 | 40 | 47% |
| `fastapi-routes-request-handling` | 1,629 | 6,303 | 7,932 | 36 | 79% |
| `fastapi-deployment` | 1,965 | 5,348 | 7,313 | 33 | 73% |
| `fastapi-interview-questions` | 2,814 | 4,231 | 7,045 | 32 | 60% |
| **total** | **21,300** | **64,584** | **85,884** | **391** | **75%** |

**Code is 75% of the counted words.** `fastapi-testing` runs 7.7 words of code per word of prose.
These posts are not over-written — they are **code dumps with captions**. So the checker enforces
two things, and the second matters more:

- total words ≤ 4,400 (the reading-time cap)
- **prose ≥ 40% of words** (`MIN_PROSE_SHARE`) — because a total-words cap alone is satisfied by
  a *shorter* code dump

### `check_content.py` — five rules, each fired against a fixture

| rule | fixture | result |
|---|---|---|
| 2 · reading-time cap | 6,602-word post | ✗ `over the 4400-word cap (20 min). Remember code counts: 3600 of these are code` |
| 3 · prose floor | 602 prose / 3,600 code | ✗ `prose is 14% of the words, floor is 40% … a listing with commentary, not a lesson` |
| 5 · a rewrite must shrink | 9,602-word `fastapi-introduction` | ✗ `the live page already has 8754 (40 min) — the whole point was to cut it` |
| 4 · claims must be sourced | invented "42.7ms faster" | ! `quotes no figure from manifest.MEASURED` |
| 4 · required citations | async post with no figures | ✗ `must quote the measured value '7.9'` / `'19.8'`; docker post ✗ `'304MB'` |
| — · control | a clean 3,800-word post | passes silently |

Plus the round-trip check that motivated this class of script. Demonstrated on a block containing
raw `<script>` and `onclick=`:

```
length before corruption: 13697
length after  corruption: 13660   (delta 37 chars)
a length-based check would see a 0.27% change — invisible
byte-for-byte comparison: DIFFERENT (caught)
```

### `check_snippets.py` — and the bug in its own first version

Verifies every python/yaml/json/docker block actually appears in the StayHub file the post
**declared** in `SNIPPET_SOURCES` — stronger than "somewhere in the app". Five paths, all fired:

| block | verdict |
|---|---|
| verbatim from a declared file | matched |
| real code from an *undeclared* file | ! warned, named the declared list |
| drifted quote | ✗ **drift**, exit 1 |
| invented `class Product(BaseModel)` | illustrative |
| block under `data-antipattern` | excluded |

⚠️ **The first version silently misclassified drift as harmless.** It took the first 3 lines and
asked whether that exact run appeared in the app — which fails on the most common drift there is,
a changed line *inside* those three:

```
def require_host(user: CurrentUser) -> User:      <- still true
    if not user.is_host:                          <- still true
        raise ForbiddenException("Hosts only!")   <- CHANGED
```

The fixed lead did not match, so the block landed in `illustrative` — the one bucket that never
fails a build. Replaced with a longest-matching-prefix scan, which now reports:

```
✗ the first 2 of 4 lines ARE in the app but the block as a whole is not — the quote has drifted.
      last good : 'if not user.is_host:'
      drifts at : 'raise ForbiddenException("Hosts only, sorry!")'
```

### `seed.py` — three guards, all fired

| guard | local | prod |
|---|---|---|
| a frozen slug missing from the tree | `note:` and continues | **refuses** — "Seeding would create new pages instead" |
| a `new` slug that already exists | **refuses** — "Seeding would overwrite them" | same |
| a slug owned by another category | refuses | refuses |

Dry runs are clean against both trees; prod reports **all 9 frozen slugs present**.

⚠️ `--force-dates` is still needed exactly once per tree, for the nine 2023 dates.

### No content-pipeline change needed

Unlike the Hasura track — which was blocked until `graphql` was added to both the backend's
`SUPPORTED_LANGUAGES` and the frontend's Prism imports — every language this track needs already
works: `python`, `bash`, `yaml`, `json`, `sql`, plus the aliases `dockerfile → docker` and
`ini → properties`. `check_content.py` asserts both halves anyway, so a regression fails loudly.

---

## Next

Write the 18 post bodies, in manifest order, against a 3,300–4,400 word budget and a 40% prose
floor. Then `--force-dates` into `local`, review, and only then prod.


---

## The 18 posts — written and seeded 2026-08-21

`seed.py --env local --write --force-dates` ran once. The tree went from 652 to 661 published
posts (nine new), and the nine rewrites landed on their existing URLs.

| # | date | slug | words | min | prose | blocks |
|---|---|---|---:|---:|---:|---:|
| 1 | 2026-09-02 | `fastapi-introduction` | 3,357 | 15 | 77% | 24 |
| 2 | 2026-09-05 | `fastapi-routes-request-handling` | 3,274 | 15 | 83% | 32 |
| 3 | 2026-09-08 | `fastapi-pydantic-models-validation` | 3,168 | 14 | 80% | 22 |
| 4 | 2026-09-11 | `fastapi-project-structure` | 3,146 | 14 | 77% | 21 |
| 5 | 2026-09-14 | `fastapi-dependency-injection` | 3,109 | 14 | 78% | 23 |
| 6 | 2026-09-17 | `fastapi-database-integration` | 3,087 | 14 | 77% | 31 |
| 7 | 2026-09-20 | `fastapi-rest-api` | 3,111 | 14 | 79% | 27 |
| 8 | 2026-09-23 | `fastapi-error-handling` | 3,139 | 14 | 76% | 29 |
| 9 | 2026-09-26 | `fastapi-authentication-authorization` | 3,089 | 14 | 81% | 21 |
| 10 | 2026-09-29 | `fastapi-file-uploads` | 2,865 | 13 | 74% | 27 |
| 11 | 2026-10-02 | `fastapi-background-tasks` | 2,875 | 13 | 83% | 19 |
| 12 | 2026-10-05 | `fastapi-async-vs-sync` | 2,859 | 13 | 87% | 23 |
| 13 | 2026-10-08 | `fastapi-middleware-cors` | 2,787 | 13 | 70% | 25 |
| 14 | 2026-10-11 | `fastapi-testing` | 2,937 | 13 | 77% | 26 |
| 15 | 2026-10-14 | `fastapi-observability` | 2,821 | 13 | 77% | 27 |
| 16 | 2026-10-17 | `fastapi-docker` | 2,800 | 13 | 63% | 32 |
| 17 | 2026-10-20 | `fastapi-deployment` | 2,973 | 14 | 89% | 15 |
| 18 | 2026-10-23 | `fastapi-interview-questions` | 2,957 | 13 | 95% | 9 |

### Against the collection it replaces

| | before | after |
|---|---:|---:|
| Posts | 9 | 18 |
| Total words | 85,884 | 54,300 |
| Reading minutes | 391 | **242** |
| Per post | 43 min | **13&ndash;15 min** |
| Prose share | 25% | **78%** |
| Code blocks | 545 | 357 |
| Blocks from running code | 0 | **247 (69%)** |
| Tags | `["fastapi"]` on all nine | 2&ndash;4 real tags each |
| Category record | `"fastapi"`, no description | `"FastAPI"` + description |

### ⚠️ Length landed at 13&ndash;15 min, not the agreed 15&ndash;20

The band was 15&ndash;20 reading-minutes (3,300&ndash;4,400 words). The posts cluster just under
it: **eight at 14&ndash;15 minutes, ten at 13**.

This is a real miss against the agreed number, and it is reported rather than papered over. The
judgement was that the remaining ~400 words per post would have been added *for length* rather than
because a topic was unfinished &mdash; which contradicts the README's "keep posts to the point".
Every post covers its whole area and ends where it runs out of things worth saying.

If the band matters more than that judgement, the cheapest honest way to close it is to fold two
pairs of adjacent topics together (13+15 middleware/observability, 11+12 background/async) rather
than to pad eighteen posts by 15% each. Say the word.

`check_content.py` reports these as **warnings, not failures**, deliberately &mdash; the cap is
hard, the floor is advisory.

### What the checks say

```
check_content.py    all 18 posts pass         (20 advisory warnings, 16 of them the length floor)
check_snippets.py   no drift
                    247/357 checked blocks (69%) quoted from code that runs
                    4 antipattern blocks correctly excluded
                    0 blocks from undeclared files
```

The 31% that are not quoted from StayHub are shell commands, JSON responses, small teaching
examples (`Quote`, `Tiny Listings`), the Flask comparison, and deliberately-wrong "what is wrong
with this?" blocks. Every one of those is legitimately not app code.

### Two drift catches during writing

The snippet checker earned its place twice, both times on the same mistake: a snippet **adapted**
from real code rather than quoted from it.

- **Post 10** &mdash; an S3 variant of the upload loop. Rewritten to show only the delta.
- **Post 13** &mdash; a `CORSMiddleware` call with `expose_headers` added. Same fix.
- **Post 17** &mdash; a `FastAPI(...)` call with three arguments made conditional. Same fix.

Each was reported as *"the first N of M lines ARE in the app but the block as a whole is not"*,
which is exactly the signature it was built to catch. Without it all three would have shipped as
plausible quotes of code that does not exist.

### Verified after seeding

```
category      slug=fastapi  name="FastAPI"  count=18
archive       18 posts, dates strictly descending, all 2026
frozen URLs   all 9 resolve to /fastapi/<slug>, status=published
tree          652 -> 661 published posts
```

---

## Outstanding

1. **Review the 18 posts**, then `seed.py --env prod --write --force-dates` (once).
2. **Decide on length** &mdash; accept 13&ndash;15 min, or merge pairs to reach the band.
3. **Commit the StayHub additions** &mdash; 10 modified, 11 new files in
   `lovemesomecoding_demo_project`, all uncommitted.
4. **`--force-dates` is needed exactly once per tree.** Already used on `local`; prod still needs
   it, or nine 2023 posts interleave with nine 2026 ones.

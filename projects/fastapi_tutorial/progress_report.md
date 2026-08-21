# FastAPI tutorial track — progress report

**Status:** APP WORK DONE — all eight StayHub gaps built, verified and covered by tests
(58 → 100 passing). Post bodies not started.
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
| `manifest.py` | ⬜ **next** |
| `check_content.py` / `check_snippets.py` | ⬜ |
| `seed.py` | ⬜ |
| Post bodies | ⬜ 0 of 18 |
| Category record fixed | ⬜ still `"name": "fastapi"`, empty description |
| Seeded to `local` | ⬜ |
| Published to `prod` | ⬜ |

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

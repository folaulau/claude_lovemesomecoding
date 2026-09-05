# System Design track — progress report

**Status:** ✅ **PUBLISHED AND LIVE** — 18 posts on https://lovemesomecoding.com/system-design,
all 18 URLs verified serving at the edge. Build `394b0bd`, deployed 2026-08-22.
**Started:** 2026-08-22
**Where it lands:** https://lovemesomecoding.com/system-design

---

## What is there now

`/system-design` is **not empty** — it holds 7 published posts. But unlike `/fastapi` (where every
post was too long), the problem here is the Hasura one: **everything is thin, and none of it is
structured.** Measured off the **prod** content tree on 2026-08-22:

| date | slug | title | prose words | code blocks | h2 | h3 | images | reading |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 2018-03-05 | `system-design-basics` | System Basics | 2,871 | 0 | 0 | 0 | 15 | 13m |
| 2019-03-04 | `system-design-introduction` | Introduction | 674 | 0 | 0 | 0 | 3 | 3m |
| 2019-03-05 | `system-design-notification-system` | Notification System | 780 | 2 | 0 | 0 | 3 | 4m |
| 2019-03-09 | `system-design-unique-id-generator` | Unique ID Generator | 382 | 0 | 0 | 0 | 3 | 2m |
| 2019-03-10 | `system-design-chat-system` | Chat System | 1,223 | 0 | 0 | 0 | 7 | 6m |
| 2019-03-14 | `system-design-url-shortener` | Url Shortener | 334 | 0 | 0 | 0 | 4 | 2m |
| 2023-07-19 | `system-design-interview-questions` | System Design – Interview Questions | 878 | 0 | 0 | 0 | 0 | 4m |
| | **total** | | **7,142** | **2** | **0** | **0** | **35** | **34m** |

Five defects, all confirmed:

1. **Zero headings across the entire track.** Not one `<h2>` or `<h3>` in 7,142 words. The bodies
   are raw WordPress boldgrid markup — `<div class="boldgrid-section"><div class="container">…`
   wrapping bare `<p>` tags with `<strong>` doing the work a heading should do. Nothing generates a
   table of contents (`toc: []` on every post) and nothing is skimmable.
2. **Two code blocks in the whole track.** A system design track can live on diagrams, but two
   snippets across seven posts means nothing is grounded in code that runs.
3. **35 images, and every one is a screenshot.** Filenames are literally
   `Screen-Shot-2022-03-04-at-6.27.18-PM.png`. They serve from the media CDN and still resolve, but
   they are raster screenshots of diagrams — they do not adapt to the site's dark theme, they do not
   scale on mobile, and their provenance is a book, not this site.
4. **The category record is broken** — `{"slug": "system-design", "name": "system-design",
   "description": ""}`. Lowercase display name, empty description. Same defect the Hasura and
   FastAPI tracks each had to fix.
5. **No tags.** `tags: []` on all seven.

Titles are also inconsistent with the rest of the site: *"Introduction"*, *"System Basics"*,
*"Chat System"* carry no subject, so they read as orphans in search results and in the archive.

### The seven slugs are frozen

All seven are live, indexed URLs. The frontend runs `trailingSlash: false` with a build guard
(`scripts/verify-build.mjs`) that **fails the build** if an indexed post URL stops resolving. They
get rewritten **in place**. Renaming one is a dead link, not a refactor.

They also carry 2018/2019/2023 dates, and `upsert_post` never overwrites an existing date — so
seeding this track needs `seed.py --force-dates` exactly once per tree, or the archive interleaves
seven old posts with the new ones and the pager reads nonsense. Documented trap; not rediscovering it.

---

## The demo app

`lovemesomecoding_demo_project/stayhub/stayhub-fastapi-backend` — per the README.

StayHub is **an Airbnb-style short-let app**, which is a gift for one of the three requested case
studies and a question mark for the other two. Its shape:

```
                 ┌── writes ──> FastAPI ──> Postgres
   React apps ───┤                              │
                 ├── reads  ──> Hasura ─────────┘
                 └── search ──> FastAPI ──> Elasticsearch
                                              ▲
                        sunk in application code from every write path
```

Surfaces that already exist and map directly onto system-design topics:

| StayHub surface | System-design topic it grounds |
|---|---|
| `search/indexer.py` — Postgres → Elasticsearch sink in app code | CQRS, read/write split, denormalised read models, dual-write consistency |
| Hasura for reads, FastAPI for writes | read/write separation, why one JWT and two APIs |
| `services/pricing_service.py` — server recomputes every price | trust boundaries, idempotent server-side authority |
| `services/booking_service.py` — availability check | write contention, double-booking, locking |
| `core/middleware.py` — request context, CORS ordering | request IDs, tracing, middleware order |
| `repositories/` never commit; services own the transaction | transaction boundaries across aggregates |
| `public_id` UUID exposed, BIGINT PK internal | id generation, enumeration attacks |
| `services/notification_service.py` | the notification-system case study |
| `docker-compose.yml` — postgres · hasura · elasticsearch | the moving parts of a small distributed system |

**Gaps** — nothing in StayHub currently demonstrates: caching (no Redis), rate limiting, a message
queue, sharding/partitioning, a CDN path, or load balancing across replicas.

Two other demo apps exist and are relevant to the case studies: `pizza` (Pizza Hut-style, Spring
Boot + React, cart/checkout/Stripe/admin reports) and `bank` (console, no services).

---

## Decisions — 2026-08-22

Four questions were put to Folau; all four answered.

| # | Question | Decision |
|---|---|---|
| 1 | Track size | **18 posts** — the 7 rewritten in place plus 11 new. |
| 2 | The 35 screenshots | **Replace all with ASCII diagrams.** Drops every raster image from the track. Site convention already proven across five tracks; works in both themes, scales on mobile, and is our own work. |
| 3 | Amazon and Delta code | **Add the missing pieces to StayHub, then reuse them.** Build what StayHub genuinely lacks and all three case studies need. Airbnb quotes StayHub throughout; Amazon and Delta reuse those primitives plus schema/pseudo-code for their domain specifics, framed as design rather than running code. |
| 4 | Post length | **Medium — 15–20 reading-minutes**, ~2,500–3,000 prose words. Roughly triple what is there now. |

Decision 3 carries the rule the Hasura track paid for and the FastAPI track adopted: **build the
additions first, then write. Quote only code that has actually run.** Hasura's four posts describing
surfaces that were never built remain that track's four least-verified posts.

---

## The topic table — 18 posts

Ordering is teaching order: what a system is made of, how each part scales, then four case studies
that assemble the parts, then the interview post. Dates ascend with the track so the archive reads
as a course.

### Rewritten in place — slugs frozen, titles fixed

| # | slug | title becomes | what it becomes |
|---|---|---|---|
| 1 | `system-design-introduction` | System Design: Introduction | What system design is, what an interview actually scores, and the four-step framework (scope → estimate → high-level design → deep dive). Currently 674 words and three screenshots. |
| 2 | `system-design-basics` | System Design Basics: The Parts of a Production System | Every box named — DNS, CDN, load balancer, stateless web tier, cache, primary/replica database, queue, object store, logging and metrics — and how the diagram grows from one box to many. Absorbs the monolith-vs-services discussion. Currently 15 screenshots and zero headings. |
| 11 | `system-design-unique-id-generator` | Designing a Unique ID Generator | UUIDv4/v7, database auto-increment, ticket server, Snowflake — and the tradeoff that decides it: sortability vs coordination. StayHub's BIGINT-PK-plus-`public_id`-UUID split is the worked example. Currently 382 words. |
| 12 | `system-design-url-shortener` | Designing a URL Shortener | Estimates, base62 vs hash-and-truncate, collisions, the 301-vs-302 decision, cache hit path, cleanup. Currently 334 words — the thinnest post in the track. |
| 13 | `system-design-chat-system` | Designing a Chat System | WebSockets vs polling, the connection/presence problem, message ordering, fan-out for group chat, storage choice. Currently 1,223 words. |
| 14 | `system-design-notification-system` | Designing a Notification System | Fan-out, provider abstraction, retries and idempotency, dedup, rate control, opt-outs. StayHub's `notification_service.py` and the new outbox are the worked example. Currently 780 words. |
| 18 | `system-design-interview-questions` | System Design Interview Questions | Rewritten against the other seventeen. |

### New

| # | slug | title | why it earns a post |
|---|---|---|---|
| 3 | `system-design-back-of-envelope-estimation` | Back-of-the-Envelope Estimation | The step candidates skip and interviewers weight most. Powers of two, latency numbers, QPS/storage/bandwidth arithmetic — run against StayHub's real row counts rather than invented ones. |
| 4 | `system-design-load-balancing` | Load Balancing and the Stateless Tier | L4 vs L7, algorithms, health checks, why sticky sessions are a trap, and what "stateless" actually requires. Includes the CDN — the cheapest request is the one that never reaches a server. |
| 5 | `system-design-caching` | Caching | Cache-aside vs write-through, TTL and eviction, invalidation, stampede/thundering herd, and what must never be cached. **Needs the StayHub Redis addition.** |
| 6 | `system-design-database-scaling` | Scaling the Database | Indexing, connection pools, read replicas and replica lag, vertical vs horizontal, partitioning vs sharding, choosing a shard key, hot shards, resharding. |
| 7 | `system-design-consistency-and-availability` | Consistency, Availability and CAP | CAP and PACELC without the folklore, strong vs eventual, read-your-writes, and the dual-write problem. StayHub's Postgres→Elasticsearch sink is a live eventual-consistency example with a real failure mode. |
| 8 | `system-design-message-queues` | Message Queues and Async Work | Queue vs log, at-least-once and why idempotency is mandatory, the transactional outbox, retries, backoff, DLQs — and when `BackgroundTasks` is enough. **Needs the StayHub outbox addition.** |
| 9 | `system-design-concurrency-and-locking` | Concurrency: Double Booking and Distributed Locks | Two guests, one room, the same millisecond. Optimistic vs pessimistic locking, database constraints as the real guard, idempotency keys, distributed locks and why they are the last resort. **Already fully grounded** — StayHub ships a Postgres `EXCLUDE` constraint (`bookings_no_overlapping_bookings`), a friendly pre-check, and `IntegrityError` disambiguation. Nothing to build. |
| 10 | `system-design-rate-limiting` | Rate Limiting | Token bucket, leaky bucket, fixed and sliding window, where the limiter belongs, distributed counters, and the `429` + `Retry-After` contract. **Needs the StayHub rate-limit addition.** |
| 15 | `system-design-airbnb` | Designing Airbnb | The full walkthrough — requirements, estimates, API, schema, search, availability, booking, payments, scale-up. Quotes StayHub throughout because StayHub *is* this system. |
| 16 | `system-design-amazon` | Designing Amazon | Catalog and search, cart, inventory reservation, checkout and order state, fulfilment, recommendations. Reuses the caching/queue/sharding primitives; catalog and inventory specifics are schema and pseudo-code. |
| 17 | `system-design-delta-airlines` | Designing an Airline Booking System (Delta) | Flight search over a graph of routes, fare and seat inventory, the seat-hold problem, overbooking, PNR/ticketing, GDS integration, irregular operations. The hold problem is the same one post 9 solves, at a harder scale. |

**Deliberately left out** (README: *"keep posts to the point"*): microservices vs monolith as its own
post (it is a section of post 2), service discovery, service mesh, Kubernetes, geo-proximity search,
consensus algorithms, blob storage internals, data pipelines. None of them are needed to answer the
questions this track sets out to answer.

---

## StayHub additions — build before writing

Decision 3. Three gaps, each one blocking a specific post. Everything else the track needs already
exists and runs.

| # | Addition | Blocks | Shape |
|---|---|---|---|
| A | **Redis + a cache layer** | post 5 (caching), post 15 (Airbnb) | Redis in `docker-compose.yml`, a `core/cache.py` with cache-aside get/set/invalidate, applied to property detail reads. Must degrade to a no-op when Redis is absent so the existing quickstart still runs. |
| B | **Rate limiting** | post 10 (rate limiting) | Token bucket over Redis in `core/middleware.py`, applied to auth and search. Returns `429` with `Retry-After` and the `X-RateLimit-*` headers. Same no-Redis degradation. |
| C | **A transactional outbox** | post 8 (queues), post 14 (notifications), post 7 (consistency) | An `outbox` table written in the same transaction as the booking, plus a drain worker. Replaces the "log it and hope" comment in `search/indexer.py` with a real retry path — that comment currently reads *"in production this is where you would enqueue a retry instead of only logging."* |

**Constraint from the README:** *"make sure they don't break the app."* All three are additive and
must degrade cleanly with no Redis running, because `stayhub/CLAUDE.md`'s documented quickstart is
`docker compose up -d` → postgres, hasura, elasticsearch. The 100 backend tests and both Playwright
suites must still pass unchanged.

### Already grounded — nothing to build

| Post | StayHub surface it quotes |
|---|---|
| 9 concurrency | `bookings_no_overlapping_bookings` EXCLUDE constraint · `booking_repository.overlapping()` · `_is_overlap_violation()` |
| 7 consistency | `search/indexer.py` — the Postgres → Elasticsearch sink in application code |
| 6 database scaling | `repositories/` · the BIGINT-PK / `public_id`-UUID split · Alembic migrations |
| 11 unique id | the same PK/UUID split, and why the API exposes only the UUID |
| 4 load balancing | the stateless JWT tier — one token, two APIs, no session store |
| 2 basics | `docker-compose.yml` — postgres · hasura · elasticsearch as the real moving parts |

### ✅ Done — 2026-08-22

All three built, wired, tested and run. Full detail in
`lovemesomecoding_demo_project/stayhub/progress_report.md`; the headline is that **the test count
went 100 → 165 and nothing regressed.**

| | files | applied to |
|---|---|---|
| A · Cache | `app/core/cache.py` | `GET /properties/{id}` — cache-aside, 5-min TTL, invalidated from `_sync` |
| B · Rate limit | `app/core/rate_limit.py` | `POST /auth/login` (10 / 5 min) · `GET /search` (60 / min) |
| C · Outbox | `app/models/outbox.py` · `app/services/outbox_service.py` · `scripts/drain_outbox.py` · migration `35c27e31465b` | `booking.created` · `booking.cancelled` · `property.changed` |

Plus `redis:7-alpine` on port 6380 in Compose, a `cache` boolean on `/health`, and a `headers`
field on `ApiException` so a 429 can carry `Retry-After`.

**The README's constraint held.** *"Make sure they don't break the app."* Verified both directions
on 2026-08-22:

| | result |
|---|---|
| Redis running | **165 passed** |
| `docker compose stop redis` | **142 passed, 23 skipped, 0 failed** |
| Elasticsearch stopped | **165 passed** |

### Numbers this track can quote, because they were measured here

Not repeated from a blog post — produced on the machine that wrote them, 2026-08-22.

| claim | measurement | post |
|---|---|---|
| Cache hit vs miss, over HTTP | **15.2ms → 2.0ms** | 5 caching |
| Cache hit vs miss, service layer | **8.8ms → 0.3ms** (~28×) | 5 caching |
| Token bucket is atomic | 50 concurrent threads, 20-token bucket → **exactly 20** allowed | 10 rate limiting |
| Retry budget | 2, 4, 8, 16, 32, 64, 128, 256s — 8 attempts over **~4.2 min**, then DEAD | 8 queues |
| Two workers, one queue | `SKIP LOCKED` → disjoint sets, **no blocking** (asserted <1s) | 8 queues |

### Three findings that became post material

Each one is a bug that a plausible implementation has and a test caught:

1. **A fail-open guarantee is only as wide as its narrowest `try`.** `check()` wrapped the Lua call
   but not `register_script`, so a misconfigured `redis_url` failed **closed** — every login 500ing,
   which is precisely the outcome the fail-open decision existed to prevent. → post 10.
2. **`FOR UPDATE` without `SKIP LOCKED`** makes worker B *wait* for A rather than take different
   rows, so a second worker adds zero throughput. The test asserts B returns empty **and fast**,
   because only the timing distinguishes the two. → post 8.
3. **Two delivery paths sent every guest two emails.** `BackgroundTasks` and the outbox both fired.
   Found by running the app, not by a test — and it is the cleanest possible illustration of
   at-least-once delivery, which post 8 now opens with. → posts 8 and 14.

## Standard workflow position

1. ✅ Clarify requirements — audit complete, four decisions taken
2. ✅ Shared context — this file
3. ✅ Topic table — 18 posts, above
4. n/a Frontend
5. ✅ **StayHub additions A/B/C — built, tested, run.** 100 → 165 tests, nothing regressed.
6. ✅ **All 18 posts written.** 60,968 words, every post 15–16 reading-minutes.
7. ✅ QA — `check_content.py` and `check_snippets.py` both green; independent structural sweep clean
8. ✅ Seeded local → seeded prod → built → deployed → verified live
9. ✅ Category record fixed on seed: `name` → "System Design", description written

### What the checkers caught while writing

Both checkers earned their keep on the first day, which is the argument for building them before
the posts rather than after:

- **`lua` was supported on neither side.** The rate-limiting post quotes the token-bucket `EVAL`
  script, and `lua` was in neither the backend's `SUPPORTED_LANGUAGES` nor the frontend's Prism
  imports. An unsupported language is silently normalised to `plaintext`, not rejected — so the
  block would have shipped unhighlighted with no error anywhere. Added to both.
- **Two mis-transcribed quotes.** `indexer.reindex_all(...)` where the real call is
  `indexer.rebuild_index(...)`, and a `rating_average` column written from memory with the wrong
  default and the wrong line breaks. Both were invisible prose-level errors that `check_snippets`
  found by byte comparison.
- **An unmarked elision.** `main.py` quoted with its `description=` block silently dropped —
  reported as drift until marked with the `...` elision marker.
- **A raw `<owner-token>` inside a `<pre>`.** Exactly the trap `CLAUDE.md` documents: a browser
  parses it as a tag. Escaped.
- **Two contradictory rules.** The "a rewrite must double" rule demanded 5,742 words of
  `system-design-basics` while the reading-time cap forbade more than 4,400. The check failed the
  post rather than the rule; the rule was wrong, and is now capped at the track floor. See
  `manifest.rewrite_floor`.
- **The word floor is a FAILURE on this track, not a warning.** Thinness is the defect being
  fixed, so a post landing under 3,300 words has reproduced the problem it was written to correct.
- **The prose CEILING earned its place.** `system-design-interview-questions` came in at 98% prose
  — a Q&A page with two code blocks — and the rule rejected it. That is the genre's besetting sin
  and precisely what the seven live posts do; the post now carries 15 diagrams.
- **`check_snippets.py` could not see attributed blocks.** Its `<pre class="language-X">` regex
  required an exact match, so any block carrying `data-antipattern` was invisible to it rather than
  excluded by it: not counted, not compared, absent from the totals. A genuinely drifted quote
  could have hidden behind any stray attribute. Caught because post 9 had four antipattern blocks
  in source and one in the report; the totals now reconcile against `check_content` (88 checked +
  197 skipped + 11 antipattern = 296). The published HTML was never affected —
  `content.normalize()` strips the attribute, so the marker is author-only metadata.

### Before writing, remember

- **`seed.py --force-dates` exactly once per tree.** All 7 existing posts carry 2018/2019/2023
  dates and `upsert_post` never overwrites a date. Without it the archive interleaves old and new
  and the pager reads nonsense.
- **The 7 slugs are frozen.** They are indexed URLs and `verify-build.mjs` fails the build if one
  stops resolving.
- **Diagrams are ASCII in `<pre class="language-plaintext">`.** Decision 2 drops all 35 raster
  screenshots.
- **Quote only code that has run.** Everything in the table above has; nothing else may be quoted
  as if it had.

## The finished track

All 18 pass both checkers. Measured off the written files, 2026-08-22:

| # | slug | words | min | prose% | h2+h3 | blocks | diagrams |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `system-design-introduction` | 3,381 | 15 | 82% | 14 | 12 | 9 |
| 2 | `system-design-basics` | 3,369 | 15 | 86% | 17 | 15 | 11 |
| 3 | `system-design-back-of-envelope-estimation` | 3,362 | 15 | 79% | 20 | 16 | 15 |
| 4 | `system-design-load-balancing` | 3,322 | 15 | 85% | 16 | 14 | 11 |
| 5 | `system-design-caching` | 3,340 | 15 | 86% | 18 | 15 | 7 |
| 6 | `system-design-database-scaling` | 3,422 | 16 | 80% | 23 | 17 | 10 |
| 7 | `system-design-consistency-and-availability` | 3,394 | 15 | 84% | 17 | 17 | 13 |
| 8 | `system-design-message-queues` | 3,360 | 15 | 84% | 16 | 18 | 5 |
| 9 | `system-design-concurrency-and-locking` | 3,451 | 16 | 81% | 17 | 23 | 6 |
| 10 | `system-design-rate-limiting` | 3,460 | 16 | 84% | 21 | 20 | 7 |
| 11 | `system-design-unique-id-generator` | 3,361 | 15 | 83% | 19 | 17 | 13 |
| 12 | `system-design-url-shortener` | 3,368 | 15 | 80% | 21 | 15 | 12 |
| 13 | `system-design-chat-system` | 3,361 | 15 | 77% | 16 | 16 | 14 |
| 14 | `system-design-notification-system` | 3,333 | 15 | 78% | 16 | 14 | 9 |
| 15 | `system-design-airbnb` | 3,344 | 15 | 77% | 17 | 19 | 10 |
| 16 | `system-design-amazon` | 3,429 | 16 | 75% | 17 | 16 | 10 |
| 17 | `system-design-delta-airlines` | 3,329 | 15 | 72% | 16 | 15 | 11 |
| 18 | `system-design-interview-questions` | 3,582 | 16 | 85% | 52 | 17 | 15 |
| | **total** | **60,968** | **277** | **81%** | **343** | **296** | **188** |

### Against the baseline

| | before | after |
|---|---:|---:|
| posts | 7 | 18 |
| words | 7,142 | 60,968 |
| reading-minutes | 34 | 277 |
| headings | **0** | 343 |
| code blocks | 2 | 296 |
| ASCII diagrams | 0 | 188 |
| raster screenshots | 35 | **0** |
| posts with tags | 0 | 18 |
| category display name | `system-design` | `System Design` |
| category description | *(empty)* | written |

### Snippet provenance

`check_snippets.py`: **48 of 88 checked blocks (55%) are quoted verbatim from code that runs**,
11 are marked antipatterns, 40 are illustrative, and there is **no drift**. The four posts with
zero verbatim quotes — url-shortener, chat, amazon, delta-airlines — declare empty
`SNIPPET_SOURCES` deliberately: they are not StayHub, so their content is SQL, diagrams and
sketches rather than Python passed off as real.

## Log

- **2026-08-22** — Audited the 7 live posts off the prod tree. Five defects confirmed: zero headings
  in 7,142 words, two code blocks total, 35 book screenshots, a broken category record, no tags.
  Audited StayHub for what the track can quote: no Redis, no rate limiting, no real queue — but the
  double-booking guard is already there and is better than what most tutorials show (a Postgres
  `EXCLUDE` constraint, not an application-level check). Four scope decisions taken.
- **2026-08-22** — Built StayHub additions A (cache), B (rate limiting) and C (transactional
  outbox). 100 → 165 tests. Verified the app still runs with Redis stopped and with Elasticsearch
  stopped. Measured the numbers the caching and rate-limiting posts quote. Found and fixed three
  real bugs along the way (fail-open hole, a test-isolation flaw, duplicate emails), all of which
  became post material. `stayhub/CLAUDE.md` and `stayhub/progress_report.md` updated.
- **2026-08-22** — Scaffolding built (`manifest.py`, `seed.py`, `check_content.py`,
  `check_snippets.py`), then all 18 posts written. Both checkers green, plus an independent
  structural sweep (unbalanced tags, raw tags inside code blocks, bad entities, placeholders):
  clean. Seeded to the **local** tree with `--force-dates`; archive holds 18, category count 18,
  category renamed. Every internal cross-link resolves to a slug in the manifest.

## Published — 2026-08-22

```
seed.py --env prod --write --force-dates    672 posts in the tree (was 661)
npm run sync-content                        pulled prod, indexes consistent
npm run build                               verify-build: 672/672 posts,
                                            42/42 category counts agree
./scripts/deploy.sh                         1757 files, edge fn republished,
                                            invalidation completed
                                            edge serves build 394b0bd  ✓
```

Verified live after deploy:

| check | result |
|---|---|
| 18 post URLs | all **200** |
| `/system-design` archive | 200, lists **18** distinct posts, titled "System Design" |
| `/sitemap.xml` | 200, contains all **18** system-design URLs |
| `system-design-url-shortener` (was 334 words, 4 screenshots, 0 headings) | 15 `h2`, 6 `h3`, **0 images**, 15 code blocks, no boldgrid markup |
| Prism highlighting | `lua` block highlighted — the language added to both sides for this track works end to end |
| Legacy redirects | `/feed`, `/java-8`, `/java-8/java-11-api-improvements` all still **301** |

### Rollback

The content-DB bucket has **no versioning**, so a snapshot was taken before writing:
`.backup-prod-2026-08-22/` holds the seven original post objects plus `index/posts.json`,
`index/categories.json`, `index/by-category/system-design.json` and `search/index.json`. It is
gitignored (a migration artifact) but must stay on disk until this track has clearly settled.

To roll back: copy those objects back to `s3://…/lovemesomecoding/prod/`, then rebuild and deploy
the frontend. Note that the eleven NEW slugs would then 404 — they are already in the sitemap, so a
rollback should also remove them from it by rebuilding after the restore.

### Notes from the publish

- **The admin console's Publish button still does not work.** `/lovemesomecoding/prod/github-token`
  is still absent from SSM (`ParameterNotFound`, checked 2026-08-22), so `repository_dispatch`
  cannot fire. This deploy went out via `npm run sync-content && npm run build && ./scripts/deploy.sh`
  from the frontend repo, which needs no PAT. The SSM task in the root `CLAUDE.md` is still open.
- **`NAV_GROUP` in the manifest said "Engineering" and was wrong.** `nav.ts` already lists
  `system-design` under **Software Engineering** with the display name "System Design", so there was
  nothing to add. Comment corrected; no code change was needed.
- **Diagrams render on a fixed dark palette in both themes.** `--code-bg` / `--code-text` are
  defined once on `:root` and not overridden per theme, and `.code-wrap pre` is `overflow-x: auto`.
  The widest ASCII diagram line in the track is 95 characters, so wide diagrams scroll inside their
  own block rather than breaking the page. Decision 2 holds in light and dark.

## Re-dated to 2022-2025 (2026-08-24)

The track shipped stamped `2026-08-24` + 2 days per lesson, which put all eighteen posts in the
future and clustered them inside five weeks. Re-based to **one lesson roughly every eleven weeks
across 2022-2025**: `START_DATE = 2022-01-18`, `STEP_DAYS = 82`, first post 2022-01-18, last
2025-11-12.

Two reasons beyond the ask. Future dates are not cosmetic here — archives and the sitemap sort
newest-first, so the whole track pinned itself to the top of the site and shipped `<lastmod>`
values that postdated the crawl. And seven of these URLs have genuinely been live since
2018/2019/2023, so a block of 2026 dates contradicted the pages' own history.

`manifest.DATE_RANGE` now asserts at import that the computed dates stay inside the window, so
moving `START_DATE` without meaning to leave it fails before it can be seeded.

### Dates inside the posts had to move too

Five posts quoted 2026 dates in code blocks, which a post dated 2023 cannot do. All were
illustrative or captured output, none were verbatim source quotes, and `check_snippets.py` still
reports no drift:

| post | was | now | why |
|---|---|---|---|
| database-scaling | `bookings_2026_q1/q2` | `bookings_2023_q1/q2` | post is 2023-03-04; the `DROP TABLE bookings_2019_q1` line still reads as old data |
| message-queues | `20260822T190807…` | `20230815T190807…` | terminal output from the duplicate-delivery run, dated to the post |
| notification-system | `20260822T190807…` | `20230815T190807…` | **same** timestamps deliberately — post 14 recalls the event from post 08, so they must match, and they belong to the earlier post's date |
| rate-limiting | `user:42:2026-08-22T14:31` | `user:42:2024-01-26T14:31` | fixed-window key example |
| delta-airlines | flight `2026-11-04` | `2025-11-04` | post is 2025-08-22; 15 months out is past the real booking window |

### ⚠️ `_reindex` lost six index updates, silently

Worth recording because nothing downstream would have caught it. The first re-seed wrote all
eighteen post objects correctly, but `index/posts.json` came back with **six entries still
carrying their old date** (`system-design-back-of-envelope-estimation`, `concurrency-and-locking`,
`airbnb`, `amazon`, `delta-airlines`, `interview-questions`) — their `modified` field was still the
2026-08-22 publish. `index/by-category/system-design.json` was completely correct.

`_reindex` is a read-modify-write of one file holding every published post (778 of them now), run
once per post in the loop. Re-running the seed converged it; the cause was not pinned down.

The dangerous part is that the drift is invisible to every existing guard. The category index was
right, so the category count still agreed, every URL still resolved, and `verify-build.mjs` passed
clean — including check 6, which cross-checks the indexes against each other. The only symptom
would have been six posts sorted to the wrong place in the site-wide archive and the sitemap, and
nothing looks at that.

`seed.py` now ends with `verify_indexes()`: re-read both indexes from S3, compare every date
against the post objects, repair once by re-upserting the drifted slugs, verify again, and exit
non-zero rather than let a build run on a bad index.

### `seed.py --republish`

The `new`-slug collision guard is a pre-publish guard and it expires the moment the track ships —
once the eleven new posts are live they exist on every subsequent run, so it fires on a correct
re-seed. `--republish` acknowledges they are ours now. It is deliberately not the default: the day
that guard is genuinely right is the day a typo'd slug would silently eat an unrelated post.

### Verified live

Post pages render "January 18, 2022" … "November 12, 2025"; the archive lists lesson order
(the category template sorts oldest-first, which is what a course wants); prev/next still walks
notification-system → airbnb → amazon; no `2026` remains in any post body — the only 2026 left on
a page is `dateModified` / "Updated 8/24/2026" / the footer copyright, all correct.

Deployed: 2013 files, 95 redirects, invalidation complete, edge serving build `394b0bd`.

**Unrelated but noticed:** the `vue` track is dated to 2026-11-21 and holds the site-wide newest
slots. If future-dating is not intentional there, it has the same sitemap `<lastmod>` problem this
change just fixed here.

## Lesson 14 added: Designing a Customer Data Platform (2026-08-29)

The track is now **19 posts**. `system-design-customer-data-platform` was written from a separate
design brief (see `projects/customer_data_platform/`) and slotted into the track.

### The date problem, and why the manifest grew a new mechanism
Folau asked for the post to carry a 2024 date. Dates here are COMPUTED from `START_DATE +
index * STEP_DAYS`, so an inserted post normally shifts every date after it — and all eighteen
existing posts are live with the 2022–2025 dates set on 2026-08-24. Re-dating them again to make
room for one post is churn on published pages for no reader benefit.

Three options were considered:

| Option | Cost |
|---|---|
| `STEP_DAYS` 82 → 80, 19 computed dates | Fits 2022–2025, but re-dates all 18 live posts |
| Append at the end with an explicit date | `check_content.py` fails: manifest dates must ascend |
| **Explicit date that skips the computed index** | **Zero change to any published post** ← chosen |

So `_build_posts()` replaced the POSTS comprehension: an entry carrying its own `"date"` uses it
verbatim **and does not consume a slot in the computed sequence**. Every other lesson keeps the
exact date it already had in prod — verified post-seed, all 18 unchanged.

The post sits at position 14 (`2024-11-08`), between `chat-system` (2024-09-28) and
`notification-system` (2024-12-19). Files 14–18 were renamed to 15–19; slugs and therefore URLs are
untouched.

### Other manifest changes
- `assert len(POSTS) == 19`.
- The DATE_RANGE assertion now checks **the dates POSTS actually carries**, not the computed
  endpoints. It had to: an explicitly dated entry never passes through `_date()`, so endpoint
  arithmetic cannot see it and would have asserted against a post that does not exist.
- `SNIPPET_SOURCES` entry is **empty**, following the Amazon and Delta precedent. This post is not
  StayHub — a CDP has no counterpart in a booking app — so its code is schema and Java presented as
  design. `check_snippets.py` skips Java (not in `SOURCE_LANGS`) and classes the SQL and JSON as
  illustrative, which is the honest result.

### Deviation worth flagging
This is the only post in the track whose code is **Java/Spring Boot** rather than FastAPI. That was
Folau's explicit instruction on the brief ("use springboot as the backend api", and "dont use any
demo app because none of them is a good fit"). It is a real inconsistency with the other eighteen,
recorded here rather than smoothed over.

### Verification
- `check_content.py` — all 19 pass. New post: 3,367 words, 65% prose, 7 plaintext diagrams, 15 min.
- `check_snippets.py` — "no drift". 48/90 checked blocks quoted from running code.
- `seed.py --env prod --republish --write` — 18 updates, 1 create; 873 posts in the tree;
  "indexes verified: all 19 posts agree" (no `_reindex` drift this run).
- `npm run deploy` — 873/873 posts, 42/42 categories agree, 2,239 files, build `42a2593` at the edge.
- Live: page returns 200, renders "November 8, 2024", Java blocks are Prism-highlighted, the archive
  lists it 14th in lesson order, the pager walks chat-system → CDP → notification-system, and the
  sitemap carries the URL.

---

## Lesson 19 added: Designing YouTube (2026-08-31)

Folau asked for a YouTube design post, then mid-write added **"include adds and marketing"** — so
advertising and the distribution machinery are designed here as first-class parts of the system
rather than an appendix. That instruction shaped the post: steps 7 and 9 (ads, marketing) are the
two longest sections, and the ad decision appears in the architecture diagram as a *sibling* of
playback rather than a step inside it.

### Where it goes and why

Position **19**, between `delta-airlines` (2025-08-22) and `interview-questions` (2025-11-12).
The interview post has to stay last — it is the wrap-up and it links to everything above it — so
"append at the end" was never available.

That forced the same date problem as lesson 14, and the mechanism built then solved it unchanged:

| | |
|---|---|
| Computed slot after `interview-questions` | 2026-02-02 — outside `DATE_RANGE`, and in the future |
| Shrink `STEP_DAYS` to fit | re-dates all 19 live posts |
| **Explicit date, skipping the computed index** | **zero change to any published date** ← used |

`"date": "2025-10-08T09:00:00"`. `_build_posts()` already skips explicit entries when advancing the
computed sequence, so every other lesson kept the exact date it had in prod — confirmed against the
seed output. This is now the **second** hand-dated entry; if a third is ever needed the mechanism
scales, but the comment on each explicit date should keep saying *why* it is explicit.

`file` still numbers by list position, so `19-system-design-interview-questions.html` was
`git mv`d to `20-`. Slug unchanged, so the indexed URL is untouched.

### Two cross-references had to move with it

Inserting a post before the last one breaks the chain the posts state in prose, and neither of
these is caught by any check:

- `delta-airlines` ended **"Next, and last: the interview questions"**. It now points at YouTube,
  and the "and last" is gone. Left uncaught this would have been a live page telling readers the
  track ends one post early.
- `interview-questions` opened with "it assumes the other **seventeen**". That was *already* stale —
  lesson 14 made it eighteen and nobody updated it — so it is now "the other **nineteen**". Worth
  noting as a standing hazard: prose that counts the track goes stale on every insertion, and
  `check_content.py` cannot see it. A grep for spelled-out numbers is the cheapest guard before any
  future insertion.

`manifest.CATEGORY["description"]` also gained YouTube in its list of walkthroughs, because
`upsert_category` rewrites the stored standfirst from the manifest on every seed.

### Content decisions

- **`SNIPPET_SOURCES` is empty**, the Amazon/Delta/URL-shortener footing. Nothing in StayHub
  transcodes video or runs an ad auction, so the post is SQL, JSON contracts and ASCII diagrams —
  no Python pretending to come out of a repository. `check_snippets.py` reports 2 illustrative
  blocks and no drift.
- **No Java this time.** Lesson 14 used Spring Boot because Folau asked for it there specifically;
  that instruction did not carry over, so this post returns to the track's convention.
- Deliberately avoided the words `measured`/`benchmark` and any `N ms` figure. Every number on the
  page is arithmetic the reader can check (uploads/day → TB/day → Tbps), which
  `CLAIMS_MEASUREMENT` correctly does not fire on. Nothing here was run on this machine and the
  post must not imply otherwise.
- The estimate is the load-bearing section: **egress is ~300x ingest**, ~17 Tbps at peak, which is
  what makes "almost no watch traffic may reach your servers" a conclusion rather than an opinion.
- Ads coverage: cue points fixed at transcode, decision in parallel under a hard deadline with
  `"fill": false` as a normal answer, SSAI vs CSAI with the cache cost quantified (the manifest is
  kilobytes; the segments stay shared), and impression billing deduped on a **server-minted**
  `decision_id` so a replayed beacon collapses rather than double-charging.
- Marketing coverage: offline candidates + online ranking, subscription fan-out spread over
  minutes, stored experiment assignment (not `hash(user) % 2`), and the **one shared frequency cap**
  across ads, pushes and campaigns — the cheapest thing to design up front and the most expensive
  to retrofit.

### Verification

```
check_content.py    all 20 pass — youtube 4,240 words / 19 min / 63% prose / 14 plaintext blocks
check_snippets.py   no drift; 48/92 checked blocks quoted from running code
seed.py --env prod --republish --write
                    20 posts, 874 in tree (was 873)
                    indexes verified: all 20 posts agree
npm run deploy      874/874 posts, 42/42 category counts agree, 2,241 files, build 42a2593
live                200, "October 8, 2025", 2 json / 2 sql / 28 plaintext blocks,
                    82 prism keyword tokens, pager reads
                    ‹ Airline Booking System · Interview Questions ›
```

At 19 minutes it is the longest post in the track, and the only one above 18 — the ads and
marketing sections are the extra four minutes. It is inside the 15-20 budget with 160 words of
headroom under the cap.

## Still to do

1. **Submit the sitemap to Search Console** if the eleven new URLs should be indexed promptly.
   (The root `CLAUDE.md` already lists sitemap submission as an open task.) Note the re-dating
   changed only `date`, not the URLs, so nothing needs re-submitting on account of it.
2. **Commit.** Three repos, three separate commits:
   - `claude_lovemesomecoding` — `projects/system_design/` (this track)
   - `lovemesomecoding_demo_project` — the StayHub cache/rate-limit/outbox work
   - `lovemesomecoding_frontend` + `lovemesomecoding_backend` — the one-line `lua` addition each.
     ⚠️ Both of those repos also carry **pre-existing uncommitted changes from earlier tracks**
     (typescript/scss/nginx/graphql languages, `schemas.py`, `posts.py`, deploy scripts). Those are
     not from this work and should not be swept into a commit for it.

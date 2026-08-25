"""The System Design track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend
with the track and the last lesson is the newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because this track is
authored before it is published: move START_DATE and every lesson re-bases in order, still
ascending, with no chance of a hand-typed date landing out of sequence.

⚠️ SEVEN of these eighteen slugs are not new. `/system-design` has been live since 2018 and every
one of its URLs is indexed. They are being rewritten IN PLACE, not replaced: changing one of those
slugs changes a live URL, and `verify-build.mjs` fails the frontend build when an indexed post URL
stops resolving.

Because `upsert_post` never overwrites an existing date, seeding needs `seed.py --force-dates`
or the archive interleaves the seven original 2018/2019/2023 dates with the computed ones and the
pager reads nonsense. That applies to a date CHANGE too, not just the first seed: all eighteen now
carry a stored date, so re-basing the track means --force-dates again. See progress_report.md.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "system-design",
    # ⚠️ The stored record currently says "system-design" in lowercase with an EMPTY description.
    # upsert_category rewrites both from here, which is the only reason the archive page gets a
    # display name and a standfirst at all.
    "name": "System Design",
    "description": (
        "System design from the parts list to the whiteboard — estimation, load balancing, "
        "caching, database scaling, consistency, queues, concurrency and rate limiting, then "
        "full walkthroughs of Airbnb, Amazon, an airline booking system, a URL shortener, chat "
        "and notifications. Every mechanism is shown working in a real booking application "
        "rather than described, and every number quoted was measured on the machine that wrote "
        "it."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself lives in
# lovemesomecoding_frontend/src/lib/nav.ts, which ALREADY lists `system-design` under the
# "Software Engineering" group with the display name "System Design" — verified 2026-08-22.
# Nothing to add there.
NAV_GROUP = "Software Engineering"

# The app every code sample is taken from.
DEMO_APP = "lovemesomecoding_demo_project/stayhub/stayhub-fastapi-backend"

# ---------------------------------------------------------------------------
# Versions — READ OFF THIS MACHINE, not chosen
# ---------------------------------------------------------------------------
VERSIONS = {
    "python": "3.12.4",
    "fastapi": "0.115.5",
    "sqlalchemy": "2.0.36",
    "postgres": "16 (postgres:16-alpine)",
    "redis": "7 (redis:7-alpine), redis-py 5.2.1",
    "elasticsearch": "8.15.3 (client 8.15.1)",
    "hasura": "v2 (graphql-engine)",
    "docker engine": "27.4.0",
    "host": "Docker Desktop on aarch64 (Apple Silicon)",
}

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together, then
# `readingMinutes = max(1, round(words / 220))`. See lovemesomecoding_backend/app/services/
# content.py. Budgeting prose alone silently doubles the published reading time.
#
# Folau asked for 15-20 reading-minutes, so:
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (15, 20)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 3,300
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 4,400

# ⚠️ A prose FLOOR, as on every other track — but this one also needs a prose CEILING, and that is
# specific to system design.
#
# The failure mode here is the opposite of the FastAPI track's. There, posts were code dumps with
# captions (code was 75% of the words). System design invites the reverse: paragraphs of received
# wisdom about scalability with nothing you could run, check or disagree with. That is the genre's
# besetting sin and it is what the current seven posts already do.
#
# So: at least 45% prose (not a listing), and at most 88% (something concrete is on the page).
MIN_PROSE_SHARE = 0.45
MAX_PROSE_SHARE = 0.88

# ⚠️ AND a diagram floor. A system design post with no picture of the system is a post that has
# not done its job — and since decision 2 dropped all 35 raster screenshots, the pictures are
# ASCII in <pre class="language-plaintext">. check_content.py counts them.
MIN_PLAINTEXT_BLOCKS = 1

# What the collection looks like TODAY, measured off the prod tree on 2026-08-22. This is the
# baseline the rewrite has to beat, and check_content.py reports against it.
#
# ⚠️ Note the direction. On the FastAPI track a rewrite had to SHRINK; here every one of the seven
# has to GROW, because the defect is thinness. `system-design-url-shortener` is 334 words with
# four screenshots and no headings at all.
EXISTING = {
    #                                     prose,  code, total, minutes, images, h2, h3
    "system-design-basics":              (2871,    0,  2871, 13, 15, 0, 0),
    "system-design-chat-system":         (1223,    0,  1223,  6,  7, 0, 0),
    "system-design-interview-questions":  (878,    0,   878,  4,  0, 0, 0),
    "system-design-notification-system":  (780,   34,   780,  4,  3, 0, 0),
    "system-design-introduction":         (674,    0,   674,  3,  3, 0, 0),
    "system-design-unique-id-generator":  (382,    0,   382,  2,  3, 0, 0),
    "system-design-url-shortener":        (334,    0,   334,  2,  4, 0, 0),
}

# ⚠️ A flat "must double" rule was tried first and was WRONG, in a way worth recording because it
# looked obviously right.
#
# Six of the seven live posts are tiny — `system-design-url-shortener` is 334 words — so doubling
# is a trivially low bar for them and the real floor is the track's own TOTAL_WORDS_MIN of 3,300.
# But `system-design-basics` is 2,871 words, and doubling THAT demands 5,742 — which the 4,400
# cap forbids. The two rules contradicted each other on exactly one post, and the check failed the
# post rather than the rule.
#
# So the growth requirement is capped at the track floor: a rewrite has to reach 3,300 words like
# everything else, and for the thin six that already is roughly a doubling or far more. A rewrite
# coming out SMALLER than the page it replaces is still a hard failure, because that could only
# mean the thinness was not addressed at all.
REWRITE_MIN_GROWTH = 2.0


def rewrite_floor(baseline: int) -> int:
    """Words a rewrite of a `baseline`-word live page must reach."""
    return min(int(baseline * REWRITE_MIN_GROWTH), TOTAL_WORDS_MIN)

# ---------------------------------------------------------------------------
# Measured facts — quoted by posts, held here so they cannot drift
# ---------------------------------------------------------------------------
# Every number a post states about performance comes from this block. Written down once because a
# figure repeated in prose in three posts is a figure that disagrees with itself within a month,
# and because check_content.py can then assert that a post which CLAIMS a measurement quotes one
# of these.
#
# ⚠️ ALL of these were produced on 2026-08-22 by running the StayHub stack on this machine — see
# lovemesomecoding_demo_project/stayhub/progress_report.md. None is repeated from a book or a
# blog post. If a post wants a number that is not here, measure it and add it here first.
MEASURED = {
    # curl against `GET /api/v1/properties/{id}`, uvicorn on localhost, 4 consecutive requests
    # with the Redis key deleted first.
    "cache_http_cold_ms": 15.2,
    "cache_http_warm_ms": 2.0,
    # The same read at the service layer, without HTTP framing — PropertyService.get_public_view.
    "cache_service_cold_ms": 8.8,
    "cache_service_warm_ms": 0.3,
    "cache_speedup": "28x",
    "cache_ttl_seconds": 300,

    # 50 threads through ThreadPoolExecutor against one 20-token bucket, capacity 20, window
    # 3600s so refill cannot mask a lost update. tests/test_rate_limit.py::TestAtomicity.
    "limiter_threads": 50,
    "limiter_capacity": 20,
    "limiter_allowed": 20,
    # The configured production limits.
    "limit_login": "10 requests per 5 minutes",
    "limit_search": "60 requests per minute",

    # outbox_service.backoff_for(1..8), and the sum of the first seven waits.
    "backoff_sequence": "2, 4, 8, 16, 32, 64, 128, 256 seconds",
    "backoff_total_seconds": 254,
    "outbox_max_attempts": 8,

    # The StayHub test suite, run three ways on 2026-08-22.
    "tests_with_redis": 165,
    "tests_without_redis_passed": 142,
    "tests_without_redis_skipped": 23,

    # Row counts in the seeded local database, used by the estimation post so its arithmetic
    # starts from something real.
    "seed_listings": 12,
    "seed_users": 4,
}

# Strings that must appear literally in a post that makes the corresponding argument. If the
# argument rests on a number, the number has to be on the page.
MUST_CITE = {
    "system-design-caching": ["15.2", "2.0"],
    "system-design-rate-limiting": ["50", "20"],
    "system-design-message-queues": ["2, 4, 8, 16, 32, 64, 128, 256"],
}

# ---------------------------------------------------------------------------
# Where each post's snippets come from
# ---------------------------------------------------------------------------
# check_snippets.py reads these files out of DEMO_APP and verifies that every quoted block appears
# in one of them, byte for byte. A post quoting code that is not in its list fails.
#
# ⚠️ SOME LISTS ARE DELIBERATELY EMPTY, and that is the honest half of decision 3. Amazon and
# Delta are not StayHub — their catalog, inventory and seat-hold specifics are schema and
# pseudo-code, presented as design rather than as something running here. An empty list says "this
# post quotes nothing from the demo app", and check_snippets then requires that its code blocks
# are SQL, plaintext or clearly-marked sketches rather than Python passed off as real.
# A block deliberately showing the WRONG way — the check-then-write race, the racy limiter, the
# line after the commit — carries `data-antipattern` on its <pre> and is excluded from the
# verbatim check. This track needs the marker more than any other: half of what it teaches is a
# plausible implementation and the reason it fails.
ANTIPATTERN_MARKER = "data-antipattern"

SNIPPET_SOURCES = {
    "system-design-introduction": ["app/main.py"],
    "system-design-basics": [
        "app/main.py", "app/core/config.py", "app/search/indexer.py", "app/core/cache.py",
        "app/core/security.py", "app/services/property_service.py",
    ],
    "system-design-back-of-envelope-estimation": [
        "app/models/property.py", "app/models/booking.py",
    ],
    "system-design-load-balancing": [
        "app/core/security.py", "app/core/deps.py", "app/main.py",
    ],
    "system-design-caching": [
        "app/core/cache.py", "app/services/property_service.py",
        "app/api/v1/routes/properties.py", "app/core/config.py", "app/main.py",
        # The negative-caching test. Quoting the TEST rather than the code is deliberate here:
        # the post's claim is about behaviour that is deliberately absent, and an assertion is the
        # only honest way to show that something does not happen.
        "tests/test_cache.py",
    ],
    "system-design-database-scaling": [
        "app/models/booking.py", "app/models/property.py", "app/db/session.py",
        "app/repositories/booking_repository.py", "app/db/base.py",
        "app/services/property_service.py",
    ],
    "system-design-consistency-and-availability": [
        "app/search/indexer.py", "app/services/property_service.py",
        "app/models/outbox.py", "app/main.py",
    ],
    "system-design-message-queues": [
        "app/models/outbox.py", "app/services/outbox_service.py",
        "app/services/booking_service.py", "scripts/drain_outbox.py",
        "app/services/notification_service.py",
        # The SKIP LOCKED timing assertion. Quoting the test is the point there: the difference
        # between waiting and skipping is only visible on the clock.
        "tests/test_outbox.py",
        # The index-retry enqueue, quoted to show where the outbox does NOT reach.
        "app/services/property_service.py",
    ],
    "system-design-concurrency-and-locking": [
        "app/services/booking_service.py", "app/repositories/booking_repository.py",
        "app/models/booking.py", "app/models/enums.py",
        # The concurrency test — the only honest way to show a race is an assertion that fails
        # against the racy version.
        "tests/test_rate_limit.py", "app/core/rate_limit.py",
    ],
    "system-design-rate-limiting": [
        "app/core/rate_limit.py", "app/core/deps.py", "app/core/config.py",
        "app/core/exceptions.py", "tests/test_rate_limit.py",
    ],
    "system-design-unique-id-generator": [
        "app/db/base.py", "app/models/property.py",
    ],
    "system-design-url-shortener": [],
    "system-design-chat-system": [],
    "system-design-notification-system": [
        "app/services/notification_service.py", "app/services/outbox_service.py",
        "app/models/outbox.py", "app/services/booking_service.py",
    ],
    "system-design-airbnb": [
        "app/models/property.py", "app/models/booking.py", "app/services/booking_service.py",
        "app/services/pricing_service.py", "app/search/indexer.py", "app/search/queries.py",
        "app/core/cache.py", "app/main.py", "app/services/cancellation_policy.py",
        "app/api/v1/routes/bookings.py", "app/repositories/booking_repository.py",
        "app/services/property_service.py",
    ],
    "system-design-amazon": [],
    "system-design-delta-airlines": [],
    "system-design-interview-questions": [],
}

# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
# Teaching order: what a system is made of, how each part scales, then the case studies that
# assemble the parts, then the interview post.

_TRACK = [
    # ------------------------------------------------------------- foundations
    {
        "slug": "system-design-introduction",
        "title": "System Design – Where to Start",
        "state": "rewrite",
        "tags": ["system-design", "interview"],
        "excerpt": (
            "What system design actually is, why the question has no single right answer, and "
            "the four-step framework that keeps an hour from wandering: scope the requirements, "
            "estimate the load, sketch a high-level design, then go deep on the part that "
            "matters. What an interviewer is really scoring, the mistakes that sink candidates "
            "who know the material, and how the rest of this track is ordered."
        ),
    },
    {
        "slug": "system-design-basics",
        "title": "System Design Basics – The Parts of a Production System",
        "state": "rewrite",
        "tags": ["system-design", "architecture"],
        "excerpt": (
            "Every box on the whiteboard, named and justified: DNS, CDN, load balancer, a "
            "stateless web tier, cache, primary and replica databases, a message queue, object "
            "storage, and the logging and metrics that tell you which one is broken. Built up "
            "from a single server to a system that survives real traffic, with the reason each "
            "part gets added at the point it stops being optional — plus where a monolith is "
            "still the right answer."
        ),
    },
    {
        "slug": "system-design-back-of-envelope-estimation",
        "title": "Back-of-the-Envelope Estimation",
        "state": "new",
        "tags": ["system-design", "interview"],
        "excerpt": (
            "The step most candidates skip and most interviewers weight heavily. Powers of two "
            "and the latency numbers worth memorising, then the arithmetic that turns \"design "
            "Airbnb\" into concrete QPS, storage and bandwidth figures — worked end to end from "
            "real row counts. How to size a cache, when a number tells you the design is wrong, "
            "and why being an order of magnitude out is fine but a thousand times out is not."
        ),
    },
    {
        "slug": "system-design-load-balancing",
        "title": "Load Balancing and the Stateless Tier",
        "state": "new",
        "tags": ["system-design", "architecture", "scalability"],
        "excerpt": (
            "Getting a request to a server that can answer it — and, better, not sending it at "
            "all. Layer 4 versus layer 7, round robin against least connections, health checks "
            "that actually detect a sick instance, and why sticky sessions are a trap rather "
            "than a feature. What \"stateless\" really requires of your application, how a JWT "
            "delivers it, and where a CDN removes the request entirely."
        ),
    },
    {
        "slug": "system-design-caching",
        "title": "Caching – Patterns, Invalidation and What Breaks",
        "state": "new",
        "tags": ["system-design", "redis", "performance"],
        "excerpt": (
            "A cache-aside read on a real endpoint, measured cold and warm, then everything that "
            "makes caching hard rather than easy. Write-through against write-behind, TTL and "
            "eviction policies, the two invalidation strategies and why you want both, cache "
            "stampede and how to stop it, and the rule that decides whether a cache is an "
            "optimisation or a new single point of failure."
        ),
    },
    {
        "slug": "system-design-database-scaling",
        "title": "Scaling the Database",
        "state": "new",
        "tags": ["system-design", "database", "scalability"],
        "excerpt": (
            "The order to do things in, because most systems reach for sharding several steps "
            "too early. Indexes and query plans, connection pooling, read replicas and the "
            "replica lag that breaks read-your-writes, vertical against horizontal, partitioning "
            "versus sharding, choosing a shard key you will not regret, hot shards, and what "
            "resharding actually costs once you are live."
        ),
    },
    {
        "slug": "system-design-consistency-and-availability",
        "title": "Consistency, Availability and CAP",
        "state": "new",
        "tags": ["system-design", "distributed-systems"],
        "excerpt": (
            "CAP without the folklore — what the theorem says, what it does not say, and why "
            "PACELC is the more useful version day to day. Strong against eventual consistency, "
            "read-your-writes and monotonic reads, quorums, and the dual-write problem that "
            "appears the moment a second datastore enters the design. Shown against a live "
            "Postgres-to-Elasticsearch sink, including exactly where it goes wrong."
        ),
    },
    {
        "slug": "system-design-message-queues",
        "title": "Message Queues and Asynchronous Work",
        "state": "new",
        "tags": ["system-design", "distributed-systems", "architecture"],
        "excerpt": (
            "Why the line after a commit is the most dangerous line in the file, and what to do "
            "about it. Queues against logs, at-least-once delivery and the idempotency it "
            "forces, the transactional outbox, retries with exponential backoff, dead-letter "
            "queues, and how a worker claims work without two workers doing it twice. Every "
            "piece taken from a queue that runs, including the duplicate it produced."
        ),
    },
    {
        "slug": "system-design-concurrency-and-locking",
        "title": "Concurrency – Double Booking and Distributed Locks",
        "state": "new",
        "tags": ["system-design", "database", "concurrency"],
        "excerpt": (
            "Two guests, one room, the same millisecond. Why the check-then-write everyone "
            "writes first is always wrong, optimistic against pessimistic locking, the database "
            "constraints that make a race impossible rather than unlikely, idempotency keys for "
            "requests that must not run twice, and distributed locks — what they cost, how they "
            "fail, and why they belong last on the list rather than first."
        ),
    },
    {
        "slug": "system-design-rate-limiting",
        "title": "Rate Limiting",
        "state": "new",
        "tags": ["system-design", "redis", "security"],
        "excerpt": (
            "Four algorithms and what each one does at the boundary: fixed window and its "
            "doubling bug, sliding log, sliding window counter, and the token bucket that wins "
            "most of the time. Where the limiter belongs, how to identify a caller without "
            "handing them a way to reset their own quota, why the counter must be atomic, and "
            "the 429 contract a client can actually back off against."
        ),
    },
    {
        "slug": "system-design-unique-id-generator",
        "title": "Designing a Unique ID Generator",
        "state": "rewrite",
        "tags": ["system-design", "distributed-systems"],
        "excerpt": (
            "Four ways to mint an id at scale and the single tradeoff that decides between them: "
            "sortability against coordination. Database auto-increment, UUIDv4 and v7, a ticket "
            "server, and Snowflake — with the bit layout worked through, the clock-skew failure "
            "everyone forgets, and why a system can want two ids for the same row rather than "
            "one."
        ),
    },
    # ------------------------------------------------------------ case studies
    {
        "slug": "system-design-url-shortener",
        "title": "Designing a URL Shortener",
        "state": "rewrite",
        "tags": ["system-design", "interview"],
        "excerpt": (
            "The classic warm-up question, worked properly. Requirements and estimates, base62 "
            "encoding against hash-and-truncate, how to handle collisions without a retry loop "
            "that never terminates, the 301-versus-302 decision that also decides whether you "
            "get analytics, the read path and its cache, custom aliases, and expiry that does "
            "not require scanning the table."
        ),
    },
    {
        "slug": "system-design-chat-system",
        "title": "Designing a Chat System",
        "state": "rewrite",
        "tags": ["system-design", "websockets"],
        "excerpt": (
            "Real-time messaging end to end. Polling, long polling, server-sent events and "
            "WebSockets — what each costs and when each is right; the connection registry that "
            "lets one server find a user connected to another; message ordering when clocks "
            "disagree; storage that supports \"load older messages\" cheaply; group chat fan-out "
            "and the point at which it stops working; presence, delivery receipts and offline "
            "delivery."
        ),
    },
    {
        "slug": "system-design-notification-system",
        "title": "Designing a Notification System",
        "state": "rewrite",
        "tags": ["system-design", "architecture"],
        "excerpt": (
            "One system, three channels, and every hard part in the delivery guarantees. "
            "Provider abstraction so a failing vendor is a config change, fan-out that survives "
            "a burst, retries and deduplication when delivery is at-least-once, the preference "
            "and opt-out rules that are a legal requirement rather than a feature, rate control "
            "so a bug cannot send ten thousand emails, and the templating that keeps copy out of "
            "code."
        ),
    },
    {
        "slug": "system-design-airbnb",
        "title": "Designing Airbnb",
        "state": "new",
        "tags": ["system-design", "interview", "case-study"],
        "excerpt": (
            "The full walkthrough, and the one case study where every claim is backed by a "
            "running application. Requirements and estimates, the API and the schema, search "
            "over a denormalised index, availability and the booking race, pricing as a security "
            "boundary, payments and the webhook that is the real source of truth, cancellation "
            "policy, then how each piece changes when the traffic multiplies."
        ),
    },
    {
        "slug": "system-design-amazon",
        "title": "Designing Amazon",
        "state": "new",
        "tags": ["system-design", "interview", "case-study"],
        "excerpt": (
            "An e-commerce system at the scale where every easy answer stops working. Catalog "
            "modelling for wildly different product types, search and faceting, the cart that "
            "must survive a logout, inventory reservation and oversell, the order state machine "
            "and why payment is a saga rather than a transaction, fulfilment across warehouses, "
            "and recommendations that are computed offline rather than at request time."
        ),
    },
    {
        "slug": "system-design-delta-airlines",
        "title": "Designing an Airline Booking System",
        "state": "new",
        "tags": ["system-design", "interview", "case-study"],
        "excerpt": (
            "Flight booking, which is the seat-hold problem from the concurrency post at a much "
            "harder scale. Searching a graph of routes rather than a list of rows, fare classes "
            "and the inventory buckets that make pricing possible, holding a seat while payment "
            "completes, deliberate overbooking as a business rule, PNRs and ticketing, "
            "integration with systems older than the web, and what happens when a storm cancels "
            "four hundred flights at once."
        ),
    },
    {
        "slug": "system-design-interview-questions",
        "title": "System Design Interview Questions",
        "state": "rewrite",
        "tags": ["system-design", "interview"],
        "excerpt": (
            "The questions you need to be able to answer, with answers that are short enough to "
            "say out loud. Fundamentals, scaling, data, distributed systems and the case-study "
            "openers — each answered in a few sentences, each linked to the post that works it "
            "through properly, and each followed by the follow-up an interviewer actually asks "
            "next."
        ),
    },
]

# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------
# The track is dated across 2022-2025 rather than published all at once, because eighteen posts
# stamped within a few weeks of each other read as a bulk dump — and seven of them have genuinely
# been live since 2018/2019/2023, so a cluster of 2026 dates also contradicted the pages' own
# history. One lesson roughly every eleven weeks reads like a series built up over four years.
#
# Every date must stay in the PAST. A future date is not cosmetic here: archives and the sitemap
# sort newest-first, so a post dated ahead of today pins itself to the top of /system-design and
# ships a <lastmod> that postdates the crawl.
START_DATE = datetime(2022, 1, 18, 9, 0, 0)
STEP_DAYS = 82

# Inclusive bounds the computed dates have to land inside. Asserted below, so moving START_DATE or
# STEP_DAYS without meaning to leave the window fails at import rather than at publish.
DATE_RANGE = (datetime(2022, 1, 1), datetime(2025, 12, 31, 23, 59, 59))


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=index * STEP_DAYS)).strftime("%Y-%m-%dT%H:%M:%S")


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

# Slugs that already exist on the live site and must never change. All seven predate this rewrite;
# check_content.py fails if one leaves the manifest, and seed.py refuses to write to prod if one is
# missing from the target tree.
FROZEN_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "rewrite"}

NEW_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "new"}

assert FROZEN_SLUGS == set(EXISTING), (
    "the frozen slugs and the measured baseline must describe the same seven posts: "
    f"{FROZEN_SLUGS ^ set(EXISTING)}"
)
assert len(POSTS) == 18, f"the track is 18 posts, got {len(POSTS)}"

_first = START_DATE
_last = START_DATE + timedelta(days=(len(POSTS) - 1) * STEP_DAYS)
assert DATE_RANGE[0] <= _first and _last <= DATE_RANGE[1], (
    "the computed post dates must stay inside DATE_RANGE: "
    f"{_first:%Y-%m-%d}..{_last:%Y-%m-%d} vs "
    f"{DATE_RANGE[0]:%Y-%m-%d}..{DATE_RANGE[1]:%Y-%m-%d}"
)
assert set(SNIPPET_SOURCES) == {e["slug"] for e in _TRACK}, (
    "every post needs a SNIPPET_SOURCES entry, even an empty one: "
    f"{set(SNIPPET_SOURCES) ^ {e['slug'] for e in _TRACK}}"
)

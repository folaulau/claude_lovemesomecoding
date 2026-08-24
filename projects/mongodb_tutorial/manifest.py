"""The MongoDB track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend
with the track and the last lesson is the newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because this track is
authored before it is published: when the publish date is finally known, move START_DATE and every
lesson re-bases in order.

⚠️ THREE of these sixteen slugs are not new. `/mongodb` was published in July 2019 and all three
of its URLs are indexed. They are being rewritten IN PLACE, not replaced: changing one of those
slugs changes a live URL, and `verify-build.mjs` fails the frontend build when an indexed post URL
stops resolving.

Because all three carry 2019 dates and `upsert_post` never overwrites an existing date, seeding
needs `seed.py --force-dates` or the archive interleaves three 2019 posts with thirteen 2024-25
ones and the pager reads nonsense. The same applies to any later re-base of START_DATE: once a post
is published its stored date is sticky. See progress_report.md.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "mongodb",
    # ⚠️ The stored record currently says "mongodb" in lowercase with an EMPTY description.
    # upsert_category rewrites both from here, which is the only reason the archive page gets a
    # display name and a standfirst at all.
    "name": "MongoDB",
    "description": (
        "MongoDB from a first document to a schema you can defend in review — documents and BSON "
        "types, CRUD and query operators, when to embed and when to reference, indexes and the ESR "
        "rule, the aggregation pipeline, transactions, replication, change streams and Spring Data. "
        "Every example is taken from a real short-video CMS, and the measurements come from the "
        "machine that wrote them rather than from a marketing page."
    ),
}

# Where the category sits in the site navigation, for reference. nav.ts already lists `mongodb`
# under the Data Store group (line 18) and already maps it to the display name "MongoDB"
# (line 51) — nothing to add there.
NAV_GROUP = "Data Store"

# The app every code sample is taken from. Built in the same session as this track, and its own
# CLAUDE.md states that producing snippets for this site is why it exists.
DEMO_APP = "lovemesomecoding_demo_project/reelcms"
DEMO_BACKEND = f"{DEMO_APP}/reelcms-springboot-backend"

# ---------------------------------------------------------------------------
# Dates — CONSTRAINED TO 2024-2025
# ---------------------------------------------------------------------------
# Folau's requirement: every post date must fall between 2024 and 2025. Sixteen posts at a 21-day
# step from 2024-09-03 lands the last one on 2025-07-15, so the whole track sits inside the window
# and still reads as a course in order.
#
# ⚠️ Changing STEP_DAYS or START_DATE can push the tail out of 2025. check_content.py asserts the
# window, so a re-base that breaks it fails the check rather than shipping.
START_DATE = datetime(2024, 9, 3, 9, 0, 0)
STEP_DAYS = 21
DATE_WINDOW = (datetime(2024, 1, 1), datetime(2025, 12, 31, 23, 59, 59))

# ---------------------------------------------------------------------------
# Versions — READ OFF THIS MACHINE, not chosen
# ---------------------------------------------------------------------------
# `mvnw dependency:list`, `mongosh --eval db.version()`, `java -version`, `docker --version`,
# taken 2026-08-24 with the ReelCMS stack up and its 91 tests passing.
VERSIONS = {
    "mongodb": "8.0.29 (single-node replica set rs0)",
    "java": "21.0.7 LTS",
    "spring-boot": "4.1.0",
    "spring-data-mongodb": "5.1.0",
    "mongodb-driver-sync": "5.8.0",
    "bson": "5.8.0",
    "lombok": "1.18.46",
    "vue": "3.5.41",
    "vite": "8.2.2",
    "bootstrap": "5.3.8",
    "docker engine": "27.4.0",
    "host": "Apple Silicon (aarch64)",
}

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together, then
# `readingMinutes = max(1, round(words / 220))`. See lovemesomecoding_backend/app/services/
# content.py:165. Budgeting prose alone silently doubles the published reading time.
#
# Folau asked for SHORT posts — 6-9 reading minutes — so:
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (6, 9)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 1,320
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 1,980

# A floor on the prose share. At this length it matters MORE than it did on the FastAPI track, not
# less: 1,980 words is roughly a dozen modest code blocks, and a post that spends 70% of that on
# listings has explained nothing. 45% leaves ~600-890 words of actual writing.
MIN_PROSE_SHARE = 0.45

# What the collection looks like TODAY, measured off the prod tree on 2026-08-24. This is the
# baseline the rewrite has to beat, and check_content.py reports against it.
#
# Note how different this is from the FastAPI track's baseline: there every post was 2-3x too
# LONG. Here `mongodb-data-modeling` serves an empty body on an indexed URL.
EXISTING = {
    #                                 prose, code, total, minutes
    "mongodb-why-nosql-or-mongodb":   (193, 0, 193, 1),
    "mongodb-type-of-applications":   (106, 0, 106, 1),
    "mongodb-data-modeling":          (0,   0, 0,   1),
}

FROZEN_SLUGS = tuple(EXISTING)

# ---------------------------------------------------------------------------
# Measured facts — quoted by posts, held here so they cannot drift
# ---------------------------------------------------------------------------
# Every number a post states about storage, plans or counts comes from this block. Written down
# once because a figure repeated in three posts is a figure that disagrees with itself within a
# month, and because check_content.py can then assert that a post making a measurement claim
# quotes one of these.
MEASURED = {
    # db.<c>.countDocuments({}) against the seeded reelcms database, 2026-08-24.
    "docs_reels": 16,
    "docs_creators": 5,
    "docs_comments": 55,
    "docs_reel_collections": 4,
    "docs_view_events": 30187,
    "docs_users": 2,

    # db.reels.find({status:"PUBLISHED"}).sort({publishedAt:-1}).explain("executionStats")
    # The 1:1 keys-to-returned ratio is the thing worth teaching.
    "feed_plan_stages": "FETCH <- IXSCAN",
    "feed_plan_index": "status_1_publishedAt_-1",
    "feed_keys_examined": 12,
    "feed_docs_examined": 12,
    "feed_returned": 12,

    # Spring Data renames a nested Java field called `id` to `_id`. The index declared as
    # `creator.id` is STORED as `creator._id`. Queries still hit it (verified FETCH <- IXSCAN),
    # but a hand-written mongosh query must use `creator._id`.
    "creator_index_declared": "creator.id",
    "creator_index_stored": "creator._id_1_status_1_publishedAt_-1",

    # Time-series storage, 30,187 documents, measured after forcing a checkpoint with fsync.
    # ⚠️ The saving is a WASH. See progress_report.md — this is the honest result and the post
    # says so rather than repeating the marketing claim.
    "ts_random_mb": 0.84,
    "ts_sorted_mb": 0.85,
    "ts_plain_mb": 0.91,
    "ts_ratio": 1.1,
    "ts_buckets": 17967,
    "ts_measurements": 30187,
    "ts_per_bucket": 1.7,
    "ts_metadata_combos": 49,

    # Test suites, after the app work this track is built on.
    "tests_backend": 66,
    "tests_e2e": 25,
}

# ---------------------------------------------------------------------------
# Snippet sources
# ---------------------------------------------------------------------------
# Which ReelCMS files each post is allowed to quote. check_snippets.py reads these and verifies
# that the java blocks in a post actually appear in one of the named sources.
#
# ⚠️ This is the rule that separates this track from the three posts it replaces. Those quote
# nothing at all — they have no code. Every java block here must be traceable to a file that runs
# and is covered by the 66-test suite.
#
# mongosh/javascript blocks are NOT checked this way: they are typed at a shell, not compiled into
# the app. check_content.py checks those for round-trip integrity only.
#
# A block deliberately showing the WRONG way carries the ANTIPATTERN_MARKER on its wrapper and is
# excluded from the traceability check.
ANTIPATTERN_MARKER = "data-antipattern"

# A block that illustrates a FRAMEWORK feature this app does not happen to use. Excluded from the
# traceability check, because the alternative is adding unused code to ReelCMS purely so a snippet
# has somewhere to point — which is how demo apps fill up with things nobody runs.
#
# Use it sparingly and never for a claim ABOUT ReelCMS. The post must read as "here is how Spring
# Data does X", not "here is how ReelCMS does X".
GENERIC_MARKER = "data-generic"

_ENTITY = "src/main/java/com/reelcms/api/entity"
_CONFIG = "src/main/java/com/reelcms/api/config"
_REPORT = "src/main/java/com/reelcms/api/report"

SNIPPET_SOURCES = {
    "mongodb-why-nosql-or-mongodb": [
        f"{_ENTITY}/reel/Reel.java",
        f"{_ENTITY}/reel/ReelStats.java",
    ],
    "mongodb-installation-and-mongosh": [
        "docker-compose.yml",
        "src/main/resources/application.properties",
    ],
    "mongodb-documents-and-bson-types": [
        f"{_ENTITY}/reel/Reel.java",
        f"{_ENTITY}/viewevent/ViewEvent.java",
        f"{_ENTITY}/reel/CreatorRef.java",
    ],
    "mongodb-crud-operations": [
        f"{_ENTITY}/reel/ReelRepository.java",
        f"{_ENTITY}/reel/ReelServiceImpl.java",
        f"{_ENTITY}/reel/ReelDAOImp.java",
    ],
    "mongodb-query-operators": [
        f"{_ENTITY}/reel/ReelDAOImp.java",
        f"{_ENTITY}/reel/ReelRepository.java",
    ],
    "mongodb-data-modeling": [
        f"{_ENTITY}/reel/Reel.java",
        f"{_ENTITY}/reel/VideoAsset.java",
        f"{_ENTITY}/reel/CreatorRef.java",
        f"{_ENTITY}/reel/ReelStats.java",
        f"{_ENTITY}/comment/Comment.java",
        f"{_ENTITY}/creator/CreatorServiceImpl.java",
        f"{_ENTITY}/reel/ReelDAOImp.java",
    ],
    "mongodb-schema-validation": [
        f"{_ENTITY}/reel/Reel.java",
        f"{_ENTITY}/reel/ReelServiceImpl.java",
        "src/main/java/com/reelcms/api/dto/Dtos.java",
    ],
    "mongodb-indexes": [
        f"{_CONFIG}/MongoIndexConfig.java",
        f"{_ENTITY}/reel/ReelRepository.java",
        f"{_ENTITY}/reel/ReelServiceImpl.java",
    ],
    "mongodb-text-search-and-indexes": [
        f"{_CONFIG}/MongoIndexConfig.java",
        f"{_ENTITY}/reel/ReelDAOImp.java",
    ],
    "mongodb-aggregation-pipeline": [
        f"{_REPORT}/ReportDAOImp.java",
        f"{_ENTITY}/reel/ReelDAOImp.java",
    ],
    "mongodb-aggregation-lookup-and-facets": [
        f"{_REPORT}/ReportDAOImp.java",
        f"{_ENTITY}/viewevent/ViewEvent.java",
    ],
    "mongodb-transactions": [
        f"{_ENTITY}/reel/ReelServiceImpl.java",
        f"{_ENTITY}/reel/ReelDAOImp.java",
        f"{_ENTITY}/reel/ReelStats.java",
        f"{_ENTITY}/viewevent/ViewEventService.java",
    ],
    "mongodb-replication-and-sharding": [
        "docker-compose.yml",
        "src/main/resources/application.properties",
    ],
    "mongodb-change-streams": [
        "src/main/java/com/reelcms/api/stream/ReelStatsStreamService.java",
        f"{_ENTITY}/viewevent/ViewEvent.java",
        f"{_CONFIG}/MongoIndexConfig.java",
    ],
    "mongodb-type-of-applications": [
        f"{_ENTITY}/viewevent/ViewEvent.java",
        f"{_ENTITY}/reel/ReelStats.java",
    ],
    "mongodb-spring-data-mongodb": [
        "src/main/resources/application.properties",
        "src/test/java/com/reelcms/api/ReelcmsIntegrationTest.java",
        f"{_CONFIG}/MongoConfig.java",
        f"{_CONFIG}/MongoIndexConfig.java",
        f"{_ENTITY}/reel/Reel.java",
        f"{_ENTITY}/reel/ReelRepository.java",
        f"{_ENTITY}/reel/ReelDAOImp.java",
        f"{_CONFIG}/Timestamps.java",
    ],
}

# ---------------------------------------------------------------------------
# The posts
# ---------------------------------------------------------------------------
# `tags` matter: not one of the three existing posts has any, so the tag pages for this category
# are empty. Every post carries "mongodb" plus what it is actually about.

_P = [
    # (slug, title, tags, summary)
    (
        "mongodb-why-nosql-or-mongodb",
        "MongoDB – Why NoSQL, and When Not To",
        ["mongodb", "nosql", "database-design"],
        "What a document store actually buys you, what it costs, and the four cases where a "
        "relational database is still the right answer.",
    ),
    (
        "mongodb-installation-and-mongosh",
        "MongoDB – Installation and mongosh",
        ["mongodb", "mongosh", "docker"],
        "Get a MongoDB running in Docker, connect with mongosh, and understand why this track "
        "runs a replica set from the very first command.",
    ),
    (
        "mongodb-documents-and-bson-types",
        "MongoDB – Documents and BSON Types",
        ["mongodb", "bson", "data-types"],
        "Documents, the BSON type system, _id and ObjectId — and the string-versus-ObjectId "
        "mismatch that silently breaks joins.",
    ),
    (
        "mongodb-crud-operations",
        "MongoDB – CRUD Operations",
        ["mongodb", "crud", "mongosh"],
        "insertOne through deleteMany, upserts and bulk writes, and why an update should touch "
        "one field rather than rewrite a document.",
    ),
    (
        "mongodb-query-operators",
        "MongoDB – Query Operators",
        ["mongodb", "queries", "mongosh"],
        "Comparison, logical, element and array operators, plus projection — the vocabulary every "
        "later query is built from.",
    ),
    (
        "mongodb-data-modeling",
        "MongoDB – Data Modeling: Embed or Reference",
        ["mongodb", "data-modeling", "schema-design"],
        "The one decision that shapes every MongoDB schema, with the 16 MB limit, unbounded "
        "growth and the real cost of denormalization.",
    ),
    (
        "mongodb-schema-validation",
        "MongoDB – Schema Validation",
        ["mongodb", "schema-design", "validation"],
        "$jsonSchema, validation levels and actions — and why a flexible store still wants rules "
        "at the boundary.",
    ),
    (
        "mongodb-indexes",
        "MongoDB – Indexes and the ESR Rule",
        ["mongodb", "indexes", "performance"],
        "Single, compound, multikey, unique and partial indexes, the field order that makes them "
        "work, and how to read explain().",
    ),
    (
        "mongodb-text-search-and-indexes",
        "MongoDB – Text Search",
        ["mongodb", "search", "indexes"],
        "Text indexes and field weights, the one-per-collection limit, and the point where you "
        "should stop and reach for a real search engine.",
    ),
    (
        "mongodb-aggregation-pipeline",
        "MongoDB – The Aggregation Pipeline",
        ["mongodb", "aggregation", "queries"],
        "The mental model: documents flowing through stages. $match, $group, $sort, $project — "
        "and why stage order decides your query plan.",
    ),
    (
        "mongodb-aggregation-lookup-and-facets",
        "MongoDB – $lookup, $unwind and $facet",
        ["mongodb", "aggregation", "queries"],
        "Joining collections in an aggregation, flattening arrays, running several pipelines at "
        "once — and the strict type match that makes a join return nothing.",
    ),
    (
        "mongodb-transactions",
        "MongoDB – Atomicity and Transactions",
        ["mongodb", "transactions", "concurrency"],
        "Single-document atomicity covers more than you would think. What multi-document "
        "transactions cost, and when you genuinely need one.",
    ),
    (
        "mongodb-replication-and-sharding",
        "MongoDB – Replication and Sharding",
        ["mongodb", "replication", "scaling"],
        "Replica sets, the oplog, read preference and write concern — and an honest look at when "
        "sharding is the answer and when it is not.",
    ),
    (
        "mongodb-change-streams",
        "MongoDB – Change Streams and Time-Series",
        ["mongodb", "change-streams", "time-series"],
        "Tail the oplog to push live updates to a browser, and see what a time-series collection "
        "measurably does and does not save.",
    ),
    (
        "mongodb-type-of-applications",
        "MongoDB – Which Applications Actually Fit",
        ["mongodb", "architecture", "database-design"],
        "Five shapes of application MongoDB suits well, and four where choosing it is a decision "
        "you will be undoing later.",
    ),
    (
        "mongodb-spring-data-mongodb",
        "MongoDB – Spring Data MongoDB",
        ["mongodb", "spring-data", "java"],
        "The Java side: repositories versus MongoTemplate, how mapping works, where to declare "
        "indexes, and the field rename that catches everyone.",
    ),
]

POSTS = [
    {
        "slug": slug,
        "title": title,
        "tags": tags,
        "summary": summary,
        "file": f"{i + 1:02d}-{slug}.html",
        "date": (START_DATE + timedelta(days=STEP_DAYS * i)).isoformat(timespec="seconds"),
        "frozen": slug in FROZEN_SLUGS,
    }
    for i, (slug, title, tags, summary) in enumerate(_P)
]


FROZEN_SLUGS_SET = set(FROZEN_SLUGS)
NEW_SLUGS = {p["slug"] for p in POSTS if not p["frozen"]}


def by_slug(slug):
    for post in POSTS:
        if post["slug"] == slug:
            return post
    raise KeyError(slug)


if __name__ == "__main__":
    print(f"{CATEGORY['name']} — {len(POSTS)} posts")
    print(f"budget: {TARGET_MINUTES[0]}-{TARGET_MINUTES[1]} min "
          f"= {TOTAL_WORDS_MIN}-{TOTAL_WORDS_MAX} words total (prose + code)")
    print(f"prose floor: {MIN_PROSE_SHARE:.0%}\n")
    for post in POSTS:
        flag = "FROZEN" if post["frozen"] else "new   "
        print(f"  {post['date'][:10]}  {flag}  {post['slug']}")
    print(f"\nfirst: {POSTS[0]['date'][:10]}   last: {POSTS[-1]['date'][:10]}")

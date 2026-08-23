"""The Elasticsearch track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend
with the track and the last lesson is the newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because this track is
authored before it is published: when the publish date is finally known, move START_DATE and every
lesson re-bases in order.

⚠️ THIRTEEN of these eighteen slugs are not new. The whole /elasticsearch collection was published
between 2019 and 2021 and every one of its URLs is indexed. They are being rewritten IN PLACE, not
replaced: changing one of those slugs changes a live URL, and `verify-build.mjs` fails the frontend
build when an indexed post URL stops resolving.

Because all thirteen carry their own 2019-2021 dates and `upsert_post` never overwrites an existing
date, seeding needs `seed.py --force-dates` or the lessons keep whatever order they were originally
published in and the prev/next pager walks the track out of sequence. See progress_report.md.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "elasticsearch",
    # The stored record already says "Elasticsearch" correctly — unlike `fastapi` and `postgre`,
    # which were both lowercase. Only the description is empty, so the archive page has no
    # standfirst. upsert_category rewrites both from here.
    "name": "Elasticsearch",
    "description": (
        "Elasticsearch from a first document to a search feature you can put in front of users — "
        "mappings and analysis, the query DSL, filtering, relevance, aggregations, geo search, "
        "keeping an index in step with a database, aliases and zero-downtime reindexing, "
        "snapshots and production hardening. Every example is taken from a real short-let "
        "booking app, and every query in it has been run against the cluster it describes."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself lives in
# lovemesomecoding_frontend/src/lib/nav.ts, which already lists `elasticsearch` under the Data
# Store group — nothing to add there.
NAV_GROUP = "Data Store"

# The app every code sample is taken from.
DEMO_APP = "lovemesomecoding_demo_project/stayhub"

# ---------------------------------------------------------------------------
# Versions — READ OFF THIS MACHINE, not chosen
# ---------------------------------------------------------------------------
# `curl localhost:9200`, `pip show`, `python -V`, `docker --version`, taken while the StayHub
# stack was up and its 193 tests passing, 2026-08-22.
VERSIONS = {
    "elasticsearch": "8.15.3",
    "lucene": "9.11.1",
    "elasticsearch-py": "8.15.1",
    "python": "3.12.4",
    "postgres": "16.15",
    "docker engine": "27.4.0",
    "host": "Docker Desktop on arm64 (Apple Silicon)",
}

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together, then
# `readingMinutes = max(1, round(words / 220))`. See lovemesomecoding_backend/app/services/
# content.py. Budgeting prose alone silently doubles the published reading time.
#
# Folau asked for 12-18 reading-minutes, so:
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (12, 18)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 2,640
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 3,960

# ⚠️ AND a floor on the prose share.
#
# This track's problem is the opposite of the FastAPI track's — those posts were code dumps with
# captions; these are stubs with almost no code at all. The floor still matters, because the fix
# for a 123-word post is not 3,000 words of JSON.
MIN_PROSE_SHARE = 0.40

# What the collection looks like TODAY, measured off the prod tree on 2026-08-22. This is the
# baseline the rewrite has to beat, and check_content.py reports against it.
#                            prose, code, total, minutes
EXISTING = {
    "elasticsearch-search-api":    (1967, 1552, 3519, 16),
    "elasticsearch-data-types":    (1358,   32, 1390,  6),
    "elasticsearch-sorting":       ( 852,  213, 1065,  5),
    "what-is-elasticsearch":       ( 843,    0,  843,  4),
    "elasticsearch-document-api":  ( 603,  482, 1085,  5),
    "elasticsearch-modeling-data": ( 597,   26,  623,  3),
    "elasticsearch-mapping":       ( 449,   74,  523,  2),
    "elasticsearch-filter":        ( 321,  244,  565,  3),
    "elasticsearch-geo-point":     ( 273,  246,  519,  3),
    "elasticsearch-installation":  ( 143,  120,  263,  1),
    "elasticsearch-cat-api":       ( 123,   62,  185,  1),
    "elasticsearch-aggregation":   ( 148,   40,  188,  2),
    "elasticsearch-snapshot":      (  59,    0,   59,  1),
}

# ---------------------------------------------------------------------------
# Measured facts — quoted by posts, held here so they cannot drift
# ---------------------------------------------------------------------------
# Every number a post states about timing, sizes or hit counts comes from this block. Written down
# once because a figure repeated in prose in three posts is a figure that disagrees with itself
# within a month, and because check_content.py can then assert that a post which CLAIMS a
# measurement quotes one of these.
#
# All taken 2026-08-22 against the StayHub cluster described in VERSIONS: one node, one shard,
# zero replicas, twelve listings.
MEASURED = {
    "cluster_status": "green",
    "docs": 12,
    "shards": 1,
    "replicas": 0,
    "store_bytes": 57675,
    "segments": 2,

    # The bug the hybrid text clause fixes. `q = "san francisco loft"`, operator: and.
    "best_fields_hits": 0,
    "cross_fields_hits": 1,
    "hybrid_hits": 1,

    # Median of 30 client-side round trips after a 5-request warm-up, plus the `took` the cluster
    # reported for one of them. The gap between the two IS the lesson about `took`.
    "search_no_facets_ms": 4.5,
    "search_with_facets_ms": 11.0,
    "search_took_no_facets": 2,
    "search_took_with_facets": 7,

    # 200 documents into a fresh index with the real mapping, same machine, same documents.
    "index_one_by_one_200_ms": 526,
    "index_bulk_200_ms": 47,
    "bulk_speedup": "11x",

    # BM25 for `title:cabin` on the seeded index — the full arithmetic from `_explain`.
    "bm25_score": 4.3190,
    "bm25_boost": 4.4,
    "bm25_idf": 2.1595,
    "bm25_tf": 0.4545,
    "bm25_n": 1,
    "bm25_N": 12,

    # `snapshot --create` on the 12-document index. Genuinely 0 — a snapshot of one small,
    # already-written segment is a metadata operation, and quoting it matters because it is the
    # number that makes "snapshots are incremental" concrete rather than a claim.
    "snapshot_took": "0ms",

    "tests_before": 165,
    "tests_after": 193,
}

# ---------------------------------------------------------------------------
# Snippet sources
# ---------------------------------------------------------------------------
# Which StayHub files each post is allowed to quote. check_snippets.py reads these and verifies
# that the python blocks in a post actually appear in the named source.
#
# ⚠️ This is the rule that separates this track from the thirteen posts it replaces. Those quote
# `curl` against invented `movies` and `students` indexes copied out of tutorialspoint. Every
# python block here must be traceable to a file that runs and is covered by the 193-test suite.
#
# The one exception is a block deliberately showing the WRONG way — those sit in a section flagged
# by ANTIPATTERN_MARKER and are excluded.
ANTIPATTERN_MARKER = "data-antipattern"

BACKEND = "stayhub-fastapi-backend"

SNIPPET_SOURCES = {
    "what-is-elasticsearch": [f"{BACKEND}/app/search/index.py", f"{BACKEND}/app/search/indexer.py"],
    "elasticsearch-installation": [
        "docker-compose.yml", f"{BACKEND}/app/search/client.py", f"{BACKEND}/app/core/config.py",
    ],
    "elasticsearch-mapping": [f"{BACKEND}/app/search/index.py"],
    "elasticsearch-data-types": [f"{BACKEND}/app/search/index.py"],
    "elasticsearch-analyzers-text-analysis": [
        f"{BACKEND}/app/search/index.py", f"{BACKEND}/scripts/analyze_demo.py",
    ],
    "elasticsearch-modeling-data": [
        f"{BACKEND}/app/search/index.py", f"{BACKEND}/app/models/property.py",
        f"{BACKEND}/app/search/indexer.py", f"{BACKEND}/app/api/v1/routes/search.py",
    ],
    "elasticsearch-document-api": [
        f"{BACKEND}/app/search/indexer.py", f"{BACKEND}/app/search/index.py",
    ],
    "elasticsearch-bulk-indexing-data-sync": [
        f"{BACKEND}/app/search/indexer.py", f"{BACKEND}/scripts/reindex.py",
        f"{BACKEND}/app/services/outbox_service.py",
    ],
    "elasticsearch-search-api": [
        f"{BACKEND}/app/search/queries.py", f"{BACKEND}/app/api/v1/routes/search.py",
        f"{BACKEND}/app/schemas/search.py",
    ],
        "elasticsearch-filter": [
        f"{BACKEND}/app/search/queries.py", f"{BACKEND}/tests/test_search.py",
    ],
    "elasticsearch-relevance-tuning": [
        f"{BACKEND}/app/search/queries.py", f"{BACKEND}/scripts/explain_search.py",
    ],
    "elasticsearch-sorting": [
        f"{BACKEND}/app/search/queries.py", f"{BACKEND}/app/search/index.py",
    ],
    "elasticsearch-aggregation": [
        f"{BACKEND}/app/search/queries.py", f"{BACKEND}/app/schemas/search.py",
        f"{BACKEND}/app/api/v1/routes/search.py",
    ],
    "elasticsearch-geo-point": [
        f"{BACKEND}/app/search/queries.py", f"{BACKEND}/app/search/index.py",
        f"{BACKEND}/app/schemas/search.py", f"{BACKEND}/app/api/v1/routes/search.py",
        f"{BACKEND}/tests/test_search.py",
    ],
    "elasticsearch-index-aliases-reindex": [
        f"{BACKEND}/app/search/index.py", f"{BACKEND}/scripts/reindex.py",
        f"{BACKEND}/app/search/indexer.py", f"{BACKEND}/app/core/config.py",
    ],
        "elasticsearch-cat-api": [
        f"{BACKEND}/scripts/reindex.py", f"{BACKEND}/app/search/client.py",
    ],
    "elasticsearch-snapshot": [f"{BACKEND}/scripts/snapshot.py", "docker-compose.yml"],
    "elasticsearch-production-checklist": [
        f"{BACKEND}/scripts/es_security.py", f"{BACKEND}/app/search/client.py",
        f"{BACKEND}/app/core/config.py", "docker-compose.yml",
        f"{BACKEND}/app/search/index.py", f"{BACKEND}/app/api/v1/routes/search.py",
        f"{BACKEND}/tests/test_search.py",
    ],
}

# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later, so the archive
# reads as a course rather than a pile.
#
# ⚠️ The track is dated into 2020-2021 ON PURPOSE, not because it was written then. The thirteen
# rewritten slugs were published between 2019-06 and 2021-09 and Google has those dates indexed;
# re-stamping them into 2026 would move thirteen live URLs to the front of every archive and the
# sitemap at once, which is a large, unexplained churn signal on pages whose content is a rewrite
# rather than a new post. Keeping the track in its original era leaves the site's history intact.
#
# 18 lessons x 40 days spans 2020-02-04 to 2021-12-15, which brackets the whole original range —
# so the rewritten posts land close to where they already were and the five new ones interleave
# rather than piling up at one end.
START_DATE = datetime(2020, 2, 4, 9, 0, 0)
STEP_DAYS = 40


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=STEP_DAYS * index)).strftime("%Y-%m-%dT%H:%M:%S")


# Authored in reading order. `state` is documentation, not data: "rewrite" means the slug already
# exists on the live site and must not change.
_TRACK = [
    # ----------------------------------------------------------------- foundations
    {
        "slug": "what-is-elasticsearch",
        "title": "What is Elasticsearch, and When Should You Use One?",
        "state": "rewrite",
        "tags": ["elasticsearch", "search"],
        "excerpt": (
            "Start here. What an inverted index actually does that a database index cannot, the "
            "queries that justify running a second datastore, and the ones that do not. The "
            "vocabulary you need before anything else makes sense — cluster, node, index, shard, "
            "replica, document — and the single most important consequence of the whole design: "
            "the index is a derived copy, and treating it as the source of truth is the mistake "
            "every other lesson in this track is arranged to prevent."
        ),
    },
    {
        "slug": "elasticsearch-installation",
        "title": "Elasticsearch – Installation and First Connection",
        "state": "rewrite",
        "tags": ["elasticsearch", "docker"],
        "excerpt": (
            "Getting 8.x running and talking to it, including the part that changed and breaks "
            "every older tutorial: security is on by default, so the plain docker run you were "
            "given in 2020 now answers 401. Docker Compose with sensible settings, what the "
            "enrollment token and elastic password are for, checking cluster health, and "
            "connecting the Python client with a timeout that will not take your API down."
        ),
    },
    {
        "slug": "elasticsearch-mapping",
        "title": "Elasticsearch – Mappings, and Why You Should Write Your Own",
        "state": "rewrite",
        "tags": ["elasticsearch", "mapping"],
        "excerpt": (
            "Dynamic mapping guesses a field's type from the first document it sees, and it "
            "guesses from ONE document. A price that happens to arrive as 120 becomes a long and "
            "the next listing at 119.50 is a problem. Writing an explicit mapping, what "
            "dynamic: strict buys, multi-fields, and the constraint that shapes everything "
            "afterwards: a field's type cannot be changed once it has been written."
        ),
    },
    {
        "slug": "elasticsearch-data-types",
        "title": "Elasticsearch – The Field Types That Matter",
        "state": "rewrite",
        "tags": ["elasticsearch", "mapping"],
        "excerpt": (
            "Not a catalogue. The eight or so types a real project actually needs and the "
            "decisions behind them: text versus keyword and why that one distinction causes most "
            "beginner confusion, scaled_float for money, date and what it accepts, boolean, "
            "geo_point, and object versus nested — including the array-flattening behaviour that "
            "makes nested necessary and is invisible until it returns a wrong result."
        ),
    },
    {
        "slug": "elasticsearch-analyzers-text-analysis",
        "title": "Elasticsearch – Analyzers and Text Analysis",
        "state": "new",
        "tags": ["elasticsearch", "analysis", "search"],
        "excerpt": (
            "Almost every “why does my search return nothing?” is one bug: the analyzer that "
            "ran when the document was indexed and the analyzer that ran on the query disagreed, "
            "so the terms never matched. What an analyzer is made of, the _analyze API that shows "
            "you the tokens instead of making you guess, building a custom one, and the two "
            "classic traps — keyword fields are not analysed at all, and changing an analyzer "
            "does nothing to documents already indexed."
        ),
    },
    {
        "slug": "elasticsearch-modeling-data",
        "title": "Elasticsearch – Modelling Your Data for Search",
        "state": "rewrite",
        "tags": ["elasticsearch", "modeling"],
        "excerpt": (
            "The hardest habit to break coming from SQL: stop normalising. One document per "
            "thing a user searches for, denormalised on purpose, because a join at query time is "
            "exactly the work the index exists to avoid. When nested is worth its cost, why "
            "parent/join is almost always the wrong answer, index-per-tenant versus a filter, "
            "and how to decide what belongs in the document at all."
        ),
    },
    # ----------------------------------------------------------------- writing
    {
        "slug": "elasticsearch-document-api",
        "title": "Elasticsearch – Indexing, Updating and Deleting Documents",
        "state": "rewrite",
        "tags": ["elasticsearch", "crud"],
        "excerpt": (
            "The write side. Index, get, update and delete, why choosing your own document id is "
            "what makes indexing idempotent, and what near-real-time actually means — the reason "
            "a test that indexes and immediately searches finds nothing and looks like a broken "
            "query. Then refresh and what it costs, and optimistic concurrency with seq_no and "
            "primary_term for the case where two writers race."
        ),
    },
    {
        "slug": "elasticsearch-bulk-indexing-data-sync",
        "title": "Elasticsearch – Bulk Indexing and Keeping It in Sync",
        "state": "new",
        "tags": ["elasticsearch", "python", "architecture"],
        "excerpt": (
            "Indexing 200 documents one call at a time took 526ms; the same 200 in one bulk "
            "request took 47ms. The bulk API, its partial-failure model — a 200 response that "
            "contains failures — and helpers.bulk. Then the harder half: how a Postgres row and "
            "a search document stay in step. Index after the commit and never before, why a "
            "failed index must not fail the write, and the outbox that retries it."
        ),
    },
    # ----------------------------------------------------------------- reading
    {
        "slug": "elasticsearch-search-api",
        "title": "Elasticsearch – The Search API and Query DSL",
        "state": "rewrite",
        "tags": ["elasticsearch", "search", "query-dsl"],
        "excerpt": (
            "The read side, in the order you need it. The anatomy of a response, match versus "
            "term and the single most common beginner bug hiding in that difference, "
            "multi_match across fields, _source filtering, pagination and the 10,000-result wall "
            "that from + size hits, track_total_hits, and highlighting — including the setting "
            "that stops a highlighted fragment from being an XSS hole."
        ),
    },
    {
        "slug": "elasticsearch-filter",
        "title": "Elasticsearch – bool, Filters and the Filter Cache",
        "state": "rewrite",
        "tags": ["elasticsearch", "search", "query-dsl"],
        "excerpt": (
            "How real queries are assembled. The four bool clauses — must, filter, should, "
            "must_not — and the distinction that decides both correctness and speed: filter "
            "clauses do not score and are cached, must clauses score and never can be. Then "
            "term versus terms when a filter panel has two boxes ticked, ranges, exists, and "
            "why a filter on a text field quietly matches the wrong things."
        ),
    },
    {
        "slug": "elasticsearch-relevance-tuning",
        "title": "Elasticsearch – Relevance Tuning That Is Not Guesswork",
        "state": "new",
        "tags": ["elasticsearch", "search", "relevance"],
        "excerpt": (
            "A relevance complaint is never settled by opinion. What BM25 actually computes, "
            "reading the _explain output that shows the arithmetic, what a field boost is worth "
            "and why ^2 shows up as 4.4, the multi_match types and a real bug one of them caused "
            "— “san francisco loft” returning nothing — fuzziness, and folding a rating into a "
            "text score with function_score without letting it take over."
        ),
    },
    {
        "slug": "elasticsearch-sorting",
        "title": "Elasticsearch – Sorting Results",
        "state": "rewrite",
        "tags": ["elasticsearch", "search"],
        "excerpt": (
            "Sorting looks trivial until the first field you try refuses. Why sorting on a text "
            "field fails and what fielddata has to do with it, tie-breakers and why a sort "
            "without one gives unstable pages, missing values, sorting by distance and by script, "
            "what happens to _score when you sort by a field, and reading the sort values back "
            "off a hit — which is also how search_after paginates past the 10,000-result wall."
        ),
    },
    {
        "slug": "elasticsearch-aggregation",
        "title": "Elasticsearch – Aggregations and Faceted Search",
        "state": "rewrite",
        "tags": ["elasticsearch", "aggregations"],
        "excerpt": (
            "Aggregations are the other half of Elasticsearch, and the half that turns a search "
            "box into a filter panel. Metric, bucket and pipeline aggregations, nesting them, "
            "aggregating on keyword rather than text and why that is not optional, and the part "
            "most tutorials skip: a facet counted inside its own filter collapses to a single "
            "row, so the guest can never switch cities without clearing the filter first."
        ),
    },
    {
        "slug": "elasticsearch-geo-point",
        "title": "Elasticsearch – Geo Queries and geo_point",
        "state": "rewrite",
        "tags": ["elasticsearch", "geo"],
        "excerpt": (
            "“Show me places near here”, done properly. Mapping geo_point and the five formats "
            "it accepts — including the one that reverses longitude and latitude and silently "
            "puts your listings in the Gulf of Guinea. geo_distance as a filter, geo_bounding_box "
            "for a map viewport, sorting by _geo_distance and reading the distance back off each "
            "hit for free, and geo_shape when a point is not enough."
        ),
    },
    # ----------------------------------------------------------------- operating
    {
        "slug": "elasticsearch-index-aliases-reindex",
        "title": "Elasticsearch – Aliases and Zero-Downtime Reindexing",
        "state": "new",
        "tags": ["elasticsearch", "operations"],
        "excerpt": (
            "A field type cannot be changed once it has been written, so sooner or later you "
            "have to move every document into a new index. Whether that is an outage depends on "
            "one decision you make on day one: never let your application name a concrete index. "
            "Aliases, _reindex, the atomic alias swap, what happens to writes that land during "
            "the copy, and how to migrate a cluster that already got this wrong."
        ),
    },
    {
        "slug": "elasticsearch-cat-api",
        "title": "Elasticsearch – The _cat APIs and Reading Cluster Health",
        "state": "rewrite",
        "tags": ["elasticsearch", "operations"],
        "excerpt": (
            "The APIs you actually type when something is wrong. _cat/health, indices, nodes, "
            "shards and allocation, with the v, h and s parameters that make them readable. Then "
            "the questions they answer: what yellow really means and why a single-node cluster is "
            "yellow by default, which shard is unassigned and why, where the disk went, and how "
            "to tell a slow query from a slow cluster."
        ),
    },
    {
        "slug": "elasticsearch-snapshot",
        "title": "Elasticsearch – Snapshots, Restores and SLM",
        "state": "rewrite",
        "tags": ["elasticsearch", "operations", "backup"],
        "excerpt": (
            "Registering a repository, taking a snapshot, restoring it, and automating the whole "
            "thing with a lifecycle policy — plus the retention setting that stops a cluster "
            "which was off for a month from deleting every backup it has the moment it comes "
            "back. And an honest answer to the question underneath: if your index is derived from "
            "a database, a rebuild may be the better restore, and knowing which is the point."
        ),
    },
    {
        "slug": "elasticsearch-production-checklist",
        "title": "Elasticsearch – What to Do Before You Go to Production",
        "state": "new",
        "tags": ["elasticsearch", "operations", "security"],
        "excerpt": (
            "The list, in the order it bites. Shard sizing and why more shards is usually the "
            "wrong instinct, replicas and what green actually promises, JVM heap and the 50% "
            "rule, security beyond turning it on — an API key scoped to one index rather than "
            "the elastic superuser every guide leaves you using — index lifecycle management, "
            "what to monitor, and the failure modes to rehearse before they happen."
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

# Slugs that already exist on the live site and must never change. All thirteen were published
# between 2019 and 2021; check_content.py fails if one leaves the manifest, and seed.py refuses to
# write to prod if one is missing from the target tree.
FROZEN_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "rewrite"}

NEW_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "new"}

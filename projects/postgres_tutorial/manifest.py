"""The Postgres track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend
with the track and the last lesson is the newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because this track is
authored before it is published: when the publish date is finally known, move START_DATE and every
lesson re-bases in order.

⚠️ TWO of these eighteen slugs are not new. `postgres-introduction` and `postgres-installation`
were published in February 2020 and both URLs are indexed. They are being rewritten IN PLACE, not
replaced: changing either slug changes a live URL, and `verify-build.mjs` fails the frontend build
when an indexed post URL stops resolving.

Both carry 2020-02-19 and `upsert_post` never overwrites an existing date, so seeding needs
`seed.py --force-dates` or those two keep their stored date, land in the middle of the track
instead of at its head, and the pager reads nonsense. See progress_report.md.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "postgre",
    # ⚠️ The slug is `postgre`, not `postgres`. It is wrong, it has been wrong since 2020, and it
    # is the live URL — /postgre/postgres-introduction is indexed. Not renaming it.
    #
    # The stored record currently says "postgre" in lowercase with an EMPTY description.
    # upsert_category rewrites both from here, which is the only reason the archive page gets a
    # display name and a standfirst at all.
    "name": "Postgres",
    "description": (
        "PostgreSQL from a first CREATE TABLE to something you can put in front of users — psql "
        "and roles, data types and constraints, the SQL you write every day, JSONB, indexes, "
        "EXPLAIN, transactions and locking, migrations and the production checklist. Every query "
        "is run against a real 400,000-row booking database before it ships, and every plan is a "
        "plan Postgres actually chose."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself lives in
# lovemesomecoding_frontend/src/lib/nav.ts, which already lists `postgre` under the Data Store
# group with the display name "Postgres" — nothing to add there.
NAV_GROUP = "Data Store"

# ---------------------------------------------------------------------------
# The databases every example runs against
# ---------------------------------------------------------------------------
# `stayhub` is the demo app's own database: the real schema, 12 properties, 3 bookings. Right for
# showing what a schema looks like, useless for showing a query plan.
#
# `stayhub_lab` is the SAME schema at 400,000 bookings, built by lab/setup.sh. Every index,
# EXPLAIN, VACUUM and locking example runs there. See progress_report.md for why.
DEMO_APP = "lovemesomecoding_demo_project/stayhub"
LAB_DB = "stayhub_lab"
LAB_TODAY = "2024-10-01"  # "now" in the lab data; status is derived from the dates against it

# ---------------------------------------------------------------------------
# Versions — READ OFF THIS MACHINE, not chosen
# ---------------------------------------------------------------------------
VERSIONS = {
    "postgres": "16.15 (postgres:16-alpine, aarch64-unknown-linux-musl)",
    "psql": "16.15",
    "docker engine": "27.4.0",
    "host": "Docker Desktop on aarch64 (Apple Silicon)",
    "alembic": "1.14.0",
    "sqlalchemy": "2.0.36",
    "psycopg": "3.2.3",
}

# Row counts in stayhub_lab after lab/setup.sh, 2026-08-22. Quoted by posts, held here so a number
# repeated in three places cannot disagree with itself.
LAB_ROWS = {
    "users": 50_000,
    "properties": 20_000,
    "bookings": 400_000,
    "payments": 374_518,
    "reviews": 200_612,
    "bookings_by_status": {
        "COMPLETED": 200_612,
        "CONFIRMED": 152_854,
        "PENDING": 25_482,
        "CANCELLED": 21_052,
    },
    "check_in_range": ("2024-01-01", "2025-06-05"),
}

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together, then
# `readingMinutes = max(1, round(words / 220))`. See lovemesomecoding_backend/app/services/
# content.py:161. Budgeting prose alone silently doubles the published reading time.
#
# Folau asked for 6-10 reading-minutes — "keep posts to the point" — so:
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (6, 10)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 1,320
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 2,200

# AND a floor on the prose share. A SQL lesson is the easiest thing in the world to satisfy a word
# budget with by pasting a longer query, and the result is a listing with captions rather than an
# explanation illustrated by code.
MIN_PROSE_SHARE = 0.40

# What the collection looks like TODAY, measured off the local content tree on 2026-08-22. This is
# the baseline the rewrite has to beat, and check_content.py reports against it.
EXISTING = {
    #                          prose, code, total, minutes
    "postgres-introduction":  (176, 0, 176, 1),
    "postgres-installation":  (78, 34, 112, 1),
}

# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------
# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later, so the archive and
# the pager agree.
#
# Folau asked for this track to sit in 2018-2020 rather than alongside the other 2026 tracks, so
# eighteen lessons are spread across roughly two and a half years at a lesson every seven or eight
# weeks: 2018-03-06 through 2020-08-06.
#
# ⚠️ This moves the two frozen posts BACKWARDS. `postgres-introduction` and `postgres-installation`
# are stored with 2020-02-19, and as lessons 1 and 2 they now take 2018-03-06 and 2018-04-27.
# `upsert_post` never overwrites an existing date, so seeding needs `seed.py --force-dates` — see
# progress_report.md.
START_DATE = datetime(2018, 3, 6, 9, 0, 0)
STEP_DAYS = 52


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=STEP_DAYS * index)).strftime("%Y-%m-%dT%H:%M:%S")


# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
# `state` is "rewrite" for a slug that already exists on the live site and "new" otherwise.
_TRACK = [
    {
        "slug": "postgres-introduction",
        "title": "Postgres – Introduction",
        "state": "rewrite",
        "tags": ["postgres", "database"],
        "excerpt": (
            "What Postgres actually is under the marketing: one process per connection, a "
            "write-ahead log, and MVCC — which is why a reader never blocks a writer and why "
            "VACUUM has to exist. Which version to run, what the release cycle promises, and an "
            "honest table of where Postgres beats MySQL, where it does not, and the three "
            "questions worth asking before you pick either."
        ),
    },
    {
        "slug": "postgres-installation",
        "title": "Postgres – Install and Connect",
        "state": "rewrite",
        "tags": ["postgres", "docker"],
        "excerpt": (
            "Postgres 16 in a container in one command, then the same thing done properly: a "
            "docker-compose file with a named volume, a healthcheck that waits for the database "
            "rather than the process, and an init script. Why the published port is the one that "
            "enforces a password and the container socket is not, what happens to your data on "
            "`down -v`, and how to connect from psql, a URI and an app."
        ),
    },
    {
        "slug": "postgres-psql-and-tooling",
        "title": "Postgres – psql and the Tools You Actually Use",
        "state": "new",
        "tags": ["postgres", "psql", "tooling"],
        "excerpt": (
            "psql is the tool that ships with the database and the one every answer online "
            "assumes. The meta-commands worth memorising — \\d, \\d+, \\di, \\l, \\dn, \\x, "
            "\\timing — the connection URI in full, running a file with ON_ERROR_STOP so a "
            "migration does not half-apply, and a .psqlrc that makes the shell bearable. Plus "
            "where a GUI still wins."
        ),
    },
    {
        "slug": "postgres-databases-schemas-and-roles",
        "title": "Postgres – Databases, Schemas, Roles and Privileges",
        "state": "new",
        "tags": ["postgres", "security"],
        "excerpt": (
            "A database holds schemas, a schema holds tables, and a role is both a user and a "
            "group. Creating an application account that is not a superuser: what `public` "
            "grants you by default and why the first thing to do is revoke it, GRANT versus "
            "ALTER DEFAULT PRIVILEGES and why the second one is the one people forget, "
            "search_path, and the owner/app/read-only split worth having on day one."
        ),
    },
    {
        "slug": "postgres-data-types",
        "title": "Postgres – Data Types",
        "state": "new",
        "tags": ["postgres", "sql", "schema"],
        "excerpt": (
            "The choices you cannot cheaply undo later. `text` versus `varchar(n)` and why the "
            "length limit buys nothing, `numeric` for money and never a float, `timestamptz` "
            "versus `timestamp` and what actually gets stored, `uuid` alongside an integer key "
            "rather than instead of it, arrays, and why StayHub stores its enums as varchar. "
            "With a mapping table to Python and Java types."
        ),
    },
    {
        "slug": "postgres-tables-and-constraints",
        "title": "Postgres – Tables, Keys and Constraints",
        "state": "new",
        "tags": ["postgres", "sql", "schema"],
        "excerpt": (
            "CREATE TABLE, then the constraints that make wrong data impossible instead of "
            "unlikely. Identity columns rather than serial, primary and foreign keys and what "
            "ON DELETE actually chooses, UNIQUE, NOT NULL, CHECK — and the exclusion constraint "
            "that stops two guests booking the same property on the same night, enforced by the "
            "database rather than by hoping the application checked."
        ),
    },
    {
        "slug": "postgres-select-and-filtering",
        "title": "Postgres – SELECT, WHERE and ORDER BY",
        "state": "new",
        "tags": ["postgres", "sql"],
        "excerpt": (
            "The query you write a hundred times a day, done carefully. Filtering with AND/OR "
            "and the parenthesis that changes the answer, LIKE versus ILIKE, IN and BETWEEN, "
            "ordering with NULLS LAST, DISTINCT versus DISTINCT ON, and keyset pagination — "
            "because OFFSET 10000 reads ten thousand rows to throw them away. Plus the three "
            "ways NULL will surprise you."
        ),
    },
    {
        "slug": "postgres-joins",
        "title": "Postgres – Joins",
        "state": "new",
        "tags": ["postgres", "sql"],
        "excerpt": (
            "INNER, LEFT, RIGHT, FULL and CROSS, each with the row count it produces on real "
            "tables so the difference is visible rather than described. The LEFT JOIN whose "
            "WHERE clause silently turns it back into an INNER JOIN, anti-joins with NOT EXISTS, "
            "self-joins, and LATERAL — the one that lets you write top-N-per-group without a "
            "window function."
        ),
    },
    {
        "slug": "postgres-aggregation-and-grouping",
        "title": "Postgres – Aggregation and GROUP BY",
        "state": "new",
        "tags": ["postgres", "sql"],
        "excerpt": (
            "count, sum, avg, min, max, and the rule that decides what may appear in the SELECT "
            "list. WHERE versus HAVING and why the order matters for speed, count(*) versus "
            "count(column) on nullable data, FILTER for counting several things in one pass, "
            "string_agg and array_agg, and GROUPING SETS for a subtotal row without a second "
            "query."
        ),
    },
    {
        "slug": "postgres-subqueries-and-ctes",
        "title": "Postgres – Subqueries and CTEs",
        "state": "new",
        "tags": ["postgres", "sql"],
        "excerpt": (
            "Scalar subqueries, IN, EXISTS and the difference that matters when the inner query "
            "returns NULL. WITH for naming the steps of a query you can still read next month, "
            "the MATERIALIZED keyword that Postgres 12 made optional and when to force it, "
            "recursive CTEs, and writing to two tables in one statement with a data-modifying "
            "CTE."
        ),
    },
    {
        "slug": "postgres-window-functions",
        "title": "Postgres – Window Functions",
        "state": "new",
        "tags": ["postgres", "sql", "analytics"],
        "excerpt": (
            "An aggregate collapses rows; a window function keeps them and adds a column. OVER "
            "and PARTITION BY, row_number versus rank versus dense_rank and which one you meant, "
            "running totals with a frame clause, lag and lead for comparing a row to the one "
            "before it, and top-N-per-group — the query that is ugly with a subquery and three "
            "lines with a window."
        ),
    },
    {
        "slug": "postgres-insert-update-delete",
        "title": "Postgres – INSERT, UPDATE, DELETE and Upsert",
        "state": "new",
        "tags": ["postgres", "sql"],
        "excerpt": (
            "Writing data, including the parts SQL tutorials skip. RETURNING so you do not need "
            "a second round trip for the generated id, ON CONFLICT DO UPDATE for a real upsert "
            "and the unique index it requires, UPDATE ... FROM and DELETE ... USING for joining "
            "in the rows you are changing, COPY for bulk loads, and why a soft delete is a "
            "column and not a DELETE."
        ),
    },
    {
        "slug": "postgres-json-and-jsonb",
        "title": "Postgres – JSON and JSONB",
        "state": "new",
        "tags": ["postgres", "jsonb"],
        "excerpt": (
            "jsonb is a real column type with real operators, not a text field you parse in the "
            "application. -> versus ->>, the containment operator @> and the GIN index that "
            "makes it fast, jsonb_path_query, updating one key with jsonb_set, and expanding an "
            "array into rows. Ends with the harder question: which of your columns should NOT "
            "have been jsonb."
        ),
    },
    {
        "slug": "postgres-indexes",
        "title": "Postgres – Indexes",
        "state": "new",
        "tags": ["postgres", "performance", "indexes"],
        "excerpt": (
            "Every index in this post is created on a 400,000-row table and the plan before and "
            "after is shown. B-tree and why column order in a composite index decides whether it "
            "is used, partial indexes for the status you actually query, expression indexes for "
            "lower(email), covering indexes and index-only scans, GIN for jsonb, and the write "
            "cost that makes an unused index worse than no index."
        ),
    },
    {
        "slug": "postgres-explain-and-query-performance",
        "title": "Postgres – EXPLAIN and Query Performance",
        "state": "new",
        "tags": ["postgres", "performance", "explain"],
        "excerpt": (
            "How to read a plan instead of guessing. EXPLAIN versus EXPLAIN ANALYZE and the "
            "danger of running the second one on an UPDATE, what BUFFERS tells you that timing "
            "does not, the scan and join nodes you will actually meet, and the single most "
            "useful signal in the output — the gap between estimated and actual rows. Plus "
            "pg_stat_statements for finding the query worth fixing."
        ),
    },
    {
        "slug": "postgres-transactions-and-locking",
        "title": "Postgres – Transactions, Isolation and Locking",
        "state": "new",
        "tags": ["postgres", "transactions", "concurrency"],
        "excerpt": (
            "BEGIN, COMMIT, ROLLBACK, and what Postgres promises in between. Read Committed "
            "versus Repeatable Read versus Serializable, shown with two real psql sessions "
            "rather than described. SELECT FOR UPDATE, the lost update it prevents, deadlocks "
            "and the ordering rule that avoids them, advisory locks, and the "
            "idle-in-transaction connection that blocks your next deploy."
        ),
    },
    {
        "slug": "postgres-schema-migrations",
        "title": "Postgres – Schema Migrations Without Downtime",
        "state": "new",
        "tags": ["postgres", "migrations", "production"],
        "excerpt": (
            "The DDL that takes a lock long enough to be an outage, and the version of the same "
            "change that does not. Adding a column with a default, adding NOT NULL in two steps "
            "with a validated CHECK, CREATE INDEX CONCURRENTLY and the invalid index it can "
            "leave behind, renaming a column across two deploys, and lock_timeout — the one "
            "setting that turns a migration from an outage into a retry."
        ),
    },
    {
        "slug": "postgres-in-production",
        "title": "Postgres – The Production Checklist",
        "state": "new",
        "tags": ["postgres", "production", "operations"],
        "excerpt": (
            "What has to be true before the database is in front of users. Connection pooling "
            "and why max_connections is not the answer, the four settings worth changing from "
            "the defaults, autovacuum and how to see whether it is keeping up, pg_dump versus "
            "physical backup and point-in-time recovery, the monitoring queries to have ready "
            "before you need them, and what managed Postgres does and does not do for you."
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

# Slugs that already exist on the live site and must never change. check_content.py fails if one
# leaves the manifest, and seed.py refuses to write to prod if one is missing from the target tree.
FROZEN_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "rewrite"}

NEW_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "new"}

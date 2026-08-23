"""The Snowflake track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend
with the track and the last lesson is the newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because this track is
authored before it is published: when the publish date is finally known, move START_DATE and every
lesson re-bases in order.

⚠️ ONE of these sixteen slugs is not new. `snowflake-introduction` was published on 2019-04-05 and
its URL is indexed. It is being rewritten IN PLACE, not replaced: changing that slug changes a
live URL, and `verify-build.mjs` fails the frontend build when an indexed post URL stops resolving.

Because it carries a 2019 date and `upsert_post` never overwrites an existing date, seeding needs
`seed.py --force-dates` or lesson 1 sits three years behind lessons 2-16 and the pager walks from
the last lesson straight back to the first. See progress_report.md.

⚠️ `--force-dates` MOVES THAT LIVE POST'S PUBLISHED DATE, from 2019-04-05 to its lesson-1 slot.
That is intended — the page is being rewritten, so the 2019 date describes content that no longer
exists — but it is a visible change to an indexed URL, not just an internal one.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "snowflake",
    # ⚠️ The stored record currently says "snowflake" in lowercase with an EMPTY description.
    # upsert_category rewrites both from here, which is the only reason the archive page gets a
    # display name and a standfirst at all.
    "name": "Snowflake",
    "description": (
        "Snowflake from a first query to a warehouse you can put a product on — the architecture "
        "that makes storage and compute separable, sizing virtual warehouses, loading data with "
        "stages and Snowpipe, querying JSON without a schema, making slow queries fast, Time "
        "Travel, streams and tasks, role-based access control, and keeping the credit bill "
        "predictable. Every query runs against SNOWFLAKE_SAMPLE_DATA, which your account already "
        "has on day one."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself lives in
# lovemesomecoding_frontend/src/lib/nav.ts, which already lists `snowflake` under the Data Store
# group with the display name "Snowflake" — nothing to add there.
NAV_GROUP = "Data Store"

# ---------------------------------------------------------------------------
# ⚠️ NOTHING IN THIS TRACK WAS EXECUTED
# ---------------------------------------------------------------------------
# There is no Snowflake account, no snowsql, no `snow` CLI and no snowflake-connector-python on
# this machine — checked 2026-08-22. Every other track on this site runs its samples before
# shipping them; this one cannot, and the posts are written to be honest about that:
#
#   - Result blocks are ILLUSTRATIVE. They are shaped like real output, not captured from it.
#   - No post claims a timing, a byte count or a credit total as a measurement.
#   - No post prints a dollar price. Credit CONSUMPTION per warehouse size is documented and
#     stable; the price per credit varies by edition, cloud and region. Link the pricing page.
#
# check_content.py enforces the last two mechanically. See progress_report.md for the full note.
VERIFIED = False

# ---------------------------------------------------------------------------
# The dataset every query lesson uses
# ---------------------------------------------------------------------------
# SNOWFLAKE_SAMPLE_DATA is a shared database present in every account from creation — the reader
# needs to load nothing to follow along. TPCH_SF1 is the small one (~6M lineitem rows); the
# performance lessons step up to TPCH_SF100 so the answers are not trivially cached.
#
# ⚠️ You cannot COPY INTO a share. The loading lessons (7, 8) create their own tables and stage
# their own files, written out in the post.
SAMPLE_DB = "SNOWFLAKE_SAMPLE_DATA"
SAMPLE_SCHEMAS = ("TPCH_SF1", "TPCH_SF10", "TPCH_SF100", "TPCH_SF1000")

# The database the track creates for anything it writes to. Named in one place so a rename is one
# edit, and so check_content.py can assert no post invents a second one.
LAB_DB = "LEARN_SNOWFLAKE"

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together, then
# `readingMinutes = max(1, round(words / 220))`. See lovemesomecoding_backend/app/services/
# content.py:161. Budgeting prose alone silently doubles the published reading time.
#
# Folau asked for short posts — 6-10 reading-minutes — so:
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (6, 10)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 1,320
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 2,200

# A floor on the prose share. The FastAPI track measured its own live posts at 75% code and had to
# introduce this; starting with it is cheaper than retrofitting it. SQL is terse, so a Snowflake
# post that is mostly code is usually a post that forgot to explain anything.
MIN_PROSE_SHARE = 0.40

# What the collection looks like TODAY, measured off the local tree on 2026-08-22. Kept here so
# the before/after in progress_report.md can be re-checked rather than trusted.
BEFORE = {
    "posts": 1,
    "counted_words": 624,
    "code_blocks": 0,
    "headings": 0,
    "reading_minutes": 3,
}

# What the ONE live post measures today — (prose, code, total, reading-minutes), taken off the
# local content tree on 2026-08-22. check_content.py asserts the rewrite is BIGGER than this.
#
# ⚠️ That is the INVERSE of the FastAPI and Postgres rules, and deliberately so. Those tracks were
# cutting bloated posts down; this one is replacing a 624-word marketing blurb with a lesson. A
# "rewrite" that lands near 624 words did not happen.
EXISTING = {
    "snowflake-introduction": (624, 0, 624, 3),
}

# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------
# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later, so the archive
# reads in lesson order and the pager walks the track.
#
# ⚠️ BACKDATED to 2022 on request (2026-08-23). 16 posts × 3 days = a 45-day run, 2022-05-03 to
# 2022-06-17, which sits inside the asked-for 2021–2022 window and just after the 2022-04-05
# `/snowflake-table-of-content` page that used to index this collection.
#
# The consequence is deliberate and worth knowing before changing it back: the site sorts every
# archive newest-first, so a 2022 post does NOT appear on the homepage or in the 50-item RSS feed.
# This track lands deep in the archive and is reached by /snowflake, search, and Google. Dating it
# in the present would have put all 16 across the top of the homepage instead.
START_DATE = datetime(2022, 5, 3, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=STEP_DAYS * index)).strftime("%Y-%m-%dT%H:%M:%S")


_TRACK = [
    # ------------------------------------------------------------- foundations
    {
        "slug": "snowflake-introduction",
        "title": "Snowflake – What It Is and Why It Exists",
        "state": "rewrite",
        "tags": ["snowflake", "data-warehouse"],
        "excerpt": (
            "Start here. What Snowflake actually is — a SQL data warehouse you rent by the "
            "second, on somebody else's cloud — and what problem it was built to solve that "
            "Postgres and Hadoop did not. What you get on day one, what you pay for, when it is "
            "the wrong tool, and the lesson index for this track in reading order."
        ),
    },
    {
        "slug": "snowflake-architecture",
        "title": "Snowflake – Architecture: Storage, Compute and Cloud Services",
        "state": "new",
        "tags": ["snowflake", "architecture"],
        "excerpt": (
            "The three layers, and why every cost and performance decision later in this track "
            "comes back to them. Micro-partitions and how they replace the indexes you are used "
            "to, why two teams can query the same table at full speed without blocking each "
            "other, and what the services layer does for free — including the result cache that "
            "makes a repeated query cost nothing at all."
        ),
    },
    {
        "slug": "snowflake-getting-started",
        "title": "Snowflake – Getting Started: Account, Worksheet and Connectors",
        "state": "new",
        "tags": ["snowflake", "getting-started"],
        "excerpt": (
            "From a trial signup to your first query against SNOWFLAKE_SAMPLE_DATA. Picking an "
            "edition and a region, the four things every session needs set, running SQL in "
            "Snowsight, and connecting from outside the browser — the Snowflake CLI, the Python "
            "connector and JDBC — with the key-pair auth you should use instead of a password."
        ),
    },
    {
        "slug": "snowflake-virtual-warehouses",
        "title": "Snowflake – Virtual Warehouses and Sizing",
        "state": "new",
        "tags": ["snowflake", "warehouse", "performance"],
        "excerpt": (
            "The compute you are actually paying for. What a size means in credits, why doubling "
            "the size can cost the same as leaving it alone, auto-suspend and auto-resume and the "
            "one setting people get wrong, multi-cluster warehouses for concurrency versus a "
            "bigger warehouse for one slow query, and how to split workloads so a loading job "
            "cannot slow down a dashboard."
        ),
    },
    # ------------------------------------------------------------------ modelling
    {
        "slug": "snowflake-databases-schemas-and-tables",
        "title": "Snowflake – Databases, Schemas and Tables",
        "state": "new",
        "tags": ["snowflake", "sql", "ddl"],
        "excerpt": (
            "The object hierarchy and the DDL you will use every day. Permanent, transient and "
            "temporary tables and what the difference costs you, views versus materialised views, "
            "why Snowflake accepts a primary key and then ignores it, CREATE TABLE ... LIKE and "
            "CLONE, and the naming and identifier-casing rules that bite everyone exactly once."
        ),
    },
    {
        "slug": "snowflake-data-types",
        "title": "Snowflake – Data Types That Matter",
        "state": "new",
        "tags": ["snowflake", "sql", "data-types"],
        "excerpt": (
            "The short list worth knowing, and the three that cause real bugs. Why NUMBER is the "
            "only sensible choice for money, why VARCHAR(16777216) costs nothing extra, the three "
            "TIMESTAMP flavours and which one to standardise on, and VARIANT — the type that lets "
            "a column hold JSON and still be queried with SQL."
        ),
    },
    # ------------------------------------------------------------------- loading
    {
        "slug": "snowflake-loading-data",
        "title": "Snowflake – Loading Data with Stages and COPY INTO",
        "state": "new",
        "tags": ["snowflake", "etl", "copy-into"],
        "excerpt": (
            "Getting files in. Internal versus external stages, PUT and COPY INTO, file formats "
            "as reusable objects, why a hundred medium files load faster than one huge one, and "
            "what to do when a row fails — ON_ERROR, VALIDATION_MODE and the load metadata that "
            "silently skips a file you already loaded."
        ),
    },
    {
        "slug": "snowflake-snowpipe-and-continuous-loading",
        "title": "Snowflake – Snowpipe and Continuous Loading",
        "state": "new",
        "tags": ["snowflake", "etl", "snowpipe"],
        "excerpt": (
            "When a nightly COPY is not enough. Snowpipe with cloud-storage event notifications, "
            "how its serverless billing differs from a warehouse, monitoring a pipe that has "
            "quietly stopped, and where the newer options — Snowpipe Streaming and directory "
            "tables — fit. Includes the notification setup that is the only genuinely fiddly part."
        ),
    },
    {
        "slug": "snowflake-semi-structured-data",
        "title": "Snowflake – JSON and Semi-Structured Data",
        "state": "new",
        "tags": ["snowflake", "json", "variant"],
        "excerpt": (
            "Loading JSON without designing a schema first, then querying it as if you had. The "
            "colon path syntax, casting out of VARIANT and why forgetting to cast makes strings "
            "come back with quotes, FLATTEN for arrays, and the decision that actually matters: "
            "when to leave data in a VARIANT column and when to shred it into real columns."
        ),
    },
    # ------------------------------------------------------------------ querying
    {
        "slug": "snowflake-querying-data",
        "title": "Snowflake – Querying Data",
        "state": "new",
        "tags": ["snowflake", "sql", "query"],
        "excerpt": (
            "The SQL that is worth knowing beyond SELECT ... WHERE. CTEs, window functions, "
            "QUALIFY — the clause Snowflake has and Postgres does not — SAMPLE for exploring a "
            "large table cheaply, GROUP BY ALL, and the date and string functions that come up in "
            "every reporting query. All of it against TPCH_SF1."
        ),
    },
    {
        "slug": "snowflake-query-performance",
        "title": "Snowflake – Making Queries Fast",
        "state": "new",
        "tags": ["snowflake", "performance", "query-profile"],
        "excerpt": (
            "Why a query is slow, in the order worth checking. Reading the Query Profile, pruning "
            "and what breaks it, spilling to local and remote storage and what to do about it, "
            "the three caches and which one you are actually hitting, and when clustering keys "
            "earn their cost — which is far less often than people reach for them."
        ),
    },
    # ------------------------------------------------------------------ operating
    {
        "slug": "snowflake-time-travel-and-cloning",
        "title": "Snowflake – Time Travel, Cloning and Undrop",
        "state": "new",
        "tags": ["snowflake", "time-travel", "cloning"],
        "excerpt": (
            "The two features that change how you work, not just what you can recover. Querying a "
            "table as it was before the bad UPDATE, UNDROP, zero-copy clones that give you a full "
            "copy of production for a dev branch at no storage cost, and Fail-safe — which is "
            "Snowflake's insurance policy, not your backup."
        ),
    },
    {
        "slug": "snowflake-streams-and-tasks",
        "title": "Snowflake – Streams and Tasks",
        "state": "new",
        "tags": ["snowflake", "streams", "tasks", "etl"],
        "excerpt": (
            "Native change tracking and scheduling, so a pipeline needs no extra orchestrator. "
            "What a stream really is (an offset, not a copy), the consumption rule that surprises "
            "everyone, task trees and serverless tasks, and the standard pattern: a stream feeds "
            "a MERGE, a task runs it only when there is something to do."
        ),
    },
    {
        "slug": "snowflake-access-control",
        "title": "Snowflake – Roles, Grants and Access Control",
        "state": "new",
        "tags": ["snowflake", "security", "rbac"],
        "excerpt": (
            "Snowflake's RBAC in the order you need to understand it. Why ACCOUNTADMIN is not "
            "your working role, ownership versus grants, future grants — the single feature that "
            "stops permissions rotting every time someone adds a table — and a functional role "
            "layout you can copy. Plus masking policies and row access policies, briefly."
        ),
    },
    {
        "slug": "snowflake-cost-management",
        "title": "Snowflake – Understanding and Controlling Cost",
        "state": "new",
        "tags": ["snowflake", "cost", "operations"],
        "excerpt": (
            "Where the credits actually go, and the handful of changes that move the bill most. "
            "Reading ACCOUNT_USAGE for warehouse, storage and serverless spend, resource monitors "
            "that suspend rather than warn, the auto-suspend and idle-warehouse waste everybody "
            "has, and why the fastest query is usually also the cheapest one."
        ),
    },
    {
        "slug": "snowflake-in-production",
        "title": "Snowflake – Putting It in Production",
        "state": "new",
        "tags": ["snowflake", "production", "operations"],
        "excerpt": (
            "The checklist between a working warehouse and one other people depend on. Separating "
            "dev, staging and production, versioning DDL in git and deploying it in CI, key-pair "
            "auth and network policies for service accounts, monitoring and alerting on the views "
            "that matter, and the failure modes worth having an answer for before they happen."
        ),
    },
]

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

# The one slug that already exists on the live site and must never change. check_content.py fails
# if it leaves the manifest, and seed.py refuses to write to prod if it is missing from the target
# tree — because upserting a frozen slug that is absent MINTS A NEW URL rather than rewriting the
# indexed one.
FROZEN_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "rewrite"}

NEW_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "new"}

# The one image already on the media CDN that the rewritten post 1 keeps. Anything else a post
# wants has to be uploaded first — check_content.py fails on an <img> pointing anywhere else.
MEDIA_HOST = "d2q2snz6diubfd.cloudfront.net"

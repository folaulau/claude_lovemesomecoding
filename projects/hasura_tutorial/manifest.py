"""The Hasura track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and the last lesson is the
newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because
this track is authored before it is published: when the publish date is finally
known, move START_DATE and every lesson re-bases in order.

⚠️ ELEVEN of these twenty slugs are not new. The whole /hasura collection was
published in early 2020 and every one of its URLs is indexed — while carrying
1,266 words between them, four of the eleven with no body at all. They are being
rewritten in place, NOT replaced: changing one of those slugs changes a live URL.

Because all eleven carry 2020 dates and `upsert_post` never overwrites an
existing date, seeding needs `seed.py --force-dates` or the archive interleaves
nine 2026 posts with eleven 2020 ones and the pager reads nonsense.
See progress_report.md.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "hasura",
    "name": "Hasura",
    # The stored record currently says "hasura" in lowercase. upsert_category
    # rewrites it from here, which is the only reason the display name is fixed.
    "description": (
        "Hasura end to end — instant GraphQL over Postgres, permissions and JWT auth, "
        "relationships, Actions, event triggers, migrations and CI/CD, and shipping to "
        "production. Every v2 example is taken from a real short-let booking app, and every "
        "topic also covers what changes in v3 (DDN)."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, which already lists `hasura`
# under Databases with the display name "Hasura" — nothing to add there.
NAV_GROUP = "Databases"

# The app every v2 code sample is taken from. Unlike the Docker track, the Hasura
# surface already existed: StayHub has run Hasura over Postgres since it was
# built. Four things it lacked — an Action, an event trigger, a subscription and
# a Hasura-side mutation — are added BY this track and run before being quoted.
DEMO_APP = "lovemesomecoding_demo_project/stayhub"

# The versions the v2 half of the track is written against.
#
# READ OFF THIS MACHINE, not chosen — `curl localhost:8081/v1/version`,
# `hasura version`, `docker ps`, the compose file and the two lockfiles. The
# StayHub stack was up and healthy when these were taken.
#
# ⚠️ `ce` is load-bearing. Community Edition cannot demonstrate query caching
# (`@cached`), allow-lists or rate limiting — those are Enterprise/Cloud. Lessons
# 14 and 15 label them as such instead of showing them running.
VERSIONS = {
    "hasura graphql engine": "v2.42.0 (server_type: ce — Community Edition)",
    "hasura cli": "v2.40.0",
    "postgres": "16-alpine",
    "docker engine": "27.4.0",
    "host": "Docker Desktop on aarch64 (Apple Silicon)",
}

# What the demo app around the engine is built from, quoted by the client-side
# and Action lessons.
APP_VERSIONS = {
    "apollo client": "4.2.12",
    "react": "19.2.8 (Vite 8, TypeScript 6)",
    "fastapi": "0.115.5",
    "sqlalchemy": "2.0.36",
    "alembic": "1.14.0",
}

# ---------------------------------------------------------------------------
# v3 / DDN
# ---------------------------------------------------------------------------
# The `ddn` CLI is NOT installed on this machine and no supergraph was stood up.
# Every "In v3 (DDN)" section is transcribed from the official docs on the date
# below and is explicitly NOT run locally — a deliberate trade, recorded in
# progress_report.md, and the most likely source of a wrong snippet here.
#
# The rules that follow from it, enforced by check_content.py:
#   * every v3 section names this date
#   * v3 snippets are quoted from the docs, never improvised
#   * NO v3 snippet may claim output — v2 shows real responses, v3 shows config
V3_DOCS_READ = "2026-08-21"

V3 = {
    "product": "Hasura DDN (Data Delivery Network)",
    "cli install": "curl -L https://graphql-engine-cdn.hasura.io/ddn/cli/v4/get.sh | bash",
    "requires": "Docker Compose v2.20+",
    "layout": "supergraph.yaml, globals/, app/metadata/*.hml, "
              "app/connector/<name>/configuration.json, engine/build/",
}

# The HML object kinds, quoted by lessons 3, 9 and 19.
V3_METADATA_KINDS = [
    "DataConnectorLink", "ObjectType", "Model", "Command", "Relationship",
    "BooleanExpressionType", "AggregateExpression", "OrderByExpression",
    "TypePermissions", "ModelPermissions", "CommandPermissions",
    "GraphqlConfig", "AuthConfig", "CompatibilityConfig", "EnginePlugins",
]

# ⚠️ v2 and v3 are different products, not two releases of one. Terminology does
# NOT carry over, and this map is the reference every post writes against.
# Nowhere in the track may a v2 command appear under a v3 heading or the reverse.
V2_TO_V3_TERMS = {
    "tracking a table": "adding a Model",
    "console-driven metadata": "*.hml files compiled by `ddn supergraph build`",
    "Action": "Command on a lambda connector",
    "remote schema": "the GraphQL connector",
    "select permission": "ModelPermissions + TypePermissions",
    "event trigger": "work in progress in DDN — see lesson 12",
    "cron / scheduled trigger": "NOT SUPPORTED in DDN — see lesson 12",
    "admin secret": "GONE — there is no admin secret in DDN",
}

# ---------------------------------------------------------------------------
# The v2 -> v3 comparison table
# ---------------------------------------------------------------------------
# Required by the README: "on the getting started page, have a comparison table
# for v2 and v3 and show each item and how they are different in v3".
#
# It lives here as DATA, not as prose inside one post, for two reasons. It is
# quoted at two different granularities — the full table on the getting-started
# page and a short orientation cut in lesson 1 — and a table maintained twice is
# a table that disagrees with itself within a month. check_content.py asserts the
# getting-started post actually renders every row.
#
# ⚠️ SOURCED, NOT REMEMBERED. The availability column comes from Hasura's own
# feature-availability matrix and glossary, read on V3_DOCS_READ. Two rows here
# contradict what "everyone knows" about DDN and were wrong in this project's
# first draft:
#
#   * Event triggers are WIP, not absent. It is CRON triggers that are gone.
#   * The admin secret does not exist in DDN at all. Every v2 tutorial leans on
#     it, so this is the single most surprising row in the table.
#
# Legend used in the `v3` column, matching Hasura's own:
#   (C)  connector-dependent      WIP  work in progress
#   *    supported, but implemented differently than v2
V2_V3_COMPARISON = [
    # ------------------------------------------------------- how you work
    ("Workflow", [
        ("Where you configure it",
         "The web Console — click to track a table, click to add a permission",
         "`.hml` files in your editor, driven by the `ddn` CLI and a VS Code extension",
         "Code-first. The DDN console is for testing, traces and analytics, not authoring."),
        ("Metadata format",
         "A JSON/YAML tree, applied to a running engine over the metadata API",
         "HML — 'an extension of YAML' — compiled into a build",
         "Metadata stops being a live API you mutate and becomes source you compile."),
        ("Applying a change",
         "Apply metadata; the running engine picks it up immediately",
         "`ddn supergraph build create` produces an **immutable** build",
         "Every build is immutable and gets its own unique GraphQL endpoint, so you "
         "can test one before it is anyone's production."),
        ("CLI",
         "`hasura`",
         "`ddn`",
         "Different binary, different install, no shared commands."),
        ("Running it locally",
         "`docker run hasura/graphql-engine`, then open the console",
         "`ddn supergraph init` then `ddn run docker-start`",
         "The CLI scaffolds a project directory; Docker Compose v2.20+ is required."),
        ("Open source",
         "Community Edition is Apache-2.0 and the whole engine self-hosts",
         "Engine and connectors are open source and self-hostable",
         "⚠️ The **control plane is closed-source and commercial**. The v3 split has "
         "no v2 counterpart."),
    ]),
    # ----------------------------------------------------------- data sources
    ("Data sources", [
        ("Connecting a database",
         "Built-in support for a fixed set of sources, configured with a connection URL",
         "A **Native Data Connector (NDC)** per source, from the Connector Hub",
         "`ddn connector init` scaffolds it. Adding a new kind of source is writing "
         "a connector, not waiting for a Hasura release."),
        ("Exposing a table",
         "**Track** the table",
         "Add a **Model** (`ddn model add`)",
         "The word changes and so does the mechanism: a Model is a metadata object "
         "you keep in git, not a row in the engine's state."),
        ("Several sources at once",
         "Several sources on one engine",
         "**Subgraphs** composed into a **supergraph**",
         "A subgraph is a self-contained domain with its own permissions, SDLC and "
         "repository — the unit of team ownership."),
        ("Query push-down",
         "Hasura compiles to SQL for sources it supports natively",
         "The connector declares its capabilities and Hasura pushes down what it can",
         "Including **authorization** push-down, which v2 could not do."),
    ]),
    # ------------------------------------------------------------- the API
    ("The GraphQL API", [
        ("Queries", "✅", "✅", "The generated schema is deliberately v2-compatible."),
        ("Mutations", "✅ generated insert/update/delete",
         "✅ (C)", "Connector-dependent — a connector must implement them."),
        ("Native mutations", "❌", "✅",
         "New in v3 — v2 had native queries but no native mutations."),
        ("Subscriptions", "✅ live queries and streaming", "✅, **streaming WIP**",
         "Plain subscriptions work; streaming subscriptions are not finished."),
        ("Filtering",
         "`where` on an auto-generated `bool_exp`",
         "An explicit **BooleanExpressionType**",
         "You declare which fields are filterable instead of getting all of them."),
        ("Sorting / aggregates",
         "Auto-generated `order_by`, `_aggregate`",
         "**OrderByExpression** and **AggregateExpression** (C)",
         "Declared per model rather than generated wholesale."),
        ("Relationships",
         "Object and array relationships, within one source",
         "The **Relationship** kind",
         "Can cross connectors and subgraphs, which v2's could not."),
        ("Field naming",
         "`HASURA_GRAPHQL_DEFAULT_NAMING_CONVENTION` env var",
         "**GraphqlConfig** in the globals subgraph",
         "Moves from an env var to a metadata object."),
        ("REST",
         "RESTified endpoints, built in",
         "Via **plugins**; plus a first-class **JSON:API**",
         "JSON:API has no v2 counterpart."),
    ]),
    # -------------------------------------------------------- business logic
    ("Business logic", [
        ("Custom logic in the schema",
         "**Actions** — declare types, point at an HTTP endpoint",
         "**Commands** on a **lambda connector**",
         "You write a TypeScript/Python/Go function in the project instead of "
         "hosting a webhook and describing it."),
        ("Existing GraphQL API",
         "**Remote schemas**",
         "The **GraphQL connector**",
         "Same goal, different mechanism — it becomes a connector like any other."),
        ("On data change",
         "**Event triggers** — webhook on insert/update/delete, with retries",
         "**WIP**",
         "⚠️ Not yet available. Plan to keep this outside Hasura when moving to v3."),
        ("On a schedule",
         "**Cron / scheduled triggers**",
         "❌ **Not supported**",
         "⚠️ No replacement. This one is simply gone."),
    ]),
    # ------------------------------------------------------------------ auth
    ("Auth", [
        ("Authentication",
         "`HASURA_GRAPHQL_JWT_SECRET` or an auth webhook, set as env vars",
         "**AuthConfig**, in the globals subgraph",
         "Configured as metadata, and it is **supergraph-level** — one auth setup "
         "for every subgraph."),
        ("Admin access",
         "`HASURA_GRAPHQL_ADMIN_SECRET` grants the unrestricted built-in `admin` role",
         "❌ **There is no admin secret**",
         "⚠️ The biggest surprise in this table. Every v2 habit built on the admin "
         "secret — seeding, scripts, the console — needs rethinking. API access "
         "uses a Cloud PAT (`cloud_pat` header)."),
        ("Permissions",
         "`select` / `insert` / `update` / `delete` permissions, per role, per table",
         "**TypePermissions** (fields) + **ModelPermissions** (rows) + "
         "**CommandPermissions**",
         "Split by what is being protected instead of by operation, and declared "
         "**per subgraph** rather than globally."),
    ]),
    # ------------------------------------------------------------ production
    ("Production", [
        ("Caching", "✅ `@cached` — Enterprise/Cloud only", "✅* via **plugins**",
         "Both are paid surfaces, by different means."),
        ("Allow list", "✅ Enterprise/Cloud only", "✅* via **plugins**", ""),
        ("API limits / rate limiting", "✅ Enterprise/Cloud only", "**WIP**", ""),
        ("Read replicas", "✅ Enterprise/Cloud only", "✅",
         "No longer gated behind Enterprise."),
        ("Database migrations",
         "`hasura migrate` manages your SQL migrations",
         "Not Hasura's job",
         "⚠️ Use your own migration tool, then `ddn connector introspect` to pick "
         "the change up. A real workflow change for anyone leaning on the v2 CLI."),
        ("CI/CD",
         "`hasura migrate apply` + `hasura metadata apply`",
         "`ddn supergraph build create`",
         "Builds are immutable and independently testable, so promotion replaces "
         "in-place apply."),
        ("Hosting",
         "Self-host the engine, or Hasura Cloud",
         "DDN Cloud, or **Private DDN**",
         "The data plane self-hosts; the control plane does not."),
    ]),
]

# The post that must render the full table. The README asks for it "on the
# getting started page", and this is the page named Getting Started — it is also
# the one about moving a v2 project to v3, which is where the table earns its
# keep. Lesson 1 carries a short orientation cut of the same data.
COMPARISON_HOME = "hasura-ddn-getting-started"

# The rows lesson 1 shows, by item name — enough to establish "these are two
# different products" without pre-empting lesson 18.
COMPARISON_TEASER = [
    "Where you configure it",
    "Exposing a table",
    "Custom logic in the schema",
    "Admin access",
    "On a schedule",
]

# ---------------------------------------------------------------------------
# Ordering
# ---------------------------------------------------------------------------
# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later,
# so the pager reads lesson 1 -> lesson 20. Re-base the whole track by editing
# these two values; nothing else needs to change.
START_DATE = datetime(2026, 6, 24, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    """The publish timestamp for the index-th lesson, 0-based."""
    return (START_DATE + timedelta(days=STEP_DAYS * index)).strftime("%Y-%m-%dT%H:%M:%S")


# Authored in reading order. `state` is documentation, not data: "rewrite" means
# the slug already exists on the live site and must not change. `words` on a
# rewrite records what that URL serves TODAY, measured off the prod tree on
# 2026-08-21 — it is why the rewrite is worth doing.
_TRACK = [
    # ----------------------------------------------------------- foundations
    {
        "slug": "hasura-introduction",
        "title": "Hasura – What It Is and Why It Exists",
        "state": "rewrite", "words": 84,
        "tags": ["hasura", "graphql", "postgres"],
        "excerpt": (
            "Start here. What Hasura actually does — point it at a Postgres database and get a "
            "GraphQL API with filtering, pagination, relationships and permissions without "
            "writing a resolver — and, just as important, what it does not do. Why v2 and v3 "
            "(DDN) are two different products rather than two releases of one, the exact "
            "versions this track is written against, the booking app every example comes from, "
            "and the full lesson index in reading order."
        ),
    },
    {
        "slug": "hasura-installation",
        "title": "Hasura – Installation and Your First Query",
        "state": "rewrite", "words": 135,
        "tags": ["hasura", "graphql", "docker"],
        "excerpt": (
            "Get an engine running and a real query answered in one sitting. The Docker Compose "
            "service that runs Hasura next to Postgres, why the database port inside the compose "
            "network is not the one you published, the admin secret and what it grants, and the "
            "console. Then the same thing in v3: installing the `ddn` CLI, `ddn supergraph init` "
            "and `ddn run docker-start`."
        ),
    },
    {
        "slug": "hasura-metadata",
        "title": "Hasura – Metadata Is the Source of Truth",
        "state": "rewrite", "words": 0,   # this URL currently serves an empty page
        "tags": ["hasura", "graphql", "metadata"],
        "excerpt": (
            "Hasura's schema is not in your database and not in your code — it is metadata, and "
            "understanding that one fact explains most of the product. What tracking a table "
            "means, why clicking in the console is fine until two people do it, and how to keep "
            "metadata in version control and apply it from a script. Then v3, where metadata "
            "stops being a live API and becomes `.hml` files you compile."
        ),
    },
    # --------------------------------------------------------- the data API
    {
        "slug": "hasura-query",
        "title": "Hasura – Queries",
        "state": "rewrite", "words": 0,
        "tags": ["hasura", "graphql", "query"],
        "excerpt": (
            "The query language you get for free. `where` with `_eq`, `_gt`, `_in`, `_like`, "
            "`_and`/`_or`/`_not`, then `order_by`, `limit`/`offset`, cursor pagination, "
            "aggregates and `distinct_on` — each shown with the real response from a running "
            "engine. Also the naming-convention setting that decides whether your fields come "
            "back `price_per_night` or `pricePerNight`, and what it looks like in v3."
        ),
    },
    {
        "slug": "hasura-relationships",
        "title": "Hasura – Relationships and Nested Queries",
        "state": "new",
        "tags": ["hasura", "graphql", "postgres"],
        "excerpt": (
            "Relationships are what make a Hasura API worth using: one round trip returns a "
            "listing, its host, its photos and its reviews. Object versus array relationships, "
            "how foreign keys suggest them and why you can define one without a foreign key, "
            "filtering and ordering a parent by a child's column, and the n+1 question everyone "
            "asks. Plus the `Relationship` kind in v3 and what changes when the two sides live "
            "in different connectors."
        ),
    },
    {
        "slug": "hasura-mutation",
        "title": "Hasura – Mutations",
        "state": "rewrite", "words": 73,
        "tags": ["hasura", "graphql", "mutation"],
        "excerpt": (
            "Writing through the API. `insert`, `update`, `delete`, their `_one` variants, "
            "`returning`, upserts with `on_conflict`, and the fact that several mutations in one "
            "request run in a single transaction while several requests do not. Also the harder "
            "question this track's demo app answers with a deliberate no: which writes belong in "
            "Hasura at all, and which belong behind your own API."
        ),
    },
    {
        "slug": "hasura-subscription",
        "title": "Hasura – Subscriptions",
        "state": "rewrite", "words": 0,
        "tags": ["hasura", "graphql", "subscription", "react"],
        "excerpt": (
            "Live data over a websocket, wired into a real React app with Apollo Client. The "
            "difference between a live query and a streaming subscription, why a subscription is "
            "just a query you keep open, how Hasura multiplexes many clients onto few database "
            "polls, and the permission and cost questions that decide whether you should use one "
            "at all. Includes the auth handshake that trips everyone up."
        ),
    },
    # ------------------------------------------------------------------ auth
    {
        "slug": "hasura-authentication",
        "title": "Hasura – Authentication",
        "state": "rewrite", "words": 458,
        "tags": ["hasura", "graphql", "jwt", "security"],
        "excerpt": (
            "Hasura does not log anyone in — it verifies a token somebody else issued, and "
            "getting that split right is most of the work. JWT mode versus webhook mode, the "
            "`x-hasura-*` claims a token has to carry, the admin secret and why it must never "
            "reach a browser, and the unauthorized role that decides what a visitor with no "
            "token can see. Shown with one JWT secret shared between Hasura and a FastAPI "
            "backend — then `AuthConfig` in v3, where the admin secret does not exist at all."
        ),
    },
    {
        "slug": "hasura-authorization",
        "title": "Hasura – Authorization and Permissions",
        "state": "rewrite", "words": 234,
        "tags": ["hasura", "graphql", "security", "postgres"],
        "excerpt": (
            "The most important chapter in the track, because a mistake here is a data breach "
            "rather than a bug. Roles, row-level filters, column allowlists and session "
            "variables, worked through four real roles. Three traps with teeth: `admin` is "
            "reserved and cannot be given permissions, roles do not inherit from each other, and "
            "permissions do not cascade through relationships. Then `TypePermissions` and "
            "`ModelPermissions` in v3."
        ),
    },
    # ------------------------------------------------- beyond the database
    {
        "slug": "hasura-action",
        "title": "Hasura – Actions",
        "state": "rewrite", "words": 115,
        "tags": ["hasura", "graphql", "actions"],
        "excerpt": (
            "Actions are how anything Hasura cannot generate gets into the same GraphQL schema: "
            "you declare a type, point it at an HTTP endpoint, and it appears alongside the "
            "generated fields. Custom types, the request payload Hasura sends, forwarding client "
            "headers so your handler still knows who is calling, permissions, and error shapes. "
            "Shown with a real Action in front of a FastAPI endpoint, and its v3 replacement — a "
            "`Command` on a business-logic connector."
        ),
    },
    {
        "slug": "hasura-remote-schemas",
        "title": "Hasura – Remote Schemas and Federation",
        "state": "new",
        "tags": ["hasura", "graphql", "federation"],
        "excerpt": (
            "Stitching an existing GraphQL API into Hasura's schema so clients see one graph "
            "instead of two. Adding a remote schema, the namespacing and type-collision problems "
            "that follow, remote relationships that join a database row to a field on another "
            "service, and how permissions and header forwarding work across the boundary. Then "
            "v3, where this stops being a bolt-on and becomes what the supergraph is."
        ),
    },
    {
        "slug": "hasura-triggers",
        "title": "Hasura – Event Triggers and Scheduled Triggers",
        "state": "rewrite", "words": 1,
        "tags": ["hasura", "graphql", "webhooks"],
        "excerpt": (
            "Running code when data changes, without polling. Event triggers fire a webhook on "
            "insert, update or delete and retry it with a backoff; scheduled triggers do the "
            "same on a cron or at a one-off future time. Delivery guarantees, why your handler "
            "must be idempotent, and how to inspect and replay a failed event. Shown on a real "
            "bookings table — and with the awkward v3 news stated plainly: event triggers are "
            "still work in progress and cron triggers are not supported at all."
        ),
    },
    # ------------------------------------------------------------ production
    {
        "slug": "hasura-migrations-and-cicd",
        "title": "Hasura – Migrations, Metadata and CI/CD",
        "state": "new",
        "tags": ["hasura", "graphql", "devops", "cicd"],
        "excerpt": (
            "How a schema change gets from your laptop to production without anyone clicking in "
            "a console. What the Hasura CLI's migrations, metadata and seeds directories each "
            "hold, why metadata and migrations must move together, and the awkward question of "
            "who owns the schema when your ORM already runs its own migrations. Then a pipeline "
            "that applies both on merge, and the v3 equivalent built on `ddn supergraph build`."
        ),
    },
    {
        "slug": "hasura-caching-and-performance",
        "title": "Hasura – Caching and Performance",
        "state": "new",
        "tags": ["hasura", "graphql", "performance"],
        "excerpt": (
            "Making it fast, and knowing what to measure first. Reading the SQL Hasura generates "
            "with `EXPLAIN`, the indexes that decide whether a filter is instant or a table "
            "scan, why deep nesting costs more than it looks, and the row limits that stop one "
            "query taking the database down. Also RESTified endpoints for clients that want a "
            "URL, and a straight account of which caching features need Enterprise."
        ),
    },
    {
        "slug": "hasura-security",
        "title": "Hasura – Securing It for Production",
        "state": "new",
        "tags": ["hasura", "graphql", "security", "devops"],
        "excerpt": (
            "The checklist between a working Hasura and one you can put on the internet. Turning "
            "the console and introspection off, keeping the admin secret out of everything a "
            "client can read, why an unauthenticated request is not the same as a blocked one, "
            "restricting what the engine can reach at the database level, and the allow-list and "
            "rate-limiting features that need Enterprise — said plainly rather than assumed."
        ),
    },
    {
        "slug": "hasura-observability",
        "title": "Hasura – Logging, Metrics and Tracing",
        "state": "new",
        "tags": ["hasura", "graphql", "devops", "observability"],
        "excerpt": (
            "Knowing what your API is doing once real traffic hits it. The log types Hasura can "
            "emit and which ones are worth turning on, reading a query log to find the slow "
            "operation rather than guessing, the health and metrics endpoints, and tracing a "
            "request across Hasura and the service behind an Action. Plus what changes in v3."
        ),
    },
    {
        "slug": "hasura-deployment",
        "title": "Hasura – Deployment",
        "state": "rewrite", "words": 166,
        "tags": ["hasura", "graphql", "devops", "docker"],
        "excerpt": (
            "Getting it running somewhere that is not your laptop. The environment variables that "
            "actually matter in production, running the engine on Docker or Kubernetes with "
            "health checks and more than one replica, database connection pooling and why it bites "
            "before anything else does, zero-downtime metadata changes, and where Hasura Cloud "
            "saves you work. Then DDN and Private DDN in v3."
        ),
    },
    # ----------------------------------------------------------- v3 in depth
    {
        "slug": "hasura-ddn-getting-started",
        "title": "Hasura v3 (DDN) – Getting Started, and Upgrading from v2",
        "state": "new",
        "tags": ["hasura", "graphql", "ddn"],
        "excerpt": (
            "The v3 half of the track in one piece. What a supergraph, a subgraph and a data "
            "connector are, the whole `ddn` walkthrough from `supergraph init` to a running local "
            "engine, and what the generated project tree actually contains. Then the part most "
            "people arrive for: what an existing v2 project has to become, which concepts carry "
            "over, and which ones — event triggers most sharply — simply do not."
        ),
    },
    {
        "slug": "hasura-ddn-data-modeling",
        "title": "Hasura v3 (DDN) – Data Modeling with HML",
        "state": "new",
        "tags": ["hasura", "graphql", "ddn", "metadata"],
        "excerpt": (
            "v3's metadata in depth, because in v3 the metadata is the product. Every object kind "
            "and what it is for — `DataConnectorLink`, `ObjectType`, `Model`, `Command`, "
            "`Relationship`, the boolean-expression, aggregate and order-by types, the three "
            "permission kinds, and the global config objects — worked through by modelling the "
            "same booking schema the v2 half of this track uses."
        ),
    },
    {
        "slug": "hasura-interview-questions",
        "title": "Hasura – Interview Questions",
        "state": "new",
        "tags": ["hasura", "graphql", "interview"],
        "excerpt": (
            "The questions Hasura interviews actually ask, answered the way you would say them "
            "out loud. How Hasura generates a schema without resolvers, how permissions really "
            "work and why relationships do not cascade them, when to reach for an Action instead "
            "of a mutation, what an event trigger guarantees, the n+1 question, and the one that "
            "separates people who have shipped it: what you turn off before going to production."
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

# Slugs that already exist on the live site and must never change. All eleven
# were published in early 2020; check_content.py fails if one leaves the manifest.
FROZEN_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "rewrite"}

# What each frozen URL serves today, measured off the prod tree on 2026-08-21.
# Four of them are empty pages. This is the baseline the rewrite has to beat, and
# check_content.py uses it to refuse a "rewrite" that is not actually longer.
EXISTING_WORDS = {e["slug"]: e["words"] for e in _TRACK if e["state"] == "rewrite"}

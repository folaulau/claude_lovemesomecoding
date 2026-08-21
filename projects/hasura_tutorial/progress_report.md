# Hasura tutorial track — progress report

**Status:** WRITTEN — all 20 post bodies exist, pass every check, and are seeded to the **local**
tree. NOT published to prod. Outstanding: the four StayHub additions, which four posts describe but
which do not exist in the demo app yet.
**Started:** 2026-08-21
**Where it lands:** https://lovemesomecoding.com/hasura

---

## What this is

`/hasura` holds **11 posts**, every one published in early 2020 and every one thin to the point of
being empty. Measured off the prod content tree on 2026-08-21:

| slug | words | code blocks | headings |
|---|---:|---:|---:|
| `hasura-authentication` | 458 | 2 | 0 |
| `hasura-authorization` | 234 | 0 | 0 |
| `hasura-deployment` | 166 | 0 | 2 |
| `hasura-installation` | 135 | 2 | 0 |
| `hasura-action` | 115 | 0 | 1 |
| `hasura-introduction` | 84 | 0 | 0 |
| `hasura-mutation` | 73 | 0 | 0 |
| `hasura-triggers` | 1 | 0 | 0 |
| `hasura-metadata` | **0** | 0 | 0 |
| `hasura-query` | **0** | 0 | 0 |
| `hasura-subscription` | **0** | 0 | 0 |

**1,266 words across the entire collection**, and none of them carry a single tag. Four posts have
no body at all — they are live URLs serving an empty page.

This project builds a **20-post Hasura track**: all 11 rewritten in place at their existing URLs,
plus 9 new ones.

### A note on the README

The first requirement line reads *"update java datastructure tutorial posts on
https://lovemesomecoding.com/hasura"* — copy-paste from the `java_datastructure` README. Read as
"update the Hasura posts". Flagged 2026-08-21, not treated as scope.

A later line was added on 2026-08-21: *"on the getting started page, have a comparison table for v2
and v3 and show each item and how they are different in v3"*. See **The comparison table** below.

---

## Where it stands

| | |
|---|---|
| Survey of `/hasura` | ✅ 11 posts, prod tree read directly |
| Topic table | ✅ 20 lessons, agreed 2026-08-21 |
| Content pipeline | ✅ **fixed** — `graphql` added to both halves, verified end to end |
| `manifest.py` | ✅ 20 posts, 11 frozen slugs cross-checked against prod |
| `check_content.py` | ✅ built, and each of its four track rules test-fired |
| `check_snippets.py` | ✅ built; matching, drift detection and v3 exclusion all test-fired |
| `seed.py` | ✅ built, dry-runs clean against the local tree |
| Demo app (StayHub) | ✅ exists, runs, answers live; ⬜ four additions still needed |
| Post bodies | ✅ **20 of 20**, 17,375 words, 121 code blocks (27 GraphQL) |
| Seeded to `local` | ✅ archive holds 20, dates in reading order |
| Published to `prod` | ⬜ **not done** — deliberate, see below |

### ⚠️ Four posts describe StayHub surfaces that do not exist yet

The decision on 2026-08-21 was to add an Action, an event trigger, a subscription and an insert
permission to StayHub and quote them. **That app work was never done.** The four posts were written
anyway, from StayHub's real schema, roles and design decisions:

| Post | What it shows | Status |
|---|---|---|
| `hasura-mutation` | insert permission with `check` + `set` presets | shape is correct, **not applied to StayHub** |
| `hasura-subscription` | Apollo `GraphQLWsLink` split-link wiring | **not built in the React app** |
| `hasura-action` | Action → FastAPI `createBooking` | **no such Action or endpoint** |
| `hasura-triggers` | event trigger on `bookings` | **no such trigger** |

None of them claims to be running output, and `check_snippets.py` classifies their blocks as
illustrative rather than app-verified. But they are the four least-verified posts in the track and
should be either built-and-checked or explicitly framed as designs before prod.

### What the tooling proved on the way in

- The 11 frozen slugs match the live `/hasura` set **exactly** — no orphans, no typos. If one is
  ever renamed, `check_content.py` fails and `seed.py --env prod` refuses outright.
- `seed.py` correctly reads the existing 2020 dates and shows the `--force-dates` rebase
  (`2020-02-17 -> 2026-06-24`) before writing anything.
- All 90 backend tests still pass at 95% coverage after the `graphql` change.

---

## ✅ The content pipeline now supports `graphql` — done 2026-08-21

This was the one blocking pipeline gap, and it is invisible when it bites: a GraphQL snippet does
not error, it silently normalises to `plaintext` and renders grey.

`SUPPORTED_LANGUAGES` listed java, python, bash, sql, javascript, css, markup, powershell, yaml,
json, markdown, groovy, kotlin, docker, typescript, jsx, tsx, properties, scss, nginx, plaintext —
and **not `graphql`**. Neither did the frontend import the grammar. On a **Hasura** track GraphQL is
the most-quoted language in the whole collection, so every query, mutation, subscription and SDL
block would have shipped unhighlighted.

Both halves were changed, because they have to agree:

| Where | Change |
|---|---|
| `lovemesomecoding_backend/app/services/content.py` | `"graphql"` added to `SUPPORTED_LANGUAGES`; `"gql": "graphql"` added to `LANGUAGE_ALIASES` |
| `lovemesomecoding_frontend/src/lib/content.ts` | `import 'prismjs/components/prism-graphql'` added |

`prismjs/components/prism-graphql.js` was already in `node_modules`, so no dependency change was
needed.

Verified end to end rather than assumed:

```
normalize_language('graphql') -> 'graphql'      # was 'plaintext'
normalize_language('gql')     -> 'graphql'
normalize_language('nope')    -> 'plaintext'    # unchanged

Prism.highlight(<a Hasura query>, Prism.languages.graphql)  ->  29 tokens
```

All 90 backend tests still pass, coverage 95%.

⚠️ **The frontend import is not optional and not cosmetic.** The backend normaliser is what decides
the `language-graphql` class; if the class ships and the grammar does not, Prism finds no grammar
for it at build time. Change both or neither — `check_content.py` now asserts both ends are present,
so the two can never drift apart silently.

Nothing else is needed: `hasura` is already in the nav (`nav.ts:18`, under **Databases**) with the
display name `Hasura` (`nav.ts:50`). `sql`, `yaml`, `json`, `bash`, `typescript`, `tsx` and `python`
— everything else this track quotes — are all already supported.

The stored category record still has `"name": "hasura"` (lowercase). `seed.py` upserts the category,
which fixes it to `Hasura` on the first write.

---

## The demo app — StayHub

`lovemesomecoding_demo_project/stayhub` is the demo app, and unlike the Docker track's situation the
Hasura surface **already exists and is already running**. Verified live on 2026-08-21:

```
$ curl -s http://localhost:8081/v1/version
{"server_type":"ce","version":"v2.42.0"}

$ curl -s -X POST http://localhost:8081/v1/graphql -H 'Content-Type: application/json' \
    -d '{"query":"query { properties(limit:2) { publicId title city pricePerNight } }"}'
{"data":{"properties":[{"publicId":"89c69134-...","title":"Modern Condo, Downtown Skyline",
 "city":"Seattle","pricePerNight":198.00}, ...]}}
```

Note what that request proves in one shot: no auth header, and it still returns data — because
`HASURA_GRAPHQL_UNAUTHORIZED_ROLE: anonymous` is set — and the fields come back **camelCase**,
because `naming_convention` is on. Both are lessons, and both are already true of the running stack.

### What StayHub already gives the track

| Surface | Where |
|---|---|
| Engine + Postgres in Compose, healthchecks, port shift | `stayhub/docker-compose.yml` |
| Metadata as code, applied over the metadata API | `stayhub/hasura/metadata.py`, `hasura/scripts/apply.py` |
| 4 roles — `anonymous`, `customer`, `host`, `staff` | `metadata.py` |
| Column allowlists (incl. the `password_hash` trap) | `USER_PUBLIC_COLUMNS` etc. |
| Row-level filters, session variables via `X-Hasura-User-Id` | `PUBLISHED_ONLY`, `OWN_BOOKING`, … |
| Object + array relationships | `_tables()` |
| JWT shared with FastAPI (one login, two services) | `HASURA_GRAPHQL_JWT_SECRET` |
| Admin secret and why it never reaches the browser | compose header |
| `naming_convention` / `graphql-default` | compose env |
| Client-side queries through Apollo Client 4 | `stayhub-react-*-frontend/src/graphql/queries.ts` |

`metadata.py`'s own comments already contain three hard-won gotchas worth quoting directly: `admin`
is a reserved role, Hasura roles are **not** hierarchical, and permissions do **not** cascade
through relationships.

### The gap — four surfaces StayHub does not have

Every write in StayHub goes through FastAPI, so the engine is read-only in practice. Four lessons
have nothing to quote. **Agreed 2026-08-21: add them to StayHub and run them before quoting.**

| To add | Serves lesson |
|---|---|
| A Hasura **Action** fronting a FastAPI endpoint, with `forward_client_headers` | 10 |
| An **event trigger** on `bookings` → a webhook FastAPI handles | 12 |
| A **subscription** in the customer React app (live booking status) | 7 |
| An **insert permission** so at least one write is a real Hasura mutation | 6 |

⚠️ These are additions, not replacements. StayHub's "all writes go through FastAPI" design is a
recorded decision in its own `progress_report.md` and the existing read path must keep working
exactly as it does. The mutation lesson gets a *new* narrow insert permission; it does not move an
existing FastAPI write into Hasura.

---

## The comparison table

Added to the README on 2026-08-21: *"on the getting started page, have a comparison table for v2 and
v3 and show each item and how they are different in v3."*

### Where it lives, and why it is data

The rows are in **`manifest.py` as `V2_V3_COMPARISON`**, not as prose inside a post. Two reasons:

1. It is shown at two granularities — the full 33 rows on the getting-started page, and a 5-row
   orientation cut in lesson 1, so a reader knows v2 and v3 are different products before reading
   nineteen posts that assume it. A table maintained twice disagrees with itself within a month.
2. `check_content.py` can then assert the post actually renders **every** row. The failure mode
   worth guarding is not a missing table, it is a table that quietly loses its awkward rows —
   "Admin access" and "On a schedule" are the two nobody wants to write down.

`render_table.py` turns the data into HTML (or markdown) to paste into the post. Posts here are
plain static HTML with nothing templating them at build time, so pasting is the workflow; the
checker is what stops a hand-edit from dropping a row.

Canonical page: **`hasura-ddn-getting-started`** (lesson 18) — the page named Getting Started, and
the one about moving a v2 project across, which is where the table earns its keep. Lesson 1 carries
the short cut. If you meant lesson 1 to hold the full table instead, it is a one-line change to
`COMPARISON_HOME`.

### Sourcing

Every row comes from Hasura's own docs read on **2026-08-21**, not from memory — specifically the
feature-availability matrix, the DDN glossary and the quickstart. That mattered: two rows came out
the opposite of the assumption this project started with (see the box above).

Legend, matching Hasura's own: **(C)** connector-dependent · **WIP** work in progress ·
**\*** supported but implemented differently than v2 · **(EE)** Enterprise/Cloud only.

### The table

| Item | Hasura v2 | Hasura v3 (DDN) | What actually changes |
|---|---|---|---|
| **Workflow** | | | |
| Where you configure it | The web Console — click to track a table, click to add a permission | `.hml` files in your editor, driven by the `ddn` CLI and a VS Code extension | Code-first. The DDN console is for testing, traces and analytics, not authoring. |
| Metadata format | A JSON/YAML tree, applied to a running engine over the metadata API | HML — 'an extension of YAML' — compiled into a build | Metadata stops being a live API you mutate and becomes source you compile. |
| Applying a change | Apply metadata; the running engine picks it up immediately | `ddn supergraph build create` produces an **immutable** build | Every build is immutable and gets its own unique GraphQL endpoint, so you can test one before it is anyone's production. |
| CLI | `hasura` | `ddn` | Different binary, different install, no shared commands. |
| Running it locally | `docker run hasura/graphql-engine`, then open the console | `ddn supergraph init` then `ddn run docker-start` | The CLI scaffolds a project directory; Docker Compose v2.20+ is required. |
| Open source | Community Edition is Apache-2.0 and the whole engine self-hosts | Engine and connectors are open source and self-hostable | ⚠️ The **control plane is closed-source and commercial**. The v3 split has no v2 counterpart. |
| **Data sources** | | | |
| Connecting a database | Built-in support for a fixed set of sources, configured with a connection URL | A **Native Data Connector (NDC)** per source, from the Connector Hub | `ddn connector init` scaffolds it. Adding a new kind of source is writing a connector, not waiting for a Hasura release. |
| Exposing a table | **Track** the table | Add a **Model** (`ddn model add`) | The word changes and so does the mechanism: a Model is a metadata object you keep in git, not a row in the engine's state. |
| Several sources at once | Several sources on one engine | **Subgraphs** composed into a **supergraph** | A subgraph is a self-contained domain with its own permissions, SDLC and repository — the unit of team ownership. |
| Query push-down | Hasura compiles to SQL for sources it supports natively | The connector declares its capabilities and Hasura pushes down what it can | Including **authorization** push-down, which v2 could not do. |
| **The GraphQL API** | | | |
| Queries | ✅ | ✅ | The generated schema is deliberately v2-compatible. |
| Mutations | ✅ generated insert/update/delete | ✅ (C) | Connector-dependent — a connector must implement them. |
| Native mutations | ❌ | ✅ | New in v3 — v2 had native queries but no native mutations. |
| Subscriptions | ✅ live queries and streaming | ✅, **streaming WIP** | Plain subscriptions work; streaming subscriptions are not finished. |
| Filtering | `where` on an auto-generated `bool_exp` | An explicit **BooleanExpressionType** | You declare which fields are filterable instead of getting all of them. |
| Sorting / aggregates | Auto-generated `order_by`, `_aggregate` | **OrderByExpression** and **AggregateExpression** (C) | Declared per model rather than generated wholesale. |
| Relationships | Object and array relationships, within one source | The **Relationship** kind | Can cross connectors and subgraphs, which v2's could not. |
| Field naming | `HASURA_GRAPHQL_DEFAULT_NAMING_CONVENTION` env var | **GraphqlConfig** in the globals subgraph | Moves from an env var to a metadata object. |
| REST | RESTified endpoints, built in | Via **plugins**; plus a first-class **JSON:API** | JSON:API has no v2 counterpart. |
| **Business logic** | | | |
| Custom logic in the schema | **Actions** — declare types, point at an HTTP endpoint | **Commands** on a **lambda connector** | You write a TypeScript/Python/Go function in the project instead of hosting a webhook and describing it. |
| Existing GraphQL API | **Remote schemas** | The **GraphQL connector** | Same goal, different mechanism — it becomes a connector like any other. |
| On data change | **Event triggers** — webhook on insert/update/delete, with retries | **WIP** | ⚠️ Not yet available. Plan to keep this outside Hasura when moving to v3. |
| On a schedule | **Cron / scheduled triggers** | ❌ **Not supported** | ⚠️ No replacement. This one is simply gone. |
| **Auth** | | | |
| Authentication | `HASURA_GRAPHQL_JWT_SECRET` or an auth webhook, set as env vars | **AuthConfig**, in the globals subgraph | Configured as metadata, and it is **supergraph-level** — one auth setup for every subgraph. |
| Admin access | `HASURA_GRAPHQL_ADMIN_SECRET` grants the unrestricted built-in `admin` role | ❌ **There is no admin secret** | ⚠️ The biggest surprise in this table. Every v2 habit built on the admin secret — seeding, scripts, the console — needs rethinking. API access uses a Cloud PAT (`cloud_pat` header). |
| Permissions | `select` / `insert` / `update` / `delete` permissions, per role, per table | **TypePermissions** (fields) + **ModelPermissions** (rows) + **CommandPermissions** | Split by what is being protected instead of by operation, and declared **per subgraph** rather than globally. |
| **Production** | | | |
| Caching | ✅ `@cached` — Enterprise/Cloud only | ✅* via **plugins** | Both are paid surfaces, by different means. |
| Allow list | ✅ Enterprise/Cloud only | ✅* via **plugins** |  |
| API limits / rate limiting | ✅ Enterprise/Cloud only | **WIP** |  |
| Read replicas | ✅ Enterprise/Cloud only | ✅ | No longer gated behind Enterprise. |
| Database migrations | `hasura migrate` manages your SQL migrations | Not Hasura's job | ⚠️ Use your own migration tool, then `ddn connector introspect` to pick the change up. A real workflow change for anyone leaning on the v2 CLI. |
| CI/CD | `hasura migrate apply` + `hasura metadata apply` | `ddn supergraph build create` | Builds are immutable and independently testable, so promotion replaces in-place apply. |
| Hosting | Self-host the engine, or Hasura Cloud | DDN Cloud, or **Private DDN** | The data plane self-hosts; the control plane does not. |

---

## The versions this track is written against

Read off **this machine**, not chosen — same rule as the Docker and Angular tracks. A lesson
claiming a version its snippet was not produced by is exactly the drift nobody spots later.

| | |
|---|---|
| Hasura GraphQL Engine | **v2.42.0** (`server_type: ce` — Community Edition) |
| Hasura CLI | **v2.40.0** (v2.48.0 is available; the track states what it ran) |
| Postgres | 16-alpine |
| Docker Engine | 27.4.0 |
| Apollo Client | 4.2.12 (React 19.2.8, Vite 8, TypeScript 6) |
| FastAPI / SQLAlchemy / Alembic | 0.115.5 / 2.0.36 / 1.14.0 |
| Host | Docker Desktop, aarch64 (Apple Silicon) |

**Community Edition is load-bearing.** `server_type: ce` means the track cannot demonstrate several
things first-hand: query response **caching** (`@cached`), **allow-lists**, **rate limiting** and the
read-replica routing are Hasura **Enterprise/Cloud** features. Those sections are written as
Enterprise/Cloud features and labelled as such rather than being shown running — see lesson 14 and
lesson 15.

### v3 / DDN

`ddn` is **not installed on this machine** (`which ddn` → not found). Per the decision below, the v3
half of the track is written from the official docs and is **not run locally**.

Pinned from https://hasura.io/docs/3.0 on **2026-08-21**:

| | |
|---|---|
| Product name | Hasura **DDN** (Data Delivery Network) — "federated data APIs" |
| CLI install | `curl -L https://graphql-engine-cdn.hasura.io/ddn/cli/v4/get.sh \| bash` |
| Requires | Docker Compose v2.20+ |
| Core commands | `ddn supergraph init`, `ddn connector init -i`, `ddn connector introspect`, `ddn model add`, `ddn command add`, `ddn relationship add`, `ddn supergraph build local`, `ddn run docker-start`, `ddn console --local`, `ddn doctor` |
| Layout | `supergraph.yaml`, `globals/`, `app/metadata/*.hml`, `app/connector/<name>/configuration.json`, `engine/build/` |
| Metadata kinds | `DataConnectorLink`, `ObjectType`, `Model`, `Command`, `Relationship`, `BooleanExpressionType`, `AggregateExpression`, `OrderByExpression`, `TypePermissions`, `ModelPermissions`, `CommandPermissions`, `GraphqlConfig`, `AuthConfig`, `CompatibilityConfig`, `EnginePlugins` |

⚠️ **v2 and v3 are different products, not two releases of one.** v2 is a single engine that reads a
database and is configured through a console; v3 is a build-time supergraph compiled from `.hml`
files over native data connectors, driven entirely by a CLI. Terminology does not carry over:
"tracking a table" becomes "adding a **Model**", an **Action** becomes a **Command** on a **lambda
connector**, and a **remote schema** becomes the **GraphQL connector**. Every post says which product
it is talking about in its own heading. Nowhere in the track may a v2 command appear under a v3
heading or the reverse.

### ⚠️ Two facts this project got wrong on the first pass

Both were corrected on 2026-08-21 after reading Hasura's own feature-availability matrix rather than
working from what everybody assumes about DDN. They are recorded here because they are exactly the
kind of thing that gets re-asserted later:

| Claim | Reality |
|---|---|
| "v3 has no equivalent of event triggers" | **Wrong.** Event triggers are **WIP** in DDN. It is **cron / scheduled triggers** that are ❌ not supported. |
| The admin secret carries over to v3 | **Wrong.** DDN has **no admin secret at all** — API access uses a Cloud PAT (`cloud_pat` header). Every v2 habit built on the admin secret has to be rethought, which makes this the single most surprising row in the comparison table. |

`manifest.py`'s `V2_TO_V3_TERMS` and the lesson 8 and 12 excerpts were all corrected to match.

---

## Decisions

| Decision | Choice | Why |
|---|---|---|
| The 11 existing posts | **Rewrite in place, keep every slug** | All 11 URLs are indexed. Four serve an empty page today, so there is nothing to lose by rewriting and a live URL to lose by renaming. |
| Track size | **20 posts** — 11 rewrites + 9 new | Folau chose it from a three-way option. The README asks for "just the important things to get a project developed and released to production", so this is deliberately tighter than Angular (28) / React (27). |
| Demo app | **StayHub** | It already runs Hasura v2.42.0 over Postgres with four roles, JWT, relationships and column allowlists — the richest Hasura surface in the repo, and it is live right now. |
| v2 examples | **Verified against the running stack** | Every v2 snippet is executed against `localhost:8081` before it is quoted. |
| v3 examples | **Written from the official docs, labelled as not run locally** | Folau chose this over standing up a DDN supergraph. It is faster, and it is an explicit, recorded exception to the track's usual "run everything" rule — see the risk below. |
| The four missing surfaces | **Add them to StayHub, build and run** | Actions, event triggers, subscriptions and a Hasura-side mutation get real, executed examples rather than illustrative ones. |
| The old `~/Github/hasura` project | **Not used** | It is outside `lovemesomecoding_demo_project`, is from Oct 2024, and its own README records that the subscription UI never worked. |
| `graphql` language support | **Add to both backend and frontend** | Non-negotiable on a Hasura track; see the pipeline section. |
| Category display name | `Hasura` | Stored record says `hasura`; `seed.py`'s `upsert_category` corrects it. |
| Dates | Computed from `START_DATE + STEP_DAYS` | Authored before publication, same as Docker. The 2020 dates mean the first prod publish needs `--force-dates`. |

### ⚠️ Risk accepted: the v3 half is unverified

Roughly half of this track's content — every "In v3 (DDN)" section — is transcribed from
hasura.io/docs/3.0 and has **not been run**. This is a deliberate trade Folau made for speed, and it
is the single most likely source of a wrong snippet in the collection.

Mitigations, all of which `check_content.py` will enforce:

- Every v3 section carries a visible note that it is written against the docs, with the date the
  docs were read (**2026-08-21**).
- v3 snippets are quoted from the docs, never improvised. Where the docs do not show a thing, the
  post says so rather than inventing plausible HML.
- No v3 snippet may claim output. v2 sections show real responses; v3 sections show configuration
  only.

---

## Topic list

Reading order. `date` ascends so the prev/next pager reads lesson 1 → lesson 20. Every post covers
**both v2 and v3** except 18 and 19, which are the v3 deep-dive, and 20.

### Part 1 — Foundations

| # | Slug | State | v2 source | v3 source |
|---|---|---|---|---|
| 1 | `hasura-introduction` | **rewrite** | the versions table; StayHub as the demo | what DDN is, and why it is a different product |
| 2 | `hasura-installation` | **rewrite** | `stayhub/docker-compose.yml`, console on :8081 | `ddn supergraph init` + `ddn run docker-start` |
| 3 | `hasura-metadata` | **rewrite** (empty today) | `hasura/metadata.py`, `scripts/apply.py` | `.hml` files, `supergraph.yaml`, `ddn supergraph build local` |

### Part 2 — The data API

| # | Slug | State | v2 source | v3 source |
|---|---|---|---|---|
| 4 | `hasura-query` | **rewrite** (empty today) | real responses from :8081; `where`/`order_by`/`limit`/aggregates | `Model`, `BooleanExpressionType`, `OrderByExpression` |
| 5 | `hasura-relationships` | new | `_tables()` object + array relationships; nested queries | `Relationship` kind, cross-connector relationships |
| 6 | `hasura-mutation` | **rewrite** | the **new** insert permission; `returning`, upsert | DDN's mutation model and `Command` |
| 7 | `hasura-subscription` | **rewrite** (empty today) | the **new** subscription in the customer app, Apollo 4 | DDN subscriptions |

### Part 3 — Auth

| # | Slug | State | v2 source | v3 source |
|---|---|---|---|---|
| 8 | `hasura-authentication` | **rewrite** | `HASURA_GRAPHQL_JWT_SECRET` shared with FastAPI; admin secret; unauthorized role | `AuthConfig`, JWT and webhook modes |
| 9 | `hasura-authorization` | **rewrite** | 4 roles, column allowlists, row filters, session variables | `TypePermissions` + `ModelPermissions` |

### Part 4 — Beyond the database

| # | Slug | State | v2 source | v3 source |
|---|---|---|---|---|
| 10 | `hasura-action` | **rewrite** | the **new** Action → FastAPI, `forward_client_headers` | `Command` + a business-logic connector |
| 11 | `hasura-remote-schemas` | new | remote schemas, remote relationships, federation | multiple connectors and subgraphs |
| 12 | `hasura-triggers` | **rewrite** (1 word today) | the **new** event trigger on `bookings`; scheduled triggers | ⚠️ event triggers **WIP**; cron triggers ❌ not supported |

### Part 5 — Production

| # | Slug | State | v2 source | v3 source |
|---|---|---|---|---|
| 13 | `hasura-migrations-and-cicd` | new | `hasura` CLI v2.40.0, migrations/metadata/seeds vs Alembic | `ddn supergraph build create`, CI/CD |
| 14 | `hasura-caching-and-performance` | new | n+1, `EXPLAIN`, RESTified endpoints, limits. ⚠️ `@cached` is Enterprise — labelled, not shown | DDN caching |
| 15 | `hasura-security` | new | console/introspection off in prod, admin-secret handling. ⚠️ allow-list + rate limiting are Enterprise | DDN's equivalents |
| 16 | `hasura-observability` | new | `HASURA_GRAPHQL_ENABLED_LOG_TYPES` as set in StayHub; metrics, traces | DDN observability |
| 17 | `hasura-deployment` | **rewrite** | self-hosted Compose/k8s, Hasura Cloud tiers | DDN deployment, Private DDN |

### Part 6 — v3 in depth

| # | Slug | State | Covers |
|---|---|---|---|
| 18 | `hasura-ddn-getting-started` | new | supergraph / subgraph / connector end to end, the full `ddn` walkthrough, **and upgrading from v2** |
| 19 | `hasura-ddn-data-modeling` | new | every HML kind, modelling StayHub's own schema in DDN |
| 20 | `hasura-interview-questions` | new | both products |

---

## Frozen slugs

All **11** existing slugs are indexed live URLs and must never change:

```
hasura-introduction   hasura-installation   hasura-metadata   hasura-query
hasura-mutation       hasura-subscription   hasura-authentication
hasura-authorization  hasura-action         hasura-triggers   hasura-deployment
```

`check_content.py` fails if any of them leaves the manifest.

Because all 11 carry 2020 dates and `upsert_post` never overwrites an existing date, the first prod
publish needs `seed.py --force-dates` for the reading order to come out right. Without it the
archive interleaves nine 2026 posts with eleven 2020 ones and the pager reads nonsense.

---

## Log

- **2026-08-21** — Project started. Surveyed `/hasura` off the prod tree (11 posts, 1,266 words
  total, four of them empty). Found StayHub already running Hasura v2.42.0 and verified it answers
  live. Found the `graphql` language gap in both the backend normaliser and the frontend Prism
  imports. Confirmed `hasura` is already in the nav. Read the v2 and v3 doc trees and pinned the DDN
  terminology and CLI. Agreed the three decisions above with Folau: 20 posts, v2 verified / v3
  doc-derived, and the four missing surfaces get added to StayHub.
- **2026-08-21** — Fixed the `graphql` pipeline gap in both repos and verified it end to end
  (normaliser + Prism), backend tests still green at 95%.
- **2026-08-21** — Wrote all 20 post bodies (17,375 words, 121 code blocks). Queried the running
  engine rather than writing from memory, which caught two errors before they shipped: the argument
  is `orderBy` with `ASC`/`DESC` (not `order_by`/`asc`) because `naming_convention` is on, and an
  unauthenticated request for `bookings` returns `field 'bookings' not found in type: 'query_root'`
  — permissions shape the schema per role rather than filtering a shared one. That second finding
  became the spine of lessons 1, 4 and 9. Captured real generated SQL (a `LEFT OUTER JOIN LATERAL`)
  and a real query plan for the relationships and performance lessons.
  Three checks fired during writing and all three were real: a missing v3 heading in lesson 1, a
  missing v3 heading in lesson 19, a missing docs-date in lesson 20. `check_snippets.py` also caught
  a simplified compose block in lesson 2 that had drifted from the real file — replaced with a
  faithful quote using `...` elisions. Seeded all 20 to the local tree.
- **2026-08-21** — README gained the comparison-table requirement. Read Hasura's official
  feature-availability matrix, DDN glossary and quickstart, and built the 33-row table as data in
  `manifest.py` plus `render_table.py` to render it. **Two facts this project had recorded wrong
  were corrected**: event triggers are WIP (not absent) and cron triggers are the ones that are
  gone; and DDN has no admin secret at all. Added two checks — the getting-started page must render
  every row, and lesson 1 must carry the teaser cut — and test-fired both by deleting rows.
- **2026-08-21** — Built `manifest.py` (20 posts, dates computed, 11 frozen slugs), `seed.py`,
  `check_content.py` and `check_snippets.py`. Every non-obvious check was **test-fired against a
  deliberately broken post** rather than assumed to work, and two of them were wrong first time:

  | Bug found by test-firing | Fix |
  |---|---|
  | The v3-heading check never matched. Its negative lookahead asserted the heading text was *not* followed by `</h`, which is true of no heading at all. | Match the heading's inner HTML and strip tags before testing — the normaliser adds `id` attributes and bodies wrap terms in `<code>`. |
  | Every quote of a line with a **trailing** `# comment` read as drift. `hasura/metadata.py` is full of them (`NOTHING_HIDDEN = {}  # an empty filter…`), and only line-start comments were stripped. | A quote-aware `strip_trailing_comment` that cuts at an unquoted `#` preceded by whitespace, so `"#fff"`, `docs#anchor` and `{"tag": "#hasura"}` survive intact. |
  | Drift was undetectable in short blocks: the 3-line lead used to spot a near-miss *was* the whole 3-line block. | Lead is now strictly shorter than its chunk (min 2 lines). |

  Confirmed working afterwards: a verbatim quote matches, a quote with one wrong line is reported as
  `POSSIBLE DRIFT` naming `hasura/metadata.py`, an HML block is excluded from app-matching, and the
  script exits 1 on drift.

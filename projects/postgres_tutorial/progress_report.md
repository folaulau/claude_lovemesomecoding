# Postgres tutorial track — progress report

**Status:** ✅ **PUBLISHED AND LIVE** — 18 posts on https://lovemesomecoding.com/postgre, all 18
URLs verified serving at the edge. Build `394b0bd`, deployed 2026-08-23.
**Started:** 2026-08-22
**Where it lands:** https://lovemesomecoding.com/postgre

---

## What is there now

`/postgre` is **not empty, but it is nearly empty** — two WordPress leftovers, measured off the
local content tree on 2026-08-22:

| slug | date | prose words | code blocks | h2/h3 | reading |
|---|---|---:|---:|---:|---:|
| `postgres-introduction` | 2020-02-19 | 176 | 0 | 0 | 1m |
| `postgres-installation` | 2020-02-19 | 112 | 2 | 0 | 1m |
| **total** | | **288** | **2** | **0** | **2m** |

Three defects, all the same ones the Hasura and FastAPI tracks had to fix:

1. **Both posts are stubs.** 288 prose words across the entire collection. No headings at all, so
   no table of contents and no deep links. `postgres-installation` still tells you to
   `docker pull postgres:12` and download an installer from EnterpriseDB.
2. **Both still carry the WordPress `boldgrid-section` / `container` / `row` / `col-md-12` wrapper
   divs** and `class=""` on every paragraph — dead Bootstrap markup from the old theme.
3. **The category record is broken** — `{"slug": "postgre", "name": "postgre", "description": ""}`.
   Lowercase display name, no standfirst on the archive page.

Neither post has tags. Both are `status: published`.

### The two slugs are frozen

`/postgre/postgres-introduction` and `/postgre/postgres-installation` are live, indexed URLs. The
frontend runs `trailingSlash: false` with a build guard (`scripts/verify-build.mjs`) that **fails
the build** if an indexed post URL stops resolving. They get rewritten **in place** — renaming
either one is a dead link, not a refactor.

Both carry **2020-02-19** dates, and `upsert_post` never overwrites an existing date. Seeding this
track therefore needs `seed.py --force-dates` exactly once per tree, or the archive interleaves two
2020 posts with the rest and the ‹ prev / next › pager reads nonsense. Same trap the FastAPI track
documented.

### Navigation — nothing to do

`src/lib/nav.ts` already lists `postgre` in the **Data Store** group with the display name
`Postgres`. Only the stored category record needs fixing, and `upsert_category` does that.

---

## Sources

Per the README:

- https://www.postgresql.org/docs/current/index.html — the topic spine
- https://www.w3schools.com/postgresql/index.php — cross-check on what a beginner actually needs

Filter: *"the important things to get a project developed and released to production"* — not a post
per catalogue entry.

## Candidate example app

`lovemesomecoding_demo_project/stayhub` runs **Postgres 16-alpine** and is unusually good raw
material for this track — it is not a toy schema:

- `btree_gist` + an `ExcludeConstraint` on `daterange(check_in, check_out, '[)')` that makes
  double-booking impossible at the database level
- `NUMERIC(10,2)` money throughout, `timestamptz`, `UUID` public ids alongside integer PKs
- partial / unique / composite indexes, FK constraints, check constraints
- an outbox table, Alembic migrations, and a real connection-pool configuration

That means transactions, isolation, indexes, constraints and migrations can all be demonstrated
against schema that already exists and already runs, instead of an invented `employees` table.

---

## Decisions — 2026-08-22

| # | Question | Decision |
|---|---|---|
| 1 | Track size | **18 posts** — the 2 frozen slugs rewritten in place plus 16 new. |
| 2 | Post length | **Short — 6–10 reading-minutes**, ~1,200–1,800 prose words. Postgres is reference-heavy; dense tables and runnable SQL beat essays. |
| 3 | Example source | **StayHub's real schema.** Every SQL block is executed before it ships. |

### The lab database — why there is one

Decision 3 has a problem the FastAPI track did not: StayHub's own database holds **12 properties and
3 bookings**. At that size the planner seq-scans everything, so an "add an index" lesson written
against it would show an index the planner never chooses, and an `EXPLAIN` post would be quoting
plans that are true only of a toy.

So `lab/` builds a **separate** database, `stayhub_lab`, in the same container: StayHub's real
schema (`pg_dump --schema-only`, re-takeable with `lab/dump-schema.sh`) filled to production-ish
scale. The `stayhub` database is never written to.

| table | rows | |
|---|---:|---|
| bookings | 400,000 | 20 per property, 2024-01-01 → 2025-06-05 |
| payments | 374,518 | one per booking that is not PENDING |
| reviews | 200,612 | one per COMPLETED booking |
| users | 50,000 | every 10th is a host |
| properties | 20,000 | |

Total about 330 MB, built in ~28 seconds by `lab/setup.sh`.

Two things about it are load-bearing and were each got wrong once:

- **`bookings` carries an `EXCLUDE USING gist` constraint** on `(property_id, daterange(check_in,
  check_out))` for blocking statuses. Generated stays march on an 18-day stride with a 6-night
  maximum, so they cannot overlap *by construction*. Lengthen a stay past the stride and the whole
  insert fails on the constraint.
- **"Today" in the lab is `LAB_TODAY = 2024-10-01`**, and booking status is derived from the dates
  against it. The first version keyed status off the loop counter instead and produced 400,000
  bookings of which **zero were CONFIRMED** — the branch was unreachable. The second put LAB_TODAY
  at the end of the date span, which made 95% of the table COMPLETED. LAB_TODAY now sits mid-span:
  200,612 COMPLETED / 152,854 CONFIRMED / 25,482 PENDING / 21,052 CANCELLED.

`setseed(0.42)` runs first, so a plan quoted in a post is reproducible on another machine.

---

## The track — 18 posts

Topics come from the PostgreSQL 16 manual, cross-checked against the w3schools tutorial for what a
beginner meets first, then filtered to *what you need to ship*.

| # | slug | state |
|---|---|---|
| 1 | `postgres-introduction` | **rewrite (frozen)** |
| 2 | `postgres-installation` | **rewrite (frozen)** |
| 3 | `postgres-psql-and-tooling` | new |
| 4 | `postgres-databases-schemas-and-roles` | new |
| 5 | `postgres-data-types` | new |
| 6 | `postgres-tables-and-constraints` | new |
| 7 | `postgres-select-and-filtering` | new |
| 8 | `postgres-joins` | new |
| 9 | `postgres-aggregation-and-grouping` | new |
| 10 | `postgres-subqueries-and-ctes` | new |
| 11 | `postgres-window-functions` | new |
| 12 | `postgres-insert-update-delete` | new |
| 13 | `postgres-json-and-jsonb` | new |
| 14 | `postgres-indexes` | new |
| 15 | `postgres-explain-and-query-performance` | new |
| 16 | `postgres-transactions-and-locking` | new |
| 17 | `postgres-schema-migrations` | new |
| 18 | `postgres-in-production` | new |

**Full-text search is deliberately not in the track.** It is the one big manual chapter that got
cut. The site already has an `/elasticsearch` category, StayHub itself searches through
Elasticsearch rather than `tsvector`, and nothing in "get a project released to production" needs
it. Say the word and it becomes post 19.

---

## Incident — 2026-08-22: check_sql.py dropped the demo application's database

Recorded in full because the fix is a rule, not a patch.

**What happened.** Post 4 illustrates the namespace hierarchy with `CREATE DATABASE stayhub;`.
`check_sql.py` classified that as a statement it had to run outside a transaction, ran it against a
scratch database, and then — "cleaning up after itself" — issued
`DROP DATABASE IF EXISTS stayhub WITH (FORCE)` for every database name it had seen in a
`CREATE DATABASE`. The demo application's own database was dropped.

**Recovery.** Fully restored in about four minutes, and everything needed was already checked in:

1. `CREATE DATABASE stayhub OWNER stayhub`, then `lab/stayhub-schema.sql` for the schema
2. `INSERT INTO alembic_version VALUES ('35c27e31465b')` — the migration head it was on
3. `stayhub-fastapi-backend/.venv/bin/python -m scripts.seed` — the app's own idempotent fixture
4. `docker restart stayhub-hasura` to rebuild `hdb_catalog`, then `hasura/scripts/apply.py` to
   reapply the tracked tables and permissions
5. Verified: 193 tests pass, Hasura reports 8 tables tracked and metadata consistent

**Not recovered.** The database held **3 bookings and 1 payment**; `scripts/seed.py` creates
**2 bookings and 0 payments**. The extra booking and its payment were made through the running
application after the last seed, and nothing on disk describes them. Re-running `scripts.seed`
restores the canonical fixture, not that state. If either mattered, they need remaking through the
app.

**The fix.** `CLUSTER_LEVEL` in `check_sql.py`. `CREATE DATABASE`, `DROP DATABASE`, `ALTER SYSTEM`
and tablespace DDL are now classified as **never executed** — they change the server rather than a
database and no transaction can undo them. `DROP DATABASE` is issued from exactly one function,
`drop_scratch()`, which asserts on its own constant before running. A post can now contain any
statement at all without the checker acting on it.

`CREATE ROLE` was deliberately left executable: role DDL *is* transactional, so post 4's whole
subject stays verified rather than waved through.

**The general rule, for the next script in this repo that wants to be tidy:** a checker may create
what it names and drop only what it created. Deriving the name of something to delete from the
content being checked is how content becomes an instruction.

---

## Incident — 2026-08-23: a post's own COMMIT escaped the checker's wrapper

Smaller than the first one — it dirtied `stayhub_lab`, which is a fixture this project builds, not
the demo application — but it is the same shape and worth writing down.

Post 12 ends by demonstrating the habit that saves you from a mistyped `WHERE`:

```sql
BEGIN;
UPDATE bookings SET status = 'CANCELLED' WHERE property_id = 42;
COMMIT;
```

`check_sql.py` runs every block as `BEGIN; <replayed context> <block> ROLLBACK;`. That `COMMIT`
ended **the wrapper's** transaction, so everything the replayed context had inserted became
permanent and the trailing `ROLLBACK` had nothing left to undo. Four amenities and fourteen booking
status changes were written into `stayhub_lab`, and the next run failed on a duplicate key —
blaming a block that was correct.

**Fixed** by classifying any block containing `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT` or
`START TRANSACTION` as `no-transaction`, which routes it to the scratch database — thrown away
whole afterwards — with no cumulative context. Verified: a full `check_sql.py` run over all twelve
posts now leaves the booking status counts and the empty `amenities` table exactly as
`lab/setup.sh` built them.

`lab/setup.sh` was re-run to rebuild the lab from scratch, so every figure quoted in the posts is
against clean deterministic data.

---

## Log

- **2026-08-22** — Audited `/postgre`, read the two existing posts, confirmed the two slugs are
  frozen and the 2020 dates need `--force-dates`. Confirmed nav needs no change. Identified StayHub
  as the candidate example app.
- **2026-08-22** — Decisions taken: 18 posts, 6–10 reading-minutes, StayHub's real schema.
- **2026-08-22** — Built `lab/` (`dump-schema.sh`, `seed.sql`, `setup.sh`) after two wrong cuts at
  the booking status distribution. `stayhub_lab` now holds 400,000 bookings across four statuses.
- **2026-08-22** — Wrote `manifest.py` (18 posts, dates 2026-10-26 → 2026-12-16, three days apart,
  starting after the FastAPI track's last post), ported `seed.py`, wrote `check_content.py` and
  `check_sql.py`.
- **2026-08-22** — `check_sql.py` dropped the `stayhub` database; restored, and the checker
  rewritten so it cannot. See the incident above.
- **2026-08-22** — Two adjustments to `check_content.py` that came out of using it: the reading-time
  budget is tested on `readingMinutes` (which is rounded, and is what the reader sees) rather than
  on `TARGET_MINUTES * 220`, and the "quoted figure" rule only fires on a number in the same
  sentence as a lab table name, so ordinary arithmetic in prose is not reported as an invention.
- **2026-08-22** — Posts 1–4 written and passing: introduction, installation, psql, roles.
- **2026-08-23** — Posts 5–9 written and passing: data types, tables and constraints, SELECT,
  joins, aggregation. All nine sit at 6 reading-minutes with prose between 67% and 90%.
- **2026-08-23** — `check_sql.py` grew three capabilities, each because it let something through:
  **cumulative replay** (a post that creates a role in one block and grants to it in the next was
  being reported as broken), a **fragment** kind for column definitions quoted to show syntax, and
  **quoted-output verification**. See below.

### check_sql.py now verifies the output too

The check that mattered most. A `plaintext` block following a `sql` block is re-derived: the query
runs and every row quoted in the post must appear in the real result.

It caught fabrication on its first run. The aggregation post quoted average-nights of
`3.50 / 3.50 / 3.51 / 3.50`; the database returns `3.49 / 3.52 / 3.52 / 3.50`. The SQL was correct
and ran cleanly — the numbers beneath it had been written from memory. **Nothing else in this
pipeline would ever have caught that**, and it is the single most likely thing to be wrong in a
SQL tutorial.

Three bugs were found while building it, all of the same family — a check that silently compares
nothing:

- `\o /dev/null` around the replayed context blocks. Without it, context SELECTs printed their own
  rows into the comparison and a quoted row could match output from a different query.
- The `(4 rows)` footer filter dropped every line starting with `(` — which is also how a `ctid`
  is written, so the MVCC example was compared against an empty list and passed.
- `NON_REPRODUCIBLE` needs two alternations: `\bnow\(\)\b` matches nothing, because `\b` cannot
  match between `)` and `:`. With the single-alternation version every timestamp example was
  compared and failed.

Queries mentioning `now()`, `random()`, a uuid, `xmin` or `ctid` are reported as `output-varies`
and not compared — a check that always fails is a check everybody learns to ignore.


---

## Final state — 2026-08-23

All 18 posts written, checked and seeded to `lovemesomecoding/local/`.

| | |
|---|---|
| Posts | 18, every one at **6 reading-minutes** |
| Words | 22,437 total — 17,171 prose, 5,266 code (**77% prose**, floor is 40%) |
| Code blocks | 195 |
| SQL blocks executed | **157**, all against `stayhub_lab` |
| Quoted result tables re-derived | 5 |
| Build | `708/708 posts served, 42/42 categories, index cross-check agrees, all indexed URLs accounted for` |

Compare with what `/postgre` held before: two posts, 288 words, no headings, 2 reading-minutes.

### Verified

- `check_content.py` — all 18 pass, no warnings
- `check_sql.py` — 157 SQL blocks run; 128 plain, 8 no-transaction, 4 fragment, 3 multi-session,
  3 cluster-level, 2 unavailable, 1 expect-error, 1 recovers, 5 outputs re-derived, 2 output-varies
- `seed.py --env local --write --force-dates` — 692 → 708 posts, archive holds 18, category count 18
- `npm run build` with `CONTENT_ENV=local` — passes every `verify-build.mjs` guard
- Both frozen URLs present in `out/`; syntax highlighting confirmed (73 Prism token spans on one page)
- `stayhub` and `stayhub_lab` both verified byte-identical to their seeded state after the full run

### Dates

Folau asked for 2018–2020 rather than the 2026 slot the other tracks use. The eighteen lessons run
**2018-03-06 → 2020-08-06**, one every 52 days.

⚠️ **This moves the two frozen posts backwards**, from their stored 2020-02-19 to 2018-03-06 and
2018-04-27, which is why `--force-dates` is required.

### ⚠️ Open question: the dates and the content disagree

The posts are written against **Postgres 16** and cite features by version. Several of those
versions did not exist by 2020:

| Post | Reference | Released |
|---|---|---|
| 1, 2 | `16.15` as the version everything was run on | 2023 (16.0) |
| 4 | "Since Postgres 15 a new database is less permissive" | 2022 |
| 6 | "Postgres 15 added `UNIQUE NULLS NOT DISTINCT`" | 2022 |
| 10 | "Postgres 14 added `CYCLE`" | 2021 |
| 17 | "since Postgres 11 the default is stored once" | 2018 — fine |
| 10, 13, 17 | Postgres 12 behaviour (CTE inlining, generated columns, `SET NOT NULL` proof) | 2019 — fine for the later posts, not for one dated 2018 |

Nothing is *wrong* as Postgres; it is wrong as of the post's date. One outright contradiction was
removed ("differences that are still true in 2026" → "that have held for years"). The rest are the
version references above.

Three ways out, and it is Folau's call:

1. **Leave it.** The dates are metadata, nobody diffs a tutorial against its publication year, and
   the content is correct today. Zero work.
2. **Move the dates later** — one line in `manifest.py` (`START_DATE`, `STEP_DAYS`) and a re-seed
   with `--force-dates`. Ten minutes.
3. **Rewrite to a 2018-era Postgres (10/11).** Not recommended: the lab runs 16, so every plan,
   every output and every version claim would have to be re-derived on a different server, and the
   track would teach an unsupported version.

### To publish

```bash
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python \
    projects/postgres_tutorial/seed.py --env prod --write --force-dates
cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy
```

⚠️ `--force-dates` is needed on the first prod seed **and on every later seed that changes a
date**. A published date is sticky — `upsert_post` never overwrites one — so a re-base of
`START_DATE` followed by a plain re-run moves nothing at all.

### Left undone

- Not seeded or published to **prod**. Deliberate — that is an outward-facing publish.
- The **`postgre` slug stays wrong**. It should be `postgres`, it has been wrong since 2020, and
  it is an indexed URL. Renaming it means 18 redirects in `postbuild.mjs` plus a CloudFront
  Function republish. Not attempted.
- **Full-text search** is still out of the track. See the note above the track table.


---

## Two corrections adopted from the FastAPI track — 2026-08-23

`seed.py` here was ported from `projects/fastapi_tutorial/seed.py` before commit `d38048a`, so it
carried two bugs that commit had already found and fixed. Both were ported across after reading it.

**`--force-dates` is not "exactly once per tree".** The docstring said it was. It is wrong for the
same reason in both tracks: `upsert_post` never overwrites an existing date, so a published post's
date is sticky forever. The first seed is only the first instance — every re-base of `START_DATE`
is the same problem, and after the first seed it applies to all eighteen posts rather than the two
rewrites. Corrected in the docstring, the `--help` text, the README and above.

**The `new`-slug collision guard failed on the second seed.** It rejected any `new` slug that
already existed, which after one seed is all sixteen of them — because this track created them. It
exists to stop a first seed silently overwriting a stranger's page, which is a real risk since post
slugs are global, so it was not deleted: it now fails only when a `new` slug is found in a
**different category**, and merely notes the ones already in `/postgre`. Verified by running a
second dry-run seed against `local`: 18 updates, no false failure.

Both were caught by reading `git log` rather than by any check, which is the argument for reading
the other tracks' reports before porting their tooling.

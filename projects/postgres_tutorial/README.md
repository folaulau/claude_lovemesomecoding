# Postgres Tutorial

## About
- this tutorial is for the Postgres database

## Requirements
- create or update posts on https://lovemesomecoding.com/postgre collection.
- keep posts to the point.
- Use https://www.postgresql.org/docs/current/index.html and https://www.w3schools.com/postgresql/index.php to generate the main topics to create posts. We don't need to create a post for every single small thing. We need just the important things to get a project developed and released to production.

---

## What is here

```
projects/postgres_tutorial/
  manifest.py          category metadata + one entry per post (slug, title, date, tags, excerpt)
  posts/NN-slug.html   the post bodies, plain semantic HTML
  lab/                 builds `stayhub_lab` — StayHub's real schema at 400,000 bookings
  check_content.py     the HTML round-trips, and this track's own length/prose rules
  check_sql.py         EXECUTES every SQL sample, and re-derives every quoted result
  seed.py              writes the category and posts into a content tree
  progress_report.md   status, decisions, and two incidents worth not repeating
```

## The track

18 posts at `/postgre/{slug}`, 6 reading-minutes each, dated 2018-03-06 → 2020-08-06.

| # | Slug | State |
|---|------|-------|
| 1 | `postgres-introduction` | **rewrite — live URL** |
| 2 | `postgres-installation` | **rewrite — live URL** |
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

⚠️ **Posts 1 and 2 are live, indexed URLs** published 2020-02-19. They are rewritten in place.
Changing either slug is a dead link, and `verify-build.mjs` fails the frontend build for it.

Both are stored with 2020-02-19 and `upsert_post` never overwrites a date, so seeding needs
`--force-dates` or they land in the middle of the track instead of at its head.

⚠️ **`--force-dates` is not a one-off.** A published post's date is sticky forever, so after the
first seed *every* post has one and a plain re-run moves none of them. Pass it on the first seed
**and after any change to `START_DATE`**. (This is the correction the FastAPI track's 2025 re-base
established — its docstring had promised the opposite.)

## The lab database

Every SQL sample runs against `stayhub_lab`: StayHub's real schema (`pg_dump --schema-only`) filled
to 400,000 bookings, 374,518 payments, 200,612 reviews, 50,000 users, 20,000 properties. StayHub's
own database has 12 properties and 3 bookings — at that size the planner seq-scans everything and
an "add an index" lesson would show an index nothing ever chooses.

```bash
cd lovemesomecoding_demo_project/stayhub && docker compose up -d postgres   # if not running
projects/postgres_tutorial/lab/setup.sh          # build, ~30s
projects/postgres_tutorial/lab/setup.sh --drop   # tear down
projects/postgres_tutorial/lab/dump-schema.sh    # re-take the schema after a StayHub migration
```

`stayhub_lab` is separate from `stayhub`. Nothing here writes to the demo application's database.

## Commands

Run from the repo root. `check_content.py` needs no AWS credentials or container; `check_sql.py`
needs the container; `seed.py` needs AWS.

```bash
# the HTML round-trips, and the track's length/prose rules hold
lovemesomecoding_backend/.venv/bin/python projects/postgres_tutorial/check_content.py

# every SQL sample runs, and every quoted result is re-derived. Takes a few minutes.
projects/postgres_tutorial/check_sql.py
projects/postgres_tutorial/check_sql.py --post postgres-joins --verbose

# dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/postgres_tutorial/seed.py --env local

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/postgres_tutorial/seed.py --env local --write --force-dates
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/postgres_tutorial/seed.py --env prod  --write --force-dates
```

`seed.py` is idempotent. Leave `--force-dates` off when only a post body changed; pass it whenever
a date in the manifest has to move.

## What check_sql.py actually does

More than "does it parse". Blocks are replayed **in order, cumulatively** — block 5 runs with
blocks 1-4 already applied — inside a transaction that is rolled back, so a post that creates a
role in one block and grants to it in the next is checked the way a reader meets it.

A `plaintext` block following a `sql` block is treated as that query's output and **re-derived**.
This caught fabricated numbers on its first run: an aggregation post quoted average-nights of
3.50/3.50/3.51/3.50 where the database returns 3.49/3.52/3.52/3.50. The SQL was correct and ran
cleanly. Nothing else in the pipeline would have noticed.

Blocks are classified automatically so a post cannot quietly opt out:

| kind | handling |
|---|---|
| `sql` | run in a rolled-back transaction with cumulative context |
| `expect-error` | contains a `-- ERROR:` line, so it must FAIL; running clean is the finding |
| `no-transaction` | `CREATE INDEX CONCURRENTLY`, `VACUUM`, or a block with its own `BEGIN/COMMIT` — gets a fresh scratch database with the context applied |
| `recovers` | rolls back to a savepoint, so it is run with `ON_ERROR_STOP` off |
| `cluster-level` | `CREATE DATABASE`, `ALTER SYSTEM` — **never executed**, see progress_report.md |
| `fragment` | does not start with a statement keyword: a column definition quoted to show syntax |
| `multi-session` | half of a two-session locking demo; reported, not run |
| `unavailable` | needs something this container lacks, declared with a reason |
| `output-varies` | the query mentions `now()`, `random()`, `xmin`… so its output is not compared |

## Editing a post later

```bash
lovemesomecoding_backend/.venv/bin/python projects/postgres_tutorial/check_content.py
projects/postgres_tutorial/check_sql.py --post <slug>
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/postgres_tutorial/seed.py --env prod --write
cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy
```

Editing through `/admin` works too, but the TipTap editor will not round-trip the raw HTML in these
files, so the file here would then be stale. Pick one source of truth per post.

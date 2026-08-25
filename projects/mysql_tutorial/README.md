# MySQL Tutorial

## About
- this tutorial is for the MySQL tutorial

## Requirements
- create or update posts on https://lovemesomecoding.com/sql collection
- keep posts to the point.
- update all posts in the tutorial.
- update posts and keep content to the point and not too lengthy if they don't have to.
- use https://www.w3schools.com/mysql/default.asp and https://www.mysqltutorial.org/ to generate the main topics and posts for this tutorial. We don't need to create a post for each small thing.
- Use this project /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend to provide examples for this tutorial.
---

## Layout

```
projects/mysql_tutorial/
  manifest.py          category metadata + one entry per post (slug, title, date, tags, excerpt)
  posts/NN-slug.html   the post bodies, plain semantic HTML
  lab/build.sql        builds `pizza_lab` — the pizza schema at 400,000 orders
  lab/setup.sh         run/verify/drop the lab
  check_content.py     the HTML round-trips, plus this track's length/prose/no-image rules
  check_sql.py         EXECUTES every SQL sample and re-derives every quoted result
  seed.py              writes the category and posts into a content tree
  progress_report.md   status, decisions, and the bugs worth not repeating — read this first
```

## The track

**52 posts** at `/sql/{slug}`, dated 2024-05-06 → 2025-01-16.

⚠️ **42 of the 52 slugs are live, indexed URLs** published 2018-2021. They are rewritten in
place. Changing one is a dead link and `verify-build.mjs` fails the frontend build for it.
`manifest.FROZEN_SLUGS` holds all 42 and `check_content.py` asserts they are all still there.

The other 10 are new: introduction, install, data types, CREATE TABLE, normalization, UNION,
CTEs, window functions, users/privileges, replication.

⚠️ **`seed.py` needs `--force-dates`, and it is not a one-off.** Every one of the 52 posts
already exists with a date, so a plain re-run moves none of them and the archive keeps reading in
2018-2021 historical order instead of lesson order.

## No images

The rewritten posts contain **no `<img>` and no `<figure>`**, enforced by `check_content.py`.
The 99 images in the live posts are almost all screenshots of query output; those become real
`plaintext` blocks that `check_sql.py` re-derives. A screenshot cannot be verified.

## Prerequisites

```bash
# the demo database (required for check_sql.py)
cd lovemesomecoding_demo_project/pizza/pizza-springboot-backend && docker compose up -d

# the lab database, for the posts in manifest.LAB_POSTS
projects/mysql_tutorial/lab/setup.sh           # build, ~50s
projects/mysql_tutorial/lab/setup.sh --check   # verify an existing build
projects/mysql_tutorial/lab/setup.sh --drop    # tear down
```

MySQL is on **127.0.0.1:3308**, not 3306 — the demo publishes a non-default host port on purpose.

## Commands

Run from the repo root. `check_content.py` needs no database and no AWS; `check_sql.py` needs the
container; `seed.py` needs AWS.

```bash
# the HTML round-trips, and the track's length / prose / no-image rules hold
lovemesomecoding_backend/.venv/bin/python projects/mysql_tutorial/check_content.py

# every SQL sample runs, and every quoted result is re-derived
projects/mysql_tutorial/check_sql.py
projects/mysql_tutorial/check_sql.py --post sql-select --verbose
projects/mysql_tutorial/check_sql.py --list        # classify blocks, run nothing

# compare the manifest against what is actually in a tree — writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/mysql_tutorial/seed.py \
    --env prod --check-live

# dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/mysql_tutorial/seed.py --env local

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/mysql_tutorial/seed.py \
    --env local --write --force-dates
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/mysql_tutorial/seed.py \
    --env prod  --write --force-dates
```

`seed.py` is idempotent. Use `--only slug1,slug2` to seed a subset while the rest of the track is
still unwritten.

## Adding or updating a post

1. Edit or add the HTML in `posts/`, and its entry in `manifest.py`.
2. To insert mid-track, add it to `_TRACK` in reading position — dates and `NN-` filenames are
   derived from that order, so nothing else needs renumbering.
3. Run `check_sql.py --post <slug>` — **paste output from the checker, never by hand.** The
   mysql client right-aligns numeric columns; transcribing a result set by eye gets that wrong,
   and that is exactly what the first run of this checker caught.
4. `check_content.py`, then seed `--env local --write --force-dates`, then review at `:3000`.
5. Seed `--env prod --write --force-dates`, then
   `cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy`.

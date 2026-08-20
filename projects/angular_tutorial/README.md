# Angular Tutorial

## About
- this tutorial is for the Angular frontend framework.

## Requirements
- update posts on https://lovemesomecoding.com/angular collection.
- keep posts to the point.
- Use https://angular.dev and https://www.w3schools.com/angular/ to generate the main topics to create posts. We don't need to create a post for every single small thing. We need just the important things to get a project developed and released to production.
- let's use this project /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-angular-frontend for examples. If examples are not found there, add them and make sure they don't break the app.
---

## Layout

```
projects/angular_tutorial/
  manifest.py        category metadata + one entry per post (slug, title, date, tags, excerpt)
  posts/NN-slug.html the post bodies, plain semantic HTML   <- EMPTY, see below
  seed.py            writes the category and posts into a content tree
  check_content.py   proves the normaliser round-trips every code sample (no AWS needed)
  progress_report.md status, decisions and the full topic table — read this first
```

## Status: scaffolded, bodies blocked

The 29-post topic table, the manifest and the tooling are done. **No post body is written**, because
every snippet must come from `lovemesomecoding_demo_project/pizza/pizza-angular-frontend` and that
directory is still empty (Phase 7 of the pizza demo). `check_content.py` validates the manifest
today; `seed.py` refuses to run until every file exists.

`progress_report.md` holds the topic table and the decisions.

## Commands

Run from the repo root. `check_content.py` needs no AWS credentials; `seed.py` does.

```bash
# Verify the manifest and any written content
lovemesomecoding_backend/.venv/bin/python projects/angular_tutorial/check_content.py

# Dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/angular_tutorial/seed.py --env local

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/angular_tutorial/seed.py --env local --write
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/angular_tutorial/seed.py --env prod  --write
```

`seed.py` is idempotent — a re-run updates the posts in place.

### `--force-dates`

`upsert_post` never overwrites an existing post's `date`. `angular-component` was published
2019-07-31, so without this flag it keeps that timestamp and sorts to the back of the track.
**Needed exactly once, on the first prod publish** — every run without it leaves the archive alone,
which is what you want the rest of the time.

### Re-dating the track

Dates are computed, not hard-coded. Edit `START_DATE` (and `STEP_DAYS`) in `manifest.py` and the
whole track re-bases in order.

## Adding or updating a post

1. Edit or add the HTML in `posts/`. Add or update its entry in `manifest.py`.
2. To insert mid-track, add it to `_TRACK` in reading position — dates and `NN-` filenames are
   derived from that order, so nothing else needs renumbering.
3. If it is a **new** post, add it to the lesson index in `posts/01-angular-get-started.html`.
4. `check_content.py`, then seed `--env local --write`, then review at `:3000`.
5. Seed `--env prod --write`, then `cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy`.

## Frozen slugs

`angular-component` was published in 2019 and its URL is indexed. It is rewritten in place — that
slug must never change. `check_content.py` fails if it leaves the manifest.

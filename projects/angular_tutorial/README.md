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
  check_snippets.py  proves every quoted snippet still matches the demo app (no AWS needed)
  progress_report.md status, decisions and the full topic table — read this first
```

## Status: ready to author

The 28-post topic table, the manifest and the tooling are done, and the demo app is built. Every
snippet comes from `lovemesomecoding_demo_project/pizza/pizza-angular-frontend` (Angular 21.2,
TypeScript 5.9, Bootstrap 5 + Sass, NgRx 21, standalone and zoneless).

**All 28 post bodies written**, seeded to the local tree and verified rendering.

⚠️ **Only lessons 4 and 5 are on prod.** The other 26 exist locally and have not been reviewed.
Publishing them is `seed.py --env prod --write` plus a frontend deploy.

Lesson 1's lesson index is **generated from `manifest.POSTS`**, so adding or reordering a lesson
means re-running the generator rather than hand-editing a list that will drift.

Four examples the track needed were added to the app and are covered by new unit tests: an
`Autofocus` directive, a debounced menu search, a `CanDeactivate` guard on checkout, and a Vitest
suite. One lesson (SSR) was cut rather than risk `ng add @angular/ssr` on a working app.

`progress_report.md` holds the topic table, the decisions and the full audit.

## Commands

Run from the repo root. `check_content.py` needs no AWS credentials; `seed.py` does.

```bash
# Verify the manifest and any written content
lovemesomecoding_backend/.venv/bin/python projects/angular_tutorial/check_content.py

# Verify every quoted snippet still matches the demo app. Run BOTH — they check
# different things, and only this one goes stale on its own.
python3 projects/angular_tutorial/check_snippets.py

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

### `--only`

`seed.py` normally refuses to run while any post file is missing, which is right for publishing and
useless for drafting. `--only` seeds a subset so a post can be previewed at `:3000` while the rest
of the track is still unwritten:

```bash
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/angular_tutorial/seed.py \
  --env local --only angular-component --write
```

It does not make the track publishable — a full `--env prod` run still needs all 28 files.

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

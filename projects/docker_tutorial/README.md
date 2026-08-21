# Docker Tutorial

## About
- this tutorial is for the Docker tutorial

## Requirements
- update posts on https://lovemesomecoding.com/docker collection.
- keep posts to the point.
- Use https://docs.docker.com to generate the main topics to create posts. We don't need to create a post for every single small thing. We need just the important things to get a project developed and released to production.
- every example comes from `lovemesomecoding_demo_project/pizza`. The Docker artifacts did not exist
  when this track started; they were added by it, and they are built and run before being quoted.

---

## Layout

```
projects/docker_tutorial/
  manifest.py          category metadata + one entry per post (slug, title, date, tags, excerpt)
  posts/NN-slug.html   the post bodies, plain semantic HTML
  seed.py              writes the category and posts into a content tree
  check_content.py     proves the normaliser round-trips every code sample (no AWS needed)
  check_snippets.py    proves every quoted snippet still matches the demo app (no AWS needed)
  verify_stack.mjs     drives a browser at the containerised demo app
  verify_rendered.mjs  drives a browser at the built site
  progress_report.md   status, decisions and the full topic table — read this first
```

## Status: LIVE

All 22 posts are published at https://lovemesomecoding.com/docker (2026-08-21, build `394b0bd`).

⚠️ **`--force-dates` has already been used**, to move `docker-what-is-docker` off its 2020 date.
Never pass it again — every later run must leave the archive's dates alone. A correction is
`seed.py --env prod --write` followed by `npm run deploy`.

Lesson 1's lesson index is checked against `manifest.POSTS` by `check_content.py`, so a lesson
added to the manifest and not linked from the index fails the check rather than becoming
unreachable.

## What this track added to the demo app

`lovemesomecoding_demo_project/pizza` had no Dockerfile anywhere. It now has three images, two
nginx configs, a full-stack compose file and a CI workflow — all built, run and exercised in a
browser before being quoted. See `progress_report.md` for the list and the measurements.

⚠️ **`pizza/compose.yaml` is not `pizza-springboot-backend/docker-compose.yml`.** The latter is the
daily development loop (backing services only, app on the host). The new one runs everything in
containers and is what this track is written against. Its host ports are deliberately shifted off
the development ones so both can run at once.

## Commands

Run from the repo root. The two `check_*` scripts need no AWS credentials; `seed.py` does.

```bash
# Verify the manifest and every written post
lovemesomecoding_backend/.venv/bin/python projects/docker_tutorial/check_content.py

# Verify every quoted snippet still matches the demo app. Run BOTH — they check
# different things, and only this one goes stale on its own.
python3 projects/docker_tutorial/check_snippets.py

# Dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/docker_tutorial/seed.py --env local

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/docker_tutorial/seed.py --env local --write
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/docker_tutorial/seed.py --env prod  --write
```

`seed.py` is idempotent — a re-run updates the posts in place.

### Reviewing the rendered track

```bash
cd lovemesomecoding_frontend
CONTENT_ENV=local AWS_PROFILE=folau ./scripts/sync-content.sh
AWS_PROFILE=folau npm run build && npm run preview      # :4321

# in another terminal
node projects/docker_tutorial/verify_rendered.mjs
```

`verify_rendered.mjs` checks all 22 pages for a 200, code blocks that are actually
**highlighted** rather than plaintext, table-of-contents anchors that resolve, and a track index in
lesson 1 that links every lesson. `verify-build.mjs` already proves the URLs resolve; this proves a
reader sees what they should.

### Verifying the demo app's containers

```bash
cd lovemesomecoding_demo_project/pizza
docker compose --profile angular up -d --build

node ../../projects/docker_tutorial/verify_stack.mjs

docker compose --profile angular down       # `down -v` also wipes the database
```

`verify_stack.mjs` drives headless Chromium at both containerised frontends: a deep link must
return the app rather than a 404, product cards must render, and every `/api/` request must go to
the SPA's own origin — which is what proves the nginx proxy is carrying the traffic rather than an
absolute URL having been baked into the bundle.

### `--force-dates`

`upsert_post` never overwrites an existing post's `date`. `docker-what-is-docker` was published
2020-10-11, so without this flag it keeps that timestamp and sorts to the back of the track.

⚠️ **Already used, on the 2026-08-21 prod publish. Do not pass it again.** Its one job is done —
that post now carries 2026-06-15 and reads first. Every later run must leave the archive's dates
alone, which is what happens by default.

### `--only`

`seed.py` normally refuses to run while any post file is missing. `--only` seeds a subset so one
post can be previewed while others are being edited:

```bash
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/docker_tutorial/seed.py \
  --env local --only docker-compose --write
```

### Re-dating the track

Dates are computed, not hard-coded. Edit `START_DATE` (and `STEP_DAYS`) in `manifest.py` and the
whole track re-bases in order.

## Adding or updating a post

1. Edit or add the HTML in `posts/`. Add or update its entry in `manifest.py`.
2. To insert mid-track, add it to `_TRACK` in reading position — dates and `NN-` filenames are
   derived from that order, so nothing else needs renumbering.
3. If it is a **new** post, add it to the lesson index in `posts/01-docker-what-is-docker.html`.
   `check_content.py` fails if you forget.
4. `check_content.py` and `check_snippets.py`, then seed `--env local --write`, then review
   at `:4321`.
5. Seed `--env prod --write`, then `cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy`.

### Quoting the demo app

`check_snippets.py` searches for each code block, contiguously, in `pizza/`. To quote a file with
the middle left out, put a line that is exactly `...` where you cut — each chunk is then verified
separately. A block that matches nothing is reported as `illustrative` and does not fail; a block
whose **opening lines** match but whose body does not is reported as drift and fails, because that
is what a quote of a file that has since changed looks like.

## Frozen slugs

`docker-what-is-docker` was published 2020-10-11 and its URL is indexed. It is rewritten in
place — that slug must never change. `check_content.py` fails if it leaves the manifest.

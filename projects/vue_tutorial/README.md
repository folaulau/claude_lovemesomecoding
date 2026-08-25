# Vue Tutorial

## About
- this tutorial is for the Vue 3 frontend framework.

## Requirements
- publish a new **`/vue`** collection on lovemesomecoding.com. It does not exist yet — every slug
  is new.
- keep posts to the point.
- Use https://vuejs.org and https://www.w3schools.com/vue/ to generate the main topics. We don't
  need a post for every small thing — just what it takes to get a project developed and released to
  production.
- Use `lovemesomecoding_demo_project/reelcms/reelcms-vue-frontend` for examples. If an example is
  not there, add it to the app and make sure it doesn't break anything.
- **Composition API only.** One lesson covers the Options API so legacy code is readable; the rest
  of the track uses `<script setup>`.

---

## Layout

```
projects/vue_tutorial/
  manifest.py        category metadata + one entry per post (slug, title, part, date, tags, excerpt)
  authoring.py       code() / from_app() helpers — NEVER hand-escape a code block
  posts/NN-slug.html the post bodies, plain semantic HTML
  seed.py            writes the category and posts into a content tree
  check_content.py   proves the normaliser round-trips every code sample (no AWS needed)
  check_snippets.py  proves every quoted snippet still matches the demo app (no AWS needed)
  gen_index.py       regenerates lesson 1's lesson index from the manifest
  progress_report.md status, decisions and the full topic table — read this first
```

## Status: ✅ published

All 28 posts are **live at https://lovemesomecoding.com/vue**. The content pipeline was extended to
support Vue and verified end to end, the backend Lambda and the frontend are both deployed, and every
one of the 28 URLs returns 200 and appears in the sitemap.

Two gaps in the demo app were closed to serve the track — composables (`useIntersectionObserver`,
`useDebounced`) and a `<Teleport>`'d confirm modal — and both are improvements to the app on their own
terms. A Vitest unit suite, a custom directive and named slots were deliberately **not** added; the
lessons that would have used them say so plainly and use generic examples instead.
`progress_report.md` holds the gap table, the decision and the full publish log.

Lesson 1's lesson index is **generated from `manifest.POSTS`**, so adding or reordering a lesson
means re-running `gen_index.py` rather than hand-editing a list that will drift.
`check_content.py` fails if it is stale.

## Versions the track is written against

Stated on lesson 1 and assumed throughout. **Read off the demo app, not chosen.** When the app
moves, that table is the first edit.

| | |
|---|---|
| vue | **3.5.41** |
| vite / @vitejs/plugin-vue | 8.2.2 / 6.0.8 |
| vue-router | 4.6.4 |
| pinia | 4.0.3 |
| bootstrap | 5.3.8 |
| chart.js / vue-chartjs | 4.5.1 / 5.3.4 |
| Node.js | 22 |

⚠️ **This track is plain JavaScript, not TypeScript** — unlike `/react` (TSX) and `/angular`. The
demo app is JavaScript and snippets are copied verbatim so they can be checked automatically.
Lesson 1 says so outright.

## Commands

Run from the repo root. `check_content.py` and `check_snippets.py` need no AWS credentials;
`seed.py` does.

```bash
# Verify the manifest and any written content
lovemesomecoding_backend/.venv/bin/python projects/vue_tutorial/check_content.py

# Verify every quoted snippet still matches the demo app. Run BOTH — they check
# different things, and only this one goes stale on its own.
python3 projects/vue_tutorial/check_snippets.py

# Regenerate lesson 1's index after adding, renaming or reordering a lesson
lovemesomecoding_backend/.venv/bin/python projects/vue_tutorial/gen_index.py --write

# Dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/vue_tutorial/seed.py --env local

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/vue_tutorial/seed.py --env local --write
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/vue_tutorial/seed.py --env prod  --write
```

`seed.py` is idempotent — a re-run updates the posts in place.

### `--only`

`seed.py` normally refuses to run while any post file is missing, which is right for publishing and
useless for drafting. `--only` seeds a subset so a post can be previewed at `:3000` while the rest
of the track is still unwritten:

```bash
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/vue_tutorial/seed.py \
  --env local --only vue-sfc --write
```

It does not make the track publishable — a full `--env prod` run still needs all 28 files.

### `--force-dates`

Not needed for a *first* publish — `upsert_post` applies the manifest date when it creates a post,
and only refuses to overwrite one that already exists. It **is** needed to re-date a track that is
already published, which is what happened here on 2026-08-24 when the whole track was re-based out of
2026 and into 2025.

### Re-dating the track

Dates are computed, not hard-coded. Edit `START_DATE` (and `STEP_DAYS`) in `manifest.py`, then seed
with `--force-dates`, then redeploy the frontend.

⚠️ **Post dates must fall between 2023 and 2025, and never in the future.** `check_content.py`
enforces both. The track currently runs **2025-10-09 .. 2025-12-29**.

## Adding or updating a post

1. Edit or add the HTML in `posts/`. Add or update its entry in `manifest.py`.
2. To insert mid-track, add it to `_TRACK` in reading position — dates and `NN-` filenames are
   derived from that order, so nothing else needs renumbering.
3. Re-run `gen_index.py --write` so lesson 1's index matches.
4. `check_content.py` **and** `check_snippets.py`, then seed `--env local --write`, review at `:3000`.
5. Seed `--env prod --write`, then `cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy`.

## Gotchas paid for already

- **Prism ships no `vue` grammar**, and it does not need one — `prism-markup` highlights a
  `<script>` block as JavaScript and a `<style>` block as CSS, which is exactly an SFC. Two changes
  in lockstep make `language-vue` work:
  `"vue"` in `SUPPORTED_LANGUAGES` (`lovemesomecoding_backend/app/services/content.py`) and
  `Prism.languages.vue = Prism.languages.markup` (`lovemesomecoding_frontend/src/lib/content.ts`).
  `check_content.py` asserts the backend half directly, so trimming that list fails a check instead
  of turning 28 posts grey.
- ✅ **The backend Lambda was deployed with the new language list on 2026-08-24**, so editing a Vue
  post through `/admin` keeps its highlighting. This is the hazard the React track hit with `tsx`:
  seeding runs the *local* service layer, so S3 is correct either way — but an `/admin` save against
  a Lambda whose `SUPPORTED_LANGUAGES` lacks `vue` normalises every block down to `plaintext` and
  loses the highlighting silently. Redeploy the backend before editing these posts in the admin if
  its code is ever rolled back.
- **Never hand-escape an SFC inside a `<pre>`.** Vue is the worst case this pipeline has faced: a
  snippet contains a literal `<template>`, `<script setup>` and often `<style scoped>`, and one
  missed `&lt;` opens a real element and swallows everything after it. Use `authoring.py` —
  `code()` escapes once, correctly, and `from_app()` reads the file out of the demo app instead of
  retyping it, which is what makes `check_snippets.py` meaningful.
- **A seed can leave a post out of the derived indexes, and nothing else catches it.** On the first
  prod publish, two posts were written correctly but were missing from `index/posts.json` and the
  category indexes. The static build reads *only* the indexes, so those lessons would have been
  silently absent — and `verify-build.mjs` would have passed, because it cross-checks the indexes
  against each other and all of them were missing the same two. Re-running the seed repairs it.
  `seed.py` now verifies every seeded slug landed in both indexes and exits non-zero if not.
- **`scripts/deploy.sh` in the backend needs `API_DOMAIN`, `API_CERT_ARN` and `HOSTED_ZONE_ID`**, or
  it passes an empty `DomainName` and `sam` refuses — which is the only thing preventing
  CloudFormation from tearing down `api.lovemesomecoding.com`. The working invocation is in
  `progress_report.md`.
- **An unsupported language normalises to `plaintext` silently — it is never rejected.** The code is
  all still there, just grey, which is easy to miss in review. `check_content.py` treats an authored
  `language-X` that comes out as `plaintext` as a hard failure.

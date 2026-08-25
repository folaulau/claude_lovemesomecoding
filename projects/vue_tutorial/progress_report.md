# Vue tutorial track — progress report

**Status:** ✅ **PUBLISHED.** All 28 posts live at https://lovemesomecoding.com/vue.
**Started:** 2026-08-24
**Where it lands:** https://lovemesomecoding.com/vue

---

## What this is

`/vue` **does not exist** on the live site. There are 42 categories and none of them is Vue, so
unlike the React and Angular tracks there is no legacy post to rewrite, no indexed URL to preserve
and no `--force-dates` dance on the first publish. Every slug is new and the category is created by
the first seed.

This project builds a **28-post Vue 3 track**, Composition API throughout, every code sample taken
from `lovemesomecoding_demo_project/reelcms/reelcms-vue-frontend`.

## Where it stands

| | |
|---|---|
| Topic table | ✅ 28 lessons |
| `manifest.py` | ✅ every lesson has slug, title, part, tags, excerpt, computed date, source |
| `seed.py` / `check_content.py` / `check_snippets.py` / `gen_index.py` | ✅ all four run clean |
| Content pipeline | ✅ `vue` language support added **and verified end to end** (see below) |
| Site nav | ✅ `vue` added to the JavaScript group in `nav.ts` |
| Demo app | ✅ two gaps closed (composables, Teleport), tests pass |
| Post bodies | ✅ **28 of 28**, 233 code blocks, 82 verified verbatim against the app |
| Internal links | ✅ 72 checked, all resolve |
| Prod | ✅ seeded, frontend deployed, all 28 URLs return 200 and are in the sitemap |

## The demo app

**`reelcms-vue-frontend`, not the pizza app.** The React and Angular tracks both quote
`lovemesomecoding_demo_project/pizza/`, and there is no Vue pizza frontend. ReelCMS is the app that
is actually written in Vue, and it is the better fit anyway: a vertical scroll-snap video feed
exercises lifecycle hooks, template refs and IntersectionObserver far harder than a menu page does.

Versions are **read off the app**, not chosen — a lesson claiming a version its snippet was not
copied from is the kind of drift nobody spots later.

| | |
|---|---|
| vue | 3.5.41 |
| vite / @vitejs/plugin-vue | 8.2.2 / 6.0.8 |
| vue-router | 4.6.4 |
| pinia | 4.0.3 |
| bootstrap | 5.3.8 |
| chart.js / vue-chartjs | 4.5.1 / 5.3.4 |
| node | 22 |

⚠️ **The app is plain JavaScript, not TypeScript.** React is TSX and Angular is TypeScript; this
track is not, because ReelCMS is not, and snippets are copied verbatim so `check_snippets.py` can
prove they are real. Lesson 1 states this outright rather than letting a reader arriving from
`/react` assume otherwise. Where TypeScript changes the answer — props especially — the lesson shows
the typed form without pretending the app uses it.

## The pipeline change — `vue` is a language now

This is the load-bearing technical work, and it is **done and verified**, not assumed.

**Prism ships no `vue` grammar** and it does not need one: `prism-markup` already highlights a
`<script>` block's contents as JavaScript and a `<style>` block's as CSS, which is precisely an
SFC's three sections. Two changes, in lockstep:

| File | Change |
|---|---|
| `lovemesomecoding_backend/app/services/content.py` | `"vue"` added to `SUPPORTED_LANGUAGES` |
| `lovemesomecoding_frontend/src/lib/content.ts` | `Prism.languages.vue = Prism.languages.markup` |

Verified at every stage rather than by inspection:

1. A full SFC — literal `<template>`, `<script setup>`, `<style scoped>` and a raw `onclick=` —
   round-trips through the normaliser **byte-for-byte**.
2. `language-vue` survives normalisation instead of degrading to plaintext.
3. Stored S3 content for `vue-sfc` holds `['vue','vue','vue','vue','vue']`.
4. The **real frontend highlighter**, run over that stored content, produced 134/59/43/40/30 tokens
   across the five blocks — 5 highlighted, 0 grey.

⚠️ **Vue is the worst case this content pipeline has faced.** The CLAUDE.md gotcha — an HTML parser
eating raw `<script>`/`<style>` *inside* code samples, with almost no change in character count — is
about content exactly like an SFC, and most snippets in this track are one. The
extract-`<pre>`-before-parse ordering in `content.py` is what saves it, and `check_content.py` is
what proves the ordering still holds. Do not reorder that.

⚠️ **The deployed backend Lambda has the old language list.** Seeding runs the local service layer,
so what is in S3 is correct — but editing one of these posts through `/admin` before
`lovemesomecoding_backend/scripts/deploy.sh` runs would normalise every `vue` block down to
`plaintext` and silently lose the highlighting. Same hazard the React track hit with `tsx`.

## Gaps in the demo app — needs a decision

The topic table was written against Vue as a subject; the app was written against ReelCMS as a
product. These are the features a 28-post track needs that the app has **zero** usage of. Counts are
from a grep over `src/`, not an impression.

| Missing | Lesson it serves | Cheapest honest fix |
|---|---|---|
| `src/composables/` — **no composables at all** | 15 (Composables) | Extract `useIntersectionObserver` from `FeedView` and a debounced search from `ExploreView`. The search has **no debounce today**, so this is a real improvement, not a contrivance. |
| `provide` / `inject` | 16 | Provide the admin layout's sidebar-collapsed state, or teach generically. |
| `<Teleport>` | 23 | A confirm-delete modal in `ReelListView` — deleting a reel currently has no confirmation at all. |
| `defineAsyncComponent`, `<Suspense>`, `<KeepAlive>` | 24 | Route-level lazy loading **does** exist and is quotable; the rest would be prose. |
| Custom directives | 15 (folded in) | `v-autofocus` on the login email field — 6 lines. Exactly what the Angular track did. |
| Named / scoped slots | 13 | Only `EmptyState` has a slot, and it is a bare default. Give `PaginationBar` or a list component a named slot. |
| Vitest + `@vue/test-utils` | 26 | The app has Playwright e2e and **no unit tests**. Angular hit this too and added a Vitest suite. |
| `reactive()`, `toRefs` | 5 | Everything is `ref`. Fine to teach generically — the lesson's advice is "use `ref`" anyway. |
| `defineModel` | 12 | `TagInput` implements `modelValue`/`update:modelValue` by hand, which is the better *teaching* example. Show `defineModel` as the shorthand without changing the app. |
| `watchEffect` | 7 | Ten `watch` calls, no `watchEffect`. Teach generically. |
| Sass | — | Styles are plain CSS. No lesson depends on Sass, so nothing is blocked. |

### Decision (2026-08-24, Folau)

**Close two: composables and the Teleport modal.** Both are genuine improvements to the app on
their own terms — the menu search has no debounce today, and deleting a reel has no confirmation at
all — so neither is a change made purely to serve a lesson.

**Not closed, and the affected lessons say so plainly rather than faking it:**

| Not added | How the lesson handles it |
|---|---|
| Vitest + `@vue/test-utils` | Lesson 26 teaches unit testing from generic examples and is explicit that the app's own suite is Playwright end-to-end. The Playwright specs it *does* quote are real. |
| `v-autofocus` custom directive | Lesson 15's directive section is generic. Vue developers write directives far less often than Angular developers do, so this costs the track little. |
| Named / scoped slots | Lesson 13 quotes `EmptyState` for the default slot and shows named and scoped slots as generic examples. |

This is the same shape of call the Angular track made: close the gaps that improve the app, teach
the small points generically, and never pretend an invented snippet came from the codebase.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Demo app | **ReelCMS**, not pizza | It is the only Vue app that exists, and it is a better fit for lifecycle/refs/observer lessons. |
| Track size | 28 posts | Matches Angular (28) and React (27) so `/vue` does not read as the thin one in its nav group. |
| API style | **Composition API only**, `<script setup>` | What vuejs.org leads with. One lesson (18) covers the Options API so legacy code is readable, then never uses it again — mirroring how the React track chose hooks over class components. |
| Snippet language | JavaScript + `.vue` SFCs | Read off the app. See the warning above. |
| Code block language | `vue` | Not `markup`. The class stays honestly `language-vue`; the frontend maps it to the markup grammar. |
| Dates | **Computed** from `START_DATE` + `STEP_DAYS`, **2025-10-09 .. 2025-12-29** | Post dates must fall between 2023 and 2025. Computing them made the re-base a one-line edit when the first publish got this wrong. |
| Lesson index | **Generated** by `gen_index.py` | A hand-written index of 28 links drifts the first time a lesson moves. `check_content.py` fails if it is stale. |
| Custom directives | Folded into lesson 15 | vuejs.org groups Composables, Custom Directives and Plugins under one "Reusability" heading. Vue developers write directives far less often than Angular developers do. |
| Seeding | Backend service layer, as React and Angular do | The static build reads only the derived indexes; reusing the admin API's own code is the only way to be sure indexes and posts agree. |
| Source material | vuejs.org + w3schools.com/vue | Per the standing instruction to draw on the official docs and w3schools. |

## Topic list

Reading order. `date` ascends so the prev/next pager reads lesson 1 → lesson 28. **Every slug is
new.** "app" means the lesson's snippets come from ReelCMS; "gap" means it needs one of the
additions above or generic examples.

### Part 1 — Getting started

| # | Slug | Source | |
|---|------|--------|---|
| 1 | `vue-get-started` | the track index, versions table | ✅ written |
| 2 | `vue-set-up` | `package.json`, `vite.config.js`, `index.html`, `main.js` | app |
| 3 | `vue-sfc` | `EmptyState.vue`, `AppToast.vue` | ✅ written |
| 4 | `vue-template-syntax` | `ReelCard.vue`, `StatusBadge.vue` | app |

### Part 2 — Reactivity

| # | Slug | Source | |
|---|------|--------|---|
| 5 | `vue-reactivity` | `stores/toast.js`, `FeedView.vue` | app + generic `reactive` |
| 6 | `vue-computed` | `stores/auth.js`, `ReelPlayer.vue` | app |
| 7 | `vue-watchers` | `ExploreView.vue`, `ReelPlayer.vue` | app + generic `watchEffect` |
| 8 | `vue-list-rendering` | `ExploreView.vue`, `TagInput.vue` | app |

### Part 3 — Components

| # | Slug | Source | |
|---|------|--------|---|
| 9 | `vue-components` | `components/ui/*`, `PublicLayout.vue` | app |
| 10 | `vue-props` | `EmptyState.vue`, `ReelPlayer.vue` | app |
| 11 | `vue-events` | `ReelPlayer.vue`, `TagInput.vue` | app |
| 12 | `vue-v-model` | `TagInput.vue`, `ReelEditView.vue` | app + `defineModel` prose |
| 13 | `vue-slots` | `EmptyState.vue` | **gap** — default slot only |
| 14 | `vue-lifecycle` | `FeedView.vue`, `ReelPlayer.vue` | app |

### Part 4 — Reusing logic and state

| # | Slug | Source | |
|---|------|--------|---|
| 15 | `vue-composables` | extracted from `FeedView`/`ExploreView` | **gap** — none exist |
| 16 | `vue-provide-inject` | `AdminLayout.vue` | **gap** — none exist |
| 17 | `vue-pinia` | `stores/auth.js`, `stores/toast.js`, `AppToast.vue` | app |
| 18 | `vue-options-api` | one app component rewritten both ways | app |

### Part 5 — Routing, forms and data

| # | Slug | Source | |
|---|------|--------|---|
| 19 | `vue-router` | `router/index.js`, both layouts | app |
| 20 | `vue-router-guards` | `router/index.js`, `stores/auth.js` | app |
| 21 | `vue-forms` | `LoginView.vue`, `ReelEditView.vue` | app |
| 22 | `vue-http` | `api/index.js`, `api/http.js`, `api/session.js` | app |

### Part 6 — Advanced features and shipping

| # | Slug | Source | |
|---|------|--------|---|
| 23 | `vue-transitions-and-teleport` | `AppToast.vue` (TransitionGroup) | **gap** — no Teleport |
| 24 | `vue-async-components` | `router/index.js` lazy routes | partial — lazy routes only |
| 25 | `vue-performance` | `FeedView.vue` (observer, cursor pagination) | app |
| 26 | `vue-testing` | `tests/` | **gap** — Playwright only, no unit tests |
| 27 | `vue-deployment` | `vite.config.js`, `.env`, `dist/` | app |
| 28 | `vue-interview-questions` | the whole track | — |

## Layout

```
projects/vue_tutorial/
  manifest.py        category metadata + one entry per post (slug, title, part, date, tags, excerpt)
  authoring.py       code() / from_app() helpers -- NEVER hand-escape a code block
  posts/NN-slug.html the post bodies, plain semantic HTML
  seed.py            writes the category and posts into a content tree
  check_content.py   proves the normaliser round-trips every code sample (no AWS needed)
  check_snippets.py  proves every quoted snippet still matches the demo app (no AWS needed)
  gen_index.py       regenerates lesson 1's lesson index from the manifest
  progress_report.md this file — read it first
```

## Commands

```bash
# Verify the manifest and any written content
lovemesomecoding_backend/.venv/bin/python projects/vue_tutorial/check_content.py

# Verify every quoted snippet still matches the demo app. Run BOTH — they check
# different things, and only this one goes stale on its own.
python3 projects/vue_tutorial/check_snippets.py

# Regenerate lesson 1's index after adding/renaming/reordering a lesson
lovemesomecoding_backend/.venv/bin/python projects/vue_tutorial/gen_index.py --write

# Seed. --only takes a subset while the rest of the track is unwritten.
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/vue_tutorial/seed.py \
  --env local --only vue-sfc --write
```

## Gotchas paid for already

- **Prism has no `vue` grammar.** Discovered before authoring rather than after. `markup` is the
  right grammar and the alias is registered on the frontend. `check_content.py` asserts
  `normalize_language("vue") == "vue"` directly, so the day someone trims `SUPPORTED_LANGUAGES` the
  check fails instead of 28 posts quietly turning grey.
- **An unsupported language degrades to plaintext silently, never rejected.** That is why the
  checker treats an authored `language-X` that normalises to `plaintext` as a hard failure.
- **Never hand-escape an SFC in a `<pre>`.** A snippet contains a literal `<template>` and
  `<script setup>`; one missed `&lt;` opens a real element and everything after it disappears into
  it. `authoring.py` escapes once, correctly, and `from_app()` reads the app file rather than
  retyping it — which is what makes `check_snippets.py` meaningful.
- **`reelcms-vue-frontend` uses Pinia 4 and Vite 8**, both ahead of what most tutorials show. Read
  versions off `package.json`, never from memory.


---

## Publish log — 2026-08-24

| Step | Result |
|---|---|
| `check_content.py` | 28/28 written, 233 code blocks, every one round-trips byte-for-byte, 72 internal links resolve |
| `check_snippets.py` | 82 blocks verbatim from the demo app, 131 illustrative, no drift |
| Backend tests | 90 passed |
| Backend deploy | `lovemesomecoding-admin-api-prod` updated — `vue` now in the Lambda's `SUPPORTED_LANGUAGES` |
| Prod seed | 28 created, category count 28 |
| Frontend deploy | build 394b0bd, `verify-build` 778/778 posts and 43/43 categories, CloudFront invalidated |
| Live check | 28/28 URLs 200, 28 sitemap entries, `vue-sfc` renders 5 `language-vue` blocks with 306 Prism tokens |

### ⚠️ The backend deploy needs three env vars that nothing documents

`scripts/deploy.sh` passes `DomainName`, `CertificateArn` and `HostedZoneId` **explicitly on every
deploy**, reading them from `API_DOMAIN`, `API_CERT_ARN` and `HOSTED_ZONE_ID`. With none of them set
it passes `DomainName=` and `sam deploy` refuses the empty value — which is lucky, because that is
the one thing standing between a bare `./scripts/deploy.sh` and CloudFormation tearing down
`api.lovemesomecoding.com`. The script's own guard only covers the case where `API_DOMAIN` is set and
the cert is not.

The values are on the live stack, and this is the command that works:

```bash
AWS_PROFILE=folau \
API_DOMAIN="api.lovemesomecoding.com" \
API_CERT_ARN="arn:aws:acm:us-west-2:329580012644:certificate/4a17f02e-5d4e-42b1-86fd-31e7068cb347" \
HOSTED_ZONE_ID="Z000531818AC6P1IJ8LJL" \
./scripts/deploy.sh
```

Verified afterwards: `api.lovemesomecoding.com/health` → 200, and the parameters the script does
*not* pass (`MediaCdn`, `GithubRepo`, `StorageBucket`, `DbBucket`) kept their values, as
CloudFormation's omitted-parameter behaviour promises. **Worth fixing in `deploy.sh`** — it should
read the current values off the stack rather than requiring three undocumented variables.

### ⚠️ NEW GOTCHA: the first prod seed silently left two posts out of the indexes

On the first `seed.py --env prod --write`, `vue-watchers` and `vue-list-rendering` were written as
correct post objects but were **absent from `index/posts.json`, `index/categories.json` and
`index/by-category/vue.json`**. The archive said 28; the category count said 26.

This is the most dangerous shape of bug this content pipeline has, because nothing catches it:

- **The static build reads only the indexes**, so the two lessons would simply not exist on the
  site. No 404, no error — a 28-lesson track quietly serving 26.
- **`verify-build.mjs` would have passed.** Its index cross-check compares the derived indexes
  against *each other*, and all three agreed, because all three were missing the same two posts.
  Nothing anywhere compares the indexes against the actual post objects in `posts/`.

`upsert_post` → `_reindex` rewrites the entire index per post — read, drop the slug, append, sort,
write — and a seed of 28 posts does that 28 times in a row. Re-running the seed repaired it
completely, so the write path recovers; the problem was purely that nothing noticed.

**`seed.py` now checks.** After writing, it asserts every seeded slug is present in both
`index/posts.json` and the category index, prints exactly what is missing, and exits non-zero telling
you to re-run. The check was verified by reproducing the drift against the local tree: it reported
precisely `vue-watchers` and `vue-list-rendering`.

Final prod state audited object-by-object: **778 post objects, 778 index entries, vue count 28,
`by-category/vue.json` 28 entries.** The 750 pre-existing posts were consistent throughout, and
nothing in the index lacked an object.


---

## Date correction — 2026-08-24

**Post dates must be between 2023 and 2025.** The first publish used `START_DATE = 2026-09-01`,
putting the track at 2026-09-01 .. 2026-11-21 — outside that range, and (since it shipped on
2026-08-24) **dated in the future**. A future-dated post sorts to the top of every archive and the
sitemap while claiming a publish day that has not happened.

Fixed by re-basing `START_DATE` to **2025-10-09**, which puts the 81-day span at
**2025-10-09 .. 2025-12-29**. That is exactly the one-line edit the computed-dates design exists for.

Republishing needed **`--force-dates`**: `upsert_post` never overwrites the date of a post that
already exists, so without it all 28 would have kept their 2026 timestamps. This is the case the flag
was kept for.

```bash
AWS_PROFILE=folau .../seed.py --env local --write --force-dates
AWS_PROFILE=folau .../seed.py --env prod  --write --force-dates
cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy
```

`check_content.py` now **enforces the range**: every post's date must fall within 2023-01-01 ..
2025-12-31 and must not be in the future. Verified by re-basing to 2026 and confirming it produced 56
failures (28 out of range + 28 future-dated), then restoring.

Live afterwards: lesson 1 renders "October 9, 2025", lesson 28 "December 29, 2025", 28/28 URLs 200,
28 sitemap entries, and no 2026 date anywhere in the track.

### ⚠️ Other tracks are still dated 2026

This rule was applied to `/vue` only, because that is what was being published. **`/react`
(2026-06-03 .. 2026-08-20) and `/angular` (2026-05-28 .. 2026-08-17) both violate it**, and 340 posts
across the whole site carry a 2026 date. Both tracks compute or hard-code their dates the same way,
so re-basing either is the same one-line edit plus a `--force-dates` seed — but it reshuffles the
archive, so it is a decision rather than a cleanup. Not done.

### Note on the concurrent publish

Prod grew from 778 to 782 posts during this work — four posts published from elsewhere while the
re-seed was running. Nothing was clobbered: the seed only touches its own 28 slugs, and the synced
content (782) matches prod (782) exactly. One deploy also hit four transient
`Need to rewind the stream` upload failures; re-running the deploy fixed them, and all four URLs
return 200.

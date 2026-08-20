# Frontend Dev track — progress report

**Status:** PUBLISHED — live on prod, 2026-08-20
**Started:** 2026-08-20
**Where it lands:** https://lovemesomecoding.com/frontend-dev

---

## What this is

`/frontend-dev` holds **2 posts published 2019-02-06** (last touched 2021). Both are short career
prose with no code, both still wrapped in the WordPress `boldgrid-section` divs, and neither has a
single `<h2>` — so neither has a table of contents.

| Slug | Title | Words |
|---|---|---:|
| `frontend-dev-what-is-a-frontend-engineer` | What is a frontend engineer? | 86 |
| `frontend-dev-what-to-learn-in-a-framework-as-a-frontend-engineer` | What to learn in a framework as a frontend engineer? | 225 |
| | **total** | **311** |

The second post is **truncated**. It ends on a bare `<strong>#8 Cache</strong>` heading with no
body, and its "Optionals" paragraph promises items 8+ that were never written. It has been live in
that state since 2019.

This project rewrites both **in place** — same slugs, so no indexed URL is lost — and builds the
category out into a **12-post roadmap track** matched to the `/backend-dev` track.

## The conflict this track had to resolve

The README says "update **java** frontend dev posts". There is no Java anywhere in
`/frontend-dev` — that phrase is a copy-paste from `projects/backend_dev/README.md` ("update java
backend dev posts"). Read as "the frontend-dev posts". Flagged to Folau 2026-08-20 before writing.

Second: "update all posts in the tutorial" taken literally means editing 2 posts and stopping,
which leaves `/frontend-dev` a stub next to `/react` (27), `/css` (21), `/javascript` (19),
`/html` (12) and `/backend-dev` (10). Put to Folau as an explicit choice.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Scope | **Rewrite 2 + build out to 12** | Folau, 2026-08-20. A 2-post category is not a track. 12 mirrors `/backend-dev`'s 10 so the pair reads as one curriculum. |
| Angle | **Career/roadmap, links out** | Folau, 2026-08-20. `/react`, `/javascript`, `/css`, `/html` already hold 79 posts of hands-on teaching. This track names what to learn and in what order, then sends you there. Duplicating them would compete with them in search. |
| Existing 2 posts | Rewrite in place, keep both slugs | They are indexed URLs from 2019. |
| Track size | **12** — 2 rewritten + 10 new | |
| Snippets | Lifted from `pizza-react-frontend` | Per `CLAUDE.md`. Real React 19 / TS / Vite / Redux Toolkit / React Router 7 code, verified by `check_snippets.py`. |
| Dates | 2026-08-01 … 2026-08-23, 2 days apart, at **12:00** | See the hour-collision note below. |
| Publish | **Seed local → Folau reviews → prod** | Folau, 2026-08-20. Published to prod same day on his go-ahead. |
| Nav | No change needed | `src/lib/nav.ts:57` already maps `frontend-dev` → "Frontend Development" under "Software Engineering". |

### The 12:00 stamp is deliberate

The archive sorts by date and an exact tie makes the order arbitrary. Hours already taken on prod:

| Hour | Track | Posts |
|---|---|---:|
| 09:00 | `/react` + `/spring-boot` | 62 |
| 10:00 | `/data-structure-algorithm` | 25 |
| 11:00 | `/backend-dev` | 10 |
| 14:00 | `/spring-study-guide` | 9 |
| **12:00** | **`/frontend-dev`** | **12** |

The first draft of this plan used 09:00, which would have collided head-on with 62 posts. Caught by
the parallel `backend_dev` session before any dates were written.

## Coordination with the `backend_dev` session

`/backend-dev` was rewritten in a **parallel Claude session on 2026-08-20**, and it publishes into
the same content tree. Confirmed with that session directly:

- **All 10 backend-dev slugs are final and already live on prod.** Safe to link.
- **Seeding must not overlap.** `upsert_post` read-modify-writes three *global* derived indexes —
  `index/posts.json`, `index/categories.json`, `search/index.json`. Two seed scripts running at
  once is a lost-update race: last writer wins, one track vanishes from the indexes while every
  individual post JSON still resolves. That is the `/oracle` "12 tutorials over a list of 13" bug.
  The window is per-run, not per-session — once a seed script exits, it is safe.
- **The local tree is stale.** backend_dev seeded prod last, so local is at 557 posts and prod at
  583. Re-sync local from prod before seeding, or the seed builds on a stale index.
- **Baseline prod at 583** and cross-check `index/categories.json` against `index/posts.json`
  after seeding. `verify-build.mjs` check 6 does the same, so a build failure also catches drift.

## The 12 posts

Numbered as they read. `#2` and `#5` are the two pre-existing slugs — their names look odd for
their position because the slug is fixed and cannot be renamed without losing the URL.

| # | Slug | Title | State |
|---|---|---|---|
| 1 | `frontend-dev-get-started` | Frontend Dev – Get Started | new |
| 2 | `frontend-dev-what-is-a-frontend-engineer` | Frontend Dev – What a Frontend Engineer Actually Does | **rewrite** |
| 3 | `frontend-dev-html-css-and-the-browser` | Frontend Dev – The HTML, CSS and Browser You Actually Need | new |
| 4 | `frontend-dev-javascript-and-typescript` | Frontend Dev – The JavaScript and TypeScript You Actually Need | new |
| 5 | `frontend-dev-what-to-learn-in-a-framework-as-a-frontend-engineer` | Frontend Dev – What to Learn in a Framework | **rewrite** |
| 6 | `frontend-dev-state-management` | Frontend Dev – State Management | new |
| 7 | `frontend-dev-talking-to-the-backend` | Frontend Dev – Talking to the Backend | new |
| 8 | `frontend-dev-routing-and-forms` | Frontend Dev – Routing, Forms and Validation | new |
| 9 | `frontend-dev-auth-and-security` | Frontend Dev – Authentication and Security in the Browser | new |
| 10 | `frontend-dev-performance-and-accessibility` | Frontend Dev – Performance and Accessibility | new |
| 11 | `frontend-dev-testing` | Frontend Dev – Testing | new |
| 12 | `frontend-dev-build-and-deployment` | Frontend Dev – Build Tooling and Deployment | new |

Post 12 pairs with `/backend-dev/backend-dev-deployment-and-observability`; posts 7 and 9 pair with
`backend-dev-apis-and-http` and `backend-dev-auth-and-security`. Those cross-links are the point of
matching the structure.

## Versions the track is written against

Read off `pizza-react-frontend/package.json` — not from memory. When the app moves, the landing
page's table is the first edit.

| | |
|---|---|
| React | 19.2.8 |
| TypeScript | ~6.0.2 |
| Vite | 8.2.0 |
| React Router | 7.18.2 |
| Redux Toolkit | 2.12.0 |
| Bootstrap | 5.3.8 |
| Playwright | 1.62.1 |
| Sass | 1.102.0 |

## Demo-app changes

**None expected.** `pizza-react-frontend` already covers every topic in the track with real code:

| Topic | Backed by |
|---|---|
| Browser/CSS | `styles/_tokens.scss`, `styles/theme.scss` |
| TypeScript | `types/index.ts`, the `ApiError` class in `lib/api.ts` |
| Framework | `App.tsx`, `components/`, `pages/` |
| State | `context/` (4 contexts) + `store/` (5 slices) — and the documented reason for the split |
| Talking to the backend | `lib/api.ts`, `lib/adminApi.ts`, `lib/profileApi.ts` |
| Routing/forms | `App.tsx` routes, `ProtectedRoute.tsx`, `LoginPage.tsx`, `CheckoutPage.tsx` |
| Auth/security | `context/AuthContext.tsx`, `tokenStore`, `ProtectedRoute.tsx` |
| Performance | `lazy`/`Suspense` in `App.tsx`, `useMemo`/`useCallback`, the admin-chunk Redux split |
| Accessibility | `useId` label wiring, `visually-hidden`, `prefers-reduced-motion` mixin |
| Testing | 12 Playwright specs in `e2e/` |
| Build/deploy | `vite.config.ts`, `package.json` scripts, `VITE_API_BASE_URL` |

So this track is **content-only**. No branch, no app edits.

## Tooling

Copied from `projects/backend_dev/` and repointed at the React app:

| Script | What it proves |
|---|---|
| `check_content.py` | Every code sample round-trips the normaliser byte-for-byte, and comes out in the exact `<pre class="language-X"><code class="language-X">` shape the build-time Prism highlighter matches. Compares sources, never lengths. |
| `check_links.py` | HTML is well-formed, and every internal href resolves to a real category or post — including the 10 live `/backend-dev/...` targets. |
| `check_snippets.py` | Every substantial code line in every post exists in `pizza-react-frontend` source. Corpus repointed from `*.java` to `*.ts/*.tsx/*.scss/*.json`. |
| `verify_track.spec.ts` | Playwright delivery check against the built site: the archive lists all 12 in order, every post renders with a real outline and anchored headings, **both 2019 URLs still resolve to the rewritten posts**, code is highlighted, cross-track `/backend-dev` links work, and each post links to the next. |
| `seed.py` | Writes through the backend's own service layer so the derived indexes stay consistent. `--force-dates` needed once, because both rewritten posts carry 2019 dates and `upsert_post` never overwrites an existing date. |

## Log

- **2026-08-20** — Read the category. Found 2 posts, 311 words total, one truncated mid-sentence
  since 2019. Flagged the "java frontend dev" README copy-paste and the 2-post scope question to
  Folau; got the build-out + roadmap-angle + review-before-prod answers.
- **2026-08-20** — Found `/backend-dev` already rewritten to 10 posts by a parallel session.
  Adopted its structure and title convention so the two tracks pair.
- **2026-08-20** — Coordinated with that session on the shared-index race. Moved the hour from
  09:00 to 12:00 on its advice (09:00 already holds 62 posts).
- **2026-08-20** — Project scaffolded, manifest written.
- **2026-08-20** — All 12 posts written. 16,989 words, 64 code blocks, every block
  highlighted. Verification: `check_content.py` (all samples round-trip byte-for-byte),
  `check_links.py` (82 internal links resolve, including the 10 live `/backend-dev` targets),
  `check_snippets.py` (119 code lines, all present in `pizza-react-frontend`).
- **2026-08-20** — Reset the local tree from prod first (it was 26 objects behind; diffed both
  trees to confirm the sync was purely additive and destroyed nothing). Seeded local with
  `--force-dates`: 583 → 593 posts, `/frontend-dev` count 12. Cross-checked the derived indexes —
  44/44 category counts agree, by-category matches posts.json, all 12 in the search index.
- **2026-08-20** — Built the site: `verify-build.mjs` passed 593/593 posts, 44/44 categories,
  index cross-check 44/44. Playwright delivery check (`verify_track.spec.ts`) — 6/6 pass.
- **2026-08-20** — **PUBLISHED.** Seeded prod 583 → 593, `/frontend-dev` count 12. Prod indexes
  cross-checked before building: 44/44 category counts agree, by-category matches posts.json, all
  12 in the search index. `npm run deploy` — verify-build 593/593 posts and 44/44 categories, 1571
  files to S3, CloudFront function republished (41 redirects, 2.8 KB of the 10 KB limit),
  invalidation `IA5LN952211IPCNV7X84BZBPN9` completed, edge verified serving build `394b0bd`.
  All 12 URLs return 200 live, all 12 in `sitemap.xml`, and both 2019 URLs serve rewritten bodies
  with zero `boldgrid-section` wrappers. `verify_track.spec.ts` re-run against
  https://lovemesomecoding.com — 6/6 pass.

## Follow-ups

- `/frontend-dev` is 12 new/changed URLs. Worth resubmitting `sitemap.xml` to Search Console —
  which is already an open item in `CLAUDE.md` and now has more reason to happen.
- The two rewritten 2019 slugs keep their URLs but their content changed completely. Expect
  Search Console to re-crawl and re-rank them; that is the intended trade.

# Angular tutorial track — progress report

**Status:** SCAFFOLDED — topic table, manifest and tooling done. **Post bodies are blocked.**
**Started:** 2026-08-20
**Where it lands:** https://lovemesomecoding.com/angular

---

## What this is

`/angular` currently holds **exactly one post**: `angular-component`, published 2019-07-31, with an
**empty body** (`wordCount: 0`). The URL is indexed; there is nothing on it.

This project builds a **29-post Angular 22 track** in that collection — 28 new posts plus
`angular-component` rewritten in place at its existing URL.

## The blocker — read this first

Every code sample must come from
`lovemesomecoding_demo_project/pizza/pizza-angular-frontend`, per the project README and
`lovemesomecoding_demo_project/pizza/CLAUDE.md`.

**That directory is empty.** It is Phase 7 of the pizza demo and Folau is building it. Until it
exists there is nothing honest to snippet from, so:

- ✅ Written: `manifest.py`, `seed.py`, `check_content.py`, this report, the topic table.
- ⛔ Not written: anything in `posts/`. **Do not author a post body from invented code.**

`check_content.py` reports un-written posts as `not written` and exits 0, so the manifest can be
validated today. `seed.py` refuses to run at all while any file is missing — it fails on the first
one rather than half-seeding.

### What the app needs to contain

The track's snippet plan (right-hand column of the topic table) assumes the Angular app reaches
roughly the same surface as `pizza-react-frontend`: menu, pizza builder, cart, checkout, login,
order history, profile, and at least one admin page with a table and a report. Anything the app
does not do, the lesson cannot show. Per the README, **if an example is missing, add it to the app
first and make sure it still works** — the same rule the React track followed, which is how Redux
Toolkit and Sass ended up in `pizza-react-frontend`.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Existing `angular-component` | Rewrite in place, keep the slug | It is an indexed URL. Rewriting fills an empty page without losing it. |
| Track size | 29 posts | Folau chose ~25–30. Comparable to the React track's 27; deep enough to ship a project from, finite enough to maintain. |
| Angular version | **22** (current on angular.dev) | Signals-first, standalone by default, zoneless available. Writing against 20 or below would ship stale on day one. |
| Styling | **Tailwind 4** | `pizza/CLAUDE.md` already specifies Tailwind for the Angular frontend, deliberately different from the React app's Bootstrap. |
| Snippet language | TypeScript + HTML templates | Copied verbatim from the demo app, so every snippet is provably real code. |
| Dates | **Computed** in `manifest.py` from `START_DATE` + `STEP_DAYS` | The React manifest hard-codes dates, which only worked because it shipped the day it was written. This track is authored well before it publishes, so re-basing must be a one-line edit. |
| Seeding | Backend service layer, as `projects/react_tutorial/seed.py` does | The static build reads only the derived indexes; reusing the admin API's own code is the only way to be sure indexes and posts agree. |
| Source material | angular.dev + w3schools.com/angular | Per the README. w3schools' Angular section is **modern Angular, not AngularJS** — checked 2026-08-20. |

## Topic list

The order is the reading order. `date` ascends with the track so the prev/next pager reads
lesson 1 → lesson 29. Slugs are all new except where marked.

### Part 1 — Getting started

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 1 | `angular-get-started` | Get Started | new | the track index; versions table |
| 2 | `angular-set-up` | Set Up a Project with the Angular CLI | new | `angular.json`, `package.json`, `main.ts`, `app.config.ts` |
| 3 | `angular-typescript` | The TypeScript You Need First | new | `types/` — the shared API contract |

### Part 2 — Components and templates

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 4 | `angular-component` | Your First Component | **rewrite** | `ProductCard`, `Footer`, `App` |
| 5 | `angular-templates` | Templates and Data Binding | new | `ProductCard`, `HomePage` |
| 6 | `angular-events` | Handling Events | new | `ProductCard`, `LoginPage`, pizza builder |
| 7 | `angular-control-flow` | Control Flow with `@if`, `@for`, `@switch` | new | `MenuPage`, `CartDrawer` |
| 8 | `angular-inputs-outputs` | Inputs, Outputs and Two-Way Binding | new | `ProductCard`, pizza builder |
| 9 | `angular-content-projection` | Content Projection and `ng-template` | new | modal / drawer shell |
| 10 | `angular-directives` | Directives | new | a custom directive in the app |
| 11 | `angular-pipes` | Pipes | new | money formatting, order dates |
| 12 | `angular-styles` | Component Styles with Tailwind | new | Tailwind setup + `:host` usage |

### Part 3 — Reactivity

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 13 | `angular-signals` | Signals | new | cart state, menu state |
| 14 | `angular-computed-effect` | `computed`, `effect` and `linkedSignal` | new | cart totals, toast auto-dismiss |
| 15 | `angular-lifecycle` | The Component Lifecycle | new | wherever `ngOnInit` / `DestroyRef` are used |

### Part 4 — Services, DI and data

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 16 | `angular-services-dependency-injection` | Services and Dependency Injection | new | `AuthService`, `CartService`, `MenuService` |
| 17 | `angular-http-client` | Talking to an API with HttpClient | new | the API layer against `:8085` |
| 18 | `angular-interceptors` | HTTP Interceptors | new | auth-token and error interceptors |
| 19 | `angular-rxjs` | RxJS, and How Much of It You Still Need | new | search box `switchMap`, `toSignal` |

### Part 5 — Routing

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 20 | `angular-router` | Routing | new | `app.routes.ts` |
| 21 | `angular-route-guards` | Guards, Resolvers and Lazy Loading | new | admin guard + lazy admin chunk |

### Part 6 — Forms

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 22 | `angular-forms` | Template-Driven Forms | new | login form |
| 23 | `angular-reactive-forms` | Reactive Forms and Validation | new | checkout / address form |

### Part 7 — Shipping it

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 24 | `angular-state-management` | State Management | new | the signal store service |
| 25 | `angular-testing` | Testing | new | the app's own specs |
| 26 | `angular-performance` | Change Detection, OnPush, Zoneless and `@defer` | new | `@defer` on a heavy admin view |
| 27 | `angular-ssr` | Server-Side Rendering and Hydration | new | `ng add @angular/ssr` on the app |
| 28 | `angular-build-deploy` | Build and Deploy to Production | new | bundle report, budgets, CI |
| 29 | `angular-interview-questions` | Interview Questions | new | — |

## Versions the track is written against

Stated on lesson 1 and assumed throughout. Held in `manifest.VERSIONS`. **When these move, that
table is the first edit.**

| | |
|---|---|
| angular / @angular/cli | **22.1** |
| typescript | 6.0 |
| tailwindcss | 4.2 |
| rxjs | 7.8 |
| Node.js | 22 (20.19 is Angular 22's minimum) |

## Things already checked, so nobody re-checks them

- **No language-pipeline changes are needed.** The React track had to add `typescript`, `jsx` and
  `tsx` to `SUPPORTED_LANGUAGES` and static-import three Prism grammars. Angular needs
  `typescript`, `html` (aliased to `markup`), `css`, `json` and `bash` — **all already supported**
  on both ends. Verified in `lovemesomecoding_backend/app/services/content.py:28` and
  `lovemesomecoding_frontend/src/lib/content.ts`.
  ⚠️ The one gap: **`scss` is not supported** and would silently normalise to `plaintext`. Tailwind
  4 configures in plain CSS, so use `language-css` and there is nothing to add. If a lesson ever
  needs real Sass, `scss` must be added to both ends first.
- **The site nav already lists Angular** — `nav.ts:26` has it in the `JavaScript` group. No nav edit.
- **`w3schools.com/angular/` is modern Angular, not AngularJS.** Checked 2026-08-20; safe as a
  topic source, which is what the README asks it for.
- **Angular's current release is 22.** Checked against angular.dev on 2026-08-20.

## Gotchas to expect when the bodies get written

- **Do not hand-escape Angular templates in a `<pre>`.** Bodies will be full of
  `<app-product-card [product]="p" />`, `@if (…) {`, and `{{ total() }}`. One missed `&lt;` is
  invisible until it renders. `check_content.py` compares authored source against the normaliser's
  output byte-for-byte and is the only thing that catches it.
- **`angular-component`'s slug is frozen.** `check_content.py` fails if it leaves the manifest.
- **`--force-dates` will be needed exactly once**, for `angular-component`: `upsert_post` never
  overwrites an existing post's `date`, so without it that lesson keeps its 2019 timestamp and
  sorts to the very back of the track. Do not use the flag on later runs.
- **The category description is currently empty** in `index/categories.json`. `seed.py` sets it from
  `manifest.CATEGORY`, so `/angular` gets a real description on the first write.

## Next steps

1. ⛔ **Blocked on Folau:** build `pizza-angular-frontend` (Angular 22 + Tailwind 4 against the
   existing Spring Boot API on `:8085`).
2. Walk the topic table against the finished app; anything with no source gets added to the app
   first, per the README.
3. Re-base `manifest.START_DATE` to land lesson 29 on the intended publish date.
4. Author `posts/`, running `check_content.py` as each one lands.
5. Seed `--env local --write`, review at `:3000`.
6. Seed `--env prod --write --force-dates`, then
   `cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy`.

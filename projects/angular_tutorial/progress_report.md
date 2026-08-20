# Angular tutorial track — progress report

**Status:** READY TO AUTHOR — demo app built, gaps closed, tooling verified. Post bodies not started.
**Started:** 2026-08-20
**Where it lands:** https://lovemesomecoding.com/angular

---

## What this is

`/angular` currently holds **exactly one post**: `angular-component`, published 2019-07-31, with an
**empty body** (`wordCount: 0`). The URL is indexed; there is nothing on it.

This project builds a **28-post Angular 21 track** in that collection — 27 new posts plus
`angular-component` rewritten in place at its existing URL.

Every code sample comes from `lovemesomecoding_demo_project/pizza/pizza-angular-frontend`.

## Where it stands

| | |
|---|---|
| Topic table | ✅ 28 lessons, agreed |
| `manifest.py` | ✅ every lesson has slug, title, tags, excerpt, computed date |
| `seed.py` / `check_content.py` | ✅ both run clean |
| Content pipeline | ✅ `scss` support added (see below) |
| Demo app | ✅ built, and the four missing examples added |
| Post bodies | ⛔ **none written** — this is the whole remaining job |

## The demo app

Built by Folau, finished 2026-08-20. Angular **21.2.21**, TypeScript **5.9.3**, Bootstrap 5.3 +
Sass, NgRx 21, Stripe.js. Standalone, **zoneless** (no zone.js installed at all), `OnPush` on all
30 components.

⚠️ **The app is on Angular 21 while 22 is current.** The versions in `manifest.VERSIONS` are read
off the app, not chosen — a lesson claiming 22 over a snippet copied from a 21 codebase is exactly
the kind of drift nobody spots later. If the app is upgraded, that table is the first edit.

⚠️ **An earlier plan said Tailwind.** It was overruled: both frontends use Bootstrap so the diff
between them is purely framework. `pizza/CLAUDE.md` records this. Lesson 12 was written for
Tailwind and has been rewritten.

### What was added to close gaps

The audit found eight things the track needed and the app did not have. Folau chose which to close;
four were added, and all of them are covered by new unit tests.

| Added | Where | Serves |
|---|---|---|
| `Autofocus` directive | `core/autofocus.directive.ts`, used on the login email field | Lesson 10 — the app had **no `@Directive` at all** |
| Debounced menu search | `pages/menu/menu-page.ts` + `.html` | Lesson 19 — `toObservable` → `debounceTime` → `distinctUntilChanged` → `switchMap` → `toSignal` |
| `confirmLeaveGuard` | `core/guards.ts`, on the `checkout` route | Lesson 21 — `CanDeactivateFn` returning a **promise**, answered by a modal rather than `window.confirm` |
| Vitest unit suite | 5 spec files, 23 tests | Lesson 25 — the app had **zero** unit tests, only Playwright |

The search hits `GET /api/search/products?q=…`, which **already existed** on the backend
(Elasticsearch-backed with a database fallback). No backend change was needed.

### Deliberately NOT added

| Not added | Consequence for the track |
|---|---|
| `@angular/ssr` | **Lesson 27 (SSR) was cut.** `ng add @angular/ssr` touches Stripe.js, `localStorage` and `window` access across the whole app; the risk to a working app outweighed one lesson. Track went 29 → 28. |
| `@defer` | Lesson 26 covers change detection, `OnPush` and zoneless — all richly sourced — and treats `@defer` as prose plus route-level code splitting, which the app does use. |
| `@switch`, `linkedSignal` | Illustrated generically in lessons 7 and 14. Both are small syntax points; neither needs a worked example. |
| `CanMatch`, `ResolveFn` | Lesson 21 covers `CanActivate` and `CanDeactivate`, both real in the app. |

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Existing `angular-component` | Rewrite in place, keep the slug | It is an indexed URL. Rewriting fills an empty page without losing it. |
| Track size | 28 posts | Folau chose ~25–30; SSR was then cut. Comparable to the React track's 27. |
| Angular version | **21**, matching the app | See the warning above. |
| Snippet language | TypeScript, HTML templates, SCSS | Copied verbatim, so every snippet is provably real code. |
| Dates | **Computed** from `START_DATE` + `STEP_DAYS` | This track is authored well before it publishes, so re-basing must be a one-line edit. The React manifest hard-codes dates and only got away with it by shipping the same day. |
| Seeding | Backend service layer, as `projects/react_tutorial/seed.py` does | The static build reads only the derived indexes; reusing the admin API's own code is the only way to be sure indexes and posts agree. |
| Source material | angular.dev + w3schools.com/angular | Per the README. w3schools' Angular section is **modern Angular, not AngularJS** — checked 2026-08-20. |

## Topic list

Reading order. `date` ascends so the prev/next pager reads lesson 1 → lesson 28. All slugs new
except where marked.

### Part 1 — Getting started

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 1 | `angular-get-started` | new | the track index; versions table |
| 2 | `angular-set-up` | new | `angular.json`, `main.ts`, `app.config.ts`, the three tsconfigs |
| 3 | `angular-typescript` | new | `core/models.ts` — the shared API contract |

### Part 2 — Components and templates

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 4 | `angular-component` | **rewrite** | `product-card`, `app-footer` (no logic at all), `app.ts` |
| 5 | `angular-templates` | new | `product-card`, `home.html` |
| 6 | `angular-events` | new | `login`, `pizza-builder-modal`, `(keydown.escape)` in `modal.ts` |
| 7 | `angular-control-flow` | new | `menu-page.html`, `cart-drawer.html`; the one surviving `*ngIf` in `app-navbar.html` |
| 8 | `angular-inputs-outputs` | new | `modal.ts` (`input`/`output`), `Autofocus` (`booleanAttribute` transform) |
| 9 | `angular-content-projection` | new | `modal.ts` — three named slots via `select` |
| 10 | `angular-directives` | new | **`core/autofocus.directive.ts`** (added) |
| 11 | `angular-pipes` | new | `core/money.pipe.ts` — `MoneyPipe` and `HumanisePipe` |
| 12 | `angular-styles` | new | `styles.scss`, `styles/_tokens.scss`, `theme.scss`, `angular.json` load order |

### Part 3 — Reactivity

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 13 | `angular-signals` | new | `cart.service`, `auth.service`, `menu.service` |
| 14 | `angular-computed-effect` | new | cart totals, `effect` with `onCleanup` in `cart.service` |
| 15 | `angular-lifecycle` | new | the *absence* of hooks; `DestroyRef`, `afterRenderEffect`, `afterNextRender` |

### Part 4 — Services, DI and data

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 16 | `angular-services-dependency-injection` | new | `api.service`, `providedIn: 'root'`, `inject()` in 35 files |
| 17 | `angular-http-client` | new | `menu.service` — **`httpResource`**, and the `hasValue()` gotcha |
| 18 | `angular-interceptors` | new | `core/api.interceptor.ts` + its new spec |
| 19 | `angular-rxjs` | new | **the menu search** (added) — one worked example, six operators |

### Part 5 — Routing

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 20 | `angular-router` | new | `app.routes.ts`, `withComponentInputBinding` in `menu-page` |
| 21 | `angular-route-guards` | new | `authGuard`/`adminGuard`; **`confirmLeaveGuard`** (added); lazy `/admin` |

### Part 6 — Forms

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 22 | `angular-forms` | new | `login`, `register` — template-driven, deliberately |
| 23 | `angular-reactive-forms` | new | `checkout`, `profile`; `FormArray` in `admin-products` |

### Part 7 — Shipping it

| # | Slug | State | Source in the demo app |
|---|------|-------|------------------------|
| 24 | `angular-state-management` | new | signal services vs NgRx; `admin/store/` and the `NG0201` note |
| 25 | `angular-testing` | new | **the five new spec files** (added) + the Playwright suite |
| 26 | `angular-performance` | new | zoneless, `OnPush` everywhere, lazy chunks in the build output |
| 27 | `angular-build-deploy` | new | `ng build` output, budgets in `angular.json`, `environments/` |
| 28 | `angular-interview-questions` | new | — |

## Things already checked, so nobody re-checks them

- **`scss` was NOT a supported code language.** The app's styles are `styles.scss`, `_tokens.scss`
  and `theme.scss`, and every one would have silently normalised to `plaintext`. Fixed in both
  places, the same shape as the React track's `tsx` fix:
  `lovemesomecoding_backend/app/services/content.py` (added `"scss"` plus a `sass` → `scss` alias)
  and `lovemesomecoding_frontend/src/lib/content.ts` (`import 'prismjs/components/prism-scss'`).
  90 backend tests pass.
  ⚠️ **The deployed Lambda still has the old list.** Seeding runs the local service layer so what
  lands in S3 is correct, but editing one of these posts through `/admin` before
  `lovemesomecoding_backend/scripts/deploy.sh` runs would flatten its `scss` blocks to `plaintext`.
  Same trap the React track hit with `tsx`.
- Everything else the track needs is already supported: `typescript`, `html` (aliased to `markup`),
  `css`, `json`, `bash`.
- **The site nav already lists Angular** — `nav.ts:26`, in the `JavaScript` group. No nav edit.
- **`w3schools.com/angular/` is modern Angular, not AngularJS.** Checked 2026-08-20.
- **`GET /api/search/products?q=` already existed.** No backend change was needed for the search.

## Verification run on the app, 2026-08-20

| | |
|---|---|
| `npm run build` | clean; login chunk 3.23 kB, menu-page 12.69 kB |
| `npm test` (Vitest) | **23 passed** across 5 spec files |
| `npm run test:all` (Playwright) | **72 passed, 1 skipped, 0 failed** |

The skip is `payment.spec.ts`'s Stripe integration test, which needs `STRIPE_SECRET_KEY` — it skips
by design.

⚠️ One earlier Playwright run reported 2 failures (`admin.spec` topping, `payment.spec`) that did
not reproduce on two later runs and passed in isolation. It was started while the dev server was
still rebuilding after an edit. **If those two fail again, suspect leftover fixtures from an
interrupted run before suspecting the code** — the suite is serial against one database.

## Next steps

1. Re-base `manifest.START_DATE` so lesson 28 lands on the intended publish date.
2. Author `posts/`, running `check_content.py` as each lands. Snippets copied verbatim from the app.
3. Seed `--env local --write`, review at `:3000`.
4. Seed `--env prod --write --force-dates` (the flag is needed **once**, for `angular-component`),
   then `cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy`.
5. Deploy the backend so `/admin` edits do not flatten `scss` blocks.

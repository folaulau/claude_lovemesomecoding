# Angular tutorial track — progress report

**Status:** DRAFT COMPLETE — all 28 written, seeded locally and verified. Lessons 4–5 are LIVE on prod; the other 26 are not.
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
| `seed.py` / `check_content.py` / `check_snippets.py` | ✅ all three run clean |
| Content pipeline | ✅ `scss` support added (see below) |
| Demo app | ✅ built, and the four missing examples added |
| Post bodies | ✅ **28 of 28** written and rendering; **only 4 and 5 are on prod** |

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
| 7 | `angular-control-flow` | new | `menu-page.html`, `home.html` (`@else`), `cart-drawer.html` + `orders.html` (`@empty`) |
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

## Lesson 4 — `angular-component` (written 2026-08-20)

Written first, out of order, deliberately: it is the only indexed URL in the collection and the only
one currently empty, and settling the house style on it means 27 posts inherit a decided style
rather than setting one.

1081 words, 12 headings, 9 code blocks, all highlighted. Verified:

- `check_content.py` — round-trips byte-for-byte.
- **Snippets diffed against the app**, which `check_content.py` does NOT do: `main.ts`, `app.ts` and
  `index.html` match verbatim, and `spinner.ts` matches exactly once its teaching comment is
  stripped. Worth repeating for every post — the check proves the HTML is stable, not that a quote
  is still true.
- Rendered at `:3000`: 223 Prism token spans, all 12 headings anchored, Angular markup showing as
  literal `<app-greeting />` rather than being eaten.

Style settled here, for the rest of the track to follow:

- Escape code blocks **programmatically**, never by hand. One missed `&lt;` is invisible until it
  renders, and there are hundreds per post.
- `language-typescript` for `.ts`, `language-markup` for templates and HTML, `language-bash` for CLI.
- Open with a two-or-three-line invented example to make the idea concrete, then immediately show
  the real thing from the demo app. Lesson 5 of the React track does the same.
- Quote the app **verbatim**, minus its `ANGULAR CONCEPT:` teaching comments — those are the
  tutorial's job, and repeating them in the post says everything twice.
- Keep the React comparison to a sentence where it genuinely helps, not a running commentary.

### `seed.py --only`

Added while writing this. `seed.py` refuses to run while any file is missing — correct for
publishing, useless for drafting — so `--only <slugs>` seeds a subset for preview. It does not make
the track publishable.

## Lesson 5 — `angular-templates` (written 2026-08-21)

1210 words, 11 headings, 13 code blocks. Covers the four bindings as a set, then interpolation,
property vs **attribute** binding (including `[attr.x]="… : null"` removing the attribute),
class/style bindings with the `[style.width.%]` unit suffix, two-way, template reference variables,
`@let`, and the expression restrictions.

## `check_snippets.py` — the check that was missing

Written after lesson 5, because `check_content.py` proves a post's HTML round-trips and says
**nothing** about whether a quoted snippet is still true. A post can round-trip perfectly while
quoting a component that was refactored a month ago.

It searches every code block for a contiguous match in the demo app, ignoring indentation (fragments
are dedented when quoted) and ignoring comments (the house style quotes the app minus its
`ANGULAR CONCEPT:` blocks). Blocks matching nothing are reported as `illustrative` rather than
failing — many are three-line examples written for the lesson. It fails only on the drift signature:
the opening lines match somewhere but the whole block does not.

**It immediately caught two things I had got wrong**, neither of which any other check would have
found:

- Lesson 4 quoted `export class ProductCard { }` — an empty body the app does not have.
- Lesson 5 quoted the price `<span>` as a standalone line, when in the app it sits inside a
  `from …` wrapper.

Two design notes paid for while writing it:

- **The elision marker must be a line that is exactly `...`**, never the bare substring —
  `Math.min(...xs)` and every other spread operator would split a block in half.
- **A shared first line is not drift.** `import { Component } from '@angular/core';` opens half the
  app and every invented example alike; the threshold is three matching opening lines.

Current state: 15 blocks verbatim from the app, 6 illustrative — and all 6 are genuinely invented
(the `Greeting` component, the binding cheat-sheet, the `<img>` comparison, the `[(ngModel)]`
expansion, the old `@NgModule`).

## Correction: there is no `*ngIf` in the demo app

An early audit reported one surviving `*ngIf` in `app-navbar.html`. There is not. The match was
inside a COMMENT — "unlike the old `*ngIf` it needs no import" — and grep does not know the
difference. The app uses block control flow exclusively.

Consequence for lesson 7: the legacy syntax is shown as an illustrative block, clearly labelled as
what NOT to write, rather than quoted from the app. `check_snippets.py` classifies it correctly.

## Lessons 6–8 (written 2026-08-21)

| # | Slug | Words | Blocks | From the app | Illustrative |
|---|------|-------|--------|---|---|
| 6 | `angular-events` | ~900 | 7 | 7 | 0 |
| 7 | `angular-control-flow` | ~1100 | 9 | 6 | 3 |
| 8 | `angular-inputs-outputs` | ~1000 | 10 | 8 | 2 |

Every illustrative block is something the app deliberately does not contain — `@switch`, the aliased
`$index` form, the old `*ngIf`/`*ngFor`, and the two `model()` examples — so each is presented as an
example rather than as a quote. That distinction is the point of `check_snippets.py`.

Content notes worth keeping:

- Lesson 6 explains `$any($event.target).value` in the menu search rather than quietly using it. It
  is a real trade the app makes — `EventTarget` has no `value`, and the correct alternative is a
  narrowing handler in the class.
- Lesson 6 makes the `(ngSubmit)` vs `(submit)` point sharply: the latter reloads the page.
- Lesson 7 leads on `track` being **mandatory**, which is the biggest practical difference from
  `*ngFor` and the reason a whole family of performance complaints went away.
- Lesson 8 carries the `NG0950` warning from `pizza/CLAUDE.md` — a required input is not readable
  from a constructor.

## Lessons 9–12 (written 2026-08-21)

| # | Slug | Words | From the app | Illustrative |
|---|------|-------|---|---|
| 9 | `angular-content-projection` | 551 | 3 | 3 |
| 10 | `angular-directives` | 555 | 4 | 2 |
| 11 | `angular-pipes` | 680 | 4 | 1 |
| 12 | `angular-styles` | 730 | 6 | 0 |

Running total: **53 blocks verbatim from the app, 17 illustrative.**

Lesson 12 is the first to use `language-scss`, which makes it the end-to-end test of the pipeline
fix: it renders as `scss` with `$pizza-red` tokenised as a variable and `@use` as a keyword, not
flattened to `plaintext`. The fix works.

Content notes:

- Lesson 9 explains the two things that surprise people about projection: content is created in the
  CALLER's context, and it is created even when the slot is not rendered.
- Lesson 12 leads on the Sass-variable vs custom-property distinction, because it is the most
  useful idea in the app's stylesheet — build-time value versus runtime value — and carries the
  `:host { display: block }` chart bug from `pizza/CLAUDE.md`.
- Lesson 11 states plainly that the app uses `| async` zero times, and why: state is signals, so
  there is no subscription for it to manage.

## `check_snippets.py` scanned too little

It only looked at `src/`, so a block quoted from **`angular.json` was never verified** — it was
silently reported as `illustrative` instead. Now it scans the whole project (minus `node_modules`,
`dist`, `.angular`, build and report output).

The moment it did, it failed on that block: the post wrote `],` where `angular.json` has `]`, since
`styles` is the last key in `options`. A one-character error, invisible to every other check, in a
block presented as a quote. Fixed.

**Lesson: a checker's scope is part of the checker.** Silently classifying an unverifiable block as
"illustrative" is the failure mode to watch for — it looks like a pass.

## Lessons 13–15 — Part 3, reactivity (written 2026-08-21)

| # | Slug | Words | From the app | Illustrative |
|---|------|-------|---|---|
| 13 | `angular-signals` | 648 | 3 | 2 |
| 14 | `angular-computed-effect` | 856 | 6 | 0 |
| 15 | `angular-lifecycle` | 709 | 5 | 1 |

Running total: **67 blocks verbatim from the app, 20 illustrative.**

`cart.service.ts` carries this part almost single-handedly, and it is the best-commented file in the
app. The three ideas the lessons take from it:

- **Totals are derived, never stored.** One source of truth; a stored total is a second one that can
  disagree and eventually will.
- **`onCleanup` debounces the server write.** Clicking "+" three times is one PUT, not three,
  because each change cancels the pending timer.
- **The effect guards are plain fields, not signals** — `hydrationStarted`, `cartId`. Reading a
  signal inside an effect subscribes to it, so guarding on a signal and then setting it schedules a
  second run that has nothing to do. The file's own comments call this the equivalent of `useRef`.

Lesson 15's angle is that the app has **one `ngOnInit` across thirty components and no other hook at
all**, so the lesson is mostly about what replaced them: `computed` for `ngOnChanges`,
`afterNextRender` for `ngAfterViewInit`, `DestroyRef` for `ngOnDestroy`. The `DestroyRef` argument
worth keeping is that it can be injected in a plain function — `observedWidth` in `chart-size.ts`
puts the `ResizeObserver` setup and its `disconnect()` on adjacent lines, which is the leak that
pattern exists to prevent. It also carries the `NG0950` warning from `pizza/CLAUDE.md`.

## Lessons 16–19 — Part 4, services and data (written 2026-08-21)

| # | Slug | Words | From the app | Illustrative |
|---|------|-------|---|---|
| 16 | `angular-services-dependency-injection` | 810 | 5 | 2 |
| 17 | `angular-http-client` | 650 | 6 | 1 |
| 18 | `angular-interceptors` | 557 | 5 | 0 |
| 19 | `angular-rxjs` | 795 | 3 | 1 |

Running total: **86 blocks verbatim from the app, 24 illustrative.**

Lesson 19 is the payoff for adding the menu search: it is built entirely around that one pipeline,
naming the specific bug each operator prevents, and it closes by quoting the spec's
`expect(first.cancelled).toBe(true)` — the only direct evidence `switchMap` cancels, since
cancellation is invisible from the rendered output. Had the gap not been closed in the app, this
lesson would have been prose.

Other notes:

- Lesson 16 has no `InjectionToken` from the app because there isn't one, and says so: the app's
  only configuration is a build-time constant, so it is a plain import. A token buys runtime or
  test-time swapping — worth it when needed, ceremony when not.
- Lesson 17 leads with the two `fetch` differences that actually catch people: an observable is
  COLD (a discarded `get()` makes no request), and a non-2xx is an error rather than a response to
  inspect. It carries the `hasValue()` gotcha in full.
- Lesson 18 frames the `startsWith('/api/')` check as a security boundary rather than tidiness —
  an interceptor sees requests to every origin, so sending the bearer token to Stripe is one
  missing check away. The app's own spec asserts exactly that.

## Lessons 20–28 and 1–3 — the rest of the track (written 2026-08-21)

The track is now complete in draft. Lessons 1–3 were written **last, deliberately**: lesson 1 is the
track index, and its lesson list is **generated from `manifest.POSTS`** rather than typed, so it
cannot drift from the manifest. Verified: 28 links, correct order, none broken, none missing.

### Verification of the whole track

Every one of the 28 pages: HTTP 200, no `plaintext` code block, headings anchored, **4,210
highlighted tokens** in total. `check_content.py` reports *every code sample round-trips
byte-for-byte*; `check_snippets.py` reports **145 blocks verbatim from the demo app, 30
illustrative** — and every illustrative one is something the app deliberately does not contain.

Two more real errors the drift checker caught while finishing, neither findable any other way:

- Lesson 2 quoted `angularCompilerOptions` closing with `}` where `tsconfig.json` has `},`.
- Lesson 12 quoted the `styles` array closing with `],` where `angular.json` has `]`.

Both were one character, in blocks presented to readers as quotes.

### Deliberate shapes worth not "fixing"

- **`angular-interview-questions` has zero code blocks.** It is spoken answers, and adding snippets
  would work against what it is for.
- **`angular-get-started` has only two.** It is the index plus orientation.
- **Post length varies 590–1467 words.** Length follows the topic: templates genuinely is a bigger
  subject than forms-the-template-driven-kind. The README says keep posts to the point.

## Gotcha: a new post 404s until `next dev` restarts

`npm run dev` runs `sync-content.sh` **once, at startup**. Seeding a new post while the server is
running leaves it 404ing at `:3000` — the content is in S3 but not in the local `content/` tree, and
the dynamic route was generated without it. Restart the dev server after every `seed.py --only`.
Editing an existing post does not need this; adding one does.

## Next steps

1. **Read the drafts.** 26 of 28 have never been reviewed by a human.
2. Re-base `manifest.START_DATE` so lesson 28 lands on the intended publish date.
2. Author `posts/`, running `check_content.py` as each lands. Snippets copied verbatim from the app.
3. Seed `--env local --write`, review at `:3000`.
4. Seed `--env prod --write --force-dates` (the flag is needed **once**, for `angular-component`),
   then `cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy`.
5. Deploy the backend so `/admin` edits do not flatten `scss` blocks.

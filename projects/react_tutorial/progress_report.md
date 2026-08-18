# React tutorial track — progress report

**Status:** PUBLISHED — live on prod, 2026-08-17
**Started:** 2026-08-17
**Where it lands:** https://lovemesomecoding.com/react

---

## What this is

`/react` already holds **17 posts published in 2019**. They were copied from w3schools, teach
class components and `this.setState`, run 13–957 words, and still carry the WordPress
`boldgrid-section` wrapper divs. They are live and indexed.

This project rewrites all 17 **in place** — same slugs, so no URL is lost — as modern React 19
(function components, hooks, TypeScript) and adds 8 new posts for the topics that hooks-era React
needs and no existing slug covers.

**Result: a 27-post track** — a `react-get-started` landing page at the front and a `react-interview-questions` page at the end.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Existing 17 posts | Rewrite in place, keep every slug | They are indexed URLs. Rewriting keeps the ranking and kills the stale content in one move. |
| Track size | 27 posts (17 rewritten + 10 new) | Comparable to the Oracle track's 14; deep enough to be a real tutorial, finite enough to maintain. |
| Dates | Restamped to 2026-06-03 … 2026-08-17, 3 days apart | The old posts carried 2019 dates, which `upsert_post` never overwrites — hence `seed.py --force-dates`. Without it the pager reads in the wrong order. |
| Redux example | Redux Toolkit for the admin area only | Folau built it: four slices, `<Provider>` inside `AdminLayout`. Storefront keeps its four contexts, so `pizza/CLAUDE.md` still holds — and Redux lands in the lazy admin chunk. |
| Sass example | `theme.css` converted to `theme.scss` + `_tokens.scss` | Compiled output diffed against the original: identical bar Sass normalising `rgb()`, a computed `--pizza-red-dark`, and `prefers-reduced-motion` inverted to `no-preference`. |
| Snippet language | TypeScript | Copied verbatim from `pizza-react-frontend`, so every snippet is provably real, runnable code. |
| Example source | `pizza-react-frontend` | Per the README. Where the app lacks an example, add it to the app first, then snippet from it. |
| Seeding | Backend service layer, as `projects/oracle/seed.py` does | The static build reads only the derived indexes; reusing the admin API's own code is the only way to be sure indexes and posts agree. |

## Topic list

The order is the reading order. `date` ascends with the track so the prev/next pager reads
lesson 1 → lesson 27 (see `projects/oracle/README.md` for why).

### Part 1 — Getting started

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 1 | `react-get-started` | Get Started | **new** | the track index; versions table |
| 2 | `react-set-up` | Set Up a Project with Vite | rewrite | `package.json`, `vite.config.ts`, `index.html` |
| 3 | `react-es6` | The JavaScript You Need First | rewrite | destructuring, spread and `map`, all over the app |
| 4 | `react-render-html` | Rendering to the DOM | rewrite | `main.tsx` |

### Part 2 — Describing the UI

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 5 | `react-components` | Your First Component | rewrite | `Footer.tsx`, `ProductCard.tsx`, `App.tsx` |
| 6 | `react-jsx` | JSX | rewrite | `ProductCard`, `HomePage`, `LoginPage` |
| 7 | `react-props` | Props | rewrite | `ProductCard`, `ProtectedRoute` |
| 8 | `react-conditional-rendering` | Conditional Rendering | **new** | `ProtectedRoute`, `AppNavbar`, `CartDrawer` |
| 9 | `react-keys` | Rendering Lists and Keys | rewrite | `MenuPage`, `CartDrawer`, `PizzaBuilderModal` |

### Part 3 — Interactivity

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 10 | `react-events` | Handling Events | rewrite | `ProductCard`, `LoginPage`, `PizzaBuilderModal` |
| 11 | `react-state` | State with useState | rewrite | `PizzaBuilderModal`, `MenuPage`, `App` |
| 12 | `react-update-state` | Updating State Correctly | rewrite | `cartReducer`, `ToastContext` |
| 13 | `react-forms` | Forms and Controlled Inputs | rewrite | `LoginPage`, `PizzaBuilderModal` |

### Part 4 — Managing state

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 14 | `react-context` | Passing Data Deeply with Context | **new** | all four providers |
| 15 | `react-usereducer` | useReducer | **new** | `CartContext.tsx` |
| 16 | `react-custom-hooks` | Custom Hooks | **new** | `useCart`, `useAuth`, `useMenu`, `useToast` |
| 17 | `react-redux` | Redux, and Whether You Need It | rewrite | `store/` — four slices, `AdminLayout`, `AdminOrdersPage` |

### Part 5 — Escape hatches

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 18 | `react-lifecycle` | The Component Lifecycle with useEffect | rewrite | `MenuContext`, `CartContext` |
| 19 | `react-useref` | Refs | **new** | `PizzaBuilderModal`, `CartContext` |
| 20 | `react-error-boundary` | Error Boundaries | **new** | `ErrorBoundary.tsx`, `App.tsx` |

### Part 6 — Going to production

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 21 | `react-route` | Routing with React Router | rewrite | `App`, `ProtectedRoute`, `AdminLayout`, `MenuPage` |
| 22 | `react-usememo-usecallback` | useMemo, useCallback and memo | **new** | `MenuPage`, `CartContext`, `ProductCard` |
| 23 | `react-lazy-suspense` | Code Splitting with lazy and Suspense | **new** | `App.tsx` + real build output |
| 24 | `react-css` | Styling | rewrite | `theme.scss`, utility classes |
| 25 | `react-with-bootstrap` | Bootstrap | rewrite | `CartDrawer`, `PizzaBuilderModal`, `AppNavbar` |
| 26 | `react-sass` | Sass | rewrite | `_tokens.scss`, `theme.scss` |

### Part 7 — Interview prep

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 27 | `react-interview-questions` | Interview Questions | **new** | draws on the whole app + the real build output |

## Demo-app changes this required

Both gaps are closed; every one of the 26 posts now snippets from running code.

| Change | Owner | State |
|---|---|---|
| Redux Toolkit for `/admin` — `catalogSlice`, `ordersSlice`, `reportsSlice`, `usersSlice`, `apiFailure.ts`, `<Provider>` in `AdminLayout` | Folau | done, `npm run build` passes |
| `theme.css` → `theme.scss` + `_tokens.scss`, `sass` devDependency, import swapped in `main.tsx` | Claude | done, compiled output diffed against the original |

## Site changes this required

The track is written in TypeScript, and neither end of the pipeline knew those language names.

- `lovemesomecoding_backend/app/services/content.py` — added `typescript`, `jsx`, `tsx` to
  `SUPPORTED_LANGUAGES`. The `"ts": "javascript"` alias was deliberately **left alone**: it is what
  the 512 migrated posts used, and remapping it would change how they highlight on their next save.
- `lovemesomecoding_frontend/src/lib/content.ts` — static-imported `prism-typescript`,
  `prism-jsx`, `prism-tsx`. Order matters: `tsx` depends on the other two.

⚠️ **The backend Lambda has not been redeployed.** Seeding ran the local service layer, so what is
in S3 is correct — but until `lovemesomecoding_backend/scripts/deploy.sh` runs, editing one of these
posts through `/admin` would normalise its `tsx` blocks down to `plaintext` and silently lose the
highlighting.

## Files

```
projects/react_tutorial/
  README.md            the requirements
  progress_report.md   this file
  manifest.py          category metadata + one entry per post
  posts/NN-slug.html   post bodies, plain semantic HTML
  seed.py              writes the posts into a content tree
  check_content.py     proves the normaliser round-trips every code sample
```

## Task log

| Date | Task | Owner | Status |
|---|---|---|---|
| 2026-08-17 | Audit the 17 live posts, read react.dev + w3schools curricula | Claude | done |
| 2026-08-17 | Inventory `pizza-react-frontend` React feature coverage | Claude | done |
| 2026-08-17 | Agree scope, snippet language, fate of the old posts | Folau | done |
| 2026-08-17 | Topic list above | Claude | done |
| 2026-08-17 | Scaffold `manifest.py` / `seed.py` / `check_content.py` | Claude | in progress |
| | Author the 25 post bodies | Claude | not started |
| | Close the Redux and Sass example gaps in the pizza app | Claude | not started |
| | Run the pizza app + its Playwright suite, confirm nothing broke | Claude | not started |
| | `check_content.py`, then seed `--env local`, review at :3000 | Claude | not started |
| | Seed `--env prod --write`, deploy | Folau | not started |

# React tutorial track — progress report

**Status:** planning complete, authoring in progress
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

**Result: a 25-post track.**

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Existing 17 posts | Rewrite in place, keep every slug | They are indexed URLs. Rewriting keeps the ranking and kills the stale content in one move. |
| Track size | 25 posts (17 rewritten + 8 new) | Comparable to the Oracle track's 14; deep enough to be a real tutorial, finite enough to maintain. |
| Snippet language | TypeScript | Copied verbatim from `pizza-react-frontend`, so every snippet is provably real, runnable code. |
| Example source | `pizza-react-frontend` | Per the README. Where the app lacks an example, add it to the app first, then snippet from it. |
| Seeding | Backend service layer, as `projects/oracle/seed.py` does | The static build reads only the derived indexes; reusing the admin API's own code is the only way to be sure indexes and posts agree. |

## Topic list

The order is the reading order. `date` ascends with the track so the prev/next pager reads
lesson 1 → lesson 25 (see `projects/oracle/README.md` for why).

### Part 1 — Getting started

| # | Slug | Title | State | Pizza example |
|---|------|-------|-------|---------------|
| 1 | `react-set-up` | Set Up a React Project with Vite | rewrite (57w) | the app's own `package.json` / `vite.config.ts` |
| 2 | `react-es6` | The JavaScript You Need First | rewrite (346w) | destructuring, spread, `map`, modules — all over the app |
| 3 | `react-render-html` | Rendering to the DOM | rewrite (334w) | `main.tsx` — `createRoot`, `StrictMode` |

### Part 2 — Describing the UI

| # | Slug | Title | State | Pizza example |
|---|------|-------|-------|---------------|
| 4 | `react-components` | Your First Component | rewrite (434w) | `Footer.tsx`, `ProductCard.tsx` |
| 5 | `react-jsx` | JSX | rewrite (530w) | `HomePage.tsx` |
| 6 | `react-props` | Props | rewrite (372w) | `ProductCard.tsx`, `CartDrawer.tsx` |
| 7 | `react-conditional-rendering` | Conditional Rendering | **new** | `AppNavbar.tsx`, `ProtectedRoute.tsx` |
| 8 | `react-keys` | Rendering Lists and Keys | rewrite (194w) | `MenuPage.tsx`, `CartDrawer.tsx` |

### Part 3 — Interactivity

| # | Slug | Title | State | Pizza example |
|---|------|-------|-------|---------------|
| 9 | `react-events` | Handling Events | rewrite (416w) | `ProductCard.tsx`, `AppNavbar.tsx` |
| 10 | `react-state` | State with useState | rewrite (188w) | `PizzaBuilderModal.tsx` |
| 11 | `react-update-state` | Updating State Correctly | rewrite (88w) | `CartContext.tsx` reducer — objects and arrays |
| 12 | `react-forms` | Forms and Controlled Inputs | rewrite (302w) | `LoginPage.tsx`, `CheckoutPage.tsx` |

### Part 4 — Managing state

| # | Slug | Title | State | Pizza example |
|---|------|-------|-------|---------------|
| 13 | `react-context` | Passing Data Deeply with Context | **new** | `AuthContext.tsx`, `MenuContext.tsx` |
| 14 | `react-usereducer` | useReducer | **new** | `CartContext.tsx` |
| 15 | `react-custom-hooks` | Custom Hooks | **new** | `useCart`, `useAuth`, `useMenu`, `useToast` |
| 16 | `react-redux` | Redux — and Whether You Need It | rewrite (957w) | Context + `useReducer` as the alternative. **Gap: pizza has no Redux.** |

### Part 5 — Escape hatches

| # | Slug | Title | State | Pizza example |
|---|------|-------|-------|---------------|
| 17 | `react-lifecycle` | The Component Lifecycle with useEffect | rewrite (416w) | `MenuContext.tsx` — fetching, cleanup, deps |
| 18 | `react-useref` | Refs | **new** | `PizzaBuilderModal.tsx` |
| 19 | `react-error-boundary` | Error Boundaries | **new** | `ErrorBoundary.tsx` |

### Part 6 — Going to production

| # | Slug | Title | State | Pizza example |
|---|------|-------|-------|---------------|
| 20 | `react-route` | Routing with React Router | rewrite (38w) | `App.tsx`, `ProtectedRoute.tsx`, `AdminLayout.tsx` |
| 21 | `react-usememo-usecallback` | useMemo, useCallback and memo | **new** | `MenuPage.tsx`, `CartContext.tsx`, `ProductCard.tsx` |
| 22 | `react-lazy-suspense` | Code Splitting with lazy and Suspense | **new** | `App.tsx` — the admin bundle |
| 23 | `react-css` | Styling | rewrite (284w) | `theme.css`, `className` patterns |
| 24 | `react-with-bootstrap` | React with Bootstrap | rewrite (13w) | the whole app — `react-bootstrap` |
| 25 | `react-sass` | Sass | rewrite (41w) | **Gap: pizza uses plain CSS.** |

## Known gaps in the demo app

Two posts have no example in `pizza-react-frontend` yet. Per the README these need the app
extended first:

- **`react-redux`** — the app deliberately uses Context + `useReducer` (`pizza/CLAUDE.md` asks for
  a React context use case). Bolting Redux onto it would contradict that. Resolution pending.
- **`react-sass`** — the app styles with `bootstrap.min.css` + `src/styles/theme.css`, no Sass.
  Resolution pending.

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

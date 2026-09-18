# React tutorial track — progress report

**Status:** PUBLISHED — live on prod, 2026-08-17.
Lesson 27 (`react-project-structure`) added 2026-09-17, **seeded to local only — not yet on prod.**
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

**Result: a 28-post track** — a `react-get-started` landing page at the front and a `react-interview-questions` page at the end.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Existing 17 posts | Rewrite in place, keep every slug | They are indexed URLs. Rewriting keeps the ranking and kills the stale content in one move. |
| Track size | 28 posts (17 rewritten + 11 new) | Comparable to the Oracle track's 14; deep enough to be a real tutorial, finite enough to maintain. |
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
| 27 | `react-project-structure` | Project Structure for a Large App | **new** | the whole `src/` tree, measured — see below |

### Part 7 — Interview prep

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 28 | `react-interview-questions` | Interview Questions — 24 senior Q&A in 7 sections | **new** | draws on the whole app + the real build output |

## Lesson 27 — decisions

Added 2026-09-17 because `/react` had no post on how to organise a React codebase, which is the
question that dominates once an app is past a few dozen files.

| Decision | Choice | Why |
|---|---|---|
| Refactor the pizza app to feature folders? | **No** | It is a working app with Playwright suites, and 26 other posts cite its current file paths. Moving 43 files to illustrate one lesson would stale every one of them. |
| So how are the snippets real? | The pizza app is the honest **"before"** | Its type-based layout is shown exactly as it is, and the strain is *measured* rather than asserted. The feature-based layout is presented as a target with a file-by-file mapping table, clearly labelled as such. |
| Placement | Lesson **27**, dated `2026-08-19` | Between Sass (08-17) and Interview Questions (08-20), so architecture closes "Going to production" and interview prep stays last. Only the new post gets a date, so **no `--force-dates` was needed**. |
| Track wrap-up | Moved from `react-sass` to lesson 27 | Sass had the "That is the track" ending and is no longer the last content lesson. `26-react-sass.html` now ends with a plain Next link. |
| ESLint config in the post | Verified by running it | Built a throwaway project, wrote deliberate violations, confirmed all three rules fire. Two real bugs were caught this way — see below. |

### The measured evidence (re-derive with these, they are all in the post)

```bash
cd lovemesomecoding_demo_project/pizza/pizza-react-frontend
grep -rho "from '\(\.\./\)\+[^']*'" src | wc -l        # 99 parent-relative imports
grep -rho "from '\(\.\./\)\{2,\}[^']*'" src | wc -l    # 36 of them two or more levels
grep -rl "from '.*types'" src | wc -l                    # 23 of 43 files import types/index.ts
grep -rn "from '.*money'" src                            # 14 importers; 9 want only formatMoney
```

The `lib/money.ts` finding is the post's strongest argument and is a genuine structural bug in the
demo app: one module mixes `formatMoney` (generic) with `TAX_RATE` / `DELIVERY_FEE` /
`calculateTotals` (cart domain), so **all five admin screens depend on the delivery fee** purely
because they wanted a currency formatter. Left in place deliberately — it is the lesson.

### Two bugs the verification caught

Both were in the post's own ESLint snippet, and both would have shipped as advice that does not work:

1. The config imported `eslint-plugin-import` but never registered it in `plugins`, so
   `import/no-restricted-paths` fails with *"Definition not found"*.
2. **`import/no-restricted-paths` silently does nothing for aliased imports** unless
   `eslint-import-resolver-typescript` is configured. The rule works on *resolved* paths, and an
   unresolvable specifier is skipped rather than reported. Since the post recommends `@/` aliases two
   sections earlier, the rule as first written was a no-op against exactly the import style being
   taught. Proven both ways in a scratch project. This now has its own section in the post.

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
| 2026-08-17 | Scaffold `manifest.py` / `seed.py` (+ `--force-dates`) / `check_content.py` | Claude | done |
| 2026-08-17 | Teach both ends of the pipeline about `tsx` / `typescript` | Claude | done |
| 2026-08-17 | Convert the pizza theme to Sass (`_tokens.scss` + `theme.scss`) | Claude | done |
| 2026-08-17 | Add Redux Toolkit to the admin area — four slices, `<Provider>` in `AdminLayout` | Folau | done |
| 2026-08-17 | Add `react-get-started` at the front, restamp all dates | Claude | done |
| 2026-08-17 | Author 26 post bodies — 30,238 words, 266 code blocks | Claude | done |
| 2026-08-17 | `check_content.py` — every sample round-trips byte-for-byte | Claude | done |
| 2026-08-17 | Seed local, sync, build — `verify-build` 542/542 | Claude | done |
| 2026-08-17 | Seed prod `--force-dates --write`, `npm run deploy` — edge serving `394b0bd` | Claude | done |
| 2026-08-17 | Add `react-interview-questions` — 20 senior questions, 3,842 words | Claude | done |
| 2026-08-17 | Add a dedicated **Context** section — 4 new questions + the perf one moved in; 24 total, 4,852 words | Claude | done |
| 2026-08-17 | Re-seed prod + deploy — 569/569 posts, 27 in `/react` | Claude | done |
| 2026-09-17 | Add lesson 27 `react-project-structure`; renumber interview questions to 28 | Claude | done |
| 2026-09-17 | Move the track wrap-up out of `react-sass` and onto lesson 27 | Claude | done |
| 2026-09-17 | Verify the post's ESLint boundary config actually fires, in a throwaway project | Claude | done |
| 2026-09-17 | Seed local, screenshot, review | Claude | done |
| | Seed prod + `npm run deploy` for lesson 27 | Folau | **outstanding** |
| | Redeploy the backend Lambda so `/admin` edits keep `tsx` highlighting | Folau | **outstanding** |
| | Run the pizza Playwright suite against the Sass + Redux + `/interview-questions` changes | Folau | **outstanding** |

## Outstanding

0. **Lesson 27 is on local only.** `react-project-structure` is seeded to the `local` tree and
   reviewed at `:3000`. Prod still shows 27 posts. To publish:
   `seed.py --env prod --write` (no `--force-dates` — it is a new slug, nothing is being reordered),
   then `cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy`.
1. **Backend Lambda not redeployed.** Seeding ran the local service layer, so what is in S3 is
   correct — but until `lovemesomecoding_backend/scripts/deploy.sh` runs, editing one of these 27
   posts through `/admin` would normalise its `tsx` blocks down to `plaintext` and silently lose the
   highlighting. This is the only thing that can quietly undo the work.
2. **Pizza Playwright suite has not run** against the combined Sass, Redux and
   `/interview-questions` changes. `npm run build` and `npm run typecheck` both pass.

# React Native tutorial track — progress report

**Status:** ✅ **LIVE.** All 25 published, the rename is done, every old URL 301s. Deployed 2026-08-24 (build `394b0bd`).
**Started:** 2026-08-24
**Where it lands:** https://lovemesomecoding.com/react-native

---

## What this is

`/rea-native` — note the typo — holds **exactly five posts**, all published 2018-02-05, all
**placeholders**. The URLs are indexed; there is effectively nothing on them.

⚠️ They are **not literally empty**, and an early note in this file wrongly said they were — that
claim came from reading the wrong field (`body`, which does not exist; the content is in
`contentHtml`). Each carries WordPress `boldgrid-section` scaffolding, and between all five the real
content is two headings, one screenshot, a bare link to reactnavigation.org and the word "Co"
(wordCount 0–7). `retire_old.py` refuses to delete a non-empty body without `--allow-nonempty`,
which is what caught the error.

This project does two things at once:

1. **Renames the collection** `rea-native` → `react-native`, and the five `rea-native-*` post slugs
   to `react-native-*`, with a redirect for every old URL.
2. Builds a **25-lesson React Native track** in it — 20 new lessons plus those five, rewritten.

Every code sample comes from `lovemesomecoding_demo_project/pizza/pizza-react-native-mobile`, built 2026-08-24.

## Where it stands

| | |
|---|---|
| Topic table | ✅ 25 lessons, agreed |
| `manifest.py` | ✅ every lesson has slug, title, tags, excerpt, computed date and its demo-app sources |
| `check_content.py` | ✅ runs clean — manifest is consistent |
| `check_snippets.py` | ✅ runs clean — indexes 119 source files from the demo app |
| `seed.py` | ✅ runs, correctly refuses (no bodies yet) |
| `add_redirects.py` | ✅ runs, correctly refuses (destinations do not exist yet) |
| `retire_old.py` | ✅ runs, correctly refuses (replacements do not exist yet) |
| Demo app | ✅ built, 193 Jest + 31 Playwright tests green |
| Post bodies | ✅ **25 of 25** — 100 code blocks, all round-trip byte-for-byte |
| Snippet provenance | ✅ **88 blocks verified verbatim** against the demo app, 0 drift, 0 illustrative |
| Local seed | ✅ 25 posts + 6 redirects written to `lovemesomecoding/local/` |
| Local render | ✅ all 25 URLs return 200, TSX highlighting works, lesson index has 25 links |
| Prod | ✅ 25 posts live, `rea-native` retired, 63 redirects |
| Frontend edits | ✅ applied — the rename REMOVED two special cases rather than adding any |
| Deploy | ✅ build `394b0bd`, edge function republished (101 redirects, 6.7 KB of a 10 KB limit) |

## The demo app

`pizza-react-native-mobile`, finished 2026-08-24. Expo SDK 57, React Native 0.86, React 19,
TypeScript 6, expo-router, Context for state, Stripe PaymentSheet behind a platform-split module.
Customer flows only — there is no `/admin`, deliberately.

⚠️ **It has never been run on a simulator.** The machine it was built on has Xcode 15.4 and no
installed simulator runtime; RN 0.86 needs Xcode 16.1+. Everything was verified through Expo's web
target, Jest and the live API. Lessons that describe the native build (2, 19, 20, 25) are written
from the config and the docs, not from a device — worth a second look once it has run.

### Versions the track is written against

Read off the app, not chosen. If the app is upgraded, `manifest.VERSIONS` is the first edit.

| | |
|---|---|
| `expo` | 57.0 |
| `react-native` | 0.86 |
| `react` | 19.2 |
| `expo-router` | 57.0 |
| `typescript` | 6.0 |
| `@stripe/stripe-react-native` | 0.64 |
| `jest-expo` | 57.0 |
| `@testing-library/react-native` | 14.0 |
| `node` | 22 |
| `xcode` | 16.1+ (React Native 0.86's minimum) |

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Category slug | **Rename `rea-native` → `react-native`** | Folau's call. The nav already *labelled* it "React Native"; only the slug carried the typo. |
| The five 2018 posts | **Rewritten as lessons 1, 3, 5, 11, 24** at new slugs | Folau's call. Their titles — Introduction, Core Components, Flexbox, Navigation, Internals — map onto the track's natural shape. Same precedent as `angular-component`. |
| Old URLs | **Redirected, never dropped** | Six entries, derived from `manifest.OLD_SLUG_REDIRECTS` so the map cannot drift from the track. |
| Slugs, not in-place edits | **New slugs + delete the originals** | A post's slug IS its URL and its identity, and the category is stored on the post. There is no rename operation; create-then-retire is the only safe order. |
| Track size | 25 lessons | Folau chose ~25. Comparable to React's 27 and Angular's 28. |
| Snippet languages | `tsx`, `typescript`, `json` | **No pipeline change needed** — unlike the Angular track, which had to teach the normaliser `scss`. `tsx`/`jsx` were already in `SUPPORTED_LANGUAGES` and already imported in the frontend's Prism bundle. |
| Dates | **Computed** from `START_DATE` + `STEP_DAYS` | Back-dated so lesson 25 lands 2026-08-21 rather than publishing into the future. Re-basing is a one-line edit. |
| Seeding | Backend service layer, as the React and Angular tracks do | The static build reads only the derived indexes; reusing the admin API's own code is the only way to be sure indexes and posts agree. |
| Source material | reactnative.dev + tutorialspoint | Per the README. |

## Topic list

25 lessons in reading order. **rewrite** means the lesson replaces one of the five 2018 posts and
its old URL redirects here.

| # | Slug | Title | | Quoted from |
|---|---|---|---|---|
| 1 | `react-native-introduction` | Introduction | **rewrite** | `README.md`<br>`package.json` |
| 2 | `react-native-set-up` | Set Up a Project with Expo |  | `package.json`<br>`app.config.ts`<br>`tsconfig.json` |
| 3 | `react-native-core-components` | Core Components | **rewrite** | `src/components/ui/Text.tsx`<br>`src/components/ui/Button.tsx`<br>`src/components/ui/Card.tsx` |
| 4 | `react-native-styling` | Styling and a Design System |  | `src/theme/tokens.ts`<br>`src/theme/theme.ts`<br>`src/components/ui/Text.tsx` |
| 5 | `react-native-flexbox` | Flexbox and Layout | **rewrite** | `src/features/menu/components/ProductCard.tsx`<br>`src/features/menu/components/PizzaBuilderSheet.tsx` |
| 6 | `react-native-safe-area` | Safe Areas, Notches and the Keyboard |  | `src/components/ui/Screen.tsx`<br>`src/components/ui/Sheet.tsx` |
| 7 | `react-native-lists` | Lists with FlatList |  | `src/features/menu/screens/MenuScreen.tsx`<br>`src/features/orders/screens/OrdersScreen.tsx` |
| 8 | `react-native-forms` | TextInput and Forms |  | `src/components/ui/TextField.tsx`<br>`src/features/checkout/hooks/useCheckoutForm.ts`<br>`src/features/auth/screens/LoginScreen.tsx` |
| 9 | `react-native-modals` | Modals, Sheets and Overlays |  | `src/components/ui/Sheet.tsx`<br>`src/features/cart/components/CartSheet.tsx`<br>`src/providers/ToastProvider.tsx` |
| 10 | `react-native-animations` | Animations and the Native Driver |  | `src/providers/ToastProvider.tsx` |
| 11 | `react-native-navigation` | Navigation | **rewrite** | `app/_layout.tsx`<br>`app/(tabs)/_layout.tsx`<br>`app/(tabs)/index.tsx`<br>`app/order/[orderId].tsx` |
| 12 | `react-native-deep-linking` | Deep Linking and the URL as State |  | `app.config.ts`<br>`src/features/menu/screens/MenuScreen.tsx` |
| 13 | `react-native-project-structure` | Structuring a Real App |  | `tsconfig.json`<br>`src/types/index.ts`<br>`src/api/index.ts` |
| 14 | `react-native-state-management` | State: Context, Reducers and Custom Hooks |  | `src/features/cart/state/cartReducer.ts`<br>`src/features/cart/state/CartProvider.tsx`<br>`src/providers/AppProviders.tsx` |
| 15 | `react-native-data-fetching` | Talking to an API |  | `src/api/client.ts`<br>`src/api/config.ts`<br>`src/features/menu/state/MenuProvider.tsx` |
| 16 | `react-native-storage` | Storing Data on the Device |  | `src/storage/secureStorage.ts`<br>`src/storage/deviceStorage.ts`<br>`src/storage/index.ts` |
| 17 | `react-native-platform-apis` | Platform APIs and Device Differences |  | `src/storage/secureStorage.ts`<br>`src/features/cart/state/CartProvider.tsx`<br>`src/features/profile/screens/ProfileScreen.tsx` |
| 18 | `react-native-native-modules` | Native Modules and Config Plugins |  | `app.config.ts`<br>`src/features/checkout/payment/index.ts`<br>`src/features/checkout/payment/paymentGateway.web.tsx` |
| 19 | `react-native-payments` | Taking Payments with Stripe |  | `src/features/checkout/payment/paymentGateway.tsx`<br>`src/features/checkout/screens/CheckoutScreen.tsx` |
| 20 | `react-native-accessibility` | Accessibility |  | `src/components/ui/Button.tsx`<br>`src/components/ui/SegmentedControl.tsx`<br>`src/components/ui/StateViews.tsx` |
| 21 | `react-native-performance` | Performance |  | `src/features/menu/components/ProductCard.tsx`<br>`src/features/menu/screens/MenuScreen.tsx` |
| 22 | `react-native-error-handling` | Error Boundaries and Failure States |  | `src/components/RouteErrorBoundary.tsx`<br>`src/api/apiError.ts`<br>`src/components/ui/StateViews.tsx` |
| 23 | `react-native-testing` | Testing |  | `jest.setup.ts`<br>`src/features/cart/state/__tests__/cartReducer.test.ts`<br>`src/features/cart/state/__tests__/CartProvider.test.tsx` |
| 24 | `react-native-internals` | Internals: Hermes, JSI and the New Architecture | **rewrite** | `app.config.ts`<br>`package.json` |
| 25 | `react-native-build-deploy` | Building and Releasing to the App Stores |  | `app.config.ts`<br>`package.json` |

### What was deliberately left out

| Not covered | Why |
|---|---|
| Camera, permissions, push notifications, maps | The demo app uses none of them. A lesson with invented snippets is exactly what `check_snippets.py` exists to catch, and the README says examples come from the app. |
| Redux / Zustand | The app uses Context, because the thing that justified Redux in `pizza-react-frontend` (`/admin`) is absent here. Lesson 14 covers when you would reach for a store. |
| Reanimated / Gesture Handler in depth | The app animates with the `Animated` API. Lesson 10 names where Reanimated takes over rather than pretending to teach it. |
| A standalone debugging lesson | Thin from the app. Folded into lessons 22 (error handling) and 23 (testing). |
| Interview questions | React and Angular both close with one. Worth adding as a 26th later; not in the 25 Folau asked for. |

---

## The rename runbook

⚠️ **ORDER MATTERS.** Each step assumes the one before it. Nothing here has been run against prod.

```
1. write the 25 post bodies                       posts/NN-*.html
2. lovemesomecoding_backend/.venv/bin/python projects/react_native/check_content.py
3. python3 projects/react_native/check_snippets.py
4. seed.py        --env local --write             creates /react-native + 25 posts
5. add_redirects.py --env local --write           6 entries into redirects.json
6. review at :3000
7. seed.py        --env prod  --write
8. add_redirects.py --env prod  --write
9. APPLY THE FRONTEND EDITS BELOW
10. cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy
11. retire_old.py --env prod --write              deletes the 5 originals + old category
12. deploy again                                  so the archive count and nav are right
```

Steps 9–10 must land **before** step 11. Delete first and the old URLs 404 in the gap.

### Frontend edits — staged, not applied

These are correct only **after** the category exists as `react-native`. Applied today they would
point `/react-native-table-of-content` at `/` and drop React Native out of the nav, so they are
written down rather than made.

The rename **removes** two special cases rather than adding any:

| File | Change |
|---|---|
| `src/lib/nav.ts` | in the `JavaScript` group, `'rea-native'` → `'react-native'` |
| `src/lib/nav.ts` | delete the `'rea-native': 'React Native'` entry from `DISPLAY_NAMES` — the category's own name is now correct |
| `src/lib/pages.ts` | delete `'react-native-table-of-content': 'rea-native'` from `TOC_CATEGORY_OVERRIDES` — the mechanical rule now yields the right slug |
| `scripts/postbuild.mjs` | delete the same entry from `TOC_OVERRIDES`. `verify-build.mjs` asserts these two mirror each other, so they change together |

⚠️ **Republish the CloudFront function.** The redirect map is compiled into the edge function, so a
redirect added to `redirects.json` does nothing at the edge until it is republished. `deploy.sh`
does this; a manual `aws s3 sync` does not.

---

## Gotchas paid for while scaffolding

- ⚠️ **`S3Repository.get_json` does NOT prepend the tree prefix.** `get_json("redirects.json")`
  reads a key that does not exist and returns `None`. `add_redirects.py` would then have written a
  fresh six-entry map over the **fifty-seven** already on prod. Caught by noticing the dry run said
  "0 redirect(s) already recorded" when prod's file is 3.7 KB. The helper now builds the full key
  and says so in a comment.
- **A redirect to a destination that does not exist is worse than no redirect** — it turns one 404
  into a redirect to a 404, which nobody notices. `add_redirects.py` refuses unless every target
  post exists in the same tree.
- **`content/` is gitignored.** `redirects.json` is CONTENT, in S3, not a file in the frontend repo.
  Editing the repo would have changed nothing.
- **`package-lock.json` was being indexed** by `check_snippets.py` — half a megabyte of noise no
  post will ever quote. Excluded, along with `ios/` and `android/`, which `expo prebuild` generates.
- **The five originals cannot be re-dated into the track.** `upsert_post` never overwrites an
  existing `date`, and these carry 2018 timestamps. Since they are being replaced by new slugs
  rather than reused, this stops mattering — but it is why the track does not simply keep them.

### Found while publishing

- ⚠️ **The five old posts were NOT empty, and I said they were.** That claim came from reading
  `body` and `content` on the post JSON — neither field exists; the content is in `contentHtml`.
  `retire_old.py`'s own guard caught it and refused to delete. Reading them showed WordPress
  scaffolding around two headings, a May-2020 Hacker News hiring chart, a bare link and the word
  "Co" — placeholders, as assumed, but the assumption was verified only because the guard forced it.
  Deletion then needed the explicit `--allow-nonempty`.
- **`delete_category` leaves `index/by-category/<slug>.json` behind** as an empty array. Nothing
  renders it, so it is litter rather than a bug — but it survives `aws s3 sync --delete` into every
  content checkout. `retire_old.py` now removes it.
- **`list_posts()` and `index/posts.json` count different things.** The index holds 815 entries: 575
  marked `published` and 240 legacy migrated posts with no `status` field at all. Comparing the two
  numbers looks like data loss and is not — `verify-build.mjs`'s 43/43 cross-check is the invariant
  that actually matters.
- **`deploy.sh` republishes the CloudFront Function BEFORE uploading to S3.** That ordering is what
  makes retire-then-deploy safe: the redirects are live at the edge before the old pages leave the
  origin, so there is no window where an indexed URL 404s.

### Found while writing the posts

- ⚠️ **The snippet checker's comment stripper ate its own haystack.** An unanchored
  `/\*.*?\*/` also matches the `/*` inside the STRING `"@/*": ["./src/*"]` in `tsconfig.json`, then
  runs forward to the next real `*/` — swallowing the whole `paths` block out of the source being
  searched. The symptom is a snippet quoted verbatim from the app reported as `illustrative`, which
  reads as "you invented this example" rather than "the tool broke". Every block comment in the
  codebase begins its own line, so the patterns are now anchored with `^[ \t]*`. Two blocks were
  being mis-reported before the fix.
- **`package-lock.json` in the search index** made every run slow for no reason; excluded along with
  the `expo prebuild` output.

## What the writing produced

25 posts, 750–1000 words each, 100 code blocks. **88 of those blocks are verbatim from the demo
app** and verified by `check_snippets.py`; the rest are shell commands and folder trees, which that
checker deliberately ignores.

One lesson is prose-only by design. `react-native-internals` explains Hermes, JSI, Fabric and the
two threads — none of which any application file demonstrates, so its `sources` list is empty and
`check_content.py` reports that as a note rather than quoting `app.config.ts` as decoration.

### Verified locally

```
seed.py --env local --write          25 created, category count 25, archive newest-first correct
add_redirects.py --env local --write 56 -> 62 redirects
frontend at :3000                    all 25 URLs 200; Prism tokens present in tsx blocks;
                                     heading anchors generated; lesson index resolves 25 links
```

## Verified live

```
25/25   post URLs return 200 on https://lovemesomecoding.com/react-native/*
6/6     old URLs 301 to their replacement (/rea-native and the five posts)
1       /react-native-table-of-content -> /react-native  (now resolves mechanically)
25      sitemap entries; 0 references to rea-native anywhere
0       stray rea-native links in the nav
43/43   category counts agree; 815/815 posts served
```

## Still open

- ⚠️ **Two `frontend-dev` posts still link to `/rea-native`** —
  `frontend-dev-get-started` and `frontend-dev-what-is-a-frontend-engineer`. They resolve via the
  301, so nothing is broken, but they take an unnecessary hop. The fix belongs in
  `projects/frontend_dev`'s own post sources, not in the content DB, or the next seed of that track
  reverts it.
- The demo app has still never run on a simulator, which slightly weakens lessons 2, 19, 20 and 25 —
  they describe the native build from config and documentation rather than from a device.
- A 26th "interview questions" lesson, matching the React and Angular tracks, is worth considering.
- Submit the updated sitemap to Search Console so the five renamed URLs are recrawled promptly.

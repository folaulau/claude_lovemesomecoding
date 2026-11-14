# Android tutorial track — progress report

**Status:** ✅ **WRITTEN, seeded to LOCAL, built and verified. NOT published to prod** — waiting on
Folau's review (step 8).
**Started / last updated:** 2026-10-10
**Will land at:** https://lovemesomecoding.com/android, under the **Mobile** nav dropdown next to iOS

---

## What this is

The Android mirror of the 22-lesson iOS track (`projects/ios_tutorial/`). Kotlin and Jetpack
Compose, every code block quoted from a demo app that builds and has tests behind it.

## Decisions (Folau, 2026-10-10)

| Question | Answer |
|---|---|
| Where do the examples come from? | **Build `pizza-android-mobile` first**, then write lessons quoting it — same bar as iOS. |
| How closely to mirror iOS? | **Mirror, but adapt to Android** — same backbone and order; swap/merge where Android differs. |
| DI | **Hilt.** The DI lesson contrasts it with the iOS app's hand-written composition root. |

## Plan and owners

| # | Step | Owner | Status |
|---|---|---|---|
| 1 | Build `lovemesomecoding_demo_project/pizza/pizza-android-mobile` (Kotlin, Compose, Hilt), port of `pizza-ios-mobile`, same API | Claude | ✅ 71 files |
| 2 | Unit tests (JVM) for reducer, pricing, validator, HTTP client, view models | Claude | ✅ 104/104 |
| 3 | Run it on the API 35 emulator against the live backend, screenshot | Claude | ✅ |
| 4 | `manifest.py`, `seed.py`, `check_content.py`, `check_snippets.py` (adapted from iOS) + `build_posts.py` | Claude | ✅ |
| 5 | Write the lessons | Claude | ✅ 23/23 |
| 6 | Nav: add `android` to the Mobile group in `lovemesomecoding_frontend/src/lib/nav.ts` | Claude | ✅ (uncommitted) |
| 7 | Seed **local**, `npm run build` + verify-build | Claude | ✅ |
| 8 | Review the content, then seed prod + deploy | **Folau** | ⏳ |

## Pipeline prerequisites (checked 2026-10-10)

- `kotlin` is already in `SUPPORTED_LANGUAGES` (backend) and `prism-kotlin` is already imported
  (frontend) — no language registration needed, unlike the iOS track's Swift.
- `xml` → `markup` and `properties` already exist (AndroidManifest, gradle.properties).
- TOML (`libs.versions.toml`): not registered — TBD whether to add or label as `properties`.

## Toolchain on this machine (2026-10-10)

- Android SDK at `~/Library/Android/sdk`: platforms 34 + 35, build-tools 35.0.0, emulator, an API 35
  `google_apis_playstore` image. **No Android Studio, no cmdline-tools.**
- JDK 17 / 21 / 25 (Corretto), Gradle 8.12 on PATH.
- Current stable versions (read from Google Maven / Maven Central 2026-10-10): AGP 9.4.1,
  Kotlin 2.4.21, Compose BOM 2026.09.00, Hilt 2.60.1, Navigation 2.10.2, Lifecycle 2.11.0,
  Activity 1.13.0, DataStore 1.2.1, Stripe Android 23.22.0, Retrofit 3.0.0, OkHttp 5.5.0,
  kotlinx.serialization 1.11.0, coroutines 1.11.0, Turbine 1.2.1, Robolectric 4.17.

## Proposed lesson plan (iOS → Android)

| # | Android lesson | Mirrors iOS | Android-specific angle |
|---|---|---|---|
| 1 | android-get-started | ios-get-started | Android Studio, modules, Gradle + version catalog, emulator, `10.0.2.2` |
| 2 | android-kotlin-essentials | ios-swift-essentials | null safety, data/sealed classes, extension fns, lambdas, scope functions |
| 3 | android-compose-layout | ios-swiftui-views-and-layout | composables, modifier order, Row/Column/Box |
| 4 | android-compose-state | ios-state-and-observable | remember/rememberSaveable, hoisting, StateFlow → collectAsStateWithLifecycle |
| 5 | android-viewmodel-and-process-death | (new) | ViewModel scope, config changes, `SavedStateHandle`, process death |
| 6 | android-navigation | ios-navigation | type-safe Navigation Compose routes, bottom bar, back stack per tab |
| 7 | android-lists-and-performance | ios-lists-and-performance | LazyColumn/Grid, keys, contentType, stability |
| 8 | android-forms-and-input | ios-forms-and-input | TextField, KeyboardOptions/IME actions, focus, validation outside the UI |
| 9 | android-bottom-sheets-and-dialogs | ios-sheets-and-modals | ModalBottomSheet, AlertDialog, one sheet state |
| 10 | android-design-system | ios-design-system | Material 3 theme, tokens → semantic → components |
| 11 | android-networking | ios-networking | Retrofit + OkHttp + kotlinx.serialization, interceptors, config via BuildConfig |
| 12 | android-error-handling | ios-error-handling | sealed ApiError, UiState, ActionOutcome |
| 13 | android-coroutines-and-flow | ios-concurrency | viewModelScope, Flow/StateFlow, dispatchers, cancellation, debounce |
| 14 | android-app-architecture | ios-app-architecture | layers, repositories, the cart reducer, UDF |
| 15 | android-dependency-injection-hilt | ios-dependency-injection | Hilt modules, scopes, test replacement |
| 16 | android-persistence-and-keystore | ios-persistence-and-keychain | DataStore, Android Keystore-encrypted token |
| 17 | android-app-lifecycle | ios-app-lifecycle | Activity lifecycle, ProcessLifecycleOwner background flush, launch gate |
| 18 | android-payments | ios-payments | Stripe PaymentSheet for Android |
| 19 | android-accessibility | ios-accessibility | semantics, TalkBack, mergeDescendants, 48dp targets |
| 20 | android-testing | ios-testing | JUnit, MockWebServer, coroutines-test, Turbine, Compose UI tests |
| 21 | android-previews-and-tooling | ios-previews-and-tooling | @Preview, Lint, ktlint/detekt, Profiler |
| 22 | android-build-and-ship | ios-build-and-ship | build types, R8, signing, App Bundle, Play Console, CI |
| 23 | android-interview-questions | ios-interview-questions | answered against the lessons before it |

---

## Log

### 2026-10-10
- Requirements clarified (table above). Project folder created.
- Surveyed `pizza-ios-mobile` (78 Swift files): the Android app ports its architecture —
  `Core` / `Domain` / `Data` / `Features` / `App`, pure `CartReducer`, `ViewState`, `ActionOutcome`,
  server-side cart with debounced PUT + background flush, order-then-pay with Stripe, payment-status
  polling.

- Demo app built, tested (104/104, three rules mutation-checked), lint clean, release + R8 verified
  by running a minified build on the emulator, signed bundle verified with a throwaway key, driven
  end to end against the live backend (guest order PAID, confirmed in MySQL; process death
  recovered). Details in `lovemesomecoding_demo_project/pizza/progress_report.md`.
- Added during lesson writing: autofill `ContentType`s on every form field (lesson 8 needed them to
  exist before describing them), release signing from env/local.properties, `lint { warningsAsErrors }`,
  `.editorconfig`, `pizza/.github/workflows/android.yml` (never run — no remote, same as ios.yml).

## How the posts are written — `build_posts.py`

Lessons are authored in `src/NN-slug.src.html`. Code fences are `@@lang … @@`, and a line
`<<K/path.kt | START | END | nc>>` inside one is replaced by the real lines from the app — so a quote
is exact the moment it is written. `posts/*.html` is GENERATED; edit `src/`, then
`python build_posts.py && python check_content.py && python check_snippets.py`.

Gotchas paid for while building it:
- A START that matches inside a KDoc (`@Parcelize`, `@Stable` are mentioned in prose comments) starts
  the quote mid-comment and is reported as drift. Starts now skip comment lines.
- END/START are literal substrings unless anchored with `^`/`$` — `PizzaButton(text = …` broke a regex.
- Never close a truncated quote with a hand-typed `}`; end it with `// …` (same rule as iOS).
- First drafts land 50–250 words under the 1,760 floor. Budget an extra section.
- TOML is authored `language-ini` (aliased to `properties` by the backend) — no pipeline change needed.

## Verified — 2026-10-10

- ✅ `check_content.py`: **all 23 pass.** 1,762–1,999 words each (8–9 reading-minutes), prose 65–93%
  against the 42% floor. The only warning left was the nav, now fixed.
- ✅ `check_snippets.py`: **no drift. 249 of 251 checked blocks (99%) quoted from code that runs**;
  the 2 others are deliberate illustrations; 4 "wrong way" blocks excluded. Includes the two Swift
  contrast quotes from the iOS app — `.swift` was added to the checker so they are verified too.
- ✅ Seeded **local**: 873 → 896 posts, category `android` count 23, newest `android-interview-questions`.
- ✅ `npm run build` → verify-build: **896/896 posts served, 48/48 category counts agree**, 1,138 HTML
  files. 238 `language-kotlin` blocks with 10,294 Prism token spans; 6 plaintext blocks are the
  intended directory trees and error messages. 23 sitemap entries. Pager walks lesson 1 → 23. Nav data
  order: Mobile → iOS, Android.
- ✅ **Viewed rendered** (headless Chrome against `npm run preview`; the Chrome extension was not
  connected): the category page and lesson 13 render with highlighting and the sidebar.

## Things writing the lessons found in the APP (all fixed, all re-verified on the emulator)

Writing about the code is a review of the code. These were real:
1. **Orders tab never refreshed** after an order was placed in another tab (its ViewModel survives a
   tab switch). Fixed with `LifecycleResumeEffect` + cancel-and-replace loading — lesson 17 quotes it.
2. **…and then the new order was still invisible**: a keyed `LazyColumn` anchors scroll to the first
   visible key, so an order inserted above lands off-screen. Fixed by scrolling to top only if already
   there — lesson 7 quotes it. Verified: order created via API behind the app's back appears first.
3. **"Unavailable" price label at 2.3:1 contrast** (WCAG text needs 4.5:1). Measured every palette
   pairing; switched to the 5.1:1 muted grey — lesson 19 states the measured numbers.
4. **Autofill**: no field told autofill services what it held. Added `ContentType`s — lesson 8.
5. **Flaky lint**: `lintAnalyzeDebugUnitTest` failed on the first build after any test change
   ("bug in lint", reading a Hilt KSP file mid-regeneration). `lint { ignoreTestSources = true }`;
   three consecutive post-change runs clean — lesson 21 tells the story.
6. **Checker blind spot**: a `//` comment containing `/api/me/**` opened a block comment for the
   snippet checker (not for Kotlin), hiding real code from it. Comment reworded.

## Test data left behind (local MySQL, pizza-mysql container)
- Guest order "Guest Android" (5bbdb133…, PAID). Customer orders "Resume Check" (42d0fd81…) and
  "Resume Check 2" (a66b06ee…), both PENDING_PAYMENT, for `customer@pizza.test`. Guest server cart
  6bf4202a… holds one Pepsi. Orders have no delete API.

## Still open
- **Review the content (Folau).** Checked mechanically and read once while writing; not reviewed by
  a second person.
- **Publish to prod (Folau's call):** `AWS_PROFILE=folau python projects/android_tutorial/seed.py --env prod --write`,
  then `AWS_PROFILE=folau npm run deploy` in the frontend (needs the nav.ts change committed/deployed).
  No backend deploy needed — `kotlin` and the `ini`/`xml` aliases are already live.
- **Nothing is committed** — three repos have changes: `lovemesomecoding_frontend` (nav.ts),
  `lovemesomecoding_demo_project` (pizza-android-mobile, android.yml, pizza CLAUDE.md/progress_report),
  `claude_lovemesomecoding` (projects/android_tutorial).
- `pizza/.github/workflows/android.yml` has never run (no remote) — same as ios.yml.
- The demo app has no baseline profile and no ktlint/detekt enforcement in CI — both named as next
  steps in lessons 21–22 rather than claimed.

## Live — 2026-10-10

- Prod seed: 23 posts created, prod tree 954 → 977 posts, `/android` category count 23.
- Frontend deploy: verify-build 977/977 posts, 47/47 categories; edge serves build `c0ff134`
  (source zip `c0ff134-dirty` — `nav.ts` deployed from the working tree, not yet committed).
- Checked live: `/android` and sampled lessons return 200, the Mobile nav shows Android, Kotlin
  blocks render highlighted.
- Still open: commits in three repos (none made). **Commit frontend `nav.ts` before the next push to
  `main`** — the GitHub Actions deploy builds from the commit and would drop the Android nav link.

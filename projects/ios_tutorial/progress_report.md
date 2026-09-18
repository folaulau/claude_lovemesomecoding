# iOS tutorial track — progress report

**Status:** ✅ **Seeded to `local` and verified.** 22 lessons written, both checkers green, site builds.
**NOT published to prod.** That is a separate, deliberate step — see "Still open".
**Started / last updated:** 2026-09-18
**Where it will land:** https://lovemesomecoding.com/ios, under a new **Mobile** nav dropdown

---

## What this is

A 22-lesson native iOS track — Swift and SwiftUI — built entirely from
`lovemesomecoding_demo_project/pizza/pizza-ios-mobile`, the SwiftUI app written and run earlier the
same week. Every code block is quoted from source that compiles and has tests behind it.

It also required two pieces of infrastructure that did not exist:

1. A **Mobile** top-level nav group, between "Software Engineering" and "JavaScript".
2. **Swift registered with Prism**, on both halves of the pipeline.

---

## The two frontend/backend changes

### Nav — `lovemesomecoding_frontend/src/lib/nav.ts` (committed)

A new group rather than a slot in an existing one: iOS is not JavaScript and it is not general
software engineering, and a reader looking for mobile should not have to guess.

`react-native` deliberately **stays** under JavaScript. It would read well under Mobile too, but
moving an existing category is a separate decision from adding a new one. Folau's call.

`navTree()` drops a group whose categories do not exist, so the nav change was safe to land before
the content — Mobile simply stayed invisible until there was something to link to.

### Swift grammar — lockstep on both sides

⚠️ **This was a real gap, not a regression guard.** `swift` was in neither
`lovemesomecoding_backend/app/services/content.py` (`SUPPORTED_LANGUAGES`) nor
`lovemesomecoding_frontend/src/lib/content.ts` (the Prism imports). Without both, **all 22 lessons
would have shipped as plaintext, silently** — an unsupported language is normalised, never rejected.

Two aliases were added alongside it: `xcconfig` → `properties` (an .xcconfig is key=value, which
Prism already highlights) and `plist` → `markup`.

⚠️ **The backend change is NOT committed.** `app/services/content.py` already had ~50 lines of
uncommitted changes from earlier tracks when this session started, so the `swift` addition is mixed
in with somebody else's pending work and cannot be isolated into its own commit. The frontend half
IS committed.

---

## The track

| # | Slug | Topic |
|---|---|---|
| 1 | ios-get-started | Xcode, targets/schemes/configs, the .xcodeproj problem |
| 2 | ios-swift-essentials | value types, optionals, enums, protocols, closures, errors |
| 3 | ios-swiftui-views-and-layout | a View is a value; layout negotiation; modifier order |
| 4 | ios-state-and-observable | @State/@Binding/@Observable/@Environment, and the rule |
| 5 | ios-navigation | typed routes, a stack per tab, programmatic navigation |
| 6 | ios-lists-and-performance | List vs LazyVStack vs LazyVGrid, identity, what replaced memo |
| 7 | ios-forms-and-input | the keyboard as UI, @FocusState, validation outside the view |
| 8 | ios-sheets-and-modals | sheet(item:) vs isPresented, detents, alerts |
| 9 | ios-design-system | tokens → semantic layer → components; ButtonStyle; Layout |
| 10 | ios-networking | Endpoint as data, HTTPClient protocol, URLSession, config |
| 11 | ios-error-handling | typed errors, ErrorPresenter, ViewState, ActionOutcome |
| 12 | ios-concurrency | async let, .task, cancellation, @MainActor, actors |
| 13 | ios-app-architecture | layering, repository protocols, the cart reducer |
| 14 | ios-dependency-injection | composition root, no singletons, previews and tests |
| 15 | ios-persistence-and-keychain | where each thing belongs; the Keychain in detail |
| 16 | ios-app-lifecycle | scenePhase, the background flush, the launch gate |
| 17 | ios-payments | PaymentSheet, order-then-pay, the gateway protocol |
| 18 | ios-accessibility | labels/values/traits, the combine trap, touch targets |
| 19 | ios-testing | what to test, URLProtocol, async and main-actor tests |
| 20 | ios-previews-and-tooling | stubbed previews, SwiftLint, SwiftFormat, Instruments |
| 21 | ios-build-and-ship | xcconfig, Info.plist, signing, CI, the review |
| 22 | ios-interview-questions | answered against the twenty-one before it |

Dates run 2026-07-17 → 2026-09-18, three days apart, so lesson 22 is newest.

---

## Verified

- ✅ **`check_content.py`: all 22 pass.** 39,474 words, every post 8 reading-minutes, prose 71–95%
  against a 42% floor, 243 headings.
- ✅ **`check_snippets.py`: no drift.** 222 of 227 checked blocks (98%) quoted from code that runs;
  7 excluded as deliberate non-compiling examples; the rest illustrative.
- ✅ Seeded to `local`: 835 → 857 posts, category `ios` count 22.
- ✅ `npm run build` passes `verify-build`: 857/857 posts served, 46/46 category counts agree,
  1089 HTML files.
- ✅ **Swift highlights.** `out/ios/ios-concurrency.html` has 24 `language-swift` blocks with 337
  Prism token spans and zero `language-plaintext`.
- ✅ Nav order confirmed in the built HTML: Data Store · Software Engineering · **Mobile** ·
  JavaScript.
- ✅ 22 entries in the sitemap; the pager walks lesson 1 → 22.
- ❌ **Not viewed in a browser.** The Chrome extension was not connected, so the verification above
  is HTML parsing of the built output rather than a rendered page.

---

## Decisions

- **22 lessons at 8–10 reading-minutes**, matching the TypeScript track's depth rather than React's
  4–7. A Swift lesson that only shows syntax teaches nothing a language reference does not.
- **Prose floor 42%** — between TypeScript's 45% and FastAPI's 40%. Swift is verbose and a SwiftUI
  view is long, so a lesson quoting one real screen runs code-heavier than a TypeScript lesson
  legitimately can.
- **The React Native app is quoted for contrast**, not for code. The two apps are the same product
  on the same device, so a difference between them is a difference between the *stacks* — which is
  the most useful comparison this track can draw. It appears in lessons 3, 5, 6, 10, 12, 14 and 16.
- **The toolchain ceiling is stated, not hidden.** Xcode 15.4 / Swift 5.10 pins several lessons:
  `@Observable` yes, Swift 6 language mode no, `@Previewable` no. Where a lesson would read
  differently on a newer Xcode, it names the version.

---

## Gotchas paid for — do not rediscover these

- ⚠️ **`check_snippets.py` requires a quote to be CONTIGUOUS.** Truncating a struct and closing the
  brace yourself produces a block that looks right and exists nowhere in the app. It caught this
  eight times. Truncation is marked with a trailing `// …` comment instead, which the checker strips
  before matching — and it only works at the **end** of a block, never in the middle.
- ⚠️ **Every file a lesson quotes must be in `SNIPPET_SOURCES`.** A block matching the app but not
  the declared list is reported, which is the check that stops a snippet drifting in from an
  unrelated module. This fired ~15 times while writing.
- ⚠️ **Config dotfiles have no suffix.** `Path(".swiftformat").suffix` is `""`, so the checker's
  suffix test silently skipped it and reported the file as not existing. Fixed with a
  `SOURCE_FILENAMES` set.
- ⚠️ **`sync-content.sh` takes `CONTENT_ENV`, not a positional argument.**
  `./scripts/sync-content.sh local` silently syncs **prod**. Use
  `CONTENT_ENV=local ./scripts/sync-content.sh`, or `npm run sync-content:local`.
- Posts consistently came out ~400 words under the floor on a first draft. Budget for two or three
  extra sections rather than one.

---

## Still open

- **Publish to prod.** `python projects/ios_tutorial/seed.py --env prod --write`, then deploy. Not
  done — it was not asked for, and it triggers a real rebuild and CloudFront invalidation.
- **Commit the backend `swift` language addition.** It is entangled with pre-existing uncommitted
  changes in `app/services/content.py`. **Publishing before this lands would ship all 22 lessons as
  plaintext**, because the backend decides the `language-` class at save time.
- **Review the content.** It has been checked mechanically — length, prose share, snippet accuracy,
  markup — and not read end to end by a human.
- **Look at it in a browser.** The Chrome extension was unavailable this session.
- Consider whether `react-native` should move into the Mobile group. Deliberately left under
  JavaScript for now.

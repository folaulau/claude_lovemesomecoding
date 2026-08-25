"""The React Native track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and the last lesson is newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because
this track is authored before it publishes: when the publish date is known, move
START_DATE and every lesson re-bases in order.

⚠️ THE CATEGORY SLUG CHANGED. This collection was `rea-native` — a typo, carrying
five PLACEHOLDER posts published 2018-02-05. They are not literally empty (each has
WordPress `boldgrid-section` scaffolding); between them the real content is two
headings, one screenshot, a bare link and the word "Co". It is now `react-native`, and
the five post slugs move `rea-native-*` -> `react-native-*` with it. Five entries
below are marked `state: "rewrite"`: they are the same lessons at new URLs, and
`projects/react_native/retire_old.py` plus the frontend redirect map keep every
old URL resolving. See progress_report.md.

Because the five originals carry 2018 dates and `upsert_post` never overwrites an
existing date, the ORIGINALS are not reused in place — new slugs are created, so
no `--force-dates` dance is needed for them. The flag exists anyway, for re-dating
the track later.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "react-native",
    "name": "React Native",
    "description": (
        "React Native from the ground up — core components, flexbox, navigation, native APIs, "
        "native modules and shipping to the App Store, every example lifted from a real "
        "pizza-ordering app running on iOS and Android."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, which already labels this
# collection "React Native" — only the slug carried the typo.
NAV_GROUP = "JavaScript"

# The app every code sample is taken from, so a reader can see the whole thing in
# context rather than a fragment invented for the tutorial. Built 2026-08-24:
# Expo Router, feature-first, Context for state, Stripe PaymentSheet behind a
# platform-split module, 193 Jest tests and 31 Playwright tests.
DEMO_APP = "lovemesomecoding_demo_project/pizza/pizza-react-native-mobile"

# The versions the whole track is written against. Lesson 1 prints this table and
# every other lesson assumes it.
#
# These are READ OFF THE DEMO APP, not chosen — a lesson claiming a version the
# snippets were not copied from is the kind of drift nobody spots later.
VERSIONS = {
    "expo": "57.0",
    "react-native": "0.86",
    "react": "19.2",
    "expo-router": "57.0",
    "typescript": "6.0",
    "@stripe/stripe-react-native": "0.64",
    "jest-expo": "57.0",
    "@testing-library/react-native": "14.0",
    "node": "22",
    "xcode": "16.1+ (React Native 0.86's minimum)",
}

# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later, so
# the pager reads lesson 1 -> lesson 25. Re-base the whole track by editing these
# two values; nothing else changes.
#
# Deliberately back-dated so the finished track sits in the past rather than
# publishing into the future — lesson 25 lands 2026-08-21.
START_DATE = datetime(2026, 6, 10, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    """The publish timestamp for the index-th lesson, 0-based."""
    return (START_DATE + timedelta(days=STEP_DAYS * index)).strftime("%Y-%m-%dT%H:%M:%S")


# Authored in reading order. `state` is documentation, not data:
#   "new"     — a slug that has never existed
#   "rewrite" — replaces one of the five 2018 `rea-native-*` posts, which had an
#               indexed URL and an empty body. `old_slug` records what redirects to it.
# `sources` names the demo-app files the lesson quotes, so the topic review and
# check_snippets.py disagree loudly rather than quietly.
_TRACK = [
    # ------------------------------------------------------------- start here
    {
        "slug": "react-native-introduction",
        "title": "React Native – Introduction",
        "state": "rewrite",
        "old_slug": "rea-native-introduction",
        "tags": ["react-native", "react", "mobile"],
        "sources": ["README.md", "package.json"],
        "excerpt": (
            "Start here. What React Native actually is — real native views driven by JavaScript, "
            "not a web view — how it differs from React on the web and from Flutter, when a team "
            "picks it and when it should not, Expo versus bare React Native, the exact versions "
            "this track is written against, the pizza-ordering app every example comes from, and "
            "the full lesson index in reading order."
        ),
    },
    {
        "slug": "react-native-set-up",
        "title": "React Native – Set Up a Project with Expo",
        "state": "new",
        "tags": ["react-native", "expo", "typescript"],
        "sources": ["package.json", "app.config.ts", "tsconfig.json"],
        "excerpt": (
            "One command scaffolds the project. What `create-expo-app` generates and what each "
            "file is for, why `app.config.ts` beats a static `app.json` the moment you need an "
            "environment variable, path aliases that Metro reads straight from `tsconfig.json`, "
            "and the difference that trips everyone up — Expo Go versus a development build, and "
            "why anything with a native module needs the latter."
        ),
    },
    {
        "slug": "react-native-core-components",
        "title": "React Native – Core Components",
        "state": "rewrite",
        "old_slug": "rea-native-core-components",
        "tags": ["react-native", "components", "ui"],
        "sources": [
            "src/components/ui/Text.tsx",
            "src/components/ui/Button.tsx",
            "src/components/ui/Card.tsx",
        ],
        "excerpt": (
            "There is no DOM. `View` instead of `div`, `Text` instead of `span` — and unlike the "
            "web, text cannot live outside a `Text`. `Pressable` and why it replaced the four "
            "Touchable components, `Image`, `ScrollView`, and the rule that catches every web "
            "developer: nothing inherits, so every piece of text names its own size and colour."
        ),
    },
    {
        "slug": "react-native-styling",
        "title": "React Native – Styling and a Design System",
        "state": "new",
        "tags": ["react-native", "styling", "ui"],
        "sources": [
            "src/theme/tokens.ts",
            "src/theme/theme.ts",
            "src/components/ui/Text.tsx",
        ],
        "excerpt": (
            "Styles are JavaScript objects, not CSS. No cascade, no `var()`, no `:hover` — so a "
            "design system stops being a nicety and becomes the only way to stay consistent. "
            "`StyleSheet.create`, style arrays and how they merge, `Pressable`'s function-style "
            "prop for pressed states, and the platform split that makes shadows work on both iOS "
            "and Android instead of only one."
        ),
    },
    {
        "slug": "react-native-flexbox",
        "title": "React Native – Flexbox and Layout",
        "state": "rewrite",
        "old_slug": "rea-native-flexbox",
        "tags": ["react-native", "flexbox", "layout"],
        "sources": [
            "src/features/menu/components/ProductCard.tsx",
            "src/features/menu/components/PizzaBuilderSheet.tsx",
        ],
        "excerpt": (
            "Flexbox is the whole layout system — there is no grid and no float. The three "
            "defaults that differ from the web and bite constantly: `flexDirection` is `column`, "
            "`alignItems` is `stretch`, and `flex: 1` means something subtly different. Plus "
            "`gap`, wrapping rows of chips, and why `numberOfLines` is the only `text-overflow` "
            "you get."
        ),
    },
    # --------------------------------------------------------------- layout & UI
    {
        "slug": "react-native-safe-area",
        "title": "React Native – Safe Areas, Notches and the Keyboard",
        "state": "new",
        "tags": ["react-native", "layout", "ui"],
        "sources": [
            "src/components/ui/Screen.tsx",
            "src/components/ui/Sheet.tsx",
        ],
        "excerpt": (
            "The screen is not a rectangle you own. A notch, a camera cut-out, the home indicator "
            "and rounded corners all eat into it, and the amounts differ per device and "
            "orientation — so they cannot be constants. `useSafeAreaInsets`, where the navigation "
            "header already handles it for you, and `KeyboardAvoidingView`, which needs different "
            "behaviour on each platform to work at all."
        ),
    },
    {
        "slug": "react-native-lists",
        "title": "React Native – Lists with FlatList",
        "state": "new",
        "tags": ["react-native", "flatlist", "performance"],
        "sources": [
            "src/features/menu/screens/MenuScreen.tsx",
            "src/features/orders/screens/OrdersScreen.tsx",
        ],
        "excerpt": (
            "`ScrollView` renders every child immediately and holds them all in memory. "
            "`FlatList` virtualises — and on a phone that is the difference between a list that "
            "opens and one that hangs. `keyExtractor`, `renderItem`, header and empty components, "
            "multi-column grids, pull-to-refresh in two props, and why `numColumns` needs a `key` "
            "to change."
        ),
    },
    {
        "slug": "react-native-forms",
        "title": "React Native – TextInput and Forms",
        "state": "new",
        "tags": ["react-native", "forms", "textinput"],
        "sources": [
            "src/components/ui/TextField.tsx",
            "src/features/checkout/hooks/useCheckoutForm.ts",
            "src/features/auth/screens/LoginScreen.tsx",
        ],
        "excerpt": (
            "`TextInput` is where a mobile app is won or lost. `keyboardType` and "
            "`textContentType` change the keyboard itself and unlock password autofill; "
            "`autoCapitalize=\"none\"` on an email field is the single most common React Native "
            "bug. Controlled inputs, validation without a form library, per-field errors, and "
            "submitting from the keyboard when there is no Enter key."
        ),
    },
    {
        "slug": "react-native-modals",
        "title": "React Native – Modals, Sheets and Overlays",
        "state": "new",
        "tags": ["react-native", "modal", "ui"],
        "sources": [
            "src/components/ui/Sheet.tsx",
            "src/features/cart/components/CartSheet.tsx",
            "src/providers/ToastProvider.tsx",
        ],
        "excerpt": (
            "React Native's `Modal` is a real native window, which is why there is no `createPortal` "
            "in a React Native codebase — the z-index wars simply do not happen. Building a bottom "
            "sheet, the three things a web modal library gave you for free and you now wire by hand "
            "(Android's back button, tap-the-backdrop, the keyboard), and toasts that need no portal "
            "at all."
        ),
    },
    {
        "slug": "react-native-animations",
        "title": "React Native – Animations and the Native Driver",
        "state": "new",
        "tags": ["react-native", "animation", "performance"],
        "sources": ["src/providers/ToastProvider.tsx"],
        "excerpt": (
            "The `Animated` API, and the one flag that matters: `useNativeDriver`. With it the "
            "animation runs on the UI thread and stays smooth while JavaScript is busy; without it "
            "every frame crosses the bridge. Which properties can be driven natively and which "
            "cannot, `interpolate`, starting an animation in an effect rather than in render, and "
            "where Reanimated takes over."
        ),
    },
    # -------------------------------------------------------------- navigation
    {
        "slug": "react-native-navigation",
        "title": "React Native – Navigation",
        "state": "rewrite",
        "old_slug": "rea-native-navigation",
        "tags": ["react-native", "navigation", "expo-router"],
        "sources": [
            "app/_layout.tsx",
            "app/(tabs)/_layout.tsx",
            "app/(tabs)/index.tsx",
            "app/order/[orderId].tsx",
        ],
        "excerpt": (
            "Navigation is not a router over URLs — it is a stack of native screens. Expo Router "
            "makes the folder structure the navigation graph: `(tabs)` groups without adding a URL "
            "segment, `[orderId]` declares a dynamic route, `+not-found` catches the rest. Stacks "
            "versus tabs, passing and reading params, `push` versus `replace`, and why route files "
            "should be one line long."
        ),
    },
    {
        "slug": "react-native-deep-linking",
        "title": "React Native – Deep Linking and the URL as State",
        "state": "new",
        "tags": ["react-native", "navigation", "deep-linking"],
        "sources": [
            "app.config.ts",
            "src/features/menu/screens/MenuScreen.tsx",
        ],
        "excerpt": (
            "A phone app has URLs too. Registering a scheme, what a universal link needs beyond "
            "that, and the habit worth keeping from the web: putting screen state in route params "
            "so a link opens the app already filtered. Also the trap — a deep link can point at a "
            "screen a newer build removed, which is why `+not-found` matters more here than on the "
            "web."
        ),
    },
    # ----------------------------------------------------------- architecture
    {
        "slug": "react-native-project-structure",
        "title": "React Native – Structuring a Real App",
        "state": "new",
        "tags": ["react-native", "architecture", "typescript"],
        "sources": ["tsconfig.json", "src/types/index.ts", "src/api/index.ts"],
        "excerpt": (
            "The folder layout that survives a second developer. Feature-first rather than "
            "type-first, why route files should name a screen and never implement one, path "
            "aliases so nothing imports `../../../`, a single shared type contract with the "
            "backend, and the rule that keeps it honest: anything two features need moves down, "
            "never sideways."
        ),
    },
    {
        "slug": "react-native-state-management",
        "title": "React Native – State: Context, Reducers and Custom Hooks",
        "state": "new",
        "tags": ["react-native", "state", "react"],
        "sources": [
            "src/features/cart/state/cartReducer.ts",
            "src/features/cart/state/CartProvider.tsx",
            "src/providers/AppProviders.tsx",
        ],
        "excerpt": (
            "Same React you already know, with one extra constraint: a phone can be killed at any "
            "moment. `useReducer` for rules that depend on previous state, Context for what the "
            "whole tree needs, custom hooks for what one screen owns, and the ordering problem "
            "nobody warns you about — when one provider reads another, the nesting order becomes "
            "load-bearing."
        ),
    },
    {
        "slug": "react-native-data-fetching",
        "title": "React Native – Talking to an API",
        "state": "new",
        "tags": ["react-native", "networking", "api"],
        "sources": [
            "src/api/client.ts",
            "src/api/config.ts",
            "src/features/menu/state/MenuProvider.tsx",
        ],
        "excerpt": (
            "`fetch` works, and then reality arrives. `localhost` means three different things to "
            "a simulator, an emulator and a real phone — so the API host has to be resolved, not "
            "hard-coded. A request needs a timeout, because a weak signal does not fail fast. "
            "`AbortController` and cleanup, one error type instead of scattered `catch` blocks, "
            "and the loading/empty/error triple every screen owes its user."
        ),
    },
    {
        "slug": "react-native-storage",
        "title": "React Native – Storing Data on the Device",
        "state": "new",
        "tags": ["react-native", "storage", "security"],
        "sources": [
            "src/storage/secureStorage.ts",
            "src/storage/deviceStorage.ts",
            "src/storage/index.ts",
        ],
        "excerpt": (
            "There is no `localStorage`, and that turns out to be an improvement. `AsyncStorage` "
            "for what is inconvenient to lose, `expo-secure-store` — the iOS Keychain and Android "
            "EncryptedSharedPreferences — for anything an attacker could use. Both are "
            "asynchronous, which is why an app that reads a token on launch needs an "
            "`initialising` state and a splash screen that waits for it."
        ),
    },
    # --------------------------------------------------------- platform & native
    {
        "slug": "react-native-platform-apis",
        "title": "React Native – Platform APIs and Device Differences",
        "state": "new",
        "tags": ["react-native", "ios", "android"],
        "sources": [
            "src/storage/secureStorage.ts",
            "src/features/cart/state/CartProvider.tsx",
            "src/features/profile/screens/ProfileScreen.tsx",
        ],
        "excerpt": (
            "Where \"write once\" stops. `Platform.OS` and `Platform.select`, `.ios.tsx`/`.android.tsx` "
            "files that the bundler picks for you, `Alert` instead of `window.confirm`, "
            "`Dimensions` versus `useWindowDimensions` — and `AppState`, the one with no web "
            "equivalent at all: the OS can suspend or kill your process without warning, and "
            "unsaved work goes with it."
        ),
    },
    {
        "slug": "react-native-native-modules",
        "title": "React Native – Native Modules and Config Plugins",
        "state": "new",
        "tags": ["react-native", "expo", "native-modules"],
        "sources": [
            "app.config.ts",
            "src/features/checkout/payment/index.ts",
            "src/features/checkout/payment/paymentGateway.web.tsx",
        ],
        "excerpt": (
            "The moment you need something JavaScript cannot do. Why Expo Go cannot load a native "
            "module and a development build can, what `expo prebuild` generates, config plugins "
            "that edit the native projects for you, and the architectural move that keeps a "
            "native-only dependency from infecting the whole app — one folder, one interface, and "
            "a platform-split file the bundler resolves."
        ),
    },
    {
        "slug": "react-native-payments",
        "title": "React Native – Taking Payments with Stripe",
        "state": "new",
        "tags": ["react-native", "stripe", "payments"],
        "sources": [
            "src/features/checkout/payment/paymentGateway.tsx",
            "src/features/checkout/screens/CheckoutScreen.tsx",
        ],
        "excerpt": (
            "A worked native-module example that happens to involve money. Stripe's PaymentSheet "
            "rather than a card form of your own — the card never touches your code, which is what "
            "keeps you out of PCI scope. The two-step flow and why the order must exist before the "
            "sheet opens, treating a dismissed sheet as cancelled rather than failed, and the rule "
            "that outranks all of it: the device is never the authority on whether a payment "
            "succeeded."
        ),
    },
    {
        "slug": "react-native-accessibility",
        "title": "React Native – Accessibility",
        "state": "new",
        "tags": ["react-native", "accessibility", "ui"],
        "sources": [
            "src/components/ui/Button.tsx",
            "src/components/ui/SegmentedControl.tsx",
            "src/components/ui/StateViews.tsx",
        ],
        "excerpt": (
            "On the web a `<button>` announces itself. A `View` announces nothing, so every role, "
            "state and label is something you declare. `accessibilityRole`, `accessibilityState` "
            "and `accessibilityLabel`, grouping with `accessible` — and the trap inside it, which "
            "hides children from the accessibility tree and can make a button unreachable. Plus "
            "`hitSlop`, and why a spinner needs a label."
        ),
    },
    # ----------------------------------------------------------- quality & ship
    {
        "slug": "react-native-performance",
        "title": "React Native – Performance",
        "state": "new",
        "tags": ["react-native", "performance", "react"],
        "sources": [
            "src/features/menu/components/ProductCard.tsx",
            "src/features/menu/screens/MenuScreen.tsx",
        ],
        "excerpt": (
            "Why a React Native app drops frames and what to do about it. There are two threads "
            "and most of your code is on one of them. `memo` and `useCallback` as a pair — one is "
            "useless without the other — `FlatList` over `ScrollView`, animations on the native "
            "driver, and the honest advice: measure before you optimise, because the usual "
            "suspects are usually innocent."
        ),
    },
    {
        "slug": "react-native-error-handling",
        "title": "React Native – Error Boundaries and Failure States",
        "state": "new",
        "tags": ["react-native", "error-handling", "react"],
        "sources": [
            "src/components/RouteErrorBoundary.tsx",
            "src/api/apiError.ts",
            "src/components/ui/StateViews.tsx",
        ],
        "excerpt": (
            "A crash on a phone is a blank screen the user cannot refresh away. Error boundaries "
            "and what they deliberately do NOT catch — event handlers, timeouts, async functions, "
            "which is most of the code that fails. Turning an API error into something a customer "
            "can read, distinguishing a failure from a cancellation, and the LogBox and red screen "
            "you only see in development."
        ),
    },
    {
        "slug": "react-native-testing",
        "title": "React Native – Testing",
        "state": "new",
        "tags": ["react-native", "testing", "jest"],
        "sources": [
            "jest.setup.ts",
            "src/features/cart/state/__tests__/cartReducer.test.ts",
            "src/features/cart/state/__tests__/CartProvider.test.tsx",
        ],
        "excerpt": (
            "What to test and with what. `jest-expo` and React Native Testing Library, mocking the "
            "native modules that do not exist in Node, querying by accessibility label so the tests "
            "check what a screen reader would find, and the trap in the current version — `render` "
            "and `fireEvent` are async now, and forgetting an `await` produces an error that "
            "describes the opposite problem. Then where end-to-end testing takes over."
        ),
    },
    {
        "slug": "react-native-internals",
        "title": "React Native – Internals: Hermes, JSI and the New Architecture",
        "state": "rewrite",
        "old_slug": "rea-native-internals",
        "tags": ["react-native", "architecture", "hermes"],
        # Deliberately prose-only. This lesson explains Hermes, JSI, Fabric and the two threads —
        # none of which any application file demonstrates. Quoting `app.config.ts` here to satisfy a
        # convention would be decoration, not evidence.
        "sources": [],
        "excerpt": (
            "How the thing actually works. JavaScript runs in Hermes; your components are not "
            "drawn by a web view but turned into real native views. The old asynchronous bridge, "
            "why it was the bottleneck, and what JSI, Fabric and TurboModules replaced it with. "
            "What the New Architecture changes in practice, why Hermes matters for startup time, "
            "and how to reason about the two threads when something feels slow."
        ),
    },
    {
        "slug": "react-native-build-deploy",
        "title": "React Native – Building and Releasing to the App Stores",
        "state": "new",
        "tags": ["react-native", "expo", "deployment"],
        "sources": ["app.config.ts", "package.json"],
        "excerpt": (
            "The last mile, and the part web developers underestimate. `expo prebuild` and what it "
            "generates, EAS Build for machines you do not own, bundle identifiers, versioning and "
            "build numbers, environment configuration without leaking secrets, over-the-air "
            "updates and what they can and cannot change, and what App Store and Play Store review "
            "will ask you for."
        ),
    },
]

# Slug -> filename, and the dates, are derived so a reorder is one edit.
POSTS = [
    {
        "slug": entry["slug"],
        "title": entry["title"],
        "file": f"{i + 1:02d}-{entry['slug']}.html",
        "date": _date(i),
        "tags": entry["tags"],
        "excerpt": entry["excerpt"],
        "state": entry["state"],
        "sources": entry.get("sources", []),
    }
    for i, entry in enumerate(_TRACK)
]

# The five 2018 posts this track replaces: old slug -> new slug. Everything that
# has to keep resolving is derived from this one mapping — retire_old.py deletes
# the originals from it, and the frontend redirect map is generated from it.
OLD_SLUG_REDIRECTS = {
    entry["old_slug"]: entry["slug"] for entry in _TRACK if entry.get("old_slug")
}

# The category slug this collection used to live under.
OLD_CATEGORY_SLUG = "rea-native"

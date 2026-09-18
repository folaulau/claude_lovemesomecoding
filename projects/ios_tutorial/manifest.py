"""The iOS track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend with
the track and lesson 22 is the newest.

Every slug here is new. There is no `ios` category in the content DB (checked 2026-09-18 against
the categories in `content/index/categories.json`), so no indexed URL is at risk and `seed.py` never
needs `--force-dates`. If that ever stops being true — if an `ios` post is published by hand before
this track seeds — add it to FROZEN_SLUGS and the seed guard starts protecting it.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, so re-basing the whole
track is one edit.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "ios",
    "name": "iOS",
    "description": (
        "Native iOS from an empty Xcode project to an app that ships — Swift and SwiftUI first, "
        "then everything a tutorial usually skips: the layer boundaries that keep a codebase "
        "readable, structured concurrency instead of callbacks, the Keychain, what a phone does to "
        "your app when it leaves the foreground, and how to test any of it. Every example is lifted "
        "from a working pizza ordering app, so code in these posts is code that runs."
    ),
}

# Where the category sits in the site navigation.
#
# ⚠️ A REAL task, not a note. `ios` is a brand-new slug AND `Mobile` is a brand-new top-level
# group, so lovemesomecoding_frontend/src/lib/nav.ts needs both adding or the dropdown never
# appears. `navTree()` drops a group whose categories do not exist, so the nav change is safe to
# land before the seed — it simply stays invisible until there is something to link to.
NAV_GROUP = "Mobile"

# The app every code sample is taken from.
#
# Chosen over the React Native app next door for the obvious reason — this is the native track —
# but also because it was written to be read. Every architectural decision in it already carries a
# comment explaining why, which is the raw material these lessons are made of.
#
# State on 2026-09-18: committed, 130/130 tests passing on an iPhone 15 simulator, and run against
# the live backend. A tutorial that quotes a tree nobody has executed is a tutorial that ships
# plausible code.
DEMO_APP = "lovemesomecoding_demo_project/pizza"

# The iOS half of it. Paths in SNIPPET_SOURCES are relative to DEMO_APP, not to the repo root —
# that is what check_content.py and check_snippets.py resolve against. Keeping DEMO_APP at the
# `pizza` level rather than at `pizza-ios-mobile` also lets a lesson quote the CI workflow, which
# lives beside the app rather than inside it.
A = "pizza-ios-mobile"

# The React Native sibling, quoted ONLY for contrast and only in a handful of lessons. The two apps
# are the same product on the same device, so a difference between them is a difference between the
# stacks rather than between the apps — which is the most useful comparison this track can draw.
RN = "pizza-react-native-mobile"

# ---------------------------------------------------------------------------
# Versions — READ OFF THIS MACHINE, not chosen
# ---------------------------------------------------------------------------
# `xcodebuild -version`, `swift --version`, `xcrun simctl list runtimes` and the resolved SPM
# version, all 2026-09-18.
#
# ⚠️ Xcode 15.4 is not the newest release, and the track says so rather than pretending otherwise.
# It is what pins the ceiling on several lessons: Swift 5.10 rather than 6, `@Observable` available
# but strict concurrency not enforced, no `@Previewable`. Where a lesson would read differently on
# a newer toolchain, it says which version changes it.
VERSIONS = {
    "xcode": "15.4",
    "swift": "5.10",
    "ios-deployment-target": "17.0",
    "ios-sdk": "17.5",
    "simulator-runtime": "17.5 (21F79)",
    "stripe-payment-sheet": "23.32.0",
    "xcodegen": "2.46.0",
}

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together, then
# `readingMinutes = max(1, round(words / 220))`. See lovemesomecoding_backend/app/services/
# content.py. Budgeting prose alone silently doubles the published reading time.
#
# 8-10 reading-minutes, matching the TypeScript track. Deeper than React's 4-7, because a Swift
# lesson that only shows the syntax teaches nothing a language reference does not.
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (8, 10)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 1,760
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 2,200

# ⚠️ 42% prose floor — between the TypeScript track's 45% and FastAPI's 40%.
#
# Swift is verbose and SwiftUI view code is long, so a lesson quoting one real view legitimately
# runs code-heavy in a way a TypeScript lesson does not. But the failure mode is the same: when
# code takes over the word count it is usually because the post has become a listing with captions
# instead of an argument. 42% is the line where that starts.
MIN_PROSE_SHARE = 0.42

# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------
# 22 posts, 3 days apart, landing the last one on 2026-09-18.
START_DATE = datetime(2026, 7, 17, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=index * STEP_DAYS)).strftime("%Y-%m-%dT%H:%M:%S")


# ---------------------------------------------------------------------------
# Which files each post is allowed to quote
# ---------------------------------------------------------------------------
# Paths are relative to the repo root. check_snippets.py checks a post's code blocks against THESE
# files first, and reports a block that matches the app but not the declared list — a snippet that
# has drifted in from an unrelated module is a finding, not a pass.
SNIPPET_SOURCES = {
    "ios-get-started": [
        f"{A}/project.yml", f"{A}/Config/Shared.xcconfig", f"{A}/Config/Debug.xcconfig",
        f"{A}/Scripts/generate-project.sh", f"{A}/Pizza/App/PizzaApp.swift",
    ],
    "ios-swift-essentials": [
        f"{A}/Pizza/Domain/Models/Catalog.swift", f"{A}/Pizza/Domain/Models/Cart.swift",
        f"{A}/Pizza/Core/Utilities/Money.swift", f"{A}/Pizza/Domain/Models/User.swift",
        f"{A}/Pizza/Core/Networking/HTTPMethod.swift",
        f"{A}/Pizza/Domain/Models/Common.swift",
        # Forward references. The lesson shows each of these as a SHAPE and says which later
        # lesson builds it out — an enum with associated values, a typed error, a captured
        # closure, an extension on a type we do not own.
        f"{A}/Pizza/Core/Utilities/ViewState.swift",
        f"{A}/Pizza/Core/Networking/APIError.swift",
        f"{A}/Pizza/App/ToastCenter.swift",
        f"{A}/Pizza/Features/Checkout/CheckoutForm.swift",
    ],
    "ios-swiftui-views-and-layout": [
        f"{A}/Pizza/Features/Home/HomeView.swift",
        f"{A}/Pizza/Core/DesignSystem/Components/CardContainer.swift",
        f"{A}/Pizza/Core/DesignSystem/Components/PriceRow.swift",
        f"{A}/Pizza/Core/DesignSystem/Components/ScreenContainer.swift",
    ],
    "ios-state-and-observable": [
        f"{A}/Pizza/Features/Menu/MenuStore.swift",
        f"{A}/Pizza/App/ToastCenter.swift",
        f"{A}/Pizza/Features/Menu/MenuView.swift",
        f"{A}/Pizza/Features/Cart/Components/CartSheetView.swift",
        f"{A}/Pizza/Features/Menu/Components/PizzaBuilderViewModel.swift",
        # The injection half of the lesson: where the stores are put in, and where one is read out.
        f"{A}/Pizza/App/PizzaApp.swift", f"{A}/Pizza/App/RootView.swift",
        f"{A}/Pizza/Features/Home/HomeView.swift",
    ],
    "ios-navigation": [
        f"{A}/Pizza/App/AppRouter.swift", f"{A}/Pizza/App/RootView.swift",
    ],
    "ios-lists-and-performance": [
        f"{A}/Pizza/Features/Menu/MenuView.swift",
        f"{A}/Pizza/Features/Menu/Components/ProductCardView.swift",
        f"{A}/Pizza/Features/Orders/OrdersView.swift",
        # The identity section quotes the model that makes `ForEach(products)` work without a key
        # path, and the enumerated-with-element-id idiom from the cart.
        f"{A}/Pizza/Domain/Models/Catalog.swift",
        f"{A}/Pizza/Features/Cart/Components/CartSheetView.swift",
    ],
    "ios-forms-and-input": [
        f"{A}/Pizza/Core/DesignSystem/Components/LabeledTextField.swift",
        f"{A}/Pizza/Features/Auth/SignInView.swift",
        f"{A}/Pizza/Features/Checkout/CheckoutForm.swift",
        # The keyboard-dismiss modifier, and the validator tests that are the payoff for keeping
        # the rules out of the view.
        f"{A}/Pizza/Core/DesignSystem/Components/ScreenContainer.swift",
        f"{A}/PizzaTests/CheckoutFormValidatorTests.swift",
    ],
    "ios-sheets-and-modals": [
        f"{A}/Pizza/Core/DesignSystem/Components/SheetScaffold.swift",
        f"{A}/Pizza/Features/Cart/Components/CartSheetView.swift",
        f"{A}/Pizza/Features/Menu/MenuView.swift",
        f"{A}/Pizza/Features/Profile/ProfileView.swift",
        f"{A}/Pizza/App/AppRouter.swift",
        # The builder sheet is the `.sheet(item:)` example, and its preview is the presentation idiom.
        f"{A}/Pizza/Features/Menu/Components/PizzaBuilderSheet.swift",
        # The detents are applied where the sheet is presented, which is the root view.
        f"{A}/Pizza/App/RootView.swift",
    ],
    "ios-design-system": [
        f"{A}/Pizza/Core/DesignSystem/Tokens.swift",
        f"{A}/Pizza/Core/DesignSystem/Theme.swift",
        f"{A}/Pizza/Core/DesignSystem/Typography.swift",
        f"{A}/Pizza/Core/DesignSystem/Components/PizzaButton.swift",
        f"{A}/Pizza/Core/DesignSystem/Components/FlowLayout.swift",
        # The exhaustive-switch argument is made with the order-status badge.
        f"{A}/Pizza/Core/DesignSystem/Components/StatusBadge.swift",
    ],
    "ios-networking": [
        f"{A}/Pizza/Core/Networking/Endpoint.swift",
        f"{A}/Pizza/Core/Networking/HTTPClient.swift",
        f"{A}/Pizza/Core/Networking/URLSessionHTTPClient.swift",
        f"{A}/Pizza/Core/Networking/APIConfiguration.swift",
        f"{A}/Pizza/Data/Endpoints/APIEndpoints.swift",
        # The shared coder, and the repository that sits on top of the client.
        f"{A}/Pizza/Core/Networking/JSONCoding.swift",
        f"{A}/Pizza/Data/Repositories/RemoteRepositories.swift",
    ],
    "ios-error-handling": [
        f"{A}/Pizza/Core/Networking/APIError.swift",
        f"{A}/Pizza/Core/Utilities/ViewState.swift",
        f"{A}/Pizza/Core/Utilities/ActionOutcome.swift",
        f"{A}/Pizza/Core/DesignSystem/Components/StateViews.swift",
        # The store that produces a ViewState, the view that switches over one, the profile
        # screen's toast reporter, and the tests that prove the retryability rule.
        f"{A}/Pizza/Features/Menu/MenuStore.swift",
        f"{A}/Pizza/Features/Menu/MenuView.swift",
        f"{A}/Pizza/Features/Profile/ProfileView.swift",
        f"{A}/PizzaTests/SupportTypeTests.swift",
    ],
    "ios-concurrency": [
        f"{A}/Pizza/Features/Menu/MenuStore.swift",
        f"{A}/Pizza/Core/Persistence/TokenStore.swift",
        f"{A}/Pizza/Features/Orders/OrderConfirmationViewModel.swift",
        f"{A}/Pizza/Features/Cart/CartStore.swift",
        f"{A}/Pizza/Features/Profile/ProfileViewModel.swift",
        # The startup sequence, which is where `.task` and the ordering rule are shown.
        f"{A}/Pizza/App/RootView.swift",
    ],
    "ios-app-architecture": [
        f"{A}/Pizza/Domain/Repositories/Repositories.swift",
        f"{A}/Pizza/Data/Repositories/RemoteRepositories.swift",
        f"{A}/Pizza/Domain/Services/CartReducer.swift",
        f"{A}/Pizza/Features/Cart/CartStore.swift",
        # The pure pricing rules that live beside the reducer, and the reducer's own tests.
        f"{A}/Pizza/Domain/Services/CartPricing.swift",
        f"{A}/PizzaTests/CartReducerTests.swift",
    ],
    "ios-dependency-injection": [
        f"{A}/Pizza/App/AppEnvironment.swift",
        f"{A}/Pizza/App/PizzaApp.swift",
        f"{A}/Pizza/Data/Repositories/PreviewRepositories.swift",
        f"{A}/Pizza/Features/Checkout/CheckoutView.swift",
        # The test-side payoff: spies that record calls, a store built with everything injected,
        # and the one-method protocol that breaks the client/session cycle.
        f"{A}/PizzaTests/Support/TestDoubles.swift",
        f"{A}/PizzaTests/StoreTests.swift",
        f"{A}/Pizza/Core/Networking/HTTPClient.swift",
        f"{A}/Pizza/Features/Menu/MenuView.swift",
    ],
    "ios-persistence-and-keychain": [
        f"{A}/Pizza/Core/Persistence/SecureStore.swift",
        f"{A}/Pizza/Core/Persistence/TokenStore.swift",
        f"{A}/Pizza/Core/Persistence/KeyValueStore.swift",
        f"{A}/Pizza/Core/Persistence/StorageKey.swift",
        f"{A}/Pizza/Core/Persistence/CartIdentifierStore.swift",
        # The cache test, which is the only way to prove a cache is a cache.
        f"{A}/PizzaTests/SupportTypeTests.swift",
    ],
    "ios-app-lifecycle": [
        f"{A}/Pizza/App/PizzaApp.swift",
        f"{A}/Pizza/Features/Cart/CartStore.swift",
        f"{A}/Pizza/App/RootView.swift",
        f"{A}/Pizza/Features/Auth/AuthStore.swift",
    ],
    "ios-payments": [
        f"{A}/Pizza/Features/Checkout/Payment/PaymentGateway.swift",
        f"{A}/Pizza/Features/Checkout/Payment/StripePaymentGateway.swift",
        f"{A}/Pizza/Features/Checkout/CheckoutViewModel.swift",
        f"{A}/Pizza/Resources/Info.plist",
    ],
    "ios-accessibility": [
        f"{A}/Pizza/Core/DesignSystem/Components/SegmentedPicker.swift",
        f"{A}/Pizza/Core/DesignSystem/Components/ToppingChip.swift",
        f"{A}/Pizza/Core/DesignSystem/Components/StateViews.swift",
        f"{A}/Pizza/Core/DesignSystem/Components/PriceRow.swift",
        f"{A}/Pizza/Features/Checkout/Components/SavedAddressPicker.swift",
    ],
    "ios-testing": [
        f"{A}/PizzaTests/CartReducerTests.swift",
        f"{A}/PizzaTests/URLSessionHTTPClientTests.swift",
        f"{A}/PizzaTests/Support/StubURLProtocol.swift",
        f"{A}/PizzaTests/Support/TestDoubles.swift",
        f"{A}/PizzaTests/ViewModelTests.swift",
        f"{A}/PizzaTests/EndpointTests.swift",
    ],
    "ios-previews-and-tooling": [
        f"{A}/Pizza/Data/Repositories/PreviewRepositories.swift",
        f"{A}/Pizza/Features/Menu/MenuView.swift",
        f"{A}/Pizza/Features/Checkout/Components/SavedAddressPicker.swift",
        f"{A}/.swiftlint.yml", f"{A}/.swiftformat",
    ],
    "ios-build-and-ship": [
        f"{A}/project.yml", f"{A}/Config/Shared.xcconfig", f"{A}/Config/Release.xcconfig",
        f"{A}/Pizza/Resources/Info.plist",
        f"{A}/Scripts/generate-project.sh",
        ".github/workflows/ios.yml",
    ],
    "ios-interview-questions": [
        f"{A}/Pizza/Domain/Services/CartReducer.swift",
        f"{A}/Pizza/Core/Utilities/ViewState.swift",
        f"{A}/Pizza/Core/Persistence/TokenStore.swift",
    ],
}

# A section deliberately showing the WRONG way. check_snippets.py excludes blocks near this marker
# from the "must match the app" rule, because not matching is the entire point of them.
#
# This track needs it less than the TypeScript one — Swift lessons argue from working code more
# often than from rejected code — but four lessons genuinely depend on it, and all four are about
# things the compiler stops you doing: main-actor isolation, `deinit`, default-argument isolation,
# and `@MainActor` on an XCTestCase.
ANTIPATTERN_MARKER = "does not compile"

# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
_TRACK = [
    # ----------------------------------------------------- the language and the framework
    {
        "slug": "ios-get-started",
        "title": "iOS – Getting Started",
        "tags": ["ios", "swift", "xcode"],
        "excerpt": (
            "What you actually need to build an iOS app, what each piece of Xcode is for, and the "
            "anatomy of a project — targets, schemes, build configurations and the .xcodeproj "
            "nobody can read. Ending with a project generated from a manifest instead, so a build "
            "setting change is a line in a diff rather than an opaque edit."
        ),
    },
    {
        "slug": "ios-swift-essentials",
        "title": "iOS – The Swift You Need First",
        "tags": ["ios", "swift"],
        "excerpt": (
            "Not the whole language — the parts a SwiftUI app leans on every day. Value types "
            "versus reference types and why it changes how you reason about a screen, optionals, "
            "enums with associated values, protocols and extensions, closures, and the error model. "
            "With the models of a real ordering app as the running example."
        ),
    },
    {
        "slug": "ios-swiftui-views-and-layout",
        "title": "iOS – SwiftUI Views and Layout",
        "tags": ["ios", "swiftui", "layout"],
        "excerpt": (
            "A View is a value, not an object, and almost everything surprising about SwiftUI "
            "follows from that. Stacks, frames and the layout conversation between parent and "
            "child, modifier order and why it is not decoration, and how to build a reusable "
            "container — the card every screen in this app is made of."
        ),
    },
    {
        "slug": "ios-state-and-observable",
        "title": "iOS – State, @Observable and Data Flow",
        "tags": ["ios", "swiftui", "state"],
        "excerpt": (
            "@State, @Binding, @Observable and @Environment: which one to reach for, and the rule "
            "that decides it. Why @Observable replaced ObservableObject and what it actually "
            "changed, @Bindable, and the line between state a screen owns and state the app owns — "
            "with the three stores this app has and the many it deliberately does not."
        ),
    },
    {
        "slug": "ios-navigation",
        "title": "iOS – Navigation",
        "tags": ["ios", "swiftui", "navigation"],
        "excerpt": (
            "NavigationStack with a path, so a route is a value you can push, log and restore "
            "rather than a view built eagerly for a row nobody tapped. Typed routes, tabs that "
            "each keep their own stack, programmatic navigation after a payment, and where deep "
            "links plug in."
        ),
    },
    {
        "slug": "ios-lists-and-performance",
        "title": "iOS – Lists, Grids and Keeping Them Fast",
        "tags": ["ios", "swiftui", "performance"],
        "excerpt": (
            "List, LazyVStack and LazyVGrid, and the difference that matters: which of them builds "
            "every row before showing you the first one. Identity and why a bad id is a rendering "
            "bug, pull-to-refresh, and what SwiftUI does instead of React's memo — including what "
            "you still have to do yourself."
        ),
    },
    {
        "slug": "ios-forms-and-input",
        "title": "iOS – Forms, Text Input and Validation",
        "tags": ["ios", "swiftui", "forms"],
        "excerpt": (
            "The keyboard is part of your UI. keyboardType, textContentType and AutoFill, the "
            "autocapitalisation default that breaks every email field, @FocusState and moving "
            "between fields, and a validation model that keeps the rules out of the view and "
            "testable in microseconds."
        ),
    },
    {
        "slug": "ios-sheets-and-modals",
        "title": "iOS – Sheets, Modals and Alerts",
        "tags": ["ios", "swiftui", "sheets"],
        "excerpt": (
            "sheet(isPresented:) versus sheet(item:), and why the second one resets a form for "
            "free. Detents, drag indicators, alerts and confirmation dialogs, and the boolean-flag "
            "mistake that makes a tap look like it was dropped — with the one enum that makes it "
            "unrepresentable."
        ),
    },
    {
        "slug": "ios-design-system",
        "title": "iOS – Building a Design System",
        "tags": ["ios", "swiftui", "design-system"],
        "excerpt": (
            "Tokens, a semantic layer over them, and components that consume the semantic layer — "
            "the three tiers, and why skipping the middle one makes a retune impossible. "
            "ViewModifier versus wrapper view, ButtonStyle instead of a custom button, and writing "
            "a Layout by hand when SwiftUI ships nothing that wraps."
        ),
    },
    # ----------------------------------------------------- talking to a server
    {
        "slug": "ios-networking",
        "title": "iOS – Networking with URLSession",
        "tags": ["ios", "swift", "networking"],
        "excerpt": (
            "One type that performs requests, and everything else describing them. An Endpoint as "
            "inert data so routes are testable without a socket, async/await over URLSession, "
            "Codable and the decoding failures that only happen in production, and configuration "
            "that comes from the build rather than a constant."
        ),
    },
    {
        "slug": "ios-error-handling",
        "title": "iOS – Error Handling That Reaches the User",
        "tags": ["ios", "swift", "errors"],
        "excerpt": (
            "A typed error whose cases are the decisions a caller can make, not the places it went "
            "wrong. LocalizedError, field-level messages from a server, telling a cancelled request "
            "apart from a failed one, and the ViewState enum that makes the eternal spinner "
            "impossible to write."
        ),
    },
    {
        "slug": "ios-concurrency",
        "title": "iOS – async/await, Tasks and Actors",
        "tags": ["ios", "swift", "concurrency"],
        "excerpt": (
            "Structured concurrency in the shape you will actually use it: async let for requests "
            "that should overlap, .task tying work to a view's lifetime, cancellation you get for "
            "free, @MainActor and what it enforces, and an actor for state several callers touch "
            "at once. Plus the deinit rule nobody mentions."
        ),
    },
    # ----------------------------------------------------- structure
    {
        "slug": "ios-app-architecture",
        "title": "iOS – Architecture: Layers That Hold",
        "tags": ["ios", "architecture", "mvvm"],
        "excerpt": (
            "MVVM is not an architecture, it is a naming convention for one third of one. The "
            "layering underneath it: domain models and rules that import nothing, repository "
            "protocols the features depend on, implementations they never see, and a pure reducer "
            "for the one piece of state worth being strict about."
        ),
    },
    {
        "slug": "ios-dependency-injection",
        "title": "iOS – Dependency Injection Without a Framework",
        "tags": ["ios", "architecture", "testing"],
        "excerpt": (
            "A composition root — one initialiser that decides every concrete type the app runs "
            "with — instead of singletons scattered through it. Why a static shared is a testing "
            "problem before it is a design problem, injecting through the SwiftUI environment, and "
            "the constructor parameter that turns an ordering rule into a compiler guarantee."
        ),
    },
    {
        "slug": "ios-persistence-and-keychain",
        "title": "iOS – Persistence, UserDefaults and the Keychain",
        "tags": ["ios", "swift", "security"],
        "excerpt": (
            "Where each thing belongs and why the split is a security decision, not a convenience "
            "one. UserDefaults for preferences, the Keychain for a session token, the accessibility "
            "class that actually matters, and why the Security API makes you write save as "
            "delete-then-add. Plus what SwiftData is for."
        ),
    },
    {
        "slug": "ios-app-lifecycle",
        "title": "iOS – The App Lifecycle and What a Phone Does to You",
        "tags": ["ios", "swiftui", "lifecycle"],
        "excerpt": (
            "A browser tab lives until it is closed; your app can be suspended mid-sentence and "
            "killed without warning. scenePhase, the write you have to flush before backgrounding, "
            "the launch gate an async Keychain read forces on you, and the startup ordering that "
            "is load-bearing rather than tidy."
        ),
    },
    {
        "slug": "ios-payments",
        "title": "iOS – Taking Payments with Stripe",
        "tags": ["ios", "stripe", "payments"],
        "excerpt": (
            "PaymentSheet rather than a card form of your own, and the PCI reason that is not "
            "negotiable. The two-step order-then-pay flow and why it has to be two steps, "
            "quarantining the SDK behind a protocol so checkout is testable, bridging a completion "
            "handler into async, and the dismissed sheet that is not an error."
        ),
    },
    {
        "slug": "ios-accessibility",
        "title": "iOS – Accessibility",
        "tags": ["ios", "swiftui", "accessibility"],
        "excerpt": (
            "A drawn control carries no meaning. Labels, values, traits and the difference between "
            "them, combining a row into one announcement and the trap that hides its button, "
            "Dynamic Type, touch target size, and how to check any of it in about a minute — with "
            "the real controls in this app that needed each fix."
        ),
    },
    # ----------------------------------------------------- shipping
    {
        "slug": "ios-testing",
        "title": "iOS – Testing an iOS App",
        "tags": ["ios", "testing", "xctest"],
        "excerpt": (
            "What to test and what to skip. Pure rules first because they cost nothing, a real "
            "URLSession against a stubbed URLProtocol so the assertions are about the bytes you "
            "would send, hand-written doubles over a mocking framework, testing async and "
            "main-actor code, and why @MainActor on an XCTestCase is wrong."
        ),
    },
    {
        "slug": "ios-previews-and-tooling",
        "title": "iOS – Previews, Linting and the Tools Around the Code",
        "tags": ["ios", "swiftui", "tooling"],
        "excerpt": (
            "A preview that needs a running backend is a preview nobody uses. Stub repositories so "
            "every screen renders instantly — including its failure state — plus SwiftLint and "
            "SwiftFormat configured to catch what review keeps catching, and the Instruments "
            "templates worth knowing before you need them."
        ),
    },
    {
        "slug": "ios-build-and-ship",
        "title": "iOS – Build Configuration, CI and Shipping",
        "tags": ["ios", "ci", "release"],
        "excerpt": (
            "xcconfig files so a build setting is reviewable, Info.plist keys a custom plist makes "
            "you own, signing and what actually needs an Apple account, a CI workflow that checks "
            "the committed project still matches its manifest, and the archive-to-App-Store path "
            "with the rejections worth avoiding."
        ),
    },
    {
        "slug": "ios-interview-questions",
        "title": "iOS – Interview Questions",
        "tags": ["ios", "swift", "interview"],
        "excerpt": (
            "The questions an iOS role actually asks, answered against the twenty-one lessons "
            "before this one. Struct versus class, what @State really stores, how SwiftUI decides "
            "to redraw, retain cycles in closures, what @MainActor guarantees, actor reentrancy, "
            "and how you would make a screen testable. Short answers, with the reasoning."
        ),
    },
]

POSTS = [
    {
        "slug": entry["slug"],
        "title": entry["title"],
        "file": f"{i + 1:02d}-{entry['slug']}.html",
        "date": _date(i),
        "tags": entry["tags"],
        "excerpt": entry["excerpt"],
    }
    for i, entry in enumerate(_TRACK)
]

# Nothing is frozen: this category does not exist on the live site yet, so no slug here is an
# indexed URL. Kept as an empty set rather than deleted so seed.py's guard stays wired up — the day
# an ios post is published outside this track, adding it here is the whole fix.
FROZEN_SLUGS: set[str] = set()

NEW_SLUGS = {e["slug"] for e in _TRACK}

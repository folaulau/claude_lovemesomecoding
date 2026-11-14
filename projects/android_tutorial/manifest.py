"""The Android track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site — archives and the
sitemap sort newest first, and prev/next walks the category oldest-first — so the dates ascend with
the track and lesson 23 is the newest.

Every slug here is new. There is no `android` category in the content DB (checked 2026-10-10), so
no indexed URL is at risk and `seed.py` never needs `--force-dates`. If that ever stops being true,
add the slug to FROZEN_SLUGS and the seed guard starts protecting it.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, so re-basing the whole
track is one edit.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "android",
    "name": "Android",
    "description": (
        "Native Android from an empty Gradle project to an app on the Play Store — Kotlin and "
        "Jetpack Compose first, then everything a tutorial usually skips: ViewModels and process "
        "death, layer boundaries that keep a codebase readable, coroutines and Flow, Hilt, the "
        "Keystore, what the OS does to your app in the background, and how to test any of it. "
        "Every example is lifted from a working pizza ordering app, so code in these posts is "
        "code that runs."
    ),
}

# The `Mobile` group already exists (added for iOS, 2026-09-18). `android` is a new slug in it.
NAV_GROUP = "Mobile"

# The app every code sample is taken from. Paths in SNIPPET_SOURCES are relative to DEMO_APP.
# Keeping DEMO_APP at the `pizza` level lets a lesson quote the CI workflow beside the app.
#
# State on 2026-10-10: 104/104 JVM tests passing, lint clean, a minified release build run on an
# emulator, and a full guest order driven against the live backend through Stripe test mode.
DEMO_APP = "lovemesomecoding_demo_project/pizza"

A = "pizza-android-mobile"
K = f"{A}/app/src/main/java/com/lovemesomecoding/pizza"
T = f"{A}/app/src/test/java/com/lovemesomecoding/pizza"
RES = f"{A}/app/src/main/res"

# The SwiftUI sibling, quoted ONLY for contrast. The two apps are the same product with the same
# layering, so a difference between them is a difference between the platforms.
IOS = "pizza-ios-mobile/Pizza"

# ---------------------------------------------------------------------------
# Versions — READ OFF GOOGLE MAVEN / MAVEN CENTRAL, 2026-10-10, and built with
# ---------------------------------------------------------------------------
VERSIONS = {
    "gradle": "9.8.1",
    "agp": "9.4.1",
    "kotlin": "2.4.21",
    "compose-bom": "2026.09.00",
    "hilt": "2.60.1",
    "navigation": "2.10.2",
    "lifecycle": "2.11.0",
    "retrofit": "3.0.0",
    "okhttp": "5.5.0",
    "stripe-android": "23.22.0",
    "compileSdk": "37",
    "targetSdk": "37",
    "minSdk": "26",
    "emulator": "API 35",
}

# ---------------------------------------------------------------------------
# Length budget — identical to the iOS track
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together.
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (8, 10)
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 1,760
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 2,200
MIN_PROSE_SHARE = 0.42

# ---------------------------------------------------------------------------
# Dates: 23 posts, 3 days apart, the last landing on 2026-10-10.
# ---------------------------------------------------------------------------
START_DATE = datetime(2026, 8, 5, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    return (START_DATE + timedelta(days=index * STEP_DAYS)).strftime("%Y-%m-%dT%H:%M:%S")


# A section deliberately showing the WRONG way. check_snippets.py excludes blocks near this marker.
ANTIPATTERN_MARKER = "the wrong way"

# ---------------------------------------------------------------------------
# Which files each post is allowed to quote (relative to DEMO_APP)
# ---------------------------------------------------------------------------
SNIPPET_SOURCES = {
    "android-get-started": [
        f"{A}/settings.gradle.kts", f"{A}/build.gradle.kts", f"{A}/gradle.properties",
        f"{A}/gradle/libs.versions.toml", f"{A}/app/build.gradle.kts",
        f"{A}/app/src/main/AndroidManifest.xml", f"{K}/MainActivity.kt", f"{K}/PizzaApplication.kt",
    ],
    "android-kotlin-essentials": [
        f"{K}/domain/model/Catalog.kt", f"{K}/domain/model/Cart.kt", f"{K}/domain/model/Order.kt",
        f"{K}/domain/model/User.kt", f"{K}/domain/model/Common.kt", f"{K}/core/util/Money.kt",
        f"{K}/core/util/UiState.kt", f"{K}/core/network/ApiError.kt", f"{K}/core/util/ActionOutcome.kt",
        f"{K}/feature/checkout/CheckoutForm.kt", f"{K}/domain/cart/CartReducer.kt",
        f"{K}/domain/cart/CartPricing.kt", f"{K}/feature/menu/MenuScreen.kt",
        f"{K}/PizzaApplication.kt", f"{K}/core/persistence/SecureStore.kt",
    ],
    "android-compose-layout": [
        f"{K}/feature/home/HomeScreen.kt", f"{K}/feature/menu/ProductCard.kt",
        f"{K}/core/designsystem/components/CardContainer.kt",
        f"{K}/core/designsystem/components/PriceRow.kt",
        f"{K}/core/designsystem/components/PizzaButton.kt",
    ],
    "android-compose-state": [
        f"{K}/feature/menu/MenuScreen.kt", f"{K}/feature/menu/MenuViewModel.kt",
        f"{K}/feature/menu/PizzaBuilderState.kt", f"{K}/feature/menu/MenuStore.kt",
        f"{K}/core/designsystem/components/QuantityStepper.kt", f"{K}/feature/cart/CartStore.kt",
        f"{K}/feature/auth/AuthSheets.kt",
    ],
    "android-viewmodel-and-process-death": [
        f"{K}/feature/checkout/CheckoutViewModel.kt", f"{K}/feature/checkout/CheckoutForm.kt",
        f"{K}/feature/orders/OrderConfirmationViewModel.kt", f"{K}/feature/menu/MenuScreen.kt",
        f"{K}/feature/auth/AuthSheets.kt", f"{K}/app/AppViewModel.kt",
        f"{T}/feature/CheckoutViewModelTest.kt",
    ],
    "android-navigation": [
        f"{K}/app/AppRoutes.kt", f"{K}/app/PizzaApp.kt",
        f"{K}/feature/orders/OrderConfirmationViewModel.kt",
    ],
    "android-lists-and-performance": [
        f"{K}/feature/menu/MenuScreen.kt", f"{K}/feature/orders/OrdersScreen.kt",
        f"{K}/feature/cart/CartSheet.kt", f"{K}/feature/menu/PizzaBuilderState.kt",
        f"{K}/feature/menu/MenuViewModel.kt", f"{K}/core/designsystem/Theme.kt",
    ],
    "android-forms-and-input": [
        f"{K}/core/designsystem/components/LabeledTextField.kt", f"{K}/feature/auth/AuthSheets.kt",
        f"{K}/feature/checkout/CheckoutScreen.kt", f"{K}/feature/checkout/CheckoutForm.kt",
        f"{K}/feature/checkout/CheckoutViewModel.kt", f"{K}/feature/profile/AddressFormSheet.kt",
    ],
    "android-bottom-sheets-and-dialogs": [
        f"{K}/feature/menu/PizzaBuilderSheet.kt", f"{K}/feature/cart/CartSheet.kt",
        f"{K}/app/AppRoutes.kt", f"{K}/app/PizzaApp.kt", f"{K}/app/AppViewModel.kt",
        f"{K}/feature/profile/ProfileScreen.kt", f"{K}/feature/profile/AddressFormSheet.kt",
        f"{K}/feature/menu/MenuScreen.kt",
    ],
    "android-design-system": [
        f"{K}/core/designsystem/Tokens.kt", f"{K}/core/designsystem/Theme.kt",
        f"{K}/core/designsystem/components/PizzaButton.kt",
        f"{K}/core/designsystem/components/StatusBadge.kt",
        f"{K}/core/designsystem/components/OptionPicker.kt",
        f"{K}/core/designsystem/components/StateViews.kt", f"{RES}/values/themes.xml",
    ],
    "android-networking": [
        f"{K}/data/api/PizzaApi.kt", f"{K}/core/network/Authenticated.kt",
        f"{K}/core/network/AuthInterceptor.kt", f"{K}/core/network/JsonConfig.kt",
        f"{K}/core/network/ApiConfig.kt", f"{K}/di/AppModule.kt", f"{A}/app/build.gradle.kts",
        f"{RES}/xml/network_security_config.xml",
        f"{A}/app/src/debug/res/xml/network_security_config.xml",
    ],
    "android-error-handling": [
        f"{K}/core/network/ApiError.kt", f"{K}/core/network/ApiCall.kt", f"{K}/core/util/UiState.kt",
        f"{K}/core/util/ActionOutcome.kt", f"{K}/app/ToastCenter.kt",
        f"{K}/feature/profile/ProfileViewModel.kt", f"{K}/feature/menu/MenuScreen.kt",
        f"{K}/core/designsystem/components/StateViews.kt", f"{K}/data/repository/RemoteRepositories.kt",
        f"{K}/feature/menu/MenuStore.kt", f"{K}/feature/cart/CartStore.kt",
    ],
    "android-coroutines-and-flow": [
        f"{K}/feature/menu/MenuStore.kt", f"{K}/feature/cart/CartStore.kt",
        f"{K}/feature/orders/OrderConfirmationViewModel.kt", f"{K}/feature/orders/OrdersViewModel.kt",
        f"{K}/di/ApplicationScope.kt", f"{K}/di/AppModule.kt", f"{K}/core/persistence/TokenStore.kt",
        f"{K}/feature/menu/MenuScreen.kt", f"{K}/app/AppViewModel.kt",
        f"{K}/core/persistence/SecureStore.kt",
    ],
    "android-app-architecture": [
        f"{K}/domain/repository/Repositories.kt", f"{K}/data/repository/RemoteRepositories.kt",
        f"{K}/domain/cart/CartReducer.kt", f"{K}/domain/cart/CartPricing.kt",
        f"{K}/feature/cart/CartStore.kt", f"{K}/feature/cart/CartViewModel.kt",
        f"{K}/feature/menu/MenuScreen.kt",
    ],
    "android-dependency-injection-hilt": [
        f"{K}/PizzaApplication.kt", f"{K}/MainActivity.kt", f"{K}/di/AppModule.kt",
        f"{K}/di/RepositoryModule.kt", f"{K}/di/ApplicationScope.kt", f"{K}/di/PaymentModule.kt",
        f"{K}/feature/menu/MenuStore.kt", f"{K}/feature/menu/MenuViewModel.kt",
        f"{K}/data/repository/RemoteRepositories.kt", f"{T}/di/HiltGraphTest.kt",
        f"{A}/app/build.gradle.kts", f"{IOS}/App/AppEnvironment.swift",
    ],
    "android-persistence-and-keystore": [
        f"{K}/core/persistence/StorageKey.kt", f"{K}/core/persistence/KeyValueStore.kt",
        f"{K}/core/persistence/SecureStore.kt", f"{K}/core/persistence/TokenStore.kt",
        f"{K}/core/persistence/CartIdentifierStore.kt", f"{K}/di/AppModule.kt",
        f"{RES}/xml/data_extraction_rules.xml", f"{A}/app/src/main/AndroidManifest.xml",
    ],
    "android-app-lifecycle": [
        f"{K}/PizzaApplication.kt", f"{K}/MainActivity.kt", f"{K}/app/AppViewModel.kt",
        f"{K}/feature/cart/CartStore.kt", f"{K}/feature/auth/AuthStore.kt", f"{RES}/values/themes.xml",
        f"{K}/feature/orders/OrdersScreen.kt",
        f"{A}/app/src/main/AndroidManifest.xml",
    ],
    "android-payments": [
        f"{K}/feature/checkout/payment/Payment.kt", f"{K}/feature/checkout/payment/SetupIntentReader.kt",
        f"{K}/feature/checkout/CheckoutViewModel.kt", f"{K}/feature/checkout/CheckoutScreen.kt",
        f"{K}/feature/profile/ProfileViewModel.kt", f"{K}/PizzaApplication.kt",
        f"{K}/domain/model/Order.kt", f"{IOS}/Features/Checkout/Payment/PaymentGateway.swift",
        f"{K}/feature/orders/OrderConfirmationViewModel.kt",
    ],
    "android-accessibility": [
        f"{K}/feature/menu/ProductCard.kt", f"{K}/core/designsystem/components/QuantityStepper.kt",
        f"{K}/core/designsystem/components/LabeledTextField.kt",
        f"{K}/core/designsystem/components/PizzaButton.kt",
        f"{K}/core/designsystem/components/PriceRow.kt", f"{K}/core/designsystem/components/ToastHost.kt",
        f"{K}/core/designsystem/components/StateViews.kt", f"{K}/core/designsystem/Tokens.kt",
        f"{K}/feature/checkout/CheckoutScreen.kt", f"{K}/app/PizzaApp.kt", f"{T}/ui/MenuContentTest.kt",
        f"{K}/feature/cart/CartSheet.kt", f"{K}/feature/menu/PizzaBuilderSheet.kt",
        f"{K}/core/designsystem/components/StatusBadge.kt",
    ],
    "android-testing": [
        f"{T}/domain/CartReducerTest.kt", f"{T}/data/PizzaApiTest.kt", f"{T}/feature/CartStoreTest.kt",
        f"{T}/feature/CheckoutViewModelTest.kt", f"{T}/feature/OrderAndProfileViewModelTest.kt",
        f"{T}/support/MainDispatcherRule.kt", f"{T}/support/TestDoubles.kt", f"{T}/ui/MenuContentTest.kt",
        f"{T}/feature/PizzaBuilderStateTest.kt", f"{A}/app/build.gradle.kts",
        f"{A}/app/src/test/resources/robolectric.properties",
    ],
    "android-previews-and-tooling": [
        f"{K}/feature/menu/ProductCard.kt", f"{K}/feature/home/HomeScreen.kt",
        f"{K}/feature/orders/OrdersScreen.kt", f"{K}/preview/SampleData.kt",
        f"{K}/feature/menu/MenuScreen.kt", f"{A}/app/build.gradle.kts", f"{A}/.editorconfig",
        f"{A}/gradle.properties", f"{K}/di/AppModule.kt", f"{K}/core/network/ApiCall.kt",
    ],
    "android-build-and-ship": [
        f"{A}/app/build.gradle.kts", f"{A}/app/proguard-rules.pro", f"{K}/core/network/ApiConfig.kt",
        f"{RES}/mipmap-anydpi/ic_launcher.xml", f".github/workflows/android.yml",
        f"{A}/app/src/main/AndroidManifest.xml",
    ],
    "android-interview-questions": [
        f"{K}/feature/cart/CartStore.kt", f"{K}/feature/checkout/CheckoutViewModel.kt",
        f"{K}/domain/cart/CartReducer.kt", f"{K}/feature/menu/MenuStore.kt",
        f"{K}/core/util/UiState.kt", f"{K}/feature/menu/PizzaBuilderState.kt",
    ],
}

# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
_TRACK = [
    {
        "slug": "android-get-started",
        "title": "Android – Getting Started",
        "tags": ["android", "kotlin", "gradle"],
        "excerpt": (
            "What you actually need to build an Android app, what Gradle is doing on your behalf, "
            "and the anatomy of a project — settings, the version catalog, the app module, the "
            "manifest, one Activity. Ending with the app running on an emulator against a real "
            "backend, and why the emulator calls your Mac 10.0.2.2."
        ),
    },
    {
        "slug": "android-kotlin-essentials",
        "title": "Android – The Kotlin You Need First",
        "tags": ["android", "kotlin"],
        "excerpt": (
            "Not the whole language — the parts an Android app leans on every day. Null safety, "
            "val and immutable data classes, sealed types and exhaustive when, extension functions, "
            "lambdas and the scope functions, and exceptions as the error model. With the models of "
            "a real ordering app as the running example."
        ),
    },
    {
        "slug": "android-compose-layout",
        "title": "Android – Jetpack Compose and Layout",
        "tags": ["android", "compose", "layout"],
        "excerpt": (
            "A composable is a function that describes UI, and almost everything surprising about "
            "Compose follows from that. Column, Row and Box, weight and alignment, why modifier "
            "order IS the layout, and how to build the reusable card every screen in this app is "
            "made of."
        ),
    },
    {
        "slug": "android-compose-state",
        "title": "Android – State and Recomposition",
        "tags": ["android", "compose", "state"],
        "excerpt": (
            "remember, rememberSaveable, state hoisting and StateFlow: which one to reach for, and "
            "the rule that decides it. What recomposition is and what triggers it, derivedStateOf, "
            "stateless components, and the line between state a screen owns and state the whole "
            "app owns."
        ),
    },
    {
        "slug": "android-viewmodel-and-process-death",
        "title": "Android – ViewModels, Rotation and Process Death",
        "tags": ["android", "viewmodel", "lifecycle"],
        "excerpt": (
            "The Android-only lesson. What a ViewModel survives and what it does not, why rotating "
            "the phone destroys your Activity, and the case most apps get wrong: the OS killing "
            "your process in the background and recreating the screen as if nothing happened. "
            "SavedStateHandle, rememberSaveable, and what deserves to be saved."
        ),
    },
    {
        "slug": "android-navigation",
        "title": "Android – Navigation Compose",
        "tags": ["android", "compose", "navigation"],
        "excerpt": (
            "Type-safe routes as @Serializable classes instead of strings that crash at runtime. "
            "A NavHost with a nested graph per tab, a bottom bar that remembers each tab's history, "
            "arguments read back through SavedStateHandle, and replacing checkout with the receipt "
            "so Back cannot return to a paid order."
        ),
    },
    {
        "slug": "android-lists-and-performance",
        "title": "Android – Lazy Lists and Keeping Them Fast",
        "tags": ["android", "compose", "performance"],
        "excerpt": (
            "LazyColumn versus a Column in a scroll, keys and why a missing one is a state bug, "
            "contentType, pull-to-refresh, and how Compose decides what to skip — stability, "
            "@Stable and @Immutable, lambdas, and the few things you still have to do yourself."
        ),
    },
    {
        "slug": "android-forms-and-input",
        "title": "Android – Forms, Text Input and Validation",
        "tags": ["android", "compose", "forms"],
        "excerpt": (
            "The keyboard is part of your UI. KeyboardOptions and IME actions, moving focus "
            "between fields, input filtering, imePadding so the button is not hidden, error "
            "semantics for TalkBack, and a validation model that keeps the rules out of the "
            "composable and testable on the JVM."
        ),
    },
    {
        "slug": "android-bottom-sheets-and-dialogs",
        "title": "Android – Bottom Sheets and Dialogs",
        "tags": ["android", "compose", "sheets"],
        "excerpt": (
            "In Compose a sheet is shown by being composed and dismissed by leaving composition. "
            "ModalBottomSheet and its state, skipPartiallyExpanded, AlertDialog for destructive "
            "actions, resetting a form for free with keyed state, and the one nullable enum that "
            "makes two sheets at once impossible."
        ),
    },
    {
        "slug": "android-design-system",
        "title": "Android – Building a Design System with Material 3",
        "tags": ["android", "compose", "material"],
        "excerpt": (
            "Tokens, a semantic layer and components — and where Material 3's ColorScheme fits in "
            "that, where it runs out, and how a CompositionLocal fills the gap. The window theme "
            "versus the Compose theme, dynamic colour and why this app turns it off, and a button "
            "that prevents the double-submitted order."
        ),
    },
    {
        "slug": "android-networking",
        "title": "Android – Networking with Retrofit and OkHttp",
        "tags": ["android", "kotlin", "networking"],
        "excerpt": (
            "Retrofit interfaces as the API surface, OkHttp interceptors for the token, "
            "kotlinx.serialization and the three settings that bite, the base URL from build "
            "configuration rather than code, and why plain HTTP to your dev machine fails until "
            "you write a network security config."
        ),
    },
    {
        "slug": "android-error-handling",
        "title": "Android – Error Handling That Users Can Act On",
        "tags": ["android", "kotlin", "errors"],
        "excerpt": (
            "One sealed ApiError whose cases are decisions, one place that maps every library "
            "exception onto it, the CancellationException you must never swallow, UiState instead "
            "of three booleans, and ActionOutcome for writes — including the cancelled case that a "
            "Result has nowhere to put."
        ),
    },
    {
        "slug": "android-coroutines-and-flow",
        "title": "Android – Coroutines and Flow",
        "tags": ["android", "kotlin", "coroutines"],
        "excerpt": (
            "Structured concurrency on Android: viewModelScope, an application scope for work that "
            "must outlive a screen, async for parallel requests, cancellation as a debounce, a "
            "polling loop that stops itself, Mutex instead of synchronized, and StateFlow with "
            "stateIn and collectAsStateWithLifecycle."
        ),
    },
    {
        "slug": "android-app-architecture",
        "title": "Android – App Architecture",
        "tags": ["android", "architecture"],
        "excerpt": (
            "Layers with dependencies pointing inwards: repository interfaces in the domain, Retrofit "
            "in the data layer, a pure reducer for the rules and a store for the effects, and "
            "unidirectional data flow from StateFlow to screen and back. With the parts of Google's "
            "guide this app follows and the parts it skips."
        ),
    },
    {
        "slug": "android-dependency-injection-hilt",
        "title": "Android – Dependency Injection with Hilt",
        "tags": ["android", "hilt", "architecture"],
        "excerpt": (
            "What Hilt actually generates, @Inject constructors, modules with @Provides and @Binds, "
            "components and scopes as lifetimes, qualifiers, @HiltViewModel, and swapping the "
            "network for fakes in a test — set against the hand-written composition root the iOS "
            "version of this app uses instead."
        ),
    },
    {
        "slug": "android-persistence-and-keystore",
        "title": "Android – DataStore and the Keystore",
        "tags": ["android", "persistence", "security"],
        "excerpt": (
            "Where each thing an app remembers belongs. DataStore and why it replaced "
            "SharedPreferences, encrypting a token with an Android Keystore key that never leaves "
            "the device, why EncryptedSharedPreferences is no longer the answer, and backup rules "
            "that keep secrets off other phones."
        ),
    },
    {
        "slug": "android-app-lifecycle",
        "title": "Android – The App Lifecycle",
        "tags": ["android", "lifecycle"],
        "excerpt": (
            "What Android does to your app when it leaves the screen, and the two problems the web "
            "never has: saving work before the process is killed, and not knowing who is signed in "
            "for the first few milliseconds. ProcessLifecycleOwner, the splash screen API, and a "
            "launch sequence whose order is load-bearing."
        ),
    },
    {
        "slug": "android-payments",
        "title": "Android – Payments with Stripe PaymentSheet",
        "tags": ["android", "payments", "stripe"],
        "excerpt": (
            "Create the order, then pay — and why the device is never the authority on price. "
            "Stripe's PaymentSheet in Compose, why a ViewModel cannot hold it, events as state, "
            "saving a card with a SetupIntent, and asking the server whether the payment really "
            "settled."
        ),
    },
    {
        "slug": "android-accessibility",
        "title": "Android – Accessibility in Compose",
        "tags": ["android", "compose", "accessibility"],
        "excerpt": (
            "The semantics tree is what TalkBack reads, and it is what your UI tests read too. "
            "contentDescription, mergeDescendants and the trap in it, roles and state "
            "descriptions, one adjustable control instead of three nodes, live regions, headings, "
            "and 48dp touch targets."
        ),
    },
    {
        "slug": "android-testing",
        "title": "Android – Testing",
        "tags": ["android", "testing"],
        "excerpt": (
            "What is worth testing in an Android app and where each test runs. Pure JVM tests for "
            "the rules, MockWebServer for the network, virtual time for debounces and polling, "
            "ViewModels with a test Main dispatcher, Robolectric when Android is genuinely needed, "
            "and Compose UI tests through the semantics tree."
        ),
    },
    {
        "slug": "android-previews-and-tooling",
        "title": "Android – Previews, Lint and Tooling",
        "tags": ["android", "tooling"],
        "excerpt": (
            "Compose previews that render without a backend, and the screen/content split that "
            "makes them possible. Android Lint as a build gate, .editorconfig and ktlint, Gradle "
            "properties that matter, and what to reach for when the app is slow."
        ),
    },
    {
        "slug": "android-build-and-ship",
        "title": "Android – Building and Shipping",
        "tags": ["android", "release", "gradle"],
        "excerpt": (
            "Build types and BuildConfig, R8 and why the release build is the only one that can "
            "crash on a missing keep rule, signing with an upload key that never touches Git, App "
            "Bundles, a CI workflow, and what Play Console review actually asks of you."
        ),
    },
    {
        "slug": "android-interview-questions",
        "title": "Android – Interview Questions",
        "tags": ["android", "kotlin", "interview"],
        "excerpt": (
            "The questions an Android role actually asks, answered against the lessons before this "
            "one. Activity versus ViewModel lifetimes, process death, recomposition and stability, "
            "StateFlow versus LiveData, structured concurrency, Hilt scopes, and how you would make "
            "a screen testable. Short answers, with the reasoning."
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

FROZEN_SLUGS: set[str] = set()

NEW_SLUGS = {e["slug"] for e in _TRACK}

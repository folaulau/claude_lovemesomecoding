"""The Vue track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and the last lesson is the
newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because
this track is authored before it is published: when the publish date is finally
known, move START_DATE and every lesson re-bases in order. Same choice the
Angular manifest made, and for the same reason.

EVERY SLUG HERE IS NEW. `/vue` does not exist on the live site — there are 42
categories and none of them is Vue — so unlike the React and Angular tracks
there is no indexed URL to preserve and no `--force-dates` dance on the first
publish. That also means the category itself is created by the first seed.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "vue",
    "name": "Vue",
    "description": (
        "Vue 3 from the ground up — single-file components, the Composition API and reactivity, "
        "props and events, composables, Pinia, Vue Router, forms and shipping to production, "
        "every example lifted from a real short-video CMS."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, where `vue` has to be added
# to the JavaScript group or the category is reachable only by direct URL.
NAV_GROUP = "JavaScript"

# The app every code sample is taken from, so a reader can go and see the whole
# thing in context rather than a fragment invented for the tutorial.
#
# NOTE this is NOT the pizza app the React and Angular tracks use. There is no
# Vue pizza frontend; ReelCMS is the app that is actually written in Vue, and it
# is a better fit anyway — a vertical video feed exercises lifecycle hooks,
# template refs and IntersectionObserver far harder than a menu page does.
DEMO_APP = "lovemesomecoding_demo_project/reelcms/reelcms-vue-frontend"

# The versions the whole track is written against. Lesson 1 prints this table,
# and every other lesson assumes it.
#
# These are READ OFF THE DEMO APP, not chosen — a lesson claiming a version the
# snippet was not copied from is exactly the kind of drift nobody spots later.
VERSIONS = {
    "vue": "3.5.41",
    "vite": "8.2.2",
    "@vitejs/plugin-vue": "6.0.8",
    "vue-router": "4.6.4",
    "pinia": "4.0.3",
    "bootstrap": "5.3.8",
    "chart.js / vue-chartjs": "4.5.1 / 5.3.4",
    "node": "22",
}

# ⚠️ The demo app is plain JavaScript, NOT TypeScript.
#
# The React track is TSX and the Angular track is TypeScript throughout. This one
# is not, because ReelCMS is not — and snippets are copied verbatim so that
# check_snippets.py can prove they are real. Lesson 1 says so explicitly rather
# than letting a reader arriving from /react assume otherwise, and the tooling
# lessons mention `vue-tsc` as the typed path without pretending the app uses it.
SNIPPET_LANGUAGE = "javascript"

# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later,
# so the pager reads lesson 1 -> lesson 28. Re-base the whole track by editing
# these two values; nothing else needs to change.
START_DATE = datetime(2026, 9, 1, 9, 0, 0)
STEP_DAYS = 3


def _date(index: int) -> str:
    """The publish timestamp for the index-th lesson, 0-based."""
    return (START_DATE + timedelta(days=STEP_DAYS * index)).strftime("%Y-%m-%dT%H:%M:%S")


# Authored in reading order. `source` is documentation, not data: it records
# which part of the demo app the lesson's snippets come from, so a reviewer can
# check a lesson against the code without reading the whole app.
_TRACK = [
    # ------------------------------------------------------------- start here
    {
        "slug": "vue-get-started",
        "part": "Getting started",
        "title": "Vue – Get Started",
        "tags": ["vue", "javascript"],
        "source": "the track index; the versions table",
        "excerpt": (
            "Start here. What Vue is and what problem it solves, how it compares to React and "
            "Angular and when a team picks it, the exact versions this track is written against "
            "— Vue 3.5, Vite 8, Pinia, Vue Router 4 — one command to create a project and see it "
            "running, the demo application every example is taken from, and the full lesson "
            "index in reading order."
        ),
    },
    {
        "slug": "vue-set-up",
        "title": "Vue – Set Up a Project with Vite",
        "tags": ["vue", "vite", "javascript"],
        "source": "package.json, vite.config.js, index.html, src/main.js",
        "excerpt": (
            "One command scaffolds the project: what `npm create vue@latest` generates, what each "
            "file is for, how `index.html` is the real entry point under Vite, what "
            "`createApp(App).use(pinia).use(router).mount('#app')` is actually doing, the dev "
            "server and its proxy, and the handful of npm scripts you will run every day."
        ),
    },
    {
        "slug": "vue-sfc",
        "title": "Vue – The Single-File Component",
        "tags": ["vue", "components", "javascript"],
        "source": "components/ui/EmptyState.vue, components/ui/AppToast.vue",
        "excerpt": (
            "A `.vue` file holds a template, a script and a style block, and that co-location is "
            "the whole idea. What `<script setup>` compiles to and why it replaced `export "
            "default`, why `<style scoped>` does not leak, when a component needs a name, and how "
            "the build turns three blocks in one file into a render function."
        ),
    },
    {
        "slug": "vue-template-syntax",
        "title": "Vue – Template Syntax and Directives",
        "tags": ["vue", "templates", "javascript"],
        "source": "components/public/ReelCard.vue, components/ui/StatusBadge.vue",
        "excerpt": (
            "Everything you can write in a template. Text interpolation and what expressions are "
            "allowed inside `{{ }}`, attribute binding with `v-bind` and its `:` shorthand, "
            "`v-on` and `@`, dynamic `:class` and `:style` — object, array and the template "
            "literal form the demo app uses for Bootstrap variants — plus `v-html` and the "
            "injection risk that comes with it."
        ),
    },
    # -------------------------------------------------------------- reactivity
    {
        "slug": "vue-reactivity",
        "part": "Reactivity",
        "title": "Vue – Reactivity: ref and reactive",
        "tags": ["vue", "reactivity", "javascript"],
        "source": "stores/toast.js, views/public/FeedView.vue",
        "excerpt": (
            "The core of Vue. Why `ref()` needs `.value` in script but not in a template, how "
            "`reactive()` differs and the three ways it will surprise you — destructuring, "
            "reassignment and primitives — the rule this track follows (`ref` for everything "
            "unless you have a reason), and what actually happens when a dependency changes."
        ),
    },
    {
        "slug": "vue-computed",
        "title": "Vue – Computed Properties",
        "tags": ["vue", "reactivity", "javascript"],
        "source": "stores/auth.js (isAuthenticated, isAdmin), components/public/ReelPlayer.vue",
        "excerpt": (
            "Derived state that caches. Why a computed beats a method for anything a template "
            "reads more than once, how caching is invalidated, writable computeds with a getter "
            "and a setter, and the rule that keeps them predictable — a computed must be pure, "
            "so anything that fetches or mutates belongs in a watcher instead."
        ),
    },
    {
        "slug": "vue-watchers",
        "title": "Vue – Watchers: watch and watchEffect",
        "tags": ["vue", "reactivity", "javascript"],
        "source": "views/public/ExploreView.vue, components/public/ReelPlayer.vue",
        "excerpt": (
            "For the side effects a computed must not do. `watch` with a getter source, the "
            "`immediate` and `deep` options and what each really costs, `watchEffect` and how it "
            "collects dependencies for you, cleaning up so a stale request cannot overwrite a "
            "fresh one, and the demo app's rule that the URL — not component state — is the "
            "single source of truth a watcher reacts to."
        ),
    },
    {
        "slug": "vue-list-rendering",
        "title": "Vue – Conditional and List Rendering",
        "tags": ["vue", "templates", "javascript"],
        "source": "views/public/ExploreView.vue, components/admin/TagInput.vue",
        "excerpt": (
            "`v-if` versus `v-show` and which one to reach for, `v-else-if` and `v-else`, `v-for` "
            "over arrays and objects, and `:key` — what it is for, why an index is usually the "
            "wrong choice, and the class of bug that only appears once you reorder or delete. "
            "Also why `v-if` and `v-for` on the same element is a mistake Vue now warns about."
        ),
    },
    # -------------------------------------------------------------- components
    {
        "slug": "vue-components",
        "part": "Components",
        "title": "Vue – Components",
        "tags": ["vue", "components", "javascript"],
        "source": "components/ui/*, layouts/PublicLayout.vue",
        "excerpt": (
            "Breaking a page into pieces. Importing and using a component with `<script setup>` "
            "and no registration step, naming and casing in templates, where components live in "
            "a project that has grown past a dozen of them, and how the demo app splits `ui/`, "
            "`public/` and `admin/` so that a component's folder tells you who is allowed to "
            "use it."
        ),
    },
    {
        "slug": "vue-props",
        "title": "Vue – Props",
        "tags": ["vue", "components", "props", "javascript"],
        "source": "components/ui/EmptyState.vue, components/public/ReelPlayer.vue",
        "excerpt": (
            "Passing data down. `defineProps` with an object declaration, types, `required`, "
            "`default` and the function form every object and array default needs, why props are "
            "one-way and what to do instead of mutating one, prop casing between template and "
            "script, and reading a prop in script versus in a template."
        ),
    },
    {
        "slug": "vue-events",
        "title": "Vue – Events and Emits",
        "tags": ["vue", "components", "events", "javascript"],
        "source": "components/public/ReelPlayer.vue, components/admin/TagInput.vue",
        "excerpt": (
            "Passing messages back up. `defineEmits` and why declaring events is worth the line, "
            "emitting with a payload, event modifiers — `.prevent`, `.stop`, `.once`, `.self` — "
            "and key modifiers like the `@keydown.enter.prevent` the tag editor uses, plus why "
            "a child emits a request rather than reaching up and changing something itself."
        ),
    },
    {
        "slug": "vue-v-model",
        "title": "Vue – v-model and Two-Way Binding",
        "tags": ["vue", "forms", "javascript"],
        "source": "components/admin/TagInput.vue, views/admin/ReelEditView.vue",
        "excerpt": (
            "What `v-model` desugars to on an input, its `.lazy`, `.number` and `.trim` "
            "modifiers, and then the part that matters: `v-model` on your own component. The "
            "`modelValue` prop and `update:modelValue` event the demo app's tag editor "
            "implements by hand, named models for multiple bindings, and `defineModel` — the "
            "3.4+ shorthand that collapses all of it into one line."
        ),
    },
    {
        "slug": "vue-slots",
        "title": "Vue – Slots",
        "tags": ["vue", "components", "javascript"],
        "source": "components/ui/EmptyState.vue",
        "excerpt": (
            "Letting a caller pass markup in, not just data. The default slot and fallback "
            "content, named slots and the `#name` shorthand, scoped slots that hand data back "
            "out to the caller, and how to tell when a problem wants a slot rather than another "
            "prop — the question is whether the parent is deciding *what it looks like* or "
            "*what it says*."
        ),
    },
    {
        "slug": "vue-lifecycle",
        "title": "Vue – Lifecycle Hooks and Template Refs",
        "tags": ["vue", "lifecycle", "javascript"],
        "source": "views/public/FeedView.vue, components/public/ReelPlayer.vue",
        "excerpt": (
            "When your code runs. `onMounted`, `onBeforeUnmount` and the ones in between, why "
            "every listener, timer and observer you create needs an unmount that undoes it, "
            "template refs for reaching a real DOM node — the `<video>` element the player "
            "controls — refs inside a `v-for`, and `nextTick` for the moment after the DOM has "
            "caught up with your data."
        ),
    },
    # --------------------------------------------------- reusing logic & state
    {
        "slug": "vue-composables",
        "part": "Reusing logic and state",
        "title": "Vue – Composables: Reusing Logic",
        "tags": ["vue", "composables", "javascript"],
        "source": "utils/format.js and logic extracted from FeedView/ExploreView",
        "excerpt": (
            "The pattern that replaced mixins and the single most useful thing the Composition "
            "API bought. What makes a function a composable, the `useX` naming convention, "
            "returning refs so the caller keeps reactivity, accepting refs or getters as "
            "arguments, cleaning up inside one, and where custom directives fit as the other "
            "half of Vue's reusability story."
        ),
    },
    {
        "slug": "vue-provide-inject",
        "title": "Vue – provide and inject",
        "tags": ["vue", "components", "javascript"],
        "source": "layouts/AdminLayout.vue",
        "excerpt": (
            "Getting a value to a deep descendant without threading it through every component "
            "in between. `provide` and `inject`, injection keys and why a Symbol beats a string, "
            "default values, keeping provided state readonly so a child cannot silently rewrite "
            "it, and the honest comparison with Pinia — which one a piece of shared state "
            "actually belongs in."
        ),
    },
    {
        "slug": "vue-pinia",
        "title": "Vue – State Management with Pinia",
        "tags": ["vue", "pinia", "state-management", "javascript"],
        "source": "stores/auth.js, stores/toast.js, components/ui/AppToast.vue",
        "excerpt": (
            "App-wide state, the official way. Setup stores versus option stores and why this "
            "track uses setup stores, state as refs, getters as computeds and actions as plain "
            "functions, `storeToRefs` and the destructuring bug it exists to prevent, using a "
            "store outside a component, and how the demo app's auth store survives a refresh "
            "without trusting anything it cached."
        ),
    },
    {
        "slug": "vue-options-api",
        "title": "Vue – The Options API (and Why This Track Uses the Composition API)",
        "tags": ["vue", "javascript"],
        "source": "a Composition-API component from the app, rewritten both ways",
        "excerpt": (
            "You will meet the Options API in every Vue 2 codebase and plenty of Vue 3 ones, so "
            "you need to read it. `data`, `methods`, `computed`, `watch` and the lifecycle "
            "options, what `this` binds to and why arrow functions break it, the same component "
            "written both ways side by side, and a straight answer on which to use for new work "
            "— after which this track does not use it again."
        ),
    },
    # ----------------------------------------------------- routing, forms, data
    {
        "slug": "vue-router",
        "part": "Routing, forms and data",
        "title": "Vue – Routing with Vue Router",
        "tags": ["vue", "vue-router", "javascript"],
        "source": "router/index.js, layouts/PublicLayout.vue, layouts/AdminLayout.vue",
        "excerpt": (
            "Turning one page into an application. `createRouter` and history mode, "
            "`<RouterLink>` and `<RouterView>`, route params and `useRoute`, nested routes and "
            "the layout trick the demo app uses to serve a public site and an admin console from "
            "one build, named routes, the catch-all 404, and lazy route components that keep the "
            "first load small."
        ),
    },
    {
        "slug": "vue-router-guards",
        "title": "Vue – Route Guards and Navigation",
        "tags": ["vue", "vue-router", "javascript"],
        "source": "router/index.js (beforeEach, afterEach, scrollBehavior), stores/auth.js",
        "excerpt": (
            "Deciding who gets in. `beforeEach` and returning a redirect, `meta` fields that mark "
            "a route as needing auth or an admin role, sending someone to the login page and "
            "bouncing them back to where they were going, `afterEach` for the document title, "
            "per-route and in-component guards, and `scrollBehavior` — including when to switch "
            "it off."
        ),
    },
    {
        "slug": "vue-forms",
        "title": "Vue – Forms and Validation",
        "tags": ["vue", "forms", "javascript"],
        "source": "views/admin/LoginView.vue, views/admin/ReelEditView.vue",
        "excerpt": (
            "A real form, end to end. Binding every input type, a submit handler that cannot "
            "double-fire, disabling the button while a request is in flight, client-side checks "
            "and why they are a convenience rather than a guarantee, and — the part tutorials "
            "skip — rendering the field errors the server sends back next to the fields they "
            "belong to."
        ),
    },
    {
        "slug": "vue-http",
        "title": "Vue – Fetching Data from an API",
        "tags": ["vue", "http", "javascript"],
        "source": "api/index.js, api/http.js, api/session.js",
        "excerpt": (
            "Talking to a backend without scattering `fetch` through thirty components. One "
            "module that owns the transport, loading and error state that the UI can actually "
            "render, a typed error that separates \"the API is down\" from \"your password is "
            "wrong\", attaching a JWT and handling a 401 in exactly one place, and the mock "
            "implementation that lets the UI be built before the API exists."
        ),
    },
    # ------------------------------------------------------ advanced & shipping
    {
        "slug": "vue-transitions-and-teleport",
        "part": "Advanced features and shipping",
        "title": "Vue – Transitions and Teleport",
        "tags": ["vue", "animation", "javascript"],
        "source": "components/ui/AppToast.vue (TransitionGroup), an admin confirm modal",
        "excerpt": (
            "Two small features that solve disproportionately annoying problems. `<Transition>` "
            "and the six CSS classes it toggles, `<TransitionGroup>` for a list that gains and "
            "loses items — the toast stack — and `<Teleport>`, which renders a modal at the end "
            "of `<body>` so it stops being clipped by whatever `overflow` and `z-index` its "
            "parent happened to set."
        ),
    },
    {
        "slug": "vue-async-components",
        "title": "Vue – Async Components, Suspense and KeepAlive",
        "tags": ["vue", "performance", "javascript"],
        "source": "router/index.js (lazy routes), the admin dashboard's charts",
        "excerpt": (
            "Not shipping everything on the first load. `defineAsyncComponent` with loading and "
            "error components, route-level code splitting and what Vite actually emits, "
            "`<Suspense>` and its still-experimental status, and `<KeepAlive>` for the tab or "
            "list that should not throw away its state and refetch every time you navigate back "
            "to it."
        ),
    },
    {
        "slug": "vue-performance",
        "title": "Vue – Performance",
        "tags": ["vue", "performance", "javascript"],
        "source": "views/public/FeedView.vue (IntersectionObserver, cursor pagination)",
        "excerpt": (
            "Making it fast, and knowing whether it was slow. Where re-renders actually come "
            "from, `v-once` and `v-memo`, `shallowRef` for a large object you replace rather "
            "than edit, why an IntersectionObserver beats a scroll listener, cursor pagination "
            "instead of offset, keeping heavy work out of computeds, and reading a flame chart "
            "in Vue DevTools before changing anything."
        ),
    },
    {
        "slug": "vue-testing",
        "title": "Vue – Testing with Vitest and Vue Test Utils",
        "tags": ["vue", "testing", "vitest", "javascript"],
        "source": "tests/ — Playwright e2e, plus the Vitest unit suite this track adds",
        "excerpt": (
            "Tests you will keep running. Vitest and why a Vite project gets it almost for free, "
            "mounting a component with Vue Test Utils, asserting on rendered output rather than "
            "internals, testing props and emitted events, `flushPromises` for anything async, "
            "testing a Pinia store on its own, and where an end-to-end Playwright test earns its "
            "much higher cost."
        ),
    },
    {
        "slug": "vue-deployment",
        "title": "Vue – Building and Deploying to Production",
        "tags": ["vue", "vite", "deployment", "javascript"],
        "source": "vite.config.js, .env, dist/, the app's Docker/nginx setup",
        "excerpt": (
            "The last mile. What `vite build` produces and how to read the output, environment "
            "variables with `import.meta.env` and the `VITE_` prefix that decides what gets "
            "baked into a public bundle, the history-mode rewrite rule every static host needs "
            "or your routes 404 on refresh, cache headers for hashed assets, and a GitHub "
            "Actions workflow that ships it."
        ),
    },
    {
        "slug": "vue-interview-questions",
        "title": "Vue – Interview Questions",
        "tags": ["vue", "interview", "javascript"],
        "source": "the whole track",
        "excerpt": (
            "The questions Vue interviews actually ask, answered the way you would say them out "
            "loud. `ref` versus `reactive`, computed versus watch, how the reactivity system "
            "tracks a dependency, what `<script setup>` compiles to, why `:key` matters, props "
            "down and events up, Pinia versus provide/inject, and the Composition-versus-Options "
            "question that is really asking whether you have shipped Vue or only read about it."
        ),
    },
]

# `part` is written on the first lesson of each section only; carry it forward so
# every entry has one. The lesson index in lesson 1 is GENERATED from this
# grouping (gen_index.py) rather than hand-maintained, because a hand-written
# index of 28 links drifts the first time a lesson is inserted.
_part = None
for _entry in _TRACK:
    _part = _entry.get("part", _part)
    _entry["part"] = _part

# Slug -> filename, and the dates, are derived so a reorder is one edit.
POSTS = [
    {
        "slug": entry["slug"],
        "title": entry["title"],
        "file": f"{i + 1:02d}-{entry['slug']}.html",
        "date": _date(i),
        "tags": entry["tags"],
        "excerpt": entry["excerpt"],
        "source": entry["source"],
        "part": entry["part"],
    }
    for i, entry in enumerate(_TRACK)
]

# Every slug in this track is new — /vue does not exist on the live site — so
# nothing here is frozen. Kept so check_content.py reads the same as the React
# and Angular checkers, and so the day a Vue post IS indexed there is an obvious
# place to record it.
FROZEN_SLUGS: set[str] = set()

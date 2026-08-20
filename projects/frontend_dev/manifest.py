"""The Frontend Dev track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and post 12 is the newest.

Both pre-existing slugs were published on 2019-02-06 and are indexed. They are
being rewritten in place, NOT replaced: changing either of those slugs changes a
live URL. That is why posts 2 and 5 carry names that read oddly for their
position — `...-what-is-a-frontend-engineer` and
`...-what-to-learn-in-a-framework-as-a-frontend-engineer` are fixed. The other
10 are new and named to match the /backend-dev track.

Because the old posts carry a 2019 date and `upsert_post` never overwrites an
existing date, seeding this track needs `seed.py --force-dates` for the reading
order to come out right. See progress_report.md.

The 12:00 stamps are deliberate. Four other tracks date their posts over an
overlapping range — /react and /spring-boot at 09:00 (62 posts between them),
/data-structure-algorithm at 10:00, /backend-dev at 11:00 and
/spring-study-guide at 14:00 — and an exact tie makes the archive order
arbitrary. 12:00 is free.
"""

CATEGORY = {
    "slug": "frontend-dev",
    "name": "Frontend Development",
    "description": (
        "What a frontend engineer actually does, and what you need to learn to become one — the "
        "browser, HTML and CSS, JavaScript and TypeScript, a component framework, state, talking "
        "to a backend, routing and forms, security, performance and accessibility, testing, and "
        "shipping it. A roadmap that names the order and then points you at the deeper tracks. "
        "Every example is real React 19 and TypeScript from a working pizza ordering app."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, which already maps this slug
# to the display name "Frontend Development" under the "Software Engineering"
# group — so this track needs no nav change.
NAV_GROUP = "Software Engineering"

# The app every code sample is taken from, so a reader can go and see the whole
# thing in context rather than a fragment invented for the post.
DEMO_APP = "lovemesomecoding_demo_project/pizza/pizza-react-frontend"

# Stated on the landing page and assumed by every other post. Read off the demo
# app's package.json — when it moves, the landing page's table is the first edit.
VERSIONS = {
    "react": "19.2.8",
    "typescript": "6.0.2",
    "vite": "8.2.0",
    "react-router": "7.18.2",
    "redux-toolkit": "2.12.0",
    "bootstrap": "5.3.8",
    "playwright": "1.62.1",
    "sass": "1.102.0",
}

# The sibling tracks this one deliberately does NOT duplicate. Every post that
# names a topic these cover should link out rather than re-teach it.
LINKS_OUT = {
    "react": 27,
    "css": 21,
    "javascript": 19,
    "html": 12,
    "backend-dev": 10,
    "system-design": 7,
    "rea-native": 5,
}

POSTS = [
    {
        "slug": "frontend-dev-get-started",
        "title": "Frontend Dev – Get Started",
        "file": "01-frontend-dev-get-started.html",
        "date": "2026-08-01T12:00:00",
        "tags": ["frontend", "career", "react", "typescript"],
        "excerpt": (
            "Start here. What a frontend engineer builds, the twelve things you need to learn and "
            "the order to learn them in, and the exact stack every example in this track uses — "
            "React 19, TypeScript and Vite. Also: how this track fits with the deeper ones on the "
            "site, so you know when to stop reading here and go read those instead."
        ),
    },
    {
        "slug": "frontend-dev-what-is-a-frontend-engineer",
        "title": "Frontend Dev – What a Frontend Engineer Actually Does",
        "file": "02-frontend-dev-what-is-a-frontend-engineer.html",
        "date": "2026-08-03T12:00:00",
        "tags": ["frontend", "career", "ux", "api"],
        "excerpt": (
            "The job, described by what lands in your queue rather than by a job posting. What you "
            "own — the interface, the state behind it, what happens on a slow phone, and whether "
            "somebody using a keyboard can get through it — where the line sits between you and "
            "design, backend and QA, and what a real ticket looks like from mockup to deploy."
        ),
    },
    {
        "slug": "frontend-dev-html-css-and-the-browser",
        "title": "Frontend Dev – The HTML, CSS and Browser You Actually Need",
        "file": "03-frontend-dev-html-css-and-the-browser.html",
        "date": "2026-08-05T12:00:00",
        "tags": ["frontend", "html", "css", "browser"],
        "excerpt": (
            "The platform underneath every framework. What the browser does with your page — DOM, "
            "CSSOM, layout, paint — why semantic HTML decides what a screen reader and Google can "
            "see, and the small part of CSS that carries most real layouts: the box model, "
            "flexbox, grid, the cascade and custom properties."
        ),
    },
    {
        "slug": "frontend-dev-javascript-and-typescript",
        "title": "Frontend Dev – The JavaScript and TypeScript You Actually Need",
        "file": "04-frontend-dev-javascript-and-typescript.html",
        "date": "2026-08-07T12:00:00",
        "tags": ["frontend", "javascript", "typescript", "async"],
        "excerpt": (
            "The subset of the language that matters in a component app, which is not the subset a "
            "beginner course teaches. Immutable updates, the async model that makes a spinner "
            "possible, modules, and the handful of TypeScript ideas that catch real bugs — typing "
            "the API response, discriminated unions for loading state, and why `any` is a loss."
        ),
    },
    {
        "slug": "frontend-dev-what-to-learn-in-a-framework-as-a-frontend-engineer",
        "title": "Frontend Dev – What to Learn in a Framework",
        "file": "05-frontend-dev-what-to-learn-in-a-framework.html",
        "date": "2026-08-09T12:00:00",
        "tags": ["frontend", "react", "framework", "components"],
        "excerpt": (
            "The small part of a big framework you use every day. Components and props, the render "
            "model, effects and when you do not need one, composition over configuration, and the "
            "project-level concerns every framework makes you answer — structure, dependencies, "
            "and per-environment configuration. React here, but the checklist is portable."
        ),
    },
    {
        "slug": "frontend-dev-state-management",
        "title": "Frontend Dev – State Management",
        "file": "06-frontend-dev-state-management.html",
        "date": "2026-08-11T12:00:00",
        "tags": ["frontend", "react", "redux", "state"],
        "excerpt": (
            "Where a value should live, which is the question most frontend bugs are really about. "
            "Local state, lifting up, context, and a store — and the honest criteria for moving "
            "between them. Includes a real app that uses context on one half and Redux on the "
            "other, and the documented reason the line runs where it does."
        ),
    },
    {
        "slug": "frontend-dev-talking-to-the-backend",
        "title": "Frontend Dev – Talking to the Backend",
        "file": "07-frontend-dev-talking-to-the-backend.html",
        "date": "2026-08-13T12:00:00",
        "tags": ["frontend", "api", "http", "fetch"],
        "excerpt": (
            "One request has four outcomes and beginners handle one of them. Building a single API "
            "layer instead of scattering fetch calls, turning an error response into something a "
            "component can render, loading and error and empty states, cancelling a request that "
            "no longer matters, and why CORS fails the way it does."
        ),
    },
    {
        "slug": "frontend-dev-routing-and-forms",
        "title": "Frontend Dev – Routing, Forms and Validation",
        "file": "08-frontend-dev-routing-and-forms.html",
        "date": "2026-08-15T12:00:00",
        "tags": ["frontend", "react-router", "forms", "validation"],
        "excerpt": (
            "The URL is state, and forms are where most of your users actually touch the app. "
            "Routes, nested layouts, guarded routes and the redirect-back pattern; then controlled "
            "inputs, what the browser validates for free, where validation has to be repeated on "
            "the server, and how to show a field error that came back from an API."
        ),
    },
    {
        "slug": "frontend-dev-auth-and-security",
        "title": "Frontend Dev – Authentication and Security in the Browser",
        "file": "09-frontend-dev-auth-and-security.html",
        "date": "2026-08-17T12:00:00",
        "tags": ["frontend", "security", "auth", "jwt"],
        "excerpt": (
            "Everything the browser runs is public, so a frontend guard is a courtesy and never a "
            "control. Login flows, where to put a token and the real trade between localStorage "
            "and an HttpOnly cookie, restoring a session on refresh, XSS and CSRF in the terms "
            "that actually bite, and what a Content-Security-Policy buys you."
        ),
    },
    {
        "slug": "frontend-dev-performance-and-accessibility",
        "title": "Frontend Dev – Performance and Accessibility",
        "file": "10-frontend-dev-performance-and-accessibility.html",
        "date": "2026-08-19T12:00:00",
        "tags": ["frontend", "performance", "accessibility", "a11y"],
        "excerpt": (
            "Two subjects in one post because they are the same subject: whether the person on the "
            "other end can actually use this. Bundle size and code splitting, the render cost you "
            "can measure, images, Core Web Vitals — then semantics, labels, focus order, keyboard "
            "operation and contrast, and the four checks that catch most of it."
        ),
    },
    {
        "slug": "frontend-dev-testing",
        "title": "Frontend Dev – Testing",
        "file": "11-frontend-dev-testing.html",
        "date": "2026-08-21T12:00:00",
        "tags": ["frontend", "testing", "playwright", "e2e"],
        "excerpt": (
            "How you change code you did not write without being afraid. What is worth testing in "
            "a UI and what is not, testing what the user sees rather than what the component "
            "holds, querying by role so a test breaks when the app breaks and not when a class "
            "name changes, and where end-to-end tests earn their keep."
        ),
    },
    {
        "slug": "frontend-dev-build-and-deployment",
        "title": "Frontend Dev – Build Tooling and Deployment",
        "file": "12-frontend-dev-build-and-deployment.html",
        "date": "2026-08-23T12:00:00",
        "tags": ["frontend", "vite", "deployment", "ci"],
        "excerpt": (
            "What happens between your source and the files a browser downloads, and how those "
            "files get somewhere real. Bundling, the dev server, environment variables and why "
            "they are not secret, static hosting on a CDN, cache headers and content hashing, the "
            "SPA fallback that 404s every deep link if you forget it, and a CI pipeline worth having."
        ),
    },
]

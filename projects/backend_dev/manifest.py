"""The Backend Dev track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and post 10 is the newest.

Both pre-existing slugs were published on 2020-01-19 and are indexed. They are
being rewritten in place, NOT replaced: changing either of those slugs changes a
live URL. The other 8 are new.

Because the old posts carry a 2020 date and `upsert_post` never overwrites an
existing date, seeding this track needs `seed.py --force-dates` for the reading
order to come out right. See progress_report.md.

The 11:00 stamps are deliberate. Three other tracks date their posts over an
overlapping range — /spring-boot at 09:00, the DS&A track at 10:00 and
/spring-study-guide at 14:00 — and an exact tie makes the archive order arbitrary.
"""

CATEGORY = {
    "slug": "backend-dev",
    "name": "Backend Development",
    "description": (
        "What a Java backend engineer actually does, and what you need to learn to become one — "
        "the language, the framework, HTTP and API design, databases, authentication, caching "
        "and async work, testing, and getting it deployed and observable. Every example is real "
        "Java 21 and Spring Boot 4.1 code from a working pizza ordering API."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, which already maps this slug
# to the display name "Backend Development" under the "Software Engineering" group.
NAV_GROUP = "Software Engineering"

# The app every code sample is taken from, so a reader can go and see the whole
# thing in context rather than a fragment invented for the post.
DEMO_APP = "lovemesomecoding_demo_project/pizza/pizza-springboot-backend"

# Stated on the landing page and assumed by every other post. Read off the demo
# app's pom.xml — when it moves, the landing page's table is the first edit.
VERSIONS = {
    "spring-boot": "4.1.0",
    "java": "21",
    "jakarta-ee": "11",
    # Boot 4.1.0's BOM sets junit-jupiter.version to 6.0.3 and the demo app does not
    # override it. Read off the BOM, not from memory — "JUnit 5" was wrong in draft.
    "junit": "6.0.3",
}

POSTS = [
    {
        "slug": "backend-dev-get-started",
        "title": "Backend Dev – Get Started",
        "file": "01-backend-dev-get-started.html",
        "date": "2026-07-31T11:00:00",
        "tags": ["backend", "career", "java", "spring-boot"],
        "excerpt": (
            "Start here. What a backend engineer builds, the ten things you need to learn and the "
            "order to learn them in, and the exact stack every example in this track uses — Java "
            "21 and Spring Boot 4.1. Also: how this track fits with the deeper ones on the site, "
            "so you know when to stop reading here and go read those instead."
        ),
    },
    {
        "slug": "backend-dev-what-is-a-backend-engineer",
        "title": "Backend Dev – What a Backend Engineer Actually Does",
        "file": "02-backend-dev-what-is-a-backend-engineer.html",
        "date": "2026-08-02T11:00:00",
        "tags": ["backend", "career", "api", "database"],
        "excerpt": (
            "The job, described by what lands in your queue rather than by a job posting. What you "
            "own — the API contract, the data, correctness under concurrency, and what happens at "
            "3am — where the line sits between you and frontend, devops, DBA and data engineering, "
            "and what a real ticket looks like from request to deploy."
        ),
    },
    {
        "slug": "backend-dev-java-and-the-jvm",
        "title": "Backend Dev – The Java and the JVM You Actually Need",
        "file": "03-backend-dev-java-and-the-jvm.html",
        "date": "2026-08-04T11:00:00",
        "tags": ["java", "jvm", "backend", "collections"],
        "excerpt": (
            "You do not need all of Java before you start a framework, but you do need a specific "
            "subset — and one that is not the subset a beginner course teaches. Collections and "
            "which one to reach for, equals and hashCode, Optional, streams, exceptions that mean "
            "something, records, and the handful of JVM facts that explain your production bugs."
        ),
    },
    {
        "slug": "backend-dev-what-to-learn-in-a-framework",
        "title": "Backend Dev – What to Learn in a Framework",
        "file": "04-backend-dev-what-to-learn-in-a-framework.html",
        "date": "2026-08-06T11:00:00",
        "tags": ["spring-boot", "framework", "dependency-injection", "configuration"],
        "excerpt": (
            "Frameworks look enormous, but the part you use every day is small and it is the same "
            "part in every framework. Project layout, dependencies, configuration and profiles, "
            "dependency injection and why it is not just a fashion, the request path from URL to "
            "method, and how to tell a framework problem from your own bug."
        ),
    },
    {
        "slug": "backend-dev-apis-and-http",
        "title": "Backend Dev – HTTP and API Design",
        "file": "05-backend-dev-apis-and-http.html",
        "date": "2026-08-08T11:00:00",
        "tags": ["rest", "http", "api", "dto"],
        "excerpt": (
            "The contract you hand to every other team. What HTTP actually gives you — methods, "
            "status codes, headers, idempotency — how to shape URLs and payloads so they survive "
            "the next feature, why a DTO is not busywork, validating input at the edge, one error "
            "format for the whole API, pagination, and versioning before you need it."
        ),
    },
    {
        "slug": "backend-dev-databases",
        "title": "Backend Dev – Databases",
        "file": "06-backend-dev-databases.html",
        "date": "2026-08-10T11:00:00",
        "tags": ["database", "sql", "jpa", "transactions"],
        "excerpt": (
            "The part of the job that bites hardest and gets taught least. Modelling a schema you "
            "can live with, the indexes that decide whether a query takes 2ms or 2 seconds, what a "
            "transaction guarantees and what it does not, ORM versus plain SQL and when to drop "
            "down, the N+1 problem, connection pools, and migrations you can run on a live table."
        ),
    },
    {
        "slug": "backend-dev-auth-and-security",
        "title": "Backend Dev – Authentication, Authorization and Security",
        "file": "07-backend-dev-auth-and-security.html",
        "date": "2026-08-12T11:00:00",
        "tags": ["security", "authentication", "authorization", "jwt"],
        "excerpt": (
            "Who are you, and are you allowed to do that — two different questions that beginners "
            "merge into one. Password storage that survives a database leak, sessions versus "
            "stateless JWT and the trade you are making, OAuth2 login, checking permissions on the "
            "object and not just the endpoint, and the handful of attacks worth knowing by name."
        ),
    },
    {
        "slug": "backend-dev-caching-async-and-messaging",
        "title": "Backend Dev – Caching, Async Work and Messaging",
        "file": "08-backend-dev-caching-async-and-messaging.html",
        "date": "2026-08-14T11:00:00",
        "tags": ["cache", "async", "messaging", "performance"],
        "excerpt": (
            "Three ways to stop making the caller wait, and the cost of each. What is safe to "
            "cache and how to invalidate it, why the cache goes in front of the slow thing and not "
            "in front of everything, moving work off the request thread, events inside one process "
            "versus a real queue between services, and retries that do not double-charge anyone."
        ),
    },
    {
        "slug": "backend-dev-testing",
        "title": "Backend Dev – Testing",
        "file": "09-backend-dev-testing.html",
        "date": "2026-08-16T11:00:00",
        "tags": ["testing", "junit", "mockito", "integration-test"],
        "excerpt": (
            "Tests are how you change code you did not write without being afraid. What is worth "
            "testing and what is theatre, unit tests that run in milliseconds, integration tests "
            "against a real database, testing the API through HTTP, test data that does not rot, "
            "and why chasing a coverage number produces a suite that catches nothing."
        ),
    },
    {
        "slug": "backend-dev-deployment-and-observability",
        "title": "Backend Dev – Deployment and Observability",
        "file": "10-backend-dev-deployment-and-observability.html",
        "date": "2026-08-18T11:00:00",
        "tags": ["deployment", "docker", "observability", "logging"],
        "excerpt": (
            "Code that only runs on your laptop is not finished. Building one artifact and "
            "configuring it per environment, secrets that are not in git, containers and what they "
            "actually fix, a deploy pipeline, health checks the load balancer can use, and logs, "
            "metrics and traces — enough to answer “is it broken and where” at 3am."
        ),
    },
]

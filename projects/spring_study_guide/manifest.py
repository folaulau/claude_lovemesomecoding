"""The Spring Study Guide track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and post 9 is the newest.

All 8 pre-existing slugs were published on 2019-08-21 and are indexed. They are
being rewritten in place, NOT replaced: changing one of those slugs changes a
live URL. Only `spring-study-guide-get-started` is new.

Because the old posts carry a 2019 date and `upsert_post` never overwrites an
existing date, seeding this track needs `seed.py --force-dates` for the reading
order to come out right. See progress_report.md.

The 14:00 stamps are deliberate: the /spring-boot track dates its posts at 09:00
over an overlapping range, and an exact tie makes the archive order arbitrary.
"""

CATEGORY = {
    "slug": "spring-study-guide",
    "name": "Spring Study Guide",
    "description": (
        "The questions you need to be able to answer about Spring — the container and "
        "dependency injection, AOP, transactions and JPA, Spring MVC and REST, security "
        "and testing — answered against Spring Framework 7 and Spring Boot 4, with every "
        "example lifted from a real pizza ordering API."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts.
NAV_GROUP = "Java"

# The app every code sample is taken from, so a reader can go and see the whole
# thing in context rather than a fragment invented for the guide.
DEMO_APP = "lovemesomecoding_demo_project/pizza/pizza-springboot-backend"

# Stated on the landing page and assumed by every other post. Read off the demo
# app's pom.xml — when it moves, the landing page's table is the first edit.
VERSIONS = {
    "spring-boot": "4.1.0",
    "spring-framework": "7.0.8",
    "java": "21",
    "jakarta-ee": "11",
    "junit": "5",
    "jjwt": "0.12.6",
}

POSTS = [
    {
        "slug": "spring-study-guide-get-started",
        "title": "Spring Study Guide – Get Started",
        "file": "01-spring-study-guide-get-started.html",
        "date": "2026-08-02T14:00:00",
        "tags": ["spring", "spring-boot", "java", "interview"],
        "excerpt": (
            "Start here. What this guide is, who it is for, and the exact versions every answer "
            "is written against — Spring Framework 7 and Spring Boot 4.1 on Java 21. The eight "
            "topic areas in reading order, the pizza ordering API every snippet is lifted from, "
            "and the short list of things that changed between Spring 5 and Spring 7 that will "
            "make an old answer wrong."
        ),
    },
    {
        "slug": "spring-study-guide-core",
        "title": "Spring Study Guide – Core Spring",
        "file": "02-spring-study-guide-core.html",
        "date": "2026-08-04T14:00:00",
        "tags": ["spring", "dependency-injection", "beans", "application-context"],
        "excerpt": (
            "The container, and everything that lives in it. What dependency injection buys you, "
            "how an ApplicationContext starts and stops, the full bean lifecycle in the order it "
            "actually runs, the five scopes, component scanning, @Bean versus @Component, "
            "resolving ambiguity with @Qualifier and @Primary, profiles, @Value and SpEL, and the "
            "two proxy types Spring can create."
        ),
    },
    {
        "slug": "spring-study-guide-aop",
        "title": "Spring Study Guide – AOP",
        "file": "03-spring-study-guide-aop.html",
        "date": "2026-08-06T14:00:00",
        "tags": ["spring", "aop", "aspectj", "proxy"],
        "excerpt": (
            "Cross-cutting concerns, and the vocabulary you are expected to use precisely: join "
            "point, pointcut, advice, aspect, weaving. The five advice types and when each runs, "
            "the pointcut expressions worth memorising, what JoinPoint and ProceedingJoinPoint "
            "give you, the self-invocation limitation that catches everyone — and the Boot 4 "
            "starter rename that breaks every old pom."
        ),
    },
    {
        "slug": "spring-study-guide-data-integration",
        "title": "Spring Study Guide – Data Integration",
        "file": "04-spring-study-guide-data-integration.html",
        "date": "2026-08-08T14:00:00",
        "tags": ["spring", "jdbc", "transactions", "jpa", "spring-data"],
        "excerpt": (
            "Data access, transactions and JPA. Why Spring's exception hierarchy is unchecked, "
            "what JdbcTemplate does with a connection, what @Transactional actually generates, "
            "the seven propagation modes and the four isolation levels, the default rollback rule "
            "and how to change it, the persistence context and when it flushes, and how a Spring "
            "Data repository interface becomes a working implementation."
        ),
    },
    {
        "slug": "spring-study-guide-spring-boot",
        "title": "Spring Study Guide – Spring Boot",
        "file": "05-spring-study-guide-spring-boot.html",
        "date": "2026-08-10T14:00:00",
        "tags": ["spring-boot", "auto-configuration", "starters", "properties"],
        "excerpt": (
            "What Spring Boot adds to Spring and what it does not. Starters and why one "
            "dependency drags in twelve, how auto-configuration decides, what "
            "@SpringBootApplication expands to, where component scanning starts, the property "
            "source order in full, embedded servers versus a WAR, and the Boot 3 to Boot 4 "
            "changes that turn a working answer into a wrong one."
        ),
    },
    {
        "slug": "spring-study-guide-web-layer",
        "title": "Spring Study Guide – Web Layer",
        "file": "06-spring-study-guide-web-layer.html",
        "date": "2026-08-12T14:00:00",
        "tags": ["spring", "spring-mvc", "dispatcherservlet", "thymeleaf"],
        "excerpt": (
            "Spring MVC end to end. What the DispatcherServlet does with a request, the six "
            "delegates it hands off to, how a URL reaches a method, the controller method "
            "parameters and return types worth knowing, the Model and where the view gets it, "
            "view resolution, the web scopes, and why the whole design is testable without a "
            "servlet container."
        ),
    },
    {
        "slug": "spring-study-guide-rest",
        "title": "Spring Study Guide – REST",
        "file": "07-spring-study-guide-rest.html",
        "date": "2026-08-14T14:00:00",
        "tags": ["spring", "rest", "http", "restclient"],
        "excerpt": (
            "REST as Spring implements it. Resources, the safe and idempotent methods and why "
            "the distinction matters, status codes for each verb, @RestController versus "
            "@Controller, @RequestBody and @ResponseBody, HttpMessageConverters and how content "
            "negotiation picks one, error responses with @ControllerAdvice, and RestClient — the "
            "replacement for the RestTemplate every old answer names."
        ),
    },
    {
        "slug": "spring-study-guide-security",
        "title": "Spring Study Guide – Security",
        "file": "08-spring-study-guide-security.html",
        "date": "2026-08-16T14:00:00",
        "tags": ["spring", "spring-security", "jwt", "authentication"],
        "excerpt": (
            "Authentication, authorisation, and the filter chain that implements both. How a "
            "request travels through the filters, what the SecurityContext holds and how it is "
            "cleared, password hashing and salting, matcher ordering and the mistake that "
            "silently opens an endpoint, method security with @PreAuthorize, stateless JWT "
            "auth, and the lambda DSL that replaced every old configuration answer."
        ),
    },
    {
        "slug": "spring-study-guide-testing",
        "title": "Spring Study Guide – Testing",
        "file": "09-spring-study-guide-testing.html",
        "date": "2026-08-18T14:00:00",
        "tags": ["spring", "testing", "junit", "mockito"],
        "excerpt": (
            "When a test needs Spring and when it does not. Plain unit tests with Mockito, the "
            "cached test context and what silently evicts it, slice tests versus @SpringBootTest, "
            "@MockitoBean, why a @Transactional test rolls back by default, testing controllers "
            "with MockMvc and a whole API over a real port — every example from a suite that "
            "runs green."
        ),
    },
]

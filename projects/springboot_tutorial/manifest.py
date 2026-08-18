"""The Spring Boot track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and lesson 35 is the newest.

All 31 pre-existing slugs were published between 2018 and 2023 and are indexed.
They are being rewritten in place, NOT replaced: changing one of those slugs
changes a live URL. The 4 marked `new` below did not exist before.

Because the old posts carry 2018-2023 dates and `upsert_post` never overwrites an
existing date, seeding this track needs `seed.py --force-dates` for the reading
order to come out right. See progress_report.md.
"""

CATEGORY = {
    "slug": "spring-boot",
    "name": "Spring Boot",
    "description": (
        "Spring Boot 4 from the ground up — beans and dependency injection, REST APIs, "
        "JPA and JdbcTemplate, security and JWT, caching, messaging and testing, every "
        "example lifted from a real pizza ordering API."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts.
NAV_GROUP = "Java"

# The app every code sample is taken from, so a reader can go and see the whole
# thing in context rather than a fragment invented for the tutorial.
DEMO_APP = "lovemesomecoding_demo_project/pizza/pizza-springboot-backend"

# Stated on lesson 1 and assumed by every other post. Read off the demo app's
# pom.xml — when it moves, lesson 1's table is the first edit.
VERSIONS = {
    "spring-boot": "4.1.0",
    "spring-framework": "7.0.8",
    "java": "21",
    "springdoc-openapi": "2.8.6",
    "mapstruct": "1.6.3",
    "jjwt": "0.12.6",
    "stripe-java": "29.2.0",
    "spotless": "2.44.5",
}

POSTS = [
    # ------------------------------------------------------- 1. getting started
    {
        "slug": "spring-boot-get-started",
        "title": "Spring Boot – Get Started",
        "file": "01-spring-boot-get-started.html",
        "date": "2026-06-11T09:00:00",
        "tags": ["spring-boot", "java", "setup"],
        "excerpt": (
            "Start here. What Spring Boot is and what problem it solves, the exact versions this "
            "track is written against — Spring Boot 4.1 on Java 21 — one command to generate a "
            "project and see it running, the pizza ordering API every example is taken from, and "
            "the full lesson index in reading order."
        ),
    },
    {
        "slug": "spring-boot-introduction",
        "title": "Spring Boot – What It Actually Does",
        "file": "02-spring-boot-introduction.html",
        "date": "2026-06-13T09:00:00",
        "tags": ["spring-boot", "auto-configuration", "starters"],
        "excerpt": (
            "Starters, auto-configuration and the embedded server — the three things that "
            "separate Spring Boot from plain Spring. Why one dependency drags in twelve, how "
            "Boot decides which beans to create for you, and how to see every decision it made "
            "with the condition evaluation report."
        ),
    },
    {
        "slug": "spring-boot-migration-from-spring",
        "title": "Spring Boot – Migrating from Spring, and from Boot 3 to 4",
        "file": "03-spring-boot-migration-from-spring.html",
        "date": "2026-06-15T09:00:00",
        "tags": ["spring-boot", "migration", "spring-boot-4"],
        "excerpt": (
            "What XML configuration, a WAR file and a servlet container turn into once Boot is "
            "doing the work. Then the migration people actually face today: Boot 3 to Boot 4, "
            "where the modularised starters mean a dependency that used to bring "
            "autoconfiguration with it now silently brings none."
        ),
    },
    {
        "slug": "spring-boot-code-structure",
        "title": "Spring Boot – Structuring a Project",
        "file": "04-spring-boot-code-structure.html",
        "date": "2026-06-17T09:00:00",
        "tags": ["spring-boot", "architecture", "packages"],
        "excerpt": (
            "Package by feature, not by layer. The controller / service / DAO split the pizza API "
            "uses, why every service and DAO is an interface plus an implementation, where DTOs "
            "and mappers live, and why component scanning makes the application class's package "
            "the one structural decision you cannot get wrong."
        ),
    },
    # ----------------------------------------------------------- 2. the container
    {
        "slug": "spring-boot-bean",
        "title": "Spring Boot – Beans, Scopes and Lifecycle",
        "file": "05-spring-boot-bean.html",
        "date": "2026-06-19T09:00:00",
        "tags": ["spring-boot", "beans", "application-context"],
        "excerpt": (
            "What a bean is, the difference between @Component and @Bean and when you need the "
            "second one, singleton versus prototype scope, the callbacks that run as a bean is "
            "created and destroyed, and why @Primary and @Qualifier exist the moment two beans "
            "satisfy the same type."
        ),
    },
    {
        "slug": "spring-boot-dependency-injection",
        "title": "Spring Boot – Dependency Injection",
        "file": "06-spring-boot-dependency-injection.html",
        "date": "2026-06-21T09:00:00",
        "tags": ["spring-boot", "dependency-injection", "ioc"],
        "excerpt": (
            "Inversion of control in the only form that matters day to day: constructor "
            "injection. Why field injection with @Autowired is the wrong default, how Lombok's "
            "@RequiredArgsConstructor removes the boilerplate that made people reach for it, and "
            "how to break a circular dependency instead of papering over it with @Lazy."
        ),
    },
    {
        "slug": "spring-boot-configuration-properties",
        "title": "Spring Boot – Configuration, Profiles and Properties",
        "file": "07-spring-boot-configuration-properties.html",
        "date": "2026-06-23T09:00:00",
        "tags": ["spring-boot", "configuration", "profiles"],
        "excerpt": (
            "Where configuration comes from and which source wins, @Value versus "
            "@ConfigurationProperties and why typed records beat scattered strings, profiles for "
            "local versus production, and how to keep secrets out of the repository without "
            "making the app impossible to run."
        ),
    },
    {
        "slug": "spring-boot-aop",
        "title": "Spring Boot – Aspect-Oriented Programming",
        "file": "08-spring-boot-aop.html",
        "date": "2026-06-25T09:00:00",
        "tags": ["spring-boot", "aop", "aspectj"],
        "excerpt": (
            "Cross-cutting concerns without copying the same five lines into forty methods. "
            "Pointcuts, @Around advice and a real timing aspect over the service layer — plus the "
            "proxy rule that catches everyone: a self-invocation inside the same class never goes "
            "through the proxy, so the aspect simply does not run."
        ),
    },
    {
        "slug": "spring-boot-event-handling",
        "title": "Spring Boot – Application Events",
        "file": "09-spring-boot-event-handling.html",
        "date": "2026-06-27T09:00:00",
        "tags": ["spring-boot", "events", "decoupling"],
        "excerpt": (
            "Publishing an event instead of calling four services. @EventListener, ordering, "
            "async listeners, and @TransactionalEventListener — because a listener that fires "
            "before the transaction commits will happily email a customer about an order that is "
            "about to be rolled back."
        ),
    },
    # ----------------------------------------------------------- 3. the web layer
    {
        "slug": "spring-boot-web-mvc",
        "title": "Spring Boot – Spring Web MVC",
        "file": "10-spring-boot-web-mvc.html",
        "date": "2026-06-29T09:00:00",
        "tags": ["spring-boot", "spring-mvc", "web"],
        "excerpt": (
            "How a request actually reaches your method: DispatcherServlet, handler mapping, "
            "argument resolvers and message converters. Where CORS is configured and why it has "
            "to agree with the security filter chain, and what Boot 4's webmvc starter gives you "
            "before you write a line."
        ),
    },
    {
        "slug": "spring-boot-rest",
        "title": "Spring Boot – Building a REST API",
        "file": "11-spring-boot-rest.html",
        "date": "2026-07-01T09:00:00",
        "tags": ["spring-boot", "rest", "api"],
        "excerpt": (
            "@RestController end to end: path and query binding, request bodies, Bean Validation, "
            "and returning the right status code instead of 200 for everything. Why the pizza API "
            "exposes a UUID rather than its primary key, and why a DTO is not ceremony once an "
            "entity has a password field on it."
        ),
    },
    {
        "slug": "spring-boot-exception-handling",
        "title": "Spring Boot – Exception Handling",
        "file": "12-spring-boot-exception-handling.html",
        "date": "2026-07-03T09:00:00",
        "tags": ["spring-boot", "exception-handling", "rest"],
        "excerpt": (
            "One @RestControllerAdvice, one error shape, every endpoint. Turning a validation "
            "failure into a field-by-field response the frontend can render, mapping your own "
            "exceptions to status codes, and why returning 404 instead of 403 for a "
            "foreign-owned resource is a security decision rather than a sloppy one."
        ),
    },
    {
        "slug": "spring-boot-rest-file-upload",
        "title": "Spring Boot – File Upload",
        "file": "13-spring-boot-rest-file-upload.html",
        "date": "2026-07-05T09:00:00",
        "tags": ["spring-boot", "file-upload", "multipart"],
        "excerpt": (
            "Accepting a MultipartFile, the size limits you have to raise in two different places, "
            "and validating what was actually uploaded rather than trusting the filename or the "
            "content type the browser claimed. Ends with streaming a file back out again."
        ),
    },
    {
        "slug": "spring-boot-with-swagger",
        "title": "Spring Boot – API Docs with springdoc-openapi",
        "file": "14-spring-boot-with-swagger.html",
        "date": "2026-07-07T09:00:00",
        "tags": ["spring-boot", "swagger", "openapi"],
        "excerpt": (
            "Springfox is dead; springdoc is what generates OpenAPI 3 from your controllers now. "
            "Wiring it up, documenting an endpoint properly, describing JWT auth so the Try It Out "
            "button works — and the version pin Boot 4 forces on you, because Boot no longer "
            "manages springdoc's version."
        ),
    },
    {
        "slug": "spring-boot-with-thymeleaf",
        "title": "Spring Boot – Server-Rendered Pages with Thymeleaf",
        "file": "15-spring-boot-with-thymeleaf.html",
        "date": "2026-07-09T09:00:00",
        "tags": ["spring-boot", "thymeleaf", "templates"],
        "excerpt": (
            "Not every page needs a JavaScript framework. A @Controller that returns a view name, "
            "the Thymeleaf syntax worth knowing, layout fragments, and rendering the same template "
            "to a string for an email body. Includes when to reach for this instead of a REST "
            "endpoint, and when not to."
        ),
    },
    # ----------------------------------------------------------------- 4. data
    {
        "slug": "spring-boot-hibernate",
        "title": "Spring Boot – JPA and Hibernate",
        "file": "16-spring-boot-hibernate.html",
        "date": "2026-07-11T09:00:00",
        "tags": ["spring-boot", "jpa", "hibernate"],
        "excerpt": (
            "Entities, relationships and the persistence context. Lazy loading and the N+1 query "
            "it hands you, why open-in-view is switched off here, soft deletes with "
            "@SQLRestriction, and the ddl-auto setting to use once something other than Hibernate "
            "owns your schema."
        ),
    },
    {
        "slug": "spring-boot-jdbc",
        "title": "Spring Boot – JdbcTemplate",
        "file": "17-spring-boot-jdbc.html",
        "date": "2026-07-13T09:00:00",
        "tags": ["spring-boot", "jdbc", "sql"],
        "excerpt": (
            "When JPA has nothing to offer — aggregates, reports, any query whose result is not an "
            "entity. NamedParameterJdbcTemplate, RowMappers in their own testable classes, and the "
            "trap that silently inflated a revenue report: hand-written SQL never sees the "
            "@SQLRestriction that hides deleted rows."
        ),
    },
    {
        "slug": "spring-boot-liquibase",
        "title": "Spring Boot – Schema Migrations with Liquibase",
        "file": "18-spring-boot-liquibase.html",
        "date": "2026-07-15T09:00:00",
        "tags": ["spring-boot", "liquibase", "database"],
        "excerpt": (
            "Let the database schema live in version control. Changelogs, changesets and the "
            "checksum that makes editing an applied migration a mistake you only make once. "
            "Pairing Liquibase with ddl-auto=validate so drift fails at boot, and the Boot 4 "
            "starter you need or Liquibase silently never runs at all."
        ),
    },
    {
        "slug": "spring-boot-mapstruct",
        "title": "Spring Boot – Mapping DTOs with MapStruct",
        "file": "19-spring-boot-mapstruct.html",
        "date": "2026-07-17T09:00:00",
        "tags": ["spring-boot", "mapstruct", "dto"],
        "excerpt": (
            "Generated mapping code instead of hand-written getters and setters, checked at "
            "compile time. Writing a mapper, handling nested objects and custom expressions — and "
            "the annotation-processor ordering that makes MapStruct and Lombok work together, "
            "because getting it wrong produces mappers that compile and map nothing."
        ),
    },
    {
        "slug": "spring-boot-lombok",
        "title": "Spring Boot – Lombok",
        "file": "20-spring-boot-lombok.html",
        "date": "2026-07-19T09:00:00",
        "tags": ["spring-boot", "lombok", "java"],
        "excerpt": (
            "The annotations worth using — @Getter, @Setter, @RequiredArgsConstructor, @Builder, "
            "@Slf4j — and the two to be careful with: @Data on a JPA entity generates an equals "
            "and hashCode that break the moment the entity is in a HashSet, and @ToString will "
            "happily log a password field."
        ),
    },
    {
        "slug": "spring-boot-cache",
        "title": "Spring Boot – Caching",
        "file": "21-spring-boot-cache.html",
        "date": "2026-07-21T09:00:00",
        "tags": ["spring-boot", "caching", "performance"],
        "excerpt": (
            "@EnableCaching, @Cacheable, @CacheEvict and the key generation you almost always want "
            "to override. Caching the menu in the pizza API, why an eviction has to be wired to "
            "every write path that can invalidate it, and the same proxy rule AOP has: a "
            "self-invocation is never cached."
        ),
    },
    {
        "slug": "spring-boot-elasticsearch",
        "title": "Spring Boot – Elasticsearch",
        "file": "22-spring-boot-elasticsearch.html",
        "date": "2026-07-23T09:00:00",
        "tags": ["spring-boot", "elasticsearch", "search"],
        "excerpt": (
            "Full-text search that a LIKE query cannot do. Spring Data Elasticsearch repositories, "
            "mapping a document, keeping the index in step with the database, and being honest "
            "about the operational cost — this is the point where the demo app stops needing only "
            "MySQL."
        ),
    },
    # ------------------------------------------------------------- 5. security
    {
        "slug": "spring-security-authentication",
        "title": "Spring Security – How Authentication Works",
        "file": "23-spring-security-authentication.html",
        "date": "2026-07-25T09:00:00",
        "tags": ["spring-security", "authentication", "spring-boot"],
        "excerpt": (
            "The filter chain, AuthenticationManager, UserDetailsService and the "
            "SecurityContext — the four pieces everything else in Spring Security is built on. "
            "Password hashing with BCrypt, and why a login failure should be deliberately vague "
            "about which half of the credentials was wrong."
        ),
    },
    {
        "slug": "spring-boot-security-config",
        "title": "Spring Boot – Configuring the Security Filter Chain",
        "file": "24-spring-boot-security-config.html",
        "date": "2026-07-27T09:00:00",
        "tags": ["spring-security", "configuration", "spring-boot"],
        "excerpt": (
            "The modern lambda DSL — WebSecurityCustomizer is gone and so is "
            "WebSecurityConfigurerAdapter. Ordering rules so a permitAll does not accidentally "
            "open an admin endpoint, disabling CSRF only where it is genuinely safe to, and making "
            "CORS and security agree instead of fighting."
        ),
    },
    {
        "slug": "spring-boot-api-authentication",
        "title": "Spring Boot – Stateless API Authentication with JWT",
        "file": "25-spring-boot-api-authentication.html",
        "date": "2026-07-29T09:00:00",
        "tags": ["spring-security", "jwt", "api"],
        "excerpt": (
            "Issuing a token at login, validating it in a OncePerRequestFilter, and putting the "
            "result in the SecurityContext. Where the signing key comes from, what does and does "
            "not belong in a claim, and the honest trade-off nobody mentions: a stateless token "
            "cannot be revoked."
        ),
    },
    {
        "slug": "spring-boot-security-secured-on-method-level",
        "title": "Spring Boot – Method-Level Security",
        "file": "26-spring-boot-security-secured-on-method-level.html",
        "date": "2026-07-31T09:00:00",
        "tags": ["spring-security", "authorization", "spring-boot"],
        "excerpt": (
            "@PreAuthorize, @PostAuthorize and @Secured, and why URL rules alone stop being enough "
            "as soon as two entry points reach the same service. Expression-based checks against "
            "the authenticated principal, and the proxy rule that makes an internal call skip the "
            "check entirely."
        ),
    },
    {
        "slug": "spring-boot-oauth2",
        "title": "Spring Boot – OAuth2",
        "file": "27-spring-boot-oauth2.html",
        "date": "2026-08-02T09:00:00",
        "tags": ["spring-security", "oauth2", "sso"],
        "excerpt": (
            "The authorization code flow in the terms Spring actually names things, sign in with "
            "Google against the pizza app, and the piece every tutorial skips: reconciling an "
            "OAuth2 identity with the user row you already have, so the same person logging in "
            "both ways does not end up as two accounts."
        ),
    },
    # -------------------------------------------------- 6. async and integration
    {
        "slug": "spring-boot-thread-pool",
        "title": "Spring Boot – Async Work and Thread Pools",
        "file": "28-spring-boot-thread-pool.html",
        "date": "2026-08-04T09:00:00",
        "tags": ["spring-boot", "async", "concurrency"],
        "excerpt": (
            "@EnableAsync, @Async and a ThreadPoolTaskExecutor sized on purpose rather than left "
            "at the default. What the queue and rejection policy actually do under load, "
            "@Scheduled for recurring work, and why an @Async method that returns void throws "
            "away its own exceptions."
        ),
    },
    {
        "slug": "spring-boot-retry",
        "title": "Spring Boot – Retries",
        "file": "29-spring-boot-retry.html",
        "date": "2026-08-06T09:00:00",
        "tags": ["spring-boot", "resilience", "retry"],
        "excerpt": (
            "@Retryable with exponential backoff and a @Recover fallback, applied to the Stripe "
            "calls in the pizza API. Which exceptions are worth retrying and which just waste "
            "time, and the correctness rule underneath all of it: retrying a non-idempotent call "
            "is how you charge a customer twice."
        ),
    },
    {
        "slug": "spring-boot-jms",
        "title": "Spring Boot – Messaging with JMS",
        "file": "30-spring-boot-jms.html",
        "date": "2026-08-08T09:00:00",
        "tags": ["spring-boot", "jms", "messaging"],
        "excerpt": (
            "Handing work to a queue so the request can return. JmsTemplate, @JmsListener, "
            "converting a message payload to JSON, and what to do with a message that keeps "
            "failing — because without a dead-letter destination it is redelivered forever."
        ),
    },
    {
        "slug": "spring-boot-email",
        "title": "Spring Boot – Sending Email",
        "file": "31-spring-boot-email.html",
        "date": "2026-08-10T09:00:00",
        "tags": ["spring-boot", "email", "javamail"],
        "excerpt": (
            "JavaMailSender, a MimeMessageHelper for HTML and attachments, and rendering the body "
            "from the Thymeleaf template built earlier in the track. Sending it off the request "
            "thread, and testing the whole thing against a local sink instead of a real inbox."
        ),
    },
    # ------------------------------------------------- 7. build, test, reference
    {
        "slug": "spring-boot-testing",
        "title": "Spring Boot – Testing",
        "file": "32-spring-boot-testing.html",
        "date": "2026-08-12T09:00:00",
        "tags": ["spring-boot", "testing", "junit"],
        "excerpt": (
            "The test pyramid as Spring Boot expresses it: a plain unit test with Mockito, a "
            "@WebMvcTest slice, a @DataJpaTest slice, and @SpringBootTest for the cases that "
            "genuinely need the whole context. Testing secured endpoints, and why the slice you "
            "reach for first should be the smallest one that fails honestly."
        ),
    },
    {
        "slug": "spring-boot-gradle",
        "title": "Spring Boot – Building with Gradle",
        "file": "33-spring-boot-gradle.html",
        "date": "2026-08-14T09:00:00",
        "tags": ["spring-boot", "gradle", "build"],
        "excerpt": (
            "The same pizza backend built with Gradle instead of Maven — the plugins, the "
            "dependency management, annotation processors for Lombok and MapStruct, and the "
            "wrapper. Side by side with the pom.xml it replaces, so you can read either build "
            "file and know what the other one says."
        ),
    },
    {
        "slug": "spring-boot-code-snippets",
        "title": "Spring Boot – Cheat Sheet",
        "file": "34-spring-boot-code-snippets.html",
        "date": "2026-08-16T09:00:00",
        "tags": ["spring-boot", "reference", "cheat-sheet"],
        "excerpt": (
            "The annotations and snippets from this whole track in one page, grouped by what you "
            "are trying to do — wire a bean, expose an endpoint, query a database, secure a route, "
            "cache a result, schedule a job. Written to be scanned rather than read, with a link "
            "to the lesson behind each one."
        ),
    },
    {
        "slug": "springboot-interview-questions",
        "title": "Spring Boot – Interview Questions",
        "file": "35-springboot-interview-questions.html",
        "date": "2026-08-18T09:00:00",
        "tags": ["spring-boot", "interview", "java"],
        "excerpt": (
            "Senior-level questions and answers, every one drawn from a real decision or a real "
            "bug in the pizza codebase rather than from a list. Auto-configuration, bean scopes, "
            "the proxy rule, transactions, N+1, stateless auth, and the trade-offs an interviewer "
            "is actually listening for."
        ),
    },
]

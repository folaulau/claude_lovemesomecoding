# Spring Boot tutorial track — progress report

**Status:** IN PROGRESS — demo-app gaps 6/13 closed, post authoring not started
**Started:** 2026-08-18
**Where it lands:** https://lovemesomecoding.com/spring-boot

---

## What this is

`/spring-boot` already holds **31 posts published 2018–2023**. They teach the Spring Boot 2 era,
run 13,543 words *in total* (median ~230 words), and five of them are effectively empty:

| Slug | Bytes of content |
|---|---|
| `spring-boot-aop` | **0** |
| `spring-boot-migration-from-spring` | **0** |
| `spring-boot-rest` | **0** |
| `spring-boot-code-snippets` | 154 |
| `spring-boot-oauth2` | 299 |

One is genuinely substantial — `springboot-interview-questions`, 5,380 words.

This project rewrites all 31 **in place** — same slugs, so no indexed URL is lost — against
**Spring Boot 4.1.0 / Java 21**, and adds 4 new posts for topics the demo app already demonstrates
but no existing slug covers.

**Result: a 35-post track** — a `spring-boot-get-started` landing page at the front and
`springboot-interview-questions` at the end.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Existing 31 posts | Rewrite in place, keep every slug | They are indexed URLs. Rewriting keeps the ranking and kills the stale Boot 2 content in one move. |
| Track size | 35 posts (31 rewritten + 4 new) | Between Oracle's 14 and a full curriculum. Deep enough to be a real track, finite enough to maintain. |
| Gap topics | **Add every missing feature to the pizza app** | Folau's call, 2026-08-18. The README rule — "if examples are not found in this project, add them" — applied without exception, including the infra-heavy ones. See the risk note below. |
| Dates | Restamped 2026-06-11 … 2026-08-18, 2 days apart | The old posts carry 2018–2023 dates, which `upsert_post` never overwrites — hence `seed.py --force-dates`. Without it the pager reads in the wrong order. |
| Snippet language | Java 21 | Copied verbatim from `pizza-springboot-backend`, so every snippet is provably real, compiling code. |
| Example source | `pizza-springboot-backend` | Per the README. |
| Seeding | Backend service layer, as `projects/react_tutorial/seed.py` does | The static build reads only the derived indexes; reusing the admin API's own code is the only way to be sure indexes and posts agree. |
| Sibling categories | Out of scope | `spring-data` (15), `spring-study-guide` (8), `spring-interview` (5) are separate categories. The README names `/spring-boot` only. |

### ⚠️ Risk accepted on the "add everything to the pizza app" decision

Flagged before starting, and Folau confirmed. Recording it so the trade-off is not rediscovered:

- `pizza/CLAUDE.md` says **"Keep it minimal."** Elasticsearch, JMS, email, OAuth2 and Thymeleaf
  each pull in infrastructure a pizza ordering app has no product reason to have.
- **Running the demo app gets harder.** It currently needs local MySQL and nothing else. Adding
  these means a broker, an ES node and an SMTP sink before `./mvnw spring-boot:run` works.
- **Mitigation:** every added integration must be behind a Spring profile and default to **off**,
  so a plain `./mvnw spring-boot:run` and the existing 60-test suite keep working untouched. The
  README's own constraint — "make sure your changes don't break existing functionalities" — is the
  acceptance bar.

## Versions the track is written against

Read off `pizza-springboot-backend/pom.xml`. Stated on lesson 1 and assumed throughout.
**When these move, that table is the first edit.**

| | |
|---|---|
| Spring Boot | **4.1.0** |
| Spring Framework | 7.0.8 |
| Java | **21** |
| MySQL connector | Boot-managed |
| Liquibase | Boot-managed (`spring-boot-starter-liquibase`) |
| springdoc-openapi | 2.8.6 (Boot 4.1 does not manage it — pinned) |
| MapStruct | 1.6.3 (+ lombok-mapstruct-binding 0.2.0) |
| jjwt | 0.12.6 |
| Stripe | 29.2.0 |
| Spotless | 2.44.5 (palantirJavaFormat) |

## Topic list

The order is the reading order. `date` ascends with the track so the prev/next pager reads
lesson 1 → lesson 35.

**State:** `rewrite` = existing indexed slug, rewritten in place · **new** = did not exist before.
**App gap** = the feature is not in the pizza backend yet and must be added first.

### Part 1 — Getting started

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 1 | `spring-boot-get-started` | Get Started | **new** | track index; versions table; running the app |
| 2 | `spring-boot-introduction` | What Spring Boot Is | rewrite | starters + auto-configuration in `pom.xml` |
| 3 | `spring-boot-migration-from-spring` | From Spring to Spring Boot (and Boot 3 → 4) | rewrite | the Boot 4 notes already in `pom.xml` |
| 4 | `spring-boot-code-structure` | Structuring a Project | rewrite | the whole `com.pizza.api` layout |

### Part 2 — The container

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 5 | `spring-boot-bean` | Beans, Scopes and Lifecycle | rewrite | `OpenApiConfig`, `RestMVCConfig`, `ThreadPoolConfig` |
| 6 | `spring-boot-dependency-injection` | Dependency Injection | rewrite | every `*ServiceImpl`; `@Qualifier`, `@Primary` |
| 7 | `spring-boot-configuration-properties` | Configuration, Profiles and Properties | **new** | `application.properties`, `@Value`, 4 `@Profile` uses · **app gap:** `@ConfigurationProperties` |
| 8 | `spring-boot-aop` | Aspect-Oriented Programming | rewrite | **app gap:** no `@Aspect` anywhere |
| 9 | `spring-boot-event-handling` | Application Events | rewrite | **app gap:** no `@EventListener` anywhere |

### Part 3 — The web layer

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 10 | `spring-boot-web-mvc` | Spring Web MVC | rewrite | `RestMVCConfig`, the controller layer |
| 11 | `spring-boot-rest` | Building a REST API | rewrite | `ProductRestController`, `CustomerOrderRestController`, DTOs |
| 12 | `spring-boot-exception-handling` | Exception Handling | **new** | `RestExceptionHandler`, `ApiError`, `ApiSubError`, `ApiException` |
| 13 | `spring-boot-rest-file-upload` | File Upload | rewrite | **app gap:** no `MultipartFile` anywhere |
| 14 | `spring-boot-with-swagger` | API Docs with springdoc | rewrite | `OpenApiConfig` + every documented endpoint |
| 15 | `spring-boot-with-thymeleaf` | Server-Rendered Pages with Thymeleaf | rewrite | **app gap:** `templates/` is empty |

### Part 4 — Data

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 16 | `spring-boot-hibernate` | JPA and Hibernate | rewrite | `Product`, `CustomerOrder`, `@SQLRestriction` soft delete |
| 17 | `spring-boot-jdbc` | JdbcTemplate | rewrite | `ReportDAOImp` + the `mapper/` RowMappers |
| 18 | `spring-boot-liquibase` | Schema Migrations with Liquibase | **new** | `db/changelog/` — 9 changesets, `ddl-auto=validate` |
| 19 | `spring-boot-mapstruct` | Mapping DTOs with MapStruct | rewrite | `EntityDTOMapper` + the annotation-processor ordering |
| 20 | `spring-boot-lombok` | Lombok | rewrite | 28 files use `@Slf4j`; entities and DTOs |
| 21 | `spring-boot-cache` | Caching | rewrite | **app gap:** no `@Cacheable` anywhere |
| 22 | `spring-boot-elasticsearch` | Elasticsearch | rewrite | **app gap:** not present · infra |

### Part 5 — Security

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 23 | `spring-security-authentication` | How Spring Security Authenticates | rewrite | the filter chain, `UserDAOImp` |
| 24 | `spring-boot-security-config` | Configuring the Filter Chain | rewrite | `SecurityConfig` |
| 25 | `spring-boot-api-authentication` | Stateless API Auth with JWT | rewrite | `JwtService`, `JwtAuthenticationFilter`, `AuthRestController` |
| 26 | `spring-boot-security-secured-on-method-level` | Method-Level Security | rewrite | **app gap:** no `@PreAuthorize` / `@Secured` |
| 27 | `spring-boot-oauth2` | OAuth2 | rewrite | **app gap:** not present · infra |

### Part 6 — Async and integration

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 28 | `spring-boot-thread-pool` | Async Work and Thread Pools | rewrite | `ThreadPoolConfig`, the `@Async` and `@Scheduled` uses |
| 29 | `spring-boot-retry` | Retries | rewrite | **app gap:** no `@Retryable` |
| 30 | `spring-boot-jms` | Messaging with JMS | rewrite | **app gap:** not present · infra |
| 31 | `spring-boot-email` | Sending Email | rewrite | **app gap:** not present · infra |

### Part 7 — Build, test, reference

| # | Slug | Title | State | Source in the demo app |
|---|------|-------|-------|------------------------|
| 32 | `spring-boot-testing` | Testing | rewrite | the 60-test suite; slice tests vs `@SpringBootTest` |
| 33 | `spring-boot-gradle` | Building with Gradle | rewrite | **app gap:** a Gradle build equivalent to `pom.xml` |
| 34 | `spring-boot-code-snippets` | Cheat Sheet | rewrite | annotation + snippet reference drawn from the whole app |
| 35 | `springboot-interview-questions` | Interview Questions | rewrite | the whole app + its real bugs and decisions |

## Demo-app changes this requires

Every one behind a profile, defaulting to **off**, so `./mvnw spring-boot:run` and the existing
60 tests keep working. Nothing here is done yet.

| # | Change | For post | Infra needed | State |
|---|---|---|---|---|
| 1 | `PizzaProperties` — the whole `pizza.*` namespace bound to validated records; all 9 `@Value` sites refactored onto it | 7 | none | **done** |
| 2 | `aspect/ServiceTimingAspect` — `@Around` timing over the service layer | 8 | none | **done** |
| 3 | `OrderPlacedEvent` + `OrderPlacedListener`; published from `createOrder` | 9 | none | **done** |
| 4 | `MultipartFile` — product image upload | 13 | none | not started |
| 5 | `CacheConfig` + `@Cacheable` on the menu, `@CacheEvict` on all 4 write paths | 21 | none | **done** |
| 6 | `@EnableMethodSecurity` + `@PreAuthorize` on all 3 `AdminUserServiceImpl` methods | 26 | none | **done** |
| 7 | `@Retryable` on the Stripe calls, with a Stripe idempotency key | 29 | none | **done** |
| 8 | Thymeleaf — a server-rendered receipt page | 15 | none | not started |
| 9 | Elasticsearch — menu search | 22 | **ES node** | not started |
| 10 | JMS — order events onto a queue | 30 | **broker** | not started |
| 11 | Email — order confirmation mail | 31 | **SMTP sink** | not started |
| 12 | OAuth2 — social login | 27 | **identity provider** | not started |
| 13 | Gradle build alongside Maven | 33 | none | not started |

**Verified after every change: `./mvnw test` → 60/60 passing, `spotless:apply` clean.** The 60-test
baseline was captured before the first edit precisely so "don't break existing functionality" is a
measured claim rather than an assumption.

### Three findings from doing it — all of them post material

1. **`spring-boot-starter-aop` no longer exists.** Boot 4 renamed it `spring-boot-starter-aspectj`
   and dropped the old name from the BOM entirely, so a Boot 3 pom fails with
   *"'dependencies.dependency.version' ... is missing"* — an error that never mentions the rename.
   Goes in lesson 8 and lesson 3.
2. **Spring Framework 7 ships retry in the core container.** `@Retryable` +
   `@EnableResilientMethods` live in `org.springframework.resilience.annotation`, so the
   `spring-retry` dependency is now legacy and the project needs neither it nor `@EnableRetry`.
   Note it has **no `@Recover` equivalent** — it rethrows once retries are exhausted. Lesson 29.
3. **`spring-boot-starter-cache` IS still BOM-managed**, unlike the aop starter — so the Boot 4
   modularisation is inconsistent enough that you have to check each starter rather than assume.

## Site changes this requires

- ⚠️ **`properties` is not a supported language at either end of the pipeline.**
  `application.properties` is the single most common config format in this track, and today it
  normalises to `plaintext` — no highlighting. Prism ships `prism-properties.js` and it is already
  in `node_modules`. Two edits, exactly analogous to what the React track did for `tsx`:
  - `lovemesomecoding_backend/app/services/content.py` — add `properties` to `SUPPORTED_LANGUAGES`
    (and alias `ini` → `properties`).
  - `lovemesomecoding_frontend/src/lib/content.ts` — `import 'prismjs/components/prism-properties'`.
- Everything else this track needs is already supported: `java`, `sql`, `groovy`, `kotlin`, `yaml`,
  `json`, `bash`, `docker`, and `xml` → `markup`.
- ⚠️ **The React track left the backend Lambda un-redeployed.** That is still outstanding and now
  affects this track too — until `lovemesomecoding_backend/scripts/deploy.sh` runs, editing any of
  these posts through `/admin` normalises unknown languages down to `plaintext`.

## Files

```
projects/springboot_tutorial/
  README.md            the requirements
  progress_report.md   this file
  manifest.py          category metadata + one entry per post      (to build)
  posts/NN-slug.html   post bodies, plain semantic HTML            (to build)
  seed.py              writes the posts into a content tree        (to build)
  check_content.py     proves the normaliser round-trips every code sample  (to build)
```

## Task log

| Date | Task | Owner | Status |
|---|---|---|---|
| 2026-08-18 | Audit the 31 live posts — word counts, dates, empty bodies | Claude | done |
| 2026-08-18 | Inventory `pizza-springboot-backend` Spring feature coverage | Claude | done |
| 2026-08-18 | Confirm pipeline language support; find the `properties` gap | Claude | done |
| 2026-08-18 | Agree scope, fate of the old posts, how to close the app gaps | Folau | done |
| 2026-08-18 | Write this progress report + the 35-post topic table | Claude | done |
| 2026-08-18 | Teach both ends of the pipeline about `properties` (+ `ini`/`conf` aliases) | Claude | done |
| 2026-08-18 | Scaffold `manifest.py` (35 entries) / `seed.py` / `check_content.py` | Claude | done |
| 2026-08-18 | Capture the demo-app baseline — 60 tests green before any edit | Claude | done |
| 2026-08-18 | Close app gaps 1, 2, 3, 5, 6, 7 — config, AOP, events, cache, method security, retry | Claude | done |
| | Close app gaps 4, 8–13 — upload, Thymeleaf, ES, JMS, email, OAuth2, Gradle | Claude | not started |
| | Author 35 post bodies | Claude | not started |
| | `check_content.py` — every sample round-trips byte-for-byte | Claude | not started |
| | Seed local, sync, build, review at `:3000` | Claude | not started |
| | Seed prod `--force-dates --write`, `npm run deploy` | Claude | not started |
| | Redeploy the backend Lambda | Folau | **outstanding, inherited from the React track** |

## Outstanding

1. Everything below "Write this progress report" in the task log.
2. **Backend Lambda still not redeployed** (inherited). Seeding runs the local service layer, so
   what lands in S3 is correct — but `/admin` edits would normalise unknown languages to
   `plaintext` and silently lose highlighting.

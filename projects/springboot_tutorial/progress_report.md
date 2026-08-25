# Spring Boot tutorial track — progress report

**Status:** PUBLISHED — live on prod, 2026-08-18
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
| 4 | `storage/` — image upload validated by magic number; upload + stream-back endpoints | 13 | none | **done** |
| 5 | `CacheConfig` + `@Cacheable` on the menu, `@CacheEvict` on all 4 write paths | 21 | none | **done** |
| 6 | `@EnableMethodSecurity` + `@PreAuthorize` on all 3 `AdminUserServiceImpl` methods | 26 | none | **done** |
| 7 | `@Retryable` on the Stripe calls, with a Stripe idempotency key | 29 | none | **done** |
| 8 | Thymeleaf — `receipt.html` + layout fragments, `OrderReceiptController` | 15 | none | **done** |
| 9 | `search/` — `ProductDocument`, repository, service, endpoint **with a DB fallback** | 22 | **ES node** | **done**, profile `search` |
| 10 | `messaging/` — Artemis publisher + listener, JSON converter, DLQ | 30 | **broker** | **done**, profile `messaging` |
| 11 | `mail/` — `MimeMessageHelper`, body rendered from the receipt template | 31 | **SMTP sink** | **done**, off until `spring.mail.host` is set |
| 12 | `security/oauth2/` — Google login, reconciled on **verified** email only | 27 | **identity provider** | **done**, profile `oauth2` |
| 13 | `build.gradle.kts` + wrapper pinned to 8.14.3, `GRADLE.md` | 33 | none | **done**, on its own branch |

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
4. **`DefaultJmsListenerContainerFactoryConfigurer` moved** from
   `org.springframework.boot.autoconfigure.jms` to `org.springframework.boot.jms.autoconfigure` —
   Boot 4 split autoconfiguration into per-technology modules. Lesson 30.
5. **`MappingJackson2MessageConverter` is deprecated for removal** in Spring 7 (it is tied to
   Jackson 2); `JacksonJsonMessageConverter` is the Jackson 3 replacement. Lesson 30.
6. **Boot 4.1's Gradle plugin requires Gradle 8.14+.** The machine had 8.12 and the failure names
   the version but not the fix — which is the argument for committing a wrapper. Lesson 33.
7. **The stale-class trap in `pizza/CLAUDE.md` is real and cost time twice**, both times presenting
   as `NoClassDefFoundError` with an *unqualified* class name. `./mvnw clean compile` fixes it.
   Worth a callout in lesson 32.

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

## Demo-app branches

`lovemesomecoding_demo_project` is a separate repo. **Not pushed — Folau does that.**

| Branch | Holds |
|---|---|
| `main` | **merged 2026-08-18** (fast-forward): all 12 non-Gradle features, 40 files, 1 commit |
| `springboot-tutorial-examples` | same commit as `main`; can be deleted once pushed |
| `springboot-tutorial-gradle` | the above + the Gradle build, kept separate so two build files never sit on one branch and confuse an IDE import |

### Verified on `main` after the merge

- `./mvnw clean compile` clean · `./mvnw test` **60/60**
- App boots on the default `local` profile in **4.6 s** with only MySQL running — **zero** errors
  and zero connection failures in the log, which is the profile gating doing its job
- Old endpoints: menu 200, login 200, admin-with-token 200, admin-without-token 403, Swagger 200
- New endpoints: search falls back to the DB and returns real hits; `/api/search/reindex` gives
  503 with an admin token and 403 without; the Thymeleaf receipt renders real order data at
  `/orders/{id}/receipt`
- Menu cache measurably serving (first call 3.5 ms, subsequent ~1.5 ms); all **5** product write
  paths carry evictions

⚠️ **The Gradle branch's history is untidy.** Two commits landed on it during the session with the
messages `asdf` and `a`, and the first of them mixes the Gradle files together with pre-existing
uncommitted changes to `pizza/CLAUDE.md`, `pizza/progress_report.md` and 10 frontend screenshots —
none of which belong on a Gradle branch. The *content* is all correct and the build passes; only
the history is wrong. Left alone rather than rewritten, because they are Folau's commits.

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
| 2026-08-18 | Close app gaps 4, 8, 9, 10, 11, 12 — upload, Thymeleaf, ES, JMS, mail, OAuth2 | Claude | done |
| 2026-08-18 | Close app gap 13 — Gradle build + wrapper, verified `build`/`test`/`bootJar` | Claude | done |
| 2026-08-18 | Commit the demo-app work to branches (see below) | Claude | done |
| 2026-08-18 | Author 35 post bodies — 39,909 words, 326 code blocks | Claude | done |
| 2026-08-18 | `check_content.py` — 35 posts, 326 blocks round-trip byte-for-byte | Claude | done |
| 2026-08-18 | Seed local `--force-dates --write` — 35 posts, category count 35 | Claude | done |
| 2026-08-18 | Sync + build — `verify-build` 547/547, index cross-check 44/44 | Claude | done |
| 2026-08-18 | Back up the prod content tree (S3 versioning is OFF) — 674 objects | Claude | done |
| 2026-08-18 | Seed prod `--force-dates --write` — 573 posts, 35 in `/spring-boot` | Claude | done |
| 2026-08-18 | `npm run deploy` — 1523 files, edge serving `394b0bd`, all 35 URLs 200 | Claude | done |
| | Review the 35 published posts | Folau | **next** |
| | Redeploy the backend Lambda | Folau | **outstanding, inherited from the React track** |

## Publish state — LIVE

| Tree | State |
|---|---|
| `local` | 36 posts, dates 2026-06-11 … 2026-08-18 |
| `prod` | **36 posts written**, 871 posts total. ⚠️ Lesson 15 is in the content DB but the site has NOT been rebuilt — see "GraphQL" below. |
| backup | `.../backups/prod-2026-08-18-pre-springboot/` and `.../backups/prod-2026-08-25-pre-graphql/` (973 objects) |

Verified after deploy: `verify-build` 573/573 posts, 44/44 category counts agree, 746 HTML files,
1523 files uploaded, edge serving build `394b0bd`. **All 35 URLs return 200**, and Prism tokenises
the `properties` blocks live — confirming the pipeline fix end to end.

### ⚠️ The prod backup matters

**S3 object versioning is NOT enabled on the content bucket.** Overwriting a post is therefore
irreversible, and this publish rewrote 31 indexed URLs. The full prod tree was copied to
`backups/prod-2026-08-18-pre-springboot/` (674 objects, verified equal) before the first write.

**Enabling versioning on that bucket is worth doing** — it would make every future seed reversible
without a manual backup step.

## Outstanding

1. **Review the 35 published posts.** They went live without a human read.
2. **Backend Lambda not redeployed.** `properties` was added to `app/services/content.py`, but
   seeding ran the local service layer — so what is in S3 is correct while the deployed Lambda
   still has the old language list. Editing any of these 35 posts through `/admin` before
   `lovemesomecoding_backend/scripts/deploy.sh` runs would normalise every
   `application.properties` block down to `plaintext` and silently lose the highlighting. Same
   outstanding item the React track left behind — it now affects two tracks.
3. **Enable S3 object versioning** on the content bucket.
4. **Run the pizza Playwright suite** against the 12 backend features added for this track.

---

## Lesson 15 — GraphQL (2026-08-25)

Added on request. `/spring-boot/spring-boot-graphql`, dated 2026-07-08 so it sits between the
springdoc lesson and Thymeleaf — GraphQL is a web-layer topic, and that is where a reader following
the track expects it.

### ⚠️ The track was renumbered

Inserting at 15 rather than appending at 36 was a deliberate call: appending would have left GraphQL
sitting after "Interview questions", which is plainly wrong for anyone reading in order. The cost is
that everything from Thymeleaf on moved up by one, and **the numbers are load-bearing** — the index
in lesson 1 numbers them, and 22 `lesson N` cross-references in the post bodies point at them. All of
it was shifted together:

- `posts/15..35-*.html` → `16..36-*.html` (`git mv`, so the history follows)
- every `lesson N` for N ≥ 15 bumped by one, descending so the replacements cannot collide
- lesson 1's index: GraphQL inserted into Part 3, and the `<ol start=…>` on Parts 4-7 bumped
- lesson 14's "Next" now points at GraphQL; GraphQL's points at Thymeleaf
- the cheat sheet (now 35) gained a GraphQL section and an eleventh silent failure

`check_content.py` passes: 36 posts, 353 code blocks, every sample round-trips byte-for-byte. A link
audit confirms all 36 slugs resolve.

### Demo app

Branch `springboot-tutorial-graphql` in `lovemesomecoding_demo_project`, commit 707b9fa, **not
merged to main**. `com.pizza.api.graphql` + `resources/graphql/pizza.graphqls`, calling the same
services the REST controllers call. 72 tests (9 new). Full detail in `pizza/progress_report.md`.

Two defects it surfaced, both of which would have shipped: `Principal` throws rather than being null
for an anonymous GraphQL caller (guest checkout was broken), and a `ConstraintViolationException`
from `@Valid` has no mapping, so validation failures were opaque `INTERNAL_ERROR`s.

### Claims verified by running them, not by assuming

- **No schema file ⇒ no endpoint, silently.** The autoconfiguration is gated on
  `@ConditionalOnGraphQlSchema`, so the app boots normally and 404s. My first draft said it fails the
  context, which is what most Boot starters do — it does not. Booted with the schema removed from
  both `src/main/resources` and `target/classes` to check.
- **A declared-but-unimplemented scalar DOES fail the context**, with
  `SchemaProblem{errors=[There is no scalar implementation for the named 'UUID' scalar type…]}`.
  Booted with the scalar registration removed.
- **Schema inspection is a report, not a gate** — it logs unmapped fields and carries on.
- Anonymous mutation → `UNAUTHORIZED`, customer token → `FORBIDDEN`, admin token → passes the gate
  (checked with a nonexistent id so nothing was actually mutated). All read off the running app.

### State: saved, NOT published

The prod content DB has the post; **the site has not been rebuilt**, so nothing is live yet. The
build was run locally and passes — `verify-build` 871/871 posts, 42/42 category counts, 1102 HTML
files, and `out/spring-boot/spring-boot-graphql.html` renders with 929 Prism spans and the right
prev/next neighbours.

⚠️ **Deploying needs a decision first.** `lovemesomecoding_frontend` has four uncommitted files
(`nav.ts`, `pages.ts`, `postbuild.mjs`, `cloudfront-function.js`) from the 2026-08-24 brainteaser
retirement. `npm run deploy` would ship those too. They look complete and match the current content
DB, but they are not mine to publish.

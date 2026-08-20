# Backend Dev track — progress report

**Status:** WRITTEN AND SEEDED TO LOCAL — awaiting Folau's review before prod
**Started:** 2026-08-18
**Where it lands:** https://lovemesomecoding.com/backend-dev

---

## What this is

`/backend-dev` is not a tutorial track today. It is a **2-post stub** published 2020-01-19 and
untouched since.

| Slug | Title | Words | Code | `<h2>` | Tags |
|---|---|---:|---:|---:|---:|
| `backend-dev-what-is-a-backend-engineer` | Backend – What is a backend engineer? | 88 | 0 | 0 | 0 |
| `backend-dev-what-to-learn-in-a-framework` | Backend – What to learn in a framework? | 304 | 0 | 0 | 0 |
| | **total** | **392** | **0** | | |

Both bodies still carry the WordPress `boldgrid` wrapper `<div>`s and `class=""` noise from the
migration. Neither uses `<h2>`, so **neither has a table of contents**. Between them they contain
**zero lines of code** — the second post is a bare bullet list of ten topic headings with no
explanation and no example under any of them.

This project turns `/backend-dev` into a **10-post track**: the 2 rewritten **in place** (same
slugs, so no indexed URL is lost) plus 8 new.

## The conflict this track had to resolve

`README.md` originally said *"update java **datastructure** tutorial posts on
https://lovemesomecoding.com/backend-dev"*. That sentence was copy-pasted from
`projects/java_datastructure/README.md` — same wording, but that project targets
`/data-structure-algorithm`. Data structures have nothing to do with the two posts at
`/backend-dev`.

Flagged to Folau before any writing started. **Decision: build out `/backend-dev` as a backend-engineering
track.** Independently confirmed while auditing — a peer session named `java_datastructure` is doing
that other track right now (see *Concurrency hazard* below), so the two are genuinely separate
pieces of work.

**Folau then fixed the README** (2026-08-18): it now reads *"update **java backend dev** posts on
https://lovemesomecoding.com/backend-dev"*. That resolves the conflict and adds one constraint —
the track is explicitly **Java** backend, so Java 21 / Spring Boot 4.1 is the stack throughout
rather than one illustration among several.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Intent | **Build out `/backend-dev`**, ignore the "java datastructure" phrase | Folau, 2026-08-18. The phrase is a copy-paste slip from a sibling project that is separately in flight. |
| Track size | **10** — 2 rewritten + 8 new | Folau's call ("~8-10"). Matches the depth of `/spring-study-guide`. |
| Existing 2 posts | Rewrite in place, keep both slugs | They are indexed URLs. Rewriting keeps the ranking and kills the 2020 content in one move. |
| Positioning | **A Java backend roadmap** — concepts first, one real Boot 4.1 snippet each, then a link out | See below — this is the decision that keeps the track from duplicating `/spring-boot`. |
| Stack | **Java 21 / Spring Boot 4.1**, stated once and assumed | The corrected README says "java backend dev". Matches the demo app and every sibling Java track. |
| Snippets | Lifted from `pizza-springboot-backend` | Per `CLAUDE.md`. Every sample is provably compiling Boot 4.1 / Java 21 code. |
| Dates | Restamped 2026-07-31 … 2026-08-18, 2 days apart, at **11:00** | Both old posts carry `2020-01-19`, which `upsert_post` never overwrites — hence `seed.py --force-dates`. 11:00 avoids ties with `/spring-boot` (09:00), the DS&A track (10:00) and `/spring-study-guide` (14:00). |
| Publish | **Seed local → Folau reviews → prod** | Folau's call. |
| `/frontend-dev` | Out of scope | The mirror-image 2-post stub, same 2019 vintage, same problems. The README names `/backend-dev` only. Worth its own project later. |
| Demo-app changes | **None expected** | See below. |

### The positioning decision — why this track is not another Spring track

`/backend-dev` sits next to tracks that already teach these topics in depth:

| Already covered by | Posts |
|---|---:|
| `/spring-boot` | 35 |
| `/sql` | 42 |
| `/aws` | 33 |
| `/java-8`, `/java` | 36 + 28 |
| `/data-structure-algorithm` | 25 |
| `/swedesignpattern` | 16 |
| `/elasticsearch` | 13 |
| `/git`, `/linux` | 14 + 14 |
| `/spring-study-guide` | 9 |
| `/system-design` | 7 |

Re-teaching `@Transactional` here would be the eleventh place on the site it appears. So the rule
for this track is:

> **Explain the concept plainly and stack-independently, show it once in real Java 21 / Boot 4.1
> code, then link to the deep post.**

`/backend-dev` answers *"what do I need to learn, in what order, and why does it matter"*. The deep
tracks answer *"how do I do it in Spring"*. A reader should be able to finish this track and know
what the other 200 posts are for.

The concept half stays stack-independent on purpose — an index, a cache, a JWT and an idempotent
`PUT` are not Java ideas — but every example is Java, because that is what the README asks for and
what the rest of the site teaches.

That also makes it the right landing spot for the audience `CLAUDE.md` names first — *aspiring
developers who want to know what they need to know to start a career in programming*.

### No demo-app changes needed

`pizza-springboot-backend` on `main` already has real code for every topic in the track:

| Topic | Backed by |
|---|---|
| Java & the JVM | Java 21 throughout, `entity/**`, records in `dto/**`, `ThreadPoolConfig`, `Optional`/stream use across `*ServiceImpl` |
| Framework | `PizzaProperties`, `CacheConfig`, `RestMVCConfig`, `SecurityConfig`, `OpenApiConfig`, 5 `application-*.properties` profiles |
| HTTP & API design | 9 `*RestController`, `dto/**` + `EntityDTOMapper`, `exception/RestExceptionHandler` + `ApiError`, `OpenApiConfig` |
| Databases | `entity/**` (JPA), the 8 `*Repository`, the 6 `*DAOImp` + `mapper/`, `db/changelog/` (Liquibase) |
| Auth & security | `SecurityConfig`, `JwtService`, `JwtAuthenticationFilter`, `security/oauth2/`, `@PreAuthorize` on `AdminUserServiceImpl` |
| Caching, async, messaging | `CacheConfig`, `ThreadPoolConfig`, `OrderPlacedEvent`/`OrderPlacedListener`, `messaging/` (Artemis), `mail/`, `payment/StripeService` |
| Testing | the test suite — `ApiSecurityIntegrationTest`, `OrderApiIntegrationTest`, `PricingServiceTest`, `ProductServiceImplTest`, `ReportServiceImplTest`, 2 DAO integration tests |
| Deploy & observability | `pom.xml`, `application-docker.properties`, `aspect/ServiceTimingAspect` |

**So this track is content-only.** No branch, no app edits, no new infrastructure.

## Versions the track is written against

Read off `pizza-springboot-backend/pom.xml` and **verified against the resolved jars and the Boot
4.1.0 BOM**, not from memory. That check caught a wrong claim — see *Two things found by checking*
below.

| | | Verified from |
|---|---|---|
| Spring Boot | **4.1.0** | `pom.xml` parent |
| Java | **21** | `pom.xml` `<java.version>` |
| Jakarta EE | **11** (`jakarta.*`, never `javax.*`) | BOM: persistence 3.2.0, validation 3.1.1, servlet 6.1.0 |
| JUnit | **6.0.3** (Jupiter) | BOM `<junit-jupiter.version>`; app does not override |
| Hibernate | 7.4.1.Final | BOM `<hibernate.version>` |
| Database | MySQL 8.4 | `docker-compose.yml` |

JUnit 6 kept the `org.junit.jupiter.api` package and the same annotations, so every test snippet in
the track is unaffected by the correction.

## Topic list

Reading order is the order a person actually learns these. `date` ascends with the track so the
prev/next pager reads 1 → 10 and the archive lists it correctly newest-first.

| # | Slug | Title | State | Date |
|---|------|-------|-------|------|
| 1 | `backend-dev-get-started` | Backend Dev – Get Started | **new** | 2026-07-31 |
| 2 | `backend-dev-what-is-a-backend-engineer` | Backend Dev – What a Backend Engineer Actually Does | rewrite | 2026-08-02 |
| 3 | `backend-dev-java-and-the-jvm` | Backend Dev – The Java and the JVM You Actually Need | **new** | 2026-08-04 |
| 4 | `backend-dev-what-to-learn-in-a-framework` | Backend Dev – What to Learn in a Framework | rewrite | 2026-08-06 |
| 5 | `backend-dev-apis-and-http` | Backend Dev – HTTP and API Design | **new** | 2026-08-08 |
| 6 | `backend-dev-databases` | Backend Dev – Databases | **new** | 2026-08-10 |
| 7 | `backend-dev-auth-and-security` | Backend Dev – Authentication, Authorization and Security | **new** | 2026-08-12 |
| 8 | `backend-dev-caching-async-and-messaging` | Backend Dev – Caching, Async Work and Messaging | **new** | 2026-08-14 |
| 9 | `backend-dev-testing` | Backend Dev – Testing | **new** | 2026-08-16 |
| 10 | `backend-dev-deployment-and-observability` | Backend Dev – Deployment and Observability | **new** | 2026-08-18 |

The ten headings in the old `what-to-learn-in-a-framework` post are the skeleton posts 4–10 flesh
out. Nothing in the old list is dropped; the "Optionals" tail (OAuth2, Swagger, Docker, AWS,
Elasticsearch, batch jobs) is redistributed into the post each item actually belongs to instead of
being parked at the bottom as an afterthought.

## What "keep posts to the point" means here

The two old posts fail in opposite directions, and the rewrite rule differs per post:

- `what-is-a-backend-engineer` is **88 words** — a single paragraph that says almost nothing and
  contains a grammar error (*"Backend engineers are usually write the web services"*). It needs to
  **grow**.
- `what-to-learn-in-a-framework` is **304 words of bullet points** — ten headings, no prose, no
  code, no explanation of why any item is on the list. It is a table of contents pretending to be a
  post. It needs to be **rewritten, not extended**.

For the new posts the rule is: **the concept in a sentence, then real code, then the one caveat
that actually bites, then the link to the deep post.** Target ≈1,200–1,800 words each — enough to
be useful standalone, short enough that a beginner finishes it.

Every post gets `<h2>` sections, which neither old post had, so the table of contents works.

## Files

```
projects/backend_dev/
  README.md            the requirements
  progress_report.md   this file
  manifest.py          category metadata + one entry per post
  posts/NN-slug.html   post bodies, plain semantic HTML
  seed.py              writes the posts into a content tree
  check_content.py     proves the normaliser round-trips every code sample
  check_links.py       HTML well-formedness + every internal link resolves
  check_snippets.py    every code line really exists in the demo app source
```

`seed.py` and `check_content.py` are lifted from `projects/spring_study_guide/`. They run the
backend's own service layer so the posts and the derived indexes cannot drift.

`check_links.py` and `check_snippets.py` are **new in this track** and worth keeping. The snippet
checker is the one that earns its place: it takes every substantial line out of every code block and
requires it to appear somewhere in the demo app source, so a snippet cannot quietly drift into
invention. It normalises the edits a post is allowed to make (an elided `{ ... }` body, an added
trailing comment) and keeps a short, individually justified allowlist for the handful of lines
written for the page. Run all three before seeding:

```bash
python projects/backend_dev/check_content.py
AWS_PROFILE=folau python projects/backend_dev/check_links.py
python projects/backend_dev/check_snippets.py
```

## ⚠️ Concurrency hazard — a peer session is writing to prod

A second interactive session, **`java_datastructure`**, is running against this same repo and the
same S3 content tree, and it is **already writing to prod**. Observed during this audit:

- The first `list_categories()` read of the session returned `data-structure-algorithm: 24` and
  **574** published posts.
- A read minutes later returned **25** and **575** — a new post,
  `data-structure-algorithm-get-started` (dated `2026-07-01T10:00:00`), had appeared in prod
  in between.

Consequences for this track, all of them at publish time:

1. **Do not seed prod while that session is mid-publish.** Both seeds rewrite `index/posts.json`,
   `index/categories.json` and `search/index.json`. These are read-modify-write on whole objects
   with no locking, so two overlapping seeds mean the second one's read happens before the first
   one's write lands and a category silently loses its posts from the indexes. Check `ListAgents`
   immediately before seeding prod.
2. **Take the prod backup at publish time, not now.** A backup taken today would be stale by the
   time this track is ready, and restoring it would roll back the other track.
3. **Re-audit the counts right before and right after seeding.** `verify-build.mjs` check 6
   cross-checks the indexes against each other; the drift this would produce is exactly the class
   of bug that shipped `/oracle` reading "12 tutorials" over a list of 13.

Checked at planning time: prod and local both agree with themselves — 575/549 published posts, 44
categories, **every category count matches the actual post list in both trees**. That is the
baseline to compare against later.

**Update, end of session:** the `java_datastructure` session has exited. Prod finished at **575**
posts with all 44 category counts agreeing, so its publish landed cleanly and nothing this project
did touched it. The hazard above still applies to the prod seed whenever that happens — check
`ListAgents` first, and re-run the count check before and after.

## Task log

| Date | Task | Owner | Status |
|---|---|---|---|
| 2026-08-18 | Audit the 2 live posts — words, dates, markup state, code count | Claude | done |
| 2026-08-18 | Flag the "java datastructure vs. backend-dev" README conflict | Claude | done |
| 2026-08-18 | Agree intent, track size and publish path | Folau | done |
| 2026-08-18 | Survey sibling categories to fix positioning and avoid duplication | Claude | done |
| 2026-08-18 | Confirm the demo app covers all 10 topics — no app gaps | Claude | done |
| 2026-08-18 | Baseline prod/local counts; find the concurrent-session hazard | Claude | done |
| 2026-08-18 | Write this progress report + the 10-post topic table | Claude | done |
| 2026-08-18 | README corrected by Folau to "java backend dev" — conflict closed | Folau | done |
| 2026-08-18 | Scaffold `manifest.py` / `seed.py` / `check_content.py` | Claude | done |
| 2026-08-18 | Author 10 post bodies — 15,101 words, 52 code blocks | Claude | done |
| 2026-08-18 | `check_content.py` — 52 blocks round-trip byte-for-byte | Claude | done |
| 2026-08-18 | Write `check_links.py`; 46 internal links resolve, HTML well-formed | Claude | done |
| 2026-08-18 | Write `check_snippets.py`; 244 code lines verified against the app | Claude | done |
| 2026-08-18 | Verify version claims against the resolved jars — **found 1 error** | Claude | done |
| 2026-08-18 | Verify snippets against the demo app — **found 1 dead config rule** | Claude | done |
| 2026-08-18 | Seed local `--force-dates --write` — 10 posts, category count 10 | Claude | done |
| 2026-08-18 | Build + `verify-build` — 557/557 posts, 44/44 counts agree | Claude | done |
| 2026-08-18 | Serve built output — all 10 URLs 200, Prism tokenises, no legacy markup | Claude | done |
| 2026-08-18 | Restore the frontend content dir to prod so no stray deploy leaks local | Claude | done |
| 2026-08-20 | Read the 10 posts; approve for publish | Folau | done |
| 2026-08-20 | Back up the prod tree to scratchpad (versioning is still off) | Claude | done |
| 2026-08-20 | Seed prod `--force-dates --write` — 583 posts (was 575) | Claude | done |
| 2026-08-20 | Build + `verify-build` — 583/583 posts, 44/44 counts agree | Claude | done |
| 2026-08-20 | `npm run deploy` — 1,547 files, CF function republished, invalidated | Claude | done |
| 2026-08-20 | Verify live — all 10 URLs 200, in sitemap, no 2020 dates | Claude | done |

## Publish state

**Published 2026-08-20.** The track is live.

| Tree | State |
|---|---|
| `prod` | **10 posts** live at `/backend-dev`, dates 2026-07-31 … 2026-08-18. 583 posts in the tree (was 575). |
| `local` | 557 posts — the review tree, now behind prod. Re-seed it before the next round of edits. |
| backup | `scratchpad/prod-backup-20260820/` — the full 575-post prod tree as it stood before the seed (680 objects). Session-scoped, so it will not survive indefinitely. |
| edge | build `394b0bd`, invalidation `I849WPEQ0C6WZSXMQ8YWSFM6U3` complete; `version.txt` matches |

### Verified live

All 10 URLs return 200 and carry no `boldgrid` markup. Prism tokenises every code block
(114–464 tokens per page; `get-started` has none because it has no code). The archive returns 200
with **no 2020 date remaining**, and all 10 posts are in `sitemap.xml`. `verify-build` reported
583/583 posts and 44/44 category counts agreeing before the upload, and the prod indexes
cross-check clean after it — no drift from the concurrent sessions.

### Verified against the local tree (pre-publish)

`verify-build` reports 557/557 posts and 44/44 category counts agreeing, 727 HTML files emitted.
Serving the built output: all 10 URLs return 200, the archive lists all 10 in reading order, the
prev/next pager walks 1 → 10, all 10 are in the sitemap, **no page carries the `boldgrid` markup any
more**, no 2020 date remains, and Prism tokenises every code block (114–464 tokens per page;
`get-started` has none because it has no code). Every content heading carries an anchor id — the
only id-less `<h3>` on a page is the site template's own category label.

### Word counts — before and after

| Post | Before | After |
|---|---:|---:|
| get-started | — | 926 |
| what-is-a-backend-engineer | 88 | 1,218 |
| java-and-the-jvm | — | 1,518 |
| what-to-learn-in-a-framework | 304 | 1,619 |
| apis-and-http | — | 1,544 |
| databases | — | 1,821 |
| auth-and-security | — | 1,678 |
| caching-async-and-messaging | — | 1,797 |
| testing | — | 1,347 |
| deployment-and-observability | — | 1,634 |
| **total** | **392** | **15,102** |

The two rewrites went in opposite directions on purpose, as planned: the 88-word stub grew into a
real post, and the 304-word bullet list was replaced rather than extended — none of its ten headings
was dropped, they became the spine of posts 4–10.

## Two things found by checking rather than assuming

Recorded because both were wrong in the draft and would have shipped.

1. **Spring Boot 4.1 ships JUnit Jupiter 6, not 5.** The draft's version table said
   *"JUnit 5 (Jupiter)"* — copied from the `/spring-study-guide` landing page and from habit.
   Reading `spring-boot-dependencies-4.1.0.pom` shows `<junit-jupiter.version>6.0.3</junit-jupiter.version>`,
   the demo app's `pom.xml` does not override it, and `junit-jupiter-api-6.0.3.jar` is what resolves.
   Corrected on the landing page and in `manifest.py`. **No snippet was affected** — Jupiter 6 kept
   the `org.junit.jupiter.api` package and the same annotations, which is precisely why the error is
   easy to make and invisible in the code.

   ⚠️ **The same wrong claim is published on `/spring-study-guide`.** Re-confirmed live on
   2026-08-20: it is the post `/spring-study-guide/spring-study-guide-get-started`, in its versions
   table, row "JUnit | 5 (Jupiter)" — not the category landing page, as first recorded. The other
   JUnit mentions on that track ("`@RunWith(SpringRunner.class)` → JUnit 5", and the JUnit 5
   extension wording in `spring-study-guide-testing`) are about migrating off JUnit 4 and are
   correct as written — only the versions-table row is wrong. Out of scope for this
   project, but it is live and it is wrong. Listed under Outstanding.

2. **The demo app permits `/actuator/health` but has no Actuator dependency.** `SecurityConfig`
   carries `.requestMatchers("/actuator/health").permitAll()`, and `grep -r actuator` over the whole
   project finds nothing else — not in `pom.xml`, not in any properties file. So the rule is dead
   and the path returns 404. The draft quoted that matcher as if it demonstrated a working health
   check. Rather than drop the snippet, post 10 now says exactly this and makes it the lesson:
   nothing fails at startup to tell you, and a probe pointed at a URL that does not exist looks
   identical to a healthy one until the load balancer starts failing every instance.

Verified and correct as written: Jakarta EE 11 (`jakarta.persistence-api` 3.2.0,
`jakarta.validation-api` 3.1.1, `jakarta.servlet-api` 6.1.0 in the Boot 4.1 BOM), Spring Boot 4.1.0
and Java 21 off the demo app's `pom.xml`, and all 244 substantial code lines across the 52 blocks
appear in the demo app source.

### On the snippet allowlist

`check_snippets.py` flagged 14 lines on its first run. Every one was inspected by hand; none was
invented code. Eleven were safe edit forms now normalised automatically (an elided `{ ... }` body, a
trailing explanatory comment added for the page, a line the formatter had split). The remaining
seven sit in an allowlist with a one-line justification each — the largest being that
`RestExceptionHandler` does not import `HttpStatus`, so the real source spells it
`org.springframework.http.HttpStatus.BAD_REQUEST` and the posts shorten it.


## Outstanding / inherited

1. **Enable S3 object versioning on the content bucket.** Still off. Four tracks have now each
   needed a manual backup step that one bucket setting would make unnecessary. With two sessions
   writing to the same tree concurrently, this stopped being a nice-to-have.
2. **Backend Lambda still not redeployed** — inherited from the React, Spring Boot and Spring Study
   Guide tracks. Seeding runs the local service layer, so what lands in S3 is correct; but editing
   any of these posts through `/admin` before `lovemesomecoding_backend/scripts/deploy.sh` runs
   would normalise `properties` blocks down to `plaintext`. Would now affect four tracks.
3. **`/frontend-dev` is the same stub problem** — 2 posts, 311 words total, 2019, same boldgrid
   markup, no headings, no code. Deliberately out of scope here; flagging it so it is not
   forgotten. It is the exact mirror of what this project just fixed, so the tooling here would
   transplant onto it almost unchanged.
4. **`/spring-study-guide` states the wrong JUnit version, live.** See finding 1 above. A one-line
   fix to `projects/spring_study_guide/posts/01-spring-study-guide-get-started.html` plus a re-seed
   and deploy. Worth folding into whatever the next publish of that track is rather than deploying
   on its own.
5. **The demo app's dead `/actuator/health` rule.** See finding 2. Either add
   `spring-boot-starter-actuator` so the rule means something, or delete the matcher. Post 10 links
   its lesson to this, so if it is fixed, that paragraph needs a revisit.

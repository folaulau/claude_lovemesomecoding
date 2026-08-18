# Spring Study Guide track — progress report

**Status:** PUBLISHED — live on prod, 2026-08-18
**Started:** 2026-08-18
**Where it lands:** https://lovemesomecoding.com/spring-study-guide

---

## What this is

`/spring-study-guide` holds **8 posts published 2019-08-21** (last touched 2022). They are the
**Spring Professional Certification study guide** — one post per exam topic area, written as
question-and-answer, against **Spring 5 / Spring Boot 2**.

| Slug | Title | Words | Read | Questions | Code |
|---|---|---|---:|---:|---:|
| `spring-study-guide-core` | Core Spring | 4,734 | 22 min | ~38 | 34 |
| `spring-study-guide-aop` | AOP | 1,014 | 5 min | 15 | 2 |
| `spring-study-guide-data-integration` | Data Integration | 7,454 | 34 min | 37 | 27 |
| `spring-study-guide-spring-boot` | Spring Boot | 1,953 | 9 min | 12 | 6 |
| `spring-study-guide-web-layer` | Web Layer | 2,392 | 11 min | 21 | 5 |
| `spring-study-guide-security` | Security | 2,859 | 13 min | 16 | 11 |
| `spring-study-guide-rest` | REST | 1,862 | 8 min | 22 | 8 |
| `spring-study-guide-testing` | Testing | 1,209 | 5 min | ~9 | 10 |
| | **total** | **23,477** | | **~170** | **103** |

Every body still carries the WordPress `boldgrid` wrapper `<div>`s, empty `wp-block-embed`
figures and `class=""` noise from the migration. None uses `<h2>` — so **none of the 8 has a
table of contents**, on posts that run up to 34 minutes.

This project rewrites all 8 **in place** — same slugs, so no indexed URL is lost — against
**Spring Framework 7 / Spring Boot 4.1 / Java 21**, and adds a landing page.

**Result: a 9-post track.**

## The conflict this track had to resolve

The README asks for "the latest version of Spring." These posts are structured around the
**Spring Professional certification**, and that exam has *not* moved: Broadcom's current
2V0-72.22 still targets Spring 5.3 / Boot 2.x. There is no Spring 6 or Spring 7 exam.

"Latest Spring" and "matches the current exam" cannot both be true. Flagged to Folau before any
writing started; **decision: write against Spring 7 / Boot 4.1 and drop the exam framing.**

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Framing | **Keep Q&A, drop the exam** | The question-and-answer shape is what makes this track distinct from the 35-post `/spring-boot` tutorial track. Positioned as "know these answers to work with — or interview on — Spring." Folau, 2026-08-18. |
| Spring version | **Framework 7.0.8 / Boot 4.1.0 / Java 21** | Matches the demo app and the `/spring-boot` track. Anything else means shipping content that is stale the day it publishes. |
| Existing 8 posts | Rewrite in place, keep every slug | They are indexed URLs. Rewriting keeps the ranking and kills the Spring 5 content in one move. |
| Track size | **9** — 8 rewritten + 1 landing page | Folau's call. Trim `data-integration` hard rather than splitting it, so no new sibling slugs appear mid-track. |
| Snippets | Lifted from `pizza-springboot-backend` | Per `CLAUDE.md`. Every sample is provably compiling Boot 4.1 / Java 21 code. |
| Dates | Restamped 2026-08-02 … 2026-08-18, 2 days apart, at **14:00** | The old posts all carry `2019-08-21`, which `upsert_post` never overwrites — hence `seed.py --force-dates`. 14:00 avoids an exact tie with the `/spring-boot` track's 09:00 stamps. |
| Publish | **Seed local → Folau reviews → prod** | Folau's call. The `/spring-boot` track went live unreviewed; this one will not. |
| Sibling categories | Out of scope | `spring-boot` (35), `spring-data` (15), `spring-interview` (5) are separate categories. The README names `/spring-study-guide` only. |
| Demo-app changes | **None expected** | Unlike the `/spring-boot` track, which needed 13 features added. See below. |

### No demo-app changes needed

The `/spring-boot` track already added everything. `pizza-springboot-backend` on `main` now covers
all 8 topic areas with real code:

| Topic | Backed by |
|---|---|
| Core | `PizzaProperties`, `CacheConfig`, `OpenApiConfig`, `RestMVCConfig`, `ThreadPoolConfig`, `SecurityConfig`, every `*ServiceImpl` |
| AOP | `aspect/ServiceTimingAspect` |
| Data | `Product`, `CustomerOrder`, the 8 `*Repository` interfaces, `ReportDAOImp` + `mapper/`, `db/changelog/` |
| Spring Boot | `pom.xml`, `application.properties`, 4 `@Profile` uses |
| Web | `RestMVCConfig`, `OrderReceiptController` + Thymeleaf templates |
| REST | 9 `*RestController`, `RestExceptionHandler`, `ApiError`, `EntityDTOMapper` |
| Security | `SecurityConfig`, `JwtService`, `JwtAuthenticationFilter`, `@PreAuthorize` on `AdminUserServiceImpl`, `security/oauth2/` |
| Testing | the 60-test suite — `ApiSecurityIntegrationTest`, `OrderApiIntegrationTest`, `PricingServiceTest`, `ProductServiceImplTest`, 2 DAO integration tests |

**So this track is content-only.** No branch, no app edits, no new infrastructure.

## Versions the track is written against

Read off `pizza-springboot-backend/pom.xml`. Stated on the landing page and assumed throughout.

| | |
|---|---|
| Spring Boot | **4.1.0** |
| Spring Framework | **7.0.8** |
| Java | **21** |
| Jakarta EE | 11 (`jakarta.*`, not `javax.*`) |
| JUnit | 5 (Jupiter) |
| Hibernate | Boot-managed |
| jjwt | 0.12.6 |

## Topic list

Reading order = the classic exam topic order, which is also a sound learning order. `date` ascends
with the track so the prev/next pager reads 1 → 9.

| # | Slug | Title | State | Date |
|---|------|-------|-------|------|
| 1 | `spring-study-guide-get-started` | Get Started | **new** | 2026-08-02 |
| 2 | `spring-study-guide-core` | Core Spring — Container, Beans, DI | rewrite | 2026-08-04 |
| 3 | `spring-study-guide-aop` | AOP | rewrite | 2026-08-06 |
| 4 | `spring-study-guide-data-integration` | Data Integration — JDBC, Transactions, JPA | rewrite | 2026-08-08 |
| 5 | `spring-study-guide-spring-boot` | Spring Boot | rewrite | 2026-08-10 |
| 6 | `spring-study-guide-web-layer` | Web Layer — Spring MVC | rewrite | 2026-08-12 |
| 7 | `spring-study-guide-rest` | REST | rewrite | 2026-08-14 |
| 8 | `spring-study-guide-security` | Security | rewrite | 2026-08-16 |
| 9 | `spring-study-guide-testing` | Testing | rewrite | 2026-08-18 |

## What "keep posts to the point" means here

The old posts pad answers with restatements and dumps of XML config nobody writes any more.
The rewrite rule per answer: **a direct sentence first, then the code, then only the caveat that
actually bites.** Target ≈2,000–3,000 words per topic post against the old 1,000–7,500 spread —
so `data-integration` shrinks hard while `aop` and `testing` grow.

Every post gets `<h2>` sections, which the old ones lacked, so the table of contents works.

## Files

```
projects/spring_study_guide/
  README.md            the requirements
  progress_report.md   this file
  manifest.py          category metadata + one entry per post
  posts/NN-slug.html   post bodies, plain semantic HTML
  seed.py              writes the posts into a content tree
  check_content.py     proves the normaliser round-trips every code sample
```

`seed.py` and `check_content.py` are lifted from `projects/springboot_tutorial/`, which lifted
them from `projects/react_tutorial/`. They run the backend's own service layer so the posts and
the derived indexes cannot drift.

## Task log

| Date | Task | Owner | Status |
|---|---|---|---|
| 2026-08-18 | Audit the 8 live posts — words, dates, questions, markup state | Claude | done |
| 2026-08-18 | Extract all ~170 existing questions for triage | Claude | done |
| 2026-08-18 | Confirm the demo app covers all 8 topics — no app gaps | Claude | done |
| 2026-08-18 | Flag the "latest Spring vs. current exam" conflict | Claude | done |
| 2026-08-18 | Agree framing, track size, snippet source, publish path | Folau | done |
| 2026-08-18 | Write this progress report + the 9-post topic table | Claude | done |
| 2026-08-18 | Scaffold `manifest.py` / `seed.py` / `check_content.py` | Claude | done |
| 2026-08-18 | Author 9 post bodies — 14,750 words, 59 code blocks | Claude | done |
| 2026-08-18 | `check_content.py` — 59 blocks round-trip byte-for-byte | Claude | done |
| 2026-08-18 | HTML well-formedness + internal-link check across all 9 | Claude | done |
| 2026-08-18 | Verify version claims against the resolved jars — found 1 error | Claude | done |
| 2026-08-18 | Verify snippets against the demo app source — found 1 bug | Claude | done |
| 2026-08-18 | Seed local `--force-dates --write` — 9 posts, category count 9 | Claude | done |
| 2026-08-18 | Build + `verify-build` — 548/548 posts, 44/44 counts agree | Claude | done |
| 2026-08-18 | Serve built output, confirm all 9 URLs 200 and Prism tokenises | Claude | done |
| 2026-08-18 | Folau authorised publishing without a pre-review | Folau | done |
| 2026-08-18 | Back up the prod tree — 678 objects, verified key+size | Claude | done |
| 2026-08-18 | Seed prod `--force-dates --write` — 574 posts, 9 in the category | Claude | done |
| 2026-08-18 | Build against prod content — `verify-build` 574/574, 44/44 | Claude | done |
| 2026-08-18 | `npm run deploy` — 1525 files, invalidated, edge verified | Claude | done |
| 2026-08-18 | Verify live — all 9 URLs 200, new content, no legacy markup | Claude | done |
| | **Read the 9 published posts** | **Folau** | **next** |

## Publish state

| Tree | State |
|---|---|
| `local` | 9 posts, dates 2026-08-02 … 2026-08-18. 548 posts in the tree. |
| `prod` | **9 posts LIVE**, 574 posts total (was 573) |
| backup | `s3://lovemesomecoding-db-.../lovemesomecoding/backups/prod-2026-08-18-pre-spring-study-guide/` |

Verified live after deploy: all 9 URLs return 200, each serves the rewritten body (checked for a
distinctive marker per post), **no page still carries the `boldgrid` / `wp-block-embed` markup**,
Prism tokenises every block (241–488 tokens per page), the archive lists the 9 in reading order,
the sitemap holds all 9, and no 2019 date remains on the archive. `verify-build` 574/574 posts and
44/44 category counts agree; 1525 files uploaded and the edge confirmed serving the new build.

Verified against the local tree: `verify-build` 548/548 posts, 44/44 category counts agree, 716
HTML files emitted, all 9 URLs return 200 off the built output, and Prism tokenises every block
(241–488 tokens per page). The category archive lists the 9 in reading order, and all 14 `<h2>`
anchors on the longest post carry ids.

### Word counts — before and after

| Post | Before | After |
|---|---:|---:|
| get-started | — | 675 |
| core | 4,734 | 2,382 |
| aop | 1,014 | 1,284 |
| data-integration | 7,454 | 2,677 |
| spring-boot | 1,953 | 1,320 |
| web-layer | 2,392 | 1,489 |
| rest | 1,862 | 1,618 |
| security | 2,859 | 1,807 |
| testing | 1,209 | 1,509 |
| **total** | **23,477** | **14,761** |

`data-integration` went from a 34-minute read to 12 while gaining coverage; `aop` and `testing`
grew, because both were thin. That is what "keep posts to the point" cashed out as.

### ⚠️ The prod backup matters

**S3 object versioning is still NOT enabled on the content bucket** — confirmed again before this
publish (`get-bucket-versioning` returns empty). Overwriting a post is therefore irreversible, and
this publish rewrote 8 indexed URLs. The full prod tree was copied to
`backups/prod-2026-08-18-pre-spring-study-guide/` first — 678 objects, verified equal on key
*and* size, not just count.

**Enabling versioning on that bucket is still worth doing.** Three tracks have now each needed a
manual backup step that one bucket setting would make unnecessary.

## Two things found by checking rather than assuming

Recorded because both were wrong in the draft and would have shipped.

1. **`spring-boot-starter-web` was NOT renamed in Boot 4.** The draft said it was, by analogy with
   the aop starter. Checking `spring-boot-dependencies-4.1.0.pom` shows it is still in the BOM,
   marked *"deprecated in favor of spring-boot-starter-webmvc"*, and it resolves to the same
   dependencies — so an unchanged pom keeps building. `spring-boot-starter-aop` is the opposite:
   gone from the BOM entirely, so an unchanged pom fails with *"version is missing"*. Two renames
   in one release with two different migration stories. Corrected in posts 1, 5 and 7, and the
   contrast is now the point being made rather than a glossed-over detail.
2. **The illustrative Mockito test stubbed the wrong method.** It stubbed
   `productDAO.findByPublicId(...)`, but `PricingService.price()` calls
   `findByPublicIdWithSizes(...)`. Both exist on `ProductDAO`, so it compiles — and the stub would
   simply never match, failing for a reason unrelated to the behaviour under test. Fixed, and the
   trap is now called out in the snippet's comment.

Verified and correct as written: Spring Security 7 really does expose only the `Customizer`
overloads on `HttpSecurity` (`javap` on `spring-security-config-7.1.0`), and `RestTestClient` and
`MockitoBean` both exist in `spring-test-7.0.8`.

## Outstanding

1. **Read the 9 published posts.** Folau authorised publishing without a pre-review, so they went
   live unread — same as the `/spring-boot` track. Rolling one back means re-seeding that slug from
   the backup below.
2. **No visual QA was done.** The Chrome extension was not connected, so verification was at the
   rendered-HTML level — status codes, content markers, Prism tokens, table and heading structure,
   no escaping defects — never a human look at a rendered page.
3. **Backend Lambda still not redeployed** — inherited from the React and Spring Boot tracks.
   Seeding runs the local service layer, so what lands in S3 is correct; but editing any of these
   posts through `/admin` before `lovemesomecoding_backend/scripts/deploy.sh` runs would normalise
   `properties` blocks down to `plaintext`. Now affects three tracks.
4. **Enable S3 object versioning** on the content bucket.

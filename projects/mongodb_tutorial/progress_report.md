# MongoDB tutorial track — progress report

**Status:** ✅ **PUBLISHED AND LIVE** — 16 posts on https://lovemesomecoding.com/mongodb, all 16
URLs verified serving at the edge. Build `394b0bd`, deployed 2026-08-24.
**Started:** 2026-08-24
**Where it lands:** https://lovemesomecoding.com/mongodb

---

## What this is

`/mongodb` is live and holds **three posts**, all published 2019-07-30. Measured off the **prod**
content tree on 2026-08-24:

| slug | prose words | code blocks | h2 | h3 | reading | tags |
|---|---:|---:|---:|---:|---:|---|
| `mongodb-why-nosql-or-mongodb` | 193 | 0 | 0 | 0 | 1m | — |
| `mongodb-type-of-applications` | 106 | 0 | 0 | 0 | 1m | — |
| `mongodb-data-modeling` | **0** | 0 | 0 | 0 | 1m | — |
| **total** | **299** | **0** | **0** | **0** | **3m** | |

This is the **Hasura situation, not the FastAPI one**. FastAPI's problem was nine posts that were
each three times too long. Here the problem is that there is essentially nothing:

1. **`mongodb-data-modeling` is completely empty.** `contentHtml` is `""`. It is an indexed, live
   URL that serves a title and nothing else.
2. **No code, no headings, anywhere.** Three hundred words of plain `<p>` across the whole
   category. `mongodb-why-nosql-or-mongodb` ends with two bare WordPress embed URLs pasted as
   `<figure class="wp-block-embed">` — a Medium link and a mongodb.com link, rendered as raw text.
3. **No tags on any post.** Same defect the Hasura track had.
4. **The category record is broken** — `{"slug": "mongodb", "name": "mongodb", "description": ""}`.
   Lowercase display name, no description. Identical to what the FastAPI track had to fix.

### What is already fine

`nav.ts` line 18 already lists `mongodb` in the **Data Store** group, and line 51 already maps it
to the display name `MongoDB`. **No nav work is needed** — unlike the category record, which
`upsert_category` rewrites from `manifest.CATEGORY`.

### The three slugs are frozen

All three are indexed URLs. The frontend runs `trailingSlash: false` with a build guard
(`scripts/verify-build.mjs`) that **fails the build** if an indexed post URL stops resolving.
They are rewritten **in place**. Renaming one is not a refactor, it is a dead link — see the
migration notes in `projects/rewrite/progress_report.md`.

---

## Decisions — 2026-08-24

Five questions were put to Folau; all five answered.

| Question | Decision |
|---|---|
| Example source | **ReelCMS** — `lovemesomecoding_demo_project/reelcms`, built in this same session for exactly this purpose |
| Track size | **16 posts** — the 3 rewritten in place plus 13 new |
| Post length | **Short — 6–9 reading minutes**, ~1,000–1,400 prose words |
| The three live slugs | **Rewritten in place.** Slugs and URLs unchanged |
| Post dates | **Must fall in 2024–2025** |

### The length decision changes the topic table

6–9 minutes is the tightest reading of the README's *"keep posts to the point"*, and it is
**half** what the FastAPI track landed on. It has a consequence that has to be designed for rather
than discovered: **a short post cannot carry a large topic.** Aggregation and indexes each need
two posts, not one, or they turn into the code dumps this track is supposed to avoid. The 16 below
are sized so each is genuinely one idea.

### Dates: 2024-09-03 → 2025-07-15

`START_DATE = 2024-09-03`, `STEP_DAYS = 21`. Sixteen posts × 21 days lands the last one on
2025-07-15, so the whole track sits inside the 2024–2025 window and reads as a course in order.

⚠️ The three existing posts carry **2019** dates, and `upsert_post` never overwrites an existing
date. Seeding this track needs `seed.py --force-dates` exactly once per tree, or the archive
interleaves three 2019 posts with thirteen 2024–25 ones and the pager reads nonsense. Same trap
the FastAPI and Hasura tracks both documented.

---

## The topic table — 16 posts

Derived from the MongoDB Manual (mongodb.com/docs), W3Schools MongoDB and TutorialsPoint MongoDB,
filtered to the README's bar: **the main topics, not a post for every small thing.**

Ordering is teaching order. Dates ascend with the track.

### Rewritten in place — slugs frozen

| # | date | slug | what it becomes |
|---|---|---|---|
| 1 | 2024-09-03 | `mongodb-why-nosql-or-mongodb` | When a document store fits and when it does not. Keeps the honest "bad fit" list the 2019 post gestured at; replaces the two pasted links with actual reasoning. |
| 6 | 2024-12-17 | `mongodb-data-modeling` | **The flagship.** Embed vs reference, the 16 MB cap, unbounded growth, denormalization and what it costs. Currently empty. |
| 15 | 2025-06-24 | `mongodb-type-of-applications` | Which applications MongoDB suits, and the four where it is the wrong answer. |

### New — 13 posts

| # | date | slug | covers |
|---|---|---|---|
| 2 | 2024-09-24 | `mongodb-installation-and-mongosh` | Docker, Atlas, `mongosh` basics, why this track runs a replica set from the start |
| 3 | 2024-10-15 | `mongodb-documents-and-bson-types` | Documents, BSON types, `_id`, ObjectId, and the String↔ObjectId trap |
| 4 | 2024-11-05 | `mongodb-crud-operations` | insert / find / update / delete, upserts, bulk writes |
| 5 | 2024-11-26 | `mongodb-query-operators` | Comparison, logical, element, array and projection operators |
| 7 | 2025-01-07 | `mongodb-schema-validation` | `$jsonSchema`, validation levels and actions, and why a schemaless store still wants one |
| 8 | 2025-01-28 | `mongodb-indexes` | Single, compound, multikey, unique, partial. The **ESR rule** and `explain()` |
| 9 | 2025-02-18 | `mongodb-text-search-and-indexes` | Text indexes, weights, the one-per-collection limit, and when to reach for Atlas Search |
| 10 | 2025-03-11 | `mongodb-aggregation-pipeline` | The mental model: `$match` → `$group` → `$sort` → `$project`, and stage order |
| 11 | 2025-04-01 | `mongodb-aggregation-lookup-and-facets` | `$lookup`, `$unwind`, `$facet`, `$dateTrunc` — and the strict-type join trap |
| 12 | 2025-04-22 | `mongodb-transactions` | Single-document atomicity first, multi-document transactions second, and `$inc` vs read-modify-write |
| 13 | 2025-05-13 | `mongodb-replication-and-sharding` | Replica sets, the oplog, read preference, and when sharding is actually the answer |
| 14 | 2025-06-03 | `mongodb-change-streams` | Tailing the oplog, `updateLookup`, resume tokens, and pushing to a browser |
| 16 | 2025-07-15 | `mongodb-spring-data-mongodb` | The Java side: `MongoTemplate` vs repositories, mapping, and index declaration |

**Deliberately cut**, to stay inside 16 short posts: GridFS, geospatial queries, backup/restore,
Atlas administration, field-level encryption, migrations, and a separate interview-questions post.
Time-series is folded into post 14 (`mongodb-change-streams`) rather than given its own, since ReelCMS's measured result
(below) is a caveat, not a feature tour.

---

## The demo app

**`lovemesomecoding_demo_project/reelcms`** — a short-video CMS built in this same session, whose
own `CLAUDE.md` states that it exists to produce MongoDB snippets for this site. Every code sample
in this track is quoted from it, and it is running and tested: **66 backend tests + 25 Playwright
tests, all green.**

It already demonstrates, in code that executes, every topic in the table above:

| Topic | Where it lives in ReelCMS |
|---|---|
| Embed vs reference | `Reel`, `VideoAsset`, `CreatorRef`, `ReelStats`, `Comment` |
| Denormalization + fan-out | `CreatorServiceImpl.update()` → `ReelDAOImp.refreshCreatorSnapshot()` |
| `$inc` counters | `ReelDAOImp.incrementStat()` |
| Compound / multikey / text / unique indexes | `MongoIndexConfig` |
| Cursor pagination | `ReelServiceImpl.feed()` |
| Aggregation pipelines | `ReportDAOImp` — five of them |
| `$lookup` + strict types | `ViewEvent.ViewMetadata` with `@Field(targetType = OBJECT_ID)` |
| Time-series | `ViewEvent`, created in `MongoIndexConfig` |
| Change streams → SSE | `ReelStatsStreamService` |
| Spring Data mapping | the whole `entity/` tree |

### Versions — read off this machine, not chosen

`mvnw dependency:list`, `mongosh --eval db.version()`, `java -version`, taken 2026-08-24 with the
ReelCMS stack up and its 91 tests passing.

| | |
|---|---|
| MongoDB server | **8.0.29** (single-node replica set `rs0`) |
| Java | 21.0.7 LTS (Temurin) |
| Spring Boot | 4.1.0 |
| Spring Data MongoDB | **5.1.0** |
| MongoDB Java driver (sync) | **5.8.0** |
| BSON | 5.8.0 |
| Lombok | 1.18.46 |
| Vue / Vite / Bootstrap | 3.5.41 / 8.2.2 / 5.3.8 |
| Docker Engine | 27.4.0 |
| Host | Apple Silicon (aarch64) |

---

## Measured facts — quoted by posts, held here so they cannot drift

Every number a post states comes from this block. Written down once, because a figure repeated in
three posts is a figure that disagrees with itself within a month.

### Seeded dataset

| collection | documents |
|---|---:|
| `reels` | 16 |
| `creators` | 5 |
| `comments` | 55 |
| `reel_collections` | 4 |
| `view_events` | 30,187 |
| `users` | 2 |

### The feed query plan — the ESR rule, demonstrated

`db.reels.find({status:"PUBLISHED"}).sort({publishedAt:-1}).explain("executionStats")`:

```
stages        : FETCH <- IXSCAN
index         : status_1_publishedAt_-1
keysExamined  : 12
docsExamined  : 12
nReturned     : 12
```

**No `SORT` stage, and keys examined equals documents returned.** That 1:1 ratio is the thing to
teach — it means the index answered both the filter and the ordering, and nothing was read and
thrown away.

### 🔎 Spring Data renames a nested `id` field to `_id`

`CreatorRef` declares a Java field called `id`. The index declared in `MongoIndexConfig` as
`creator.id` is stored by MongoDB as **`creator._id`**:

```
index name : creator._id_1_status_1_publishedAt_-1
stored key : {"creator._id":1,"status":1,"publishedAt":-1}
```

It still works — Spring Data applies the same rename to queries, and
`Criteria.where("creator.id")` was verified to hit that index (`FETCH <- IXSCAN`, index
`creator._id_1_status_1_publishedAt_-1`). But **a hand-written `mongosh` query must say
`creator._id`**, and anyone comparing the config to `getIndexes()` will see two different names
for the same index. Worth a paragraph in post 16.

### 📊 Time-series collections did NOT save space here — and that is the lesson

The marketing claim is large storage savings. Measured on the actual `view_events` data, 30,187
documents, after forcing a checkpoint with `fsync`:

| storage | size |
|---|---:|
| time-series, random insert order | 0.84 MB |
| time-series, sorted by timestamp | 0.85 MB |
| **ordinary collection** | **0.91 MB** |

**A 1.1× saving. Effectively a wash.** Insert order made no measurable difference either, which
was the first hypothesis and it was wrong.

The reason is bucket density:

```
measurements                   : 30,187
buckets                        : 17,967
average measurements per bucket:      1.7
distinct metadata combinations :     49
```

A time-series collection buckets documents that share a `metaField` value **within a time
window**, then stores the measurements column-wise. Columnar compression pays off in proportion to
how many measurements land in each bucket. At **1.7 per bucket** there is nothing to compress —
49 metadata combinations scattered across 30 days of hourly windows produce roughly 35,000
possible buckets for 30,000 events.

So the honest teaching point is: **time-series collections are not a free win. The saving is
proportional to bucket density.** They pay off with few metadata combinations and a high event
rate — one sensor emitting every second — and do nothing for sparse events spread across many
metadata combinations. Check `system.buckets.<name>` before assuming a benefit. The TTL and the
time-ordered query optimisations are still worth having; the compression is not automatic.

This is the kind of claim the site's own rule exists for: *never repeat a number you did not
measure.*

---

## Where it stands

- [x] `manifest.py` — category record, 16 entries, versions, MEASURED, snippet sources
- [x] `check_content.py` — round-trip proof + six track rules, each test-fired against a fixture
- [x] `check_snippets.py` — every Java block traceable to a ReelCMS file that runs
- [x] `seed.py` — with the frozen-slug, foreign-slug and date-window guards
- [x] All 16 posts written
- [x] Seeded to `local` and verified
- [x] **Seeded prod, deployed, verified at the edge**

### What the checks say

```
check_content.py   ✅ all 16 posts pass every rule   (0 warnings)
check_snippets.py  ✅ 24 blocks traceable, 1 marked generic
```

| | prose | code | total | min | prose% |
|---|---:|---:|---:|---:|---:|
| 16 posts | 16,970 | 3,416 | 20,386 | **93** | **83%** |

Every post lands on **6 reading minutes** — inside the agreed 6–9 band and consistent across the
track. 133 code blocks against the three live posts' zero.

### Seeded to `local`, 2026-08-24

```
category mongodb -> /mongodb  name='MongoDB'   count=16
archive holds 16 posts, newest first: mongodb-spring-data-mongodb
published posts in this tree: 708 -> 721
```

Verified off the local tree afterwards:

- Category record fixed: `"name": "MongoDB"` (was lowercase `"mongodb"`), description populated.
- All 16 dates inside **2024–2025**; `--force-dates` re-based the three 2019 posts.
- **Every post carries tags.** None of the three live posts had any.
- Archive order is correct, newest first, and reads as a course in reverse.

### Tooling notes

`check_content.py` enforces six rules. Three fired during authoring and caught real problems:

- **Rule 5 is inverted from the FastAPI track.** There a rewrite had to shrink; here it must
  **grow**, because the live pages serve 193, 106 and 0 words.
- **Rule 4** flagged a post making a measurement claim with no citation. It also produced one false
  positive — `100 MB` is a documented server limit, not our benchmark — so `DOCUMENTED_LIMITS`
  now exempts the manual's constants. The rule is about unsourced numbers, not well-known ones.
- **The plaintext check** was rewritten mid-track. Warning on every `plaintext` block made the
  deliberate ones noise; it now compares the language **asked for** against the one emitted, and
  only complains about a silent downgrade.

`check_snippets.py` caught an invented `ReelSummary` interface that exists nowhere in ReelCMS —
exactly what it is for. Rather than add unused code to the demo app so a snippet had somewhere to
point, the block is marked `data-generic` and the prose says plainly that ReelCMS does not use it.
Two escape hatches exist and neither may be used for a claim about what ReelCMS does:

| marker | means |
|---|---|
| `data-antipattern` | deliberately showing the wrong way |
| `data-generic` | a framework feature this app does not use |

**No content-pipeline change was needed.** All seven languages this track uses — `javascript`,
`java`, `bash`, `json`, `yaml`, `properties`, `plaintext` — already exist on both sides
(`SUPPORTED_LANGUAGES` in the backend, static Prism imports in the frontend). `javascript` needs no
frontend import because Prism core ships it. Unlike the Hasura track, which had to add `graphql`
to both.

---

## Published — 2026-08-24

`seed.py --env prod --write --force-dates` ran once, then `npm run deploy`.

### Before writing, a rollback snapshot was taken

The three original post objects plus every index the publish touches
(`index/posts.json`, `index/categories.json`, `index/by-category/mongodb.json`,
`search/index.json`) — 7 files, 628 KB, saved outside the repo at:

```
/tmp/mongodb-rollback-20260824-140644
```

Restoring is a straight `aws s3 cp` back, followed by a rebuild.

### The deploy

```
next build          927 static pages generated
verify-build        posts served       722/722
                    categories served  42/42
                    pages redirected   95
                    archive pages      144 (/page/2../page/145)
                    index cross-check  42/42 category counts agree
                    all indexed URLs accounted for
deploy.sh           1877 files -> s3://lovemesomecoding.com  (build 394b0bd)
                    CloudFront function republished (95 redirects, 6.3 KB / 10 KB)
                    invalidation I2264QPQZCDMTRAJ8G5PTVWPRS — complete
                    edge serves 394b0bd  (match)
```

`verify-build.mjs` passing is the guard that matters: it fails the build if any indexed post URL
stops resolving, and all three 2019 URLs were rewritten in place rather than replaced.

### Verified live

- **16/16 post URLs return 200** at the edge, plus `/mongodb` itself.
- Category page renders as **"MongoDB Tutorials"** with the standfirst — it had a lowercase name
  and no description before.
- **`mongodb-data-modeling`**, which served a completely empty body, now renders 1,351 words,
  6 `<h2>` sections, 4 code blocks and **203 Prism token spans**.
- Syntax highlighting confirmed for every language used: `java`, `javascript`, `bash`, `yaml`,
  `properties`. The only `plaintext` blocks are the three authored as plaintext deliberately
  (a server error message, two measurement tables).
- **Sitemap carries all 16** post URLs plus the category URL.
- Nav links `/mongodb` under **Data Store**.

### Prod content tree

```
published posts: 709 -> 722   (13 new, 3 rewritten in place)
category mongodb -> /mongodb  name='MongoDB'  count=16
```

---

## Claims verified against a running MongoDB

Every factual assertion in the track was executed before it was written down, and three were wrong
on the first pass:

| Claim | First written | Actual |
|---|---|---|
| `scheduledFor: {$exists:false}` count | 0 | **15** — the field is absent, not null |
| `scheduledFor: {$type:"null"}` count | 15 | **0** — none is explicitly null |
| views for `#motorsport` | 8,911 | **5,733** |
| ObjectId match count for one reel | 1,878 | **1,649** |

The first two were backwards, and the correction made the post *better*: Spring Data omits null
fields rather than storing them, so "the value is null" and "there is no such field" are the same
state on disk. That is a sharper lesson than the one originally drafted.

Verified exactly as written: `0.1 + 0.2 → 0.30000000000000004`; `Decimal128` sums exactly;
`$sum` silently skips a string; a string never matches an ObjectId; `$text` for `fade` returns 0
while `fadeaway` returns 1; a second text index fails with `IndexOptionsConflict`; a covered query
reports `PROJECTION_COVERED <- IXSCAN` with `totalDocsExamined: 0`; the index prefix rule; a
mixed inclusion/exclusion projection is rejected; `collMod` validation rejects a bad document and
`$nor: [{$jsonSchema}]` lists what would fail.

---

## Traps carried in from the other tracks

- **`--force-dates` exactly once per tree.** Three 2019 dates are sticky otherwise.
- **`wordCount` counts prose AND code together**, then `readingMinutes = max(1, round(words/220))`
  (`lovemesomecoding_backend/app/services/content.py`). A 6–9 minute budget is **1,320–1,980 total
  words**, not 1,320–1,980 words of prose. Budgeting prose alone doubles the published figure.
- **Extract `<pre>` blocks with regex before any HTML parsing.** Post bodies contain raw
  `<script>`/`<style>`/`onclick=` inside code samples; a parser turns them into real elements and
  `get_text()` deletes them with almost no change in character count, so length checks pass.
- **Slugs are frozen.** `verify-build.mjs` fails the build when an indexed post URL stops
  resolving.
- **Category display name and description come from `manifest.CATEGORY`.** Nothing else writes
  them, which is why the archive page currently has neither.

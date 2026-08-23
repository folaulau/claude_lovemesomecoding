# Snowflake tutorial track — progress report

**Status:** ✅ **LIVE.** Published to prod and deployed 2026-08-23. https://lovemesomecoding.com/snowflake
**Started:** 2026-08-22
**Where it lands:** https://lovemesomecoding.com/snowflake

---

## What is there now

`/snowflake` holds **one post**, measured off the local content tree on 2026-08-22:

| slug | date | counted words | code blocks | h2/h3 | reading |
|---|---|---:|---:|---:|---:|
| `snowflake-introduction` | 2019-04-05 | 624 | 0 | 0 | 3m |

Four defects, three of them the same ones the Hasura, FastAPI and Postgres tracks had to fix:

1. **It is a stub, and it is marketing copy.** 624 words, no headings, no code, no `SELECT`. Whole
   paragraphs are lifted from Snowflake's own product page — *"instant, nearly unlimited
   scalability"*, *"automation made easy"* — and one bullet is a customer quote with no attribution
   (*"Our goal was to deliver the analysis in less than 5 seconds…"*). A reader finishes it knowing
   Snowflake is enthusiastic about itself and nothing about how to use it.
2. **It still carries the WordPress `boldgrid-section` / `container` / `row` / `col-md-12` wrapper
   divs** and `class=""` on every paragraph — dead Bootstrap markup from the old theme. The one
   `<ul>` also carries `class="ul1"` / `li1` / `s1`, Pages-export junk.
3. **The category record is broken** — `{"slug": "snowflake", "name": "snowflake", "description": ""}`.
   Lowercase display name, no standfirst on the archive page.
4. **`/snowflake-table-of-content` is an orphaned page** (WP id 7870, 2022-04-05) whose entire body
   is an ordered list of one link plus an empty `<li>`. It is not in the nav and nothing links to
   it. **It also already 301s to `/snowflake`** — see *The table-of-content page* below, which
   corrects what this report first said about it.

The post has no tags and is `status: published`. It embeds one image,
`architecture-overview.png`, already served from the media CDN — that one is worth keeping.

### One frozen slug

`/snowflake/snowflake-introduction` is a live, indexed URL. The frontend runs `trailingSlash: false`
with a build guard (`scripts/verify-build.mjs`) that **fails the build** if an indexed post URL
stops resolving. It gets rewritten **in place** — renaming it is a dead link, not a refactor.

It carries a **2019-04-05** date, and `upsert_post` never overwrites an existing date. Seeding this
track therefore needs `seed.py --force-dates` exactly once per tree, or a 2019 post sits at the far
end of the archive while the other fifteen cluster in 2026, and the ‹ prev / next › pager walks
from lesson 16 back to lesson 1. Same trap the FastAPI and Postgres tracks documented.

### Navigation — nothing to do

`src/lib/nav.ts` already lists `snowflake` in the **Data Store** group with the display name
`Snowflake`. Only the stored category record needs fixing, and `upsert_category` does that.

### The table-of-content page — ⚠️ it was already solved, and better

`/snowflake-table-of-content` is a hand-written page, not a post, so it is outside the category
index and outside this track's seeding. It is a hand-maintained duplicate of what `/snowflake`
already generates automatically, and hand-maintained indexes rot — this one already has.

**The first version of this report proposed rewriting its body, on the assumption the page was
being served. It is not.** `postbuild.mjs` has a rule that redirects every `*-table-of-content`
URL to its matching category, and that redirect is compiled into the CloudFront Function:

```js
// scripts/postbuild.mjs
if (url.endsWith('-table-of-content')) {
  const slug = TOC_OVERRIDES[url] ?? url.replace(/-table-of-content$/, '');
  redirects[`/${url}`] = categorySlugs.has(slug) ? `/${slug}` : '/';
}
```

Verified against production on 2026-08-23:

```
curl -I https://lovemesomecoding.com/snowflake-table-of-content
301  ->  https://lovemesomecoding.com/snowflake
```

So the page body has not been served to anybody since the migration, and a 301 is the better
outcome anyway — it consolidates the URL's search signal into `/snowflake` instead of keeping a
thin duplicate alive. Three ToC pages are exempted in `postbuild.mjs`'s `KEEP` set — `datadog`,
`jquery`, `test-driven-development` — because no category of that name exists for them to point at.

The body was rewritten anyway (`update_page.py`), and it is worth being clear about what that is:
**dead content, kept only as a correct fallback.** If somebody ever adds this slug to `KEEP`, the
page says something true instead of listing one post out of sixteen. It changes nothing a visitor
sees. Say the word and it reverts.

---

## Sources

Per the README:

- https://docs.snowflake.com/en/ — the topic spine
- https://docs.snowflake.com/en/learn-tutorials — what Snowflake itself thinks a newcomer does first
- https://www.tutorialspoint.com/snowflake/index.htm — cross-check on beginner ordering

Filter: *"the important things to get a project developed and released to production"* — not a post
per catalogue entry.

---

## Decisions — 2026-08-22

| # | Question | Decision |
|---|---|---|
| 1 | Verification | **Docs-only, unverified.** No Snowflake account. |
| 2 | Example data | **`SNOWFLAKE_SAMPLE_DATA`** — the TPC-H share every account gets free. |
| 3 | Post length | **Short — 6–10 reading-minutes** (~1,320–2,200 counted words). |
| 4 | Track size | **16 posts** — the 1 frozen slug rewritten in place plus 15 new. |
| 5 | Dates (2026-08-23) | **Backdated to 2022-05-03 → 2022-06-17.** See below. |

### Decision 5 — backdating, and what it costs

Asked for on 2026-08-23: date the track anywhere in 2021–2022. `START_DATE` is now
**2022-05-03**, stepping 3 days to **2022-06-17** — a 45-day run sitting just after the
2022-04-05 `/snowflake-table-of-content` page that used to index this collection.

**The trade is real and it is the point of writing it down.** Every archive on this site sorts
newest-first, so measured against the 687-post local tree:

| | |
|---|---|
| Position in the archive | **#386–#401** of 687 |
| Archive page | **39–41** of 138 |
| On the homepage (first 10) | **0 posts** |
| In the 50-item RSS feed | **0 posts** |

The track is reached through `/snowflake`, on-site search, and Google — not through the front
page. Dating it in the present would have put all 16 across the top of the homepage instead.
Neither is wrong; they are different intentions, and this one reads as long-standing reference
material rather than a launch.

`--force-dates` also moved the frozen post's published date from **2019-04-05 to 2022-05-03**.
That is a visible change to an indexed URL. It is defensible — the 2019 date described content
that no longer exists — but it is not an internal-only edit, and it is recorded here as a change
rather than a side effect. `lastmod` in the sitemap is today's date, which is accurate: the
content really was modified today.

To move the track again, change `manifest.START_DATE` and re-run
`seed.py --write --force-dates`. Every lesson re-bases in order.

### ⚠️ Decision 1 is a real departure, and it is recorded here on purpose

Every other track on this site executes its samples before shipping them. The Postgres track built
a 330 MB lab database so its `EXPLAIN` output would be true; the FastAPI track ran 100 tests and
read its version numbers off `pip show`. **This track cannot do that.** There is no Snowflake
account, no `snowsql`, no `snow` CLI and no `snowflake-connector-python` on this machine — checked
2026-08-22.

What that means concretely, so nobody has to rediscover it:

- **No output block is a transcript.** Query results, `QUERY_HISTORY` rows, credit figures and
  timings shown in these posts are illustrative, written to be plausible and shaped like the real
  thing. They are not measured.
- **So they are not written as measurements.** No post says "this took 1.3 s on an X-Small" or
  quotes a byte count as fact. Where a number would carry weight it is either omitted or attributed
  to the docs with a link.
- **Pricing is never stated as a dollar figure.** Credit *consumption* per warehouse size is
  documented and stable; the dollar price per credit varies by edition, cloud and region, and
  printing one would be wrong somewhere and stale everywhere. Posts link to Snowflake's pricing page.
- **SQL syntax is checked, not just typed.** Every statement is written against the current
  docs.snowflake.com reference page for that command, and `check_content.py` enforces the
  structural rules the build depends on.

If a trial account turns up later, the fix is mechanical: run `posts/*.html` code blocks in order
against a fresh trial, replace the illustrative outputs, and delete this section.

### Why `SNOWFLAKE_SAMPLE_DATA` and not StayHub

Continuity with the Postgres track argued for modelling StayHub's booking schema as the warehouse.
It lost to a simpler test: **a reader on day one of a free trial can run every query in this track
without loading anything.** `SNOWFLAKE_SAMPLE_DATA` is a shared database present in every account
from creation, holding TPC-H at several scale factors — `TPCH_SF1` through `TPCH_SF1000`. That
gives the performance and clustering lessons tables large enough that the answers are not trivial,
which is exactly what the Postgres track needed a purpose-built lab for.

The one place it does not stretch is loading: you cannot `COPY INTO` a share. The loading posts
therefore build their own small tables and stage files, written out in the post itself.

---

## The track — 16 posts

Topics come from the Snowflake docs' own top-level structure, cross-checked against the tutorials
index and the tutorialspoint ordering, then filtered to *what you need to ship*.

| # | slug | state |
|---|---|---|
| 1 | `snowflake-introduction` | **rewrite (frozen)** |
| 2 | `snowflake-architecture` | new |
| 3 | `snowflake-getting-started` | new |
| 4 | `snowflake-virtual-warehouses` | new |
| 5 | `snowflake-databases-schemas-and-tables` | new |
| 6 | `snowflake-data-types` | new |
| 7 | `snowflake-loading-data` | new |
| 8 | `snowflake-snowpipe-and-continuous-loading` | new |
| 9 | `snowflake-semi-structured-data` | new |
| 10 | `snowflake-querying-data` | new |
| 11 | `snowflake-query-performance` | new |
| 12 | `snowflake-time-travel-and-cloning` | new |
| 13 | `snowflake-streams-and-tasks` | new |
| 14 | `snowflake-access-control` | new |
| 15 | `snowflake-cost-management` | new |
| 16 | `snowflake-in-production` | new |

### What got cut, and why

- **Snowpark, dynamic tables, Iceberg tables, Cortex/AI** — real features, none of them on the path
  from nothing to a released project. A reader who needs Snowpark will not learn it from a
  16-post intro track.
- **Data sharing and the Marketplace** — the track *consumes* a share (`SNOWFLAKE_SAMPLE_DATA`) in
  post 3 and explains what that means there. Producing one is an organisational decision, not a
  shipping step.
- **dbt and orchestration** — belongs to whichever tool you picked, not to Snowflake. Post 13
  covers the native answer (streams + tasks), which is what you get without adding a vendor.
- **Connectors and drivers** get a section in post 3 rather than a post: choosing between the
  Python connector, JDBC and the CLI is a paragraph, not a lesson.

Say the word and any of these becomes post 17.

---

---

## What was built

| File | What it is |
|---|---|
| `manifest.py` | Category record, the 16 entries, dates, length budget, `FROZEN_SLUGS` |
| `seed.py` | Writes the track through the backend's own service layer, so every derived index is maintained by the code the admin API uses |
| `check_content.py` | Round-trip proof for every code block, plus this track's nine rules |
| `posts/*.html` | The 16 lessons |
| `update_page.py` | Rewrites the orphaned `/snowflake-table-of-content` body. Pages have no service in the backend, so it writes the S3 object — through `content.normalize`, so the fields match every post. Idempotent. |

### Where it landed

Seeded to the **`local`** tree on 2026-08-22 with `--force-dates`, then synced and built:

```
archive /snowflake holds 16 posts, newest first: snowflake-in-production
category count recorded: 16
published posts in this tree now: 687 (was 672)

verify-build
  posts served       687/687
  index cross-check  42/42 category counts agree
  all indexed URLs accounted for
```

`/snowflake/snowflake-introduction` still resolves, so the indexed URL survived the rewrite. The
category record now reads `name: "Snowflake"` with a standfirst, and the archive page renders the
same shape as `/fastapi` — lesson-order index at the top, excerpts below.

### The collection, before and after

| | before | after |
|---|---:|---:|
| posts | 1 | 16 |
| counted words | 624 | 21,315 |
| code blocks | 0 | 120 |
| headings | 0 | 118 |
| reading-minutes | 3 | 98 |

Every post lands at **6 or 7 reading-minutes**, inside the 6–10 budget. Prose share is 76% across
the track, well above the 40% floor — the lowest single post is `snowflake-querying-data` at 57%,
which is what a SQL-reference lesson looks like.

### Two checker rules had to be split after false positives

Worth recording, because both look like the rule working and are not:

- **The no-dollars rule matched `$1`.** `COPY INTO … SELECT $1, $2 FROM @stage` uses positional
  column references, and inline `<code>$1</code>` appears in the prose of post 7 explaining them.
  The rule is now two patterns: broad in prose, and in code it must see something only money has —
  a cents part or a per-unit phrase. Inline `<code>` counts as code.
- **The no-benchmarks rule matched "TPC-H benchmark data".** That is a dataset name, not a claim.
  It now matches the verb (`benchmarked`, `benchmarking`) and appeals to results
  (`benchmarks show`), not the bare noun.

The length floor also moved from raw words to **published reading-minutes**. `readingMinutes`
rounds, so a 1,270-word post publishes as 6 minutes and is inside budget; warning on 6 × 220 = 1,320
flagged posts that were fine.

---

## Published — 2026-08-23

```
seed.py --env prod --write --force-dates    ->  687 posts (was 672)
update_page.py --env prod --write           ->  ToC page body replaced
npm run deploy                              ->  build 394b0bd
      verify-build     687/687 posts, all indexed URLs accounted for
      cloudfront fn    republished LIVE (94 redirects, 6.2 KB / 10 KB)
      invalidation     IC1V6CRFJEPYFQ1MDTRJ6PJYA0, completed
      edge check       /version.txt -> 394b0bd (match)
```

Verified against the live site afterwards, not just against the build:

| Check | Result |
|---|---|
| All 16 post URLs | 200 |
| `/snowflake` | 200, reports 16 tutorials |
| Frozen URL `/snowflake/snowflake-introduction` | 200, renders "May 3, 2022" |
| `/snowflake-table-of-content` | still 301 → `/snowflake` |
| Sitemap | 16 snowflake entries |
| Regression: `/fastapi`, `/oracle`, `/postgre`, `/java`, `/rss.xml` | all 200 |

The CloudFront Function republish is the step that silently breaks redirects when skipped
(CLAUDE.md gotcha); `deploy.sh` does it unprompted and reported `LIVE`.

---

## What is left

1. **The admin console's Publish button still does not work.** Checked again 2026-08-23:
   `aws ssm get-parameter --name /lovemesomecoding/prod/github-token` returns `ParameterNotFound`.
   This deploy went out via `npm run deploy` instead. That CLAUDE.md item is still open and will
   bite the next person who edits a post in the admin UI and waits for a rebuild.
2. **Nothing was committed.** `projects/snowflake_tutorial/` is untracked. Per CLAUDE.md the commit
   and the push are yours.
3. **If a Snowflake account ever appears**, the verification note in Decision 1 becomes actionable:
   run every code block in order against a fresh trial, replace the illustrative outputs, flip
   `manifest.VERIFIED` to `True`, and delete that section. Until then the track is docs-derived and
   `check_content.py` is what keeps it honest.
4. **`seed.py` in the FastAPI track carries the re-seed guard bug** fixed here on 2026-08-23. It
   will refuse to run a second time against a tree it has already seeded.

---

## Log

- **2026-08-22** — Audited `/snowflake`: one 2019 stub, boldgrid wrappers, broken category record,
  orphaned table-of-content page. Confirmed nav needs no change and the single slug is frozen with
  a 2019 date needing `--force-dates`. Confirmed **no Snowflake access on this machine**. Took the
  four decisions above. Track list drawn up.
- **2026-08-22** — Wrote `manifest.py`, `seed.py` and `check_content.py`, then all 16 posts. Split
  the dollars and benchmark rules after the false positives above, and moved the length floor onto
  published reading-minutes. All 16 pass. Seeded to `local` with `--force-dates`, synced, built:
  687/687 posts served, all indexed URLs accounted for. Verified the rendered archive and the
  rewritten intro against the served HTML.
- **2026-08-23** — Readiness pass: verified all 16 internal cross-links resolve against the built
  output (0 broken) and all 4 external links return 200. Found and fixed one defect — the pricing
  link 301'd, so both citations now point at `snowflake.com/en/pricing-options/` directly.
- **2026-08-23** — Backdated the track to 2022 per Decision 5, re-seeded with `--force-dates`,
  rebuilt: 687/687 posts served, all indexed URLs accounted for. Lesson 1 renders "May 3, 2022"
  and the pager walks lesson order.
- **2026-08-23** — **Fixed a guard in `seed.py` that made the script refuse to run twice.** The
  `NEW_SLUGS` collision check compared against every existing slug, so on a re-seed it flagged this
  track's own 15 posts as accidental overwrites — contradicting the "idempotent" promise in its own
  docstring. It now fires only when a slug sits in a *different* category, which is the case worth
  stopping, and prints a note when it detects a re-seed. The FastAPI track carries the same
  unfixed guard.
- **2026-08-23** — Rewrote the `/snowflake-table-of-content` body via `update_page.py`, then found
  while rebuilding that **the URL has 301'd to `/snowflake` all along** — `postbuild.mjs` redirects
  every `*-table-of-content` URL to its category and compiles it into the CloudFront Function.
  Confirmed against production. The audit section above is corrected; the rewrite is kept as a
  fallback that nothing currently reads.

# Elasticsearch tutorial track — progress report

**Status:** ✅ **PUBLISHED AND LIVE** — 18 posts on https://lovemesomecoding.com/elasticsearch, all
18 URLs plus the archive verified serving at the edge. Build `394b0bd`, deployed 2026-08-23.
**Started:** 2026-08-22
**Where it lands:** https://lovemesomecoding.com/elasticsearch

---

## What is there now

`/elasticsearch` holds **13 posts**, all WordPress leftovers dated 2019-06-28 … 2021-09-27.
Measured off the **prod** content tree on 2026-08-22:

| slug | date | prose words | code blocks | h2 | h3 | reading | toc |
|---|---|---:|---:|---:|---:|---:|---:|
| `elasticsearch-data-types` | 2019-06-28 | 1,358 | 2 | 0 | 0 | 6m | 0 |
| `elasticsearch-aggregation` | 2019-06-29 | 148 | 2 | 0 | 0 | 2m | 0 |
| `elasticsearch-geo-point` | 2019-09-27 | 273 | 5 | 0 | 0 | 3m | 0 |
| `elasticsearch-modeling-data` | 2019-09-27 | 597 | 1 | 0 | 0 | 3m | 0 |
| `elasticsearch-snapshot` | 2020-09-11 | 59 | 0 | 0 | 0 | 1m | 0 |
| `elasticsearch-cat-api` | 2020-09-24 | 123 | 5 | 0 | 0 | 1m | 0 |
| `elasticsearch-document-api` | 2020-09-24 | 603 | 20 | 0 | 0 | 5m | 0 |
| `elasticsearch-installation` | 2020-09-24 | 143 | 6 | 0 | 0 | 1m | 0 |
| `elasticsearch-mapping` | 2020-09-24 | 449 | 2 | 0 | 1 | 2m | 1 |
| `elasticsearch-search-api` | 2020-09-24 | 1,967 | 24 | 0 | 4 | 16m | 4 |
| `what-is-elasticsearch` | 2020-09-24 | 843 | 0 | 0 | 1 | 4m | 1 |
| `elasticsearch-sorting` | 2021-03-21 | 852 | 5 | 0 | 6 | 5m | 6 |
| `elasticsearch-filter` | 2021-09-27 | 321 | 7 | 0 | 3 | 3m | 0 |
| **total** | | **7,736** | **79** | **0** | **15** | **52m** | **12** |

This is the Hasura/Postgres shape, not the FastAPI shape — the problem is thinness, not bloat.
Four defects:

1. **Most of them are stubs.** Six posts are under 350 prose words. `elasticsearch-snapshot` is 59
   words and zero code — it defines the word "snapshot", links the docs, then recommends an npm
   package. `elasticsearch-cat-api` is 123 words wrapped around five one-line `curl`s.
2. **Zero `<h2>` across the entire collection.** Sections are marked with `<p><strong>…</strong></p>`,
   which produces no anchors, so 12 of 13 posts render with no table of contents and no deep links.
3. **The content is stale by four major versions.** `elasticsearch-installation` tells you to pull
   `elasticsearch:7.1.0` and pass `discovery.type=single-node`; `elasticsearch-cat-api` links the
   `reference/7.1/` docs. Current is 8.x/9.x, where **security is on by default** — that 7.1 command
   no longer describes what happens when you run the current image, and nothing in the track
   mentions `elastic` passwords, enrollment tokens or TLS.
4. **All 13 still carry the WordPress `boldgrid-section` / `container` / `row` / `col-md-12` wrapper
   divs** and `class=""` on every paragraph, plus imported Asciidoc junk classes
   (`ulist itemizedlist`, `listitem`, `xref`) on the lists lifted out of the elastic.co docs.

No post has a single tag. All 13 are `status: published`.

### The 13 slugs are frozen

Every one is a live, indexed URL. The frontend runs `trailingSlash: false` with a build guard
(`scripts/verify-build.mjs`) that **fails the build** if an indexed post URL stops resolving. They
get rewritten **in place** — renaming one is a dead link, not a refactor.

All 13 carry 2019–2021 dates, and `upsert_post` never overwrites an existing date. Seeding this
track therefore needs `seed.py --force-dates` exactly once per tree, or the archive interleaves
thirteen old posts with the new ones and the ‹ prev / next › pager reads nonsense. Same trap the
FastAPI and Postgres tracks documented.

### Category record needs fixing — but less than the others

`{"slug": "elasticsearch", "name": "Elasticsearch", "description": "", "count": 13}`. The display
name is already correct (unlike `fastapi`/`postgre`); only the empty `description` needs writing,
so the archive page gets a standfirst.

### Navigation — nothing to do

`src/lib/nav.ts:18` already lists `elasticsearch` in the **Data Store** group.

---

## Sources

Per the README:

- https://www.elastic.co/guide/index.html — the topic spine
- https://www.tutorialspoint.com/elasticsearch/index.htm — cross-check on beginner ordering

Filter: *"the important things to get a project developed and released to production"* — not a post
per API endpoint.

---

## The example app — StayHub already runs Elasticsearch

`lovemesomecoding_demo_project/stayhub` is an unusually strong fit for this track. It is not a toy
`curl` against a `movies` index; it is a working search feature on **Elasticsearch 8.15.3**
(`docker-compose.yml`) with the `elasticsearch==8.15.1` Python client, and the code already
demonstrates most of what a production track needs to say:

| StayHub file | What it already demonstrates |
|---|---|
| `app/search/index.py` | explicit mapping with `dynamic: strict`; custom `asciifolding` analyzer; `text` + `.raw` keyword multi-field; `scaled_float` for money; `geo_point`; why mappings are immutable |
| `app/search/queries.py` | `bool` **must vs filter** (scoring vs cacheable); `multi_match` with `^3`/`^2` boosts and `fuzziness: AUTO`; `term` vs `terms` (AND vs OR on a filter panel); range filters; sort with tie-break; `from`/`size` + `track_total_hits` |
| `app/search/indexer.py` | `helpers.bulk`; index **after** commit, never before; failures logged not raised; **outbox retry** when the cluster is down; `rebuild_index` from Postgres |
| `docker-compose.yml` | a real 8.x container, ports, health check |

So mapping, analysis, relevance, filtering, bulk indexing, sync strategy and rebuilds can all be
written against code that has actually run.

### What StayHub does NOT have yet

These are the gaps a "released to production" track would otherwise have to invent. Each is a
small, real addition to StayHub rather than a fictional snippet:

- **Aggregations** — the filter panel shows no facet counts. `terms` on `city.raw`/`amenities`,
  `range` on price, `stats` on rating. This is the single biggest gap: the current
  `elasticsearch-aggregation` post is 148 words and the app never runs one.
- **Geo search** — `location` is mapped as `geo_point` and populated, but **nothing ever queries
  it**. No `geo_distance` filter, no `_geo_distance` sort, no "within 10 km of this map view".
- **Autocomplete** — no `search_as_you_type` / completion suggester on the city box.
- **Highlighting** — hits come back without `highlight`, so matched terms are not marked in the UI.
- **Aliases + zero-downtime reindex** — `ensure_index` writes to a concrete index name and the
  comment concedes it cannot change a mapping. An alias flip is the production answer.
- **Deep pagination** — `from`/`size` only; no `search_after` and no note on the 10,000-result wall.
- **Security** — the compose file runs with `xpack.security.enabled=false`. Production needs at
  minimum a password and TLS, and the track currently says nothing about either.

---

## Decisions — 2026-08-22

| Question | Decision |
|---|---|
| Track size | **18 posts** — the 13 frozen slugs rewritten in place, plus 5 new. |
| Post length | **Medium — 12–18 reading-minutes**, ~2,000–2,500 prose words. One whole area end to end per post. |
| StayHub gaps | **Build the additions in StayHub first, then write.** Quote only code that has actually run. |

---

## The 18-post spine

Ordered as a track: zero → production. `#` is lesson order, which is also date order (dates are
computed in `manifest.py` from a `START_DATE`, so the last lesson is the newest).

| # | slug | state | what it covers |
|---:|---|---|---|
| 1 | `what-is-elasticsearch` | rewrite | what it is, when it beats a database, cluster/node/index/shard/replica/document vocabulary |
| 2 | `elasticsearch-installation` | rewrite | ES 8.15 in Docker, **security on by default**, passwords/enrollment, health check, connecting the Python client |
| 3 | `elasticsearch-mapping` | rewrite | explicit vs dynamic, `dynamic: strict`, multi-fields, why mappings are immutable |
| 4 | `elasticsearch-data-types` | rewrite | the types that actually matter: `text` vs `keyword`, `scaled_float` for money, `date`, `geo_point`, `nested` vs `object` |
| 5 | `elasticsearch-analyzers-text-analysis` | **new** | analyzers, tokenizers, token filters, the `_analyze` API, `asciifolding` — why a search returns nothing |
| 6 | `elasticsearch-modeling-data` | rewrite | denormalise on purpose, one document per search result, `nested` vs parent/join, index-per-thing |
| 7 | `elasticsearch-document-api` | rewrite | index/get/update/delete, `refresh`, versioning and optimistic concurrency |
| 8 | `elasticsearch-bulk-indexing-data-sync` | **new** | the bulk API, `helpers.bulk`, partial failures, and keeping Postgres → ES in sync (index after commit, outbox retry, rebuild) |
| 9 | `elasticsearch-search-api` | rewrite | query DSL, `match`/`multi_match`, `_source` filtering, pagination, `track_total_hits`, highlighting |
| 10 | `elasticsearch-filter` | rewrite | `bool` must/should/filter/must_not, `term` vs `terms` vs `match`, the filter cache |
| 11 | `elasticsearch-relevance-tuning` | **new** | BM25, field boosts, `fuzziness`, the `_explain` API, `function_score` |
| 12 | `elasticsearch-sorting` | rewrite | sorting on a field, tie-breaks, why sorting on `text` fails, missing values, `_score` |
| 13 | `elasticsearch-aggregation` | rewrite | `terms`/`range`/`stats`, facet counts for a filter panel, aggs alongside a query |
| 14 | `elasticsearch-geo-point` | rewrite | `geo_distance` filter, `_geo_distance` sort, bounding box for a map viewport |
| 15 | `elasticsearch-index-aliases-reindex` | **new** | aliases, `_reindex`, changing a mapping in production with zero downtime |
| 16 | `elasticsearch-cat-api` | rewrite | `_cat/indices`, `nodes`, `health`, `shards`; reading cluster health; diagnosing yellow |
| 17 | `elasticsearch-snapshot` | rewrite | snapshot repositories, SLM policies, restore, what a backup actually guarantees |
| 18 | `elasticsearch-production-checklist` | **new** | shard sizing, replicas, JVM heap, API keys/TLS, ILM, monitoring, capacity |

### As written — measured after seeding, 2026-08-23

| # | date | slug | words | min | headings |
|---:|---|---|---:|---:|---:|
| 1 | 2020-02-04 | `what-is-elasticsearch` | 2,670 | 12 | 13 |
| 2 | 2020-03-15 | `elasticsearch-installation` | 2,641 | 12 | 13 |
| 3 | 2020-04-24 | `elasticsearch-mapping` | 2,650 | 12 | 15 |
| 4 | 2020-06-03 | `elasticsearch-data-types` | 2,710 | 12 | 18 |
| 5 | 2020-07-13 | `elasticsearch-analyzers-text-analysis` | 2,652 | 12 | 18 |
| 6 | 2020-08-22 | `elasticsearch-modeling-data` | 2,687 | 12 | 18 |
| 7 | 2020-10-01 | `elasticsearch-document-api` | 2,644 | 12 | 15 |
| 8 | 2020-11-10 | `elasticsearch-bulk-indexing-data-sync` | 2,669 | 12 | 17 |
| 9 | 2020-12-20 | `elasticsearch-search-api` | 3,645 | 17 | 21 |
| 10 | 2021-01-29 | `elasticsearch-filter` | 2,643 | 12 | 17 |
| 11 | 2021-03-10 | `elasticsearch-relevance-tuning` | 2,669 | 12 | 15 |
| 12 | 2021-04-19 | `elasticsearch-sorting` | 2,691 | 12 | 16 |
| 13 | 2021-05-29 | `elasticsearch-aggregation` | 2,734 | 12 | 16 |
| 14 | 2021-07-08 | `elasticsearch-geo-point` | 2,653 | 12 | 14 |
| 15 | 2021-08-17 | `elasticsearch-index-aliases-reindex` | 2,678 | 12 | 14 |
| 16 | 2021-09-26 | `elasticsearch-cat-api` | 2,684 | 12 | 18 |
| 17 | 2021-11-05 | `elasticsearch-snapshot` | 2,662 | 12 | 15 |
| 18 | 2021-12-15 | `elasticsearch-production-checklist` | 2,822 | 13 | 16 |
| | | **total** | **49,195** | **220** | **328** |

Against the 13 live posts: **10,827 words / 52 minutes / 0 `<h2>`** → **49,195 words / 220 minutes /
328 headings**. Post 9 is the only one over 18 minutes, and deliberately: `check_content.py` rule 5
requires a rewrite to beat the page it replaces, and the live `elasticsearch-search-api` is already
3,519 words.

### Dates — 2020-2021, decided 2026-08-23

Folau asked for the track to be dated into **2020-2021** rather than 2026. `START_DATE` is
2020-02-04 with `STEP_DAYS = 40`, spanning 2020-02-04 → 2021-12-15, which brackets the original
2019-06 → 2021-09 range. The thirteen rewrites therefore land close to where their URLs already sit
instead of moving thirteen indexed pages to the front of every archive at once.

⚠️ **One conflict this creates, flagged rather than papered over.** The posts are written against
**Elasticsearch 8.15.3**, which shipped in October 2024 — and 8.0 itself did not exist until
February 2022. Post 2 is largely about "security is on by default since 8.0" and explicitly says
older tutorials are stale. A reader who notices the byline date will find a 2020 post describing
software from 2024. Three ways out, none taken yet:

1. Leave it. The dates order the archive; the content states its own version in post 1 and post 2.
2. Re-date the five NEW posts to 2026 and leave the thirteen rewrites where they are — honest about
   which are rewrites, but the track no longer reads in lesson order.
3. Move the whole track to 2026 (the original plan) and accept the archive churn.

---

## StayHub additions — build before writing

Decision 3 means these ship in `lovemesomecoding_demo_project/stayhub` **first**, and the posts
quote them afterwards.

| For post | Addition | Where it landed | Status |
|---|---|---|---|
| 5 | `_analyze` against the real `stayhub_text` analyzer | `scripts/analyze_demo.py` | ✅ |
| 9 | `highlight` with `encoder: "html"` | `search/queries.py::_highlight_spec` | ✅ |
| 11 | `_explain`, field boosts, `function_score` | `scripts/explain_search.py` | ✅ |
| 13 | drill-down-aware facet counts | `search/queries.py::build_aggs` | ✅ |
| 14 | `geo_distance` filter + `_geo_distance` sort | `search/queries.py` + `GET /search` | ✅ |
| 15 | write-alias, generations and `_reindex` | `search/index.py`, `scripts/reindex.py` | ✅ |
| 17 | snapshot repository, restore, SLM policy | `docker-compose.yml`, `scripts/snapshot.py` | ✅ |
| 18 | `secure` compose profile + least-privilege API key | `docker-compose.yml`, `scripts/es_security.py` | ✅ |

**193 backend tests pass** (was 165). `tests/test_search.py` adds 28, and the cluster-backed half
skips cleanly when Elasticsearch is not running.

### One real bug found while building

`multi_match` with `operator: and` and the default `best_fields` **returned nothing for "san
francisco loft"** — `best_fields` requires every term in ONE field, and "san francisco" is in
`city` while "loft" is in `title`. `cross_fields` fixes it and cannot carry `fuzziness` (ES returns
a 400), so the text clause is now both types in a `should`. This is post 11's opening example, and
it is the kind of thing that only turns up against real documents.

### Verified numbers to quote

Measured on this machine, 2026-08-22, Elasticsearch **8.15.3**, client `elasticsearch==8.15.1`:

- `best_fields` on "san francisco loft": **0 hits**. Hybrid: **1 hit**. `"cabbin"` → Cedar Cabin.
- `_analyze`: `"Málaga"` → `['málaga']` under `standard`, `['malaga']` under `stayhub_text`;
  `city` → `['san','francisco']`, `city.raw` → `['San Francisco']`.
- BM25 for `title:cabin`: `4.3190 = boost 4.4 x idf 2.1595 x tf 0.4545`, N=12, n=1.
  ⚠️ `boost` reads 4.4 for `title^2` because Lucene folds `(k1 + 1) = 2.2` into it.
- Highlight without an encoder returns a live `<script>` tag; with `encoder: "html"` it returns
  `&lt;script&gt;`.
- Alias flip `…-000001` → `…-000002`, 12 documents, alias never resolving to nothing.
- Snapshot round trip: 12 docs → `_delete_by_query` → 0 → restore → 12.
- The scoped API key indexes and searches; it is refused (403) on another index, on deleting one,
  on listing users, and on minting another key.

---

## Log

- **2026-08-22** — Synced the prod content tree (672 posts). Audited all 13 `/elasticsearch` posts:
  7,736 prose words, 79 code blocks, **zero `<h2>`**, no tags, WordPress wrappers intact, pinned to
  Elasticsearch 7.1. Confirmed the 13 slugs are frozen and the 2019–2021 dates need `--force-dates`.
  Confirmed nav needs no change and only the category `description` is empty. Read StayHub's
  `app/search/` package (ES 8.15.3) and mapped what it covers vs. the seven gaps above. Awaiting
  the three decisions.
- **2026-08-22** — Decisions taken: **18 posts**, **medium length (12–18 min)**, **build the StayHub
  additions before writing**. Locked the 18-post spine and the eight StayHub additions above. Next:
  build the StayHub search additions.
- **2026-08-22** — Built all eight StayHub additions and verified every one against the live
  cluster. Found and fixed a real search bug (`best_fields` + `operator: and` returned nothing for
  "san francisco loft"). Added `tests/test_search.py`; suite went 165 → **193 passing**, no
  regressions. Documented the lot in the demo app's `CLAUDE.md` and `progress_report.md`.
  Next: draft the 18 posts, starting at lesson 1.

- **2026-08-23** — Wrote all **18 posts** (49,195 words, 328 headings, 188 code blocks). Built the
  track tooling by adapting the FastAPI track's: `manifest.py`, `seed.py`, `check_content.py`,
  `check_snippets.py`. Every non-trivial claim was run against the live 8.15.3 cluster first —
  `long` coercion truncating 119.99 to 119, `strict_dynamic_mapping_exception`, the
  index-then-search-returns-0-but-GET-works demo, bulk returning HTTP 200 with `errors: true`,
  the analyzer-mismatch case where BOTH spellings return zero, `must + filter` scoring identically
  to `must` alone, the `should`-next-to-`must` trap, `[lat, lon]` silently swapping, the
  alias-delete refusal, and a full yellow-cluster `allocation/explain`.
  `check_content.py`: **all 18 pass** (floor, cap, prose share, must-cite, rewrite-must-grow,
  byte-for-byte code round-trip). `check_snippets.py`: **no drift**, 93 of 188 blocks traced to
  files that run. Re-dated the track to 2020-2021 at Folau's request and recorded the version
  conflict that creates. Seeded to the **local** tree with `--force-dates` and ran a full
  `next build` + `verify-build.mjs`: **692/692 post URLs served, 42/42 categories, index
  cross-check agrees**. Spot-checked the rendered HTML — Prism highlighting live, heading anchors
  present, no WordPress wrapper divs. **Not seeded to prod.**

- **2026-08-23 (later)** — Found that `seed.py` had been copied from the FastAPI track *before*
  commit `d38048a` fixed two things in it, and ported both. (1) The `new`-slug collision guard
  rejected mere existence, so the second seed of this track would have aborted on all five new
  slugs; it now fails only when a `new` slug is found in a **different** category, which is the
  case that would actually drag a stranger's page into `/elasticsearch`. (2) `--force-dates` is
  **not** a one-off — `upsert_post` never overwrites an existing date, so after the first seed all
  eighteen dates are sticky and every re-base of `START_DATE` needs the flag again. Both docstrings
  corrected. Re-ran the dry run against the already-seeded local tree: 18 updates, guard prints a
  note instead of aborting.
  Also recorded `snapshot_took: "0ms"` in `MEASURED` — it was quoted from a real
  `snapshot --create` run but `check_content.py` had no way to know that. **Zero warnings, zero
  failures** across `check_content.py`, `check_snippets.py`, and the demo app's 193 tests.

- **2026-08-23 — PUBLISHED.** Seeded to **prod** with `--force-dates`: 13 updates in place, 5
  creates, tree 687 → **692 posts**, `/elasticsearch` archive holds 18, category count recorded 18.
  `npm run deploy` — content synced from prod, `next build`, `verify-build.mjs` **692/692 post URLs
  and 42/42 categories**, 1,805 files to `s3://lovemesomecoding.com`, CloudFront Function
  republished (94 redirects, 6.2 KB of the 10 KB limit) and **LIVE**, invalidation
  `ICDGLIF2LL1E2986A3LMV2SLGO` completed, edge verified serving build `394b0bd`.

  Checked at the edge afterwards: archive **200** and all **18 post URLs 200**; served HTML carries
  the new headings, Prism-highlighted code and **no** `boldgrid`/`col-md-12` wrappers; the archive
  lists 18 distinct posts with the category standfirst; the sitemap contains all **5** new URLs.

  ⚠️ The Elasticsearch-8.15-in-a-2020-post conflict recorded above is **live as written**. Folau
  said publish with the dates as set; it is not resolved, only shipped. The three options are still
  in the Dates section, and changing course later is a `START_DATE` edit plus a re-seed with
  `--force-dates` — no post body would need touching.

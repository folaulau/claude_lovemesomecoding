# Elasticsearch tutorial track — progress report

**Status:** 🟢 **StayHub additions built and verified. Ready to write.** 0 of 18 posts drafted.
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

# MySQL tutorial track — progress report

**Status:** ✅ **PUBLISHED AND LIVE.** All 52 posts on https://lovemesomecoding.com/sql, all 52 URLs verified at the edge.
**Started:** 2026-08-24
**Where it lands:** https://lovemesomecoding.com/sql

---

## What this is

A **52-post MySQL 8.4 track** at `/sql`. Unlike every other track in this repo, `/sql` is not
empty and not nearly empty — it is a **populated WordPress-era collection of 42 indexed posts**
published between 2018-09-29 and 2021-09-13.

| | |
|---|---|
| Existing posts | 42, all live and indexed |
| Rewritten in place | 42 — every slug frozen |
| New posts | 10 |
| **Total** | **52** |
| Redirects | **0** |

## Where it stands

| | |
|---|---|
| Topic table | ✅ 52 lessons across 12 parts |
| `manifest.py` | ✅ every lesson has slug, title, part, tags, excerpt, computed date, source |
| `FROZEN_SLUGS` | ✅ 42, cross-checked against the live category index — exact match, no drift |
| Lab database | ✅ `pizza_lab` built and verified: 400,000 orders, 1,000,000 items |
| `lab/build.sql` + `setup.sh` | ✅ deterministic, reproducible, integrity-checked |
| `seed.py` / `check_content.py` / `check_sql.py` / `authoring.py` | ✅ all four run clean |
| Post bodies | ✅ **52 of 52** — 278 statement blocks executed, 160 results re-derived |
| Content pipeline | ✅ nothing to do — see below |
| Site nav | ✅ nothing to do — `sql` is already in the Data Store group |

### Published 2026-08-24 — the complete track

Seeded to prod with `--force-dates` (the full date re-base, correct to run now that all 52 exist)
and the frontend deployed. **All 52 URLs return 200, all 52 are in the sitemap, none contains an
`<img>` or a `boldgrid` wrapper.** `/sql` holds 52 posts; the archive reads lesson 1 -> 52, the same
way `/vue` and `/postgre` do.

| | before | after |
|---|---:|---:|
| Posts | 42 | 52 |
| Total words | 18,643 | 50,126 |
| Prose share | — | 73% |
| Posts with no body | 2 | 0 |
| `<img>` tags | 99 | **0** |
| WordPress wrapper divs | 36 posts | **0** |
| Quoted results verified against a live database | 0 | **160** |

The command, for any later re-seed:

```bash
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/mysql_tutorial/seed.py \
    --env prod --write --force-dates
cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy
```

### Posts written so far

| # | slug | was | now | min | prose | results verified |
|---|---|---:|---:|---:|---:|---:|
| 08 | `sql-select` | 757 | 956 | 4 | 65% | 6 |
| 09 | `sql-where` | 62 | 833 | 4 | 60% | 7 |
| 10 | `sql-isnull` | 21 | 847 | 4 | 75% | 4 |
| 11 | `sql-between` | 80 | 669 | 3 | 56% | 4 |
| 12 | `sql-like` | 188 | 651 | 3 | 78% | 4 |
| 13 | `sql-order-by` | 135 | 781 | 4 | 73% | 3 |
| 14 | `sql-limit` | 169 | 783 | 4 | 70% | 4 |
| 16 | `sql-join-or-inner-join` | 165 | 878 | 4 | 71% | 3 |
| 17 | `sql-left-join` | 99 | 886 | 4 | 61% | 7 |
| 18 | `sql-right-join` | 56 | 635 | 3 | 78% | 2 |
| 19 | `sql-cross-join` | 25 | 636 | 3 | 70% | 3 |
| 20 | `sql-self-join` | 48 | 791 | 4 | 62% | 3 |
| 21 | `mysql-union` | new | 884 | 4 | 68% | 5 |
| | **total** | **1,805** | **10,230** | | **68%** | **55** |

`mysql-union` is the first NEW post published, so `/sql` went 42 -> 43 and it is now the newest
post in the archive (2024-08-14, its manifest date). The five rewrites kept 2019-03-31.

Written out of order deliberately: the "Reading data" section shares one set of tables, so its
outputs could be captured in batches. The remaining 45 are listed in `manifest.py` in reading
order.

---

## What is there now

Measured off `index/by-category/sql.json` and the 42 post objects in the **prod** tree on
2026-08-24. Word counts are the pipeline's own `wordCount`, which counts prose *and* code.

| | |
|---|---|
| Posts | 42 |
| Total words | 18,643 — but **5,944 of that is one post** |
| Posts under 100 words | 12 |
| Posts with **zero** words | 1 (`mysql-transaction`) |
| Posts still carrying WordPress `boldgrid-section` wrapper divs | 36 of 42 |
| `<img>` tags | 99 across 30 posts |

The thin end of the collection:

| slug | words | code blocks |
|---|---:|---:|
| `mysql-transaction` | 0 | 0 |
| `mysql-binlog` | 0 | 0 |
| `sql-explain` | 1 | 0 |
| `sql-isnull` | 21 | 0 |
| `sql-cross-join` | 25 | 1 |
| `mysql-server-helpful-functions` | 37 | 5 |
| `sql-self-join` | 48 | 1 |
| `sql-right-join` | 56 | 1 |
| `sql-where` | 62 | 1 |

`mysql-transaction` and `mysql-binlog` are **completely empty** — a title and an excerpt with no
body at all. `sql-explain` is one word. These are live URLs that have been indexed for years.

### The 42 slugs are frozen

Every one is a live, indexed URL. The frontend runs `trailingSlash: false` with a build guard
(`scripts/verify-build.mjs`) that **fails the build** if an indexed post URL stops resolving.
They are rewritten **in place** — renaming one is a dead link, not a refactor.

`manifest.FROZEN_SLUGS` holds all 42, read off the live category index rather than typed, and
`check_content.py` asserts every one is still in the track.

**This was a decision, not a default.** The alternative — consolidating the five separate join
posts and the one-idea stubs (`sql-isnull`, `sql-if`, `sql-between`) behind redirects — produces
better-shaped content and was rejected because those URLs have ranked since 2019. The cost
accepted: a handful of pages that are thin by nature. They are written tight and cross-linked
rather than padded to hit a length.

### Dates are re-based

The stored posts carry their original 2018-2021 dates, and `upsert_post` **never overwrites an
existing date**. The archive and the ‹ prev / next › pager sort by date, so leaving them produces
a track that reads in historical order rather than teaching order.

`START_DATE = 2024-05-06`, `STEP_DAYS = 5` → 52 lessons spanning **2024-05-06 → 2025-01-16**,
inside the 2023-2025 window the Vue and Postgres tracks use.

⚠️ **`--force-dates` is not optional here and is not a one-off.** Every one of the 52 posts
already exists with a date, so the *first* seed needs it, and so does any later change to
`START_DATE`. This is the trap the FastAPI track documented and the Postgres track corrected.

### No images — decided 2026-08-24

The rewritten posts contain **no `<img>` and no `<figure>`**, and `check_content.py` enforces it.

The 99 images in the existing posts are almost entirely WordPress screenshots of query output
(`image-2.png`, `image-4.png`, …). A screenshot of a result set is the worst possible form for it:
not searchable, not copyable, not selectable, invisible to a screen reader, and — the reason that
matters most here — **impossible for `check_sql.py` to verify.** Every one of them becomes a real
`plaintext` block holding the actual output, which the checker then re-derives.

`sql-interview-fundamentals` additionally hotlinks three third-party images from
`miro.medium.com`, `i.stack.imgur.com` and `assets.interviewbit.com` — a broken-link risk and a
licensing problem at once. Those go with the rest.

### Navigation and the content pipeline — nothing to do

- `src/lib/nav.ts` already lists `sql` in the **Data Store** group.
- `sql` is already in the backend's `SUPPORTED_LANGUAGES`, and `mysql` already aliases to it
  (`app/services/content.py`).
- `prismjs/components/prism-sql` is already statically imported by the frontend
  (`src/lib/content.ts`).

Only the stored category record needs fixing — it currently has an empty description — and
`upsert_category` does that on seed.

---

## Sources

Per the README:

- https://www.w3schools.com/mysql/default.asp — what a beginner actually needs, and the spine
- https://www.mysqltutorial.org/ — depth and the topics w3schools skips

Filter, from the README: *"We don't need to create a post for each small thing."* Applied to the
**new** posts. It could not be applied to the 42 existing ones without retiring indexed URLs.

---

## The demo application

`lovemesomecoding_demo_project/pizza/pizza-springboot-backend` — a Spring Boot 4 pizza-ordering
API on **MySQL 8.4**, schema managed by Liquibase in
`src/main/resources/db/changelog/sql/001..009`.

It is unusually good raw material, because the schema was written with its reasoning in comments:

- `customer_order.user_id` is **nullable on purpose** — that is what makes guest checkout work,
  and it is the LEFT JOIN lesson's example rather than an invented one
- `order_item` **snapshots** `product_name` / `crust_name` / `unit_price`, while `cart` stores no
  prices at all and recomputes — the same schema arguing both sides of denormalization
- `ON DELETE CASCADE` and `ON DELETE SET NULL` both appear, each chosen for a stated reason
- `DECIMAL(10,2)` money throughout, `DATETIME(6)`, `BIGINT` PK alongside a `CHAR(36)` public UUID
- tables named `app_user` and `customer_order` because `user` and `order` are reserved

Versions are **read off the running container and the pom**, not chosen:

| | |
|---|---|
| MySQL server | 8.4.11 |
| image | `mysql:8.4` |
| Spring Boot | 4.1.0 |
| character set | utf8mb4 / utf8mb4_0900_ai_ci |
| `transaction_isolation` | REPEATABLE-READ |
| `sql_mode` | includes `ONLY_FULL_GROUP_BY` |

Reached on **127.0.0.1:3308** — not 3306. The demo publishes a non-default host port on purpose;
see the comment in its `docker-compose.yml`.

---

## Two databases, and the difference matters

### `pizza` — the demo application's own

18 orders, 14 products, 27 order items. That is the **right** size for SELECT, joins and
aggregation: a reader can hold the whole result set in their head and check the answer by eye.

### `pizza_lab` — built by `lab/build.sql`

The same schema at a size where the optimizer has to make choices. At 18 rows InnoDB scans
everything, so an "add an index" lesson would show an index the planner never chooses and an
EXPLAIN that says `ALL` no matter what you do.

| table | rows |
|---|---:|
| `app_user` | 50,000 |
| `customer_order` | 400,000 |
| `order_item` | 1,000,000 |
| `order_item_topping` | 1,000,000 |
| `product` / `product_size` | 14 / 42 |

Orders by status: COMPLETED 340,000 · CANCELLED 24,000 · PENDING_PAYMENT 16,000 ·
PREPARING 12,000 · PAID 8,000. Guest orders (`user_id IS NULL`): 80,000. Order dates span
**2023-01-02 → 2025-01-01**.

Only the posts in `manifest.LAB_POSTS` use it, and they say so.

That it works is measured, not assumed:

```
EXPLAIN SELECT * FROM customer_order WHERE customer_name = 'Customer 42';
  type: ALL   rows: 396091   -- no index                    234 ms
EXPLAIN SELECT COUNT(*) FROM customer_order WHERE status = 'PAID';
  type: ref   key: idx_customer_order_status  Using index    16 ms
```

### Two properties `build.sql` deliberately has

**It is fully deterministic — not one `RAND()` call.** Row counts, the status mix, items per order
and every date are derived from the row number with modular arithmetic. Two builds produce
identical tables, which is what lets `check_sql.py` re-derive a figure a post quotes and compare
it exactly. A seeded `RAND()` is reproducible on one server version and not across an upgrade.

**Dates are anchored to a fixed epoch (`@LAB_EPOCH = 2025-01-01`), not to `NOW()`.** The demo seed
uses `DATE_SUB(NOW(), ...)`, which is right for a dashboard that should always look populated and
wrong for a tutorial — every quoted result would go stale overnight and `check_sql.py` would fail
every day after the one it was written on.

---

## Two bugs the lab build hit, both worth not repeating

### 1. `AUTO_INCREMENT` values from `INSERT ... SELECT` have gaps

The numbers table is built by doubling (`INSERT INTO seq SELECT NULL FROM seq`). It ended up with
the right **count** — 1,648,576 — and a `MAX(n)` of **1,976,220**.

`innodb_autoinc_lock_mode` is `2` (interleaved) by default in MySQL 8. For an `INSERT ... SELECT`
the server does not know the row count in advance, so it grabs auto-increment values in growing
batches and discards whatever it did not use.

So `WHERE n <= 400000` quietly selected 262,144 rows, and every table downstream was short:
`app_user` 32,768 instead of 50,000, `customer_order` 262,144 instead of 400,000. **The tell was
that every count was an exact power of two.** Nothing errored.

Fixed by renumbering with `ROW_NUMBER() OVER (ORDER BY n)` into a second table.

### 2. Product ids are not contiguous

The demo menu is ids **1-8** (pizzas) and **20-25** (drinks) — 14 products, but not `1..14`.
Picking one with `p.id = 1 + something % 14` therefore only ever names ids 1..14, and the join
silently dropped every drink.

`order_item` came out at **571,430** instead of 1,000,000 — which is exactly **8/14** of the
intended number, the same tell as above. Fixed with a dense `product_pick` mapping table built
from `ROW_NUMBER()`, so the generator survives the menu changing.

Both bugs produced *plausible* databases that were quietly wrong. Neither raised an error. That is
why `setup.sh` ends by asserting counts and referential integrity rather than printing "done".

### 3. A quoted result that was only *usually* right

`sql-limit` opened with `ORDER BY total DESC LIMIT 3`. Two orders in the demo data share the total
32.18, so the third row could legitimately come back as either of them — and `check_sql.py` passed
it, once, by luck.

That is worse than a wrong number: it fails on someone else's machine, long after it was written,
for no visible reason. **`check_sql.py` now executes every post TWICE from a rebuilt state and
fails any compared output that differs between the runs.** `--once` skips it.

The irony is that the post is *about* this bug — pagination over a non-unique sort key repeats and
skips rows. It now demonstrates it with deterministic queries and a unique tiebreaker.

### 4. A block the checker skipped and reported as passing

`mysql-union` quotes a UNION whose branches are parenthesised so each can carry its own
`ORDER BY`/`LIMIT`. It therefore starts with `(`, which `STATEMENT_START` did not match, so the
block was classified `fragment` and **never run** — while the post reported `all pass`.

A checker that silently skips work is worse than one that fails, because the summary line looks
identical either way. The `--list` output is the tell: watch the `fragment` count and know why each
one is there. `STATEMENT_START` now allows leading parentheses.

### 5. A checker rule that cried wolf

The "only declared posts may show a query plan" rule searched the whole post body, so
`sql-order-by` failed for using the words *Using filesort* in a sentence. A quoted plan is by
definition output, and output lives in a `plaintext` block — the rule now searches those only.
A rule that fires on correct work is a rule that gets switched off.

---

## The plan

1. ✅ Topic table, `manifest.py`, `FROZEN_SLUGS` cross-checked against live
2. ✅ `lab/build.sql` + `setup.sh`, built and verified
3. ✅ `seed.py`, `check_content.py`, `check_sql.py`, `authoring.py`
4. 🟡 Author 52 post bodies, running `check_sql.py` per post as it is written — **7 done**
5. ⬜ Seed `--env local --write --force-dates`, review at `:3000`
6. ⬜ Seed `--env prod --write --force-dates`, deploy the frontend
7. ⬜ Verify all 52 URLs serve and are in the sitemap

## Open questions

None blocking. Two noted for when the posts are written:

- `mysql-replication` needs a second container to demonstrate against. `check_sql.py` will have to
  classify those blocks as multi-session/unavailable rather than run them, the way the Postgres
  checker does.
- `mysql-json` has no JSON column in the pizza schema. The lesson adds one to a scratch copy
  rather than pretending the app has one — it must not claim the demo app uses JSON when it does
  not.

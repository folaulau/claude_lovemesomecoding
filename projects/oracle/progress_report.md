# Oracle Database track — progress report

**Status: DONE and live.** 13 posts under `/oracle` on https://lovemesomecoding.com.
Two follow-ups left — see *Outstanding*.

Step 9 records a real bug this work exposed in `sync-content.sh`, which briefly shipped a wrong
category count. Fixed, and the build now rejects it.

Started and completed 2026-08-04.

## Requirement

> "now add oracle as a data store and create posts for it … do this on local as well as prod"

Read as: Oracle joins the six existing categories in the *Data Store* nav dropdown (screenshot showed
SQL 42, Postgres 2, Elasticsearch 13, Hasura 11, MongoDB 3, Snowflake 1), with real tutorial content
behind it, in both the `local` and `prod` content trees.

Followed the same day by: *"create a post for CROSS APPLY in oracle"* — see step 8.

## What was done

| | |
|---|---|
| Category | `oracle`, display name **Oracle**, `/oracle` |
| Posts | **13**, ~19,000 words, 143 code blocks |
| Trees | `local` and `prod`, both 512 → **525** posts, 43 → **44** categories |
| Nav | `Data Store` group, second position, after SQL |

### 1. Backend — optional publish date

`PostUpsert` gained an optional `date` (`YYYY-MM-DDTHH:MM:SS`, regex-validated) and
`upsert_post` honours it **only when the post is new**:

```python
"date": existing.get("date") or payload.get("date") or now,
```

This was needed, not cosmetic. Without it every post in a seeded track gets the same
second-precision `now_iso()` timestamp, and then:

- the category archive's order depends on Python sort stability rather than intent, and
- `siblings()` (which reverses the category index to walk a track oldest-first) produces a pager
  that runs backwards.

An existing post keeps its original date, so the field cannot rewrite history through the admin API —
and re-seeding an edited post never reshuffles the archive. Three tests added: ordering, immutability
on update, and rejection of a malformed date. **90 tests pass, 95.33% coverage** (was 87 tests).

### 2. Content

One HTML file per post in `posts/`, plain semantic markup — no WordPress `boldgrid-section` wrappers,
which the frontend does not need. Track order and dates are in `README.md`.

Written as a progression rather than 13 standalone pages: architecture → container →
schema/privileges → types → DDL → SELECT → joins → CROSS APPLY → analytics → PL/SQL → indexes and
plans → transactions → Spring Boot. The angle throughout is "what differs from MySQL/Postgres and
what has cost people an afternoon" — `VARCHAR2(n CHAR)` vs `BYTE`, `DATE` carrying a time, the empty
string that is `NULL`, `NOT IN` with a `NULL` returning zero rows, the `ROWS`/`RANGE` default frame,
`allocationSize` vs `INCREMENT BY`.

Java examples use Lombok, per the repo standard. The Spring Boot post explicitly warns against
Lombok's default `@EqualsAndHashCode` on an entity.

### 3. Verification before writing

`check_content.py` normalises every post through `app/services/content.py` and compares each code
sample **byte-for-byte** against what was authored — not by length, because that is exactly the check
that let the migration nearly ship corrupted code blocks. It also asserts every emitted block matches
the `<pre class="language-X"><code class="language-X">` shape the frontend highlighter keys on, that
every heading got an anchor, and that no excerpt exceeds 500 chars.

Result: **143/143 code blocks round-trip identically.** Needs no AWS credentials, so it runs before
anything is written anywhere.

### 4. Seeding

`seed.py` drives `app.services.posts.upsert_post` and `app.services.categories.upsert_category`
rather than writing S3 objects itself, so the post objects and all four derived indexes are
maintained by the same code the admin API uses. Dry run by default; `--write` to commit.

Pre-flight checks that every content file exists and that no slug already belongs to another
category (post slugs are global — `getPost(slug)` is not scoped by category) before writing
anything, so a failure cannot half-seed a tree.

### 5. Frontend

`src/lib/nav.ts`: `oracle` added to the *Data Store* group and `oracle: 'Oracle'` to
`DISPLAY_NAMES`. Nothing else needed — categories, archives, sitemap, RSS and the search index are
all derived from the content indexes at build time. `tsc --noEmit` clean.

### 6. Build verification

Full `npm run build` against **both** trees:

```
posts served       525/525
categories served  44/44
pages redirected   41
archive pages      104 (/page/2../page/105)
html files emitted 688
all indexed URLs accounted for
```

Spot-checked in `npm run preview` (:4321, CloudFront's real routing rules):

- `/oracle` → 200, archive lists all 13, description renders, "13 tutorials"
- every `/oracle/{slug}` → 200
- `/oracle/` → 301 (edge function strips the trailing slash, as designed)
- `/oracle-table-of-content` → 404, correctly — that page never existed, so unlike the other 38
  categories there is no legacy TOC page to redirect
- Prism highlighting present; languages emitted are `java`, `sql`, `yaml`, `bash`, `markup`,
  `plaintext`
- Pager walks the track: Introduction has only *next*, Spring Boot has only *prev*

### 7. Deployed

`AWS_PROFILE=folau npm run deploy` — files to `s3://lovemesomecoding.com`, edge function republished
(41 redirects, 2.8 KB of the 10 KB limit), CloudFront `E30YUPLP37MY9U` invalidated and waited on,
`version.txt` read back from the edge.

Note: the build stamp is derived from the git SHA, so with nothing committed it stays `394b0bd`
across deploys and the `version.txt` match is a weak signal. Verified against served content
instead — see step 8.

### 8. CROSS APPLY added afterwards (same day)

Requested separately. It became lesson **8**, `/oracle/oracle-cross-apply`, dated 2024-02-22 so it
sits between joins (the 19th) and analytic functions (the 26th). Confirmed in the built output, the
pager now reads joins → cross apply → analytic functions.

Rather than leave the same material in two places, the joins post's `LATERAL`/`APPLY` section was cut
down to the one thing that belongs there — *a plain join cannot let the right side see the row it is
joined to* — and hands off to the new post. The analytic-functions post's top-N section gained a
cross-reference the other way, since the two features answer the same question with opposite
performance characteristics. Both edited posts kept their original `date`, as designed.

File prefixes 08–12 were renumbered to 09–13. They are readability only; `manifest.py` order and
`date` are what the site reads.

Verified on the **live** page, not just the build: `/oracle/oracle-cross-apply` serves 102 KB of
static HTML containing the full prose, 10 code blocks and 424 Prism token spans, with **zero**
`fetch()`/`XMLHttpRequest` calls and **zero** references to `api.lovemesomecoding.com`. Sitemap and
`search-index.json` each carry 13 Oracle entries.

### 9. Bug found and fixed: the content sync could skip a changed index

The first deploy of the 13th post shipped `/oracle` reading **"12 tutorials"** above a list of 13.
Not a cache — the built HTML itself was wrong, because `content/index/categories.json` on disk still
said 12 while S3 said 13.

Cause, from the `aws s3 sync` docs: *"same-sized items will be ignored unless the local version is
newer than the S3 version."* The derived indexes defeat both halves of that test.

- `"count":12` → `"count":13` does not change the file's **length** — still 4101 bytes.
- The local mtime is stamped at *download* time, and S3's `LastModified` is **UTC**. The S3 write
  (21:44 UTC = 14:44 local) therefore looked *older* than a local file downloaded at 15:27 local.

Same size, local "newer" → skipped. Silently, on the file that decides every category count.

**Two fixes, both committed:**

1. `scripts/sync-content.sh` now passes **`--exact-timestamps`**, which skips only on an exact
   timestamp match. Verified: re-running the old command left the file at 12; with the flag it
   immediately corrected to 13.
2. `scripts/verify-build.mjs` gained check **6**, cross-checking the derived indexes against each
   other — every `categories.json` count against the post index, the sum of counts against the total
   post count, and each `by-category/{slug}.json` length against its count. Nothing else in the file
   could have caught this: every URL still resolved, so a stale count renders happily.

Confirmed the new guard fails the exact build that shipped, by reverting the count to 12:

```
BUILD REJECTED:
  ✗ 1 category count(s) disagree with the post index: oracle says 12, index has 13
  ✗ category counts total 524 but the post index holds 525
  ✗ 1 category archive(s) out of step with the count: oracle (13 vs 12)
```

Then rebuilt and redeployed. Live now: `/oracle` says "13 tutorials", the Data Store dropdown reads
SQL 42 · **Oracle 13** · Postgres 2 · Elasticsearch 13 · Hasura 11 · MongoDB 3 · Snowflake 1, and the
homepage says 525.

## Decisions

**Seed through the backend service layer, not direct S3 writes.** The static build reads only the
derived indexes and never the post bodies, so an index that disagrees with the posts produces a wrong
site with no error anywhere. One code path for writes is the only way to keep them in step.

**Add `date` to the API rather than post-patching the JSON.** The alternative was writing records and
then calling the private `_reindex`, which duplicates index logic in a throwaway script — precisely
the drift the previous decision avoids. Backdating a post is also a legitimate admin capability.

**No `oracle-table-of-content` redirect.** The 38 existing redirects exist because WordPress had
hand-maintained TOC pages that the generated archives replaced. Oracle never had one; inventing a
redirect for a URL that was never indexed would add a rule with nothing pointing at it.

**Slugs are prefixed `oracle-`**, matching `snowflake-introduction` and `postgres-introduction`. Post
slugs are global in this schema, so a bare `introduction` would have collided.

**Track dates are Jan–Mar 2024, not today.** Backdating keeps the homepage's "Latest tutorials" from
being 13 consecutive Oracle posts, and gives the track a sensible internal order. The trade-off is
that the posts do not appear on page 1 of the archive; they are found through the nav, the category
page and search, which is how a reference track is actually read. Reversing this means deleting and
re-seeding, because `date` is immutable once set.

## Outstanding

- [ ] Resubmit `https://lovemesomecoding.com/sitemap.xml` to Search Console so the 13 new URLs get
      crawled. (Folds into the pre-existing sitemap-submission item in the root `CLAUDE.md`.)
- [ ] Nothing is committed. Three repos have uncommitted changes:

| Repo | Files |
|---|---|
| `claude_lovemesomecoding` | `CLAUDE.md`, `projects/oracle/` (new) |
| `lovemesomecoding_frontend` | `src/lib/nav.ts`, `scripts/sync-content.sh`, `scripts/verify-build.mjs`, `CLAUDE.md`, `README.md` |
| `lovemesomecoding_backend` | `app/schemas.py`, `app/services/posts.py`, `tests/test_posts.py`, `CLAUDE.md` |

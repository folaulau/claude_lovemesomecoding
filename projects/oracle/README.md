# Oracle Database track

Adds **Oracle** as a category under the *Data Store* nav group and publishes a 14-post tutorial
track into it.

```
projects/oracle/
  manifest.py        category metadata + one entry per post (slug, title, date, tags, excerpt)
  posts/NN-slug.html the post bodies, plain semantic HTML
  seed.py            writes the category and posts into a content tree
  check_content.py   proves the normaliser round-trips every code sample (no AWS needed)
  progress_report.md status and decisions
```

## The track

| # | Slug | Date |
|---|------|------|
| 1 | `oracle-introduction` | 2024-01-08 |
| 2 | `oracle-run-with-docker` | 2024-01-15 |
| 3 | `oracle-users-schemas-and-privileges` | 2024-01-22 |
| 4 | `oracle-data-types` | 2024-01-29 |
| 5 | `oracle-tables-constraints-and-sequences` | 2024-02-05 |
| 6 | `oracle-select-essentials` | 2024-02-12 |
| 7 | `oracle-joins` | 2024-02-19 |
| 8 | `oracle-cross-apply` | 2024-02-22 |
| 9 | `oracle-analytic-functions` | 2024-02-26 |
| 10 | `oracle-pivot` | 2024-03-01 |
| 11 | `oracle-pl-sql` | 2024-03-04 |
| 12 | `oracle-indexes-and-execution-plans` | 2024-03-11 |
| 13 | `oracle-transactions-and-locking` | 2024-03-18 |
| 14 | `oracle-with-spring-boot` | 2024-03-25 |

URLs are `/oracle/{slug}`. **The slugs are now live — changing one changes a URL.**

The dates ascend with the track on purpose. Archives and the sitemap sort newest first (so the
archive leads with Spring Boot), and `siblings()` in `src/lib/content.ts` reverses the category index
to walk oldest-first, which is what makes the ‹ prev / next › pager read as lesson 1 → lesson 14.
Identical timestamps would leave that ordering up to sort stability.

To insert a post mid-track, give it a date between its neighbours (`oracle-cross-apply` is
2024-02-22, between joins on the 19th and analytic functions on the 26th) and renumber the `NN-`
file prefixes. The prefixes are for humans only — `manifest.py` order and `date` are what the site
uses.

## Commands

Run from the repo root. `check_content.py` needs no AWS credentials; `seed.py` does.

```bash
# Verify the content before writing anything anywhere
lovemesomecoding_backend/.venv/bin/python projects/oracle/check_content.py

# Dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/oracle/seed.py --env local

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/oracle/seed.py --env local --write
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/oracle/seed.py --env prod  --write
```

`seed.py` is idempotent — a re-run updates the posts in place. `date` is only applied when a post is
new, so a re-run never reshuffles the archive.

## Why seed through the backend service layer

`seed.py` imports `app.services.posts` and `app.services.categories` from
`lovemesomecoding_backend` rather than writing S3 objects itself. The static build reads **only** the
derived indexes (`index/posts.json`, `index/by-category/oracle.json`, `index/categories.json`,
`search/index.json`) and never the post bodies, so an index that disagrees with the posts is
invisible until the site is wrong. Reusing the same code the admin API uses is the only way to be
sure they agree.

It also means the bodies go through `app/services/content.py`, which produces the exact
`<pre class="language-X"><code class="language-X">` shape the frontend's build-time Prism highlighter
matches.

## Editing a post later

Edit the HTML in `posts/`, then:

```bash
lovemesomecoding_backend/.venv/bin/python projects/oracle/check_content.py
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/oracle/seed.py --env prod --write
cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy
```

Editing through `/admin` works too, but the admin's TipTap editor will not round-trip the raw HTML in
these files, so the file here would then be stale. Pick one source of truth per post.

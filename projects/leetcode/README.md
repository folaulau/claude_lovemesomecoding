# Leetcode

## Where problems and solutions?
./leetcode

## What do we need to do?
- We need to move these leetcode problems and solutions to lovemesomecoding.com under Software Engineering > Fundamental Problems

## How to post them?
- let's post by rounds like problem 1 - 10, then 11 - 20, then 21 - 30, etc

## My goal
- my goal is to be able to use these problems to prepare for coding interviews.

---

## How this is built

One post per problem, published in rounds of ten LeetCode numbers, into the **existing**
`fundamental-problem` category. That category is already in the nav under "Software Engineering" as
"Fundamental Problems", so there is no frontend change and no new category.

```
projects/leetcode/
  manifest.py         category metadata + one entry per problem (number, slug, title, date, tags, excerpt)
  posts/NNN-slug.html the post bodies, plain semantic HTML
  seed.py             writes the category and posts into a content tree
  check_content.py    proves the normaliser round-trips every code sample (no AWS needed)
  tests/              extracts the code blocks from the HTML and actually runs them
  progress_report.md  status and decisions
```

URLs are `/fundamental-problem/leetcode-{number}-{title}`. **Slugs are frozen once published —
changing one changes a live URL.**

The source repo (`leetcode/github-2022-9-30/`) is a **reference for the approach, not the copy
source.** 460 of its 601 files carry Chinese-language notes and many are LintCode variants with
different constraints. Every post here is written fresh and every solution rewritten. See
`progress_report.md` for the reasoning.

## The rounds

A round is ten LeetCode numbers, holding however many of them the source repo actually has.

| Round | Numbers | Posts | Status |
|---|---|---|---|
| 1 | 1–10 | 7 — missing 3, 4, 6 | **live** since 2026-08-12 |
| 2 | 11–20 | 6 — missing 11, 16, 17, 18 | **live** since 2026-08-12 |
| 3 | 21–30 | 4 — 21, 22, 23, 28 | **live** since 2026-08-13 |
| 4 | 31–40 | 6 — 31, 33, 34, 36, 39, 40 | **live** since 2026-08-14 |
| 5 | 41–50 | 6 — 41, 42, 43, 46, 47, 49 | not started |

`seed.py --round N` publishes exactly one round.

### Interview essentials (out of round order)

Four posts published ahead of their rounds because they cover patterns rounds 1–4 leave out —
one-pass scanning, grid BFS/DFS, bucket sort, and the return-one-record-another tree recursion.
They carry `"batch": "interview-essentials"` in the manifest instead of belonging to a round, and
seed with `--batch` rather than `--round`:

| # | Problem | Pattern |
|---|---|---|
| 121 | Best Time to Buy and Sell Stock | one pass, running minimum |
| 200 | Number of Islands | grid DFS/BFS |
| 347 | Top K Frequent Elements | bucket sort / min-heap of size k |
| 543 | Diameter of Binary Tree | return depth, record diameter |

`--round` and `--batch` are mutually exclusive. When these numbers come up in their real rounds
(13, 20, 35, 55), drop the `batch` key rather than adding a duplicate entry.

## Dates, and why they ascend

Archives and the sitemap sort newest first, and `siblings()` in `src/lib/content.ts` reverses the
category index so ‹ prev / next › walks oldest-first. Dates therefore ascend with the LeetCode
number, which is what makes the pager read 1 → 2 → 5 → 7. Identical timestamps would leave that
ordering up to sort stability.

Rounds 1 and 2 are spaced an hour apart on 2026-08-12, after the 11 legacy 2019 posts in this
category, so the track is one contiguous run. Round 3 moved to 2026-08-13 — **one day per round from
here on**, since cramming further rounds into a single day gets silly. **Later rounds must take
later dates.**

## Commands

Run from the repo root. `check_content.py` and the tests need no AWS credentials; `seed.py` does.

```bash
# Do the code samples actually work? Extracts them from the HTML and runs them.
python projects/leetcode/tests/test_python.py
python projects/leetcode/tests/build_java.py && \
  javac -d projects/leetcode/tests/out projects/leetcode/tests/Main.java && \
  java -cp projects/leetcode/tests/out Main

# Do they survive the content pipeline intact?
lovemesomecoding_backend/.venv/bin/python projects/leetcode/check_content.py

# Dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/leetcode/seed.py --env local --round 1

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/leetcode/seed.py --env local --round 1 --write
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/leetcode/seed.py --env prod  --round 1 --write

# posts published outside the round sequence
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/leetcode/seed.py --env prod --batch interview-essentials --write
```

`seed.py` is idempotent — a re-run updates the posts in place. `date` is only applied when a post is
new, so a re-run never reshuffles the archive.

`build_java.py` writes `tests/Main.java`; it and `tests/out/` are build artifacts, not sources.

## Why seed through the backend service layer

Same reason as `projects/oracle/` — `seed.py` imports `app.services.posts` and
`app.services.categories` rather than writing S3 objects itself. The static build reads **only** the
derived indexes (`index/posts.json`, `index/by-category/fundamental-problem.json`,
`index/categories.json`, `search/index.json`) and never the post bodies, so an index that disagrees
with the posts is invisible until the site is wrong. Reusing the same code the admin API uses is the
only way to be sure they agree.

It also means the bodies go through `app/services/content.py`, which produces the exact
`<pre class="language-X"><code class="language-X">` shape the frontend's build-time Prism highlighter
matches. Only `java`, `python`, `bash`, `sql`, `javascript`, `markup`, `yaml`, `json`, `markdown`,
`groovy`, `kotlin`, `docker` and `plaintext` are loaded — anything else silently renders unhighlighted.

## Adding a post

1. Write `posts/NNN-slug.html` — plain semantic HTML, no wrapper divs. Escape `<`, `>` and `&`
   inside `<pre>` blocks as `&lt;`, `&gt;`, `&amp;`.
2. Add an entry to `manifest.py` in LeetCode-number order, with a date later than the one before it.
3. Run the tests, then `check_content.py`, then `seed.py` dry, then `--write`.

Editing through `/admin` works too, but the admin's TipTap editor will not round-trip the raw HTML
in these files, so the file here would then be stale. Pick one source of truth per post.

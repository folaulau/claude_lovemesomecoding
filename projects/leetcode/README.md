# Leetcode

## Where problems and solutions?
./leetcode

## What do we need to do?
- We need to move these leetcode problems and solutions to lovemesomecoding.com under Software Engineering > Fundamental Problems

## How to post them?
- let's post by rounds like problem 1 - 10, then 11 - 20, then 21 - 30, etc

## My goal
- my goal is to be able to use these problems to prepare for coding interviews.

- date these leetcode posts on a random date between 2022 and 2024

- add a category to each post so I know what kind of algorithm being use like Dynamic Programming, String, Sorting, Searching, etc.

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
| 5 | 41–50 | 6 — 41, 42, 43, 46, 47, 49 | **live** since 2024-08/09 |
| 6 | 51–60 | 7 — 51, 52, 53, 55, 56, 57, 58 | **live** since 2024-09 |
| 7 | 61–70 | 8 — 62, 63, 64, 65, 67, 68, 69, 70 | **live** since 2024-09/10 |
| 8 | 71–80 | 4 — 71, 72, 76, 78 | **live** since 2024-10/11 |
| 9 | 81–90 | 3 — 81, 83, 88 | **live** since 2024-11 |
| 10 | 91–100 | 4 — 91, 94, 98, 100 | **live** since 2024-11 |
| 11 | 101–110 | 6 — 101, 102, 103, 104, 105, 110 | not started |
| 12 | 111–120 | 5 — 111, 112, 114, 118, 119 | not started |

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

## Algorithm categories

Every entry carries an `algorithm` from the `ALGORITHMS` taxonomy in `manifest.py` — the standard
HackerRank algorithm-domain list. `check_content.py` fails the build if one is missing or misspelt,
so a typo cannot quietly create a category of one.

`seed.py` emits it slugified as the **first** tag on the post, ahead of the free-form ones:
`leetcode-15-3sum` gets `["sorting", "leetcode", "array", "two-pointers"]`.

**Nothing on the public site renders tags.** They are stored on the post record, carried in
`index/posts.json` and the category index, and editable in `/admin` — but no page component reads
them, and the search index only holds url, title, category and excerpt. This is metadata waiting for
a browse UI, not something a reader sees today.

Current distribution across the 62 posts:

| Algorithm | Posts |
|---|---|
| Implementation | 11 |
| Strings | 10 |
| Dynamic Programming | 10 |
| Recursion | 9 |
| Sorting | 8 |
| Searching | 6 |
| Graph Theory | 5 |
| Greedy | 2 |
| Bit Manipulation | 1 |

Constructive Algorithms, Game Theory and Warmup are in the taxonomy but unused so far —
nothing published fits them.

Changing an `algorithm` means re-seeding that post, which rewrites its content too. That is safe
(the content files are the source of truth) but it does bump `modified`.

`--round` and `--batch` are mutually exclusive. When these numbers come up in their real rounds
(13, 20, 35, 55), drop the `batch` key rather than adding a duplicate entry.

### Legacy rewrites (`--batch legacy-rewrite`)

Three posts migrated from WordPress in 2019 that already own their URLs, rewritten in place. They
have **no `number`**, so `check_content.py` exempts them from the manifest's number/date ordering
checks, and `seed.py --round` skips them.

| Slug | Was | Now |
|---|---|---|
| `fundamental-problem-two-number-sum` | 3 solutions, all `language-plaintext`, hash-set version did not compile | highlighted, compiling, Java + Python, indices variant |
| `fundamental-problem-three-number-sum` | 1 solution, `language-plaintext` | highlighted, Java + Python, duplicates contrast with LeetCode 15 |
| `fundamental-problem-recursion` | **empty** — `wordCount: 0` | recursion as an interview technique |

`upsert_post` keeps an existing post's `date`, so re-seeding these never moves them in the archive
and the manifest `date` is documentation only. **Their slugs are live — do not change them.**

`fundamental-problem-recursion` deliberately does *not* re-explain what recursion is;
`/data-structure-algorithm/data-structure-algorithm-recursion` already does that, and two posts
competing for the same query would cannibalise each other. The two cross-link.

## Dates, and why they ascend

Archives and the sitemap sort newest first, and `siblings()` in `src/lib/content.ts` reverses the
category index so ‹ prev / next › walks oldest-first. Dates therefore ascend with the LeetCode
number, which is what makes the pager read 1 → 2 → 5 → 7. Identical timestamps would leave that
ordering up to sort stability.

The LeetCode dates are spread randomly across **2022–2024** — generated once with a fixed seed, then
sorted — so the track reads as written over three years rather than bulk-published on one day. They
are random but **strictly ascending with the LeetCode number**, because the pager ordering above
depends on it. Shuffling them properly would scramble prev/next.

They still sit after the 2018/2019 legacy posts, so the track remains one contiguous run at the top
of the category.

The manifest is ordered by LeetCode number and `check_content.py` enforces that **both** the numbers
and the dates ascend. A new round therefore has to be slotted into the date gap left by its numeric
neighbours, not simply appended. Round 5 (numbers 41–49) sits between LeetCode 40
(`2024-08-09`) and LeetCode 121 (`2024-09-18`), so its dates run `2024-08-11` to `2024-09-14`. Round
6 (51–58) had only the 90 hours left in that gap, so its seven dates run `2024-09-14 22:22` to
`2024-09-17 15:43` — a tighter cluster than the rest of the track.

Round 7 had **no** room left, so LeetCode 121 was moved forward with `--redate`, from
`2024-09-18` to `2024-11-10`. That reopened the two-month gap between it and LeetCode 200
(`2024-11-19`), and round 7's eight posts are spread across `2024-09-18` to `2024-10-29`.

**That is the move to repeat when the gap runs out** — but check first rather than doing it by
reflex. Round 8 needed only four slots and the 12 days left after round 7 were plenty, so nothing
was moved. Round 10 was where it finally ran out, and rather than nudge 121 again the **whole
interview-essentials block moved at once**: 121 to `2024-12-08`, 200 to `2024-12-14`, 347 to
`2024-12-21`, 543 left at `2024-12-28`. The repo holds 15 posts numbered 91–120 that must sort
before 121, so one operation buys rounds 10, 11 and 12 instead of three separate ones. Rounds 11 and
12 have `2024-11-16` to `2024-12-08` to work with.

**The 2022–2024 window is the real constraint and it is nearly spent.** Only 55 of roughly 300
numbered problems in the repo are published, and the track already spans March 2022 to December 2024.
Round 13 starts at LeetCode 121, where the numbered rounds catch up with the interview-essentials
posts and this juggling stops working. That needs a decision — spread the whole track more tightly,
or extend past 2024 — and it is a decision about the brief, not a technical one.

The four interview-essentials posts (121, 200, 347, 543) are the only things standing between the
numbered rounds and the end of 2024, and their dates are synthetic track ordering exactly like every
other LeetCode date here — moving one forward is cheap, idempotent and reversible. Once the numbered
rounds pass 121 the constraint disappears and later rounds simply take dates after `2024-12-28`.

### Changing a date after publication

`upsert_post` deliberately never re-applies `date` to an existing post, so editing the manifest and
re-seeding does **not** move anything. That is on purpose — it stops a routine content fix from
reshuffling the archive. Use the dedicated path instead:

```bash
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/leetcode/seed.py --env prod --redate
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/leetcode/seed.py --env prod --redate --write
```

It patches only `date` on the stored record and re-runs the same index maintenance the admin API
uses, so `wpId`, the body, the excerpt and `modified` all survive. It refuses to touch entries with
no `number` — the legacy rewrites' 2018/2019 dates are real, not track ordering. Idempotent: a
second run reports that everything already matches.

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

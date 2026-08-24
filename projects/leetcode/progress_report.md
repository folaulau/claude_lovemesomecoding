# LeetCode track — progress report

Moving the LeetCode problems and solutions in `leetcode/` onto lovemesomecoding.com under
**Software Engineering → Fundamental Problems**, published in rounds of ten LeetCode numbers.

**Status: rounds 1–6, the interview-essentials batch and three legacy rewrites are all LIVE.**

---

## Where things stand

| | |
|---|---|
| Round 1 (LeetCode 1–10) | 7 posts — **live** |
| Round 2 (LeetCode 11–20) | 6 posts — **live** |
| Round 3 (LeetCode 21–30) | 4 posts — **live** |
| Round 4 (LeetCode 31–40) | 6 posts — **live** |
| Interview essentials | 4 posts — **live** (121, 200, 347, 543, out of round order) |
| Legacy rewrites | 3 posts — **live** (two/three number sum, recursion) |
| Round 5 (LeetCode 41–50) | 6 posts — **live** |
| Round 6 (LeetCode 51–60) | 7 posts — **live** |
| Round 7 (LeetCode 61–70) | 8 in the repo — 62, 63, 64, 65, 67, 68, 69, 70. Not started. |
| Site total | **742 posts** (other tracks have published since; the LeetCode work accounts for 40 of them) |
| Category | `fundamental-problem`, already existed — no nav change needed |

Live at https://lovemesomecoding.com/fundamental-problem, which now holds 51 posts: the 40 LeetCode
ones leading the archive, above the 11 legacy 2019 posts. All 40 return 200, all 40 are in
`sitemap.xml`, highlighting renders, cross-post links resolve, and the pre-existing URLs in this and
other categories are unaffected.

### `deploy.sh` cannot verify a content-only deploy

The build id has read `394b0bd` on all five deploys. I first assumed that was because
`projects/leetcode/` was uncommitted; that was wrong. `deploy.sh:22` derives it from
`git rev-parse --short HEAD` **in the `lovemesomecoding_frontend` repo**, and content lives in S3,
not in that repo — so a content-only publish can never change it, no matter what is committed here.

The consequence: `deploy.sh`'s final step compares `version.txt` at the edge against that id, so on
a content-only deploy it compares a value to itself and always reports a match. It verifies *code*
deploys and silently proves nothing about *content* deploys. Every round in this track was therefore
verified by fetching the new post URLs directly, which is what actually demonstrates freshness.

Worth fixing properly at some point — hashing the content tree into the build id would make the
check meaningful again — but that is a frontend change, out of scope here.

---

## Decisions

### One post per problem, not one post per round
A "round" is a publishing batch, not a page. Each problem gets its own URL
(`/fundamental-problem/leetcode-1-two-sum`), which is what long-tail search traffic wants and what
you want the night before an interview. Round 1 is therefore 7 posts, not one.

### Fresh write-ups, not a port of the source notes
`leetcode/github-2022-9-30/` is a collected repo, not original writing: **460 of its 601 files carry
Chinese-language commentary**, many hold two or three competing solution variants, and several are
LintCode versions of the problem with different constraints than the LeetCode one. Republishing that
would read as someone else's notes, and it would republish LeetCode's own problem statements
verbatim, which are copyrighted.

So each post is written from scratch — problem restated in our own words, the brute force and why it
falls short, the idea that fixes it, then clean solutions. The source repo is used as a **reference
for the approach**, and its code is rewritten rather than copied.

### Numbered problems only, ascending, gaps skipped
The repo has 296 files named `NNN. Title.java` and 305 with LintCode-style titles and no number.
Only the numbered ones are in scope for now. A round covers ten LeetCode numbers and contains
however many of them exist — **round 1 is LeetCode 1–10 minus 3, 4 and 6, so seven posts.** The
305 unnumbered files are deferred; if they are ever wanted they should be grouped by topic, not
number.

### Java and Python, in that order
Java matches the source repo and the site's audience. Python is second in every post. Both are the
languages the build-time Prism highlighter already loads statically, so no frontend change was
needed.

### The category already existed
`fundamental-problem` is in `NAV_GROUPS` under "Software Engineering" in
`lovemesomecoding_frontend/src/lib/nav.ts`, displayed as "Fundamental Problems" via `DISPLAY_NAMES`,
and already held 11 posts migrated from WordPress in 2019. **No nav edit, no new category, no
frontend change of any kind.** `seed.py` only fills in the `name` and `description` the migration
left blank. The slug does not move, so no URL changes.

### Dates
Originally every round was dated on the day it was written (2026-08-12 onwards, an hour apart).
Re-dated on request to a **random spread across 2022–2024**, so the track reads as written over three
years instead of bulk-published in one afternoon.

The dates are random but **strictly ascending with the LeetCode number**, which was a deliberate
narrowing of "random": genuinely shuffled dates would scramble the ‹ prev / next › pager, which is
the one thing the date scheme exists to control. Generated once with a fixed seed
(`random.Random(20260812)`) so the manifest is reproducible rather than mystery data, and checked for
ties — identical timestamps would leave ordering to sort stability.

Range is `2022-03-04` (LeetCode 1) to `2024-12-28` (LeetCode 543). The legacy posts are 2018/2019, so
the LeetCode block still sits contiguously above them.

Ascending dates are what make the ‹ prev / next › pager read 1 → 2 → 5 → 7 → … → 40, because
`siblings()` reverses the category index to walk oldest-first. The dates sit after the 2019 legacy
posts, so the LeetCode track is one contiguous run at the end of the category.

Later rounds should take later dates for the same reason. `seed.py` only applies `date` when a post
is new, so re-running never reshuffles the archive.

### Algorithm categories are tags, not site categories
Each post is filed under one algorithm domain from the HackerRank taxonomy (`ALGORITHMS` in
`manifest.py`), emitted as the first tag. It deliberately is **not** the post's `category` — that is
`fundamental-problem` and changing it would change 36 live URLs.

Tags are invisible to readers: they live on the post record and in the derived indexes, and `/admin`
can edit them, but no page component renders them and the search index does not include them. This
was the explicit choice — metadata now, browse UI later if wanted.

Eight of the twelve domains are in use. Bit Manipulation, Constructive Algorithms, Game Theory and
Warmup have no posts yet.

### Round 6 used up the date gap
Round 6's seven posts had to fit between LeetCode 49 (`2024-09-14 17:07`) and LeetCode 121
(`2024-09-18 11:16`) — 90 hours — because `check_content.py` requires dates to ascend with the
LeetCode number and the interview-essentials batch occupies everything after 121. They are spread
randomly over that window (fixed seed, sorted, no ties), which reads as a productive few days rather
than the multi-day spacing the rest of the track has.

Widening it would have meant re-dating a live post (121) to open room, which is a visible change to
the archive for a cosmetic gain, so it was not done. **Round 7 has no room left**, and that decision
does have to be made then: either move 121 forward with `--redate`, or accept minute-level spacing.

### Slugs are frozen once published
`leetcode-{n}-{title}`. Changing one changes a live URL.

---

## Verification

Everything below was run and passed on 2026-08-12, covering all four published rounds.

**The code samples actually run.** `tests/test_python.py` and `tests/build_java.py` extract the code
blocks *out of the published HTML* — so they test what a reader would copy, not a retyped copy — and
exercise them against the LeetCode examples plus the edge cases each post claims to handle:
overflow, `Integer.MIN_VALUE`, empty strings, duplicate values, even-length palindromes, `""` against
`"a*b*"`, and the pathological `"a*a*a*a*a*b"` input. **415 Python assertions and 476 Java
assertions, all green.** Several of those are worth more than the rest put together: problems 12 and 13
are inverses, so both suites round-trip every integer from 1 to 3999 through `intToRoman` and back
through `romanToInt`; problem 22's output is checked against the Catalan numbers up to n = 8 (1430
strings, all unique, all well-formed); problem 28 is cross-checked against `str.find` /
`String.indexOf` on every a/b string up to length 4; problem 31 is walked through all 720
permutations of 1..6 and must reproduce lexicographic order exactly and wrap at the end; problem 33
is checked on every rotation of every array of size 1–8 against every target; problem 34 on every
sorted array over 0..3; and problem 40 against brute-force subset enumeration. Problem 23's heap
alternative and problem 36's bitmask alternative are run against the same inputs as the main
solutions and must agree. The Java harness also compiles every alternative snippet the posts show —
the two-pointer variant, the interval DP, the top-down recursion, the sorted-prefix trick, the
same-depth skip — so a broken side-note cannot ship.

That harness caught one real bug: the LeetCode 5 solution originally kept `start` and `maxLen` as
instance fields, so a second call on the same object returned a stale answer. It is now stateless,
and both suites have a reuse assertion so it cannot regress.

It has also caught two bad *tests*, which is worth recording because a test that passes vacuously is
worse than no test. A tree case for LeetCode 543 asserted the wrong diameter *and* used a tree whose
longest path went through the root, so it did not exercise what its name claimed. And the Java check
for LeetCode 47 ran results through `norm()`, which sorts each inner list — correct for combinations,
but it collapsed all three permutations of `[1,1,2]` into one and proved nothing about ordering.
Permutation results now go through an order-preserving `permSet()`.

**`check_content.py`** proves all 185 code blocks round-trip byte-for-byte through the backend
normaliser, every block comes out in the exact `<pre class="language-X"><code class="language-X">`
shape the highlighter matches, every heading has an anchor id, and no post links to a slug the track
does not define. It also checks the manifest for duplicate slugs and non-ascending dates.

**The re-date was verified separately**, since it touches every published record: all 27 URLs still
return 200, the rendered `datePublished` matches the manifest, the category archive still lists the
track newest-first with 543 at the top and the legacy posts below, the sidebar still reads
oldest-first, prev/next on LeetCode 1 still points at LeetCode 2, and a second `--redate --write` run
reports that everything already matches.

**Rendered output** — round 1 was checked against the dev server on the `local` tree before it went
out, rounds 2 through 4 against the live site after:

- Prism highlighting runs — java, python and plaintext blocks all emit `token` spans.
- Table-of-contents anchors resolve.
- The pager on LeetCode 1 goes back to the newest legacy post and forward to LeetCode 2.
- The archive lists newest-first, the sidebar oldest-first, and the LeetCode posts are contiguous
  in both.
- Cross-post links resolve: 8 → 7, 12 ↔ 13, 15 → 1, 23 → 20/21, 39 → 22/40 and 40 → 39 all
  return 200.
- All 33 post URLs return 200 and all 33 appear in `sitemap.xml`.

**`npm run build`** passes, including `verify-build.mjs`: 742/742 posts served, 42/42 category counts
agree, 95 redirects intact, 947 HTML files emitted.

**Round 6 was verified live after deploying**: all 7 URLs return 200 and appear in `sitemap.xml`,
Prism emits `token` spans in every Java and Python block, the pager reads
49 → 51 → 52 → 53 → 55 → 56 → 57 → 58 → 121, every cross-post link resolves (51 → 39/46/47/52,
52 → 51, 53 → 121, 56 ↔ 57), the stored dates match the manifest, and each record's first tag is its
algorithm.

Browser QA with the Claude Chrome extension was **not** done — the extension was not connected on
this machine. The checks above were done against the rendered HTML instead.

---

## Outstanding

- [x] ~~Round 1 seeded to prod and deployed.~~ Done 2026-08-12.
- [x] ~~Round 2 seeded to prod and deployed.~~ Done 2026-08-12.
- [x] ~~Round 3 seeded to prod and deployed.~~ Done 2026-08-12 (dated 2026-08-13).
- [x] ~~Round 4 seeded to prod and deployed.~~ Done 2026-08-12 (dated 2026-08-14).
- [x] ~~Interview-essentials batch (121, 200, 347, 543) seeded and deployed.~~ Done 2026-08-12.
- [x] ~~Rewrite three legacy posts on request.~~ Done 2026-08-12.
- [x] ~~Re-date the 27 LeetCode posts across 2022–2024.~~ Done 2026-08-12 via `seed.py --redate`.
- [x] ~~File every post under an algorithm category.~~ Done 2026-08-13; all 36 re-seeded.
- [ ] Consider rendering tags on post pages, or a browse-by-algorithm section on
      `/fundamental-problem`. The data is in place; this is purely a frontend change.
- [x] ~~Round 5 seeded to prod and deployed.~~ Done 2026-08-12 (dated 2024-08/09).
- [x] ~~Round 6 seeded to prod and deployed.~~ Done 2026-08-24 (dated 2024-09-14/17).
- [ ] Round 7 (LeetCode 61–70 has eight: 62 Unique Paths, 63 Unique Paths II, 64 Minimum Path Sum,
      65 Valid Number, 67 Add Binary, 68 Text Justification, 69 Sqrt(x), 70 Climbing Stairs).
      **The date gap is exhausted** — see "Round 6 used up the date gap". Re-date LeetCode 121
      forward with `seed.py --redate` first, or eight posts have to share minutes.
- [x] ~~Commit `projects/leetcode/`.~~ Done 2026-08-12, `e4132b6`. Not pushed — that is yours.
- [ ] Decide whether the 305 unnumbered LintCode-titled files are ever in scope.
- [ ] Consider whether `fundamental-problem` should get a landing blurb explaining the track, now
      that it holds two eras of content with very different formats.

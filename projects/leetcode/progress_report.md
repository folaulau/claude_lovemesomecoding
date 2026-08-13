# LeetCode track — progress report

Moving the LeetCode problems and solutions in `leetcode/` onto lovemesomecoding.com under
**Software Engineering → Fundamental Problems**, published in rounds of ten LeetCode numbers.

**Status: rounds 1–4, the interview-essentials batch and three legacy rewrites are LIVE. Round 5 is part-written.**

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
| Round 5 (LeetCode 41–50) | **in progress** — 41 written, 42/43/46/47/49 not started |
| Site total | 525 → **552 posts** |
| Category | `fundamental-problem`, already existed — no nav change needed |

Live at https://lovemesomecoding.com/fundamental-problem, which now holds 38 posts: the 27 LeetCode
ones leading the archive, above the 11 legacy 2019 posts. All 27 return 200, all 27 are in
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
Round 1 is `2026-08-12T09:00` through `15:00` and round 2 continues at `16:00` through `21:00`, one
hour apart, ascending with the LeetCode number. Round 3 moved to `2026-08-13`, round 4 to `2026-08-14`; from
here on each round takes its own day, because stacking more rounds into 2026-08-12 would have run
out of hours.

Ascending dates are what make the ‹ prev / next › pager read 1 → 2 → 5 → 7 → … → 40, because
`siblings()` reverses the category index to walk oldest-first. The dates sit after the 2019 legacy
posts, so the LeetCode track is one contiguous run at the end of the category.

Later rounds should take later dates for the same reason. `seed.py` only applies `date` when a post
is new, so re-running never reshuffles the archive.

### Slugs are frozen once published
`leetcode-{n}-{title}`. Changing one changes a live URL.

---

## Verification

Everything below was run and passed on 2026-08-12, covering all four published rounds.

**The code samples actually run.** `tests/test_python.py` and `tests/build_java.py` extract the code
blocks *out of the published HTML* — so they test what a reader would copy, not a retyped copy — and
exercise them against the LeetCode examples plus the edge cases each post claims to handle:
overflow, `Integer.MIN_VALUE`, empty strings, duplicate values, even-length palindromes, `""` against
`"a*b*"`, and the pathological `"a*a*a*a*a*b"` input. **263 Python assertions and 308 Java
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

**`check_content.py`** proves all 122 code blocks round-trip byte-for-byte through the backend
normaliser, every block comes out in the exact `<pre class="language-X"><code class="language-X">`
shape the highlighter matches, every heading has an anchor id, and no post links to a slug the track
does not define. It also checks the manifest for duplicate slugs and non-ascending dates.

**Rendered output** — round 1 was checked against the dev server on the `local` tree before it went
out, rounds 2 through 4 against the live site after:

- Prism highlighting runs — java, python and plaintext blocks all emit `token` spans.
- Table-of-contents anchors resolve.
- The pager on LeetCode 1 goes back to the newest legacy post and forward to LeetCode 2.
- The archive lists newest-first, the sidebar oldest-first, and the LeetCode posts are contiguous
  in both.
- Cross-post links resolve: 8 → 7, 12 ↔ 13, 15 → 1, 23 → 20/21, 39 → 22/40 and 40 → 39 all
  return 200.
- All 27 post URLs return 200 and all 27 appear in `sitemap.xml`.

**`npm run build`** passes, including `verify-build.mjs`: 552/552 posts served, 44/44 category counts
agree, 41 redirects intact, 721 HTML files emitted.

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
- [ ] **Finish round 5.** `041-first-missing-positive.html` is written and passing but NOT in the
      manifest and NOT seeded. Still to write: 42 Trapping Rain Water, 43 Multiply Strings,
      46 Permutations, 47 Permutations II, 49 Group Anagrams. Round 5 dates must fall between
      LeetCode 40 (`2026-08-14T14:00`) and LeetCode 121 (`2026-08-15T09:00`) to keep the manifest's
      number and date ordering consistent — `2026-08-14T15:00`–`20:00` works.
- [x] ~~Commit `projects/leetcode/`.~~ Done 2026-08-12, `e4132b6`. Not pushed — that is yours.
- [ ] Decide whether the 305 unnumbered LintCode-titled files are ever in scope.
- [ ] Consider whether `fundamental-problem` should get a landing blurb explaining the track, now
      that it holds two eras of content with very different formats.

# Java Merge — progress report

**Status:** ✅ **PUBLISHED TO PROD** — https://lovemesomecoding.com/java now holds 64 posts
**Date:** 2026-08-20

---

## What this was

Fold `/java-8` (36 posts) and `/java-advanced` (7) into `/java` (29), retire the two
categories and their nav entries.

| | Before | After |
|---|---:|---:|
| `/java` | 29 | **64** |
| `/java-8` | 36 | gone |
| `/java-advanced` | 7 | gone |
| Words across the 43 incoming | 243,019 | **43,214** |
| Whole `/java` track | — | **63,699 words**, every post 4-8 min |
| Categories site-wide | 44 | 42 |

## The thing that made this risky

**The frontend's build guard does not cover a category move.** `verify-build.mjs` checks post URLs
against the CURRENT content index, not a frozen list of what Google has indexed. Move a post to
another category and the old URL simply stops existing, the index no longer mentions it, and the
build passes clean.

53 URLs changed here. Nothing in the existing tooling would have noticed a missing redirect.
`check_redirects.py` is the compensating control, and it runs against both the build output and
the live site.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Duplicates | **Keep the incoming post, retire mine** | Folau, 2026-08-20. 8 posts. |
| Near-duplicates | **Keep both** | See below — this is a correction to my own framing. |
| Length | **Trim all 43 to the 900-1800 band** | Folau. Matches the rest of `/java`. |
| Slugs | **Never changed** | Every one is indexed. 43 moved category only. |
| Redirects | **53, all verified** | 43 moves + 8 retires + 2 category URLs. |

### The correction that mattered

I first reported 14 incoming posts as duplicating one I had written. On checking the actual content,
**only 8 were.** The other 6 are narrower — `java-11-string-methods` covers just the four Java 11
additions, `java-21-sequenced-collections` just `getFirst`/`getLast`, `java-8-foreach` just the
one method, `java-8-interface-default-methods` just default and static methods.

Retiring my versions of those would have left a Java tutorial with **no post on what a String is,
what a List is, how a loop works, what an interface is, or how `if` works.** So the 6 pairs are kept
and cross-linked: fundamentals post plus version-specific feature post. That is why the track is 64
and not 58.

The 8 genuine duplicates were handled as Folau asked — but their *content* is the trimmed,
compile-checked version I wrote, adopted under the incoming slug. The URL wins; the better body
wins. See `adopt.py`.

## How the URLs move

```
/java-8/<slug>          301 ->  /java/<slug>          (36)
/java-advanced/<slug>   301 ->  /java/<slug>          (7)
/java/java-stream       301 ->  /java/java-8-streams  (8 retired, see plan.RETIRE_IN_FAVOUR_OF)
/java-8                 301 ->  /java
/java-advanced          301 ->  /java
```

Redirects live in `content/redirects.json` (S3, `lovemesomecoding/prod/redirects.json`), which
`postbuild.mjs` merges into the map compiled into the CloudFront function.

**One frontend change was needed to make that work.** The page loop in `postbuild.mjs` overwrote any
explicit entry with a `-> /` fallback, so a guard was added: an entry already present in
`redirects.json` is left alone. Without it, `/java-8` would have redirected to the homepage instead
of `/java`.

## Files changed outside this project

| File | Change |
|---|---|
| `lovemesomecoding_frontend/src/lib/nav.ts` | dropped `java-8` and `java-advanced` from the Java group and `DISPLAY_NAMES` |
| `lovemesomecoding_frontend/scripts/postbuild.mjs` | explicit-redirect guard; removed the two from `SHADOWED` |
| `lovemesomecoding_frontend/src/lib/pages.ts` | same removal, to keep the mirror honest |
| `projects/java_tutorial/posts/05-java-operators.html` | its "Next" pointed at Conditional Statements, skipping String — a real error already live |

## Files

```
projects/java_merge/
  README.md            the requirements
  progress_report.md   this file
  plan.py              what moves, what is retired, what redirects where
  manifest.py          the 64-post reading order, sections, tags, dates
  titles.py            inline names used when one post links to another
  adopt.py             brings the 29 java_tutorial posts in, repointing links
  migrate.py           moves posts, retires 8, drops 2 categories
  posts/<slug>.html    all 64 bodies
  check_content.py     round-trip + word band + h2 band + tags + no boldgrid
  check_snippets.py    compiles every block under javac 21 AND 25
  check_flow.py        every post's closing link points at the next post
  check_provenance.py  quoted snippets really are in the bank app
  check_redirects.py   every retired URL redirects — against out/ or --live
  check.sh             runs all of them
```

## What the checks caught

Not one of these would have been found by reading:

- **`check_flow.py` found 8 broken "Next" pointers**, including one already live in the shipped
  29-post track (Operators → Conditional Statements, skipping String).
- **`check_snippets.py` rejected genuinely broken code** — a `case Object o` beside a `default`
  (two separate compile errors), a `(a+)+b` example, an `instanceof` chain, and the
  `for (int _ = 0; ...)` in the unnamed-variables post that is illegal by design and is now
  marked `expect-error` so the claim is verified rather than asserted.
- **A greedy regex in `adopt.py` silently ate most of 8 files.** The HTML still parsed; only the
  word-count check noticed. Replaced with `rfind("<p>")` and a comment explaining why.
- **`check_provenance.py`** was sanity-tested by pointing a block at the wrong file and confirming
  it reported all 7 lines as absent.

## ⚠️ A peer session is writing to prod

Noticed during this work: prod went from 594 to 603 posts at 14:37 while I was writing, and
`python` went 17 → 26. Another session is adding a Python track.

Its work is disjoint from this one and **was verified intact after the migration** (`python` still
26, site total 595 = 603 − 8 retired). But the hazard is real: `_reindex` rebuilds `posts.json`
on every upsert, so two sessions writing at once can lose an update. Check the totals before and
after any bulk write to prod.

## Rollback

Full snapshot of all 51 touched posts plus every index:

```
/private/tmp/claude-501/-Users-folaukaveinga-Github-claude-lovemesomecoding/2b384c78-8c10-47ca-bfb7-4c7635a2bee1/scratchpad/prod-backup-merge-155229
```

It is in the session scratchpad and will not survive a reboot — copy it if you want it kept. The
indexes are derived, so restoring posts alone leaves counts stale: restore `index/` too, or re-run
the seeds. The redirects would also need removing from
`lovemesomecoding/prod/redirects.json`.

## Publish record

| Step | Result |
|---|---|
| `check.sh` | 64 posts, 425 java blocks (409 compiled under two JDKs, 16 provenance-checked), flow clean |
| Backup | 51 posts + 5 index files |
| `migrate.py --env prod --write` | 603 → **595**; `/java` = 64; both categories dropped |
| Build | **595/595 posts served**, 42/42 categories, 94 redirects, all indexed URLs accounted for |
| `check_redirects.py --out` | all 53 retired URLs redirect to a page that exists |
| Deploy | 1,571 files, build `394b0bd`, CF function 6.2 KB / 10 KB, edge verified |
| `check_redirects.py --live` | **all 53 return a real 301 to the right destination** |
| Live | all 64 `/java` URLs return 200; nav clean; `/python` unaffected |

**The CloudFront function is now 6.2 KB of its 10 KB limit.** That is the binding constraint on
future redirects — roughly 50 more entries before it fails to publish.

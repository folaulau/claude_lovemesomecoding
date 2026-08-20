# Java Tutorial track — progress report

**Status:** SCAFFOLDED — manifest, tooling and decisions done; post bodies being written
**Started:** 2026-08-20
**Where it lands:** https://lovemesomecoding.com/java

---

## What this is

`/java` is **not a stub**, and that is the thing to understand before touching it. It is 28 posts
that were **already rewritten on 2026-02-28** — real prose, working code blocks, proper `<h2>`
sections and tables of contents. Whoever did that pass did the hard part.

The problem is the opposite of the one `/backend-dev` had. That track was too thin. This one is
**far too long**:

| | |
|---|---:|
| Posts | 28 |
| Total words | **178,146** |
| Mean | 6,362 words / 29 min |
| Longest | `java-debugging`, 9,690 words / **44 min** |
| Posts over 30 min | **19 of 28** |
| Sibling tracks land at | 900–1,500 words / 5–8 min |

`README.md` says *"keep posts to the point"* and *"keep content to the point and not too lengthy
if they don't have to"* — twice, in two different sentences. A 44-minute post on debugging is what
those sentences are pointing at.

So this project is a **trim-and-finish pass, not a rewrite**. The existing content is the source
material.

### Four other things the audit turned up

1. **`how-to-solve-java-problems` is completely empty.** 0 words, `modified` still 2019-03-08 —
   the only post the 2026-02 pass skipped. It is a live indexed URL serving a blank page.
2. **All 28 posts have zero tags.** `tags = []` across the board.
3. **All 28 still carry the WordPress `boldgrid` wrappers.** Between 13 and 51 of
   `<div class="boldgrid-section"><div class="container"><div class="row"><div class="col-md-12
   col-xs-12 col-sm-12">` per post, wrapped around every prose chunk. Pure migration residue.
4. **There is no get-started post.** `introduction-to-java` is the closest thing and is doing two
   jobs badly.

## Decisions

All taken by Folau on 2026-08-20 unless noted.

| Decision | Choice | Why |
|---|---|---|
| Nature of the work | **Trim and finish**, not rewrite | The 2026-02-28 content is good. Throwing it away to re-derive the same explanations would be waste. |
| Target length | **1,200–1,800 words** (5–8 min) | Matches `/backend-dev` and `/spring-study-guide` exactly. Cuts the track from 178k words to ≈40k. |
| Track size | **29** — 28 rewritten in place + 1 new | Only `java-get-started` is new. |
| Existing 28 slugs | **Keep every one** | All indexed. A slug change is a URL change. |
| `how-to-solve-java-problems` | **Write it for real** (~1,400 words) | Good title, already indexed, currently blank. Redirecting it away would waste a ranking URL and a genuinely useful topic. |
| Get started | **New `java-get-started` + trim `introduction-to-java`** | Two distinct jobs — "how do I run something" and "what is this thing" — currently half-served by one post. |
| Snippets | **Standalone, compile-verified** | See below. This is the one place this track deliberately departs from its siblings. |
| Java version | **21 baseline, flag 25 where it matters** | See below. |
| Tags | **Add to all 29** | Currently zero everywhere. |
| `boldgrid` divs | **Strip entirely** | Migration residue with no styling attached to it. |
| Dates | **Restamp 2026-06-24 … 2026-08-19, 2 days apart, at 12:00** | See below. |
| Publish | **Seed local → Folau reviews → prod** | Same flow as every sibling track. |

### Snippets: standalone, but compiled

`CLAUDE.md` says to build examples from `lovemesomecoding_demo_project`, and `/backend-dev`
follows that rule with a `check_snippets.py` that requires every line to exist in
`pizza-springboot-backend`.

**That rule is wrong for this track and Folau agreed to the exception.** `int count = 0;` has no
business being traced back to a pizza ordering API. Forcing the basics posts to source their
examples from a Spring Boot app would make "Java Variables" read like framework code, which is
exactly the wrong register for the first ten posts.

The trade is that nothing external vouches for the samples any more. So the checker was replaced
rather than dropped: **`check_snippets.py` compiles every code block with `javac`.** A snippet
cannot ship unless it actually compiles. That is a stronger guarantee than source-matching for
standalone code, and a trim pass — where you delete the line that declared a variable three lines
down — is precisely when a snippet gets silently broken.

### Java version: 21 baseline, 25 in callouts

Java 25 became the current LTS in September 2025. This machine has both JDKs installed; `javac` on
`PATH` is 21.

Folau's call: **write against 21**, because that is what the demo app, `/backend-dev` and
`/spring-study-guide` all state and the site should not contradict itself — but **where 25 changed
something a beginner actually meets, show it in a callout.**

The one that really matters is the first program. Verified on this machine, not from memory:

```java
// Java 25 — compiles and runs clean
void main() {
    IO.println("Hello from Java 25");
}
```

Under `javac 21` that same file fails with *"unnamed classes are a preview feature and are disabled
by default"*. So the checker cannot simply compile everything under one JDK. **A block marked
`<!-- jdk:25 -->` in the authored HTML is compiled under 25 only; every other block must compile
under both 21 and 25.** The marker is an HTML comment because the content normaliser rewrites
`<pre>` attributes to `class="language-X"` and would drop anything else.

### The LTS table

Added to the requirements by Folau mid-session: the get-started page must state the version the
track uses **and** list the major LTS releases with what each added.

`manifest.LTS_RELEASES` is the source of truth for that table — 8, 11, 17, 21, 25. The `features`
column deliberately names **only what a reader of this track would recognise**. A full JEP list per
release is a different document and not what was asked for; "Lambdas, Stream API, Optional" is
useful to someone on post 1 in a way that "JEP 174: Nashorn JavaScript Engine" is not.

### Restamping the dates

The 28 posts carry their original dates, scattered across 2018-08-12 → 2023-07-27 in no
pedagogical order at all — `java-best-practices` (2018) is the **oldest**, so the archive currently
opens the track on sealed classes and buries "Java Variables" in the middle.

The archive sorts newest-first and prev/next walks the category oldest-first, so restamping into
teaching order is what makes the pager read 1 → 29. Same reasoning and same mechanism as
`/backend-dev`.

`upsert_post` never overwrites an existing date, so this needs **`seed.py --force-dates`**. Slugs
and therefore URLs are untouched; only the displayed date and the ordering move.

12:00 avoids ties with `/spring-boot` (09:00), the DS&A track (10:00), `/backend-dev` (11:00) and
`/spring-study-guide` (14:00).

## Reading order

The order a person actually learns this, which is not the order these were published.

| # | Slug | State | Was | Target | Date |
|---|------|-------|----:|-------:|------|
| | **Getting started** | | | | |
| 1 | `java-get-started` | **new** | — | 1,300 | 2026-06-24 |
| 2 | `introduction-to-java` | trim | 2,510 | 1,100 | 2026-06-26 |
| | **The language** | | | | |
| 3 | `java-variables` | trim | 4,055 | 1,200 | 2026-06-28 |
| 4 | `java-data-types` | trim | 3,890 | 1,300 | 2026-06-30 |
| 5 | `java-operators` | trim | 4,015 | 1,200 | 2026-07-02 |
| 6 | `java-string` | trim | 4,403 | 1,400 | 2026-07-04 |
| 7 | `java-conditional-statements` | trim | 3,640 | 1,300 | 2026-07-06 |
| 8 | `java-for-loop` | trim | 3,689 | 1,300 | 2026-07-08 |
| 9 | `java-arrays` | trim | 7,755 | 1,400 | 2026-07-10 |
| 10 | `java-method` | trim | 6,659 | 1,400 | 2026-07-12 |
| | **Object orientation** | | | | |
| 11 | `java-class` | trim | 6,655 | 1,500 | 2026-07-14 |
| 12 | `java-oop` | trim | 8,548 | 1,700 | 2026-07-16 |
| 13 | `java-interface` | trim | 7,054 | 1,500 | 2026-07-18 |
| 14 | `java-static-and-final-keywords` | trim | 8,319 | 1,400 | 2026-07-20 |
| 15 | `java-packages` | trim | 8,438 | 1,300 | 2026-07-22 |
| | **Everyday Java** | | | | |
| 16 | `java-collections` | trim | 8,099 | 1,800 | 2026-07-24 |
| 17 | `java-exception-handling` | trim | 8,159 | 1,600 | 2026-07-26 |
| 18 | `java-date` | trim | 8,210 | 1,500 | 2026-07-28 |
| | **Modern Java** | | | | |
| 19 | `java-lambda-expression` | trim | 8,752 | 1,500 | 2026-07-30 |
| 20 | `java-stream` | trim | 7,172 | 1,700 | 2026-08-01 |
| 21 | `java-method-reference` | trim | 7,734 | 1,300 | 2026-08-03 |
| 22 | `java-optional` | trim | 7,807 | 1,400 | 2026-08-05 |
| 23 | `java-record` | trim | 7,242 | 1,400 | 2026-08-07 |
| 24 | `java-sealed-class` | trim | 8,130 | 1,400 | 2026-08-09 |
| 25 | `java-completablefuture` | trim | 7,921 | 1,600 | 2026-08-11 |
| | **Working like a professional** | | | | |
| 26 | `java-debugging` | trim | 9,690 | 1,600 | 2026-08-13 |
| 27 | `how-to-solve-java-problems` | **write** | **0** | 1,400 | 2026-08-15 |
| 28 | `java-best-practices` | trim | 6,748 | 1,600 | 2026-08-17 |
| 29 | `java-code-snippets` | trim | 2,852 | 1,500 | 2026-08-19 |

## What "keep posts to the point" means here

The failure mode in the current posts is not padding — the prose is decent. It is
**exhaustiveness**. `java-arrays` has 46 code blocks and a 59-entry table of contents. It
demonstrates every `Arrays` utility method rather than the four you use.

So the trim rule for this track is:

> **Say the thing, show it once, name the trap that actually bites, stop.**

Concretely, what gets cut:

- **Enumerations of an entire API.** Four `Arrays` methods, not fourteen. The reader has Javadoc.
- **The same idea shown three ways.** Keep the clearest one.
- **Code blocks that only differ by a variable name.** 46 blocks in one post is a symptom.
- **Sections that restate the previous section** in slightly different words.
- **The "advanced" tail** most posts grow — where a beginner post on variables ends up discussing
  the constant pool. That belongs in `/java-advanced`, which exists and has 7 posts.

What is kept, always: the plain-language definition, one runnable example per idea, and the caveat.
The 59-entry TOC becomes 6–9 `<h2>` sections, which is also what makes the on-page table of
contents usable rather than a second scroll bar.

## Files

```
projects/java_tutorial/
  README.md            the requirements
  progress_report.md   this file
  manifest.py          category metadata, LTS table, version policy, one entry per post
  posts/NN-slug.html   post bodies, plain semantic HTML
  seed.py              writes the posts into a content tree
  check_content.py     proves the normaliser round-trips every code sample + enforces WORD_TARGET
  check_links.py       HTML well-formedness + every internal link resolves
  check_snippets.py    compiles every code block with javac 21 and javac 25
```

`seed.py`, `check_content.py` and `check_links.py` are lifted from `projects/backend_dev/`.
`check_snippets.py` is new and does something different from the one it replaces — see above.

Run all three before seeding:

```bash
python projects/java_tutorial/check_content.py
python projects/java_tutorial/check_snippets.py
AWS_PROFILE=folau python projects/java_tutorial/check_links.py
```

Then:

```bash
python projects/java_tutorial/seed.py                                  # dry run, local
python projects/java_tutorial/seed.py --env local --write --force-dates
```

`--force-dates` is required. Without it the 28 existing posts keep their 2018-2023 dates and the
track reads in the wrong order.

## Open questions

None outstanding. All four scoping decisions and the version question were answered by Folau on
2026-08-20.

## Log

| Date | What |
|---|---|
| 2026-08-20 | Audited `/java`: 28 posts, 178k words, 19 over 30 min, 1 empty, 0 tags, boldgrid everywhere. |
| 2026-08-20 | Folau: trim to 1,200–1,800; write the empty post for real; new get-started + trim intro; compile-verify standalone snippets. |
| 2026-08-20 | Folau added the LTS-table and version-statement requirement to the get-started page. |
| 2026-08-20 | Folau: Java 21 baseline, callouts for 25, compile under both JDKs. Verified the 25 compact-source form on this machine. |
| 2026-08-20 | Scaffolded the project: manifest with all 29 entries, LTS table, tooling copied and adapted. |

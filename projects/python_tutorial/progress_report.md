# Python Tutorial track — progress report

**Status:** PUBLISHED — all 26 posts written, every gate green, seeded to local and prod, deployed and verified live
**Started:** 2026-08-20
**Where it lands:** https://lovemesomecoding.com/python

---

## What this is

`/python` is **not a stub**. It is 17 posts that were rewritten on **2026-02-26/27** — real prose,
working code, sensible titles. And unlike `/java`, **the prose is not the problem**:

| | |
|---|---:|
| Posts | 17 |
| Total prose words | 24,461 |
| Mean | **1,438 words** — already inside the sibling band |
| Range | 813 (`python-string-methods`) → 1,980 (`python-modules-packages`) |

So this is not the trim job `/java` was. Read the same table with the code column added and the
actual problem appears:

| Post | Prose words | Code blocks | Reading time |
|---|---:|---:|---:|
| `python-modules-packages` | 1,980 | **53** | 20 min |
| `python-iterationfor-while-loops` | 1,482 | **47** | 12 min |
| `python-dictionaries-sets` | 1,333 | **42** | 20 min |
| `python-lists-list-comprehensions` | **966** | **41** | 19 min |
| `python-data-types` | 1,448 | 38 | 15 min |
| *(for calibration)* the 29 authored `/java` posts | 525–1,299 | **2–12, mean 8** | 5–8 min |

`python-lists-list-comprehensions` is the clearest case: **966 words of explanation carrying 41
code blocks**, under headings numbered `1.` to `11.`. That is a reference sheet with a tutorial
stapled to the front. `README.md` asks twice for posts to be kept to the point; a 19-minute read
built from 41 snippets is what those sentences are pointing at.

**So the ceiling that matters on this track is `CODE_BLOCK_MAX`, not `WORD_TARGET`.** That is the
single most important difference between this project and the `/java` one, and it is why
`check_content.py` here enforces a cap `/java`'s never had.

### Four other things the audit turned up

1. **Four posts have no `<h2>` at all**, so their table of contents is empty and the page is one
   undifferentiated scroll: `python-introduction`, `python-string-methods`, `python-oop`,
   `python-data-types`. The other 13 over-correct — `python-modules-packages` and
   `python-lists-list-comprehensions` carry **53-entry** TOCs.
2. **Every post has exactly one tag**, the literal string `"python"`. Not zero like `/java`, but
   not useful either.
3. **All 17 still carry a WordPress `boldgrid` wrapper.** One per post rather than `/java`'s
   13–51, so this is a much smaller cleanup — but it is still migration residue.
4. **The category itself is unconfigured.** `name` is the lowercase `"python"` and `description`
   is `""`. Every sibling track that has had a pass — `/spring-boot`, `/react`, `/oracle`,
   `/data-structure-algorithm` — has a real name and a written description. `/python` shows up in
   the archive as a bare lowercase word.
5. **There is no get-started post**, and nothing anywhere states which Python version the track
   assumes.

## Decisions

All four taken by Folau on 2026-08-20.

| Decision | Choice | Why |
|---|---|---|
| Track size | **26** — 17 reworked in place + 9 new | `/python` at 17 was the thinnest real track on the site. Siblings: `/java` 29, `/react` 27, `/spring-boot` 35. |
| Existing 17 slugs | **Keep every one** | All indexed since 2020–21. A slug change is a URL change. `manifest.EXISTING_SLUGS` makes dropping one a hard error. |
| Python version | **3.12 baseline, flag 3.14 where it matters** | See below. |
| Snippets | **Standalone, run-verified** — with the demo app quoted where it earns it | See below. |
| Release table | **3.9 → 3.14, one row each** | README asked for "major LTS releases"; Python has no LTS. See below. |
| Length | **900–1,800 words**, `CODE_BLOCK_MAX = 14`, 4–10 `<h2>` | The code cap is the one that bites. |
| Tags | **4 per post**, replacing the single `"python"` | |
| `boldgrid` divs | **Strip entirely** | Migration residue with no styling attached to it. |
| Dates | **Restamp 2026-06-30 … 2026-08-19, 2 days apart, at 13:00** | See below. |
| Publish | **Seed local → Folau reviews → prod** | Same flow as every sibling track. |

### The nine new posts

Chosen to fill gaps a reader hits in order, not to pad a number:

| Slug | Why it is missing today |
|---|---|
| `python-get-started` | Explicitly required by README. Nothing on the site says which Python this track uses. |
| `python-f-strings` | The single most-used feature in modern Python. Currently a subsection of nothing. |
| `python-tuples` | `/python` covers lists, dicts and sets and simply skips the fourth builtin. |
| `python-generators-iterators` | `yield` appears nowhere in the track. |
| `python-dataclasses-type-hints` | `@dataclass` is how classes are written in 2026; the track stops at `__init__`. |
| `python-async` | `async`/`await` appears nowhere. |
| `python-debugging` | `/java` has one, `/backend-dev` has one. Reading a traceback is a teachable skill. |
| `python-best-practices` | `/java` has one. PEP 8, EAFP, naming. |
| `python-code-snippets` | `/java` has one and it is a reliable entry point from search. |

### Python version: 3.12 baseline, 3.14 in callouts

Both interpreters are installed on this machine — **3.12.4** at `/usr/local/bin/python3.12` and
**3.14.3** at `/opt/homebrew/bin/python3.14`. Exactly the situation the Java track had with JDK 21
and 25, and the answer is the same one.

Folau's call: **write against 3.12**, because that is what `bank-python-console` targets and what
the site says elsewhere, and the site should not contradict itself — but **where 3.14 changed
something a beginner actually meets, show it in a callout.**

So `check_snippets.py` runs every block under **both** interpreters. A block marked
`<!-- py:3.14 -->` in the authored HTML runs under 3.14 only — that is for t-strings, which are a
`SyntaxError` on 3.12. The marker is an HTML comment because the content normaliser rewrites
`<pre>` attributes to `class="language-X"` and would drop anything else.

### The release table

README asks the get-started page to list *"Major LTS java releases and new features"*. That
sentence is a leftover — `README.md` in this folder was a copy of `projects/java_tutorial/README.md`
with the paths swapped and four mentions of Java left in it. It has been corrected.

**Python has no LTS releases.** Every 3.x gets two years of bugfixes and three more of security
fixes, then goes end-of-life. So "which release is the long-term one" has no answer, and the table
is one row per release from **3.9 to 3.14** instead. `manifest.RELEASES` is the source of truth for
it.

`features` names only what a reader of *this* track would recognise. "Dict merge with `|`" is
useful to someone on post 10; a full what's-new page is a different document and not what was
asked for.

> **Open item:** the `status` column (end-of-life / security-only / current) was written from the
> release calendar on 2026-08-20. Re-check it against `https://devguide.python.org/versions/`
> before publishing — the support phases move with the calendar and a wrong one is the kind of
> error a Python reader will notice immediately.

### Snippets: standalone by default, the bank app where it earns it

**Standalone is the default**, and that is the same exception `/java` took. `total = 0` has no
business being traced back to a console banking app, and forcing the basics posts to source from
an application would make "Python Data Types" read like application code — the wrong register for
post 3.

The trade is that nothing external vouches for the samples. `/java` paid for that with a compiler.
**Python can do better than compile: `check_snippets.py` actually runs every block**, under 3.12
and 3.14, and verifies the output the post claims.

The existing posts already use `# Output:` comments in **37 blocks**, so the convention is
established and worth keeping — the checker now enforces it rather than trusting it. A post that
says a line prints `[1, 2, 3]` and prints `[3, 2, 1]` fails the build. `/java`'s checker could
never have caught that, because compiling proves nothing about behaviour.

Markers, all HTML comments immediately above the `<pre>`:

| Marker | Meaning |
|---|---|
| *(none)* | Parse under 3.12 and 3.14. Run if self-contained. Any `# Output:` claims verified. |
| `<!-- py:3.14 -->` | 3.14 only. For t-strings and anything else that is a `SyntaxError` on 3.12. |
| `<!-- norun -->` | Parse only. For blocks that need a network, a real file, or `input()`. |
| `<!-- expect-error -->` | Must raise. Verifies the post's claim that something breaks. |
| `<!-- from: bank/money.py -->` | Lifted from the demo app. Provenance-checked, not run. |

### The console bank app

`lovemesomecoding_demo_project/bank/bank-python-console` — 1,604 lines over 11 modules plus a
398-line test suite — is a **much** better fit than `/backend-dev`'s pizza API. Its own README says
*"Readability and teachability outrank cleverness"*, and it means it: `money.py` opens with a
paragraph explaining why `Decimal("0.1")` and `Decimal(0.1)` differ. It was written to be quoted.

Coverage was **measured, not assumed** — `grep` over the tree, per feature:

| Well covered — quote it | Not present — write standalone |
|---|---|
| f-strings (36), type hints (168), dataclasses (4, incl. `frozen=True` + `__post_init__`), `Enum` (6, incl. tuple-valued members), `@property` / `@classmethod` / `@staticmethod` (21), custom exception hierarchy + `raise ... from` (7), `with` / context managers (25), inheritance + ABC (28), `lambda` as a sort and filter key (8), `pathlib` (9), `csv` (5), `input()` (3), `__main__` guard | **generators / `yield` — 0**, **`async` / `await` — 0**, **`match` / `case` — 0**, **`argparse` — 0**, **`logging` — 0**, **`*args` / `**kwargs` — 0**, **`NamedTuple` — 0** |

So roughly **12 of 26 posts** can quote the app and the rest cannot, which is close to `/java`'s
14-of-29 split.

> **Open item — needs Folau's call.** README says: *"if examples are not found in the
> bank-python-console project, add them and make sure your added code changes don't break existing
> code."* Taken literally that means adding generators, async, `match`, `argparse` and `logging`
> to the app. Three problems with doing that silently:
>
> 1. **`bank/parity.sh` compares the Java and Python apps' console output byte for byte**, plus all
>    three CSV files. Any change touching `menu.py`'s output or `__main__.py`'s arguments breaks
>    parity unless the same change is made to `bank-java-console`. The blast radius is two apps,
>    not one.
> 2. **`async` genuinely does not belong** in an app whose entire I/O is three local CSV files.
>    Adding it would produce a snippet that is worse than a standalone one, which defeats the point
>    of quoting real code.
> 3. `match`/`case` in `menu.py` and a `--data-dir` `argparse` in `__main__.py` are both genuine
>    improvements that would need mirroring in Java to keep parity.
>
> Recommendation: **add `yield` and `logging` only** (both are additive and invisible to parity —
> a lazy transaction iterator in `stores.py`, and logging alongside the existing prints), and write
> `async`, `match`, `argparse` and `*args`/`**kwargs` standalone. Not actioned pending your call.

### Restamping the dates

The 17 posts carry dates scattered across **2020-03-06 → 2021-03-15** in no pedagogical order:
`python-fileread-write` is the **oldest**, so the archive currently opens the track on file I/O and
buries `python-introduction` two-thirds of the way down.

The archive sorts newest-first and prev/next walks the category oldest-first, so restamping into
teaching order is what makes the pager read 1 → 26. Same reasoning and same mechanism as `/java`
and `/backend-dev`.

`upsert_post` never overwrites an existing date, so this needs **`seed.py --force-dates`**. Slugs
and therefore URLs are untouched; only the displayed date and the ordering move.

**13:00** was chosen because it was free. The hours already taken over an overlapping date range:
09:00 (`/spring-boot`, `/react`, `/oracle`), 10:00 (DS&A), 11:00 (`/backend-dev`), 12:00 (`/java`,
`/frontend-dev`), 14:00 (`/spring-study-guide`). An exact tie makes the archive order arbitrary.

## Reading order

The order a person actually learns this, which is not the order these were published.

| # | Slug | State | Was (words / blocks) | Date |
|---|------|-------|---:|------|
| | **Getting started** | | | |
| 1 | `python-get-started` | **new** | — | 2026-06-30 |
| 2 | `python-introduction` | rework | 1,561 / 9 | 2026-07-02 |
| | **The language** | | | |
| 3 | `python-data-types` | rework | 1,448 / 38 | 2026-07-04 |
| 4 | `python-string-methods` | rework | 813 / 28 | 2026-07-06 |
| 5 | `python-f-strings` | **new** | — | 2026-07-08 |
| 6 | `python-conditional-statements` | rework | 1,247 / 35 | 2026-07-10 |
| 7 | `python-iterationfor-while-loops` | rework | 1,482 / **47** | 2026-07-12 |
| | **Collections** | | | |
| 8 | `python-lists-list-comprehensions` | rework | 966 / **41** | 2026-07-14 |
| 9 | `python-tuples` | **new** | — | 2026-07-16 |
| 10 | `python-dictionaries-sets` | rework | 1,333 / **42** | 2026-07-18 |
| | **Functions** | | | |
| 11 | `python-function` | rework | 1,607 / 30 | 2026-07-20 |
| 12 | `python-lambda-functions` | rework | 1,592 / 28 | 2026-07-22 |
| 13 | `python-generators-iterators` | **new** | — | 2026-07-24 |
| 14 | `python-decorators` | rework | 1,902 / 32 | 2026-07-26 |
| | **Objects** | | | |
| 15 | `python-class` | rework | 1,302 / 14 | 2026-07-28 |
| 16 | `python-oop` | rework | 1,637 / 13 | 2026-07-30 |
| 17 | `python-dataclasses-type-hints` | **new** | — | 2026-08-01 |
| | **Everyday Python** | | | |
| 18 | `python-exception-handling` | rework | 1,311 / 33 | 2026-08-03 |
| 19 | `python-fileread-write` | rework | 1,393 / 26 | 2026-08-05 |
| 20 | `python-user-input` | rework | 1,220 / 34 | 2026-08-07 |
| 21 | `python-modules-packages` | rework | 1,980 / **53** | 2026-08-09 |
| 22 | `python-async` | **new** | — | 2026-08-11 |
| | **Working like a professional** | | | |
| 23 | `python-testing` | rework | 1,667 / 27 | 2026-08-13 |
| 24 | `python-debugging` | **new** | — | 2026-08-15 |
| 25 | `python-best-practices` | **new** | — | 2026-08-17 |
| 26 | `python-code-snippets` | **new** | — | 2026-08-19 |

Note that `python-class` (14 blocks) and `python-oop` (13) are already close to the cap. Those two
need heading structure and tags, not surgery.

## What "keep posts to the point" means here

The failure mode is **exhaustiveness in code**, not padding in prose. `python-lists-list-comprehensions`
demonstrates every list operation rather than the ones you use.

> **Say the thing, show it once, name the trap that actually bites, stop.**

Concretely, what gets cut:

- **A block per method.** `.append`, `.extend`, `.insert`, `.remove`, `.pop`, `.clear` do not need
  six separate `<pre>` blocks. One block, six lines, one `# Output:`.
- **Numbered section headings.** `1. Creating Lists` … `11. Stacks and Queues` is an index, not a
  narrative. Six to nine `<h2>` sections with names.
- **The same idea shown three ways.** Keep the clearest.
- **The "advanced" tail** most posts grow. `/python-advanced` exists as a separate category.

What is kept, always: the plain-language definition, one runnable example per idea, and the caveat.

## Files

```
projects/python_tutorial/
  README.md            the requirements (corrected — the original was a copy of the Java one)
  progress_report.md   this file
  manifest.py          category metadata, release table, version policy, one entry per post
  posts/NN-slug.html   post bodies, plain semantic HTML — all 26 written
  seed.py              writes the posts into a content tree
  check_content.py     normaliser round-trip + word/code-block/heading/tag gates
  check_snippets.py    RUNS every code block under 3.12 and 3.14, verifies `# Output:` claims
  check_provenance.py  proves every `<!-- from: -->` block really is in the demo app
  check_links.py       HTML well-formedness + every internal link resolves
  check.sh             runs all of the above
```

`seed.py`, `check_content.py`, `check_links.py` and `check_provenance.py` are adapted from
`projects/java_tutorial/`. `check_snippets.py` is new and does something stronger than the one it
replaces — it executes rather than compiles.

```bash
./projects/python_tutorial/check.sh            # offline gates
./projects/python_tutorial/check.sh --links    # + the S3-backed link check (needs AWS_PROFILE=folau)
```

Then:

```bash
python3 projects/python_tutorial/seed.py                                  # dry run, local
python3 projects/python_tutorial/seed.py --env local --write --force-dates
```

`--force-dates` is required. Without it the 17 existing posts keep their 2020–21 dates and the
track reads in the wrong order.

## Result

| | Before | After |
|---|---:|---:|
| Posts | 17 | **26** |
| Code blocks per post | 9–**53** | 4–12 (cap 14) |
| Posts with no headings | 4 | 0 |
| `<h2>` per post | 0–53 | 7–10 |
| Tags per post | 1 | 4 |
| `boldgrid` residue | all 17 | 0 |
| Category name / description | `python` / empty | `Python` / written |
| Dates | 2020-03 → 2021-03, scattered | 2026-06-30 → 08-19, teaching order |
| Verified code samples | 0 | **202 blocks, 403 runs, 456 output claims** |

`python-modules-packages` went from 53 code blocks to 7; `python-iterationfor-while-loops` from 47
to 10; `python-lists-list-comprehensions` from 41 to 10.

Live and confirmed: `/python` lists 26 posts in reading order, all 17 original URLs still resolve
200, and the edge is serving build `394b0bd`.

## What the checkers actually caught

Recording these because they are the argument for the tooling. Every one was a real error in a
draft, found by a machine rather than a reader:

| Post | Caught |
|---|---|
| `python-data-types` | `Decimal(0.1)` — I wrote the repr from memory and it was truncated. Real value is 55 digits. |
| `python-conditional-statements` | `"pizza" in "pizzeria"` is **False**. It is not a substring. |
| `python-lists-list-comprehensions` | `round(8400.50 * 1.05, 2)` is `8820.52`, not `.53` — banker's rounding. Now explained in the post rather than hidden. |
| `python-iterationfor-while-loops` | The mutate-while-iterating example **coincidentally returned the right answer** with my input. Needed two consecutive negatives to actually show the bug. That is now a teaching point in the post. |
| `python-function` | Claimed a type-hint violation would run harmlessly; `"not a number" < 2.50` raises. |
| `python-oop` | I paraphrased the demo app's docstrings while claiming the block was lifted verbatim. Provenance refused it. |
| `python-class`, `python-modules-packages` | Output claims written in the wrong order, and `"json" in sys.modules` asserted True when nothing had imported it. |

Two of the checkers were fixed by the content rather than the other way round:

- **`-I` was wrong for the executor.** Isolated mode refuses to put the script's directory on
  `sys.path`, so `import money` failed for a snippet that had just written `money.py` beside itself
  — breaking every import example in `python-modules-packages` for reasons unrelated to the post.
  Now `-s -E`, which keeps the isolation that matters (no user site-packages, no `PYTHONPATH`) and
  leaves normal import behaviour alone.
- **Output claims now match against stderr as well as stdout.** `logging` writes to stderr by
  default, and a claim about a log line is not a wrong claim. Order is still enforced within each
  stream.

A third fix was found by the fixture that tests the checker itself: REPL blocks were being sent to
`ast.parse` before reaching doctest, and `>>> sorted(xs)` is not valid Python source, so every REPL
block in the track failed. They now skip the parse step and let doctest compile each example.

## Open questions

1. **How far to go in `bank-python-console`** to satisfy the README's "add them if not found"
   clause. **Not actioned** — the recommendation above (`yield` + `logging` only, both invisible to
   `parity.sh`) still stands and nothing published depends on it. Seven blocks across seven posts
   quote the app as it is, all provenance-verified.
2. **Verify `manifest.RELEASES[*]["status"]`** against `https://devguide.python.org/versions/`.
   Still outstanding — the release *dates* and *features* in the published table are sound, but the
   support-phase column was written from the calendar on 2026-08-20 and should be confirmed.

## Log

| Date | What |
|---|---|
| 2026-08-20 | Audited `/python`: 17 posts, prose already on target at 1,438 mean, but 9–53 code blocks per post, 4 posts with no headings at all, 1 tag each, boldgrid on all 17, category name and description unset, no get-started post. |
| 2026-08-20 | Noted `README.md` was a copy of the Java one — "update java backend dev posts", "what version of java", "Major LTS java releases". Corrected. |
| 2026-08-20 | Folau: expand to 26 (17 + 9 new); Python 3.12 baseline with 3.14 callouts; standalone run-verified snippets; release table 3.9 → 3.14 rather than an LTS table. |
| 2026-08-20 | Measured demo-app feature coverage by grep rather than assuming it — 12 of 26 posts can quote it; generators, async, match, argparse, logging and `*args` are absent from the app. Raised as open question 1. |
| 2026-08-20 | Scaffolded: manifest with all 26 entries and the release table, tooling adapted, `check_snippets.py` written to execute rather than compile. |
| 2026-08-20 | Proved the checker works before trusting it — a deliberately broken fixture confirmed it catches a wrong output claim, a syntax error, a stale `expect-error`, and a mismatched REPL session, while passing a 3.14-pinned block, a `norun` block and a correct doctest. Provenance sanity-tested both ways. |
| 2026-08-20 | Wrote all 26 post bodies. Seven caught errors and three checker fixes, all recorded above. |
| 2026-08-20 | All gates green: 202 blocks / 403 runs / 456 output claims, provenance clean, demo app suite passing, 93 internal links resolve, build guard 603/603 posts and 44/44 category counts. |
| 2026-08-20 | Seeded local (595 posts), then prod (603 posts). Deployed build `394b0bd`; CloudFront invalidated and the edge verified serving it. `/python` live with 26 posts in reading order. |

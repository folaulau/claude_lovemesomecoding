# TypeScript tutorial track — progress report

**Status:** WRITTEN AND SEEDED TO `local` — not yet on prod
**Started:** 2026-09-05
**Where it lands:** https://lovemesomecoding.com/typescript

---

## What this is

A **brand-new collection**. There is no `typescript` category in the content DB today — checked
against `lovemesomecoding_frontend/content/index/categories.json` on 2026-09-05, which lists 42
categories and none of them is this one. Two posts elsewhere have "typescript" in the slug
(`angular-typescript`, `frontend-dev-javascript-and-typescript`) and both stay where they are.

That makes this the easiest kind of track to seed: **every slug is new**, no indexed URL is at
risk, and `seed.py` never needs `--force-dates`.

The track is **21 posts**, sourced from the topic lists at w3schools.com/typescript and
typescripttutorial.net per the README, with the small stuff dropped and the important stuff given
room.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Category | new `typescript` slug, name "TypeScript" | Nothing to rewrite. No URL risk. |
| Nav | `JavaScript` group, after `javascript` | README: "Add the link to the collection under Javascript dropdown." |
| Track size | 21 posts | Between React's 27 and FastAPI's 19. Covers both source syllabi without a post per keyword. |
| Post length | **8–10 reading-minutes** | Folau's call, 2026-09-05. Deeper than the React track's 4–7, half of FastAPI's 13–16. |
| Prose floor | 45% of counted words | Higher than FastAPI's 40%: a language tutorial's snippets are short, so a low prose share here means the post is a syntax dump. |
| Example source | `lovemesomecoding_demo_project/pizza` — the React **and** Angular halves | The contractor app was still being written. See below. |
| Dates | 2026-07-07 … 2026-09-05, 3 days apart | Computed from `START_DATE`, so a re-base is one edit. Ascending, so the pager reads lesson 1 → 21. |
| Seeding | Backend service layer, as the FastAPI/React/Oracle tracks do | The static build reads only the derived indexes; reusing the admin API's own code is the only way to be sure the indexes and the posts agree. |
| Optional lessons | decorators, React, tsconfig and interview questions all IN | Folau's call, 2026-09-05. |

## ⚠️ Why NOT the contractor app

`lovemesomecoding_demo_project/contractor/README.md` says outright: *"typescript tutorial will be
from this project just FYI."* That was the plan, and it was abandoned on day one for a good
reason.

**The contractor app was being written while this track was being scaffolded.** Not "recently
written" — concurrently, by another session:

- Its entire source tree was created between **00:22 and 00:57 on 2026-09-05**, a 35-minute window.
- Nothing in it is committed. `git status` reports the whole directory as untracked.
- Its own `progress_report.md` claims phases 0–5 are "not started" while the frontend pages and
  the NestJS services are both fully written — the report is stale by several phases.
- Mid-survey, `contractor-react-frontend/src/api/client.ts` was split into `queries.ts` +
  `apollo.ts` and then **restored, rewritten, at 00:57:35** — twenty seconds before the check ran.
- `check_content.py` caught it: six posts failed because a file named in `SNIPPET_SOURCES` had
  ceased to exist between writing the manifest and running the check.

Every code sample in this track is meant to be provably real. Quoting a tree that changes every
thirty seconds gives the *appearance* of that with none of the substance. Folau's call, made on
those facts: use pizza instead.

If the contractor app settles and gets committed, its NestJS half would genuinely strengthen
lesson 19 — Nest's `@Controller`/`@Injectable`/`@Column` are the canonical decorator examples.
Nothing is missing without it, though, because Angular supplies decorators already.

## Why the pizza app works

Stable — last touched **2026-08-24**, twelve days before this track started, committed, and both
halves typecheck. 201 TypeScript files across three apps.

It is also teaching material *already*: the files carry `REACT CONCEPT:` / `ANGULAR CONCEPT:`
comment blocks explaining the choices, so snippets arrive with their reasoning attached.

**The two halves are on different TypeScript versions, and that is the single most useful thing
about it.** Angular 21 pins its own compiler and had not moved to 6.x:

| | React half | Angular half |
|---|---|---|
| TypeScript | **6.0.3** | **5.9.3** |
| Key flag | `erasableSyntaxOnly: true` | `experimentalDecorators: true` |
| Consequence | no `enum`, no parameter properties, **no decorators** | decorators everywhere |

Each config forbids something the other depends on. That turns the abstract question — *should you
use `enum`? should you use parameter properties?* — into a concrete one: under this flag it does
not compile, and here is what the app does instead. Lessons 9, 12, 18 and 19 are all built on it.

Non-invented examples for the hard lessons:

- **`request<T>(path, options): Promise<T>`** in `lib/api.ts`, with an `api` object whose methods
  fix the HTTP verb and forward `T` — and take `Omit<RequestOptions, 'method' | 'body'>` so the
  caller cannot pass the two things the wrapper already decided. Lessons 13 and 14 in one file.
- **`toApiFailure(err: unknown, …)`** in `store/apiFailure.ts` proves what it has before touching
  it — `err instanceof ApiError`, then `err instanceof Error`, then a fallback. `failureMessage`
  goes further with `typeof err === 'object' && 'message' in err`. That is lesson 4 and lesson 10
  written for us, in code that runs.
- **`export type Outcome = { ok: true } | { ok: false; failure: ApiFailure }`** in the Angular
  admin store — a textbook discriminated union, doing a real job. Lesson 10.
- **`ReturnType<typeof store.getState>`** in `store/index.ts`, with a comment saying why the types
  are derived from the store rather than declared beside it. Lessons 14 and 15.
- **`Page<T>`** in `types/index.ts` — a generic interface for Spring's pagination envelope.
- **`type UUID = string`** plus five string-literal unions (`OrderStatus`, `SizeName`, …). The
  enums lesson's answer, in the file that would have used `enum` in another codebase.
- **`class ApiError extends Error`**, written twice — once per half. The Angular one adds
  `Object.setPrototypeOf(this, ApiError.prototype)` with a comment about ES5 and `instanceof`.
  Lesson 12.
- **`@Pipe`, `@Directive`, `@Injectable`, `@Component`** in the Angular half, each already carrying
  an explanatory comment block. Lesson 19.
- **`createContext<AuthContextValue | undefined>(undefined)`** in `AuthContext.tsx` — the exact
  pattern lesson 20 needs for removing `| undefined` from every consumer.

### Versions — read off this machine, not chosen

`npx tsc --version` in both app directories and `node --version`, 2026-09-05.

| | |
|---|---|
| TypeScript | **6.0.3** (React half) / **5.9.3** (Angular half) |
| Node | v22.23.2 |
| React | 19.2.8 · Vite 8.2.0 · Redux Toolkit 2.12.0 |
| Angular | 21.2.0 · NgRx 21.1.1 · RxJS 7.8 |

## Topic list

The order is the reading order. `date` ascends with the track so the prev/next pager reads
lesson 1 → lesson 21.

### Part 1 — Getting started

| # | Slug | Title | Source in the demo app |
|---|------|-------|------------------------|
| 1 | `typescript-get-started` | Get Started | the track index; versions table |
| 2 | `typescript-set-up` | Setting Up a Project | both `package.json`s, `tsconfig.app.json`, `vite.config.ts` |
| 3 | `typescript-basic-types` | The Basic Types | `types/index.ts`, `lib/money.ts` |
| 4 | `typescript-special-types` | any, unknown, never and void | `store/apiFailure.ts`, `core/api-error.ts` |

### Part 2 — Shaping data

| # | Slug | Title | Source in the demo app |
|---|------|-------|------------------------|
| 5 | `typescript-arrays-and-tuples` | Arrays and Tuples | `types/index.ts` (`Array<{…}>`), `lib/money.ts` |
| 6 | `typescript-object-types` | Object Types | `types/index.ts` — optional props, `\| null`, nesting |
| 7 | `typescript-interfaces-vs-type-aliases` | Interfaces vs Type Aliases | `types/index.ts`, `admin/store/outcome.ts` |
| 8 | `typescript-union-and-intersection-types` | Unions and Intersections | `OrderStatus`, `Outcome` |
| 9 | `typescript-enums` | Enums — and What to Use Instead | `types/index.ts` + `erasableSyntaxOnly` |
| 10 | `typescript-narrowing` | Narrowing and Type Guards | `store/apiFailure.ts`, `outcome.ts`, `api-error.ts` |

### Part 3 — Behaviour

| # | Slug | Title | Source in the demo app |
|---|------|-------|------------------------|
| 11 | `typescript-functions` | Functions | `lib/money.ts`, `lib/api.ts` |
| 12 | `typescript-classes` | Classes | both `ApiError`s, `MoneyPipe` |
| 13 | `typescript-generics` | Generics | `request<T>` and the `api` object; `Page<T>` |
| 14 | `typescript-utility-types` | The Utility Types Worth Knowing | `Omit<>`, `Record<>`, `ReturnType<typeof …>` |
| 15 | `typescript-mapped-and-conditional-types` | keyof, Mapped and Conditional Types | `store/index.ts` |
| 16 | `typescript-type-assertions` | Assertions, `as const` and `satisfies` | `parsed as T`, `error.error as ApiErrorBody \| null` |

### Part 4 — Real projects

| # | Slug | Title | Source in the demo app |
|---|------|-------|------------------------|
| 17 | `typescript-modules` | Modules and Type-Only Imports | `import type` throughout; `verbatimModuleSyntax` |
| 18 | `typescript-tsconfig` | tsconfig — The Flags That Matter | the two configs, which disagree correctly |
| 19 | `typescript-decorators` | Decorators | `@Pipe`, `@Directive`, `@Injectable`, `@Component` |
| 20 | `typescript-with-react` | TypeScript with React | `ProductCard.tsx`, `AuthContext.tsx` |
| 21 | `typescript-interview-questions` | Interview Questions | the twenty lessons before it |

---

## The scripts

Same three the FastAPI track uses, adapted. Run all three before seeding.

```bash
python projects/typescript_tutorial/check_content.py    # HTML round-trips the normaliser
python projects/typescript_tutorial/check_snippets.py   # quotes still match the app
python projects/typescript_tutorial/seed.py --env local # dry run
```

`check_snippets.py` differs from the FastAPI one in one way that matters. A framework tutorial
quotes the app for nearly every block, so a low match rate there is drift. **A language tutorial
does not** — most blocks are three lines of syntax that exist to demonstrate one rule and belong
in no repository. So the match rate is expected to be low, and the check that earns its keep is
the near-miss detector: a block whose opening lines *are* in the app but whose body is not, which
is the signature of a quote that has gone stale.

---

## Open items

- [x] Write the 21 post bodies — done 2026-09-05. All 21 land at **8 reading-minutes**, inside the
      8–10 budget, and `check_content.py` reports no warnings and no failures.
- [x] Add `typescript` to the `JavaScript` group in `lovemesomecoding_frontend/src/lib/nav.ts`.
      `navTree()` filters against `allCategories()`, so the entry was inert until the category
      existed. Frontend typechecks clean.
- [x] Seed `local` — 21 posts written, archive holds 21, category count 21, dates
      2026-07-07 → 2026-09-05 ascending.
- [ ] **Review on `:3000`**, then seed `prod` (`seed.py --env prod --write`) and deploy the frontend
      so the nav entry ships with the category.
- [ ] `contractor/progress_report.md` is stale — it says phase 0/1 while the app is much further
      along. Not this track's job to fix, but do not trust it.

## Final numbers

| | |
|---|---|
| Posts | 21, every one at 8 reading-minutes |
| Words | 30,786 counted (prose + code), 82% prose against a 45% floor |
| Code blocks | 316 — 120 verified against the running app, 30 marked as deliberately non-compiling, 166 short illustrations |
| Drift | none |

The 38% "quoted from code that runs" figure is expected and is explained at length in
`check_snippets.py`'s docstring: a language tutorial's snippets are mostly three-line demonstrations
of one rule, which belong in no repository. The number that matters is the drift count, and it is
zero.

## QA on `:3000` (2026-09-05)

Ran the dev server against the seeded `local` tree and checked the things that fail silently.

| Check | Result |
|---|---|
| All 21 post URLs | 200 |
| `/typescript` archive | 21 post links, h1 "TypeScript Tutorials" |
| Nav | `typescript` present in the JavaScript group |
| Prism highlighting | 13/13 blocks on `typescript-enums` carry token markup — `typescript`, `tsx`, `json`, `javascript` all highlight |
| TOC anchors | present on every `<h2>` (14 on the enums post) |
| Reading time | renders "8 min read" |
| **Prev/next pager** | walked lesson 1 → 21; order matches the manifest exactly, lesson 1 has no prev, lesson 21 has no next |
| **Cross-links** | 21 distinct internal hrefs across the track, every one resolves 200 and points at a slug in this track |
| Derived indexes | `categories.json` count 21 · `by-category/typescript.json` 21 · `index/posts.json` 21 · `search/index.json` 21 |
| Sitemap | 21 `/typescript/` URLs |

The pager walk is the one worth keeping: it is the only check that proves the computed dates
actually produce the intended reading order, and it walks the real rendered HTML rather than the
manifest.

### One error this caught

The category description and lesson 1's excerpt both described the source as *"a working
marketplace app"* — left over from when this track was going to be written from the contractor
marketplace. The source is a **pizza ordering app**. Both strings fixed in `manifest.py` and the
category re-seeded.

Worth noting the class of mistake: it survived every automated check, because nothing verifies that
prose about the app is true of the app. `check_snippets.py` proves the *code* is real; it has
nothing to say about a sentence.

## Log

**2026-09-05** — Surveyed the ground. Confirmed no `typescript` category exists, settled length
(8-10 min) and scope (21 posts, all four optional lessons in) with Folau, and wrote the manifest
and `check_content.py`.

**2026-09-05, later** — Changed the example source from contractor to **pizza**. The contractor app
turned out to be under active construction in another session while this track was being
scaffolded: `check_content.py` failed on six posts because `api/client.ts` stopped existing
between writing `SNIPPET_SOURCES` and running the check, and the file came back rewritten twenty
seconds later. Folau's call. Repointed `DEMO_APP`, `VERSIONS` and all 21 `SNIPPET_SOURCES` entries
at pizza; every declared path now verifies. The swap turned out to be an upgrade rather than a
compromise — see "Why the pizza app works" above, in particular the two halves being on different
TypeScript versions with contradictory flags.

Also added the nav entry, and confirmed `typescript` and `tsx` Prism grammars already exist on
both halves of the pipeline, so no highlighter work is needed.

**2026-09-05, later still** — Wrote all 21 posts and seeded `local`.

Three fixes to the checking scripts came out of writing, each prompted by a real miss:

1. **`check_snippets.py` only looked at the first chunk of a block.** A block split by `// ...`
   whose opening chunk still matched was never examined further, so drift in a later chunk was
   invisible. Caught by deliberately renaming `crustPriceDelta` in a quoted interface and watching
   the check pass. Now every chunk is examined.

2. **Prefix-only matching missed drift on a chunk's FIRST line.** The renamed field was the opening
   line of its chunk, so the matching prefix was zero and the block was filed as `illustrative` —
   the bucket that never fails a build. Added `longest_suffix`, so a chunk is also read from the
   end. Both drift shapes now fail; verified with two deliberately drifted fixtures.

3. **Generic JSON openers produced false drift.** `{` and `"compilerOptions": {` open every tsconfig
   in the app, so a hand-written config illustrating `allowJs`/`checkJs` cleared `DRIFT_LEAD` and
   was reported as a stale quote. `substantive()` now counts only lines that name something.

And one to `check_content.py`: **banning `plaintext` outright was wrong.** A `tsc` diagnostic is not
TypeScript and Prism has no grammar for it, so `plaintext` is the correct language for the several
blocks that quote compiler output. But an unsupported language is *normalised* to plaintext rather
than rejected, so a misspelt class lands in the same place silently. The rule now compares the
authored class against the pipeline's output, which separates the two cases exactly.

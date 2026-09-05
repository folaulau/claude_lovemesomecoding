# NestJS tutorial track — progress report

**Status:** IN PROGRESS — app extended and verified; writing the track
**Started:** 2026-09-05
**Where it lands:** https://lovemesomecoding.com/nestjs

---

## What this is

A **brand-new collection**. There is no `nestjs` category in the content DB today — checked on
2026-09-05 against `lovemesomecoding_frontend/content/index/categories.json`, which lists 43
categories and none of them is this one. So every slug is new, no indexed URL is at risk, and
`seed.py` never needs `--force-dates`.

The track is **20 posts**, sourced from the section lists at docs.nestjs.com and the topic list on
geeksforgeeks.org/javascript/nestjs per the README, with the small stuff dropped.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Category | new `nestjs` slug, name "NestJS" | Nothing to rewrite. No URL risk. |
| Nav | `JavaScript` group, after `typescript` | README: "put a link to this collection under the Javascript menu. Call it NestJS". Reading order — Nest is TypeScript applied. |
| Track size | 20 posts | Folau's call, 2026-09-05. Covers docs.nestjs.com's Introduction and Fundamentals plus the Techniques that matter, without a post per decorator. |
| Post length | **8–10 reading-minutes** | Folau's call, 2026-09-05. Same budget as the TypeScript track. |
| Prose floor | 40% of counted words | Lower than the TypeScript track's 45%, matching FastAPI. A framework post legitimately quotes whole modules; the code IS the lesson here in a way it is not for a language tutorial. |
| Example source | `lovemesomecoding_demo_project/contractor/contractor-nestjs-backend` | README names it explicitly. |
| Extending the app | Add the missing core primitives | README, updated 2026-09-05: "add to the project if a teaching material is not there yet but make sure the project still runs." Folau's call on scope. See below. |
| Dates | 2026-06-19 … 2026-09-05, 3 days apart | Ascending, so the pager reads lesson 1 → 20. Computed from `START_DATE`, so a re-base is one edit. |
| Seeding | Backend service layer, as the TypeScript/FastAPI/React tracks do | The static build reads only the derived indexes; reusing the admin API's own code is the only way to be sure the indexes and the posts agree. |

## Why the contractor app works this time

The TypeScript track **rejected** this same app on 2026-09-05 and used pizza instead. That was the
right call then and does not apply now. The reason it was rejected was that the app was being
written *concurrently* — its whole source tree appeared inside a 35-minute window, and
`api/client.ts` was split and restored twenty seconds before the check ran.

Re-checked on 2026-09-05 before starting this track:

| Check | Result |
|---|---|
| Last modification anywhere in the tree | 01:13 — over seven hours before this track started |
| `npx tsc --noEmit -p tsconfig.json` | **exit 0**, no errors |
| Committed? | No — and it never will be. `lovemesomecoding_demo_project` is in `.gitignore` (line 14), so `git status` reporting it as untracked was never evidence of work in progress. |

So the objection was *churn*, and the churn has stopped. Nothing else about the app was ever the
problem — the opposite, in fact.

**It is unusually good teaching material.** The source carries `⚠️` comment blocks that explain the
*why* behind each choice, not just the what: why the guard order in `@UseGuards(JwtAuthGuard,
RolesGuard)` is load-bearing, why `verifyAsync` and never `decode`, why login burns a bcrypt
comparison against a dummy hash even when there is no user, why `memoryStorage()` is a security
decision rather than a performance one. A tutorial normally has to invent that commentary. Here it
is already attached to code that compiles.

### Versions — read off this machine, not chosen

`node --version` and `npx tsc --version` in the backend directory, plus the installed package
versions, 2026-09-05.

| | |
|---|---|
| @nestjs/core, @nestjs/common, @nestjs/typeorm | **12.0.1** |
| TypeORM | 1.1.1 |
| class-validator | 0.15.1 |
| TypeScript | 6.0.3 |
| Node | v22.23.2 |
| Vitest | 4.1.11 |

⚠️ The app is **ESM** — `"type": "module"` with `moduleResolution: nodenext`. Every relative import
carries a `.js` extension even though the source is `.ts`. That is not optional and it is not a
typo; it is the single thing most likely to confuse a reader copying a snippet, so lesson 2 covers
it and every quoted snippet keeps it.

## What the app already covered, and what had to be added

Surveyed 2026-09-05 by grepping the decorators and `implements` clauses across `src/` and `test/`.

**Already there** — modules including `@Global()`, controllers, providers and constructor
injection, DTOs with `class-validator` behind a global `ValidationPipe`, two guards implementing
`CanActivate`, a `createParamDecorator` param decorator, `SetMetadata` + `Reflector`, TypeORM
entities/migrations/transactions/pessimistic locks, `ConfigModule` with a typed factory, JWT
auth, `FileInterceptor` file upload, and a 477-line e2e suite using `Test.createTestingModule`.

**Missing, and added for this track** — see the log below for what landed:

| Primitive | Lesson | What landed |
|---|---|---|
| Middleware | 11 | `common/middleware/request-id.middleware.ts` — assigns/echoes `x-request-id`, bound in `AppModule.configure()` |
| Interceptor | 10 | `common/interceptors/logging.interceptor.ts` — one log line per request, bound with `APP_INTERCEPTOR` |
| Exception filter | 12 | `common/filters/all-exceptions.filter.ts` — `@Catch()`, bound with `APP_FILTER` |
| Custom pipe | 7 | `common/pipes/trim.pipe.ts` — registered before `ValidationPipe` in `main.ts` |
| Unit tests | 19 | `trim.pipe.spec.ts`, `roles.guard.spec.ts`, `auth.service.spec.ts` |

The rule for every addition: it has to be something the app should have had anyway, not a demo
bolted on for the tutorial. Each one earns its place:

- **The middleware is middleware for a reason a lesson can use.** It runs before guards, so a 401
  thrown by `JwtAuthGuard` still carries an id. An interceptor doing the same job would stamp every
  200 and no 401 — and the failures are the requests you most want to correlate. Lesson 11 is that
  sentence with the evidence attached.
- **The interceptor is an interceptor for the mirror-image reason.** It needs the *outcome*, which
  middleware has already handed onward by the time it exists.
- **The filter fixes a real 500.** `acceptQuote` relies on the partial unique index
  `uq_one_accepted_quote_per_project` as a backstop, and until now that firing produced a bare 500.
  It is a 409 now. `message` keeps the exact shape Nest produced — a string, or an **array** for a
  `ValidationPipe` rejection — because the e2e suite asserts on both and so does the React client.
- **The pipe fixes a real bug.** `RegisterDto` says `@Length(1, 80) firstName` and `AuthService`
  stores `dto.firstName.trim()`. Three spaces passed the validator and were stored as `""`. The
  validator and the service disagreed about what the value *was*; trimming first removes the
  disagreement. Every `@Length` rule in the app had this.
- **The unit tests close a gap in what is testable at all.** Before them `npm test` found no files:
  nothing could be tested without Docker and a migrated Postgres. The three that landed need
  neither, and `auth.service.spec.ts` proves a property the e2e suite structurally cannot — that
  the three login failures are indistinguishable.

### Verification — the app still runs

| Check | Before | After |
|---|---|---|
| `npx tsc --noEmit` | exit 0 | **exit 0** |
| `nest build` | — | **exit 0** |
| `npm test` (unit) | *no test files found* | **17 passed, 3 files** |
| `npm run test:e2e` | 19 passed | **19 passed** — no assertion changed |

Then run for real (`node dist/main.js` against the running compose stack) and exercised with curl,
because a passing test suite is not the same as a working pipeline:

| | |
|---|---|
| `x-request-id` on a guard-thrown 401 | present — the thing an interceptor could not do |
| A well-formed client `x-request-id` | echoed back |
| `x-request-id: bad id with spaces` | replaced with a fresh UUID, not repeated into the log |
| Validation error body | `message` still an **array**, plus `path`/`timestamp`/`requestId` |
| `{"firstName":"   "}` | now **400**, `"firstName must be longer than or equal to 1 characters"` |
| Log lines | `POST /api/v1/auth/login 200 74ms AuthController.login req=… user=…`, WARN for 4xx |
| Foreign project | still **404**, not 403 — existing behaviour unchanged |

⚠️ Port 3001 had a stale API from the 2026-09-05 01:05 session still running the pre-change build.
Killed and restarted on the new build; it is up now.

⚠️ `user.entity.ts` has a stale comment referring to `users/dto/user.dto.ts`, which does not exist
— `common/serializers.ts` does that job. Do not quote that line; the rest of the file is accurate.

## Topic list

The order is the reading order. `date` ascends with the track so the prev/next pager reads
lesson 1 → lesson 20.

### Part 1 — Foundations

| # | Slug | Title | Source in the app |
|---|------|-------|-------------------|
| 1 | `nestjs-get-started` | Get Started | the track index; versions table |
| 2 | `nestjs-project-setup` | Setting Up a Project | `package.json`, `tsconfig.json`, `nest-cli.json`, `main.ts` |
| 3 | `nestjs-modules` | Modules | `app.module.ts`, `auth.module.ts` (`@Global`), `projects.module.ts` |
| 4 | `nestjs-controllers` | Controllers | all five controllers |
| 5 | `nestjs-providers-and-dependency-injection` | Providers and DI | the services, `JwtModule.registerAsync` |

### Part 2 — The request pipeline

| # | Slug | Title | Source in the app |
|---|------|-------|-------------------|
| 6 | `nestjs-dtos-and-validation` | DTOs and Validation | `auth.dto.ts`, the global `ValidationPipe` |
| 7 | `nestjs-pipes` | Pipes | `ParseUUIDPipe`, the pipe added for this track |
| 8 | `nestjs-guards` | Guards | `jwt-auth.guard.ts`, `roles.guard.ts` |
| 9 | `nestjs-custom-decorators` | Custom Decorators | `current-user.decorator.ts`, `roles.decorator.ts` |
| 10 | `nestjs-interceptors` | Interceptors | `FileInterceptor`, the interceptor added for this track |
| 11 | `nestjs-middleware` | Middleware | the middleware added for this track |
| 12 | `nestjs-exception-filters` | Exception Filters | the built-in `HttpException`s the services throw; the filter added for this track |
| 13 | `nestjs-request-lifecycle` | The Request Lifecycle | ties lessons 6–12 together against one real request |

### Part 3 — Real applications

| # | Slug | Title | Source in the app |
|---|------|-------|-------------------|
| 14 | `nestjs-configuration` | Configuration | `configuration.ts`, `ConfigModule.forRoot` |
| 15 | `nestjs-database-typeorm` | Databases with TypeORM | the entities, migrations, `acceptQuote`'s transaction |
| 16 | `nestjs-authentication-jwt` | Authentication with JWT | `auth.service.ts`, `jwt-payload.ts` |
| 17 | `nestjs-authorization-roles` | Authorization and Roles | `@Roles` + `RolesGuard`, the ownership checks |
| 18 | `nestjs-file-upload` | File Upload | `contractors.controller.ts`, `image-validation.ts` |
| 19 | `nestjs-testing` | Testing | `rules.e2e-spec.ts`; the unit tests added for this track |
| 20 | `nestjs-interview-questions` | Interview Questions | the nineteen lessons before it |

---

## The scripts

Same three the TypeScript track uses, adapted. Run all three before seeding.

```bash
python projects/nestjs_tutorial/check_content.py    # HTML round-trips the normaliser
python projects/nestjs_tutorial/check_snippets.py   # quotes still match the app
python projects/nestjs_tutorial/seed.py --env local # dry run
```

Unlike the TypeScript track, this one is a **framework** tutorial: a high snippet match rate
against the app is expected, and a low one is the finding. The near-miss detector matters just as
much though — a block whose opening lines are in the app but whose body is not is a stale quote.

## Open items

- [x] Add the five missing primitives to the contractor backend — done, all gates green
- [ ] Write `manifest.py`, `check_content.py`, `check_snippets.py`
- [ ] Write the 20 post bodies
- [ ] Add `nestjs` to the `JavaScript` group in `lovemesomecoding_frontend/src/lib/nav.ts`
- [ ] Seed `local`, QA on `:3000`
- [ ] Seed `prod`, deploy, verify on the live site

## Log

**2026-09-05** — Surveyed the ground. Confirmed no `nestjs` category exists (43 in the content DB).
Re-checked the contractor backend that the TypeScript track had rejected: stable for seven hours
and `tsc --noEmit` exits 0, so the churn objection no longer holds. Read both sources named in the
README and mapped their topics onto what the app can actually demonstrate. Settled size (20),
length (8–10 min) and the app-extension scope with Folau.

**2026-09-05, later** — Extended the contractor backend with the five missing primitives and
verified the app still runs (table above). Recorded the new request pipeline in the contractor's
own `CLAUDE.md`, next to the layer rules, since it is now part of how that app works and not a
tutorial artefact.

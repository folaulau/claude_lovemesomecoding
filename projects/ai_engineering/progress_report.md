# AI-Assisted Engineering track: progress report

**Status (2026-10-04): ✅ LIVE.** All 16 posts at https://lovemesomecoding.com/ai-engineering, under
the AI nav group. Backend with `diff` deployed by CI (Folau's push, run 37237508552); frontend nav +
prism-diff deployed by CI (run 37237503439); prod seeded (938 → 954 posts); CodeBuild Publish
`484eec7f…` succeeded. Verified live: 16/16 post URLs 200, archive lists 16, diff highlighting
renders, sitemap has the category + 16 posts. PR #1 open on the demo repo.
Uncommitted in this repo: projects/ai_engineering/, CLAUDE.md (pocsoft note). Session `.jsonl` raw
transcripts are logs — keep out of git; the `.md` transcripts are the record.

## Decisions (2026-10-04)
| Question | Decision |
|---|---|
| Relation to the existing `claude` category (10 posts, Feb 2026) | New category `ai-engineering` alongside it; old URLs untouched, new posts link to them |
| Example source | Pizza demo app, using real sessions only |
| Tool scope | Claude Code first; claude.ai / Chrome / MCP where the task needs them |
| Length | 5–8 min per post |
| Nav | Append `ai-engineering` to the existing **AI** group (no new group needed) |
| Core theme (Folau) | Engineers must **read the code and follow the plan, not just click Accept**. Dedicated post #2, plus a "Before you accept" section closing every post |

## Proposed outline (category `ai-engineering`)
| # | Slug | Topic | Status |
|---|---|---|---|
| 1 | ai-engineering-mindset | Working with AI as an engineer: you own the output | live |
| 2 | ai-engineering-read-before-you-accept | Read the code, follow the plan: why "Accept" is not a review. The job moves from writing to reviewing; how to read a diff fast; spotting drift from the plan; what blind accepting costs (real pizza-app example); when to stop and say no | live |
| 3 | ai-engineering-setup | Setting Claude up for a real codebase: CLAUDE.md, memory, permissions, MCP | live |
| 4 | ai-engineering-codebase-analysis | Analysis: learning an unfamiliar codebase, tracing a flow, sizing a change | live |
| 5 | ai-engineering-requirements | Turning a ticket into requirements: clarifying questions, edge cases | live |
| 6 | ai-engineering-planning | Planning: plan mode, progress report, splitting the work. The plan is the contract you review against | live |
| 7 | ai-engineering-writing-code | Writing code: small diffs, house style, verify each step | live |
| 8 | ai-engineering-writing-tests | Writing tests that prove behaviour | live |
| 9 | ai-engineering-debugging | Debugging and production incidents | live |
| 10 | ai-engineering-aws-investigation | Investigating AWS: CloudWatch, costs, config, read-only guardrails | live |
| 11 | ai-engineering-ui-walkthrough | UI feature walkthroughs with Playwright / Claude in Chrome | live |
| 12 | ai-engineering-pull-requests | Creating PRs: commits that explain why, PR descriptions | live |
| 13 | ai-engineering-pr-review | Responding to PR review | live |
| 14 | ai-engineering-customer-support | Customer support: triage, reproduce, draft the reply | live |
| 15 | ai-engineering-guardrails | Guardrails: secrets, destructive actions, hallucinations, when not to use it | live |
| 16 | ai-engineering-capstone | Capstone: one pizza feature from ticket to merged PR | live |

Every post closes with **"Before you accept"**: what to read and check for that workflow (e.g. tests:
does the assertion actually fail without the fix? PRs: does the description match the diff?).

## The feature the series follows: PIZZA-42, pay with a saved card at checkout
Demo repo `lovemesomecoding_demo_project`, branch `feature/checkout-saved-cards` (local only, not pushed).
Chosen because the pizza CLAUDE.md lists it as the open item, so it is real work.

**How sessions run:** `run_session.py` drives headless `claude -p` in the pizza app and saves
`sessions/<name>.jsonl` (raw) + `.md` (readable). One conversation (`aa622bee-…`) is resumed
through every step, like a real working session. I act as the engineer: verify claims, review each
diff, decide, commit. My checks are recorded in `sessions/*.verification.md` or below.

**Product-owner answers (Folau, 2026-10-04):** Q1 save-at-checkout out of scope (new ticket);
Q3/Q5 choose card on the payment step, retry another card on the same order after a decline;
Q4 expired cards shown disabled; Q8 backend + React only. Q2/Q6/Q7/Q9 took the assistant's
defaults (primary preselected, no CVC re-entry, explicit "Pay $X with Visa ••4242", no card
management at checkout). Folau may overrule these.

| Session | Post | Result |
|---|---|---|
| 04-analysis (plan mode) | 4 | Full trace with line refs; 8 claims spot-checked, all true. Missed: order test stubs `isConfigured()=false` |
| 05-requirements | 5 | 9 PO questions w/ defaults, edge cases, 5 conflicts (biggest: cards can only be saved on profile) |
| 06-planning | 6 | 7-step plan, one commit each, explicit out-of-scope list. Flagged the Co-Authored-By conflict between global and project CLAUDE.md |
| 07-step1 (acceptEdits) | 7, 8, 2 | DAO + expiry rule, 8 new tests pass. Reported 4 pre-existing failures honestly and could not prove it (needed approvals) — I proved it by stashing and re-running. Review: dropped an unused "for later" JdbcTemplate. Mutation check: removing the ownership filter fails `ignoresSomeoneElsesCard`. Commit `1b0549a0` |
| 07-step2 | 7 | Service + Stripe update, 15 tests. Disclosed 6 additions beyond the plan. Accepted; createOrder error-text mismatch noted as follow-up. `fb1105a0` |
| 07-step3 | 7, 8 | Endpoint + security rule. **Changed a test expectation from the plan (401→403)** and said so; verified against `ApiSecurityIntegrationTest` before accepting. `03c16ae8` |
| 07-step4 | 7 | Frontend helpers; refactor verified behaviour-identical by reading. `64e300d5` |
| 07-step5 (+review) | 7, 11 | Card chooser; it ran real Stripe payments itself. My screenshots (`walkthrough/`) found nothing visual; I nearly filed a false finding (green radios = Bootstrap validation state). Reading found an a11y bug (div label → fieldset/legend), sent back, re-verified by accessible name. `34784b02` |
| 08-step6-tests | 8 | 7 Playwright tests; it proved 3 by breaking code. I re-ran 7/7 and checked cleanup. `5fe44211` |
| 07-step7-docs | 6, 9 | Docs. **Its "make seed dates relative to today" fix was wrong — they already use NOW(), evaluated once.** Caught by checking the changeset; corrected before commit. `ba636cdc` |
| 09-debugging (fresh) | 9 | Evidence-first prompt. Root cause: soft-delete test picks its victim with `findAll()`, outside the 30-day window. Also caught that tests use native MySQL 3306, not the 3308 container I assumed. Its inferences confirmed by my SQL. Fix deferred (out of scope) |
| 12-pull-request | 12 | PR body in `sessions/12-pr-body.md`. Write outside cwd was denied (needs --add-dir); extracted from the answer. My check vs diff: counts right; one stale claim (3 vs 2 report failures) and an outdated root cause, fixed |
| 13-ai-review (fresh, plan) | 13 | Found a real should-fix all of us missed: already-paid-at-Stripe → "choose another card". Plus 4 nits. Decisions: fix (a) + DAO doc; decline 4 as follow-ups |
| 13-review-fixes | 13 | 409 for succeeded intents (checks Stripe status, not error wording), 3 tests proven by disabling the fix. `86e819e3`, `9dbe4a68`, `36a2b08c` |
| 14-support (fresh, on main) | 14 | Ticket "checkout forgets my name". Triage/root cause/reply/eng ticket all correct (line refs verified). It could NOT reproduce (no /tmp write) and said so; I had reproduced it earlier by accident. Real bug, not fixed |
| 10-aws (read-only allowlist) | 10 | See AWS below |

### AWS (session 10, verified by me read-only)
The two "unverified" pocsoft leftovers exist, cost ≈ $0, and no DNS points at them. But REST API
`anwkjt5ckf` is fully unauthenticated with its default URL live, and `POST /sushi/turnon-servers`
targets ECS cluster `pocsoft`, still ACTIVE with 3 services. A third leftover (CloudFront
`E3KFWG5MPNJ9CK`) was missing from CLAUDE.md. Root CLAUDE.md updated. **Nothing changed in AWS** —
cleanup order is in `sessions/10-aws.md`. **2026-10-04: ECS cluster `pocsoft` + 3 services deleted on Folau's instruction**; the rest remains.

### Real "accept blind and it ships wrong" cases collected (for post 2)
1. Step 7 docs: plausible wrong root cause + wrong fix ("make seed dates relative").
2. AI review: already-paid order told to "choose another card" — missed by author session AND me.
3. Step 3: test expectation silently-ish changed from the plan (justified, but exactly the pattern).
4. Step 5: div label → no accessible group name.
5. Step 1: unused dependency "for later".
6. PR body: stale numbers after data changed.
And one where the reviewer (me) was wrong: green radios.

**Commit attribution:** the demo repo and this repo have never carried a Co-Authored-By trailer,
and the project CLAUDE.md says not to, so feature commits follow that. Flagged to Folau.

**Pre-existing, out of scope:** 4 backend tests fail on main (`CustomerOrderDAOIntegrationTest.
filtersByStatus`: leftover e2e orders; 3 `ReportServiceImplTest`: seed orders aged out of the 30-day
window). Worth a ticket.

**Needs infra before publish:** `diff` is not a supported code language (backend
`SUPPORTED_LANGUAGES` + frontend Prism import), and this track quotes diffs. Add both in lockstep,
as was done for `swift`.

## Owners
- Content, sessions, tooling: Claude
- Outline sign-off, review, publish: Folau

## Next steps
1. ~~Write posts~~ done. ~~diff language~~ done locally. ~~nav~~ done locally. ~~seed local~~ done.
2. Folau reviews on :3000, then the publish sequence above.
5. PR opened 2026-10-04: https://github.com/folaulau/lovemesomecoding_demo_project/pull/1 (10 commits, pushed at Folau's request). Folau: decide on pocsoft cleanup.
6. Follow-up tickets in the demo app: report tests' victim selection, checkout name/email on reload
   (#3117), the 4 declined review findings, save-card-at-checkout.

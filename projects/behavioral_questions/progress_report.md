# Behavioral Questions track — progress report

**Status:** **LIVE 2026-10-25.** 10 posts seeded to prod (988 posts in the tree, was 978), frontend
deployed (build `c0ff134-dirty`, includes the nav.ts change), all 10 pages + archive return 200.
Nothing committed yet.
**Lands at:** https://lovemesomecoding.com/behavioral-questions

## The ask
> *"i want to add "Behavirial Questions" for non technical questions. Something like "Tell me a
> project you are so proud of" put this series under System Engineering"*

Clarified with Folau (2026-10-25):
| Question | Decision |
|---|---|
| Placement | No "System Engineering" nav group exists. **New category `behavioral-questions` in the "Software Engineering" dropdown**, directly after `system-design`. Kept separate from `soft-skills` (17 skill essays, not interview answers). |
| Scope | **Track of ~10 posts**: intro, story bank, one post per question family. |
| Examples | **Folau's real projects**, from the progress reports in this repo. Nothing invented. |

## The track
| # | slug | answer built from |
|---|---|---|
| 1 | `behavioral-interview-introduction` | (STAR, what's scored, the question families) |
| 2 | `behavioral-story-bank` | worksheet + Folau's 8-story bank and its gaps |
| 3 | `behavioral-proudest-project` | WordPress → AWS migration (`projects/rewrite/`) |
| 4 | `behavioral-failure-and-mistakes` | "12 tutorials" stale index (`projects/oracle/` §9); node_modules + 72 MB pushed (`rewrite` §14) |
| 5 | `behavioral-conflict-and-disagreement` | **skeleton only for people**; real story = the "must double" rule vs the reading cap (`system_design/manifest.py`) |
| 6 | `behavioral-ambiguity-and-tradeoffs` | SEO vs runtime fetch (`rewrite` §4); keeping wrong slugs; cutting comments/TOC pages/image opt |
| 7 | `behavioral-ownership-and-initiative` | pocsoft unauthenticated API (`ai_engineering/sessions/10-aws.md`, root CLAUDE.md); `_reindex` drift (`system_design`); checkers before writing |
| 8 | `behavioral-learning-fast` | RDS MySQL 8.0 → 8.4 drill (`projects/rds-mysql-84-upgrade/`) |
| 9 | `behavioral-leadership-and-feedback` | teaching at scale (this site); **skeletons** for mentoring / giving / receiving feedback |
| 10 | `behavioral-why-this-company` | guidance + questions to ask + night-before checklist; links to `/soft-skills/soft-skills-negotiating-salary` |

Dated one a day, 2026-10-15 → 2026-10-24 (all past; stories are Aug–Oct 2026 so a 2026 date is
the honest one).

## Honesty decisions — Folau should review these
- **Gaps are shown, not filled.** No documented story exists for a conflict with a teammate,
  disagreeing with a manager, mentoring someone, or receiving feedback. Those posts teach the
  shape and give a skeleton; post 5 says plainly that solo projects have no teammates to clash with.
  **If Folau has real work stories for these, they would make the strongest additions.**
- **The coding assistant is named.** The projects were built with Claude doing much of the
  implementation. Post 3's "did you do it alone?" follow-up and a note in post 2 say "I" means the
  decisions, requirements and verification. Post 8 says the drill infrastructure was scripted by an
  assistant and the upgrade was driven by hand (matches the drill's "owner split").
- **Things NOT claimed:** how long the migration took; that the real work upgrade has happened
  (the drill's "carry into work" list is still unchecked); a root cause for `_reindex` (never
  found, and the post says so); a finished pocsoft cleanup (API + Lambda still exist; the post says
  the dangerous part, the ECS cluster, was removed first and the rest is documented).
- Every quoted figure is in `check_content.py` `STORY_FACTS`, mapped to the file that records it,
  and the check fails if the source stops containing it.

## Tooling
- `manifest.py` — category, 10 posts, computed dates, 6–12 min budget. The floor started at 7;
  seven posts landed at 6 having said what they needed, so the floor moved instead of padding.
- `seed.py` — copied from `system_design/seed.py` (same guards: new-slug collision, index verify).
- `check_content.py` — byte-for-byte `<pre>` round-trip, heading anchors, budget, ≥1 plaintext
  block per post, ascending dates, excerpt ≤ 500, STORY_FACTS present in their sources.
- `screenshots/shoot.mjs` — Playwright, against :3000.

## Frontend
`lovemesomecoding_frontend/src/lib/nav.ts`: `'behavioral-questions'` added after `system-design`.
⚠️ That file ALSO carries Folau's uncommitted Android change (`slugs: ['ios', 'android']`). Commit
them together or separately, but commit before the next push to `main`, or CI redeploys without.

## Verification (local)
```
check_content.py   all 10 pass — 1,330–1,689 words, 6–8 min each
seed.py --env local --write   10 created, category count 10, 909 posts in tree, indexes verified
:3000              archive 200 with 10 posts; nav links /behavioral-questions; all 10 posts 200;
                   every internal link in every post resolves 200
screenshots/       archive.png, proudest-project-answer.png (blockquote answers render correctly)
```

## To publish
```
AWS_PROFILE=folau python projects/behavioral_questions/seed.py --env prod --write
cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy     # nav.ts must be in this build
```

## Revision 2026-10-27: Sidecar Health becomes the proudest-project story

Folau supplied their own proudest-project story (Sidecar Health: provider ratings, reviews and prices
for members). It replaces the WordPress migration as the worked answer in post 03; the migration
stays in the bank as story 2 (best trade-off story, second proudest-project choice) and still
drives posts 04 and 06.

- Original account saved verbatim in `stories/sidecar-health.md`; `40%` added to `STORY_FACTS`
  against it.
- Corrected in the telling: "not allowed by law" now applies to prices only (reviews were never
  illegal); the law is "federal price transparency rules" until Folau names the specific one.
- Not invented: Folau's own part, the hard problem and choice, team size, any result number. Post 03
  shows the answer as given and adds a "What would make it stronger" section that names exactly
  these gaps as the lesson. When Folau supplies them, rewrite the Action/Result paragraphs and trim
  that section.
- Knock-on edits: post 01 (sources of examples), post 02 (bank now 9 stories, "I"/assistant note
  scoped to stories 2-9), post 04 ("same migration" no longer has an antecedent), manifest excerpt.
- Same day, Folau supplied the missing pieces (saved verbatim in the story file): owned the backend,
  team of three (backend, front-end, QA), MySQL 5.7 full-text search too slow, learned
  Elasticsearch, built a POC, demoed it, moved searchable data into ES. Action/Result rewritten;
  "What would make it stronger" cut to the one gap left: no result number. Bank row 1 now also
  marks OWNER and LEARN. `MySQL 5.7` and `team of three` added to STORY_FACTS.
- LIVE 2026-10-27: posts 01-04 re-seeded to prod, frontend deployed (build `c0ff134-dirty`).

## Revision 2026-10-27: startup MVP story added to the ownership post

Folau supplied an "above and beyond" story (startup MVP, backend engineer who helped the
overwhelmed front-end team after finishing their own work). Saved verbatim in
`stories/mvp-frontend-help.md`. It is now worked answer 1 in post 07 (the others renumbered 2-4),
with "Why it works" and "What would make it stronger" (front-end stack, features, one concrete
bug, whether the seed round closed; the "was that sustainable?" probe). Company: Sidecar Health,
confirmed by Folau after first publish and updated the same day. Bank: story 10, OWNER ## / LEARN #. Post 01 and 02 wording, manifest
excerpt updated. LIVE 2026-10-27 (posts 01, 02, 07 re-seeded to prod, frontend deployed).

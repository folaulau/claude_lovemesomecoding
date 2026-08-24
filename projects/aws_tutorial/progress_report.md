# AWS tutorial track — progress report

**Status:** ✅ **STAGE 1 WRITTEN AND VERIFIED ON LOCAL** — 7 blank posts rewritten, 6,397 words
replacing 0. Seeded to the `local` tree and built clean. **Prod is untouched, awaiting review.**
**Started:** 2026-08-24
**Where it lands:** https://lovemesomecoding.com/aws

---

## What is there now

33 published posts, measured off the **prod** content tree synced 2026-08-24
(`scripts/sync-content.sh`). No drafts. No redirects touch `/aws`.

| slug | date | prose words | code | headings | imgs | WP cruft |
|---|---|---:|---:|---:|---:|---:|
| `aws-ecs` | 2018-10-30 | 39 | 5 | 0 | 0 | 9 |
| `aws-lambda-to-start-an-ec2-instance` | 2019-04-22 | 29 | 4 | 0 | 0 | 0 |
| `aws-lambda-to-start-an-rds-instance` | 2019-04-22 | **0** | 0 | 0 | 0 | 0 |
| `aws-lambda-to-stop-an-ec2-instance` | 2019-04-22 | 37 | 5 | 0 | 0 | 7 |
| `aws-lambda-to-stop-an-rds-instance` | 2019-04-22 | **0** | 0 | 0 | 0 | 0 |
| `aws-alexa` | 2019-08-05 | **0** | 0 | 0 | 0 | 0 |
| `aws-api-gateway` | 2019-08-05 | 105 | 0 | 0 | 1 | 0 |
| `aws-cli` | 2019-08-05 | 122 | 6 | 1 | 0 | 12 |
| `aws-cloudformation` | 2019-08-05 | **0** | 0 | 0 | 0 | 0 |
| `aws-cloudfront` | 2019-08-05 | 641 | 0 | 1 | 2 | 13 |
| `aws-cloudwatch` | 2019-08-05 | 386 | 3 | 0 | 3 | 20 |
| `aws-codebuild` | 2019-08-05 | 110 | 0 | 0 | 1 | 11 |
| `aws-codecommit` | 2019-08-05 | 204 | 0 | 0 | 0 | 0 |
| `aws-codedeploy` | 2019-08-05 | **0** | 0 | 0 | 0 | 0 |
| `aws-codepipeline` | 2019-08-05 | 590 | 4 | 0 | 2 | 37 |
| `aws-dynamodb` | 2019-08-05 | 610 | 4 | 0 | 0 | 0 |
| `aws-ec2` | 2019-08-05 | 653 | 0 | 0 | 0 | 0 |
| `aws-elasticache` | 2019-08-05 | 2184 | 0 | 0 | 4 | 0 |
| `aws-elasticbeanstalk` | 2019-08-05 | 161 | 0 | 0 | 1 | 0 |
| `aws-iam` | 2019-08-05 | 1006 | 0 | 0 | 3 | 0 |
| `aws-kinesis` | 2019-08-05 | **0** | 0 | 0 | 0 | 0 |
| `aws-kms-and-ecryption` | 2019-08-05 | 234 | 0 | 0 | 3 | 0 |
| `aws-lambda` | 2019-08-05 | 828 | 1 | 0 | 1 | 14 |
| `aws-load-balancer` | 2019-08-05 | 617 | 0 | 0 | 6 | 0 |
| `aws-rds` | 2019-08-05 | 534 | 4 | 0 | 0 | 15 |
| `aws-route-53` | 2019-08-05 | 254 | 0 | 0 | 0 | 0 |
| `aws-s3` | 2019-08-05 | 1037 | 13 | 0 | 1 | 36 |
| `aws-ses` | 2019-08-05 | 1246 | 2 | 0 | 5 | 0 |
| `aws-sns` | 2019-08-05 | 222 | 5 | 0 | 0 | 0 |
| `aws-sqs` | 2019-08-05 | 760 | 10 | 0 | 1 | 24 |
| `aws-secrets-manager` | 2019-08-07 | 184 | 6 | 0 | 0 | 11 |
| `aws-aurora` | 2019-08-21 | 738 | 0 | 0 | 2 | 0 |
| `aws-kubernetes-on-aws` | 2019-09-06 | **0** | 0 | 0 | 0 | 0 |
| **total** | | **13,531** | **72** | **2** | **36** | |

Note the misspelled slug `aws-kms-and-ecryption` (*ecryption*). It is a live indexed URL —
see "The slugs are frozen" below.

### Six defects

1. **Seven posts are completely empty** — 0 prose words, 0 code, nothing:
   `aws-alexa`, `aws-cloudformation`, `aws-codedeploy`, `aws-kinesis`, `aws-kubernetes-on-aws`,
   `aws-lambda-to-start-an-rds-instance`, `aws-lambda-to-stop-an-rds-instance`.
   All seven are `status: published` and all seven serve a blank page today.

2. **Two headings across the entire 33-post collection.** `toc` is empty on 32 of 33, so there
   is no table of contents and no deep links anywhere in `/aws`.

3. **The prose is copied AWS marketing blurb, not a tutorial.** `aws-lambda` opens with the
   verbatim "lets you run code without provisioning or managing servers… Just upload your code
   and Lambda takes care of everything" product-page paragraph. `aws-ec2` and `aws-elasticache`
   do the same. This is the opposite of what CLAUDE.md says the site is for, and it is
   duplicate content against aws.amazon.com for SEO.

4. **WordPress `boldgrid-section` / `container` / `row` / `col-md-12` wrappers and `class=""`**
   survive on 14 posts — dead Bootstrap markup from the old theme.

5. **12 of 36 images hotlink to AWS's own domains** — 10 to `docs.aws.amazon.com`, 2 to
   `d1.awsstatic.com`. AWS reorganizes those paths without notice; they are already a latent
   broken-image bug and they are not ours to serve. The other 24 are on our media CDN.

6. **The category record is broken** — `{"slug": "aws", "name": "AWS", "description": ""}`.
   No standfirst on the archive page. (Name is at least correct here, unlike `/postgre`.)

Plus, outside the posts themselves:

7. **`/aws-table-of-content` is a page of dead links.** 28 of its 29 `href`s are old WordPress
   query strings — `/index.php?name=aws-iam&category=aws`. Every one of them 404s today. The
   page is live and `status: published`.

### The slugs are frozen

All 33 are live, indexed URLs. `scripts/verify-build.mjs` check 1 fails the frontend build if
any URL in `index/posts.json` stops resolving, so every post is **rewritten in place**.
Renaming `aws-kms-and-ecryption` to fix the typo is a dead link, not a refactor — if the typo
is worth fixing it needs a redirect in `postbuild.mjs` *and* a CloudFront Function republish.

Dates are sticky: `upsert_post` never overwrites an existing date, and all 33 already have one.
Seeding therefore needs `--force-dates` whenever a manifest date moves — **and it is not a
one-off**, per the correction the FastAPI track established.

### Navigation — nothing to do

`src/lib/nav.ts:28` already lists `aws` in the **DevOps** group and `:61` maps it to the display
name `AWS`. Only the stored category record needs fixing, via `upsert_category`.

---

## Sources

The README names no source, unlike the Postgres track. Proposed spine:

- https://docs.aws.amazon.com — per-service developer guides, the authority on current behaviour
- https://docs.aws.amazon.com/whitepapers/latest/aws-overview/ — what belongs in a "get to
  production" filter
- This site's own infrastructure (see below), which is the part that is genuinely first-hand

Filter, from the README: *"keep content to the point and not too lengthy if they don't have to."*

---

## Two things that make 2019 content actively wrong

**AWS CodeCommit closed to new customers on 2024-07-25.** Only accounts with an existing
repository can create more. AWS recommends GitHub/GitLab/CodeCatalyst instead. A 2026 tutorial
that teaches a reader to "create a CodeCommit repository" sends them to a wall — the console
refuses. `aws-codecommit` cannot be a straight rewrite; it has to become a "this is closed, here
is what to use and how to migrate" post, or a redirect.

**`aws-alexa` is not an AWS service post.** The Alexa Skills Kit lives on the Amazon Developer
portal, not in the AWS console, and it does not belong in a track about shipping a backend to
production. It is also one of the seven empty posts, so there is no existing content to preserve.

Both are called out as decisions below rather than settled unilaterally, because both slugs are
frozen and the choice is a product call.

---

## Raw material we already own

Unlike the Postgres track, this one does not need an invented example — **lovemesomecoding.com
is itself a non-trivial AWS deployment**, documented in CLAUDE.md and running in the `folau`
account:

| post | first-hand material already in this account |
|---|---|
| `aws-s3` | site bucket, private + OAC only; the `sync`-skips-metadata trap |
| `aws-cloudfront` | dist `E30YUPLP37MY9U`, OAC, a CloudFront Function doing 41 redirects |
| `aws-lambda` | `lovemesomecoding-admin-api-prod`, FastAPI + Mangum, the manylinux wheel trap |
| `aws-api-gateway` | the `$default`-stage-vs-custom-domain 404 trap |
| `aws-cloudformation` | the SAM stack, and CFN keeping the previous value for an omitted param |
| `aws-iam` | the OAC bucket policy, the CI deploy user |
| `aws-route-53` | zone `Z000531818AC6P1IJ8LJL`, ALIAS records, the 60s-TTL rollback plan |
| `aws-cli` | `--profile folau`, `--exact-timestamps`, `--metadata-directive REPLACE` |

Every one of those "gotchas" in CLAUDE.md is a paragraph someone else will search for. That is
the differentiator against the AWS docs, and it costs nothing to run because it already runs.

The four demo apps (`stayhub`, `pizza`, `bank`, `reelcms`) cover the app-side services —
`stayhub` is FastAPI + Postgres + Hasura and maps onto RDS/Aurora, ECS, ALB, ElastiCache.

---

## Decisions — 2026-08-24

| # | Question | Decision |
|---|---|---|
| 1 | Verification | **Validate every CLI sample against botocore offline.** No account touched, nothing billed. |
| 2 | Dead-end services | **Rewrite in place as "this is closed — use X".** Both URLs keep serving, no redirect machinery. |
| 3 | Post length | **Short — 4–6 reading-minutes**, ~800–1,200 words total. |
| 4 | Scope | **Staged.** The 7 blank posts first, then the remaining 26. |
| 5 | Dates | **Keep the stored 2018–2019 dates.** Decided here, not asked — see below. |

### Why botocore, and what it actually proves

The AWS CLI ships its entire API surface as data: `botocore` carries a service model for each of
403 services listing every operation and every parameter. The CLI derives its own command and flag
names from that model by `xform_name`, so the mapping is exact and reversible:

    CreateBucket               -> aws s3api create-bucket
    ObjectLockEnabledForBucket -> --object-lock-enabled-for-bucket
    ACL                        -> --acl          (not --a-c-l; xform_name knows acronyms)

So for any `aws …` line in a post we can prove **the service exists, the operation exists on it,
and every flag is a real parameter of that operation** — offline, in milliseconds, against the
same data the installed CLI uses. Local versions: `aws-cli/2.32.24`, `botocore 1.35.99`.

That is not "does it parse". It is precisely the failure mode of seven-year-old cloud content:
an operation that was renamed, a flag that was dropped, a service that moved. It is the AWS
analogue of what `check_sql.py` does for the Postgres track.

**What it does not prove**, stated plainly so nobody trusts it further than it goes:

- Not that the command *succeeds* — no IAM permission, quota, or account state is consulted.
- Not that argument *values* are valid; only that the flags are real.
- Not the CLI's own high-level commands. `aws s3 cp|sync|ls|mb`, `cloudformation deploy|package`,
  `ecr get-login-password` and friends are CLI customizations with no botocore operation behind
  them. Those get an explicit declared allowlist of permitted flags, so a made-up flag on
  `aws s3 sync` still fails — it just fails against a table we maintain rather than against the
  model. The allowlist is small and lives in `check_aws.py`.
- Nothing about the console click-paths, IAM policy semantics, or CloudFormation templates.
  Templates are checked separately by parsing them and asserting required keys.

### Why the dates stay

All 33 posts carry stored dates from 2018-10 to 2019-09 that already ascend cleanly, and every one
is an indexed URL. The Postgres track re-based its dates because it was a *new* track being
authored before publication; this one is a rewrite of a published archive. Re-stamping 33 indexed
posts buys nothing and moves 33 URLs in the sitemap at once, so `START_DATE` and `--force-dates`
are deliberately **not** part of this track. `modified` updates on its own through `upsert_post`.

If that turns out to be wrong, it is one flag on `seed.py` to reverse.

### Stage 1 — the seven blanks

The bug worth fixing first: seven published posts serve an empty page today.

| slug | becomes |
|---|---|
| `aws-cloudformation` | infrastructure as code, against this site's own SAM stack |
| `aws-codedeploy` | where CodeDeploy still fits in 2026, and where it does not |
| `aws-kinesis` | streams vs Firehose vs SQS — which one you actually want |
| `aws-kubernetes-on-aws` | EKS, and the honest "do you need this yet" answer |
| `aws-alexa` | short: skills live on the Amazon Developer portal, not AWS. Points onward. |
| `aws-lambda-to-start-an-rds-instance` | the scheduled start/stop pattern, done properly |
| `aws-lambda-to-stop-an-rds-instance` | the stop half, plus the 7-day auto-restart gotcha |

---

## Stage 1 — done

Seven posts that served a blank page now carry 6,397 words, 45 headings and 30 code samples
between them. Measured through the backend's own `normalize`, so these are the published numbers:

| slug | words | min | prose | headings | blocks | was |
|---|---:|---:|---:|---:|---:|---:|
| `aws-lambda-to-start-an-rds-instance` | 919 | 4 | 83% | 6 | 4 | 0 |
| `aws-lambda-to-stop-an-rds-instance` | 917 | 4 | 79% | 7 | 5 | 0 |
| `aws-alexa` | 920 | 4 | 90% | 6 | 4 | 0 |
| `aws-kinesis` | 896 | 4 | 90% | 6 | 5 | 0 |
| `aws-codedeploy` | 904 | 4 | 93% | 7 | 3 | 0 |
| `aws-cloudformation` | 904 | 4 | 85% | 6 | 5 | 0 |
| `aws-kubernetes-on-aws` | 937 | 4 | 97% | 7 | 4 | 0 |
| **total** | **6,397** | | **88%** | **45** | **30** | **0** |

Verified: `check_content.py` clean, `check_aws.py` clean over 28 samples (20 CLI commands, 3 CLI
customizations, 1 waiter, 2 IAM policies, 2 templates), seeded to `local`, all seven rendering at
`localhost:3000` with anchored headings and Prism highlighting, and a full production build with
`verify-build.mjs` reporting **708/708 post URLs served** and all indexed URLs accounted for.

The archive now carries a standfirst; it was an empty string before.

### What the checker caught that review would not have

Worth recording, because it is the argument for having built it:

1. **`aws deploy` is CodeDeploy.** The CLI command is `aws deploy`; botocore calls the service
   `codedeploy`. The commands in the post were right and the alias table was wrong — reported as
   "no such service" until fixed. `SERVICE_ALIASES` now also asserts at startup that every alias
   target exists, after `iot-data -> iot-data-plane` was added as a guess and was wrong.
2. **`cloudfront create-invalidation --paths` and `eks update-kubeconfig` are CLI conveniences**
   with no matching API shape, so a strict model-based validator rejects both. Found by the
   self-test, not by reading source.
3. **The Firehose naming split.** The docs say "Amazon Data Firehose" and "Firehose stream"; the
   service model still says "Amazon Kinesis Firehose" and every operation is still
   `*-delivery-stream`. That detail is in the Kinesis post because the model was checked.

Two bugs in the tooling itself were found by using it, and both now have regression tests:

- **The shell splitter cut through quoted strings.** `re.split(r'\||&&|;')` broke
  `--data "$(echo -n '{"a":1}' | base64)"` in half and shlex then reported "No closing quotation"
  on a correct sample. Replaced with a scanner that tracks quotes and `$( )` depth.
- **The account-id rule flagged a UUID.** The last group of a UUID is twelve hex characters, so
  an all-numeric example skill id tripped the no-account-numbers rule. A false positive on a
  safety rule is how a safety rule gets switched off. Matches inside a UUID are now skipped —
  but `my-bucket-123456789012` still fails, because that is a real way an account id leaks.

---

## Still to do

- [ ] **Stage 2 — the remaining 26 posts.** All are rewrites of live URLs; the tooling is built
      and the pattern is set. The worst are `aws-api-gateway` (105 words), `aws-codebuild` (110),
      `aws-cli` (122) and `aws-elasticbeanstalk` (161).
- [ ] **Seed stage 1 to prod and deploy** — held for review. One command each, below.
- [ ] **`/aws-table-of-content` is 28 dead WordPress links.** Not a post, so no tooling here
      touches it. It needs either a rewrite pointing at the real `/aws/...` URLs or a redirect
      to `/aws`, which the archive already does better. Decide before stage 2 ships.
- [ ] **12 hotlinked images on the 26 unwritten posts** point at `docs.aws.amazon.com` and
      `d1.awsstatic.com`. `check_content.py` rule 8 fails any post that keeps one, so this
      resolves itself as stage 2 proceeds — noted so it is not a surprise.

---

## Log

- **2026-08-24** — Synced prod content, audited all 33 posts, wrote this report. Nothing seeded.
- **2026-08-24** — Decisions taken (botocore validation, rewrite-in-place for closed services,
  4-6 minutes, staged). Built `manifest.py`, `check_content.py`, `check_aws.py`, `seed.py` and
  `tests/test_check_aws.py`. Wrote all seven stage-1 posts. Seeded `local` only; verified in the
  dev server and through a full production build. Prod untouched.

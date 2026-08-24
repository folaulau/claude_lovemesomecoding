# AWS Tutorial

## About
- this tutorial is for the AWS tutorial

## Requirements
- update aws posts on https://lovemesomecoding.com/aws
- keep posts to the point.
- update all posts in the tutorial.
- update posts and keep content to the point and not too lengthy if they don't have to.

---

## What is here

```
projects/aws_tutorial/
  manifest.py            category metadata + one entry per post (slug, title, date, tags, excerpt)
  posts/NN-slug.html     the post bodies, plain semantic HTML
  check_content.py       the HTML round-trips, and this track's own length/prose/safety rules
  originals/             snapshot of the 33 original bodies, so a rewrite can be proved to be one
  check_aws.py           VALIDATES every `aws …` command against the botocore service model
  tests/test_check_aws.py  proves check_aws actually catches things
  seed.py                writes the category and posts into a content tree
  progress_report.md     status, decisions, and the bugs worth not repeating
```

## The track

34 posts at `/aws/{slug}`, 4–6 reading-minutes each, dated **2024-01-09 → 2025-12-02**.

33 are rewrites of live indexed URLs; **`aws-ecr` is the one genuinely new post**, added because
the collection covered ECS and EKS but nothing on the registry both pull from.

⚠️ **All 33 slugs are live, indexed URLs.** There are no new posts in this track — it is a rewrite
of a published archive. `scripts/verify-build.mjs` fails the frontend build if any indexed post URL
stops resolving, so every post is rewritten **in place**. A slug that leaves `manifest.py` is a 404
on a page Google already has.

That includes `aws-kms-and-ecryption`, which is misspelled and staying that way.

⚠️ **`--force-dates` is REQUIRED, and it is not a one-off.** The dates are computed from
`START_DATE` + `STEP_DAYS` in `manifest.py`, but all 33 posts were published in 2018-2019 and
`upsert_post` never overwrites an existing date. So a plain seed moves nothing at all — every post
silently keeps its 2019 date while the manifest claims 2024. Pass it on any seed that changes a
date, and again after any change to `START_DATE`.

(An earlier version of this track kept the 2019 dates and deliberately had no such flag. That was
reversed; `progress_report.md` records both sides.)

### State

**All 33 posts are written and verified.** 30,445 words replacing 16,481; 151 headings replacing 2.

| | before | after |
|---|---:|---:|
| posts | 33 | 34 |
| words | 16,481 | 31,977 |
| headings | 2 | 168 |
| blank posts | 7 | 0 |
| code samples | 72 | 169 |

**Published 2026-08-25.** All 34 live at https://lovemesomecoding.com/aws.

`/aws/aws-eks` redirects to `/aws/aws-kubernetes-on-aws` — the post is about EKS but carries the
old WordPress slug, so the obvious URL had to resolve.

## Commands

Run from the repo root. The checks need no AWS credentials; `seed.py` does.

```bash
# the HTML round-trips, and the track's length/prose/safety rules hold
lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/check_content.py

# every `aws` command is a real command, offline, against the botocore model
lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/check_aws.py
lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/check_aws.py --post aws-kinesis --verbose

# prove the checker still catches planted errors
lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/tests/test_check_aws.py

# re-take the "before" snapshot (only if the live posts change, which they should not)
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python \
  projects/aws_tutorial/originals/snapshot.py

# dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/seed.py --env local
```

Seeding. `--force-dates` is not optional here — see above:

```bash
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/seed.py \
  --env local --write --force-dates

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/seed.py \
  --env prod  --write --force-dates
```

`--only slug-a,slug-b` seeds a subset. Every slug here is already live, so a partial seed leaves
no half-built archive — it just updates fewer posts.

Then deploy:

```bash
cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy
```

## What check_aws.py actually does

More than "does it parse". The AWS CLI generates its whole command surface from `botocore`, which
ships a model of every service, operation and parameter, and derives the names by `xform_name`:

```
CreateBucket               ->  aws s3api create-bucket
ObjectLockEnabledForBucket ->  --object-lock-enabled-for-bucket
ACL                        ->  --acl        (not --a-c-l — xform_name knows acronyms)
```

That mapping is exact, so for any `aws …` line we prove **the service exists, the operation exists
on it, and every flag is a real parameter of that operation** — offline, in milliseconds, with no
credentials and nothing billed. It is the AWS analogue of the Postgres track's `check_sql.py`, and
it targets exactly how old cloud content is wrong: a renamed operation, a dropped flag, a moved
service, in a sample that still looks perfect.

It also parses every JSON and YAML block, checks IAM policy statements have a valid `Version` and
an `Effect`, and checks CloudFormation resources have a `Type`.

| kind | handling |
|---|---|
| `aws <service> <operation>` | operation and every flag checked against the service model |
| `aws <service> wait <name>` | waiter name checked against the service's waiter model |
| CLI customizations | `aws s3 cp\|sync\|ls`, `cloudformation deploy\|package`, `ecr get-login-password`, `eks update-kubeconfig` — no API operation exists, so flags come from a declared allowlist in `check_aws.py` |
| `EXTRA_FLAGS` | operations where the CLI adds a convenience flag on top of the API shape, e.g. `cloudfront create-invalidation --paths` |
| `json` / `yaml` blocks | parsed; IAM policies and CFN templates additionally shape-checked |

### What it does NOT prove

Stated plainly so nobody trusts it further than it goes:

- **Not that the command succeeds.** No account, permission, quota or resource state is consulted.
- **Not that argument values are valid.** `--instance-type banana` passes; `--instance-typo` fails.
- **Not `sam`, `eksctl`, `kubectl` or `ask` commands** — only lines beginning `aws`.
- Nothing about console click-paths or IAM policy semantics.

## Editing a post later

```bash
lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/check_content.py
lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/check_aws.py --post <slug>
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/seed.py \
  --env prod --only <slug> --write
cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy
```

Editing through `/admin` works too, but the TipTap editor will not round-trip the raw HTML in these
files, so the file here would then be stale. Pick one source of truth per post.

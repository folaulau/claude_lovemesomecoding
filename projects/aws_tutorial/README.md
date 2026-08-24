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
  check_aws.py           VALIDATES every `aws …` command against the botocore service model
  tests/test_check_aws.py  proves check_aws actually catches things
  seed.py                writes the category and posts into a content tree
  progress_report.md     status, decisions, and the bugs worth not repeating
```

## The track

33 posts at `/aws/{slug}`, 4–6 reading-minutes each, dated 2018-10-30 → 2019-09-06.

⚠️ **All 33 slugs are live, indexed URLs.** There are no new posts in this track — it is a rewrite
of a published archive. `scripts/verify-build.mjs` fails the frontend build if any indexed post URL
stops resolving, so every post is rewritten **in place**. A slug that leaves `manifest.py` is a 404
on a page Google already has.

That includes `aws-kms-and-ecryption`, which is misspelled and staying that way.

⚠️ **There is no `--force-dates`, deliberately.** The dates in `manifest.py` are *transcribed* from
the stored posts rather than computed from a `START_DATE`, and `upsert_post` never overwrites an
existing date — which is exactly what we want on a published archive. A re-seed cannot reshuffle
it. This is the opposite of the Postgres and FastAPI tracks; see `progress_report.md`.

### Progress

| stage | posts | state |
|---|---|---|
| 1 | the 7 that served a **blank page** | ✅ written, verified, seeded to `local` |
| 2 | the other 26 | ⬜ not started |

Stage 1: `aws-alexa`, `aws-cloudformation`, `aws-codedeploy`, `aws-kinesis`,
`aws-kubernetes-on-aws`, `aws-lambda-to-start-an-rds-instance`, `aws-lambda-to-stop-an-rds-instance`.

**Prod has not been seeded.** Stage 1 is on `local` only, pending review.

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

# dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/seed.py --env local
```

Seeding a stage (`--only` takes a comma-separated slug list):

```bash
STAGE1=$(lovemesomecoding_backend/.venv/bin/python -c \
  "import sys;sys.path.insert(0,'projects/aws_tutorial');import manifest;print(','.join(manifest.STAGE_1))")

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/seed.py \
  --env local --only "$STAGE1" --write

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/seed.py \
  --env prod  --only "$STAGE1" --write
```

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

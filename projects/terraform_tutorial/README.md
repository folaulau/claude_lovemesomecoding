# Terraform Tutorial

## About
- this tutorial is for the Terraform Tutorial.

## Requirements
- update posts on https://lovemesomecoding.com/terraform collection.
- keep posts to the point
- Use https://developer.hashicorp.com/terraform/tutorials and https://www.tutorialspoint.com/devops/devops-terraform.htm to generate main topics and posts. We don't need to create a post for each small things. We just need the most important topics to cover.
- use this project /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend to write a script to deploy it to ECS in AWS and set up a CI/CD pipeline in github action. Then use that script as an example

---

## Layout

```
projects/terraform_tutorial/
  manifest.py           category metadata + one entry per post (slug, title, date, tags, excerpt)
  posts/NN-slug.html    the post bodies, plain semantic HTML
  seed.py               writes the category and posts into a content tree
  check_content.py      the HTML round-trips, and this track's length/prose rules
  check_hcl.py          VALIDATES every HCL block against the real provider schema
  infra/                the ECS stack itself — applied to AWS, verified, destroyed
  progress_report.md    status, decisions and the bugs worth not repeating — READ FIRST
```

## The track

16 posts at `/terraform/{slug}`, dated 2026-07-10 → 2026-08-24.

⚠️ **Three slugs are live, indexed URLs** — `terraform-introduction`, `terraform-fundamentals` and
`terraform-with-aws`. Two of the three have served the literal string "Coming soon…" since 2019.
They are rewritten **in place**; a slug that leaves `manifest.py` is a 404 on a page Google already
has. `scripts/verify-build.mjs` fails the frontend build if any indexed post URL stops resolving.

⚠️ **Post dates must fall between 2024 and 2026.** Dates are computed from `START_DATE` in
`manifest.py`, and `_date()` **raises** if a re-base would walk any lesson out of that window — so
the rule is enforced rather than remembered.

### Progress

See `progress_report.md` for the live status table. It is the shared context; this file is the
standing instructions.

## Versions

Written against **Terraform 1.15.9** and **AWS provider 6.61.0**.

⚠️ `terraform` on this machine is `~/bin/terraform`, **not** Homebrew's. `brew upgrade terraform`
fails here with an unrelated `Your Xcode (15.4) … is too outdated` error; the binary was installed
from HashiCorp's official release, checksum-verified, into `~/bin`, which is first on `PATH`.
Do not spend time re-trying the Homebrew upgrade — the blocker is Xcode, not Terraform.

## Commands

Run from the repo root. The two `check_*` scripts need no AWS credentials; `seed.py` does.

```bash
# the HTML round-trips, and the track's rules hold
lovemesomecoding_backend/.venv/bin/python projects/terraform_tutorial/check_content.py

# every HCL block is real Terraform, offline, against the pinned provider schema
python3 projects/terraform_tutorial/check_hcl.py
python3 projects/terraform_tutorial/check_hcl.py --post terraform-with-aws -v

# the applied stack itself: validate + fmt across the root and every module
python3 projects/terraform_tutorial/check_hcl.py --infra

# dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/terraform_tutorial/seed.py --env local
```

Run **both** checks. They prove different things, and only `check_hcl.py` goes stale on its own —
when a provider release renames an argument, the HTML still round-trips perfectly.

Seeding:

```bash
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/terraform_tutorial/seed.py \
  --env local --write

# ⚠️ --force-dates is REQUIRED on the first prod publish. See below.
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/terraform_tutorial/seed.py \
  --env prod --write --force-dates
```

Then deploy:

```bash
cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy
```

### `--force-dates`

`upsert_post` never overwrites an existing post's `date`. All three rewritten slugs were published
2019-07-09, so without this flag they keep that timestamp and **lessons 1, 2 and 12 sort to the
back of the archive** — exactly backwards.

Unlike the Docker track, this is **not** a one-off to be used once and then forbidden. Dates here
are *computed* from `START_DATE`, so re-basing the track is an intended operation and the flag is
whatever a manifest date change requires. (The AWS track is the opposite case: its dates are
transcribed from a published archive and must never move.)

## What `check_hcl.py` actually does

More than "does it parse". It writes each HCL block into a throwaway module pinned to
`hashicorp/aws ~> 6.0` and runs `terraform validate` against the **real downloaded provider
schema**, so for every block it proves the resource type exists, the arguments exist on that
resource, and the nested block types are allowed — offline, in milliseconds, no credentials,
nothing billed.

That is precisely how old infrastructure content rots: an argument is renamed, a resource moves, a
block type is removed, and the sample still looks perfect.

Blocks are reported in three states:

| state | meaning |
|---|---|
| `ok` | validated clean |
| `fragment` | only failed on references to things defined in another block or lesson — the normal shape of a quoted snippet. Reported, does not fail. |
| `FAIL` | the provider rejected something it knows about: unknown argument, unknown resource type, removed block. **This is rot.** |

Undeclared `var.x` and `local.x` references are synthesised before validating, so a snippet that is
honest apart from its inputs comes out `ok` rather than `fragment`.

### What it does NOT prove

- **Not that `apply` succeeds.** No account, permission, quota or resource state is consulted.
- **Not that argument values are valid.** `instance_class = "banana"` passes; `instance_clas` fails.
- Nothing about whether the resulting infrastructure is reachable, correct or secure.

## The ECS stack

`infra/` holds the real thing — VPC, RDS, ECR, Fargate service and ALB — and it was **applied,
verified through the load balancer, and destroyed**. See `infra/README.md` for the run book and
`progress_report.md` for what it cost and what broke.

⚠️ It bills about **$0.13/hour** while up. `terraform destroy` is not optional.

## Editing a post later

```bash
lovemesomecoding_backend/.venv/bin/python projects/terraform_tutorial/check_content.py
python3 projects/terraform_tutorial/check_hcl.py --post <slug>
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/terraform_tutorial/seed.py \
  --env prod --only <slug> --write
cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy
```

Editing through `/admin` works too, but the TipTap editor will not round-trip the raw HTML in these
files, so the file here would then be stale. Pick one source of truth per post.

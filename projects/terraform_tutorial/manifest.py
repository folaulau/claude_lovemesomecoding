"""The Terraform track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and the last lesson is the
newest.

Dates are COMPUTED from START_DATE + STEP_DAYS rather than hand-written, because
this track is authored before it is published: when the publish date is finally
known, move START_DATE and every lesson re-bases in order.

Three slugs here are not new. `terraform-introduction`, `terraform-fundamentals`
and `terraform-with-aws` were published 2019-07-09 and their URLs are indexed.
Two of the three have served the literal string "Coming soon…" ever since. They
are being rewritten in place, NOT replaced — changing those slugs changes live
URLs.

Because all three carry a 2019 date and `upsert_post` never overwrites an
existing date, the first prod seed needs `seed.py --force-dates` for the reading
order to come out right. Dates here are computed, so a re-base is an intended
operation rather than a one-off. See progress_report.md.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "terraform",
    "name": "Terraform",
    "description": (
        "Terraform from the ground up — the plan/apply loop, HCL, providers and state, "
        "variables, modules and remote state, then deploying a real Spring Boot API to AWS "
        "ECS Fargate behind a load balancer with a GitHub Actions pipeline. Written against "
        "Terraform 1.15 and AWS provider 6.x, and every stack in it was applied to a real "
        "account before it was written about."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, which already lists
# `terraform` under DevOps with the display name "Terraform" — nothing to add
# there. Only the stored category record above needs fixing; it currently has a
# lowercase name and an empty description.
NAV_GROUP = "DevOps"

# The app the AWS lessons deploy. Per the README: "use this project
# pizza-springboot-backend to write a script to deploy it to ECS in AWS and set
# up a CI/CD pipeline in github action. Then use that script as an example".
DEMO_APP = "lovemesomecoding_demo_project/pizza/pizza-springboot-backend"

# The versions the whole track is written against. Lesson 1 prints this table,
# and every other lesson assumes it.
#
# These are READ OFF THIS MACHINE, not chosen — `terraform version`, `aws
# --version`, and the provider version the lock file resolved to.
#
# ⚠️ Terraform 1.15.9 is NOT the Homebrew one. `brew upgrade terraform` fails on
# this machine with an unrelated Xcode version check; the binary was installed
# from HashiCorp's official release, checksum-verified, into ~/bin, which is
# ahead of /opt/homebrew/bin on PATH. See progress_report.md.
VERSIONS = {
    "terraform": "1.15.9",
    "aws provider": "6.61.0",
    "aws cli": "2.32.24",
    "region": "us-west-2",
}

# What the deployed app itself is built from, quoted by the AWS lessons.
APP_VERSIONS = {
    "java": "21 (Spring Boot 4.1.0)",
    "mysql": "8.4 (RDS)",
    "runtime": "ECS Fargate, 0.5 vCPU / 1 GB",
}

# Every AWS resource this track creates carries this prefix and this tag, so a
# `destroy` is provably complete and nothing collides with the three unrelated
# ECS clusters already in the account (learnmymath-api, development, pocsoft).
RESOURCE_PREFIX = "pizza-tf"
RESOURCE_TAGS = {"Project": "terraform-tutorial", "ManagedBy": "terraform"}

# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later,
# so the pager reads lesson 1 -> lesson 16. Re-base the whole track by editing
# these two values; nothing else needs to change.
#
# As computed below this track runs 2026-07-10 -> 2026-08-24.
START_DATE = datetime(2026, 7, 10, 9, 0, 0)
STEP_DAYS = 3

# ⚠️ Every post date must land inside this window — Folau's rule, 2026-08-24.
#
# It is enforced at import time rather than written down and hoped for, because
# the dates are COMPUTED: moving START_DATE re-bases all 16 at once, and a
# re-base that walked the last lesson into 2027 would otherwise be found by a
# reader rather than by a check. `_date()` raises on the way out, so seed.py,
# check_content.py and anything else that imports this module all inherit it.
DATE_WINDOW = (datetime(2024, 1, 1), datetime(2026, 12, 31, 23, 59, 59))


def _date(index: int) -> str:
    """The publish timestamp for the index-th lesson, 0-based."""
    stamp = START_DATE + timedelta(days=STEP_DAYS * index)
    lo, hi = DATE_WINDOW
    if not lo <= stamp <= hi:
        raise ValueError(
            f"lesson {index + 1} would publish {stamp:%Y-%m-%d}, outside the allowed window "
            f"{lo:%Y-%m-%d}..{hi:%Y-%m-%d}. Move START_DATE or reduce STEP_DAYS."
        )
    return stamp.strftime("%Y-%m-%dT%H:%M:%S")


# Authored in reading order. `state` is documentation, not data: "rewrite" means
# the slug already exists on the live site and must not change.
_TRACK = [
    # ------------------------------------------------------------ foundations
    {
        "slug": "terraform-introduction",
        "title": "Terraform – What It Is and Why It Exists",
        "state": "rewrite",  # published 2019-07-09, 54 words of copied blurb
        "tags": ["terraform", "infrastructure-as-code", "devops"],
        "excerpt": (
            "Start here. What infrastructure as code actually buys you over clicking around a "
            "console, where Terraform sits next to CloudFormation, CDK, Pulumi and Ansible, the "
            "2023 licence change and what OpenTofu is, the exact versions this track is written "
            "against, the application the AWS lessons deploy, and the full lesson index in "
            "reading order."
        ),
    },
    {
        "slug": "terraform-fundamentals",
        "title": "Terraform – Install It and Run Your First Apply",
        "state": "rewrite",  # published 2019-07-09, body is "Coming soon…"
        "tags": ["terraform", "devops", "getting-started"],
        "excerpt": (
            "Install Terraform, point it at AWS, and create something real. The four commands "
            "the whole tool is built around — `init`, `plan`, `apply`, `destroy` — what each one "
            "actually does, how to read a plan before you approve it, and why `init` downloads "
            "hundreds of megabytes the first time and nothing the second."
        ),
    },
    {
        "slug": "terraform-hcl-syntax",
        "title": "Terraform – HCL Syntax You Will Actually Use",
        "state": "new",
        "tags": ["terraform", "hcl", "devops"],
        "excerpt": (
            "HCL is small, and this is the part of it you need. Blocks and arguments, the type "
            "system, string interpolation and heredocs, the functions worth memorising, "
            "`terraform console` for trying an expression without an apply, and `terraform fmt` "
            "so nobody reviews your indentation."
        ),
    },
    {
        "slug": "terraform-providers",
        "title": "Terraform – Providers, Versions and the Lock File",
        "state": "new",
        "tags": ["terraform", "providers", "devops"],
        "excerpt": (
            "A provider is the plugin that knows how to talk to AWS, and pinning it is the "
            "difference between a reproducible build and a surprise on Tuesday. "
            "`required_providers`, version constraint operators and which one to use, what "
            "`.terraform.lock.hcl` is for and why it belongs in git, provider aliases, and "
            "deploying to two regions from one configuration."
        ),
    },
    {
        "slug": "terraform-resources-and-state",
        "title": "Terraform – Resources and the State File",
        "state": "new",
        "tags": ["terraform", "state", "devops"],
        "excerpt": (
            "State is the thing people misunderstand and then get burned by. What Terraform "
            "stores and why it cannot work without it, how resource addresses map to real "
            "infrastructure, implicit dependencies versus `depends_on`, the `lifecycle` block "
            "including `prevent_destroy`, and the `terraform state` subcommands you reach for "
            "when the file and reality disagree."
        ),
    },
    {
        "slug": "terraform-variables-and-outputs",
        "title": "Terraform – Variables, Locals and Outputs",
        "state": "new",
        "tags": ["terraform", "variables", "devops"],
        "excerpt": (
            "One configuration, many environments. Typed input variables and why you should "
            "always declare the type, `validation` blocks that reject a bad value at plan time, "
            "`sensitive` and what it does and does not hide, `.tfvars` files, the full precedence "
            "order when the same variable is set four ways, locals, and outputs."
        ),
    },
    {
        "slug": "terraform-data-sources",
        "title": "Terraform – Data Sources and Reading Existing Infrastructure",
        "state": "new",
        "tags": ["terraform", "data-sources", "aws"],
        "excerpt": (
            "Not everything you reference is something you created. Data sources read what is "
            "already there — the latest AMI, the availability zones in this region, an existing "
            "VPC, another stack's remote state. When a data source is the right answer, when "
            "importing the resource is, and the hard-coded AMI id that stopped existing."
        ),
    },
    {
        "slug": "terraform-remote-state",
        "title": "Terraform – Remote State and Locking on S3",
        "state": "new",
        "tags": ["terraform", "state", "aws", "devops"],
        "excerpt": (
            "Local state works until there are two of you, then it corrupts. The S3 backend, "
            "native state locking with `use_lockfile` — and why every tutorial you will find "
            "still tells you to create a DynamoDB table that Terraform 1.11 deprecated. "
            "Bootstrapping the bucket that holds the state, versioning and encryption on it, and "
            "migrating a local state file into it without losing anything."
        ),
    },
    {
        "slug": "terraform-loops-and-conditionals",
        "title": "Terraform – count, for_each and Dynamic Blocks",
        "state": "new",
        "tags": ["terraform", "hcl", "devops"],
        "excerpt": (
            "Three subnets should not be three copy-pasted blocks. `count` and its index, "
            "`for_each` over a map or a set, and the specific reason `count` will destroy and "
            "recreate half your resources when you remove one from the middle of a list. Then "
            "`for` expressions, `dynamic` blocks for repeated nested blocks, and the conditional "
            "expression."
        ),
    },
    {
        "slug": "terraform-modules",
        "title": "Terraform – Writing and Using Modules",
        "state": "new",
        "tags": ["terraform", "modules", "devops"],
        "excerpt": (
            "A module is a directory of Terraform you can call more than once. Structuring one, "
            "its inputs and outputs, calling a local module and a registry module, pinning a "
            "module version, what `terraform get` does — and an honest section on when a module "
            "is the wrong answer and a bit of duplication is cheaper than the abstraction."
        ),
    },
    {
        "slug": "terraform-environments-and-workspaces",
        "title": "Terraform – Dev, Staging and Prod Without Copy-Paste",
        "state": "new",
        "tags": ["terraform", "workspaces", "devops"],
        "excerpt": (
            "Three ways to run the same configuration against three environments: workspaces, "
            "separate directories with a shared module, and one directory with per-environment "
            "`.tfvars` and backend config. What each actually gives you, why workspaces are a "
            "trap for prod specifically, and the layout that survives the fourth environment."
        ),
    },
    # ------------------------------------------------------------------- AWS
    {
        "slug": "terraform-with-aws",
        "title": "Terraform with AWS – Building the Network and Database",
        "state": "rewrite",  # published 2019-07-09, body is "Coming soon…"
        "tags": ["terraform", "aws", "vpc", "rds"],
        "excerpt": (
            "The first half of a real deployment. A VPC with public and private subnets across "
            "two availability zones, an internet gateway and route tables, security groups that "
            "reference each other instead of hard-coding CIDRs, and an RDS MySQL instance for "
            "the pizza API — with the database password kept out of both the code and the state "
            "file."
        ),
    },
    {
        "slug": "terraform-ecs-fargate-deploy",
        "title": "Terraform – Deploying a Spring Boot API to ECS Fargate",
        "state": "new",
        "tags": ["terraform", "aws", "ecs", "fargate", "docker"],
        "excerpt": (
            "The second half. An ECR repository, a Fargate task definition with the environment "
            "and secrets the app needs, an ECS service, an application load balancer with a "
            "target group and health check, and CloudWatch logs — deploying the real "
            "pizza-springboot-backend image. Including what the health check has to point at, "
            "and why the first deploy sat in PENDING."
        ),
    },
    {
        "slug": "terraform-github-actions-cicd",
        "title": "Terraform – A CI/CD Pipeline in GitHub Actions",
        "state": "new",
        "tags": ["terraform", "ci-cd", "github-actions", "aws", "devops"],
        "excerpt": (
            "Plan on the pull request, apply on merge, and no AWS keys stored anywhere. "
            "Configuring GitHub's OIDC provider and the IAM role it assumes, posting the plan as "
            "a PR comment, the image build and push to ECR, rolling the ECS service onto the new "
            "image, and the concurrency group that stops two applies running at once."
        ),
    },
    {
        "slug": "terraform-production-practices",
        "title": "Terraform – Running It in Production",
        "state": "new",
        "tags": ["terraform", "production", "devops"],
        "excerpt": (
            "What changes when the state file matters. Reading a plan properly and the three "
            "words that should stop a merge, `prevent_destroy` on the things you cannot lose, "
            "drift and what to do about it, secrets in SSM instead of variables, `moved` and "
            "`import` for refactoring without destroying, least-privilege CI credentials, "
            "keeping the bill visible, and `terraform test`."
        ),
    },
    {
        "slug": "terraform-interview-questions",
        "title": "Terraform – Interview Questions",
        "state": "new",
        "tags": ["terraform", "interview", "devops"],
        "excerpt": (
            "The questions Terraform interviews actually ask, answered the way you would say "
            "them out loud. What state is for, `count` versus `for_each`, how locking works, "
            "module versioning, what happens when someone changes something in the console, "
            "Terraform versus CloudFormation versus Ansible, and how you would recover a "
            "corrupted state file."
        ),
    },
]

# Slug -> filename, and the dates, are derived so a reorder is one edit.
POSTS = [
    {
        "slug": entry["slug"],
        "title": entry["title"],
        "file": f"{i + 1:02d}-{entry['slug']}.html",
        "date": _date(i),
        "tags": entry["tags"],
        "excerpt": entry["excerpt"],
        "state": entry["state"],
    }
    for i, entry in enumerate(_TRACK)
]

# Slugs that already exist on the live site and must never change.
FROZEN_SLUGS = {e["slug"] for e in _TRACK if e["state"] == "rewrite"}

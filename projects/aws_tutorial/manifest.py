"""The AWS track: category metadata plus one entry per post.

`file` is relative to `posts/`. Numbering follows the stored publication order.

⚠️ EVERY ONE OF THESE 33 SLUGS IS LIVE AND INDEXED. There is no `new` state in this track — it is
a rewrite of a published archive, not a track being authored. `scripts/verify-build.mjs` check 1
fails the frontend build if any URL in `index/posts.json` stops resolving, so a slug that leaves
this manifest is a 404 on a page Google already has.

⚠️ THE DATES ARE NOT COMPUTED, unlike the Postgres and FastAPI tracks.

Those two tracks derived every date from a START_DATE because they were authored before they were
published and the whole track had to be re-based when the publish day arrived. This one is the
opposite situation: all 33 posts were published between 2018-10 and 2019-09, the stored dates
already ascend cleanly, and every URL is indexed. Re-stamping them buys nothing and moves 33
sitemap entries at once.

So the dates below are TRANSCRIBED FROM THE STORED POSTS, and `seed.py` has no `--force-dates`.
`upsert_post` never overwrites an existing date, which is exactly the behaviour we want here —
it means a re-seed cannot reshuffle the archive even by accident. `modified` updates on its own.

If a date ever does need to move, that is a deliberate change to this file plus a new flag on
seed.py, and it is worth reading progress_report.md first.
"""

CATEGORY = {
    "slug": "aws",
    "name": "AWS",
    # The stored record has the right name but an EMPTY description, so the archive page has no
    # standfirst. upsert_category rewrites both from here.
    "description": (
        "Amazon Web Services from the parts you actually touch shipping a backend — IAM and the "
        "least-privilege policy that took three tries, EC2 and the load balancer in front of it, "
        "S3 and CloudFront, Lambda behind API Gateway, RDS and Aurora, the queues, and the "
        "CI/CD that puts it all there. Every command in this track is checked against the AWS "
        "API model before it ships, and the traps are ones that cost this site real time."
    ),
}

# Where the category sits in site navigation, for reference. nav.ts already lists `aws` under the
# DevOps group with the display name "AWS" — nothing to add there.
NAV_GROUP = "DevOps"

# ---------------------------------------------------------------------------
# Versions — READ OFF THIS MACHINE, not chosen
# ---------------------------------------------------------------------------
# check_aws.py validates against the botocore below. A post that quotes a CLI version quotes this.
VERSIONS = {
    "aws-cli": "2.32.24",
    "botocore": "1.35.99",
    "boto3": "1.35.90",
    "python (cli)": "3.13.11",
    "host": "Darwin 25.2.0 arm64",
}

# ---------------------------------------------------------------------------
# This site's own infrastructure — the first-hand material
# ---------------------------------------------------------------------------
# lovemesomecoding.com runs on the account these posts are written from, and that is the whole
# differentiator against the AWS docs. Held here so a resource id quoted in three posts cannot
# disagree with itself, and so check_content.py can verify any id a post prints is a real one.
#
# These are all PUBLIC-SAFE identifiers: a CloudFront distribution id and a bucket name are
# visible in any response header or DNS lookup. No account number, no key, no ARN with an account
# in it. Keep it that way — see check_content.py, which fails on a 12-digit number.
SITE = {
    "domain": "lovemesomecoding.com",
    "site_bucket": "lovemesomecoding.com",
    "site_distribution": "E30YUPLP37MY9U",
    "site_domain_cf": "d32j0xfm775hkk.cloudfront.net",
    "media_distribution": "EYALMP5J1OET3",
    "edge_function": "lovemesomecoding-router",
    "lambda_function": "lovemesomecoding-admin-api-prod",
    "sam_stack": "lovemesomecoding-admin-api-prod",
    "hosted_zone": "Z000531818AC6P1IJ8LJL",
    "region": "us-west-2",
    "cf_cert_region": "us-east-1",
    "profile": "folau",
    "runtime": "python3.12",
    "arch": "x86_64",
    "memory_mb": 512,
    "monthly_cost_usd": 0.60,
}

DEMO_APPS = "lovemesomecoding_demo_project"  # stayhub, pizza, bank, reelcms

# ---------------------------------------------------------------------------
# Length budget
# ---------------------------------------------------------------------------
# ⚠️ `wordCount` in the content pipeline counts PROSE **AND** CODE TEXT together, then
# `readingMinutes = max(1, round(words / 220))`. See lovemesomecoding_backend/app/services/
# content.py. Budgeting prose alone silently doubles the published reading time — a post with a
# 40-line IAM policy in it can blow the budget without a single extra sentence.
WORDS_PER_MINUTE = 220
TARGET_MINUTES = (4, 6)                                  # Folau: "keep posts to the point"
TOTAL_WORDS_MIN = TARGET_MINUTES[0] * WORDS_PER_MINUTE   # 880
TOTAL_WORDS_MAX = TARGET_MINUTES[1] * WORDS_PER_MINUTE   # 1,320

# AND a floor on the prose share. JSON is even easier than SQL to fill a word budget with — one
# pasted IAM policy or CloudFormation template is 400 words of `"Effect": "Allow"` — and the
# result is a listing with captions rather than an explanation illustrated by code.
MIN_PROSE_SHARE = 0.45

# What the collection looks like TODAY, measured off the prod content tree on 2026-08-24 through
# the backend's own `normalize`, so these are the numbers the pipeline produced and not a
# re-derivation that could disagree with them.
#
#                                            prose, code, total, minutes
EXISTING = {
    "aws-ecs":                              (39, 185, 224, 1),
    "aws-lambda-to-stop-an-ec2-instance":   (37, 333, 370, 2),
    "aws-lambda-to-start-an-ec2-instance":  (29, 168, 197, 1),
    "aws-lambda-to-start-an-rds-instance":  (0, 0, 0, 1),
    "aws-lambda-to-stop-an-rds-instance":   (0, 0, 0, 1),
    "aws-iam":                              (1006, 0, 1006, 5),
    "aws-ec2":                              (653, 0, 653, 3),
    "aws-load-balancer":                    (617, 0, 617, 3),
    "aws-route-53":                         (254, 0, 254, 1),
    "aws-cli":                              (122, 30, 152, 1),
    "aws-rds":                              (534, 18, 552, 3),
    "aws-dynamodb":                         (610, 436, 1046, 5),
    "aws-elasticache":                      (2184, 0, 2184, 10),
    "aws-s3":                               (1037, 547, 1584, 7),
    "aws-cloudfront":                       (641, 0, 641, 3),
    "aws-lambda":                           (828, 29, 857, 4),
    "aws-api-gateway":                      (105, 0, 105, 1),
    "aws-alexa":                            (0, 0, 0, 1),
    "aws-kms-and-ecryption":                (234, 0, 234, 1),
    "aws-sqs":                              (760, 324, 1084, 5),
    "aws-ses":                              (1246, 331, 1577, 7),
    "aws-sns":                              (222, 157, 379, 2),
    "aws-elasticbeanstalk":                 (161, 0, 161, 1),
    "aws-kinesis":                          (0, 0, 0, 1),
    "aws-codecommit":                       (204, 0, 204, 1),
    "aws-codedeploy":                       (0, 0, 0, 1),
    "aws-codepipeline":                     (590, 19, 609, 3),
    "aws-codebuild":                        (110, 0, 110, 1),
    "aws-cloudformation":                   (0, 0, 0, 1),
    "aws-cloudwatch":                       (386, 17, 403, 2),
    "aws-secrets-manager":                  (184, 356, 540, 2),
    "aws-aurora":                           (738, 0, 738, 3),
    "aws-kubernetes-on-aws":                (0, 0, 0, 1),
}

# The seven that serve a completely blank page today. They are the reason the track is staged:
# these are a live bug, the other 26 are merely bad. check_content.py holds them to a higher floor
# than "grew a bit", because 4x of zero is zero.
BLANK = {slug for slug, v in EXISTING.items() if v[2] == 0}

# Stage 1 of the rewrite. Everything here must be written before the stage is seeded.
STAGE_1 = sorted(BLANK)

# ---------------------------------------------------------------------------
# The track
# ---------------------------------------------------------------------------
# `date` is transcribed from the stored post — see the module docstring. `state` is "rewrite" for
# every entry because every slug is live; the field is kept for symmetry with the other tracks and
# check_content.py asserts none of them says anything else.
#
# `closed` marks a post about a service that a reader CANNOT adopt today. It is not a synonym for
# "old": it means the console will refuse them. Those posts are held to a different rule by
# check_content.py — they must say so above the fold rather than teach the happy path.
_TRACK = [
    {
        "slug": "aws-ecs",
        "title": "AWS – ECS: Running Containers Without Kubernetes",
        "date": "2018-10-30T18:18:24",
        "tags": ["aws", "ecs", "containers", "fargate"],
        "excerpt": (
            "ECS in the three nouns it actually has — task definition, service, cluster — and why "
            "Fargate means you never touch an EC2 instance again. A task definition for the "
            "StayHub API, the service that keeps two of them running behind a load balancer, and "
            "rolling deploys with circuit breaker rollback. Plus the two things that make a task "
            "die on startup with no useful log: the execution role and the log group."
        ),
    },
    {
        "slug": "aws-lambda-to-stop-an-ec2-instance",
        "title": "AWS – Stop an EC2 Instance on a Schedule with Lambda",
        "date": "2019-04-22T05:00:18",
        "tags": ["aws", "lambda", "ec2", "cost"],
        "excerpt": (
            "A dev instance running nights and weekends is roughly 70% waste. Twenty lines of "
            "boto3, an EventBridge schedule, and an IAM policy scoped to a tag instead of `*`. "
            "Why the handler filters on instance state before it calls stop, what the stopping "
            "→ stopped transition means for your EBS bill, and the mistake that stops your "
            "production fleet: a tag filter that matches nothing is a filter that matches all."
        ),
    },
    {
        "slug": "aws-lambda-to-start-an-ec2-instance",
        "title": "AWS – Start an EC2 Instance on a Schedule with Lambda",
        "date": "2019-04-22T05:00:51",
        "tags": ["aws", "lambda", "ec2", "eventbridge"],
        "excerpt": (
            "The other half of the schedule: bring the instance back before anyone needs it. The "
            "cron expression EventBridge actually accepts — it is not standard cron, and the "
            "day-of-week field is the part that bites — why UTC ruins this twice a year, and the "
            "waiter that turns 'the API returned' into 'the box is up'. Plus a public IP that "
            "changes on every stop, and the one-line fix."
        ),
    },
    {
        "slug": "aws-lambda-to-start-an-rds-instance",
        "title": "AWS – Start an RDS Instance on a Schedule with Lambda",
        "date": "2019-04-22T05:01:23",
        "tags": ["aws", "lambda", "rds", "cost"],
        "excerpt": (
            "Starting a stopped RDS instance is one API call and a wait measured in minutes, not "
            "seconds, which changes how you schedule it. The handler, the IAM policy, and the "
            "state check that stops a retry storm — calling start on an instance that is already "
            "starting is an error, not a no-op. Plus the configuration that cannot be stopped at "
            "all: anything with a read replica, or that is one."
        ),
    },
    {
        "slug": "aws-lambda-to-stop-an-rds-instance",
        "title": "AWS – Stop an RDS Instance on a Schedule with Lambda",
        "date": "2019-04-22T05:01:39",
        "tags": ["aws", "lambda", "rds", "cost"],
        "excerpt": (
            "Stopping RDS saves the instance hours but not the storage, and it does not last: AWS "
            "restarts any instance that has been stopped for seven days. That single fact is why "
            "a stop-on-a-schedule Lambda is a schedule and not a one-off click. The handler, the "
            "seven-day trap and how to notice it, and the difference between stopping an instance "
            "and stopping an Aurora cluster."
        ),
    },
    {
        "slug": "aws-iam",
        "title": "AWS – IAM: Policies, Roles and Least Privilege",
        "date": "2019-08-05T06:37:40",
        "tags": ["aws", "iam", "security"],
        "excerpt": (
            "IAM is the service you get wrong first and it is the one that matters most. The five "
            "parts of a policy document, the difference between an identity policy and a resource "
            "policy — and why an S3 bucket needs both — roles versus users and why your code "
            "should never hold a key, and how a deny always wins. Ends with the real bucket policy "
            "that lets exactly one CloudFront distribution read this site and nothing else."
        ),
    },
    {
        "slug": "aws-ec2",
        "title": "AWS – EC2: Instances, Storage and What They Cost",
        "date": "2019-08-05T06:38:12",
        "tags": ["aws", "ec2", "compute"],
        "excerpt": (
            "Reading an instance type instead of guessing — what m7g.large tells you before you "
            "look it up — and the four purchase options ranked by how much they actually save. "
            "Security groups are stateful and NACLs are not, which explains most 'why can I not "
            "connect' questions. EBS volume types, why gp3 replaced gp2, user data for first-boot "
            "setup, and SSM Session Manager so you can close port 22 for good."
        ),
    },
    {
        "slug": "aws-load-balancer",
        "title": "AWS – Load Balancers: ALB, NLB and Target Groups",
        "date": "2019-08-05T06:38:30",
        "tags": ["aws", "elb", "alb", "networking"],
        "excerpt": (
            "ALB or NLB, decided in one table instead of three paragraphs. The target group is the "
            "object that actually matters and the health check on it is what decides whether your "
            "deploy is a deploy or an outage — including the arithmetic that turns a 30-second "
            "interval into a two-and-a-half minute outage. Path and host routing rules, sticky "
            "sessions and why you probably do not want them, and draining connections."
        ),
    },
    {
        "slug": "aws-route-53",
        "title": "AWS – Route 53: DNS, Alias Records and Health Checks",
        "date": "2019-08-05T06:39:07",
        "tags": ["aws", "route53", "dns"],
        "excerpt": (
            "The one thing Route 53 does that other DNS does not: an ALIAS record, which points a "
            "bare domain at a CloudFront or ALB target with no CNAME and no charge. Hosted zones "
            "and delegation, the record types worth knowing, routing policies from simple to "
            "weighted to failover, and TTL as the rollback lever it is. Plus how to tell a "
            "propagation problem from your own resolver cache — `dig @8.8.8.8`, not `curl`."
        ),
    },
    {
        "slug": "aws-cli",
        "title": "AWS – The CLI: Profiles, Queries and the Flags That Bite",
        "date": "2019-08-05T06:39:30",
        "tags": ["aws", "aws-cli", "tooling"],
        "excerpt": (
            "Named profiles so you never run a command against the wrong account, SSO login, and "
            "`--query` — JMESPath — which turns a screenful of JSON into the one field you wanted. "
            "Then the flags that have cost real time on this site: `s3 sync` skips unchanged files "
            "so metadata never updates, `--exact-timestamps` is not a tidy-up, and "
            "`--metadata-directive REPLACE` without `--content-type` rewrites every object."
        ),
    },
    {
        "slug": "aws-rds",
        "title": "AWS – RDS: Managed Databases and What Managed Means",
        "date": "2019-08-05T06:39:53",
        "tags": ["aws", "rds", "database"],
        "excerpt": (
            "What RDS takes off your hands and what it very much does not. Multi-AZ is failover "
            "and not a read replica — the single most expensive misunderstanding in the service — "
            "plus parameter groups, subnet groups and the security group rule that is the reason "
            "you cannot connect. Backups, PITR and the retention window that defaults to a number "
            "you would not choose, and how to restore without praying."
        ),
    },
    {
        "slug": "aws-dynamodb",
        "title": "AWS – DynamoDB: Keys, Indexes and Access Patterns",
        "date": "2019-08-05T06:40:26",
        "tags": ["aws", "dynamodb", "nosql"],
        "excerpt": (
            "DynamoDB rewards you for knowing your queries before you design your table, and "
            "punishes you for anything else. Partition key and sort key, why a scan is a bug, and "
            "the single-table pattern in the smallest example that shows why it exists. GSIs and "
            "LSIs and the difference that cannot be undone after creation, on-demand versus "
            "provisioned, and the hot partition that throttles a table that looks under quota."
        ),
    },
    {
        "slug": "aws-elasticache",
        "title": "AWS – ElastiCache: Redis in Front of Your Database",
        "date": "2019-08-05T06:40:51",
        "tags": ["aws", "elasticache", "redis", "caching"],
        "excerpt": (
            "Cache-aside in fifteen lines, then the four questions that decide whether it helps: "
            "what you key on, what you invalidate, what happens on a miss storm, and what happens "
            "when Redis is down. Valkey and Redis OSS engines, cluster mode on versus off, why "
            "your client needs the configuration endpoint and not a node address, and TTL as the "
            "only invalidation strategy that never goes stale forever."
        ),
    },
    {
        "slug": "aws-s3",
        "title": "AWS – S3: Buckets, Policies and Static Sites",
        "date": "2019-08-05T06:41:20",
        "tags": ["aws", "s3", "storage"],
        "excerpt": (
            "S3 as the service everything else leans on. Storage classes and the lifecycle rule "
            "that moves objects between them, versioning as an undo button with a bill attached, "
            "and Block Public Access — which should stay on, because a static site is served "
            "through CloudFront with OAC, not a public bucket. Ends with the bucket that serves "
            "this site: private, one policy, one distribution allowed to read it."
        ),
    },
    {
        "slug": "aws-cloudfront",
        "title": "AWS – CloudFront: Caching, OAC and Edge Functions",
        "date": "2019-08-05T06:46:13",
        "tags": ["aws", "cloudfront", "cdn"],
        "excerpt": (
            "A CDN is a cache, and a cache you cannot explain is an outage waiting. Origins and "
            "behaviours, cache policies and what actually forms the cache key, and Origin Access "
            "Control so the bucket behind it can stay private. Invalidation and why fingerprinted "
            "filenames beat it, the certificate that must live in us-east-1, and a CloudFront "
            "Function doing URL rewriting at the edge — including why it needs republishing."
        ),
    },
    {
        "slug": "aws-lambda",
        "title": "AWS – Lambda: Handlers, Cold Starts and Packaging",
        "date": "2019-08-05T06:46:44",
        "tags": ["aws", "lambda", "serverless"],
        "excerpt": (
            "The handler signature, what actually lives in the execution context between "
            "invocations, and why that one fact decides where you open a database connection. "
            "Cold starts measured rather than feared, memory as the CPU dial it really is, layers "
            "versus a zip versus a container image, and the packaging trap that ships a Lambda "
            "which dies at import: compiled wheels built for your laptop instead of for Lambda."
        ),
    },
    {
        "slug": "aws-api-gateway",
        "title": "AWS – API Gateway: HTTP APIs, Routes and Custom Domains",
        "date": "2019-08-05T06:47:04",
        "tags": ["aws", "api-gateway", "serverless"],
        "excerpt": (
            "HTTP API or REST API — one table, and for most backends the answer is the cheaper, "
            "faster one. Routes, proxy integration and the event shape your handler receives, "
            "CORS as configuration rather than code, and authorizers. Then the stage trap that "
            "makes one of your two URLs 404 forever: a named stage prefixes every path while a "
            "custom domain does not, and `$default` is the way out."
        ),
    },
    {
        "slug": "aws-alexa",
        "title": "AWS – Alexa Skills: Where They Actually Live",
        "date": "2019-08-05T06:47:32",
        "tags": ["aws", "alexa", "lambda"],
        "closed": True,
        "excerpt": (
            "Short and honest: an Alexa skill is not an AWS service. You build it on the Amazon "
            "Developer portal with the Alexa Skills Kit, and the only AWS part is the Lambda "
            "function it invokes. What that split means for where you configure things, what the "
            "ASK CLI does that the AWS CLI cannot, and how the skill's endpoint is wired to a "
            "function ARN. If you came here for AWS, the Lambda post is the one you want."
        ),
    },
    {
        "slug": "aws-kms-and-ecryption",
        "title": "AWS – KMS and Encryption at Rest",
        "date": "2019-08-05T06:48:17",
        "tags": ["aws", "kms", "encryption", "security"],
        "excerpt": (
            "Encryption at rest is a checkbox until something needs decrypting from another "
            "account. Customer managed keys versus AWS managed keys and the cost and control that "
            "separates them, envelope encryption in one diagram, and the key policy — which is "
            "the resource policy that IAM alone cannot override. Rotation, aliases, and the "
            "deletion window that is the only irreversible button in the service."
        ),
    },
    {
        "slug": "aws-sqs",
        "title": "AWS – SQS: Queues, Visibility Timeout and DLQs",
        "date": "2019-08-05T06:48:40",
        "tags": ["aws", "sqs", "messaging"],
        "excerpt": (
            "A queue is the simplest way to stop a slow dependency from becoming a 500. Standard "
            "versus FIFO, long polling and the empty receives it saves you paying for, and "
            "visibility timeout — the setting that quietly processes your message twice when it is "
            "shorter than your handler. Dead-letter queues and the redrive policy, idempotency as "
            "a requirement rather than a nicety, and Lambda event source mapping with batching."
        ),
    },
    {
        "slug": "aws-ses",
        "title": "AWS – SES: Sending Email That Arrives",
        "date": "2019-08-05T06:49:08",
        "tags": ["aws", "ses", "email"],
        "excerpt": (
            "Getting SES to send is easy; getting the mail delivered is the work. Verifying a "
            "domain, and the three DNS records — SPF, DKIM, DMARC — that decide whether you land "
            "in an inbox or a spam folder. The sandbox and what leaving it requires, the "
            "reputation metrics AWS will suspend you over, and handling bounces and complaints "
            "through SNS instead of discovering them when your sending is paused."
        ),
    },
    {
        "slug": "aws-sns",
        "title": "AWS – SNS: Fan-out, Filtering and SQS Subscriptions",
        "date": "2019-08-05T06:49:27",
        "tags": ["aws", "sns", "messaging"],
        "excerpt": (
            "SNS pushes, SQS pulls, and the useful thing is putting them together: one topic, "
            "several queues, each consumer at its own pace. Topics and subscriptions, the "
            "confirmation handshake an HTTP endpoint has to complete, message filtering so a "
            "consumer is not woken for events it ignores, and the raw message delivery setting "
            "that stops your payload arriving wrapped in an envelope you did not ask for."
        ),
    },
    {
        "slug": "aws-elasticbeanstalk",
        "title": "AWS – Elastic Beanstalk, and Whether to Use It in 2026",
        "date": "2019-08-05T06:50:10",
        "tags": ["aws", "elastic-beanstalk", "deployment"],
        "excerpt": (
            "Beanstalk still works and still deploys a web app in one command, and it is still "
            "the fastest path from a zip file to a URL with a load balancer in front. What it "
            "actually creates on your behalf, `.ebextensions` and where the abstraction leaks, "
            "the deployment policies and which ones can serve two versions at once — and an "
            "honest comparison against ECS Fargate and App Runner before you commit."
        ),
    },
    {
        "slug": "aws-kinesis",
        "title": "AWS – Kinesis: Streams, Firehose and When to Use SQS Instead",
        "date": "2019-08-05T06:50:39",
        "tags": ["aws", "kinesis", "streaming"],
        "excerpt": (
            "Most teams reaching for Kinesis want SQS, so this starts with the table that tells "
            "them apart: replay, ordering, and many consumers reading the same records. Then "
            "shards and the partition key that decides your hot shard, the retention window, and "
            "Data Firehose for the case where you only wanted the data in S3. Note the names "
            "changed — Firehose and Managed Service for Apache Flink are not called Kinesis now."
        ),
    },
    {
        "slug": "aws-codecommit",
        "title": "AWS – CodeCommit Is Closed. Here Is What to Use",
        "date": "2019-08-05T06:51:08",
        "tags": ["aws", "codecommit", "git", "ci-cd"],
        "closed": True,
        "excerpt": (
            "On 25 July 2024 AWS stopped onboarding new customers to CodeCommit without "
            "announcing it. If you do not already have a repository there you cannot create one, "
            "and no new features are coming. What that means if you are on it — you can stay, "
            "and here is how to mirror out — and what to use instead: GitHub or GitLab, wired to "
            "CodePipeline or CodeBuild through a connection. Nobody should start here in 2026."
        ),
    },
    {
        "slug": "aws-codedeploy",
        "title": "AWS – CodeDeploy: Blue/Green and Where It Still Fits",
        "date": "2019-08-05T06:51:35",
        "tags": ["aws", "codedeploy", "ci-cd", "deployment"],
        "excerpt": (
            "CodeDeploy is the piece that takes a built artifact and puts it on the thing that "
            "runs it — and in 2026 it earns its place on EC2 and in ECS blue/green, not much "
            "elsewhere. The appspec file, the lifecycle hooks in the order they fire, and the "
            "validation hook that is the only reason blue/green is safer than in-place. Plus the "
            "automatic rollback alarm, and why a deployment can hang for an hour."
        ),
    },
    {
        "slug": "aws-codepipeline",
        "title": "AWS – CodePipeline: Stages, Artifacts and Approvals",
        "date": "2019-08-05T06:52:06",
        "tags": ["aws", "codepipeline", "ci-cd"],
        "excerpt": (
            "A pipeline is stages, and between them an artifact in an S3 bucket — get that one "
            "idea and the rest is configuration. Source from GitHub through a CodeStar connection "
            "rather than a token, build, a manual approval gate, deploy. Where CodePipeline beats "
            "GitHub Actions and where it plainly does not, and the input-artifact mismatch that "
            "is the single most common reason a stage fails with nothing useful in the log."
        ),
    },
    {
        "slug": "aws-codebuild",
        "title": "AWS – CodeBuild: buildspec, Caching and Build Speed",
        "date": "2019-08-05T06:52:29",
        "tags": ["aws", "codebuild", "ci-cd"],
        "excerpt": (
            "The buildspec file phase by phase, what each one is actually for, and the artifacts "
            "block that decides what the next stage receives. Then the two things that make "
            "builds slow and expensive: no dependency cache, and a compute type chosen by "
            "guessing. Local caching versus S3 caching, environment variables that should be "
            "parameter references, and privileged mode for building a container image."
        ),
    },
    {
        "slug": "aws-cloudformation",
        "title": "AWS – CloudFormation: Infrastructure You Can Re-create",
        "date": "2019-08-05T06:53:07",
        "tags": ["aws", "cloudformation", "iac", "sam"],
        "excerpt": (
            "Click-ops is fine until the day you have to build it again. A template's five "
            "sections, parameters and outputs, change sets so you see what an update will do "
            "before it does it, and SAM as the shorthand that turns forty lines of Lambda plumbing "
            "into six. Then the trap that ships stale config in silence: CloudFormation keeps the "
            "previous value for any parameter an update omits — it does not read your new default."
        ),
    },
    {
        "slug": "aws-cloudwatch",
        "title": "AWS – CloudWatch: Logs, Metrics and Alarms Worth Having",
        "date": "2019-08-05T06:53:52",
        "tags": ["aws", "cloudwatch", "monitoring", "observability"],
        "excerpt": (
            "Log groups, retention that defaults to never expire and quietly bills you forever, "
            "and Logs Insights queries that find the error instead of scrolling to it. Metrics "
            "and the difference between a missing datapoint and a zero — which is what makes an "
            "alarm lie. Alarms that page a human versus alarms that trigger a rollback, and the "
            "handful actually worth creating on day one."
        ),
    },
    {
        "slug": "aws-secrets-manager",
        "title": "AWS – Secrets Manager and Parameter Store",
        "date": "2019-08-07T03:32:16",
        "tags": ["aws", "secrets-manager", "ssm", "security"],
        "excerpt": (
            "Two services do this job and the right answer is usually the cheaper one. Parameter "
            "Store SecureString versus Secrets Manager, compared on the three things that "
            "differ: rotation, cross-account access, and price per secret per month. How to read "
            "one from a Lambda without shipping a key, caching so you are not billed per "
            "invocation, and why an environment variable holding a secret is visible in the console."
        ),
    },
    {
        "slug": "aws-aurora",
        "title": "AWS – Aurora: What It Changes About RDS",
        "date": "2019-08-21T19:58:25",
        "tags": ["aws", "aurora", "database", "rds"],
        "excerpt": (
            "Aurora is RDS with the storage layer replaced, and every difference that matters "
            "follows from that one change: replicas share storage so they lag in milliseconds, "
            "failover is fast, and storage grows on its own. The reader and writer endpoints and "
            "the bug you get from pointing writes at the wrong one, Serverless v2 scaling, and an "
            "honest look at when plain RDS Postgres is the better-value answer."
        ),
    },
    {
        "slug": "aws-kubernetes-on-aws",
        "title": "AWS – EKS: Kubernetes, and Whether You Need It",
        "date": "2019-09-06T21:01:13",
        "tags": ["aws", "eks", "kubernetes", "containers"],
        "excerpt": (
            "The honest version: most teams shipping one backend do not need Kubernetes, and ECS "
            "Fargate costs less to run and far less to learn. If you do need it — several teams, "
            "many services, or portability you can name — here is what EKS gives you, what the "
            "control plane costs before a single pod runs, node groups versus Fargate profiles, "
            "and the two AWS-specific pieces: IRSA for pod IAM, and the load balancer controller."
        ),
    },
]

# Slug -> filename is derived so a reorder is one edit.
POSTS = [
    {
        "slug": entry["slug"],
        "title": entry["title"],
        "file": f"{i + 1:02d}-{entry['slug']}.html",
        "date": entry["date"],
        "tags": entry["tags"],
        "excerpt": entry["excerpt"],
        "state": "rewrite",
        "closed": entry.get("closed", False),
    }
    for i, entry in enumerate(_TRACK)
]

# Every slug in this track is live and indexed. check_content.py fails if one leaves the manifest,
# and seed.py refuses to write to prod if one is missing from the target tree.
FROZEN_SLUGS = {e["slug"] for e in _TRACK}

# There are no new slugs in this track. Kept so seed.py can stay shaped like the other tracks'.
NEW_SLUGS: set[str] = set()

# Posts about something a reader cannot adopt today. They must say so above the fold.
CLOSED_SLUGS = {e["slug"] for e in _TRACK if e.get("closed")}

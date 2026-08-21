# Lovemesomecoding.com

## About
- Help aspiring developers understand what they need to know to start a career in programming
- Provide practical solutions to real-world coding problems — clean, well-explained tutorials drawn from official documentation and hands-on experience, not just quick hacks

---

## Current state (updated 2026-08-04)

**The WordPress → AWS migration is DONE and live.** lovemesomecoding.com serves from CloudFront;
WordPress is no longer in the request path.

| | |
|---|---|
| Site | https://lovemesomecoding.com (also `www`) |
| Admin console | https://lovemesomecoding.com/admin — user `folauk` |
| Admin API | https://api.lovemesomecoding.com |
| Content | **661 posts**, 42 categories, 12 static pages, 336 images |
| Cost | ≈ **$0.60/month** + $16/yr domain (was $25/mo on DreamHost) |

### Architecture
```
Next.js 14 static export ──> S3 (lovemesomecoding.com) ──> CloudFront ──> visitors
                                      ▲
content DB (JSON in S3) ──────────────┘ read at BUILD time only
        ▲
FastAPI on Lambda (admin writes) ──> GitHub repository_dispatch ──> rebuild
```

Nothing is fetched at runtime. Saving a post writes JSON to S3 and changes nothing a visitor sees
until **Publish** triggers a rebuild (~3–5 min).

### ⚠️ DreamHost — do not cancel before ~2026-09-03
It is the cutover rollback target and Search Console needs 30 days to confirm index coverage.
Rollback = point the apex/www ALIAS records back to `69.163.227.84` (60s TTL).

### Outstanding
- [ ] Commit the Oracle track — three repos have uncommitted changes
      (`projects/oracle/progress_report.md` lists them). The content itself is live.
- [ ] Store GitHub PAT so **Publish** works: `aws ssm put-parameter --name /lovemesomecoding/prod/github-token --type SecureString --value ghp_xxx --region us-west-2 --profile folau`
- [ ] Submit `https://lovemesomecoding.com/sitemap.xml` to Search Console
- [ ] `lovemesomecoding_backend` repo does not exist on GitHub yet — its CI cannot run until created
- [ ] Rotate the admin password: `python scripts/create_admin.py --username folauk --write`

---

## Repos

Three separate git repos. Only `claude_lovemesomecoding` (this one) holds project docs.

- `lovemesomecoding_frontend` — Next.js 14 static export. **Public repo.**
- `lovemesomecoding_backend` — FastAPI + Mangum on Lambda. Remote not yet created.
- `claude_lovemesomecoding` — parent; `projects/rewrite/` holds the migration scripts and
  `progress_report.md` (full history and decisions live there, not here).

## Local development

```bash
# terminal 1 — API against the isolated `local` content tree
cd lovemesomecoding_backend
./scripts/seed-local-data.sh          # once: copy prod content -> local tree
AWS_PROFILE=folau ./scripts/run-local.sh        # :8099

# terminal 2 — site + admin
cd lovemesomecoding_frontend
AWS_PROFILE=folau npm run dev                   # :3000, uses the local tree

# production preview: the real built output with CloudFront's routing rules
npm run build && npm run preview                # :4321, uses the LIVE API
```

`:3000` is safe to experiment in — writes go to `lovemesomecoding/local/` in S3, verified isolated
from prod. `:4321` talks to the live API, so saves there are real.

## Deploying

```bash
AWS_PROFILE=folau npm run deploy                 # frontend: build, S3, invalidate, verify
AWS_PROFILE=folau ./scripts/deploy.sh            # backend: tests, sam build, deploy, smoke test
```

Or push to `main` — both repos have GitHub Actions using `AWS_ACCESS_KEY_ID` /
`AWS_SECRET_ACCESS_KEY` secrets (frontend also has `CLOUDFRONT_DIST_ID`).

The frontend build **fails** if any indexed post URL stops resolving — the 512 migrated ones above
all (`scripts/verify-build.mjs`). That guard is the point — do not weaken it.

---

## Gotchas that already cost time — do not rediscover these

### Content pipeline
- **Extract `<pre>` blocks with regex BEFORE any HTML parsing.** Post bodies contain raw unescaped
  `<script>`, `<button onclick=…>`, `<style>` *inside* code samples. An HTML parser turns those
  into real elements and `get_text()` then deletes them — with almost no change in character count,
  so length-based checks pass. Compare code-block sources byte-for-byte, not lengths.
  (`migration/transform.py`, `app/services/content.py` — the ordering is load-bearing.)
- Code blocks must end up as `<pre class="language-X"><code class="language-X">` — the build-time
  Prism highlighter matches that exact shape.

### Next.js
- **`trailingSlash: false` is load-bearing.** WordPress serves `/java-8/foo` with no trailing slash
  and that is what Google indexed on 512 pages. Turning it on rewrites every canonical URL.
- **`output: 'export'` is scoped to production builds only.** Next 14's dev server rejects dynamic
  routes under it with *"missing exported function generateStaticParams()"* even when it is exported.
- **Import Prism languages statically.** `prismjs/components/index.js` uses a dynamic `require()`
  webpack cannot follow — it builds fine, then throws `MODULE_NOT_FOUND` at page generation.
- Next requires the **same param name per dynamic level**, hence `[slug]` and `[slug]/[post]`.

### Deploys / AWS
- **`aws s3 sync` skips unchanged files, so metadata never updates.** Changing `Cache-Control` in
  the deploy script does not reach objects already in the bucket. Non-fingerprinted files upload
  with `cp --recursive`.
- **`sync-content.sh` needs `--exact-timestamps`, and it is load-bearing.** Downloading, `aws s3
  sync` skips a same-sized object unless S3 is *newer* than the local file. The derived indexes beat
  both halves: `"count":12` → `"count":13` is byte-identical in length, and S3's `LastModified` is
  UTC while the local mtime was stamped at download time, so a fresh write can look older. This
  shipped `/oracle` reading "12 tutorials" over a list of 13. `verify-build.mjs` check 6 now
  cross-checks the indexes against each other, because every URL still resolved.
- **Never use `--metadata-directive REPLACE` without an explicit `--content-type`** — it rewrites
  every object to `binary/octet-stream`.
- **Republish the CloudFront Function on every deploy.** The redirect map is compiled into it, so
  a redirect added in `postbuild.mjs` does nothing at the edge until the function is republished.
- **CloudFormation keeps the PREVIOUS value for any parameter an update omits** — it does not adopt
  a changed template default. Pass parameters explicitly or ship stale config silently.
- **Lambda needs manylinux wheels.** `pydantic-core` and `bcrypt` are compiled; a plain `pip install`
  on macOS produces a Lambda that dies at import. The `Makefile` + `BuildMethod: makefile` forces
  the right platform. Verify: `file .aws-sam/build/ApiFunction/pydantic_core/*.so` → `ELF … x86-64`.
- **API Gateway uses the `$default` stage.** A named stage prefixes paths with `/<stage>` while a
  custom domain does not, so one of the two URLs always 404s.
- An empty `API_CERT_ARN` makes CloudFormation **delete** the api custom domain. `deploy.sh` guards
  against this.
- Stop `next dev` before `next build` — they share `.next` and the build fails.
- A local DNS cache can make it look like a change did not take. Check with
  `dig +short A <host> @8.8.8.8`, not just `curl`.

---

## AWS

Use the **`folau`** profile for all CLI/API access. Region **us-west-2** (certs for CloudFront are
in **us-east-1**).

### Resources for this project
| Resource | Id / name |
|---|---|
| Site bucket | `lovemesomecoding.com` (private, OAC only) |
| Site CloudFront | `E30YUPLP37MY9U` → `d32j0xfm775hkk.cloudfront.net` |
| Media bucket | `lovemesomecoding-storage-329580012644-us-west-2-an` |
| Media CloudFront | `EYALMP5J1OET3` → `d2q2snz6diubfd.cloudfront.net` (OriginPath `/lovemesomecoding/prod`) |
| Content DB bucket | `lovemesomecoding-db-329580012644-us-west-2-an` (`prod/` and `local/` trees) |
| Edge function | `lovemesomecoding-router` (URL rewriting + 41 legacy redirects) |
| Lambda | `lovemesomecoding-admin-api-prod` (python3.12, x86_64, 512 MB) |
| SAM stack | `lovemesomecoding-admin-api-prod` |
| Route 53 zone | `Z000531818AC6P1IJ8LJL` |
| Certs | apex+www in us-east-1; `api.` in us-west-2 |
| Secrets | SSM `/lovemesomecoding/prod/jwt-secret`, `/lovemesomecoding/prod/github-token` |

Content DB layout (`lovemesomecoding/{prod|local}/`): `posts/{slug}.json`, `index/posts.json`,
`index/drafts.json`, `index/by-category/{cat}.json`, `index/categories.json`, `search/index.json`,
`users/admin.json`. One object per post plus small derived indexes — a save is O(1) in post count.
Never collapse this back into one blob.

Media uploaded from **local** dev deliberately lands in the **prod** media tree
(`media_env=prod`), because the CDN only serves `/lovemesomecoding/prod`. Uploads are uuid-prefixed
and additive, so nothing is overwritten.

### Route 53 — domains
All registered via Amazon Registrar in this account, all `.com`, auto-renew, $16/yr each ($80/yr):
folaukaveinga.com (2026-11-22) · folautech.com (2027-06-19) · learntongan.com (2027-07-20) ·
lovemesomecoding.com (2027-05-31) · pitaconcrete.com (2027-08-30).
Hosted zones exist for lovemesomecoding.com, pitaconcrete.com, folaukaveinga.com.

Stay on `.com` — checked 2026-08-04, no cheaper TLD (.dev $17, .app $20, .co $38, .ai $137).
Don't re-run that comparison.

pocsoft.com is NOT in this account (Unstoppable Domains, DNS at Vercel, expires 2027-03-22). Its
orphaned hosted zone was deleted 2026-08-04. Two resources it used may still bill and are
unverified: API Gateway `d-slp5iqnci4.execute-api.us-west-2`, CloudFront `d1zmyros44lee`.

---

## Projects
Projects live in `projects/`. Each has its own folder with a `README.md` of instructions, and a
`progress_report.md` tracking status and decisions. Also check the project folder for resources
(screenshots, SQL, etc.).

## Standard Workflow

1. **Clarify requirements** — analyse the criteria and ask until they are understood. Flag conflicts
   before building, not after.
2. **Create shared context** — `progress_report.md` in the project folder, tracking progress and
   decisions.
3. **Track solutions and responsibilities** — record the proposed solution and who owns each task.
4. **Frontend first** — build UI with mock data, focusing on styling, layout and interactions.
   Skip if there is no frontend work.
5. **Then backend** — implement the endpoints the frontend needs; coordinate on database changes.
   Use Lombok annotations wherever applicable in Java code.
6. **Integrate** — wire the frontend to the real endpoints and verify.
7. **QA** — run both apps and exercise the UI; validate backend logic by code review.
8. **Iterate** until requirements are met and no bugs remain.
9. **Final delivery check** — demonstrate with Playwright, write tests covering 90% of changes, and
   run `spotless apply` on Java changes. Notify me for review.
10. **Resume work** by reading `progress_report.md` first.
11. **Documentation** — keep all related documents, files and Playwright scripts in the project
    directory.

Note: only these agent types exist here — `claude`, `general-purpose`, `Explore`, `Plan`,
`claude-code-guide`, `statusline-setup`. Do not invoke agents unless I ask for them.

## Git
- Do **not** add `Co-Authored-By` or any author trailer to commits.
- Do **not** push to remote — I do that.
- Never commit log files, `node_modules`, build output, or migration artifacts. Delete stray logs.
- Write a real commit message explaining *why*, not just what.

## Demo projects
- lovemesomecoding_demo_project directory has apps that we must use to reference and create snippets from for examples.
- pizza in lovemesomecoding_demo_project is an app like https://www.pizzahut.com or https://www.dominos.com
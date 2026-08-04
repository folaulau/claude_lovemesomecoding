# Rewrite — Progress Report

**Status:** Phase 1 — Research & Analysis (no code written)
**Last updated:** 2026-08-04

---

## 1. Content Inventory (measured from the live WP REST API)

Pulled from `https://lovemesomecoding.com/wp-json/wp/v2/*`. The API is public — **no DreamHost
admin access is needed to migrate.**

| Asset | Count | Notes |
|---|---|---|
| Posts | **512** | avg 30–45 KB rendered HTML each → ~15–20 MB total |
| Pages | **56** | almost all are hand-maintained "X Table of Content" pages |
| Categories | **52** | all flat (`parent=0`); no post has >1 category |
| Comments | **2** | comments are effectively unused across the whole site |
| Media | **333** | 78% PNG, ~70 KB avg → ~25 MB total |

**URL structure is uniform and 2 levels deep:** `/{category-slug}/{post-slug}`
e.g. `https://lovemesomecoding.com/java-8/java-25-migration-guide` (no trailing slash).

Post bodies contain `<pre>` code blocks; inline images are rare. Sitemap lives at
`/wp-sitemap.xml`; `robots.txt` points at it.

### Observations worth acting on
- The 56 "Table of Content" pages are manual category indexes. In the rewrite these should be
  **auto-generated** from the category index — 56 pages of maintenance burden disappears.
- Category slugs are stale/wrong: Java 25 content lives under `/java-8/`, `rea-native` is a typo,
  `swedesignpattern` is unreadable. Fixing them costs 301 redirects on ~500 indexed URLs.
  **Recommendation: keep the slugs, change only the display names.**
- With 2 comments total, a live comment system is not worth putting in the SEO read path.

---

## 2. AWS Environment (verified via `aws --profile folau`)

Account `329580012644`, region `us-west-2`. Buckets exist and are **all empty**:
- `lovemesomecoding.com` — static site
- `lovemesomecoding-db-329580012644-us-west-2-an` — JSON database
- `lovemesomecoding-storage-329580012644-us-west-2-an` — media

**Gaps that must be sequenced before cutover:**
- No Route 53 hosted zone for `lovemesomecoding.com` (only `pocsoft.com`, `pitaconcrete.com`,
  `folaukaveinga.com` exist). Registrar for the domain is unknown.
- No ACM certificate for `lovemesomecoding.com`. Must be issued in **us-east-1** for CloudFront.
- No CloudFront distribution yet.

### Cost projection
| Item | Est. / month |
|---|---|
| S3 storage (~50 MB) + requests | < $0.10 |
| CloudFront (site + media) | ~$0–1 (well inside free tier at this traffic) |
| Lambda + API Gateway (admin writes only) | ~$0 (free tier) |
| Route 53 hosted zone | $0.50 |
| ACM | free |
| **Total** | **~$1–3/mo vs. $25/mo today → ~$270/yr saved** |

---

## 3. Reference Projects Studied

### `/Users/folaukaveinga/Github/pitaconcrete.com` (frontend pattern)
- Next.js 14 App Router, **`output: 'export'`** + `trailingSlash: true` + `images.unoptimized`
- Bootstrap 5 + react-bootstrap + bootstrap-icons, axios API layer, react-query
- `src/api/*Api.js` thin axios wrappers; `src/components/Auth.js` stores JWT in `localStorage`
- Split into `server_components/` (SEO'd) and `client_components/` (`'use client'`)
- `.env.development` / `.env.production` with `NEXT_PUBLIC_API_URL` and
  `NEXT_PUBLIC_MEDIA_CLOUDFRONT_URL`
- GitHub Actions: build → upload `out/` artifact → sync to S3 on push to `main`

### `/Users/folaukaveinga/Github/backend-folaukaveinga` (backend pattern)
- Chalice app, one `Blueprint` per site (`pitaconcrete_api`, `math_api`, `learntongan_api`)
- `AwsS3Service` keys everything as `{app}/{env}/{key}` — good multi-tenant + env isolation
- `JwtService` (PyJWT HS256), `SimpleCache` (in-process TTL dict)
- Presigned PUT URLs for uploads (browser → S3 direct) — good pattern, keeps files out of Lambda
- `.chalice/config.json` with `local` / `prod` stages; GH Actions `chalice deploy --stage prod`

### Patterns to carry over
Presigned-URL uploads · `{app}/{env}/{key}` S3 layout · blueprint-per-domain · env-staged config ·
GH Actions deploy · static export + S3 sync.

### Patterns to **fix**, not copy
| Issue in reference | Why it breaks here | Fix |
|---|---|---|
| All records in one JSON blob (`projects.json`) + a second `sorted_projects.json` | 512 posts × 40 KB = a ~20 MB object rewritten on **every single save**. Slow, expensive, and last-writer-wins data loss. | One S3 object per post + small derived indexes |
| Hardcoded admin password in source (`"folaulisa1"`) | Public GitHub repo → site takeover | Hashed password in S3 or Cognito |
| Hardcoded JWT secret (`"db-soft-8j4q"`) in source | Anyone can forge an admin token | Secret in SSM Parameter Store / Lambda env |
| JWT stored in `localStorage`, 100-day expiry | XSS-exfiltratable, and effectively permanent | Short-lived token; acceptable risk for a 1-admin panel but shorten it |
| `SimpleCache` in Lambda process memory | Useless across cold starts / concurrent Lambdas | Drop it, or rely on CloudFront caching |
| No auth enforcement — `authenticated_endpoints = []` is declared but never checked | Every write endpoint is public | Real middleware guard on all write routes |

---

## 4. The Central Architectural Tension

The README asks for two things that pull against each other:

1. *"Use Next.js so pages are SEO-friendly and readable by Google"* + host static on S3/CloudFront
2. *"Posts and comments should be pulled from the database (S3) for each page"*

If posts are fetched **client-side at runtime**, Googlebot receives an empty shell. For a site whose
entire value is **512 organically-indexed tutorial pages**, that is a direct regression from
WordPress and the single biggest risk in this project.

### Options

**A. Static export + rebuild-on-publish (SSG)** ← recommended
`generateStaticParams` reads the post index from S3 at build time and prerenders all 512 pages.
Admin publishes → API writes JSON to S3 → triggers a GitHub Actions `repository_dispatch` →
rebuild + `s3 sync` + CloudFront invalidation.
- ✅ Perfect SEO, zero Lambda in the read path, fastest possible pages, cheapest
- ❌ ~3–5 min from "Publish" to live; needs CI trigger plumbing
- The `/admin` panel is a client-only, `noindex` route — it does *not* need prerendering

**B. SSR/ISR on Lambda** (OpenNext / Amplify Hosting)
- ✅ Instant publish, incremental revalidation
- ❌ Much more infrastructure, Lambda cold starts in the read path, higher cost, diverges from the
  reference project the README says to copy

**C. Runtime client-side fetch**
- ❌ Rejected — destroys the SEO that is the site's entire asset

**Recommended shape:** A for all public content; a small Lambda API for **writes only**; comments
(if kept) submitted via API into a moderation queue and rendered statically on the next build.

---

## 5. Proposed S3 "Database" Layout

```
s3://lovemesomecoding-db-329580012644-us-west-2-an/
  lovemesomecoding/{env}/                     # env = local | prod
    posts/{slug}.json                         # full post body, one object per post
    index/posts.json                          # slug,title,excerpt,category,date,tags (~150 KB)
    index/categories.json                     # slug, displayName, count, order
    index/by-category/{category-slug}.json
    comments/{post-slug}.json                 # pending + approved
    search/index.json                         # prebuilt client-side search index
    redirects.json
    users/admin.json                          # bcrypt hash only
```

Writes touch one post object + the small indexes. Build reads a single `s3 sync` of the prefix.
Media goes to `lovemesomecoding-storage-.../lovemesomecoding/{env}/...` behind its own CloudFront
distribution, referenced via `NEXT_PUBLIC_MEDIA_CLOUDFRONT_URL`.

---

## 6. SEO Migration Checklist (non-negotiable)

- [ ] Preserve every `/{category}/{post-slug}` URL **exactly** — 512 indexed pages at stake
- [ ] Resolve trailing-slash behavior: WP serves `/a/b`, `trailingSlash: true` produces `/a/b/`.
      Needs a CloudFront Function to normalize and map paths → `index.html`
- [ ] Generate `sitemap.xml` at build (WP currently exposes `/wp-sitemap.xml` — 301 it)
- [ ] `robots.txt`, canonical tags, JSON-LD `Article` schema, Open Graph / Twitter cards
- [ ] RSS feed (WordPress provided one at `/feed`)
- [ ] 404 → CloudFront custom error response
- [ ] Redirect map for any URL that does change
- [ ] Carry over Google Analytics / GTM (pitaconcrete uses `@next/third-parties`)
- [ ] Post-cutover: submit new sitemap in Search Console, watch coverage for 30 days
- [ ] Keep DreamHost live for 30 days after DNS flip before cancelling

---

## 7. Frontend Direction (w3schools-inspired)

- Sticky top navbar with category dropdowns (w3schools style), left sidebar tutorial tree,
  prev/next pager at the bottom of each tutorial, dark syntax-highlighted code blocks
- Bootstrap 5 as the component base, with a custom theme layer
- **Search**: prebuilt client-side index (Pagefind / Fuse.js) over the 512-post index — no backend,
  no cost, works on a static site
- Note: build an *inspired-by* design, not a pixel clone — w3schools' exact branding/trade dress
  should not be reproduced 1:1

---

## 8. Decisions (locked 2026-08-04)

| # | Decision | Choice | Consequence |
|---|---|---|---|
| 1 | Publish flow | **Static rebuild on publish (SSG)** | All 512 pages prerendered. Admin save → S3 → CI rebuild → sync → CF invalidation. ~3–5 min publish latency accepted. Zero Lambda in read path. |
| 2 | Content format | **Keep rendered HTML as-is** | No conversion fidelity risk. Must sanitize + normalize CSS classes at migration so code blocks are restylable. |
| 3 | Comments | **Dropped entirely** | No comments subsystem, no moderation, no spam surface. Newsletter signup stays as the engagement path. Removes `comments/` from the S3 layout. |
| 4 | Backend framework | **FastAPI + Mangum** | Pydantic validation, auto OpenAPI docs, good local dev, portable off Lambda. Replaces Chalice blueprints with APIRouter. |
| 5 | Auth | **Self-managed JWT** — bcrypt hash in S3, secret in SSM Parameter Store, short-lived token | Proportionate for a single-admin panel. Explicitly *not* the reference project's hardcoded creds. Cognito rejected as over-ceremony here. |
| 6 | DNS | **Already solved — see below** | No registrar transfer needed. |

### DNS finding (verified)
`lovemesomecoding.com` is registered with **Amazon Registrar inside this same AWS account**
(`329580012644`) — confirmed via `route53domains list-domains`. NS delegation currently points at
`ns1/ns2/ns3.dreamhost.com` (A record → `69.163.227.84`).

The entire cutover therefore stays inside AWS: create the Route 53 hosted zone → populate records →
update the NS delegation at the registrar. No third party, no transfer wait, and **instant
rollback** by pointing NS back at DreamHost if anything goes wrong.

---

## 9. Phased Plan

**Phase 0 — Foundation (no app code)**
Route 53 hosted zone · ACM cert in **us-east-1** · CloudFront distros for site + media ·
S3 bucket policies + OAC · SSM parameter for the JWT secret.

**Phase 1 — Content migration (one-off script)**
Pull all 512 posts, 56 pages, 52 categories, 333 media from the WP REST API → sanitize/normalize
HTML → write the S3 layout in §5 → rewrite `wp-content/uploads/...` URLs to the media CloudFront
domain. Output a URL manifest for verification.

**Phase 2 — Frontend** (`lovemesomecoding_frontend`, Next.js 14 static export + Bootstrap 5)
w3schools-inspired navbar + sidebar tree + prev/next pager + dark code blocks · auto-generated
category index pages (retires the 56 manual TOC pages) · Pagefind/Fuse client-side search ·
sitemap, RSS, canonical, JSON-LD, OG tags · `/admin` as a `noindex` client-only route.

**Phase 3 — Backend** (`lovemesomecoding_backend`, FastAPI + Mangum on Lambda)
Auth (login, JWT verify middleware enforced on **every** write route) · collections/categories
CRUD · posts CRUD · presigned-URL media uploads · index regeneration on write · CI rebuild trigger
via `repository_dispatch`.

**Phase 4 — Verification**
Crawl all 512 legacy URLs against the new site and diff · Playwright walkthrough of the admin
publish loop · Lighthouse/SEO audit · staging CloudFront before DNS flip.

**Phase 5 — Cutover**
Flip NS to Route 53 · 301 `/wp-sitemap.xml` → `/sitemap.xml` · submit sitemap in Search Console ·
**keep DreamHost paid and live for 30 days** while watching index coverage · then cancel.

---

## 10. Task Assignments

_To be assigned at Phase 2 kickoff (frontend first, per CLAUDE.md §6)._

Note: `CLAUDE.md` §1 references `trading-coach`, `market-analyst`, and `tradestation-expert`
subagents for strategy validation. Those are leftovers from a trading project template and are
not applicable here; they also are not registered agent types in this environment. Skipping.

---

## 11. Phase 1 — Content Migration: COMPLETE

Scripts live in `projects/rewrite/migration/`. All are idempotent and re-runnable.

| Script | Purpose |
|---|---|
| `fetch_wp.py` | Pull raw WP REST data → `migration/raw/` |
| `transform.py` | Raw → S3 database layout → `migration/out/db/` |
| `fetch_media.py` | Download referenced originals → `migration/out/media/` |

### Results
- **512** posts, **56** pages, **43** non-empty categories (9 empty skipped), 17 tags
- **5,152** code blocks converted EnlighterJS → `<pre class="language-X"><code>`
- **634** tables given Bootstrap classes; **214** posts have an auto-generated TOC
- Post payload **9.9 MB** (avg 19 KB); index 256 KB; search index 130 KB
- **336** images (47.4 MB) uploaded to
  `s3://lovemesomecoding-storage-.../lovemesomecoding/prod/media/` with
  `Cache-Control: public, max-age=31536000, immutable`

### Verification (all passing)
| Check | Result |
|---|---|
| Code block source fidelity | **5152 / 5152 byte-identical** to WordPress source |
| URL preservation | **568 / 568** unchanged (`/{category}/{slug}`) |
| Index integrity | 512 index entries = 512 files; category counts sum to 512 |
| Referenced images resolvable | **257 / 257** present |
| Live `<script>` / `on*` handlers in output | **0** |
| Media download failures | **0 / 336** |

### Migration findings worth remembering
1. **Code samples contain raw HTML.** Several posts embed unescaped `<script>`,
   `<button onclick=…>`, `<style>` *inside* `<pre>` blocks. Parsing the document
   with an HTML parser makes these real elements and `get_text()` then silently
   deletes them — the sample renders as bare words with no visible size change.
   `transform.py` therefore extracts `<pre>` regions with a regex **before** any
   HTML parsing and reinserts them escaped. Any future re-run must preserve this
   ordering. URL rewriting also runs while code is stashed, so sample code is
   never URL-rewritten.
2. **1131 referenced image URLs → 257 originals.** The rest are WordPress resize
   variants (`foo-1024x463.jpeg`), collapsed back to the original. One original
   (`2019/08/disp.jpeg`) is referenced but absent from the media library — still
   served by DreamHost, so it was fetched directly.
3. **`css-applying-css` has malformed source**: MDN tooltip text pasted with
   unescaped tags inside a `title="…"` attribute (`title="The HTML <style> element…"`).
   This breaks attribute parsing; WordPress mis-renders it today too.
   `repair_attributes()` escapes angle brackets inside `title` values (2 fixed).
4. **No post has a featured image** (0/512) and there are **2 comments site-wide**.
   Post listings are therefore text-only by nature — which suits the w3schools
   layout well and removes the need for card thumbnails.
5. **The 9 empty categories** are dead taxonomy and should not appear in the nav.
6. `{{MEDIA_CDN}}` is a placeholder token in the generated content. Re-run
   `transform.py --media-cdn https://<distribution>` once Phase 0 creates the
   media CloudFront distribution.

### Not yet done
- Image optimization (WebP conversion, width caps) deliberately skipped. Largest
  image is 2.5 MB. Worth doing for Core Web Vitals before launch.

---

## 12. Phase 0 — AWS Foundation: IN PROGRESS

### Built so far (nothing here touches the live site)
| Resource | Identifier |
|---|---|
| Media CloudFront distribution | `EYALMP5J1OET3` → **`d2q2snz6diubfd.cloudfront.net`** |
| Origin Access Control | `E32X5SRICE1LXZ` (`lovemesomecoding-media-oac`) |
| Storage bucket policy | grants `s3:GetObject` to `cloudfront.amazonaws.com`, scoped by `AWS:SourceArn` |

The distribution's `OriginPath` is `/lovemesomecoding/prod`, so media URLs read
`https://d2q2snz6diubfd.cloudfront.net/media/2019/11/foo.png`. Both buckets stay fully
private (`BlockPublicPolicy: true`); CloudFront is the only reader.
Price class 100, HTTP/2+3, compression on, `CachingOptimized` policy.

**Set `NEXT_PUBLIC_MEDIA_CLOUDFRONT_URL=https://d2q2snz6diubfd.cloudfront.net`.**

### Content DB uploaded
`s3://lovemesomecoding-db-329580012644-us-west-2-an/lovemesomecoding/prod/` —
**615 objects, 11.2 MB**, regenerated with real CDN URLs (0 `{{MEDIA_CDN}}` placeholders left).

### Current live DNS (captured before any change)
```
lovemesomecoding.com.      A   69.163.227.84
www.lovemesomecoding.com.  A   69.163.227.84
ftp.lovemesomecoding.com.  A   69.163.227.84
NS -> ns1/ns2/ns3.dreamhost.com
```
**No MX, no TXT, no SPF/DMARC, no AAAA.** There is no email on this domain, which removes
the usual biggest risk of an NS migration.

### DNS migrated to Route 53 — DONE (2026-08-04)
Hosted zone **`Z000531818AC6P1IJ8LJL`**, nameservers:
`ns-153.awsdns-19.com` · `ns-835.awsdns-40.net` · `ns-1441.awsdns-52.org` · `ns-1876.awsdns-42.co.uk`

Procedure used (repeat this shape for any future zone move):
1. Create the zone and **mirror every existing record** (3 A records → `69.163.227.84`).
2. **Verify before flipping** — query the new Route 53 nameservers directly and diff against
   DreamHost's answers. All three matched exactly, so the flip was a guaranteed no-op.
3. Flip NS at the registrar (`route53domains update-domain-nameservers`, async operation).
4. Confirm the site stayed up throughout — homepage and a deep post URL both returned HTTP 200
   before, during, and after.

Propagation: Google (8.8.8.8) and Quad9 picked up the new NS immediately; Cloudflare (1.1.1.1)
was still serving the cached DreamHost delegation (old NS record had a 172800s TTL).
**The site continues to serve from DreamHost either way** — only DNS authority moved.

Rollback if ever needed: point the registrar's NS back at ns1/ns2/ns3.dreamhost.com.

### ACM certificate
`arn:aws:acm:us-east-1:329580012644:certificate/e30c1952-4bbb-4e9a-b448-16f86cc21944`
covering `lovemesomecoding.com` + `www.lovemesomecoding.com`.
**Status: ISSUED** — both domains validated SUCCESS.

### Remaining in Phase 0
- [ ] Site CloudFront distribution + OAC for the `lovemesomecoding.com` bucket (needs the cert)
- [ ] CloudFront Function for `/path` → `/path/index.html` rewriting and trailing-slash
      normalization (see §6 — WordPress serves `/a/b` with no trailing slash)
- [ ] SSM SecureString parameter for the JWT secret
- [ ] Custom 404 error response

**Nothing is pointed at AWS yet.** The A records still resolve to DreamHost, so the live
WordPress site is unaffected until we deliberately repoint them at cutover.

---

## 12. Changelog

- **2026-08-04** — Research complete: content inventory measured, AWS state verified,
  both reference projects analyzed, architecture options drafted.
- **2026-08-04** — Decisions locked (§8): SSG rebuild-on-publish · HTML kept as-is · comments
  dropped · FastAPI+Mangum · self-managed JWT. DNS confirmed to be Amazon Registrar inside the
  same AWS account, so cutover never leaves AWS.
- **2026-08-04** — **Phase 1 complete** (§11): all 512 posts + 56 pages + 336 images migrated and
  verified. Code-block fidelity bug found and fixed.
- **2026-08-04** — **Phase 0 mostly complete** (§12): media CloudFront live, content DB uploaded
  (615 objects), DNS moved to Route 53 with zero downtime, ACM cert ISSUED. Remaining: site
  CloudFront distribution, CloudFront Function for URL rewriting, SSM secret.
  Next: Phase 2 frontend.

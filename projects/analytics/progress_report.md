# Analytics — progress report

**Status:** built and verified locally — **not deployed, not committed.** Measurement ID `G-ETM6754MYL`.

## Findings (2026-09-29)
- Live homepage: no `gtag`, `googletagmanager`, `G-`/`UA-`/`GTM-` id, or any other analytics script.
- `lovemesomecoding_frontend`: no analytics code, no id in `.env.production`, nothing in git history.
- Old WordPress site (DreamHost, `69.163.227.84`) did not answer over HTTPS, so whether it had GA
  could not be checked. Any historical GA data would live in an old UA property (UA is shut down).
- No Content-Security-Policy is set anywhere, so Google's script domains need no allow-listing.
- `src/app/admin/layout.tsx` renders **inside** `src/app/layout.tsx` → the root layout alone
  cannot keep GA off `/admin`; the loader has to check the path.

## Proposed solution

### 1. GA4 property — owner: **Folau**
analytics.google.com → Admin → Create property "Love Me Some Coding" → Web stream
`https://lovemesomecoding.com`. Keep *Enhanced measurement* ON, including
**"Page changes based on browser history events"** — that is what counts Next.js client-side
navigations (`<Link>` soft navs), so no manual route-change tracking is needed.
Send the `G-XXXXXXXXXX` id. Then link Search Console to the property (Admin → Product links).

### 2. Frontend — owner: **Claude**
- `.env.production`: `NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX`. A GA id is public (it ships in every page),
  so committing it to the public repo is fine. `.env.development` gets nothing.
- New `src/components/Analytics.tsx`, rendered from `src/app/layout.tsx`:
  - renders nothing unless `NEXT_PUBLIC_GA_ID` is set **and** `NEXT_PUBLIC_ENV === 'prod'`;
  - inline bootstrap bails out when `location.pathname` starts with `/admin`, before loading
    `gtag/js` — so the admin page never requests Google at all;
  - loads `https://www.googletagmanager.com/gtag/js?id=…` async.
  Plain `<script>` tags rather than `@next/third-parties` — no new dependency, and the admin
  guard needs to run before the loader, which is easier to see in ten lines of our own.
- `scripts/verify-build.mjs`: new check — `out/index.html` and a sample post contain the GA id;
  `out/admin.html` does not.
- `npm run preview` (`:4321`) uses the prod build, so it *will* send hits; filter it with GA's
  internal-traffic rule or set a `debug_mode` flag for localhost. Decide during QA.

### 3. Optional events (phase 2) — owner: **Claude**
- `code_copy` from the existing delegated listener in `src/components/CodeCopy.tsx`
  (params: post path, code language) — the most useful engagement signal a tutorial site has.
- Outbound links and scroll depth come free with Enhanced measurement.

### 4. Deploy + verify — owner: **Claude** builds, **Folau** confirms in GA
`AWS_PROFILE=folau npm run deploy`, then: GA **Realtime** shows a visit; DevTools shows a
`collect?v=2` request on a post page; `/admin` makes no request to googletagmanager.com;
Playwright script in this folder asserts both.

## Decisions (2026-09-29)
- **No consent banner for now** (option a below). Revisit if EU traffic turns out to matter.
- **Code-copy tracking: yes**, shipped with page views rather than as a later phase.
- **Hostname guard added** (not in the original plan): the bootstrap only runs on
  `lovemesomecoding.com`/`www`, so `npm run preview` on `:4321` — a prod build — sends nothing.
  That removed the need for a GA internal-traffic filter.

## What was built (lovemesomecoding_frontend)
| File | Change |
|---|---|
| `.env.production` | `NEXT_PUBLIC_GA_ID=G-ETM6754MYL` |
| `src/components/Analytics.tsx` | new — inline gtag bootstrap; renders only when `NEXT_PUBLIC_ENV=prod` and the id matches `^G-[A-Z0-9]+$`; bails on `/admin(/…)` and on any other hostname before requesting Google |
| `src/app/layout.tsx` | renders `<Analytics />` in `<head>` |
| `src/components/CodeCopy.tsx` | fires `code_copy` `{language, page_path}` after a successful copy; `window.gtag?.` so it is a no-op wherever GA did not load |
| `scripts/verify-build.mjs` | check 9 — GA tag present on home, a post and a category page; `admin.html` carries the `/admin` guard. Warns (does not fail) if the id is unset |

## Verification
- `npm run build` → `analytics  G-ETM6754MYL on 3 sampled page(s), admin guarded`, all 938 posts served.
- `projects/analytics/verify_analytics.mjs` (Playwright) — 9/9 pass against the preview with
  `lovemesomecoding.com` mapped to `127.0.0.1:4321`. All Google requests are intercepted and
  aborted, so tests never send hits. Checks: gtag.js loads with the id; `config` issued; copy
  button still says "Copied"; exactly one `code_copy` with the real path and language; `/admin`
  makes zero Google requests and never touches `dataLayer`; `localhost:4321` sends nothing.
  After deploy: `BASE=https://lovemesomecoding.com node projects/analytics/verify_analytics.mjs`.
- Test gotcha: the mapped origin is plain http, so `navigator.clipboard` does not exist and
  headless Chromium ignores `--unsafely-treat-insecure-origin-as-secure`. The script stubs the
  clipboard for the local run only.

## Remaining
- [ ] **Deploy** — blocked on a decision: the frontend working tree also holds unrelated
      uncommitted edits (`cloudfront-function.js`, `postbuild.mjs`, `globals.css`, `pages.ts`)
      that `npm run deploy` would ship too.
- [ ] After deploy: GA Realtime shows a visit; run the script with `BASE=` against live.
- [ ] Folau: in GA, register `language` and `page_path` as **custom dimensions** (Admin → Custom
      definitions, event scope) or the `code_copy` params will not be reportable.
- [ ] Folau: link Search Console to the GA4 property.
- [ ] Commit (frontend + this folder) when asked.

## Options considered for consent
1. **Cookie consent.** GA4 sets cookies; EU/UK visitors legally need consent first. Options:
   (a) no banner — simplest, common for small blogs, carries GDPR risk;
   (b) Consent Mode v2 with `analytics_storage: 'denied'` by default + a small banner —
   compliant, GA models the missing data; (c) swap GA for cookieless analytics (e.g. Plausible,
   ~$9/mo, or Cloudflare Web Analytics, free) — no banner needed at all.

## Log
- 2026-09-29 — Confirmed GA absent; wrote this plan.
- 2026-09-29 — Got id `G-ETM6754MYL`; built, build check + Playwright 9/9 green. Not deployed.

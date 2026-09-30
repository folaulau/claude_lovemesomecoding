# Analytics — Google Analytics 4 on lovemesomecoding.com

## Goal
Know who reads the site and what they read. Today the only traffic signal is Search Console
(checked 2026-09-29: no GA, GTM or other analytics tag in the live HTML, the frontend code, or its
git history).

## Requirements
1. GA4 page views on every **public** page of https://lovemesomecoding.com (and `www`).
2. **Never** load on `/admin` — the admin console shares the root layout, so this must be explicit.
3. **Never** load in local dev (`:3000`) or the local preview unless deliberately turned on —
   dev traffic must not pollute the numbers.
4. No regression to the static-export contract: no runtime fetches beyond Google's own script,
   no change to URLs, canonicals or `trailingSlash`.
5. No measurable hit to page load: script loads `afterInteractive`/`async`, never blocks paint.
6. The build must prove the tag is present on public pages and absent from `/admin`
   (a new `verify-build.mjs` check), so it cannot silently disappear in a refactor.

## Out of scope (for now)
Google Tag Manager, AdSense, server-side tagging, a custom analytics dashboard.

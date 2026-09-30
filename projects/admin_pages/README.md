# Admin — editable static pages

## Goal
Edit https://lovemesomecoding.com/about-me (and the other static pages) from `/admin`, the same way
posts are edited, instead of hand-editing `pages/*.json` in S3.

## Requirements
- A **Pages** tab in the admin console listing the pages the site actually renders.
- Edit title and body with the same Visual / HTML / Preview editor posts use.
- **Edit-only** — no create, no delete, no slug/URL change: page URLs are live and the set of pages
  is fixed by `KEEP` in `lovemesomecoding_frontend/src/lib/pages.ts`.
- Saves go to S3 and reach the site on **Publish site**, like posts.

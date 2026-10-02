# Homepage "Most viewed" section — progress report

**Status:** built and verified locally (2026-10-02). Not deployed, not committed.

## Requirement
The homepage led with "Latest tutorials". Lead instead with a hand-picked list that grabs
attention: every post tagged `most-view` appears in that section.

## Decisions
- **Hand-curated tag, not analytics.** GA4 has only been live since 2026-09-29, so there is no
  view data to rank by yet. Revisit once there is a few months of it.
- **No backend change.** Tags are already editable in `/admin` (Tags field, comma separated) and
  are already in `index/posts.json`, which the homepage reads at build time.
- **Latest tutorials stays, below it.** `/page/2…` continue the homepage's latest list, so removing
  it would orphan their "‹ Newer" link back to `/`.
- **Section hides itself when no post has the tag** — the homepage looks exactly as before.
- Order follows the posts index (newest first). Cards, not the list style, to stand apart.

## What was built (lovemesomecoding_frontend)
| File | Change |
|---|---|
| `src/lib/content.ts` | `MOST_VIEWED_TAG = 'most-view'`, `postsWithTag(tag)` |
| `src/components/MostViewed.tsx` | new — card grid (category, title, 3-line excerpt, read time) |
| `src/app/page.tsx` | renders `MostViewed` above `LatestPosts` when non-empty |
| `src/app/globals.css` | `.mv-grid` / `.mv-card` |

## QA
- `tsc --noEmit` clean; `npm run build` passes `verify-build` (938/938 posts).
- Tagged 4 posts in the local `content/` copy only (S3 untouched), built, previewed on :4321:
  4 cards on `/`, none on `/page/2`; no horizontal scroll at 1280px or 390px; light + dark OK.
  Screenshots `home-*.png`, script `screenshot_home.mjs`. Local content restored afterwards.

## To go live — owner: Folau
1. `/admin` → edit each post you want featured → add `most-view` to Tags → Save.
2. Deploy the frontend code (`AWS_PROFILE=folau npm run deploy`) — Publish alone rebuilds from the
   source zip the last deploy uploaded, so the code change must be deployed once first.

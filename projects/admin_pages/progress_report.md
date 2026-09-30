# Admin pages — progress report

**Status:** built and verified locally — **not deployed, not committed** (2026-09-29).

## Decision
Folau chose a Pages tab covering all 12 live pages over About-Me-only or a one-off edit.

## What was built

### Backend (`lovemesomecoding_backend`)
| File | Change |
|---|---|
| `app/services/pages.py` | new — `EDITABLE_PAGES` allowlist (= frontend `KEEP`), list / get / update. Update keeps slug, url, date, wpId, status; rewrites title, body, toc, modified, updatedBy |
| `app/routers/pages.py` | new — `GET /pages`, `GET /pages/{slug}`, `PUT /pages/{slug}`; admin-only; 404 for anything off the allowlist or missing (PUT never creates) |
| `app/schemas.py` | `PageUpdate {title, contentHtml}`, `extra="forbid"` so a body cannot smuggle in `url` |
| `app/main.py` | registers the router |
| `tests/test_pages.py` | new — 13 tests incl. a check that `EDITABLE_PAGES` equals the frontend `KEEP` set |
| `tests/test_auth.py` | 3 new routes in the protected-route matrix (now 13) |

Bodies go through the same `content.normalize()` as posts (script/on* stripping, heading ids,
code-block shape). **Checked against all 12 live pages: normalising the stored body returns it
byte-for-byte**, so opening a page and saving without changes is a no-op.

### Frontend (`lovemesomecoding_frontend`)
| File | Change |
|---|---|
| `src/components/admin/BodyEditor.tsx` | new — the Visual/HTML/Preview tabs, toolbar, image upload and WordPress-markup warning, **extracted from PostEditor** so posts and pages share one editor |
| `src/components/admin/PostEditor.tsx` | uses BodyEditor; behaviour unchanged |
| `src/components/admin/PageEditor.tsx` | new — title + body + Save; shows the fixed live URL |
| `src/app/admin/page.tsx` | **Pages** button and view; pages load with posts/categories |
| `src/lib/api.ts` | `listPages`, `getPage`, `savePage` |

## Verification
- Backend: full suite green, coverage 95.7% (gate 90%); `services/pages.py` 100%.
- `npm run build` green (938/938 posts).
- `projects/admin_pages/verify_admin_pages.mjs` (Playwright, local stack, `local` S3 tree) —
  **15/15**: 12 pages listed; About Me loads; wrapper-markup warning shows; HTML tab holds the
  stored body byte-for-byte; preview renders the edit; save lands in `local/`, keeps
  `<div class="about-hero">`, url/date, records updatedBy; **prod untouched**; post editor still
  works after the extraction; no page errors. The script restores `local/pages/about-me.json`
  from prod afterwards. Screenshots in `screenshots/`.

## ⚠️ Use the HTML tab for About Me
About Me is built from styled `<div>` blocks (hero, stat boxes). The Visual editor cannot represent
them — it shows the warning, and the first keystroke there flattens the layout. Edit it in
**HTML**, check **Preview**, then Save.

## Remaining
- [ ] Deploy backend and frontend. Order does not matter: a failed `/pages` call yields an empty
      Pages list instead of breaking the post list (`listPages().catch(() => [])`).
- [ ] After deploy: edit About Me in `/admin`, Save, **Publish site** (needs the GitHub PAT in
      SSM — still outstanding per root CLAUDE.md; otherwise run `npm run deploy`).
- [ ] Commit both repos when asked.

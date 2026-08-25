# React Native Tutorial

## About
- this is for React Native tutorial

## Requirements
- create or update posts on https://lovemesomecoding.com/react-native collection
- the collection slug was `rea-native` (a typo, 5 placeholder posts — see progress_report.md).
  Rename it to
  `react-native`, rename the five `rea-native-*` post slugs to `react-native-*`, and redirect every
  old URL so nothing that is indexed stops resolving.
- use https://reactnative.dev/ and https://www.tutorialspoint.com/react_native/index.htm to generate topics and posts for this tutorial. Don't generate a post for everything single small thing. Focus only on important topics.
- use the /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-native-mobile project to give examples from.

---

## Layout

```
projects/react_native/
  manifest.py         category metadata + one entry per post (slug, title, date, tags, excerpt, sources)
  posts/NN-slug.html  the post bodies, plain semantic HTML   <- EMPTY, see progress_report.md
  seed.py             writes the category and posts into a content tree
  check_content.py    proves the normaliser round-trips every code sample (no AWS needed)
  check_snippets.py   proves every quoted snippet still matches the demo app (no AWS needed)
  add_redirects.py    writes the /rea-native -> /react-native redirects into the content tree
  retire_old.py       deletes the five 2018 originals and the old category, once replaced
  progress_report.md  status, decisions, the topic table and the rename runbook — read this first
```

## Status: ✅ live

All 25 post bodies are written — 100 code blocks, of which **88 are verbatim from**
`lovemesomecoding_demo_project/pizza/pizza-react-native-mobile` (Expo SDK 57, React Native 0.86,
React 19, TypeScript 6, expo-router) and verified by `check_snippets.py`.

**Published 2026-08-24** (build `394b0bd`). All 25 live at
https://lovemesomecoding.com/react-native, the `rea-native` → `react-native` rename is complete, and
all six old URLs 301 to their replacements. The rename runbook in `progress_report.md` is done end
to end.

`progress_report.md` holds the topic table, the decisions and the ordered rename runbook.

## Commands

Run from the repo root. The two checkers need no AWS credentials; the three writers do.

```bash
# Verify the manifest and any written content
lovemesomecoding_backend/.venv/bin/python projects/react_native/check_content.py

# Verify every quoted snippet still matches the demo app. Run BOTH — they check
# different things, and only this one goes stale on its own.
python3 projects/react_native/check_snippets.py

# Dry runs — report what would happen and write nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/react_native/seed.py --env local
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/react_native/add_redirects.py --env local
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/react_native/retire_old.py --env local

# Add --write to any of them to actually write.
```

`seed.py` is idempotent — a re-run updates the posts in place.

### `--only`

`seed.py` refuses to run while any post file is missing, which is right for publishing and useless
for drafting. `--only` seeds a subset so a post can be previewed at `:3000` while the rest of the
track is unwritten:

```bash
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/react_native/seed.py \
  --env local --only react-native-introduction --write
```

It does not make the track publishable — a full `--env prod` run still needs all 25 files.

### Re-dating the track

Dates are computed, not hard-coded. Edit `START_DATE` (and `STEP_DAYS`) in `manifest.py` and the
whole track re-bases in order.

## Adding or updating a post

1. Edit or add the HTML in `posts/`. Add or update its entry in `manifest.py`.
2. To insert mid-track, add it to `_TRACK` in reading position — dates and `NN-` filenames are
   derived from that order, so nothing else needs renumbering.
3. If it is a **new** post, add it to the lesson index in `posts/01-react-native-introduction.html`.
4. `check_content.py` and `check_snippets.py`, then seed `--env local --write`, then review at `:3000`.
5. Seed `--env prod --write`, then `cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy`.

## The rename

`rea-native` -> `react-native` is a multi-step migration with a strict order, because a post's slug
IS its URL and there is no rename operation — the new posts are created, then the originals are
deleted. **The full runbook is in `progress_report.md`.** The short version:

seed -> add redirects -> apply the staged frontend edits -> deploy -> retire the originals -> deploy.

Deleting before redirecting leaves five URLs indexed since 2018 returning 404.


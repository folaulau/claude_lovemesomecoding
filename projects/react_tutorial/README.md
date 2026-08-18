# React tutorial track

A 27-post React tutorial published under **`/react`** on lovemesomecoding.com.

```
projects/react_tutorial/
  manifest.py        category metadata + one entry per post (slug, title, date, tags, excerpt)
  posts/NN-slug.html the post bodies, plain semantic HTML
  seed.py            writes the category and posts into a content tree
  check_content.py   proves the normaliser round-trips every code sample (no AWS needed)
  progress_report.md status, decisions and the full topic table — read this first
```

## What this replaced

`/react` held **17 posts published in 2019**: copied from w3schools, class components and
`this.setState`, 13–957 words each, still carrying WordPress `boldgrid-section` wrapper divs.

All 17 were **rewritten in place — same slugs, so no URL was lost** — and 10 new posts added for the
topics hooks-era React needs and no existing slug covered, including a `react-get-started` landing
page at the front and `react-interview-questions` at the end. See `progress_report.md` for the topic
table and which is which.

## Original requirements

- Draw on https://react.dev and https://www.w3schools.com/react/default.asp — the main topics, not
  everything.
- Use `lovemesomecoding_demo_project/pizza/pizza-react-frontend` for every example. Where the app
  lacked one, extend the app first and snippet from the result.
- Keep the topic list explicit, so the next revision is an update-and-add rather than a rewrite.

Both gaps were closed rather than faked: Redux Toolkit was added to the admin area, and the
stylesheet was converted to Sass. Every snippet in the track is running code.

## Versions the track is written against

Stated on lesson 1 and assumed throughout. **When these move, that table is the first edit.**

| | |
|---|---|
| react / react-dom | **19.2** |
| typescript | 6.0 |
| vite / @vitejs/plugin-react | 8.2 / 6.0 |
| react-router-dom | 7.18 |
| react-bootstrap / bootstrap | 2.10 / 5.3 |
| @reduxjs/toolkit / react-redux | 2.12 / 9.3 |
| sass | 1.102 |
| Node.js | 22 (20.19 is Vite 8's minimum) |

## Commands

Run from the repo root. `check_content.py` needs no AWS credentials; `seed.py` does.

```bash
# Verify the content before writing anything anywhere
lovemesomecoding_backend/.venv/bin/python projects/react_tutorial/check_content.py

# Dry run — reports create/update per post and writes nothing
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/react_tutorial/seed.py --env local

AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/react_tutorial/seed.py --env local --write
AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python projects/react_tutorial/seed.py --env prod  --write
```

`seed.py` is idempotent — a re-run updates the posts in place.

### `--force-dates`

`upsert_post` never overwrites an existing post's `date`, so the 17 rewritten posts would have kept
their 2019 timestamps and the track would have read in the wrong order. `--force-dates` stamps the
manifest date onto a post that already exists.

**It was needed once, for the initial publish, and should not be used again** unless you are
deliberately reordering the track — every run without it leaves the archive alone, which is what you
want the rest of the time.

## Adding or updating a post

1. Edit or add the HTML in `posts/`. Add or update its entry in `manifest.py`.
2. To insert mid-track, give it a date between its neighbours and renumber the `NN-` file prefixes.
   The prefixes are for humans only — `manifest.py` order and `date` are what the site uses.
3. If it is a **new** post, add it to the lesson index in `posts/01-react-get-started.html`.
4. `check_content.py`, then seed `--env local --write`, then review at `:3000`.
5. Seed `--env prod --write`, then `cd lovemesomecoding_frontend && AWS_PROFILE=folau npm run deploy`.

## Gotchas paid for already

- **The snippets are TypeScript, so the posts use `language-tsx` and `language-typescript`.** Neither
  end of the pipeline knew those names. `app/services/content.py` now lists `typescript`, `jsx` and
  `tsx` in `SUPPORTED_LANGUAGES`, and `src/lib/content.ts` static-imports `prism-typescript`,
  `prism-jsx` and `prism-tsx` — in that order, because `tsx` depends on the other two.
  The `"ts": "javascript"` alias was **left alone on purpose**: it is what the 512 migrated posts
  used, and remapping it would change how they highlight on their next save.
- ⚠️ **The backend Lambda still has the old language list.** Seeding runs the local service layer, so
  what is in S3 is correct — but editing one of these posts through `/admin` before
  `lovemesomecoding_backend/scripts/deploy.sh` runs would normalise its `tsx` blocks down to
  `plaintext` and silently lose the highlighting.
- **Do not hand-escape JSX in a `<pre>`.** Post bodies are full of `<Component />`, and one missed
  `&lt;` is invisible until it renders. `check_content.py` compares authored source against the
  normaliser's output byte-for-byte and is the only thing that catches it.
- **Slugs are frozen.** 17 of these are indexed URLs from 2019.

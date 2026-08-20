# Python Advanced

## About
- this tutorial is the advanced half of the Python track

## Requirements
- update the posts on https://lovemesomecoding.com/python-advanced
- keep posts to the point.
- update all posts in the tutorial.
- update posts and keep content to the point and not too lengthy if they don't have to.
- use this project for examples /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/bank/bank-python-console
- if examples are not found in that project, add them and make sure your added code changes don't
  break existing code.

## Scope

This track is the continuation of `/python` (26 posts, `projects/python_tutorial/`), not a parallel
one. It assumes that track and links back to it rather than re-explaining anything it covers.

Three of these eight posts duplicated `/python` once that track was expanded on 2026-08-20. All
eight slugs are indexed, so none was deleted — the three were repointed to go deeper.
`manifest.OVERLAP` records the boundary for each. See `progress_report.md`.

## Snippets

Standalone and **executed**, same contract as `/python`. The addition here is that half this track
is about third-party libraries, so `check_snippets.py` runs those blocks in a pinned virtualenv:

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-check.txt
./check.sh
```

A block marked `<!-- needs: numpy -->` runs in that venv under 3.12 only. The marker is mandatory —
the checker refuses an unmarked block that imports anything in `manifest.THIRD_PARTY`.

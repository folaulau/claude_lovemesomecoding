# iOS Tutorial

## About
- this is for the native iOS (Swift + SwiftUI) tutorial

## Requirements
- create a new tutorial collection for iOS. Add a **Mobile** dropdown to the nav, between
  "Software Engineering" and "JavaScript", and put the iOS collection under it.
- keep posts to the point. Don't generate a post for every small thing — cover the topics that
  matter.
- use the
  `/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-ios-mobile`
  project for every example. Code in these posts must be code that runs.

---

## Layout

```
projects/ios_tutorial/
  manifest.py         category metadata + one entry per post (slug, title, date, tags, excerpt, sources)
  posts/NN-slug.html  the post bodies, plain semantic HTML
  seed.py             writes the category and posts into a content tree
  check_content.py    length budget, prose share, heading and markup rules (no AWS needed)
  check_snippets.py   proves every quoted snippet still matches the demo app (no AWS needed)
  progress_report.md  status, decisions and the topic table — read this first
```

## Running it

```bash
python projects/ios_tutorial/check_content.py     # length, structure, markup
python projects/ios_tutorial/check_snippets.py    # snippets vs the real app
python projects/ios_tutorial/seed.py              # dry run against the local tree
python projects/ios_tutorial/seed.py --env local --write
```

The nav is a **separate step** `seed.py` cannot do — see `lovemesomecoding_frontend/src/lib/nav.ts`.

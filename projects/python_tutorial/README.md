# Python Tutorial

## About
- this tutorial is for Python tutorial

## Requirements
- update python posts on https://lovemesomecoding.com/python
- update python posts on https://lovemesomecoding.com/python-advanced
- keep posts to the point.
- update all posts in the tutorial.
- update posts and keep content to the point and not too lengthy if they don't have to.
- update or add a Get Started page and mention what version of Python is being used in the
  tutorial. On this get started page, have a section there where we list out the major Python 3
  releases and the new features that came out on each release. (Python has no LTS releases the way
  Java does — the table is 3.9 through 3.14, one row per release.)
- use this project for examples /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/bank/bank-python-console
- if examples are not found in the /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/bank/bank-python-console project, add them and make sure your added code changes don't break existing code.

## Note on the last two requirements

Folau's call on 2026-08-20: this track takes the same exception `/java` took. The basics posts
write **standalone** snippets rather than lifting them from the bank app — `total = 0` has no
business being traced back to a console banking app, and framework-flavoured code is the wrong
register for post 1. The exception is paid for with a checker: `check_snippets.py` **runs** every
code block under Python 3.12 and 3.14, and verifies the `# Output:` comments the posts claim.

Where a post genuinely is about the demo app's territory, a block may still be lifted from
`bank-python-console` with a `<!-- from: bank/services.py -->` marker, which `check_provenance.py`
verifies. See `progress_report.md`.

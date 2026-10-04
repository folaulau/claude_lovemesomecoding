# AI-Assisted Engineering

## About
- A tutorial series on **how an engineer should use an AI assistant (Claude) across the whole
  development lifecycle**: analysis, requirements, planning, code, tests, debugging, AWS
  investigation, UI walkthroughs, PRs, PR review, and customer support.
- Audience: aspiring and working developers. The message is "you own the output": every post shows
  how to verify what the assistant produced, not just how to prompt it.

## Requirements (agreed 2026-10-04)
- **New category** `ai-engineering`, alongside the existing `claude` category. The 10 older Claude
  Code basics posts stay where they are, and this series links to them rather than repeating them.
  Nav: append to the existing **AI** group in `lovemesomecoding_frontend/src/lib/nav.ts`.
- **Examples come from the pizza demo app**
  (`lovemesomecoding_demo_project/pizza`: Spring Boot backend, React/Angular frontends, iOS/RN apps).
  Prompts, outputs, diffs and PRs shown in a post must come from a real session against that code.
- **Claude Code first.** Bring in claude.ai, Claude in Chrome or MCP servers only where the task needs
  them (support replies, UI walkthroughs, AWS/GitHub access).
- **To the point, 5–8 min per post.** One workflow per post: real prompt → real output → how to
  verify it → a short checklist.
- **Core theme: read the code, follow the plan, don't just click Accept** (added 2026-10-04).
  The engineer's job has shifted from typing code to reviewing it: read every diff, hold the
  assistant to the agreed plan, and reject drift. This gets its own post (#2), and **every post ends
  with a "Before you accept" section** listing what to read and check for that workflow. Show at least
  one real case per post where accepting blindly would have shipped a bug or wandered off the plan.

## Layout (mirrors projects/ios_tutorial)
```
projects/ai_engineering/
  manifest.py         category metadata + one entry per post
  posts/NN-slug.html  post bodies, plain semantic HTML
  seed.py             writes the category and posts into a content tree
  check_content.py    length, structure, markup rules
  progress_report.md  status, decisions, topic table (read first)
```

#!/usr/bin/env python3
"""Each post's closing link should point at the post that actually follows it.

A "Next" paragraph that names the wrong post is not a broken link — it resolves
fine — so nothing else catches it. It just quietly sends the reader past a post.
One such error was already live in the 29-post track (Operators pointed at
Conditional Statements, skipping String) and would have survived the merge.

    python projects/java_merge/check_flow.py
"""
import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

LINK = re.compile(r'<a href="/java/([a-z0-9-]+)"')
order = [p["slug"] for p in manifest.POSTS]
nxt = {s: order[i + 1] for i, s in enumerate(order[:-1])}

problems, checked, missing = [], 0, 0
for i, entry in enumerate(manifest.POSTS):
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        continue
    slug = entry["slug"]
    html = path.read_text(encoding="utf-8")
    # The closing section is where a "next" pointer lives.
    tail = html[html.rfind("<h2"):] if "<h2" in html else html
    links = LINK.findall(tail)
    if slug not in nxt:
        checked += 1
        continue                      # last post: nothing to point at
    if not links:
        missing += 1
        problems.append(f"{slug}: closing section has no link (should lead to {nxt[slug]})")
        continue
    checked += 1
    if nxt[slug] not in links:
        problems.append(f"{slug}: closing links to {links} — the next post is {nxt[slug]}")

print(f"checked {checked} posts")
if problems:
    print(f"\n{len(problems)} flow problem(s):")
    for p in problems:
        print(f"  x {p}")
    sys.exit(1)
print("every post leads to the one that follows it")

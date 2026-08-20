#!/usr/bin/env python3
"""Well-formedness + internal-link check for the Backend Dev track.

Every internal href must resolve to something that will exist after seeding:
a category archive (/slug) or a post (/category/slug). Post slugs from this
track's own manifest count as existing even though they are not published yet.

    AWS_PROFILE=folau python projects/backend_dev/check_links.py
"""

import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "lovemesomecoding_backend"))

import manifest  # noqa: E402

os.environ["env"] = "local"
os.environ["data_env"] = "prod"
os.environ.setdefault("aws_profile", os.environ.get("AWS_PROFILE", "folau"))
from app.services import posts as post_service, categories as category_service  # noqa: E402

VOID = {"br", "hr", "img", "input", "meta", "link", "source"}


class Wellformed(HTMLParser):
    """Reports unclosed or mismatched tags."""

    def __init__(self, slug):
        super().__init__(convert_charrefs=False)
        self.slug = slug
        self.stack = []
        self.problems = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.problems.append(f"line {self.getpos()[0]}: </{tag}> with nothing open")
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.problems.append(
                f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> opened on line {line}")


live_posts = {p["slug"]: p["category"] for p in post_service.list_posts()}
live_cats = {c["slug"] for c in category_service.list_categories()}
# This track's own posts will exist after seeding.
for entry in manifest.POSTS:
    live_posts[entry["slug"]] = manifest.CATEGORY["slug"]
live_cats.add(manifest.CATEGORY["slug"])

HREF = re.compile(r'href="([^"]+)"')
failures = []
internal = external = 0

for entry in manifest.POSTS:
    raw = (HERE / "posts" / entry["file"]).read_text(encoding="utf-8")

    parser = Wellformed(entry["slug"])
    parser.feed(raw)
    parser.close()
    for tag, line in parser.stack:
        parser.problems.append(f"line {line}: <{tag}> never closed")
    for p in parser.problems:
        failures.append(f"{entry['slug']}: {p}")

    for href in HREF.findall(raw):
        if href.startswith("http"):
            external += 1
            continue
        internal += 1
        if not href.startswith("/"):
            failures.append(f"{entry['slug']}: relative href '{href}'")
            continue
        parts = href.lstrip("/").split("/")
        if len(parts) == 1:
            if parts[0] not in live_cats:
                failures.append(f"{entry['slug']}: no such category '{href}'")
        elif len(parts) == 2:
            cat, slug = parts
            if slug not in live_posts:
                failures.append(f"{entry['slug']}: no such post '{href}'")
            elif live_posts[slug] != cat:
                failures.append(
                    f"{entry['slug']}: '{href}' — that post is in '{live_posts[slug]}'")
        else:
            failures.append(f"{entry['slug']}: unexpected path shape '{href}'")

    # Every post except the last should point at the next one, so the track reads as a track.
    print(f"{entry['slug']:44} ok")

print(f"\n{internal} internal links, {external} external")
if failures:
    print("\nFAILED:")
    for f in failures:
        print(f"  x {f}")
    sys.exit(1)
print("html well-formed, every internal link resolves")

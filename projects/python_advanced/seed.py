#!/usr/bin/env python3
"""Write the Python Advanced category and its posts into a content tree.

Runs the backend's own service layer rather than touching S3 directly, so the
post objects, the post index, the category archive, the category counts and the
search index are all maintained by the same code the admin API uses. Anything
else would risk the derived indexes drifting from the posts, and the static
build reads only the indexes.

    # dry run against the local tree (default)
    python projects/python_advanced/seed.py

    python projects/python_advanced/seed.py --env local --write
    python projects/python_advanced/seed.py --env prod  --write

Idempotent: re-running updates the posts in place. `date` is only applied when a
post is new, so a re-run never reshuffles the archive.

The 17 pre-existing slugs were published between 2020-03 and 2021-03 and
therefore already carry dates that upsert_post will not overwrite. `--force-dates`
stamps the manifest date onto an existing post before upserting it, which is what
makes the reworked track read in reading order. It is not the default: without it
a re-run leaves the archive alone, which is the behaviour you want every other
time.
"""

import argparse
import importlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
BACKEND = REPO_ROOT / "lovemesomecoding_backend"

sys.path.insert(0, str(HERE))
import manifest  # noqa: E402


def load_backend(data_env: str):
    """Import the backend services with the target tree selected.

    app/config.py reads os.environ at import time, so the environment has to be
    set before the first import — and re-selecting a tree means reloading the
    modules that captured the prefix.
    """
    os.environ["env"] = "local"  # use the named AWS profile, not a Lambda role
    os.environ["data_env"] = data_env
    os.environ.setdefault("aws_profile", os.environ.get("AWS_PROFILE", "folau"))
    sys.path.insert(0, str(BACKEND))

    from app import config

    importlib.reload(config)
    from app.services import posts, categories, s3

    importlib.reload(s3)
    importlib.reload(posts)
    importlib.reload(categories)
    s3.reset_repo()
    return config, posts, categories


def read_post_html(entry: dict) -> str:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        raise SystemExit(f"missing content file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=("local", "prod"), default="local")
    parser.add_argument("--write", action="store_true",
                        help="actually write. Without it, only report what would happen.")
    parser.add_argument("--force-dates", action="store_true",
                        help="stamp the manifest date onto posts that already exist. "
                             "Needed once, to reorder the 17 reworked 2020-2021 posts.")
    parser.add_argument("--author", default="folauk")
    args = parser.parse_args()

    config, post_service, category_service = load_backend(args.env)
    prefix = config.db_prefix()
    print(f"target  s3://{config.DB_BUCKET}/{prefix}/")
    print(f"posts   {len(manifest.POSTS)}")
    print(f"mode    {'WRITE' if args.write else 'dry run'}\n")

    index_before = len(post_service.list_posts())
    print(f"published posts in this tree before: {index_before}")

    # Fail early rather than half-seeding: every file must exist and no slug may
    # already belong to a different category.
    bodies = {}
    for entry in manifest.POSTS:
        bodies[entry["slug"]] = read_post_html(entry)
        existing = post_service.get_post(entry["slug"])
        if existing and existing.get("category") != manifest.CATEGORY["slug"]:
            raise SystemExit(
                f"slug collision: {entry['slug']} already exists in category "
                f"'{existing['category']}'. Post slugs are global."
            )

    if not args.write:
        for entry in manifest.POSTS:
            existing = post_service.get_post(entry["slug"])
            state = "update" if existing else "create"
            note = ""
            if existing and existing.get("date") != entry["date"]:
                note = (f"  date {existing.get('date')} -> {entry['date']}"
                        if args.force_dates
                        else f"  date stays {existing.get('date')} (use --force-dates)")
            print(f"  {state:6}  /{manifest.CATEGORY['slug']}/{entry['slug']}"
                  f"  ({len(bodies[entry['slug']]):,} bytes){note}")
        print("\nnothing written. Re-run with --write.")
        return 0

    category = category_service.upsert_category(manifest.CATEGORY)
    print(f"category {category['slug']} -> {category['url']}")

    for entry in manifest.POSTS:
        if args.force_dates:
            # upsert_post keeps `existing["date"]`, so the only way to move a
            # published post's date is to change it on the stored object first.
            # The upsert below then re-sorts every index that mentions it.
            existing = post_service.get_post(entry["slug"])
            if existing and existing.get("date") != entry["date"]:
                existing["date"] = entry["date"]
                post_service.repo().put_json(post_service.post_key(entry["slug"]), existing)

        record = post_service.upsert_post(
            {
                "slug": entry["slug"],
                "title": entry["title"],
                "category": manifest.CATEGORY["slug"],
                "contentHtml": bodies[entry["slug"]],
                "tags": entry.get("tags", []),
                "excerpt": entry.get("excerpt"),
                "status": "published",
                "date": entry["date"],
            },
            author=args.author,
        )
        print(f"  {record['url']:52} {record['date']}  "
              f"{record['wordCount']:>5} words  {record['readingMinutes']} min  "
              f"{len(record['toc'])} headings")

    # Report the state the static build will actually see.
    archive = post_service.list_posts(category=manifest.CATEGORY["slug"])
    total = len(post_service.list_posts())
    counts = {c["slug"]: c["count"] for c in category_service.list_categories()}
    print(f"\narchive /{manifest.CATEGORY['slug']} holds {len(archive)} posts, "
          f"newest first: {archive[0]['slug']}")
    print(f"category count recorded: {counts.get(manifest.CATEGORY['slug'])}")
    print(f"published posts in this tree now: {total} (was {index_before})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

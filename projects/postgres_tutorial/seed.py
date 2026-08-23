#!/usr/bin/env python3
"""Write the Postgres category and its posts into a content tree.

Runs the backend's own service layer rather than touching S3 directly, so the post objects, the
post index, the category archive, the category counts and the search index are all maintained by
the same code the admin API uses. Anything else would risk the derived indexes drifting from the
posts, and the static build reads only the indexes.

    # dry run against the local tree (default)
    python projects/postgres_tutorial/seed.py

    python projects/postgres_tutorial/seed.py --env local --write
    python projects/postgres_tutorial/seed.py --env prod  --write

Idempotent: re-running updates the posts in place. `date` is only applied when a post is new, so a
re-run never reshuffles the archive.

⚠️ TWO of the eighteen slugs — `postgres-introduction` and `postgres-installation` — were
published in February 2020 and therefore already carry dates that upsert_post will not overwrite.
`--force-dates` stamps the manifest date onto an existing post before upserting it, which is what
makes the rewritten track read in lesson order. Without it the archive buries the two rewritten
posts six years under the other sixteen and the ‹ prev / next › pager reads nonsense.

It is not the default: without it a re-run leaves the archive alone, which is the behaviour you
want every other time. Expect to pass it exactly once per tree.
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

    app/config.py reads os.environ at import time, so the environment has to be set before the
    first import — and re-selecting a tree means reloading the modules that captured the prefix.
    """
    os.environ["env"] = "local"  # use the named AWS profile, not a Lambda role
    os.environ["data_env"] = data_env
    os.environ.setdefault("aws_profile", os.environ.get("AWS_PROFILE", "folau"))
    sys.path.insert(0, str(BACKEND))

    from app import config

    importlib.reload(config)
    from app.services import categories, posts, s3

    importlib.reload(s3)
    importlib.reload(posts)
    importlib.reload(categories)
    s3.reset_repo()
    return config, posts, categories


def read_post_html(entry: dict) -> str:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        raise SystemExit(
            f"missing content file: {path}\n"
            "Every SQL sample in this track is executed against the stayhub_lab database built "
            "by lab/setup.sh. Run check_content.py and check_sql.py before seeding — see "
            "progress_report.md."
        )
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=("local", "prod"), default="local")
    parser.add_argument("--write", action="store_true",
                        help="actually write. Without it, only report what would happen.")
    parser.add_argument("--force-dates", action="store_true",
                        help="stamp the manifest date onto posts that already exist. "
                             "Needed once, to reorder the two rewritten 2020 posts.")
    parser.add_argument("--only", default=None,
                        help="comma-separated slugs to seed, instead of the whole track. "
                             "For previewing a post while the rest are still unwritten — the "
                             "track is not publishable until every file exists.")
    parser.add_argument("--author", default="folauk")
    args = parser.parse_args()

    posts = manifest.POSTS
    if args.only:
        wanted = [slug.strip() for slug in args.only.split(",") if slug.strip()]
        known = {entry["slug"] for entry in manifest.POSTS}
        unknown = [slug for slug in wanted if slug not in known]
        if unknown:
            raise SystemExit(f"not in the manifest: {', '.join(unknown)}")
        posts = [entry for entry in manifest.POSTS if entry["slug"] in wanted]

    config, post_service, category_service = load_backend(args.env)
    prefix = config.db_prefix()
    print(f"target  s3://{config.DB_BUCKET}/{prefix}/")
    print(f"posts   {len(posts)}" + (f" of {len(manifest.POSTS)} (--only)" if args.only else ""))
    print(f"mode    {'WRITE' if args.write else 'dry run'}\n")

    index_before = len(post_service.list_posts())
    print(f"published posts in this tree before: {index_before}")

    # A frozen slug that is missing from the target tree means the URL this rewrite is meant to
    # land on does not exist there. Harmless on `local`, which is seeded from a copy — but on
    # `prod` it means the slug is wrong, and upserting would mint a NEW url rather than rewrite
    # the indexed one.
    #
    # ⚠️ This runs BEFORE the post bodies are read, deliberately. While the track is being
    # authored every file is missing, and a guard placed after the file check is one that never
    # runs until the day it finally matters.
    if not args.only:
        absent = [slug for slug in sorted(manifest.FROZEN_SLUGS)
                  if not post_service.get_post(slug)]
        if absent:
            message = "frozen slugs not present in this tree: " + ", ".join(absent)
            if args.env == "prod":
                raise SystemExit(
                    message + "\nThese are supposed to be the indexed 2020 URLs being rewritten "
                    "in place. Seeding would create new pages instead. Check the slugs before "
                    "writing to prod.")
            print(f"note: {message}")
        else:
            print(f"all {len(manifest.FROZEN_SLUGS)} frozen slugs present — "
                  "every rewrite lands on its existing URL")

        # ⚠️ And the reverse: a NEW slug that already exists is not a new post, it is an
        # accidental overwrite of somebody else's page. Post slugs are global across categories.
        collisions = [slug for slug in sorted(manifest.NEW_SLUGS)
                      if post_service.get_post(slug)]
        if collisions:
            raise SystemExit(
                "slugs marked `new` already exist in this tree: " + ", ".join(collisions) +
                "\nSeeding would overwrite them. Either they are not new, or the slug is wrong.")

    # Fail early rather than half-seeding: every file must exist and no slug may already belong to
    # a different category.
    bodies = {}
    for entry in posts:
        bodies[entry["slug"]] = read_post_html(entry)
        existing = post_service.get_post(entry["slug"])
        if existing and existing.get("category") != manifest.CATEGORY["slug"]:
            raise SystemExit(
                f"slug collision: {entry['slug']} already exists in category "
                f"'{existing['category']}'. Post slugs are global."
            )

    if not args.write:
        for entry in posts:
            existing = post_service.get_post(entry["slug"])
            state = "update" if existing else "create"
            note = ""
            if existing and existing.get("date") != entry["date"]:
                note = (f"  date {existing.get('date')[:10]} -> {entry['date'][:10]}"
                        if args.force_dates
                        else f"  date stays {existing.get('date')[:10]} (use --force-dates)")
            print(f"  {state:6}  /{manifest.CATEGORY['slug']}/{entry['slug']}"
                  f"  ({len(bodies[entry['slug']]):,} bytes){note}")
        print("\nnothing written. Re-run with --write.")
        return 0

    category = category_service.upsert_category(manifest.CATEGORY)
    print(f"category {category['slug']} -> {category['url']}  name={category['name']!r}")

    for entry in posts:
        if args.force_dates:
            # upsert_post keeps `existing["date"]`, so the only way to move a published post's
            # date is to change it on the stored object first. The upsert below then re-sorts
            # every index that mentions it.
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
        flag = ""
        if record["readingMinutes"] > manifest.TARGET_MINUTES[1]:
            flag = f"  ⚠️ over {manifest.TARGET_MINUTES[1]} min"
        print(f"  {record['url']:52} {record['date'][:10]}  "
              f"{record['wordCount']:>5} words  {record['readingMinutes']:>2} min  "
              f"{len(record['toc'])} headings{flag}")

    # Report the state the static build will actually see.
    archive = post_service.list_posts(category=manifest.CATEGORY["slug"])
    total = len(post_service.list_posts())
    counts = {c["slug"]: c["count"] for c in category_service.list_categories()}
    print(f"\narchive /{manifest.CATEGORY['slug']} holds {len(archive)} posts, "
          f"newest first: {archive[0]['slug']}")
    print(f"category count recorded: {counts.get(manifest.CATEGORY['slug'])}")
    print(f"published posts in this tree now: {total} (was {index_before})")

    if len(archive) != len(manifest.POSTS) and not args.only:
        print(f"\n⚠️  archive holds {len(archive)} but the manifest has "
              f"{len(manifest.POSTS)} — something else is in this category.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Write the AWS category and its posts into a content tree.

Runs the backend's own service layer rather than touching S3 directly, so the post objects, the
post index, the category archive, the category counts and the search index are all maintained by
the same code the admin API uses. Anything else would risk the derived indexes drifting from the
posts, and the static build reads only the indexes.

    # dry run against the local tree (default)
    python projects/aws_tutorial/seed.py

    python projects/aws_tutorial/seed.py --env local --write
    python projects/aws_tutorial/seed.py --env prod  --write

Idempotent: re-running updates the posts in place.

⚠️ THERE IS NO `--force-dates` HERE, AND THAT IS DELIBERATE.

The Postgres and FastAPI tracks both need one, because both compute their dates from a START_DATE
and both had to re-base a whole track onto its real publication day. `upsert_post` never overwrites
an existing date, so those tracks need a way to override it.

This track is the opposite case. All 33 posts were published between 2018-10 and 2019-09, every
date already ascends, and every URL is indexed. The dates in manifest.py are TRANSCRIBED from the
stored posts rather than computed, so `upsert_post` keeping the existing date is precisely the
behaviour we want: a re-seed cannot reshuffle a published archive even by accident.

Adding the flag "for symmetry" would add exactly one capability — silently moving 33 indexed posts
in the sitemap — so it is left out. If a date genuinely has to move, that is a considered change to
manifest.py plus a flag written on purpose. See progress_report.md.

Staging: `--only` seeds a subset, which is how stage 1 (the seven blank posts) goes out before the
other 26 are written. The frozen-slug guard below still runs against the whole manifest.
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
            "Every `aws` command in this track is validated against the botocore service model "
            "before it ships. Run check_content.py and check_aws.py before seeding — see "
            "progress_report.md. To seed a stage before the rest is written, pass --only."
        )
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=("local", "prod"), default="local")
    parser.add_argument("--write", action="store_true",
                        help="actually write. Without it, only report what would happen.")
    parser.add_argument("--only", default=None,
                        help="comma-separated slugs to seed, instead of the whole track. This "
                             "is how a stage ships. Unlike the other tracks every slug here is "
                             "ALREADY live, so a partial seed leaves no half-built archive — it "
                             "just updates fewer posts.")
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
    #
    # ⚠️ And it runs REGARDLESS of --only, which is where this differs from the Postgres track.
    # There, --only meant "preview one of the new posts" and the guard was about the two frozen
    # ones, so skipping it was harmless. Here EVERY slug is frozen and --only is the normal way
    # a stage ships, so gating this on `not args.only` would mean the guard never runs at all —
    # on precisely the track where all 33 URLs are indexed. It validates the manifest against the
    # tree, which does not depend on which subset is being written.
    absent = [slug for slug in sorted(manifest.FROZEN_SLUGS)
              if not post_service.get_post(slug)]
    if absent:
        message = "frozen slugs not present in this tree: " + ", ".join(absent)
        if args.env == "prod":
            raise SystemExit(
                message + "\nThese are supposed to be the indexed 2018-2019 URLs being "
                "rewritten in place. Seeding would create new pages instead. Check the slugs "
                "before writing to prod.")
        print(f"note: {message}")
    else:
        print(f"all {len(manifest.FROZEN_SLUGS)} frozen slugs present — "
              "every rewrite lands on its existing URL")

    if not args.only:
        # ⚠️ And the reverse: a NEW slug that already exists MAY be an accidental overwrite of
        # somebody else's page, because post slugs are global across categories.
        #
        # "May be", not "is" — once this track has been seeded, every `new` slug exists and it is
        # ours. What still has to fail is a slug sitting in a DIFFERENT category: upserting that
        # would drag a stranger's page into /aws and rewrite its body. So the check is on the
        # category, not on mere existence. Keep it that way — reducing it to "warn if it exists"
        # would wave a genuine collision through on the second seed and every seed after it.
        taken = [(slug, existing["category"])
                 for slug in sorted(manifest.NEW_SLUGS)
                 if (existing := post_service.get_post(slug))]
        foreign = [f"{slug} (in '{cat}')" for slug, cat in taken
                   if cat != manifest.CATEGORY["slug"]]
        if foreign:
            raise SystemExit(
                "slugs marked `new` already belong to another category: " + ", ".join(foreign) +
                "\nSeeding would overwrite them. Either they are not new, or the slug is wrong.")
        if taken:
            print(f"{len(taken)} slug(s) marked `new` already exist in /"
                  f"{manifest.CATEGORY['slug']} — this track has been seeded here before")

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
                # The manifest transcribes the stored dates, so this should never fire. If it
                # does, manifest.py and the tree disagree and one of them is wrong.
                note = (f"  ⚠️ manifest says {entry['date'][:10]} but the tree says "
                        f"{existing.get('date')[:10]}")
            print(f"  {state:6}  /{manifest.CATEGORY['slug']}/{entry['slug']}"
                  f"  ({len(bodies[entry['slug']]):,} bytes){note}")
        print("\nnothing written. Re-run with --write.")
        return 0

    category = category_service.upsert_category(manifest.CATEGORY)
    print(f"category {category['slug']} -> {category['url']}  name={category['name']!r}")

    for entry in posts:
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

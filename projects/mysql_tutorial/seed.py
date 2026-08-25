#!/usr/bin/env python3
"""Write the SQL category and its posts into a content tree.

Runs the backend's own service layer rather than touching S3 directly, so the
post objects, the post index, the category archive, the category counts and the
search index are all maintained by the same code the admin API uses. Anything
else would risk the derived indexes drifting from the posts, and the static
build reads only the indexes.

    # dry run against the local tree (default)
    python projects/mysql_tutorial/seed.py

    python projects/mysql_tutorial/seed.py --env local --write --force-dates
    python projects/mysql_tutorial/seed.py --env prod  --write --force-dates

Idempotent: re-running updates the posts in place.

⚠️ THIS TRACK ALWAYS NEEDS --force-dates, AND IT IS NOT A ONE-OFF.

`upsert_post` applies the manifest date when it CREATES a post and never
overwrites the date of one that already exists. 42 of these 52 slugs are live
posts carrying their original 2018-2021 dates, and after the first seed the
other 10 have dates too. So a plain re-run moves nothing, and the archive keeps
reading in historical order instead of teaching order.

Pass it on every seed where a date in the manifest has to land, which is every
seed until the track is published and stable. Leave it off only when you have
changed a post BODY and nothing else. (This is the correction the Postgres track
established after the FastAPI track's docstring promised the opposite.)

⚠️ 42 SLUGS HERE ARE LIVE, INDEXED URLS. This script only ever creates or
updates — it never deletes — but a typo in a manifest slug creates a 53rd post
and leaves the original untouched and stale rather than failing. `--check-live`
compares the manifest against what is actually in the tree and reports both
directions.
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
        raise SystemExit(
            f"missing content file: {path}\n"
            "Use --only to seed a subset while the rest of the track is still being "
            "written — see progress_report.md."
        )
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=("local", "prod"), default="local")
    parser.add_argument("--write", action="store_true",
                        help="actually write. Without it, only report what would happen.")
    parser.add_argument("--force-dates", action="store_true",
                        help="stamp the manifest date onto posts that already exist. "
                             "THIS TRACK NEEDS IT on essentially every seed — 42 of the 52 "
                             "slugs already exist with 2018-2021 dates. See the docstring.")
    parser.add_argument("--only", default=None,
                        help="comma-separated slugs to seed, instead of the whole track. "
                             "For previewing a post while the rest are still unwritten.")
    parser.add_argument("--check-live", action="store_true",
                        help="compare the manifest against what is in the tree and exit. "
                             "Writes nothing.")
    parser.add_argument("--author", default="folauk")
    args = parser.parse_args()

    config, post_service, category_service = load_backend(args.env)
    prefix = config.db_prefix()

    # ---------------------------------------------------------------- --check-live
    if args.check_live:
        in_tree = {p["slug"] for p in
                   post_service.list_posts(category=manifest.CATEGORY["slug"])}
        in_manifest = {e["slug"] for e in manifest.POSTS}
        print(f"tree      s3://{config.DB_BUCKET}/{prefix}/")
        print(f"in /{manifest.CATEGORY['slug']}: {len(in_tree)}   in manifest: {len(in_manifest)}\n")

        orphaned = sorted(in_tree - in_manifest)
        if orphaned:
            print("IN THE TREE BUT NOT IN THE MANIFEST — these would be left stale, not "
                  "updated, and they are live URLs:")
            for slug in orphaned:
                print(f"  ! /{manifest.CATEGORY['slug']}/{slug}")
        else:
            print("nothing in the tree is missing from the manifest.")

        unseeded = sorted(in_manifest - in_tree)
        if unseeded:
            print(f"\nin the manifest but not yet in this tree ({len(unseeded)}) — expected for "
                  "the 10 new posts before the first seed:")
            for slug in unseeded:
                mark = "new" if any(e["slug"] == slug and e["new"] for e in manifest.POSTS) else "!!"
                print(f"  {mark} /{manifest.CATEGORY['slug']}/{slug}")

        # The frozen list is the real contract. Anything in it that is not in the
        # manifest is an indexed URL about to be orphaned.
        missing_frozen = sorted(manifest.FROZEN_SLUGS - in_manifest)
        if missing_frozen:
            print("\nFROZEN SLUGS MISSING FROM THE MANIFEST — these are indexed URLs:")
            for slug in missing_frozen:
                print(f"  x /{manifest.CATEGORY['slug']}/{slug}")
            return 1
        return 1 if orphaned else 0

    posts = manifest.POSTS
    if args.only:
        wanted = [slug.strip() for slug in args.only.split(",") if slug.strip()]
        known = {entry["slug"] for entry in manifest.POSTS}
        unknown = [slug for slug in wanted if slug not in known]
        if unknown:
            raise SystemExit(f"not in the manifest: {', '.join(unknown)}")
        posts = [entry for entry in manifest.POSTS if entry["slug"] in wanted]

    print(f"target  s3://{config.DB_BUCKET}/{prefix}/")
    print(f"posts   {len(posts)}" + (f" of {len(manifest.POSTS)} (--only)" if args.only else ""))
    print(f"mode    {'WRITE' if args.write else 'dry run'}"
          f"{'  +force-dates' if args.force_dates else ''}\n")

    index_before = len(post_service.list_posts())
    print(f"published posts in this tree before: {index_before}")

    # Fail early rather than half-seeding: every file must exist and no slug may
    # already belong to a different category.
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
        stale_dates = 0
        for entry in posts:
            existing = post_service.get_post(entry["slug"])
            state = "update" if existing else "create"
            note = ""
            if existing and existing.get("date") != entry["date"]:
                if args.force_dates:
                    note = f"  date {existing.get('date')[:10]} -> {entry['date'][:10]}"
                else:
                    note = f"  date STAYS {existing.get('date')[:10]} (needs --force-dates)"
                    stale_dates += 1
            print(f"  {state:6}  /{manifest.CATEGORY['slug']}/{entry['slug']}"
                  f"  ({len(bodies[entry['slug']]):,} bytes){note}")
        if stale_dates:
            print(f"\n⚠️  {stale_dates} post(s) would keep a date that disagrees with the "
                  "manifest.\n    This track re-bases 2018-2021 dates into lesson order — "
                  "add --force-dates.")
        print("\nnothing written. Re-run with --write.")
        return 0

    category = category_service.upsert_category(manifest.CATEGORY)
    print(f"category {category['slug']} -> {category['url']}")

    for entry in posts:
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
        print(f"  {record['url']:48} {record['date'][:10]}  "
              f"{record['wordCount']:>5} words  {record['readingMinutes']} min  "
              f"{len(record['toc'])} headings")

    # VERIFY THE DERIVED INDEXES ACTUALLY CONTAIN WHAT WE JUST WROTE.
    #
    # `upsert_post` -> `_reindex` rewrites the whole index per post: read it,
    # drop this slug, append, sort, write. A seed of 52 posts does that 52 times
    # in a row. On the first prod run of the VUE track two posts ended up with a
    # correct post object and NO entry in index/posts.json — and that failure is
    # invisible everywhere else, because the static build reads only the indexes.
    # No 404, no error, just two lessons silently missing from the track. And
    # `verify-build.mjs` cross-checks the indexes against EACH OTHER, which all
    # agreed, because all three were missing the same two posts.
    #
    # Re-running the seed repairs it. So the only thing needed is to notice.
    missing = []
    index_slugs = {p["slug"] for p in post_service.list_posts()}
    category_slugs = {p["slug"] for p in post_service.list_posts(category=manifest.CATEGORY["slug"])}
    for entry in posts:
        if entry["slug"] not in index_slugs:
            missing.append(f"{entry['slug']} is not in index/posts.json")
        elif entry["slug"] not in category_slugs:
            missing.append(f"{entry['slug']} is not in index/by-category/"
                           f"{manifest.CATEGORY['slug']}.json")

    if missing:
        print("\nDERIVED INDEX IS INCOMPLETE — the post objects were written but the "
              "indexes do not list them:")
        for m in missing:
            print(f"  x {m}")
        print("\nThe static build reads ONLY the indexes, so these posts would be "
              "silently absent from the site.\nRe-run this exact command — the seed is "
              "idempotent and rewriting the indexes fixes it.")
        return 1

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

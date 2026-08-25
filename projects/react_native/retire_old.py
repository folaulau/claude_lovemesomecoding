#!/usr/bin/env python3
"""Retire the five 2018 `rea-native-*` posts and the `rea-native` category.

WHY THIS EXISTS. The collection was created with a typo: slug `rea-native`,
holding five posts (`rea-native-introduction`, `-core-components`, `-flexbox`,
`-navigation`, `-internals`) published 2018-02-05 as PLACEHOLDERS. They are not
literally empty — each has WordPress `boldgrid-section` scaffolding, and between all
five the real content is two headings, one screenshot, a bare link and the word "Co".
That is why deleting them needs `--allow-nonempty`. The new track lives at
`react-native` with matching `react-native-*` slugs.

The originals cannot simply be renamed — a post's slug is its identity and its
URL, and the category is stored on the post. So the order is:

    1. seed.py          creates the new posts under the new category
    2. THIS SCRIPT      deletes the five originals and the empty old category
    3. the frontend     redirects every old URL to its replacement

Steps 1 and 3 must both be done before step 2 runs on prod, or the old URLs 404
in the window between. Run with no flags first — it reports and writes nothing.

    python projects/react_native/retire_old.py --env local
    python projects/react_native/retire_old.py --env local --write
    python projects/react_native/retire_old.py --env prod  --write

⚠️ This DELETES published posts. It refuses to run unless every replacement
already exists in the same tree, and it refuses to delete a post whose body is
not empty — if someone has written into one of the originals since 2018, that is
a decision for a human, not for this script.
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
    os.environ["env"] = "local"
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=("local", "prod"), default="local")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--allow-nonempty", action="store_true",
                        help="delete an original even if it has a body. Do not use this "
                             "without reading the body first.")
    args = parser.parse_args()

    config, post_service, category_service = load_backend(args.env)
    repo = post_service.repo()
    print(f"target  s3://{config.DB_BUCKET}/{config.db_prefix()}/")
    print(f"mode    {'WRITE' if args.write else 'dry run'}\n")

    problems = []
    plan = []

    for old_slug, new_slug in sorted(manifest.OLD_SLUG_REDIRECTS.items()):
        old = post_service.get_post(old_slug)
        new = post_service.get_post(new_slug)

        if old is None:
            print(f"  {old_slug:32} already gone")
            continue

        # The replacement must exist FIRST. Deleting before seeding leaves an
        # indexed URL pointing at nothing for however long the gap lasts.
        if new is None:
            problems.append(f"{old_slug}: replacement {new_slug} does not exist in this tree yet")
            continue

        body = (old.get("contentHtml") or old.get("body") or "").strip()
        if body and not args.allow_nonempty:
            problems.append(
                f"{old_slug}: has a {len(body)}-char body. These were supposed to be empty — "
                "read it before deleting, then pass --allow-nonempty.")
            continue

        plan.append((old_slug, new_slug, len(body)))
        print(f"  {old_slug:32} -> delete  (replacement {new_slug} is live, body {len(body)} chars)")

    old_category_posts = post_service.list_posts(category=manifest.OLD_CATEGORY_SLUG)
    remaining = [p["slug"] for p in old_category_posts
                 if p["slug"] not in {s for s, _, _ in plan}]
    if remaining:
        problems.append(
            f"/{manifest.OLD_CATEGORY_SLUG} also holds posts this script does not know about: "
            f"{', '.join(remaining)}. Add them to the manifest or move them by hand.")

    if problems:
        print("\nREFUSING TO RUN:")
        for p in problems:
            print(f"  x {p}")
        return 1

    if not plan:
        print("\nnothing to retire.")
        return 0

    if not args.write:
        print(f"\nwould delete {len(plan)} post(s) and the empty "
              f"/{manifest.OLD_CATEGORY_SLUG} category. Re-run with --write.")
        return 0

    for old_slug, new_slug, _ in plan:
        post_service.delete_post(old_slug)
        print(f"  deleted {old_slug}  (readers now redirect to /{manifest.CATEGORY['slug']}/{new_slug})")

    left = post_service.list_posts(category=manifest.OLD_CATEGORY_SLUG)
    if left:
        print(f"\n/{manifest.OLD_CATEGORY_SLUG} still holds {len(left)}; leaving the category alone.")
        return 1

    category_service.delete_category(manifest.OLD_CATEGORY_SLUG)
    print(f"\ndeleted the empty /{manifest.OLD_CATEGORY_SLUG} category")

    # ⚠️ `delete_category` removes the category from index/categories.json but leaves
    # index/by-category/<slug>.json behind as an empty array. Nothing renders it — the
    # archive is driven by categories.json — so it is litter rather than a bug, but it
    # survives `aws s3 sync --delete` into every content checkout and confuses the next
    # person who greps for the old slug.
    orphan = f"{config.db_prefix()}/index/by-category/{manifest.OLD_CATEGORY_SLUG}.json"
    if repo.get_json(orphan) is not None:
        repo.delete(orphan)
        print(f"removed the orphaned {orphan.split('/', 2)[-1]}")
    print("⚠️  the frontend redirect map and the CloudFront function must already be deployed, "
          "or these URLs now 404.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

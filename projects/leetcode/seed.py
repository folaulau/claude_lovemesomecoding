#!/usr/bin/env python3
"""Write the LeetCode posts into a content tree.

Runs the backend's own service layer rather than touching S3 directly, so the
post objects, the post index, the category archive, the category counts and the
search index are all maintained by the same code the admin API uses. Anything
else would risk the derived indexes drifting from the posts, and the static
build reads only the indexes.

    # dry run against the local tree (default)
    python projects/leetcode/seed.py

    python projects/leetcode/seed.py --env local --write
    python projects/leetcode/seed.py --env prod  --write

    # one publishing round at a time (round 1 = LeetCode 1-10)
    python projects/leetcode/seed.py --env prod --round 1 --write

    # a named batch, for posts published outside the round sequence
    python projects/leetcode/seed.py --env prod --batch interview-essentials --write

Idempotent: re-running updates the posts in place. `date` is only applied when a
post is new, so a re-run never reshuffles the archive.
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


def select(round_no: int | None, batch: str | None) -> list[dict]:
    """Round N is LeetCode numbers (N-1)*10+1 .. N*10, minus the ones the source
    repo does not have. Round 1 is seven posts, not ten.

    Posts published outside the round sequence carry a `batch` name instead, so
    they can be seeded as a group without inventing a round they do not belong to.
    """
    if round_no is not None and batch is not None:
        raise SystemExit("pass --round or --batch, not both")

    if batch is not None:
        chosen = [p for p in manifest.POSTS if p.get("batch") == batch]
        if not chosen:
            known = sorted({p["batch"] for p in manifest.POSTS if p.get("batch")})
            raise SystemExit(f"no posts in batch '{batch}'. Known batches: {known or 'none'}")
        return chosen

    if round_no is None:
        return list(manifest.POSTS)

    lo, hi = (round_no - 1) * 10 + 1, round_no * 10
    chosen = [p for p in manifest.POSTS if lo <= p["number"] <= hi]
    if not chosen:
        raise SystemExit(f"round {round_no} (LeetCode {lo}-{hi}) has no posts in the manifest")
    return chosen


def read_post_html(entry: dict) -> str:
    path = HERE / "posts" / entry["file"]
    if not path.exists():
        raise SystemExit(f"missing content file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=("local", "prod"), default="local")
    parser.add_argument("--round", type=int, default=None,
                        help="publish only this round of ten LeetCode numbers")
    parser.add_argument("--batch", default=None,
                        help="publish only this named batch (posts outside the round sequence)")
    parser.add_argument("--write", action="store_true",
                        help="actually write. Without it, only report what would happen.")
    parser.add_argument("--author", default="folauk")
    args = parser.parse_args()

    entries = select(args.round, args.batch)

    config, post_service, category_service = load_backend(args.env)
    prefix = config.db_prefix()
    print(f"target  s3://{config.DB_BUCKET}/{prefix}/")
    if args.round:
        scope = f"  (round {args.round})"
    elif args.batch:
        scope = f"  (batch {args.batch})"
    else:
        scope = "  (whole manifest)"
    print(f"posts   {len(entries)}{scope}")
    print(f"mode    {'WRITE' if args.write else 'dry run'}\n")

    index_before = len(post_service.list_posts())
    print(f"published posts in this tree before: {index_before}")

    # Fail early rather than half-seeding: every file must exist and no slug may
    # already belong to a different category.
    bodies = {}
    for entry in entries:
        bodies[entry["slug"]] = read_post_html(entry)
        existing = post_service.get_post(entry["slug"])
        if existing and existing.get("category") != manifest.CATEGORY["slug"]:
            raise SystemExit(
                f"slug collision: {entry['slug']} already exists in category "
                f"'{existing['category']}'. Post slugs are global."
            )

    if not args.write:
        for entry in entries:
            state = "update" if post_service.get_post(entry["slug"]) else "create"
            print(f"  {state:6}  /{manifest.CATEGORY['slug']}/{entry['slug']}"
                  f"  ({len(bodies[entry['slug']]):,} bytes)")
        print("\nnothing written. Re-run with --write.")
        return 0

    # The category already exists with 11 legacy posts. This only fills in the
    # name and description the migration left empty; the slug does not move.
    category = category_service.upsert_category(manifest.CATEGORY)
    print(f"category {category['slug']} -> {category['url']}")

    for entry in entries:
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
        print(f"  {record['url']:60} {record['date']}  "
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

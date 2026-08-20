#!/usr/bin/env python3
"""Move 43 posts into /java, retire 8 duplicates, drop 2 empty categories.

Runs the backend's own service layer so the post objects and every derived index
(post index, category archives, category counts, search index) are maintained by
the same code the admin API uses. Doing it with raw S3 writes would leave the
indexes drifting from the posts, and the static build reads only the indexes.

    python projects/java_merge/migrate.py                     # dry run, local
    python projects/java_merge/migrate.py --env local --write
    python projects/java_merge/migrate.py --env prod  --write

Order is load-bearing:
  1. upsert every moving post with category=java  (upsert_post's _reindex takes
     previous_category and pulls it out of the old archive)
  2. delete the 8 retired posts
  3. delete the 2 now-empty categories — delete_category REFUSES while any post
     still points at one, which is the check that proves step 1 finished

Content: a post is rewritten from posts/<slug>.html when that file exists, and
otherwise MOVED AS-IS. That lets the migration run before every post has been
trimmed without inventing content for the ones that have not.
"""

import argparse
import importlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
BACKEND = REPO / "lovemesomecoding_backend"

sys.path.insert(0, str(HERE))
import manifest  # noqa: E402
import plan      # noqa: E402


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
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", choices=("local", "prod"), default="local")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--author", default="folauk")
    args = ap.parse_args()

    config, post_service, category_service = load_backend(args.env)
    print(f"target  s3://{config.DB_BUCKET}/{config.db_prefix()}/")
    print(f"mode    {'WRITE' if args.write else 'dry run'}\n")

    before = len(post_service.list_posts())
    rewritten = moved_asis = 0
    problems = []

    # ---------------------------------------------------------------- 1. move
    for entry in manifest.POSTS:
        slug = entry["slug"]
        existing = post_service.get_post(slug)
        if not existing:
            problems.append(f"{slug}: not found in this tree")
            continue

        body_file = HERE / "posts" / f"{slug}.html"
        has_new_body = body_file.exists()
        if has_new_body:
            rewritten += 1
        elif entry["moves"]:
            moved_asis += 1

        if not args.write:
            if entry["moves"]:
                state = "MOVE+rewrite" if has_new_body else "MOVE as-is"
                print(f"  {state:14} /{existing['category']}/{slug}  ->  /java/{slug}")
            elif has_new_body:
                print(f"  {'rewrite':14} /java/{slug}")
            continue

        payload = {
            "slug": slug,
            "title": existing["title"],
            "category": manifest.TARGET_CATEGORY,
            "contentHtml": (body_file.read_text(encoding="utf-8")
                            if has_new_body else existing["contentHtml"]),
            "tags": entry["tags"],
            # A rewritten post gets a fresh excerpt from its new body: the stored
            # one summarises the 6,000-word version being replaced. Posts moving
            # as-is keep theirs.
            "excerpt": None if has_new_body else existing.get("excerpt"),
            "status": "published",
        }
        # upsert_post never overwrites an existing date, so the reading order has
        # to be stamped onto the stored object first.
        if existing.get("date") != entry["date"]:
            existing["date"] = entry["date"]
            post_service.repo().put_json(post_service.post_key(slug), existing)

        record = post_service.upsert_post(payload, author=args.author)
        print(f"  {record['url']:56} {record['date'][:10]}  {record['wordCount']:>5}w")

    # ------------------------------------------------------------- 2. retire
    print()
    for dead, survivor in sorted(plan.RETIRE_IN_FAVOUR_OF.items()):
        if not post_service.get_post(dead):
            print(f"  retire  /java/{dead}  (already gone)")
            continue
        if not post_service.get_post(survivor):
            problems.append(f"refusing to delete {dead}: survivor {survivor} does not exist")
            continue
        if not args.write:
            print(f"  RETIRE  /java/{dead}  ->  301  /java/{survivor}")
            continue
        post_service.delete_post(dead)
        print(f"  retired /java/{dead}  -> 301 -> /java/{survivor}")

    # --------------------------------------------------------- 3. categories
    #
    # _rebuild_category_counts rebuilds categories.json from the post index on
    # every upsert, so a category loses its entry the moment its last post moves
    # out — before delete_category ever runs. It then reports "category not
    # found", which is success, not failure. What it does NOT clean up in that
    # path is the now-empty index/by-category/<slug>.json object, so remove that
    # here rather than leaving litter in the bucket.
    print()
    for cat in plan.RETIRE_CATEGORIES:
        still = len(post_service.list_posts(category=cat))
        if not args.write:
            print(f"  DROP category /{cat}  ({still} post(s) still in it)")
            continue
        if still:
            problems.append(f"category {cat} still holds {still} post(s) — not dropped")
            print(f"  KEPT category /{cat}  ({still} post(s) remain)")
            continue

        ok, why = category_service.delete_category(cat)
        if ok:
            print(f"  dropped category /{cat}")
            continue
        if why == "category not found":
            # Already gone from categories.json; just sweep the orphan index.
            post_service.repo().delete(post_service.category_index_key(cat))
            print(f"  dropped category /{cat}  (counts rebuild removed it; orphan index swept)")
            continue
        problems.append(f"category {cat} not deleted: {why}")
        print(f"  KEPT category /{cat}  ({why})")

    print(f"\nrewritten {rewritten}, moved as-is {moved_asis}")
    if args.write:
        total = len(post_service.list_posts())
        counts = {c["slug"]: c["count"] for c in category_service.list_categories()}
        print(f"/java now holds {counts.get('java')} posts; tree total {total} (was {before})")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(f"  x {p}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

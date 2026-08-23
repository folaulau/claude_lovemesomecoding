#!/usr/bin/env python3
"""Rewrite the orphaned `/snowflake-table-of-content` page to point at `/snowflake`.

⚠️ Pages are NOT managed by the admin API. There is no `app/services/pages.py` and no pages
router — the `pages/` tree is migration output that the frontend reads straight off disk after
`sync-content.sh`. So this writes the S3 object itself, but runs the body through
`content.normalize` first so `contentHtml`, `toc` and `wordCount` are produced by exactly the same
pipeline as every post. Hand-writing those fields is how a page starts rendering differently from
the rest of the site.

There is no pages index to maintain — `index/` holds posts, drafts, categories and by-category
only — so updating the one object is the whole job.

Why this page is being changed at all: its entire body is an ordered list of ONE link plus an
empty <li>, written in 2022 when the collection had one post. The collection now has sixteen, so
the page is no longer merely thin, it is wrong. It is also an indexed URL, which is why it is being
rewritten rather than deleted.

Why it points at /snowflake instead of listing the sixteen: a hand-maintained index rots, and this
one already did. `/snowflake` builds the same list from the posts and cannot fall behind them.

    # dry run against the local tree (default) &mdash; prints a diff, writes nothing
    python projects/snowflake_tutorial/update_page.py

    python projects/snowflake_tutorial/update_page.py --env local --write
    python projects/snowflake_tutorial/update_page.py --env prod  --write

Idempotent: re-running against an already-updated page reports "no change" and writes nothing.
"""

import argparse
import difflib
import importlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
BACKEND = REPO_ROOT / "lovemesomecoding_backend"

SLUG = "snowflake-table-of-content"

# The replacement body. Deliberately short: this page's job is now to hand the reader off, and
# anything longer invites somebody to maintain it again.
NEW_BODY = """<p>This page used to hold a hand-written index of the Snowflake tutorials. It is no
longer maintained &mdash; the <a href="/snowflake">Snowflake category page</a> builds that index
automatically from the posts themselves, so it cannot fall behind them the way this one did.</p>

<p><strong><a href="/snowflake">Go to the Snowflake tutorials</a></strong></p>
"""


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
    from app.services import content, s3

    importlib.reload(s3)
    s3.reset_repo()
    return config, content, s3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=("local", "prod"), default="local")
    parser.add_argument("--write", action="store_true",
                        help="actually write. Without it, only show the diff.")
    args = parser.parse_args()

    config, content, s3 = load_backend(args.env)
    repo = s3.repo()
    key = f"{config.db_prefix()}/pages/{SLUG}.json"

    print(f"target  s3://{config.DB_BUCKET}/{key}")
    print(f"mode    {'WRITE' if args.write else 'dry run'}\n")

    page = repo.get_json(key)
    if not page:
        raise SystemExit(
            f"no page at {key}\n"
            "This is an INDEXED URL. If it is missing from this tree the slug is wrong — check "
            "before writing, because a wrong slug mints a new page rather than fixing the live one."
        )

    before = page.get("contentHtml", "")

    # ⚠️ Through the pipeline, not hand-written. normalize() extracts code blocks, assigns heading
    # anchors, styles tables and computes wordCount — a page that skips it renders subtly unlike
    # every post on the site.
    result = content.normalize(NEW_BODY)

    if before.strip() == result["contentHtml"].strip():
        print("no change — the page already points at /snowflake.")
        return 0

    print("--- before " + "-" * 60)
    print(before.strip() or "(empty)")
    print("--- after  " + "-" * 60)
    print(result["contentHtml"].strip())
    print("-" * 71)
    print(f"\nwords {len(before.split())} -> {result['wordCount']}, "
          f"headings {len(page.get('toc') or [])} -> {len(result['toc'])}")

    stale_links = before.count("/snowflake/")
    print(f"stale post links removed: {stale_links}")

    if not args.write:
        print("\nnothing written. Re-run with --write.")
        return 0

    page["contentHtml"] = result["contentHtml"]
    page["toc"] = result["toc"]
    page["modified"] = content.now_iso()
    # `date`, `wpId`, `url`, `title` and `status` are deliberately untouched: the URL is indexed and
    # the original publish date is a fact about the page, not about this edit.

    repo.put_json(key, page)
    print(f"\nwritten. modified -> {page['modified']}")
    print("The live site does not change until the frontend is rebuilt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

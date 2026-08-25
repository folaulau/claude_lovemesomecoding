#!/usr/bin/env python3
"""Add the /rea-native -> /react-native redirects to a content tree.

`content/redirects.json` is NOT in the frontend repo — `content/` is gitignored
and synced from the content DB, so a redirect is a CONTENT change, not a code
change. This writes the six entries the rename needs, straight into
`s3://<db-bucket>/lovemesomecoding/<env>/redirects.json`:

    /rea-native                          -> /react-native
    /rea-native/rea-native-introduction  -> /react-native/react-native-introduction
    ... one per lesson that replaces a 2018 post

Every entry is derived from `manifest.OLD_SLUG_REDIRECTS`, so the map cannot
drift from the track.

    python projects/react_native/add_redirects.py --env local
    python projects/react_native/add_redirects.py --env local --write
    python projects/react_native/add_redirects.py --env prod  --write

⚠️ ORDER MATTERS. These must be live BEFORE `retire_old.py` deletes the
originals, or the old URLs 404 in the gap. And a redirect only reaches visitors
once the frontend is rebuilt AND the CloudFront function is republished — the
map is compiled into the edge function, so a deploy that skips that step changes
nothing at the edge. `deploy.sh` does both.
"""

import argparse
import importlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent.parent / "lovemesomecoding_backend"

sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

REDIRECTS_FILE = "redirects.json"


def redirects_key(config) -> str:
    """The FULL S3 key, prefix included.

    ⚠️ `S3Repository.get_json` does NOT prepend the tree prefix — that is what
    `posts.post_key()` is for. Passing a bare "redirects.json" reads a key that
    does not exist, gets `None` back, and would then write a fresh six-entry map
    over the fifty-seven that were already there. Ask how I know.
    """
    return f"{config.db_prefix()}/{REDIRECTS_FILE}"


def load_backend(data_env: str):
    os.environ["env"] = "local"
    os.environ["data_env"] = data_env
    os.environ.setdefault("aws_profile", os.environ.get("AWS_PROFILE", "folau"))
    sys.path.insert(0, str(BACKEND))

    from app import config

    importlib.reload(config)
    from app.services import posts, s3

    importlib.reload(s3)
    importlib.reload(posts)
    s3.reset_repo()
    return config, posts


def wanted_redirects() -> dict[str, str]:
    """The rename's redirect map, derived from the manifest."""
    new_cat = manifest.CATEGORY["slug"]
    old_cat = manifest.OLD_CATEGORY_SLUG

    entries = {f"/{old_cat}": f"/{new_cat}"}
    for old_slug, new_slug in manifest.OLD_SLUG_REDIRECTS.items():
        entries[f"/{old_cat}/{old_slug}"] = f"/{new_cat}/{new_slug}"
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=("local", "prod"), default="local")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    config, post_service = load_backend(args.env)
    repo = post_service.repo()

    key = redirects_key(config)
    print(f"target  s3://{config.DB_BUCKET}/{key}")
    print(f"mode    {'WRITE' if args.write else 'dry run'}\n")

    current = repo.get_json(key)
    if current is None:
        # A tree with no redirects at all is possible but surprising. Say so
        # rather than quietly treating it as an empty map and overwriting.
        print(f"no {REDIRECTS_FILE} in this tree — a new one will be created")
        current = {}
    elif not isinstance(current, dict):
        raise SystemExit(f"{key} is not a JSON object")
    print(f"{len(current)} redirect(s) already recorded")

    entries = wanted_redirects()
    changed = {}
    for source, target in sorted(entries.items()):
        existing = current.get(source)
        if existing == target:
            print(f"  {source:44} -> {target}   (already set)")
            continue
        if existing:
            # Never silently retarget somebody else's deliberate redirect.
            print(f"  {source:44} -> {target}   ⚠️ REPLACES {existing}")
        else:
            print(f"  {source:44} -> {target}")
        changed[source] = target

    if not changed:
        print("\nnothing to change.")
        return 0

    # A redirect whose destination does not exist is worse than no redirect —
    # it turns one 404 into a redirect to a 404, which is harder to notice.
    missing = []
    for target in changed.values():
        parts = [p for p in target.split("/") if p]
        if len(parts) == 2 and post_service.get_post(parts[1]) is None:
            missing.append(target)
    if missing:
        print("\nREFUSING TO RUN — these destinations do not exist in this tree yet:")
        for m in sorted(set(missing)):
            print(f"  x {m}")
        print("Seed the track first (seed.py --write), then re-run.")
        return 1

    if not args.write:
        print(f"\nwould add or change {len(changed)} entry(ies). Re-run with --write.")
        return 0

    current.update(changed)
    repo.put_json(key, current)
    print(f"\nwrote {len(current)} redirect(s)")
    print("⚠️  not live until the frontend is rebuilt AND the CloudFront function republished.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

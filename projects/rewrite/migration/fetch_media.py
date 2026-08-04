#!/usr/bin/env python3
"""
Phase 1c — download the images the migrated content actually needs.

Post bodies reference 1131 distinct upload URLs, but most of those are WordPress'
auto-generated resize variants (foo-1024x463.jpeg). transform.py collapses every
variant back to its original, so only the originals need migrating. The media
library also holds orphans never referenced by any post; those are fetched too so
the admin media picker isn't missing anything.

Downloads to ./out/media/<uploads-relative-path>, mirroring the key layout used
under s3://<storage-bucket>/lovemesomecoding/<env>/media/.

    python3 fetch_media.py
    python3 fetch_media.py --skip-orphans
"""

import argparse
import json
import os
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "out")
MEDIA_DIR = os.path.join(OUT, "media")
BASE = "https://lovemesomecoding.com/wp-content/uploads/"

TIMEOUT = 90
RETRIES = 3

session = requests.Session()
session.headers["User-Agent"] = "lovemesomecoding-migration/1.0"


def download(path, dest):
    for attempt in range(RETRIES):
        try:
            r = session.get(BASE + path, timeout=TIMEOUT, stream=True)
            r.raise_for_status()
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            tmp = dest + ".part"
            with open(tmp, "wb") as fh:
                for chunk in r.iter_content(65536):
                    fh.write(chunk)
            os.replace(tmp, dest)
            return os.path.getsize(dest), None
        except Exception as e:  # noqa: BLE001
            if attempt == RETRIES - 1:
                return 0, str(e)
            time.sleep(2 ** attempt)
    return 0, "unreachable"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-orphans", action="store_true",
                    help="only fetch images actually referenced by content")
    args = ap.parse_args()

    needed = set(json.load(open(os.path.join(OUT, "reports", "media_needed.json"))))
    referenced = len(needed)

    if not args.skip_orphans:
        for m in json.load(open(os.path.join(RAW, "media.json"), encoding="utf-8")):
            url = m.get("source_url", "")
            if "/wp-content/uploads/" in url:
                needed.add(url.split("/wp-content/uploads/", 1)[1])

    targets = sorted(needed)
    print(f"referenced by content: {referenced}")
    print(f"total to fetch (incl. library orphans): {len(targets)}\n")

    ok = skipped = 0
    total_bytes = 0
    failures = []

    for i, path in enumerate(targets, 1):
        dest = os.path.join(MEDIA_DIR, path)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skipped += 1
            total_bytes += os.path.getsize(dest)
            continue
        size, err = download(path, dest)
        if err:
            failures.append({"path": path, "error": err})
            print(f"  [{i}/{len(targets)}] FAIL {path}: {err}", file=sys.stderr)
        else:
            ok += 1
            total_bytes += size
            if i % 25 == 0 or i == len(targets):
                print(f"  [{i}/{len(targets)}] {total_bytes / 1024 / 1024:.1f} MB")

    report = {
        "referenced": referenced,
        "attempted": len(targets),
        "downloaded": ok,
        "already_present": skipped,
        "failed": len(failures),
        "total_bytes": total_bytes,
        "failures": failures,
    }
    os.makedirs(os.path.join(OUT, "reports"), exist_ok=True)
    with open(os.path.join(OUT, "reports", "media_fetch.json"), "w") as fh:
        json.dump(report, fh, indent=1)

    print(f"\ndownloaded {ok}, cached {skipped}, failed {len(failures)}")
    print(f"total {total_bytes / 1024 / 1024:.1f} MB -> {MEDIA_DIR}")
    if failures:
        print("see out/reports/media_fetch.json for failures", file=sys.stderr)


if __name__ == "__main__":
    main()

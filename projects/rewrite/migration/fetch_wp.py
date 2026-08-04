#!/usr/bin/env python3
"""
Phase 1a — pull everything out of the live WordPress site via its public REST API.

Writes untransformed JSON to ./raw/ so the rest of the migration never has to hit
DreamHost again. Safe to re-run: each endpoint is written atomically and skipped if
already complete unless --force is passed.

    python3 fetch_wp.py            # fetch anything missing
    python3 fetch_wp.py --force    # re-fetch everything
"""

import argparse
import json
import os
import sys
import time

import requests

SITE = "https://lovemesomecoding.com"
API = f"{SITE}/wp-json/wp/v2"
RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")

PER_PAGE = 100
TIMEOUT = 60
RETRIES = 4
PAUSE = 0.3  # be polite to a $25/mo shared host

# endpoint -> whether we need the heavy rendered content
ENDPOINTS = {
    "posts": None,       # None = all fields (we need content.rendered)
    "pages": None,
    "categories": None,
    "tags": None,
    "media": "id,slug,source_url,mime_type,alt_text,media_details,date,post",
    "users": "id,name,slug,description",
}

session = requests.Session()
session.headers["User-Agent"] = "lovemesomecoding-migration/1.0"


def get(url, params):
    """GET with retries. Returns (json, headers)."""
    last = None
    for attempt in range(RETRIES):
        try:
            r = session.get(url, params=params, timeout=TIMEOUT)
            if r.status_code == 400 and "rest_post_invalid_page_number" in r.text:
                return [], r.headers  # walked past the last page
            r.raise_for_status()
            return r.json(), r.headers
        except Exception as e:  # noqa: BLE001 - network layer, retry anything
            last = e
            wait = 2 ** attempt
            print(f"    retry {attempt + 1}/{RETRIES} in {wait}s ({e})", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"giving up on {url} {params}: {last}")


def fetch_all(endpoint, fields):
    """Page through an endpoint until exhausted."""
    params = {"per_page": PER_PAGE, "page": 1}
    if fields:
        params["_fields"] = fields

    items, page, total = [], 1, None
    while True:
        params["page"] = page
        batch, headers = get(f"{API}/{endpoint}", params)
        if total is None:
            total = int(headers.get("X-WP-Total", 0))
            print(f"  {endpoint}: {total} items reported")
        if not batch:
            break
        items.extend(batch)
        print(f"  {endpoint}: page {page} -> {len(items)}/{total}")
        if len(items) >= total:
            break
        page += 1
        time.sleep(PAUSE)

    if total and len(items) != total:
        print(
            f"  !! {endpoint}: expected {total}, got {len(items)}",
            file=sys.stderr,
        )
    return items, total


def write_atomic(path, payload):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-fetch even if raw file exists")
    args = ap.parse_args()

    os.makedirs(RAW_DIR, exist_ok=True)
    summary = {}

    for endpoint, fields in ENDPOINTS.items():
        out = os.path.join(RAW_DIR, f"{endpoint}.json")
        if os.path.exists(out) and not args.force:
            existing = json.load(open(out, encoding="utf-8"))
            print(f"{endpoint}: already have {len(existing)} items, skipping (--force to redo)")
            summary[endpoint] = {"count": len(existing), "skipped": True}
            continue

        print(f"{endpoint}: fetching...")
        items, total = fetch_all(endpoint, fields)
        write_atomic(out, items)
        summary[endpoint] = {"count": len(items), "reported_total": total, "skipped": False}
        print(f"{endpoint}: wrote {len(items)} -> {out}")

    write_atomic(os.path.join(RAW_DIR, "_fetch_summary.json"), summary)

    print("\n--- summary ---")
    for name, info in summary.items():
        note = " (cached)" if info.get("skipped") else ""
        print(f"  {name:12s} {info['count']:5d}{note}")


if __name__ == "__main__":
    main()

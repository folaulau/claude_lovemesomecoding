#!/usr/bin/env python3
"""
The definitive migration check: replay every URL WordPress serves today against
the new deployment and confirm each one returns 200 or a 301 to something real.

    python3 verify_live_urls.py --base https://d32j0xfm775hkk.cloudfront.net
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, 'migration', 'out', 'reports', 'url_manifest.json')

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=32, pool_maxsize=32)
session.mount('https://', adapter)


def check(base, entry):
    path = entry['old'].split('lovemesomecoding.com', 1)[1] or '/'
    url = base + path
    try:
        r = session.get(url, timeout=30, allow_redirects=False)
        if r.status_code == 200:
            return ('ok', path, r.status_code, '')
        if r.status_code in (301, 302):
            target = r.headers.get('location', '')
            f = session.get(target if target.startswith('http') else base + target,
                            timeout=30, allow_redirects=True)
            kind = 'redirect' if f.status_code == 200 else 'broken-redirect'
            return (kind, path, r.status_code, target)
        return ('fail', path, r.status_code, '')
    except Exception as e:  # noqa: BLE001
        return ('error', path, 0, str(e)[:80])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True, help='deployment base URL')
    ap.add_argument('--workers', type=int, default=16)
    args = ap.parse_args()
    base = args.base.rstrip('/')

    manifest = json.load(open(MANIFEST))
    print(f'replaying {len(manifest)} WordPress URLs against {base}\n')

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda e: check(base, e), manifest))

    buckets = {}
    for kind, path, code, extra in results:
        buckets.setdefault(kind, []).append((path, code, extra))

    for kind in ('ok', 'redirect', 'broken-redirect', 'fail', 'error'):
        rows = buckets.get(kind, [])
        if not rows:
            continue
        print(f'{kind:16s} {len(rows)}')
        if kind not in ('ok', 'redirect'):
            for path, code, extra in rows[:15]:
                print(f'    {code}  {path}  {extra}')

    bad = len(buckets.get('fail', [])) + len(buckets.get('error', [])) + len(buckets.get('broken-redirect', []))
    healthy = len(buckets.get('ok', [])) + len(buckets.get('redirect', []))
    print(f'\n{healthy}/{len(manifest)} URLs healthy')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()

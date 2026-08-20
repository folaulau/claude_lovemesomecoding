#!/usr/bin/env python3
"""Every URL this merge retires must redirect somewhere that resolves.

This exists because the frontend's own guard does not cover category moves.
`verify-build.mjs` checks post URLs against the CURRENT content index: once a
post moves to `java`, the index stops mentioning the old URL and the build has
no idea it ever existed. 45 URLs change here and nothing else would notice.

Run against the built `out/` before deploying:

    python projects/java_merge/check_redirects.py --out lovemesomecoding_frontend/out

or against the live site after deploying:

    python projects/java_merge/check_redirects.py --live
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))
import plan  # noqa: E402

# The category each moving slug lives in today, needed to build the old URL.
OLD_CATEGORY = {}
for s in plan.MOVE_TO_JAVA:
    OLD_CATEGORY[s] = "java-advanced" if s.startswith("java-advanced-") else "java-8"


def served(out: Path, url: str) -> bool:
    clean = url.lstrip("/")
    if not clean:
        return (out / "index.html").exists()
    return ((out / f"{clean}.html").exists()
            or (out / clean / "index.html").exists()
            or (out / clean).exists())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="path to the built out/ directory")
    ap.add_argument("--live", action="store_true", help="check https://lovemesomecoding.com")
    args = ap.parse_args()

    redirects_expected = plan.build_redirects(OLD_CATEGORY)
    print(f"{len(redirects_expected)} URLs are retired by this merge\n")

    failures = []

    if args.live:
        for old, new in sorted(redirects_expected.items()):
            url = "https://lovemesomecoding.com" + old
            req = urllib.request.Request(url, method="GET")
            try:
                with urllib.request.urlopen(req) as r:
                    final = r.url.replace("https://lovemesomecoding.com", "")
                    code = r.status
            except Exception as e:  # noqa: BLE001
                failures.append(f"{old}: {e}")
                continue
            if final.rstrip("/") != new.rstrip("/"):
                failures.append(f"{old} -> landed on {final}, expected {new} (status {code})")
            else:
                print(f"  ok  {old:52} -> {final}")
    else:
        if not args.out:
            print("pass --out <dir> or --live")
            return 1
        out = Path(args.out)
        redirects_file = out / "redirects.json"
        if not redirects_file.exists():
            print(f"no redirects.json in {out} — run the build first")
            return 1
        shipped = json.loads(redirects_file.read_text())

        for old, new in sorted(redirects_expected.items()):
            if served(out, old):
                # Still a real page: the move did not happen, or a stale file
                # survived. Either way the redirect will never fire.
                failures.append(f"{old} still resolves as a page — it should redirect to {new}")
                continue
            if shipped.get(old) != new:
                failures.append(f"{old} has no redirect (expected -> {new}); "
                                f"got {shipped.get(old)!r}")
                continue
            if not served(out, new):
                failures.append(f"{old} -> {new}, but {new} does not exist")
                continue
            print(f"  ok  {old:52} -> {new}")

    print()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(f"  x {f}")
        return 1
    print("every retired URL redirects to a page that exists")
    return 0


if __name__ == "__main__":
    sys.exit(main())

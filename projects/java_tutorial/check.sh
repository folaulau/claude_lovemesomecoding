#!/usr/bin/env bash
# Run every content gate for this track. Add --links for the S3-backed link check
# (needs AWS_PROFILE=folau); the other two are offline.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fail=0
python3 "$ROOT/projects/java_tutorial/check_content.py"  || fail=1
echo
python3 "$ROOT/projects/java_tutorial/check_snippets.py" || fail=1
if [[ "${1:-}" == "--links" ]]; then
  echo
  python3 "$ROOT/projects/java_tutorial/check_links.py"  || fail=1
fi
exit $fail

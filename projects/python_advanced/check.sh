#!/usr/bin/env bash
# Run every gate for this track. Add --links for the S3-backed link check
# (needs AWS_PROFILE=folau); everything else is offline.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HERE="$ROOT/projects/python_advanced"
APP="$ROOT/lovemesomecoding_demo_project/bank/bank-python-console"
fail=0

python3 "$HERE/check_content.py"     || fail=1
echo
python3 "$HERE/check_snippets.py"    || fail=1
echo
python3 "$HERE/check_provenance.py"  || fail=1
echo

# Blocks quoted from the demo app are NOT run by check_snippets.py — a method
# lifted out of its module refers to collaborators it had there. Running the
# app's own suite is what proves those files import and behave.
echo "bank-python-console suite (backs every quoted snippet)"
if "$APP/test.sh" >/tmp/bank-python-suite.log 2>&1; then
  tail -1 /tmp/bank-python-suite.log
else
  echo "  x demo app suite FAILED — see /tmp/bank-python-suite.log"
  fail=1
fi

if [[ "${1:-}" == "--links" ]]; then
  echo
  python3 "$HERE/check_links.py"     || fail=1
fi
exit $fail

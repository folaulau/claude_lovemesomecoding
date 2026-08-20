#!/usr/bin/env bash
# Run every content gate for this track. Add --links for the S3-backed link check
# (needs AWS_PROFILE=folau); the other two are offline.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fail=0
python3 "$ROOT/projects/java_tutorial/check_content.py"  || fail=1
echo
python3 "$ROOT/projects/java_tutorial/check_snippets.py" || fail=1
echo
python3 "$ROOT/projects/java_tutorial/check_provenance.py" || fail=1
echo
# Demo-app quotes are not compiled by check_snippets.py — they reference the
# fields and collaborators of the class they came from. Running the app's own
# suite is what proves those files compile and behave.
echo "bank-java-console suite (backs every quoted snippet)"
"$ROOT/lovemesomecoding_demo_project/bank/bank-java-console/test.sh" >/tmp/bank-suite.log 2>&1 \
  && tail -1 /tmp/bank-suite.log \
  || { echo "  x demo app suite FAILED — see /tmp/bank-suite.log"; fail=1; }
if [[ "${1:-}" == "--links" ]]; then
  echo
  python3 "$ROOT/projects/java_tutorial/check_links.py"  || fail=1
fi
exit $fail

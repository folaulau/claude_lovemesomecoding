#!/usr/bin/env bash
# Every gate for the merged /java track.
set -uo pipefail
R="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
f=0
python3 "$R/check_content.py"   || f=1
echo
python3 "$R/check_snippets.py" 2>&1 | tail -4 || f=1
echo
python3 "$R/check_flow.py"      || f=1
echo
python3 "$R/check_provenance.py" || f=1
exit $f

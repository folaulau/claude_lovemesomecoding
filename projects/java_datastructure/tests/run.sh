#!/usr/bin/env bash
# Compile every source in src/dsa and run all the assertions.
#
# Needs no build tool, no dependencies and no AWS credentials — which is the point: a reader
# can run the published code exactly this way.
#
#   projects/java_datastructure/tests/run.sh
#
# The track is written against Java 25, so this REQUIRES Java 25 or newer and fails loudly
# otherwise. It deliberately does not honour an existing JAVA_HOME: on this machine that
# variable points at Corretto 21, and an earlier version of this script inherited it and
# quietly ran the whole suite on the wrong JDK — green, and not testing what it claimed to.
# A silent fallback to an older toolchain is the exact failure mode this track keeps warning
# about, so it is an error here rather than a shrug.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../src/dsa"
OUT="$HERE/out"
REQUIRED=25

if [[ -n "${DSA_JAVA_HOME:-}" ]]; then
  JDK="$DSA_JAVA_HOME"                       # explicit override, for CI or another machine
elif command -v /usr/libexec/java_home >/dev/null 2>&1; then
  JDK="$(/usr/libexec/java_home -v "$REQUIRED" 2>/dev/null || true)"
else
  JDK="${JAVA_HOME:-}"
fi

if [[ -z "$JDK" || ! -x "$JDK/bin/javac" ]]; then
  echo "error: no JDK $REQUIRED found." >&2
  echo "       Install one, or point DSA_JAVA_HOME at it." >&2
  exit 1
fi

FEATURE="$("$JDK/bin/java" -XshowSettings:properties -version 2>&1 \
  | awk -F'= *' '/java.specification.version/ {print $2; exit}')"

if (( FEATURE < REQUIRED )); then
  echo "error: this track is written against Java $REQUIRED, but $JDK is Java $FEATURE." >&2
  echo "       Refusing to run — a green suite on the wrong JDK proves nothing." >&2
  exit 1
fi

echo "using $("$JDK/bin/java" -version 2>&1 | head -1)"

rm -rf "$OUT"
# -Werror on purpose: a warning in code that gets published is a defect.
"$JDK/bin/javac" -Xlint:all -Werror -d "$OUT" "$SRC"/*.java
"$JDK/bin/java" -cp "$OUT" dsa.RunAll

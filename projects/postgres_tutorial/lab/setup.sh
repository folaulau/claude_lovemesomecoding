#!/usr/bin/env bash
# Build `stayhub_lab` — StayHub's real schema at a scale where query plans mean something.
#
# StayHub's own database has 12 properties and 3 bookings. Every index, EXPLAIN, VACUUM and
# locking example in the /postgre track runs against THIS database instead, so the plans quoted
# in the posts are plans Postgres actually chose rather than plans it would choose if the table
# were big. The stayhub database is never touched.
#
#   projects/postgres_tutorial/lab/setup.sh          # build (drops and recreates stayhub_lab)
#   projects/postgres_tutorial/lab/setup.sh --drop   # tear it down
#
# Takes about a minute. Needs the stayhub-postgres container up.
set -euo pipefail

CONTAINER=stayhub-postgres
DB=stayhub_lab
USER=stayhub
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
    echo "error: container '$CONTAINER' is not running." >&2
    echo "       cd lovemesomecoding_demo_project/stayhub && docker compose up -d postgres" >&2
    exit 1
fi

psql_root() { docker exec -i "$CONTAINER" psql -U "$USER" -d postgres -v ON_ERROR_STOP=1 "$@"; }
psql_lab()  { docker exec -i "$CONTAINER" psql -U "$USER" -d "$DB"   -v ON_ERROR_STOP=1 "$@"; }

# Refuse to point at the demo app's database, however the variables get edited later.
if [ "$DB" = "stayhub" ]; then echo "error: refusing to rebuild the demo app database" >&2; exit 1; fi

echo "==> dropping $DB if it exists"
psql_root -q -c "DROP DATABASE IF EXISTS $DB WITH (FORCE);"

if [ "${1:-}" = "--drop" ]; then echo "dropped. nothing rebuilt."; exit 0; fi

echo "==> creating $DB"
psql_root -q -c "CREATE DATABASE $DB OWNER $USER;"

echo "==> loading StayHub's schema (pg_dump --schema-only of the live stayhub database)"
psql_lab -q < "$HERE/stayhub-schema.sql"

echo "==> generating rows (this is the slow part)"
time psql_lab -q < "$HERE/seed.sql"

echo
echo "==> what got built"
psql_lab -c "
SELECT relname AS table,
       to_char(n_live_tup, 'FM999,999,999') AS rows,
       pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
WHERE n_live_tup > 0
ORDER BY n_live_tup DESC;"

echo "connect with:  docker exec -it $CONTAINER psql -U $USER -d $DB"

#!/usr/bin/env python3
"""Execute every SQL sample in the track against a real Postgres and fail on the ones that break.

`check_content.py` proves a post's HTML survives the normaliser. It says nothing about whether the
SQL in it is valid — a post can round-trip perfectly while quoting a query with a typo in a column
name, and SQL is the language where that is hardest to spot by eye and easiest to publish.

⚠️ THIS IS THE CHECK THAT JUSTIFIES THE TRACK. The two posts being replaced tell you to
`docker pull postgres:12` and download an installer; nothing in them was ever run. Every `sql`
block here is executed against `stayhub_lab` (lab/setup.sh — StayHub's real schema, 400,000
bookings) before it can ship.

Blocks are replayed IN ORDER, cumulatively: block 5 is checked with blocks 1-4 already applied,
inside a transaction that is then ROLLED BACK. That is how a reader meets them — a post that
creates a role in one block and grants to it in the next is correct, and checking each block in
isolation would report the grant as a broken reference to a role that does not exist.

Nothing is mutated: the whole replay happens in one transaction and ends in ROLLBACK. A block that
runs is not necessarily a block that is *correct*, but a block that does not run is definitely
wrong, and that is the class of error this catches.

Four kinds of block are handled specially, and the classification is automatic so a post cannot
quietly opt out of being checked:

  expect-error  the block contains an `ERROR:` line, so it is TEACHING a failure. The check
                inverts: the block must fail, and failing to fail is the finding.
  no-transaction  either a statement Postgres refuses to run inside a transaction (CREATE INDEX
                CONCURRENTLY, VACUUM) or a block carrying its OWN BEGIN/COMMIT — whose commit would
                otherwise end this script's wrapper and make the replayed context permanent. Both
                run against a scratch database that is dropped afterwards.
  cluster-level  CREATE DATABASE, ALTER SYSTEM and friends change the whole server and no
                transaction can undo them. NEVER executed — see the comment on CLUSTER_LEVEL for
                what happened the one time this script thought it could clean up after them.
  fragment      the block does not begin with a statement keyword, so it is a column definition
                or a clause quoted to show syntax. Reported and counted, not executed — watch the
                count, because "make it a fragment" is the easy way to dodge this check.
  multi-session  a `-- session A` / `-- session B` marker means the block is half of a locking
                demonstration and has no meaning run alone. Reported, not executed.
  psql-meta     the block is psql meta-commands (\\d, \\timing). Executed, since psql understands
                them, but a failure there is a typo rather than bad SQL.

Output whose query mentions now(), random(), a uuid, xmin or ctid is reported as `output-varies`
and not compared — those results are different on every run by construction, and a check that
always fails is a check everybody learns to ignore.

QUOTED OUTPUT IS ALSO CHECKED. A `plaintext` block that follows a `sql` block and looks like a
psql result table is re-derived: the query is run, and every data row quoted in the post must
appear in the real output. This exists because it caught real fabrication on its first run — an
aggregation post quoted average-nights of 3.50/3.50/3.51/3.50 where the database returns
3.49/3.52/3.52/3.50. The SQL was correct and ran cleanly; the numbers under it were remembered
rather than copied, and nothing else in the pipeline would ever have noticed.

    projects/postgres_tutorial/check_sql.py
    projects/postgres_tutorial/check_sql.py --post postgres-joins
    projects/postgres_tutorial/check_sql.py --verbose
"""

import argparse
import html
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

CONTAINER = "stayhub-postgres"
DB = manifest.LAB_DB
SCRATCH_DB = "stayhub_lab_scratch"
USER = "stayhub"

BLOCK = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-[\w-]+">(.*?)</code></pre>', re.S)

# psql draws a result as  header / ----+---- / rows. The separator line is the reliable marker.
RESULT_SEPARATOR = re.compile(r"^[-+]{3,}$")

# psql's row-count footer, and ONLY that. An earlier version dropped every line starting with "("
# — which is also how a ctid is written, so the MVCC example compared against nothing at all.
ROW_COUNT_FOOTER = re.compile(r"^\(\d+ rows?\)$")

# Output that cannot be reproduced, because the query asks for something that moves. Comparing it
# would fail on every run and train everyone to ignore the check.
# ⚠️ Two alternations, not one. A trailing \b cannot match after "now()" — the next character is
# ":" or ",", and \b needs a word character on one side. The first version had it and matched
# nothing, so every timestamp example was compared and every one of them failed.
NON_REPRODUCIBLE = re.compile(
    r"(?:\b(?:now|clock_timestamp|random|gen_random_uuid|uuid_generate_v4|pg_backend_pid"
    r"|statement_timestamp|timeofday)\s*\()"
    r"|(?:\b(?:current_timestamp|current_date|current_time|xmin|xmax|ctid"
    r"|pg_stat_activity|pg_sleep)\b)", re.I)

# ⚠️ Statements that change the CLUSTER rather than a database, and that nothing can undo.
#
# These are NEVER executed. An earlier version of this script ran them against a scratch database
# and then dropped every database name it had seen in a CREATE DATABASE, on the theory that it was
# cleaning up after itself. A post's `CREATE DATABASE stayhub;` — an illustration of the syntax —
# therefore caused the checker to DROP the demo application's own database. It was restored from
# lab/stayhub-schema.sql plus the app's seed script, and this list is the fix: a post cannot ask
# this script to touch the cluster, whatever it contains.
# CREATE ROLE is deliberately NOT here. Roles are cluster-wide objects, but role DDL *is*
# transactional — `BEGIN; CREATE ROLE x; ROLLBACK;` leaves nothing behind — so the roles post gets
# its main subject checked rather than waved through.
CLUSTER_LEVEL = re.compile(
    r"^\s*(CREATE\s+DATABASE|DROP\s+DATABASE|ALTER\s+SYSTEM|ALTER\s+DATABASE"
    r"|CREATE\s+TABLESPACE|DROP\s+TABLESPACE)",
    re.I | re.M)

# Statements that Postgres refuses to run inside a transaction block, but that are confined to one
# database and so are safe on a scratch copy.
NO_TRANSACTION = re.compile(
    r"^\s*(CREATE\s+INDEX\s+CONCURRENTLY|DROP\s+INDEX\s+CONCURRENTLY"
    r"|REINDEX\s+\w+\s+CONCURRENTLY|VACUUM)",
    re.I | re.M)

# Every keyword a complete statement can start with. A block that begins with anything else is a
# FRAGMENT — a column definition, a constraint clause, a WHERE line quoted on its own — which is a
# legitimate way to show syntax and is not something that can be executed.
STATEMENT_START = re.compile(
    r"^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|WITH|BEGIN|COMMIT|ROLLBACK|SAVEPOINT"
    r"|RELEASE|SET|RESET|SHOW|GRANT|REVOKE|EXPLAIN|ANALYZE|VACUUM|COMMENT|TRUNCATE|COPY|DO|CALL"
    r"|PREPARE|EXECUTE|DEALLOCATE|REINDEX|CLUSTER|REFRESH|LOCK|LISTEN|NOTIFY|VALUES|TABLE|DECLARE"
    r"|FETCH|CLOSE|START|END|ABORT|CHECKPOINT)\b",
    re.I)

# ⚠️ Transaction control INSIDE a block breaks the wrapper this script relies on.
#
# Every block is normally run as `BEGIN; <context> <block> ROLLBACK;`. A block containing its own
# COMMIT ends the WRAPPER's transaction, and everything the context had inserted becomes permanent
# — the trailing ROLLBACK then has nothing left to undo. A post demonstrating `BEGIN; UPDATE ...;
# COMMIT;` therefore wrote four amenities and fourteen booking status changes into the lab
# database, which then failed on the next run with a duplicate key.
#
# These blocks run against the scratch database instead, where a commit is thrown away with the
# whole database afterwards.
TRANSACTION_CONTROL = re.compile(
    r"^\s*(BEGIN|COMMIT|END|ROLLBACK|START\s+TRANSACTION|SAVEPOINT|RELEASE\s+SAVEPOINT)\b",
    re.I | re.M)

# Blocks that need something this container does not have, declared here rather than silently
# passing. Each entry is a marker and the reason it cannot run — keep the list short and read it
# when it grows, because "add a skip" is the easy way to make a failing check green.
UNAVAILABLE = {
    "pg_stat_statements":
        "needs shared_preload_libraries = 'pg_stat_statements' and a server restart. This "
        "container is shared with the demo application, so its configuration is left alone.",
}

# A block that rolls back to a savepoint is DEMONSTRATING recovery from an error. Run under
# ON_ERROR_STOP=1, psql aborts at the very error the savepoint exists to absorb, so the example
# gets reported as broken while being exactly right. These run with the flag off and are judged on
# whether the block as a whole completes.
RECOVERS = re.compile(r"^\s*ROLLBACK\s+TO\s+(SAVEPOINT\s+)?\w+", re.I | re.M)

MULTI_SESSION = re.compile(r"^--\s*session\s+[AB]\b", re.I | re.M)
PSQL_META = re.compile(r"^\s*\\", re.M)
TEACHES_AN_ERROR = re.compile(r"^--\s*ERROR:", re.I | re.M)


def container_running() -> bool:
    out = subprocess.run(["docker", "ps", "--format", "{{.Names}}"],
                         capture_output=True, text=True).stdout
    return CONTAINER in out.split()


def database_exists(name: str) -> bool:
    r = psql("postgres", f"SELECT 1 FROM pg_database WHERE datname = '{name}'")
    return r.returncode == 0 and "1" in r.stdout


# ⚠️ A per-statement ceiling, and a hard one on the process behind it.
#
# Cumulative replay means an expensive block is re-run once for every block after it, so one slow
# query does not cost its own runtime — it costs that times the number of blocks that follow. A
# `NOT IN (SELECT ...)` over 400,000 rows takes over 25 seconds here and hung the whole check.
# A block that is too slow to run repeatedly is a block a reader should not be handed either.
STATEMENT_TIMEOUT = "20s"
PROCESS_TIMEOUT = 240


def psql(db: str, sql: str, on_error_stop: bool = True):
    cmd = ["docker", "exec", "-i", CONTAINER, "psql", "-U", USER, "-d", db, "-q"]
    if on_error_stop:
        cmd += ["-v", "ON_ERROR_STOP=1"]
    try:
        return subprocess.run(cmd, input=f"SET statement_timeout = '{STATEMENT_TIMEOUT}';\n{sql}",
                              capture_output=True, text=True, timeout=PROCESS_TIMEOUT)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            cmd, 1, "", f"psql: killed after {PROCESS_TIMEOUT}s — the block never finished")


def _as_context(index: int, source: str, kind: str) -> str:
    """Replay an earlier block so a later one has the state it expects.

    An earlier block that is SUPPOSED to fail would abort the transaction and take every following
    block with it, so it is wrapped in a savepoint and rolled back to — the error happens, the
    transaction survives, and the state it would have left behind is correctly absent.
    """
    if kind == "expect-error":
        return (f"\\set ON_ERROR_STOP 0\n"
                f"SAVEPOINT blk{index};\n{source}\nROLLBACK TO SAVEPOINT blk{index};\n"
                f"\\set ON_ERROR_STOP 1\n")
    return source + "\n"


def run_block(blocks: list[tuple[int, str, str]], target: int):
    """Check block `target` with every earlier block already applied.

    Returns (ok, detail). `ok` means the block behaved as its kind says it should.
    """
    _index, source, kind = blocks[target]

    if kind in ("recovers", "no-transaction"):
        # Three sorts of block land here: statements Postgres refuses to run inside a transaction
        # (CREATE INDEX CONCURRENTLY, VACUUM), blocks carrying their own BEGIN/COMMIT whose commit
        # would otherwise end the wrapper and make the replayed context permanent, and blocks that
        # recover from their own error with a savepoint.
        #
        # None can be rolled back, so each gets a FRESH copy of the database — and the context is
        # applied to it first. Without that, a post that adds a column in one block and indexes it
        # CONCURRENTLY in the next reports "column does not exist" for a sequence that is correct.
        reset_scratch()
        context = "".join(
            _as_context(i, src, k) for i, src, k in blocks[:target]
            if k not in ("multi-session", "cluster-level", "fragment", "unavailable"))
        if context:
            psql(SCRATCH_DB, context, on_error_stop=False)
        result = psql(SCRATCH_DB, source, on_error_stop=(kind != "recovers"))
    else:
        context = "".join(
            _as_context(i, src, k)
            for i, src, k in blocks[:target]
            if k not in ("multi-session", "no-transaction", "cluster-level", "fragment",
                         "unavailable", "recovers"))
        # ROLLBACK, not COMMIT: a CREATE TABLE in a lesson must be checked, not applied.
        result = psql(DB, f"BEGIN;\n{context}{source}\nROLLBACK;")

    failed = result.returncode != 0
    # ⚠️ The LAST error, not the first. Blocks that are supposed to fail have already written
    # their error to stderr by now, and reporting that one blames a line that is working.
    errors = [line for line in (result.stderr or result.stdout).splitlines()
              if line.startswith("ERROR:") or line.startswith("psql:")]
    detail = errors[-1] if errors else (result.stderr or result.stdout).strip()

    if kind == "expect-error":
        # The block is teaching a failure. Running clean means the example no longer demonstrates
        # what the prose says it does.
        return failed, ("ran without error, but the post says it fails" if not failed
                        else detail if detail else "")
    return not failed, detail


def reset_scratch() -> None:
    """A fresh disposable copy of the lab database.

    Costs about a second (`CREATE DATABASE ... TEMPLATE`), which is worth paying per block: a
    no-transaction block cannot be wrapped in a rollback, so the only way to give it the state its
    post has built up — and still leave nothing behind — is to hand it a whole database to dirty.
    """
    drop_scratch()
    psql("postgres", f"CREATE DATABASE {SCRATCH_DB} TEMPLATE {DB};")


def drop_scratch() -> None:
    """Drop the scratch database — and nothing else, ever.

    The name is a module constant and this is the only place a DROP DATABASE is issued, so there
    is exactly one line to read when asking whether this script can destroy anything.
    """
    assert SCRATCH_DB not in ("stayhub", DB, "postgres"), "refusing to drop a real database"
    psql("postgres", f"DROP DATABASE IF EXISTS {SCRATCH_DB} WITH (FORCE);")


def _without_comments(source: str) -> str:
    return "\n".join(line for line in source.splitlines()
                     if line.strip() and not line.strip().startswith("--"))


def quoted_rows(block: str) -> list[tuple[str, ...]] | None:
    """Parse a psql result table out of a plaintext block, as tuples of trimmed cells.

    Returns None if the block is not a result table — a tree diagram, a shell transcript and an
    error message all live in plaintext blocks too.
    """
    lines = [l.rstrip() for l in block.splitlines()]
    separator = next((i for i, l in enumerate(lines)
                      if RESULT_SEPARATOR.match(l.replace("-", "-").strip())), None)
    if separator is None or separator == 0:
        return None
    rows = []
    for line in lines[separator + 1:]:
        stripped = line.strip()
        if not stripped or ROW_COUNT_FOOTER.match(stripped):
            continue
        if RESULT_SEPARATOR.match(stripped):
            # A second separator means a SECOND result set in the same block, so the line before
            # it was that set's header, not data. Drop it and carry on.
            if rows:
                rows.pop()
            continue
        cells = tuple(c.strip() for c in line.split("|"))
        if len(cells) < 2:
            return None       # not a table after all
        rows.append(cells)
    return rows or None


def actual_rows(context: str, query: str) -> list[tuple[str, ...]]:
    """Run a query and return its rows as tuples, unaligned so parsing is exact."""
    cmd = ["docker", "exec", "-i", CONTAINER, "psql", "-U", USER, "-d", DB,
           "-q", "-A", "-F", "|", "-t", "-v", "ON_ERROR_STOP=1"]
    # ⚠️ The context blocks are SELECTs as often as not, and their rows would land in stdout
    # beside the target query's. Silence them, or "actual" reports another block's answer and the
    # comparison quietly passes on rows that came from the wrong query.
    script = f"BEGIN;\n\\o /dev/null\n{context}\\o\n{query}\nROLLBACK;"
    try:
        result = subprocess.run(cmd, input=f"SET statement_timeout = '{STATEMENT_TIMEOUT}';\n{script}",
                                capture_output=True, text=True, timeout=PROCESS_TIMEOUT)
    except subprocess.TimeoutExpired:
        return []
    rows = []
    for line in result.stdout.splitlines():
        if not line.strip() or line.strip().startswith("("):
            continue
        rows.append(tuple(c.strip() for c in line.split("|")))
    return rows


def classify(source: str) -> str:
    if any(marker in source for marker in UNAVAILABLE):
        return "unavailable"
    if MULTI_SESSION.search(source):
        return "multi-session"
    if not STATEMENT_START.match(_without_comments(source)):
        return "fragment"
    if CLUSTER_LEVEL.search(source):
        return "cluster-level"
    if TEACHES_AN_ERROR.search(source):
        return "expect-error"
    if RECOVERS.search(source):
        return "recovers"
    if NO_TRANSACTION.search(source) or TRANSACTION_CONTROL.search(source):
        return "no-transaction"
    if PSQL_META.search(source):
        return "psql-meta"
    return "sql"


def main() -> int:
    # ⚠️ One run at a time. Two concurrent runs share the scratch database and take locks on the
    # same tables: the first to finish drops `stayhub_lab_scratch` out from under the second, and
    # the migration post's ALTER TABLE statements fail on lock_timeout waiting for the other run's
    # backfill. Every failure it produces blames a post that is correct.
    lock_path = HERE / ".check_sql.lock"
    try:
        lock_file = open(lock_path, "x")
    except FileExistsError:
        print(f"error: another check_sql.py run holds {lock_path}.\n"
              "       Wait for it, or delete the file if no run is active.", file=sys.stderr)
        return 2
    try:
        return _run()
    finally:
        lock_file.close()
        lock_path.unlink(missing_ok=True)


def _run() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--post", default=None, help="check one slug instead of the whole track")
    parser.add_argument("--verbose", action="store_true", help="print every block, not just fails")
    args = parser.parse_args()

    if not container_running():
        print(f"error: container '{CONTAINER}' is not running.\n"
              "       cd lovemesomecoding_demo_project/stayhub && docker compose up -d postgres",
              file=sys.stderr)
        return 2
    if not database_exists(DB):
        print(f"error: database '{DB}' does not exist.\n"
              "       projects/postgres_tutorial/lab/setup.sh", file=sys.stderr)
        return 2

    posts = manifest.POSTS
    if args.post:
        posts = [p for p in manifest.POSTS if p["slug"] == args.post]
        if not posts:
            print(f"not in the manifest: {args.post}", file=sys.stderr)
            return 2

    # Extract every post's blocks up front. ⚠️ Scan the EXTRACTED SOURCES, not the raw HTML: in
    # the file the first statement shares a line with the <pre> tag, so an anchored regex over the
    # markup never matches and the scratch database silently never gets built.
    extracted, all_blocks = {}, {}
    for entry in posts:
        path = HERE / "posts" / entry["file"]
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8")
        every = [(i, lang, html.unescape(body))
                 for i, (lang, body) in enumerate(BLOCK.findall(raw))]
        all_blocks[entry["slug"]] = every
        extracted[entry["slug"]] = [(i, body) for i, lang, body in every if lang == "sql"]

    all_sources = [src for blocks in extracted.values() for _i, src in blocks]
    needs_scratch = any(NO_TRANSACTION.search(src) or TRANSACTION_CONTROL.search(src)
                        or RECOVERS.search(src) for src in all_sources)

    if needs_scratch:
        reset_scratch()

    failures, counts = [], {}
    missing = []

    for entry in posts:
        path = HERE / "posts" / entry["file"]
        if not path.exists():
            missing.append(entry["slug"])
            continue

        sql_blocks = extracted[entry["slug"]]

        # (block index within the post, source, kind) in document order — the order the reader
        # meets them, which is the order they have to work in.
        ordered = [(i, src, classify(src)) for i, src in sql_blocks]

        per_post = {}
        for position, (index, source, kind) in enumerate(ordered):
            per_post[kind] = per_post.get(kind, 0) + 1
            counts[kind] = counts.get(kind, 0) + 1

            if kind in ("multi-session", "cluster-level", "fragment", "unavailable"):
                if args.verbose:
                    print(f"    block {index}: {kind}, not executed")
                continue

            ok, detail = run_block(ordered, position)
            if not ok:
                first_line = next((l for l in source.splitlines() if l.strip()), "")
                failures.append(
                    f"{entry['slug']} block {index} ({kind})\n"
                    f"      {first_line.strip()[:100]}\n"
                    f"      {detail[:160] if detail else 'no message'}")
            elif args.verbose:
                print(f"    block {index}: {kind} ok")

        # --- quoted output ------------------------------------------------------------------
        # A plaintext block right after a sql block is that block's result, as printed in the
        # post. Re-derive it and require every quoted row to be in the real answer.
        checked_outputs = 0
        for position, (index, lang, body) in enumerate(all_blocks[entry["slug"]]):
            if lang != "plaintext" or position == 0:
                continue
            prev_index, prev_lang, prev_body = all_blocks[entry["slug"]][position - 1]
            if prev_lang != "sql" or classify(prev_body) != "sql":
                continue
            if NON_REPRODUCIBLE.search(prev_body):
                counts["output-varies"] = counts.get("output-varies", 0) + 1
                continue
            quoted = quoted_rows(body)
            if not quoted:
                continue

            sql_position = next((n for n, (i, _s, _k) in enumerate(ordered) if i == prev_index),
                                None)
            if sql_position is None:
                continue
            context = "".join(
                _as_context(i, src, k) for i, src, k in ordered[:sql_position]
                if k not in ("multi-session", "no-transaction", "cluster-level", "fragment",
                         "unavailable", "recovers"))
            real = actual_rows(context, prev_body)
            checked_outputs += 1

            missing_rows = [r for r in quoted if r not in real]
            if missing_rows:
                failures.append(
                    f"{entry['slug']} block {index}: quoted output does not match the query in "
                    f"block {prev_index}\n"
                    + "".join(f"      quoted:  {' | '.join(r)}\n" for r in missing_rows[:3])
                    + (f"      actual:  {' | '.join(real[0])}\n" if real
                       else "      actual:  no rows\n"))
            counts["output-checked"] = counts.get("output-checked", 0) + 1

        summary = "  ".join(f"{n} {k}" for k, n in sorted(per_post.items()))
        print(f"{entry['slug']:<44} {len(sql_blocks):>3} sql blocks   {summary}")

    if needs_scratch:
        drop_scratch()

    print("-" * 96)
    total = sum(counts.values())
    print(f"{total} sql blocks executed against {DB}: "
          + ", ".join(f"{n} {k}" for k, n in sorted(counts.items())))

    for slug in missing:
        print(f"  not written: {slug}")

    if failures:
        print(f"\n{len(failures)} FAILURE(S):")
        for f in failures:
            print(f"  ✗ {f}")
        return 1

    print(f"\nevery SQL sample in the {len(posts) - len(missing)} written post(s) runs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

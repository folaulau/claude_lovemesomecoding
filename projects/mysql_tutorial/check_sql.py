#!/usr/bin/env python3
"""EXECUTE every SQL sample in the track, and re-derive every quoted result.

This is the check that matters. `check_content.py` proves a code block survives the pipeline
byte-for-byte; it has no idea whether the SQL is correct or whether the output printed under it
was ever produced by a computer. On the Postgres track this checker caught fabricated numbers on
its first run — an aggregation post quoted averages of 3.50/3.50/3.51/3.50 where the database
returns 3.49/3.52/3.52/3.50. The SQL was correct and ran cleanly. Nothing else would have noticed.

    projects/mysql_tutorial/check_sql.py
    projects/mysql_tutorial/check_sql.py --post sql-join-or-inner-join --verbose
    projects/mysql_tutorial/check_sql.py --list          # classify blocks, run nothing

Needs the demo container up:
    cd lovemesomecoding_demo_project/pizza/pizza-springboot-backend && docker compose up -d
and, for the posts in manifest.LAB_POSTS, the lab built:
    projects/mysql_tutorial/lab/setup.sh


HOW A POST IS RUN
-----------------
Blocks are replayed **in order, cumulatively, in one session** — block 5 runs with blocks 1-4
already applied — so a post that creates a table in one block and inserts into it in the next is
checked the way a reader meets it. Session state (user variables, temporary tables, an open
transaction) carries across blocks for the same reason.

⚠️ MySQL HAS NO TRANSACTIONAL DDL. This is the big difference from the Postgres checker, which
wraps a whole post in a transaction and rolls it back. In MySQL, CREATE/ALTER/DROP each cause an
implicit COMMIT, so a rollback protects nothing the moment a post creates a table.

So isolation is by DATABASE, not by transaction:

  * An ordinary post gets its own scratch database cloned from `pizza` — schema and all 1,600-odd
    rows, which takes a fraction of a second — and it is dropped afterwards. The post may do
    anything it likes in there, DDL included.

  * A post in manifest.LAB_POSTS runs against `pizza_lab` itself, because cloning 400,000 orders
    and 1,000,000 items per post is not worth the minutes. Those posts are read-mostly by nature,
    and anything they DO create is reversed afterwards: the checker snapshots the indexes, tables,
    views, routines, triggers and events before the post and drops whatever is new, then re-runs
    ANALYZE TABLE so the next post's query plans are not read off stale statistics.

  ⚠️ `pizza` itself is never written to. It is cloned, never used directly.


HOW OUTPUT IS CHECKED
---------------------
A `plaintext` block **immediately following** a `sql` block is treated as that statement's output
and re-derived — the checker runs the statement, formats the result with the mysql client's own
`-t` table renderer, and compares. That is the same renderer the post is quoting, so a match is
exact rather than approximate.

Blocks are classified automatically so a post cannot quietly opt out of being checked:

| kind            | handling                                                                  |
|-----------------|---------------------------------------------------------------------------|
| `sql`           | run, cumulatively, in the post's session                                   |
| `expect-error`  | carries a `-- ERROR` line, so it MUST fail; running clean is the finding   |
| `fragment`      | does not begin with a statement keyword — a column definition quoted to    |
|                 | show syntax. Not run, and it may not have an output block.                 |
| `multi-session` | carries `-- session 2`: half of a two-terminal locking demo. Reported.     |
| `unavailable`   | carries `-- unavailable: <reason>`. Reported with the reason.              |
| `output-varies` | mentions NOW(), RAND(), UUID(), CONNECTION_ID()... — run, output NOT       |
|                 | compared, because it cannot be stable                                     |
| `bash`/other    | not SQL. Not run.                                                         |

A `sql` block with an output block that does not match is a FAILURE. A `sql` block with no output
block is fine — plenty of statements have nothing worth printing.
"""

import argparse
import os
import re
import subprocess
import sys
import html
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

DB = manifest.DEMO_DB
MYSQL = os.environ.get("MYSQL_CLIENT", "mysql")

PRE = re.compile(r"<pre\b[^>]*>(.*?)</pre>", re.S | re.I)
LANG = re.compile(r'language-([\w-]+)', re.I)
INNER_CODE = re.compile(r"^\s*<code\b[^>]*>(.*)</code>\s*$", re.S | re.I)

# A block that begins with one of these is a statement we can run.
STATEMENT_START = re.compile(
    r"^\s*(?:--[^\n]*\n\s*)*"                     # leading comments
    r"(SELECT|INSERT|UPDATE|DELETE|REPLACE|WITH|CREATE|ALTER|DROP|TRUNCATE|"
    r"EXPLAIN|DESCRIBE|DESC|SHOW|SET|USE|START|BEGIN|COMMIT|ROLLBACK|SAVEPOINT|"
    r"GRANT|REVOKE|FLUSH|ANALYZE|OPTIMIZE|CALL|PREPARE|EXECUTE|DEALLOCATE|"
    r"LOCK|UNLOCK|RENAME|KILL|DELIMITER|HANDLER|DO|VALUES|TABLE)\b",
    re.I)

# Output that cannot be stable, so it is run but not compared.
NONDETERMINISTIC = re.compile(
    r"\b(NOW|CURDATE|CURTIME|CURRENT_DATE|CURRENT_TIME|CURRENT_TIMESTAMP|SYSDATE|"
    r"UNIX_TIMESTAMP|RAND|UUID|UUID_SHORT|CONNECTION_ID|LAST_INSERT_ID|BENCHMARK|SLEEP|"
    r"VERSION|DATABASE|USER|CURRENT_USER|SHOW\s+PROCESSLIST|SHOW\s+ENGINE|"
    r"INFORMATION_SCHEMA|PERFORMANCE_SCHEMA|@@)\b", re.I)

MARK_ERROR = re.compile(r"^\s*--\s*ERROR\b", re.I | re.M)
MARK_SESSION2 = re.compile(r"^\s*--\s*session\s*2\b", re.I | re.M)
MARK_UNAVAILABLE = re.compile(r"^\s*--\s*unavailable:\s*(.+)$", re.I | re.M)
MARK_NOCHECK = re.compile(r"^\s*--\s*output-varies\b", re.I | re.M)

SENTINEL = "@@@LMSC_BLOCK_{}@@@"
SENTINEL_ANY = re.compile(r"@@@LMSC_BLOCK_(\d+)@@@")


def my(args: list[str], stdin: str | None = None, database: str | None = None) -> tuple[int, str]:
    """Run the mysql client.

    ⚠️ stderr is redirected INTO stdout with subprocess.STDOUT rather than captured
    separately and concatenated. They have to interleave in real time: with two separate
    pipes every ERROR line lands at the very END of the transcript, after all the output,
    so it cannot be attributed to the block that caused it — and a block marked
    `-- ERROR` then reads as having run cleanly.
    """
    cmd = [MYSQL, "-h", DB["host"], "-P", str(DB["port"]), "-u", DB["user"]]
    if database:
        cmd.append(database)
    cmd += args
    p = subprocess.run(cmd, input=stdin, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout or ""


def server_up() -> bool:
    return my(["-N", "-B", "-e", "SELECT 1"])[0] == 0


def database_exists(name: str) -> bool:
    rc, out = my(["-N", "-B", "-e",
                  f"SELECT COUNT(*) FROM information_schema.SCHEMATA "
                  f"WHERE SCHEMA_NAME = '{name}'"])
    return rc == 0 and out.strip().endswith("1")


# ---------------------------------------------------------------- block extraction
def blocks_of(path: Path) -> list[dict]:
    """Every <pre> in the post, in order, with its language and classification."""
    out = []
    for raw_inner in PRE.findall(path.read_text(encoding="utf-8")):
        m = INNER_CODE.match(raw_inner)
        inner = m.group(1) if m else raw_inner
        lang_m = LANG.search(raw_inner)
        lang = (lang_m.group(1).lower() if lang_m else "plaintext")
        if lang == "mysql":
            lang = "sql"
        out.append({"lang": lang, "sql": html.unescape(inner)})

    for i, b in enumerate(out):
        b["kind"] = classify(b, out[i - 1] if i else None)
    return out


def classify(block: dict, prev: dict | None) -> str:
    if block["lang"] == "plaintext":
        # Output of the statement above it, or just a quoted listing.
        return "output" if prev and prev["lang"] == "sql" else "prose-block"
    if block["lang"] != "sql":
        return block["lang"]

    body = block["sql"]
    if MARK_UNAVAILABLE.search(body):
        return "unavailable"
    if MARK_SESSION2.search(body):
        return "multi-session"
    if MARK_ERROR.search(body):
        return "expect-error"
    if not STATEMENT_START.match(body):
        return "fragment"
    if MARK_NOCHECK.search(body) or NONDETERMINISTIC.search(body):
        return "output-varies"
    return "sql"


RUNNABLE = {"sql", "output-varies", "expect-error"}


def split_chunks(out: str) -> dict[int, str]:
    """Cut a transcript into one chunk per block, keyed by block index.

    In -t (table) mode `SELECT '@@@LMSC_BLOCK_3@@@' AS marker;` renders as exactly five
    lines: a top rule, the `marker` header, a rule, the value, and a closing rule. So a
    block's own output starts 2 lines after the line holding the sentinel value (skipping
    that closing rule), and ends 3 lines before the NEXT sentinel value line (excluding
    its top rule and header).

    Slicing by line index rather than trimming leading "+--" is what keeps the real
    table's own top border, which a trim-based version silently ate.
    """
    lines = out.splitlines()
    marks = [(i, int(m.group(1)))
             for i, line in enumerate(lines)
             if (m := SENTINEL_ANY.search(line)) and not line.lstrip().startswith("SELECT")]
    chunks: dict[int, str] = {}
    for idx, (line_no, num) in enumerate(marks):
        start = line_no + 2
        end = (marks[idx + 1][0] - 3) if idx + 1 < len(marks) else len(lines)
        chunks[num] = "\n".join(lines[start:max(start, end)]).strip("\n")
    return chunks


# ---------------------------------------------------------------- scratch databases
def clone_pizza(scratch: str) -> None:
    """A full copy of the demo database. Small enough that this is cheap."""
    tables = ["crust", "topping", "product", "product_size", "app_user",
              "customer_order", "order_item", "order_item_topping",
              "cart", "cart_item", "cart_item_topping",
              "user_address", "user_payment_method"]
    stmt = [f"DROP DATABASE IF EXISTS {scratch};",
            f"CREATE DATABASE {scratch} CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;",
            f"USE {scratch};", "SET FOREIGN_KEY_CHECKS=0;"]
    for t in tables:
        stmt.append(f"CREATE TABLE {t} LIKE pizza.{t};")
    for t in tables:
        stmt.append(f"INSERT INTO {t} SELECT * FROM pizza.{t};")
    stmt.append("SET FOREIGN_KEY_CHECKS=1;")
    rc, out = my(["-e", "\n".join(stmt)])
    if rc != 0:
        raise SystemExit(f"could not create scratch database {scratch}:\n{out}")


def drop_db(name: str) -> None:
    my(["-e", f"DROP DATABASE IF EXISTS {name};"])


def object_snapshot(db: str) -> dict[str, set]:
    """Everything a post could create, so it can be dropped again afterwards."""
    q = {
        "tables": f"SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='{db}' AND TABLE_TYPE='BASE TABLE'",
        "views": f"SELECT TABLE_NAME FROM information_schema.VIEWS WHERE TABLE_SCHEMA='{db}'",
        "indexes": f"SELECT CONCAT(TABLE_NAME,'.',INDEX_NAME) FROM information_schema.STATISTICS WHERE TABLE_SCHEMA='{db}'",
        "routines": f"SELECT CONCAT(ROUTINE_TYPE,':',ROUTINE_NAME) FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA='{db}'",
        "triggers": f"SELECT TRIGGER_NAME FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA='{db}'",
        "events": f"SELECT EVENT_NAME FROM information_schema.EVENTS WHERE EVENT_SCHEMA='{db}'",
    }
    snap = {}
    for key, sql in q.items():
        rc, out = my(["-N", "-B", "-e", sql])
        snap[key] = set(filter(None, (line.strip() for line in out.splitlines()))) if rc == 0 else set()
    return snap


def restore(db: str, before: dict[str, set]) -> list[str]:
    """Drop whatever the post created in a shared database. Returns what it undid."""
    after = object_snapshot(db)
    undone = []
    for name in sorted(after["events"] - before["events"]):
        my(["-e", f"DROP EVENT IF EXISTS {db}.{name};"]); undone.append(f"event {name}")
    for name in sorted(after["triggers"] - before["triggers"]):
        my(["-e", f"DROP TRIGGER IF EXISTS {db}.{name};"]); undone.append(f"trigger {name}")
    for item in sorted(after["routines"] - before["routines"]):
        kind, _, name = item.partition(":")
        my(["-e", f"DROP {kind} IF EXISTS {db}.{name};"]); undone.append(f"{kind.lower()} {name}")
    for name in sorted(after["views"] - before["views"]):
        my(["-e", f"DROP VIEW IF EXISTS {db}.{name};"]); undone.append(f"view {name}")
    for item in sorted(after["indexes"] - before["indexes"]):
        table, _, index = item.partition(".")
        if index == "PRIMARY" or table in (after["tables"] - before["tables"]):
            continue
        my(["-e", f"DROP INDEX `{index}` ON {db}.`{table}`;"]); undone.append(f"index {item}")
    for name in sorted(after["tables"] - before["tables"]):
        my(["-e", f"SET FOREIGN_KEY_CHECKS=0; DROP TABLE IF EXISTS {db}.`{name}`;"])
        undone.append(f"table {name}")
    if undone:
        # Statistics change when an index is added and dropped; the next post's plans
        # would otherwise be read off whatever was left behind.
        my(["-e", f"USE {db}; ANALYZE TABLE customer_order, order_item, app_user;"])
    return undone


# ---------------------------------------------------------------- running a post
def run_post(entry: dict, verbose: bool, twice: bool = True) -> tuple[list[str], dict]:
    """Execute a post's blocks and compare every quoted result.

    ⚠️ By default the whole post is executed TWICE, from a freshly rebuilt state, and any
    compared output that differs between the two runs is reported as non-deterministic.

    That check exists because of a real near-miss. `sql-limit` opened with
    `ORDER BY total DESC LIMIT 3` on a table where two orders share the total 32.18 — so
    the third row could legitimately come back as either of them. It passed, once, by
    luck. A quoted result that is only usually right is worse than one that is wrong,
    because it fails on someone else's machine long after it was written.

    A tie in ORDER BY is the common cause; the other is any output whose row order is not
    fully determined (GROUP BY with no ORDER BY, a plan-dependent scan order).
    """
    path = HERE / "posts" / entry["file"]
    blocks = blocks_of(path)
    slug = entry["slug"]
    is_lab = slug in manifest.LAB_POSTS

    stats = {k: 0 for k in
             ("sql", "output-varies", "expect-error", "fragment", "multi-session",
              "unavailable", "output", "checked", "nondeterministic", "other")}
    for b in blocks:
        stats[b["kind"]] = stats.get(b["kind"], 0) + 1

    runnable = [(i, b) for i, b in enumerate(blocks) if b["kind"] in RUNNABLE]
    if not runnable:
        return [], stats

    if is_lab:
        database = manifest.LAB_DB["database"]
        before = object_snapshot(database)
        scratch = None
    else:
        scratch = f"pzcheck_{re.sub(r'[^a-z0-9]', '_', slug)}"[:60]
        clone_pizza(scratch)
        database = scratch
        before = None

    # One session, all blocks, sentinels between them. --force so an expect-error block
    # does not abort the rest of the post.
    script = []
    for i, b in runnable:
        script.append(f"SELECT '{SENTINEL.format(i)}' AS marker;")
        body = b["sql"].strip()
        if not body.endswith(";") and not body.rstrip().endswith("END"):
            body += ";"
        script.append(body)
    script.append(f"SELECT '{SENTINEL.format(999999)}' AS marker;")
    script_text = "\n".join(script)

    _rc, out = my(["-t", "--force"], stdin=script_text, database=database)

    # Second pass from a rebuilt state, to catch output that is not deterministic.
    second: dict[int, str] | None = None
    if twice:
        if scratch:
            clone_pizza(scratch)
        else:
            restore(database, before)
        _rc2, out2 = my(["-t", "--force"], stdin=script_text, database=database)
        second = split_chunks(out2)

    chunks = split_chunks(out)

    failures = []
    for i, b in runnable:
        chunk = chunks.get(i, "")
        errored = "ERROR " in chunk
        if b["kind"] == "expect-error":
            if not errored:
                failures.append(
                    f"{slug} block {i}: marked `-- ERROR` but ran cleanly.\n"
                    f"    {b['sql'].strip().splitlines()[0][:100]}")
            continue
        if errored:
            msg = next((l for l in chunk.splitlines() if "ERROR " in l), chunk[:200])
            failures.append(f"{slug} block {i}: {msg.strip()}\n"
                            f"    {b['sql'].strip().splitlines()[0][:100]}")
            continue

        # Compare against the plaintext block that follows, if there is one.
        nxt = blocks[i + 1] if i + 1 < len(blocks) else None
        if not nxt or nxt["kind"] != "output":
            continue
        if b["kind"] == "output-varies":
            continue

        expected = nxt["sql"].strip("\n").rstrip()
        actual = chunk.rstrip()
        stats["checked"] += 1

        # Non-determinism first: an output that changes between two runs cannot be quoted
        # at all, and reporting "does not match" for it would send you looking for the
        # wrong bug.
        if second is not None and _normalise(second.get(i, "")) != _normalise(actual):
            stats["nondeterministic"] = stats.get("nondeterministic", 0) + 1
            failures.append(
                f"{slug} block {i}: OUTPUT IS NOT DETERMINISTIC — two runs of the same "
                f"statement disagreed, so no quoted result can be correct.\n"
                f"    Usually a tie in ORDER BY, or a query with no total ordering at all. "
                f"Add a unique tiebreaker (the primary key will do).\n"
                f"  --- run 1 ---\n{_indent(actual)}\n"
                f"  --- run 2 ---\n{_indent(second.get(i, ''))}")
            continue

        if _normalise(expected) != _normalise(actual):
            failures.append(
                f"{slug} block {i}: quoted output does not match what the database returns.\n"
                f"  --- quoted ---\n{_indent(expected)}\n"
                f"  --- actual ---\n{_indent(actual)}")
        elif verbose:
            print(f"    block {i} output re-derived and matches ({len(expected.splitlines())} lines)")

    if scratch:
        drop_db(scratch)
    elif before is not None:
        undone = restore(database, before)
        if undone and verbose:
            print(f"    restored {database}: dropped {', '.join(undone)}")

    return failures, stats


def _normalise(text: str) -> str:
    """Trailing whitespace and blank lines only. Column alignment IS compared."""
    return "\n".join(line.rstrip() for line in text.strip().splitlines() if line.strip())


def _indent(text: str) -> str:
    return "\n".join("      " + l for l in text.splitlines()[:24])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--post", default=None, help="one slug, instead of the whole track")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--list", action="store_true",
                    help="classify every block and exit without running anything")
    ap.add_argument("--once", action="store_true",
                    help="run each post once instead of twice. Skips the non-determinism "
                         "check — faster, and weaker.")
    args = ap.parse_args()

    entries = manifest.POSTS
    if args.post:
        entries = [e for e in manifest.POSTS if e["slug"] == args.post]
        if not entries:
            raise SystemExit(f"not in the manifest: {args.post}")

    present = [e for e in entries if (HERE / "posts" / e["file"]).exists()]
    absent = [e for e in entries if not (HERE / "posts" / e["file"]).exists()]

    if args.list:
        for e in present:
            bs = blocks_of(HERE / "posts" / e["file"])
            kinds: dict[str, int] = {}
            for b in bs:
                kinds[b["kind"]] = kinds.get(b["kind"], 0) + 1
            print(f"{e['slug']:<38} " + "  ".join(f"{k}:{v}" for k, v in sorted(kinds.items())))
        if absent:
            print(f"\n{len(absent)} post(s) not written yet")
        return 0

    if not present:
        print(f"no post files written yet ({len(absent)} in the manifest). Nothing to run.")
        return 0

    if not server_up():
        print(f"cannot reach MySQL at {DB['host']}:{DB['port']}.\n"
              "start it with:  cd lovemesomecoding_demo_project/pizza/pizza-springboot-backend "
              "&& docker compose up -d")
        return 2
    if not database_exists("pizza"):
        print("the `pizza` database is not there. Start the app once so Liquibase runs.")
        return 2

    needs_lab = [e for e in present if e["slug"] in manifest.LAB_POSTS]
    if needs_lab and not database_exists(manifest.LAB_DB["database"]):
        print(f"{len(needs_lab)} post(s) need `{manifest.LAB_DB['database']}`, which does not "
              "exist.\nbuild it with:  projects/mysql_tutorial/lab/setup.sh")
        return 2

    all_failures = []
    totals = {"checked": 0, "sql": 0}
    for e in present:
        print(f"{e['slug']:<38}", end=" ", flush=True)
        failures, stats = run_post(e, args.verbose, twice=not args.once)
        totals["checked"] += stats.get("checked", 0)
        totals["sql"] += stats.get("sql", 0) + stats.get("output-varies", 0)
        summary = (f"{stats.get('sql', 0) + stats.get('output-varies', 0)} run, "
                   f"{stats.get('checked', 0)} output checked")
        extra = [f"{k} {stats[k]}" for k in
                 ("expect-error", "fragment", "multi-session", "unavailable")
                 if stats.get(k)]
        print(f"{summary}" + (f"  [{', '.join(extra)}]" if extra else "")
              + ("" if not failures else f"  ✗ {len(failures)}"))
        all_failures += failures

    print()
    if absent:
        print(f"{len(absent)} post(s) not written yet.")
    print(f"{totals['sql']} statement block(s) executed, "
          f"{totals['checked']} quoted result(s) re-derived.")

    if all_failures:
        print(f"\n{len(all_failures)} FAILURE(S):")
        for f in all_failures:
            print(f"  ✗ {f}")
        return 1
    print("all pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

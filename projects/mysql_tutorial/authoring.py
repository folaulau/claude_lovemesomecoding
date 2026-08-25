#!/usr/bin/env python3
"""Emit a ready-to-paste sql + output block pair, with the output taken from the database.

The first post written for this track quoted `| 22.51    |` where the mysql client actually
prints `|    22.51 |` — it right-aligns numeric columns. check_sql.py caught it, but the better
answer is not to type result sets by hand at all.

    projects/mysql_tutorial/authoring.py "SELECT name, type FROM product ORDER BY id LIMIT 5"
    projects/mysql_tutorial/authoring.py --lab "SELECT status, COUNT(*) FROM customer_order GROUP BY status"
    projects/mysql_tutorial/authoring.py --db pzscratch -f snippet.sql
    projects/mysql_tutorial/authoring.py --no-output "CREATE INDEX ..."   # sql block only

Prints the two <pre> blocks exactly as they should appear in the post. The SQL is echoed as you
wrote it — indentation included — so format it the way you want it to read.
"""

import argparse
import html
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manifest  # noqa: E402

DB = manifest.DEMO_DB


def run(sql: str, database: str) -> str:
    p = subprocess.run(
        ["mysql", "-h", DB["host"], "-P", str(DB["port"]), "-u", DB["user"], database, "-t"],
        input=sql, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.stdout.rstrip("\n")


def block(lang: str, body: str) -> str:
    return (f'<pre class="language-{lang}"><code class="language-{lang}">'
            f'{html.escape(body, quote=False)}</code></pre>')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("sql", nargs="?", help="the statement (or use -f)")
    ap.add_argument("-f", "--file", help="read the statement from a file")
    ap.add_argument("--lab", action="store_true", help="run against pizza_lab")
    ap.add_argument("--db", default=None, help="run against a named database")
    ap.add_argument("--no-output", action="store_true", help="emit only the sql block")
    args = ap.parse_args()

    sql = Path(args.file).read_text() if args.file else args.sql
    if not sql:
        ap.error("give a statement, or -f FILE")
    sql = sql.strip().rstrip(";")

    database = args.db or (manifest.LAB_DB["database"] if args.lab else DB["database"])

    print(block("sql", sql + ";"))
    if args.no_output:
        return 0

    out = run(sql + ";", database)
    if "ERROR" in out and not out.lstrip().startswith("+"):
        print(f"\n-- the statement failed against `{database}`:\n{out}", file=sys.stderr)
        return 1
    print()
    print(block("plaintext", out))

    # A quiet nudge: anything non-deterministic will be reclassified `output-varies` by
    # check_sql.py and its output will NOT be compared, so pasting it is decoration.
    if re.search(r"\b(NOW|RAND|UUID|SYSDATE|CURDATE|CONNECTION_ID|VERSION)\s*\(", sql, re.I):
        print("\n-- note: non-deterministic. check_sql.py will run this but not compare the "
              "output.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

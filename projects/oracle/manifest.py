"""The Oracle Database track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and lesson 14 is the newest.

Slugs are frozen the moment this is published. Changing one changes a URL.
"""

CATEGORY = {
    "slug": "oracle",
    "name": "Oracle",
    "description": (
        "Oracle Database from the ground up — architecture, SQL, PL/SQL, indexes, "
        "transactions and Spring Boot integration."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts.
NAV_GROUP = "Data Store"

POSTS = [
    {
        "slug": "oracle-introduction",
        "title": "Oracle Database – Introduction",
        "file": "01-oracle-introduction.html",
        "date": "2024-01-08T09:00:00",
        "tags": ["oracle", "architecture"],
        "excerpt": (
            "Oracle Database is what you meet the moment you work on anything old and important. "
            "Instance versus database, the tablespace-to-block storage hierarchy, CDB and PDB, "
            "which edition to install, and a table of every place Oracle behaves differently from "
            "MySQL and Postgres — a user is a schema, an empty string is NULL, and a DATE carries "
            "a time."
        ),
    },
    {
        "slug": "oracle-run-with-docker",
        "title": "Oracle Database – Run It Locally with Docker",
        "file": "02-oracle-run-with-docker.html",
        "date": "2024-01-15T09:00:00",
        "tags": ["oracle", "docker"],
        "excerpt": (
            "Oracle Database Free in a container: the image to pull, the three environment "
            "variables that matter, how to tell when the database is genuinely ready, and why you "
            "must connect to the FREEPDB1 service rather than FREE. Includes a docker-compose file "
            "with schema init scripts, and the gotchas on Apple Silicon."
        ),
    },
    {
        "slug": "oracle-users-schemas-and-privileges",
        "title": "Oracle Database – Users, Schemas and Privileges",
        "file": "03-oracle-users-schemas-and-privileges.html",
        "date": "2024-01-22T09:00:00",
        "tags": ["oracle", "security"],
        "excerpt": (
            "In Oracle a user is a schema, so CREATE USER is how you create a namespace. Setting up "
            "a proper application account: why a tablespace quota is not optional, what CONNECT and "
            "RESOURCE really grant, the owner/role/service-account split, three ways to stop "
            "qualifying table names, and the password expiry that locks out service accounts."
        ),
    },
    {
        "slug": "oracle-data-types",
        "title": "Oracle Database – Data Types",
        "file": "04-oracle-data-types.html",
        "date": "2024-01-29T09:00:00",
        "tags": ["oracle", "sql"],
        "excerpt": (
            "VARCHAR2 versus CHAR and why the BYTE/CHAR length qualifier matters in UTF-8. NUMBER "
            "precision and why money never goes in a binary float. The fact that DATE includes a "
            "time, and the range comparison that follows from it. Booleans before 23ai, the empty "
            "string that is NULL, and a full mapping table to Java types."
        ),
    },
    {
        "slug": "oracle-tables-constraints-and-sequences",
        "title": "Oracle Database – Tables, Constraints and Sequences",
        "file": "05-oracle-tables-constraints-and-sequences.html",
        "date": "2024-02-05T09:00:00",
        "tags": ["oracle", "sql"],
        "excerpt": (
            "A CREATE TABLE worth copying, and the five constraint types. Why an unindexed foreign "
            "key locks the child table, why composite UNIQUE lets partly-null duplicates through, "
            "and the ON UPDATE CASCADE Oracle does not have. Identity columns versus sequences, "
            "CACHE and the gaps it creates, and how to drop a column on a large table."
        ),
    },
    {
        "slug": "oracle-select-essentials",
        "title": "Oracle Database – SELECT Essentials",
        "file": "06-oracle-select-essentials.html",
        "date": "2024-02-12T09:00:00",
        "tags": ["oracle", "sql"],
        "excerpt": (
            "The querying idioms that are specific to Oracle: DUAL, FETCH FIRST versus the ROWNUM "
            "pagination trap, NVL against COALESCE, NULLS FIRST, date format masks where MM and MI "
            "are not the same thing, LISTAGG and its 4000-byte overflow, ROLLUP, MERGE as the "
            "upsert, and INSERT ALL because Oracle rejects a multi-row VALUES list."
        ),
    },
    {
        "slug": "oracle-joins",
        "title": "Oracle Database – Joins",
        "file": "07-oracle-joins.html",
        "date": "2024-02-19T09:00:00",
        "tags": ["oracle", "sql"],
        "excerpt": (
            "ANSI joins, the legacy (+) operator you will meet in every pre-2005 codebase and why "
            "missing one silently turns an outer join into an inner one, semi-joins with EXISTS, and "
            "the NOT IN trap that returns zero rows without an error when the subquery contains a "
            "NULL. Plus the correlated join a plain JOIN cannot do, the three join methods Oracle "
            "picks between, and how to recognise a bad nested loop in a plan."
        ),
    },
    {
        "slug": "oracle-cross-apply",
        "title": "Oracle Database – CROSS APPLY and OUTER APPLY",
        "file": "08-oracle-cross-apply.html",
        "date": "2024-02-22T09:00:00",
        "tags": ["oracle", "sql"],
        "excerpt": (
            "An inline view that can see the row it is joined to, evaluated once per outer row. The "
            "four spellings and why CROSS APPLY silently drops rows where OUTER APPLY keeps them. "
            "Top-N per group and exactly when it beats ROW_NUMBER, several aggregates in one pass, "
            "per-row table functions, and how to read Starts and WINDOW NOSORT STOPKEY in the plan."
        ),
    },
    {
        "slug": "oracle-analytic-functions",
        "title": "Oracle Database – Analytic Functions",
        "file": "09-oracle-analytic-functions.html",
        "date": "2024-02-26T09:00:00",
        "tags": ["oracle", "sql"],
        "excerpt": (
            "Window functions are the feature that most changes how you write SQL. ROW_NUMBER, RANK "
            "and DENSE_RANK compared on ties, top-N per group, deduplication by ROWID, LAG and LEAD, "
            "running totals — including the ROWS versus RANGE default that quietly gives wrong "
            "numbers — the LAST_VALUE frame trap, KEEP DENSE_RANK, and gaps and islands."
        ),
    },
    {
        "slug": "oracle-pivot",
        "title": "Oracle Database – PIVOT and UNPIVOT",
        "file": "10-oracle-pivot.html",
        "date": "2024-03-01T09:00:00",
        "tags": ["oracle", "sql"],
        "excerpt": (
            "Rows into columns and back again. The implicit GROUP BY over every column you did not "
            "mention — the one fact behind almost every surprising PIVOT result — plus why values "
            "missing from the IN list vanish silently, why an empty cell is NULL from sum but 0 "
            "from count, the three errors you get for a non-constant IN list and what to do "
            "instead, and UNPIVOT's habit of dropping NULLs by default."
        ),
    },
    {
        "slug": "oracle-pl-sql",
        "title": "Oracle Database – PL/SQL",
        "file": "11-oracle-pl-sql.html",
        "date": "2024-03-04T09:00:00",
        "tags": ["oracle", "plsql"],
        "excerpt": (
            "Anonymous blocks, %TYPE and %ROWTYPE, the two exceptions SELECT INTO can raise, cursor "
            "FOR loops, and packages as the unit of organisation. Exception handling done properly, "
            "why WHEN OTHERS THEN NULL is the worst line of code in the Oracle world, BULK COLLECT "
            "and FORALL with SAVE EXCEPTIONS — and when to write plain SQL instead."
        ),
    },
    {
        "slug": "oracle-indexes-and-execution-plans",
        "title": "Oracle Database – Indexes and Execution Plans",
        "file": "12-oracle-indexes-and-execution-plans.html",
        "date": "2024-03-11T09:00:00",
        "tags": ["oracle", "performance"],
        "excerpt": (
            "Tuning Oracle is one skill: get the real plan and compare estimated rows against actual "
            "rows. Index types and the composite leading-column rule, the four reasons your index is "
            "ignored — including implicit conversion and the NULLs a B-tree does not store — "
            "DBMS_XPLAN with GATHER_PLAN_STATISTICS, bind variables, and invisible indexes."
        ),
    },
    {
        "slug": "oracle-transactions-and-locking",
        "title": "Oracle Database – Transactions and Locking",
        "file": "13-oracle-transactions-and-locking.html",
        "date": "2024-03-18T09:00:00",
        "tags": ["oracle", "concurrency"],
        "excerpt": (
            "Why readers never block writers, and how undo delivers both rollback and read "
            "consistency. Where a transaction starts, the DDL that commits behind your back, the two "
            "isolation levels Oracle actually has and the ORA-08177 retry that SERIALIZABLE requires. "
            "SELECT FOR UPDATE SKIP LOCKED as a work queue, deadlocks, and finding the blocker."
        ),
    },
    {
        "slug": "oracle-with-spring-boot",
        "title": "Oracle Database – With Spring Boot",
        "file": "14-oracle-with-spring-boot.html",
        "date": "2024-03-25T09:00:00",
        "tags": ["oracle", "spring-boot", "java"],
        "excerpt": (
            "Driver, URL, and the colon-versus-slash that decides between a SID and a service name. "
            "A tuned Hikari and JPA configuration, a Lombok entity that does not break hashCode, the "
            "allocationSize mismatch that causes ORA-00001 under load, batching, calling PL/SQL "
            "packages, Testcontainers against real Oracle, and a table of the errors you will hit."
        ),
    },
]

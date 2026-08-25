"""The MySQL track: category metadata plus one entry per post.

`file` is relative to `posts/`. `date` drives ordering everywhere on the site —
archives and the sitemap sort newest first, and prev/next walks the category
oldest-first — so the dates ascend with the track and the last lesson is the
newest.

⚠️ FORTY-TWO OF THESE SLUGS ARE LIVE, INDEXED URLS.

Unlike the Vue track (every slug new) or the Postgres track (two legacy stubs),
`/sql` is a populated WordPress-era collection: 42 posts published between
2018-09-29 and 2021-09-13. Every one of them is rewritten IN PLACE. Renaming any
of them is a dead link, and `lovemesomecoding_frontend/scripts/verify-build.mjs`
fails the build for exactly that. The full list is FROZEN_SLUGS below and
check_content.py asserts every one of them is still in the manifest.

That decision was taken deliberately over the alternative — consolidating the
five separate join posts and the one-idea stubs behind redirects. Keeping them
costs a handful of thin-by-nature pages; retiring them costs indexed URLs that
have ranked since 2019. Nothing here is redirected, so `add_redirects.py` has no
equivalent in this project.

Ten posts are NEW (marked `new: True`), filling the gaps the WordPress
collection never had: getting started, install, data types, DDL, normalization,
UNION, CTEs, window functions, privileges and replication.

DATES ARE COMPUTED, not preserved. The stored posts carry their original
2018-2021 dates and `upsert_post` never overwrites a date, so seeding this track
needs `seed.py --force-dates` — see the docstring there. Re-basing was chosen so
the archive and the ‹ prev / next › pager read lesson 1 -> lesson 52 instead of
the historical jumble the WordPress dates produce.
"""

from datetime import datetime, timedelta

CATEGORY = {
    "slug": "sql",
    "name": "SQL",
    "description": (
        "MySQL 8 from first connection to production — schema design and data types, "
        "SELECT and joins, aggregation, CTEs and window functions, indexes and query plans, "
        "transactions and deadlocks, backup, binlog and replication, every query run against "
        "a real pizza-ordering database."
    ),
}

# Where the category sits in the site navigation, for reference. The nav itself
# lives in lovemesomecoding_frontend/src/lib/nav.ts, where `sql` is ALREADY
# listed in the Data Store group. Nothing to do there — only the stored category
# record needs its description filled in, and `upsert_category` does that.
NAV_GROUP = "Data Store"

# The app every schema and query is taken from, so a reader can go and see the
# whole thing in context rather than a fragment invented for the tutorial.
DEMO_APP = "lovemesomecoding_demo_project/pizza/pizza-springboot-backend"

# The versions the whole track is written against. Lesson 1 prints this table,
# and every other lesson assumes it.
#
# These are READ OFF THE RUNNING CONTAINER AND THE POM, not chosen — a lesson
# claiming a version its output was not captured from is exactly the kind of
# drift nobody spots later.
VERSIONS = {
    "MySQL server": "8.4.11",
    "image": "mysql:8.4",
    "Spring Boot": "4.1.0",
    "connector": "mysql-connector-j",
    "migrations": "Liquibase (spring-boot-starter-liquibase)",
    "character set": "utf8mb4 / utf8mb4_0900_ai_ci",
}

# How the demo database is reached. The host port is deliberately NOT 3306 —
# see the comment in the app's docker-compose.yml.
DEMO_DB = {
    "host": "127.0.0.1",
    "port": 3308,
    "user": "root",
    "password": "",
    "database": "pizza",
}

# ⚠️ Two databases, and the difference matters.
#
# `pizza` is the demo application's own database: 18 orders, 14 products. It is
# the right size for teaching SELECT, joins and aggregation, because a reader can
# hold the whole result set in their head and check the answer by eye.
#
# It is the WRONG size for teaching indexes, EXPLAIN, or anything about
# contention. At 18 rows the optimizer table-scans everything, and an "add an
# index" lesson would show an index the planner never chooses. `pizza_lab` is the
# same schema filled to a realistic size — see lab/. The posts listed in
# LAB_POSTS use it and say so.
LAB_DB = dict(DEMO_DB, database="pizza_lab")

# Row counts in `pizza_lab`, from one build of lab/setup.sh. check_content.py
# rejects any figure a post quotes about the lab that is not one of these, and
# check_sql.py re-derives them. A plausible-looking round number that nobody ran
# is exactly what that catches.
LAB_ROWS = {
    "app_user": 50_000,
    "product": 14,
    "product_size": 42,
    "customer_order": 400_000,
    "order_item": 1_000_000,
    "order_item_topping": 1_000_000,
    "guest_orders": 80_000,          # customer_order.user_id IS NULL
    "orders_by_status": {
        "COMPLETED": 340_000,
        "CANCELLED": 24_000,
        "PENDING_PAYMENT": 16_000,
        "PREPARING": 12_000,
        "PAID": 8_000,
    },
    # The window every date-range and GROUP BY month lesson works inside. Anchored
    # to lab/build.sql's @LAB_EPOCH, NOT to NOW(), so a quoted result does not go
    # stale the day after it was written.
    "oldest_order": "2023-01-02",
    "newest_order": "2025-01-01",
}

# Only these posts may quote a query plan or a lab row count. EXPLAIN output is
# the most tempting thing in the track to invent — it looks authoritative and
# nobody checks — so the posts that show one are declared here and check_sql.py
# re-runs every plan they print.
LAB_POSTS = {
    "mysql-index",
    "sql-explain",
    "mysql-deadlock",
    "mysql-transaction",
    "mysql-run-query-in-production",
    "mysql-replication",
    "mysql-interview-advanced-queries",
}

# Lesson 1 is stamped START_DATE and each following lesson is STEP_DAYS later,
# so the pager reads lesson 1 -> lesson 52. Re-base the whole track by editing
# these two values; nothing else needs to change.
#
# 52 lessons x 5 days = a 255-day span, 2024-05-06 -> 2025-01-16.
#
# ⚠️ `--force-dates` is NOT a one-off here: every one of these 52 posts already
# exists with a 2018-2021 date, so the FIRST seed needs it and so does any later
# change to START_DATE.
#
# On the window: 2024-05 -> 2025-01 is THIS TRACK'S choice, not a site rule.
# There is no global date ceiling — the LeetCode track retired its own
# 2022-2024 brief on 2026-08-24 and now runs past 2025 with no ceiling above
# problem 543. The two constraints that are real:
#   * dates must ASCEND with the track, or the prev/next pager reads out of order
#   * a date must not be in the FUTURE (today is 2026-08), which is the mistake
#     the Vue track made on its first publish — it shipped 2026-09-01
# check_content.py enforces the first and warns on the second.
START_DATE = datetime(2024, 5, 6, 9, 0, 0)
STEP_DAYS = 5


def _date(index: int) -> str:
    """The publish timestamp for the index-th lesson, 0-based."""
    return (START_DATE + timedelta(days=STEP_DAYS * index)).strftime("%Y-%m-%dT%H:%M:%S")


# Authored in reading order. `source` is documentation, not data: it records
# which part of the demo app the lesson's schema and queries come from, so a
# reviewer can check a lesson against the code without reading the whole app.
#
# `new: True` marks a post that does not exist on the live site. Everything else
# is a rewrite of an indexed URL and its slug is frozen.
_TRACK = [
    # ----------------------------------------------------------- getting started
    {
        "slug": "mysql-introduction",
        "new": True,
        "part": "Getting started",
        "title": "MySQL – Get Started",
        "tags": ["mysql", "sql", "database"],
        "source": "the track index; the versions table; docker-compose.yml",
        "excerpt": (
            "Start here. What MySQL is and where it fits against Postgres and SQLite, why 8.4 is "
            "the version to learn and what LTS means for it, InnoDB and why the storage engine "
            "is a choice you no longer have to make, the pizza-ordering database every query in "
            "this track runs against, and the full lesson index in reading order."
        ),
    },
    {
        "slug": "mysql-install",
        "new": True,
        "title": "MySQL – Install and Connect",
        "tags": ["mysql", "docker", "sql"],
        "source": "docker-compose.yml (mysql service), application-local.properties",
        "excerpt": (
            "Getting a server you can type into. One `docker compose up -d` for a throwaway "
            "MySQL 8.4, why the demo publishes 3308 instead of 3306, installing the client on "
            "macOS, Linux and Windows, connecting with `mysql` and with a GUI, the healthcheck "
            "that stops your app racing the database, and loading the pizza schema so the rest "
            "of the track has something to query."
        ),
    },
    {
        "slug": "mysql-connection",
        "title": "MySQL – Connections, URLs and Pooling",
        "tags": ["mysql", "spring-boot", "sql"],
        "source": "application.properties, application-local.properties, HikariCP defaults",
        "excerpt": (
            "How an application actually talks to MySQL. Reading a JDBC URL parameter by "
            "parameter, why `serverTimezone` and `allowPublicKeyRetrieval` exist and when you "
            "need them, connection pooling with HikariCP and how to size a pool, `wait_timeout` "
            "and the stale-connection errors it causes overnight, and `max_connections` — the "
            "limit you meet on a bad day rather than a good one."
        ),
    },

    # -------------------------------------------------------- schema and types
    {
        "slug": "mysql-data-types",
        "new": True,
        "part": "Designing a schema",
        "title": "MySQL – Data Types",
        "tags": ["mysql", "sql", "database"],
        "source": "001-schema.sql — product, customer_order, order_item",
        "excerpt": (
            "Picking the right column type, and the two that cost real money to get wrong. "
            "INT versus BIGINT and what AUTO_INCREMENT actually runs out of, why every price "
            "column in the pizza schema is DECIMAL(10,2) and never FLOAT, VARCHAR versus CHAR "
            "and what the length really limits, TEXT and BLOB, ENUM and why the schema uses "
            "VARCHAR instead, BOOLEAN being TINYINT(1) in disguise, and utf8mb4 — the reason "
            "MySQL's own `utf8` cannot store an emoji."
        ),
    },
    {
        "slug": "sql-date-types",
        "title": "MySQL – Date and Time Types",
        "tags": ["mysql", "sql", "date"],
        "source": "001-schema.sql (DATETIME(6) columns), 005-add-audit-timestamps.sql",
        "excerpt": (
            "DATE, TIME, DATETIME, TIMESTAMP and YEAR, and the one difference that matters: "
            "TIMESTAMP converts to and from the session time zone and DATETIME does not. Why the "
            "pizza schema stores DATETIME(6), what the fractional-seconds argument buys you, the "
            "2038 problem TIMESTAMP still has, DEFAULT CURRENT_TIMESTAMP and ON UPDATE, and how "
            "to store an instant so it survives a server moving between time zones."
        ),
    },
    {
        "slug": "mysql-create-table",
        "new": True,
        "title": "MySQL – CREATE TABLE, Constraints and ALTER",
        "tags": ["mysql", "sql", "ddl"],
        "source": "001-schema.sql in full; 004/005/006 ALTER migrations",
        "excerpt": (
            "Writing the schema. CREATE TABLE column by column, PRIMARY KEY and why the pizza "
            "tables use a surrogate BIGINT, NOT NULL and DEFAULT, UNIQUE constraints and what "
            "they buy that application code cannot, FOREIGN KEY with ON DELETE CASCADE versus "
            "SET NULL — a choice the order tables make both ways on purpose — CHECK constraints, "
            "AUTO_INCREMENT, and ALTER TABLE on a table that already has rows in it."
        ),
    },
    {
        "slug": "mysql-normalization",
        "new": True,
        "title": "MySQL – Normalization and Schema Design",
        "tags": ["mysql", "sql", "database", "design"],
        "source": "the whole pizza schema — product/product_size, order_item snapshots, cart",
        "excerpt": (
            "Why the pizza schema looks the way it does. First, second and third normal form "
            "explained on tables you can see rather than on students and courses, why price "
            "lives in `product_size` and not in `product`, the one place the schema "
            "deliberately denormalizes — `order_item` snapshots the product name and price so "
            "editing the menu cannot rewrite what someone already bought — and why `cart` does "
            "the opposite and stores no prices at all."
        ),
    },

    # ------------------------------------------------------------ reading data
    {
        "slug": "sql-select",
        "part": "Reading data",
        "title": "MySQL – SELECT",
        "tags": ["mysql", "sql", "select"],
        "source": "product, product_size — 14 products, 42 size rows",
        "excerpt": (
            "The statement you will write more than all the others combined. Choosing columns "
            "instead of SELECT *, and why the star is a habit worth losing, column and table "
            "aliases, DISTINCT, expressions and arithmetic in the select list, the order MySQL "
            "actually evaluates a query in — which is not the order you type it — and why that "
            "explains half the errors beginners hit."
        ),
    },
    {
        "slug": "sql-where",
        "title": "MySQL – WHERE",
        "tags": ["mysql", "sql", "where"],
        "source": "product, customer_order",
        "excerpt": (
            "Filtering rows. Comparison operators, AND / OR / NOT and the precedence rule that "
            "makes parentheses worth typing, IN and NOT IN, filtering on a boolean column, and "
            "the trap that silently returns nothing: comparing to NULL with `=` instead of "
            "IS NULL. Also why wrapping a column in a function in the WHERE clause quietly "
            "disables the index on it."
        ),
    },
    {
        "slug": "sql-isnull",
        "title": "MySQL – NULL, IS NULL and ISNULL()",
        "tags": ["mysql", "sql", "null"],
        "source": "customer_order.user_id (NULL for guest orders), order_item.product_id",
        "excerpt": (
            "NULL is not a value, it is the absence of one, and every surprising thing about it "
            "follows from that. IS NULL and IS NOT NULL, the ISNULL() function, IFNULL() and "
            "COALESCE(), why `= NULL` is always false, how NULL behaves in aggregates and in "
            "GROUP BY, and the nullable column the pizza schema uses on purpose — `user_id` is "
            "NULL exactly when the order was placed by a guest."
        ),
    },
    {
        "slug": "sql-between",
        "title": "MySQL – BETWEEN",
        "tags": ["mysql", "sql", "where"],
        "source": "product_size.price, customer_order.created_at",
        "excerpt": (
            "BETWEEN as shorthand for two comparisons, and the two things that catch people out: "
            "it is inclusive at both ends, and on a DATETIME column `BETWEEN '2024-01-01' AND "
            "'2024-01-31'` silently drops almost the whole of the 31st. NOT BETWEEN, BETWEEN on "
            "strings, and the half-open `>= ... < ...` form that is the right answer for dates."
        ),
    },
    {
        "slug": "sql-like",
        "title": "MySQL – LIKE and Pattern Matching",
        "tags": ["mysql", "sql", "where"],
        "source": "product.name, product.description, app_user.email",
        "excerpt": (
            "Matching text patterns. The `%` and `_` wildcards, ESCAPE for matching a literal "
            "percent sign, why LIKE is case-insensitive here and what the column's collation has "
            "to do with it, NOT LIKE, REGEXP when LIKE is not enough, and the performance rule "
            "worth remembering: `LIKE 'Pep%'` can use an index and `LIKE '%roni'` cannot."
        ),
    },
    {
        "slug": "sql-order-by",
        "title": "MySQL – ORDER BY",
        "tags": ["mysql", "sql", "order-by"],
        "source": "product.display_order, product_size.price, customer_order.created_at",
        "excerpt": (
            "Sorting results. ASC and DESC, sorting by several columns, sorting by an expression "
            "or an alias, where NULLs land in MySQL and how to force them to the other end, "
            "sorting by a column you did not select, and why a query without ORDER BY has no "
            "guaranteed order at all — even when it looks sorted every time you run it."
        ),
    },
    {
        "slug": "sql-limit",
        "title": "MySQL – LIMIT and Pagination",
        "tags": ["mysql", "sql", "pagination"],
        "source": "customer_order — paging the admin order list",
        "excerpt": (
            "LIMIT, LIMIT with OFFSET, and why LIMIT without ORDER BY is a bug waiting to "
            "happen. Then the part most tutorials skip: OFFSET pagination gets slower the deeper "
            "you page, because the server still has to walk and discard every row it skips — "
            "and what keyset (seek) pagination does instead."
        ),
    },
    {
        "slug": "sql-if",
        "title": "MySQL – IF, CASE and Conditional Expressions",
        "tags": ["mysql", "sql", "functions"],
        "source": "customer_order.status / order_type, delivery_fee",
        "excerpt": (
            "Branching inside a query. IF() for the two-way case, CASE WHEN for everything else, "
            "IFNULL() and NULLIF(), COALESCE() for the first non-NULL of several, and the "
            "pattern that makes CASE genuinely useful — conditional aggregation, counting "
            "completed and cancelled orders in a single pass instead of running two queries."
        ),
    },

    # ------------------------------------------------------------------- joins
    {
        "slug": "sql-join-or-inner-join",
        "part": "Joins",
        "title": "MySQL – INNER JOIN",
        "tags": ["mysql", "sql", "join"],
        "source": "product JOIN product_size; customer_order JOIN order_item",
        "excerpt": (
            "Reading columns from two tables in one result. The ON clause and how a join is "
            "evaluated, why INNER JOIN and JOIN are the same thing, joining more than two "
            "tables — order to item to topping is three deep in the pizza schema — table "
            "aliases, joining on something other than a foreign key, and why a missing ON "
            "clause silently gives you every row times every row."
        ),
    },
    {
        "slug": "sql-left-join",
        "title": "MySQL – LEFT JOIN",
        "tags": ["mysql", "sql", "join"],
        "source": "customer_order LEFT JOIN app_user (guest orders have no user)",
        "excerpt": (
            "Keeping every row on the left whether or not the right side matches. Where the "
            "NULLs come from, the guest-order case the pizza schema is built around, finding "
            "rows with NO match using `WHERE right.id IS NULL`, and the single most common "
            "LEFT JOIN mistake: putting a condition on the right-hand table in WHERE instead of "
            "ON, which turns the whole thing back into an INNER JOIN."
        ),
    },
    {
        "slug": "sql-right-join",
        "title": "MySQL – RIGHT JOIN",
        "tags": ["mysql", "sql", "join"],
        "source": "app_user RIGHT JOIN customer_order",
        "excerpt": (
            "RIGHT JOIN is LEFT JOIN with the tables the other way round, and that is very "
            "nearly the whole lesson. What it does, the identical query written both ways, why "
            "you will almost never see one in a real codebase, and the one honest argument for "
            "it — a long chain of joins where flipping the order would mean rewriting every "
            "line."
        ),
    },
    {
        "slug": "sql-cross-join",
        "title": "MySQL – CROSS JOIN",
        "tags": ["mysql", "sql", "join"],
        "source": "product CROSS JOIN sizes — generating the full menu grid",
        "excerpt": (
            "Every row on the left paired with every row on the right. The Cartesian product, "
            "how CROSS JOIN differs from a comma join with no WHERE (it does not), the row count "
            "arithmetic that makes an accidental one so expensive, and the case where you "
            "actually want it: generating a complete grid — every product against every size — "
            "to find the combinations that are missing."
        ),
    },
    {
        "slug": "sql-self-join",
        "title": "MySQL – Self Join",
        "tags": ["mysql", "sql", "join"],
        "source": "order_item paired with itself; app_user referral-style example",
        "excerpt": (
            "Joining a table to itself, which is not a special kind of join — it is an ordinary "
            "join where both aliases point at the same table. Why the aliases stop being "
            "optional, comparing rows within a table, finding pairs without duplicating them "
            "with `a.id < b.id`, and the classic employee-and-manager shape done on a table you "
            "can actually see."
        ),
    },
    {
        "slug": "mysql-union",
        "new": True,
        "title": "MySQL – UNION and UNION ALL",
        "tags": ["mysql", "sql", "union"],
        "source": "customer_order — registered and guest email addresses in one list",
        "excerpt": (
            "Stacking result sets on top of each other instead of side by side. UNION versus "
            "UNION ALL and why the default deduplication is not free, the rules the branches "
            "have to satisfy, where ORDER BY and LIMIT go when there is more than one SELECT, "
            "MySQL 8's INTERSECT and EXCEPT, and when a UNION is the wrong tool and a "
            "conditional aggregate is the right one."
        ),
    },

    # ---------------------------------------------------- aggregating and more
    {
        "slug": "sql-group-by-having",
        "part": "Aggregation and advanced queries",
        "title": "MySQL – GROUP BY and HAVING",
        "tags": ["mysql", "sql", "group-by"],
        "source": "customer_order by status; order_item by product",
        "excerpt": (
            "Collapsing many rows into one per group. COUNT, SUM, AVG, MIN and MAX, grouping by "
            "several columns, HAVING versus WHERE and why they are not interchangeable, counting "
            "with COUNT(*) versus COUNT(column) when NULLs are involved, WITH ROLLUP for "
            "subtotals, and ONLY_FULL_GROUP_BY — the mode that is ON by default in MySQL 8 and "
            "rejects the sloppy GROUP BY that MySQL 5 quietly accepted."
        ),
    },
    {
        "slug": "sql-sub-query",
        "title": "MySQL – Subqueries",
        "tags": ["mysql", "sql", "subquery"],
        "source": "product_size, customer_order, order_item",
        "excerpt": (
            "A query inside a query. Scalar subqueries in the select list, subqueries in WHERE "
            "with IN, EXISTS and the comparison operators, derived tables in FROM and why they "
            "need an alias, correlated subqueries and why they are the expensive kind, the "
            "NOT IN trap that returns nothing at all when the inner query yields a NULL, and "
            "when to reach for a join instead."
        ),
    },
    {
        "slug": "mysql-cte",
        "new": True,
        "title": "MySQL – Common Table Expressions (WITH)",
        "tags": ["mysql", "sql", "cte"],
        "source": "customer_order revenue rollups; a recursive date series",
        "excerpt": (
            "WITH, added in MySQL 8, and the reason a long query stops being unreadable. A CTE "
            "versus a derived table versus a view, chaining several CTEs so each step is named, "
            "referencing one twice, and RECURSIVE — walking a parent-child tree and generating "
            "a gap-free date series to report on days that had no orders at all."
        ),
    },
    {
        "slug": "mysql-window-functions",
        "new": True,
        "title": "MySQL – Window Functions",
        "tags": ["mysql", "sql", "window-functions"],
        "source": "customer_order — running revenue totals, per-customer ranking",
        "excerpt": (
            "Aggregating without collapsing the rows. OVER (PARTITION BY ... ORDER BY ...), "
            "ROW_NUMBER, RANK and DENSE_RANK and the difference ties make, LAG and LEAD for "
            "comparing a row to the one before it, running totals with a frame clause, "
            "NTILE, and the top-N-per-group problem — which is genuinely awkward without window "
            "functions and three lines with them."
        ),
    },

    # ------------------------------------------------------------ writing data
    {
        "slug": "sql-insert",
        "part": "Writing data",
        "title": "MySQL – INSERT",
        "tags": ["mysql", "sql", "insert"],
        "source": "002-seed-menu.sql, 003-seed-orders.sql",
        "excerpt": (
            "Putting rows in. Single-row and multi-row INSERT and why the multi-row form is "
            "dramatically faster, INSERT ... SELECT, leaving AUTO_INCREMENT and DEFAULT columns "
            "out, INSERT IGNORE and what it actually swallows, ON DUPLICATE KEY UPDATE for an "
            "upsert, REPLACE and why it is usually the wrong one, and LOAD DATA for a bulk load."
        ),
    },
    {
        "slug": "sql-update",
        "title": "MySQL – UPDATE",
        "tags": ["mysql", "sql", "update"],
        "source": "005-add-audit-timestamps.sql backfills; order status transitions",
        "excerpt": (
            "Changing rows that already exist. UPDATE with WHERE and the habit that saves you — "
            "run it as a SELECT first, UPDATE with a JOIN for a backfill, updating from a "
            "subquery, ORDER BY and LIMIT on an UPDATE to work through a large table in "
            "batches, and `sql_safe_updates`, the setting that refuses an UPDATE with no WHERE "
            "clause before it becomes an incident."
        ),
    },
    {
        "slug": "sql-delete",
        "title": "MySQL – DELETE",
        "tags": ["mysql", "sql", "delete"],
        "source": "006-add-soft-delete.sql; ON DELETE CASCADE in 001-schema.sql",
        "excerpt": (
            "Removing rows, and the several ways to regret it. DELETE with WHERE, DELETE with a "
            "JOIN, deleting in batches so a big cleanup does not hold one enormous transaction, "
            "TRUNCATE versus DELETE and what each does to AUTO_INCREMENT, what ON DELETE CASCADE "
            "takes with it, and soft delete — the `deleted` flag the pizza schema uses so a "
            "historical order never loses the product it referenced."
        ),
    },
    {
        "slug": "sql-last_insert_id",
        "title": "MySQL – LAST_INSERT_ID",
        "tags": ["mysql", "sql", "insert"],
        "source": "order creation — customer_order then order_item then order_item_topping",
        "excerpt": (
            "Getting the AUTO_INCREMENT id of the row you just inserted, which is exactly what "
            "you need when saving an order and then its line items. Why LAST_INSERT_ID() is "
            "per-connection and therefore safe under concurrency, what it returns after a "
            "multi-row INSERT, why it does not see a trigger's own inserts, and how JDBC's "
            "`getGeneratedKeys` exposes the same thing to Java."
        ),
    },

    # --------------------------------------------------------------- functions
    {
        "slug": "mysql-functions",
        "part": "Functions and searching",
        "title": "MySQL – Built-in Functions",
        "tags": ["mysql", "sql", "functions"],
        "source": "product.name, customer_order totals, app_user.email",
        "excerpt": (
            "The functions you reach for weekly. String work with CONCAT, CONCAT_WS, SUBSTRING, "
            "TRIM, REPLACE, UPPER and LOWER, LPAD — the one the schema uses to backfill UUIDs — "
            "numbers with ROUND, CEIL, FLOOR, ABS and MOD, why ROUND on a DECIMAL and on a FLOAT "
            "do not agree, GROUP_CONCAT for rolling a group into one string, and UUID() and "
            "RAND()."
        ),
    },
    {
        "slug": "sql-date_format",
        "title": "MySQL – DATE_FORMAT and Date Functions",
        "tags": ["mysql", "sql", "date"],
        "source": "customer_order.created_at — grouping revenue by day and month",
        "excerpt": (
            "Formatting and calculating with dates. DATE_FORMAT and the specifier table you will "
            "keep coming back to, NOW() versus CURDATE() versus SYSDATE(), DATE_ADD and "
            "DATE_SUB, DATEDIFF and TIMESTAMPDIFF, EXTRACT, LAST_DAY, STR_TO_DATE for parsing, "
            "and why grouping by DATE_FORMAT(created_at, '%Y-%m') is convenient and quietly "
            "prevents the index on created_at from being used."
        ),
    },
    {
        "slug": "mysql-server-helpful-functions",
        "title": "MySQL – Server and Session Functions",
        "tags": ["mysql", "sql", "functions"],
        "source": "the running 8.4.11 container",
        "excerpt": (
            "The small functions that tell you where you are and what you are connected to. "
            "VERSION(), DATABASE(), USER() and CURRENT_USER() and why they differ, "
            "CONNECTION_ID(), @@variables for session and global settings, SHOW STATUS and SHOW "
            "VARIABLES, BENCHMARK() for a crude timing, and SLEEP() — useful for reproducing a "
            "lock wait on purpose."
        ),
    },
    {
        "slug": "mysql-json",
        "title": "MySQL – JSON Columns",
        "tags": ["mysql", "sql", "json"],
        "source": "a JSON options column added to order_item for this lesson",
        "excerpt": (
            "MySQL's native JSON type, which is not just a string. Storing and validating JSON, "
            "reading values with `->` and `->>`, JSON_EXTRACT, JSON_UNQUOTE, JSON_SET, "
            "JSON_ARRAY and JSON_OBJECT, JSON_TABLE for turning a document into rows, indexing "
            "a JSON path with a generated column — the only way to index one — and the question "
            "worth asking first: should this be a column instead?"
        ),
    },
    {
        "slug": "mysql-full-text-search",
        "title": "MySQL – Full-Text Search",
        "tags": ["mysql", "sql", "search"],
        "source": "product.name + product.description — searching the menu",
        "excerpt": (
            "Searching text properly instead of with `LIKE '%...%'`. Creating a FULLTEXT index, "
            "MATCH ... AGAINST in natural language mode, boolean mode with `+`, `-` and `*`, "
            "relevance scores and ordering by them, the default minimum word length and stopword "
            "list that make short searches return nothing, and where full-text search stops "
            "being enough and Elasticsearch starts."
        ),
    },

    # ------------------------------------------------------------- performance
    {
        "slug": "mysql-index",
        "part": "Performance",
        "title": "MySQL – Indexes",
        "tags": ["mysql", "sql", "index", "performance"],
        "source": "001-schema.sql indexes; measured on pizza_lab at 400,000 orders",
        "excerpt": (
            "The single biggest lever on query speed. What a B-tree index is and what it costs "
            "on every write, the clustered primary key and why a secondary index lookup is two "
            "lookups, composite indexes and the leftmost-prefix rule that decides whether yours "
            "gets used, covering indexes, why an index on a low-cardinality column is often "
            "ignored, and the four common ways to write a query that cannot use the index you "
            "just added."
        ),
    },
    {
        "slug": "sql-explain",
        "title": "MySQL – EXPLAIN and Reading a Query Plan",
        "tags": ["mysql", "sql", "explain", "performance"],
        "source": "measured on pizza_lab at 400,000 orders",
        "excerpt": (
            "Finding out what the optimizer decided instead of guessing. Reading EXPLAIN column "
            "by column, what the `type` values mean from `ALL` to `const` and which ones should "
            "worry you, `key` and `rows` and how rough the estimate is, EXPLAIN ANALYZE for "
            "actual timings rather than predictions, EXPLAIN FORMAT=JSON, and a worked example "
            "taking one slow query from a full scan to an index lookup."
        ),
    },
    {
        "slug": "mysql-closure-table",
        "title": "MySQL – Storing Hierarchies with a Closure Table",
        "tags": ["mysql", "sql", "design"],
        "source": "a menu-category tree modelled three ways",
        "excerpt": (
            "Trees in a relational database. The adjacency list everyone starts with and the "
            "query that makes it painful, MySQL 8's recursive CTE which fixes most of that, and "
            "the closure table — one row per ancestor-descendant pair — which trades write cost "
            "and storage for subtree reads that are a single indexed lookup. When each one is "
            "the right answer, with the numbers."
        ),
    },

    # --------------------------------------------------- transactions and locks
    {
        "slug": "mysql-transaction",
        "part": "Transactions and concurrency",
        "title": "MySQL – Transactions",
        "tags": ["mysql", "sql", "transaction"],
        "source": "checkout — customer_order + order_item + order_item_topping in one unit",
        "excerpt": (
            "Making several statements succeed or fail together. START TRANSACTION, COMMIT and "
            "ROLLBACK, autocommit and why it is on by default, savepoints, the four isolation "
            "levels and what each one lets through, why MySQL's default is REPEATABLE READ when "
            "most databases use READ COMMITTED, SELECT ... FOR UPDATE, and the DDL statement "
            "that silently commits your transaction out from under you."
        ),
    },
    {
        "slug": "mysql-deadlock",
        "title": "MySQL – Deadlocks",
        "tags": ["mysql", "sql", "transaction", "innodb"],
        "source": "two sessions against customer_order, reproduced on purpose",
        "excerpt": (
            "Two transactions each waiting for a lock the other holds. Reproducing one in two "
            "terminals so you can see it happen, reading SHOW ENGINE INNODB STATUS to find out "
            "which statements were involved, the difference between a deadlock and a lock wait "
            "timeout, gap locks and why REPEATABLE READ produces deadlocks READ COMMITTED does "
            "not, and the two fixes that actually work: consistent lock ordering, and retrying."
        ),
    },

    # ----------------------------------------------------- server-side objects
    {
        "slug": "mysql-view",
        "part": "Server-side objects",
        "title": "MySQL – Views",
        "tags": ["mysql", "sql", "view"],
        "source": "an order-summary view over customer_order + order_item",
        "excerpt": (
            "Naming a query so the rest of the schema can use it. CREATE VIEW and CREATE OR "
            "REPLACE VIEW, what a view costs at query time, MERGE versus TEMPTABLE and why the "
            "second one loses your indexes, updatable views and the conditions they have to "
            "meet, WITH CHECK OPTION, using a view as a permission boundary, and why MySQL has "
            "no materialized views and what people do instead."
        ),
    },
    {
        "slug": "mysql-stored-procedure",
        "title": "MySQL – Stored Procedures and Functions",
        "tags": ["mysql", "sql", "stored-procedure"],
        "source": "an order-total recalculation procedure over the pizza tables",
        "excerpt": (
            "Code that lives in the database. DELIMITER and why you need it, CREATE PROCEDURE, "
            "IN / OUT / INOUT parameters, variables, IF and CASE, WHILE and REPEAT loops, "
            "cursors and the handler that stops one looping forever, stored functions and how "
            "they differ from procedures, error handling with DECLARE ... HANDLER, and an honest "
            "look at when to put logic here rather than in the application."
        ),
    },
    {
        "slug": "mysql-trigger",
        "title": "MySQL – Triggers",
        "tags": ["mysql", "sql", "trigger"],
        "source": "an audit trigger on customer_order.status",
        "excerpt": (
            "Running a statement automatically when a row changes. BEFORE and AFTER, INSERT, "
            "UPDATE and DELETE, the NEW and OLD rows, writing an audit trail, keeping a derived "
            "total in step, the limitations that bite — a trigger cannot touch its own table, "
            "and it does not fire for TRUNCATE — and the real argument against them: logic that "
            "runs invisibly is logic nobody debugging your application will think to look for."
        ),
    },
    {
        "slug": "mysql-event",
        "title": "MySQL – Scheduled Events",
        "tags": ["mysql", "sql", "event"],
        "source": "a nightly job clearing abandoned carts",
        "excerpt": (
            "Cron inside the database. The event_scheduler variable that is OFF by default so "
            "your first event never runs, CREATE EVENT with AT and with EVERY, STARTS and ENDS, "
            "ON COMPLETION PRESERVE, altering and disabling one, where errors go, what happens "
            "on a replica, and the question to settle first — whether this belongs in the "
            "database at all or in the scheduler you already operate."
        ),
    },

    # ------------------------------------------------------------- production
    {
        "slug": "mysql-information-schema",
        "part": "Running MySQL in production",
        "title": "MySQL – INFORMATION_SCHEMA",
        "tags": ["mysql", "sql", "administration"],
        "source": "the pizza database's own catalog",
        "excerpt": (
            "Querying the database about itself. TABLES, COLUMNS, STATISTICS, KEY_COLUMN_USAGE "
            "and REFERENTIAL_CONSTRAINTS, finding every foreign key pointing at a table before "
            "you drop it, listing indexes that duplicate each other, estimating table and index "
            "size on disk, why TABLE_ROWS is an estimate and not a count, and how SHOW commands "
            "map onto the same data."
        ),
    },
    {
        "slug": "mysql-users-and-privileges",
        "new": True,
        "title": "MySQL – Users, Privileges and Roles",
        "tags": ["mysql", "security", "administration"],
        "source": "the application account the pizza API should connect as",
        "excerpt": (
            "Not connecting as root. CREATE USER and why `'app'@'%'` and `'app'@'localhost'` are "
            "two different accounts, GRANT at the database, table and column level, the "
            "principle of least privilege applied to an application account, REVOKE, roles in "
            "MySQL 8 and why they need activating, `mysql_native_password` versus "
            "`caching_sha2_password`, and reading SHOW GRANTS to audit what an account can do."
        ),
    },
    {
        "slug": "mysql-reset-root-password",
        "title": "MySQL – Reset the Root Password",
        "tags": ["mysql", "administration"],
        "source": "the mysql:8.4 container and a package-installed server",
        "excerpt": (
            "Locked out of your own server. The `--skip-grant-tables` procedure step by step on "
            "MySQL 8, why FLUSH PRIVILEGES is required before ALTER USER will work in that mode, "
            "the `--init-file` alternative that avoids opening the server up at all, doing it in "
            "a Docker container where the answer is usually simpler, and the check to run "
            "afterwards to confirm you did not leave the server unauthenticated."
        ),
    },
    {
        "slug": "mysql-dump",
        "title": "MySQL – Backup and Restore with mysqldump",
        "tags": ["mysql", "backup", "administration"],
        "source": "the pizza database, dumped and restored",
        "excerpt": (
            "Taking a backup you can actually restore from. mysqldump for one database, several, "
            "or all, --single-transaction and why omitting it locks your tables, schema-only and "
            "data-only dumps, --routines and --events which are NOT included by default, "
            "restoring, why a dump is a logical backup and what that costs at size, and the only "
            "test that matters — restoring it somewhere and looking."
        ),
    },
    {
        "slug": "mysql-binlog",
        "title": "MySQL – The Binary Log",
        "tags": ["mysql", "administration", "replication"],
        "source": "binlog on the 8.4 container",
        "excerpt": (
            "The log that makes replication and point-in-time recovery possible. What the binlog "
            "records and what it does not, ROW versus STATEMENT versus MIXED format and why ROW "
            "is the default now, reading one with mysqlbinlog, finding the statement that "
            "deleted the rows, replaying up to a position or a timestamp to recover, "
            "expire_logs_days and the disk it fills if you forget."
        ),
    },
    {
        "slug": "mysql-replication",
        "new": True,
        "title": "MySQL – Replication",
        "tags": ["mysql", "replication", "administration"],
        "source": "a two-container primary/replica pair",
        "excerpt": (
            "Running a second copy of the database. Asynchronous replication and what it costs "
            "you, setting up a primary and a replica with GTIDs from scratch, reading SHOW "
            "REPLICA STATUS and the one field that tells you it is behind, replication lag and "
            "the read-after-write bug it causes in an application, semi-synchronous replication, "
            "and read/write splitting — plus when a replica is not a backup."
        ),
    },
    {
        "slug": "mysql-run-query-in-production",
        "title": "MySQL – Running Queries in Production Safely",
        "tags": ["mysql", "administration", "performance"],
        "source": "pizza_lab — the same queries at 400,000 orders",
        "excerpt": (
            "The habits that keep an ad-hoc query from becoming an incident. Reading before "
            "writing, wrapping a change in a transaction you can roll back, sql_safe_updates, "
            "always EXPLAIN before running something new against a big table, deleting and "
            "updating in batches, MAX_EXECUTION_TIME, finding and killing a runaway query with "
            "SHOW PROCESSLIST, the slow query log, and why a long ALTER TABLE needs a plan."
        ),
    },

    # --------------------------------------------------------------- interview
    {
        "slug": "sql-interview-fundamentals",
        "part": "Interview preparation",
        "title": "MySQL Interview – Fundamentals",
        "tags": ["mysql", "sql", "interview"],
        "source": "the whole track",
        "excerpt": (
            "The questions almost every SQL interview asks, answered the way you would say them "
            "out loud. The difference between the joins, WHERE versus HAVING, DELETE versus "
            "TRUNCATE versus DROP, what an index actually is and its cost, primary versus unique "
            "key, NULL behaviour, the ACID properties with an example each, normalization up to "
            "third normal form, and UNION versus UNION ALL."
        ),
    },
    {
        "slug": "mysql-interview-advanced-queries",
        "title": "MySQL Interview – Advanced Queries",
        "tags": ["mysql", "sql", "interview"],
        "source": "the pizza and pizza_lab databases",
        "excerpt": (
            "The whiteboard questions that separate people who have written SQL from people who "
            "have read about it. Second-highest value, top N per group, finding and deleting "
            "duplicates, a running total, gaps in a sequence, a pivot with conditional "
            "aggregation, rows in one table with no match in another, and month-over-month "
            "growth — each one solved, then explained, then checked against a real database."
        ),
    },
]

# `part` is written on the first lesson of each section only; carry it forward so
# every entry has one. The lesson index in lesson 1 is GENERATED from this
# grouping (gen_index.py) rather than hand-maintained, because a hand-written
# index of 52 links drifts the first time a lesson is inserted.
_part = None
for _entry in _TRACK:
    _part = _entry.get("part", _part)
    _entry["part"] = _part

# Slug -> filename, and the dates, are derived so a reorder is one edit.
POSTS = [
    {
        "slug": entry["slug"],
        "title": entry["title"],
        "file": f"{i + 1:02d}-{entry['slug']}.html",
        "date": _date(i),
        "tags": entry["tags"],
        "excerpt": entry["excerpt"],
        "source": entry["source"],
        "part": entry["part"],
        "new": entry.get("new", False),
    }
    for i, entry in enumerate(_TRACK)
]

# ⚠️ EVERY SLUG IN HERE IS A LIVE, INDEXED URL on lovemesomecoding.com/sql,
# published between 2018-09-29 and 2021-09-13. Renaming or dropping one is a 404
# on a page that has ranked for years, and `verify-build.mjs` fails the frontend
# build for it.
#
# This list is the state of /sql BEFORE this track — read off
# index/by-category/sql.json on 2026-08-24, not typed from memory.
# check_content.py asserts every one of them is still in POSTS.
FROZEN_SLUGS: set[str] = {
    "mysql-binlog",
    "mysql-closure-table",
    "mysql-connection",
    "mysql-deadlock",
    "mysql-dump",
    "mysql-event",
    "mysql-full-text-search",
    "mysql-functions",
    "mysql-index",
    "mysql-information-schema",
    "mysql-interview-advanced-queries",
    "mysql-json",
    "mysql-reset-root-password",
    "mysql-run-query-in-production",
    "mysql-server-helpful-functions",
    "mysql-stored-procedure",
    "mysql-transaction",
    "mysql-trigger",
    "mysql-view",
    "sql-between",
    "sql-cross-join",
    "sql-date-types",
    "sql-date_format",
    "sql-delete",
    "sql-explain",
    "sql-group-by-having",
    "sql-if",
    "sql-insert",
    "sql-interview-fundamentals",
    "sql-isnull",
    "sql-join-or-inner-join",
    "sql-last_insert_id",
    "sql-left-join",
    "sql-like",
    "sql-limit",
    "sql-order-by",
    "sql-right-join",
    "sql-select",
    "sql-self-join",
    "sql-sub-query",
    "sql-update",
    "sql-where",
}


# ---------------------------------------------------------------- track rules
#
# The reading-time budget. ⚠️ The pipeline counts PROSE AND CODE together, so
# this is a cap on the total, not on the writing.
#
# The floor is 4 rather than the Postgres track's 6 because this track was told
# to "keep posts to the point", and it inherited genuinely small topics —
# `sql-isnull` and `sql-between` are one idea each. Padding them to six minutes
# to satisfy a checker is the failure mode, not the fix.
TARGET_MINUTES = (4, 9)

# The two interview posts are reference pages people scroll rather than lessons
# they read start to finish, so they get a wider band.
LONG_POSTS = {"sql-interview-fundamentals", "mysql-interview-advanced-queries"}
TARGET_MINUTES_LONG = (6, 15)

# Posts that are ONE IDEA and are allowed to be short.
#
# These exist because the track inherited them — `/sql/sql-between` and
# `/sql/sql-cross-join` are indexed URLs, so they stay as their own pages even
# though a from-scratch track would have folded them into WHERE and JOIN. See
# the decision recorded in progress_report.md.
#
# The README's instruction is "keep content to the point and not too lengthy if
# they don't have to" be. Padding BETWEEN to six minutes to satisfy a checker is
# the failure mode this list prevents — but it is a NAMED list rather than a
# lower global floor, so a genuinely thin post on a big topic is still caught.
SHORT_POSTS = {
    "sql-between",
    "sql-like",
    "sql-limit",
    "sql-if",
    "sql-cross-join",
    "sql-self-join",
    "sql-right-join",
    "sql-last_insert_id",
    "mysql-server-helpful-functions",
    "mysql-reset-root-password",
}
TARGET_MINUTES_SHORT = (3, 6)

# Prose has to be at least this share of the words. SQL is the easiest language
# in the world to fill a word budget with — paste a longer query — and the result
# is a listing with captions rather than a lesson.
MIN_PROSE_SHARE = 0.40

# What is on the live site TODAY, per slug: (prose, code, total, readingMinutes).
#
# MEASURED off the 42 post objects in the prod tree on 2026-08-24 using the
# pipeline's own wordCount, not estimated. check_content.py prints the before and
# after so the size of the rewrite is visible, and asserts this agrees with
# FROZEN_SLUGS.
#
# ⚠️ Note the two extremes, because they pull in OPPOSITE directions:
#   * `mysql-transaction` and `mysql-binlog` are 0 words — a title and an excerpt
#     with no body at all.
#   * `sql-interview-fundamentals` is 5,944 words / 27 minutes and has to SHRINK.
# This is why there is no "a rewrite must grow" rule here the way the Postgres
# track has one. The reading-minute band is the check, in both directions.
EXISTING = {
    'mysql-binlog'                        : (    0,    0,     0,  1),
    'mysql-closure-table'                 : (  451,  306,   757,  3),
    'mysql-connection'                    : (  123,    3,   126,  1),
    'mysql-deadlock'                      : (  475,    5,   480,  2),
    'mysql-dump'                          : (  687,  247,   934,  4),
    'mysql-event'                         : (  279,  157,   436,  2),
    'mysql-full-text-search'              : (  408,   52,   460,  2),
    'mysql-functions'                     : (  383,   31,   414,  2),
    'mysql-index'                         : (  306,   87,   393,  2),
    'mysql-information-schema'            : (  319,  229,   548,  2),
    'mysql-interview-advanced-queries'    : (  478,  445,   923,  4),
    'mysql-json'                          : (  421,  173,   594,  3),
    'mysql-reset-root-password'           : (  129,   54,   183,  1),
    'mysql-run-query-in-production'       : (  504,   21,   525,  2),
    'mysql-server-helpful-functions'      : (   17,   20,    37,  1),
    'mysql-stored-procedure'              : (  272,  257,   529,  2),
    'mysql-transaction'                   : (    0,    0,     0,  1),
    'mysql-trigger'                       : (  257,   95,   352,  2),
    'mysql-view'                          : (  201,   12,   213,  1),
    'sql-between'                         : (   80,    0,    80,  1),
    'sql-cross-join'                      : (   18,    7,    25,  1),
    'sql-date-types'                      : (  523,  141,   664,  3),
    'sql-date_format'                     : (  431,    0,   431,  2),
    'sql-delete'                          : (  169,   46,   215,  1),
    'sql-explain'                         : (    1,    0,     1,  1),
    'sql-group-by-having'                 : (  223,    9,   232,  1),
    'sql-if'                              : (   93,    3,    96,  1),
    'sql-insert'                          : (  306,  117,   423,  2),
    'sql-interview-fundamentals'          : ( 5481,  463,  5944, 27),
    'sql-isnull'                          : (   21,    0,    21,  1),
    'sql-join-or-inner-join'              : (  151,   14,   165,  1),
    'sql-last_insert_id'                  : (  115,   24,   139,  1),
    'sql-left-join'                       : (   83,   16,    99,  1),
    'sql-like'                            : (  188,    0,   188,  1),
    'sql-limit'                           : (  148,   21,   169,  1),
    'sql-order-by'                        : (  124,   11,   135,  1),
    'sql-right-join'                      : (   47,    9,    56,  1),
    'sql-select'                          : (  627,  130,   757,  3),
    'sql-self-join'                       : (   37,   11,    48,  1),
    'sql-sub-query'                       : (  190,   13,   203,  1),
    'sql-update'                          : (  439,  147,   586,  3),
    'sql-where'                           : (   56,    6,    62,  1),
}

# `state` is derived, not typed, so it cannot disagree with `new`.
for _entry in POSTS:
    _entry["state"] = "new" if _entry["new"] else "rewrite"


def target_minutes(slug: str) -> tuple[int, int]:
    """The reading-minute band this post is held to."""
    if slug in LONG_POSTS:
        return TARGET_MINUTES_LONG
    if slug in SHORT_POSTS:
        return TARGET_MINUTES_SHORT
    return TARGET_MINUTES

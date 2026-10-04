# Session 09-debugging

mode: `default`  cwd: `/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza`  allowed: `Bash(./mvnw:*) Bash(git log:*) Bash(git show:*) Bash(git blame:*) Bash(grep:*) Read Grep Glob`

## Prompt

```text
ReportServiceImplTest in pizza-springboot-backend is failing. This is the evidence; I don't have a theory I trust yet.

Run on 2026-10-04 (today), on branch feature/checkout-saved-cards, against the shared dev MySQL (docker container pizza-mysql, host port 3308):

  ReportServiceImplTest.softDeletedOrdersAreExcluded -- FAILURE
    expected: 19L  but was: 20L   (ReportServiceImplTest.java:94)
  ReportServiceImplTest.softDeletedOrdersLeaveTheStatusBreakdown -- FAILURE
    expected: -1L  but was: 0L    (ReportServiceImplTest.java:114)

Two hours earlier the same class had THREE failures (summaryIsInternallyConsistent also failed, 'expected > 0, got 0'). Since then, Playwright runs created ~35 new orders in that database. The same tests fail with the feature branch's commits stashed, so they predate the branch.

Find the ROOT CAUSE. Rules:
- Do not change any files and do not propose a fix until you have the root cause.
- Separate what you verified (with the command or file:line) from what you are inferring.
- Explain why the failure set changed between the two runs, and why the numbers are what they are.
- Then propose the fix you'd make, and say what it would NOT fix.
```

## Transcript

I'll start with the test itself and the code it exercises.

- **Bash** command="cd pizza-springboot-backend && find . -name 'ReportServiceImplTest.java' -o -name 'ReportDAOImp.java' -o -name 'ReportServiceImpl.java' | grep -v target"
- **Read** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/test/java/com/pizza/api/report/ReportServiceImplTest.java'
- **Read** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/main/java/com/pizza/api/report/ReportDAOImp.java'
- **Read** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/main/java/com/pizza/api/report/ReportServiceImpl.java'
- **Bash** command='docker ps --filter name=pizza-mysql --format \'{{.Names}} {{.Ports}}\'; docker exec pizza-mysql mysql -uroot -N -e "SELECT NOW(), @@global.time_zone, @@session.time_zone;" pizza 2>&1; date'
- **Grep** pattern='customer_order'
- **Read** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/main/resources/db/changelog/sql/003-seed-orders.sql'
- **Bash** command='docker exec pizza-mysql mysql -uroot -e "SELECT NOW() AS db_now, @@global.time_zone AS gtz, @@session.time_zone AS stz, @@system_time_zone AS systz;" pizza'
- **Bash** command='mysql -h127.0.0.1 -P3308 -uroot pizza -e "\nSELECT NOW() db_now, @@session.time_zone tz;\nSELECT dateexecuted, id FROM DATABASECHANGELOG WHERE id LIKE \'20%\' ORDER BY orderexecuted;\nSELECT id, status, de'
Direct DB access needs approval I don't have in this non-interactive session. So I'll verify the rest from the code: which database the test actually connects to, and how `findAll()` orders its rows.

- **Bash** command='ls src/test/resources 2>/dev/null; ls src/main/resources; grep -n "datasource\\|jpa\\|time_zone\\|timezone\\|serverTimezone" src/main/resources/application*.properties src/test/resources/*.properties 2>/d'
- **Grep** pattern='interface CustomerOrderRepository|findAll|@OrderBy|class CustomerOrder|createdAt|@SQLRestriction'
- **Bash** command='grep -n "datasource.url\\|spring.profiles\\|ddl-auto\\|liquibase" src/main/resources/application.properties src/main/resources/application-docker.properties; grep -rn "ActiveProfiles\\|TestPropertySource"'
Two things to check: `progress_report.md` already describes this, and tests don't set `@ActiveProfiles`, so I need to confirm which port the test really connects to.

- **Bash** command='sed -n 1530,1575p ../progress_report.md; echo ----; grep -n "datasource" src/main/resources/application-local.properties; echo ----; ls target/surefire-reports 2>/dev/null | grep -i report; '
There's a surefire report from the run. It records the JVM properties, so it shows which profile and port the run actually used.

- **Bash** command="cd target/surefire-reports; ls -la --time-style=full-iso TEST-com.pizza.api.report.ReportServiceImplTest.xml 2>/dev/null || stat -f '%Sm %N' TEST-com.pizza.api.report.ReportServiceImplTest.xml; grep -"
Important detail: the only JDBC URL in this report is **port 3306**, not 3308. Also, `summaryIsInternallyConsistent`'s element isn't self-closing, so it has a child element. Let me look at both.

- **Bash** command='grep -n \'jdbc:mysql\' TEST-com.pizza.api.report.ReportServiceImplTest.xml | cut -c1-300; grep -n \'profiles\' TEST-com.pizza.api.report.ReportServiceImplTest.xml | cut -c1-300; awk \'/testcase name="summa'
- **Grep** pattern='jdbc:mysql|profiles|summaryIsInternallyConsistent|HikariPool|Liquibase|system-out'
- **Grep** pattern='profile|active'
- **Bash** command='lsof -nP -iTCP:3306 -iTCP:3308 -sTCP:LISTEN'
- **Grep** pattern='image:|3306|3308|container_name'
## Root cause

The test picks its victim from **all** orders, but the report only counts the **last 30 days**. The seeded orders have aged out of that window, so the test soft-deletes an order the report never counted, and the count doesn't move.

- `ReportServiceImplTest.java:83` and `:102` pick the victim with `orderRepository.findAll().stream().filter(EARNING).findFirst()`. There is no date filter and no ordering.
- `ReportServiceImpl.java:39` limits every query to `created_at >= LocalDate.now().minusDays(29).atStartOfDay()`, which today is 2026-09-05 00:00.
- `003-seed-orders.sql:19-36` dates the seed orders with `DATE_SUB(NOW(), …)`. `NOW()` was evaluated once, when the changeset ran, so the dates are now fixed in the past.

The `deleted = 0` regression the test was written to catch is **not** the cause. All four queries have the predicate (`ReportDAOImp.java:78-79, 83, 101, 125-126, 145`).

## Verified

| Fact | Evidence |
|---|---|
| Every report query filters `deleted = 0` | `ReportDAOImp.java` lines above |
| The victim query has no date filter or ordering | `ReportServiceImplTest.java:83-86`, `:102-105` |
| The window starts at the beginning of the day 29 days ago | `ReportServiceImpl.java:39` |
| Seed dates are set when the changeset runs, then stay fixed | `003-seed-orders.sql:3-5, 19-36` |
| Seeds are dated 2026-08-04..13 and aged out; earlier this was "3 failures" | `progress_report.md:1536-1539, 1569-1571` (recorded before today) |
| **The run used port 3306, not the 3308 container** | `target/surefire-reports/TEST-…ReportServiceImplTest.xml:120` shows `jdbc:mysql://127.0.0.1:3306/pizza`; `:88` and `:140` show only `local` active, no `docker` profile. Report written 2026-10-04 11:32. |
| The tests don't choose a profile themselves | No `@ActiveProfiles` in `src/test`; `application-local.properties` has no datasource override; only `application-docker.properties:9` points at 3308 |

## The numbers, worked from the assertions

- **Test 1: expected 19, was 20.** Expected is `before − 1`, so there were 20 earning orders in the window, and still 20 after the delete.
- **Test 2: expected −1, was 0.** Expected is `before − 1`, so `before` was **0**. The victim's status had no orders at all in the window, so the victim can't be in the window.

Test 2 rules out the other explanation, that the delete was invisible to the JDBC query. If the victim were inside the window, its status count would have been at least 1 before the delete.

## Inferred (I couldn't query the database)

My `mysql` and `docker exec` commands needed approval, which this session can't grant, so I didn't confirm these against the data:

- **The victim is order id 1** (COMPLETED, the oldest seed). `findAll()` with no `ORDER BY` returns InnoDB rows in primary-key order in practice, though that isn't guaranteed.
- **The 20 orders are PAID orders from today's Playwright runs.** Playwright orders stop at PAID or PENDING_PAYMENT and never reach COMPLETED, which is why the COMPLETED count is 0. `progress_report.md` says `saved-card-checkout.spec.ts` leaves 3 PAID and 4 PENDING orders per run.
- **The Playwright backend was also on 3306.** The new orders showed up in the database the tests read, which is 3306. So the shared dev data today is on the native MySQL, not `pizza-mysql`. The container may not be in use at all.

## Why the failure set changed

- **Two hours earlier:** the window held 0 earning orders.
  - `summaryIsInternallyConsistent` failed on `isPositive()`.
  - Both soft-delete tests failed as `0 − 1`.
  - `dailyRevenueSumsToTotal` and `topProductsStayWithinItemsSold` passed only because they had nothing to check (0 == 0, empty list).
- **Now:** about 35 Playwright orders put 20 earning orders in the window.
  - The summary test passes.
  - The soft-delete tests still fail, because the victim is still the oldest seed order, outside the window.
- **Stashing the branch changes nothing,** because the cause is the calendar plus the data, not code. These tests started failing once the newest seed order was more than 30 days old, around early September.

## Proposed fix

In `ReportServiceImplTest`, have each soft-delete test **create its own earning order** inside its `@Transactional` test: status PAID, `createdAt` now, one line item. Then:

1. Assert the report counts it (`before` includes it). If the fixture ever falls outside the window again, the test fails loudly instead of quietly checking the wrong thing.
2. Delete it.
3. Assert it's gone.

Do the same for `summaryIsInternallyConsistent`, and give the two tests that currently pass on empty data a fixture so they actually check something. The rollback cleans everything up. Don't re-seed with fresh dates: a new changeset just restarts the 30-day countdown.

To confirm the inferences before I change anything, run on 3306:

```sql
SELECT id, status, created_at FROM customer_order ORDER BY id LIMIT 1;
SELECT status, COUNT(*) FROM customer_order WHERE deleted = 0 AND created_at >= '2026-09-05' GROUP BY status;
```

## What it would NOT fix

- **`admin.spec.ts`'s 2 revenue-chart failures.** Same stale seed, but in the UI. Those need seed dates relative to today, or a fixed clock.
- **`CustomerOrderDAOIntegrationTest.filtersByStatus`.** It fails on leftover Playwright orders; the specs that create them need to clean up.
- **The admin dashboard for a demo user.** It still shows almost nothing apart from leftover test orders.
- **The 3306 vs 3308 mix-up.** `./mvnw test` ignores the container unless you pass `-Dspring.profiles.active=local,docker`. Any test that depends on what's already in the database will keep seeing different data depending on which MySQL it hits.
- **Other code that relies on `findAll()` order.** I only checked this test class.

I didn't change any files.


_turns: 20, duration: 135s, cost: $0.87_

## Final answer

## Root cause

The test picks its victim from **all** orders, but the report only counts the **last 30 days**. The seeded orders have aged out of that window, so the test soft-deletes an order the report never counted, and the count doesn't move.

- `ReportServiceImplTest.java:83` and `:102` pick the victim with `orderRepository.findAll().stream().filter(EARNING).findFirst()`. There is no date filter and no ordering.
- `ReportServiceImpl.java:39` limits every query to `created_at >= LocalDate.now().minusDays(29).atStartOfDay()`, which today is 2026-09-05 00:00.
- `003-seed-orders.sql:19-36` dates the seed orders with `DATE_SUB(NOW(), …)`. `NOW()` was evaluated once, when the changeset ran, so the dates are now fixed in the past.

The `deleted = 0` regression the test was written to catch is **not** the cause. All four queries have the predicate (`ReportDAOImp.java:78-79, 83, 101, 125-126, 145`).

## Verified

| Fact | Evidence |
|---|---|
| Every report query filters `deleted = 0` | `ReportDAOImp.java` lines above |
| The victim query has no date filter or ordering | `ReportServiceImplTest.java:83-86`, `:102-105` |
| The window starts at the beginning of the day 29 days ago | `ReportServiceImpl.java:39` |
| Seed dates are set when the changeset runs, then stay fixed | `003-seed-orders.sql:3-5, 19-36` |
| Seeds are dated 2026-08-04..13 and aged out; earlier this was "3 failures" | `progress_report.md:1536-1539, 1569-1571` (recorded before today) |
| **The run used port 3306, not the 3308 container** | `target/surefire-reports/TEST-…ReportServiceImplTest.xml:120` shows `jdbc:mysql://127.0.0.1:3306/pizza`; `:88` and `:140` show only `local` active, no `docker` profile. Report written 2026-10-04 11:32. |
| The tests don't choose a profile themselves | No `@ActiveProfiles` in `src/test`; `application-local.properties` has no datasource override; only `application-docker.properties:9` points at 3308 |

## The numbers, worked from the assertions

- **Test 1: expected 19, was 20.** Expected is `before − 1`, so there were 20 earning orders in the window, and still 20 after the delete.
- **Test 2: expected −1, was 0.** Expected is `before − 1`, so `before` was **0**. The victim's status had no orders at all in the window, so the victim can't be in the window.

Test 2 rules out the other explanation, that the delete was invisible to the JDBC query. If the victim were inside the window, its status count would have been at least 1 before the delete.

## Inferred (I couldn't query the database)

My `mysql` and `docker exec` commands needed approval, which this session can't grant, so I didn't confirm these against the data:

- **The victim is order id 1** (COMPLETED, the oldest seed). `findAll()` with no `ORDER BY` returns InnoDB rows in primary-key order in practice, though that isn't guaranteed.
- **The 20 orders are PAID orders from today's Playwright runs.** Playwright orders stop at PAID or PENDING_PAYMENT and never reach COMPLETED, which is why the COMPLETED count is 0. `progress_report.md` says `saved-card-checkout.spec.ts` leaves 3 PAID and 4 PENDING orders per run.
- **The Playwright backend was also on 3306.** The new orders showed up in the database the tests read, which is 3306. So the shared dev data today is on the native MySQL, not `pizza-mysql`. The container may not be in use at all.

## Why the failure set changed

- **Two hours earlier:** the window held 0 earning orders.
  - `summaryIsInternallyConsistent` failed on `isPositive()`.
  - Both soft-delete tests failed as `0 − 1`.
  - `dailyRevenueSumsToTotal` and `topProductsStayWithinItemsSold` passed only because they had nothing to check (0 == 0, empty list).
- **Now:** about 35 Playwright orders put 20 earning orders in the window.
  - The summary test passes.
  - The soft-delete tests still fail, because the victim is still the oldest seed order, outside the window.
- **Stashing the branch changes nothing,** because the cause is the calendar plus the data, not code. These tests started failing once the newest seed order was more than 30 days old, around early September.

## Proposed fix

In `ReportServiceImplTest`, have each soft-delete test **create its own earning order** inside its `@Transactional` test: status PAID, `createdAt` now, one line item. Then:

1. Assert the report counts it (`before` includes it). If the fixture ever falls outside the window again, the test fails loudly instead of quietly checking the wrong thing.
2. Delete it.
3. Assert it's gone.

Do the same for `summaryIsInternallyConsistent`, and give the two tests that currently pass on empty data a fixture so they actually check something. The rollback cleans everything up. Don't re-seed with fresh dates: a new changeset just restarts the 30-day countdown.

To confirm the inferences before I change anything, run on 3306:

```sql
SELECT id, status, created_at FROM customer_order ORDER BY id LIMIT 1;
SELECT status, COUNT(*) FROM customer_order WHERE deleted = 0 AND created_at >= '2026-09-05' GROUP BY status;
```

## What it would NOT fix

- **`admin.spec.ts`'s 2 revenue-chart failures.** Same stale seed, but in the UI. Those need seed dates relative to today, or a fixed clock.
- **`CustomerOrderDAOIntegrationTest.filtersByStatus`.** It fails on leftover Playwright orders; the specs that create them need to clean up.
- **The admin dashboard for a demo user.** It still shows almost nothing apart from leftover test orders.
- **The 3306 vs 3308 mix-up.** `./mvnw test` ignores the container unless you pass `-Dspring.profiles.active=local,docker`. Any test that depends on what's already in the database will keep seeing different data depending on which MySQL it hits.
- **Other code that relies on `findAll()` order.** I only checked this test class.

I didn't change any files.

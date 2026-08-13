# Progress report — RDS MySQL 8.0 → 8.4 upgrade drill

**Started:** 2026-08-09
**Goal:** stand up a primary + 1 read replica on MySQL 8.0 in the personal AWS account so the
8.0 → 8.4 in-place major upgrade can be rehearsed in the console before doing it at work.

**Owner split:** Claude builds and tears down the infrastructure; Folau drives the upgrade
in the console by hand (that's the point of the exercise).

---

## Status

| Step | State |
|---|---|
| Security group `rds-mysql-upgrade-practice` | ✅ done |
| Custom parameter group `mysql-practice-80` | ✅ done |
| Primary `mysql-practice-primary` (8.0.43) | ✅ available — `mysql-practice-primary.ctjboy9he80j.us-west-2.rds.amazonaws.com` (us-west-2c) |
| Seed `appdb` schema + data | ✅ 5 customers / 8 orders / 10 items, trigger + proc verified |
| Read replica `mysql-practice-replica` | ✅ available — `mysql-practice-replica.ctjboy9he80j.us-west-2.rds.amazonaws.com` (us-west-2a) |
| Replication verified | ✅ `Seconds_Behind_Source: 0`, both threads Yes, replica enforces `--read-only` |
| Target parameter group `mysql-practice-84` | ✅ created in console (family `mysql8.4`), all 4 values match the 8.0 group |
| Blue/green deployment `mysql-practice-bg` | ✅ AVAILABLE — green primary `...-green-safvmt` + green replica `...-green-cyc9r8`, both **8.4.10** on `mysql-practice-84`, both read-only |
| Cross-version replication 8.0 blue → 8.4 green | ✅ write on blue primary reached all 4 instances in <6s; trigger fired correctly on green |
| **Switchover (Folau)** | ✅ 2026-08-09 — `SWITCHOVER_COMPLETED`, both pairs renamed, zero data loss (the last 8.0 write survived), same endpoint/user/password |
| Post-switchover verification | ✅ 8.4.10 on both, writes accepted, trigger + stored proc working, replication 0s lag, all 4 parameters carried over |
| Teardown | ✅ 2026-08-10 — all instances, blue/green deployment, parameter groups, security group, SSM parameter, retained backups and manual snapshot deleted. Automated `rds:` snapshots expire on their own with the 1-day retention. |

---

## Decisions

- **8.0.43 as the starting version.** Recent 8.0, and `describe-db-engine-versions` confirms a
  direct major upgrade path to 8.4.3 – 8.4.10. No intermediate hop needed.
- **db.t4g.micro, single-AZ.** ~$0.045/hr for the pair. Multi-AZ was declined — it doubles cost
  and does *not* change the upgrade story, since RDS upgrades primary and standby simultaneously
  and the instance is down either way.
- **Custom parameter group on purpose.** A `mysql8.0`-family group can't attach to an 8.4
  instance. Leaving the matching `mysql8.4` group uncreated makes that a step Folau has to
  discover and perform, which is exactly what will happen at work.
- **Auto minor version upgrade OFF.** Prevents the engine version drifting mid-drill.
- **Backup retention = 1 day, not 0.** Required to create a read replica at all, and RDS only
  takes the pre-upgrade rollback snapshots when retention > 0.
- **Publicly accessible, ingress locked to 73.65.162.171/32.** Needed so the local `mysql` client
  (8.4.10, already installed) can verify replication across the version boundary.
- **Seed data is deliberately clean** — utf8mb4, no reserved words, no obsolete types — so the
  drill exercises upgrade mechanics rather than data remediation. Includes a trigger and a stored
  procedure since the 8.4 prechecks specifically inspect routine bodies and trigger definers.

## Findings worth keeping

- AWS docs state it twice: **"you must upgrade all of the read replicas before upgrading the
  source instance."** An 8.0 source → 8.4 replica is supported; the reverse breaks replication.
  This is the single most important thing to get right at work.
- **48 parameters are removed** between the `mysql8.0` and `mysql8.4` families and 31 are new.
  Full mapping in `param-diff.md`. The ones most likely to be set at work:
  `innodb_log_file_size` → `innodb_redo_log_capacity`, `expire_logs_days` →
  `binlog_expire_logs_seconds`, every `slave_*` → `replica_*`, and `gtid_mode` → `gtid-mode`
  (hyphen).
- **RDS keeps `mysql_native_password` ON in 8.4** (default ON, not modifiable), unlike upstream
  MySQL 8.4 which disables it. The widely-repeated "8.4 will break your native-password users"
  warning does **not** apply to RDS. Verified via `describe-engine-default-parameters`.
- Prechecks run **before** the instance is stopped, so a precheck failure costs time, not downtime.
  Failures land in `PrePatchCompatibility.log`; a failed post-start lands in `upgradeFailure.log`
  with event `RDS-EVENT-0188` and RDS rolls back to 8.0 automatically.
- Major upgrade empties the `slow_log` and `general_log` tables.

## Blue/green addendum (2026-08-09)

`bluegreen-runbook.md` added — console walkthrough for the low-downtime path where the endpoint,
username and password all stay identical.

- Endpoint survives because RDS **renames** the instances at switchover: green
  `...-green-abc123` takes the blue name, blue becomes `...-old1`. Endpoint DNS is derived from
  the instance identifier, so the hostname is unchanged. Credentials come across because green is
  a snapshot restore of blue.
- **Corrected an assumption:** `binlog_format=ROW` is *not* a documented prerequisite for RDS
  MySQL blue/green — the docs list only "enable automated backups". Set it to ROW anyway
  (dynamic, no reboot) since MIXED can degrade to statement-based logging.
- Blockers to check at work: a **custom option group** prevents choosing the major version at
  creation time (ours is `default:mysql-8-0`, fine), and **Secrets Manager–managed master
  passwords are unsupported** by blue/green entirely.
- Storage initialization is unavailable on t3/t4g, so the green instance lazy-loads from S3 and
  is sluggish at first. Instance-class artifact, not an upgrade problem.
- After switchover the `-old1` instances keep running and billing. Deleting the blue/green
  deployment does **not** delete them.

## Outcome

Drill complete via the **blue/green** path. Total cost roughly $2. All AWS resources destroyed on
2026-08-10; `connect.sh` and `teardown.sh` reference endpoints that no longer exist and are kept
only as a record of the drill.

Confirmed end to end: green was built as an 8.0 replica of blue, upgraded to 8.4.10, given the
`mysql-practice-84` parameter group, and kept in sync — a write on the 8.0 blue primary reached
both 8.4 green instances in under 6 seconds, with the trigger firing correctly on green. At
switchover the instances were renamed, so the hostname, username and password were unchanged and
`connect.sh` kept working untouched.

## Carry into the work upgrade

- [ ] Run the six precheck queries in `runbook.md` §0 against the work primary **now**, not on
      upgrade day. A failed precheck after the window is booked means rescheduling.
- [ ] Diff the work parameter group against the `mysql8.4` family (`param-diff.md`) — 48
      parameters don't exist in 8.4. `max_connections` went missing during this drill and nothing
      warned about it.
- [ ] Check the Spring Boot app's JVM DNS TTL (`networkaddress.cache.ttl`). If it's `-1` the app
      stays pinned to the retired `-old1` instance after switchover. This is the only thing in the
      whole path that can hard-break the app, and it needs its own release.
- [ ] Confirm Connector/J ≥ 8.0.33. Ship that separately, before the DB upgrade.
- [ ] Prefer blue/green over in-place: it removes the replica-ordering trap entirely, and the
      read replica never goes dark (in-place takes it down for 10–15 min, which breaks read/write
      split routing).
- [ ] Budget for deleting the `-old1` instances. They keep running and billing; deleting the
      blue/green deployment does not remove them.

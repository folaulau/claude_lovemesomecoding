# RDS MySQL 8.0 → 8.4 upgrade drill

A throwaway replica of the work topology (1 primary + 1 read replica) in the **personal** AWS
account, so the real upgrade at work is the second time you do it, not the first.

## What got built

| | |
|---|---|
| Account | `329580012644` (`folau` profile), **us-west-2** |
| Primary | `mysql-practice-primary` — MySQL **8.0.43**, db.t4g.micro, single-AZ |
| Read replica | `mysql-practice-replica` — created from the primary |
| Parameter group | `mysql-practice-80` (**custom**, family `mysql8.0`) — deliberately custom, see below |
| Security group | `rds-mysql-upgrade-practice` (`sg-0d589e65523134e04`) — 3306 from your IP only |
| Subnet group | `default-vpc-60d8ba18` (default VPC, 4 AZs) |
| DB / user | `appdb` / `admin` |
| Password | SSM SecureString `/practice/mysql-upgrade/master-password` |
| Storage | 20 GB gp3, encrypted, backup retention **1 day** |
| Auto minor upgrade | **off** — so the version can't drift under you mid-drill |

Cost while running: **≈ $0.045/hr** for the pair (~$1/day). Delete when done — see Teardown.

## Why the parameter group is custom

Your work cluster almost certainly uses a custom parameter group, and that creates a step people
miss: **a `mysql8.0`-family parameter group cannot be attached to an 8.4 instance.** You must
create a `mysql8.4`-family group *first* and select it as part of the upgrade, or the console
silently drops you onto `default.mysql8.4` and every tuned parameter is gone.

That step is left undone on purpose. It's exercise #1.

## The one rule that breaks people

From the AWS docs, stated twice on the same page:

> *"If your MySQL DB instance uses read replicas, then you must upgrade all of the read replicas
> before upgrading the source instance."*

**Replica first, then primary.** MySQL replication tolerates an older source feeding a newer
replica, never the reverse. Upgrade the primary first and replication breaks with a version-
incompatibility error, and you get to rebuild the replica from scratch.

## Files

- `runbook.md` — the click-by-click drill, in order, with what to watch at each step
- `progress_report.md` — status, decisions, and what's left
- `seed.sql` — the schema/data loaded into `appdb`
- `teardown.sh` — deletes everything this project created

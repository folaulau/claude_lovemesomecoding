# Drill runbook — MySQL 8.0.43 → 8.4 with a read replica

Do these in order. The order is the point.

Console: **RDS → Databases** in **us-west-2**, `folau` account.

---

## 0. Baseline (before touching anything)

Connect to the primary:

```bash
export AWS_PROFILE=folau
PW=$(aws ssm get-parameter --region us-west-2 --name /practice/mysql-upgrade/master-password \
      --with-decryption --query Parameter.Value --output text)
PRIMARY=$(aws rds describe-db-instances --region us-west-2 \
      --db-instance-identifier mysql-practice-primary --query 'DBInstances[0].Endpoint.Address' --output text)
REPLICA=$(aws rds describe-db-instances --region us-west-2 \
      --db-instance-identifier mysql-practice-replica --query 'DBInstances[0].Endpoint.Address' --output text)

mysql -h "$PRIMARY" -u admin -p"$PW" appdb -e "SELECT VERSION(); SELECT COUNT(*) FROM orders;"
mysql -h "$REPLICA" -u admin -p"$PW" appdb -e "SELECT VERSION(); SELECT COUNT(*) FROM orders;"
```

Both should say `8.0.43` and the same row counts.

Confirm replication is live — write on the primary, read it on the replica:

```bash
mysql -h "$PRIMARY" -u admin -p"$PW" appdb -e \
  "INSERT INTO upgrade_marker(note) VALUES('written on 8.0 primary before upgrade');"
sleep 3
mysql -h "$REPLICA" -u admin -p"$PW" appdb -e \
  "SELECT * FROM upgrade_marker ORDER BY id DESC LIMIT 3;"
```

Check lag on the replica:

```sql
SHOW REPLICA STATUS\G   -- look at Seconds_Behind_Source, Replica_IO_Running, Replica_SQL_Running
```

**At work, also run the real prechecks by hand before you touch the console** — these are the ones
that actually bite:

```sql
-- 1. Users still on mysql_native_password. Disabled by default in 8.4.
SELECT user, host, plugin FROM mysql.user WHERE plugin = 'mysql_native_password';

-- 2. utf8mb3 anywhere (deprecated; prechecks warn, clients can break)
SELECT table_schema, table_name, column_name, character_set_name
FROM information_schema.columns
WHERE character_set_name LIKE 'utf8mb3%' OR character_set_name = 'utf8';

-- 3. Triggers with a missing/invalid definer
SELECT trigger_schema, trigger_name, definer FROM information_schema.triggers;

-- 4. Obsolete sql_mode values
SELECT @@sql_mode;

-- 5. FK constraint names over 64 chars
SELECT constraint_schema, constraint_name, CHAR_LENGTH(constraint_name) AS len
FROM information_schema.table_constraints
WHERE constraint_type='FOREIGN KEY' AND CHAR_LENGTH(constraint_name) > 64;
```

---

## 1. Create the 8.4 parameter group  ← the step people forget

The primary and replica are on the **custom** group `mysql-practice-80`, family `mysql8.0`. That
family cannot attach to an 8.4 instance. Build the target group first.

**Console → RDS → Parameter groups → Create parameter group**
- Engine type `MySQL Community`, Parameter group family **`mysql8.4`**
- Name `mysql-practice-84`

Then copy over the non-default values from `mysql-practice-80`. Ours sets three:
`slow_query_log=1`, `long_query_time=2`, `max_connections=100`.

To list what's actually customized in a group (use this at work — do not eyeball it):

```bash
aws rds describe-db-parameters --region us-west-2 \
  --db-parameter-group-name mysql-practice-80 --source user \
  --query 'Parameters[].{Name:ParameterName,Value:ParameterValue}' --output table
```

See `param-diff.md` for the parameters that exist in `mysql8.0` but **not** in `mysql8.4` — those
can't be carried across and are a common source of "why did my upgrade get blocked".

---

## 2. Upgrade the READ REPLICA first

> AWS docs: *"you must upgrade all of the read replicas before upgrading the source instance."*

An 8.0 source replicating into an 8.4 replica is supported. The reverse is not. Get this backwards
and you rebuild the replica.

**Console → Databases → `mysql-practice-replica` → Modify**
- **DB engine version** → `8.4.x`
- **DB parameter group** → `mysql-practice-84`
- Continue → **Apply immediately** (at work: schedule it in the maintenance window instead)

What to watch while it runs:
- Status goes `modifying` → `upgrading` → `available`. Expect **~10–15 min**.
- **Logs & events** tab: RDS runs the mandatory prechecks *before* stopping the instance, so a
  failure here costs you nothing but time.
- If it fails, read **`PrePatchCompatibility.log`** in the Logs tab — that file names the exact
  incompatibility and usually links the MySQL doc for it.
- The replica is **unavailable** for the whole upgrade. Any read traffic pointed at it fails.
  This is why you drain readers first at work.

When it's back:

```bash
mysql -h "$REPLICA" -u admin -p"$PW" appdb -e "SELECT VERSION();"      # 8.4.x
mysql -h "$REPLICA" -u admin -p"$PW" -e "SHOW REPLICA STATUS\G" | grep -E 'Running|Behind|Error'
```

Then prove cross-version replication is alive — write to the **8.0 primary**, read on the
**8.4 replica**:

```bash
mysql -h "$PRIMARY" -u admin -p"$PW" appdb -e \
  "INSERT INTO upgrade_marker(note) VALUES('8.0 primary -> 8.4 replica, mid-upgrade');"
sleep 3
mysql -h "$REPLICA" -u admin -p"$PW" appdb -e "SELECT * FROM upgrade_marker ORDER BY id DESC LIMIT 2;"
```

Seeing that row land is the whole lesson. **Don't skip it.**

---

## 3. Upgrade the PRIMARY

**Console → Databases → `mysql-practice-primary` → Modify**
- **DB engine version** → the **same** `8.4.x` you used on the replica
- **DB parameter group** → `mysql-practice-84`
- Continue → Apply immediately

What happens:
- RDS takes **up to two snapshots before** any change, plus one **after**. (Only because backup
  retention is > 0 — with retention 0 you get *no* pre-upgrade snapshot and no rollback path.)
- RDS runs `mysql_upgrade` against the data dictionary.
- `slow_log` and `general_log` tables are **emptied**. Save them first if you need them.
- The primary is **down** for the duration — single-AZ, so this is a hard outage.
  A Multi-AZ instance upgrades primary and standby *simultaneously*, so it's down too;
  Multi-AZ does **not** buy you a zero-downtime major upgrade.
- Typical: ~10 min, longer for bigger instances.

Failure behavior worth knowing: if the engine won't start on 8.4, RDS **rolls back automatically**
to 8.0 and emits event **RDS-EVENT-0188**; details land in **`upgradeFailure.log`**. Pending
parameter changes still get applied during that restart and survive the rollback.

---

## 4. Verify

```bash
mysql -h "$PRIMARY" -u admin -p"$PW" appdb -e \
  "SELECT VERSION(); SELECT COUNT(*) FROM customers; SELECT COUNT(*) FROM orders; SELECT COUNT(*) FROM order_items;"
mysql -h "$REPLICA" -u admin -p"$PW" appdb -e "SELECT VERSION(); SELECT COUNT(*) FROM orders;"

# trigger + stored proc survived?
mysql -h "$PRIMARY" -u admin -p"$PW" appdb -e "CALL customer_order_total(1);"
mysql -h "$PRIMARY" -u admin -p"$PW" appdb -e \
  "INSERT INTO orders(customer_id,status,total_cents) VALUES(1,'paid',999);"
sleep 3
mysql -h "$REPLICA" -u admin -p"$PW" appdb -e "SELECT * FROM upgrade_marker ORDER BY id DESC LIMIT 2;"
```

Counts: 5 customers, 8 orders (9 after the insert above), 10 order_items.

Confirm the parameter group actually took and isn't `pending-reboot`:

```bash
aws rds describe-db-instances --region us-west-2 --db-instance-identifier mysql-practice-primary \
  --query 'DBInstances[0].DBParameterGroups' --output table
```

**There is no un-upgrade.** Once 8.4 is running, the only way back is restoring the pre-upgrade
snapshot into a *new* instance.

---

## Notes for the real thing at work

- **Take a manual snapshot first**, named with the date. The automatic pre-upgrade snapshots exist
  but a manual one you control is worth the two minutes.
- **Replicas first, always.** Same rule, and it applies to *all* replicas, not just one.
- Consider **Blue/Green Deployments** if the outage window is tight — it stands up an 8.4 green
  environment replicating from 8.0 blue and switches over in ~a minute, instead of a ~10 min hard
  outage. Costs double for the duration.
- Bump the app's connector version before the DB. Old clients throw *unknown character set* on
  `utf8mb3`, and old connectors can trip over the `mysql_native_password` default change.
- After the upgrade, watch slow query log and `Seconds_Behind_Source` for a day — 8.4 has optimizer
  changes and a plan can regress.

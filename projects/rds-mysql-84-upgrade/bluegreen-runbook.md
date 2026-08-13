# Blue/Green upgrade 8.0 → 8.4 — AWS Console guide

The point of this method: **the endpoint hostname, username, and password all stay exactly the
same.** Your app config doesn't change. Downtime is the switchover only — typically under a
minute instead of the ~10 minute hard outage of an in-place upgrade.

## Why the endpoint survives

At switchover RDS **renames the instances**. From the AWS docs:

> *"The names and endpoints in the current production environment are assigned to the newly
> switched over production environment, requiring no changes to your application... The DB
> instances in the previous blue environment are renamed by appending `-old{n}` to the current
> name."*

So:

| Before switchover | After switchover |
|---|---|
| `mysql-practice-primary` (8.0) | `mysql-practice-primary-old1` (8.0, still running) |
| `mysql-practice-primary-green-abc123` (8.4) | **`mysql-practice-primary`** (8.4) |
| `mysql-practice-replica` (8.0) | `mysql-practice-replica-old1` (8.0, still running) |
| `mysql-practice-replica-green-abc123` (8.4) | **`mysql-practice-replica`** (8.4) |

Because the RDS endpoint DNS name is derived from the instance identifier, the green instance
inherits the identical hostname:

```
mysql-practice-primary.ctjboy9he80j.us-west-2.rds.amazonaws.com
```

The green environment is created by **restoring a snapshot of blue**, so the master user
(`admin`) and its password come across byte-identical. Nothing to rotate, nothing to update.

⚠️ One exception: **blue/green does not support master passwords managed by AWS Secrets Manager.**
If your work instance uses "Manage master credentials in AWS Secrets Manager", you must turn that
off before you can create a blue/green deployment.

---

## Prerequisites (verify before you start)

| Requirement | Ours | How to check in console |
|---|---|---|
| Automated backups enabled (retention > 0) | ✅ 1 day | Databases → instance → **Maintenance & backups** tab → Automated backups |
| Not using Secrets Manager for master password | ✅ | Databases → instance → **Configuration** tab → Master credentials |
| **Not** a custom option group (else you can't pick the major version at creation) | ✅ `default:mysql-8-0` | **Configuration** tab → Option group |
| `binlog_format` = ROW (recommended, not strictly required) | ✅ set | Parameter groups → `mysql-practice-80` → filter `binlog_format` |
| No cascading or cross-Region read replicas | ✅ | Databases list, indentation shows replica topology |
| Target 8.4 parameter group exists | ⬜ **you create this** | Parameter groups → Create |

Also disable the **Event Scheduler** on green if you use events — the docs require
`event_scheduler` be off in the green environment to avoid events firing twice.

---

## Step 1 — Create the `mysql8.4` parameter group

Same step as the in-place drill. Blue/green *can* apply a parameter group to the green
environment at creation, so you want it ready first.

1. **RDS → Parameter groups → Create parameter group**
2. Parameter group family: **`mysql8.4`**
3. Type: **DB parameter group**, Name: `mysql-practice-84`
4. Create, then select it → **Edit** and set:
   - `slow_query_log` = `1`
   - `long_query_time` = `2`
   - `max_connections` = `100`
   - `binlog_format` = `ROW`

Check `param-diff.md` for the 48 parameters that don't exist in the 8.4 family, so you know what
you can't carry over.

---

## Step 2 — Create the blue/green deployment

1. **RDS → Databases** → select **`mysql-practice-primary`** (the *primary*, not the replica —
   RDS copies the whole topology including replicas automatically).
2. **Actions → Create Blue/Green Deployment**.
3. Review the **Blue database identifiers** listed at the top. You should see both
   `mysql-practice-primary` **and** `mysql-practice-replica`. If the replica isn't listed, stop
   and figure out why before continuing.
4. **Blue/Green Deployment identifier**: `mysql-practice-bg`
5. **Engine version for green databases**: choose **`8.4.x`** ← this is the upgrade
6. **DB parameter group for green databases**: **`mysql-practice-84`**
7. Leave storage type / allocated storage / IOPS alone.
8. **Create**.

Creation takes roughly **15–30 minutes** for this small instance. RDS is snapshotting blue,
restoring it as green, upgrading green to 8.4, and wiring up binlog replication blue → green.

> Note for t-class: RDS **storage initialization** is *not* available on t3/t4g families, so green
> loads its blocks lazily from S3. First queries against green can be noticeably slow. That's the
> instance class, not the upgrade.

Watch progress under **RDS → Blue/Green Deployments** (its own left-nav item). The deployment
shows **Available** when green is ready and replicating.

---

## Step 3 — Test the green environment

Green instances appear in the **Databases** list with the `-green-{random}` suffix and their own
endpoints. **Green is read-only by default** — leave it that way.

Grab the green endpoint from the console and check the version and the data:

```bash
PW='N4ad6SO09j7lkofwgBVqk7nS'
GREEN=mysql-practice-primary-green-XXXXXX.ctjboy9he80j.us-west-2.rds.amazonaws.com

mysql -h "$GREEN" -u admin -p"$PW" appdb -e "SELECT VERSION();"   # 8.4.x
mysql -h "$GREEN" -u admin -p"$PW" appdb -e \
  "SELECT COUNT(*) FROM customers; SELECT COUNT(*) FROM orders;"
```

Note the credentials are unchanged — same `admin` / same password on green. That's the whole
promise of this method, and it's worth confirming with your own eyes here.

Now prove replication blue → green is live across the version boundary:

```bash
./connect.sh write "written on 8.0 blue, should appear on 8.4 green"
mysql -h "$GREEN" -u admin -p"$PW" appdb -e \
  "SELECT * FROM upgrade_marker ORDER BY id DESC LIMIT 2;"
```

Check replication health in the console: **Blue/Green Deployments → mysql-practice-bg** shows
replication status per instance. Confirm lag is ~0 before switching.

Do **not** write to green. Writes there cause replication conflicts and end up as phantom data in
production after switchover. (If you truly need to test writes, the documented procedure is to set
`read_only` to `1`, let the parameter group sync, then set it to `0` — but for this drill, don't.)

---

## Step 4 — Switch over

1. **RDS → Blue/Green Deployments** → select `mysql-practice-bg`
2. **Actions → Switch over**
3. Review the rename preview — it tells you exactly which names move where.
4. Set the **switchover timeout** (default 300s, range 30–3600). If guardrails aren't satisfied
   inside the window, RDS **cancels and rolls back** — blue stays production, nothing is lost.
5. Confirm.

What RDS does during switchover:
- Blocks writes on blue
- Waits for green to fully catch up (zero data loss)
- Runs guardrails: replication lag, long-running transactions, in-flight DDL
- Renames blue → `-old1` and green → the production names
- Resumes traffic

Typically **well under a minute**. Existing connections are dropped — your app must reconnect.

**A switchover that fails guardrails is a non-event.** It cancels, blue stays live, and you fix
the cause and retry. That safety is the reason to prefer this method at work.

---

## Step 5 — Verify

The endpoints have not changed, so your original commands still work verbatim:

```bash
./connect.sh status
```

Expect `8.4.x` on both, identical row counts, `Seconds_Behind_Source: 0`. Then confirm the
replica is a genuine replica of the new primary again:

```bash
./connect.sh write "post-switchover on 8.4"
```

---

## Step 6 — Clean up (do not skip — this is the expensive part)

After switchover the old blue instances are **still running and still billing**. RDS keeps them
deliberately, so you can regression-test or fall back.

1. **RDS → Blue/Green Deployments** → select `mysql-practice-bg` → **Actions → Delete**.
   This deletes the *deployment object* only. It does **not** delete `-old1` instances.
2. **RDS → Databases** → delete `mysql-practice-primary-old1` and
   `mysql-practice-replica-old1`.
   - Delete the **replica first**, then the primary.
   - Skip the final snapshot for this drill; at work, **take one**.

For this drill you're running 4 instances while the deployment exists — about **$0.09/hr**.

---

## Rollback story

- **Before switchover:** delete the blue/green deployment. Blue was never touched. Zero risk.
- **Switchover fails guardrails:** automatic cancel, blue stays production.
- **After switchover, something's wrong:** `-old1` still exists with your pre-upgrade data, but it
  is **not** in sync — it stopped receiving writes at switchover. Rolling back means accepting the
  loss of everything written since. This is why you delete `-old1` only after you're satisfied.

---

## In-place vs blue/green — when to use which

| | In-place | Blue/Green |
|---|---|---|
| Downtime | ~10 min hard outage | < 1 min switchover |
| Endpoint changes | No | No (green is renamed to blue's name) |
| Credentials change | No | No |
| Test 8.4 before committing | No | **Yes** — that's the main benefit |
| Cost during upgrade | 1× | 2× while green exists |
| Rollback before commit | Restore snapshot to a new instance | Just delete the deployment |
| Replica handling | **You upgrade replicas first, manually** | Automatic — topology is copied |
| Blocked by custom option group | No | Yes, for major upgrade at creation |
| Secrets Manager master password | Fine | **Not supported** |

For the work upgrade: blue/green removes the replica-ordering trap entirely, because RDS builds
and upgrades the whole topology for you and switches it atomically.

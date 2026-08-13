# Parameter changes: RDS family `mysql8.0` → `mysql8.4`

Generated from the RDS API on 2026-08-09 (us-west-2), not from memory:

```bash
aws rds describe-engine-default-parameters --region us-west-2 --db-parameter-group-family mysql8.0 \
  --query 'EngineDefaults.Parameters[].ParameterName' --output text | tr '\t' '\n' | sort -u > p80.txt
aws rds describe-engine-default-parameters --region us-west-2 --db-parameter-group-family mysql8.4 \
  --query 'EngineDefaults.Parameters[].ParameterName' --output text | tr '\t' '\n' | sort -u > p84.txt
comm -23 p80.txt p84.txt   # removed in 8.4
comm -13 p80.txt p84.txt   # new in 8.4
```

553 parameters in `mysql8.0`, 536 in `mysql8.4`. **48 removed, 31 new.**

Run that same diff against *your work parameter group's* customized values before upgrade day:

```bash
aws rds describe-db-parameters --db-parameter-group-name <WORK-GROUP> --source user \
  --query 'Parameters[].ParameterName' --output text | tr '\t' '\n' | sort -u > mine.txt
comm -12 mine.txt removed.txt    # <- anything here is a value you will LOSE
```

## Renames / replacements that matter

| `mysql8.0` | `mysql8.4` | Note |
|---|---|---|
| `innodb_log_file_size`, `innodb_log_files_in_group` | `innodb_redo_log_capacity` | Commonly tuned. New param is a single total byte count, not size × count. |
| `default_authentication_plugin` | `authentication_policy` | Default `*:caching_sha2_password`. |
| `expire_logs_days` | `binlog_expire_logs_seconds` | Default 2592000 (30d), **not modifiable** on RDS. |
| `gtid_mode` | `gtid-mode` | **Hyphen, not underscore** in the 8.4 family. Easy to miss in a copy script. |
| `log_slave_updates` | `log_replica_updates` | |
| `init_slave` | `init_replica` | |
| `skip-slave-start` | `skip_replica_start` | |
| `sql_slave_skip_counter` | `sql_replica_skip_counter` | |
| `rpl_stop_slave_timeout` | `rpl_stop_replica_timeout` | |
| `master_verify_checksum` | `source_verify_checksum` | |
| `log_slow_slave_statements` | `log_slow_replica_statements` | |
| all other `slave_*` | `replica_*` | `slave_parallel_workers` → `replica_parallel_workers`, etc. The `slave_*` aliases are gone, not deprecated. |
| `core-file` | `core_file` | |
| `master_info_repository`, `relay_log_info_repository`, `relay_log_info_file`, `sync_master_info`, `sync_relay_log_info` | *(none)* | Replication metadata is table-only in 8.4. Nothing to carry over. |
| `transaction_write_set_extraction` | *(none)* | Always `XXHASH64` now. |
| `binlog_transaction_dependency_tracking` | *(none)* | Always `WRITESET` now. |
| `rpl_semi_sync_master_wait_point`, `rpl_semi_sync_master_wait_for_slave_count` | *(none)* | Semisync moved to the `rpl_semi_sync_source_*` component vars. |
| `slave_compressed_protocol` | `replica_compressed_protocol` | |
| `log_bin_use_v1_row_events`, `show_old_temporals`, `avoid_temporal_upgrade`, `new`, `old-style-user-limits`, `ssl_fips_mode`, `collation_database`, `character-set-client-handshake`, `innodb_doublewrite_batch_size` | *(none)* | Just gone. |

## `mysql_native_password` — RDS differs from upstream

Upstream MySQL 8.4 ships `mysql_native_password` **disabled by default**. That's the headline
8.4 breaking change everyone warns about.

**RDS does not do that.** On the `mysql8.4` family:

```
mysql_native_password   default ON    modifiable: false
authentication_policy   default *:caching_sha2_password   modifiable: true
```

So existing `mysql_native_password` users keep working after an RDS 8.0 → 8.4 upgrade, and you
can't turn the plugin off even if you wanted to. `authentication_policy` only governs the default
for **newly created** users.

Still worth auditing before upgrade day, because the app's *connector* may not support
`caching_sha2_password` for any new users you create afterward:

```sql
SELECT user, host, plugin FROM mysql.user WHERE plugin = 'mysql_native_password';
```

## New in 8.4 worth knowing

`explain_json_format_version`, `set_operations_buffer_size`, `restrict_fk_on_non_standard_key`
(can reject FKs that 8.0 allowed), `tls_certificates_enforced_validation`,
`connection_memory_chunk_size`, `temptable_use_mmap`, `innodb_numa_interleave`.

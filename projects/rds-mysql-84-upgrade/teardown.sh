#!/usr/bin/env bash
# Deletes everything the MySQL 8.0->8.4 upgrade drill created.
# Run when you're done practicing. Idempotent-ish: missing resources are skipped.
set -uo pipefail

export AWS_PROFILE=${AWS_PROFILE:-folau}
REGION=us-west-2
SG_ID=sg-0d589e65523134e04

echo "==> deleting read replica"
aws rds delete-db-instance --region $REGION \
  --db-instance-identifier mysql-practice-replica \
  --skip-final-snapshot --delete-automated-backups >/dev/null 2>&1 \
  && echo "    delete started" || echo "    not found / already gone"

echo "==> deleting primary"
aws rds delete-db-instance --region $REGION \
  --db-instance-identifier mysql-practice-primary \
  --skip-final-snapshot --delete-automated-backups >/dev/null 2>&1 \
  && echo "    delete started" || echo "    not found / already gone"

echo "==> waiting for both to disappear (several minutes)..."
aws rds wait db-instance-deleted --region $REGION --db-instance-identifier mysql-practice-replica 2>/dev/null
aws rds wait db-instance-deleted --region $REGION --db-instance-identifier mysql-practice-primary 2>/dev/null
echo "    gone"

echo "==> deleting parameter groups"
for pg in mysql-practice-80 mysql-practice-84; do
  aws rds delete-db-parameter-group --region $REGION --db-parameter-group-name "$pg" >/dev/null 2>&1 \
    && echo "    deleted $pg" || echo "    $pg not found / still in use"
done

echo "==> deleting security group"
aws ec2 delete-security-group --region $REGION --group-id "$SG_ID" >/dev/null 2>&1 \
  && echo "    deleted $SG_ID" || echo "    $SG_ID not found / still attached"

echo "==> deleting SSM password parameter"
aws ssm delete-parameter --region $REGION --name /practice/mysql-upgrade/master-password >/dev/null 2>&1 \
  && echo "    deleted" || echo "    not found"

echo "==> leftover manual snapshots (delete by hand if any):"
aws rds describe-db-snapshots --region $REGION --snapshot-type manual \
  --query "DBSnapshots[?starts_with(DBInstanceIdentifier,'mysql-practice')].DBSnapshotIdentifier" \
  --output text

echo "done."

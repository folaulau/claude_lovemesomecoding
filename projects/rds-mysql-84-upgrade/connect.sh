#!/usr/bin/env bash
# Open a mysql shell against the drill databases.
#   ./connect.sh            -> primary
#   ./connect.sh replica    -> read replica
#   ./connect.sh status     -> version + row counts + replication lag on both
set -euo pipefail

export AWS_PROFILE=${AWS_PROFILE:-folau}
REGION=us-west-2
PRIMARY=mysql-practice-primary.ctjboy9he80j.us-west-2.rds.amazonaws.com
REPLICA=mysql-practice-replica.ctjboy9he80j.us-west-2.rds.amazonaws.com

PW=$(aws ssm get-parameter --region $REGION --name /practice/mysql-upgrade/master-password \
      --with-decryption --query Parameter.Value --output text)

Q="SELECT VERSION() AS ver,
     (SELECT COUNT(*) FROM customers) AS customers,
     (SELECT COUNT(*) FROM orders) AS orders,
     (SELECT COUNT(*) FROM order_items) AS items,
     (SELECT COUNT(*) FROM upgrade_marker) AS markers;"

case "${1:-primary}" in
  replica) exec mysql -h "$REPLICA" -u admin -p"$PW" appdb ;;
  primary) exec mysql -h "$PRIMARY" -u admin -p"$PW" appdb ;;
  status)
    echo "--- PRIMARY ---"
    mysql -h "$PRIMARY" -u admin -p"$PW" appdb --table -e "$Q" 2>/dev/null
    echo "--- REPLICA ---"
    mysql -h "$REPLICA" -u admin -p"$PW" appdb --table -e "$Q" 2>/dev/null
    echo "--- REPLICATION ---"
    mysql -h "$REPLICA" -u admin -p"$PW" -e "SHOW REPLICA STATUS\G" 2>/dev/null \
      | grep -E 'Replica_IO_Running|Replica_SQL_Running:|Seconds_Behind_Source|Last_Error' | sed 's/^ *//'
    ;;
  write)
    # write on the primary, read it back on the replica — the cross-version proof
    NOTE="${2:-manual replication check}"
    mysql -h "$PRIMARY" -u admin -p"$PW" appdb -e \
      "INSERT INTO upgrade_marker(note) VALUES('$NOTE');" 2>/dev/null
    sleep 4
    mysql -h "$REPLICA" -u admin -p"$PW" appdb --table -e \
      "SELECT id, note, noted_at FROM upgrade_marker ORDER BY id DESC LIMIT 3;" 2>/dev/null
    ;;
  *) echo "usage: $0 [primary|replica|status|write <note>]"; exit 1 ;;
esac

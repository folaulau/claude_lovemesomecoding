#!/usr/bin/env bash
#
# Build `pizza_lab` — the pizza schema at a size where the optimizer has to think.
#
#   projects/mysql_tutorial/lab/setup.sh          build (drops and recreates)
#   projects/mysql_tutorial/lab/setup.sh --drop   tear down
#   projects/mysql_tutorial/lab/setup.sh --check  verify an existing build
#
# Needs the demo app's MySQL container running:
#   cd lovemesomecoding_demo_project/pizza/pizza-springboot-backend && docker compose up -d
#
# Nothing here writes to the `pizza` database. It is read, never modified.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST=127.0.0.1
PORT=3308        # NOT 3306 — see docker-compose.yml in the demo app
USER=root

my() { mysql -h "$HOST" -P "$PORT" -u "$USER" "$@"; }

if ! my -e 'SELECT 1' >/dev/null 2>&1; then
    echo "cannot reach MySQL at $HOST:$PORT."
    echo "start it with:  cd lovemesomecoding_demo_project/pizza/pizza-springboot-backend && docker compose up -d"
    exit 1
fi

case "${1:-}" in
  --drop)
    my -e 'DROP DATABASE IF EXISTS pizza_lab;'
    echo "pizza_lab dropped."
    exit 0
    ;;
  --check) ;;
  "")
    if ! my -e 'SELECT COUNT(*) FROM pizza.customer_order' >/dev/null 2>&1; then
        echo "the \`pizza\` database is not there or not seeded — pizza_lab is built from it."
        echo "start the app once so Liquibase runs:  ./mvnw spring-boot:run"
        exit 1
    fi
    echo "building pizza_lab (about 50s)..."
    time my < "$HERE/build.sql" > /dev/null
    ;;
  *)
    echo "usage: setup.sh [--drop|--check]"; exit 2 ;;
esac

# ---------------------------------------------------------------- verify
# The load runs with FOREIGN_KEY_CHECKS off, so the constraints it would have
# enforced are checked here instead. Silence is what "referentially intact by
# construction" is worth without this.
echo
echo "row counts"
my -t pizza_lab -e "
SELECT 'app_user' AS \`table\`, COUNT(*) AS rows_ FROM app_user
UNION ALL SELECT 'customer_order',     COUNT(*) FROM customer_order
UNION ALL SELECT 'order_item',         COUNT(*) FROM order_item
UNION ALL SELECT 'order_item_topping', COUNT(*) FROM order_item_topping
UNION ALL SELECT 'product',            COUNT(*) FROM product
UNION ALL SELECT 'product_size',       COUNT(*) FROM product_size;"

echo "orders by status"
my -t pizza_lab -e "SELECT status, COUNT(*) AS orders FROM customer_order GROUP BY status ORDER BY orders DESC;"

echo "integrity"
my -t pizza_lab -e "
SELECT
  (SELECT COUNT(*) FROM order_item i
     LEFT JOIN customer_order o ON o.id = i.order_id WHERE o.id IS NULL)          AS orphan_items,
  (SELECT COUNT(*) FROM order_item_topping t
     LEFT JOIN order_item i ON i.id = t.order_item_id WHERE i.id IS NULL)         AS orphan_toppings,
  (SELECT COUNT(*) FROM customer_order o
     LEFT JOIN app_user u ON u.id = o.user_id
     WHERE o.user_id IS NOT NULL AND u.id IS NULL)                                AS orphan_users,
  (SELECT COUNT(*) FROM (SELECT public_id FROM order_item
     GROUP BY public_id HAVING COUNT(*) > 1) d)                                   AS dup_public_ids,
  (SELECT COUNT(*) FROM customer_order o
     JOIN (SELECT order_id, SUM(line_total) s FROM order_item GROUP BY order_id) t
       ON t.order_id = o.id WHERE o.subtotal <> t.s)                              AS subtotal_mismatch,
  (SELECT COUNT(DISTINCT product_id) FROM order_item)                             AS products_ordered;"

echo "Every count above must be 0 except products_ordered, which must be 14."
echo "The figures are asserted against manifest.LAB_ROWS by check_content.py."

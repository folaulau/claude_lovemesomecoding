-- Builds `pizza_lab`: the pizza application's real schema, filled to a size where
-- the optimizer has to make choices.
--
-- WHY THIS EXISTS
--   The demo database has 18 orders. That is the right size for teaching SELECT and
--   joins — a reader can check the answer by eye — and the wrong size for teaching
--   anything about indexes. At 18 rows InnoDB scans the table every time, so an
--   "add an index" lesson would show an index the planner never chooses and an
--   EXPLAIN that says `ALL` no matter what you do.
--
-- EVERYTHING HERE IS DETERMINISTIC. Not one RAND() call.
--   Row counts, the status mix, the number of items per order and every date are
--   derived from the row number with modular arithmetic. Two builds on two machines
--   produce byte-identical tables, which is what lets check_sql.py re-derive a
--   figure a post quotes and compare it exactly. A seeded RAND() would be
--   reproducible on one server version and not across an upgrade.
--
-- ⚠️ DATES ARE ANCHORED TO A FIXED EPOCH, not to NOW().
--   The demo database seeds orders with DATE_SUB(NOW(), ...), which is right for a
--   dashboard that should always look populated and wrong for a tutorial: every
--   quoted result would go stale overnight and check_sql.py would fail every day
--   after the one it was written on.
--
-- Nothing in this file touches the `pizza` database.

SET @LAB_EPOCH = '2025-01-01 00:00:00';

DROP DATABASE IF EXISTS pizza_lab;
CREATE DATABASE pizza_lab CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE pizza_lab;

-- Bulk loading with FKs enforced turns each insert into a lookup per row. The data
-- is generated referentially intact by construction; the constraints are checked
-- for real at the end of setup.sh.
SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;

-- ---------------------------------------------------------------- a numbers table
-- Doubling, not a recursive CTE: cte_max_recursion_depth defaults to 1000 and
-- raising it to a million to count is a strange thing to teach.
--
-- ⚠️ THE AUTO_INCREMENT VALUES COME OUT WITH GAPS, so the doubling table is
-- renumbered below instead of being used directly.
--
-- `innodb_autoinc_lock_mode` is 2 (interleaved) by default in MySQL 8. For an
-- INSERT ... SELECT the server does not know the row count in advance, so it
-- grabs auto-increment values in growing batches and throws away whatever it did
-- not use. The first build of this lab came out with 1,648,576 rows whose MAX(n)
-- was 1,976,220 — so `WHERE n <= 400000` quietly selected 262,144 rows and every
-- table downstream was short. The counts were all exact powers of two, which is
-- the tell.
--
-- Nothing here depends on the gaps being absent, because ROW_NUMBER() renumbers
-- the whole thing 1..N afterwards.
CREATE TABLE seq_raw (n BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE = InnoDB;
INSERT INTO seq_raw VALUES (NULL);
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --       2
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --       4
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --       8
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --      16
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --      32
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --      64
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --     128
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --     256
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --     512
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --   1,024
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --   2,048
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --   4,096
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --   8,192
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --  16,384
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --  32,768
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             --  65,536
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             -- 131,072
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             -- 262,144
INSERT INTO seq_raw SELECT NULL FROM seq_raw;             -- 524,288
-- 524,288 is already more than the 400,000 the largest generated table needs;
-- seq is trimmed to exactly that below.

-- Renumber 1..400000, contiguous and gap-free. This is the table everything else
-- joins against.
CREATE TABLE seq (n BIGINT NOT NULL PRIMARY KEY) ENGINE = InnoDB;
INSERT INTO seq (n)
SELECT ROW_NUMBER() OVER (ORDER BY n) FROM seq_raw LIMIT 400000;
DROP TABLE seq_raw;

-- ---------------------------------------------------------------- catalog
-- Copied verbatim from the demo database so a product id means the same thing in
-- both. These tables are small; their size is not what this lab is exercising.
CREATE TABLE crust        LIKE pizza.crust;
CREATE TABLE topping      LIKE pizza.topping;
CREATE TABLE product      LIKE pizza.product;
CREATE TABLE product_size LIKE pizza.product_size;

INSERT INTO crust        SELECT * FROM pizza.crust;
INSERT INTO topping      SELECT * FROM pizza.topping;
INSERT INTO product      SELECT * FROM pizza.product;
INSERT INTO product_size SELECT * FROM pizza.product_size;

-- ⚠️ PRODUCT IDS ARE NOT CONTIGUOUS. The demo menu is ids 1-8 (pizzas) and 20-25
-- (drinks). Picking a product with `p.id = 1 + something % 14` therefore only ever
-- names ids 1..14, and the join silently drops every drink — the first build came
-- out with 571,430 order items instead of 1,000,000, which is exactly 8/14 of the
-- intended number.
--
-- This maps a dense 0..N-1 onto whatever ids the catalog actually has, so the
-- generator keeps working if the menu changes.
CREATE TABLE product_pick (k INT NOT NULL PRIMARY KEY, product_id BIGINT NOT NULL);
INSERT INTO product_pick (k, product_id)
SELECT ROW_NUMBER() OVER (ORDER BY id) - 1, id FROM product;
SET @NPROD = (SELECT COUNT(*) FROM product_pick);

-- ---------------------------------------------------------------- users
CREATE TABLE app_user LIKE pizza.app_user;

INSERT INTO app_user
    (id, email, password_hash, full_name, role, created_at, updated_at,
     public_id, deleted, stripe_customer_id)
SELECT
    n,
    CONCAT('user', n, '@example.com'),
    '$2a$10$abcdefghijklmnopqrstuvwxyz012345678901234567890123456789',
    CONCAT('Customer ', n),
    -- 1 admin per 10,000 accounts, so a query filtering on role has something
    -- lopsided to work with — which is the interesting case for an index.
    IF(n % 10000 = 0, 'ADMIN', 'CUSTOMER'),
    @LAB_EPOCH - INTERVAL (n % 900) DAY,
    @LAB_EPOCH - INTERVAL (n % 900) DAY,
    CONCAT('dddddddd-0000-4000-8000-', LPAD(n, 12, '0')),
    FALSE,
    NULL
FROM seq
WHERE n <= 50000;

-- ---------------------------------------------------------------- orders
CREATE TABLE customer_order LIKE pizza.customer_order;

-- The status mix is a function of n % 1000, so the counts are exact and stated
-- rather than measured-and-hoped-for:
--   n%1000 <  850   COMPLETED         850/1000 of 400,000 = 340,000
--            850-909 CANCELLED         60/1000             =  24,000
--            910-949 PENDING_PAYMENT   40/1000             =  16,000
--            950-979 PREPARING         30/1000             =  12,000
--            980-999 PAID              20/1000             =   8,000
--
-- Every 5th order is a guest order: user_id NULL, guest_email set. That is the
-- shape the LEFT JOIN lesson needs, and it is 80,000 rows rather than the demo
-- database's handful.
INSERT INTO customer_order
    (id, user_id, guest_email, customer_name, phone, order_type, status,
     address_line1, address_line2, city, state, postal_code,
     subtotal, tax, delivery_fee, total, stripe_payment_intent_id,
     created_at, updated_at, public_id, deleted, card_brand, card_last4)
SELECT
    n,
    IF(n % 5 = 0, NULL, 1 + (n * 7) % 50000),
    IF(n % 5 = 0, CONCAT('guest', n, '@example.com'), NULL),
    IF(n % 5 = 0, CONCAT('Guest ', n), CONCAT('Customer ', 1 + (n * 7) % 50000)),
    CONCAT('801-555-', LPAD(n % 10000, 4, '0')),
    IF(n % 3 = 0, 'CARRYOUT', 'DELIVERY'),
    CASE
        WHEN n % 1000 <  850 THEN 'COMPLETED'
        WHEN n % 1000 <  910 THEN 'CANCELLED'
        WHEN n % 1000 <  950 THEN 'PENDING_PAYMENT'
        WHEN n % 1000 <  980 THEN 'PREPARING'
        ELSE                      'PAID'
    END,
    IF(n % 3 = 0, NULL, CONCAT(1 + n % 9999, ' Main St')),
    NULL,
    IF(n % 3 = 0, NULL, ELT(1 + n % 5, 'Salt Lake City', 'Sandy', 'Draper', 'Murray', 'Midvale')),
    IF(n % 3 = 0, NULL, 'UT'),
    IF(n % 3 = 0, NULL, ELT(1 + n % 5, '84101', '84070', '84020', '84107', '84047')),
    0, 0,
    IF(n % 3 = 0, 0.00, 3.99),
    0,
    IF(n % 1000 >= 910 AND n % 1000 < 950, NULL, CONCAT('pi_lab_', LPAD(n, 10, '0'))),
    -- 730 days back from the epoch, so every date-range and GROUP BY month lesson
    -- has two full years to work with.
    @LAB_EPOCH - INTERVAL (n % 730) DAY - INTERVAL (n % 1440) MINUTE,
    @LAB_EPOCH - INTERVAL (n % 730) DAY - INTERVAL (n % 1440) MINUTE,
    CONCAT('eeeeeeee-0000-4000-8000-', LPAD(n, 12, '0')),
    FALSE,
    IF(n % 1000 >= 910 AND n % 1000 < 950, NULL, ELT(1 + n % 4, 'visa', 'mastercard', 'amex', 'discover')),
    IF(n % 1000 >= 910 AND n % 1000 < 950, NULL, LPAD(n % 10000, 4, '0'))
FROM seq
WHERE n <= 400000;

-- ---------------------------------------------------------------- order items
-- Items per order = 1 + (order_id % 4), so the counts cycle 2,3,4,1 and average
-- exactly 2.5 over any run of four consecutive ids.
CREATE TABLE order_item LIKE pizza.order_item;

INSERT INTO order_item
    (order_id, product_id, product_name, size, crust_id, crust_name,
     quantity, unit_price, line_total, created_at, updated_at, public_id, deleted)
SELECT
    o.id,
    p.id,
    p.name,
    ps.size,
    c.id,
    c.name,
    1 + (o.id + s.n) % 3,
    ps.price + c.price_delta,
    (ps.price + c.price_delta) * (1 + (o.id + s.n) % 3),
    o.created_at,
    o.created_at,
    -- 8-4-4-4-12. Unique per (order_id, item-within-order), which is exactly one row.
    CONCAT(LPAD(HEX(o.id), 8, '0'), '-0000-4000-8000-', LPAD(s.n, 12, '0')),
    FALSE
FROM customer_order o
JOIN seq s           ON s.n <= 1 + (o.id % 4)
JOIN product_pick pp ON pp.k = (o.id * 3 + s.n) % @NPROD
JOIN product p       ON p.id = pp.product_id
JOIN product_size ps ON ps.product_id = p.id
                    AND ps.size = ELT(1 + (o.id + s.n) % 3, 'SMALL', 'MEDIUM', 'LARGE')
JOIN crust c         ON c.id = 1 + (o.id + s.n) % 4;

-- ---------------------------------------------------------------- item toppings
-- Toppings per item = order_item.id % 3, so a third of the items carry none. That
-- asymmetry is the point: it is what makes the LEFT JOIN and the "items with no
-- toppings" queries return something other than everything.
CREATE TABLE order_item_topping LIKE pizza.order_item_topping;

INSERT INTO order_item_topping
    (order_item_id, topping_id, topping_name, price, created_at, updated_at, public_id, deleted)
SELECT
    i.id,
    t.id,
    t.name,
    t.price,
    i.created_at,
    i.created_at,
    -- 8-4-4-4-12. Unique per (order_item_id, topping-within-item).
    CONCAT(LPAD(HEX(i.id), 8, '0'), '-0000-4000-8000-', LPAD(s.n, 12, '0')),
    FALSE
FROM order_item i
JOIN seq s     ON s.n <= i.id % 3
JOIN topping t ON t.id = 1 + (i.id * 5 + s.n) % 12;

-- ---------------------------------------------------------------- derive the money
-- subtotal is DERIVED from the line items rather than typed, so
-- `subtotal = SUM(line_total)` is true by construction. The demo seed does the
-- same thing for the same reason, and the aggregation lesson leans on it.
UPDATE customer_order o
JOIN (
    SELECT order_id, SUM(line_total) AS s
    FROM order_item
    GROUP BY order_id
) t ON t.order_id = o.id
SET o.subtotal = t.s,
    o.tax      = ROUND(t.s * 0.0725, 2),
    o.total    = t.s + ROUND(t.s * 0.0725, 2) + o.delivery_fee;

SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;

-- ---------------------------------------------------------------- statistics
-- Without this the optimizer works from whatever cardinality estimates it happened
-- to collect while the tables were being filled, and the first EXPLAIN a reader
-- runs disagrees with the one in the post.
ANALYZE TABLE app_user, customer_order, order_item, order_item_topping,
              product, product_size, crust, topping;

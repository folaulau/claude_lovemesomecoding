-- Seed data for the MySQL 8.0 -> 8.4 upgrade drill.
-- Deliberately clean: nothing here should trip an 8.4 precheck, so the drill
-- exercises the *mechanics* of the upgrade rather than data remediation.
-- Everything is utf8mb4, no reserved words, no utf8mb3, no obsolete types.

CREATE DATABASE IF NOT EXISTS appdb CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE appdb;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS upgrade_marker;

CREATE TABLE customers (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email         VARCHAR(255)    NOT NULL,
  display_name  VARCHAR(120)    NOT NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_customers_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE orders (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  customer_id  BIGINT UNSIGNED NOT NULL,
  status       ENUM('pending','paid','shipped','cancelled') NOT NULL DEFAULT 'pending',
  total_cents  INT UNSIGNED    NOT NULL DEFAULT 0,
  placed_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_orders_customer (customer_id),
  CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE order_items (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  order_id    BIGINT UNSIGNED NOT NULL,
  sku         VARCHAR(64)     NOT NULL,
  quantity    INT UNSIGNED    NOT NULL DEFAULT 1,
  price_cents INT UNSIGNED    NOT NULL DEFAULT 0,
  KEY idx_items_order (order_id),
  CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- A stored routine and a trigger: the 8.4 prechecks specifically inspect
-- routine bodies and trigger definers, so having some is more representative
-- than a schema of bare tables.
CREATE TABLE upgrade_marker (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  note       VARCHAR(255) NOT NULL,
  noted_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DELIMITER //
CREATE TRIGGER trg_orders_marker AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  INSERT INTO upgrade_marker (note) VALUES (CONCAT('order ', NEW.id, ' created'));
END//

CREATE PROCEDURE customer_order_total(IN p_customer_id BIGINT UNSIGNED)
BEGIN
  SELECT c.email, COUNT(o.id) AS order_count, COALESCE(SUM(o.total_cents),0) AS cents
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.id
  WHERE c.id = p_customer_id
  GROUP BY c.email;
END//
DELIMITER ;

INSERT INTO customers (email, display_name) VALUES
  ('folau@example.com',  'Folau K'),
  ('sione@example.com',  'Sione T'),
  ('mele@example.com',   'Mele V'),
  ('ana@example.com',    'Ana L'),
  ('tevita@example.com', 'Tevita M');

INSERT INTO orders (customer_id, status, total_cents) VALUES
  (1,'paid',12500), (1,'shipped',4200), (2,'pending',9900),
  (3,'paid',31000),  (4,'cancelled',1500), (5,'shipped',7750),
  (2,'paid',22300),  (3,'pending',640);

INSERT INTO order_items (order_id, sku, quantity, price_cents) VALUES
  (1,'SKU-RED-01',2,5000),  (1,'SKU-BLU-07',1,2500),
  (2,'SKU-GRN-03',1,4200),  (3,'SKU-RED-01',1,5000),
  (3,'SKU-YEL-09',2,2450),  (4,'SKU-BLK-02',3,10000),
  (5,'SKU-WHT-05',1,1500),  (6,'SKU-BLU-07',3,2500),
  (7,'SKU-GRN-03',5,4460),  (8,'SKU-YEL-09',1,640);

INSERT INTO upgrade_marker (note) VALUES ('seeded on MySQL 8.0.43 before the upgrade drill');

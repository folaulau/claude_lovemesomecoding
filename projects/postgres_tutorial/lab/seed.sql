-- Bulk data for the /postgre track's index, EXPLAIN, vacuum and transaction lessons.
--
-- StayHub's own database holds 12 properties and 3 bookings. That is the right size for a demo
-- app and the wrong size for teaching query plans: at 12 rows the planner seq-scans everything,
-- so an "add an index" lesson written against it would show an index that is never used. This
-- fills a SEPARATE database, `stayhub_lab`, with the SAME schema at production-ish scale.
--
-- Nothing here touches the stayhub database. Rebuild any time: lab/setup.sh
--
-- Row counts are chosen so the planner has real choices to make:
--   users        50,000   (every 10th is a host)
--   properties   20,000
--   bookings    400,000   20 per property, non-overlapping by construction
--   reviews               one per COMPLETED booking
--   payments              one per booking that is not PENDING
--
-- "Today" in this database is LAB_TODAY = 2024-10-01. Booking status is derived from the dates
-- against it, so past stays are COMPLETED and future ones CONFIRMED or PENDING. Any post that
-- quotes a result involving now() should say so — the rows do not move but the calendar does.

\set ON_ERROR_STOP on

-- Deterministic: the same seed gives the same table every time, so a query plan quoted in a post
-- is reproducible on someone else's machine.
SELECT setseed(0.42);

-- ---------------------------------------------------------------------------------------------
-- users
-- ---------------------------------------------------------------------------------------------
INSERT INTO users (email, password_hash, first_name, last_name, role, is_host, public_id,
                   created_at, updated_at, deleted)
SELECT
    'guest' || n || '@stayhub.test',
    '$2b$12$notarealhashonlyforthelabdatabase00000000000000000000',
    (ARRAY['Ana','Ben','Cara','Dev','Eve','Finn','Gia','Hugo','Iris','Jon'])[1 + n % 10],
    (ARRAY['Silva','Tui','Rossi','Novak','Haugen','Okafor','Kim','Lopez','Meyer','Patel'])[1 + (n / 10) % 10],
    CASE WHEN n % 500 = 0 THEN 'ADMIN' ELSE 'CUSTOMER' END,
    n % 10 = 0,
    gen_random_uuid(),
    TIMESTAMPTZ '2023-01-01 00:00:00+00' + (n % 900) * INTERVAL '1 day',
    TIMESTAMPTZ '2023-01-01 00:00:00+00' + (n % 900) * INTERVAL '1 day',
    false
FROM generate_series(1, 50000) AS n;

-- ---------------------------------------------------------------------------------------------
-- properties — every one owned by a host (users where is_host)
-- ---------------------------------------------------------------------------------------------
INSERT INTO properties (host_id, title, description, property_type, room_type, status,
                        address_line1, city, state, country, postal_code, latitude, longitude,
                        price_per_night, cleaning_fee, max_guests, bedrooms, beds, bathrooms,
                        rating_average, rating_count, public_id, created_at, updated_at, deleted)
SELECT
    ((n % 5000) * 10) + 10,                                   -- a host id: multiples of 10
    (ARRAY['Sunny','Quiet','Modern','Rustic','Bright','Cosy'])[1 + n % 6] || ' ' ||
        (ARRAY['loft','cabin','studio','cottage','villa','flat'])[1 + n % 6] || ' #' || n,
    'A place to stay. Generated row ' || n || ' in the lab database.',
    (ARRAY['HOUSE','APARTMENT','CABIN','CONDO','LOFT','VILLA'])[1 + n % 6],
    (ARRAY['ENTIRE_PLACE','PRIVATE_ROOM','SHARED_ROOM'])[1 + n % 3],
    CASE WHEN n % 25 = 0 THEN 'DRAFT'
         WHEN n % 97 = 0 THEN 'SUSPENDED'
         ELSE 'PUBLISHED' END,
    n || ' Example Street',
    (ARRAY['Lisbon','Porto','Auckland','Wellington','Oslo','Bergen','Lagos','Abuja',
           'Seoul','Busan','Bogota','Medellin','Munich','Berlin','Pune','Kochi'])[1 + n % 16],
    NULL,
    (ARRAY['Portugal','Portugal','New Zealand','New Zealand','Norway','Norway','Nigeria','Nigeria',
           'South Korea','South Korea','Colombia','Colombia','Germany','Germany','India','India'])[1 + n % 16],
    lpad((n % 9999)::text, 4, '0'),
    ROUND((random() * 140 - 45)::numeric, 6),
    ROUND((random() * 340 - 170)::numeric, 6),
    ROUND((45 + random() * 420)::numeric, 2),
    ROUND((15 + random() * 90)::numeric, 2),
    2 + n % 9,
    1 + n % 5,
    1 + n % 7,
    ROUND((1 + (n % 6) * 0.5)::numeric, 1),
    0, 0,
    gen_random_uuid(),
    TIMESTAMPTZ '2023-03-01 00:00:00+00' + (n % 800) * INTERVAL '1 day',
    TIMESTAMPTZ '2023-03-01 00:00:00+00' + (n % 800) * INTERVAL '1 day',
    n % 311 = 0
FROM generate_series(1, 20000) AS n;

-- ---------------------------------------------------------------------------------------------
-- bookings — 20 stays per property
--
-- Two things are deliberate here.
--
-- The EXCLUDE constraint (no_overlapping_bookings) forbids two blocking stays whose date ranges
-- overlap at the same property. Stays therefore march forward on a fixed 18-day stride with a
-- maximum length of 6 nights, so stay k always ends before stay k+1 begins and the constraint is
-- satisfied by construction rather than by luck. Lengthen a stay past the stride and the whole
-- INSERT fails — which is the constraint doing its job.
--
-- Status is derived from the dates against LAB_TODAY (2024-10-01), not from a row counter. An
-- earlier version keyed it off the loop index and produced 400,000 bookings of which exactly zero
-- were CONFIRMED, because the branch was unreachable. A calendar app whose main status never
-- occurs is a fixture that quietly teaches the wrong thing.
--
-- Each property starts its own calendar at a different offset, so the collection spans
-- 2024-01-01 to 2025-06-05 rather than every property being booked in the same six months.
-- LAB_TODAY sits near the middle of that span on purpose: put it at either end and one status
-- swallows the table, which is what the first two attempts at this file did.
-- ---------------------------------------------------------------------------------------------
INSERT INTO bookings (property_id, guest_id, check_in, check_out, guests, nights, nightly_rate,
                      subtotal, cleaning_fee, service_fee, total, status, cancelled_at,
                      public_id, created_at, updated_at)
SELECT
    p.id,
    1 + ((p.id * 7 + k * 13) % 50000),
    ci,
    ci + nights,
    1 + (k % 4),
    nights,
    p.price_per_night,
    p.price_per_night * nights,
    p.cleaning_fee,
    ROUND(p.price_per_night * nights * 0.12, 2),
    ROUND(p.price_per_night * nights * 1.12, 2) + p.cleaning_fee,
    st,
    CASE WHEN st = 'CANCELLED' THEN (ci - 4)::timestamptz END,
    gen_random_uuid(),
    (ci - 30)::timestamptz,
    (ci - 30)::timestamptz
FROM properties p
CROSS JOIN LATERAL (
    SELECT k, ci, nights,
           CASE WHEN (p.id + k) % 19 = 0        THEN 'CANCELLED'
                WHEN ci + nights <= DATE '2024-10-01' THEN 'COMPLETED'
                WHEN (p.id + k) % 7 = 0         THEN 'PENDING'
                ELSE 'CONFIRMED' END AS st
    FROM generate_series(0, 19) AS k
    CROSS JOIN LATERAL (
        SELECT DATE '2024-01-01' + ((p.id % 180) + k * 18) AS ci,
               1 + ((p.id + k) % 6)                        AS nights
    ) d
) s;

-- ---------------------------------------------------------------------------------------------
-- reviews — one per completed booking, unique on booking_id
-- ---------------------------------------------------------------------------------------------
INSERT INTO reviews (property_id, author_id, booking_id, rating, comment, public_id,
                     created_at, updated_at)
SELECT b.property_id, b.guest_id, b.id,
       1 + (b.id % 5),
       (ARRAY['Great stay.','Would book again.','Clean and quiet.','As described.',
              'Host was helpful.'])[1 + b.id % 5],
       gen_random_uuid(),
       (b.check_out + 1)::timestamptz,
       (b.check_out + 1)::timestamptz
FROM bookings b
WHERE b.status = 'COMPLETED';

-- ---------------------------------------------------------------------------------------------
-- payments — one per non-pending booking
-- ---------------------------------------------------------------------------------------------
INSERT INTO payments (booking_id, amount, currency, status, stripe_payment_intent_id,
                      public_id, created_at, updated_at)
SELECT b.id, b.total, 'usd',
       CASE WHEN b.status = 'CANCELLED' THEN 'REFUNDED' ELSE 'SUCCEEDED' END,
       'pi_lab_' || b.id,
       gen_random_uuid(),
       b.created_at, b.created_at
FROM bookings b
WHERE b.status <> 'PENDING';

-- The planner works off pg_statistic. Without this every EXPLAIN in the track would be quoting
-- estimates taken from an empty table.
VACUUM ANALYZE;

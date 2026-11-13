-- Food and animals of the self-sufficient farm: an example relational database (SQLite 3.37 or newer).
--
-- Build a file:   sqlite3 farm.db < farm.sql
-- Check:          python3 check.py
--
-- Data come from the project document (projekt/PROJEKT.md, sections 6, 7, 8, 9 and 12)
-- and from the input data of report R2 (obliczenia/R2/dane.py).
-- Names of tables and columns are English; the stored names are Polish, as in the project.

PRAGMA foreign_keys = ON;
BEGIN;

-- ---------------------------------------------------------------- places

CREATE TABLE zone (                       -- project section 7, table "Strefy"
  code     TEXT PRIMARY KEY,
  name     TEXT NOT NULL,
  parcel   TEXT NOT NULL,
  area_m2  INTEGER NOT NULL CHECK (area_m2 > 0)
) STRICT;

-- ---------------------------------------------------------------- food

CREATE TABLE food_group (                 -- rows of the diet table, project section 6
  id    INTEGER PRIMARY KEY,
  name  TEXT NOT NULL UNIQUE
) STRICT;

CREATE TABLE product (                    -- nutrition values: FAO, per 100 g as purchased
  id                  INTEGER PRIMARY KEY,
  name                TEXT NOT NULL UNIQUE,
  food_group_id       INTEGER NOT NULL REFERENCES food_group (id),
  kcal_per_100g       REAL NOT NULL CHECK (kcal_per_100g >= 0),
  protein_g_per_100g  REAL NOT NULL CHECK (protein_g_per_100g BETWEEN 0 AND 100),
  fat_g_per_100g      REAL NOT NULL CHECK (fat_g_per_100g BETWEEN 0 AND 100),
  kg_per_piece        REAL CHECK (kg_per_piece > 0)     -- set only for a product counted in pieces
) STRICT;

CREATE TABLE diet (
  id                   INTEGER PRIMARY KEY,
  name                 TEXT NOT NULL UNIQUE,
  persons              INTEGER NOT NULL CHECK (persons > 0),
  kcal_target_per_day  INTEGER NOT NULL CHECK (kcal_target_per_day > 0)
) STRICT;

CREATE TABLE diet_item (                  -- one adult, one year
  diet_id             INTEGER NOT NULL REFERENCES diet (id),
  product_id          INTEGER NOT NULL REFERENCES product (id),
  kg_per_person_year  REAL NOT NULL CHECK (kg_per_person_year > 0),
  PRIMARY KEY (diet_id, product_id)
) STRICT;

CREATE TABLE storage_place (
  id         INTEGER PRIMARY KEY,
  name       TEXT NOT NULL UNIQUE,
  zone_code  TEXT REFERENCES zone (code),              -- NULL: the project gives no zone
  volume_m3  REAL CHECK (volume_m3 > 0)                -- NULL: the project gives no volume
) STRICT;

CREATE TABLE stock (                      -- 12-month reserve for 4 persons, project section 12
  id          INTEGER PRIMARY KEY,
  name        TEXT NOT NULL UNIQUE,
  place_id    INTEGER NOT NULL REFERENCES storage_place (id),
  kg          INTEGER NOT NULL CHECK (kg > 0),
  conditions  TEXT NOT NULL
) STRICT;

-- ---------------------------------------------------------------- animals

CREATE TABLE animal_kind (                -- parameters of one head; NULL: the project gives no value
  id                      INTEGER PRIMARY KEY,
  name                    TEXT NOT NULL UNIQUE,
  species                 TEXT NOT NULL CHECK (species IN ('kura', 'kaczka', 'gęś', 'koza', 'pszczoła')),
  batches_per_year        INTEGER NOT NULL CHECK (batches_per_year >= 1),
  water_dm3_per_day_low   REAL CHECK (water_dm3_per_day_low >= 0),
  water_dm3_per_day_high  REAL,
  manure_t_per_head_year  REAL CHECK (manure_t_per_head_year > 0),
  manure_n_kg_per_t       REAL CHECK (manure_n_kg_per_t > 0),
  manure_days             INTEGER CHECK (manure_days BETWEEN 1 AND 365),   -- days per year that count for manure
  CHECK (water_dm3_per_day_low <= water_dm3_per_day_high)
) STRICT;

CREATE TABLE animal_output (              -- what one head gives per year: pieces if the product has kg_per_piece, else kg
  kind_id        INTEGER NOT NULL REFERENCES animal_kind (id),
  product_id     INTEGER NOT NULL REFERENCES product (id),
  per_head_low   REAL NOT NULL CHECK (per_head_low > 0),
  per_head_high  REAL NOT NULL,
  PRIMARY KEY (kind_id, product_id),
  CHECK (per_head_low <= per_head_high)
) STRICT;

CREATE TABLE animal_group (
  id         INTEGER PRIMARY KEY,
  name       TEXT NOT NULL UNIQUE,
  zone_code  TEXT NOT NULL REFERENCES zone (code),
  chosen     INTEGER NOT NULL CHECK (chosen IN (0, 1))   -- 1: the owner chose this group on 2026-11-11
) STRICT;

CREATE TABLE group_member (
  group_id        INTEGER NOT NULL REFERENCES animal_group (id),
  kind_id         INTEGER NOT NULL REFERENCES animal_kind (id),
  heads_per_year  INTEGER NOT NULL CHECK (heads_per_year > 0),
  PRIMARY KEY (group_id, kind_id)
) STRICT;

CREATE TABLE feed (
  id    INTEGER PRIMARY KEY,
  name  TEXT NOT NULL UNIQUE
) STRICT;

CREATE TABLE feed_ration (                -- feed for one head: per year, or per stay for a bird kept less than a year
  kind_id      INTEGER NOT NULL REFERENCES animal_kind (id),
  feed_id      INTEGER NOT NULL REFERENCES feed (id),
  kg_per_head  REAL NOT NULL CHECK (kg_per_head > 0),
  PRIMARY KEY (kind_id, feed_id)
) STRICT;

-- ---------------------------------------------------------------- data: places

INSERT INTO zone (code, name, parcel, area_m2) VALUES
  ('S1',  'Siedlisko',                 '16/1',  3382),
  ('S2',  'Warzywnik, tunel, pole P1', '16/1',  1852),
  ('S3',  'Budynek inwentarski',       '16/1',   740),
  ('S4a', 'Pole P2',                   '16/1',  1400),
  ('S4b', 'Sad tarasowy i jagodnik',   '16/1',  2064),
  ('S5',  'Pola P3, P4, P5',           '24/1',  2991),
  ('S6',  'Łąka kośna z pasieką',      '16/3',  2475),
  ('S7',  'Pastwisko kóz',             '16/3',  1852),
  ('S8a', 'Drzewostan opałowy',        '16/3', 13889),
  ('S8b', 'Zadrzewiony stok północny', '16/1',  2261),
  ('S9',  'Pole kempingowe',           '24/1',  5899),
  ('S10', 'Budynki kempingu',          '24/1',  2131),
  ('D',   'Droga',                     '19/3',  1751);

-- ---------------------------------------------------------------- data: food
-- Diet "L" of report R2: 49 products, kg per adult per year (obliczenia/R2/dane.py: DIETA and FAO).

INSERT INTO diet (id, name, persons, kcal_target_per_day) VALUES
  (1, 'Dieta L: gleba lekka, kozy i pszczoły', 4, 3000);

INSERT INTO food_group (id, name) VALUES
  (1, 'Zboża'),
  (2, 'Ziemniaki'),
  (3, 'Strączkowe suche'),
  (4, 'Olej'),
  (5, 'Nasiona oleiste'),
  (6, 'Orzechy w łupinie'),
  (7, 'Warzywa'),
  (8, 'Owoce'),
  (9, 'Jaja'),
  (10, 'Mięso drobiowe (tuszki)'),
  (11, 'Mleko kozie'),
  (12, 'Miód');

INSERT INTO product (id, name, food_group_id, kcal_per_100g, protein_g_per_100g, fat_g_per_100g, kg_per_piece) VALUES
  ( 1, 'Pszenica: mąka razowa, kasze', 1, 334, 12.2, 2.3, NULL),
  ( 2, 'Żyto: mąka razowa', 1, 319, 11, 1.9, NULL),
  ( 3, 'Owies nagi: płatki, kasza', 1, 385, 13, 7.5, NULL),
  ( 4, 'Gryka: kasza', 1, 330, 11, 2, NULL),
  ( 5, 'Proso: kasza jaglana', 1, 340, 9.7, 3, NULL),
  ( 6, 'Ziemniaki', 2, 67, 1.6, 0.1, NULL),
  ( 7, 'Fasola sucha', 3, 341, 22.1, 1.7, NULL),
  ( 8, 'Groch suchy', 3, 346, 22.5, 1.8, NULL),
  ( 9, 'Bób suchy', 3, 343, 23.4, 2, NULL),
  (10, 'Olej lniankowy (rydzowy) tłoczony na zimno', 4, 884, 0, 100, NULL),
  (11, 'Siemię lniane', 5, 498, 18, 34, NULL),
  (12, 'Słonecznik: nasiona w łusce', 5, 308, 12.3, 26.8, NULL),
  (13, 'Pestki dyni oleistej', 5, 400, 18.2, 33.9, NULL),
  (14, 'Mak', 5, 533, 18, 44.7, NULL),
  (15, 'Orzechy włoskie w łupinie', 6, 289, 6.4, 27.8, NULL),
  (16, 'Orzechy laskowe w łupinie', 6, 291, 6, 28.8, NULL),
  (17, 'Kapusta (świeża i kiszona)', 7, 19, 1, 0.1, NULL),
  (18, 'Marchew', 7, 38, 0.9, 0.2, NULL),
  (19, 'Burak ćwikłowy', 7, 22, 1.4, 0.2, NULL),
  (20, 'Cebula', 7, 31, 1.1, 0.2, NULL),
  (21, 'Czosnek', 7, 130, 5.5, 0.4, NULL),
  (22, 'Por', 7, 37, 0.7, 0.1, NULL),
  (23, 'Pietruszka korzeniowa', 7, 22, 1.4, 0.2, NULL),
  (24, 'Seler korzeniowy', 7, 22, 1.4, 0.2, NULL),
  (25, 'Brukiew, rzepa', 7, 22, 1.4, 0.2, NULL),
  (26, 'Jarmuż', 7, 22, 1.4, 0.2, NULL),
  (27, 'Ogórek', 7, 13, 0.5, 0.1, NULL),
  (28, 'Cukinia', 7, 19, 0.9, 0.1, NULL),
  (29, 'Dynia zimowa', 7, 19, 0.9, 0.1, NULL),
  (30, 'Fasola szparagowa, groszek zielony', 7, 22, 1.4, 0.2, NULL),
  (31, 'Pomidor (tunel)', 7, 17, 0.8, 0.2, NULL),
  (32, 'Papryka (tunel)', 7, 25, 1.1, 0.3, NULL),
  (33, 'Sałata, szpinak, roszponka (tunel)', 7, 12, 1.1, 0.2, NULL),
  (34, 'Jabłka', 8, 48, 0.1, 0.3, NULL),
  (35, 'Gruszki', 8, 54, 0.4, 0.4, NULL),
  (36, 'Śliwki', 8, 52, 0.7, 0.6, NULL),
  (37, 'Wiśnie', 8, 45, 0.9, 0.3, NULL),
  (38, 'Porzeczki', 8, 59, 1.4, 0.3, NULL),
  (39, 'Maliny', 8, 47, 0.9, 0.5, NULL),
  (40, 'Truskawki', 8, 28, 0.6, 0.4, NULL),
  (41, 'Aronia', 8, 49, 1, 0.7, NULL),
  (42, 'Borówka wysoka', 8, 55, 0.7, 0.4, NULL),
  (43, 'Winogrona', 8, 53, 0.5, 0.4, NULL),
  (44, 'Jaja kurze', 9, 139, 10.7, 9.8, 0.058),
  (45, 'Kurczak: tuszka', 10, 122, 12.3, 7.7, NULL),
  (46, 'Kaczka: tuszka', 10, 291, 8.3, 28.3, NULL),
  (47, 'Gęś: tuszka', 10, 301, 12.9, 27.2, NULL),
  (48, 'Mleko kozie', 11, 69, 3.6, 4.1, NULL),
  (49, 'Miód', 12, 298, 0.4, 0, NULL);

INSERT INTO diet_item (diet_id, product_id, kg_per_person_year) VALUES
  (1,  1, 10),
  (1,  2, 58),
  (1,  3, 28),
  (1,  4, 8),
  (1,  5, 8),
  (1,  6, 170),
  (1,  7, 9),
  (1,  8, 9),
  (1,  9, 3),
  (1, 10, 10),
  (1, 11, 2),
  (1, 12, 4),
  (1, 13, 3),
  (1, 14, 2),
  (1, 15, 4),
  (1, 16, 4),
  (1, 17, 45),
  (1, 18, 30),
  (1, 19, 20),
  (1, 20, 18),
  (1, 21, 2),
  (1, 22, 8),
  (1, 23, 5),
  (1, 24, 6),
  (1, 25, 6),
  (1, 26, 10),
  (1, 27, 15),
  (1, 28, 10),
  (1, 29, 20),
  (1, 30, 6),
  (1, 31, 25),
  (1, 32, 4),
  (1, 33, 8),
  (1, 34, 60),
  (1, 35, 8),
  (1, 36, 10),
  (1, 37, 6),
  (1, 38, 6),
  (1, 39, 5),
  (1, 40, 8),
  (1, 41, 2),
  (1, 42, 3),
  (1, 43, 4),
  (1, 44, 17.4),
  (1, 45, 22),
  (1, 46, 5),
  (1, 47, 4.5),
  (1, 48, 250),
  (1, 49, 8);

INSERT INTO storage_place (id, name, zone_code, volume_m3) VALUES
  (1, 'Spichlerz suchy',   NULL,  6.0),
  (2, 'Piwnica ziemna M1', 'S4b', 17.6),
  (3, 'Komora sucha',      NULL,  NULL);

INSERT INTO stock (id, name, place_id, kg, conditions) VALUES
  ( 1, 'Ziarno zbóż',                                1, 499, 'Wilgotność ziarna co najwyżej 14%. Temperatura co najwyżej 15 °C.'),
  ( 2, 'Strączkowe suche',                           1,  88, 'Worki. Temperatura od 4 °C do 10 °C.'),
  ( 3, 'Nasiona oleiste',                            1, 211, 'Tłoczenie oleju co 1 do 2 miesięcy.'),
  ( 4, 'Orzechy w łupinie',                          1,  32, 'Skrzynki z przewiewem.'),
  ( 5, 'Ziemniaki jadalne i sadzeniaki',             2, 918, 'Od 4 °C do 6 °C. Wilgotność powietrza od 90% do 95%.'),
  ( 6, 'Marchew, burak, seler, pietruszka, brukiew', 2, 201, 'Od 0 °C do 1 °C. Skrzynie z piaskiem.'),
  ( 7, 'Kapusta świeża i kiszona',                   2, 160, 'Beczka albo kamionka.'),
  ( 8, 'Jabłka i gruszki',                           2, 163, 'Osobna komora. Od −1 °C do 4 °C.'),
  ( 9, 'Cebula i czosnek',                           3,  60, '0 °C. Wilgotność powietrza od 65% do 75%.'),
  (10, 'Dynia zimowa',                               3,  60, 'Od 10 °C do 13 °C.'),
  (11, 'Przetwory w słoikach',                       2, 160, 'Pasteryzacja pomidorów, ogórków i owoców.'),
  (12, 'Susz i miód',                                1,  52, 'Temperatura mniejsza niż 18 °C.');

-- ---------------------------------------------------------------- data: animals
-- Parameters of one head: obliczenia/R2/dane.py (WODA_L_DOBA, OBORNIK) and R3 section C7 (goat water).

INSERT INTO animal_kind
  (id, name, species, batches_per_year, water_dm3_per_day_low, water_dm3_per_day_high,
   manure_t_per_head_year, manure_n_kg_per_t, manure_days) VALUES
  ( 1, 'Nioska bez doświetlania', 'kura',     1, 0.25, 0.25, 0.029, 20.7, 365),
  ( 2, 'Nioska z doświetlaniem',  'kura',     1, 0.25, 0.25, 0.029, 20.7, 365),
  ( 3, 'Kogut',                   'kura',     1, 0.25, 0.25, 0.029, 20.7, 365),
  ( 4, 'Kurka na remont stada',   'kura',     1, 0.25, 0.25, 0.008, 15.7, 365),
  ( 5, 'Kogutek z wylęgu',        'kura',     1, 0.25, 0.25, 0.008, 15.7, 365),
  ( 6, 'Kurczę rzeźne',           'kura',     2, 0.35, 0.35, 0.017, 24.7,  81),
  ( 7, 'Kaczka pekin',            'kaczka',   2, 1.0,  1.0,  0.026, 22.8,  56),
  ( 8, 'Gęś biała kołudzka',      'gęś',      1, 1.5,  1.5,  0.030, 21.8, 119),
  ( 9, 'Koza mleczna',            'koza',     1, 4.0,  10.0, NULL,  NULL, NULL),
  (10, 'Rodzina pszczela',        'pszczoła', 1, NULL, NULL, NULL,  NULL, NULL);

-- Carcass = live mass x dressing share (obliczenia/R2/c_drob.py). The culled hen is booked on the pullet that replaces it.
INSERT INTO animal_output (kind_id, product_id, per_head_low, per_head_high) VALUES
  ( 1, 44, 160,         160),           -- eggs, pieces
  ( 2, 44, 190,         190),
  ( 4, 45, 1.8 * 0.64,  1.8 * 0.64),    -- culled hen
  ( 5, 45, 2.5 * 0.64,  2.5 * 0.64),
  ( 6, 45, 3.08 * 0.73, 3.08 * 0.73),
  ( 7, 46, 3.35 * 0.71, 3.35 * 0.71),
  ( 8, 47, 4.47,        4.47),
  ( 9, 48, 600,         1400),          -- milk, kg
  (10, 49, 11,          17);            -- honey, kg

INSERT INTO animal_group (id, name, zone_code, chosen) VALUES
  (1, 'Stado domowe', 'S3', 0),
  (2, 'Stado pełne',  'S3', 1),
  (3, 'Kozy mleczne', 'S3', 1),
  (4, 'Pasieka U1',   'S6', 1);

INSERT INTO group_member (group_id, kind_id, heads_per_year) VALUES
  (1, 1,  9), (1, 3, 1), (1, 4,  5), (1, 5, 5), (1, 6, 34), (1, 7,  9), (1, 8,  5),
  (2, 2, 54), (2, 3, 4), (2, 4, 10),            (2, 6, 24), (2, 7, 16), (2, 8, 12),
  (3, 9,  2),
  (4, 10, 3);

INSERT INTO feed (id, name) VALUES
  (1, 'Pasza treściwa'),
  (2, 'Siano');

INSERT INTO feed_ration (kind_id, feed_id, kg_per_head) VALUES
  (1, 1, 0.120 * 365), (2, 1, 0.120 * 365), (3, 1, 0.120 * 365),
  (4, 1, 8.0), (5, 1, 9.0), (6, 1, 6.3), (7, 1, 11.1), (8, 1, 35.0),
  (9, 1, 200.0 / 2), (9, 2, 1262.0 / 2);

-- ---------------------------------------------------------------- views

CREATE VIEW v_diet_day AS                 -- energy and macronutrients of one adult per day
SELECT d.id AS diet_id, d.name AS diet, d.persons, d.kcal_target_per_day,
       sum(i.kg_per_person_year * 10 * p.kcal_per_100g) / 365      AS kcal_per_day,
       sum(i.kg_per_person_year * 10 * p.protein_g_per_100g) / 365 AS protein_g_per_day,
       sum(i.kg_per_person_year * 10 * p.fat_g_per_100g) / 365     AS fat_g_per_day
FROM diet d
JOIN diet_item i ON i.diet_id = d.id
JOIN product p   ON p.id = i.product_id
GROUP BY d.id;

CREATE VIEW v_group_output AS             -- yearly output of a group; "amount" is in "unit", "kg" is always kg
SELECT g.id AS group_id, g.name AS animal_group, p.id AS product_id, p.name AS product,
       CASE WHEN p.kg_per_piece IS NULL THEN 'kg' ELSE 'szt.' END              AS unit,
       sum(m.heads_per_year * o.per_head_low)                               AS amount_low,
       sum(m.heads_per_year * o.per_head_high)                              AS amount_high,
       sum(m.heads_per_year * o.per_head_low  * coalesce(p.kg_per_piece, 1)) AS kg_low,
       sum(m.heads_per_year * o.per_head_high * coalesce(p.kg_per_piece, 1)) AS kg_high
FROM animal_group g
JOIN group_member m  ON m.group_id = g.id
JOIN animal_output o ON o.kind_id = m.kind_id
JOIN product p       ON p.id = o.product_id
GROUP BY g.id, p.id;

CREATE VIEW v_group_load AS               -- heads at the peak, water at the peak, manure and nitrogen per year
SELECT g.id AS group_id, g.name AS animal_group,
       sum((m.heads_per_year + k.batches_per_year - 1) / k.batches_per_year)                              AS heads_at_peak,
       sum((m.heads_per_year + k.batches_per_year - 1) / k.batches_per_year * k.water_dm3_per_day_low)    AS water_dm3_per_day_low,
       sum((m.heads_per_year + k.batches_per_year - 1) / k.batches_per_year * k.water_dm3_per_day_high)   AS water_dm3_per_day_high,
       sum(m.heads_per_year * k.manure_t_per_head_year * k.manure_days / 365.0)                           AS manure_t,
       sum(m.heads_per_year * k.manure_t_per_head_year * k.manure_days / 365.0 * k.manure_n_kg_per_t)     AS manure_n_kg
FROM animal_group g
JOIN group_member m ON m.group_id = g.id
JOIN animal_kind k  ON k.id = m.kind_id
GROUP BY g.id;

CREATE VIEW v_group_feed AS               -- feed of a group per year
SELECT g.id AS group_id, g.name AS animal_group, f.id AS feed_id, f.name AS feed,
       sum(m.heads_per_year * r.kg_per_head) AS kg_per_year
FROM animal_group g
JOIN group_member m ON m.group_id = g.id
JOIN feed_ration r  ON r.kind_id = m.kind_id
JOIN feed f         ON f.id = r.feed_id
GROUP BY g.id, f.id;

COMMIT;

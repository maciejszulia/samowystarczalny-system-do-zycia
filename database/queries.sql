-- Example queries for farm.sql. check.py runs every query and prints the result.
-- A query starts with a line "-- Qn: title" and ends with a semicolon.

-- Q1: Energia i makroskładniki diety na 1 osobę na dobę
SELECT diet                                     AS "dieta",
       persons                                  AS "osoby",
       CAST(round(kcal_per_day) AS INTEGER)     AS "energia [kcal]",
       kcal_target_per_day                      AS "cel [kcal]",
       CAST(round(protein_g_per_day) AS INTEGER) AS "białko [g]",
       CAST(round(fat_g_per_day) AS INTEGER)    AS "tłuszcz [g]"
FROM v_diet_day;

-- Q2: Dieta roczna 1 osoby według grup
SELECT g.name                                                                   AS "grupa",
       count(*)                                                                 AS "produkty",
       round(sum(i.kg_per_person_year), 1)                                      AS "masa [kg na rok]",
       CAST(round(sum(i.kg_per_person_year * 10 * p.kcal_per_100g) / 365) AS INTEGER) AS "energia [kcal na dobę]"
FROM diet_item i
JOIN product p    ON p.id = i.product_id
JOIN food_group g ON g.id = p.food_group_id
WHERE i.diet_id = 1
GROUP BY g.id
ORDER BY g.id;

-- Q3: 5 produktów, które dają najwięcej energii
WITH energy AS (
  SELECT p.name, i.kg_per_person_year * 10 * p.kcal_per_100g / 365 AS kcal
  FROM diet_item i
  JOIN product p ON p.id = i.product_id
  WHERE i.diet_id = 1
)
SELECT name                                                                         AS "produkt",
       CAST(round(kcal) AS INTEGER)                                                 AS "energia [kcal na dobę]",
       round(100 * kcal / sum(kcal) OVER (), 1)                                     AS "udział [%]",
       round(100 * sum(kcal) OVER (ORDER BY kcal DESC, name) / sum(kcal) OVER (), 1) AS "udział narastający [%]"
FROM energy
ORDER BY kcal DESC, name
LIMIT 5;

-- Q4: Grupy zwierząt: sztuki, woda, pasza, obornik
SELECT l.animal_group                         AS "grupa",
       l.heads_at_peak                        AS "sztuki w szczycie",
       round(l.water_dm3_per_day_low, 1)      AS "woda od [dm³ na dobę]",
       round(l.water_dm3_per_day_high, 1)     AS "woda do [dm³ na dobę]",
       round(f.kg_per_year / 1000, 2)         AS "pasza treściwa [t na rok]",
       round(l.manure_t, 2)                   AS "obornik [t na rok]",
       CAST(round(l.manure_n_kg) AS INTEGER)  AS "azot [kg na rok]"
FROM v_group_load l
LEFT JOIN v_group_feed f ON f.group_id = l.group_id AND f.feed = 'Pasza treściwa'
ORDER BY l.group_id;

-- Q5: Produkcja grup zwierząt na rok
SELECT animal_group           AS "grupa",
       product                AS "produkt",
       round(amount_low, 1)   AS "ilość od",
       round(amount_high, 1)  AS "ilość do",
       unit                   AS "jednostka"
FROM v_group_output
ORDER BY group_id, product_id;

-- Q6: Bilans produktów zwierzęcych: potrzeba 4 osób i produkcja grup wybranych przez właściciela
WITH need AS (
  SELECT i.product_id, i.kg_per_person_year * d.persons AS kg
  FROM diet_item i
  JOIN diet d ON d.id = i.diet_id
  WHERE d.id = 1
), made AS (
  SELECT o.product_id, sum(o.kg_low) AS kg_low, sum(o.kg_high) AS kg_high
  FROM v_group_output o
  JOIN animal_group g ON g.id = o.group_id
  WHERE g.chosen = 1
  GROUP BY o.product_id
)
SELECT p.name                      AS "produkt",
       round(n.kg, 1)              AS "potrzeba [kg na rok]",
       round(m.kg_low, 1)          AS "produkcja od [kg]",
       round(m.kg_high, 1)         AS "produkcja do [kg]",
       round(m.kg_low - n.kg, 1)   AS "bilans od [kg]",
       round(m.kg_high - n.kg, 1)  AS "bilans do [kg]"
FROM made m
JOIN need n    ON n.product_id = m.product_id
JOIN product p ON p.id = m.product_id
ORDER BY p.id;

-- Q7: Nadwyżka jaj stada pełnego
SELECT CAST(o.amount_low AS INTEGER)                    AS "produkcja [szt. na rok]",
       CAST(round(n.pieces) AS INTEGER)                 AS "potrzeba 4 osób [szt. na rok]",
       CAST(round((o.amount_low - n.pieces) / 52) AS INTEGER) AS "nadwyżka [szt. na tydzień]"
FROM v_group_output o
JOIN (
  SELECT i.product_id, i.kg_per_person_year * d.persons / p.kg_per_piece AS pieces
  FROM diet_item i
  JOIN diet d    ON d.id = i.diet_id
  JOIN product p ON p.id = i.product_id
  WHERE d.id = 1 AND p.kg_per_piece IS NOT NULL
) n ON n.product_id = o.product_id
WHERE o.animal_group = 'Stado pełne';

-- Q8: Zapasy na 12 miesięcy według miejsca
SELECT s.name                                               AS "miejsce",
       s.zone_code                                          AS "strefa",
       count(*)                                             AS "pozycje",
       sum(t.kg)                                            AS "masa [kg]",
       round(100.0 * sum(t.kg) / sum(sum(t.kg)) OVER (), 1) AS "udział [%]"
FROM stock t
JOIN storage_place s ON s.id = t.place_id
GROUP BY s.id
ORDER BY sum(t.kg) DESC;

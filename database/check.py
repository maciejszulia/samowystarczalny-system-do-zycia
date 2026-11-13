#!/usr/bin/env python3
"""Build the example database in memory, test it against the project, show the query results.

Run from this directory:
    python3 check.py            # build, test, print the results of queries.sql as Markdown
    python3 check.py --check    # also fail if README.md shows other queries or other results
    python3 check.py --erd      # also draw erd.png from the schema (needs matplotlib)

The tests compare the database with the numbers of projekt/PROJEKT.md and with the
functions of report R2 (obliczenia/R2), which compute the same values in Python.
Requires: Python 3 with SQLite 3.37 or newer. No other package for the tests.
"""
import contextlib
import io
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R2 = HERE.parent / "obliczenia" / "R2"

# Statements that the database must reject: (what the statement tries, SQL).
REJECTED = [
    ("Pozycja diety z produktem, którego tabela `product` nie zawiera.",
     "INSERT INTO diet_item (diet_id, product_id, kg_per_person_year) VALUES (1, 999, 5)"),
    ("Zapas o masie ujemnej.",
     "INSERT INTO stock (name, place_id, kg, conditions) VALUES ('Mąka', 1, -5, 'brak')"),
    ("Drugi wiersz dla tej samej pary: grupa i rodzaj zwierzęcia.",
     "INSERT INTO group_member (group_id, kind_id, heads_per_year) VALUES (2, 2, 10)"),
    ("Usunięcie produktu, którego używa dieta.",
     "DELETE FROM product WHERE name = 'Jaja kurze'"),
    ("Tekst w kolumnie liczbowej.",
     "UPDATE zone SET area_m2 = 'siedemset' WHERE code = 'S3'"),
]


def build():
    con = sqlite3.connect(":memory:")
    con.executescript((HERE / "farm.sql").read_text(encoding="utf-8"))
    return con


def queries():
    """(id, title, sql) for every query of queries.sql."""
    text = (HERE / "queries.sql").read_text(encoding="utf-8")
    found = re.findall(r"^-- (Q\d+): (.+?)\n(.+?;)\s*$", text, flags=re.M | re.S)
    assert len(found) == len(re.findall(r"^-- Q\d+:", text, flags=re.M)), "queries.sql: a query without its semicolon"
    return [(qid, title.strip(), sql.strip()) for qid, title, sql in found]


def one(con, sql, *args):
    return con.execute(sql, args).fetchone()


def schema(con):
    """Tables with their columns, and the foreign keys, read from the database itself."""
    tables, links = {}, []
    for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"):
        fks = {row[3]: row[2] for row in con.execute(f"PRAGMA foreign_key_list({name})")}
        tables[name] = [(col[1], "PK" if col[5] else "", fks.get(col[1])) for col in con.execute(f"PRAGMA table_info({name})")]
        links += [(name, column, parent) for column, parent in fks.items()]
    return tables, sorted(links)


def test_project(con):
    """The database gives the numbers of the project document (section in the comment)."""
    assert one(con, "PRAGMA foreign_key_check") is None
    assert one(con, "PRAGMA integrity_check") == ("ok",)
    tables, links = schema(con)
    assert (len(tables), len(links)) == (13, 12)

    kcal, protein, fat = one(con, "SELECT kcal_per_day, protein_g_per_day, fat_g_per_day FROM v_diet_day")
    assert (round(kcal), round(protein)) == (3037, 110)                    # section 6
    assert round(fat) == 102          # section 6 says 103 g; the R2 calculation gives 102.4 g
    groups = dict(con.execute("""SELECT g.name, round(sum(i.kg_per_person_year), 1) FROM diet_item i
                                 JOIN product p ON p.id = i.product_id JOIN food_group g ON g.id = p.food_group_id
                                 GROUP BY g.id"""))
    assert groups == {"Zboża": 112, "Ziemniaki": 170, "Strączkowe suche": 21, "Olej": 10, "Nasiona oleiste": 11,
                      "Orzechy w łupinie": 8, "Warzywa": 238, "Owoce": 112, "Jaja": 17.4,
                      "Mięso drobiowe (tuszki)": 31.5, "Mleko kozie": 250, "Miód": 8}             # section 6
    assert round(17.4 / one(con, "SELECT kg_per_piece FROM product WHERE name = 'Jaja kurze'")[0]) == 300

    def flock(name):
        peak, water, manure, nitrogen = one(con, """SELECT heads_at_peak, water_dm3_per_day_high, manure_t, manure_n_kg
                                                     FROM v_group_load WHERE animal_group = ?""", name)
        eggs = one(con, "SELECT amount_low FROM v_group_output WHERE animal_group = ? AND unit = 'szt.'", name)[0]
        meat = one(con, "SELECT sum(kg_low) FROM v_group_output WHERE animal_group = ? AND unit = 'kg'", name)[0]
        feed = one(con, "SELECT kg_per_year FROM v_group_feed WHERE animal_group = ? AND feed = 'Pasza treściwa'", name)[0]
        return peak, round(eggs), round(meat), round(feed / 1000, 2), round(manure, 2), round(nitrogen), round(water, 1)

    assert flock("Stado domowe")[:6] == (47, 1440, 134, 1.01, 0.58, 12)    # section 8
    assert flock("Stado pełne") == (100, 10260, 157, 3.37, 2.03, 42, 47.2)  # section 8: "co najwyżej 47 dm³"
    assert one(con, "SELECT amount_low, amount_high FROM v_group_output WHERE product = 'Mleko kozie'") == (1200, 2800)
    assert one(con, "SELECT amount_low, amount_high FROM v_group_output WHERE product = 'Miód'") == (33, 51)   # section 9
    assert one(con, "SELECT kg_per_year FROM v_group_feed WHERE feed = 'Siano'") == (1262,)                    # section 9
    assert one(con, "SELECT sum(kg), count(*) FROM stock") == (2604, 12)                                       # section 12
    assert one(con, "SELECT count(*) FROM zone") == (13,) and abs(one(con, "SELECT sum(area_m2) FROM zone")[0] - 42689) <= 5
    return len(tables), len(links)


def test_r2(con):
    """The SQL views give the same values as the Python functions of report R2."""
    sys.path.insert(0, str(R2))
    with contextlib.redirect_stdout(io.StringIO()):
        import a_dieta
        import c_drob
    total = a_dieta.policz(2)[1]
    kcal, protein, fat = one(con, "SELECT kcal_per_day, protein_g_per_day, fat_g_per_day FROM v_diet_day")
    assert max(abs(kcal - total["kcal"] / 365), abs(protein - total["b"] * 1000 / 365), abs(fat - total["t"] * 1000 / 365)) < 1e-9

    r2_name = {"Nioska bez doświetlania": "nioski", "Nioska z doświetlaniem": "nioski", "Kogut": "koguty",
               "Kurka na remont stada": "kurki", "Kogutek z wylęgu": "kogutki", "Kurczę rzeźne": "brojlery",
               "Kaczka pekin": "kaczki", "Gęś biała kołudzka": "gesi"}
    for group in ("Stado domowe", "Stado pełne"):
        flock = dict.fromkeys(r2_name.values(), 0)
        for kind, heads in con.execute("""SELECT k.name, m.heads_per_year FROM group_member m JOIN animal_kind k ON k.id = m.kind_id
                                          JOIN animal_group g ON g.id = m.group_id WHERE g.name = ?""", (group,)):
            flock[r2_name[kind]] = heads
        eggs_per_hen = one(con, """SELECT o.per_head_low FROM animal_output o JOIN group_member m ON m.kind_id = o.kind_id
                                   JOIN animal_group g ON g.id = m.group_id JOIN product p ON p.id = o.product_id
                                   WHERE g.name = ? AND p.kg_per_piece IS NOT NULL""", group)[0]
        made = c_drob.produkcja(flock, eggs_per_hen)
        manure = c_drob.obornik(flock)
        peak, water, manure_t, nitrogen = one(con, """SELECT heads_at_peak, water_dm3_per_day_high, manure_t, manure_n_kg
                                                       FROM v_group_load WHERE animal_group = ?""", group)
        eggs = one(con, "SELECT amount_low FROM v_group_output WHERE animal_group = ? AND unit = 'szt.'", group)[0]
        meat = one(con, "SELECT sum(kg_low) FROM v_group_output WHERE animal_group = ? AND unit = 'kg'", group)[0]
        feed = one(con, "SELECT kg_per_year FROM v_group_feed WHERE animal_group = ? AND feed = 'Pasza treściwa'", group)[0]
        pairs = [(peak, c_drob.szczyt(flock)), (water, c_drob.woda(flock)), (manure_t, manure[0]), (nitrogen, manure[1]),
                 (eggs, made["jaja"]), (meat, made["mieso"]), (feed, sum(c_drob.pasza(flock).values()))]
        assert all(abs(sql - python) < 1e-9 for sql, python in pairs), (group, pairs)
    return 3 + 2 * 7


def rejections(con):
    """Run every statement of REJECTED and return the error message of the database."""
    messages = []
    for _, sql in REJECTED:
        try:
            con.execute(sql)
        except sqlite3.IntegrityError as error:
            messages.append(str(error))
        else:
            raise AssertionError(f"the database accepted: {sql}")
        con.rollback()
    return messages


def cell(value):
    """Polish notation: decimal comma, space between thousands, 'brak' for NULL."""
    if value is None:
        return "brak"
    if isinstance(value, int):
        return f"{value:,}".replace(",", " ")
    if isinstance(value, float):
        whole, _, rest = repr(value).partition(".")
        return f"{int(whole):,}".replace(",", " ").replace("-", "−") + "," + rest if whole != "-0" else "−0," + rest
    return str(value)


def table(cursor):
    head = [d[0] for d in cursor.description]
    rows = [[cell(v) for v in row] for row in cursor]
    return "\n".join("| " + " | ".join(r) + " |" for r in [head, ["---"] * len(head)] + rows)


def report(con):
    """Markdown: every query with its result, then every rejected statement with its error."""
    parts = []
    for qid, title, sql in queries():
        parts.append(f"### {qid}. {title}\n\n```sql\n{sql}\n```\n\n{table(con.execute(sql))}")
    lines = ["| Nr | Próba | Polecenie | Odpowiedź bazy |", "| --- | --- | --- | --- |"]
    for number, ((what, sql), message) in enumerate(zip(REJECTED, rejections(con)), 1):
        lines.append(f"| {number} | {what} | `{sql}` | `{message}` |")
    return parts, "\n".join(lines)


def facts(con, n_r2):
    """Numbers that the prose of README.md quotes, formatted as in the document."""
    tables, links = schema(con)
    rows = sum(one(con, f"SELECT count(*) FROM {t}")[0] for t in tables)
    views = one(con, "SELECT count(*) FROM sqlite_master WHERE type = 'view'")[0]
    no_data = sum(one(con, f"SELECT count(*) FROM {t} WHERE {c} IS NULL")[0] for t, c in (
        ("animal_kind", "water_dm3_per_day_low"), ("animal_kind", "water_dm3_per_day_high"),
        ("animal_kind", "manure_t_per_head_year"), ("animal_kind", "manure_n_kg_per_t"), ("animal_kind", "manure_days"),
        ("storage_place", "zone_code"), ("storage_place", "volume_m3")))
    balance = dict(con.execute("""SELECT p.name, sum(o.kg_low) - (SELECT i.kg_per_person_year * d.persons FROM diet_item i
                                  JOIN diet d ON d.id = i.diet_id WHERE i.product_id = p.id)
                                  FROM v_group_output o JOIN animal_group g ON g.id = o.group_id JOIN product p ON p.id = o.product_id
                                  WHERE g.chosen = 1 GROUP BY p.id"""))
    chicken = one(con, "SELECT sum(kg_low) FROM v_group_output WHERE animal_group = 'Stado pełne' AND product = 'Kurczak: tuszka'")[0]
    top5 = one(con, """SELECT 100 * sum(kcal) / (SELECT sum(i.kg_per_person_year * p.kcal_per_100g) FROM diet_item i JOIN product p ON p.id = i.product_id)
                       FROM (SELECT i.kg_per_person_year * p.kcal_per_100g AS kcal FROM diet_item i JOIN product p ON p.id = i.product_id
                             ORDER BY kcal DESC LIMIT 5)""")[0]
    cellar, share = one(con, """SELECT sum(kg), 100.0 * sum(kg) / (SELECT sum(kg) FROM stock) FROM stock t
                                JOIN storage_place s ON s.id = t.place_id WHERE s.name = 'Piwnica ziemna M1'""")
    fat = one(con, "SELECT fat_g_per_day FROM v_diet_day")[0]
    return [f"{len(tables)} tabel", f"{len(links)} kluczy FOREIGN KEY", f"{rows} wierszy", f"{views} obiekty VIEW",
            f"{len(queries())} zapytań", f"{one(con, 'SELECT count(*) FROM product')[0]} produktów", f"{n_r2} wartości",
            f"{len(REJECTED)} poleceń", f"{no_data} wartości NULL",
            f"{cell(round(chicken, 1))} kg", f"{cell(round(-balance['Kurczak: tuszka'], 1))} kg",
            f"{cell(round(balance['Kaczka: tuszka'], 1))} kg", f"{cell(round(balance['Gęś: tuszka'], 1))} kg",
            f"{cell(round(top5, 1))}%", f"{cell(int(cellar))} kg", f"{cell(round(share, 1))}%",
            f"{round(fat)} g", f"{cell(round(fat, 1))} g"]


# ---------------------------------------------------------------- diagram
GRID = {  # table: (column, row); every foreign key joins 2 neighbours, so every line is 1 straight segment
    "food_group": (0, 0), "product": (1, 0), "diet_item": (2, 0), "diet": (3, 0),
    "feed": (0, 1), "animal_output": (1, 1),
    "feed_ration": (0, 2), "animal_kind": (1, 2), "group_member": (2, 2), "animal_group": (3, 2),
    "stock": (1, 3), "storage_place": (2, 3), "zone": (3, 3),
}
COLOUR = {"food": "#e3f1e3", "animal": "#fde9d6", "place": "#e6ecf5"}
PART = {"food_group": "food", "product": "food", "diet": "food", "diet_item": "food", "stock": "food",
        "animal_kind": "animal", "animal_output": "animal", "animal_group": "animal", "group_member": "animal",
        "feed": "animal", "feed_ration": "animal", "storage_place": "place", "zone": "place"}


def erd(con):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    tables, links = schema(con)
    assert set(tables) == set(GRID)
    for child, _, parent in links:
        (c0, r0), (c1, r1) = GRID[child], GRID[parent]
        assert abs(c0 - c1) + abs(r0 - r1) == 1, f"{child} and {parent} are not neighbours on the grid"

    width, line, head, gap_x, gap_y = 3.9, 0.36, 0.52, 1.5, 1.2
    height = {t: head + line * len(cols) + 0.16 for t, cols in tables.items()}
    row_h = [max(height[t] for t, (_, r) in GRID.items() if r == row) for row in range(4)]
    row_mid, y = [], 0.0
    for h in row_h:                      # rows go down the page
        row_mid.append(y - h / 2)
        y -= h + gap_y
    page_bottom = y + gap_y              # lower edge of the last row
    col_mid = [c * (width + gap_x) + width / 2 for c in range(4)]
    box = {t: (col_mid[c] - width / 2, row_mid[r] - height[t] / 2, width, height[t]) for t, (c, r) in GRID.items()}

    fig, ax = plt.subplots(figsize=(13.2, 10.4), dpi=130)
    for child, column, parent in links:
        (x0, y0, w0, h0), (x1, y1, w1, h1) = box[child], box[parent]
        if GRID[child][1] == GRID[parent][1]:                 # same row: horizontal segment
            mid = row_mid[GRID[child][1]]
            left, right = (x0 + w0, x1) if x0 < x1 else (x1 + w1, x0)
            ax.plot([left, right], [mid, mid], color="black", lw=1.4, zorder=1)
            near_child, near_parent = (left, right) if x0 < x1 else (right, left)
            ax.text(near_child + (0.18 if x0 < x1 else -0.18), mid + 0.12, "N", ha="center", fontsize=9)
            ax.text(near_parent + (-0.18 if x0 < x1 else 0.18), mid + 0.12, "1", ha="center", fontsize=9)
        else:                                                 # same column: vertical segment
            mid = col_mid[GRID[child][0]]
            top, bottom = (y0, y1 + h1) if y0 > y1 else (y1, y0 + h0)
            ax.plot([mid, mid], [top, bottom], color="black", lw=1.4, zorder=1)
            near_child, near_parent = (top, bottom) if y0 > y1 else (bottom, top)
            ax.text(mid + 0.16, near_child + (-0.22 if y0 > y1 else 0.1), "N", ha="left", fontsize=9)
            ax.text(mid + 0.16, near_parent + (0.1 if y0 > y1 else -0.22), "1", ha="left", fontsize=9)
    for name, (x, y, w, h) in box.items():
        ax.add_patch(Rectangle((x, y), w, h, fc=COLOUR[PART[name]], ec="black", lw=1.3, zorder=2))
        ax.plot([x, x + w], [y + h - head, y + h - head], color="black", lw=0.9, zorder=3)
        ax.text(x + w / 2, y + h - head / 2, name, ha="center", va="center", fontsize=10.5, weight="bold", zorder=3)
        for i, (column, key, parent) in enumerate(tables[name]):
            cy = y + h - head - line * (i + 0.5) - 0.06
            mark = "PK, FK" if key and parent else key or ("FK" if parent else "")
            ax.text(x + 0.12, cy, mark, va="center", fontsize=7.6, zorder=3)
            ax.text(x + 0.98, cy, column, va="center", fontsize=8.6, zorder=3)
    legend_x, legend_y = col_mid[2] - width / 2 + 0.2, row_mid[1] + 0.75
    for i, (part, text) in enumerate((("food", "żywność: dieta, produkty, zapasy"), ("animal", "zwierzęta: rodzaje, grupy, produkcja, pasza"),
                                      ("place", "miejsca: strefy i magazyny"))):
        ax.add_patch(Rectangle((legend_x, legend_y - i * 0.5 - 0.15), 0.5, 0.3, fc=COLOUR[part], ec="black", lw=1))
        ax.text(legend_x + 0.7, legend_y - i * 0.5, text, va="center", fontsize=9)
    ax.text(legend_x, legend_y - 2.05, "PK: kolumna klucza PRIMARY KEY\nFK: kolumna klucza FOREIGN KEY\n"
            "Linia: N wierszy tabeli z FK wskazuje 1 wiersz tabeli z PK.", va="center", fontsize=9, linespacing=1.5)
    ax.set_xlim(-0.4, col_mid[3] + width / 2 + 0.4); ax.set_ylim(page_bottom - 0.4, 0.4); ax.axis("off")
    ax.set_title(f"Tabela animal_output łączy zwierzęta z żywnością: {len(tables)} tabel i {len(links)} kluczy FOREIGN KEY tworzy 1 model",
                 fontsize=12, loc="left", pad=22)
    ax.text(0, 1.012, "Schemat bazy z pliku farm.sql. Prostokąt to tabela z listą kolumn.", transform=ax.transAxes,
            fontsize=9, color="#555555", va="bottom")
    fig.text(0.012, 0.012, "Źródło: schemat odczytany z bazy poleceniami PRAGMA table_info i PRAGMA foreign_key_list.",
             fontsize=8, color="#555555", va="bottom")
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(HERE / "erd.png"); plt.close(fig)


def main():
    con = build()
    n_tables, n_links = test_project(con)
    n_r2 = test_r2(con)
    parts, rejected = report(con)
    rows = con.execute("SELECT sum(n) FROM (" + " UNION ALL ".join(
        f"SELECT count(*) AS n FROM {t}" for t in schema(con)[0]) + ")").fetchone()[0]
    print("\n\n".join(parts) + "\n\n" + rejected)
    print(f"\nschema: {n_tables} tables, {n_links} foreign keys, {rows} rows")
    print(f"tests passed: project numbers, {n_r2} values equal to the R2 functions, {len(REJECTED)} statements rejected")
    if "--check" in sys.argv:
        document = (HERE / "README.md").read_text(encoding="utf-8")
        missing = [p.split("\n", 1)[0] for p in parts + [rejected] if p not in document]
        missing += [f"number: {f}" for f in facts(con, n_r2) if f not in document]
        if missing:
            sys.exit("README.md does not show the current text of:\n  " + "\n  ".join(missing))
        print(f"README.md shows all {len(parts)} queries with current results and the {len(REJECTED)} rejected statements")
    if "--erd" in sys.argv:
        erd(con)
        print("erd.png written")


if __name__ == "__main__":
    main()

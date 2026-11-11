# -*- coding: utf-8 -*-
"""B. Tabela upraw (plon, energia, bialko, uzysk na m2) i powierzchnia na osobe."""
from dane import *

# (nazwa, klucz PLONY, klucz FAO, wsp. czesci jadalnej, podstawa plonu / zrodla)
UPRAWY = [
    ("Ziemniak", "ziemniak", "ziemniak", 1.0, "eko 23,2–30,4 t/ha; Lućmierz 15,3 [S11]; W-M 26,1 [S5]; Polska 29,6 [S7]"),
    ("Topinambur", "topinambur", "korzenie_inne", 1.0, "brak danych o plonie bulw: [założenie]"),
    ("Żyto ozime", "zyto", "zyto", 0.95, "eko 4,1–6,6 t/ha, minimum 2,3 [S9]; W-M 3,9 [S5]; klasa V przy 100–150 kg N: 6,3 [S58]"),
    ("Pszenżyto ozime", "pszenzyto", "pszenzyto", 0.95, "eko 4,2–5,7 t/ha, minimum 2,1 [S9]; W-M 4,8 [S5]"),
    ("Pszenica ozima", "pszenica_ozima", "pszenica", 0.95, "eko 4,8–6,5 t/ha, minimum 2,2 [S9]; W-M 5,5 [S5]"),
    ("Pszenica jara", "pszenica_jara", "pszenica", 0.95, "eko 2,8–3,9 t/ha, minimum 1,9 [S10]"),
    ("Owies zwyczajny", "owies", "owies", 0.70, "eko 3,8–5,2 t/ha, minimum 1,9 [S10]; W-M 3,2 [S5]"),
    ("Owies nagi", "owies_nagi", "owies", 0.95, "eko 2,5–4,8 t/ha; Szepietowo 1,0–3,0 [S10]"),
    ("Jęczmień jary", "jeczmien", "jeczmien", 0.70, "eko 3,8–5,5 t/ha, minimum 2,4 [S10]; W-M 4,1 [S5]"),
    ("Gryka", "gryka", "gryka", 0.65, "eko 1,7–1,8 t/ha; Krzyżewo 0,3–0,7 [S15]; Polska 1,6 [S7]"),
    ("Proso", "proso", "proso", 0.70, "Polska 1,6 t/ha (gryka, proso, inne) [S7]; doświadczenie 2,7–6,2 [S19]"),
    ("Kukurydza na ziarno", "kukurydza", "kukurydza", 0.95, "eko 7,0–7,9 t/ha [S14]; W-M 6,9 [S5]"),
    ("Fasola na suche ziarno", "fasola", "fasola", 0.95, "strączkowe jadalne Polska 2,4 t/ha [S7]; brak danych dla fasoli"),
    ("Groch siewny", "groch", "groch", 0.95, "eko 2,0–3,1 t/ha, minimum 0,7 [S13]; rejon II 3,5–4,5 [S16]"),
    ("Bobik, bób", "bobik", "bob", 0.95, "PDO rejon II 3,5–3,9 t/ha [S16]; brak danych eko"),
    ("Łubin słodki (wąskolistny, żółty)", "lubin", "lubin", 0.95, "eko 1,8–2,0 t/ha; Krzyżewo 0,9; Białogard 1,3 [S13]"),
    ("Soja (odmiany wczesne)", "soja", "soja", 0.95, "PDO rejon północny 3,2–3,3 t/ha [S17]; eko 2,9–3,9 na południu [S13]"),
    ("Rzepak ozimy", "rzepak", "rzepak", 1.0, "W-M 3,4 t/ha [S5]; PDO 3,9–4,5 [S12]; brak danych eko"),
    ("Lnianka siewna (rydz)", "lnianka", "lnianka", 1.0, "jara 1,0–2,0 t/ha; ozima 0,9–2,3 t/ha [S59]"),
    ("Słonecznik", "slonecznik", "slonecznik", 1.0, "PDO 3,6 t/ha [S18]; brak danych dla północy"),
    ("Len oleisty", "len", "len", 1.0, "brak danych liczbowych: [założenie]"),
    ("Mak", "mak", "mak", 1.0, "brak danych liczbowych: [założenie]"),
    ("Dynia oleista (pestki)", "dynia_oleista_pestki", "pestki_dyni", 1.0, "brak danych liczbowych: [założenie]"),
    ("Dynia zimowa", "dynia", "dynia", 1.0, "dynia, kabaczek, cukinia: Polska 44,5 t/ha [S7]"),
    ("Kapusta głowiasta", "kapusta", "kapusta", 1.0, "W-M 48,0 t/ha [S5]; Polska 45,9 [S7]"),
    ("Marchew", "marchew", "marchew", 1.0, "W-M 32,9 t/ha [S5]; Polska 38,5 [S7]"),
    ("Burak ćwikłowy", "burak", "warzywa_inne", 1.0, "W-M 34,2 t/ha [S5]; Polska 33,1 [S7]"),
    ("Cebula", "cebula", "cebula", 1.0, "W-M 19,0 t/ha [S5]; Polska 28,6 [S7]"),
    ("Czosnek", "czosnek", "czosnek", 1.0, "brak danych liczbowych: [założenie]"),
    ("Por", "por", "por", 1.0, "pozostałe warzywa 25,2 t/ha (lubelskie) [S5]: [założenie]"),
    ("Pietruszka korzeniowa", "pietruszka", "warzywa_inne", 1.0, "Polska 21,0 t/ha [S7]"),
    ("Seler korzeniowy", "seler", "warzywa_inne", 1.0, "Polska 31,5 t/ha [S7]"),
    ("Brukiew, rzepa", "brukiew", "warzywa_inne", 1.0, "brak danych: przyjęto jak burak [założenie]"),
    ("Jarmuż", "jarmuz", "warzywa_inne", 1.0, "brak danych liczbowych: [założenie]"),
    ("Pomidor (tunel nieogrzewany)", "pomidor_tunel", "pomidor", 1.0, "Olsztyn 9,2–12,3 kg/m² plonu handlowego [S37]"),
    ("Ogórek gruntowy", "ogorek", "ogorek", 1.0, "W-M 28,5 t/ha [S5]; Polska 23,2 [S7]"),
    ("Papryka (tunel)", "papryka_tunel", "papryka", 1.0, "brak danych liczbowych: [założenie]"),
    ("Cukinia", "cukinia", "dynia", 1.0, "dynia, kabaczek, cukinia: Polska 44,5 t/ha [S7]"),
    ("Sałata, szpinak, roszponka (tunel)", "lisciowe_tunel", "salata", 1.0, "brak danych liczbowych: [założenie], 1 cykl"),
    ("Jabłoń", "jablon", "jablko", 1.0, "Polska 25,9 t/ha [S7]; eko 20,5–30,5 [S38]"),
    ("Grusza", "grusza", "gruszka", 1.0, "Polska 14,1 t/ha [S7]"),
    ("Śliwa", "sliwa", "sliwka", 1.0, "Polska 7,5 t/ha [S7]"),
    ("Wiśnia", "wisnia", "wisnia", 1.0, "Polska 6,7 t/ha [S7]; eko 5,4 [S38]"),
    ("Porzeczka", "porzeczka", "porzeczka", 1.0, "Polska 2,9 t/ha [S7]"),
    ("Malina", "malina", "malina", 1.0, "Polska 4,5 t/ha [S7]"),
    ("Truskawka", "truskawka", "truskawka", 1.0, "Polska 6,1 t/ha [S7]"),
    ("Aronia", "aronia", "jagody_inne", 1.0, "Polska 3,8 t/ha [S7]"),
    ("Borówka wysoka", "borowka", "borowka", 1.0, "Polska 5,0 t/ha [S7]"),
    ("Winorośl", "winorosl", "winogrona", 1.0, "pozostałe krzewy 3,2 t/ha [S7]: [założenie]"),
    ("Leszczyna (orzechy w łupinie)", "leszczyna", "orzech_laskowy_lup", 1.0, "brak danych liczbowych: [założenie]"),
    ("Orzech włoski (w łupinie)", "orzech_wloski", "orzech_wloski_lup", 1.0, "inne drzewa owocowe 3,9 t/ha [S7]: [założenie]"),
]

def tabela_upraw():
    out = ["| Uprawa | Gleba średnia: plon ostrożny–dobry [t/ha] | Gleba lekka V–VI: plon ostrożny–dobry [t/ha] | Gleba lekka: plon ostrożny [kg/m²] | Energia [kcal/kg] | Białko [g/kg] | Część jadalna | Gleba lekka: uzysk energii ostrożny–dobry [kcal/m²] | Gleba lekka: uzysk białka ostrożny [g/m²] | Podstawa plonu |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    rank_e, rank_b = [], []
    for nazwa, kp, kf, jad, podst in UPRAWY:
        lo, hi = PLONY[kp]; llo, lhi = PLONY_L[kp]
        kcal100, b100, t100 = FAO[kf]
        kcal_kg = kcal100 * 10
        e_lo = llo / 10 * jad * kcal_kg; e_hi = lhi / 10 * jad * kcal_kg
        b_lo = llo / 10 * jad * b100 * 10
        rank_e.append((e_lo, nazwa)); rank_b.append((b_lo, nazwa))
        out.append(f"| {nazwa} | {lo:.1f}–{hi:.1f} | {llo:.1f}–{lhi:.1f} | {llo/10:.2f} | {kcal_kg} | {b100*10:.0f} | {jad:.2f} | {e_lo:.0f}–{e_hi:.0f} | {b_lo:.0f} | {podst} |")
    return "\n".join(out), sorted(rank_e, reverse=True), sorted(rank_b, reverse=True)

def powierzchnia(wariant=0, plon_idx=0, zapas=ZAPAS, plony=None):
    """Powierzchnia [m2] na 1 osobe. wariant: 0 = W0, 1 = W1, 2 = L. plon_idx 0 = ostrozny, 1 = dobry."""
    if plony is None:
        plony = PLONY_L if wariant == 2 else PLONY
    wiersze = []; grupy = {}
    for nazwa, klucz, kg0, kg1, kg2, grupa in DIETA:
        kg = (kg0, kg1, kg2)[wariant]
        if nazwa not in UPRAWA_DLA or kg == 0:
            continue
        kp, przerob, gr = UPRAWA_DLA[nazwa]
        plon = plony[kp][plon_idx]            # t/ha
        zbior = kg / przerob                   # kg zbioru na pokrycie spozycia
        zbior_z = zbior * (1 + zapas)          # kg zbioru z zapasem
        m2 = zbior_z / (plon / 10)             # kg / (kg/m2)
        kcal = kg * 10 * FAO[klucz][0]
        wiersze.append((nazwa, gr, kg, przerob, zbior, zbior_z, plon / 10, m2, kcal))
        grupy[gr] = grupy.get(gr, 0) + m2
    return wiersze, grupy

KOLEJ = ["warzywnik", "tunel foliowy", "okopowe", "strączkowe", "zboża", "oleiste", "sad i jagodnik"]

def brutto(g):
    """Dodatki: sciezki w warzywniku 25 % (zagon 1,2 m + sciezka 0,3 m [S39]); tunel 20 % [zalozenie]; uwrocia pol 10 % [zalozenie]."""
    return (g["warzywnik"] * 1.25 + g["tunel foliowy"] * 1.20
            + (g["okopowe"] + g["zboża"] + g["strączkowe"] + g["oleiste"]) * 1.10 + g["sad i jagodnik"])

if __name__ == "__main__":
    tab, re_, rb_ = tabela_upraw()
    print("## Tabela upraw: plon, energia, białko\n")
    print(tab)
    print("\n### Ranking uzysku energii na glebie lekkiej przy plonie ostrożnym [kcal/m²]\n")
    for u, n in re_[:16]:
        print(f"- {n}: {u:.0f}")
    print("\n### Ranking uzysku białka na glebie lekkiej przy plonie ostrożnym [g/m²]\n")
    for u, n in rb_[:16]:
        print(f"- {n}: {u:.0f}")

    print("\n## Wariant L (docelowy): powierzchnia na 1 osobę, gleba lekka V–VI, plon ostrożny, zapas 25 %\n")
    w, g = powierzchnia(2, 0)
    print("| Produkt | Grupa | Spożycie [kg/rok] | Współczynnik przerobu | Zbiór potrzebny [kg] | Zbiór z zapasem [kg] | Plon [kg/m²] | Powierzchnia [m²] | Uzysk [kcal/m²] |")
    print("|---|---|---|---|---|---|---|---|---|")
    for n, gr, kg, pr, z, zz, pl, m2, kcal in w:
        print(f"| {n} | {gr} | {kg:.0f} | {pr:.2f} | {z:.1f} | {zz:.1f} | {pl:.2f} | {m2:.1f} | {kcal/m2:.0f} |")
    print(f"| **Suma** | | | | | | | **{sum(x[7] for x in w):.0f}** | |")

    print("\n## Wariant L: powierzchnia wg grup [m²], zapas 25 %\n")
    gLo = powierzchnia(2, 0)[1]; gLd = powierzchnia(2, 1)[1]
    gL20 = powierzchnia(2, 0, 0.20)[1]; gL30 = powierzchnia(2, 0, 0.30)[1]
    print("| Grupa | 1 os. ostrożny | 4 os. ostrożny | 4 os. dobry | 2 os. ostrożny | 6 os. ostrożny | 4 os. ostrożny, zapas 20 % | 4 os. ostrożny, zapas 30 % |")
    print("|---|---|---|---|---|---|---|---|")
    for gr in KOLEJ:
        print(f"| {gr} | {gLo[gr]:.0f} | {4*gLo[gr]:.0f} | {4*gLd[gr]:.0f} | {2*gLo[gr]:.0f} | {6*gLo[gr]:.0f} | {4*gL20[gr]:.0f} | {4*gL30[gr]:.0f} |")
    so, sd = sum(gLo.values()), sum(gLd.values())
    print(f"| **Suma netto** | **{so:.0f}** | **{4*so:.0f}** | **{4*sd:.0f}** | **{2*so:.0f}** | **{6*so:.0f}** | **{4*sum(gL20.values()):.0f}** | **{4*sum(gL30.values()):.0f}** |")
    bo, bd = brutto(gLo), brutto(gLd)
    print(f"| **Suma brutto** (ścieżki, uwrocia) | **{bo:.0f}** | **{4*bo:.0f}** | **{4*bd:.0f}** | **{2*bo:.0f}** | **{6*bo:.0f}** | **{4*brutto(gL20):.0f}** | **{4*brutto(gL30):.0f}** |")
    print(f"\nWariant L, 4 osoby, brutto: {4*bo/10000:.2f} ha (plon ostrożny); {4*bd/10000:.2f} ha (plon dobry).")
    bez_sadu_o = 4 * (bo - gLo['sad i jagodnik']) / 10000; bez_sadu_d = 4 * (bd - gLd['sad i jagodnik']) / 10000
    print(f"Wariant L, 4 osoby, bez sadu i jagodnika (sad na działce kempingu): {bez_sadu_o:.2f} ha (plon ostrożny); {bez_sadu_d:.2f} ha (plon dobry).")

    print("\n## Wariant W0 i W1 na glebach średnich: powierzchnia netto [m²], zapas 25 %\n")
    print("| Grupa | W0: 1 os. ostrożny | W0: 4 os. ostrożny | W0: 4 os. dobry | W1: 4 os. ostrożny | W1: 4 os. dobry |")
    print("|---|---|---|---|---|---|")
    g0o = powierzchnia(0, 0)[1]; g0d = powierzchnia(0, 1)[1]; g1o = powierzchnia(1, 0)[1]; g1d = powierzchnia(1, 1)[1]
    for gr in KOLEJ:
        print(f"| {gr} | {g0o[gr]:.0f} | {4*g0o[gr]:.0f} | {4*g0d[gr]:.0f} | {4*g1o[gr]:.0f} | {4*g1d[gr]:.0f} |")
    print(f"| **Suma netto** | **{sum(g0o.values()):.0f}** | **{4*sum(g0o.values()):.0f}** | **{4*sum(g0d.values()):.0f}** | **{4*sum(g1o.values()):.0f}** | **{4*sum(g1d.values()):.0f}** |")
    print(f"| **Suma brutto** | **{brutto(g0o):.0f}** | **{4*brutto(g0o):.0f}** | **{4*brutto(g0d):.0f}** | **{4*brutto(g1o):.0f}** | **{4*brutto(g1d):.0f}** |")

    print("\n## Materiał siewny jako udział plonu ostrożnego na glebie lekkiej [obliczenie]\n")
    siew = [
        ("Żyto", 350 * 35 / 100, "350 ziaren/m² [S9] × MTZ 35 g [założenie]", PLONY_L["zyto"][0]),
        ("Pszenica ozima", 500 * 45 / 100, "500 ziaren/m² [S9] × MTZ 45 g [założenie]", PLONY_L["pszenica_ozima"][0]),
        ("Gryka", 60, "60 kg/ha [S54]", PLONY_L["gryka"][0]),
        ("Proso", 20, "20 kg/ha [S19]", PLONY_L["proso"][0]),
        ("Lnianka", 5, "od 4 do 6 kg/ha [S59]", PLONY_L["lnianka"][0]),
        ("Ziemniak", 4.0 * 10000 * 0.06, "4 rośliny/m² [S11] × sadzeniak 60 g [założenie]", PLONY_L["ziemniak"][0]),
    ]
    print("| Uprawa | Norma wysiewu [kg/ha] | Podstawa | Plon ostrożny [kg/ha] | Udział materiału siewnego w plonie |")
    print("|---|---|---|---|---|")
    for n, norma, podst, plon in siew:
        print(f"| {n} | {norma:.0f} | {podst} | {plon*1000:.0f} | {100*norma/(plon*1000):.1f} % |")

# -*- coding: utf-8 -*-
"""
Dane wejsciowe do obliczen agenta 2 (zywnosc, uprawy, drob).
Kazda liczba ma znacznik zrodla (S..) albo znacznik [zalozenie].
Lista zrodel: patrz raport agent2_zywnosc_uprawy_drob.md, sekcja "Zrodla".
"""

# --- A. Normy zywienia (NIZP PZH-PIB 2024) [S1] ---------------------------
# EER [kcal/dobe] dla PAL 1,4; 1,6; 1,8; 2,0. Masa ciala nalezna przy BMI 22.
EER = {
    # (plec, wiek, wzrost cm, masa kg): {PAL: kcal}
    ("M", "19-29", 179.0, 70.5): {1.4: 2358, 1.6: 2695, 1.8: 3032, 2.0: 3369},
    ("M", "30-59", 178.0, 69.7): {1.4: 2264, 1.6: 2588, 1.8: 2911, 2.0: 3235},
    ("M", "60-74", 176.0, 68.1): {1.4: 2063, 1.6: 2358, 1.8: 2652, 2.0: 2947},
    ("K", "19-29", 166.9, 61.2): {1.4: 1927, 1.6: 2203, 1.8: 2478, 2.0: 2753},
    ("K", "30-59", 165.0, 59.9): {1.4: 1829, 1.6: 2090, 1.8: 2351, 2.0: 2612},
    ("K", "60-74", 165.0, 59.9): {1.4: 1700, 1.6: 1943, 1.8: 2186, 2.0: 2429},
}
BIALKO_RDA_G_NA_KG = 0.83   # [S1] tab. 10-11
BIALKO_EAR_G_NA_KG = 0.66   # [S1]
TLUSZCZ_RI_PROC_E = (30, 40)      # [S1] tab. 1 s. 94 (dorosli); 20-30 % E przy malej aktywnosci
TLUSZCZ_EFSA_PROC_E = (20, 35)    # [S3]
WEGLOWODANY_RI_PROC_E = (45, 65)  # [S1] tab. 8 s. 133
BLONNIK_AI_G = 25                 # [S1] tab. 9 s. 134 (19-65 lat)
WODA_AI_ML = {"M": 2500, "K": 2000}  # [S1] tab. 1 s. 154
ALA_AI_PROC_E = 0.5               # [S1]
LA_AI_PROC_E = 4.0                # [S1]
EPA_DHA_AI_MG = 250               # [S1]

ENERGIA_PROJEKTOWA = 3000  # kcal/dobe [zalozenie]: mezczyzna 19-59 lat, 70 kg, PAL od 1,8 do 1,85

# --- Wspolczynniki FAO: sklad na 100 g "as purchased" [S4] -----------------
# (kcal, bialko g, tluszcz g)
FAO = {
    "pszenica": (334, 12.2, 2.3),
    "zyto": (319, 11.0, 1.9),
    "owies": (385, 13.0, 7.5),
    "jeczmien": (332, 11.0, 1.8),
    "jeczmien_peczak": (346, 9.0, 1.4),
    "gryka": (330, 11.0, 2.0),
    "proso": (340, 9.7, 3.0),
    "kukurydza": (356, 9.5, 4.3),
    "pszenzyto": (340, 8.0, 1.5),      # wiersz FAO "Cereals nes" uzyty jako przyblizenie
    "ziemniak": (67, 1.6, 0.1),
    "fasola": (341, 22.1, 1.7),
    "groch": (346, 22.5, 1.8),
    "bob": (343, 23.4, 2.0),
    "lubin": (390, 40.0, 13.0),
    "soja": (335, 38.0, 18.0),
    "rzepak": (494, 19.6, 45.0),
    "slonecznik": (308, 12.3, 26.8),
    "len": (498, 18.0, 34.0),
    "mak": (533, 18.0, 44.7),
    "pestki_dyni": (400, 18.2, 33.9),   # wiersz FAO "Melonseed" uzyty jako przyblizenie
    "olej": (884, 0.0, 100.0),
    "dynia": (19, 0.9, 0.1),
    "kapusta": (19, 1.0, 0.1),
    "marchew": (38, 0.9, 0.2),
    "cebula": (31, 1.1, 0.2),
    "czosnek": (130, 5.5, 0.4),
    "por": (37, 0.7, 0.1),
    "pomidor": (17, 0.8, 0.2),
    "ogorek": (13, 0.5, 0.1),
    "papryka": (25, 1.1, 0.3),
    "salata": (12, 1.1, 0.2),
    "szpinak": (16, 2.1, 0.3),
    "warzywa_inne": (22, 1.4, 0.2),     # wiersz FAO "Vegetables nes fresh"
    "korzenie_inne": (91, 1.6, 0.2),    # wiersz FAO "Roots, tubers nes" (topinambur)
    "jablko": (48, 0.1, 0.3),
    "gruszka": (54, 0.4, 0.4),
    "sliwka": (52, 0.7, 0.6),
    "wisnia": (45, 0.9, 0.3),
    "porzeczka": (59, 1.4, 0.3),
    "malina": (47, 0.9, 0.5),
    "truskawka": (28, 0.6, 0.4),
    "borowka": (55, 0.7, 0.4),
    "jagody_inne": (49, 1.0, 0.7),      # wiersz FAO "Berries nes" (aronia)
    "winogrona": (53, 0.5, 0.4),
    "orzech_laskowy_lup": (291, 6.0, 28.8),
    "orzech_wloski_lup": (289, 6.4, 27.8),
    "jaja": (139, 10.7, 9.8),
    "kurczak": (122, 12.3, 7.7),
    "kaczka": (291, 8.3, 28.3),
    "ges": (301, 12.9, 27.2),
    "mleko_kozie": (69, 3.6, 4.1),
    "miod": (298, 0.4, 0.0),
    "krolik": (118, 17.0, 5.0),
    "ryba_slodkowodna": (69, 10.9, 2.5),
}

MASA_JAJA_KG = 0.058   # [S20][S21]: jajo rasy rodzimej od 55 do 61 g; przyjeto 58 g

# --- Dieta modelowa: kg produktu na 1 doroslego na rok ----------------------
# klucz: (nazwa, klucz FAO, kg/rok wariant bazowy, kg/rok wariant z kozami i pszczolami, grupa)
DIETA = [
    # (nazwa, klucz FAO, W0 bazowy, W1 kozy+pszczoly gleby srednie, L docelowy: gleby lekkie V-VI + kozy + pszczoly, grupa)
    ("Pszenica: mąka razowa, kasze", "pszenica", 51, 36, 10, "zboża"),
    ("Żyto: mąka razowa", "zyto", 40, 34, 58, "zboża"),
    ("Owies nagi: płatki, kasza", "owies", 25, 25, 28, "zboża"),
    ("Jęczmień: kasza (pęczak)", "jeczmien_peczak", 7, 5, 0, "zboża"),
    ("Gryka: kasza", "gryka", 6, 5, 8, "zboża"),
    ("Proso: kasza jaglana", "proso", 4, 3, 8, "zboża"),
    ("Ziemniaki", "ziemniak", 160, 140, 170, "okopowe"),
    ("Fasola sucha", "fasola", 12, 9, 9, "strączkowe"),
    ("Groch suchy", "groch", 12, 9, 9, "strączkowe"),
    ("Bób suchy", "bob", 6, 3, 3, "strączkowe"),
    ("Olej rzepakowy tłoczony na zimno", "olej", 14, 9, 0, "oleiste"),
    ("Olej lniankowy (rydzowy) tłoczony na zimno", "olej", 0, 0, 10, "oleiste"),
    ("Olej lniany", "olej", 2, 2, 0, "oleiste"),
    ("Siemię lniane", "len", 4, 4, 2, "oleiste"),
    ("Słonecznik: nasiona w łusce", "slonecznik", 6, 4, 4, "oleiste"),
    ("Pestki dyni oleistej", "pestki_dyni", 3, 3, 3, "oleiste"),
    ("Mak", "mak", 2, 2, 2, "oleiste"),
    ("Orzechy włoskie w łupinie", "orzech_wloski_lup", 4, 4, 4, "sad"),
    ("Orzechy laskowe w łupinie", "orzech_laskowy_lup", 4, 4, 4, "sad"),
    ("Kapusta (świeża i kiszona)", "kapusta", 45, 45, 45, "warzywa"),
    ("Marchew", "marchew", 30, 30, 30, "warzywa"),
    ("Burak ćwikłowy", "warzywa_inne", 20, 20, 20, "warzywa"),
    ("Cebula", "cebula", 18, 18, 18, "warzywa"),
    ("Czosnek", "czosnek", 2, 2, 2, "warzywa"),
    ("Por", "por", 8, 8, 8, "warzywa"),
    ("Pietruszka korzeniowa", "warzywa_inne", 5, 5, 5, "warzywa"),
    ("Seler korzeniowy", "warzywa_inne", 6, 6, 6, "warzywa"),
    ("Brukiew, rzepa", "warzywa_inne", 6, 6, 6, "warzywa"),
    ("Jarmuż", "warzywa_inne", 10, 10, 10, "warzywa"),
    ("Ogórek", "ogorek", 15, 15, 15, "warzywa"),
    ("Cukinia", "dynia", 10, 10, 10, "warzywa"),
    ("Dynia zimowa", "dynia", 20, 20, 20, "warzywa"),
    ("Fasola szparagowa, groszek zielony", "warzywa_inne", 6, 6, 6, "warzywa"),
    ("Pomidor (tunel)", "pomidor", 25, 25, 25, "tunel"),
    ("Papryka (tunel)", "papryka", 4, 4, 4, "tunel"),
    ("Sałata, szpinak, roszponka (tunel)", "salata", 8, 8, 8, "tunel"),
    ("Jabłka", "jablko", 60, 60, 60, "sad"),
    ("Gruszki", "gruszka", 8, 8, 8, "sad"),
    ("Śliwki", "sliwka", 10, 10, 10, "sad"),
    ("Wiśnie", "wisnia", 6, 6, 6, "sad"),
    ("Porzeczki", "porzeczka", 6, 6, 6, "sad"),
    ("Maliny", "malina", 5, 5, 5, "sad"),
    ("Truskawki", "truskawka", 8, 8, 8, "sad"),
    ("Aronia", "jagody_inne", 2, 2, 2, "sad"),
    ("Borówka wysoka", "borowka", 3, 3, 3, "sad"),
    ("Winogrona", "winogrona", 4, 4, 4, "sad"),
    ("Jaja kurze (W0: 365 szt.; W1 i L: 300 szt.)", "jaja", 365 * MASA_JAJA_KG, 300 * MASA_JAJA_KG, 300 * MASA_JAJA_KG, "drób"),
    ("Kurczak: tuszka", "kurczak", 24, 22, 22, "drób"),
    ("Kaczka: tuszka", "kaczka", 7, 5, 5, "drób"),
    ("Gęś: tuszka", "ges", 9, 4.5, 4.5, "drób"),
    ("Mleko kozie", "mleko_kozie", 0, 250, 250, "kozy"),
    ("Miód", "miod", 0, 8, 8, "pszczoły"),
]

# --- Sklad wybranych produktow wg tabel Kunachowicz i in. [S1][S2] ----------
# blonnik [g/100 g czesci jadalnej]; wartosci dla produktow najblizszych
BLONNIK = {
    # produkt diety: (g/100 g, opis przyblizenia)
    "Pszenica: mąka razowa, kasze": (8.4, "dolne oszacowanie: chleb żytni razowy 8,4 g/100 g chleba"),
    "Żyto: mąka razowa": (9.1, "dolne oszacowanie: chleb żytni pełnoziarnisty 9,1 g/100 g chleba"),
    "Owies nagi: płatki, kasza": (6.9, "płatki owsiane"),
    "Jęczmień: kasza (pęczak)": (9.6, "płatki jęczmienne"),
    "Gryka: kasza": (5.9, "kasza gryczana"),
    "Ziemniaki": (1.5, "ziemniaki, średnio"),
    "Fasola sucha": (15.7, "fasola biała"),
    "Groch suchy": (15.0, "groch, nasiona suche"),
    "Bób suchy": (15.0, "przyjęto jak groch"),
    "Marchew": (3.6, "marchew"),
    "Burak ćwikłowy": (2.2, "burak"),
    "Kapusta (świeża i kiszona)": (2.6, "kapusta włoska"),
    "Jarmuż": (3.8, "jarmuż"),
    "Pomidor (tunel)": (1.2, "pomidor"),
    "Papryka (tunel)": (2.0, "papryka czerwona"),
    "Jabłka": (2.0, "jabłko"),
    "Maliny": (6.7, "maliny"),
    "Porzeczki": (7.8, "porzeczki czarne"),
    "Truskawki": (1.8, "truskawki"),
    "Winogrona": (1.5, "winogrona"),
}
# Dla pozostalych warzyw przyjeto 2,0 g/100 g (tekst [S1]: warzywa od 0,5 do 5,8 g/100 g), owoce 2,0 g/100 g.
BLONNIK_DOMYSLNY = {"warzywa": 2.0, "tunel": 1.2, "sad": 2.0}

WIT_C_MG_100G = {  # [S2] tab. 19; kapusta swieza [S50]
    "Ziemniaki": 16.0, "Jarmuż": 120.0, "Papryka (tunel)": 144.0, "Porzeczki": 182.6,
    "Truskawki": 66.0, "Burak ćwikłowy": 10.0, "Kapusta (świeża i kiszona)": 25.0,
}
WAPN_MG_100G = {  # [S2] tab. 30; mak [S51]
    "Jarmuż": 157.0, "Fasola sucha": 163.0, "Groch suchy": 163.0, "Bób suchy": 163.0, "Mak": 1266.0,
}
WAPN_MLEKO_MG_100G = 120.0   # [S2] mleko krowie 2 %; dla mleka koziego brak wartosci ze zrodla: [zalozenie]
B12_UG_100G = {"jaja": 1.6, "mieso_drobiowe": 0.4, "mleko": 0.4}   # [S2] tab. 23 (mleko krowie)
WIT_D_UG_100G = {"jaja": 1.7}                                       # [S2] tab. 26
UDZIAL_CZESCI_JADALNEJ = {"jaja": 0.89, "tuszka": 0.60}  # [zalozenie]: skorupa 11 %, kosci 40 %

# --- B. Plony: (plon ostrozny t/ha, plon dobry t/ha, podstawa) --------------
PLONY = {
    "ziemniak": (15.0, 25.0),
    "pszenica_ozima": (2.5, 4.5),
    "pszenica_jara": (2.0, 3.5),
    "zyto": (2.2, 4.0),
    "owies": (2.0, 3.5),
    "owies_nagi": (1.5, 3.0),
    "jeczmien": (2.0, 3.5),
    "gryka": (0.7, 1.6),
    "proso": (1.0, 2.5),
    "kukurydza": (4.0, 7.0),
    "fasola": (1.0, 2.0),
    "groch": (1.5, 3.0),
    "bobik": (2.0, 3.5),
    "lubin": (1.0, 2.0),
    "soja": (1.2, 2.5),
    "rzepak": (1.0, 2.5),
    "slonecznik": (1.2, 2.5),
    "len": (0.8, 1.5),
    "mak": (0.5, 1.0),
    "dynia_oleista_pestki": (0.4, 0.8),
    "dynia": (20.0, 40.0),
    "kapusta": (25.0, 45.0),
    "marchew": (20.0, 35.0),
    "burak": (20.0, 33.0),
    "cebula": (12.0, 25.0),
    "czosnek": (4.0, 8.0),
    "por": (15.0, 25.0),
    "pietruszka": (10.0, 20.0),
    "seler": (15.0, 30.0),
    "brukiew": (20.0, 33.0),
    "jarmuz": (10.0, 20.0),
    "pomidor_tunel": (50.0, 100.0),
    "ogorek": (12.0, 25.0),
    "papryka_tunel": (20.0, 40.0),
    "cukinia": (20.0, 40.0),
    "lisciowe_tunel": (10.0, 20.0),
    "fasolka": (5.0, 10.0),
    "jablon": (10.0, 20.0),
    "grusza": (6.0, 12.0),
    "sliwa": (4.0, 7.5),
    "wisnia": (3.0, 6.0),
    "porzeczka": (2.0, 3.5),
    "malina": (3.0, 5.0),
    "truskawka": (4.0, 6.5),
    "aronia": (2.5, 4.0),
    "borowka": (3.0, 5.0),
    "winorosl": (3.0, 6.0),
    "leszczyna": (1.0, 2.0),
    "orzech_wloski": (1.0, 2.5),
    "topinambur": (15.0, 30.0),
}

# Wspolczynnik przetworzenia: kg produktu jadalnego z 1 kg zbioru
PRZEROB = {
    "pszenica": 0.95, "zyto": 0.95, "owies_nagi": 0.95,   # [zalozenie]: strata na czyszczeniu 5 %
    "jeczmien_peczak": 0.70, "gryka": 0.65, "proso": 0.70,  # [zalozenie]: obluskiwanie
    "straczkowe": 0.95,                                    # [zalozenie]
    "olej_rzepakowy": 0.30,   # [obliczenie]: tluszcz 44,5 % [S12] x sprawnosc tloczenia 0,70 [zalozenie] = 0,31
    "olej_lniany": 0.28,      # [obliczenie]: tluszcz od 42 do 45 % [S12] x 0,70 [zalozenie] = od 0,29 do 0,31
}

ZAPAS = 0.25  # zapas na straty, nieurodzaj, material siewny (zadanie: od 20 do 30 %)

# Mapowanie pozycji diety na uprawe: (klucz plonu, wsp. przerobu, grupa powierzchni)
UPRAWA_DLA = {
    "Pszenica: mąka razowa, kasze": ("pszenica_ozima", PRZEROB["pszenica"], "zboża"),
    "Żyto: mąka razowa": ("zyto", PRZEROB["zyto"], "zboża"),
    "Owies nagi: płatki, kasza": ("owies_nagi", PRZEROB["owies_nagi"], "zboża"),
    "Jęczmień: kasza (pęczak)": ("jeczmien", PRZEROB["jeczmien_peczak"], "zboża"),
    "Gryka: kasza": ("gryka", PRZEROB["gryka"], "zboża"),
    "Proso: kasza jaglana": ("proso", PRZEROB["proso"], "zboża"),
    "Ziemniaki": ("ziemniak", 1.0, "okopowe"),
    "Fasola sucha": ("fasola", PRZEROB["straczkowe"], "strączkowe"),
    "Groch suchy": ("groch", PRZEROB["straczkowe"], "strączkowe"),
    "Bób suchy": ("bobik", PRZEROB["straczkowe"], "strączkowe"),
    "Olej rzepakowy tłoczony na zimno": ("rzepak", PRZEROB["olej_rzepakowy"], "oleiste"),
    "Olej lniany": ("len", PRZEROB["olej_lniany"], "oleiste"),
    "Siemię lniane": ("len", 1.0, "oleiste"),
    "Słonecznik: nasiona w łusce": ("slonecznik", 1.0, "oleiste"),
    "Pestki dyni oleistej": ("dynia_oleista_pestki", 1.0, "oleiste"),
    "Mak": ("mak", 1.0, "oleiste"),
    "Orzechy włoskie w łupinie": ("orzech_wloski", 1.0, "sad i jagodnik"),
    "Orzechy laskowe w łupinie": ("leszczyna", 1.0, "sad i jagodnik"),
    "Kapusta (świeża i kiszona)": ("kapusta", 1.0, "warzywnik"),
    "Marchew": ("marchew", 1.0, "warzywnik"),
    "Burak ćwikłowy": ("burak", 1.0, "warzywnik"),
    "Cebula": ("cebula", 1.0, "warzywnik"),
    "Czosnek": ("czosnek", 1.0, "warzywnik"),
    "Por": ("por", 1.0, "warzywnik"),
    "Pietruszka korzeniowa": ("pietruszka", 1.0, "warzywnik"),
    "Seler korzeniowy": ("seler", 1.0, "warzywnik"),
    "Brukiew, rzepa": ("brukiew", 1.0, "warzywnik"),
    "Jarmuż": ("jarmuz", 1.0, "warzywnik"),
    "Ogórek": ("ogorek", 1.0, "warzywnik"),
    "Cukinia": ("cukinia", 1.0, "warzywnik"),
    "Dynia zimowa": ("dynia", 1.0, "warzywnik"),
    "Fasola szparagowa, groszek zielony": ("fasolka", 1.0, "warzywnik"),
    "Pomidor (tunel)": ("pomidor_tunel", 1.0, "tunel foliowy"),
    "Papryka (tunel)": ("papryka_tunel", 1.0, "tunel foliowy"),
    "Sałata, szpinak, roszponka (tunel)": ("lisciowe_tunel", 1.0, "tunel foliowy"),
    "Jabłka": ("jablon", 1.0, "sad i jagodnik"),
    "Gruszki": ("grusza", 1.0, "sad i jagodnik"),
    "Śliwki": ("sliwa", 1.0, "sad i jagodnik"),
    "Wiśnie": ("wisnia", 1.0, "sad i jagodnik"),
    "Porzeczki": ("porzeczka", 1.0, "sad i jagodnik"),
    "Maliny": ("malina", 1.0, "sad i jagodnik"),
    "Truskawki": ("truskawka", 1.0, "sad i jagodnik"),
    "Aronia": ("aronia", 1.0, "sad i jagodnik"),
    "Borówka wysoka": ("borowka", 1.0, "sad i jagodnik"),
    "Winogrona": ("winorosl", 1.0, "sad i jagodnik"),
}

# --- C. Drob ---------------------------------------------------------------
JAJA_NA_NIOSKE = {"rodzima_bez_doswietlania": 160, "rodzima_z_doswietlaniem": 190, "mieszaniec": 250}
#  160: [zalozenie] na podstawie 180-190 jaj w sezonie [S20][S21] minus spadek zimowy;
#  190: [S20][S21]; 250: [zalozenie] na podstawie sredniej GUS 258 jaj (2023) [S7]
BROJLER_WOLNO = {"masa_zywa_kg": 3.08, "wyd_rzezna": 0.73, "pasza_kg": 6.3, "dni": 81}   # [S24]
KACZKA = {"masa_zywa_kg": 3.35, "wyd_rzezna": 0.71, "pasza_kg": 11.1, "tyg": 8}        # [S25]
GES = {"masa_zywa_kg": 6.96, "tuszka_kg": 4.47, "pasza_kg": 35.0, "owies_kg": 11.5, "tyg": 17}  # [S22][S23]
PASZA_NIOSKA_G_DOBA = 120    # [zalozenie] na podstawie 107 g [S26] i od 125 do 135 g [S27]
PASZA_KURKA_ODCHOW_KG = 8.0  # [zalozenie]: odchow kurki do 20. tygodnia
# Obornik i azot: program azotanowy, tab. 9, gleboka sciolka [S31]
OBORNIK = {  # (t/szt./rok, kg N/t)
    "nioska": (0.029, 20.7), "kurka_odchow": (0.008, 15.7), "brojler": (0.017, 24.7),
    "kaczka": (0.026, 22.8), "ges": (0.030, 21.8),
}
OBORNIK_P2O5_KG_T = 15.0   # [S32]
OBORNIK_K2O_KG_T = 8.0     # [S32]
N_MAX_KG_HA = 170          # [S31]
ROWNOWAZNIK_N = {"jesien": 0.40, "wiosna": 0.45}   # obornik drobiu niesnego [S31] tab. 11
WODA_L_DOBA = {"nioska": 0.25, "brojler": 0.35, "kaczka": 1.0, "ges": 1.5}
#  nioska 0,18-0,32 L, srednio 0,25 [S33]; brojler srednio 0,28 (zima) i 0,45 (lato) [S33];
#  kaczka i ges: [zalozenie], brak zrodla

# --- D. Naklady pracy: rbh/ha w gospodarstwach ekologicznych [S40] -----------
PRACA_RBH_HA_SREDNIO = {"zboża": 30.8, "okopowe": 206.1, "warzywa": 495.7, "sady": 332.0, "pastewne": 49.4}
PRACA_RBH_HA_DO5HA = {"zboża": 41.9, "okopowe": 287.0, "warzywa": 1107.5, "sady": 654.9, "pastewne": 58.2}

# --- Pobranie azotu [kg N/t plonu] z plonem ubocznym [S31] tab. 10 ----------
POBRANIE_N = {"pszenica": 27.0, "zyto": 24.0, "owies": 22.2, "jeczmien": 24.0, "kukurydza": 26.0,
              "rzepak": 50.0, "ziemniak": 4.2, "marchew": 1.7, "cebula": 1.9, "kapusta": 2.3,
              "burak": 2.7, "ogorek": 1.7, "pomidor": 2.0}

# --- E. Gestosci usypowe [kg/m3] -------------------------------------------
GESTOSC = {"pszenica": 770, "zyto": 700, "owies": 420, "jeczmien": 600, "proso": 640, "groch": 800,
           "fasola": 700, "rzepak": 770, "len": 770,           # [S45]
           "ziemniak": 650, "korzeniowe": 600, "kapusta": 400, "cebula": 550, "jablka": 350,
           "dynia": 350, "gryka": 600, "slonecznik": 400, "mak": 600}  # [zalozenie]

# --- Plony na glebach lekkich, klasa V-VI: (ostrozny, dobry) [t/ha] ----------
# Podstawa: dolne wyniki doswiadczen ekologicznych COBORU na glebach kompleksu 5 [S9][S10][S11][S13][S15],
# pomniejszone o [zalozenie] dla klasy V-VI. Warzywa, tunel i sad: gleba ulepszona kompostem i nawadniana.
PLONY_L = dict(PLONY)
PLONY_L.update({
    "ziemniak": (12.0, 22.0),
    "pszenica_ozima": (1.2, 2.5),
    "pszenica_jara": (1.0, 2.0),
    "zyto": (1.2, 2.5),
    "pszenzyto": (1.2, 2.5),
    "owies": (1.0, 2.0),
    "owies_nagi": (0.7, 1.5),
    "jeczmien": (1.0, 2.0),
    "gryka": (0.5, 1.2),
    "proso": (0.7, 1.5),
    "kukurydza": (2.5, 5.0),
    "fasola": (1.0, 2.0),          # uprawa w ulepszonym warzywniku
    "groch": (0.8, 1.8),
    "bobik": (1.0, 2.0),
    "lubin": (0.7, 1.5),
    "soja": (0.6, 1.5),
    "rzepak": (0.6, 1.5),
    "lnianka": (0.7, 1.5),
    "slonecznik": (0.8, 1.8),
    "len": (0.5, 1.0),
    "topinambur": (12.0, 25.0),
})
PLONY["pszenzyto"] = (2.2, 4.0)
PLONY["lnianka"] = (1.0, 2.0)
PRZEROB["olej_lniankowy"] = 0.24   # [obliczenie]: tluszcz 30 % [S48] x sprawnosc tloczenia 0,79 [S48] = 0,24
UPRAWA_DLA["Olej lniankowy (rydzowy) tłoczony na zimno"] = ("lnianka", PRZEROB["olej_lniankowy"], "oleiste")
FAO["lnianka"] = (494, 19.6, 45.0)  # brak wiersza w [S4]: przyjeto wiersz rzepaku jako przyblizenie [zalozenie]

# --- Kozy, owce, pszczoly ---------------------------------------------------
KOZA = {"mleko_kg_laktacja": (600, 1400), "laktacja_dni": (240, 260),          # [S41] rasy uszlachetnione
        "siano_kg_doba": (1.0, 2.5), "zielonka_kg_doba": 7.0, "tresciwa_kg_na_kg_mleka_ponad_2": 0.4,
        "pastwisko_stale_m2": (500, 1000), "kojec_m2": 1.5, "wybieg_m2": 4.0}   # [S41][S30]
OWCA = {"mleko_kg_okres_doju": (37, 84), "doj_dni": (98, 112)}                   # [S57]
MIOD_KG_RODZINA = {"slaby_rok": 11, "sredni_rok": 17, "pasieki_duze": 22}         # [S7] tabl. 145: 2020; 2023; 2023
SIANO_T_HA = 5.5      # woj. warminsko-mazurskie, siano lakowe 2024 [S5]
SIANO_T_HA_LEKKA = 3.0  # [zalozenie]: sucha gleba piaszczysta

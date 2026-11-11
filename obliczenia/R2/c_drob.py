# -*- coding: utf-8 -*-
"""C. Drob: sklad stada, produkcja, pasza, powierzchnia paszowa, woda, obornik, swiatlo, bilans ziemi."""
import math
from dane import *
from b_plony_powierzchnia import powierzchnia

# --- parametry produkcyjne ---------------------------------------------------
TUSZKA_BROJLER = BROJLER_WOLNO["masa_zywa_kg"] * BROJLER_WOLNO["wyd_rzezna"]      # 2,25 kg [S24]
TUSZKA_KACZKA = KACZKA["masa_zywa_kg"] * KACZKA["wyd_rzezna"]                     # 2,38 kg [S25]
TUSZKA_GES = GES["tuszka_kg"]                                                       # 4,47 kg [S22]
TUSZKA_KURA_WYBRAKOWANA = 1.8 * 0.64    # [zalozenie]: 1,8 kg masy zywej [S20][S21] x 64 % [S24]
TUSZKA_KOGUTEK = 2.5 * 0.64             # kogutek rasy rodzimej 20 tygodni: 2,5 kg [S20] x 64 % [S24]
PASZA_KOGUTEK_KG = 9.0                  # [zalozenie]
LATA_UZYTKOWANIA_NIOSKI = 2             # [zalozenie]
KUR_NA_KOGUTA = 12                      # [zalozenie]
ZAPAS_NIOSEK = 1.10                     # [zalozenie]: 10 % na upadki i kwoczenie

# Receptura mieszanki z wlasnych surowcow: udzial masowy, klucz plonu, klucz FAO
RECEPTURA = [
    ("pszenica", 0.35, "pszenica_ozima", "pszenica"),
    ("owies", 0.20, "owies", "owies"),
    ("jęczmień albo pszenżyto", 0.10, "jeczmien", "jeczmien"),
    ("groch", 0.20, "groch", "groch"),
    ("bobik albo łubin słodki", 0.05, "bobik", "bob"),
    ("makuch rzepakowy i lniany (własny)", 0.10, None, None),
]
BIALKO_MAKUCH = 30.0   # % [zalozenie]: makuch po tloczeniu na zimno
ZAPAS_PASZA = 0.15     # [zalozenie]: material siewny i straty

def ha_na_tone(plon_idx, z_makuchem=True):
    """Powierzchnia [ha] na 1 t mieszanki. Bez makuchu jego udzial zastepuje groch."""
    ha = 0.0
    for nazwa, udz, kp, kf in RECEPTURA:
        if kp is None:
            if not z_makuchem:
                ha += udz / PLONY["groch"][plon_idx]
            continue
        ha += udz / PLONY[kp][plon_idx]
    return ha * (1 + ZAPAS_PASZA)

def bialko_mieszanki():
    b = 0.0
    for nazwa, udz, kp, kf in RECEPTURA:
        b += udz * (BIALKO_MAKUCH if kf is None else FAO[kf][1])
    return b

def stado(n_osob, jaja_os=365, kurczak_os=24.0, kaczka_os=7.0, ges_os=9.0, niesnosc=160):
    nioski = math.ceil(n_osob * jaja_os / niesnosc * ZAPAS_NIOSEK)
    koguty = max(1, math.ceil(nioski / KUR_NA_KOGUTA))
    kurki = math.ceil(nioski / LATA_UZYTKOWANIA_NIOSKI)     # remont stada na rok
    kogutki = kurki                                           # z wylegu: 50 % kogutkow
    mieso_kury = kurki * TUSZKA_KURA_WYBRAKOWANA + kogutki * TUSZKA_KOGUTEK
    brojlery = max(0, math.ceil((n_osob * kurczak_os - mieso_kury) / TUSZKA_BROJLER))
    kaczki = math.ceil(n_osob * kaczka_os / TUSZKA_KACZKA)
    gesi = math.ceil(n_osob * ges_os / TUSZKA_GES)
    return dict(nioski=nioski, koguty=koguty, kurki=kurki, kogutki=kogutki, brojlery=brojlery, kaczki=kaczki, gesi=gesi)

def produkcja(s, niesnosc=160):
    jaja = s["nioski"] * niesnosc
    m_kurczak = s["brojlery"] * TUSZKA_BROJLER + s["kurki"] * TUSZKA_KURA_WYBRAKOWANA + s["kogutki"] * TUSZKA_KOGUTEK
    m_kaczka = s["kaczki"] * TUSZKA_KACZKA
    m_ges = s["gesi"] * TUSZKA_GES
    tl = m_kurczak * FAO["kurczak"][2] / 100 + m_kaczka * FAO["kaczka"][2] / 100 + m_ges * FAO["ges"][2] / 100
    return dict(jaja=jaja, kurczak=m_kurczak, kaczka=m_kaczka, ges=m_ges, mieso=m_kurczak + m_kaczka + m_ges, tluszcz=tl)

def pasza(s):
    p = {}
    p["nioski i koguty"] = (s["nioski"] + s["koguty"]) * PASZA_NIOSKA_G_DOBA * 365 / 1000
    p["kurki (odchów)"] = s["kurki"] * PASZA_KURKA_ODCHOW_KG
    p["kogutki"] = s["kogutki"] * PASZA_KOGUTEK_KG
    p["kurczęta rzeźne"] = s["brojlery"] * BROJLER_WOLNO["pasza_kg"]
    p["kaczki"] = s["kaczki"] * KACZKA["pasza_kg"]
    p["gęsi"] = s["gesi"] * GES["pasza_kg"]
    return p

def szczyt(s, partie_brojlerow=2, partie_kaczek=2):
    """Stan jednoczesny w szczycie (lato): nioski, koguty, kurki i kogutki z wylegu, 1 partia brojlerow, 1 partia kaczek, gesi."""
    return (s["nioski"] + s["koguty"] + s["kurki"] + s["kogutki"]
            + math.ceil(s["brojlery"] / partie_brojlerow) + math.ceil(s["kaczki"] / partie_kaczek) + s["gesi"])

def obornik(s, partie_brojlerow=2, partie_kaczek=2):
    """Obornik [t/rok] i azot [kg N/rok] wg [S31]; ptaki sezonowe liczone ulamkiem roku."""
    poz = [
        ("nioski i koguty", s["nioski"] + s["koguty"], 1.0, OBORNIK["nioska"]),
        ("kurki i kogutki (20 tygodni)", s["kurki"] + s["kogutki"], 1.0, OBORNIK["kurka_odchow"]),
        ("kurczęta rzeźne (81 dni)", s["brojlery"], 81 / 365, OBORNIK["brojler"]),
        ("kaczki (8 tygodni)", s["kaczki"], 56 / 365, OBORNIK["kaczka"]),
        ("gęsi (17 tygodni)", s["gesi"], 119 / 365, OBORNIK["ges"]),
    ]
    t = n = 0.0
    for nazwa, szt, ulamek, (t_szt, n_t) in poz:
        m = szt * ulamek * t_szt
        t += m; n += m * n_t
    return t, n

def woda(s):
    """Zuzycie wody [L/dobe] w szczycie."""
    return ((s["nioski"] + s["koguty"] + s["kurki"] + s["kogutki"]) * WODA_L_DOBA["nioska"]
            + math.ceil(s["brojlery"] / 2) * WODA_L_DOBA["brojler"] + math.ceil(s["kaczki"] / 2) * WODA_L_DOBA["kaczka"]
            + s["gesi"] * WODA_L_DOBA["ges"])

def wybieg_i_kurnik(s):
    """Normy rolnictwa ekologicznego [S35]: wybieg m2/szt., kurnik 6 niosek/m2 albo 21 kg/m2."""
    kury = s["nioski"] + s["koguty"]
    wyb = kury * 4 + (s["kurki"] + s["kogutki"]) * 1 + math.ceil(s["brojlery"] / 2) * 4 + math.ceil(s["kaczki"] / 2) * 4.5 + s["gesi"] * 15
    kurnik = (kury / 6 + (s["kurki"] + s["kogutki"]) * 1.8 / 21 + math.ceil(s["brojlery"] / 2) * BROJLER_WOLNO["masa_zywa_kg"] / 21
              + math.ceil(s["kaczki"] / 2) * KACZKA["masa_zywa_kg"] / 21 + s["gesi"] * GES["masa_zywa_kg"] / 21)
    grzedy = kury * 0.18
    gniazda = math.ceil(s["nioski"] / 7)
    return wyb, kurnik, grzedy, gniazda

def dlugosc_dnia(szer=53.76):
    """Dlugosc dnia [h] dla kazdego dnia roku; wschod i zachod przy wysokosci Slonca -0,833 stopnia."""
    wynik = []
    fi = math.radians(szer)
    for n in range(1, 366):
        dekl = math.radians(23.44) * math.sin(2 * math.pi * (284 + n) / 365)
        c = (math.sin(math.radians(-0.833)) - math.sin(fi) * math.sin(dekl)) / (math.cos(fi) * math.cos(dekl))
        c = max(-1, min(1, c))
        wynik.append(2 * math.degrees(math.acos(c)) / 15)
    return wynik

def wiersz_stada(nazwa, s, niesnosc):
    p = produkcja(s, niesnosc); pa = pasza(s); ps = sum(pa.values())
    return (f"| {nazwa} | {s['nioski']} | {s['koguty']} | {s['kurki']}+{s['kogutki']} | {s['brojlery']} | {s['kaczki']} | {s['gesi']} | "
            f"{szczyt(s)} | {p['jaja']} | {p['mieso']:.0f} | {p['tluszcz']:.1f} | {ps:.0f} |")

if __name__ == "__main__":
    print(f"Tuszka: kurczę rzeźne {TUSZKA_BROJLER:.2f} kg; kaczka {TUSZKA_KACZKA:.2f} kg; gęś {TUSZKA_GES:.2f} kg; "
          f"kura wybrakowana {TUSZKA_KURA_WYBRAKOWANA:.2f} kg; kogutek {TUSZKA_KOGUTEK:.2f} kg\n")
    print("## Skład stada dla samowystarczalności (dieta bazowa: 365 jaj, 24 kg kurczaka, 7 kg kaczki, 9 kg gęsi na osobę na rok)\n")
    print("| Wariant | Nioski | Koguty | Kurki+kogutki z wylęgu na rok | Kurczęta rzeźne na rok | Kaczki na rok | Gęsi na rok | Stan w szczycie [szt.] | Jaja [szt./rok] | Mięso w tuszkach [kg/rok] | Tłuszcz w tuszkach [kg/rok] | Pasza treściwa [kg/rok] |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    st = {}
    for n in (2, 4, 6):
        st[n] = stado(n)
        print(wiersz_stada(f"{n} osoby" if n < 5 else f"{n} osób", st[n], 160))
    # wariant pelny 100 szt.: nioski z doswietlaniem (190 jaj)
    pelny = dict(nioski=60, koguty=4, kurki=10, kogutki=0, brojlery=28, kaczki=20, gesi=12)
    print(wiersz_stada("Pełny: 100 sztuk w szczycie", pelny, 190))
    print("\nWariant pełny: 60 niosek, 4 koguty, 10 kurek na remont, 14 kurcząt rzeźnych w 1 z 2 partii, 10 kaczek w 1 z 2 partii, 12 gęsi. "
          f"Stan w szczycie: {szczyt(pelny)} szt.")
    pp = produkcja(pelny, 190)
    zap4 = 4 * 365
    print(f"Wariant pełny: jaja {pp['jaja']} szt./rok; potrzeba 4 osób {zap4} szt.; nadwyżka {pp['jaja']-zap4} szt./rok = {(pp['jaja']-zap4)/52:.0f} szt./tydzień.")
    print(f"Wariant pełny: mięso {pp['mieso']:.0f} kg tuszek/rok (kurczak {pp['kurczak']:.0f}, kaczka {pp['kaczka']:.0f}, gęś {pp['ges']:.0f}); potrzeba 4 osób {4*(24+7+9)} kg.")

    print("\n## Pasza: struktura zużycia [kg/rok]\n")
    print("| Pozycja | 2 osoby | 4 osoby | 6 osób | Pełny 100 szt. |")
    print("|---|---|---|---|---|")
    pz = {k: pasza(v) for k, v in st.items()}; pzp = pasza(pelny)
    for k in pzp:
        print(f"| {k} | {pz[2][k]:.0f} | {pz[4][k]:.0f} | {pz[6][k]:.0f} | {pzp[k]:.0f} |")
    print(f"| **Suma** | **{sum(pz[2].values()):.0f}** | **{sum(pz[4].values()):.0f}** | **{sum(pz[6].values()):.0f}** | **{sum(pzp.values()):.0f}** |")

    print("\n## Receptura mieszanki z własnych surowców\n")
    print("| Składnik | Udział [%] | Białko [g/100 g] [S4] | Plon ostrożny [t/ha] | Plon dobry [t/ha] |")
    print("|---|---|---|---|---|")
    for nazwa, udz, kp, kf in RECEPTURA:
        b = BIALKO_MAKUCH if kf is None else FAO[kf][1]
        pl = ("–", "–") if kp is None else (f"{PLONY[kp][0]:.1f}", f"{PLONY[kp][1]:.1f}")
        print(f"| {nazwa} | {udz*100:.0f} | {b:.1f} | {pl[0]} | {pl[1]} |")
    print(f"\nBiałko ogólne mieszanki: {bialko_mieszanki():.1f} % [obliczenie]. Cel dla niosek: od 16 do 18 % [S21].")
    for idx, nz in ((0, "ostrożny"), (1, "dobry")):
        print(f"Powierzchnia na 1 t mieszanki, plon {nz}: {ha_na_tone(idx):.3f} ha z makuchem własnym; {ha_na_tone(idx, False):.3f} ha bez makuchu (zapas 15 %).")

    # makuch dostepny z tloczenia oleju dla 4 osob
    makuch4 = 4 * (14 / PRZEROB["olej_rzepakowy"] * (1 - PRZEROB["olej_rzepakowy"]) + 2 / PRZEROB["olej_lniany"] * (1 - PRZEROB["olej_lniany"]))
    print(f"Makuch z tłoczenia oleju dla 4 osób: {makuch4:.0f} kg/rok [obliczenie]: wystarcza na 10 % udziału w {makuch4/0.10:.0f} kg mieszanki.")

    print("\n## Powierzchnia upraw paszowych [ha]\n")
    print("| Wariant | Pasza [t/rok] | Plon ostrożny, z makuchem | Plon ostrożny, bez makuchu | Plon dobry, z makuchem | Plon dobry, bez makuchu |")
    print("|---|---|---|---|---|---|")
    for nazwa, s in (("2 osoby", st[2]), ("4 osoby", st[4]), ("6 osób", st[6]), ("Pełny 100 szt.", pelny)):
        t = sum(pasza(s).values()) / 1000
        print(f"| {nazwa} | {t:.2f} | {t*ha_na_tone(0):.2f} | {t*ha_na_tone(0, False):.2f} | {t*ha_na_tone(1):.2f} | {t*ha_na_tone(1, False):.2f} |")
    # powierzchnia na 1 ptaka
    print("\n### Powierzchnia paszowa na 1 sztukę [m²], bez makuchu\n")
    print("| Ptak | Pasza [kg] | Plon ostrożny [m²] | Plon dobry [m²] |")
    print("|---|---|---|---|")
    for nz, kg in (("Nioska albo kogut, 1 rok", PASZA_NIOSKA_G_DOBA * 365 / 1000), ("Kurczę rzeźne, 81 dni", BROJLER_WOLNO["pasza_kg"]),
                   ("Kaczka, 8 tygodni", KACZKA["pasza_kg"]), ("Gęś, 17 tygodni", GES["pasza_kg"]), ("Kurka w odchowie, 20 tygodni", PASZA_KURKA_ODCHOW_KG)):
        print(f"| {nz} | {kg:.1f} | {kg/1000*ha_na_tone(0, False)*10000:.0f} | {kg/1000*ha_na_tone(1, False)*10000:.0f} |")

    print("\n## Woda, obornik, azot, wybieg, kurnik\n")
    print("| Wariant | Woda w szczycie [L/dobę] | Obornik [t/rok] | N w oborniku [kg/rok] | N działający wiosną [kg/rok] | P2O5 [kg/rok] | K2O [kg/rok] | Min. powierzchnia przy 170 kg N/ha [ha] | Pole nawożone dawką 12,5 t/ha [ha] | Wybieg eko [m²] | Kurnik eko [m²] | Grzędy [m] | Gniazda [szt.] |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for nazwa, s in (("2 osoby", st[2]), ("4 osoby", st[4]), ("6 osób", st[6]), ("Pełny 100 szt.", pelny)):
        t, n = obornik(s); wyb, kur, grz, gn = wybieg_i_kurnik(s)
        print(f"| {nazwa} | {woda(s):.0f} | {t:.2f} | {n:.0f} | {n*ROWNOWAZNIK_N['wiosna']:.0f} | {t*OBORNIK_P2O5_KG_T:.0f} | {t*OBORNIK_K2O_KG_T:.0f} | {n/N_MAX_KG_HA:.2f} | {t/12.5:.2f} | {wyb:.0f} | {kur:.1f} | {grz:.1f} | {gn} |")

    print("\n## Długość dnia w Olsztynie (53,76° N) [obliczenie astronomiczne]\n")
    dd = dlugosc_dnia()
    mies = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    nazwy = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]
    print("| Miesiąc | Średnia długość dnia [h] | Doświetlanie do 14 h [h/dobę] |")
    print("|---|---|---|")
    i = 0; suma_doswietl = 0.0
    for m, d in zip(nazwy, mies):
        sr = sum(dd[i:i + d]) / d
        dos = max(0.0, 14 - sr)
        suma_doswietl += sum(max(0.0, 14 - x) for x in dd[i:i + d])
        print(f"| {m} | {sr:.1f} | {dos:.1f} |")
        i += d
    dni14 = sum(1 for x in dd if x >= 14)
    pierwszy = next(k for k, x in enumerate(dd) if x >= 14) + 1
    ostatni = max(k for k, x in enumerate(dd) if x >= 14) + 1
    print(f"\nNajkrótszy dzień: {min(dd):.2f} h. Najdłuższy dzień: {max(dd):.2f} h. Dni z dniem co najmniej 14 h: {dni14} (od dnia roku {pierwszy} do dnia roku {ostatni}).")
    print(f"Suma godzin doświetlania do 14 h: {suma_doswietl:.0f} h/rok. Energia przy 3 W/m² [S49] i kurniku 11 m²: {suma_doswietl*3*11/1000:.0f} kWh/rok [obliczenie].")

    # --- bilans ziemi dla 4 osob ------------------------------------------------
    print("\n## Bilans ziemi: żywność dla 4 osób i pasza [ha]\n")
    def brutto(g):
        return (g["warzywnik"] * 1.25 + g["tunel foliowy"] * 1.20
                + (g["okopowe"] + g["zboża"] + g["strączkowe"] + g["oleiste"]) * 1.10 + g["sad i jagodnik"])
    zyw = {}
    for idx, nz in ((0, "ostrożny"), (1, "dobry")):
        zyw[nz] = 4 * brutto(powierzchnia(0, idx)[1]) / 10000
    t4 = sum(pasza(st[4]).values()) / 1000; tp = sum(pzp.values()) / 1000
    wyb4 = wybieg_i_kurnik(st[4])[0] / 10000; wybp = wybieg_i_kurnik(pelny)[0] / 10000
    print("| Element | Plon ostrożny | Plon dobry |")
    print("|---|---|---|")
    print(f"| A. Żywność roślinna dla 4 osób, brutto | {zyw['ostrożny']:.2f} | {zyw['dobry']:.2f} |")
    print(f"| B. Pasza dla stada domowego 4 osób ({t4:.2f} t/rok), z makuchem | {t4*ha_na_tone(0):.2f} | {t4*ha_na_tone(1):.2f} |")
    print(f"| C. Wybiegi stada domowego, 2 kwatery (2 × norma eko) | {2*wyb4:.2f} | {2*wyb4:.2f} |")
    sumA = {k: zyw[k] + t4 * ha_na_tone(i) + 2 * wyb4 for i, k in enumerate(("ostrożny", "dobry"))}
    print(f"| **A+B+C: 4 osoby, stado domowe, pasza własna** | **{sumA['ostrożny']:.2f}** | **{sumA['dobry']:.2f}** |")
    print(f"| D. Pasza dla 100 sztuk ({tp:.2f} t/rok), bez makuchu ponad dostępny | {tp*ha_na_tone(0, False):.2f} | {tp*ha_na_tone(1, False):.2f} |")
    print(f"| E. Wybiegi 100 sztuk, 2 kwatery | {2*wybp:.2f} | {2*wybp:.2f} |")
    sumP = {k: zyw[k] + tp * ha_na_tone(i, False) + 2 * wybp for i, k in enumerate(("ostrożny", "dobry"))}
    print(f"| **A+D+E: 4 osoby, 100 sztuk, pasza własna** | **{sumP['ostrożny']:.2f}** | **{sumP['dobry']:.2f}** |")
    sumK = {k: zyw[k] + 2 * wybp for k in ("ostrożny", "dobry")}
    print(f"| **A+E: 4 osoby, 100 sztuk, pasza kupowana ({tp:.1f} t/rok)** | **{sumK['ostrożny']:.2f}** | **{sumK['dobry']:.2f}** |")

    print("\n### Ile ptaków wyżywi ziemia, która zostaje po uprawach żywności dla 4 osób\n")
    print("| Teren otwarty [ha] | Plon | Zostaje po żywności [ha] | Pasza własna [t/rok] | Równoważnik niosek [szt.] | Wniosek |")
    print("|---|---|---|---|---|---|")
    kg_nioska = PASZA_NIOSKA_G_DOBA * 365 / 1000
    for teren in (1.0, 1.5, 2.0):
        for i, k in enumerate(("ostrożny", "dobry")):
            reszta = teren - zyw[k]
            if reszta <= 0:
                print(f"| {teren:.1f} | {k} | {reszta:.2f} | 0 | 0 | Ziemi brakuje już na żywność roślinną: brak {-reszta:.2f} ha |")
                continue
            # odejmij wybiegi stada domowego
            r2 = max(0.0, reszta - 2 * wyb4)
            t = r2 / ha_na_tone(i, False)
            wn = "pokrywa stado domowe" if t >= t4 else "nie pokrywa stada domowego"
            if t >= tp: wn = "pokrywa 100 sztuk"
            print(f"| {teren:.1f} | {k} | {reszta:.2f} | {t:.2f} | {t*1000/kg_nioska:.0f} | {wn} (stado domowe {t4:.2f} t; 100 sztuk {tp:.2f} t) |")

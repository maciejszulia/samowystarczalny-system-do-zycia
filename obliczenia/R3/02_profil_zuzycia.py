# -*- coding: utf-8 -*-
"""02 - Profil zuzycia energii elektrycznej: dom + gospodarstwo. Scenariusze S/M/L = 3000/5000/8000 kWh/rok.

Budowa od dolu (lista odbiornikow) + rezerwa domykajaca do wartosci docelowej.
Pozycje oznaczone [Z] maja zrodlo (karta produktu), pozostale to SZACUNEK wlasny z podanym wzorem.
Wzory (jedna linia):
  E_pompy = rho*g*H*V/(eta*3.6e6) [kWh]  ; rho=1000 kg/m3, H=45 m, eta=0.35 (pompa glebinowa 3-4 cale, "wire-to-water") -> 0.350 kWh/m3
  E_urzadzenia = P[W]*t[h]/1000 [kWh]
"""
import json
import math
from dane import *

# ---------- profile miesieczne (wagi sumujace sie do 1) ----------
def norm(w):
    s = sum(w)
    return [x / s for x in w]

dl = [dlugosc_dnia(n) for n in DNI_KLEINA]                         # dlugosc dnia [h]
P_FLAT = norm(DNI)
P_SWIATLO = norm([d * max(0.5, 16 - x) for d, x in zip(DNI, dl)])   # doba aktywna 16 h; swiatlo sztuczne = 16 h - dlugosc dnia (min 0.5 h)
HDD = [d * (20 - t) if t < 12 else 0 for d, t in zip(DNI, IMGW_T)]  # stopniodni (20 st C), sezon: miesiace o sredniej < 12 st C
P_GRZANIE = norm(HDD)
def frakcja_ponizej(t_sr, prog=3.0, sigma=5.0):                     # udzial czasu z T < prog; rozklad normalny T, sigma 5 K (SZACUNEK)
    return 0.5 * (1 + math.erf((prog - t_sr) / (sigma * math.sqrt(2))))
P_MROZ = norm([d * frakcja_ponizej(t) for d, t in zip(DNI, IMGW_T)])
P_PODLEW = [0, 0, 0, 0, 0.15, 0.25, 0.30, 0.25, 0.05, 0, 0, 0]
P_CHLOD = norm([d * (1 + 0.01 * (t - 8)) for d, t in zip(DNI, IMGW_T)])  # chlodziarki: +-1 %/K wzgledem 8 st C (SZACUNEK)
P_ROZSADA = [0, 0.20, 0.45, 0.35, 0, 0, 0, 0, 0, 0, 0, 0]
P_LATO = norm([0, 0, 0, 0.5, 1, 1, 1, 1, 0.5, 0, 0, 0])
P_PRZETW = [0, 0, 0, 0, 0, 0.05, 0.15, 0.30, 0.30, 0.20, 0, 0]
P_KURNIK_SW = norm([d * max(0.0, 14 - x) for d, x in zip(DNI, dl)])  # doswietlanie do 14 h dnia swietlnego
P_CHLODNIA = norm([d * max(0.0, t - 0) if m in (7, 8, 9, 10, 11, 0, 1, 2, 3) else 0 for m, (d, t) in enumerate(zip(DNI, IMGW_T))])

h_dosw = sum(d * max(0.0, 14 - x) for d, x in zip(DNI, dl))         # godziny doswietlania kurnika w roku
E_POMPA = 1000 * G * 45 / (0.35 * 3.6e6)                            # kWh/m3
print(f"Energia wlasciwa pompowania: {E_POMPA:.3f} kWh/m3 (H = 45 m, eta = 0.35)")
print(f"Doswietlanie kurnika do 14 h: {h_dosw:.0f} h/rok -> 20 W LED = {20*h_dosw/1000:.0f} kWh/rok")
print(f"Stopniodni grzania Sd(20 st C; miesiace < 12 st C) = {sum(HDD):.0f} K*d")

# woda pompowana [m3/rok]: bytowa 110 l/os./d + drob 9 m3 + podlewanie
woda_byt = {"S": 2 * 0.110 * 365 + 9, "M": 4 * 0.110 * 365 + 9, "L": 6 * 0.110 * 365 + 9}
woda_podl = {"S": 150, "M": 300, "L": 600}

# ---------- lista odbiornikow: (nazwa, S, M, L [kWh/rok], profil) ----------
ODB = [
    ("Lodowko-zamrazarka", 160, 200, 250, P_CHLOD),
    ("Zamrazarki skrzyniowe [Z: 287 l = 227 kWh/a; 497 l = 295 kWh/a]", 227, 227 + 295, 227 + 2 * 295, P_CHLOD),
    ("Oswietlenie LED dom i obejscie", 150, 250, 350, P_SWIATLO),
    ("Gotowanie (indukcja, piekarnik, czajnik)", 250, 550, 800, P_FLAT),
    ("Pralka, zmywarka", 200, 380, 550, P_FLAT),
    ("Elektronika, IT, praca zdalna", 400, 550, 737, P_FLAT),
    ("Drobne AGD, czuwanie", 150, 250, 400, P_FLAT),
    ("Kociol Atmos: wentylator 50 W x h pracy + czuwanie 3 W [Z: 50 W / 3 W]", 61, 81, 113, P_GRZANIE),
    ("Pompy c.o. i ladujaca bufor (50 W + 2-3 x 10 W)", 153, 179, 275, P_GRZANIE),
    ("Pompa glebinowa - woda bytowa i drob", round(E_POMPA * woda_byt["S"]), round(E_POMPA * woda_byt["M"]), round(E_POMPA * woda_byt["L"]), P_FLAT),
    ("Pompa glebinowa - podlewanie", round(E_POMPA * woda_podl["S"]), round(E_POMPA * woda_podl["M"]), round(E_POMPA * woda_podl["L"]), P_PODLEW),
    ("Uzdatnianie: lampa UV 20-30 W ciagle + sterownik 3 W", 200, 290, 290, P_FLAT),
    ("Kurnik: oswietlenie LED 20 W", round(20 * h_dosw / 1000), round(20 * h_dosw / 1000), round(20 * h_dosw / 1000), P_KURNIK_SW),
    ("Kurnik: ochrona poidel przed mrozem (grzalka/przewod z termostatem)", 80, 150, 250, P_MROZ),
    ("Kurnik: elektryzator ogrodzenia 5 W", 44, 44, 44, P_FLAT),
    ("Kurnik: wentylator letni 30 W, paszociag", 0, 56, 56, P_LATO),
    ("Automatyka: serwer HA, siec, kamery, wezly ESP", 250, 420, 535, P_FLAT),
    ("Rozsada: maty grzewcze, LED", 60, 150, 250, P_ROZSADA),
    ("Tunel: sterowanie, wietrzenie", 10, 30, 60, P_LATO),
    ("Robot koszacy", 0, 60, 100, P_LATO),
    ("Warsztat, luparka, narzedzia", 60, 150, 300, P_FLAT),
    ("Przetworstwo: suszarka, pasteryzacja", 50, 120, 250, P_PRZETW),
    ("Chlodnia 6 m3 (tylko L; VIII-IV)", 0, 0, 900, P_CHLODNIA),
    ("Oczyszczalnia przydomowa - dmuchawa 40 W (tylko L)", 0, 0, 350, P_FLAT),
]
CEL = {"S": 3000, "M": 5000, "L": 8000}

wynik = {}
print()
print(f"{'Odbiornik':<72}{'S':>6}{'M':>6}{'L':>6}")
for o in ODB:
    print(f"{o[0]:<72}{o[1]:>6}{o[2]:>6}{o[3]:>6}")
for i, sc in enumerate(["S", "M", "L"]):
    suma = sum(o[1 + i] for o in ODB)
    rezerwa = CEL[sc] - suma
    assert rezerwa >= 0, (sc, suma)
    mies = [0.0] * 12
    for o in ODB:
        for m in range(12):
            mies[m] += o[1 + i] * o[4][m]
    for m in range(12):
        mies[m] += rezerwa * P_FLAT[m]
    assert abs(sum(mies) - CEL[sc]) < 1e-6
    wynik[sc] = mies
    print(f"Scenariusz {sc}: suma odbiornikow {suma} kWh + rezerwa {rezerwa} kWh = {CEL[sc]} kWh/rok")

print("\nRozklad miesieczny [kWh/mies.] i srednio na dobe [kWh/d]:")
print("mies.      S     M     L   |  S/d   M/d   L/d")
for m in range(12):
    print(f"{MIES[m]:>5} {wynik['S'][m]:6.0f}{wynik['M'][m]:6.0f}{wynik['L'][m]:6.0f}   | {wynik['S'][m]/DNI[m]:5.1f} {wynik['M'][m]/DNI[m]:5.1f} {wynik['L'][m]/DNI[m]:5.1f}")
print(f"  ROK {sum(wynik['S']):6.0f}{sum(wynik['M']):6.0f}{sum(wynik['L']):6.0f}")
print("Udzial XI-II w roku: " + ", ".join(f"{sc} {100*(wynik[sc][10]+wynik[sc][11]+wynik[sc][0]+wynik[sc][1])/CEL[sc]:.1f}%" for sc in "SML"))
json.dump(wynik, open("wynik_profil.json", "w"), indent=1)

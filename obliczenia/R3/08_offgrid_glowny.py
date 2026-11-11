# -*- coding: utf-8 -*-
"""08 - Wariant glowny: pelny off-grid, 4 osoby (scenariusz M). Model dobowy z agregatem, 30 lat.

Uzupelnia skrypt 03 o: tryb zimowy M, logike agregatu (doladowanie magazynu), godziny pracy i paliwo, bilans dobowy XII i I, serie dni bez slonca.
Wzory (jedna linia):
  L_zima = suma(P_i * t_i) / 1000                     [kWh/d]  lista odbiornikow trybu zimowego
  E_agr = E_niedobor + E_lad / (eta_lad)              [kWh]    energia na zaciskach agregatu ; eta_lad = 0.95 (ladowarka) ; do magazynu trafia E_lad * eta_c
  t_agr = E_agr / P_agr                               [h]      P_agr = 2.4 kW (agregat 3 kVA przy 80 % mocy)
  V_pal = 0.51 * E_agr                                [dm3]    benzyna (Honda EU32i: 4.6 dm3 / 3.5 h / 2.6 kVA)
  E_seria = N * (L_d - PV_d) - C_uz * eta_d           [kWh]    niedobor w serii N dni bez slonca
"""
import json
import math
import numpy as np
from dane import *

PV = json.load(open("wynik_pv.json"))
LOAD = json.load(open("wynik_profil.json"))
Y50 = {int(k): v for k, v in PV["Y50"].items()}
YK = {int(k): v for k, v in PV["Ykons"].items()}

E_WL = 0.040 * 24
ETA_C = ETA_D = 0.95
ETA_LAD = 0.95
DOD = 0.90
P_AGR = 2.4
H_AGR_MAX = 6.0
SOC_CEL = 0.60
L_KWH = 4.6 / 3.5 / 2.6
CV = [0.90, 0.90, 0.70, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.70, 0.90, 0.90]
Y_CS = [2.6, 3.9, 5.2, 6.3, 6.9, 7.1, 7.0, 6.5, 5.5, 4.2, 2.9, 2.2]
dl = [dlugosc_dnia(n) for n in DNI_KLEINA]
F_DZIEN = [min(0.65, 0.15 + 0.03 * x) for x in dl]
DNI_INT = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
LATA, RHO = 30, 0.4
MIES_DNIA = np.repeat(np.arange(12), DNI_INT)

# ---------- 1. Tryb zimowy M: lista odbiornikow (SZACUNEK) ----------
ZIMA = [  # (odbiornik, moc W, czas h/d)
    ("2 zamrazarki w pomieszczeniu 5-10 st C", 38, 24),
    ("lodowko-zamrazarka", 21, 24),
    ("oswietlenie LED domu", 110, 8),
    ("gotowanie elektryczne (reszta na kuchni drzewnej lub LPG)", 300, 1),
    ("pralka 4 cykle/tydz. + zmywarka zasilana ciepla woda", 650, 1),
    ("laptopy, router domowy, telefony", 100, 8),
    ("kociol: wentylator 50 W przez 5 h + pompa ladujaca 50 W przez 6 h", 50, 11),
    ("pompy c.o. 2 x 10 W", 20, 24),
    ("pompa glebinowa 0.5 m3/d", 1100, 0.2),
    ("lampa UV 16 W na linii wody pitnej", 16, 24),
    ("serwer HA 10 W + siec 15 W + wezly ESP 6 W + 1 kamera 5 W", 36, 24),
    ("kurnik: LED 20 W przez 6 h", 20, 6),
    ("kurnik i owczarnia: ochrona poidel (izolacja + grzalki z termostatem)", 30, 24),
    ("elektryzator 5 W", 5, 24),
    ("drobne i czuwanie", 20, 24),
]
L_ZIMA = sum(p * t for _, p, t in ZIMA) / 1000
print("=== 1. Tryb zimowy M (4 osoby), XI-II ===")
for n, p, t in ZIMA:
    print(f"  {n:<72}{p:>6} W x {t:>4} h = {p*t/1000:5.2f} kWh/d")
print(f"  SUMA: {L_ZIMA:.2f} kWh/d + straty wlasne falownika 0.96 kWh/d = {L_ZIMA+E_WL:.2f} kWh/d  (tryb normalny M w XII: {LOAD['M'][11]/31:.1f} kWh/d + 0.96)")

L_NORM = list(LOAD["M"])
L_TZ = list(LOAD["M"])
for m in (10, 11, 0, 1):
    L_TZ[m] = L_ZIMA * DNI[m]
print(f"  zuzycie roczne: tryb normalny {sum(L_NORM):.0f} kWh ; z trybem zimowym {sum(L_TZ):.0f} kWh (bez strat wlasnych 350 kWh)")


def szereg_g(rng):
    g = np.zeros((LATA, 365))
    for y in range(LATA):
        z, d = 0.0, 0
        for m in range(12):
            s2 = math.log(1 + CV[m] ** 2)
            for _ in range(DNI_INT[m]):
                z = RHO * z + math.sqrt(1 - RHO ** 2) * rng.standard_normal()
                g[y, d] = math.exp(-s2 / 2 + math.sqrt(s2) * z)
                d += 1
    return g


G_BAZA = szereg_g(np.random.default_rng(20261111))


def uzysk_dobowy(Y_mies):
    out = np.zeros_like(G_BAZA)
    for m in range(12):
        idx = MIES_DNIA == m
        sr = Y_mies[m] / DNI_INT[m]
        x = G_BAZA[:, idx] * sr
        for _ in range(4):
            x = np.minimum(x, Y_CS[m] * 1.05)
            x *= sr / x.mean()
        out[:, idx] = np.minimum(x, Y_CS[m] * 1.10)
    return out


def sym(P_pv, C_nom, L_mies, Y_mies, doladuj=True):
    y = uzysk_dobowy(Y_mies) * P_pv
    C = DOD * C_nom
    soc = C * 0.5
    M = {k: np.zeros(12) for k in ("pv", "load", "bezp", "bat", "agr", "nadw")}
    agr_rok = np.zeros(LATA); dni = np.zeros(LATA)
    seria_max = 0; seria = 0
    for yr in range(LATA):
        for d in range(365):
            m = MIES_DNIA[d]
            Ld = L_mies[m] / DNI[m] + E_WL
            pv = y[yr, d]
            bezp = min(pv, F_DZIEN[m] * Ld)
            nadw = pv - bezp
            lad = min(nadw, (C - soc) / ETA_C)
            soc += lad * ETA_C
            reszta = Ld - bezp
            zbat = min(reszta, soc * ETA_D)
            soc -= zbat / ETA_D
            brak = reszta - zbat
            e_agr = 0.0
            if brak > 0.05:
                e_agr = brak
                if doladuj:
                    zapas = max(0.0, P_AGR * H_AGR_MAX - brak)               # energia agregatu dostepna na ladowanie w tej dobie
                    potrzeba = max(0.0, SOC_CEL * C - soc) / (ETA_C * ETA_LAD)  # energia AC potrzebna do osiagniecia SOC docelowego
                    e_lad = min(zapas, potrzeba)
                    soc += e_lad * ETA_LAD * ETA_C
                    e_agr += e_lad
                dni[yr] += 1
                seria += 1
                seria_max = max(seria_max, seria)
            else:
                seria = 0
            agr_rok[yr] += e_agr
            for k, v in (("pv", pv), ("load", Ld), ("bezp", bezp), ("bat", zbat), ("agr", e_agr), ("nadw", nadw - lad)):
                M[k][m] += v
    for k in M:
        M[k] /= LATA
    return dict(M=M, agr=agr_rok.mean(), agr_max=agr_rok.max(), dni=dni.mean(), dni_max=dni.max(), seria_max=seria_max)


print("\n=== 2. Siatka: energia agregatu [kWh/rok] srednia (max rok) ; panele 65 st ; magazyn doladowywany agregatem do 60 % ===")
for nazwa, L in (("tryb normalny M (5000 kWh/rok)", L_NORM), ("M z trybem zimowym (XI-II %.1f kWh/d)" % L_ZIMA, L_TZ)):
    for sc_n, Y in (("scenariusz konserwatywny", YK[65]), ("P50", Y50[65])):
        print(f"-- {nazwa} ; {sc_n} --")
        print("  kWp\\kWh " + "".join(f"{c:>16}" for c in (20, 30, 40)))
        for P in (10, 12, 15, 18, 20, 25):
            w = []
            for C in (20, 30, 40):
                r = sym(P, C, L, Y)
                w.append(f"{r['agr']:6.0f} ({r['agr_max']:4.0f})")
            print(f"  {P:>7}   " + "  ".join(f"{x:>14}" for x in w))

print("\n=== 3. Konfiguracja glowna: 15 kWp (65 st, S) + 30 kWh LiFePO4 + agregat 3 kVA ; M z trybem zimowym ===")
for sc_n, Y in (("scenariusz konserwatywny", YK[65]), ("P50", Y50[65])):
    r = sym(15, 30, L_TZ, Y)
    M = r["M"]
    print(f"-- {sc_n}: bilans miesieczny [kWh] --")
    print("  mies.  produkcja  zuzycie  bezposr.  z magazynu  agregat  nadwyzka niewykorzystana")
    for m in range(12):
        print(f"  {MIES[m]:>5} {M['pv'][m]:9.0f} {M['load'][m]:8.0f} {M['bezp'][m]:9.0f} {M['bat'][m]:11.0f} {M['agr'][m]:8.0f} {M['nadw'][m]:10.0f}")
    print(f"    ROK {M['pv'].sum():9.0f} {M['load'].sum():8.0f} {M['bezp'].sum():9.0f} {M['bat'].sum():11.0f} {M['agr'].sum():8.0f} {M['nadw'].sum():10.0f}")
    e = r["agr"]
    print(f"  agregat: {e:.0f} kWh/rok (max rok {r['agr_max']:.0f}) ; {e/P_AGR:.0f} h/rok (max {r['agr_max']/P_AGR:.0f}) ; benzyna {e*L_KWH:.0f} dm3/rok (max {r['agr_max']*L_KWH:.0f}) ; LPG {e*0.36:.0f} kg/rok ; dni pracy {r['dni']:.0f} (max {r['dni_max']:.0f}) ; najdluzsza seria dni z agregatem {r['seria_max']}")
    print(f"  udzial agregatu w zuzyciu: {100*e/M['load'].sum():.1f} %")
for opis, P, C, L in (("15 kWp/30 kWh, tryb NORMALNY zima", 15, 30, L_NORM), ("12 kWp/30 kWh, tryb zimowy", 12, 30, L_TZ), ("20 kWp/30 kWh, tryb zimowy", 20, 30, L_TZ), ("15 kWp/20 kWh, tryb zimowy", 15, 20, L_TZ), ("15 kWp/40 kWh, tryb zimowy", 15, 40, L_TZ)):
    for sc_n, Y in (("kons.", YK[65]), ("P50", Y50[65])):
        r = sym(P, C, L, Y)
        print(f"  porownanie {opis:<36} {sc_n:<6}: agregat {r['agr']:5.0f} kWh/rok = {r['agr']/P_AGR:4.0f} h = {r['agr']*L_KWH:4.0f} dm3 benzyny ; max rok {r['agr_max']:5.0f} kWh ; dni {r['dni']:3.0f}")
r35 = sym(15, 30, L_TZ, YK[35]); r35p = sym(15, 30, L_TZ, Y50[35])
print(f"  panele 35 st zamiast 65 st: agregat {r35['agr']:.0f} kWh/rok (kons.), {r35p['agr']:.0f} kWh/rok (P50)")
rb = sym(15, 30, L_TZ, YK[65], doladuj=False)
print(f"  bez doladowania magazynu z agregatu (tylko pokrycie niedoboru): {rb['agr']:.0f} kWh/rok, dni pracy {rb['dni']:.0f}")

print("\n=== 4. Bilans dobowy grudnia i stycznia: 15 kWp (65 st), tryb zimowy ===")
Ld = L_ZIMA + E_WL
C_wy = DOD * 30 * ETA_D
print(f"  zuzycie doby {Ld:.2f} kWh ; energia uzyteczna magazynu na wyjsciu {C_wy:.1f} kWh = {C_wy/Ld:.1f} doby bez produkcji")
for m in (11, 0):
    for opis, yj in (("doba pochmurna (20 % sredniej kons.)", 0.2 * YK[65][m] / DNI[m]), ("doba srednia, scenariusz kons.", YK[65][m] / DNI[m]), ("doba srednia, P50", Y50[65][m] / DNI[m]), ("doba bezchmurna", Y_CS[m] * 1.05)):
        pv = 15 * yj
        bezp = min(pv, F_DZIEN[m] * Ld)
        do_mag = max(0.0, pv - bezp)
        z_mag = Ld - bezp
        saldo = do_mag * ETA_C * ETA_D - z_mag
        print(f"  {MIES[m]:>3} {opis:<38}: PV {pv:5.1f} kWh ({yj:.2f} kWh/kWp) ; bezposrednio {bezp:4.1f} ; do magazynu {do_mag:5.1f} ; potrzeba z magazynu {z_mag:4.1f} ; saldo doby {saldo:+6.1f} kWh")
print("  Podzial doby grudnia [kWh]: noc 22-06: 8 h x 0.22 kW = 1.8 ; rano 06-09: 3 h x 0.50 kW = 1.5 ; dzien 09-15: 6 h x 0.40 kW = 2.4 ; wieczor 15-22: 7 h x 0.47 kW = 3.3 (SZACUNEK)")

print("\n=== 5. Seria dni bez slonca (uzysk = 20 % sredniej scenariusza konserwatywnego), magazyn pelny na poczatku ===")
for m in (11, 0):
    pv_d = 15 * 0.2 * YK[65][m] / DNI[m]
    for N in (3, 5, 7, 11, 14):
        niedobor = N * (Ld - pv_d)
        z_agr = max(0.0, niedobor - C_wy)
        print(f"  {MIES[m]:>3}, seria {N:>2} dni: PV {pv_d:.1f} kWh/d ; niedobor {niedobor:5.1f} kWh ; z magazynu {min(niedobor, C_wy):4.1f} ; z agregatu {z_agr:5.1f} kWh = {z_agr/P_AGR:4.1f} h = {z_agr*L_KWH:4.1f} dm3 benzyny")
print(f"  magazyn 30 kWh wystarcza na {C_wy/(Ld-15*0.2*YK[65][11]/31):.1f} doby serii grudniowej ; tryb normalny (15.2 kWh/d): {C_wy/(LOAD['M'][11]/31+E_WL-15*0.2*YK[65][11]/31):.1f} doby")

print("\n=== 6. Geometria paneli 65 st ===")
h_sl = 90 - 53.7875 - 23.44
print(f"  wysokosc Slonca w poludnie 21 grudnia (53.7875 N): {h_sl:.2f} st ; cien przeszkody o wysokosci H siega {1/math.tan(math.radians(h_sl)):.1f} x H")
slant = 2 * 1.134
print(f"  stol 2 moduly w poziomie (2 x 1.134 m): wysokosc pionowa {slant*math.sin(math.radians(65)):.2f} m ; rzut {slant*math.cos(math.radians(65)):.2f} m ; odstep rzedow dla braku cienia w poludnie 21 XII: {slant*math.sin(math.radians(65))/math.tan(math.radians(h_sl)):.1f} m")
print(f"  15 kWp = 33 moduly 455 Wp ; 1 rzad 2-pietrowy: 17 kolumn x 1.762 m = {17*1.762:.0f} m dlugosci ; drzewa 20 m rzucaja cien {20/math.tan(math.radians(h_sl)):.0f} m w poludnie 21 XII")

print("\n=== 7. Nadwyzka letnia do zagospodarowania (kons., 15 kWp, 65 st) ===")
r = sym(15, 30, L_TZ, YK[65])
n = r["M"]["nadw"]
print("  [kWh/mies.]: " + " ".join(f"{MIES[m]}:{n[m]:.0f}" for m in range(12)) + f" ; rok {n.sum():.0f}")
print(f"  III+IV+X: {n[2]+n[3]+n[9]:.0f} kWh -> grzalki w buforze zastepuja {(n[2]+n[3]+n[9])*0.95/0.78/1409:.1f} mp sosny ; V-IX: {n[4:9].sum():.0f} kWh (c.w.u. 4 osob V-IX potrzebuje {11.06*153:.0f} kWh)")

# -*- coding: utf-8 -*-
"""03 - Bilans PV + magazyn LiFePO4: warianty (a) on-grid net-billing + backup, (b) autonomia bilansowa, (c) off-grid.

Model dobowy (symulacja 30 lat, ziarno stale):
  PV_d = Y_m/D_m * P_PV * g_d                [kWh/d]  g_d: losowa zmiennosc dobowa (srednia 1)
  L_d  = L_m/D_m + E_wl                      [kWh/d]  E_wl = 0.040 kW * 24 h = 0.96 kWh/d (falownik hybrydowy + BMS, SZACUNEK)
  E_bezp = min(PV_d, f_m * L_d)              f_m = min(0.65, 0.15 + 0.03*dlugosc_dnia[h])  udzial zuzycia w godzinach pracy PV (SZACUNEK)
  ladowanie: SOC += eta_c*min(PV_d - E_bezp, (C_uz - SOC)/eta_c) ; rozladowanie: E_bat = min(L_d - E_bezp, SOC*eta_d)
  C_uz = 0.90 * C_nom (glebokosc rozladowania 90 %) ; eta_c = eta_d = 0.95 (sprawnosc cyklu 0.90) - SZACUNEK typowy dla LiFePO4
  g_d = lognormalny, CV: XI-II 0.90; III i X 0.70; IV-IX 0.45; autokorelacja AR(1) rho = 0.4 - SZACUNEK (brak danych dobowych PVGIS)
  g_d ograniczone uzyskiem dnia bezchmurnego Y_cs [kWh/kWp/d] (SZACUNEK) i przeskalowane do sredniej miesiecznej.
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
DOD = 0.90
CV = [0.90, 0.90, 0.70, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.70, 0.90, 0.90]
Y_CS = [2.6, 3.9, 5.2, 6.3, 6.9, 7.1, 7.0, 6.5, 5.5, 4.2, 2.9, 2.2]   # kWh/kWp/d, dzien bezchmurny, 35 st S (SZACUNEK)
dl = [dlugosc_dnia(n) for n in DNI_KLEINA]
F_DZIEN = [min(0.65, 0.15 + 0.03 * x) for x in dl]
DNI_INT = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
LATA = 30
RHO = 0.4


def szereg_g(rng):
    """Dobowe mnozniki uzysku g_d dla LATA lat: tablica [LATA, 365]."""
    g = np.zeros((LATA, 365))
    for y in range(LATA):
        z = 0.0
        d = 0
        for m in range(12):
            s2 = math.log(1 + CV[m] ** 2)
            for _ in range(DNI_INT[m]):
                z = RHO * z + math.sqrt(1 - RHO ** 2) * rng.standard_normal()
                g[y, d] = math.exp(-s2 / 2 + math.sqrt(s2) * z)
                d += 1
    return g


RNG = np.random.default_rng(20261111)
G_BAZA = szereg_g(RNG)
MIES_DNIA = np.repeat(np.arange(12), DNI_INT)


def uzysk_dobowy(Y_mies):
    """Dobowy uzysk jednostkowy [kWh/kWp/d], [LATA,365]; ograniczenie dniem bezchmurnym i zachowanie sredniej miesiecznej."""
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


def symulacja(P_pv, C_nom, L_mies, Y_mies, wlasne=E_WL):
    y = uzysk_dobowy(Y_mies) * P_pv
    C = DOD * C_nom
    soc = C * 0.5
    res = dict(pv=0.0, bezp=0.0, bat=0.0, eksport=0.0, importe=0.0, load=0.0)
    imp_rok = np.zeros(LATA)
    dni_imp = np.zeros(LATA)
    imp_mies = np.zeros(12)
    eks_mies = np.zeros(12)
    for yr in range(LATA):
        for d in range(365):
            m = MIES_DNIA[d]
            Ld = L_mies[m] / DNI_INT[m] * (DNI[m] / DNI_INT[m]) + wlasne
            pv = y[yr, d]
            bezp = min(pv, F_DZIEN[m] * Ld)
            nadw = pv - bezp
            lad = min(nadw, (C - soc) / ETA_C) if C > 0 else 0.0
            soc += lad * ETA_C
            eks = nadw - lad
            reszta = Ld - bezp
            zbat = min(reszta, soc * ETA_D) if C > 0 else 0.0
            soc -= zbat / ETA_D
            imp = reszta - zbat
            res["pv"] += pv; res["bezp"] += bezp; res["bat"] += zbat; res["eksport"] += eks; res["importe"] += imp; res["load"] += Ld
            imp_rok[yr] += imp
            imp_mies[m] += imp
            eks_mies[m] += eks
            if imp > 0.05:
                dni_imp[yr] += 1
    for k in res:
        res[k] /= LATA
    res["imp_max_rok"] = imp_rok.max()
    res["dni_imp"] = dni_imp.mean()
    res["imp_mies"] = imp_mies / LATA
    res["eks_mies"] = eks_mies / LATA
    return res


def pokaz(nazwa, P, C, sc, Y, opis):
    r = symulacja(P, C, LOAD[sc], Y)
    aut = 1 - r["importe"] / r["load"]
    auto = (r["bezp"] + r["bat"] / ETA_D) / r["pv"] if r["pv"] > 0 else 0
    print(f"{nazwa:<4}{sc}  PV {P:5.1f} kWp  mag. {C:4.0f} kWh  {opis:<14} produkcja {r['pv']:6.0f}  zuzycie {r['load']:5.0f}  pobor z sieci/agregatu {r['importe']:5.0f} (max rok {r['imp_max_rok']:5.0f})  nadwyzka {r['eksport']:6.0f}  samowystarczalnosc {100*aut:5.1f}%  dni z poborem {r['dni_imp']:5.0f}")
    return r


print("=== A. Bilans miesieczny deterministyczny: produkcja P50 (35 st) vs zuzycie [kWh] na 1 kWp ===")
print("mies.  Y50(35)  Ykons(35)  Ykons(65)   L_S   L_M   L_L   kWp potrzebne w danym miesiacu (kons., 65 st): S / M / L")
for m in range(12):
    need = [(LOAD[sc][m] + E_WL * DNI[m]) / YK[65][m] for sc in "SML"]
    print(f"{MIES[m]:>5} {Y50[35][m]:8.1f} {YK[35][m]:10.1f} {YK[65][m]:10.1f} {LOAD['S'][m]:6.0f}{LOAD['M'][m]:6.0f}{LOAD['L'][m]:6.0f}   {need[0]:6.1f} / {need[1]:6.1f} / {need[2]:6.1f}")

print("\n=== B. Wariant (a): on-grid, net-billing, zasilanie awaryjne; uzysk P50, dach 35 st [kWh/rok] ===")
A = {"S": (3.0, 5), "M": (5.0, 10), "L": (8.0, 10)}
ra = {sc: pokaz("(a)", *A[sc], sc, Y50[35], "P50 35st") for sc in "SML"}
print("   to samo w zlym roku (scenariusz konserwatywny):")
for sc in "SML":
    pokaz("(a)", *A[sc], sc, YK[35], "kons. 35st")

print("\n=== C. Wariant (b): autonomia bilansowa, siec jako rezerwa ===")
B = {"S": (6.0, 10), "M": (10.0, 20), "L": (16.0, 30)}
rb = {sc: pokaz("(b)", *B[sc], sc, Y50[35], "P50 35st") for sc in "SML"}
for sc in "SML":
    pokaz("(b)", *B[sc], sc, YK[35], "kons. 35st")
print("   Pobor i nadwyzka miesieczne dla (b) M, P50 [kWh]: ")
print("   mies.: " + " ".join(f"{x:>5}" for x in MIES))
print("   pobor: " + " ".join(f"{x:5.0f}" for x in rb["M"]["imp_mies"]))
print("   nadw.: " + " ".join(f"{x:5.0f}" for x in rb["M"]["eks_mies"]))

print("\n=== D. Wariant (c): off-grid; scenariusz konserwatywny; panele 65 st S; energia z agregatu [kWh/rok] (srednia z 30 lat) ===")
PVs = [6, 8, 10, 12, 15, 20, 25, 30, 40]
BATs = [10, 15, 20, 30, 40, 60]
KOSZT_PV, KOSZT_BAT, KOSZT_AGR_KWH = 4000.0, 1400.0, 3.5   # PLN/kWp, PLN/kWh, PLN/kWh z agregatu (paliwo + obsluga) - SZACUNEK
siatka = {}
for sc in "SML":
    print(f"-- scenariusz {sc} ({sum(LOAD[sc]):.0f} kWh/rok + straty wlasne {E_WL*365:.0f} kWh/rok) --")
    print("  kWp\\kWh " + "".join(f"{b:>8}" for b in BATs))
    for P in PVs:
        wiersz = []
        for C in BATs:
            r = symulacja(P, C, LOAD[sc], YK[65])
            siatka[(sc, P, C)] = r
            wiersz.append(r["importe"])
        print(f"  {P:>7} " + "".join(f"{x:8.0f}" for x in wiersz))
    best = sorted(((P * KOSZT_PV + C * KOSZT_BAT * 1.5 + 20 * siatka[(sc, P, C)]["importe"] * KOSZT_AGR_KWH, P, C) for P in PVs for C in BATs))[:4]
    print("  Najtansze w 20 lat (PV + 1.5 x magazyn [wymiana po ok. 15 latach] + paliwo): " + "; ".join(f"{P} kWp/{C} kWh -> {k/1000:.0f} tys. PLN, agregat {siatka[(sc,P,C)]['importe']:.0f} kWh/rok, max {siatka[(sc,P,C)]['imp_max_rok']:.0f}, dni {siatka[(sc,P,C)]['dni_imp']:.0f}" for k, P, C in best))

print("\n=== E. Off-grid: porownanie kata 35 st vs 65 st (kons.) i roku P50, wybrane konfiguracje ===")
C_WYB = {"S": (10, 20), "M": (15, 30), "L": (25, 40)}
for sc in "SML":
    P, C = C_WYB[sc]
    pokaz("(c)", P, C, sc, YK[65], "kons. 65st")
    pokaz("(c)", P, C, sc, YK[35], "kons. 35st")
    pokaz("(c)", P, C, sc, Y50[65], "P50 65st")

print("\n=== F. Dni autonomii magazynu przy zerowej produkcji (grudzien) ===")
for sc in "SML":
    Ld = LOAD[sc][11] / 31 + E_WL
    for C in (10, 20, 30, 40):
        print(f"  {sc}: zuzycie {Ld:4.1f} kWh/d, magazyn {C} kWh (uzyteczne {DOD*C:.0f} kWh, na wyjsciu {DOD*C*ETA_D:.1f}) -> {DOD*C*ETA_D/Ld:.1f} d")

print("\n=== G. Agregat: paliwo ===")
l_kwh = 4.6 / 3.5 / 2.6   # Honda EU32i: zbiornik 4.6 l, 3 h 30 min przy mocy znamionowej 2.6 kVA (karta producenta) -> l/kWh przy cos fi = 1
kg_lpg = 1 / (12.8 * 0.22)  # LPG: wartosc opalowa 12.8 kWh/kg, sprawnosc agregatu 22 % (SZACUNEK)
print(f"  benzyna: {l_kwh:.2f} l/kWh (z danych Honda EU32i) ; LPG: {kg_lpg:.2f} kg/kWh (SZACUNEK) ; gaz drzewny: 1.0 kg suchej biomasy/kWh (karta APL PP30)")
for e in (150, 300, 600, 1000):
    print(f"  {e:>5} kWh/rok z agregatu -> benzyna {e*l_kwh/0.9:5.0f} l, LPG {e*kg_lpg/0.9:5.0f} kg, drewno (gazogenerator) {e*1.0/0.9:5.0f} kg  [ladowarka 90 %]")

print("\n=== H. Mala turbina wiatrowa: rozklad Rayleigha, v_sr(10 m) = 2.9 m/s (IMGW Olsztyn 1991-2010) ===")
# v(h) = v10*(h/10)^alfa ; <v^3> = (6/pi)*v_sr^3 (Rayleigh) ; P_sr = 0.5*rho*A*Cp*<v^3> ; E = P_sr*8760
for h, alfa in ((10, 0.22), (15, 0.22), (18, 0.22), (24, 0.22)):
    v = 2.9 * (h / 10) ** alfa
    v3 = 6 / math.pi * v ** 3
    for D, Pn in ((3.6, 3.0),):
        A_r = math.pi * D ** 2 / 4
        P_sr = 0.5 * 1.225 * A_r * 0.25 * v3
        print(f"  maszt {h:>2} m: v_sr = {v:.2f} m/s, gestosc mocy {0.5*1.225*v3:5.1f} W/m2, turbina {Pn} kW (D = {D} m, Cp calk. 0.25): {P_sr:5.0f} W srednio = {P_sr*8.76:5.0f} kWh/rok, CF = {100*P_sr/1000/Pn:.1f}%")
print("  Porownanie: badanie IMGW-PIB (173 stacje, 10 m): sredni CF 3.75 % = ok. 328 kWh/kW/rok.")

print("\n=== I. Off-grid z ograniczeniem zuzycia zima ('tryb zimowy': XI-II 6.0 kWh/d lacznie ze stratami wlasnymi 0.72 kWh/d) ===")
# tryb zimowy: tylko odbiorniki krytyczne (zamrazarki, lodowka, pompy, kociol, oswietlenie LED, serwer); SZACUNEK
L_ZIMA = list(LOAD["S"])
for m in (10, 11, 0, 1):
    L_ZIMA[m] = (6.0 - 0.72) * DNI[m]
print(f"  zuzycie roczne w trybie zimowym: {sum(L_ZIMA):.0f} kWh + straty wlasne {0.030*24*365:.0f} kWh (30 W)")
print("  kWp\\kWh " + "".join(f"{b:>8}" for b in (15, 20, 30, 40)))
for P in (8, 10, 12, 15, 20, 25):
    w = []
    for C in (15, 20, 30, 40):
        r = symulacja(P, C, L_ZIMA, YK[65], wlasne=0.030 * 24)
        w.append(f"{r['importe']:5.0f}/{r['imp_max_rok']:<4.0f}")
    print(f"  {P:>7}   " + "  ".join(w) + "   [srednia/max rok, kWh z agregatu]")
r = symulacja(12, 30, L_ZIMA, Y50[65], wlasne=0.030 * 24)
print(f"  12 kWp / 30 kWh w roku P50: agregat {r['importe']:.0f} kWh/rok (max {r['imp_max_rok']:.0f}), dni z agregatem {r['dni_imp']:.0f}")

print("\n=== J. Wplyw turbiny wiatrowej 3 kW (maszt 18 m, 937 kWh/rok) na off-grid M: 15 kWp / 30 kWh, scenariusz kons. ===")
# rozklad miesieczny energii wiatru ~ v_m^3 ; v_m = 2.9 + 0.45*cos(2*pi*(m-1.5)/12) [m/s] (II max 3.3, VIII min 2.3 wg Pozarska i Grabowski 2015; ksztalt przyjety - SZACUNEK)
v_m = [2.9 + 0.45 * math.cos(2 * math.pi * (m - 1.0) / 12) for m in range(12)]
wagi = [d * v ** 3 for d, v in zip(DNI, v_m)]
E_W = [937 * w / sum(wagi) for w in wagi]
print("  energia turbiny [kWh/mies.]: " + " ".join(f"{x:4.0f}" for x in E_W) + f"  suma {sum(E_W):.0f}")
rng2 = np.random.default_rng(7)
def symulacja_wiatr(P_pv, C_nom, L_mies, Y_mies, E_wiatr):
    y = uzysk_dobowy(Y_mies) * P_pv
    C = DOD * C_nom
    soc = C * 0.5
    imp = 0.0
    s2 = math.log(1 + 1.2 ** 2)   # CV dobowej energii wiatru 1.2 (SZACUNEK), niezalezna od PV
    for yr in range(LATA):
        for d in range(365):
            m = MIES_DNIA[d]
            Ld = L_mies[m] / DNI_INT[m] * (DNI[m] / DNI_INT[m]) + E_WL
            w = E_wiatr[m] / DNI_INT[m] * math.exp(-s2 / 2 + math.sqrt(s2) * rng2.standard_normal())
            pv = y[yr, d]
            bezp = min(pv, F_DZIEN[m] * Ld) 
            reszta = Ld - bezp
            bw = min(w, reszta)          # wiatr pokrywa zuzycie poza godzinami PV bezposrednio
            reszta -= bw
            nadw = pv - bezp + (w - bw)
            lad = min(nadw, (C - soc) / ETA_C)
            soc += lad * ETA_C
            zbat = min(reszta, soc * ETA_D)
            soc -= zbat / ETA_D
            imp += reszta - zbat
    return imp / LATA
bez = symulacja(15, 30, LOAD["M"], YK[65])["importe"]
zw = symulacja_wiatr(15, 30, LOAD["M"], YK[65], E_W)
print(f"  agregat bez turbiny: {bez:.0f} kWh/rok ; z turbina: {zw:.0f} kWh/rok ; oszczednosc {bez-zw:.0f} kWh/rok = {(bez-zw)*l_kwh/0.9:.0f} l benzyny/rok")

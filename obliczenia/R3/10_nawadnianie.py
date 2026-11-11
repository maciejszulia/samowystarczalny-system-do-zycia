# -*- coding: utf-8 -*-
"""10 - Nawadnianie warzywnika na glebie lekkiej (klasa V-VI): ET0 wg FAO-56 Penman-Monteith + dobowy bilans wody w strefie korzeni.

Wzory (jedna linia):
  ET0 = [0.408*D*(Rn - G) + g*900/(T + 273)*u2*(es - ea)] / [D + g*(1 + 0.34*u2)]      [mm/d]  FAO-56 rown. 6
  ETc = Kc * ET0                                                                        [mm/d]
  TAW = 1000*(th_FC - th_WP)*Zr ; RAW = p*TAW                                           [mm]    FAO-56 rown. 82, 83
  Dr(t) = Dr(t-1) - P_ef(t) - I(t) + ETc(t) ; jezeli Dr < 0, to nadmiar przesiaka ponizej korzeni (Dr = 0)
  nawadnianie: gdy Dr >= RAW, dawka netto I = Dr ; dawka brutto = I / 0.9 (nawadnianie kroplowe)
Dane: T, opad, liczba dni z opadem, wilgotnosc - normy 1991-2020 (IMGW / meteomodel za Wikipedia) ; Rs - Global Solar Atlas ; wiatr - Pozarska i Grabowski 2015.
"""
import math
import numpy as np
from dane import *

MS = [3, 4, 5, 6, 7, 8]                                   # IV..IX
RH = {3: 69.9, 4: 70.4, 5: 72.6, 6: 74.7, 7: 75.3, 8: 80.7}
U10 = {3: 3.0, 4: 2.7, 5: 2.5, 6: 2.4, 7: 2.3, 8: 2.5}    # m/s (SZACUNEK ksztaltu ; srednia roczna 2.9, VIII 2.3)
DNI_OPAD = [17.37, 15.00, 14.13, 12.40, 13.50, 14.30, 14.43, 13.33, 13.03, 14.13, 15.57, 17.63]
KC = {3: 0.60, 4: 0.80, 5: 1.00, 6: 1.05, 7: 1.00, 8: 0.85}  # warzywnik mieszany (SZACUNEK na podstawie FAO-56 tab. 12: 0.7 / 1.05 / 0.95)
Z = 110.0
fi = math.radians(53.7875)
e0 = lambda T: 0.6108 * math.exp(17.27 * T / (T + 237.3))
ET0 = {}
print("=== 1. ET0 wg FAO-56 [mm/d] ===")
for m in MS:
    T = IMGW_T[m]; Tmax, Tmin = T + 5.5, T - 5.5        # amplituda dobowa 11 K (SZACUNEK)
    J = DNI_KLEINA[m]
    dr = 1 + 0.033 * math.cos(2 * math.pi * J / 365)
    d = 0.409 * math.sin(2 * math.pi * J / 365 - 1.39)
    ws = math.acos(-math.tan(fi) * math.tan(d))
    Ra = 24 * 60 / math.pi * 0.0820 * dr * (ws * math.sin(fi) * math.sin(d) + math.cos(fi) * math.cos(d) * math.sin(ws))
    Rs = GSA_GHI[m] * 3.6 / DNI[m]
    Rso = (0.75 + 2e-5 * Z) * Ra
    es = (e0(Tmax) + e0(Tmin)) / 2
    ea = RH[m] / 100 * es
    Rnl = 4.903e-9 * ((Tmax + 273.16) ** 4 + (Tmin + 273.16) ** 4) / 2 * (0.34 - 0.14 * math.sqrt(ea)) * (1.35 * min(1.0, Rs / Rso) - 0.35)
    Rn = 0.77 * Rs - Rnl
    G_ = 0.07 * (IMGW_T[m + 1] - IMGW_T[m - 1])
    D = 4098 * e0(T) / (T + 237.3) ** 2
    P = 101.3 * ((293 - 0.0065 * Z) / 293) ** 5.26
    g = 0.000665 * P
    u2 = U10[m] * 4.87 / math.log(67.8 * 10 - 5.42)
    ET0[m] = (0.408 * D * (Rn - G_) + g * 900 / (T + 273) * u2 * (es - ea)) / (D + g * (1 + 0.34 * u2))
    print(f"  {MIES[m]:>4}: Rs {Rs:5.1f} MJ/m2/d ; Rn {Rn:5.1f} ; u2 {u2:.2f} m/s ; ET0 {ET0[m]:.2f} mm/d = {ET0[m]*DNI[m]:5.0f} mm/mies. ; Kc {KC[m]:.2f} ; ETc {KC[m]*ET0[m]:.2f} mm/d = {KC[m]*ET0[m]*DNI[m]:5.0f} mm ; opad {IMGW_OPAD[m]:.1f} mm")
print(f"  suma IV-IX: ET0 {sum(ET0[m]*DNI[m] for m in MS):.0f} mm ; ETc {sum(KC[m]*ET0[m]*DNI[m] for m in MS):.0f} mm ; opad {sum(IMGW_OPAD[m] for m in MS):.1f} mm")

DI = {3: 30, 4: 31, 5: 30, 6: 31, 7: 31, 8: 30}
def sezon(rng, TAW, p=0.35, k_opad=1.0):
    RAW = p * TAW
    Dr = 0.0; I = 0.0; n = 0; maks7 = 0.0; okno = []
    for m in MS:
        pw = DNI_OPAD[m] / DNI[m]
        sr = IMGW_OPAD[m] * k_opad / DNI_OPAD[m]
        for _ in range(DI[m]):
            P = rng.exponential(sr) if rng.random() < pw else 0.0
            if P < 0.2 * ET0[m]:
                P = 0.0
            Dr = max(0.0, Dr - P) + KC[m] * ET0[m]
            dawka = 0.0
            if Dr >= RAW:
                dawka = Dr / 0.9; Dr = 0.0; n += 1
            I += dawka
            okno.append(dawka); okno = okno[-7:]
            maks7 = max(maks7, sum(okno))
    return I, n, maks7

print("\n=== 2. Potrzeby nawadniania brutto [mm = dm3/m2 na sezon IV-IX], 300 sezonow losowych ===")
rng = np.random.default_rng(5)
WYN = {}
for opis, TAW in (("piasek luzny: 60 mm/m x 0.4 m = 24 mm", 24.0), ("piasek gliniasty: 90 mm/m x 0.4 m = 36 mm (FAO-56, przyklad 36)", 36.0), ("glina: 150 mm/m x 0.4 m = 60 mm (porownanie)", 60.0)):
    for k, on in ((1.0, "opad normalny"), (0.6, "opad 60 % normy")):
        r = np.array([sezon(rng, TAW, k_opad=k) for _ in range(300)])
        WYN[(TAW, k)] = r
        print(f"  {opis:<62} {on:<16}: srednio {r[:,0].mean():4.0f} mm ; decyl 10 % {np.percentile(r[:,0],10):4.0f} ; decyl 90 % {np.percentile(r[:,0],90):4.0f} ; nawodnien {r[:,1].mean():3.0f} ; dawka {r[:,0].mean()/r[:,1].mean():4.1f} mm ; szczyt 7 dni {np.percentile(r[:,2],90):4.0f} mm")
r = WYN[(36.0, 1.0)]; rs = WYN[(36.0, 0.6)]
print("\n=== 3. Wynik dla warzywnika (piasek gliniasty, TAW 36 mm, RAW 12.6 mm) ===")
for A in (1000, 1500, 2000):
    sr, d90, such = r[:, 0].mean() * A / 1000, np.percentile(r[:, 0], 90) * A / 1000, rs[:, 0].mean() * A / 1000
    szczyt = np.percentile(r[:, 2], 90) * A / 1000 / 7
    print(f"  {A} m2: srednio {sr:4.0f} m3/sezon ; rok suchy co 10 lat {d90:4.0f} m3 ; opad 60 % normy {such:4.0f} m3 ; szczyt {szczyt:4.1f} m3/d ; energia pompy 0.44 kWh/m3: {sr*0.44:4.0f}-{such*0.44:4.0f} kWh/sezon, szczyt {szczyt*0.44:.1f} kWh/d ; praca pompy 2.2 m3/h: {szczyt/2.2:.1f} h/d")
print(f"  odstep miedzy nawodnieniami w lipcu: RAW / ETc = {0.35*36/(KC[6]*ET0[6]):.1f} d (piasek gliniasty) ; {0.35*24/(KC[6]*ET0[6]):.1f} d (piasek luzny)")
print(f"  produkcja PV 15 kWp (65 st, scenariusz kons.) w lipcu: {15*109.2/31:.0f} kWh/d ; pompa w szczycie zuzywa {100*np.percentile(r[:,2],90)*2/7*0.44/(15*109.2/31):.1f} % tej produkcji przy 2000 m2")
print(f"  pobor roczny (4 osoby 161 + zwierzeta 15 + warzywnik 2000 m2 w roku suchym {rs[:,0].mean()*2:.0f} + tunel 47 m3) = {161+15+rs[:,0].mean()*2+47:.0f} m3 = {(161+15+rs[:,0].mean()*2+47)/365:.2f} m3/d srednio (limit zwyklego korzystania z wod: 5 m3/d)")

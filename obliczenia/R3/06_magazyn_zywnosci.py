# -*- coding: utf-8 -*-
"""06 - Magazyn zywnosci: temperatura gruntu, wentylacja piwnicy ziemnej, wymiary, zamrazarki, ziarno, suszarka solarna.

Wzory (jedna linia):
  T(z,t) = T_sr + A0 * exp(-z/d) * cos(2*pi*(t - t0)/365 - z/d)     [st C]  fala roczna temperatury w gruncie (przewodzenie 1D)
  d = sqrt(2*a/omega) = sqrt(a*tau/pi)                               [m]    glebokosc tlumienia ; a = dyfuzyjnosc cieplna gruntu ; tau = 365 d
  V' = Cd * A * sqrt(2*g*h*dT/T_sr)                                  [m3/s] ciag grawitacyjny w kanale o wysokosci czynnej h
  m_wody = E_slon * eta / 0.68                                       [kg]   suszarka: 0.68 kWh na 1 kg odparowanej wody
"""
import math
from dane import *

print("=== 1. Temperatura gruntu na glebokosci z (T_sr = 9.0 st C [powietrze 8.0 + 1 K], A0 = 10.15 K, a = 0.6e-6 m2/s -> d) ===")
a = 0.6e-6
tau = 365 * 86400
d = math.sqrt(a * tau / math.pi)
print(f"  glebokosc tlumienia d = {d:.2f} m (dla a = 0.4e-6: {math.sqrt(0.4e-6*tau/math.pi):.2f} m ; a = 0.9e-6: {math.sqrt(0.9e-6*tau/math.pi):.2f} m)")
T_SR, A0, T0 = 9.0, (IMGW_T[6] - IMGW_T[0]) / 2, 198   # maksimum fali na powierzchni ok. 17 lipca (dzien 198)
srodki = [16, 46, 75, 106, 136, 167, 197, 228, 259, 289, 320, 350]
print("  z [m]  " + " ".join(f"{m:>5}" for m in MIES) + "   min   max")
for z in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
    T = [T_SR + A0 * math.exp(-z / d) * math.cos(2 * math.pi * (t - T0) / 365 - z / d) for t in srodki]
    print(f"  {z:4.1f}   " + " ".join(f"{x:5.1f}" for x in T) + f"  {min(T):5.1f} {max(T):5.1f}")
print(f"  przesuniecie fazowe na 2.0 m: {2.0/d*365/(2*math.pi):.0f} d ; amplituda {A0*math.exp(-2.0/d):.1f} K")

print("\n=== 2. Wentylacja grawitacyjna piwnicy: strumien powietrza [m3/h] (Cd = 0.6, T_sr = 275 K) ===")
print("  srednica  h[m]   dT=3K   dT=5K   dT=10K  dT=15K")
for D in (0.110, 0.160):
    A = math.pi * D ** 2 / 4
    for h in (2.0, 3.0):
        w = [0.6 * A * math.sqrt(2 * G * h * dT / 275) * 3600 for dT in (3, 5, 10, 15)]
        print(f"  {1000*D:5.0f} mm  {h:3.1f}  " + " ".join(f"{x:7.0f}" for x in w))

print("\n=== 3. Wymiary piwnicy ziemnej (ilosci na osobe - SZACUNEK roboczy; docelowe ilosci poda agent 2) ===")
ZAPAS = [("ziemniaki", 150, 680), ("korzeniowe", 100, 600), ("kapusta", 30, 400), ("jablka", 60, 300)]
v_netto = sum(kg / ro for _, kg, ro in ZAPAS) + 150 * 0.0016     # + 150 sloikow x 1.6 dm3 obrysu
v_regal = v_netto / 0.6       # wypelnienie skrzynek/regalow 60 %
v_pom = v_regal / 0.35        # regaly zajmuja 35 % kubatury (przejscia, obieg powietrza)
print(f"  objetosc netto produktow {v_netto:.2f} m3/os. ; skrzynki i regaly {v_regal:.2f} m3/os. ; kubatura pomieszczenia {v_pom:.1f} m3/os. ; powierzchnia przy h = 2.2 m: {v_pom/2.2:.2f} m2/os.")
for n, wym in ((2, (2.0, 2.5)), (4, (2.5, 3.2)), (6, (3.0, 4.0))):
    print(f"  {n} os.: potrzeba {n*v_pom/2.2:4.1f} m2 -> komora {wym[0]} x {wym[1]} m = {wym[0]*wym[1]:.1f} m2 x 2.2 m = {wym[0]*wym[1]*2.2:.0f} m3 + przedsionek 1.2 x 1.5 m")
print("  opor cieplny przykrycia: grunt 0.8 m (lambda 1.5 W/(m K)) R = " + f"{0.8/1.5:.2f} m2K/W ; + XPS 0.10 m (lambda 0.036) R = {0.10/0.036:.2f} m2K/W")

print("\n=== 4. Zamrazarki ===")
for nazwa, V, E, t in (("skrzyniowa 287 dm3 (Kernau KFCF 2905 W)", 287, 227, None), ("skrzyniowa 497 dm3 (Liebherr CFe 2500)", 497, 295, 40)):
    print(f"  {nazwa}: {E} kWh/rok = {E/365:.2f} kWh/d = {E/8.76:.0f} W srednio ; {1000*E/V/365:.1f} Wh/(dm3 d)" + (f" ; czas utrzymania bez zasilania {t} h" if t else ""))
print(f"  podtrzymanie 2 zamrazarek przez 3 doby: {3*(227+295)/365:.1f} kWh ; ladownosc orientacyjna 0.5-0.65 kg/dm3 (SZACUNEK): 287 dm3 = 145-185 kg, 497 dm3 = 250-320 kg")

print("\n=== 5. Ziarno i pasza ===")
pasza_d = 100 * 0.1179       # kg/d: 100 kur x 117.9 g (Hy-Line Brown, srednia 18-90 tyg.)
print(f"  pasza 100 kur: {pasza_d:.1f} kg/d = {pasza_d*365:.0f} kg/rok ; zapas 14 d = {pasza_d*14:.0f} kg ; 30 d = {pasza_d*30:.0f} kg = {pasza_d*30/650:.2f} m3 (pasza sypka 650 kg/m3) ; rok = {pasza_d*365/750:.1f} m3 ziarna (750 kg/m3)")
print(f"  ziarno konsumpcyjne 200 kg/os./rok (SZACUNEK): 2/4/6 os. = 400/800/1200 kg = {400/770:.2f}/{800/770:.2f}/{1200/770:.2f} m3 ; beczka stalowa 200 dm3 miesci ok. {0.2*770:.0f} kg pszenicy")

print("\n=== 6. Suszarka solarna ===")
import json
gti = [x / d for x, d in zip(GSA_GTI_38, DNI)]
for m in (6, 7, 8, 9):
    E = 2.0 * gti[m]                 # kolektor 2 m2
    print(f"  {MIES[m]}: naslonecznienie {gti[m]:.2f} kWh/(m2 d) ; kolektor 2 m2: {E:.1f} kWh/d ; sprawnosc 25 % (SZACUNEK) -> {E*0.25/0.68:.1f} kg wody/d = ok. {E*0.25/0.68/0.80:.1f} kg jablek swiezych/d (odparowanie 0.80 kg wody z 1 kg)")

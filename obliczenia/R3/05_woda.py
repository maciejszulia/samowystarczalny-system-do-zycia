# -*- coding: utf-8 -*-
"""05 - Woda: zapotrzebowanie, pompa, zbiornik przeponowy, zapas awaryjny, deszczowka.

Wzory (jedna linia):
  V_podl = max(0, ETc - 0.7*P) / eta_naw * A                   [dm3]  ETc w mm = dm3/m2 ; 0.7 = udzial opadu efektywnego (SZACUNEK) ; eta_naw = 0.9 (kroplowe)
  h_f = lambda * (L/D) * v^2 / (2*g)                           [m]   strata liniowa (Darcy-Weisbach)
  H = H_geo + p_wyl*10.2 + h_f + h_uzd                         [m]   p w barach nadcisnienia ; 1 bar = 10.2 m sl. wody
  P_el = rho*g*Q*H / eta_calk                                  [W]
  V_u = Q / (4*n)                                              [dm3] objetosc uzyteczna zbiornika przeponowego, n = liczba zalaczen na godzine
  V_t = V_u * p_zal_abs * p_wyl_abs / (p_wst_abs * (p_wyl - p_zal))  [dm3] (prawo Boyle'a, cisnienia absolutne = nadcisnienie + 1 bar)
  Y = A_dachu * P * e * eta_f                                  [dm3] e = 0.8 dach skosny twardy, eta_f = 0.9 filtr (DIN 1989-1 / PN-EN 16941-1 - wartosci typowe, DO WERYFIKACJI w normie)
"""
import math
from dane import *

print("=== 1. Zapotrzebowanie ===")
for n in (2, 4, 6):
    print(f"  ludzie {n} os. x 110 dm3/(os. d): {n*110} dm3/d = {n*0.110*365:.0f} m3/rok  (zakres 100-120 dm3/(os. d): {n*0.100*365:.0f}-{n*0.120*365:.0f} m3/rok)")
print(f"  drob 100 kur: 17.4-24.8 dm3/d (Hy-Line, 40-100 tyg.), upal x2 (SZACUNEK) = do 50 dm3/d ; rocznie {100*0.21*365/1000:.1f} m3 + mycie 1.5 m3 = ok. 9 m3")
ETC_TYG = [0, 0, 0, 15, 20, 25, 25, 25, 15, 0, 0, 0]     # mm/tydzien - potrzeby warzyw (SZACUNEK; szczyt 25 mm/tydz. wg zalozenia zadania)
PODL = {}
for opis, k in (("rok przecietny", 1.0), ("rok suchy (opad x0.5)", 0.5)):
    suma = 0
    wiersz = []
    for m in range(12):
        etc = ETC_TYG[m] * DNI[m] / 7
        v = max(0.0, etc - 0.7 * IMGW_OPAD[m] * k) / 0.9
        suma += v
        wiersz.append(v)
    PODL[opis] = suma
    print(f"  podlewanie 1000 m2, {opis}: " + " ".join(f"{MIES[m]}:{wiersz[m]:.0f}" for m in range(3, 9)) + f" mm -> {suma:.0f} dm3/m2 = {suma:.0f} m3/sezon ; 2000 m2: {2*suma:.0f} m3")
print(f"  szczyt: 25 mm/tydz. x 1000 m2 = 25 m3/tydz. = {25/7:.1f} m3/d ; tunel 60 m2 x 30 mm/tydz. x 26 tyg. = {60*0.030*26:.0f} m3/sezon")
print("  suma potrzeb ETc IV-IX: " + f"{sum(ETC_TYG[m]*DNI[m]/7 for m in range(12)):.0f} mm ; opad IV-IX (IMGW 1991-2020): {sum(IMGW_OPAD[3:9]):.1f} mm ; opad roczny {sum(IMGW_OPAD):.1f} mm")

print("\n=== 2. Dobor pompy glebinowej (zalozenia: zwierciadlo dynamiczne 12 m ppt - DO POMIARU; rura PE32, 60 m) ===")
Q = 2.5 / 3600           # m3/s
D = 0.026                # m, srednica wewnetrzna PE32 PN16
v = Q / (math.pi * D ** 2 / 4)
hf = 0.022 * 60 / D * v ** 2 / (2 * G)
for p in (3.0, 4.0):
    Hc = 12 + p * 10.2 + hf + 8      # 8 m = straty na filtrach i odzelaziaczu (0.8 bar, SZACUNEK)
    Ph = 1000 * G * Q * Hc
    print(f"  Q = 2.5 m3/h, v = {v:.2f} m/s, h_f = {hf:.1f} m ; p = {p} bar -> H = {Hc:.0f} m ; P_hydr = {Ph:.0f} W ; P_el = {Ph/0.40:.0f} W (eta calk. 0.40) ; {Ph/0.40/1000/2.5:.2f} kWh/m3")
print("  strefy nawadniania: tasma 1.0 dm3/h co 0.2 m, rozstaw linii 0.75 m -> " + f"{1/0.75*5*1.0:.1f} dm3/(h m2) ; 1000 m2 = {1000/0.75*5/1000:.1f} m3/h -> 3 sekcje po {1000/0.75*5/1000/3:.1f} m3/h")

print("\n=== 3. Zbiornik przeponowy ===")
for n in (10, 15, 20):
    Vu = 2500 / (4 * n)
    for pz, pw in ((2.5, 4.0), (3.0, 4.5)):
        pp = pz - 0.2
        Vt = Vu * (pz + 1) * (pw + 1) / ((pp + 1) * (pw - pz))
        print(f"  n = {n}/h: V_u = {Vu:.0f} dm3 ; zal. {pz} / wyl. {pw} bar (nadcisnienie), wstepne {pp} bar -> V_t = {Vt:.0f} dm3")

print("\n=== 4. Zapas awaryjny ===")
for n in (2, 4, 6):
    for dni in (3, 7, 14):
        v = n * 20 * dni + 25 * dni        # 20 dm3/(os. d) (picie, gotowanie, minimum higieny - SZACUNEK) + 25 dm3/d drob
        print(f"  {n} os., {dni:>2} d: {v:5.0f} dm3", end=" ;")
    print()
print(f"  ssanie pompy recznej (abisynki): granica teoretyczna p_atm/(rho*g) = {101325/(1000*G):.1f} m ; praktycznie 6-7 m")

print("\n=== 5. Deszczowka ===")
P = sum(IMGW_OPAD)
jedn = P * 0.8 * 0.9
print(f"  uzysk jednostkowy: {P:.1f} mm x 0.8 x 0.9 = {jedn:.0f} dm3/(m2 rok) rzutu dachu")
for A in (100, 150, 250, 400):
    sezon = A * sum(IMGW_OPAD[3:9]) * 0.72 / 1000
    print(f"  dach {A} m2: {A*jedn/1000:.0f} m3/rok ; IV-IX {sezon:.0f} m3 ; zbiornik 6 % uzysku rocznego (regula DIN 1989-1) = {0.06*A*jedn/1000:.1f} m3")
print(f"  staw 100 m2 x srednio 1.5 m = 150 m3 ; opad na lustro {100*P/1000:.0f} m3/rok ; parowanie z wolnej powierzchni 500-600 mm/rok (SZACUNEK) = 50-60 m3/rok")
print(f"  pokrycie podlewania 1000 m2 (rok przecietny {PODL['rok przecietny']:.0f} m3) z dachu 250 m2 w sezonie IV-IX: {250*sum(IMGW_OPAD[3:9])*0.72/1000/PODL['rok przecietny']*100:.0f} %")

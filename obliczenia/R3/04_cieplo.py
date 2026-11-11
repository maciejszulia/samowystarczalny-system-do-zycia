# -*- coding: utf-8 -*-
"""04 - Cieplo: zapotrzebowanie, drewno, las, bufor, pompa ciepla, kurnik, tunel.

Wzory (jedna linia):
  Q_co = EU * A                                              [kWh/rok]
  Q_cwu,netto = n * V * rho * cp * (t_c - t_z) / 3600 * 365  [kWh/rok]  V = 40 dm3/(os. d), t_z = 10 st C -> t_c = 55 st C
  Fi_H = Q_co / (Sd * 24) * (t_i - t_e)                      [kW]  Sd = 3698 K d (20 st C), t_i = 20 st C, t_e = -22 st C (strefa IV PN-EN 12831)
  H(w) = H0 * (1 - w) - 0.68 * w                             [kWh/kg] w = wilgotnosc wzgledna (udzial wody w masie mokrej); H0 = 5.20 iglaste / 5.00 lisciaste (LWF MB12)
  E_m3 = rho_s / (1 - w) * H(w)                              [kWh/m3 drewna litego]  rho_s = sucha masa na m3 swiezej objetosci
  E_mp = E_m3 * k                                            [kWh/mp]  k = 0.65 (walki 1 m) lub 0.70 (szczapy 33 cm ukladane)
  B = (Q_co + Q_cwu,sezon) / eta_sez                         [kWh paliwa/rok]
  Q_buf = V * rho * cp * dT / 3600                           [kWh]
  S_max(klasa C) = 16.66 + 8.33 * V^0.4                      [W] strata postojowa, zbiornik 65 st C / otoczenie 20 st C (rozp. UE 812/2013, 814/2013)
  V_min = 15 * T_B * Q_N * (1 - 0.3 * Q_H / Q_min)           [dm3] PN-EN 303-5
"""
import math
from dane import *

SD = sum(d * (20 - t) for d, t in zip(DNI, IMGW_T) if t < 12)
ETA_SEZ = 0.78  # sprawnosc sezonowa kotla zgazowujacego z buforem (SZACUNEK; nominalna 90.1 % wg Atmos; zakres 0.70-0.85)

print("=== 1. Zapotrzebowanie na cieplo c.o. [kWh/rok] i obciazenie projektowe [kW] przy -22 st C ===")
print(f"Stopniodni Sd(20) = {SD:.0f} K*d (normy IMGW 1991-2020, miesiace o sredniej < 12 st C)")
print("  A[m2]   EU=60          EU=100         EU=150   [kWh/(m2 rok)]")
for A in (120, 160, 200):
    w = []
    for EU in (60, 100, 150):
        Q = A * EU
        w.append(f"{Q:6.0f} / {Q/(SD*24)*42:4.1f} kW")
    print(f"  {A:>5}   " + "   ".join(w))

print("\n=== 2. Ciepla woda uzytkowa ===")
q_os = 40 * 0.99 * CP_WODY * 45 / 3600      # kWh/(os. d) netto
print(f"  netto: {q_os:.2f} kWh/(os. d) = {q_os*365:.0f} kWh/(os. rok) przy 40 dm3/(os. d), 10 -> 55 st C")
CWU = {}
for n in (2, 4, 6):
    netto = n * q_os * 365
    brutto = netto / 0.75                    # sprawnosc magazynowania i rozprowadzenia 0.75 (SZACUNEK)
    CWU[n] = brutto
    print(f"  {n} os.: netto {netto:5.0f} kWh/rok ; brutto (straty zasobnika i rur, sprawnosc 0.75) {brutto:5.0f} kWh/rok = {brutto/365:4.1f} kWh/d ; w sezonie grzewczym (225 d) {brutto*225/365:5.0f} ; latem (140 d) {brutto*140/365:5.0f}")
print(f"  zakres dla 30-60 dm3/(os. d): {30/40*q_os*365:.0f}-{60/40*q_os*365:.0f} kWh/(os. rok) netto")

print("\n=== 3. Wartosc opalowa drewna ===")
def H(w, iglaste):
    return (5.20 if iglaste else 5.00) * (1 - w) - CIEPLO_PAR * w
print("  w [%]   iglaste  lisciaste [kWh/kg]   energia na kg suchej masy lisciaste [kWh/kg s.m.]")
for w in (0.12, 0.15, 0.20, 0.25, 0.35, 0.50):
    print(f"  {100*w:5.0f}   {H(w,True):7.2f}  {H(w,False):9.2f}             {H(w,False)/(1-w):5.2f}")
# sucha masa na m3 swiezej objetosci [kg/m3]: LWF MB12 (sosna, swierk, buk, dab, topola); brzoza i olsza - wyliczone z gestosci r12-15 (LWF W42) * 0.81; wierzba, robinia - SZACUNEK
GAT = [("sosna", 431, True, "LWF"), ("swierk", 379, True, "LWF"), ("brzoza", 526, False, "wyliczone"), ("olsza czarna", 446, False, "wyliczone"),
       ("dab", 571, False, "LWF"), ("buk", 558, False, "LWF"), ("topola", 353, False, "LWF"), ("wierzba", 353, False, "SZACUNEK = topola"), ("robinia", 620, False, "SZACUNEK")]
E_MP = {}
print("\n  gatunek        s.m./m3   kg/m3(w=20%)  kWh/m3(w=20%)  kWh/mp(k=0.65)  kWh/mp(k=0.70)  kWh/mp przy w=35% (k=0.65)   zrodlo gestosci")
for nazwa, rs, igl, zr in GAT:
    e20 = rs / 0.8 * H(0.20, igl)
    e35 = rs / 0.65 * H(0.35, igl)
    E_MP[nazwa] = e20 * 0.65
    print(f"  {nazwa:<13} {rs:>6}   {rs/0.8:10.0f}   {e20:11.0f}   {e20*0.65:12.0f}   {e20*0.70:12.0f}   {e35*0.65:14.0f}             {zr}")
print(f"  kontrola z LWF MB12: sosna 2166 kWh/Fm, 1516 kWh/Rm (w=20 %) -> wyliczone {431/0.8*H(0.2,True):.0f} / {431/0.8*H(0.2,True)*0.7:.0f}")

print("\n=== 4. Roczne zuzycie drewna [mp, walki 1 m, w = 20 %] ; eta_sez = 0.78 ; c.w.u. z kotla w sezonie (225 d), 4 osoby ===")
cwu_sezon = CWU[4] * 225 / 365
print("  A / EU      Q_uz [kWh]  paliwo [kWh]   sosna  brzoza  olsza  dab   topola  [mp]   m3 lite (sosna)")
WAR = {}
for A in (120, 160, 200):
    for EU in (60, 100, 150):
        Q = A * EU + cwu_sezon
        B = Q / ETA_SEZ
        WAR[(A, EU)] = B
        print(f"  {A}/{EU:<5} {Q:10.0f} {B:12.0f}   " + "  ".join(f"{B/E_MP[g]:5.1f}" for g in ("sosna", "brzoza", "olsza czarna", "dab", "topola")) + f"        {B/E_MP['sosna']*0.65:5.1f}")
print(f"  zakres sprawnosci: przy eta 0.70 zuzycie x{0.78/0.70:.2f}; przy eta 0.85 x{0.78/0.85:.2f}")
print(f"  drewno o w = 35 % zamiast 20 %: energia z tej samej suchej masy x{(H(0.35,False)/0.65)/(H(0.20,False)/0.8):.3f} (bez spadku sprawnosci kotla)")

print("\n=== 5. Powierzchnia lasu / plantacji dla 3 wariantow paliwa ===")
# przyrost biezacy roczny brutto [m3/ha/rok] WISL 2020-2024 (ogolem / lasy prywatne): sosna 9.14/10.00, brzoza 7.19/7.92, lisciaste 8.31/9.27 (olsza: brak osobnej danej -> 'lisciaste')
PRZYROST = {"sosna": (9.14, "sosna"), "brzoza": (7.19, "brzoza"), "olsza czarna": (8.31, "lisciaste ogolem (przyblizenie dla olszy)")}
UZYT = 0.70   # udzial przyrostu pozyskiwany trwale (SZACUNEK; srednia krajowa pozyskanie/przyrost ok. 0.71 z WISL)
for klucz in ((120, 60), (160, 100), (200, 150)):
    B = WAR[klucz]
    print(f"  dom {klucz[0]} m2, EU {klucz[1]}: paliwo {B:.0f} kWh/rok")
    for g, (p, opis) in PRZYROST.items():
        m3 = B / E_MP[g] * 0.65
        print(f"     {g:<13}: {m3:5.1f} m3/rok ; przyrost {p} m3/ha/rok x {UZYT} -> {m3/(p*UZYT):4.1f} ha   [{opis}]")
    # plantacje krotkiej rotacji: plon [t s.m./ha/rok] UWM (Stolarski i in. 2015, gleba piaszczysta slaba, rotacja 4-letnia): wierzba 8.34 (5.10-10.30), topola 8.21 (5.48-10.49), robinia 2.87 (1.63-5.40)
    for g, (sr, lo, hi) in {"wierzba": (8.34, 5.10, 10.30), "topola": (8.21, 5.48, 10.49), "robinia": (2.87, 1.63, 5.40)}.items():
        e_t = 1000 / 0.8 * H(0.20, False)   # kWh na tone suchej masy po dosuszeniu do w = 20 %
        print(f"     {g:<13} SRC: {e_t*sr/1000:5.1f} MWh/ha/rok (zakres {e_t*lo/1000:.1f}-{e_t*hi/1000:.1f}) -> {B/(e_t*sr):4.2f} ha (zakres {B/(e_t*hi):.2f}-{B/(e_t*lo):.2f})")

print("\n=== 6. Kociol Atmos DC18S: ladunki i bufor ===")
QN, TB, KG_H = 20.0, 2.0, 5.6        # kW, h, kg/h (dane producenta)
kg_lad = KG_H * TB
for g, igl in (("sosna", True), ("brzoza", False)):
    e_pal = kg_lad * H(0.20, igl)
    print(f"  ladunek {kg_lad:.1f} kg ({g}, w = 20 %): {e_pal:.0f} kWh paliwa -> {e_pal*0.901:.0f} kWh ciepla przy sprawnosci 90.1 % ; producent: 20 kW x 2 h = 40 kWh")
for klucz in ((120, 60), (160, 100), (200, 150)):
    B = WAR[klucz]
    n = B / (kg_lad * H(0.20, True))
    Qd_proj = klucz[0] * klucz[1] / (SD * 24) * 42 * 24
    Qd_sty = klucz[0] * klucz[1] / (SD * 24) * 22 * 24
    print(f"  dom {klucz[0]}/{klucz[1]}: {n:4.0f} ladunkow/rok = {n/225:.1f}/d srednio w sezonie ; doba projektowa (-22 st C): {Qd_proj:4.0f} kWh = {Qd_proj/40:.1f} ladunku ; srednia doba stycznia (-2 st C): {Qd_sty:4.0f} kWh = {Qd_sty/40:.1f} ladunku")
print("  Pojemnosc cieplna bufora Q = V*rho*cp*dT/3600 (rho = 0.980 kg/dm3, cp = 4.19 kJ/(kg K)):")
for V in (500, 1000, 1500, 2000, 3000):
    q40 = V * RHO_WODY_65 * CP_WODY * 40 / 3600
    q50 = V * RHO_WODY_65 * CP_WODY * 50 / 3600
    sC = 16.66 + 8.33 * V ** 0.4
    sB = 12 + 5.93 * V ** 0.4
    print(f"    {V:>4} dm3: 85->45 st C: {q40:5.1f} kWh ; 90->40 st C: {q50:5.1f} kWh ; strata postojowa: klasa B <= {sB:4.0f} W, klasa C <= {sC:4.0f} W = {sC*24/1000:.1f} kWh/d przy dT = 45 K ; {sC*24*225/1000:.0f} kWh/sezon")
print("  Minimalna pojemnosc wg PN-EN 303-5: V = 15*T_B*Q_N*(1 - 0.3*Q_H/Q_min):")
for QH in (4, 8, 12):
    for Qmin in (10, 20):
        print(f"    Q_H = {QH:>2} kW, Q_min = {Qmin} kW: V_min = {15*TB*QN*(1-0.3*QH/Qmin):4.0f} dm3")
print("  Kontrola wzoru klasy ErP na danych Bosch (BH 200-5 B: 203 dm3, 58.2 W): granice klasy B "
      f"{8.5+4.25*203**0.4:.1f}-{12+5.93*203**0.4:.1f} W -> zgodne")

print("\n=== 7. C.w.u. latem z nadwyzki PV (grzalka) ===")
import json
Y50 = json.load(open("wynik_pv.json"))["Y50"]["35"]
for n in (2, 4, 6):
    qd = CWU[n] / 365
    y_lato = sum(Y50[4:8]) / sum(DNI[4:8])
    print(f"  {n} os.: {qd:4.1f} kWh/d -> {qd/y_lato:.1f} kWp PV przeznaczone na c.w.u. (uzysk V-VIII {y_lato:.2f} kWh/kWp/d, P50) ; zasobnik 300 dm3 45->65 st C magazynuje {300*0.985*CP_WODY*20/3600:.1f} kWh")

print("\n=== 8. Pompa ciepla powietrze-woda zamiast kotla: bilans miesieczny z PV 10 kWp (P50, 35 st), dom 160 m2 / EU 100 ===")
# COP_m = 0.45 * (T_zas + 273.15) / (T_zas - T_zew) ; T_zas = 30 + 25*(20 - T_zew)/42 [st C] (krzywa grzewcza, grzejniki niskotemperaturowe) - SZACUNEK
Qco = 16000.0
hdd = [d * (20 - t) if t < 12 else 0 for d, t in zip(DNI, IMGW_T)]
print("  mies.  cieplo[kWh]  COP   energia el. PC [kWh]   PV 10 kWp [kWh]   bilans PV - PC [kWh]")
sE = 0
for m in range(12):
    q = Qco * hdd[m] / sum(hdd) + CWU[4] / 12
    tz = IMGW_T[m]
    tzas = max(45.0, 30 + 25 * (20 - tz) / 42) if hdd[m] == 0 else 30 + 25 * (20 - tz) / 42
    cop = 0.45 * (tzas + 273.15) / (tzas - tz)
    e = q / cop
    sE += e
    print(f"  {MIES[m]:>5} {q:10.0f}  {cop:4.2f} {e:14.0f} {10*Y50[m]:18.0f} {10*Y50[m]-e:18.0f}")
print(f"  roczne zuzycie energii el. przez PC: {sE:.0f} kWh ; SCOP = {(Qco+CWU[4])/sE:.2f}")

print("\n=== 9. Kurnik 100 kur: bilans ciepla bez ogrzewania ===")
# cieplo calkowite kury: Fi = 6.28*m^0.75 + 25*Y [W] (CIGR 2002, z pamieci - DO WERYFIKACJI) ; m = 1.9 kg, Y = 0.055 kg jaj/d ; cieplo jawne ok. 70 %
fi = 6.28 * 1.9 ** 0.75 + 25 * 0.055
jawne = 0.70 * fi * 100
A_przegrod = 2 * (4 + 6) * 2.3 + 4 * 6    # sciany + sufit, kurnik 4 x 6 x 2.3 m
for U in (0.35, 1.5):
    for went in (75, 150):                 # m3/h: 0.7-0.85 m3/h/kure przy -23 st C (Hy-Line) ; 2x wiecej
        Hc = U * A_przegrod + 0.34 * went
        print(f"  U = {U} W/(m2 K), wentylacja {went} m3/h: H = {Hc:.1f} W/K ; cieplo jawne stada {jawne:.0f} W -> przyrost temperatury {jawne/Hc:.1f} K ponad zewnetrzna")

print("\n=== 10. Tunel foliowy 6 x 10 m: moc grzewcza ===")
A_folia = math.pi * 3 * 10 + math.pi * 3 ** 2
for U, opis in ((7.0, "folia pojedyncza"), (4.0, "folia podwojna pompowana")):
    for dT in (10, 20):
        P = U * A_folia * dT / 1000
        print(f"  {opis}: U = {U} W/(m2 K), A = {A_folia:.0f} m2, dT = {dT} K -> {P:.1f} kW ; noc 12 h = {P*12:.0f} kWh = {P*12/ETA_SEZ/H(0.2,True):.0f} kg drewna")

print("\n=== 11. Las wlasny: trwaly pozysk z 1 ha i powierzchnia potrzebna (wariant glowny: 4 osoby) ===")
# pozysk [m3/ha/rok] = przyrost biezacy brutto * u ; pozysk [mp/ha/rok] = pozysk [m3/ha/rok] / 0.65 ; energia paliwa [kWh/ha/rok] = pozysk [mp/ha/rok] * E_mp
# przyrost wg WISL 2020-2024: wszystkie lasy / lasy prywatne
LAS = {"sosna": (9.14, 10.00, "sosna"), "brzoza": (7.19, 7.92, "brzoza"), "olsza czarna": (8.31, 9.27, "olsza czarna")}
print("  gatunek        przyrost  u     m3/ha/rok  mp/ha/rok  kWh paliwa/ha/rok  kWh ciepla/ha/rok (eta 0.78)")
POZYSK = {}
for g, (p_all, p_pryw, klucz) in LAS.items():
    for p, opis in ((p_all, "wszystkie"), (p_pryw, "prywatne")):
        for u in (0.5, 0.7, 0.9):
            m3 = p * u
            mp = m3 / 0.65
            e = mp * E_MP[klucz]
            if opis == "wszystkie" and u == 0.7:
                POZYSK[g] = (m3, mp, e)
            print(f"  {g:<13} {p:5.2f} ({opis:<9}) {u:3.1f} {m3:9.2f} {mp:10.2f} {e:14.0f} {e*ETA_SEZ:18.0f}")
print("\n  Powierzchnia lasu [ha] dla trwalego pokrycia ciepla domu (c.o. + c.w.u. 4 osob w sezonie; u = 0.7; przyrost 'wszystkie lasy'):")
print("  A / EU    paliwo [kWh]   sosna   brzoza   olsza(lisciaste)")
for A in (120, 160, 200):
    for EU in (60, 100, 150):
        B = WAR[(A, EU)]
        print(f"  {A}/{EU:<5} {B:10.0f}   " + "   ".join(f"{B/POZYSK[g][2]:5.2f}" for g in LAS))
print("\n  Podaz z wlasnego lasu 2 ha i 3 ha (u = 0.7):")
for ha in (2.0, 2.5, 3.0):
    print(f"  {ha} ha: " + " ; ".join(f"{g}: {ha*POZYSK[g][1]:.1f} mp/rok = {ha*POZYSK[g][2]:.0f} kWh paliwa = {ha*POZYSK[g][2]*ETA_SEZ:.0f} kWh ciepla" for g in LAS))
print("\n  Najwiekszy wskaznik EU [kWh/(m2 rok)] domu, ktory pokrywa las (4 osoby, c.w.u. w sezonie 2489 kWh):")
for ha in (2.0, 3.0):
    for g in LAS:
        cieplo = ha * POZYSK[g][2] * ETA_SEZ - cwu_sezon
        print(f"  {ha} ha, {g:<13}: 120 m2 -> EU {cieplo/120:5.0f} ; 160 m2 -> EU {cieplo/160:5.0f} ; 200 m2 -> EU {cieplo/200:5.0f}")
print("\n  Wariant 2 i 6 osob (dom 160 m2, EU 100): paliwo i las sosnowy")
for n in (2, 4, 6):
    B = (16000 + CWU[n] * 225 / 365) / ETA_SEZ
    print(f"  {n} os.: paliwo {B:.0f} kWh/rok = {B/E_MP['sosna']:.1f} mp sosny = {B/POZYSK['sosna'][2]:.2f} ha")

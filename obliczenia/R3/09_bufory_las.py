# -*- coding: utf-8 -*-
"""09 - Bufory istniejace (1 x 1000 dm3 + 2 x 500 dm3 = 2000 dm3), naczynie przeponowe, czas pokrycia, las 1.82 ha.

Wzory (jedna linia):
  e = rho(20 st C)/rho(90 st C) - 1                                [-]    przyrost objetosci wody 20 -> 90 st C
  V_e = e * V_inst                                                 [dm3]  objetosc rozszerzenia
  V_n = (V_e + V_wr) * (p_e + 1) / (p_e - p_0)                     [dm3]  naczynie przeponowe (PN-EN 12828) ; p_e, p_0 jako nadcisnienie [bar]
  p_gaz * V_gaz = const                                            (Boyle, cisnienia absolutne) - kontrola
  Q = V * rho * cp * dT / 3600                                     [kWh]
  Fi(t_e) = Fi_H * (20 - t_e) / 42                                 [kW]   obciazenie przy temperaturze zewnetrznej t_e
  dT_m' = dT_m * q^(1/n) ; t_pow = 20 + dT_m' - 5*q                [st C] grzejniki 75/65/20 st C przy -22 st C, n = 1.3, q = Fi/Fi_H (SZACUNEK)
  t = Q / (Fi + P_cwu + P_str)                                     [h]
  D = I * u / k * E_mp                                             [kWh/ha/rok] ; I = przyrost [m3/ha/rok], u = 0.7, k = 0.65 m3/mp
"""
import math

CP = 4.19
RHO = {20: 998.2, 40: 992.2, 60: 983.2, 62.5: 981.9, 85: 968.6, 90: 965.3}   # kg/m3, tablice wlasnosci wody (IAPWS-IF97)

print("=== 1. Naczynie przeponowe dla 2000 dm3 buforow, woda 20 -> 90 st C ===")
e = RHO[20] / RHO[90] - 1
print(f"  e = {RHO[20]}/{RHO[90]} - 1 = {100*e:.2f} %")
for V_inst, opis in ((2000, "same bufory"), (2000 + 45 + 150, "bufory + kociol 45 dm3 + instalacja 150 dm3 (SZACUNEK)")):
    Ve = e * V_inst
    Vwr = max(3.0, 0.005 * V_inst)
    for p0, pe in ((1.0, 2.0), (0.8, 2.0), (1.0, 1.8)):
        Vn = (Ve + Vwr) * (pe + 1) / (pe - p0)
        print(f"  {opis}: V_inst = {V_inst} dm3 ; V_e = {Ve:.1f} dm3 ; V_wr = {Vwr:.1f} dm3 ; p_0 = {p0} bar (abs. {p0+1:.1f}) ; p_e = {pe} bar (abs. {pe+1:.1f}) -> V_n = {Vn:.0f} dm3")
# kontrola Boyle'a dla naczynia 300 dm3, p0 = 1.0 bar nadcisnienia
Vn, p0a = 300.0, 2.0
Ve = e * 2195
Vwr = 0.005 * 2195
p_zimne = Vn * p0a / (Vn - Vwr)
p_gorace = Vn * p0a / (Vn - Vwr - Ve)
print(f"  kontrola (naczynie 300 dm3, cisnienie wstepne 1.0 bar nadc. = 2.0 bar abs.): instalacja zimna 20 st C: {p_zimne-1:.2f} bar nadc. ({p_zimne:.2f} abs.) ; goraca 90 st C: {p_gorace-1:.2f} bar nadc. ({p_gorace:.2f} abs.) ; zawor bezpieczenstwa 2.5 bar nadc. (3.5 abs.)")
Vn = 250.0
print(f"  kontrola (naczynie 250 dm3): goraca {Vn*p0a/(Vn-Vwr-Ve)-1:.2f} bar nadc. -> zapas do zaworu bezpieczenstwa {2.5-(Vn*p0a/(Vn-Vwr-Ve)-1):.2f} bar")

print("\n=== 2. Pojemnosc cieplna 2000 dm3 ===")
def Q(V, dT, rho=RHO[62.5] / 1000):
    return V * rho * CP * dT / 3600
print(f"  40 -> 85 st C (dT = 45 K): {Q(2000,45):.1f} kWh ; 1000 dm3: {Q(1000,45):.1f} ; 500 dm3: {Q(500,45):.1f} kWh")
print(f"  45 -> 85 st C: {Q(2000,40):.1f} kWh ; 40 -> 90 st C: {Q(2000,50):.1f} kWh")
print(f"  rownowaznik: {Q(2000,45)/41:.1f} ladunku kotla DC18S (41 kWh) ; czas ladowania przy 20 kW bez odbioru: {Q(2000,45)/20:.1f} h")
print(f"  przeplyw ladowania: 20 kW / (1.163 kWh/(m3 K) x 20 K) = {20/(1.163*20):.2f} m3/h ; predkosc w rurze 35x1.5 mm: {20/(1.163*20)/3600/(math.pi*0.032**2/4):.2f} m/s")
S = lambda V: 16.66 + 8.33 * V ** 0.4
print(f"  strata postojowa (granica klasy C, dT 45 K): 1000 dm3 {S(1000):.0f} W + 2 x 500 dm3 {S(500):.0f} W = {S(1000)+2*S(500):.0f} W = {(S(1000)+2*S(500))*24/1000:.1f} kWh/d ; jeden zbiornik 2000 dm3: {S(2000):.0f} W")

print("\n=== 3. Czas pokrycia zapotrzebowania domu z naladowanego bufora 2000 dm3 (4 osoby: c.w.u. 11.1 kWh/d = 0.46 kW) ===")
SD = 3698.0
P_CWU = 11.06 / 24
P_STR = (S(1000) + 2 * S(500)) / 1000 * 0.5    # polowa straty jako strata nieodzyskana (SZACUNEK)
print("  A/EU       Fi_H   | t_e = -5 st C: Fi, t_pow, Q(grzejniki), czas ; czas przy dT 45 K | t_e = -20 st C: Fi, t_pow, Q(grzejniki), czas ; czas przy dT 45 K")
for A in (120, 160, 200):
    for EU in (60, 100, 150):
        FiH = A * EU / (SD * 24) * 42
        w = []
        for te in (-5, -20):
            q = (20 - te) / 42
            Fi = FiH * q
            dTm = 50 * q ** (1 / 1.3)
            t_pow = 20 + dTm - 5 * q
            Qg = Q(2000, 85 - t_pow)
            w.append(f"{Fi:4.1f} kW, {t_pow:4.1f} st C, {Qg:5.1f} kWh, {Qg/(Fi+P_CWU+P_STR):5.1f} h ; {Q(2000,45)/(Fi+P_CWU+P_STR):5.1f} h")
        print(f"  {A}/{EU:<4} {FiH:5.1f} kW | " + " | ".join(w))
print(f"  (strata nieodzyskana przyjeta {P_STR*1000:.0f} W)")

print("\n=== 4. Las wlasny 1.35 ha: trwaly pozysk i standard energetyczny domu (4 osoby) ===")
H = lambda w, igl: (5.20 if igl else 5.00) * (1 - w) - 0.68 * w
E_M3 = {"sosna": 431 / 0.8 * H(0.2, True), "brzoza": 526 / 0.8 * H(0.2, False), "olsza": 446 / 0.8 * H(0.2, False)}
UDZ = {"sosna": 0.3, "brzoza": 0.3, "olsza": 0.4}     # sklad drzewostanu mieszanego (SZACUNEK: mokre dno z olsza ; DO USTALENIA: opis taksacyjny dzialki 16/3)
e_m3 = sum(UDZ[g] * E_M3[g] for g in UDZ)
e_mp = e_m3 * 0.65
print(f"  drzewostan mieszany (30 % sosna, 30 % brzoza, 40 % olsza): {e_m3:.0f} kWh/m3 ; {e_mp:.0f} kWh/mp (w = 20 %, k = 0.65)")
ETA = 0.78
CWU_SEZON, CWU_LATO, CWU_ROK = 2489.0, 1549.0, 4037.0
LAS = 1.35   # powierzchnia drzewostanu wg koordynatora (dzialka lesna 16/3 ma 1.82 ha ewidencyjnie)
WAR = [("ostrozny", 6.0), ("sredni (lisciaste, WISL)", 8.31), ("dobry (lasy prywatne, WISL)", 9.94)]
print("  wariant przyrostu            I[m3/ha/rok]  pozysk[m3/rok]  [mp/rok]  [mp/ha/rok]  paliwo[kWh/rok]  cieplo[kWh/rok]")
POD = {}
for nazwa, I in WAR:
    m3 = I * 0.7 * LAS
    mp = m3 / 0.65
    pal = mp * e_mp
    POD[nazwa] = pal * ETA
    print(f"  {nazwa:<28} {I:8.2f} {m3:14.1f} {mp:10.1f} {mp/LAS:11.1f} {pal:15.0f} {pal*ETA:15.0f}")
print("\n  Najwiekszy wskaznik EU [kWh/(m2 rok)], przy ktorym las 1.35 ha pokrywa 100 % ciepla:")
print("  wariant                       c.w.u. latem z PV (drewno: c.o. + c.w.u. w sezonie)      c.w.u. caly rok z drewna")
for nazwa, _ in WAR:
    a = [(POD[nazwa] - CWU_SEZON) / A for A in (120, 160, 200)]
    b = [(POD[nazwa] - CWU_ROK) / A for A in (120, 160, 200)]
    print(f"  {nazwa:<28} 120 m2: {a[0]:4.0f} ; 160 m2: {a[1]:4.0f} ; 200 m2: {a[2]:4.0f}        120 m2: {b[0]:4.0f} ; 160 m2: {b[1]:4.0f} ; 200 m2: {b[2]:4.0f}")
print("\n  Bilans dla domu 160 m2 (4 osoby, c.w.u. latem z PV): potrzeba vs podaz lasu 1.35 ha [mp/rok drzewostanu mieszanego]")
for EU in (60, 80, 100, 120, 150):
    cieplo = 160 * EU + CWU_SEZON
    mp_potrz = cieplo / ETA / e_mp
    w = []
    for nazwa, I in WAR:
        mp_las = I * 0.7 * LAS / 0.65
        w.append(f"{nazwa.split(' ')[0]}: {mp_las-mp_potrz:+5.1f}")
    print(f"  EU {EU:>3}: cieplo {cieplo:6.0f} kWh ; drewno {mp_potrz:5.1f} mp/rok ; saldo -> " + " ; ".join(w) + " mp/rok")
print("\n  Srodki zmniejszenia zapotrzebowania (dom 160 m2):")
print(f"  - docieplenie z EU 150 do EU 100: {160*50/ETA/e_mp:.1f} mp/rok ; z EU 100 do EU 60: {160*40/ETA/e_mp:.1f} mp/rok")
print(f"  - c.w.u. latem z grzalki PV zamiast z kotla (1549 kWh ciepla ; sprawnosc kotla latem 0.5 - SZACUNEK): {CWU_LATO/0.5/e_mp:.1f} mp/rok")
print(f"  - grzalki w buforze z nadwyzki PV w III, IV, X (2034 kWh, skrypt 08): {2034*0.95/ETA/e_mp:.1f} mp/rok")
print(f"  - sprawnosc sezonowa 0.85 zamiast 0.78 (suche drewno, bufor, czysty wymiennik), dom 160/100: {(18489/0.78-18489/0.85)/e_mp:.1f} mp/rok")

print("\n=== 5. Odleglosc punktu danych slonecznych od srodka gospodarstwa ===")
dlat = (53.7875 - 53.7625) * 111.2
dlon = (20.4667 - 20.4020) * 111.32 * math.cos(math.radians(53.775))
print(f"  dN = {dlat:.2f} km ; dE = {dlon:.2f} km ; odleglosc {math.hypot(dlat, dlon):.1f} km")

print("\n=== 6. Wariant porownawczy: caly las ewidencyjny 1.82 ha ===")
for nazwa, I in WAR:
    mp = I * 0.7 * 1.82 / 0.65
    print(f"  {nazwa:<28}: {mp:5.1f} mp/rok ; cieplo {mp*e_mp*ETA:6.0f} kWh/rok ; EU max dla 160 m2: {(mp*e_mp*ETA-CWU_SEZON)/160:4.0f}")
print("\n=== 7. Zbiornik wody na szczycie pagorka: nadcisnienie hydrostatyczne p = rho*g*h ===")
for h in (6, 8, 10, 11):
    print(f"  roznica wysokosci {h} m -> {1000*9.81*h/1e5:.2f} bar nadcisnienia")

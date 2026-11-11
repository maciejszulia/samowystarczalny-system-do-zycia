# -*- coding: utf-8 -*-
"""07 - Kurnik 100 szt. (wymiary wg norm), naklady pracy po automatyzacji, kosztorys orientacyjny [PLN brutto, 2026].

Normy: rozp. MRiRW z 15.02.2010 (Dz.U. nr 56 poz. 344) par. 29 - chow bezklatkowy (obowiazuje gospodarstwa >= 350 kur; tu jako wzorzec projektowy);
       rozp. wykonawcze Komisji (UE) 2020/464, zal. I cz. IV - chow ekologiczny.
Kosztorys: [Z] = cena ze zrodla (podane w raporcie), [S] = SZACUNEK wlasny (rzad wielkosci, do weryfikacji ofertami).
"""
N = 100
print("=== 1. Kurnik i wybieg dla 100 kur ===")
print(f"{'parametr':<46}{'konwencjonalnie':>18}{'ekologicznie':>16}")
wiersze = [
    ("powierzchnia uzytkowa kurnika [m2]", N / 9, N / 6, "9 szt./m2", "6 szt./m2"),
    ("grzedy [m]", N * 0.15, N * 0.18, "15 cm/szt.", "18 cm/szt."),
    ("gniazda pojedyncze [szt.]", N / 7, N / 7, "1 na 7 kur", "1 na 7 kur"),
    ("gniazdo grupowe [m2]", N / 120, N * 120 / 10000, "120 kur/m2", "120 cm2/szt."),
    ("sciolka min. [m2]", max(N * 0.025, N / 9 / 3), N / 6 / 3, "250 cm2/szt. i 1/3 podlogi", "1/3 podlogi (2018/848)"),
    ("karmidla liniowe [m] / okragle [m obwodu]", N * 0.10, N * 0.04, "10 cm lub 4 cm/szt.", "(jak konw.)"),
    ("poidla smoczkowe [szt.]", N / 10, N / 10, "1 na 10 kur", "1 na 10 kur"),
    ("wybieg [m2]", N * 4, N * 4, "4 m2/szt. (wolny wybieg)", "4 m2/szt."),
    ("otwory wyjsciowe - laczna szerokosc [m]", 2.0 * N / 1000, 4.0 * (N / 6) / 100, "2 m/1000 kur; min 0.35 x 0.40 m", "4 m/100 m2 kurnika"),
]
for nazwa, k, e, ok, oe in wiersze:
    print(f"{nazwa:<46}{k:>8.1f} ({ok}){'':>2}{e:>8.1f} ({oe})")
print("Propozycja: kurnik 4 x 6 m = 24 m2 (16.7 m2 czesc dla kur + 7 m2 sluza/magazyn paszy), woliera zadaszona 30-40 m2 (na okres nakazu zamkniecia drobiu), wybieg 400-800 m2 w 4 kwaterach.")
print(f"Wentylacja (Hy-Line): min {0.70*N:.0f}-{0.85*N:.0f} m3/h przy -23 st C ; {1.02*N:.0f}-{1.70*N:.0f} m3/h przy 0 st C ; {9.34*N:.0f}-{12.0*N:.0f} m3/h przy 32 st C")
print(f"Pasza: {N*0.1179:.1f} kg/d ; woda: {N*0.174:.0f}-{N*0.248:.0f} dm3/d ; zapas wody 14 d = {N*0.248*14:.0f} dm3 ; zapas paszy 30 d = {N*0.1179*30:.0f} kg")

print("\n=== 2. Naklady pracy po automatyzacji [h/rok] - SZACUNEK (zakres) ===")
# (czynnosc, min, max, udzial w sezonie V-X [0..1])
PRACA = [
    ("Warzywnik 1000-2000 m2 (siew, sadzenie, pielenie, zbior, przygotowanie gleby)", 300, 700, 0.85),
    ("Pole co najwyzej 0.9 ha na dzialce 16/1 (zboza, ziemniaki, straczkowe; uslugi maszynowe)", 30, 100, 0.80),
    ("Kury 100 szt.: codzienna kontrola i zbior jaj 10-15 min/d", 61, 91, 0.50),
    ("Kury: prace tygodniowe (pasza, poidla, sciolka), wymiana sciolki 2x/rok", 60, 100, 0.50),
    ("Uboj i obrobka drobiu 50-100 szt./rok (15-20 min/szt.)", 13, 33, 0.70),
    ("Kozy lub owce mleczne 2-4 szt.: dojenie 2x/d, karmienie, sciolka, racice", 250, 500, 0.60),
    ("Przerob mleka (sery, twarog)", 80, 200, 0.65),
    ("Pszczoly 3-5 uli (15-20 h/ul)", 45, 100, 0.85),
    ("Drewno: sciecie, zrywka, ciecie, lupanie, ukladanie 9-16 mp (2.5-5 h/mp)", 30, 80, 0.30),
    ("Kociol: zaladunek, czyszczenie, popiol (2-3 ladunki/d x 5 min x 225 d + serwis)", 45, 70, 0.10),
    ("Przetworstwo i przechowywanie (wekowanie, kiszenie, suszenie, mrozenie, wedzenie)", 120, 250, 0.80),
    ("Kontrola piwnicy i zapasow, przebieranie", 15, 40, 0.20),
    ("Utrzymanie instalacji (PV, magazyn, agregat, woda, HA, ogrodzenia, robot)", 50, 90, 0.50),
]
smin = smax = sez_min = sez_max = 0
for nazwa, a, b, u in PRACA:
    smin += a; smax += b; sez_min += a * u; sez_max += b * u
    print(f"  {nazwa:<82}{a:>5}-{b:<5}")
print(f"  SUMA: {smin}-{smax} h/rok = {smin/52:.0f}-{smax/52:.0f} h/tydz. srednio")
print(f"  sezon V-X (26 tyg.): {sez_min/26:.0f}-{sez_max/26:.0f} h/tydz. ; zima XI-IV (26 tyg.): {(smin-sez_min)/26:.0f}-{(smax-sez_max)/26:.0f} h/tydz.")

print("\n=== 3. Kosztorys orientacyjny [PLN brutto, 2026] ===")
# (etap, pozycja, min, max, znacznik)
K = [
    (0, "Badanie wody (fiz.-chem. + mikrobiologia), pomiary zuzycia energii, anemometr", 800, 2500, "S"),
    (0, "Projekt PV i magazynu + uzgodnienie ppoz. (PV > 6.5 kW) + zawiadomienie PSP", 500, 2000, "S"),
    (1, "Pompa glebinowa z lagodnym rozruchem 0.75-1.1 kW, sterownik, zbiornik przeponowy, armatura (studnia istnieje)", 3500, 7000, "S"),
    (1, "Uzdatnianie: filtr, odzelaziacz/odmanganiacz automatyczny, lampa UV", 4000, 9000, "S"),
    (1, "Zbiornik gorny 3-5 m3 zakopany na pagorku + rura PE (zapas grawitacyjny)", 4000, 10000, "S"),
    (1, "Deszczowka: zbiornik 5-10 m3 z filtrem i pompa (lub 4 x IBC 1000 dm3)", 1200, 15000, "S"),
    (2, "Wlaczenie istniejacych buforow 2000 dm3: zawor ladujacy 78 st C, rury, izolacja, naczynie 300 dm3, czujniki, montaz", 6000, 14000, "S"),
    (2, "Zasobnik c.w.u. 300 dm3 z 2 wezownicami [Z: ok. 3199 PLN] + grzalka 2-3 kW + sterownik nadwyzki PV + grzalki bufora", 5000, 8500, "Z/S"),
    (2, "Wiata na drewno 20-30 mp (zapas 2-letni), luparka hydrauliczna, pilarka", 6000, 15000, "S"),
    (3, "PV 15 kWp na konstrukcji gruntowej 65 st (3000-5500 PLN/kWp)", 45000, 82500, "S"),
    (3, "Magazyn LiFePO4 30 kWh (1000-1900 PLN/kWh) [Z: 20 kWh = ok. 20 tys. budzetowo, 23 kWh > 43 tys. premium]", 30000, 57000, "Z/S"),
    (3, "Falownik wyspowy 8-10 kW z ladowarka i wejsciem agregatu", 5500, 9000, "S"),
    (3, "Agregat 3-5 kVA LPG z rozruchem elektrycznym, rozdzielnica, okablowanie, uziemienie, ograniczniki przepiec", 9000, 28000, "S"),
    (4, "Piwnica ziemna 8-12 m2 wbudowana w stok pagorka (zelbet/murowana, hydroizolacja, XPS, drenaz, wentylacja, 2 x drzwi)", 15000, 45000, "S"),
    (4, "Regaly, skrzynki, czujniki T/RH, przepustnice z silownikami", 1500, 4000, "S"),
    (4, "Zamrazarki skrzyniowe 287 + 497 dm3 [Z: 497 dm3 = 3199 PLN]", 4500, 5500, "Z/S"),
    (4, "Spizarnia sucha: beczki stalowe 200 dm3, pojemniki, silos zbozowy 3-6 t", 2000, 12000, "S"),
    (4, "Suszarka solarna, wedzarnia", 1500, 6000, "S"),
    (5, "Kurnik 24 m2 ocieplony (materialy + czesc robocizny)", 15000, 40000, "S"),
    (5, "Woliera zadaszona 30-40 m2, ogrodzenie wybiegu 400-800 m2, fartuch, siatka gorna, elektryzator", 7000, 17000, "S"),
    (5, "Wyposazenie kurnika: klapa, karmidla/silos z paszociagiem, linia smoczkowa z ogrzewaniem, gniazda wykotowe, grzedy, LED", 5600, 28500, "S"),
    (5, "Kozy lub owce 2-4 szt.: wiata 12-15 m2, poidla z ochrona przed mrozem, pasnik, siatka, dojarka konwiowa", 8000, 25000, "S"),
    (5, "Pasieka 3-5 uli z waga ula i czujnikami", 3000, 8000, "S"),
    (5, "Monitoring: 2 kamery PoE, waga paszy, czujniki T/RH/CO2/NH3, przeplywomierz", 1200, 3500, "S"),
    (6, "Nawadnianie kroplowe 1000-2000 m2: tasmy, filtry, reduktory, 4-8 elektrozaworow, sterowanie", 3000, 8000, "S"),
    (6, "Czujniki wilgotnosci gleby/tensjometry, stacja pogody", 1500, 5000, "S"),
    (6, "Tunel foliowy 6 x 10 m z automatycznym wietrzeniem", 6000, 15000, "S"),
    (6, "Robot koszacy bezprzewodowy (opcja)", 6000, 14000, "S"),
    (6, "Serwer Home Assistant, siec PoE/Wi-Fi zewn., zasilanie buforowe DC, wezly ESP32, LoRa", 2500, 6000, "S"),
]
NAZWY = {0: "Etap 0 - pomiary i projekt", 1: "Etap 1 - woda", 2: "Etap 2 - cieplo", 3: "Etap 3 - energia elektryczna off-grid (wariant c, 4 osoby)",
         4: "Etap 4 - magazyn zywnosci", 5: "Etap 5 - zwierzeta: kurnik 100 szt., kozy/owce, pasieka", 6: "Etap 6 - uprawy i automatyka"}
tmin = tmax = 0
for e in sorted(NAZWY):
    a = sum(k[2] for k in K if k[0] == e)
    b = sum(k[3] for k in K if k[0] == e)
    tmin += a; tmax += b
    print(f"{NAZWY[e]:<44}{a:>9,} - {b:>9,} PLN".replace(",", " "))
    for k in K:
        if k[0] == e:
            print(f"     [{k[4]:>3}] {k[1]:<112}{k[2]:>7} - {k[3]:>7}")
print(f"{'RAZEM':<44}{tmin:>9,} - {tmax:>9,} PLN".replace(",", " "))
assert tmin == sum(k[2] for k in K) and tmax == sum(k[3] for k in K)

print("\n=== 4. Koszt wariantow zasilania (model jednostkowy: PV 3000-5500 PLN/kWp ; magazyn 1000-1900 PLN/kWh ; falownik hybrydowy 5500-9000 PLN) ===")
def koszt(kwp, kwh, extra_min=0, extra_max=0):
    return kwp * 3000 + kwh * 1000 + 5500 + extra_min, kwp * 5500 + kwh * 1900 + 9000 + extra_max
for nazwa, kwp, kwh, emin, emax in (("(a) S: 3 kWp + 5 kWh", 3, 5, 2000, 5000), ("(a) M: 5 kWp + 10 kWh", 5, 10, 2000, 5000), ("(a) L: 8 kWp + 10 kWh", 8, 10, 2000, 5000),
                                     ("(b) S: 6 kWp + 10 kWh", 6, 10, 2000, 5000), ("(b) M: 10 kWp + 20 kWh", 10, 20, 2000, 5000), ("(b) L: 16 kWp + 30 kWh", 16, 30, 2000, 5000),
                                     ("(c) S: 10 kWp + 20 kWh + agregat", 10, 20, 9000, 28000), ("(c) M: 15 kWp + 30 kWh + agregat", 15, 30, 9000, 28000), ("(c) L: 25 kWp + 40 kWh + agregat", 25, 40, 12000, 35000)):
    a, b = koszt(kwp, kwh, emin, emax)
    print(f"  {nazwa:<36}{a:>8,} - {b:>8,} PLN".replace(",", " "))
print("  dodatki: (a),(b) 2-5 tys. PLN (rozdzielnica rezerwowana, przelacznik) ; (c) 9-35 tys. PLN (agregat 3-13 tys., drugi falownik/ladowarka, konstrukcja gruntowa 65 st, okablowanie)")

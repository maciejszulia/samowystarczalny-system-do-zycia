# -*- coding: utf-8 -*-
"""F. Plan dla 4 osob na dostepnym gruncie (gleba lekka V-VI): priorytety, drob, kozy, pszczoly, praca, azot, przechowywanie."""
import math
from dane import *
from b_plony_powierzchnia import powierzchnia, brutto, KOLEJ
import c_drob as C

N_OS = 4
# Grunt otwarty poza kempingiem [ha] (dane koordynatora: ewidencja, ortofotomapa, model terenu)
GRUNT = {"16/1 ugór (wierzchowina i stoki)": 0.60, "16/1 ogród": 0.15, "24/1 część północna (ugór, stok S–SE)": 0.33, "16/3 łąka koszona": 0.44}
POLA_M2 = (0.60 + 0.15) * 10000      # pola i ogrod: uprawy jednoroczne
SAD_M2 = 0.33 * 10000                # stok 12 %: sad, jagodnik, orzechy, wybiegi, pasieka
LAKA_M2 = 0.44 * 10000               # laka: siano i pastwisko

# --- receptura paszy dla gleb lekkich ----------------------------------------
RECEPTURA_L = [("pszenżyto", 0.30, "pszenzyto", "pszenzyto"), ("owies", 0.25, "owies", "owies"), ("żyto", 0.10, "zyto", "zyto"),
               ("proso albo gryka", 0.05, "proso", "proso"), ("łubin słodki", 0.15, "lubin", "lubin"), ("groch, peluszka", 0.05, "groch", "groch"),
               ("makuch lniankowy (własny)", 0.10, None, None)]
def ha_na_tone_L(idx, z_makuchem=True):
    ha = 0.0
    for n, u, kp, kf in RECEPTURA_L:
        if kp is None:
            if not z_makuchem: ha += u / PLONY_L["lubin"][idx]
            continue
        ha += u / PLONY_L[kp][idx]
    return ha * (1 + C.ZAPAS_PASZA)
def bialko_L():
    return sum(u * (C.BIALKO_MAKUCH if kf is None else FAO[kf][1]) for n, u, kp, kf in RECEPTURA_L)

def sekcja(t): print(f"\n## {t}\n")

if __name__ == "__main__":
    # ---------- 1. zapotrzebowanie powierzchni: zywnosc roslinna 4 osoby ----------
    sekcja("F1. Żywność roślinna dla 4 osób (wariant L): potrzebna powierzchnia brutto [m²]")
    go = powierzchnia(2, 0)[1]; gd = powierzchnia(2, 1)[1]
    mn = {"warzywnik": 1.25, "tunel foliowy": 1.20, "okopowe": 1.10, "strączkowe": 1.10, "zboża": 1.10, "oleiste": 1.10, "sad i jagodnik": 1.0}
    kcal_gr = {}
    for n, gr, kg, pr, z, zz, pl, m2, kcal in powierzchnia(2, 0)[0]:
        kcal_gr[gr] = kcal_gr.get(gr, 0) + kcal * N_OS
    print("| Priorytet | Grupa | Plon ostrożny [m²] | Plon dobry [m²] | Energia w diecie 4 osób [kcal/dobę] | Narastająco, plon ostrożny [m²] | Narastająco, plon dobry [m²] |")
    print("|---|---|---|---|---|---|---|")
    pri = ["warzywnik", "tunel foliowy", "okopowe", "strączkowe", "zboża", "oleiste"]
    co = cd = 0.0; pot = {}
    for i, gr in enumerate(pri, 1):
        a = N_OS * go[gr] * mn[gr]; b = N_OS * gd[gr] * mn[gr]; co += a; cd += b; pot[gr] = (a, b)
        print(f"| {i} | {gr} | {a:.0f} | {b:.0f} | {kcal_gr[gr]/365:.0f} | {co:.0f} | {cd:.0f} |")
    a = N_OS * go["sad i jagodnik"]; b = N_OS * gd["sad i jagodnik"]
    print(f"| osobno | sad i jagodnik (działka 24/1, część północna) | {a:.0f} | {b:.0f} | {kcal_gr['sad i jagodnik']/365:.0f} | – | – |")
    print(f"\nPola i ogród (16/1): {POLA_M2:.0f} m². Potrzeba na uprawy jednoroczne: {co:.0f} m² (plon ostrożny), {cd:.0f} m² (plon dobry).")
    print(f"Pokrycie powierzchni przy plonie ostrożnym: {100*POLA_M2/co:.0f} %. Nadwyżka przy plonie dobrym: {POLA_M2-cd:.0f} m².")

    # ---------- 2. przydzial 7500 m2 wg priorytetu, plon ostrozny ----------
    sekcja("F2. Przydział 7500 m² pól i ogrodu wg priorytetu")
    for idx, nz in ((0, "ostrożny"), (1, "dobry")):
        reszta = POLA_M2; print(f"**Plon {nz}:**\n")
        print("| Grupa | Potrzeba [m²] | Przydział [m²] | Pokrycie potrzeby |")
        print("|---|---|---|---|")
        kcal_pokr = 0.0; kcal_all = 0.0
        for gr in pri:
            potrz = pot[gr][idx]; przydz = min(potrz, reszta); reszta -= przydz
            kcal_all += kcal_gr[gr]; kcal_pokr += kcal_gr[gr] * przydz / potrz
            print(f"| {gr} | {potrz:.0f} | {przydz:.0f} | {100*przydz/potrz:.0f} % |")
        print(f"| **Zostaje** | | **{reszta:.0f}** | |")
        dieta_kcal = N_OS * 3037
        zwierz = N_OS * (66 + 74 + 40 + 37 + 473 + 65)   # jaja, kurczak, kaczka, ges, mleko, miod [kcal/dobe/os.] z a_dieta
        sad = kcal_gr["sad i jagodnik"] / 365
        print(f"\nEnergia z upraw jednorocznych: {kcal_pokr/365:.0f} z {kcal_all/365:.0f} kcal/dobę ({100*kcal_pokr/kcal_all:.0f} %). "
              f"Z sadem ({sad:.0f}) i produktami zwierzęcymi ({zwierz}) gospodarstwo pokrywa {100*(kcal_pokr/365+sad+zwierz)/dieta_kcal:.0f} % energii diety 4 osób ({dieta_kcal} kcal/dobę).\n")
        if idx == 0:
            brak_zb = pot["zboża"][0] - min(pot["zboża"][0], POLA_M2 - sum(pot[g][0] for g in pri[:4]))
            udz = brak_zb / pot["zboża"][0]
            zboza_kg = N_OS * (10/0.95 + 58/0.95 + 28/0.95 + 8/0.65 + 8/0.70)
            print(f"Przy plonie ostrożnym brakuje {brak_zb:.0f} m² zbóż ({100*udz:.0f} % potrzeby): zakup {zboza_kg*udz:.0f} kg ziarna na rok oraz {N_OS*10} kg oleju i {N_OS*(2+4+3+2)} kg nasion oleistych.\n")

    # ---------- 3. drob ----------
    sekcja("F3. Drób dla 4 osób (wariant L: 300 jaj, 22 kg kurczaka, 5 kg kaczki, 4,5 kg gęsi na osobę na rok)")
    s4 = C.stado(4, 300, 22.0, 5.0, 4.5); s2 = C.stado(2, 300, 22.0, 5.0, 4.5); s6 = C.stado(6, 300, 22.0, 5.0, 4.5)
    pelny = dict(nioski=54, koguty=4, kurki=10, kogutki=0, brojlery=24, kaczki=16, gesi=12)
    print("| Wariant | Nioski | Koguty | Kurki+kogutki z wylęgu na rok | Kurczęta rzeźne na rok | Kaczki na rok | Gęsi na rok | Stan w szczycie [szt.] | Jaja [szt./rok] | Mięso w tuszkach [kg/rok] | Tłuszcz w tuszkach [kg/rok] | Pasza treściwa [kg/rok] |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    print(C.wiersz_stada("2 osoby", s2, 160)); print(C.wiersz_stada("4 osoby (główny)", s4, 160)); print(C.wiersz_stada("6 osób", s6, 160))
    print(C.wiersz_stada("Pełny: 100 sztuk w szczycie", pelny, 190))
    pp = C.produkcja(pelny, 190); p4 = C.produkcja(s4, 160)
    print(f"\nWariant pełny: stan w szczycie {C.szczyt(pelny)} szt.; jaja {pp['jaja']} szt./rok; potrzeba 4 osób {4*300} szt.; nadwyżka {pp['jaja']-1200} szt./rok = {(pp['jaja']-1200)/52:.0f} szt./tydzień.")
    print(f"Wariant pełny: mięso {pp['mieso']:.0f} kg/rok (kurczak {pp['kurczak']:.0f}, kaczka {pp['kaczka']:.0f}, gęś {pp['ges']:.0f}); potrzeba 4 osób {4*(22+5+4.5):.0f} kg.")
    print("\n### Pasza: struktura [kg/rok]\n")
    print("| Pozycja | 4 osoby | Pełny 100 szt. |"); print("|---|---|---|")
    pz4 = C.pasza(s4); pzp = C.pasza(pelny)
    for k in pz4: print(f"| {k} | {pz4[k]:.0f} | {pzp[k]:.0f} |")
    t4 = sum(pz4.values()) / 1000; tp = sum(pzp.values()) / 1000
    print(f"| **Suma** | **{t4*1000:.0f}** | **{tp*1000:.0f}** |")
    print("\n### Receptura dla gleb lekkich\n")
    print("| Składnik | Udział [%] | Białko [g/100 g] | Plon ostrożny [t/ha] | Plon dobry [t/ha] |"); print("|---|---|---|---|---|")
    for n, u, kp, kf in RECEPTURA_L:
        b = C.BIALKO_MAKUCH if kf is None else FAO[kf][1]
        pl = ("–", "–") if kp is None else (f"{PLONY_L[kp][0]:.1f}", f"{PLONY_L[kp][1]:.1f}")
        print(f"| {n} | {u*100:.0f} | {b:.1f} | {pl[0]} | {pl[1]} |")
    print(f"\nBiałko ogólne mieszanki: {bialko_L():.1f} % [obliczenie].")
    print(f"Powierzchnia na 1 t mieszanki na glebie lekkiej: {ha_na_tone_L(0):.2f} ha (plon ostrożny), {ha_na_tone_L(1):.2f} ha (plon dobry), z makuchem własnym, zapas 15 %.")
    print(f"Bez makuchu: {ha_na_tone_L(0, False):.2f} ha i {ha_na_tone_L(1, False):.2f} ha.")
    makuch = N_OS * 10 / PRZEROB["olej_lniankowy"] * (1 - PRZEROB["olej_lniankowy"])
    print(f"Makuch lniankowy z tłoczenia 40 kg oleju: {makuch:.0f} kg/rok [obliczenie].")
    print("\n| Wariant | Pasza [t/rok] | Pole paszowe, plon ostrożny [ha] | Pole paszowe, plon dobry [ha] |"); print("|---|---|---|---|")
    for nz, t in (("Stado 4 osób", t4), ("Pełny 100 szt.", tp)):
        print(f"| {nz} | {t:.2f} | {t*ha_na_tone_L(0, False):.2f} | {t*ha_na_tone_L(1, False):.2f} |")
    kgn = PASZA_NIOSKA_G_DOBA * 365 / 1000
    print(f"\nNa 1 nioskę ({kgn:.1f} kg paszy/rok): {kgn/1000*ha_na_tone_L(0, False)*10000:.0f} m² (plon ostrożny), {kgn/1000*ha_na_tone_L(1, False)*10000:.0f} m² (plon dobry).")
    # najwieksze stado z pozostalej powierzchni
    print("\n### Największe stado wyżywione z własnego pola\n")
    print("| Scenariusz | Pole wolne po żywności [m²] | Pasza własna [kg/rok] | Równoważnik niosek [szt.] | Udział w paszy stada 4 osób | Udział w paszy 100 sztuk |"); print("|---|---|---|---|---|---|")
    wolne_o = max(0.0, POLA_M2 - co); wolne_d = max(0.0, POLA_M2 - cd)
    sad_wolne = SAD_M2 - N_OS * go["sad i jagodnik"]; sad_wolne_d = SAD_M2 - N_OS * gd["sad i jagodnik"]
    for nz, m2, idx in (("Plon ostrożny, tylko pola 16/1", wolne_o, 0), ("Plon dobry, tylko pola 16/1", wolne_d, 1),
                        ("Plon ostrożny, dodatkowo wolna część stoku 24/1", wolne_o + sad_wolne, 0), ("Plon dobry, dodatkowo wolna część stoku 24/1", wolne_d + sad_wolne_d, 1)):
        kg = m2 / 10000 / ha_na_tone_L(idx, False) * 1000
        print(f"| {nz} | {m2:.0f} | {kg:.0f} | {kg/kgn:.0f} | {100*kg/(t4*1000):.0f} % | {100*kg/(tp*1000):.0f} % |")
    print(f"\nWolna część stoku 24/1 po sadzie: {sad_wolne:.0f} m² (plon ostrożny), {sad_wolne_d:.0f} m² (plon dobry).")
    print(f"Zakup paszy: stado 4 osób {t4:.2f} t/rok; 100 sztuk {tp:.2f} t/rok. Z makuchem własnym ({makuch:.0f} kg) zakup maleje o {makuch/1000:.2f} t.")
    oszcz = 0.15
    print(f"Wybieg trawiasty i odpady z ogrodu: oszczędność paszy [założenie] {oszcz*100:.0f} % od kwietnia do października = {tp*oszcz*7/12:.2f} t/rok dla 100 sztuk.")
    print("\n### Woda, obornik, wybieg, kurnik\n")
    print("| Wariant | Woda w szczycie [L/dobę] | Obornik [t/rok] | N [kg/rok] | N działający wiosną [kg/rok] | P2O5 [kg/rok] | K2O [kg/rok] | Min. powierzchnia przy 170 kg N/ha [ha] | Pole nawożone dawką 12,5 t/ha [ha] | Wybieg eko [m²] | Kurnik eko [m²] | Grzędy [m] | Gniazda [szt.] |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for nz, s in (("Stado 4 osób", s4), ("Pełny 100 szt.", pelny)):
        t, n = C.obornik(s); wyb, kur, grz, gn = C.wybieg_i_kurnik(s)
        print(f"| {nz} | {C.woda(s):.0f} | {t:.2f} | {n:.0f} | {n*ROWNOWAZNIK_N['wiosna']:.0f} | {t*OBORNIK_P2O5_KG_T:.0f} | {t*OBORNIK_K2O_KG_T:.0f} | {n/N_MAX_KG_HA:.2f} | {t/12.5:.2f} | {wyb:.0f} | {kur:.1f} | {grz:.1f} | {gn} |")
    n_pasza = tp * 1000 * bialko_L() / 100 / 6.25
    print(f"\nAzot w kupionej paszy dla 100 sztuk: {tp:.2f} t × {bialko_L():.1f} % białka / 6,25 = {n_pasza:.0f} kg N/rok [obliczenie].")

    # ---------- 4. kozy, owce, pszczoly ----------
    sekcja("F4. Kozy albo owce mleczne, pszczoły")
    mleko = N_OS * 250
    print(f"Potrzeba mleka: {N_OS} × 250 kg = {mleko} kg/rok.\n")
    print("| Gatunek | Wydajność [kg mleka/szt./rok] | Liczba samic na 1000 kg | Źródło |"); print("|---|---|---|---|")
    print(f"| Koza rasy uszlachetnionej (biała, barwna), saaneńska | {KOZA['mleko_kg_laktacja'][0]}–{KOZA['mleko_kg_laktacja'][1]} | {math.ceil(mleko/KOZA['mleko_kg_laktacja'][0])} (przy 600 kg) | [S41] |")
    print(f"| Owca (kołudzka, merynos, mieszańce fryzyjskie), dój po odsadzeniu jagniąt | {OWCA['mleko_kg_okres_doju'][0]}–{OWCA['mleko_kg_okres_doju'][1]} | {math.ceil(mleko/OWCA['mleko_kg_okres_doju'][1])}–{math.ceil(mleko/OWCA['mleko_kg_okres_doju'][0])} | [S57] |")
    kozy = 2
    dni_zima = 200; dni_lato = 165
    siano = kozy * 2.0 * dni_zima; ziel = kozy * KOZA["zielonka_kg_doba"] * dni_lato; siano_eq = siano + ziel / 5
    tresc = kozy * 100
    print(f"\n2 kozy, siano: {kozy} × 2,0 kg × {dni_zima} dni = {siano:.0f} kg. Zielonka: {kozy} × 7 kg × {dni_lato} dni = {ziel:.0f} kg = {ziel/5:.0f} kg siana. Przelicznik: 5 kg zielonki = 1 kg siana [S60]. Razem {siano_eq:.0f} kg siana.")
    for nz, pl in (("3,0 t/ha [założenie dla suchej gleby lekkiej]", SIANO_T_HA_LEKKA), ("5,5 t/ha [S5]", SIANO_T_HA)):
        print(f"- Plon siana {nz}: potrzeba {siano_eq/1000/pl*10000:.0f} m²; łąka 16/3 (4400 m²) daje {LAKA_M2/10000*pl*1000:.0f} kg; saldo {LAKA_M2/10000*pl*1000 - siano_eq:+.0f} kg.")
    print(f"- Pasza treściwa: [założenie] 100 kg/kozę/rok = {tresc} kg/rok (owies z zakupu albo z pola: {tresc/1000/PLONY_L['owies'][0]*10000:.0f} m² przy plonie ostrożnym).")
    print(f"- Budynek: kojec grupowy {kozy} × 1,5 m² + koźlęta 4 × 0,3 m² = {kozy*1.5+4*0.3:.1f} m²; wybieg {kozy} × 4 m² = {kozy*4} m² [S30].")
    print(f"- Obornik: {kozy} × 1,2 t × 8,4 kg N/t = {kozy*1.2*8.4:.0f} kg N/rok [S31].")
    rodz = 3
    print(f"\nPszczoły: potrzeba {N_OS} × 8 kg = {N_OS*8} kg miodu/rok. {rodz} rodziny dają {rodz*MIOD_KG_RODZINA['slaby_rok']}–{rodz*MIOD_KG_RODZINA['sredni_rok']} kg/rok (11–17 kg/rodzinę [S7]).")

    # ---------- 5. praca ----------
    sekcja("F5. Nakład pracy [rbh/rok], 4 osoby, plan na 1,5 ha")
    pow_ha = {"warzywnik i tunel": (pot["warzywnik"][0] + pot["tunel foliowy"][0]) / 10000, "ziemniaki": pot["okopowe"][0] / 10000,
              "strączkowe, zboża, oleiste": min(POLA_M2 - pot["warzywnik"][0] - pot["tunel foliowy"][0] - pot["okopowe"][0], pot["strączkowe"][0] + pot["zboża"][0] + pot["oleiste"][0]) / 10000,
              "sad i jagodnik": N_OS * go["sad i jagodnik"] / 10000, "łąka (siano)": LAKA_M2 / 10000}
    klucz = {"warzywnik i tunel": "warzywa", "ziemniaki": "okopowe", "strączkowe, zboża, oleiste": "zboża", "sad i jagodnik": "sady", "łąka (siano)": "pastewne"}
    print("| Dział | Powierzchnia [ha] | Norma: średnia [rbh/ha] | Norma: gospodarstwa mniejsze niż 5 ha [rbh/ha] | Praca: średnia [rbh/rok] | Praca: małe gospodarstwa [rbh/rok] |"); print("|---|---|---|---|---|---|")
    s1 = s2_ = 0.0
    for k, ha in pow_ha.items():
        a = PRACA_RBH_HA_SREDNIO[klucz[k]]; b = PRACA_RBH_HA_DO5HA[klucz[k]]
        s1 += ha * a; s2_ += ha * b
        print(f"| {k} | {ha:.3f} | {a} | {b} | {ha*a:.0f} | {ha*b:.0f} |")
    print(f"| **Uprawy razem** | **{sum(pow_ha.values()):.2f}** | | | **{s1:.0f}** | **{s2_:.0f}** |")
    zw = {"drób: 20 min/dobę [założenie]": 20/60*365, "kozy: 2 × dój 2 × 15 min przez 250 dni + obsługa 15 min/dobę [założenie]": 2*0.25*250 + 0.25*365,
          "pszczoły: 3 rodziny × 15 h [założenie]": 45.0}
    for k, v in zw.items(): print(f"| {k} | – | – | – | {v:.0f} | {v:.0f} |")
    print(f"| **Razem** | | | | **{s1+sum(zw.values()):.0f}** | **{s2_+sum(zw.values()):.0f}** |")
    print(f"\nRazem od {s1+sum(zw.values()):.0f} do {s2_+sum(zw.values()):.0f} rbh/rok = od {(s1+sum(zw.values()))/365:.1f} do {(s2_+sum(zw.values()))/365:.1f} h/dobę średnio. Przetwórstwo i kuchnia są poza zakresem.")

    # ---------- 6. azot ----------
    sekcja("F6. Bilans azotu pól i ogrodu, 4 osoby [kg N/rok]")
    zb = {n: z * N_OS for n, gr, kg, pr, z, zz, pl, m2, kcal in powierzchnia(2, 0)[0]}
    wyn = [("Żyto", zb["Żyto: mąka razowa"], POBRANIE_N["zyto"]), ("Owies", zb["Owies nagi: płatki, kasza"], POBRANIE_N["owies"]),
           ("Pszenica", zb["Pszenica: mąka razowa, kasze"], POBRANIE_N["pszenica"]),
           ("Gryka i proso (przyjęto 24 kg N/t [założenie])", zb["Gryka: kasza"] + zb["Proso: kasza jaglana"], 24.0),
           ("Ziemniaki", zb["Ziemniaki"], POBRANIE_N["ziemniak"]),
           ("Lnianka (przyjęto wartość rzepaku 50 kg N/t [założenie])", zb["Olej lniankowy (rydzowy) tłoczony na zimno"], POBRANIE_N["rzepak"]),
           ("Warzywa (przyjęto 2,0 kg N/t [S31])", N_OS * 201, 2.0)]
    print("| Pozycja | Zbiór [kg/rok] | Pobranie [kg N/t] [S31] | Pobranie [kg N/rok] |"); print("|---|---|---|---|")
    sn = 0.0
    for n, kg, wsp in wyn:
        sn += kg / 1000 * wsp; print(f"| {n} | {kg:.0f} | {wsp} | {kg/1000*wsp:.1f} |")
    print(f"| **Pobranie razem** | | | **{sn:.1f}** |")
    t4o, n4o = C.obornik(s4); tpo, npo = C.obornik(pelny)
    straczk_ha = pot["strączkowe"][0] / 10000
    print("\n| Źródło azotu | kg N/rok | Podstawa |"); print("|---|---|---|")
    print(f"| Obornik drobiowy, stado 4 osób: N działający wiosną | {n4o*0.45:.1f} | {n4o:.0f} kg N × 0,45 [S31] |")
    print(f"| Obornik drobiowy, 100 sztuk: N działający wiosną | {npo*0.45:.1f} | {npo:.0f} kg N × 0,45 [S31] |")
    print(f"| Obornik kozi, 2 kozy: N działający wiosną | {2*1.2*8.4*0.35:.1f} | 20 kg N × 0,35 [S31] |")
    print(f"| Resztki po strączkowych | {straczk_ha*25:.1f} | {straczk_ha:.3f} ha × 25 kg N/ha [S31] |")
    print(f"| Międzyplon bobowaty przyorany na 0,20 ha | {0.20*50:.1f} | 0,20 ha × 50 kg N/ha [S31] |")
    r4 = n4o*0.45 + 2*1.2*8.4*0.35 + straczk_ha*25 + 0.20*50
    rp = npo*0.45 + 2*1.2*8.4*0.35 + straczk_ha*25 + 0.20*50
    print(f"| **Razem ze stadem 4 osób** | **{r4:.1f}** | pobranie {sn:.1f}: saldo {r4-sn:+.1f} |")
    print(f"| **Razem ze stadem 100 sztuk** | **{rp:.1f}** | pobranie {sn:.1f}: saldo {rp-sn:+.1f} |")

    # ---------- 7. przechowywanie ----------
    sekcja("F7. Zapasy na 12 miesięcy: masa i objętość, 4 osoby (wariant L)")
    d = {n: (kg0, kg1, kg2)[2] for n, k, kg0, kg1, kg2, g in DIETA}
    poz = [  # (pozycja, masa na osobe [kg], gestosc [kg/m3], metoda, czy potrzebna zamrazarka)
        ("Ziarno żyta", d["Żyto: mąka razowa"] / 0.95, GESTOSC["zyto"], "skrzynia albo silos, wilgotność ziarna co najwyżej 14 %"),
        ("Ziarno owsa nagiego", d["Owies nagi: płatki, kasza"] / 0.95, GESTOSC["owies"], "jak żyto"),
        ("Ziarno pszenicy", d["Pszenica: mąka razowa, kasze"] / 0.95, GESTOSC["pszenica"], "jak żyto"),
        ("Gryka i proso (nieobłuszczone)", d["Gryka: kasza"] / 0.65 + d["Proso: kasza jaglana"] / 0.70, GESTOSC["proso"], "jak żyto"),
        ("Strączkowe suche", (d["Fasola sucha"] + d["Groch suchy"] + d["Bób suchy"]) / 0.95, GESTOSC["fasola"], "worki, 4–10 °C, wilgotność powietrza 40–50 %"),
        ("Nasiona lnianki na olej", d["Olej lniankowy (rydzowy) tłoczony na zimno"] / PRZEROB["olej_lniankowy"], GESTOSC["rzepak"], "worki; tłoczenie co 1–2 miesiące"),
        ("Słonecznik, len, mak, pestki dyni", d["Słonecznik: nasiona w łusce"] + d["Siemię lniane"] + d["Mak"] + d["Pestki dyni oleistej"], GESTOSC["slonecznik"], "worki, sucho"),
        ("Orzechy w łupinie", 8, 400, "skrzynki, sucho, przewiew"),
        ("Ziemniaki jadalne", d["Ziemniaki"] * 1.10, GESTOSC["ziemniak"], "piwnica ziemna 4–6 °C, 90–95 %"),
        ("Sadzeniaki", 177.1 * 0.24, GESTOSC["ziemniak"], "piwnica 2–6 °C"),
        ("Marchew, burak, seler, pietruszka, brukiew", (d["Marchew"] + d["Burak ćwikłowy"] + d["Seler korzeniowy"] + d["Pietruszka korzeniowa"] + d["Brukiew, rzepa"]) * 0.75, GESTOSC["korzeniowe"], "piwnica 0–1 °C, 95–98 %, w piasku"),
        ("Kapusta świeża", 15, GESTOSC["kapusta"], "piwnica 0 °C, 90–95 %"),
        ("Kapusta kiszona", 25, 1000, "beczka albo kamionka w piwnicy"),
        ("Cebula i czosnek", (d["Cebula"] + d["Czosnek"]) * 0.75, GESTOSC["cebula"], "sucho, 0 °C, 65–75 %"),
        ("Dynia zimowa", d["Dynia zimowa"] * 0.75, GESTOSC["dynia"], "sucho, 10–13 °C, 50–70 %"),
        ("Jabłka i gruszki", (d["Jabłka"] + d["Gruszki"]) * 0.6, GESTOSC["jablka"], "piwnica −1 do 4 °C, 90–95 %"),
        ("Przetwory w słoikach (pomidory, ogórki, owoce)", 40, 600, "pasteryzacja; słoiki 0,9 L"),
        ("Susz (jabłka, śliwki, zioła, grzyby)", 5, 300, "suszarnia słoneczna albo piec"),
        ("Miód", d["Miód"], 1420, "słoiki, mniej niż 18 °C"),
    ]
    print("| Zapas | Masa na 1 osobę [kg] | Masa na 4 osoby [kg] | Gęstość usypowa [kg/m³] | Objętość netto, 4 osoby [m³] | Metoda |"); print("|---|---|---|---|---|---|")
    sm = sv = 0.0; sv_piw = 0.0
    for n, kg, ro, met in poz:
        v = N_OS * kg / ro; sm += N_OS * kg; sv += v
        if "piwnica" in met or "beczka" in met or "pasteryzacja" in met: sv_piw += v
        print(f"| {n} | {kg:.0f} | {N_OS*kg:.0f} | {ro} | {v:.2f} | {met} |")
    print(f"| **Razem** | **{sm/N_OS:.0f}** | **{sm:.0f}** | | **{sv:.2f}** | |")
    print(f"\nObjętość netto produktów: {sv:.1f} m³, w tym piwnica ziemna {sv_piw:.1f} m³. Objętość pomieszczeń przy wypełnieniu 30 % [założenie]: piwnica {sv_piw/0.3:.0f} m³, spichlerz {(sv-sv_piw)/0.3:.0f} m³.")
    print(f"Na 1 osobę: {sm/N_OS:.0f} kg zapasów i {sv/N_OS:.2f} m³ netto.")
    # zamrazarka
    sekcja("F8. Zamrażarka: ile żywności wymaga mrożenia (off-grid)")
    partie = 3
    broj = s4["brojlery"]; kacz = s4["kaczki"]; ges = s4["gesi"]
    m_partia = math.ceil(broj / partie) * C.TUSZKA_BROJLER
    m_kacz = math.ceil(kacz / 2) * C.TUSZKA_KACZKA; m_ges = ges * C.TUSZKA_GES
    print(f"Mięso drobiowe 4 osób: {4*(22+5+4.5):.0f} kg tuszek/rok = {4*(22+5+4.5)/52:.1f} kg/tydzień.")
    print(f"- Kurczęta rzeźne: {broj} szt./rok w {partie} partiach po {math.ceil(broj/partie)} szt. = {m_partia:.0f} kg tuszek na partię.")
    print(f"- Kaczki: 2 partie po {math.ceil(kacz/2)} szt. = {m_kacz:.0f} kg na partię. Gęsi: {ges} szt. = {m_ges:.0f} kg (ubój od października do grudnia).")
    szczyt_mroz = m_partia + m_kacz + m_ges * 0.5
    print(f"- Wariant A, zamrażarka: szczyt zapasu = 1 partia kurcząt + 1 partia kaczek + połowa gęsi = {szczyt_mroz:.0f} kg. Pojemność przy 0,5 kg/L [założenie]: {szczyt_mroz/0.5:.0f} L.")
    tyg = 4*(22+5+4.5)/52
    print(f"- Wariant B, bez zamrażarki: ubój co tydzień {tyg:.1f} kg (1–2 ptaki), gęsi i kaczki w słoikach i w tłuszczu. Mrożenie: 0 kg.")
    print(f"- Owoce jagodowe i warzywa: 0 kg w zamrażarce przy suszeniu, kiszeniu i pasteryzacji. Opcja: do 30 kg jagód [założenie].")

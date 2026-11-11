# -*- coding: utf-8 -*-
"""A. Normy i dieta modelowa: energia, bialko, tluszcz, weglowodany, blonnik, wybrane mikroskladniki."""
from dane import *

def interpoluj_eer(tab, pal):
    """EER jest proporcjonalne do PAL: EER = PPM x PAL. PPM = EER(1,8)/1,8."""
    ppm = tab[1.8] / 1.8
    return ppm * pal

def tabela_norm():
    w = []
    w.append("| Płeć | Wiek [lata] | Wzrost [cm] | Masa [kg] | PAL 1,6 | PAL 1,75 | PAL 1,8 | PAL 2,0 | Białko RDA [g/dobę] |")
    w.append("|---|---|---|---|---|---|---|---|---|")
    for (plec, wiek, wzrost, masa), t in EER.items():
        p175 = interpoluj_eer(t, 1.75)
        w.append(f"| {plec} | {wiek} | {wzrost:.1f} | {masa:.1f} | {t[1.6]} | {p175:.0f} | {t[1.8]} | {t[2.0]} | {masa*BIALKO_RDA_G_NA_KG:.0f} |")
    return "\n".join(w)

def policz(wariant):
    """wariant 0 = W0 bazowy, 1 = W1 z kozami i pszczolami, 2 = L docelowy (gleby lekkie). Zwraca wiersze i sumy na rok."""
    wiersze = []
    s = dict(kg=0.0, kcal=0.0, b=0.0, t=0.0)
    for nazwa, klucz, kg0, kg1, kg2, grupa in DIETA:
        kg = (kg0, kg1, kg2)[wariant]
        kcal100, b100, t100 = FAO[klucz]
        kcal = kg * 10 * kcal100
        b = kg * 10 * b100 / 1000.0   # kg bialka na rok
        t = kg * 10 * t100 / 1000.0   # kg tluszczu na rok
        wiersze.append((nazwa, grupa, kg, kcal100, b100, t100, kcal, b, t))
        s["kg"] += kg; s["kcal"] += kcal; s["b"] += b; s["t"] += t
    return wiersze, s

def md_dieta(wariant):
    wiersze, s = policz(wariant)
    out = ["| Produkt | Grupa | kg/rok | g/dobę | kcal/100 g | kcal/rok | kcal/dobę | Białko kg/rok | Tłuszcz kg/rok |",
           "|---|---|---|---|---|---|---|---|---|"]
    for n, g, kg, k100, b100, t100, kcal, b, t in wiersze:
        if kg == 0:
            continue
        out.append(f"| {n} | {g} | {kg:.1f} | {kg*1000/365:.0f} | {k100} | {kcal:.0f} | {kcal/365:.0f} | {b:.2f} | {t:.2f} |")
    out.append(f"| **Suma** |  | **{s['kg']:.0f}** | **{s['kg']*1000/365:.0f}** |  | **{s['kcal']:.0f}** | **{s['kcal']/365:.0f}** | **{s['b']:.1f}** | **{s['t']:.1f}** |")
    return "\n".join(out), wiersze, s

def grupy(wiersze):
    g = {}
    for n, gr, kg, k100, b100, t100, kcal, b, t in wiersze:
        d = g.setdefault(gr, dict(kg=0, kcal=0, b=0, t=0))
        d["kg"] += kg; d["kcal"] += kcal; d["b"] += b; d["t"] += t
    return g

def pokrycie(s, masa=69.7, energia=ENERGIA_PROJEKTOWA):
    kcal_d = s["kcal"] / 365
    b_d = s["b"] * 1000 / 365
    t_d = s["t"] * 1000 / 365
    w_kcal = kcal_d - 4 * b_d - 9 * t_d      # weglowodany z roznicy (rownowazniki Atwatera 4-9-4)
    w_d = w_kcal / 4
    out = []
    out.append("| Składnik | Dieta | Norma | Pokrycie |")
    out.append("|---|---|---|---|")
    out.append(f"| Energia [kcal/dobę] | {kcal_d:.0f} | {energia} (wartość projektowa) | {100*kcal_d/energia:.0f} % |")
    rda = masa * BIALKO_RDA_G_NA_KG
    out.append(f"| Białko [g/dobę] | {b_d:.0f} | RDA {rda:.0f} (0,83 g/kg × {masa} kg) | {100*b_d/rda:.0f} % |")
    out.append(f"| Białko [% energii] | {100*4*b_d/kcal_d:.1f} | brak normy procentowej dla dorosłych w [S1] | – |")
    out.append(f"| Tłuszcz [g/dobę] | {t_d:.0f} | od {energia*0.30/9:.0f} do {energia*0.40/9:.0f} (30–40 % E, [S1]) | – |")
    out.append(f"| Tłuszcz [% energii] | {100*9*t_d/kcal_d:.1f} | 30–40 [S1]; 20–35 [S3] | {'w zakresie [S1]' if 30 <= 100*9*t_d/kcal_d <= 40 else 'poza zakresem [S1]'} |")
    out.append(f"| Węglowodany [g/dobę] (z różnicy) | {w_d:.0f} | od {energia*0.45/4:.0f} do {energia*0.65/4:.0f} (45–65 % E) | – |")
    out.append(f"| Węglowodany [% energii] | {100*w_kcal/kcal_d:.1f} | 45–65 [S1] | {'w zakresie' if 45 <= 100*w_kcal/kcal_d <= 65 else 'poza zakresem'} |")
    return "\n".join(out), dict(kcal=kcal_d, b=b_d, t=t_d, w=w_d)

def blonnik(wiersze):
    suma = 0.0
    for n, gr, kg, *_ in wiersze:
        if n in BLONNIK:
            v = BLONNIK[n][0]
        elif gr in BLONNIK_DOMYSLNY and "Orzech" not in n:
            v = BLONNIK_DOMYSLNY[gr]
        else:
            v = 0.0   # brak wartosci: pominieto (oszacowanie dolne)
        suma += kg * 10 * v
    return suma / 365   # g/dobe

def mikro(wiersze, wariant):
    d = {n: kg for n, gr, kg, *_ in wiersze}
    out = []
    # witamina C (surowce przed stratami)
    c = sum(d.get(n, 0) * 10 * v for n, v in WIT_C_MG_100G.items()) / 365
    out.append(("Witamina C [mg/dobę], 7 pozycji, surowiec przed stratami", c, "RDA 90 (M), 75 (K) [S1]"))
    # wapn z pozycji o znanej zawartosci
    ca = sum(d.get(n, 0) * 10 * v for n, v in WAPN_MG_100G.items()) / 365
    ca_mleko = d.get("Mleko kozie", 0) * 10 * WAPN_MLEKO_MG_100G / 365
    out.append(("Wapń [mg/dobę] z jarmużu, strączkowych, maku", ca, "RDA 1000 [S2]"))
    out.append(("Wapń [mg/dobę] z mleka koziego (wartość mleka krowiego 120 mg/100 g: [założenie])", ca_mleko, "RDA 1000 [S2]"))
    # B12
    jaja_kg = [kg for n, gr, kg, *_ in wiersze if n.startswith("Jaja")][0]
    tuszki = sum(kg for n, gr, kg, *_ in wiersze if "tuszka" in n)
    b12 = (jaja_kg * UDZIAL_CZESCI_JADALNEJ["jaja"] * 10 * B12_UG_100G["jaja"]
           + tuszki * UDZIAL_CZESCI_JADALNEJ["tuszka"] * 10 * B12_UG_100G["mieso_drobiowe"]) / 365
    out.append(("Witamina B12 [µg/dobę] z jaj i mięsa drobiowego", b12, "RDA 2,4 [S2]"))
    b12m = d.get("Mleko kozie", 0) * 10 * B12_UG_100G["mleko"] / 365
    out.append(("Witamina B12 [µg/dobę] z mleka (wartość mleka krowiego: [założenie])", b12m, "RDA 2,4 [S2]"))
    wd = jaja_kg * UDZIAL_CZESCI_JADALNEJ["jaja"] * 10 * WIT_D_UG_100G["jaja"] / 365
    out.append(("Witamina D [µg/dobę] z jaj", wd, "AI 15 [S1]"))
    # ALA
    olej_rz = d.get("Olej rzepakowy tłoczony na zimno", 0)
    olej_ln = d.get("Olej lniany", 0)
    siemie = d.get("Siemię lniane", 0)
    olej_lk = d.get("Olej lniankowy (rydzowy) tłoczony na zimno", 0)
    ala = (olej_rz * 1000 * 0.096 + olej_ln * 1000 * 0.5693 + olej_lk * 1000 * 0.388 + siemie * 1000 * 0.34 * 0.5693) / 365
    out.append(("ALA [g/dobę] z oleju rzepakowego, lnianego, lniankowego i siemienia [S47]", ala, f"AI 0,5 % E = {ENERGIA_PROJEKTOWA*0.005/9:.1f} g [S1]"))
    # selen: zakres z zawartosci w zbozach i ziemniakach [S52]
    se_min = (d.get("Pszenica: mąka razowa, kasze", 0) * 50 + d.get("Żyto: mąka razowa", 0) * 150 + d.get("Owies nagi: płatki, kasza", 0) * 100
              + d.get("Jęczmień: kasza (pęczak)", 0) * 30 + d.get("Ziemniaki", 0) * 20) / 365
    se_max = (d.get("Pszenica: mąka razowa, kasze", 0) * 200 + d.get("Żyto: mąka razowa", 0) * 400 + d.get("Owies nagi: płatki, kasza", 0) * 290
              + d.get("Jęczmień: kasza (pęczak)", 0) * 350 + d.get("Ziemniaki", 0) * 20) / 365
    out.append(("Selen [µg/dobę] ze zbóż i ziemniaków: dolna granica", se_min, "AI 70 [S3]"))
    out.append(("Selen [µg/dobę] ze zbóż i ziemniaków: górna granica", se_max, "AI 70 [S3]"))
    return out

if __name__ == "__main__":
    print("## Normy energii i białka [S1]\n")
    print(tabela_norm())
    for wariant, nazwa in ((2, "L docelowy: gleby lekkie V–VI, rośliny + jaja + drób + mleko kozie + miód"), (0, "W0 bazowy: rośliny + jaja + drób, gleby średnie"), (1, "W1: z kozami mlecznymi i pszczołami, gleby średnie")):
        tab, wiersze, s = md_dieta(wariant)
        print(f"\n## Dieta modelowa, wariant {nazwa}: 1 dorosły, 1 rok\n")
        print(tab)
        print("\n### Udział grup\n")
        print("| Grupa | kg/rok | kcal/dobę | % energii | Białko g/dobę | Tłuszcz g/dobę |")
        print("|---|---|---|---|---|---|")
        for g, v in grupy(wiersze).items():
            if v["kg"] == 0: continue
            print(f"| {g} | {v['kg']:.0f} | {v['kcal']/365:.0f} | {100*v['kcal']/s['kcal']:.1f} | {v['b']*1000/365:.1f} | {v['t']*1000/365:.1f} |")
        pk, dd = pokrycie(s)
        print("\n### Pokrycie norm\n")
        print(pk)
        bl = blonnik(wiersze)
        print(f"| Błonnik [g/dobę], oszacowanie dolne | {bl:.0f} | AI {BLONNIK_AI_G} [S1] | {100*bl/BLONNIK_AI_G:.0f} % |")
        print("\n### Mikroskładniki: oszacowanie z pozycji o znanej zawartości\n")
        print("| Składnik | Dieta | Norma |")
        print("|---|---|---|")
        for n, v, norma in mikro(wiersze, wariant):
            print(f"| {n} | {v:.1f} | {norma} |")
    # jod z soli
    print("\n## Jod z soli jodowanej [obliczenie]\n")
    for ki in (20, 40):
        jod = ki * 126.90 / 166.00   # mg jodu na kg soli; masy molowe I = 126,90; KI = 166,00 g/mol
        print(f"- KI {ki} mg/kg soli = {jod:.1f} mg I/kg soli; 5 g soli na dobę = {jod*5:.0f} µg I/dobę")
    # warianty osobowe
    print("\n## Skalowanie energii na gospodarstwo\n")
    print("| Liczba osób | N × 3000 kcal/dobę | Wariant mieszany: połowa M 30–59 PAL 1,8 (2911) i połowa K 30–59 PAL 1,8 (2351) |")
    print("|---|---|---|")
    for n in (1, 2, 4, 6):
        mix = n / 2 * 2911 + n / 2 * 2351
        print(f"| {n} | {n*3000} | {mix:.0f} |")

# -*- coding: utf-8 -*-
"""Sklada raport z szablonow tpl/p1..p4.md i z tabel w out/*.md. Zamienia kropke dziesietna na przecinek w tabelach skryptow."""
import re, io
OUT = {"a": "out/a_dieta.md", "b": "out/b_plony.md", "c": "out/c_drob.md", "f": "out/f_plan.md"}
def sekcje(path):
    res = []; nagl = None; buf = []
    for line in io.open(path, encoding="utf-8"):
        if line.startswith("#"):
            if nagl is not None: res.append((nagl, "".join(buf).strip("\n")))
            nagl = line.lstrip("#").strip(); buf = []
        else:
            buf.append(line)
    if nagl is not None: res.append((nagl, "".join(buf).strip("\n")))
    return res
SEK = {k: sekcje(v) for k, v in OUT.items()}
def przecinek(t):
    return re.sub(r"(?<=\d)\.(?=\d)", ",", t)
def wstaw(m):
    plik, fraza, nr = m.group(1), m.group(2), int(m.group(3))
    traf = [b for h, b in SEK[plik] if fraza in h]
    if len(traf) < nr:
        raise SystemExit(f"BRAK SEKCJI: {plik}|{fraza}|{nr}")
    # sekcje F zawieraja podsekcje ###: dolacz je, gdy fraza zaczyna sie od "F"
    if plik == "f" and fraza.startswith("F"):
        idx = [i for i, (h, b) in enumerate(SEK[plik]) if fraza in h][nr - 1]
        czesci = [SEK[plik][idx][1]]
        j = idx + 1
        while j < len(SEK[plik]) and not re.match(r"F\d\.", SEK[plik][j][0]):
            czesci.append("**" + SEK[plik][j][0] + "**\n\n" + SEK[plik][j][1]); j += 1
        return przecinek("\n\n".join(czesci))
    return przecinek(traf[nr - 1])
tekst = "".join(io.open(f"tpl/p{i}.md", encoding="utf-8").read() for i in (1, 2, 3, 4))
tekst = re.sub(r"\{\{(\w)\|([^|}]+)\|(\d)\}\}", wstaw, tekst)
tekst = tekst.replace("[S7b]", "[S5]")
io.open("../../raporty/R2-zywnosc-uprawy-drob.md", "w", encoding="utf-8").write(tekst)
print("zapisano", len(tekst), "znakow;", len(tekst.split()), "slow")

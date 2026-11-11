#!/usr/bin/env python3
"""Mechaniczna kontrola Polszczyzny Kontrolowanej: dlugosc zdan i slowa zakazane. Uzycie: pk_check.py plik.md"""
import re, sys
BAN = [r"odpowiedni\w*", r"właściw\w*", r"stosown\w*", r"należyt\w*", r"niezwłoczn\w*", r"wkrótce", r"szybko", r"na bieżąco",
 r"regularn\w*", r"okresow\w*", r"często", r"rzadko", r"zwykle", r"kilka", r"kilku", r"kilkanaście", r"parę", r"wiele", r"wielu", r"większość\w*",
 r"duż[yaeoi]\w*", r"mał[yaeoi]\w*", r"wysok[ia]\w*", r"wysokie\w*", r"nisk[ia]\w*", r"niskie\w*", r"dług[ia]\w*", r"długie\w*", r"krótk[ia]\w*", r"krótkie\w*",
 r"około", r"ok\.", r"mniej więcej", r"prawie", r"powyżej", r"poniżej", r"ponad", r"minimum", r"maksimum", r"min\.", r"maks\.",
 r"dziś", r"dzisiaj", r"jutro", r"wczoraj", r"obecnie", r"ostatnio", r"następn\w*", r"przyszł\w*", r"zeszł\w*", r"ostatni\w*",
 r"bądź", r"względnie", r"ewentualn\w*", r"i/lub", r"jeśli", r"o ile", r"w razie", r"chyba że", r"pod warunkiem",
 r"należy", r"trzeba", r"powinno się", r"wymaga się", r"musi", r"muszą", r"powinien", r"powinna", r"powinno", r"powinny", r"może", r"mogą", r"można",
 r"itp\.", r"itd\.", r"i inne", r"m\.in\.", r"dowoln\w*", r"niektór\w*", r"pewien", r"pewna", r"pewne", r"jakiś", r"jakaś", r"jakieś",
 r"podobno", r"chyba", r"raczej", r"prawdopodobn\w*", r"\w+ąc\b", r"\w+wszy\b", r"\w+łszy\b",
 r"\bon\b", r"\bona\b", r"\bgo\b", r"\bjej\b", r"\bjego\b", r"\bich\b", r"\bsw[oó]j\w*", r"\bswoj\w*"]
ALLOW = {"więc","tysiąc","miesiąc","pieniądz","zając","obecnie"} - {"obecnie"}
def strip_md(s):
    s=re.sub(r"`[^`]*`","X",s); s=re.sub(r"\[([^\]]*)\]\([^)]*\)",r"\1",s)
    s=re.sub(r"\[(źródło|obliczenie|założenie|relacja|pomiar|obserwacja|DO USTALENIA)[^\]]*\]","",s)
    return s
def sentences(text):
    out=[]
    for line in text.splitlines():
        line=line.strip()
        if not line or line.startswith('|---') or line.startswith('```'): continue
        if line.startswith('|'):
            cells=[c.strip() for c in line.strip('|').split('|')]
        else:
            cells=[re.sub(r"^(#+|[-*]|\d+\.|>)\s*","",line)]
        for c in cells:
            c=strip_md(c)
            for s in re.split(r"(?<=[.!?])\s+(?=[A-ZŁŚŻŹĆÓ„\"(])", c):
                if s.strip(): out.append(s.strip())
    return out
def main(path, limit=25):
    text=open(path,encoding='utf-8').read()
    bad=0
    for s in sentences(text):
        n=sum(1 for w in s.split() if re.search(r"\w", w))
        if n>limit:
            print(f"[{n} słów] {s}"); bad+=1
        low=s
        for b in BAN:
            for m in re.finditer(r"(?<!\w)"+b+r"(?!\w)", low):
                w=m.group(0)
                if w in ("MUSI","MOŻE","POWINIEN","MOGĄ","MUSZĄ","POWINNA","POWINNO","POWINNY"): continue
                if w.lower() in ALLOW: continue
                if w.isupper(): continue
                print(f"[zakazane: {w}] {s[:110]}"); bad+=1
    print("naruszenia:",bad)
if __name__=="__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 25)

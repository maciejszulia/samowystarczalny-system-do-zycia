# R1. Agent 1 — lokalizacja, działki, teren, klimat, gleba, prawo

> Wydanie publiczne z 11.11.2026. Raport pokazuje stan sprzed odpowiedzi właściciela z 11.11.2026; zmiany zawiera raport R4, sekcja 9. Wydanie pomija grupy rejestrowe działek.

Stan danych i prawa: 11 listopada 2026 r. Miejsce: ul. Młodzieżowa 1, 11-041 Olsztyn (Gutkowo).

Oznaczenia w tekście:
- **[Ź]** — dana odczytana ze źródła (URL w sekcji F).
- **[O]** — moje obliczenie z danych źródłowych (podaję metodę).
- **[S]** — mój szacunek albo wiedza ogólna, której dziś nie potwierdziłem w źródle pierwotnym.

---

## 0. Korekta współrzędnych — przeczytaj najpierw

**Punkt z zadania nie leży pod tym adresem.**

| Punkt | WGS84 | EPSG:2180 (E; N) [m] | Działka pod punktem | Źródło |
|---|---|---|---|---|
| Punkt z zadania | 53.762511 N, 20.466735 E | 596 658,0; 656 309,2 | 286201_1.0110.117/32 (obręb 110, zabudowa wielorodzinna/kampusowa) | ULDK GUGiK, WMS Olsztyn [Ź] |
| Adres „Olsztyn, Młodzieżowa 1” wg państwowego rejestru adresów | **53.787124 N, 20.401189 E** | **592 284,78; 658 959,28** | **286201_1.0144.16/1** (obręb 144) | usługa UUG GUGiK [Ź], przeliczenie pyproj [O] |
| AgroCamping wg 3 serwisów kempingowych | 53.7870–53.7872 N, 20.4013–20.4020 E | ok. 592 295–592 340; 658 947–658 965 | 144-16/1 oraz 144-24/1 | campercontact, stellplatz.info, park4night [Ź] |

Odległość między punktem z zadania a adresem wynosi 5 109 m (azymut 302°) [O]. Cały raport dotyczy poprawnego punktu adresowego. Punkt adresowy leży na budynku mieszkalnym („m”) na działce 144-16/1.

---

## A. Działki i planowanie przestrzenne

### A1. Działki w promieniu ok. 500 m od punktu adresowego

Metoda:
- Identyfikatory i geometrię pobrałem z ULDK GUGiK (GetParcelByXY, EPSG:2180) [Ź].
- Powierzchnię obliczyłem z geometrii (współrzędne zaokrąglone do 0,01 m) [O]. To nie jest powierzchnia ewidencyjna. Usługa WMS Olsztyna zwraca puste pole `POLE_EWIDENCYJNE`.
- Użytki i klasy odczytałem z etykiet rastra WMS (warstwy `uzytki`, `kontury_klasyfikacyjne`) [Ź]. Odczyt jest przybliżony. Nie mierzyłem powierzchni konturów.
- Wysokości pochodzą z NMT GUGiK (305 punktów, siatka 50 m i 25 m) [Ź].

**Tabela A1a. Rdzeń (0–130 m od punktu adresowego)**

| Działka (obręb-nr) | Identyfikator | Pow. z geometrii [m²] | Użytki i klasy (odczyt z mapy) | Wys. [m n.p.m.] | Położenie |
|---|---|---|---|---|---|
| 144-16/1 | 286201_1.0144.16/1 | 11 698 | R VI (część główna), Ps VI (zachód), Ls V (pas północny), Br (dom), N, W, Ł V (skrawki) | 106,0–118,5 | Punkt adresowy. Wzgórze między drogą a jeziorem. Narożnik SW 8 m od granicy jeziora |
| 144-24/1 | 286201_1.0144.24/1 | 11 022 | Ps VI, Ps V, R VI, Br (narożnik zachodni) | 106,5–116,3 | Stok S/SE nad brzegiem Ukiela. 230 m granicy z pasem 144-25 |
| 144-19/4 | 286201_1.0144.19/4 | 255 | Bz | 105,3–107,2 | Klin gminny między 16/1 a brzegiem |
| 144-19/3 | 286201_1.0144.19/3 | 1 752 | dr | 113,2–117,4 | Droga gruntowa po granicy 16/1 i 24/1, kierunek NE |
| 144-16/2 | 286201_1.0144.16/2 | 2 535 | dr | 109–112 | Droga wewnętrzna po północnej granicy 16/1 |
| 144-25 | 286201_1.0144.25 | 7 392 | dr | 105,2–108,4 | **Pas brzegowy** o średniej szerokości ok. 6 m. Oddziela działki 19/4, 24/1–24/4 od jeziora. Leży w użytku ekologicznym „Jezioro Zgniłek” |
| 144-6 | 286201_1.0144.6 | 6 734 | dr | 105,5–120,2 | Droga gminna N–S (ul. Młodzieżowa wg położenia [S]). Granica obrębów 143 i 144 |
| 144-14 | 286201_1.0144.14 | 4 869 | Bp, Ps VI, Lzr-Ps VI, Ł V | 105,9–109,3 | Na północ od skrzyżowania dróg 6 i 16/2 |
| 144-16/3 | 286201_1.0144.16/3 | 18 218 | R V, R VI, Ps V, Lzr-Ps V, Ls V, N | 104,8–111,8 | Na północ od 16/2. Część północna to płaskie dno na poziomie jeziora Zgniłek |
| 143-22/1 | 286201_1.0143.22/1 | 4 775 | S-R VI, R V | 107,0–114,5 | Na zachód od drogi 6, stok wschodni |
| 143-22/2 | 286201_1.0143.22/2 | 2 000 | S-R V, Ps V | ok. 107 | Na zachód od drogi 6, przy brzegu |
| 143-23 | 286201_1.0143.23 | 1 105 | dr | ok. 105 | Pas brzegowy po zachodniej stronie drogi 6 |
| 143-21/2 | 286201_1.0143.21/2 | 36 151 | R VI, R V, Ps V, Ps VI, N | 106,5–121,9 | Duża działka rolna na zachód od drogi 6 |
| 143-21/3 | 286201_1.0143.21/3 | 601 | Br | ok. 112,5 | Enklawa z zabudową w 21/2 |
| 143-21/4 | 286201_1.0143.21/4 | 1 690 | Br | ok. 113 | Enklawa z zabudową w 21/2 |

**Tabela A1b. Pozostałe działki do ok. 500 m**

| Działka | Pow. z geometrii [m²] | Użytki (odczyt) | Wys. [m n.p.m.] | Odl. od adresu [m] | Położenie |
|---|---|---|---|---|---|
| 144-15/6 | 3 290 | Ł VI, Lzr-Ps VI | 106–107 | 125 | Pas między drogą 6 a 16/3 |
| 144-15/5 | 3 067 | nie odczytano | ok. 105 | 159 | jw. |
| 144-15/4 | 3 381 | nie odczytano | ok. 109 | 184 | jw. |
| 144-15/3 | 3 733 | nie odczytano | ok. 105 | 209 | jw. |
| 144-15/2 | 3 912 | nie odczytano | 107–115 | 236 | jw. |
| 144-15/1 | 6 024 | nie odczytano | ok. 105 | 154 | Wschodni kraniec pasów 15/x |
| 144-24/2 | 4 135 | R VI, R V | 111–115 | 185 | Na wschód od 24/1, przy pasie 25 |
| 144-24/3 | 4 494 | nie odczytano | 113–115 | 219 | jw. |
| 144-24/4 | 4 794 | nie odczytano | 114–117 | 248 | jw. |
| 144-19/2 | 3 514 | nie odczytano | – | 190 | Droga gminna NE. W użytku ekologicznym |
| 144-17 | 7 165 | nie odczytano | 110–117 | 270 | W użytku ekologicznym |
| 144-23 | 4 129 | nie odczytano | ok. 115 | 273 | W użytku ekologicznym |
| 144-22 | 6 405 | nie odczytano | 117–123 | 307 | W użytku ekologicznym |
| 144-21 | 27 437 | nie odczytano | 107–124 | 349 | W użytku ekologicznym |
| 144-27/1 | 59 072 | Wp | 104,8–107,4 | 211 | **Jezioro Zgniłek**. W użytku ekologicznym |
| 144-12 | 29 413 | nie odczytano | 105–113 | 292 | Na północ. W użytku ekologicznym |
| 144-8 | 30 381 | nie odczytano | 114–119 | 345 | Na północ |
| 144-3168/1 | 30 935 | nie odczytano | 107–120 | 336 | W użytku ekologicznym |
| 144-3168/2 | 32 953 | nie odczytano | 120–123 | 339 | W użytku ekologicznym |
| 144-3168/3 | 9 890 | nie odczytano | 106–111 | 354 | Półwysep na wschodzie. W użytku ekologicznym |
| 143-24 | 29 473 | Ł V, R V (fragment) | 110–125 | 195 | Na NW od drogi 6 |
| 143-26 | 21 028 | nie odczytano | ok. 122 | 386 | Na NW |
| 143-3169 | 266 249 | R VI (fragment) | 111–125 | 204 | Duża działka na zachodzie |
| 145-4 | 342 389 | Ps V, Ps VI, Ls VI | – | 208 | Brzeg na SW. W użytku ekologicznym „Żurawia Dolina” |
| 44-1/23 | nie liczono | Wp | 104,8 (lustro w NMT) | 38 (do granicy) | **Jezioro Ukiel** |
| 45-3254/1 | nie liczono | – | – | ok. 500 | Drugi brzeg jeziora (południe) |

Uwagi:
- Działki 144-27/2, 144-5/1, 144-5/5, 144-5/6 leżą na granicy promienia (500–600 m, NE). Nie pobrałem ich geometrii.
- W zasięgu 500 m **nie znalazłem ul. Porannej**. Ekofizjografia opisuje ul. Poranną jako drogę gruntową wewnątrz obszaru planu Gutkowo-Południe. Jej położenia względem działek nie ustaliłem.
- Prywatne działki 16/1 i 24/1 **nie stykają się z wodą**. Między nimi a jeziorem leży gminny pas 144-25 i klin 144-19/4.
- Pliki robocze w repozytorium: geometria `obliczenia/R1/parcels_raw.txt`, wysokości `obliczenia/R1/elev1.txt` i `obliczenia/R1/elev2.txt`.

### A2. MPZP, studium, plan ogólny

1. **MPZP pod adresem: brak** [Ź]. Usługa „Krajowa Integracja MPZP” (odczyt 11.11.2026) nie pokazuje planu na lądzie wokół adresu. Planem objęty jest akwen jeziora Ukiel (nr 55 w usłudze). Najbliższe plany lądowe leżą ok. 800 m na północ (nr 11, 87, 103). Nazw tych planów nie ustaliłem.
2. **MPZP „otoczenia jeziora Ukiel — rejon Gutkowo-Południe” jest w opracowaniu** [Ź]. Podstawa: uchwała Nr XVIII/320/20 Rady Miasta Olsztyna z 26.02.2020 r. Obszar: ok. 180 ha, od granicy gminy Jonkowo do brzegu Ukiela. Obejmuje odcinek ul. Młodzieżowej z kempingiem. Część A planu (rejon ul. Bałtyckiej i skarpy) miała dyskusję publiczną 25.09.2023 r. Statusu uchwalenia nie ustaliłem. W protokole części A nie ma ustaleń dla rejonu ul. Młodzieżowej.
3. **Studium z 2013 r.** (uchwała Nr XXXVII/660/13 z 15.05.2013 r.) wskazywało strefę O2 „otoczenie jeziora Krzywego”: usługi turystyki, sportu i rekreacji, lasy ochronne, zieleń nieurządzona [Ź]. Studium zastąpił plan ogólny.
4. **Plan ogólny miasta Olsztyna obowiązuje od 3.07.2026 r.** [Ź]. Uchwała nr XXVI/373/26 z 27.05.2026 r., Dz. Urz. Woj. Warm.-Maz. z 18.06.2026 r. poz. 2447. Powierzchnia 8 735,49 ha, 4 946 stref. Udziały: strefa zieleni i rekreacji 38,58%, strefa otwarta 17,5%, strefa z zabudową zagrodową 0,15% (12,92 ha). Obszary uzupełnienia zabudowy (OUZ): 1 487,81 ha.
5. **Strefy planistycznej dla działki 144-16/1 nie ustaliłem.** Przeglądarka `rejestrplanowogolnych.pl` nie odpowiadała z mojego środowiska. Sprawdź strefę (symbol np. SN, SO, SU), profil i przynależność do OUZ pod adresem: https://rejestrplanowogolnych.pl/?teryt=286201_1 albo w MSIPMO.
6. Skutki prawne [S, do potwierdzenia w Wydziale Urbanistyki i Architektury]:
   - Bez MPZP nowa zabudowa wymagająca pozwolenia na budowę wymaga decyzji o warunkach zabudowy (WZ). WZ musi być zgodna z planem ogólnym (strefa, profil, wskaźniki) i z OUZ (art. 61 ust. 1 pkt 1a u.p.z.p.).
   - Art. 61 ust. 4 u.p.z.p. zwalnia zabudowę zagrodową z warunku „dobrego sąsiedztwa”, gdy gospodarstwo przekracza średnią powierzchnię gospodarstwa w gminie. Według opracowania OnGeo z 21.08.2026 r. warunek OUZ nadal obowiązuje. Poselski projekt (druk sejmowy 2883 z 20.07.2026 r.) miał dopuścić WZ dla zabudowy zagrodowej poza OUZ. Statusu projektu nie znam.
   - Obiekty niewymagające pozwolenia na budowę nie wymagają WZ (art. 50 ust. 2 pkt 2 w zw. z art. 59 ust. 1 u.p.z.p.) [S].

### A3. Ochrona przyrody i wód

| Forma | Stan dla działki 144-16/1 | Źródło |
|---|---|---|
| Użytek ekologiczny „Jezioro Zgniłek” | **Sąsiaduje bezpośrednio.** Uchwała Nr VII/96/24 RM Olsztyna z 27.11.2024 r., Dz. Urz. z 10.12.2024 r. poz. 5581, 32,77 ha. Obejmuje działki 144: 3168/1, 3168/2, 3168/3, 21, 22, 23, 25, 19/2, 17, 27/1, 27/2, 5/1, 5/5, 5/6, 12. Działek prywatnych (16/1, 16/3, 14, 15/x, 24/x, 8) nie obejmuje | [Ź] |
| Użytek ekologiczny „Żurawia Dolina” | Ok. 200 m na zachód. Uchwała Nr VI/77/24 z 30.10.2024 r., Dz. Urz. z 12.11.2024 r. poz. 4915, 42,16 ha. Obejmuje m.in. działkę 145-4 | [Ź] |
| Obszar chronionego krajobrazu | Ekofizjografia z 2023 r. podaje: brak powierzchniowych form ochrony na obszarze planu. OChK Doliny Środkowej Łyny leży w sąsiedztwie. Zakaz zabudowy 100 m od brzegu z uchwały o OChK **nie dotyczy** tego terenu, jeżeli granice OChK nie zmieniły się po 2023 r. | [Ź] + [S] |
| Natura 2000, rezerwat, park krajobrazowy | Brak wg ekofizjografii z 2023 r. Serwis GDOŚ odmówił dostępu, więc nie sprawdziłem stanu na 2026 r. | [Ź] |
| GZWP | Cały teren leży nad GZWP nr 205 „Subzbiornik Warmia”. Część NE obszaru planu leży nad GZWP nr 213 „Olsztyn” | [Ź] |
| Tereny osuwiskowe | Dwa tereny zagrożone ruchami masowymi: północne zbocza Ukiela i stoki przy ul. Żurawiej. Nie leżą przy ul. Młodzieżowej wg opisu | [Ź] |
| Zagrożenie powodzią, strefy ochronne ujęć | Nie znalazłem danych | luka |

Zakazy w użytku „Jezioro Zgniłek” (§ 3 uchwały) [Ź]: niszczenie obszaru; prace ziemne trwale zmieniające rzeźbę; zmiana stosunków wodnych (wyjątek: racjonalna gospodarka rolna, leśna, wodna); likwidacja zbiorników i mokradeł; wylewanie gnojowicy (wyjątek: nawożenie użytkowanych gruntów rolnych); zmiana sposobu użytkowania ziemi; wydobywanie torfu; umieszczanie tablic reklamowych. Uchwała zakazuje też gospodarki rybackiej i wędkarstwa na jeziorze Zgniłek.

Wniosek dla projektu: każda instalacja na pasie 144-25 (rura ujęcia z jeziora, pomost, wylot) wymaga zgody gminy i narusza obszar użytku ekologicznego.

---

## B. Teren

### B4. Rzeźba, wysokości, spadki, ekspozycja

Dane: NMT GUGiK (usługa `GetHByPointList`), 305 punktów [Ź]. Spadki i azymuty: różnice centralne na siatce 25 m [O].

**Siatka wysokości 50 m [m n.p.m.]** (kolumny: E 592 000 → 592 700; wiersze: N). Punkt adresowy: E 592 285, N 658 959 → 107,3 m.

| N \ E | 2000 | 2050 | 2100 | 2150 | 2200 | 2250 | 2300 | 2350 | 2400 | 2450 | 2500 | 2550 | 2600 | 2650 | 2700 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 659 400 | 121,0 | 119,1 | 119,4 | 122,4 | 122,1 | 119,2 | 114,1 | 112,6 | 105,4 | 105,1 | 104,8 | 104,9 | 104,9 | 104,9 | 107,2 |
| 659 350 | 124,2 | 123,3 | 120,6 | 122,5 | 120,2 | 113,5 | 110,6 | 110,1 | 105,6 | 105,0 | 104,9 | 104,9 | 104,9 | 106,0 | 106,8 |
| 659 300 | 124,2 | 123,2 | 124,8 | 120,8 | 117,2 | 108,0 | 105,2 | 104,9 | 105,2 | 104,9 | 107,4 | 111,8 | 112,6 | 113,2 | 110,6 |
| 659 250 | 120,4 | 120,4 | 120,8 | 119,4 | 114,6 | 106,9 | 105,1 | 105,0 | 104,9 | 105,0 | 107,5 | 116,4 | 117,5 | 116,9 | 113,4 |
| 659 200 | 110,8 | 112,0 | 111,4 | 112,3 | 108,7 | 105,0 | 105,0 | 105,0 | 104,9 | 105,0 | 110,4 | 116,1 | 119,9 | 120,7 | 119,5 |
| 659 150 | 111,4 | 111,8 | 111,8 | 109,8 | 106,9 | 105,3 | 105,2 | 104,9 | 105,1 | 104,9 | 113,3 | 117,4 | 120,9 | 123,5 | 122,5 |
| 659 100 | 117,6 | 116,2 | 114,8 | 111,5 | 106,6 | 106,0 | 104,9 | 104,8 | 105,0 | 108,2 | 114,8 | 115,4 | 120,6 | 124,0 | 123,4 |
| 659 050 | 124,8 | 119,5 | 113,7 | 111,7 | 106,5 | 106,6 | 112,9 | 116,0 | 115,5 | 114,6 | 114,5 | 116,0 | 120,2 | 122,8 | 120,2 |
| 659 000 | 124,5 | 118,0 | 110,7 | 113,2 | 109,1 | 106,3 | 112,3 | 117,5 | 116,1 | 113,5 | 111,4 | 113,4 | 116,5 | 116,8 | 114,7 |
| 658 950 | 124,4 | 121,8 | 119,1 | 118,1 | 114,8 | 107,0 | 107,8 | 112,0 | 109,8 | 105,1 | 104,8 | 104,8 | 105,2 | 105,6 | 106,6 |
| 658 900 | 124,1 | 121,9 | 121,3 | 120,2 | 114,5 | 107,2 | 104,8 | 104,8 | 104,8 | 104,8 | 104,8 | 104,8 | 104,8 | 104,7 | 106,1 |
| 658 850 | 122,9 | 120,4 | 115,2 | 109,1 | 104,8 | 104,8 | 104,8 | 104,8 | 104,8 | 104,8 | 104,7 | 104,8 | 104,8 | 104,8 | 110,9 |

Opis:
- **Lustro jeziora Ukiel w NMT: 104,8 m n.p.m.** [Ź]. Ekofizjografia z 2023 r. podaje 103 m n.p.m. [Ź]. Źródła różnią się o ok. 1,8 m. Przyczyny nie ustaliłem. Do projektu przyjmij różnice wysokości względem lustra z NMT.
- **Jezioro Zgniłek i jego mokradło: 104,8–105,2 m n.p.m.** Płaskie dno obejmuje północ działki 16/3, wschód pasów 15/x i działkę 27/1. Zgniłek ma rów odpływowy do Ukiela.
- **Działka 16/1 to pagórek.** Szczyt 118,5 m (E 592 360, N 659 025), czyli 13,7 m nad lustrem Ukiela. Dom stoi na 107,3 m, czyli 2,5 m nad lustrem.
- **Spadki na 16/1:** średnio 12,6%, zakres 3–22% (2–12,5°) [O]. Stok zachodni i południowo-zachodni opada do domu i drogi (azymut spadku 205–275°). Stok północny opada do drogi 16/2 i mokradła (azymut 340–13°). Wierzchowina ma spadek 3–4%.
- **Spadki na 24/1:** średnio 13,2%, zakres 5–20% [O]. Ekspozycja S–SE (azymut spadku 133–212°). To najlepiej nasłoneczniony stok w rdzeniu.
- **Działki 143-22/1 i 22/2:** stok wschodni, 10–18% [O]. **Działka 144-14:** prawie płaska, 2–9% [O].
- **Dolina drogi (działka 144-6):** 105–107 m między dwoma wzniesieniami. Wzniesienie zachodnie (143-21/2) sięga 122–125 m.
- Ekofizjografia dla całego obszaru planu [Ź]: średnie rzędne 120–125 m, maksimum 128,9 m, stoki silnie nachylone 10–20° o wysokości względnej 10–20 m.
- Otoczenie [Ź/S]: lasy i zadrzewienia zajmują ok. 30% obszaru planu, grunty orne ok. 25%. Na obszarze planu działa farma PV o powierzchni ok. 1,5 ha. Brak sieci kanalizacji sanitarnej i deszczowej (stan 2023 r.). Zadrzewienia i pokrycia terenu na działkach rdzenia nie odczytałem z ortofotomapy.
- Hałas [Ź]: ul. Bałtycka 66–70 dB (dzień–wieczór–noc). Leży ok. 700–800 m na północ.

### B5. Hydrogeologia

| Parametr | Wartość | Źródło |
|---|---|---|
| Pierwszy użytkowy poziom wodonośny | 15–50 m p.p.t., miąższość 10–20 m (większość obszaru planu); 50–100 m p.p.t. i miąższość > 40 m w części NE | ekofizjografia 2023 [Ź] |
| Zwierciadło wód gruntowych | ≤ 1 m p.p.t. przy zbiornikach i w obniżeniach; głębiej niż 1 m p.p.t. poza nimi | [Ź] |
| GZWP 205 „Subzbiornik Warmia” | paleogeńsko-neogeński, porowy, ujmowany z 150–200 m, 1 660 km², zasoby 60 000 m³/d | [Ź] |
| GZWP 213 „Olsztyn” | czwartorzędowy międzymorenowy, 20–50 m, 1 383 km² | [Ź] |
| Stopień zagrożenia głównego poziomu | wysoki (MhP 1:50 000) | [Ź] |
| Podłoże | piaski i żwiry wodnolodowcowe, piaski, żwiry i głazy moren martwego lodu, torfy w obniżeniach | [Ź] |
| Jakość wód (Fe, Mn, twardość), typowe głębokości studni | **nie znalazłem danych** dla Gutkowa. Objaśnienia MhP ark. Olsztyn (0175) były niedostępne | luka |

Ocena [S]: w dolinie drogi i na dnie przy Zgniłku studnia kopana lub wąskośrednicowa trafi na wodę płytko (1–3 m). Ta woda ma kontakt z jeziorem i mokradłem. Na wodę pitną planuj studnię wierconą do poziomu 15–50 m i analizę żelaza, manganu oraz bakteriologii.

---

## C. Klimat (stacja IMGW Olsztyn, kod 12272)

### C8. Tabela miesięczna — normy 1991–2020

| Miesiąc | T śr. [°C] | T maks. śr. [°C] | T min. śr. [°C] | Opad [mm] | Dni z opadem ≥ 0,1 mm | Dni z pokrywą śnieżną | Wilgotność [%] |
|---|---|---|---|---|---|---|---|
| I | −2,0 | 0,4 | −4,4 | 42,1 | 17,4 | 18,4 | 88,2 |
| II | −1,1 | 1,8 | −3,8 | 33,1 | 15,0 | 17,6 | 85,0 |
| III | 2,2 | 6,2 | −1,5 | 39,4 | 14,1 | 9,6 | 77,6 |
| IV | 7,9 | 13,3 | 2,6 | 37,5 | 12,4 | 1,3 | 69,9 |
| V | 12,9 | 18,6 | 7,1 | 59,8 | 13,5 | 0,0 | 70,4 |
| VI | 16,1 | 21,7 | 10,7 | 70,1 | 14,3 | 0,0 | 72,6 |
| VII | 18,3 | 23,8 | 13,2 | 88,0 | 14,4 | 0,0 | 74,7 |
| VIII | 17,8 | 23,4 | 12,7 | 63,8 | 13,3 | 0,0 | 75,3 |
| IX | 13,2 | 18,1 | 8,9 | 58,5 | 13,0 | 0,0 | 80,7 |
| X | 8,0 | 11,8 | 4,8 | 57,7 | 14,1 | 0,5 | 84,7 |
| XI | 3,3 | 5,5 | 1,2 | 47,0 | 15,6 | 4,1 | 89,7 |
| XII | −0,4 | 1,7 | −2,6 | 45,4 | 17,6 | 12,5 | 89,8 |
| **Rok** | **8,0** | **12,2** | **4,1** | **642,4** | **174,8** | **64,0** | **79,9** |

Źródła: temperatury, opad i dni z pokrywą śnieżną — portal IMGW „Normy klimatyczne 1991–2020” [Ź]. Dni z opadem i wilgotność — tabela Wikipedii z przypisami do IMGW i meteomodel.pl [Ź].

Dodatkowo:
- Rekordy (1951–obecnie): maksimum 36,2 °C, minimum −30,6 °C [Ź, Wikipedia/meteomodel].
- **Usłonecznienie: IMGW nie publikuje normy 1991–2020 dla Olsztyna (wartość „NA”)** [Ź].
- **Napromieniowanie: nie pobrałem** (API PVGIS zablokowane dla mojego narzędzia). Wartość orientacyjna dla Olsztyna: ok. 1 000–1 050 kWh/m² na rok na płaszczyznę poziomą [S].
- Opad w sezonie IV–IX: 377,7 mm; V–VIII: 281,7 mm (1991–2020) [O z norm IMGW].
- Średnia prędkość wiatru: 2,9 m/s; maksimum w lutym 3,3 m/s; minimum w sierpniu 2,3 m/s (ekofizjografia, okres niepodany) [Ź].
- Ekofizjografia [Ź]: rok 2016 — 700–750 mm; rok 2017 — 950–1 000 mm.

### C6. Okresy termiczne

Nie znalazłem publikowanych dat dla stacji Olsztyn za 1991–2020. Podaję własne obliczenie i tło z literatury.

Metoda [O]: interpolacja liniowa między średnimi miesięcznymi 1991–2020 przypisanymi do środka miesiąca. Wzór: `dzień_progu = dzień_środka_miesiąca_1 + (T_progu − T_1) / (T_2 − T_1) × (liczba dni między środkami miesięcy)`.

| Okres | Próg śr. dobowej | Początek | Koniec | Długość [dni] |
|---|---|---|---|---|
| Gospodarczy | 3 °C | 20 marca | 18 listopada | 243 |
| Wegetacyjny | 5 °C | 31 marca | 4 listopada | 218 |
| Aktywnego wzrostu | 10 °C | 28 kwietnia | 4 października | 159 |
| Termiczne lato | 15 °C | 5 czerwca | 4 września | 91 |

Tło z literatury:
- Polska, 48 stacji, próg 5 °C: 1971–2000 → 31.03–04.11, 218 dni; 2001–2009 → 29.03–10.11, 226 dni (Nieróbca i in. 2013) [Ź]. W tym opracowaniu Polska północno-wschodnia miała w latach 1971–2000 poniżej 200 dni (Suwałki 197 dni).
- Ekofizjografia Olsztyna podaje ok. 200 dni [Ź].
- Trend: wydłużenie o ok. 8 dni między 1971–2000 a 2001–2009 w skali kraju; na wschodzie kraju do 6 dni [Ź].

Wniosek: przyjmij 205–218 dni dla progu 5 °C. Dolną wartość stosuj do zimnych zagłębień, górną do stoku 24/1.

### C7. Przymrozki

Stacja Olsztyn, lata 1971–2000 (Dragańska, Rynkiewicz, Panfil 2004, Acta Agrophysica 3(1)) [Ź]:

| Wskaźnik | 200 cm nad gruntem | 5 cm nad gruntem |
|---|---|---|
| Średnia data ostatniego przymrozku wiosennego | 4 maja | 24 maja |
| Średnia data pierwszego przymrozku jesiennego | 9 października | 20 września |
| Średni okres bezprzymrozkowy [dni] | 157 | 118 |
| Średnia liczba dni z przymrozkiem: IV / V / VI | 9 / 2 / 0 | 15 / 5 / 1 |
| Średnia liczba dni z przymrozkiem: IX / X | 1 / 4 | 3 / 9 |

- Daty skrajne dla Olsztyna: publikacja ich nie podaje. W regionie: najpóźniejszy przymrozek przy gruncie 24.06.1995 (Suwałki); najwcześniejszy jesienny 15.09.1973 (Suwałki, Gołdap) [Ź].
- Rekord minimum w maju w Olsztynie: −4,8 °C; w czerwcu −0,5 °C; we wrześniu −4,2 °C (1951–obecnie) [Ź].
- Nowszych dat (1991–2020) nie znalazłem.

Efekt lokalny [S, na podstawie rzeźby z B4 i uwag ekofizjografii]:
- Zimne powietrze spływa do doliny drogi (105–107 m) i na dno przy Zgniłku (105 m). Tam ryzyko przymrozku przygruntowego jest największe. Ekofizjografia potwierdza zastoiska chłodu i mgły w obniżeniach i przy wodzie.
- Stok S–SE działki 24/1 i wierzchowina 16/1 (113–118 m) są najmniej narażone.
- Jezioro Ukiel (412 ha [S]) łagodzi jesienne spadki temperatury w pasie przybrzeżnym. Wiosną opóźnia nagrzewanie.
- Do sadzenia roślin wrażliwych przyjmij termin po 25 maja w zagłębieniach i po 15 maja na stoku.

### Klimatyczny bilans wodny i susza rolnicza

- Wartości KBW dla Olsztyna nie pobrałem. Strona IMGW pokazuje tylko wybór miesiąca. Szacunek [S]: KBW IV–IX = 377,7 mm − ewapotranspiracja potencjalna ok. 500–550 mm ≈ −120 do −170 mm.
- IUNG SMSR, zboża ozime, woj. warmińsko-mazurskie [Ź]: susza wystąpiła w latach 2006, 2007, 2008, 2009, 2011 (łącznie 13 okresów sześciodekadowych); w latach 2012–2017 nie wystąpiła. Udział gmin z suszą: 2006 — 75,0%; 2008 — 72,4%.
- Gleby klas V–VI z piasków to kategoria I (bardzo lekka), najbardziej podatna na suszę [S]. Zaplanuj nawadnianie warzywnika.

### C9. Parametry projektowe

| Parametr | Wartość | Status |
|---|---|---|
| Strefa klimatyczna PN-EN 12831 | IV; temperatura projektowa −22 °C; średnia roczna 6,9 °C | [S] — nie potwierdziłem dziś w źródle |
| Stopniodni grzania, baza 20 °C, miesiące X–IV (212 dni) | 3 698 K·d; wzór: `Sd = Σ (20 − T_śr,m) × liczba dni miesiąca`; dane: normy IMGW 1991–2020 | [O] |
| Stopniodni, baza 20 °C, miesiące IX–V | 4 122 K·d | [O] |
| Głębokość przemarzania PN-81/B-03020 | 1,0 m p.p.t. wg ekofizjografii Olsztyna. Blog OnGeo podaje dla regionu 1,2–1,4 m. Do fundamentów przyjmij wartość z opinii geotechnicznej | [Ź], źródła sprzeczne |
| Strefa obciążenia śniegiem PN-EN 1991-1-3 | 4; s_k = 1,6 kN/m² | [Ź, OnGeo] |
| Strefa obciążenia wiatrem PN-EN 1991-1-4 | 1; v_b,0 = 22 m/s | [S] |
| Strefa mrozoodporności USDA | 6a–6b. Nie znalazłem mapy z okresem 1991–2020 | [S] |
| Średnia prędkość wiatru | 2,9 m/s (okres niepodany) | [Ź] |

---

## D. Gleba

- **Klasy bonitacyjne na działkach rdzenia: wyłącznie V i VI** (R V, R VI, Ps V, Ps VI, Ł V, Ł VI, Ls V) [Ź, mapa ewidencyjna WMS]. Działka 16/1: głównie R VI i Ps VI.
- **Typ gleby:** brunatne właściwe z piasków słabo gliniastych, lokalnie z gliny lekkiej. W zagłębieniach i przy zbiornikach torfy niskie [Ź, ekofizjografia].
- **Kompleksy przydatności rolniczej:** 6 (żytni słaby) i 7 (żytni bardzo słaby). Lokalnie klasa IV i kompleks 3 [Ź].
- **Struktura użytkowania obszaru planu:** lasy i zadrzewienia ok. 30%, grunty orne R V–R VI ok. 25%, pastwiska Ps V, łąki, nieużytki [Ź].
- **Odczyn i zasobność:** nie znalazłem danych OSChR dla Gutkowa. Dla takich gleb typowy jest odczyn kwaśny (pH w KCl ok. 4,5–5,5) i niska zawartość próchnicy, potasu i magnezu [S].
- **Ograniczenia [S]:** mała retencja wody, szybkie wymywanie azotu i potasu, podatność na suszę, erozja wodna na stokach 10–22%, zakwaszenie. Na dnie przy Zgniłku: podtopienia i torf.
- **Zalecenie:** zleć w OSChR Olsztyn analizę pH, P, K, Mg i próchnicy osobno dla stoku 24/1, wierzchowiny 16/1 i doliny. Zaplanuj wapnowanie, kompost i ściółkowanie na podstawie wyniku.

---

## E. Prawo

### E11. Zwierzęta gospodarskie w granicach Olsztyna

- Akt: **uchwała Nr XVI/231/25 Rady Miasta Olsztyna z 27.08.2025 r.** — Regulamin utrzymania czystości i porządku na terenie Gminy Olsztyn. Dz. Urz. Woj. Warm.-Maz. 2025 poz. 3868. Obowiązuje od 1.01.2026 r. Uchyla uchwałę Nr L/805/22 z 26.08.2022 r. [Ź]
- § 13: zakaz utrzymywania zwierząt gospodarskich dotyczy nieruchomości, które **nie wchodzą w skład gospodarstw rolnych** ani placówek naukowo-badawczych. Wyjątek od zakazu: pszczoły i króliki. **Gospodarstwo rolne jest poza zakazem.** Regulamin nie wymienia drobiu osobno.
- § 14 (dotyczy terenów objętych zakazem): ule min. 15 m od granicy i 30 m od budynków sąsiada; do 15 królików na działce jednorodzinnej ≥ 1 000 m².
- § 15–16: utrzymywanie zwierząt nie może powodować zagrożenia sanitarnego. Odpady z chowu usuwaj systematycznie.
- § 10: zbiornik bezodpływowy opróżniaj co najmniej raz na 3 miesiące. Osad z przydomowej oczyszczalni usuwaj co najmniej raz na rok.
- § 9 ust. 6: w kompostowniku wolno kompostować tylko odpady zielone, bez odpadów pochodzenia zwierzęcego.

### E12. Drób: rejestracja, sprzedaż, bioasekuracja, HPAI

Akty obowiązujące od 18.03.2026 r. [Ź]:
- Ustawa z 21.11.2025 r. o zdrowiu zwierząt (Dz.U. 2025 poz. 1795).
- Rozporządzenie MRiRW z 11.03.2026 r. w sprawie środków zwalczania chorób u drobiu (Dz.U. 2026 poz. 335). Zastąpiło rozporządzenie „HPAI” z 31.03.2022 r. i rozporządzenie o rzekomym pomorze drobiu z 25.04.2025 r.
- Rozporządzenie MRiRW z 5.03.2026 r. o kategoriach zakładów zwolnionych z rejestracji (Dz.U. 2026 poz. 292).

| Obowiązek | Drób tylko na własne potrzeby | Sprzedaż jaj lub mięsa (stado do 100 szt.) |
|---|---|---|
| Zgłoszenie miejsca utrzymywania drobiu do Powiatowego Lekarza Weterynarii (PLW) | **Tak** — § 3 ust. 1 pkt 2 lit. b rozp. poz. 335 | Tak |
| Rejestracja zakładu i numer WNI u PLW | Nie, jeżeli zakład spełnia warunki art. 3 ust. 1 rozp. (UE) 2022/1345: brak kopytnych, brak przemieszczeń zwierząt i produktów poza zakład (§ 1 rozp. poz. 292) | **Tak** — art. 55 i 57 ustawy; PLW nadaje WNI decyzją (30 dni wg materiału KPODR) |
| Wpis w IRZplus (ARiMR) | Nie (stanowisko ARiMR) | Tak — po decyzji o WNI uzupełnij dane w IRZplus |
| Rejestracja działalności „sprzedaż bezpośrednia” albo RHD u PLW | Nie | Tak; RHD: wniosek 30 dni przed startem |
| Szczepienie kur przeciw rzekomemu pomorowi | Brak obowiązku w tekście dla stad bez przemieszczeń | **Tak** — § 4 w zw. z § 3 ust. 3; stado do 350 szt.: wg charakterystyki szczepionki |
| Maty dezynfekcyjne, odzież ochronna, dokumentacja padnięć i odkażania, zapas środka na 7 dni | Nie | **Tak** — § 3 ust. 3 (zakład sprzedający bezpośrednio) |
| Plan bioasekuracji | Nie | Nie (dopiero powyżej 350 szt. średniorocznie — § 3 ust. 4) |

Nakazy i zakazy dla **każdego** stada (§ 3 ust. 1 rozp. poz. 335) [Ź]:
1. Nie pój drobiu wodą ze zbiorników dostępnych dla dzikich ptaków. **To wyklucza wodę z jeziora Ukiel bez uzdatnienia.**
2. Utrzymuj drób bez dostępu do zbiorników dostępnych dla dzikich ptaków. **Wybieg nie może sięgać brzegu ani mokradła.**
3. Utrzymuj drób w izolacji od dzikich ptaków. Wyjątki: kaczki, gęsi, kury w systemie wolnowybiegowym, kurczęta ras wolnorosnących.
4. Karm i pój drób (poza gęsiami) w miejscu zamkniętym lub osłoniętym.
5. Przechowuj paszę i ściółkę bez dostępu gryzoni, zwierząt domowych i dzikich ptaków.
6. Umieść gniazda wewnątrz budynku.
7. Przeglądaj stado codziennie i zapisuj objawy.
8. Zgłoś niezwłocznie PLW: zwiększoną śmiertelność, spadek pobierania paszy i wody, objawy nerwowe, duszność, sinicę, biegunkę, nagły spadek nieśności.

Sprzedaż bezpośrednia — rozporządzenie MRiRW z 30.09.2015 r. (Dz.U. 2015 poz. 1703) [Ź]:
- Jaja: do 2 450 szt. na tydzień (127 400 szt. na rok za zgodą PLW). Dostarcz jaja konsumentowi do 21 dni od zniesienia.
- Tuszki drobiu innego niż indyki i gęsi: do 200 szt. na tydzień; ubój w gospodarstwie przy produkcji do 10 000 szt. na rok. Indyki: 50 szt. na tydzień. Gęsi: 500 szt. na tydzień.
- Obszar: województwo produkcji i województwa sąsiednie. Chłodzenie tuszek do 4 °C.

Rolniczy handel detaliczny (RHD) [Ź, GIW]: sprzedaż konsumentom końcowym bez limitu ilości; limity dotyczą dostaw do sklepów i restauracji (rozp. MRiRW z 12.09.2022 r., Dz.U. 2022 poz. 1971 — wartości nie pobrałem); zwolnienie z PIT do 100 000 zł przychodu na rok.

Znakowanie jaj [S]: producent do 50 niosek może sprzedawać jaja bez stempla na targu lokalnym, gdy poda w punkcie sprzedaży swoje dane.

HPAI w woj. warmińsko-mazurskim:
- Wrzesień 2025 r.: ognisko w województwie; Polska straciła status kraju wolnego od HPAI. W 2025 r. do 3.11 — 100 ognisk w kraju [Ź].
- 20.02.2026 r.: rozporządzenie Nr 10 Wojewody Warmińsko-Mazurskiego wprowadziło zasady utrzymywania drobiu na wyznaczonym obszarze. Rozporządzenie Nr 39 z 19.06.2026 r. (Dz. Urz. poz. 2466) uchyliło je. Ostatnie ognisko HPAI na tym obszarze wyznaczono 13.05.2026 r. [Ź]. Zasięgu obszaru (czy obejmował Olsztyn) nie ustaliłem.
- **Sezon 2026/2027: nie ustaliłem bieżącej listy ognisk ani stref.** Decyzja wykonawcza Komisji (UE) 2026/2483 z 30.10.2026 r. zmieniła wykaz stref w UE. Sprawdź mapę GIW (https://bip.wetgiw.gov.pl/ai/mapa/) i komunikaty PIW Olsztyn przed zasiedleniem kurnika.
- PLW i wojewoda mogą rozporządzeniem nakazać utrzymywanie drobiu w określony sposób, w tym w zamknięciu (art. 27 i 28 ustawy). Zaprojektuj kurnik z zadaszonym, osiatkowanym wybiegiem.

### E13. Prawo budowlane dla rolnika

Podstawa: art. 29 ustawy — Prawo budowlane w brzmieniu z serwisu arslege.pl (stan 2026, serwis nie podaje daty) [Ź]. Nowelizacja z grudnia 2025 r. wprowadziła progi magazynów energii [Ź].

| Obiekt | Bez pozwolenia i bez zgłoszenia | Zgłoszenie | Pozwolenie |
|---|---|---|---|
| Kurnik, budynek gospodarczy, wiata w gospodarstwie | Parterowy budynek gospodarczy do 35 m², rozpiętość do 4,80 m, na działce siedliskowej (ust. 2 pkt 1 lit. a). Jednokondygnacyjny budynek gospodarczy lub wiata **związane z produkcją rolną** do 150 m², rozpiętość do 6 m, wysokość do 7 m (ust. 2 pkt 33) | Do 300 m², rozpiętość i wysokość do 7 m, obszar oddziaływania w granicach działki (ust. 1 pkt 32) | Większe |
| Szklarnia, tunel foliowy | Art. 29 ich nie wymienia. Przydomowa oranżeria do 35 m² — zgłoszenie (ust. 1 pkt 15) | — | Kwalifikacja sporna. Zapytaj organ |
| Piwnica ziemna (ziemianka) | Art. 29 jej nie wymienia. Kwalifikacja jako „budynek gospodarczy do 35 m²” jest możliwa [S] | — | Zapytaj organ |
| Zbiornik bezodpływowy na deszczówkę | Do 5 m³ (ust. 2 pkt 1 lit. c, pkt 36) | > 5 do 15 m³ (ust. 1 pkt 38); w gospodarstwie rolnym > 5 do 30 m³ (ust. 1 pkt 29 lit. e) | Większe |
| Staw na gruncie rolnym, głębokość do 3 m | Do 1 000 m² (ust. 2 pkt 32) | > 1 000 do 5 000 m² (ust. 1 pkt 31) | Większe. Dodatkowo zgłoszenie wodnoprawne [S] |
| Płyta obornikowa, szczelny zbiornik na gnojówkę, silos na kiszonkę | — | Tak (ust. 1 pkt 29 lit. a, b, d) | — |
| Silos naziemny na materiały sypkie | — | Do 250 m³ i 15 m wysokości (ust. 1 pkt 29 lit. c) | Większy |
| Przydomowa oczyszczalnia ścieków | — | Do 7,50 m³/d (ust. 1 pkt 5) | Większa |
| Zbiornik bezodpływowy na ścieki | — | Do 10 m³ (ust. 1 pkt 6) | Większy |
| Instalacja PV | Do 150 kW (ust. 4 pkt 3c). Powyżej 6,5 kW: uzgodnienie z rzeczoznawcą ppoż. i zawiadomienie PSP | — | > 150 kW |
| Pompa ciepła, kolektory wolno stojące | Tak (ust. 4 pkt 3c) | — | — |
| Magazyn energii elektrycznej | Do 30 kWh (ust. 2 pkt 39; ust. 4 pkt 3c) | > 30 do 300 kWh z uzgodnieniem ppoż. (ust. 1 pkt 40); wolno stojący > 300 do 2 000 kWh (ust. 1 pkt 3c) | > 2 000 kWh |
| Mała turbina wiatrowa (moc mikroinstalacji, do 50 kW) | Wysokość całkowita z masztem do 3 m (ust. 4 pkt 3f) | > 3 m do 12 m (ust. 3 pkt 3g) | > 12 m |
| Ogrodzenie | Do 2,20 m | > 2,20 m | — |
| Obiekt tymczasowy niepołączony trwale z gruntem | — | Do 180 dni (ust. 1 pkt 7) | Dłużej |

Zastrzeżenia:
- **Kurnik to budynek inwentarski.** Przepisy o zwolnieniach mówią o „budynkach gospodarczych związanych z produkcją rolną”. Organy różnie kwalifikują kurniki [S]. Uzyskaj stanowisko Wydziału Urbanistyki i Architektury przed budową. Kurnik mobilny na kołach nie jest obiektem budowlanym [S].
- Zwolnienia nie działają, gdy przedsięwzięcie wymaga oceny oddziaływania na środowisko (art. 29 ust. 6).

**Warunki techniczne — stan przejściowy** [Ź]:
- Rozporządzenie z 12.04.2002 r. (budynki i ich usytuowanie) wygasło 20.09.2026 r. Do 28.09.2026 r. minister nie ogłosił nowego rozporządzenia. Czy ogłosił je do 11.11.2026 r. — nie ustaliłem.
- Ustawa z 31.07.2026 r. (Dz.U. 2026 poz. 1161) dodała art. 102a Prawa budowlanego. Przez 18 miesięcy od 20.09.2026 r. inwestor może projektować według dotychczasowych warunków technicznych, po złożeniu oświadczenia.

Odległości:
- Budynek od granicy działki: 4 m dla ściany z oknami lub drzwiami, 3 m dla ściany bez otworów (§ 12 dotychczasowych WT) [S]. WT nie określają odrębnej odległości budynku inwentarskiego od budynku mieszkalnego [S].
- Budowle rolnicze — rozporządzenie MRiGŻ z 7.10.1997 r. (Dz.U. 1997 nr 132 poz. 877; tekst jednolity Dz.U. 2014 poz. 81 — zmian nie porównałem) [Ź]:

| Budowla | Od okien i drzwi pomieszczeń na pobyt ludzi na działkach sąsiednich | Od granicy działki sąsiedniej | Inne |
|---|---|---|---|
| Zamknięty zbiornik na płynne odchody (§ 6 ust. 3) | 15 m | 4 m | 15 m od magazynów żywności; 5 m od silosów |
| Otwarty zbiornik do 200 m³ i płyta obornikowa (§ 6 ust. 4) | 30 m | 4 m | 50 m od magazynów żywności i przetwórni; 10 m od magazynów pasz i silosów na kiszonki |
| Komora fermentacyjna i zbiornik biogazu do 100 m³ (§ 7) | 15 m (także od budynków inwentarskich) | 5 m | 8 m od innych budynków |

### E14. Woda i ścieki

Studnia własna:
- Zwykłe korzystanie z wód (art. 33 Prawa wodnego): pobór wód podziemnych do **5 m³ na dobę średniorocznie** na potrzeby własnego gospodarstwa domowego lub rolnego [Ź, Wody Polskie 21.07.2026].
- Studnia do **30 m głębokości** na potrzeby zwykłego korzystania nie wymaga pozwolenia ani zgłoszenia wodnoprawnego. Studnia głębsza niż 30 m wymaga pozwolenia wodnoprawnego [Ź].
- Pobór na cele inne niż zwykłe korzystanie to usługa wodna i wymaga pozwolenia wodnoprawnego niezależnie od głębokości (art. 35 i art. 389 pkt 1) [Ź].
- Poziom użytkowy leży tu na 15–50 m. Studnia do tego poziomu może przekroczyć 30 m i wtedy wymaga pozwolenia.

Odległości studni wody pitnej (§ 31 dotychczasowych WT, liczone od osi studni) [Ź]:

| Od czego | Minimalna odległość |
|---|---|
| Granica działki | 5 m (mniej dla studni wspólnej na granicy) |
| Oś rowu przydrożnego | 7,5 m |
| Budynki inwentarskie, szczelne silosy, zbiorniki na nieczystości, kompost | 15 m |
| Przewód rozsączający kanalizacji indywidualnej po biologicznym oczyszczeniu | 30 m |
| Nieutwardzone wybiegi dla zwierząt, drenaż bez oczyszczania biologicznego, pole filtracyjne | 70 m |

**Wybieg dla 100 kur musi leżeć min. 70 m od studni wody pitnej, jeżeli jest nieutwardzony.**

Pobór wody z jeziora Ukiel do podlewania [S — treść art. 32, 34, 35 Prawa wodnego z mojej wiedzy, dziś niepobrana]:
- Powszechne korzystanie z wód publicznych obejmuje potrzeby gospodarstwa domowego i rolnego **bez specjalnych urządzeń technicznych**. Wiadro tak, pompa i rurociąg nie.
- Pobór pompą to usługa wodna. Wymaga pozwolenia wodnoprawnego i opłat za usługi wodne.
- Dodatkowe przeszkody: rura przechodzi przez gminny pas 144-25 w użytku ekologicznym (zakaz prac ziemnych i zmiany stosunków wodnych). Stan JCWP Jezioro Ukiel jest niezadowalający [Ź].
- Rekomendacja: do podlewania użyj deszczówki i studni. Nie planuj ujęcia z jeziora.

Przydomowa oczyszczalnia ścieków (POŚ):
- Teren leży w aglomeracji Olsztyn (uchwała Nr XXX/508/21 z 27.01.2021 r.) [Ź]. W rejonie brakowało kanalizacji sanitarnej (stan 2023 r.) [Ź].
- Budowa POŚ do 7,50 m³/d: zgłoszenie (art. 29 ust. 1 pkt 5 Prawa budowlanego) [Ź].
- Przyłączenie do sieci jest obowiązkowe, gdy sieć istnieje, chyba że nieruchomość ma POŚ spełniającą wymagania (art. 5 ust. 1 pkt 2 ustawy o utrzymaniu czystości i porządku w gminach) [S].
- W aglomeracji ścieki z POŚ odprowadzane do ziemi muszą spełniać wymagania jak dla oczyszczalni 2 000–9 999 RLM. Miejsce wprowadzania musi leżeć min. 1,5 m nad zwierciadłem wód podziemnych (rozp. z 12.07.2019 r., Dz.U. 2019 poz. 1311, § 11) [S — sprawdź tekst]. **W dolinie i przy Zgniłku zwierciadło leży ≤ 1 m p.p.t. Drenaż rozsączający tam nie spełni warunku.**
- Eksploatację POŚ do 5 m³/d zgłoś w urzędzie miasta [S]. Osad wywoź min. raz na rok (regulamin § 10) [Ź].

### E15. Dotacje 2026–2027

| Program | Status na 11.11.2026 | Kwoty i warunki | Źródło |
|---|---|---|---|
| ARiMR I.10.2 „Inwestycje w gospodarstwach rolnych w zakresie OZE i poprawy efektywności energetycznej” | **Nabór 5.10–3.11.2026 zakończony.** Kolejny termin nieznany | Budżet 424,3 mln zł. Obszar B: PV do 50 kW z magazynem energii, pompy ciepła, magazyny ciepła, systemy zarządzania energią — do 200 tys. zł. Obszar C (ograniczenie zużycia energii w budynkach gospodarstwa) — do 200 tys. zł. B+C do 400 tys. zł. Intensywność 65%. Wymagane szkolenie z efektywności energetycznej | harmonogram ARiMR; Gramwzielone 2.10.2026 [Ź] |
| ARiMR I.10.5 „Rozwój małych gospodarstw” | Ostatni nabór: 1.10–28.11.2025. **W harmonogramie 2026 (wersja po 21.09.2026) naboru nie ma.** Termin kolejnego nieznany | Premia 100 tys. zł; 120 tys. zł dla gospodarstw ekologicznych i krótkich łańcuchów dostaw. Wielkość ekonomiczna do 25 tys. euro; przychód ze sprzedaży min. 5 tys. zł; wzrost sprzedaży o min. 30% i do min. 43 200 zł | ARiMR 3.11.2025 [Ź] |
| ARiMR I.6.2 „Modernizacja gospodarstw pasiecznych” | Nabór 23.10–27.11.2026 (otwarty) | Budżet 22,41 mln zł | harmonogram ARiMR [Ź] |
| NFOŚiGW „Energia dla Wsi”, 3. nabór | Start 1.10.2026; **budżet 400 mln zł wyczerpany 2.10.2026** | Rolnik: PV i wiatr > 50 kW do 1 MW (pożyczka do 100%); biogaz i woda > 10 kW do 1 MW (dotacja do 65%); magazyn energii przy źródle (dotacja do 20%). Za duża skala dla tego projektu | Gramwzielone 2.10.2026 [Ź] |
| NFOŚiGW „Mój Prąd” | Edycja 6.0 zakończona 12.09.2025. **Edycji 7.0 nie będzie** w dotychczasowej formule | — | GLOBEnergia 10.03.2026 [Ź] |
| NFOŚiGW „Przydomowe magazyny energii”, część 1 (KPO) | Tylko inwestycje zakończone w okresie 1.08.2024–31.10.2025 | Do 28 tys. zł łącznie; magazyn energii do 16 tys. zł; magazyn ciepła do 5 tys. zł | program priorytetowy z 17.04.2026 [Ź] |
| NFOŚiGW „Przydomowe magazyny energii”, część 2 (Fundusz Modernizacyjny) | **Zapowiedziany na IV kw. 2026.** Zasad nie opublikowano w źródłach, które znalazłem | Budżet 1 mld zł; osoby fizyczne | Gramwzielone 17.09.2026 [Ź] |
| WFOŚiGW „Mikroretencja” (następca „Mojej Wody”) | Wnioski od 22.06.2026. Stanu budżetu w WFOŚiGW Olsztyn nie sprawdziłem | Do 8 000 zł; zbiorniki od 2 m³ łącznie, pompy, nawadnianie; koszty od 1.07.2024; inwestycja zakończona. **Wyklucza instalacje służące działalności rolniczej lub gospodarczej** | Murator 2.06.2026 [Ź] |
| „Czyste Powietrze” | Nie sprawdziłem bieżących zasad | — | luka |

---

## F. Źródła

Działki, mapy, teren:
- ULDK GUGiK: https://uldk.gugik.gov.pl/?request=GetParcelByXY&xy=592329,659010&result=teryt,parcel,geom_extent,geom_wkt
- Usługa adresowa UUG GUGiK: https://services.gugik.gov.pl/uug/?request=GetAddress&address=Olsztyn,%20Młodzieżowa%201
- WMS EGiB Urzędu Miasta Olsztyna: https://webewidwms.olsztyn.eu/iip/ows
- Krajowa Integracja Ewidencji Gruntów: https://integracja.gugik.gov.pl/cgi-bin/KrajowaIntegracjaEwidencjiGruntow
- NMT GUGiK: https://services.gugik.gov.pl/nmt/?request=GetHByPointList&list=658959%20592285
- Krajowa Integracja MPZP: https://mapy.geoportal.gov.pl/wss/ext/KrajowaIntegracjaMiejscowychPlanowZagospodarowaniaPrzestrzennego
- Serwisy kempingowe: https://www.campercontact.com/en/poland/warmian-masurian-voivodeship/olsztyn/70638/agro-camping-olsztyn ; https://stellplatz.info/en/rv-park/agro-camping-olsztyn-allenstein ; https://park4night.com/en/place/97678

Planowanie i ochrona przyrody:
- Ekofizjografia Gutkowo-Południe (2023): https://olsztyn.eu/fileadmin/katalogi_wydzialowe/gospodarka/planowanie/Gutkowo_poludnie/Ekofizjografia_Gutkowo_tekst.pdf
- Protokół dyskusji publicznej, część A: https://olsztyn.eu/fileadmin/katalogi_wydzialowe/gospodarka/planowanie/Gutkowo_poludnie/Protokol_z_dyskusji_publicznej_Gutkowo_Pld_A.pdf
- Plan ogólny Olsztyna — metryka: https://e-mapa.net/plan_ogolny/286201-olsztyn ; akt: https://edzienniki.olsztyn.uw.gov.pl/legalact/2026/2447 ; mapa: https://rejestrplanowogolnych.pl/?teryt=286201_1
- Autopoprawka do planu ogólnego: https://bip.olsztyn.eu/attachment/informacja/23550/9cdf432accb41b0d0cc2ca1e38b5a9a77611dba4.html
- Użytek ekologiczny „Jezioro Zgniłek”: https://edzienniki.olsztyn.uw.gov.pl/eli/POL_WOJ_WM/2024/5581/ogl/pol/pdf
- Użytek ekologiczny „Żurawia Dolina”: https://www.inforlex.pl/download/akty_pdf,U82,2024,317,4915.pdf
- Zabudowa zagrodowa a plan ogólny (OnGeo, 21.08.2026): https://blog.ongeo.pl/zabudowa-zagrodowa-plan-ogolny-nowelizacja-bilansowanie

Klimat:
- IMGW normy 1991–2020: https://klimat.imgw.pl/pl/climate-normals/TSR_AVE ; /TMAX_AVE ; /TMIN_AVE ; /OPAD_SUMA ; /SNIEG_0 ; /USL
- Tabela klimatu Olsztyna: https://en.wikipedia.org/wiki/Olsztyn
- Przymrozki 1971–2000 (Dragańska i in. 2004): https://agro.icm.edu.pl/agro/element/bwmeta1.element.agro-article-84600007-6ae0-4ed5-b644-406a4a557084/c/Frost_frequency_and.pdf
- Okres wegetacyjny (Nieróbca i in. 2013): https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-4fd7597c-d26e-49d2-824c-a5788eaa9f9d/c/Nierobca_i_in.pdf
- Susza rolnicza 2006–2017 (Wójcik i in. 2018): https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-86b17aa1-121d-445e-97c6-7d8763de8add/c/Wojcik_i_in.pdf
- Strefy śniegowe i przemarzanie (OnGeo): https://www.blog.ongeo.pl/strefa-sniegowa-wiatrowa-przemarzanie-gruntu-projekt-domu

Prawo:
- Regulamin czystości Olsztyna (uchwała XVI/231/25): https://edzienniki.olsztyn.uw.gov.pl/WDU_N/2025/3868/oryginal/akt.pdf
- Ustawa o zdrowiu zwierząt: https://eli.gov.pl/eli/DU/2025/1795/ogl/pol/pdf
- Rozporządzenie o środkach zwalczania chorób u drobiu: https://eli.gov.pl/api/acts/DU/2026/335/text/I/D20260335.pdf
- Rozporządzenie o zakładach zwolnionych z rejestracji: https://api.sejm.gov.pl/eli/acts/DU/2026/292/text.pdf
- WNI 2026 (KPODR): https://www.kpodr.pl/wp-content/uploads/2026/07/Prezentacja-WNI-2026.pdf
- Komunikat PLW o zgłaszaniu drobiu: https://lubawka.eu/wp-content/uploads/2026/04/Komunikat_PLW-1.pdf
- Sprzedaż bezpośrednia (Dz.U. 2015 poz. 1703): https://eli.gov.pl/api/acts/DU/2015/1703/text.html ; GIW: https://www.wetgiw.gov.pl/handel-eksport-import/sprzedaz-bezposrednia
- RHD (GIW): https://www.wetgiw.gov.pl/handel-eksport-import/rolniczy-handel-detaliczny
- HPAI — GIW: https://www.wetgiw.gov.pl/nadzor-weterynaryjny/hpai ; https://www.wetgiw.gov.pl/nadzor-weterynaryjny/przepisy-prawne-dotyczace-grypy-ptakow ; https://www.wetgiw.gov.pl/nadzor-weterynaryjny/zasady-ochrony-drobiu-przed-grypa-ptakow
- Rozporządzenie Nr 39 Wojewody (Dz. Urz. 2026 poz. 2466): https://www.inforlex.pl/download/akty_pdf,U82,2026,173,2466.pdf
- Art. 29 Prawa budowlanego: https://arslege.pl/prawo-budowlane/k36/a7956/
- Magazyny energii — nowelizacja: https://www.gramwzielone.pl/?p=20345468
- Warunki techniczne po 20.09.2026: https://inzynierbudownictwa.pl/nowych-warunkow-technicznych-nie-ma-co-dalej/ ; https://muratordom.pl/prawo/formalnosci-budowlane/nowe-warunki-techniczne-spoznione-ratunek-w-prowizorce-stare-przepisy-jeszcze-przez-18-miesiecy-aa-xhtt-Q8pc-pTxz.html
- § 31 WT (studnie): https://arslege.pl/usytuowanie-studni/k218/a23178/
- Budowle rolnicze (1997): https://eli.gov.pl/eli/DU/1997/877/ogl/pol/pdf
- Zwykłe korzystanie z wód (Wody Polskie, 21.07.2026): https://www.gov.pl/web/wody-polskie-szczecin/pobor-wod-w-ramach-zwyklego-korzystania-a-wymog-posiadania-pozwolenia-wodnoprawnego

Dotacje:
- Harmonogram ARiMR 2026: https://www.gov.pl/web/arimr/harmonogram-naborow-wnioskow-ps-wpr-na-lata-2023-2027 ; https://www.gov.pl/attachment/b3bd88d8-004e-4025-b001-f3760bd55649
- Rozwój małych gospodarstw 2025: https://www.gov.pl/web/arimr/premie-na-rozwoj-malych-gospodarstw--wnioski-do-28-listopada-2025-r
- OZE dla rolników (2.10.2026): https://www.gramwzielone.pl/trendy/20379618/dotacje-oze-rolnicy-arimr-nfosigw-pazdziernik
- Energia dla Wsi — wyczerpanie budżetu: https://www.gramwzielone.pl/?p=20379764
- Plany naborów NFOŚiGW (17.09.2026): https://www.gramwzielone.pl/trendy/20377434/nfosigw-szykuje-nowe-nabory-miliardy-zlotych-na-oze-magazyny-i-cieplownictwo
- Mój Prąd 7.0: https://globenergia.pl/nie-bedzie-programu-moj-prad-7-0-a-wyplaty-w-szostej-edycji-dobiegaja-konca/
- Przydomowe magazyny energii, część 1: https://ryglice.pl/wp-content/uploads/2026/04/Program-priorytetowy_PME_Czesc-1-KPO_17_04-_2026.pdf
- Mikroretencja: https://muratordom.pl/prawo/finanse/8-000-zl-na-deszczowke-do-twojego-ogrodu-rusza-wielki-nabor-wnioskow-na-mikroretencje-aa-8iGm-6fct-mVqi.html

---

## G. Luki i niepewności

1. **Strefa planu ogólnego dla działki 144-16/1** — nieustalona. To najważniejsza luka dla każdej nowej zabudowy.
2. **Status MPZP Gutkowo-Południe** (część A i pozostałe) — nieustalony. Usługa krajowa nie pokazuje planu pod adresem.
3. **Powierzchnie ewidencyjne i powierzchnie klasoużytków** — niepublikowane w WMS. Podałem powierzchnie z geometrii. Klasy odczytałem tylko z etykiet, dla 13 działek brak odczytu.
4. **Ulica Poranna** — nie zlokalizowałem jej w promieniu 500 m.
5. **Poziom lustra Ukiela** — 104,8 m (NMT) wobec 103 m (ekofizjografia).
6. **OChK, Natura 2000 w 2026 r.** — opieram się na ekofizjografii z 2023 r. Serwis GDOŚ odmówił dostępu.
7. **Zagrożenie powodziowe (ISOK) i strefy ochronne ujęć wody** — brak danych.
8. **Jakość wód podziemnych (Fe, Mn, twardość) i typowe głębokości studni** — brak danych lokalnych.
9. **Usłonecznienie i napromieniowanie** — brak normy IMGW dla Olsztyna; PVGIS niepobrany.
10. **Daty okresów termicznych 1991–2020** — własne obliczenie z norm miesięcznych, nie dane publikowane.
11. **Przymrozki** — dane z lat 1971–2000; brak dat skrajnych dla Olsztyna i brak nowszego okresu.
12. **KBW IV–IX** — szacunek, nie wartość ze źródła.
13. **Strefa PN-EN 12831, strefa wiatrowa, strefa USDA** — z wiedzy ogólnej. **Głębokość przemarzania** — źródła sprzeczne (1,0 m wobec 1,2–1,4 m).
14. **Odczyn i zasobność gleb** — brak danych OSChR dla miejsca.
15. **HPAI w sezonie 2026/2027** — brak bieżącej listy ognisk i stref dla Olsztyna.
16. **Nowe Warunki techniczne** — nie wiem, czy minister ogłosił je między 28.09 a 11.11.2026 r.
17. **Przepisy podane z wiedzy, bez pobrania tekstu dziś [S]:** art. 32, 34, 35, 394 Prawa wodnego (pobór z jeziora, staw); § 11 rozp. z 12.07.2019 r. (POŚ w aglomeracji); § 12 i § 36 WT; art. 5 u.c.p.g.; art. 50 i 59 u.p.z.p.; znakowanie jaj; limity RHD dla dostaw do sklepów.
18. **Kwalifikacja budowlana kurnika, tunelu foliowego i ziemianki** — sporna; wymaga stanowiska organu.
19. **Dotacje:** terminy kolejnych naborów ARiMR (I.10.2, I.10.5), zasady „Przydomowych magazynów energii” część 2, budżet „Mikroretencji” w Olsztynie i zasady „Czystego Powietrza” — niepotwierdzone.

---

## H. Uzupełnienia (po korektach koordynatora, 11.11.2026)

### H0. Cztery działki właściciela — potwierdzenie i korekty do sekcji A

Obręb: **0144**. ULDK zwraca wszystkie cztery identyfikatory w obrębie 0144. Zapytanie o `286201_1.0044.16/1` zwraca „brak wyników” [Ź]. Obręb 0044 to jezioro Ukiel (działka 1/23).

| Działka | Identyfikator | Pow. z geometrii [m²] | Użytki i klasy wg EGiB (mapa WMS) | Pokrycie terenu (ortofotomapa GUGiK) | Wys. [m n.p.m.] | Odległość od granicy ewidencyjnej jeziora |
|---|---|---|---|---|---|---|
| 16/1 | 286201_1.0144.16/1 | 11 699 | R VI (środek), Ps VI (zachód), Ls V (pas wzdłuż 16/2), Br (zagroda), N, W, Ł V (skrawki) | Zagroda w narożniku SW (dom, 2–3 budynki, plac). Środek: łąka i ogród. Północ: pas drzew | 106,0–118,5 | Ukiel: 8 m od narożnika SW; ok. 64% powierzchni leży do 100 m od granicy jeziora [O] |
| 24/1 | 286201_1.0144.24/1 | 11 022 | Ps VI (środek), Ps V (wschód), R VI i Br (zachód) | Część SW: skoszony trawnik pola kempingowego. Część NE: pole lub wysoka łąka ok. 0,5 ha | 106,5–116,3 | Ukiel: 4–6 m (szerokość pasa 144-25); 100% powierzchni do 100 m; 230 m wspólnej granicy z pasem 25 [O] |
| 19/3 | 286201_1.0144.19/3 | 1 751 | dr | Droga gruntowa SW–NE między 16/1 a 24/1 | 113–117 | Ukiel: 22 m |
| 16/3 | 286201_1.0144.16/3 | 18 217 | **N (największy kontur, północ i środek)**, Lzr-Ps V, Ps V, R V (wschód), Ls V (mały kontur SW), R VI (klin SW) | Zachód i środek: zwarty drzewostan (część na poziomie jeziora, podmokła). Wschód: łąka z pojedynczymi drzewami | 104,8–111,8 | Zgniłek (działka 27/1): 0 m, wspólna granica. Ukiel: 83 m |

Razem: 42 689 m² (4,27 ha). Moje powierzchnie różnią się od pliku `dzialki_wkt.txt` o najwyżej 1 m².

Korekty i ostrzeżenia:
1. **Działka 19/3.** Właściciel podaje, że działka 19/3 jest gruntem gospodarstwa (relacja właściciela, 11.11.2026). Mapa ewidencyjna podaje użytek „dr”.
2. **Pas przy brzegu Ukiela.** Między 24/1 a jeziorem leży działka 144-25: gmina, użytek „dr”, 7 392 m², średnia szerokość ok. 6 m. Należy do użytku ekologicznego „Jezioro Zgniłek”. Przy narożniku 16/1 leży klin 144-19/4: gmina, „Bz”, 255 m². Pas drzew nad wodą rośnie głównie na działce 25. Każde przejście instalacji do jeziora przecina grunt gminy.
3. **Działka 16/3 nie jest w ewidencji lasem.** Kontur „Ls V” to mały fragment przy granicy z działką 14. Drzewostan rośnie głównie na konturach „N” i „Lzr-Ps V”. To zmienia reżim prawny wycinki (H1).
4. **MPZP:** brak planu na lądzie (usługa krajowa zwraca „brak wyniku dla wskazanego obszaru”) [Ź].
5. **Gleba — potwierdzenie deklaracji właściciela.** Wszystkie kontury klasyfikacyjne na czterech działkach mają klasę V lub VI. Najbliższy kontur klasy IVb leży ok. 250 m na wschód (rejon działek 24/4 i 22) [Ź, mapa WMS]. Ekofizjografia podaje kompleksy 6 i 7 oraz piaski słabo gliniaste [Ź]. Usługa WMS mapy glebowo-rolniczej GUGiK nie odpowiedziała, więc arkusza mapy nie odczytałem.

### H1. Działka 16/3 — las i drzewa (część 1: ustawa o lasach)

Źródło: ustawa z 28.09.1991 r. o lasach, tekst jednolity Dz.U. 2025 poz. 567 [Ź].

- **Definicja (art. 3):** las to grunt o zwartej powierzchni min. 0,10 ha pokryty roślinnością leśną i przeznaczony do produkcji leśnej. W praktyce organ opiera się na użytku „Ls” w ewidencji [S].
- **Nadzór (art. 5 ust. 1 pkt 2 i ust. 3):** lasy prywatne nadzoruje starosta. W Olsztynie zadania starosty wykonuje Prezydent Olsztyna. Starosta może powierzyć nadzór nadleśniczemu.
- **Plan (art. 19 ust. 2–3):** dla lasów prywatnych sporządza się uproszczony plan urządzenia lasu (UPUL). Dla lasów rozdrobnionych do 10 ha zadania określa decyzja starosty na podstawie inwentaryzacji stanu lasów.
- **Olsztyn:** Prezydent zatwierdził UPUL dla lasów prywatnych w mieście na lata 2017–2026 (zarządzenie nr 337 z 12.07.2017 r.) [Ź, tytuł dokumentu w BIP]. Plan wygasa 31.12.2026 r. Sprawy lasów prywatnych prowadzi ZDZiT Olsztyn (strona „lasy prywatne”). Treści strony i planu nie odczytałem. Nie wiem, czy plan obejmuje kontur Ls na 16/3.
- **Obowiązki właściciela (art. 13 ust. 1):** utrzymuj roślinność leśną i naturalne bagna. Odnów las w ciągu 5 lat od usunięcia drzewostanu. Pielęgnuj i chroń las. Pozyskuj drewno tylko w rozmiarze z UPUL albo z decyzji.
- **Zmiana lasu na użytek rolny (art. 13 ust. 2):** tylko w szczególnie uzasadnionych przypadkach, decyzją starosty.
- **Legalizacja drewna (art. 14a):** każde drewno pozyskane w lesie podlega cechowaniu. Starosta cechuje drewno i wydaje świadectwo legalności pozyskania. Złóż wniosek przed wywozem drewna.
- **Drewno opałowe na własne potrzeby:** ustawa nie daje osobnego zwolnienia ani stałego limitu w m³. Ilość wynika z zadań w UPUL albo w decyzji. Cięcie ponad plan jest możliwe tylko w przypadkach losowych, decyzją starosty (art. 23 ust. 4).
- **Egzekwowanie (art. 24):** starosta nakazuje decyzją wykonanie obowiązków.
- **Wypas (art. 30 ust. 1):** ustawa zakazuje w lasach wypasu zwierząt gospodarskich, zbierania ściółki i biwakowania poza miejscami wyznaczonymi. Art. 30 nie zawiera wyjątku dla właściciela lasu. **Kozy, owce i drób nie mogą korzystać z gruntu „Ls”.** Zakaz nie obejmuje gruntów „Lzr-Ps”, „Ps”, „R” i „N”.

### H1 (część 2). Wycinka drzew i krzewów poza lasem — art. 83f ustawy o ochronie przyrody

Źródło: art. 83f w serwisie arslege.pl (serwis nie podaje daty stanu prawnego) [Ź].

Zezwolenia nie wymaga usunięcie (art. 83f ust. 1):
- krzewów w skupisku do 25 m² (pkt 1);
- drzew o obwodzie pnia na wysokości 5 cm do: 80 cm (topola, wierzba, klon jesionolistny, klon srebrzysty); 65 cm (kasztanowiec zwyczajny, robinia akacjowa, platan klonolistny); 50 cm (pozostałe gatunki) (pkt 3);
- drzew i krzewów na nieruchomości osoby fizycznej, usuwanych na cele niezwiązane z działalnością gospodarczą (pkt 3a);
- **drzew i krzewów usuwanych w celu przywrócenia gruntów nieużytkowanych do użytkowania rolniczego (pkt 3b)**. Ustawa nie definiuje „gruntów nieużytkowanych” i nie wymaga zgłoszenia;
- drzew i krzewów owocowych (pkt 5);
- drzew w lasach (pkt 4) — tam obowiązuje ustawa o lasach;
- złomów i wywrotów, po oględzinach organu (pkt 14 lit. b).

Zgłoszenie przy pkt 3a (ust. 4–13): zgłoś Prezydentowi Olsztyna zamiar usunięcia drzewa o obwodzie ponad progi 80/65/50 cm. Organ robi oględziny w ciągu 21 dni. Organ może wnieść sprzeciw w ciągu 14 dni od oględzin. Brak sprzeciwu oznacza zgodę. Usuń drzewo w ciągu 6 miesięcy od oględzin. Opłata grozi tylko wtedy, gdy w ciągu 5 lat wystąpisz o pozwolenie na budowę związaną z działalnością gospodarczą w miejscu po drzewie (ust. 17).

Zastosowanie do działki 16/3 [S — uzgodnij z Wydziałem Środowiska UM Olsztyna]:

| Kontur EGiB | Stan w terenie | Tryb |
|---|---|---|
| R V (wschód), R VI (klin SW), Ps V | Łąka z pojedynczymi drzewami, zarośla | Grunt rolny. Samosiewy usuń na podstawie pkt 3b, gdy przywracasz pastwisko, sad albo pole. Zrób wcześniej dokumentację zdjęciową. Potem faktycznie użytkuj grunt rolniczo |
| Lzr-Ps V | Zwarty drzewostan na użytku rolnym | Grunt rolny zadrzewiony. Pkt 3b jest możliwy. Bezpieczniej: zgłoszenie z pkt 3a albo pisemne stanowisko organu przed wycinką |
| N (północ i środek, częściowo na poziomie 104,8–105,2 m n.p.m.) | Drzewostan podmokły przy Zgniłku | Nieużytek nie jest gruntem rolnym. Zastosowanie pkt 3b jest sporne. Użyj zgłoszenia (pkt 3a). Zalecenie: zostaw ten drzewostan jako bufor użytku ekologicznego; pozyskuj tylko posusz i wywroty |
| Ls V (mały kontur) | Las | Ustawa o lasach: plan albo decyzja, cechowanie, zakaz wypasu |

Drewno opałowe na własne potrzeby domu to cel niezwiązany z działalnością gospodarczą [S]. Drewno dla kempingu albo na sprzedaż to cel gospodarczy; wtedy potrzebne jest zezwolenie i opłata [S]. Przy każdej wycince obowiązuje ochrona gatunkowa i okres lęgowy ptaków (1 marca–15 października) [S].

### H2. Kozy lub owce mleczne i pszczoły

**Kozy i owce (kilka sztuk):**
1. Zarejestruj zakład u Powiatowego Lekarza Weterynarii (PLW) w Olsztynie przed zakupem zwierząt. PLW nadaje numer WNI (art. 55 i 57 ustawy o zdrowiu zwierząt; art. 84 rozp. (UE) 2016/429). Zwolnienie z rejestracji nie obejmuje zakładów ze zwierzętami kopytnymi, także na własne potrzeby (rozp. MRiRW, Dz.U. 2026 poz. 292) [Ź].
2. Zarejestruj siedzibę stada w ARiMR i prowadź zgłoszenia w IRZplus (ustawa z 4.11.2022 r. o systemie identyfikacji i rejestracji zwierząt, w mocy od 6.01.2023 r.). Od 1.01.2026 r. zgłoszenia przyjmuje tylko IRZplus [Ź, ARiMR].
3. Oznakuj każde zwierzę do 180 dni od urodzenia i zawsze przed opuszczeniem stada urodzenia [Ź]. Stosuj identyfikatory od dostawców z listy ARiMR: kolczyki zwykłe i elektroniczne, opaski na pęcinę, bolusy [Ź]. Zwierzę hodowlane nosi dwa identyfikatory, w tym jeden elektroniczny [S].
4. Zgłoś każde zdarzenie (zakup, sprzedaż, padnięcie, ubój) w ciągu 7 dni [Ź].
5. Regulamin Olsztyna nie zakazuje kóz i owiec na nieruchomości gospodarstwa rolnego (§ 13) [Ź].

**Pszczoły:**
1. Zarejestruj pasiekę u PLW w Olsztynie i uzyskaj WNI. Rozporządzenie o zwolnieniach wyłącza pszczoły ze zwolnienia, więc obowiązek dotyczy nawet 1 ula na własne potrzeby (§ 1 rozp. Dz.U. 2026 poz. 292) [Ź].
2. Przekazuj PLW informację o pasiece do 31 marca i do 30 września każdego roku (art. 68 ust. 4 ustawy o zdrowiu zwierząt) [Ź].
3. ARiMR nie prowadzi rejestru rodzin pszczelich w IRZ [S]. Nabory pszczelarskie ARiMR (I.6.x) trwają 23.10–27.11.2026 r. [Ź].
4. Odległości uli wg regulaminu Olsztyna (§ 14; wiąże nieruchomości spoza gospodarstw rolnych) [Ź]: min. 15 m od granicy nieruchomości; min. 30 m od budynków na sąsiednich nieruchomościach; mniej tylko za zgodą sąsiada i z ogrodzeniem min. 2 m, ustawionym min. 4 m od granicy; teren ogrodzony; tablica ostrzegawcza. **Regulamin nie podaje odległości od dróg.** Ustawa krajowa nie określa odległości uli [S].
5. Zalecenie [S]: zastosuj § 14 jako standard także w gospodarstwie. Ustaw ule min. 15 m od pasa 144-25, od drogi 19/3 i od pola kempingowego. Skieruj wyloty w stronę przeciwną do kempingu. Posadź żywopłot 2 m.

**Sprzedaż mleka i miodu:**

| Produkt | Sprzedaż bezpośrednia (rozp. MRiRW z 30.09.2015 r., Dz.U. 2015 poz. 1703) | RHD |
|---|---|---|
| Mleko surowe (kozie, owcze) | Do 1 000 l na tydzień, 52 000 l na rok; surowa śmietana do 200 l na tydzień (§ 6) [Ź]. Rejestracja u PLW. Wymagania zdrowotne stada i chłodzenie mleka [S] | Tak |
| Sery, jogurty | Nie [S] | Tak. Wniosek do PLW 30 dni przed startem. Sprzedaż konsumentom bez limitu ilości. Zwolnienie z PIT do 100 000 zł przychodu na rok [Ź, GIW] |
| Miód i inne nieprzetworzone produkty pszczele | Tak. § 6 nie określa limitu ilości. Ewidencja miesięczna (§ 41) [Ź]. Rejestracja u PLW | Tak |

### H3. Instalacja PV off-grid z magazynem energii

Formalności budowlane (nie zależą od przyłączenia do sieci):
- PV do 150 kW: bez pozwolenia i bez zgłoszenia, na dachu i na gruncie (art. 29 ust. 4 pkt 3 lit. c Prawa budowlanego) [Ź].
- **PV powyżej 6,5 kW: uzgodnij projekt z rzeczoznawcą do spraw zabezpieczeń przeciwpożarowych i zawiadom Państwową Straż Pożarną (art. 56 ust. 1a)** [Ź]. Przepis dotyczy instalowania urządzeń, więc obejmuje też instalację wyspową [S].
- Magazyn energii: do 30 kWh bez formalności; powyżej 30 do 300 kWh zgłoszenie budowy z uzgodnieniem ppoż.; wolno stojący powyżej 300 do 2 000 kWh zgłoszenie i zawiadomienie PSP; powyżej 2 000 kWh pozwolenie [Ź].
- Zleć pomiary i protokół odbioru elektrykowi z uprawnieniami [S].

Zgłoszenie do OSD:
- Zgłoszenie mikroinstalacji dotyczy źródeł przyłączonych do sieci. **Instalacja niepołączona z siecią nie wymaga zgłoszenia** (stanowisko Energi cytowane przez enerad.pl, aktualizacja 12.12.2024 r.) [Ź].
- Jeżeli budynek zachowuje przyłącze, a falownik hybrydowy pracuje w tej samej instalacji, zgłoś PV i magazyn do OSD [Ź].

Rozwiązanie umowy kompleksowej [S — art. 4j ust. 3–4 Prawa energetycznego; dziś niezweryfikowane w tekście ustawy]:
1. Złóż sprzedawcy pisemne wypowiedzenie umowy kompleksowej. Odbiorca w gospodarstwie domowym nie ponosi kosztów wypowiedzenia.
2. Umowa kończy się z ostatnim dniem miesiąca następującego po miesiącu doręczenia wypowiedzenia, chyba że wskażesz późniejszy termin.
3. OSD demontuje licznik (licznik jest własnością OSD) i odłącza przyłącze. Przyłącze pozostaje własnością OSD.
4. Powrót do sieci wymaga nowej umowy. Po likwidacji przyłącza wymaga nowego wniosku o przyłączenie i opłaty.
5. Sprawdź wcześniej, czy kemping ma osobną umowę i osobny licznik.

Zalecenie: utrzymaj przyłącze przez pierwsze 12 miesięcy pracy wyspowej jako rezerwę. Wypowiedz umowę po sprawdzeniu bilansu w grudniu i styczniu.

### H4. Strefa planu ogólnego dla działek 16/1, 24/1, 16/3 — nieustalona (3 próby)

| Próba | Wynik (11.11.2026) |
|---|---|
| Przeglądarka `rejestrplanowogolnych.pl/?teryt=286201_1` (2 razy) | Serwer nie odpowiada z mojego środowiska („upstream connect error”) |
| Krajowa usługa WMS „Plany ogólne gmin — uchwalone” (`https://mapy.geoportal.gov.pl/wss/ext/PlanyOgolneGmin`, warstwy `strefaPlanistyczna`, `obszarUzupelnieniaZabudowy`, `aktPlanowaniaprzestrzennego`) | Pusty obraz i komunikat „Usługa nie zwróciła żadnych informacji” dla punktu na działce 16/1. Usługa nie zawiera jeszcze danych planu Olsztyna albo nie zwraca ich w tym miejscu |
| Plik GML planu (`edzienniki.olsztyn.uw.gov.pl/WDU_N/2026/2447/Zalacznik1.gml`) | Nie przetwarzałem. Plik zawiera 4 946 stref; moje narzędzia nie pobierają go w całości |

Jak ustalić strefę:
1. Otwórz `https://rejestrplanowogolnych.pl/?teryt=286201_1` albo moduł „Planowanie Przestrzenne” w geoportal.gov.pl. Odczytaj symbol strefy (SN, SO, SU, SJ, SZ, SR…), profil podstawowy i dodatkowy oraz wskaźniki. Sprawdź warstwę „obszar uzupełnienia zabudowy”.
2. Albo wczytaj plik GML do QGIS (wtyczka APP) i przetnij go z geometrią z `dzialki_wkt.txt`.
3. Albo złóż w Wydziale Urbanistyki i Architektury wniosek o wypis i wyrys z planu ogólnego [S].

Nie zgaduję strefy. Dla orientacji: w całym mieście strefa zieleni i rekreacji zajmuje 38,58%, strefa otwarta 17,5%, strefa z zabudową zagrodową 0,15% [Ź]. Studium z 2013 r. przewidywało tu usługi turystyki, sportu i rekreacji bez intensywnej zabudowy [Ź].

### H5. HPAI — Olsztyn i powiat olsztyński, sezon 2026/2027 (2 próby)

- **Bieżącej listy ognisk i stref nie odczytałem.** GIW publikuje wykazy ognisk z 2026 r. jako pliki PDF w serwisie SharePoint. Moje narzędzia nie mają do nich dostępu.
- Akty z 2026 r., które znalazłem w Dzienniku Urzędowym województwa, **nie wymieniają Olsztyna ani powiatu olsztyńskiego** [Ź]:
  - rozporządzenie Nr 1 PLW w Braniewie z 27.02.2026 r. (poz. 844): strefa w gminie Braniewo po wykryciu HPAI u myszołowa; nakaz utrzymywania drobiu w zamknięciu w tej strefie;
  - rozporządzenie PLW w Działdowie nr 4/2026 z 14.04.2026 r., uchylone 19.06.2026 r. (poz. 2463);
  - rozporządzenie Nr 10 Wojewody z 20.02.2026 r. o zasadach utrzymywania drobiu, uchylone rozporządzeniem Nr 39 z 19.06.2026 r. (poz. 2466); ostatnie ognisko na tym obszarze: 13.05.2026 r. Zasięgu obszaru nie odczytałem.
- Decyzja wykonawcza Komisji (UE) 2026/2483 z 30.10.2026 r. potwierdza, że pod koniec października 2026 r. w UE działały strefy ograniczeń. Nie sprawdziłem, czy obejmują województwo.
- Przed zakupem ptaków sprawdź mapę `https://bip.wetgiw.gov.pl/ai/mapa/` i zadzwoń do Powiatowego Inspektoratu Weterynarii w Olsztynie.
- Niezależnie od stref stosuj przez cały rok nakazy z § 3 ust. 1 rozporządzenia Dz.U. 2026 poz. 335 (sekcja E12). Jezioro Ukiel i Zgniłek to siedliska dzikiego ptactwa wodnego tuż przy gospodarstwie, więc ryzyko zawleczenia wirusa jest tu wyższe niż przeciętne [S].

### H6. Dodatkowe źródła do sekcji H

- Ustawa o lasach, t.j. Dz.U. 2025 poz. 567: https://api.sejm.gov.pl/eli/acts/DU/2025/567/text.pdf
- Art. 83f ustawy o ochronie przyrody: https://arslege.pl/ustawa-o-ochronie-przyrody/k452/a86169/
- UPUL Olsztyna 2017–2026 (zarządzenie nr 337 z 12.07.2017 r., BIP; treści nie odczytałem): http://bip.olsztyn.eu/bip/dokument/334549/
- ZDZiT Olsztyn, lasy prywatne (treści nie odczytałem): https://zdzit.olsztyn.eu/lasy-prywatne/
- ARiMR, zasady rejestrowania i znakowania zwierząt (5.01.2023): https://www.gov.pl/web/arimr/od-6-stycznia-zmiany-w-zasadach-rejestrowania-i-znakowania-zwierzat
- PV bez zgłoszenia, off-grid a OSD (enerad.pl, akt. 12.12.2024): https://enerad.pl/instalacja-fotowoltaiczna-bez-zgloszenia-i-pozwolenia-kiedy/
- WMS planów ogólnych GUGiK (20.01.2026): https://www.geoportal.gov.pl/aktualnosci/uchwalone-plany-ogolne-gmin-pog-w-serwisie-www-geoportal-gov-pl/
- Rozporządzenie PLW w Braniewie (Dz. Urz. 2026 poz. 844): https://www.inforlex.pl/download/akty_pdf,U82,2026,62,844.pdf
- Ortofotomapa GUGiK (WMS): https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMS/StandardResolution
- WMS mapy glebowo-rolniczej GUGiK (nie odpowiedział): https://mapy.geoportal.gov.pl/wss/service/pub/guest/MapaGlebowoRolnicza/MapServer/WMSServer

### H7. Lista luk po uzupełnieniach (zastępuje sekcję G)

1. Strefa planu ogólnego i przynależność do OUZ dla 16/1, 24/1, 16/3 — nieustalone (H4).
2. Status MPZP „Gutkowo-Południe” — nieustalony; na lądzie brak planu w usłudze krajowej.
3. Status prawny 16/3: czy UPUL Olsztyna obejmuje kontur Ls V; jak urząd zakwalifikuje wycinkę na konturach N i Lzr-Ps V.
4. Powierzchnie ewidencyjne działek i konturów klasoużytków — niepublikowane; mam tylko powierzchnie z geometrii i etykiety.
5. Poziom lustra Ukiela: 104,8 m (NMT) wobec 103 m (ekofizjografia).
6. OChK i Natura 2000 w 2026 r. — opieram się na ekofizjografii z 2023 r.; serwis GDOŚ odmówił dostępu.
7. Zagrożenie powodziowe (ISOK) i strefy ochronne ujęć wody — brak danych.
8. Jakość wód podziemnych (Fe, Mn, twardość) i głębokości studni w Gutkowie — brak danych.
9. Mapa glebowo-rolnicza (arkusz) i dane OSChR o odczynie — nieodczytane; klasy V–VI potwierdzone tylko przez EGiB i ekofizjografię.
10. Usłonecznienie (IMGW: brak normy dla Olsztyna) i napromieniowanie (PVGIS niepobrany).
11. Okresy termiczne 1991–2020 — moje obliczenie; przymrozki — dane 1971–2000; KBW — szacunek.
12. Strefa PN-EN 12831, strefa wiatrowa i strefa USDA — z wiedzy ogólnej; głębokość przemarzania — źródła sprzeczne (1,0 m wobec 1,2–1,4 m).
13. HPAI w sezonie 2026/2027 dla Olsztyna — brak bieżących danych (H5).
14. Nowe Warunki techniczne — nie wiem, czy minister ogłosił je po 28.09.2026 r.
15. Przepisy podane z wiedzy [S], bez pobrania tekstu: art. 32, 34, 35, 394 Prawa wodnego; § 11 rozp. z 12.07.2019 r. (oczyszczalnia w aglomeracji); § 12 i § 36 WT; art. 5 u.c.p.g.; art. 50, 59, 61 u.p.z.p.; art. 4j Prawa energetycznego; liczba identyfikatorów u owiec i kóz; wymagania dla mleka surowego; znakowanie jaj; limity RHD dla dostaw do sklepów.
16. Kwalifikacja budowlana kurnika, tunelu foliowego i ziemianki — wymaga stanowiska organu.
17. Dotacje: terminy kolejnych naborów ARiMR (I.10.2, I.10.5), zasady „Przydomowych magazynów energii” część 2, budżet „Mikroretencji” w Olsztynie, zasady „Czystego Powietrza” — niepotwierdzone.
18. Ulica Poranna — nie zlokalizowałem jej w promieniu 500 m.

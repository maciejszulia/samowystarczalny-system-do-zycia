# R4. Raport koordynatora: horyzont stelaża, pokrycie koron, symulacja PVGIS

Data obliczeń: 2026-11-11. Raport uzupełnia raporty R1, R2 i R3. Dokument projektu cytuje dane tego raportu jako źródło Z46. Sekcja 9 zawiera dane właściciela z 2026-11-11 i zmiany, które wynikają z tych danych.

## 1. Dane wejściowe

| Dane | Wartość | Źródło |
| --- | --- | --- |
| Numeryczny model pokrycia terenu (NMPT) | Siatka 1 m, obszar 800 m × 800 m, układ PL-1992, wysokości PL-KRON86-NH | GUGiK, usługa WCS `mapy.geoportal.gov.pl/wss/service/PZGIK/NMPT/GRID1/WCS/DigitalSurfaceModel`, pokrycie `DSM_PL-KRON86-NH` |
| Numeryczny model terenu (NMT) | Siatka 1 m, ten sam obszar | GUGiK, usługa WCS `mapy.geoportal.gov.pl/wss/service/PZGIK/NMT/GRID1/WCS/DigitalTerrainModel`, pokrycie `DTM_PL-KRON86-NH` |
| Zakres obszaru | E od 591 941 do 592 741; N od 658 644 do 659 444 | parametr BBOX |
| Aktualność NMPT | 2018-03-21 (arkusz N-34-77-D-b-3-1); starszy zbiór: 2011-08-04 | GUGiK, skorowidz `PZGIK/NMPT/WMS/SkorowidzeUkladKRON86` |
| Aktualność ortofotomapy | 2025-08-14, piksel 0,05 m (arkusz N-34-77-D-b-3-1) | GUGiK, skorowidz `PZGIK/ORTO/WMS/SkorowidzeWgAktualnosci` |
| Symulacja energii | PVGIS 5.3, usługi SHScalc i PVcalc, dane 2005–2023, punkt 53,7875° N, 20,402° E | Komisja Europejska JRC |

Wysokość roślinności w komórce to różnica NMPT − NMT.

OSTRZEŻENIE: Model z 2018-03-21 pochodzi z okresu bez liści i ma 8 lat. Ten model zaniża korony drzew liściastych i nie zawiera przyrostu drzew po 2018 r.

## 2. Kontrola danych

| Punkt | Współrzędne E; N | NMT [m n.p.m.] | NMPT [m n.p.m.] |
| --- | --- | --- | --- |
| Punkt adresowy domu | 592 285; 658 959 | 107,35 | 113,15 (dach) |
| Jezioro Ukiel | 592 440; 658 900 | brak | 104,71 |
| Wierzchowina przy linii stelaża | 592 356; 659 030 | 118,52 | 118,85 |
| Gruzowisko K w strefie S2 | 592 356; 659 019 | 120,16 | 120,40 |

Raport R1 podaje dla domu 107,3 m n.p.m. i dla jeziora 104,8 m n.p.m. Różnica jest mniejsza niż 0,1 m.

## 3. Gruzowisko K w strefie S2

Model terenu pokazuje wzniesienie o wymiarach 7 m × 6 m i wysokości 2,2 m. Środek wzniesienia: E 592 357, N 659 018,5. Wierzchołek: 120,2 m n.p.m. Grunt obok wzniesienia: od 117,7 m do 118,2 m n.p.m.

Właściciel podaje: wzniesienie to gruzowisko `[relacja: właściciel, 2026-11-11]`. Dokument projektu nazywa ten obiekt „gruzowisko K”.

`V = Σ max(0; z − z_p) × 1 m²`

- V: objętość gruzowiska K nad płaszczyzną terenu [m³]. z: wysokość komórki NMT [m n.p.m.].
- z_p: wysokość płaszczyzny, którą raport dopasował do komórek w odległości od 7 m do 10 m od wierzchołka [m n.p.m.].
- Suma obejmuje komórki w promieniu R od wierzchołka. Wynik: 58,9 m³ dla R = 5 m; 62,2 m³ dla R = 6 m; 63,8 m³ dla R = 7 m.

Dokument projektu podaje objętość 60 m³ ± 5 m³. Skład gruzu: [DO USTALENIA: oględziny w terenie].

Siatka 413 punktów, której używa dokument projektu, nie trafiła w gruzowisko K. Dlatego rysunek 2 dokumentu pokazuje szczyt 118,6 m n.p.m.

## 4. Pokrycie koron w strefach (stan z 2018-03-21)

| Strefa | Komórki 1 m² | Udział komórek o wysokości roślin co najmniej 2 m [%] | co najmniej 5 m [%] | co najmniej 10 m [%] | co najmniej 15 m [%] | Średnia wysokość komórek co najmniej 5 m [m] | Największa wysokość [m] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S8a drzewostan na działce 16/3 | 13 894 | 25,8 | 13,4 | 5,9 | 2,0 | 10,2 | 25,4 |
| S8b zadrzewiony stok na działce 16/1 | 2 265 | 52,5 | 48,9 | 39,8 | 23,6 | 14,4 | 23,1 |
| S2 warzywnik i pole P1 | 1 838 | 6,3 | 2,4 | 0,1 | 0,0 | 6,4 | 10,1 |
| S4a pole P2 | 967 (uproszczony obrys) | 3,1 | 0,4 | 0,0 | 0,0 | 5,5 | 5,8 |
| S6 łąka kośna | 2 477 | 0,0 | 0,0 | 0,0 | 0,0 | brak | 0,3 |
| S7 pastwisko | 1 846 | 0,8 | 0,3 | 0,1 | 0,0 | 8,8 | 10,3 |

Wnioski:

1. Strefa S8a miała w marcu 2018 r. rośliny o wysokości co najmniej 5 m na 13,4% powierzchni: 1 861 m².
2. Strefa S8b miała takie rośliny na 48,9% powierzchni: 1 106 m².
3. Ortofotomapa z 2025-08-14 pokazuje zwarte korony w całej strefie S8a [obserwacja].
4. Te 2 obrazy różnią się. Możliwe przyczyny (lista niepełna): pomiar bez liści; przyrost młodych drzew od 2018 r.
5. Pierwsza wersja raportu liczyła dolną granicę pozysku tylko dla 0,30 ha drzew z 2018 r.: 0,30 ha × 6,5 mp/ha = 2 mp na rok.
6. Właściciel podaje wiek drzew: od 20 do 50 lat `[relacja: właściciel, 2026-11-11]`. Drzewa w tym wieku stały w 2018 r. na całej powierzchni strefy S8a.
7. Wniosek z punktu 6: model z 2018-03-21 zaniża pokrycie koron, a dolna granica 2 mp nie obowiązuje `[założenie]`.
8. Dolna granica pozysku po relacji właściciela: 1,62 ha × 6,5 mp/ha = 10 mp na rok, przy przyroście 6,0 m³/ha na rok `[założenie]`.
9. Górna granica pozysku: 1,62 ha × 10,7 mp/ha = 17 mp na rok. Ta granica wymaga zwartego drzewostanu o przyroście 9,94 m³/ha na rok.
10. Zasobność drzewostanu: [DO USTALENIA: inwentaryzacja: gatunki, liczba drzew, pierśnice, wysokości].

## 5. Profil horyzontu stelaża

Metoda:

1. Punkt obserwacji leży 0,5 m nad gruntem (dolna krawędź modułów).
2. Linia stelaża ma 9 punktów obserwacji co 4 m.
3. Kąt horyzontu w azymucie to największy kąt wzniesienia komórki NMPT na promieniu od 3 m do 560 m.
4. Profil podaje największy kąt z 9 punktów, co 5° azymutu.
5. Komórki w strefach S2 i S4a mają w obliczeniu wysokość gruntu. Projekt usuwa krzewy i drzewa z tych stref.
6. Wariant „+5 m” podnosi o 5 m każdą komórkę z roślinnością o wysokości co najmniej 2 m.

Położenie Słońca 21 grudnia (szerokość 53,79° N): 12,8° w południe słoneczne; 11,7° o 11:00 i o 13:00; 8,5° o 10:00 i o 14:00. Wschód w azymucie 132°, zachód w azymucie 228°.

| Linia stelaża | Grunt na linii [m n.p.m.] | Horyzont w azymucie od 150° do 210° [°] | Słońce na całym stelażu 21 grudnia (czas słoneczny) | Najmniejszy zapas kąta od 10:00 do 14:00 [°] | Odległość linii od drzew o wysokości co najmniej 10 m po stronie północnej [m] |
| --- | --- | --- | --- | --- | --- |
| A: N 659 044, E od 592 325 do 592 357 (pierwsza wersja projektu) | od 116,8 do 117,4 | od 4,1 do 6,0 | od 09:11 do 14:43 | 3,5 | 5 |
| B: N 659 036, E od 592 325 do 592 357 (wersja przyjęta) | od 117,6 do 118,2 | od 3,8 do 6,0 | od 09:01 do 14:59 | 4,1 | 12 |
| C: N 659 030, E od 592 336 do 592 368 | od 117,8 do 118,5 | od 4,3 do 7,1 | od 09:21 do 14:35 | 2,7 | 18 |
| B, wariant „+5 m” | od 117,6 do 118,2 | od 7,7 do 10,6 | od 10:35 do 14:12 | −1,5 | 12 |

Linia A leży 5 m od drzew strefy S8b o wysokości od 16 m do 20 m. Dlatego projekt przyjmuje linię B.

Przeszkody dla linii B (stan z 2018 r.):

| Azymut [°] | Kąt horyzontu [°] | Przeszkoda | Odległość [m] | Wysokość roślin [m] |
| --- | --- | --- | --- | --- |
| od 140 do 165 | od 3,6 do 4,9 | gruzowisko K w strefie S2 | od 17 do 21 | 0 (grunt) |
| od 170 do 205 | od 4,2 do 6,0 | drzewa przy południowym narożniku działki 16/1 i przy drodze 19/3 | od 62 do 74 | od 10 do 15 |
| od 225 do 245 | od 6,6 do 10,3 | drzewa przy siedlisku (E 592 280, N 658 998) | od 56 do 85 | od 16 do 21 |
| od 300 do 60 | od 27 do 48 | drzewa strefy S8b | od 13 do 30 | od 16 do 21 |

Wariant „+5 m” dla linii B: krzewy przy granicy strefy S4a i drogi dają od 9,8° do 10,6° w azymucie od 150° do 160°. Położenie krzewów: E 592 370, N 659 002.

Profil B (72 wartości, od północy zgodnie z ruchem wskazówek zegara, co 5°):

`48.1,44.2,44.7,45.2,46.1,45.0,42.9,38.7,38.6,36.3,32.8,29.6,27.3,23.7,19.7,14.8,6.3,6.1,5.4,4.4,4.0,3.0,1.8,2.7,3.3,3.7,4.1,4.0,3.6,4.5,3.9,4.9,3.8,4.6,4.2,4.8,5.1,4.8,4.7,6.0,5.0,4.7,4.2,3.8,3.3,6.8,10.3,9.2,7.9,6.6,3.6,5.2,5.8,5.9,5.7,5.5,4.0,2.9,9.5,21.0,27.6,30.4,33.1,35.1,39.5,38.3,42.5,42.7,44.9,46.2,43.6,44.6`

Profil B, wariant „+5 m”:

`56.3,51.5,52.5,53.8,54.4,52.3,50.9,46.7,46.3,44.9,41.9,38.1,34.7,30.7,25.8,20.2,8.0,7.2,6.3,5.4,4.9,4.2,3.2,6.4,3.5,8.1,7.9,7.8,8.8,9.4,9.8,10.3,10.6,8.3,8.7,9.3,9.4,9.0,8.9,10.3,8.8,8.8,7.7,7.3,5.9,11.8,15.0,13.5,11.8,11.7,9.9,7.7,6.6,6.7,6.5,6.3,5.8,8.2,17.0,27.6,35.3,38.5,41.7,44.2,47.1,47.8,50.2,50.6,53.5,54.2,51.2,52.4`

## 6. Symulacja PVGIS z profilem horyzontu

Parametry SHScalc: azymut południowy, dolna granica rozładowania 20%, parametr `userhorizon` z sekcji 5.

`dni puste na rok = f_e × 365,25 / 100`

- f_e: udział dni, w których magazyn energii osiągnął dolną granicę [%]; wynik usługi SHScalc.

`energia z agregatu = dni puste na rok × E_miss / 1000`

- E_miss: średni brak energii w dniu pustym [Wh]; wynik usługi SHScalc. Energia z agregatu ma jednostkę kWh na rok.

| Fotowoltaika [kWp] | Magazyn [kWh] | Zużycie [kWh na dobę] | Kąt [°] | f_e rok [%] | f_e grudzień [%] | E_miss [Wh] | Dni puste na rok | Agregat [kWh na rok] |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15 | 30 | 8 | 60 | 7,10 | 40,75 | 3 220,88 | 25,9 | 84 |
| 20 | 30 | 8 | 60 | 3,72 | 28,52 | 2 762,08 | 13,6 | 38 |
| 25 | 30 | 8 | 60 | 1,67 | 14,09 | 2 689,51 | 6,1 | 16 |
| 30 | 30 | 8 | 60 | 0,82 | 8,15 | 2 559,15 | 3,0 | 8 |
| 20 | 40 | 8 | 60 | 2,15 | 17,49 | 3 022,71 | 7,9 | 24 |
| 25 | 40 | 8 | 60 | 0,84 | 7,98 | 3 006,99 | 3,1 | 9 |
| 30 | 60 | 8 | 60 | 0,10 | 1,02 | 1 556,15 | 0,4 | 1 |
| 40 | 60 | 8 | 65 | 0,00 | 0,00 | 0 | 0,0 | 0 |
| 20 | 30 | 14 | 60 | 18,36 | 70,46 | 6 014,55 | 67,1 | 403 |

Wariant „+5 m” (profil z roślinnością wyższą o 5 m):

| Fotowoltaika [kWp] | Magazyn [kWh] | Zużycie [kWh na dobę] | f_e rok [%] | f_e grudzień [%] | Dni puste na rok | Agregat [kWh na rok] |
| --- | --- | --- | --- | --- | --- | --- |
| 20 | 30 | 8 | 5,45 | 40,24 | 19,9 | 63 |
| 25 | 30 | 8 | 3,21 | 26,99 | 11,7 | 33 |
| 30 | 30 | 8 | 1,80 | 16,81 | 6,6 | 18 |

Porównanie z horyzontem domyślnym PVGIS (bez drzew): układ 25 kWp i 30 kWh przy 8 kWh na dobę miał f_e = 1,53% (5,6 dnia). Profil B daje f_e = 1,67% (6,1 dnia).

Produkcja z usługi PVcalc (kąt 60°, straty 14%) [kWh/kWp]:

| Wariant | I | II | III | IV | V | VI | VII | VIII | IX | X | XI | XII | Rok |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Horyzont domyślny PVGIS | 32,47 | 53,84 | 90,21 | 111,31 | 116,08 | 112,43 | 111,46 | 109,98 | 99,71 | 72,03 | 30,17 | 23,89 | 963,58 |
| Profil B | 31,12 | 52,68 | 90,09 | 111,31 | 116,08 | 112,43 | 111,46 | 109,98 | 99,68 | 71,22 | 29,35 | 23,89 | 959,28 |
| Profil B, wariant „+5 m” | 27,49 | 48,60 | 89,21 | 111,31 | 116,08 | 112,43 | 111,46 | 109,98 | 99,62 | 69,25 | 28,22 | 18,02 | 941,68 |

Produkcja roczna 25 kWp dla profilu B: 25 kWp × 959,28 kWh/kWp = 23 982 kWh.

## 7. Zmiany w dokumencie projektu po weryfikacji

| Element | Przed weryfikacją | Po weryfikacji |
| --- | --- | --- |
| Linia stelaża | Północna krawędź strefy S2 (linia A) | Linia B: od 8 m do 10 m na południe od północnej granicy strefy S2 |
| Dni puste na rok (25 kWp, 30 kWh, 8 kWh na dobę) | 5,6 | 6,1 |
| Zbiornik W1 | Grunt 118,4 m n.p.m.; Δh = 11,3 m; 1,11 bar | Wschodni koniec stelaża; grunt 118,2 m n.p.m.; Δh = 10,8 m; 1,06 bar |
| Tunel T1 | Zachodnia część strefy S2 | Wschodnia krawędź strefy S2, oś północ–południe |
| Pozysk drewna | od 10 mp do 17 mp na rok | od 10 mp do 17 mp na rok po relacji właściciela o wieku drzew (sekcja 4, punkty od 5 do 8); inwentaryzacja przed pierwszą ścinką |
| Uzasadnienie zacienienia | Drzewa nad jeziorem w odległości 89 m (błąd: brzeg leży od 135 m do 150 m od stelaża) | Profil horyzontu z NMPT |

Poprzednia różnica wysokości Δh = 11,3 m nie zgadzała się z wysokościami 118,4 m i 107,3 m: 118,4 m − 107,3 m = 11,1 m.

## 8. Braki

| Nr | Brak | Sposób ustalenia |
| --- | --- | --- |
| 1 | Kąty przeszkód w 2026 r. w azymucie od 150° do 210° | Pomiar klinometrem z linii stelaża |
| 2 | Gatunki i zasobność drzewostanu w strefie S8a | Inwentaryzacja drzewostanu |
| 3 | Skład gruzu i objętość gruzowiska K w 2026 r. | Oględziny i pomiar |
| 4 | Stan drzew strefy S8b w pasie 20 m na północ od stelaża | Oględziny przed montażem |
| 5 | Użytek gruntowy pod strefą S8b (Ls albo inny) | Wypis z ewidencji gruntów |
| 6 | Typ studni, średnica, głębokość lustra wody, wydajność, wynik badania wody | Pomiar i badanie laboratoryjne |
| 7 | Wyniki analizy chemicznej gleby z 2025-04-08 | Plik od właściciela |

## 9. Dane właściciela z 2026-11-11

Właściciel odpowiedział na pytania projektu 2026-11-11. Każdy wiersz ma znacznik `[relacja: właściciel, 2026-11-11]`.

| Nr | Dane właściciela | Zmiana w projekcie |
| --- | --- | --- |
| 1 | Zasięg kempingu nie jest ważny. | Strefa S9 zostaje w granicach z ortofotomapy: 5 899 m². |
| 2 | Działka 19/3 jest gruntem właściciela. | Projekt traktuje działkę 19/3 jako grunt gospodarstwa. |
| 3 | Stado drobiu: „może być 100 sztuk”. | Projekt przyjmuje stado pełne: co najwyżej 100 sztuk w szczycie sezonu, 10 260 jaj na rok, 3,37 t paszy na rok. |
| 4 | „Mogą być kozy”. | Projekt zostawia 2 kozy mleczne. |
| 5 | Wyniki badań gleby istnieją (wiadomość z 2025-04-08). | Projekt czeka na plik z wynikami. Sekcja 5 dokumentu używa klas V i VI z ewidencji. |
| 6 | Studnia stoi przed domem i ma 8 m głębokości. | Wysokość podnoszenia pompy: od 51 m do 61 m zamiast od 55 m do 65 m. Moc pompy: od 0,87 kW do 1,04 kW. |
| 7 | Kocioł: Atmos DC18S. | Założenie R3 staje się relacją właściciela. |
| 8 | Wzniesienie w strefie S2 to gruzowisko. | Projekt usuwa gruz przed budową stelaża. Zbiornik W1 nie stoi na gruzowisku K. |
| 9 | Drzewa mają od 20 do 50 lat. | Pozysk drewna: od 10 mp do 17 mp na rok. |
| 10 | „Bierz o 50% mniejszą uwagę do prawa”. | Sekcja 17 dokumentu ma 11 pozycji zamiast 24 pozycji. |

`H = H_geo + 10,2 × p + h_f + h_uzd`

- H: wysokość podnoszenia pompy [m]. H_geo = 8 m: głębokość studni. p: nadciśnienie w zbiorniku przeponowym, od 3,0 bar do 4,0 bar `[założenie: R3]`.
- h_f = 4,4 m: strata w rurze. h_uzd = 8 m: strata na filtrach `[założenie: R3]`.
- Wynik: H = 8 + 30,6 + 4,4 + 8 = 51,0 m dla 3,0 bar; H = 8 + 40,8 + 4,4 + 8 = 61,2 m dla 4,0 bar.

`P = ρ × g × Q × H / η`

- P: moc elektryczna pompy [W]. ρ = 1000 kg/m³. g = 9,81 m/s². Q = 2,5 m³/h = 0,000694 m³/s. η = 0,40 `[założenie: R3]`.
- Wynik: P = 868 W dla H = 51,0 m; P = 1 042 W dla H = 61,2 m. Energia pompowania: od 0,35 kWh do 0,42 kWh na 1 m³ wody.

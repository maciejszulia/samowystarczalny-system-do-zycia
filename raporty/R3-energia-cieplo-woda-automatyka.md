# R3. Raport agenta 3: energia elektryczna, ciepło, woda pitna, magazyny, automatyzacja

> Raport pokazuje stan sprzed odpowiedzi właściciela z 2026-11-11. Zmiany zawiera raport R4, sekcja 9.

- Data raportu: 2026-11-11.
- Gospodarstwo: Olsztyn-Gutkowo, północno-zachodni brzeg jeziora Ukiel. Środek gospodarstwa: 53,7875° N, 20,4020° E `[relacja: koordynator, 2026-11-11]`.
- Powierzchnia: 4,27 ha. Las 1,82 ha (działka 16/3, drzewostan 1,35 ha). Siedlisko z polem 1,17 ha (działka 16/1). Kemping 1,10 ha (działka 24/1). Pas przy drodze 0,18 ha `[relacja: koordynator, 2026-11-11]`.
- Wariant główny: 4 osoby, pełne odcięcie od sieci elektrycznej. Raport podaje warianty 2 i 6 osób skrótowo.
- Stan w dniu raportu: własna studnia; kocioł zgazowujący klasy Atmos DC18; bufory 1 × 1000 dm³ i 2 × 500 dm³; brak fotowoltaiki `[relacja: koordynator, 2026-11-11]`.
- Raport pomija zużycie kempingu.
- Punkt danych słonecznych: 53,7625° N, 20,4667° E. Punkt leży 5,1 km od środka gospodarstwa `[obliczenie: 09]`. Raport nie pobierał danych ponownie.
- Skrypty obliczeń: katalog `obliczenia/R3/`, pliki od `01_pv_zasob.py` do `10_nawadnianie.py`.

## Legenda

- Raport stosuje Polszczyznę Kontrolowaną (PK). „Lub” znaczy: co najmniej 1 człon. „Albo” znaczy: dokładnie 1 człon.
- MUSI to wymóg. NIE WOLNO to zakaz. POWINIEN to zalecenie. MOŻE to zezwolenie.
- Zapis „A–B” w tabeli znaczy: od A do B włącznie.
- Znacznik `[źródło: Sn]` odsyła do pozycji Sn w sekcji „Źródła”.
- Znacznik `[obliczenie: nn]` odsyła do skryptu o numerze nn.
- Znacznik `[założenie]` oznacza szacunek autora bez sprawdzenia w źródle.
- Znacznik `[relacja: koordynator, 2026-11-11]` oznacza daną od zleceniodawcy.
- Znacznik `[DO USTALENIA: …]` oznacza brak danej.
- Ceny są cenami orientacyjnymi w PLN brutto dla roku 2026.

## Słownik

| Termin | Definicja |
|---|---|
| P50 | Uzysk fotowoltaiki równy średniej wieloletniej z bazy Global Solar Atlas. |
| scenariusz konserwatywny | Uzysk fotowoltaiki pomniejszony współczynnikiem miesięcznym: 0,50 w miesiącach XI–II; 0,75 w III i X; 0,90 w IV–IX. |
| scenariusz S, M, L | Roczne zużycie energii elektrycznej: S = 3000 kWh (2 osoby), M = 5000 kWh (4 osoby), L = 8000 kWh (6 osób z chłodnią). |
| tryb zimowy | Ograniczenie zużycia w miesiącach XI–II do 8,0 kWh na dobę (scenariusz M). |
| samowystarczalność | Udział zużycia energii elektrycznej pokryty bez sieci i bez agregatu, w procentach. |
| mp | Metr przestrzenny: 1 m³ drewna ułożonego w stos, z pustkami. |
| wilgotność drewna w | Udział masy wody w masie drewna mokrego, w procentach. |
| EU | Wskaźnik rocznego zapotrzebowania na energię użytkową do ogrzewania, w kWh/(m²·rok). |
| bufor | Zbiornik wody grzewczej, który magazynuje ciepło z kotła. |
| nadciśnienie | Ciśnienie mierzone względem ciśnienia atmosferycznego. Ciśnienie absolutne = nadciśnienie + 1,0 bar. |
| OSD | Operator systemu dystrybucyjnego. |
| PSP | Państwowa Straż Pożarna. |
| HA | Home Assistant, program serwera automatyki. |

## Streszczenie ustaleń

1. Fotowoltaika 1 kWp daje 1056 kWh/rok w scenariuszu P50 i 871 kWh/rok w scenariuszu konserwatywnym (kąt 35°) `[obliczenie: 01]`.
2. Grudzień daje 22,8 kWh/kWp w scenariuszu P50 i 11,4 kWh/kWp w scenariuszu konserwatywnym `[obliczenie: 01]`.
3. Konfiguracja główna off-grid: fotowoltaika 15 kWp pod kątem 65°, magazyn LiFePO4 30 kWh, agregat 3 kVA, tryb zimowy `[obliczenie: 08]`.
4. Agregat pracuje 11 h/rok w scenariuszu P50 i 124 h/rok w scenariuszu konserwatywnym. Zużycie benzyny wynosi 13 dm³ i 151 dm³ na rok `[obliczenie: 08]`.
5. Bez trybu zimowego agregat pracuje od 134 h do 403 h na rok i zużywa od 162 dm³ do 488 dm³ benzyny `[obliczenie: 08]`.
6. Magazyn 30 kWh zasila dom w trybie zimowym przez 3,3 doby serii bez słońca w grudniu `[obliczenie: 08]`.
7. Bufory 2000 dm³ mieszczą 102,9 kWh przy schłodzeniu z 85 °C do 40 °C. Naczynie przeponowe: 300 dm³ `[obliczenie: 09]`.
8. Drzewostan 1,35 ha daje trwale od 8,7 mp do 14,5 mp drewna na rok `[obliczenie: 09, założenie]`.
9. Drzewostan 1,35 ha pokrywa 100 % ciepła domu 160 m² dopiero przy EU od 47 do 89 kWh/(m²·rok) `[obliczenie: 09]`.
10. Warzywnik 1000 m² na piasku gliniastym wymaga 256 m³ wody na sezon. Zakres wynosi od 218 m³ do 294 m³ `[obliczenie: 10]`.
11. Pobór ze studni wynosi 2,39 m³ na dobę średnio w roku suchym. Limit zwykłego korzystania z wód wynosi 5 m³ na dobę `[obliczenie: 10; relacja: koordynator, 2026-11-11]`.
12. Prawo wymaga kontroli zwierząt co najmniej 1 raz na dobę `[źródło: S51, S53; relacja: koordynator, 2026-11-11]`.
13. Praca po automatyzacji wynosi od 1099 h do 2354 h na rok z kozami i z pszczołami `[obliczenie: 07, założenie]`.
14. Koszt całej infrastruktury wynosi od 203 800 PLN do 502 000 PLN `[obliczenie: 07, założenie]`.

# A. Energia elektryczna

## A1. Zasób słoneczny

### A1.1. Stan źródeł

- Interfejs PVGIS odrzucił zapytanie narzędzia (błąd „robots_disallowed”). Raport nie zawiera danych PVGIS `[DO USTALENIA: uzyski PVGIS dla kątów 35° i 65°]`.
- Raport używa bazy Global Solar Atlas (Solargis, Bank Światowy) dla punktu 53,7625° N, 20,4667° E `[źródło: S1]`.
- Raport używa typowego roku meteorologicznego stacji Olsztyn z lat 1971–2000 `[źródło: S2]`.
- Raport używa pomiaru 2 instalacji w województwie warmińsko-mazurskim z roku 2017 `[źródło: S3]`.

### A1.2. Dane źródłowe

- Global Solar Atlas podaje dla kąta 38° i azymutu południowego uzysk 1054,5 kWh/kWp na rok `[źródło: S1]`.
- Global Solar Atlas podaje napromieniowanie poziome 1049,8 kWh/m² na rok `[źródło: S1]`.
- Typowy rok meteorologiczny podaje napromieniowanie poziome 883,4 kWh/m² na rok, czyli o 15,9 % mniej `[źródło: S2; obliczenie: 01]`.
- Instalacja w Myślętach (39,78 kWp, dach 30°, azymut południowo-zachodni) dała w roku 2017 uzysk 879 kWh/kWp `[źródło: S3]`.
- Instalacja w Wyrandach (39,52 kWp, dach 20°, układ wschód–zachód) dała w roku 2017 uzysk 789 kWh/kWp `[źródło: S3]`.
- Model PVGIS zawyżył uzysk roczny tych 2 instalacji o 12,4 % i o 7,8 % `[źródło: S3]`.

### A1.3. Metoda przeliczenia na inne kąty

Raport przelicza dane Global Solar Atlas na kąty 35°, 65° i 90° modelem izotropowym Liu–Jordana w ujęciu miesięcznym Kleina.

`H_T = H_b·R_b + H_d·(1 + cos β)/2 + H·ρ·(1 − cos β)/2`

`R_b = [cos(φ − β)·cos δ·sin ω′ + ω′·sin(φ − β)·sin δ] / [cos φ·cos δ·sin ω + ω·sin φ·sin δ]`

`Y(β) = Y(38°)·H_T(β)/H_T(38°)`

- H_T: napromieniowanie płaszczyzny pochylonej [kWh/m² na miesiąc].
- H: napromieniowanie poziome całkowite [kWh/m² na miesiąc]. H_d: część rozproszona. H_b = H − H_d: część bezpośrednia.
- R_b: stosunek promieniowania bezpośredniego na płaszczyznę pochyloną do promieniowania bezpośredniego na poziom [–].
- β: kąt pochylenia paneli [°]. φ = 53,7625°: szerokość geograficzna. δ: deklinacja Słońca dla dnia reprezentatywnego [°].
- ω: kąt godzinny zachodu Słońca dla poziomu [rad]. ω′: kąt godzinny zachodu Słońca dla płaszczyzny pochylonej [rad].
- ρ = 0,20: albedo gruntu bez śniegu `[założenie]`.
- Y: uzysk jednostkowy [kWh/kWp na miesiąc].

Kontrola modelu: model daje dla kąta 38° napromieniowanie o 5,7 % mniejsze od wartości Global Solar Atlas `[obliczenie: 01]`. Raport używa tylko ilorazu H_T(β)/H_T(38°).

### A1.4. Uzyski miesięczne

Tabela A1. Uzysk jednostkowy [kWh/kWp na miesiąc], azymut południowy `[obliczenie: 01; źródło: S1, S2, S3]`.

| Miesiąc | P50, 35° | P50, 65° | P50, 90° | Konserwatywny, 35° | Konserwatywny, 65° | Pomiar 2017, 30° |
|---|---|---|---|---|---|---|
| I | 31,8 | 37,2 | 35,6 | 15,9 | 16,9 | 18,1 |
| II | 52,7 | 57,2 | 52,1 | 26,3 | 28,9 | 26,1 |
| III | 95,7 | 95,1 | 80,4 | 71,7 | 73,9 | brak |
| IV | 121,5 | 108,1 | 82,8 | 109,3 | 105,9 | brak |
| V | 141,4 | 116,7 | 83,4 | 127,3 | 115,7 | brak |
| VI | 134,9 | 108,0 | 75,6 | 121,4 | 111,2 | brak |
| VII | 132,4 | 107,6 | 76,5 | 119,2 | 109,2 | brak |
| VIII | 126,4 | 108,7 | 80,8 | 113,7 | 108,0 | brak |
| IX | 99,5 | 94,4 | 76,7 | 89,6 | 88,6 | brak |
| X | 66,6 | 70,3 | 62,7 | 50,0 | 52,6 | brak |
| XI | 29,8 | 33,2 | 31,0 | 14,9 | 16,3 | 14,8 |
| XII | 22,8 | 26,9 | 26,0 | 11,4 | 11,5 | 11,3 |
| Rok | 1056 | 963 | 764 | 871 | 839 | 879 |

- Scenariusz konserwatywny odtwarza pomiar z roku 2017: 871 kWh/kWp wobec 879 kWh/kWp `[obliczenie: 01]`.
- Stosunek pomiaru z roku 2017 do wartości Global Solar Atlas wynosi od 0,48 do 0,55 w miesiącach XI–II `[obliczenie: 01]`.
- Kąt 65° zwiększa uzysk miesięcy XI–II z 137,1 kWh/kWp do 154,5 kWh/kWp w scenariuszu P50, czyli o 17,4 kWh/kWp (12,7 %) `[obliczenie: 01]`.
- Kąt 65° zmniejsza uzysk roczny z 1056 kWh/kWp do 963 kWh/kWp, czyli o 93 kWh/kWp (8,8 %) `[obliczenie: 01]`.
- Typowy rok meteorologiczny daje dla grudnia stosunek uzysku 60° do 30° równy 1,015 `[źródło: S2; obliczenie: 01]`.
- Wniosek: w pochmurnym grudniu kąt 65° nie zwiększa uzysku. Kąt 65° ogranicza zaleganie śniegu `[założenie]`.

### A1.5. Serie dni bez słońca w grudniu i w styczniu

- Raport nie znalazł statystyki długości serii dni bezsłonecznych dla Olsztyna `[DO USTALENIA: rozkład długości serii, dane dobowe IMGW]`.
- Usłonecznienie względne zimą w północno-wschodniej Polsce jest mniejsze niż 15 % `[źródło: S6]`.
- W grudniu 2024 r. stacja Suwałki zanotowała 12,3 h słońca, Białystok 23,4 h, Mława 25,9 h `[źródło: S5]`. Biuletyn nie podaje wartości dla Olsztyna.
- W dniach od 2024-12-21 do 2024-12-31 stacje Suwałki i Kołobrzeg zanotowały po 24 min słońca w ciągu 11 dni `[źródło: S4]`.
- Stacja Lipnik koło Stargardu zanotowała w latach 2000–2004 średnio 91 dni bezsłonecznych na rok, w tym 45 % zimą `[źródło: S61]`.
- Raport przyjmuje do projektu serię 11 dni z uzyskiem równym 20 % średniej miesięcznej scenariusza konserwatywnego `[założenie]`.

## A2. Profil zużycia

Wzór energii pompowania: `E = ρ·g·H·V/(η·3,6·10⁶)`

- E: energia elektryczna [kWh]. ρ = 1000 kg/m³. g = 9,81 m/s². H = 45 m: wysokość podnoszenia `[założenie]`.
- V: objętość wody [m³]. η = 0,35: sprawność całkowita pompy głębinowej `[założenie]`.
- Wynik: 0,350 kWh/m³ `[obliczenie: 02]`.

Tabela A2. Odbiorniki i roczne zużycie [kWh/rok]. Wariant główny: scenariusz M `[obliczenie: 02]`.

| Odbiornik | S | M | L | Znacznik |
|---|---|---|---|---|
| Lodówko-zamrażarka | 160 | 200 | 250 | `[założenie]` |
| Zamrażarki skrzyniowe: 287 dm³ = 227 kWh/rok; 497 dm³ = 295 kWh/rok | 227 | 522 | 817 | `[źródło: S47, S48]` |
| Oświetlenie LED domu i obejścia | 150 | 250 | 350 | `[założenie]` |
| Gotowanie: płyta, piekarnik, czajnik | 250 | 550 | 800 | `[założenie]` |
| Pralka i zmywarka | 200 | 380 | 550 | `[założenie]` |
| Elektronika i praca zdalna | 400 | 550 | 737 | `[założenie]` |
| Drobne urządzenia i czuwanie | 150 | 250 | 400 | `[założenie]` |
| Kocioł Atmos: wentylator 50 W, czuwanie 3 W | 61 | 81 | 113 | `[źródło: S27; obliczenie: 02]` |
| Pompy obiegowe i pompa ładowania bufora | 153 | 179 | 275 | `[założenie]` |
| Pompa głębinowa: woda bytowa i zwierzęta | 31 | 59 | 88 | `[obliczenie: 02]` |
| Pompa głębinowa: podlewanie 150, 300, 600 m³ | 53 | 105 | 210 | `[obliczenie: 02]` |
| Lampa UV (20–30 W, praca ciągła) i sterownik | 200 | 290 | 290 | `[założenie]` |
| Kurnik: oświetlenie LED 20 W przez 946 h/rok | 19 | 19 | 19 | `[obliczenie: 02]` |
| Kurnik: ochrona poideł przed mrozem | 80 | 150 | 250 | `[założenie]` |
| Elektryzator ogrodzenia 5 W | 44 | 44 | 44 | `[założenie]` |
| Kurnik: wentylator letni i paszociąg | 0 | 56 | 56 | `[założenie]` |
| Automatyka: serwer HA, sieć, kamery, węzły ESP32 | 250 | 420 | 535 | `[założenie]` |
| Rozsada: maty grzewcze i lampy LED | 60 | 150 | 250 | `[założenie]` |
| Tunel: sterowanie i wietrzenie | 10 | 30 | 60 | `[założenie]` |
| Robot koszący | 0 | 60 | 100 | `[założenie]` |
| Warsztat, łuparka, narzędzia | 60 | 150 | 300 | `[założenie]` |
| Przetwórstwo: suszarka, pasteryzacja | 50 | 120 | 250 | `[założenie]` |
| Chłodnia 6 m³, praca w miesiącach VIII–IV | 0 | 0 | 900 | `[założenie]` |
| Oczyszczalnia przydomowa: dmuchawa 40 W | 0 | 0 | 350 | `[założenie]` |
| Rezerwa (kozy, dojarka, schładzanie mleka) | 392 | 385 | 6 | `[obliczenie: 02]` |
| Suma | 3000 | 5000 | 8000 | `[obliczenie: 02]` |

Tabela A3. Rozkład miesięczny zużycia [kWh na miesiąc], tryb normalny `[obliczenie: 02]`.

| Scenariusz | I | II | III | IV | V | VI | VII | VIII | IX | X | XI | XII | Rok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S | 284 | 263 | 285 | 247 | 214 | 216 | 231 | 239 | 226 | 256 | 258 | 282 | 3000 |
| M | 444 | 422 | 472 | 422 | 374 | 381 | 410 | 427 | 391 | 411 | 405 | 441 | 5000 |
| L | 620 | 598 | 713 | 731 | 523 | 543 | 595 | 939 | 786 | 721 | 616 | 614 | 8000 |

- Scenariusz M zużywa w grudniu 14,2 kWh na dobę w trybie normalnym `[obliczenie: 02]`.
- Właściciel POWINIEN mierzyć zużycie każdego obwodu licznikiem przez 12 miesięcy `[założenie]`.

## A3. Wariant główny (c): pełny off-grid dla 4 osób

### A3.1. Model

Skrypt 08 symuluje 30 lat z krokiem 1 doby `[obliczenie: 08]`.

`E_bezp = min(E_PV, f·L)`

`SOC₁ = SOC₀ + η_c·min(E_PV − E_bezp, (C_u − SOC₀)/η_c)`

`E_bat = min(L − E_bezp, SOC₁·η_d)`

`E_agr = E_brak + E_ład`

`t_agr = E_agr/P_agr`

`V_pal = 0,51·E_agr`

- E_PV: produkcja doby [kWh]. L: zużycie doby [kWh]. E_bezp: zużycie bezpośrednie [kWh].
- f = min(0,65; 0,15 + 0,03·t_d): udział zużycia w godzinach pracy fotowoltaiki. t_d: długość dnia [h] `[założenie]`.
- SOC: energia w magazynie [kWh]. C_u = 0,90·C_n: pojemność użyteczna. C_n: pojemność nominalna [kWh] `[założenie]`.
- η_c = η_d = 0,95: sprawność ładowania i sprawność rozładowania `[założenie]`.
- E_bat: energia z magazynu [kWh]. E_brak: niedobór doby [kWh].
- E_agr: energia na zaciskach agregatu [kWh]. E_ład: energia doładowania magazynu do 60 % pojemności użytecznej [kWh].
- P_agr = 2,4 kW: moc pracy agregatu 3 kVA `[założenie]`. Agregat pracuje co najwyżej 6 h na dobę `[założenie]`.
- t_agr: czas pracy agregatu [h]. V_pal: benzyna [dm³]; 0,51 dm³/kWh `[źródło: S23; obliczenie: 03]`.
- Straty własne falownika i układu BMS: 40 W, czyli 0,96 kWh na dobę `[założenie]`.
- Zmienność uzysku dobowego: rozkład logarytmiczno-normalny, współczynnik zmienności 0,90 w miesiącach XI–II, autokorelacja 0,4 `[założenie]`.

Ograniczenie modelu: raport nie ma danych dobowych PVGIS `[DO USTALENIA: kalibracja zmienności na danych dobowych]`.

### A3.2. Tryb zimowy: redukcja zużycia w miesiącach XI–II

Tabela A4. Odbiorniki trybu zimowego, 4 osoby `[obliczenie: 08, założenie]`.

| Odbiornik | Moc | Czas na dobę | Energia na dobę |
|---|---|---|---|
| 2 zamrażarki w pomieszczeniu od 5 °C do 10 °C | 38 W | 24 h | 0,91 kWh |
| Lodówko-zamrażarka | 21 W | 24 h | 0,50 kWh |
| Oświetlenie LED domu | 110 W | 8 h | 0,88 kWh |
| Gotowanie elektryczne (reszta na kuchni drzewnej lub na LPG) | 300 W | 1 h | 0,30 kWh |
| Pralka (4 cykle na tydzień) i zmywarka zasilana ciepłą wodą | 650 W | 1 h | 0,65 kWh |
| Laptopy, router, telefony | 100 W | 8 h | 0,80 kWh |
| Kocioł: wentylator i pompa ładowania | 50 W | 11 h | 0,55 kWh |
| Pompy obiegowe 2 × 10 W | 20 W | 24 h | 0,48 kWh |
| Pompa głębinowa, 0,5 m³ na dobę | 1100 W | 0,2 h | 0,22 kWh |
| Lampa UV 16 W na linii wody pitnej | 16 W | 24 h | 0,38 kWh |
| Serwer HA, sieć, węzły ESP32, 1 kamera | 36 W | 24 h | 0,86 kWh |
| Kurnik: LED | 20 W | 6 h | 0,12 kWh |
| Ochrona poideł: izolacja i grzałki z termostatem | 30 W | 24 h | 0,72 kWh |
| Elektryzator | 5 W | 24 h | 0,12 kWh |
| Drobne urządzenia i czuwanie | 20 W | 24 h | 0,48 kWh |
| Suma | brak | brak | 7,98 kWh |

- Tryb zimowy zmniejsza zużycie doby z 14,2 kWh do 8,0 kWh, czyli o 6,2 kWh (44 %) `[obliczenie: 08]`.
- Zużycie roczne spada z 5000 kWh do 4248 kWh `[obliczenie: 08]`.
- Tryb zimowy przenosi gotowanie na kuchnię drzewną lub na LPG i wyłącza czajnik elektryczny.

### A3.3. Dobór mocy fotowoltaiki i pojemności magazynu

Tabela A5. Energia z agregatu [kWh/rok]: średnia z 30 lat i największa wartość roczna w nawiasie. Panele 65° `[obliczenie: 08]`.

| Fotowoltaika | Tryb zimowy, konserwatywny, 20 kWh | Tryb zimowy, konserwatywny, 30 kWh | Tryb zimowy, konserwatywny, 40 kWh | Tryb zimowy, P50, 30 kWh | Tryb normalny, konserwatywny, 30 kWh | Tryb normalny, P50, 30 kWh |
|---|---|---|---|---|---|---|
| 10 kWp | 647 (823) | 571 (749) | 529 (706) | 122 (216) | 1321 (1483) | 629 (778) |
| 12 kWp | 518 (657) | 439 (605) | 393 (547) | 63 (130) | 1159 (1368) | 475 (619) |
| 15 kWp | 373 (500) | 299 (432) | 264 (374) | 26 (86) | 966 (1152) | 321 (461) |
| 18 kWp | 270 (365) | 208 (317) | 172 (274) | 10 (43) | 815 (994) | 212 (317) |
| 20 kWp | 226 (316) | 161 (274) | 127 (216) | 7 (29) | 730 (878) | 165 (288) |
| 25 kWp | 142 (215) | 86 (173) | 60 (158) | 1 (14) | 552 (691) | 87 (187) |

- Wniosek 1: tryb zimowy zmniejsza energię z agregatu z 966 kWh do 299 kWh na rok przy 15 kWp i 30 kWh `[obliczenie: 08]`.
- Wniosek 2: zmiana magazynu z 30 kWh na 40 kWh zmniejsza energię z agregatu z 299 kWh do 264 kWh na rok.
- Wniosek 3: zmiana fotowoltaiki z 15 kWp na 20 kWp zmniejsza energię z agregatu z 299 kWh do 161 kWh na rok.
- Wniosek 4: magazyn 30 kWh nie wymaga formalności budowlanych `[relacja: koordynator, 2026-11-11]`.
- Raport wybiera konfigurację główną: 15 kWp, 30 kWh, agregat 3 kVA, tryb zimowy.

### A3.4. Konfiguracja główna: bilans miesięczny

Tabela A6. 15 kWp (65°, południe), 30 kWh, tryb zimowy, scenariusz konserwatywny [kWh] `[obliczenie: 08]`.

| Miesiąc | Produkcja | Zużycie | Bezpośrednio | Z magazynu | Z agregatu | Nadwyżka bez odbioru |
|---|---|---|---|---|---|---|
| I | 254 | 277 | 99 | 163 | 77 | 28 |
| II | 434 | 250 | 107 | 142 | 9 | 172 |
| III | 1109 | 502 | 248 | 252 | 6 | 585 |
| IV | 1588 | 451 | 254 | 197 | 0 | 1114 |
| V | 1736 | 404 | 251 | 153 | 0 | 1314 |
| VI | 1667 | 410 | 266 | 143 | 0 | 1242 |
| VII | 1637 | 440 | 280 | 159 | 0 | 1181 |
| VIII | 1620 | 457 | 268 | 189 | 0 | 1144 |
| IX | 1330 | 419 | 219 | 200 | 0 | 889 |
| X | 788 | 441 | 200 | 239 | 10 | 336 |
| XI | 244 | 268 | 99 | 156 | 67 | 28 |
| XII | 173 | 277 | 88 | 160 | 130 | 7 |
| Rok | 12 582 | 4597 | 2380 | 2155 | 299 | 8039 |

- Zużycie w tabeli A6 zawiera straty własne falownika 350 kWh na rok.
- W scenariuszu P50 produkcja wynosi 14 451 kWh, a agregat daje 26 kWh na rok: XII 16 kWh, XI 5 kWh, I 4 kWh `[obliczenie: 08]`.
- Agregat pokrywa 6,5 % zużycia w scenariuszu konserwatywnym i 0,6 % w scenariuszu P50 `[obliczenie: 08]`.

### A3.5. Bilans dobowy grudnia i stycznia

Zużycie doby w trybie zimowym wynosi 8,94 kWh ze stratami własnymi `[obliczenie: 08]`.

Tabela A7. Bilans doby dla 15 kWp i 30 kWh [kWh] `[obliczenie: 08]`.

| Miesiąc i rodzaj doby | Uzysk [kWh/kWp] | Produkcja | Bezpośrednio | Do magazynu | Potrzeba z magazynu | Saldo doby |
|---|---|---|---|---|---|---|
| XII, doba pochmurna | 0,07 | 1,1 | 1,1 | 0,0 | 7,8 | −7,8 |
| XII, doba średnia, konserwatywny | 0,37 | 5,6 | 3,3 | 2,3 | 5,7 | −3,6 |
| XII, doba średnia, P50 | 0,87 | 13,0 | 3,3 | 9,7 | 5,7 | +3,1 |
| XII, doba bezchmurna | 2,31 | 34,7 | 3,3 | 31,4 | 5,7 | +22,6 |
| I, doba pochmurna | 0,11 | 1,6 | 1,6 | 0,0 | 7,3 | −7,3 |
| I, doba średnia, konserwatywny | 0,55 | 8,2 | 3,4 | 4,8 | 5,5 | −1,2 |
| I, doba średnia, P50 | 1,20 | 18,0 | 3,4 | 14,5 | 5,5 | +7,6 |
| I, doba bezchmurna | 2,73 | 41,0 | 3,4 | 37,5 | 5,5 | +28,3 |

- Doba pochmurna oznacza uzysk równy 20 % średniej scenariusza konserwatywnego `[założenie]`.
- Uzysk doby bezchmurnej jest szacunkiem `[założenie]`.
- Podział doby grudnia: noc 1,8 kWh; rano 1,5 kWh; godziny 09:00–15:00 2,4 kWh; wieczór 3,3 kWh `[założenie]`.
- 1 doba bezchmurna ładuje magazyn 30 kWh od 0 % do 100 %.

### A3.6. Serie dni bez słońca

`E_seria = N·(L − E_PV) − C_u·η_d`

- E_seria: energia z agregatu w serii [kWh]. N: liczba dni serii. L = 8,94 kWh: zużycie doby. E_PV: produkcja doby pochmurnej [kWh].
- C_u·η_d = 25,6 kWh: energia magazynu 30 kWh na wyjściu `[obliczenie: 08]`.

Tabela A8. Seria dni pochmurnych, magazyn pełny na początku serii `[obliczenie: 08]`.

| Długość serii | XII: energia z agregatu | XII: czas pracy | XII: benzyna | I: energia z agregatu | I: czas pracy | I: benzyna |
|---|---|---|---|---|---|---|
| 3 dni | 0 kWh | 0 h | 0 dm³ | 0 kWh | 0 h | 0 dm³ |
| 5 dni | 13,5 kWh | 5,6 h | 6,8 dm³ | 10,9 kWh | 4,5 h | 5,5 dm³ |
| 7 dni | 29,1 kWh | 12,1 h | 14,7 dm³ | 25,5 kWh | 10,6 h | 12,9 dm³ |
| 11 dni | 60,5 kWh | 25,2 h | 30,6 dm³ | 54,7 kWh | 22,8 h | 27,7 dm³ |
| 14 dni | 83,9 kWh | 35,0 h | 42,4 dm³ | 76,6 kWh | 31,9 h | 38,7 dm³ |

- Magazyn 30 kWh zasila tryb zimowy przez 3,3 doby serii grudniowej `[obliczenie: 08]`.
- Ten sam magazyn zasila tryb normalny (15,2 kWh na dobę) przez 1,8 doby `[obliczenie: 08]`.

### A3.7. Agregat rezerwowy

Tabela A9. Praca agregatu na rok, konfiguracja główna `[obliczenie: 08]`.

| Wielkość | P50, tryb zimowy | Konserwatywny, tryb zimowy | Największa wartość roczna | Konserwatywny, tryb normalny |
|---|---|---|---|---|
| Energia | 26 kWh | 299 kWh | 432 kWh | 966 kWh |
| Czas pracy | 11 h | 124 h | 180 h | 403 h |
| Benzyna | 13 dm³ | 151 dm³ | 218 dm³ | 488 dm³ |
| LPG | 10 kg | 107 kg | 155 kg | 348 kg |
| Liczba dni pracy | 2 | 21 | 30 | 67 |

- Zużycie LPG przyjmuje sprawność agregatu 22 %, czyli 0,36 kg/kWh `[założenie]`.
- Agregat Honda EU32i ma moc ciągłą 2,6 kVA, zbiornik 4,6 dm³ i czas pracy 3 h 30 min przy mocy znamionowej `[źródło: S23]`.
- Agregat Honda EU32i ma rozruch ręczny `[źródło: S23]`. Automatyka wymaga agregatu z rozruchem elektrycznym `[założenie]`.
- Agregat MUSI pokryć moc ładowarki 2,4 kW i obwody krytyczne w tym samym czasie.
- Zalecenie: agregat inwertorowy od 3 kVA do 5 kVA na LPG, z rozruchem elektrycznym. LPG nie starzeje się w butli `[założenie]`.
- Zapas paliwa na najgorszy rok: 218 dm³ benzyny albo 155 kg LPG (15 butli po 11 kg) `[obliczenie: 08]`.
- Gazogenerator Power Pallet PP30 zużywa 1,0 kg suchej biomasy na 1 kWh i ma moc od 18 kW do 22 kW `[źródło: S24]`.
- Wniosek: gazogenerator ma moc 7 razy większą od potrzeby i wymaga obsługi przy każdym rozruchu. Raport nie zaleca gazogeneratora.

### A3.8. Zarządzanie obciążeniami

Tabela A10. Klasy odbiorników `[założenie]`.

| Klasa | Odbiorniki | Reguła |
|---|---|---|
| 1, krytyczna | Zamrażarki, lodówka, pompy kotła, pompa głębinowa, serwer HA, sieć, oświetlenie, elektryzator | Zasilanie przez całą dobę. |
| 2, przesuwalna | Pralka, zmywarka, płukanie odżelaziacza, pompa podlewania, grzałka ciepłej wody, suszarka, łuparka, robot | Praca tylko w godzinach 10:00–15:00 albo przy SOC większym niż 70 %. |
| 3, zrzucana | Płyta i piekarnik, czajnik, lampy rozsady, chłodnia, 3 z 4 kamer, grzałki bufora | Wyłączenie przy SOC mniejszym niż 30 %. |

Progi sterowania `[założenie]`:

1. Jeżeli SOC jest większy niż 90 %, to sterownik włącza grzałkę ciepłej wody 3 kW.
2. Jeżeli SOC jest większy niż 95 % i zasobnik ma 65 °C, to sterownik włącza grzałki bufora.
3. Jeżeli SOC jest mniejszy niż 50 %, to sterownik blokuje klasę 2 po godzinie 15:00.
4. Jeżeli SOC jest mniejszy niż 30 %, to sterownik wyłącza klasę 3.
5. Jeżeli SOC jest mniejszy niż 15 %, to sterownik uruchamia agregat.
6. Gdy SOC osiągnie 60 %, sterownik wyłącza agregat.
7. Jeżeli prognoza produkcji na 2 doby jest większa niż zużycie 2 dób, to sterownik odracza start agregatu do SOC 10 %.

- Falownik wykonuje progi 4, 5 i 6 samodzielnie. Serwer HA wykonuje progi 1, 2, 3 i 7.
- Zamrażarki schładzają zapas do −24 °C w godzinach 10:00–15:00. Ten zapas chłodu skraca pracę sprężarek nocą `[założenie]`.

### A3.9. Elementy instalacji

- Fotowoltaika 15 kWp to 33 moduły po 455 Wp `[obliczenie: 08]`.
- Stół o kącie 65° z 2 modułami w poziomie ma wysokość 2,06 m i długość 30 m `[obliczenie: 08]`.
- Słońce stoi w południe 21 grudnia na wysokości 12,8° `[obliczenie: 08]`.
- Przeszkoda o wysokości H rzuca wtedy cień o długości 4,4·H. Drzewa 20 m rzucają cień 88 m `[obliczenie: 08]`.
- Drugi rząd stołów wymaga odstępu 9,1 m `[obliczenie: 08]`.
- Stok działki 24/1 ma ekspozycję od południowej do południowo-wschodniej i spadek 12 % `[relacja: koordynator, 2026-11-11]`.
- Wniosek: 1 rząd stołów na stoku albo na polu działki 16/1, co najmniej 88 m na północ od ściany lasu `[DO USTALENIA: położenie lasu względem stołów]`.
- Falownik: wyspowy z ładowarką, z wejściem agregatu i ze stykiem startu agregatu. Moc ciągła od 8 kW do 10 kW `[założenie]`.
- Magazyn LiFePO4 POWINIEN stać w pomieszczeniu o temperaturze większej niż 5 °C `[założenie; DO USTALENIA: zakres temperatury ładowania z karty magazynu]`.
- Moduł Pylontech US5000 ma 48 V, 100 Ah, 4,8 kWh i trwałość co najmniej 6000 cykli `[źródło: S25]`. Magazyn 30 kWh to 6 takich modułów (28,8 kWh).
- Instalacja większa niż 6,5 kW wymaga uzgodnienia przeciwpożarowego i zawiadomienia PSP `[źródło: S16; relacja: koordynator, 2026-11-11]`.
- Instalacja off-grid bez połączenia z siecią nie wymaga zgłoszenia do OSD `[założenie; DO USTALENIA: rozdział instalacji domu i kempingu]`.
- Koszt konfiguracji głównej wynosi od 89 500 PLN do 176 500 PLN `[obliczenie: 07, założenie]`.

### A3.10. Nadwyżka letnia

- Konfiguracja główna ma 8039 kWh nadwyżki bez odbioru na rok w scenariuszu konserwatywnym `[obliczenie: 08]`.
- Miesiące V–IX mają 5769 kWh nadwyżki. Ciepła woda 4 osób zużywa w tym czasie 1692 kWh `[obliczenie: 08]`.
- Miesiące III, IV i X mają 2034 kWh nadwyżki. Grzałki bufora zastępują wtedy 1,7 mp drewna `[obliczenie: 08, 09]`.
- Pompa podlewania zużywa w szczycie 4,3 kWh na dobę przy 2000 m², czyli 8,1 % produkcji lipca `[obliczenie: 10]`.
- Pozostałe odbiory nadwyżki: suszarka żywności, chłodnia, gotowanie, pompowanie wody do zbiornika górnego.

### A3.11. Mała turbina wiatrowa

- Średnia roczna prędkość wiatru w Olsztynie wynosi 2,9 m/s na wysokości 10 m (lata 1991–2010) `[źródło: S8]`.
- Luty ma średnią prędkość 3,3 m/s, a sierpień 2,3 m/s. Cisze stanowią 7,4 % czasu `[źródło: S8]`.
- Badanie IMGW-PIB objęło 173 stacje i turbinę na wysokości 10 m. Średni współczynnik wykorzystania mocy wyniósł 3,75 % `[źródło: S9]`.
- Koszt turbiny wynosił w badaniu od 12 700 PLN do 28 400 PLN na 1 kW `[źródło: S9]`.

`P_śr = 0,5·ρ·A·C_p·(6/π)·v_śr³`

- P_śr: średnia moc turbiny [W]. ρ = 1,225 kg/m³. A: powierzchnia wirnika [m²]. C_p = 0,25: sprawność całkowita `[założenie]`.
- v_śr = 2,9·(h/10)^0,22: średnia prędkość wiatru na wysokości h [m/s]; rozkład Rayleigha `[założenie]`.

- Turbina 3 kW (wirnik 3,6 m) na maszcie 18 m daje 937 kWh na rok. Współczynnik wykorzystania mocy wynosi 3,6 % `[obliczenie: 03]`.
- Turbina zmniejsza energię z agregatu o 336 kWh na rok w trybie normalnym `[obliczenie: 03]`.
- Turbina 3 kW kosztuje od 38 100 PLN do 85 200 PLN `[obliczenie: 03; źródło: S9]`.
- Wiatry zachodnie przeważają `[źródło: S8]`. Jezioro leży na południowy wschód od gospodarstwa i nie poprawia napływu wiatru zachodniego.
- Wniosek: raport nie zaleca turbiny. Właściciel POWINIEN zmierzyć wiatr na szczycie pagórka (118 m n.p.m.) przez 12 miesięcy przed decyzją.

### A3.12. Warianty 2 i 6 osób, off-grid

| Wariant | Fotowoltaika, 65° | Magazyn | Agregat, P50 | Agregat, scenariusz konserwatywny | Koszt |
|---|---|---|---|---|---|
| 2 osoby (S), tryb normalny | 10 kWp | 20 kWh | 156 kWh/rok | 550 kWh/rok | 64 500–130 000 PLN |
| 2 osoby (S), tryb zimowy 6,0 kWh na dobę | 12 kWp | 30 kWh | 1 kWh/rok | 88 kWh/rok | brak danej |
| 6 osób (L), tryb normalny | 25 kWp | 40 kWh | 232 kWh/rok | 1029 kWh/rok | 132 500–257 500 PLN |

Znacznik tabeli: `[obliczenie: 03, 07]`. Magazyn 40 kWh wymaga zgłoszenia z uzgodnieniem przeciwpożarowym `[relacja: koordynator, 2026-11-11]`.

### A3.13. Warianty (a) i (b): odniesienie kosztowe

Tabela A11. Warianty z siecią, scenariusz M, panele 35° `[obliczenie: 03, 07]`.

| Wariant | Fotowoltaika | Magazyn | Pobór z sieci, P50 | Nadwyżka, P50 | Samowystarczalność, P50 | Samowystarczalność, konserwatywny | Koszt |
|---|---|---|---|---|---|---|---|
| (a) on-grid, net-billing, zasilanie awaryjne | 5 kWp | 10 kWh | 1534 kWh/rok | 1309 kWh/rok | 71,4 % | 61,9 % | 32 500–60 500 PLN |
| (b) autonomia bilansowa, sieć jako rezerwa | 10 kWp | 20 kWh | 708 kWh/rok | 5691 kWh/rok | 86,8 % | 76,2 % | 57 500–107 000 PLN |
| (c) off-grid, wariant główny | 15 kWp | 30 kWh | 0 | 8039 kWh/rok bez odbioru | 99,4 % | 93,5 % | 89 500–176 500 PLN |

- Wariant (b) pobiera z sieci 253 kWh w grudniu i 188 kWh w styczniu `[obliczenie: 03]`.
- Zestaw 10 kWp, falownik hybrydowy 10 kW i magazyn 20 kWh kosztował 52 500 PLN w wersji budżetowej w marcu 2026 r. `[źródło: S21]`.
- Wersja premium tego zestawu kosztowała więcej niż 90 000 PLN `[źródło: S21]`.
- Źródło S22 podaje od 5200 PLN do 6300 PLN za 1 kWp instalacji dachowej bez magazynu `[źródło: S22]`.
- Źródła S21 i S22 dają różny koszt 1 kWp. Raport przyjmuje od 3000 PLN do 5500 PLN za 1 kWp `[założenie]`.

### A3.14. Net-billing i formalności (dla wariantów z siecią)

- Prosument, który pierwszy raz wprowadził energię do sieci po 2024-06-30, rozlicza energię według ceny godzinowej RCE `[źródło: S11, S12]`.
- Ustawa z 2024-11-27 (Dz.U. 2024 poz. 1847) zwiększa wartość depozytu prosumenckiego współczynnikiem 1,23 `[źródło: S10, S11]`.
- Zwrot niewykorzystanych środków wynosi co najwyżej 30 % wartości energii z danego miesiąca przy cenie RCE `[źródło: S11]`.
- Raport nie ustalił zasady rozliczenia godzin z ceną ujemną `[DO USTALENIA: art. 4b ustawy o OZE]`.
- Fotowoltaika o mocy co najwyżej 150 kW nie wymaga pozwolenia na budowę `[relacja: koordynator, 2026-11-11]`.
- Magazyn o pojemności co najwyżej 30 kWh nie wymaga formalności budowlanych `[źródło: S13, S15; relacja: koordynator, 2026-11-11]`.
- Magazyn od 30 kWh do 300 kWh wymaga zgłoszenia z uzgodnieniem przeciwpożarowym `[źródło: S13; relacja: koordynator, 2026-11-11]`.
- Projekt nowych warunków technicznych (WT 2026) nie obowiązywał w dniu 2026-09-01 `[źródło: S15; DO USTALENIA: stan w dniu 2026-11-11]`.
- Energa wymaga zgłoszenia mikroinstalacji najpóźniej 30 dni przed planowanym uruchomieniem `[źródło: S17]`.
- Od 2027-01-01 moduł typu A MUSI mieć certyfikat zgodności z kodeksem NC RfG i z wymogami WOS 2025 `[źródło: S18]`.
- Program „Przydomowe Magazyny Energii” wymaga mikroinstalacji przyłączonej do sieci `[źródło: S19]`. Wariant (c) nie spełnia tego warunku.

# B. Ciepło

## B4. Zapotrzebowanie na ciepło

`Q_co = EU·A`

`Φ_H = Q_co/(S_d·24)·(t_i − t_e)`

`Q_cwu = n·V·ρ·c_p·(t_c − t_z)/3600·365`

- Q_co: roczne ciepło do ogrzewania [kWh/rok]. EU: wskaźnik [kWh/(m²·rok)]. A: powierzchnia ogrzewana [m²].
- Φ_H: projektowe obciążenie cieplne [kW]. S_d = 3698 K·d: stopniodni dla temperatury 20 °C, miesiące X–IV `[obliczenie: 04; źródło: S7]`.
- t_i = 20 °C: temperatura wewnętrzna. t_e = −22 °C: temperatura projektowa strefy IV `[relacja: koordynator, 2026-11-11]`.
- Q_cwu: roczne ciepło netto ciepłej wody [kWh/rok]. n: liczba osób. V = 40 dm³ na osobę na dobę `[założenie]`.
- ρ = 0,99 kg/dm³. c_p = 4,19 kJ/(kg·K). t_z = 10 °C: woda zimna. t_c = 55 °C: woda ciepła.

Tabela B1. Ciepło do ogrzewania Q_co [kWh/rok] i obciążenie Φ_H [kW] przy −22 °C `[obliczenie: 04]`.

| Powierzchnia | EU = 60 | EU = 100 | EU = 150 |
|---|---|---|---|
| 120 m² | 7200; 3,4 kW | 12 000; 5,7 kW | 18 000; 8,5 kW |
| 160 m² | 9600; 4,5 kW | 16 000; 7,6 kW | 24 000; 11,4 kW |
| 200 m² | 12 000; 5,7 kW | 20 000; 9,5 kW | 30 000; 14,2 kW |

Tabela B2. Ciepła woda użytkowa. Wariant główny: 4 osoby `[obliczenie: 04]`.

| Liczba osób | Netto [kWh/rok] | Brutto [kWh/rok] | Brutto na dobę [kWh] | Sezon grzewczy, 225 dni [kWh] | Lato, 140 dni [kWh] |
|---|---|---|---|---|---|
| 2 | 1514 | 2019 | 5,5 | 1244 | 774 |
| 4 | 3028 | 4037 | 11,1 | 2489 | 1549 |
| 6 | 4542 | 6056 | 16,6 | 3733 | 2323 |

- Wartość brutto zawiera straty zasobnika i straty rur. Sprawność magazynowania i rozprowadzenia wynosi 0,75 `[założenie]`.
- Raport nie zna powierzchni domu ani wskaźnika EU `[DO USTALENIA: powierzchnia ogrzewana, zużycie drewna z 2 sezonów]`.

## B5. Drewno z własnego gruntu

### B5.1. Dane producenta kotła Atmos DC18S

| Parametr | Wartość | Znacznik |
|---|---|---|
| Moc nominalna | 20 kW | `[źródło: S26]` |
| Moc doprowadzona w paliwie | 22,2 kW | `[źródło: S26]` |
| Sprawność kotła | 90,1 % | `[źródło: S26, S27]` |
| Druga wartość sprawności przy mocy nominalnej | 82,0 % | `[źródło: S26; DO USTALENIA: definicja tej wartości]` |
| Klasa według PN-EN 303-5 | 5 | `[źródło: S26]` |
| Objętość komory załadowczej | 60 dm³ | `[źródło: S26]` |
| Długość polan | co najwyżej 330 mm | `[źródło: S26]` |
| Wilgotność drewna w | od 12 % do 20 % | `[źródło: S26, S27]` |
| Średnica polan | od 80 mm do 150 mm | `[źródło: S27]` |
| Czas sezonowania | co najmniej 2 lata | `[źródło: S27]` |
| Średnie zużycie drewna | 5,6 kg/h | `[źródło: S27]` |
| Czas spalania ładunku przy mocy nominalnej | 2 h | `[źródło: S26, S27]` |
| Temperatura wody powrotnej | co najmniej 65 °C | `[źródło: S26, S27]` |
| Temperatura wody na wyjściu | od 80 °C do 90 °C | `[źródło: S27]` |
| Nadciśnienie robocze | co najwyżej 2,5 bar | `[źródło: S27]` |
| Zawór bezpieczeństwa w zestawie producenta | 2,5 bar | `[źródło: S62]` |
| Zawór ładujący Laddomat 22: wkładka termostatyczna | 78 °C (wariant 72 °C) | `[źródło: S62]` |
| Pobór mocy: praca; czuwanie | 50 W; 3 W | `[źródło: S27]` |
| Pojemność bufora według tabeli danych | co najmniej 500 dm³ | `[źródło: S26, S27]` |
| Pojemność bufora dla kotłów od 15 kW do 20 kW | od 1000 dm³ do 1500 dm³ | `[źródło: S28]` |
| Reguła producenta | 55 dm³ bufora na 1 kW mocy kotła | `[źródło: S28]` |

- Dane dotyczą modelu DC18S. Raport nie zna dokładnego modelu kotła `[DO USTALENIA: tabliczka znamionowa kotła]`.
- Producent podaje, że bufor zmniejsza zużycie paliwa o 20 % do 30 % `[źródło: S28]`.

### B5.2. Wartość opałowa

`H(w) = H₀·(1 − w) − 0,68·w`

`E_m3 = ρ_s/(1 − w)·H(w)`

`E_mp = E_m3·k`

- H(w): wartość opałowa drewna o wilgotności w [kWh/kg]. w: ułamek masy wody w masie drewna mokrego [–].
- H₀: wartość opałowa suchej masy: 5,20 kWh/kg dla iglastych; 5,00 kWh/kg dla liściastych `[źródło: S29]`.
- 0,68 kWh/kg: ciepło parowania wody `[źródło: S29, S60]`.
- E_m3: energia 1 m³ drewna litego [kWh/m³]. ρ_s: sucha masa w 1 m³ drewna świeżego [kg/m³].
- E_mp: energia 1 mp [kWh/mp]. k = 0,65: udział drewna litego w stosie wałków 1 m `[założenie]`. k = 0,70 dla szczap 33 cm `[źródło: S29, S30]`.

Tabela B3. Wartość opałowa [kWh/kg] `[obliczenie: 04; źródło: S29]`.

| Wilgotność w | 12 % | 15 % | 20 % | 25 % | 35 % | 50 % |
|---|---|---|---|---|---|---|
| Iglaste | 4,49 | 4,32 | 4,02 | 3,73 | 3,14 | 2,26 |
| Liściaste | 4,32 | 4,15 | 3,86 | 3,58 | 3,01 | 2,16 |

Tabela B4. Energia drewna przy w = 20 % `[obliczenie: 04]`.

| Gatunek | ρ_s [kg/m³] | kWh/m³ | kWh/mp, k = 0,65 | kWh/mp, k = 0,70 | Znacznik gęstości |
|---|---|---|---|---|---|
| Sosna | 431 | 2168 | 1409 | 1518 | `[źródło: S29]` |
| Świerk | 379 | 1906 | 1239 | 1334 | `[źródło: S29]` |
| Brzoza | 526 | 2541 | 1651 | 1778 | `[obliczenie: gęstość 0,65 g/cm³ z S31 razy 0,81]` |
| Olsza czarna | 446 | 2154 | 1400 | 1508 | `[obliczenie: gęstość 0,55 g/cm³ z S31 razy 0,81]` |
| Dąb | 571 | 2758 | 1793 | 1931 | `[źródło: S29]` |
| Buk | 558 | 2695 | 1752 | 1887 | `[źródło: S29]` |
| Topola | 353 | 1705 | 1108 | 1193 | `[źródło: S29]` |
| Wierzba | 353 | 1705 | 1108 | 1193 | `[założenie: jak topola]` |
| Robinia | 620 | 2995 | 1946 | 2096 | `[założenie]` |
| Drzewostan mieszany: 30 % sosna, 30 % brzoza, 40 % olsza | brak | 2274 | 1478 | 1592 | `[obliczenie: 09, założenie]` |

- Kontrola: źródło S29 podaje dla sosny 2166 kWh/m³. Skrypt daje 2168 kWh/m³ `[obliczenie: 04]`.
- Drewno o wilgotności 60 % ma wartość opałową 1,5 kWh/kg `[źródło: S27]`.
- Drewno świeże zmniejsza moc kotła o 50 % i podwaja zużycie paliwa `[źródło: S27]`.

### B5.3. Roczne zużycie drewna

`B = (Q_co + Q_cwu,sezon)/η_sez`

- B: energia paliwa [kWh/rok]. Q_cwu,sezon = 2489 kWh: ciepła woda 4 osób w sezonie grzewczym `[obliczenie: 04]`.
- η_sez = 0,78: sprawność sezonowa kotła z buforem `[założenie]`. Zakres od 0,70 do 0,85 zmienia zużycie od +11 % do −8 %.

Tabela B5. Zużycie drewna [mp/rok], wałki 1 m, w = 20 %, 4 osoby `[obliczenie: 04, 09]`.

| Dom: m²; EU | Paliwo [kWh/rok] | Sosna | Brzoza | Olsza | Drzewostan mieszany | Drewno lite, sosna [m³] |
|---|---|---|---|---|---|---|
| 120; 60 | 12 422 | 8,8 | 7,5 | 8,9 | 8,4 | 5,7 |
| 120; 100 | 18 575 | 13,2 | 11,2 | 13,3 | 12,6 | 8,6 |
| 120; 150 | 26 268 | 18,6 | 15,9 | 18,8 | 17,8 | 12,1 |
| 160; 60 | 15 499 | 11,0 | 9,4 | 11,1 | 10,5 | 7,1 |
| 160; 100 | 23 704 | 16,8 | 14,4 | 16,9 | 16,0 | 10,9 |
| 160; 150 | 33 960 | 24,1 | 20,6 | 24,3 | 23,0 | 15,7 |
| 200; 60 | 18 575 | 13,2 | 11,2 | 13,3 | 12,6 | 8,6 |
| 200; 100 | 28 832 | 20,5 | 17,5 | 20,6 | 19,5 | 13,3 |
| 200; 150 | 41 652 | 29,6 | 25,2 | 29,7 | 28,2 | 19,2 |

- Dom 160 m² o EU = 100 zużywa 15,7 mp sosny dla 2 osób i 18,0 mp dla 6 osób `[obliczenie: 04]`.

### B5.4. Trwały pozysk z 1 ha lasu

`D = I·u/k`

- D: trwały pozysk [mp/ha na rok]. I: przyrost bieżący roczny brutto [m³/ha na rok]. u = 0,70: udział przyrostu, który właściciel pozyskuje `[założenie]`.
- k = 0,65 m³ drewna litego w 1 mp `[założenie]`.
- Przyrost w Polsce wynosi 9,09 m³/ha (okres 5-letni, wszystkie lasy) `[źródło: S32]`.
- Przyrost wynosi 9,14 m³/ha dla sosny, 7,19 m³/ha dla brzozy i 8,31 m³/ha dla liściastych `[źródło: S32]`.
- Lasy prywatne mają przyrost 10,00 m³/ha dla sosny, 7,92 m³/ha dla brzozy, 9,27 m³/ha dla liściastych i 9,94 m³/ha ogółem `[źródło: S32]`.
- Źródło S32 nie podaje osobnej wartości dla olszy ani dla województwa warmińsko-mazurskiego `[DO USTALENIA: przyrost olszy; przyrost na działce 16/3]`.

Tabela B6. Trwały pozysk z 1 ha lasu przy u = 0,70 `[obliczenie: 04]`.

| Drzewostan | Przyrost [m³/ha na rok] | Pozysk [m³/ha na rok] | Pozysk [mp/ha na rok] | Paliwo [kWh/ha na rok] | Ciepło przy η = 0,78 [kWh/ha na rok] |
|---|---|---|---|---|---|
| Sosna, wszystkie lasy | 9,14 | 6,40 | 9,84 | 13 870 | 10 819 |
| Sosna, lasy prywatne | 10,00 | 7,00 | 10,77 | 15 176 | 11 837 |
| Brzoza, wszystkie lasy | 7,19 | 5,03 | 7,74 | 12 787 | 9974 |
| Brzoza, lasy prywatne | 7,92 | 5,54 | 8,53 | 14 085 | 10 986 |
| Olsza (przyrost liściastych), wszystkie lasy | 8,31 | 5,82 | 8,95 | 12 531 | 9774 |
| Olsza (przyrost liściastych), lasy prywatne | 9,27 | 6,49 | 9,98 | 13 978 | 10 903 |

- Udział u = 0,50 daje od 5,5 mp do 7,7 mp z 1 ha. Udział u = 0,90 daje od 10,0 mp do 13,9 mp z 1 ha `[obliczenie: 04]`.

Tabela B7. Powierzchnia lasu [ha] dla trwałego pokrycia ciepła domu, 4 osoby, u = 0,70 `[obliczenie: 04]`.

| Dom: m²; EU | Sosna | Brzoza | Olsza |
|---|---|---|---|
| 120; 60 | 0,90 | 0,97 | 0,99 |
| 120; 100 | 1,34 | 1,45 | 1,48 |
| 120; 150 | 1,89 | 2,05 | 2,10 |
| 160; 60 | 1,12 | 1,21 | 1,24 |
| 160; 100 | 1,71 | 1,85 | 1,89 |
| 160; 150 | 2,45 | 2,66 | 2,71 |
| 200; 60 | 1,34 | 1,45 | 1,48 |
| 200; 100 | 2,08 | 2,25 | 2,30 |
| 200; 150 | 3,00 | 3,26 | 3,32 |

### B5.5. Własny drzewostan 1,35 ha

- Drzewostan ma 1,35 ha. Część drzewostanu rośnie na płaskim, mokrym dnie na wysokości 105 m n.p.m. `[relacja: koordynator, 2026-11-11]`.
- Raport przyjmuje skład: 40 % olsza, 30 % sosna, 30 % brzoza `[założenie; DO USTALENIA: opis taksacyjny działki 16/3]`.

Tabela B8. Trwały pozysk z drzewostanu 1,35 ha `[obliczenie: 09]`.

| Wariant przyrostu | Przyrost [m³/ha na rok] | Pozysk [m³/rok] | Pozysk [mp/rok] | Paliwo [kWh/rok] | Ciepło [kWh/rok] |
|---|---|---|---|---|---|
| Ostrożny `[założenie]` | 6,00 | 5,7 | 8,7 | 12 895 | 10 058 |
| Średni: liściaste `[źródło: S32]` | 8,31 | 7,9 | 12,1 | 17 859 | 13 930 |
| Dobry: lasy prywatne `[źródło: S32]` | 9,94 | 9,4 | 14,5 | 21 362 | 16 663 |

Tabela B9. Największy wskaźnik EU [kWh/(m²·rok)], przy którym drzewostan 1,35 ha pokrywa 100 % ciepła dla 4 osób `[obliczenie: 09]`.

| Wariant przyrostu | 120 m², ciepła woda latem z fotowoltaiki | 160 m², ciepła woda latem z fotowoltaiki | 200 m², ciepła woda latem z fotowoltaiki | 160 m², ciepła woda cały rok z drewna |
|---|---|---|---|---|
| Ostrożny | 63 | 47 | 38 | 38 |
| Średni | 95 | 72 | 57 | 62 |
| Dobry | 118 | 89 | 71 | 79 |

Tabela B10. Dom 160 m², 4 osoby: potrzeba drewna i saldo drzewostanu 1,35 ha [mp/rok] `[obliczenie: 09]`.

| EU | Ciepło [kWh/rok] | Potrzeba drewna | Saldo, przyrost ostrożny | Saldo, przyrost średni | Saldo, przyrost dobry |
|---|---|---|---|---|---|
| 60 | 12 089 | 10,5 | −1,8 | +1,6 | +4,0 |
| 80 | 15 289 | 13,3 | −4,5 | −1,2 | +1,2 |
| 100 | 18 489 | 16,0 | −7,3 | −4,0 | −1,6 |
| 120 | 21 689 | 18,8 | −10,1 | −6,7 | −4,4 |
| 150 | 26 489 | 23,0 | −14,3 | −10,9 | −8,5 |

- Saldo ujemne oznacza drewno do zakupu.
- Wniosek 1: drzewostan 1,35 ha pokrywa 100 % ciepła domu 160 m² dopiero przy EU od 47 do 89 kWh/(m²·rok).
- Wniosek 2: dom 160 m² o EU = 100 wymaga zakupu od 1,6 mp do 7,3 mp drewna na rok.
- Wniosek 3: dom 160 m² o EU = 150 wymaga zakupu od 8,5 mp do 14,3 mp drewna na rok.
- Cały las ewidencyjny 1,82 ha daje od 11,8 mp do 19,5 mp na rok i pokrywa dom 160 m² o EU od 69 do 125 `[obliczenie: 09]`.

Środki zmniejszenia potrzeby drewna, dom 160 m² `[obliczenie: 09]`:

| Środek | Oszczędność [mp/rok] | Znacznik |
|---|---|---|
| Docieplenie z EU = 150 do EU = 100 | 6,9 | `[obliczenie: 09]` |
| Docieplenie z EU = 100 do EU = 60 | 5,6 | `[obliczenie: 09]` |
| Ciepła woda latem z grzałki zamiast z kotła | 2,1 | `[założenie: sprawność kotła latem 0,5]` |
| Grzałki bufora z nadwyżki fotowoltaiki w III, IV, X (2034 kWh) | 1,7 | `[obliczenie: 08, 09]` |
| Sprawność sezonowa 0,85 zamiast 0,78 | 1,3 | `[obliczenie: 09]` |

- Raport nie zna stanu drzewostanu: wieku, zasobności i składu `[DO USTALENIA: inwentaryzacja; zasady pozysku w lesie prywatnym; zakres agenta 1]`.

### B5.6. Plantacja w krótkiej rotacji

- Doświadczenie UWM leżało w punkcie 53°59′ N, 21°04′ E, na glebie piaszczystej, w rotacji 4-letniej `[źródło: S33]`.
- Wierzba dała średnio 8,34 t suchej masy na 1 ha na rok. Zakres wynosił od 5,10 t do 10,30 t `[źródło: S33]`.
- Topola dała średnio 8,21 t suchej masy na 1 ha na rok. Zakres wynosił od 5,48 t do 10,49 t `[źródło: S33]`.
- Robinia dała średnio 2,87 t suchej masy na 1 ha na rok. Zakres wynosił od 1,63 t do 5,40 t `[źródło: S33]`.
- Plon wierzby po dosuszeniu do w = 20 % odpowiada 40,3 MWh/ha na rok, czyli 27 mp drzewostanu mieszanego `[obliczenie: 04, 09]`.
- Niedobór 7,3 mp na rok odpowiada plantacji wierzby 0,27 ha `[obliczenie: 09]`.
- Ograniczenie: kocioł DC18S wymaga polan o średnicy od 80 mm do 150 mm `[źródło: S27]`. Pędy z rotacji 4-letniej są cieńsze `[założenie]`.
- Ograniczenie: pole ma co najwyżej 0,9 ha. Plantacja zmniejsza powierzchnię upraw żywności `[DO USTALENIA: bilans gruntu w syntezie]`.

### B5.7. Sezonowanie

- Drewno świeżo ścięte ma wilgotność co najmniej 50 % `[źródło: S29, S30]`.
- Buk, świerk i sosna schną do wilgotności mniejszej niż 20 % w ciągu 1 roku po połupaniu `[źródło: S30]`.
- Drewno niepołupane schnie co najwyżej 2 lata `[źródło: S30]`.
- Olsza sinieje i butwieje przy wolnym suszeniu `[źródło: S31]`.
- Wykonaj każdy krok w tej kolejności:
  1. Zetnij drzewa w miesiącach od XI do II `[źródło: S30, S31]`.
  2. Połup drewno najpóźniej 30 dni po ścięciu `[założenie]`.
  3. Ułóż stos na paletach, co najmniej 10 cm od ściany `[źródło: S30]`.
  4. Wystaw stos na słońce i na wiatr `[źródło: S30]`.
  5. Przykryj stos od góry przed końcem lata `[źródło: S30]`.
  6. Zmierz wilgotność wilgotnościomierzem na świeżym przełomie polana.
  7. Spalaj drewno dopiero przy wilgotności od 12 % do 20 % `[źródło: S26]`.
- Zapas na 2 sezony dla domu 160 m² o EU = 100 wynosi 32 mp drzewostanu mieszanego `[obliczenie: 09]`.

## B6. Magazyn ciepła: bufory 1 × 1000 dm³ i 2 × 500 dm³

### B6.1. Wymagania i pojemność

`V_min = 15·T_B·Q_N·(1 − 0,3·Q_H/Q_min)`

- V_min: najmniejsza pojemność bufora [dm³] według PN-EN 303-5 `[źródło: S34]`.
- T_B = 2 h: czas spalania ładunku. Q_N = 20 kW: moc nominalna. Q_H: obciążenie cieplne budynku [kW].
- Q_min: najmniejsza moc kotła [kW]. Źródło S34 podaje od 50 % do 80 % mocy nominalnej `[DO USTALENIA: Q_min kotła]`.
- Wynik: od 384 dm³ do 564 dm³ `[obliczenie: 04]`. Bufory 2000 dm³ spełniają wymaganie normy i zalecenie producenta.

`Q_buf = V·ρ·c_p·ΔT/3600`

- Q_buf: ciepło w buforze [kWh]. V: pojemność [dm³]. ρ = 0,982 kg/dm³ przy 62,5 °C. c_p = 4,19 kJ/(kg·K). ΔT: różnica temperatur [K].

Tabela B11. Pojemność cieplna buforów `[obliczenie: 09]`.

| Zakres temperatur | 500 dm³ | 1000 dm³ | 2000 dm³ |
|---|---|---|---|
| 85 °C → 40 °C (ΔT = 45 K) | 25,7 kWh | 51,4 kWh | 102,9 kWh |
| 85 °C → 45 °C (ΔT = 40 K) | 22,9 kWh | 45,7 kWh | 91,4 kWh |
| 90 °C → 40 °C (ΔT = 50 K) | 28,6 kWh | 57,2 kWh | 114,3 kWh |

- Bufory 2000 dm³ mieszczą 2,5 ładunku kotła (1 ładunek = 11,2 kg drewna = 41 kWh ciepła) `[obliczenie: 04, 09]`.
- Kocioł ładuje bufory 2000 dm³ w 5,1 h bez odbioru ciepła `[obliczenie: 09]`.

### B6.2. Schemat hydrauliczny (opis)

Oznaczenia: zbiornik A = 1000 dm³; zbiorniki B i C = 2 × 500 dm³.

1. Zasilanie kotła biegnie do zaworu ładującego Laddomat 22 z wkładką 78 °C `[źródło: S62]`.
2. Zawór ładujący miesza wodę powrotną z wodą zasilania. Kocioł dostaje wodę powrotną o temperaturze co najmniej 65 °C `[źródło: S26, S27]`.
3. Zasilanie z zaworu ładującego wchodzi w górny króciec zbiornika A.
4. Dolny króciec zbiornika A łączy się z górnym króćcem zbiornika B.
5. Dolny króciec zbiornika B łączy się z górnym króćcem zbiornika C.
6. Dolny króciec zbiornika C wraca do zaworu ładującego i do kotła.
7. Obiegi grzewcze i zasobnik ciepłej wody pobierają wodę z górnego króćca zbiornika A przez zawór mieszający.
8. Powrót z obiegów grzewczych wchodzi w dolny króciec zbiornika C.
9. Naczynie przeponowe łączy się z rurą powrotną przy zbiorniku C.
10. Zawór bezpieczeństwa 2,5 bar stoi na zasilaniu kotła, bez armatury odcinającej `[źródło: S62]`.

- Producent pokazuje połączenie zbiorników szeregowe i połączenie równoległe `[źródło: S62]`.
- Raport zaleca połączenie szeregowe A → B → C `[założenie]`.
- Uzasadnienie: połączenie równoległe w układzie Tichelmanna dzieli przepływ równo między zbiorniki o równym oporze.
- Zbiornik 500 dm³ ładuje się wtedy 2 razy szybciej niż zbiornik 1000 dm³. Gorąca woda z B i C miesza się z zimną wodą z A.
- Połączenie szeregowe przesuwa 1 front temperatury przez A, B i C. Zbiornik A ma najwyższą temperaturę.
- Wariant dopuszczalny: B i C równolegle w układzie Tichelmanna jako 1 jednostka 1000 dm³, szeregowo za zbiornikiem A.
- Przepływ ładowania wynosi 0,86 m³/h przy mocy 20 kW i różnicy 20 K. Prędkość w rurze 35 × 1,5 mm wynosi 0,30 m/s `[obliczenie: 09]`.
- Rury łączące zbiorniki POWINNY mieć średnicę wewnętrzną co najmniej 32 mm `[źródło: S62; założenie]`.
- Jeżeli zawór odcina zbiornik od zaworu bezpieczeństwa, to ten zbiornik MUSI mieć własny zawór bezpieczeństwa `[założenie]`.
- Czujniki temperatury: góra A, środek B, dół C. Dół C o temperaturze 70 °C oznacza bufory pełne `[założenie]`.

OSTRZEŻENIE: Nie dokładaj drewna, gdy dół zbiornika C ma więcej niż 70 °C. Kocioł bez odbioru ciepła przegrzewa wodę.

### B6.3. Naczynie przeponowe

`e = ρ₂₀/ρ₉₀ − 1`

`V_e = e·V_inst`

`V_n = (V_e + V_wr)·(p_e + 1)/(p_e − p_0)`

- e: przyrost objętości wody przy ogrzaniu z 20 °C do 90 °C [–]. ρ₂₀ = 998,2 kg/m³. ρ₉₀ = 965,3 kg/m³ `[założenie: tablice własności wody]`.
- V_e: objętość rozszerzenia [dm³]. V_inst: objętość wody w instalacji [dm³].
- V_n: pojemność naczynia [dm³]. V_wr: rezerwa wody = 0,5 % objętości instalacji [dm³].
- p_0: nadciśnienie wstępne poduszki gazowej [bar]. p_e: nadciśnienie końcowe [bar]. Wzór używa nadciśnień; liczba 1 zamienia nadciśnienie na ciśnienie absolutne.

Tabela B12. Dobór naczynia przeponowego `[obliczenie: 09]`.

| Wielkość | Same bufory | Bufory + kocioł 45 dm³ + instalacja 150 dm³ |
|---|---|---|
| Objętość V_inst | 2000 dm³ | 2195 dm³ `[założenie: instalacja 150 dm³]` |
| Przyrost objętości e | 3,41 % | 3,41 % |
| Objętość rozszerzenia V_e | 68,2 dm³ | 74,8 dm³ |
| Rezerwa V_wr | 10,0 dm³ | 11,0 dm³ |
| Nadciśnienie wstępne p_0 | 1,0 bar (absolutne 2,0 bar) | 1,0 bar (absolutne 2,0 bar) |
| Nadciśnienie końcowe p_e | 2,0 bar (absolutne 3,0 bar) | 2,0 bar (absolutne 3,0 bar) |
| Pojemność V_n z wzoru | 234 dm³ | 257 dm³ |
| Naczynie z typoszeregu | 250 dm³ | 300 dm³ |

- Kontrola dla naczynia 300 dm³: instalacja zimna (20 °C) ma nadciśnienie 1,08 bar (absolutne 2,08 bar) `[obliczenie: 09]`.
- Instalacja gorąca (90 °C) ma nadciśnienie 1,80 bar (absolutne 2,80 bar). Zapas do zaworu bezpieczeństwa wynosi 0,70 bar `[obliczenie: 09]`.
- Naczynie 250 dm³ daje nadciśnienie 2,04 bar przy 90 °C. Zapas wynosi 0,46 bar `[obliczenie: 09]`.
- Nadciśnienie wstępne 1,0 bar pasuje do wysokości instalacji co najwyżej 7 m nad naczyniem `[założenie]`.
- Membrana naczynia wytrzymuje co najwyżej 70 °C `[założenie; DO USTALENIA: karta naczynia]`. Naczynie łączy się z rurą powrotną przez odcinek rury bez izolacji.

### B6.4. Czas pokrycia zapotrzebowania domu z naładowanych buforów

`Φ(t_e) = Φ_H·(20 − t_e)/42`

`t_pow = 20 + 50·q^(1/1,3) − 5·q`

`t = Q_buf/(Φ + P_cwu + P_str)`

- Φ(t_e): obciążenie cieplne przy temperaturze zewnętrznej t_e [kW]. q = Φ/Φ_H [–].
- t_pow: temperatura powrotu z grzejników [°C]. Grzejniki 75/65/20 °C przy −22 °C, wykładnik 1,3 `[założenie]`.
- Grzejniki wykorzystują bufory od 85 °C do temperatury t_pow: 50,6 °C przy −5 °C; 63,4 °C przy −20 °C `[obliczenie: 09]`.
- Q_buf: 78,7 kWh przy −5 °C i 49,4 kWh przy −20 °C dla grzejników; 102,9 kWh dla ogrzewania podłogowego `[obliczenie: 09]`.
- P_cwu = 0,46 kW: ciepła woda 4 osób. P_str = 0,19 kW: strata buforów poza przestrzenią ogrzewaną `[założenie]`.

Tabela B13. Czas pracy domu z buforów 2000 dm³ [h] `[obliczenie: 09]`.

| Dom: m²; EU | Φ_H | −5 °C, grzejniki | −5 °C, zakres 85 → 40 °C | −20 °C, grzejniki | −20 °C, zakres 85 → 40 °C |
|---|---|---|---|---|---|
| 120; 60 | 3,4 kW | 29,4 | 38,4 | 12,7 | 26,4 |
| 120; 100 | 5,7 kW | 19,5 | 25,5 | 8,1 | 17,0 |
| 120; 150 | 8,5 kW | 13,8 | 18,0 | 5,6 | 11,7 |
| 160; 60 | 4,5 kW | 23,4 | 30,6 | 9,9 | 20,7 |
| 160; 100 | 7,6 kW | 15,3 | 19,9 | 6,3 | 13,1 |
| 160; 150 | 11,4 kW | 10,6 | 13,9 | 4,3 | 9,0 |
| 200; 60 | 5,7 kW | 19,5 | 25,5 | 8,1 | 17,0 |
| 200; 100 | 9,5 kW | 12,5 | 16,4 | 5,1 | 10,6 |
| 200; 150 | 14,2 kW | 8,6 | 11,3 | 3,5 | 7,3 |

- Wniosek 1: dom 160 m² o EU = 100 pracuje z buforów 15,3 h przy −5 °C i 6,3 h przy −20 °C (grzejniki).
- Wniosek 2: ogrzewanie niskotemperaturowe wydłuża czas pracy z buforów 2 razy przy −20 °C.
- Wniosek 3: przy −5 °C wystarcza 1 palenie na dobę (3 ładunki). Przy −20 °C potrzeba 2 paleń na dobę.
- Strata postojowa 3 zbiorników wynosi co najwyżej 382 W (klasa C), czyli 9,2 kWh na dobę `[obliczenie: 09, założenie]`.
- Zbiornik 2000 dm³ w 1 płaszczu traci co najwyżej 191 W `[obliczenie: 09]`.
- Właściciel POWINIEN ocieplić zbiorniki wełną mineralną 120 mm i ocieplić każdy króciec `[źródło: S28]`.
- Raport nie zna izolacji istniejących zbiorników `[DO USTALENIA: grubość izolacji, ciśnienie dopuszczalne zbiorników]`.

### B6.5. Zabezpieczenie kotła przy braku prądu

OSTRZEŻENIE: Zapewnij odbiór ciepła z kotła podczas awarii zasilania. Kocioł z ładunkiem drewna bez pracy pompy przegrzewa wodę do temperatury większej niż 95 °C.

- Pompa zaworu ładującego (50 W) MUSI należeć do klasy 1 odbiorników off-grid (tabela A10).
- Zasilacz awaryjny POWINIEN zasilać pompę ładującą przez co najmniej 3 h po wyłączeniu falownika `[założenie]`.
- Raport nie sprawdził wężownicy schładzającej kotła `[DO USTALENIA: instrukcja kotła, zawór schładzający i ciśnienie wody zimnej]`.
- Jeżeli zawór schładzający korzysta z wody ze studni, to zbiornik przeponowy MUSI mieć zapas wody pod ciśnieniem.
- Zbiornik górny na pagórku daje nadciśnienie 0,98 bar bez prądu (sekcja C8.6) `[obliczenie: 09]`.

### B6.6. Ciepła woda latem

- Ciepła woda 4 osób zużywa latem 11,1 kWh na dobę `[obliczenie: 04]`.
- Grzałka wymaga 2,5 kWp fotowoltaiki przy uzysku 4,35 kWh/kWp na dobę (V–VIII, P50) `[obliczenie: 04]`.
- Konfiguracja główna ma 5769 kWh nadwyżki w miesiącach V–IX `[obliczenie: 08]`.
- Wniosek: grzałka od 2 kW do 3 kW w zasobniku 300 dm³ pokrywa ciepłą wodę latem. Kolektory słoneczne nie są potrzebne.
- Zasobnik 300 dm³ magazynuje 6,9 kWh przy ogrzaniu z 45 °C do 65 °C `[obliczenie: 04]`.
- Warianty: 2 osoby zużywają 5,5 kWh na dobę, 6 osób 16,6 kWh na dobę `[obliczenie: 04]`.

### B6.7. Pompa ciepła

`COP = 0,45·(t_zas + 273,15)/(t_zas − t_zew)`

- COP: współczynnik wydajności w danym miesiącu [–]. 0,45: stosunek do obiegu Carnota `[założenie]`.
- t_zas = 30 + 25·(20 − t_zew)/42: temperatura zasilania [°C] `[założenie]`. t_zew: średnia temperatura miesiąca [°C] `[źródło: S7]`.
- Pompa ciepła dla domu 160 m² o EU = 100 zużywa 5402 kWh na rok, w tym 1042 kWh w styczniu `[obliczenie: 04]`.
- Pompa ciepła zużywa w miesiącach XI–II 3510 kWh. Fotowoltaika 15 kWp daje w tym czasie 1105 kWh w scenariuszu konserwatywnym `[obliczenie: 04, 08]`.
- Wniosek: pompa ciepła wyklucza wariant off-grid. Ciepło zimą pochodzi z drewna.

### B6.8. Ogrzewanie kurnika i tunelu foliowego

- Producent kur Hy-Line zaleca w kurniku od 18 °C do 25 °C `[źródło: S37]`.
- Stado 100 kur oddaje 808 W ciepła jawnego `[założenie: wzór CIGR 2002; DO USTALENIA: weryfikacja wzoru]`.
- Kurnik 4 m × 6 m × 2,3 m o współczynniku U = 0,35 W/(m²·K) i wentylacji 75 m³/h utrzymuje temperaturę o 16,2 K wyższą od zewnętrznej `[obliczenie: 04]`.
- Kurnik nieocieplony (U = 1,5 W/(m²·K)) utrzymuje temperaturę o 5,2 K do 6,2 K wyższą od zewnętrznej `[obliczenie: 04]`.
- Wniosek: raport zaleca ocieplenie kurnika i ochronę poideł przed mrozem. Raport nie zaleca ogrzewania kurnika.
- Tunel foliowy 6 m × 10 m ma 123 m² folii `[obliczenie: 04]`.
- Folia pojedyncza (U = 7,0 W/(m²·K)) wymaga 8,6 kW przy różnicy 10 K `[obliczenie: 04, założenie]`.
- Noc 12 h przy różnicy 10 K zużywa 103 kWh, czyli 33 kg drewna `[obliczenie: 04]`.
- Wniosek: raport nie zaleca ogrzewania tunelu. Raport zaleca folię podwójną, włókninę wewnętrzną i beczki z wodą `[założenie]`.

# C. Woda pitna

## C7. Zapotrzebowanie

- Woda pochodzi tylko z własnej studni `[relacja: koordynator, 2026-11-11]`.
- Domy jednorodzinne w Poznaniu zużywały od 101 dm³ do 117 dm³ na osobę na dobę (pomiar) `[źródło: S38]`.
- Raport przyjmuje 110 dm³ na osobę na dobę `[założenie]`.
- Stado 100 kur w wieku od 40 do 100 tygodni pije od 17,4 dm³ do 24,8 dm³ na dobę `[źródło: S37]`.
- Kura pije od 1,5 do 2,0 razy więcej wody niż zjada paszy `[źródło: S37]`.
- Koza albo owca mleczna pije od 4 dm³ do 10 dm³ na dobę `[założenie]`. Stado 4 sztuk zużywa 15 m³ na rok z myciem sprzętu `[założenie]`.

### C7.1. Podlewanie na glebie lekkiej (klasa V–VI)

`ET₀ = [0,408·Δ·(R_n − G) + γ·900/(T + 273)·u₂·(e_s − e_a)]/[Δ + γ·(1 + 0,34·u₂)]`

`ET_c = K_c·ET₀`

`TAW = 1000·(θ_FC − θ_WP)·Z_r`

`RAW = p·TAW`

- ET₀: ewapotranspiracja wskaźnikowa [mm na dobę] według FAO-56 `[źródło: S64]`.
- Δ: nachylenie krzywej prężności pary [kPa/°C]. R_n: promieniowanie netto [MJ/m² na dobę]. G: strumień ciepła w glebie [MJ/m² na dobę].
- γ: stała psychrometryczna [kPa/°C]. T: temperatura powietrza [°C]. u₂: prędkość wiatru na wysokości 2 m [m/s].
- e_s − e_a: niedosyt prężności pary [kPa]. K_c: współczynnik roślinny [–].
- TAW: woda dostępna w strefie korzeni [mm]. θ_FC − θ_WP: 0,09 m³/m³ dla piasku gliniastego `[źródło: S64]`; 0,06 m³/m³ dla piasku luźnego `[założenie]`.
- Z_r = 0,4 m: głębokość korzeni warzyw `[założenie; źródło S64 podaje od 0,3 m do 1,0 m]`.
- RAW: woda łatwo dostępna [mm]. p = 0,35: dopuszczalne wyczerpanie `[źródło: S64]`.
- K_c: 0,60 w IV; 0,80 w V; 1,00 w VI; 1,05 w VII; 1,00 w VIII; 0,85 w IX `[założenie; źródło S64 podaje 0,7; 1,05; 0,95]`.
- Dane wejściowe: temperatura, opad i wilgotność `[źródło: S7]`; promieniowanie `[źródło: S1]`; wiatr `[źródło: S8, założenie]`.

Tabela C1. Ewapotranspiracja i opad `[obliczenie: 10]`.

| Miesiąc | ET₀ [mm na dobę] | ET₀ [mm] | K_c | ET_c [mm] | Opad [mm] |
|---|---|---|---|---|---|
| IV | 1,96 | 59 | 0,60 | 35 | 37,5 |
| V | 2,92 | 90 | 0,80 | 72 | 59,8 |
| VI | 3,40 | 102 | 1,00 | 102 | 70,1 |
| VII | 3,41 | 106 | 1,05 | 111 | 88,0 |
| VIII | 2,97 | 92 | 1,00 | 92 | 63,8 |
| IX | 1,80 | 54 | 0,85 | 46 | 58,5 |
| Suma | brak | 503 | brak | 458 | 377,7 |

Skrypt 10 liczy dobowy bilans wody w strefie korzeni dla 300 losowych sezonów `[obliczenie: 10]`.

- Model losuje opad doby z liczby dni z opadem i z sumy miesięcznej `[źródło: S7; założenie: rozkład wykładniczy]`.
- Woda, która przekracza pojemność TAW, przesiąka pod strefę korzeni.
- Sterownik nawadnia, gdy wyczerpanie osiąga RAW. Sprawność nawadniania kroplowego wynosi 0,9 `[założenie]`.

Tabela C2. Potrzeby nawadniania brutto [mm = dm³/m² na sezon IV–IX] `[obliczenie: 10]`.

| Gleba | TAW | Opad normalny: średnio (decyl 10 %; decyl 90 %) | Opad 60 % normy | Liczba nawodnień | Dawka | Szczyt 7 dni |
|---|---|---|---|---|---|---|
| Piasek luźny | 24 mm | 306 (272; 337) | 354 | 28 | 10,8 mm | 36 mm |
| Piasek gliniasty | 36 mm | 256 (218; 294) | 324 | 16 | 15,5 mm | 34 mm |
| Glina (porównanie) | 60 mm | 197 (149; 248) | 294 | 8 | 24,9 mm | 48 mm |

Tabela C3. Woda dla warzywnika na piasku gliniastym `[obliczenie: 10]`.

| Powierzchnia | Średnio na sezon | Rok suchy 1 raz na 10 lat | Opad 60 % normy | Szczyt na dobę | Energia pompy na sezon | Praca pompy w szczycie |
|---|---|---|---|---|---|---|
| 1000 m² | 256 m³ | 294 m³ | 324 m³ | 4,8 m³ | 113–142 kWh | 2,2 h na dobę |
| 1500 m² | 384 m³ | 441 m³ | 486 m³ | 7,3 m³ | 169–214 kWh | 3,3 h na dobę |
| 2000 m² | 512 m³ | 589 m³ | 648 m³ | 9,7 m³ | 225–285 kWh | 4,4 h na dobę |

- Wniosek 1: gleba lekka wymaga dawki od 11 mm do 16 mm co 2,3 doby do 3,5 doby w lipcu `[obliczenie: 10]`.
- Wniosek 2: dawka 25 mm 1 raz na tydzień przekracza RAW piasku. Nadmiar przesiąka pod strefę korzeni.
- Wniosek 3: piasek luźny zużywa o 50 mm więcej wody na sezon niż piasek gliniasty.
- Ściółka i materia organiczna zwiększają pojemność TAW `[założenie]`.
- Pompa zużywa w szczycie 4,3 kWh na dobę przy 2000 m². Fotowoltaika 15 kWp daje w lipcu 53 kWh na dobę `[obliczenie: 10]`.
- Sterownik POWINIEN nawadniać w godzinach 08:00–14:00, bezpośrednio z fotowoltaiki `[założenie]`.
- Tunel 60 m² zużywa 47 m³ na sezon przy 30 mm na tydzień przez 26 tygodni `[obliczenie: 05, założenie]`.

Tabela C4. Roczny pobór wody ze studni, 4 osoby `[obliczenie: 05, 10]`.

| Odbiorca | Rok przeciętny | Rok suchy |
|---|---|---|
| 4 osoby | 161 m³ | 161 m³ |
| Kury, kozy lub owce | 15 m³ | 15 m³ |
| Warzywnik 2000 m² | 512 m³ | 648 m³ |
| Tunel 60 m² | 47 m³ | 47 m³ |
| Suma | 735 m³ | 871 m³ |
| Średnio na dobę | 2,01 m³ | 2,39 m³ |

- Warianty: 2 osoby zużywają 80 m³ na rok, 6 osób 241 m³ na rok `[obliczenie: 05]`.
- Szczyt doby w lipcu wynosi 10,3 m³ przy 2000 m² warzywnika `[obliczenie: 10]`.
- Raport nie zna wydajności studni `[DO USTALENIA: próbne pompowanie, głębokość studni, zwierciadło wody]`.

## C8. Studnia

### C8.1. Prawo

- Zwykłe korzystanie z wód obejmuje pobór co najwyżej 5 m³ na dobę średnio w roku `[relacja: koordynator, 2026-11-11]`.
- Zwykłe korzystanie z wód obejmuje studnię o głębokości co najwyżej 30 m `[relacja: koordynator, 2026-11-11]`.
- Pobór 2,39 m³ na dobę spełnia limit 5 m³ na dobę `[obliczenie: 10]`.
- Wybieg nieutwardzony MUSI leżeć co najmniej 70 m od studni `[relacja: koordynator, 2026-11-11]`.
- Budynek inwentarski MUSI stać co najmniej 15 m od studni `[relacja: koordynator, 2026-11-11]`.
- Rozporządzenie Ministra Zdrowia z 2026-05-22 (Dz.U. 2026 poz. 748) obowiązuje od 2026-06-24 `[źródło: S39, S41]`.
- Rozporządzenie z 2026-05-22 uchyliło rozporządzenie z 2017-12-07 (Dz.U. 2017 poz. 2294) `[źródło: S39]`.
- Ustawa z 2026-03-13 (Dz.U. 2026 poz. 605) nie obejmuje indywidualnego źródła, które dostarcza średnio mniej niż 10 m³ na dobę `[źródło: S40]`.
- Wyłączenie nie działa, jeżeli dostarczanie wody jest przedmiotem działalności gospodarczej `[źródło: S40]`.
- Dla takiego źródła inspektor sanitarny ustala częstość badań: co najmniej 1 raz na rok `[źródło: S39]`.
- Wniosek 1: studnia tylko dla domu nie podlega obowiązkowi badań.
- Wniosek 2: studnia, która zasila kemping, podlega ustawie `[DO USTALENIA: źródło wody kempingu; PSSE Olsztyn]`.

### C8.2. Układ

Układ zawiera każdy element w tej kolejności:

1. Istniejąca studnia z pompą głębinową i z zabezpieczeniem przed suchobiegiem.
2. Rura tłoczna PE na głębokości większej niż głębokość przemarzania.
3. Zawór zwrotny i zbiornik przeponowy z łącznikiem ciśnienia.
4. Filtr osadu.
5. Odżelaziacz i odmanganiacz z automatycznym płukaniem.
6. Lampa UV z czujnikiem natężenia na linii wody pitnej.
7. Rozdział: dom, budynki zwierząt, nawadnianie, zbiornik górny. Nawadnianie MOŻE pomijać uzdatnianie.

### C8.3. Dobór pompy

`h_f = λ·(L/D)·v²/(2·g)`

`H = H_geo + 10,2·p + h_f + h_uzd`

`P_el = ρ·g·Q·H/η`

- h_f: strata ciśnienia w rurze [m]. λ = 0,022 `[założenie]`. L = 60 m `[założenie]`. D = 0,026 m: średnica wewnętrzna rury PE32. v: prędkość wody [m/s].
- H: wysokość podnoszenia [m]. H_geo = 12 m: głębokość zwierciadła podczas pompowania `[założenie]`.
- p: nadciśnienie w zbiorniku przeponowym [bar]. h_uzd = 8 m: strata na filtrach i na odżelaziaczu `[założenie]`.
- P_el: moc elektryczna [W]. Q: wydajność [m³/s]. η = 0,40: sprawność całkowita `[założenie]`.

- Dom stoi na wysokości 107 m n.p.m. Lustro jeziora leży na wysokości 104,8 m n.p.m. `[relacja: koordynator, 2026-11-11]`.
- Wniosek: zwierciadło wody gruntowej leży płytko. Wartość H_geo = 12 m jest założeniem ostrożnym.
- Wydajność Q = 2,5 m³/h daje prędkość 1,31 m/s i stratę h_f = 4,4 m `[obliczenie: 05]`.
- Nadciśnienie 3,0 bar wymaga H = 55 m i mocy 937 W. Nadciśnienie 4,0 bar wymaga H = 65 m i mocy 1111 W `[obliczenie: 05]`.
- Energia pompowania wynosi od 0,37 kWh/m³ do 0,44 kWh/m³ `[obliczenie: 05]`.
- Taśma kroplująca 1,0 dm³/h co 0,2 m przy rozstawie 0,75 m pobiera 6,7 m³/h na 1000 m² `[obliczenie: 05]`.
- Wniosek: warzywnik 1000 m² wymaga 3 sekcji po 2,2 m³/h.

### C8.4. Pompa w systemie off-grid

- Silnik pompy z rozruchem bezpośrednim pobiera przy starcie prąd od 4 do 6 razy większy od prądu znamionowego `[założenie]`.
- Pompa 1,1 kW z rozruchem bezpośrednim obciąża falownik mocą chwilową od 7 kVA do 10 kVA `[założenie]`.
- Pompa Grundfos SQ ma łagodny rozruch, który ogranicza prąd rozruchu `[źródło: S63]`.
- Pompa Grundfos SQ ma silnik z magnesami trwałymi, średnicę 74 mm i ochronę przed suchobiegiem `[źródło: S63]`.
- Pompa Grundfos SQ pracuje przy napięciu od 150 V do 280 V `[źródło: S63]`.
- Pompa SQE ze sterownikiem CU 301 utrzymuje stałe ciśnienie i wymaga zbiornika 8 dm³ `[źródło: S63]`.
- Pompa na prąd stały zasilana z magazynu 48 V albo z paneli jest drugą opcją `[założenie; DO USTALENIA: karta pompy]`.
- Wniosek: pompa z łagodnym rozruchem (klasa Grundfos SQ) pasuje do falownika 8 kW bez zapasu na rozruch.
- Sterownik blokuje start pompy podczas pracy płyty indukcyjnej `[założenie]`.

### C8.5. Zbiornik przeponowy

`V_u = Q/(4·n)`

`V_t = V_u·p_zał·p_wył/(p_wst·(p_wył − p_zał))`

- V_u: objętość użyteczna [dm³]. Q = 2500 dm³/h. n: liczba załączeń pompy na godzinę.
- V_t: pojemność całkowita zbiornika [dm³]. Ciśnienia p_zał, p_wył, p_wst we wzorze są ciśnieniami absolutnymi [bar].
- p_wst: ciśnienie wstępne; nadciśnienie o 0,2 bar mniejsze od nadciśnienia załączenia `[założenie]`.
- Nadciśnienie załączenia 2,5 bar i wyłączenia 4,0 bar daje V_t = 147 dm³ przy 15 załączeniach na godzinę `[obliczenie: 05]`.
- Wniosek: zbiornik od 150 dm³ do 200 dm³ dla pompy z łącznikiem ciśnienia. Zbiornik 8 dm³ dla pompy o stałym ciśnieniu `[źródło: S63]`.

### C8.6. Zbiornik górny na pagórku

`p = ρ·g·h`

- p: nadciśnienie hydrostatyczne [Pa]. ρ = 1000 kg/m³. g = 9,81 m/s². h: różnica wysokości [m].
- Działka 16/1 ma pagórek od 106 m do 118 m n.p.m. Dom stoi na wysokości 107 m n.p.m. `[relacja: koordynator, 2026-11-11]`.
- Różnica wysokości 10 m daje nadciśnienie 0,98 bar. Różnica 8 m daje 0,78 bar `[obliczenie: 09]`.
- Zbiornik górny od 3 m³ do 5 m³ zasila bez prądu poidła, krany o przepływie co najwyżej 5 dm³/min i linie kroplujące `[założenie]`.
- Pompa napełnia zbiornik górny w godzinach 10:00–15:00 z nadwyżki fotowoltaiki.
- Zbiornik 5 m³ pokrywa 7 dób zapasu awaryjnego dla 4 osób i zwierząt (735 dm³) oraz 1 dobę szczytu podlewania 1000 m² `[obliczenie: 05, 10]`.
- Zbiornik MUSI leżeć pod przykryciem gruntu co najmniej 1,2 m albo mieć opróżnienie przed mrozem `[założenie]`.

### C8.7. Uzdatnianie i wymagania jakości

Tabela C5. Wartości parametryczne wody do spożycia `[źródło: S39]`.

| Parametr | Wartość |
|---|---|
| Escherichia coli | 0 w 100 ml |
| Enterokoki | 0 w 100 ml |
| Bakterie grupy coli | 0 w 100 ml |
| Żelazo | co najwyżej 200 µg/dm³ |
| Mangan | co najwyżej 50 µg/dm³ |
| Jon amonowy | co najwyżej 0,50 mg/dm³ |
| Azotany | co najwyżej 50 mg/dm³ |
| Azotyny | co najwyżej 0,50 mg/dm³ |
| Warunek łączny | [azotany]/50 + [azotyny]/3 ≤ 1 |
| pH | od 6,5 do 9,5 |
| Przewodność przy 25 °C | co najwyżej 2500 µS/cm |

- Lampa UV MUSI dawać dawkę co najmniej 400 J/m² przy długości fali 253,7 nm według normy ÖNORM M 5873 `[źródło: S42]`.
- Mętność większa niż 1 NTU wymaga analizy ryzyka przed lampą UV `[źródło: S42]`.
- Żelazo, mangan i kwasy humusowe obniżają skuteczność lampy UV `[źródło: S42]`.
- Wniosek: odżelaziacz i odmanganiacz stoją przed lampą UV.
- Właściciel dobiera złoże filtra dopiero po badaniu wody `[DO USTALENIA: wynik badania wody ze studni]`.
- Zalecenie dla studni domowej `[założenie]`:
  1. Zbadaj wodę w laboratorium akredytowanym: parametry z tabeli C5 oraz mętność i barwa.
  2. Badaj bakteriologię co 12 miesięcy.
  3. Badaj żelazo, mangan, jon amonowy, azotany i azotyny co 12 miesięcy.
  4. Zbadaj wodę po każdym zalaniu studni i po każdej naprawie pompy.

### C8.8. Zapas awaryjny

Tabela C6. Zapas wody [dm³]: 20 dm³ na osobę na dobę oraz 25 dm³ na dobę dla zwierząt `[obliczenie: 05, założenie]`.

| Liczba osób | 3 doby | 7 dób | 14 dób |
|---|---|---|---|
| 2 | 195 | 455 | 910 |
| 4 | 315 | 735 | 1470 |
| 6 | 435 | 1015 | 2030 |

- Gotowanie przez 1 min dezynfekuje wodę klarowną `[źródło: S43]`.
- Wybielacz bez zapachu o stężeniu od 5 % do 9 % dezynfekuje wodę w dawce 2 krople na 1 dm³ po 30 min `[źródło: S43]`.
- Raport przyjmuje wymianę wody w zbiorniku co 6 miesięcy `[założenie; DO USTALENIA: zalecenie sanitarne]`.
- Pompa ręczna zasysa wodę z głębokości co najwyżej 7 m. Granica teoretyczna wynosi 10,3 m `[obliczenie: 05, założenie]`.

### C8.9. Ochrona przed mrozem

- Źródło S44 podaje strefy przemarzania 0,8 m; 1,0 m; 1,2 m; 1,4 m oraz głębokość rur 1,0 m; 1,35 m; 1,6 m; 1,85 m `[źródło: S44]`.
- Źródło S45 przypisuje Olsztyn do obszaru od 1,2 m do 1,4 m `[źródło: S45]`.
- Raport przyjmuje głębokość przemarzania 1,2 m i przykrycie rur 1,6 m `[założenie; DO USTALENIA: strefa według mapy PN-81/B-03020]`.
- Wykonaj każde zabezpieczenie:
  - Ułóż rurę tłoczną i rury do budynków zwierząt na głębokości co najmniej 1,6 m.
  - Zabuduj głowicę studni w komorze ocieplonej.
  - Owiń odcinki nad ziemią przewodem grzejnym z termostatem i otuliną.
  - Opróżnij linie nawadniania przed pierwszym mrozem.

## C9. Deszczówka i mała retencja

`Y = A·P·e·η_f`

- Y: uzysk deszczówki [dm³/rok]. A: rzut dachu [m²]. P = 642,4 mm: opad roczny (lata 1991–2020) `[źródło: S7]`.
- e = 0,8: współczynnik spływu dachu skośnego twardego `[założenie: DIN 1989-1]`. η_f = 0,9: sprawność filtra `[założenie]`.
- Wynik: 463 dm³ z 1 m² rzutu dachu na rok `[obliczenie: 05]`.

Tabela C7. Uzysk deszczówki `[obliczenie: 05]`.

| Rzut dachu | Uzysk na rok | Uzysk w miesiącach IV–IX | Zbiornik = 6 % uzysku rocznego |
|---|---|---|---|
| 100 m² | 46 m³ | 27 m³ | 2,8 m³ |
| 150 m² | 69 m³ | 41 m³ | 4,2 m³ |
| 250 m² | 116 m³ | 68 m³ | 6,9 m³ |
| 400 m² | 185 m³ | 109 m³ | 11,1 m³ |

- Dach 250 m² pokrywa 27 % podlewania warzywnika 1000 m² w roku przeciętnym (68 m³ z 256 m³) `[obliczenie: 05, 10]`.
- Zastosowania: podlewanie, mycie budynków zwierząt, spłukiwanie toalet.
- NIE WOLNO pić deszczówki bez uzdatniania i bez badania.
- Staw 100 m² o średniej głębokości 1,5 m mieści 150 m³ `[obliczenie: 05]`.
- Opad na lustro stawu wynosi 64 m³ na rok. Parowanie wynosi od 50 m³ do 60 m³ na rok `[obliczenie: 05, założenie]`.
- Gleba piaszczysta wymaga uszczelnienia stawu folią albo gliną `[założenie]`.
- Raport nie ocenił poboru wody z jeziora Ukiel `[DO USTALENIA: Prawo wodne; zakres agenta 1]`.

# D. Magazyn żywności (infrastruktura)

## D10. Piwnica ziemna, spiżarnia, zamrażarki, suszarka, wędzarnia

### D10.1. Piwnica ziemna: warunki

- Cel projektu: temperatura od 2 °C do 8 °C i wilgotność względna od 85 % do 95 % `[relacja: koordynator, 2026-11-11]`.
- Warzywa korzeniowe wymagają 0 °C i wilgotności od 90 % do 95 %. Marchew przechowuje się wtedy 5 miesięcy, a burak 3 miesiące `[źródło: S49]`.
- Ziemniaki wymagają 3,3 °C i wilgotności od 85 % do 90 %. Ziemniaki przechowują się wtedy 8 miesięcy `[źródło: S49]`.
- Cebula wymaga 0 °C i wilgotności od 55 % do 60 %. Dynia wymaga 15,6 °C i wilgotności od 55 % do 60 % `[źródło: S49]`.
- Wniosek: cebula, czosnek i dynia leżą w spiżarni suchej, a nie w piwnicy ziemnej.

`T(z,t) = T_śr + A₀·exp(−z/d)·cos(2π·(t − t₀)/365 − z/d)`

`d = √(a·τ/π)`

- T(z,t): temperatura gruntu na głębokości z [m] w dniu t [°C]. T_śr = 9,0 °C: średnia roczna gruntu `[założenie: powietrze 8,0 °C + 1 K]`.
- A₀ = 10,15 K: amplituda roczna na powierzchni `[źródło: S7; obliczenie: 06]`. t₀ = 198: dzień najwyższej temperatury powierzchni.
- d: głębokość tłumienia [m]. a = 0,6·10⁻⁶ m²/s: dyfuzyjność cieplna gruntu `[założenie]`. τ = 365 dób.
- Wynik: d = 2,45 m. Zakres wynosi od 2,00 m do 3,01 m dla a od 0,4·10⁻⁶ do 0,9·10⁻⁶ m²/s `[obliczenie: 06]`.

Tabela D1. Temperatura gruntu [°C] `[obliczenie: 06]`.

| Głębokość | I | II | III | IV | V | VI | VII | VIII | IX | X | XI | XII |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1,0 m | 2,8 | 2,3 | 3,5 | 6,2 | 9,6 | 13,0 | 15,2 | 15,7 | 14,4 | 11,7 | 8,2 | 5,0 |
| 2,0 m | 5,9 | 4,7 | 4,6 | 5,7 | 7,6 | 10,0 | 12,0 | 13,3 | 13,4 | 12,3 | 10,3 | 8,0 |
| 3,0 m | 8,0 | 6,7 | 6,1 | 6,2 | 7,0 | 8,4 | 10,0 | 11,3 | 11,9 | 11,8 | 10,9 | 9,5 |

- Grunt na głębokości 2,0 m ma 12,3 °C w październiku i 8,0 °C w grudniu `[obliczenie: 06]`.
- Wniosek: sam grunt nie daje temperatury od 2 °C do 8 °C w czasie zbiorów. Piwnica wymaga chłodzenia powietrzem nocnym.

### D10.2. Wentylacja grawitacyjna

`V′ = C_d·A·√(2·g·h·ΔT/T)`

- V′: strumień powietrza [m³/s]. C_d = 0,6 `[założenie]`. A: przekrój kanału [m²]. g = 9,81 m/s².
- h: różnica wysokości wlotu i wylotu [m]. ΔT: różnica temperatur piwnicy i otoczenia [K]. T = 275 K.

| Kanał | h | ΔT = 3 K | ΔT = 5 K | ΔT = 10 K | ΔT = 15 K |
|---|---|---|---|---|---|
| 110 mm | 2,0 m | 13 m³/h | 17 m³/h | 25 m³/h | 30 m³/h |
| 110 mm | 3,0 m | 16 m³/h | 21 m³/h | 30 m³/h | 37 m³/h |
| 160 mm | 2,0 m | 28 m³/h | 37 m³/h | 52 m³/h | 64 m³/h |
| 160 mm | 3,0 m | 35 m³/h | 45 m³/h | 64 m³/h | 78 m³/h |

Znacznik tabeli: `[obliczenie: 06]`.

- Kanał nawiewny kończy się 0,2 m nad podłogą. Kanał wywiewny zaczyna się pod sufitem po przeciwnej stronie `[założenie]`.
- Piwnica 18 m³ z 2 kanałami 160 mm wymienia powietrze od 2 do 4 razy na godzinę `[obliczenie: 06]`.
- Każdy kanał ma siatkę przeciw gryzoniom `[źródło: S49]` i przepustnicę z siłownikiem `[założenie]`.
- Reguły sterowania przepustnic `[założenie]`:
  1. Jeżeli piwnica ma więcej niż 5 °C i powietrze zewnętrzne jest zimniejsze o co najmniej 2 K, to sterownik otwiera przepustnice.
  2. Jeżeli piwnica ma mniej niż 2 °C, to sterownik zamyka przepustnice.
  3. Jeżeli powietrze zewnętrzne ma mniej niż −5 °C, to sterownik zamyka przepustnice.
  4. Jeżeli piwnica ma mniej niż 1 °C, to sterownik wysyła alarm i włącza grzałkę 100 W `[źródło: S49]`.

### D10.3. Konstrukcja i położenie

- Lustro jeziora leży na wysokości 104,8 m n.p.m. Dom stoi na wysokości 107 m n.p.m. `[relacja: koordynator, 2026-11-11]`.
- Wniosek: piwnica w wykopie przy domu leży blisko wody gruntowej.
- Zalecenie: piwnica wbudowana w stok pagórka działki 16/1, podłoga na wysokości co najmniej 108 m n.p.m. `[założenie; DO USTALENIA: poziom wody gruntowej]`.
- Wejście od strony północnej, z przedsionkiem i z 2 drzwiami ocieplonymi `[założenie]`.
- Przykrycie gruntem 0,8 m ma opór cieplny 0,53 m²·K/W. Płyta XPS 0,10 m dodaje 2,78 m²·K/W `[obliczenie: 06]`.
- Izolacja ścian sięga głębiej niż głębokość przemarzania `[źródło: S49]`.
- Podłoga z gruntu albo ze żwiru utrzymuje wilgotność `[źródło: S49]`.
- Drenaż opaskowy i spadek terenu odprowadzają wodę opadową od ścian `[źródło: S49; założenie]`.
- Wykop i wybieg zwierząt MUSZĄ zachować odległości od studni z sekcji C8.1.

Tabela D2. Wymiary piwnicy ziemnej `[obliczenie: 06, założenie]`.

| Liczba osób | Potrzebna powierzchnia | Komora | Kubatura |
|---|---|---|---|
| 2 | 3,9 m² | 2,0 m × 2,5 m × 2,2 m | 11 m³ |
| 4 (wariant główny) | 7,8 m² | 2,5 m × 3,2 m × 2,2 m | 18 m³ |
| 6 | 11,7 m² | 3,0 m × 4,0 m × 2,2 m | 26 m³ |

- Podstawa: 150 kg ziemniaków, 100 kg warzyw korzeniowych, 30 kg kapusty, 60 kg jabłek i 150 słoików na osobę `[założenie; DO USTALENIA: ilości z raportu agenta 2]`.
- Kubatura wynosi 4,3 m³ na osobę: produkty 0,90 m³, skrzynki i regały 1,50 m³, przejścia `[obliczenie: 06]`.
- Źródło S49 podaje dla rodziny piwnicę 1,2 m × 1,8 m. Ta wartość nie dotyczy pełnej samowystarczalności `[źródło: S49]`.

### D10.4. Spiżarnia sucha i ziarno

- Ziarno zbóż przechowuje się bezpiecznie przy wilgotności co najwyżej 14,0 % przez 6 miesięcy `[źródło: S50]`.
- Ziarno zbóż przechowywane dłużej niż 6 miesięcy wymaga wilgotności co najwyżej 13,0 % `[źródło: S50]`.
- Właściciel POWINIEN schłodzić ziarno do temperatury mniejszej niż 16 °C najpóźniej 7 dni po zbiorze `[źródło: S50]`.
- Ziarno o wilgotności 14 % i temperaturze 5 °C przechowuje się 150 tygodni `[źródło: S50]`.
- Wołek zbożowy niszczy 5 % przechowywanego ziarna w Polsce `[źródło: S50]`.
- Wykonaj każdy krok:
  1. Oczyść magazyn odkurzaczem przed zbiorem `[źródło: S50]`.
  2. Uszczelnij szczeliny zaprawą. Załóż siatkę metalową na każdy otwór wentylacyjny `[źródło: S50]`.
  3. Mierz temperaturę ziarna co 10 dni zimą i co 5 dni wiosną `[źródło: S50]`.
  4. Mierz wilgotność ziarna co 1 miesiąc `[źródło: S50]`.
- Beczka stalowa 200 dm³ mieści 154 kg pszenicy i chroni ziarno przed gryzoniami `[obliczenie: 06, założenie]`.
- Ziarno konsumpcyjne 4 osób (800 kg) wymaga 6 beczek `[założenie: 200 kg na osobę na rok; DO USTALENIA: ilości z raportu agenta 2]`.
- Stado 100 kur zjada 11,8 kg paszy na dobę, czyli 4303 kg na rok `[źródło: S37; obliczenie: 06]`.
- Zapas paszy na 30 dni wynosi 354 kg (0,54 m³). Zapas roczny wymaga silosu 5,7 m³ `[obliczenie: 06]`.

### D10.5. Zamrażarki

| Zamrażarka | Pojemność | Zużycie | Średnia moc | Czas utrzymania bez zasilania | Znacznik |
|---|---|---|---|---|---|
| Kernau KFCF 2905 W | 287 dm³ | 227 kWh/rok | 26 W | brak danej | `[źródło: S47]` |
| Liebherr CFe 2500 | 497 dm³ | 295 kWh/rok | 34 W | 40 h | `[źródło: S48]` |

- 2 zamrażarki zużywają 1,43 kWh na dobę. Podtrzymanie przez 3 doby wymaga 4,3 kWh `[obliczenie: 06]`.
- Zamrażarki należą do klasy 1 odbiorników (tabela A10).
- Zamrażarka w pomieszczeniu od 5 °C do 10 °C zużywa zimą mniej energii `[założenie]`.
- Klasa klimatyczna zamrażarki Kernau obejmuje temperatury otoczenia od 10 °C do 43 °C `[źródło: S47]`.
- Czujnik temperatury wysyła alarm przy temperaturze wyższej niż −15 °C `[założenie]`.

### D10.6. Suszarka i wędzarnia

`m = E·η/0,68`

- m: masa odparowanej wody [kg]. E: energia słoneczna na kolektorze [kWh]. η = 0,25: sprawność suszarki `[założenie]`.
- Kolektor 2 m² odparowuje 3,8 kg wody na dobę w lipcu i 2,9 kg we wrześniu `[obliczenie: 06]`.
- Kolektor 2 m² suszy 4,8 kg świeżych jabłek na dobę w lipcu `[obliczenie: 06]`.
- Suszarka elektryczna 500 W korzysta z nadwyżki fotowoltaiki (5769 kWh w miesiącach V–IX) `[obliczenie: 08]`.
- Wniosek: suszarka elektryczna z nadwyżki jest prostsza. Suszarka solarna jest rezerwą.
- Wędzarnia: komora 0,6 m × 0,6 m × 1,8 m z paleniskiem oddalonym o 2 m do 3 m `[założenie]`.
- Czujnik temperatury w komorze przesyła odczyt do serwera HA `[założenie]`.

# E. Automatyzacja i „pasywność”

## E11. Budynki zwierząt

### E11.1. Kurnik i wybieg dla 100 kur: wymiary

Tabela E1. Normy i wymiary `[obliczenie: 07]`.

| Parametr | Norma konwencjonalna `[źródło: S51]` | Wartość dla 100 kur | Norma ekologiczna `[źródło: S52]` | Wartość dla 100 kur |
|---|---|---|---|---|
| Powierzchnia użytkowa kurnika | co najwyżej 9 kur/m² | 11,1 m² | co najwyżej 6 kur/m² | 16,7 m² |
| Grzędy | co najmniej 15 cm na kurę | 15,0 m | co najmniej 18 cm na kurę | 18,0 m |
| Gniazda pojedyncze | co najwyżej 7 kur na gniazdo | 15 gniazd | 7 kur na gniazdo | 15 gniazd |
| Gniazdo grupowe | co najwyżej 120 kur/m² | 0,83 m² | co najmniej 120 cm² na kurę | 1,2 m² |
| Ściółka | co najmniej 250 cm² na kurę i 1/3 podłogi | 3,7 m² | brak danej | brak danej |
| Karmidła | 10 cm krawędzi na kurę albo 4 cm obwodu na kurę | 10 m albo 4 m | brak danej | brak danej |
| Poidła smoczkowe | co najmniej 1 smoczek na 10 kur | 10 smoczków | brak danej | brak danej |
| Wybieg | brak wartości w rozporządzeniu `[źródło: S51]` | 400 m² przy 4 m² na kurę `[założenie]` | co najmniej 4 m² na kurę | 400 m² |
| Otwory wyjściowe | co najmniej 0,35 m × 0,40 m; 2 m na 1000 kur | 1 otwór 0,40 m | 4 m na 100 m² kurnika | 0,7 m |

- Przepisy szczegółowe § 27–29 obowiązują gospodarstwo, które utrzymuje co najmniej 350 kur `[źródło: S51]`. Raport używa tych przepisów jako wzorca.
- Hodowca MUSI doglądać kury co najmniej 1 raz na dobę `[źródło: S51; relacja: koordynator, 2026-11-11 (Dz.U. 2026 poz. 335)]`.
- Wyposażenie automatyczne, od którego zależy dobrostan, wymaga kontroli co najmniej 1 raz na dobę `[źródło: S53]`.
- Oświetlenie sztuczne MUSI zapewnić ciągłą ciemność przez 1/3 doby `[źródło: S51]`.
- Wybieg nieutwardzony MUSI leżeć co najmniej 70 m od studni. Kurnik MUSI stać co najmniej 15 m od studni `[relacja: koordynator, 2026-11-11]`.
- Propozycja: kurnik 4 m × 6 m (16,7 m² dla kur i 7 m² śluzy z magazynem paszy) `[założenie]`.
- Propozycja: woliera zadaszona od 30 m² do 40 m² na czas nakazu zamknięcia drobiu `[założenie]`.
- Propozycja: wybieg od 400 m² do 800 m² w 4 kwaterach z rotacją `[założenie]`.

### E11.2. Kurnik: wyposażenie automatyczne

Tabela E2. Klasy urządzeń `[założenie: moc i cena]`.

| Funkcja | Rozwiązanie | Moc | Cena |
|---|---|---|---|
| Klapa | Sterownik z czujnikiem światła i z zegarem, zasilanie z baterii lub 12 V, blokada przed drapieżnikiem `[źródło: S55]` | mniej niż 2 W | 400–1200 PLN |
| Pasza | 4 karmidła tubowe po 25 kg (zapas 8 dni) albo zasobnik 0,6 m³ z paszociągiem (zapas 30 dni) | silnik 0,37 kW przez 5 min na dobę | 400–15 000 PLN |
| Woda | Zbiornik 60 dm³ z zaworem pływakowym, linia 10 smoczków, reduktor ciśnienia | 0 W | 300–900 PLN |
| Ochrona poideł przed mrozem | Zbiornik w skrzyni ocieplonej, grzałka 50 W z termostatem, przewód grzejny 10 W/m | 30–150 W średnio w mróz | 300–1100 PLN |
| Gniazda | Gniazda wykotowe: jajo stacza się do zamkniętej rynny | 0 W | 1500–4000 PLN |
| Odchody | Ruszt pod grzędami z pomiotnikiem albo głęboka ściółka | 0 W | 500–1500 PLN |
| Wentylacja | Wloty z przepustnicą i kominek; wentylator 30 W latem | 0–30 W | 300–1500 PLN |
| Oświetlenie | LED 2700 K do 3000 K ze ściemnianiem | 20 W | 300–800 PLN |
| Ogrodzenie | Siatka zgrzewana o oczku co najwyżej 19 mm, fartuch 0,5 m, siatka górna, elektryzator co najmniej 1 J | 5 W | 7000–17 000 PLN |
| Monitoring | 2 kamery PoE, waga zasobnika paszy (4 belki tensometryczne), przepływomierz wody, czujniki temperatury, wilgotności, CO₂ i NH₃ | 15 W | 1200–3500 PLN |

- Smoczek POWINIEN dawać co najmniej 60 ml wody na minutę `[źródło: S37]`.
- Wentylacja 100 kur: od 70 m³/h do 85 m³/h przy −23 °C; od 934 m³/h do 1200 m³/h przy 32 °C `[źródło: S37; obliczenie: 07]`.
- Stężenie amoniaku POWINNO być mniejsze niż 25 ppm. Stężenie CO₂ POWINNO być mniejsze niż 5000 ppm `[źródło: S37]`.
- Ściółka POWINNA mieć wilgotność od 25 % do 30 % `[źródło: S37]`.
- Zegar astronomiczny otwiera klapę 30 min po wschodzie Słońca i zamyka 30 min po zachodzie `[założenie]`.
- Kontaktron klapy wysyła alarm, jeżeli klapa nie jest zamknięta 45 min po zachodzie Słońca `[założenie]`.
- Zabezpieczenie przed kuną: każdy otwór większy niż 25 mm ma siatkę `[założenie]`.

### E11.3. Kozy lub owce mleczne (od 2 do 4 sztuk) i pszczoły

- Hodowca MUSI doglądać owce i kozy co najmniej 1 raz na dobę `[źródło: S54]`.
- Hodowca MUSI karmić owce i kozy co najmniej 2 razy na dobę `[źródło: S54]`.
- Dojenie 1 raz albo 2 razy na dobę nie podlega automatyzacji przy stadzie od 2 do 4 sztuk `[założenie]`.
- Poidło: miska z zaworem pływakowym na linii ze zbiornika górnego, z grzałką 30 W do 80 W i z termostatem `[założenie]`.
- Paśnik: paśnik z dachem na 1 balot siana, zapas od 5 dni do 10 dni dla 4 sztuk `[założenie]`.
- Lizawka solna i waga zasobnika paszy treściwej uzupełniają wyposażenie `[założenie]`.
- Ogrodzenie: siatka elektryczna od 0,9 m do 1,1 m. Woltomierz ogrodzenia wysyła alarm przy napięciu mniejszym niż 3 kV `[założenie]`.
- Waga ula: 4 belki tensometryczne po 50 kg, wzmacniacz HX711, moduł ESP32 z radiem LoRa, panel 5 W `[założenie]`.
- Waga ula mierzy masę co 15 min z rozdzielczością 0,1 kg `[założenie]`.
- Alarmy ula: spadek masy o więcej niż 1 kg w czasie 1 h (rójka albo kradzież); spadek zapasów zimą `[założenie]`.
- Czujnik temperatury w gnieździe wykrywa czerwienie: temperatura od 34 °C do 35 °C `[założenie]`.
- Koszt wagi ula: od 150 PLN do 300 PLN (budowa własna) albo od 800 PLN do 2500 PLN (gotowa) `[założenie]`.

## E12. Automatyka upraw

- Nawadnianie kroplowe: 3 sekcje po 2,2 m³/h na 1000 m², filtr dyskowy, reduktor ciśnienia, elektrozawory `[obliczenie: 05]`.
- Elektrozawór jest zamknięty bez napięcia. Zawór główny odcina wodę przy awarii sterownika `[założenie]`.
- Komponent „sprinkler” oprogramowania ESPHome obsługuje sekcje, zawór główny, pompę, kolejkę i mnożnik czasu `[źródło: S56]`.
- Integracja Smart Irrigation liczy ewapotranspirację według FAO-56 i prowadzi bilans wody dla każdej sekcji `[źródło: S58]`.
- Integracja Smart Irrigation pobiera pogodę z serwisu Open-Meteo, OpenWeatherMap albo Pirate Weather `[źródło: S58]`.
- Reguła dla gleby lekkiej: sterownik podaje dawkę od 11 mm do 16 mm, gdy bilans wody spada o 12,6 mm `[obliczenie: 10]`.
- Tensjometr albo czujnik pojemnościowy na głębokości 0,15 m i 0,30 m koryguje bilans `[założenie]`.
- Sterownik wstrzymuje nawadnianie, jeżeli prognoza opadu na 24 h przekracza 5 mm `[założenie]`.
- Tunel: siłowniki woskowe otwierają okna bez prądu. Silnik 24 V zwija boki tunelu według temperatury `[założenie]`.
- Robot koszący bez przewodu ograniczającego kosi sad i obrzeża. Robot ładuje akumulator w godzinach 10:00–15:00 `[założenie]`.

## E13. Architektura sterowania i zachowanie przy awarii

- Serwer HA pracuje na komputerze o mocy 10 W z dyskiem SSD `[założenie]`.
- Węzły ESP32 z oprogramowaniem ESPHome wykonują logikę lokalnie. Awaria serwera HA nie zatrzymuje węzłów `[założenie]`.
- Sieć: Ethernet z zasilaniem PoE do budynków w odległości co najwyżej 100 m; Zigbee w domu `[założenie]`.
- Radio LoRa łączy punkty odległe: pasiekę, zbiornik górny, wybieg. ESPHome obsługuje układy SX1276 do SX1279 `[źródło: S57]`.
- Zasilanie buforowe: akumulator LiFePO4 12,8 V 100 Ah (1,28 kWh) zasila serwer i sieć (36 W) przez 35 h `[obliczenie: 1280 Wh / 36 W; założenie]`.
- Alarmy: powiadomienie aplikacji HA, komunikator, SMS z modemu LTE, syrena lokalna `[założenie]`.

Tabela E3. Zachowanie przy awarii `[założenie]`.

| Układ | Awaria | Stan bezpieczny | Alarm |
|---|---|---|---|
| Woda dla zwierząt | Brak prądu albo awaria pompy | Zbiornik górny i zbiornik 60 dm³ zasilają poidła grawitacyjnie przez co najmniej 3 doby | Przepływ równy 0 przez 12 h; poziom zbiornika mniejszy niż 30 % |
| Klapa kurnika | Awaria sterownika | Sterownik klapy działa z własnej baterii, bez serwera HA; blokada mechaniczna trzyma klapę | Klapa otwarta 45 min po zachodzie Słońca |
| Pompa głębinowa | Suchobieg, przeciążenie, pęknięcie rury | Ochrona silnika wyłącza pompę `[źródło: S63]`; sterownik ogranicza czas pracy do 60 min | Praca dłuższa niż 60 min; przepływ w nocy |
| Kocioł | Brak prądu podczas palenia | Zasilacz awaryjny pompy ładującej; zawór bezpieczeństwa 2,5 bar; zawór schładzający | Góra bufora A ma więcej niż 92 °C; dół C ma więcej niż 70 °C |
| Zamrażarki | Brak prądu | Klasa 1 odbiorników; czas utrzymania 40 h `[źródło: S48]` | Temperatura wyższa niż −15 °C |
| Magazyn energii | Niski SOC | Falownik zrzuca klasę 3 i uruchamia agregat przy SOC 15 % | SOC mniejszy niż 20 %; agregat nie wystartował |
| Nawadnianie | Awaria sterownika albo pęknięcie linii | Elektrozawory zamknięte bez napięcia; limit czasu sekcji w węźle | Przepływ większy niż 130 % wartości sekcji |
| Piwnica | Mróz albo awaria siłownika | Przepustnice zamknięte sprężyną; grzałka 100 W | Temperatura mniejsza niż 1 °C albo większa niż 10 °C |
| Serwer HA | Zawieszenie | Węzły pracują lokalnie; układ watchdog restartuje serwer | Brak sygnału życia przez 10 min |

## E14. Realizm: praca po automatyzacji

Tabela E4. Nakłady pracy [h/rok] `[obliczenie: 07, założenie]`.

| Czynność | Od | Do |
|---|---|---|
| Warzywnik od 1000 m² do 2000 m²: siew, sadzenie, pielenie, zbiór | 300 | 700 |
| Pole co najwyżej 0,9 ha, z usługami maszynowymi | 30 | 100 |
| Kury: kontrola i zbiór jaj, od 10 min do 15 min na dobę | 61 | 91 |
| Kury: pasza, poidła, ściółka, wymiana ściółki 2 razy na rok | 60 | 100 |
| Ubój i obróbka od 50 do 100 sztuk drobiu | 13 | 33 |
| Kozy lub owce mleczne, od 2 do 4 sztuk: dojenie, karmienie, ściółka, racice | 250 | 500 |
| Przerób mleka | 80 | 200 |
| Pszczoły, od 3 do 5 uli | 45 | 100 |
| Drewno od 9 mp do 16 mp: ścinka, zrywka, cięcie, łupanie, układanie | 30 | 80 |
| Kocioł: załadunek, czyszczenie, popiół | 45 | 70 |
| Przetwórstwo i przechowywanie | 120 | 250 |
| Kontrola piwnicy i zapasów | 15 | 40 |
| Utrzymanie instalacji: fotowoltaika, magazyn, agregat, woda, HA, ogrodzenia | 50 | 90 |
| Suma | 1099 | 2354 |

- Średnia wynosi od 21 h do 45 h na tydzień `[obliczenie: 07]`.
- Sezon V–X: od 28 h do 61 h na tydzień. Zima XI–IV: od 14 h do 29 h na tydzień `[obliczenie: 07]`.
- Bez kóz, owiec i pszczół suma wynosi od 724 h do 1554 h na rok `[obliczenie: 07]`.
- Łuparka hydrauliczna łupie od 3 mp do 5 mp na godzinę `[źródło: S30]`.
- Uprawa marchwi z kombajnem zużywa od 254 h do 475 h pracy na 1 ha `[źródło: S59]`. Warzywnik ręczny zużywa więcej pracy na 1 m².
- Czynności bez automatyzacji:
  - codzienna kontrola zdrowia zwierząt (obowiązek prawny);
  - dojenie i karmienie kóz lub owiec 2 razy na dobę;
  - zbiór warzyw i owoców, siew i sadzenie;
  - ubój i obróbka drobiu;
  - przetwórstwo: wekowanie, kiszenie, serowarstwo;
  - ścinka, łupanie i załadunek kotła;
  - przeglądy uli;
  - naprawy i czyszczenie instalacji.
- Wniosek: nieobecność dłuższa niż 24 h wymaga osoby zastępczej `[źródło: S51, S53, S54]`.
- Raport nie ustalił, czy kontrola przez kamerę spełnia obowiązek doglądania `[DO USTALENIA: Powiatowy Lekarz Weterynarii w Olsztynie]`.

## E15. Kosztorys i etapy

Tabela E5. Kosztorys orientacyjny [PLN brutto, 2026] `[obliczenie: 07, założenie]`.

| Etap | Zakres | Od | Do |
|---|---|---|---|
| 0 | Badanie wody, pomiary zużycia energii i wiatru, projekt, uzgodnienie przeciwpożarowe | 1300 | 4500 |
| 1 | Woda: pompa z łagodnym rozruchem, zbiornik przeponowy, uzdatnianie, zbiornik górny, deszczówka | 12 700 | 41 000 |
| 2 | Ciepło: włączenie buforów 2000 dm³, naczynie 300 dm³, zasobnik 300 dm³ z grzałką, wiata na drewno, łuparka | 17 000 | 37 500 |
| 3 | Energia off-grid: 15 kWp, 30 kWh, falownik wyspowy, agregat LPG | 89 500 | 176 500 |
| 4 | Magazyn żywności: piwnica ziemna, regały, zamrażarki, beczki, suszarka, wędzarnia | 24 500 | 72 500 |
| 5 | Zwierzęta: kurnik, woliera, wybieg, wyposażenie, kozy lub owce, pasieka, monitoring | 39 800 | 122 000 |
| 6 | Uprawy i automatyka: nawadnianie, czujniki, tunel, robot, serwer HA i sieć | 19 000 | 48 000 |
| Suma | | 203 800 | 502 000 |

- Bufory i studnia istnieją. Kosztorys nie zawiera zakupu buforów ani wiercenia studni.
- Zbiornik 1000 dm³ kosztuje od 3099 PLN do 3999 PLN. Zasobnik 300 dm³ z 2 wężownicami kosztuje 3199 PLN `[źródło: S20]`.
- Zamrażarka Liebherr CFe 2500 kosztuje 3199 PLN `[źródło: S48]`.
- Magazyn 20 kWh kosztował 20 000 PLN w zestawie budżetowym. Magazyn 23 kWh kosztował więcej niż 43 000 PLN w zestawie premium `[źródło: S21]`.
- Pozostałe ceny są szacunkiem autora `[DO USTALENIA: oferty wykonawców]`.

Kolejność etapów `[założenie]`:

1. Etap 0: pomiary. Powód: wyniki zmieniają dobór każdego urządzenia.
2. Etap 2: bufory. Powód: zbiorniki stoją na miejscu, a bufor zmniejsza zużycie drewna o 20 % do 30 % `[źródło: S28]`.
3. Etap 1: woda. Powód: pompa z łagodnym rozruchem jest warunkiem pracy off-grid.
4. Etap 3: energia off-grid w 2 krokach: najpierw 15 kWp z magazynem 30 kWh, potem agregat z automatycznym startem.
5. Etap 4: magazyn żywności przed pierwszym pełnym sezonem upraw.
6. Etap 5: zwierzęta, po uruchomieniu wody i zasilania.
7. Etap 6: automatyka upraw, równolegle z etapami 4 i 5.

# Źródła

| Nr | Źródło |
|---|---|
| S1 | Global Solar Atlas (Solargis, Bank Światowy), punkt 53,7625° N, 20,4667° E: https://api.globalsolaratlas.info/data/lta?loc=53.7625,20.4667 |
| S2 | Ministerstwo: typowe lata meteorologiczne, stacja Olsztyn 122720: https://www.gov.pl/web/archiwum-inwestycje-rozwoj/dane-do-obliczen-energetycznych-budynkow ; https://www.gov.pl/documents/33377/436740/wmo122720iso_stat.txt |
| S3 | Golisz E. i in., 2020, „Efficiency analysis of photovoltaic systems”, E3S Web of Conferences 154, 05003: https://www.e3s-conferences.org/articles/e3sconf/pdf/2020/14/e3sconf_icores2020_05003.pdf |
| S4 | IMGW-PIB, Informator Meteorologiczny CMM nr 36, grudzień 2024: https://cmm.imgw.pl/wp-content/uploads/production/informator/202412C.pdf |
| S5 | IMGW-PIB, Biuletyn PSHM, grudzień 2024: https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/Biuletyn_PSHM/Biuletyn_PSHM_2024_12_(grudzien).pdf |
| S6 | Bartoszek K., Matuszko D., Soroka J., 2020, Atmospheric Research 245, 105097: https://core.ac.uk/download/344347373.pdf |
| S7 | Normy klimatyczne IMGW 1991–2020 dla Olsztyna (tabela w Wikipedii): https://en.wikipedia.org/wiki/Olsztyn |
| S8 | Pożarska K., Grabowski J., 2015, Woda-Środowisko-Obszary Wiejskie 15(4): https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-90f3de25-622f-43ec-97d7-39884f7eef3a/c/Pozarska_Grabowski.pdf |
| S9 | Gramwzielone.pl, 2026-10-15, badanie IMGW-PIB małych turbin (Jurasz i in., „Energy”): https://www.gramwzielone.pl/?p=20381358 |
| S10 | Ministerstwo Klimatu i Środowiska, zmiany dla prosumentów: https://www.gov.pl/web/klimat/korzystne-zmiany-dla-prosumentow-wchodza-w-zycie |
| S11 | Ustawa z 2024-11-27, Dz.U. 2024 poz. 1847: https://api.sejm.gov.pl/eli/acts/DU/2024/1847/text.html |
| S12 | GLOBEnergia, net-billing (stan 2026-09-16): https://globenergia.pl/net-billing-jak-dziala-system-rozliczen-prosumentow/ |
| S13 | Gramwzielone.pl, nowe zasady instalacji magazynów energii: https://www.gramwzielone.pl/?p=20346623 |
| S14 | GLOBEnergia, ustawa z 2025-12-04 o zmianie Prawa budowlanego: https://globenergia.pl/magazyny-energii-z-duzymi-ograniczeniami-prezydent-podpisal-ustawe/ |
| S15 | GLOBEnergia, 2026-09-01, warunki techniczne WT 2026: https://globenergia.pl/zle-przepisy-dla-magazynow-energii-poczekaja-ale-w-koncu-wejda-w-zycie-polacy-zyskali-18-miesiecy/ |
| S16 | gov.pl, uzgodnienie przeciwpożarowe instalacji większej niż 6,5 kW: https://www.gov.pl/web/kontaktoze/uzgodnienie-projektu-instalacji-z-rzeczoznawca-ds-zabezpieczen-przeciwpozarowych-pod-wzgledem-zgodnosci-urzadzen-z-wymaganiami-ochrony-przepisow-przeciwpozarowych-ppoz |
| S17 | Enerad.pl, zgłoszenie magazynu energii do OSD: https://enerad.pl/jak-zglosic-magazyn-energii/ |
| S18 | GLOBEnergia, 2026-04-30, certyfikaty NC RfG i WOS 2025: https://globenergia.pl/masz-juz-falownik-lub-magazyn-energii-po-tych-zmianach-mozesz-miec-problem-z-przylaczeniem/ |
| S19 | Gramwzielone.pl, 2026-01-23, projekt programu dotacji magazynów: https://www.gramwzielone.pl/?p=20348164 |
| S20 | Murator, 2026-07-02, ceny magazynów ciepła: https://muratordom.pl/instalacje/instalacja-grzewcza/ile-kosztuje-magazyn-ciepla-w-2026-roku-sprawdzamy-ceny-buforow-i-zasobnikow-aa-sbW6-25GV-oZnD.html |
| S21 | GLOBEnergia, 2026-03-21, ceny fotowoltaiki z magazynem: https://globenergia.pl/ile-kosztuje-fotowoltaika-z-magazynem-energii-na-wiosne-2026-roku-analizujemy-ceny/ |
| S22 | KB.pl, 2026-02-13, ceny fotowoltaiki: https://kb.pl/aktualnosci/fotowoltaika/ceny-fotowoltaiki-w-2026/ |
| S23 | Honda EU32i, karta produktu: https://www.mojahonda.pl/download/agregaty/EU32i_karta.pdf |
| S24 | All Power Labs, PP30 Power Pallet: https://allpowerlabs.com/wp-content/uploads/2019/06/PP30OneSheet2_1_23.pdf |
| S25 | Pylontech US5000, dane: https://www.portlandiaelectric.supply/pages/specs-us5000 |
| S26 | Atmos, kotły zgazowujące drewno, dane DC18S: https://atmos.eu/en/product/gasification-boilers-for-wood-drevoplyn |
| S27 | Atmos, instrukcja kotłów DCxxS (wersja niemiecka): https://atmos.eu/wp-content/uploads/2021/03/GSxx_DCxxS.pdf |
| S28 | Atmos, zbiorniki akumulacyjne: https://www.atmos.eu/en/accessories/accumulation-tanks/ |
| S29 | LWF Bayern, Merkblatt 12 „Der Energieinhalt von Holz”, 2024: https://lfl.bayern.de/mam/cms04/service/dateien/mb12_energiegehalt-2024_rz_web_bf.pdf |
| S30 | LWF Bayern, Merkblatt 20 „Scheitholz”, 2023: https://lwg.bayern.de/mam/cms04/service/dateien/mb20_scheitholz_2023_rz_web_bf.pdf |
| S31 | LWF Wissen 42, „Das Holz der Schwarzerle”: https://lwg.bayern.de/mam/cms04/forsttechnik-holz/dateien/w42_das_holz_der_schwarzerle-eigenschaften_verwendung.pdf |
| S32 | BULiGL, Wielkoobszarowa inwentaryzacja stanu lasów 2020–2024: https://bdl.lasy.gov.pl/portal/Media/Default/Publikacje/WISL2020-2024.pdf |
| S33 | Stolarski M.J. i in., 2015, Bioenergy Research 8: 1136–1147: https://link.springer.com/content/pdf/10.1007/s12155-014-9567-9.pdf |
| S34 | EnergieSchweiz (BFE), „Dimensionierungshilfe Holzheizungen”, 2015 (wzór PN-EN 303-5): https://pubdb.bfe.admin.ch/de/publication/download/2784 |
| S35 | UDT, „Inspektor” 4/2023, badania kotłów na paliwa stałe: https://www.udt.gov.pl/images/biuro-prasowe/files/pdf/INSPEKTOR_4_2023_Badania-urzadzen-grzewczych-na-paliwa_stale-WCAG.pdf |
| S36 | Bosch, karta zbiorników buforowych BH (04.2026): https://www.bosch-homecomfort.com/pl/media/country_pool/dokumenty/dlaprofesjonalistow/bosch_hc_karta_katalogowa_zbiornik_buforowy_bh_04.2026.pdf |
| S37 | Hy-Line Brown, Alternative Systems Management Guide: https://www.hyline.com/filesimages/Hy-Line-Products/Hy-Line-Product-PDFs/Brown/Brown%20Alt/BRN%20ALT%20COM%20ENG.pdf |
| S38 | Uniwersytet Przyrodniczy w Poznaniu, wykład „Gospodarka wodna”: https://sparrow.up.poznan.pl/kiwis/dydaktyka/gospwod/gosp5.pdf |
| S39 | Rozporządzenie Ministra Zdrowia z 2026-05-22, Dz.U. 2026 poz. 748: https://api.sejm.gov.pl/eli/acts/DU/2026/748/text.pdf |
| S40 | Ustawa z 2026-03-13, Dz.U. 2026 poz. 605: https://eli.gov.pl/api/acts/DU/2026/605/text/T/D20260605L.pdf |
| S41 | PSSE Nowy Dwór Mazowiecki, nowe przepisy o jakości wody: https://www.gov.pl/web/psse-nowy-dwor-mazowiecki/nowe-przepisy-dotyczace-jakosci-wody-przeznaczonej-do-spozycia |
| S42 | Land Oberösterreich, „Infoblatt UV-Desinfektionsanlagen” (ÖNORM M 5873): https://www.land-oberoesterreich.gv.at/Mediendateien/Formulare/Dokumente%20UWD%20Abt_WW/Infoblatt_UV-Desinfektionsanlagen_WW.pdf |
| S43 | CDC, dezynfekcja wody w sytuacji awaryjnej: https://www.cdc.gov/water-emergency/about/index.html |
| S44 | Murator, głębokość przemarzania gruntu: https://muratordom.pl/budowa/fundamenty/glebokosc-przemarzania-gruntu-jaka-powinna-byc-minimalna-glebokosc-fundamentow-czy-instalacji-mapa-aa-hm1u-1qbz-ZfQB.html |
| S45 | Blog OnGeo, strefy przemarzania: https://blog.ongeo.pl/strefa-sniegowa-wiatrowa-przemarzanie-gruntu-projekt-domu |
| S46 | Inżynier Budownictwa, przemarzanie gruntu: https://inzynierbudownictwa.pl/przemarzanie-gruntu-a-projektowanie-fundamentow/ |
| S47 | Kernau KFCF 2905 W, karta informacyjna: https://kernau.com/storage/file/pimcore_import/2026/4/15/82575bef3413c773b2eb7f078158de03/zamrazarka-skrzyniowa-kernau-kfcf-2905-w-karty-informacyjne.pdf |
| S48 | Liebherr CFe 2500, dane i cena: https://www.euro.com.pl/zamrazarki/liebherr-cfe-2500.bhtml |
| S49 | University of Alaska Fairbanks, Cooperative Extension, „Vegetable Storage in Root Cellars”: https://www.uaf.edu/ces/publications/database/food/vegetable-storage.php |
| S50 | IOR-PIB, 2017, „Metodyka integrowanej ochrony magazynów zbożowych”: https://www.ior.poznan.pl/plik,3170,metodyka-integrowanej-ochrony-magazynow-zbozowych-pdf.pdf |
| S51 | PIW Sławno, streszczenie rozporządzenia MRiRW z 2010-02-15 (Dz.U. 2010 nr 56 poz. 344), kury nieśne: https://fs.siteor.com/piw-slawno/files/Downloads/20130204123001/dobrostan_ciel%C4%99ta__%C5%9Bwinie__nioski.pdf?1359981003 |
| S52 | Rozporządzenie wykonawcze Komisji (UE) 2020/464, załącznik I część IV: https://www.inforlex.pl/download/akty_pdf,E0L,2020,98,2.pdf |
| S53 | Dyrektywa Rady 98/58/WE, załącznik, punkty 2 i 13: https://www.legislation.gov.uk/eudr/1998/58/annex |
| S54 | Rozporządzenie MRiRW z 2010-06-28, tekst jednolity z 2019 r., § 5 i § 9: https://api.sejm.gov.pl/eli/acts/DU/2019/1966/text.html |
| S55 | Kerbl, automatyczne klapy do kurnika: https://www.kerbl.com/en/hobbyfarming/poultry-farming/automatic-chicken-door |
| S56 | ESPHome, komponent „sprinkler”: https://esphome.io/components/sprinkler/ |
| S57 | ESPHome, komponent SX127x: https://esphome.io/components/sx127x/ |
| S58 | Smart Irrigation dla Home Assistant, wersja 2026.10.2: https://github.com/jeroenterheerdt/HAsmartirrigation |
| S59 | Kowalczuk J., Leszczyński N., 2005, Problemy Inżynierii Rolniczej 4: 101–108: https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-article-BAR0-0015-0084/c/httpwww_ibmer_waw_plpir2005pelne4kowalczukp.pdf |
| S60 | klimaaktiv, „Heizwerttabellen”, 2023: https://www.klimaaktiv.at/dam/jcr:6bceb809-17bd-4d9f-88d0-9e9e4ee2ef87/Heizwerttabellen_Werkzeuge_2023%2004%2026.pdf |
| S61 | Kalbarczyk R. i in., usłonecznienie na Nizinie Szczecińskiej 2000–2004: https://agro.icm.edu.pl/agro/element/bwmeta1.element.agro-792356ae-54bd-4f01-97f2-7108da7d0b4c/c/art13_114.pdf |
| S62 | Atmos, schemat podłączenia z zaworem Laddomat i ze zbiornikami (wersja polska): https://www.atmos.eu/wp-content/uploads/2023/05/Zapojeni-ATMOS-F12-Laddomat-s-akumulacni-bez-akumulacni-nadrze_PL.pdf |
| S63 | Grundfos, broszura pomp SQ i SQE: https://www.grundfos.com/content/dam/global/activity-assets/isolutions-wu/documents-and-cases/brochures/4014270%20WU_Submersible_Content_SQ_SQE_Brochure_GPL.pdf |
| S64 | FAO Irrigation and Drainage Paper 56, rozdziały 6 i 8: https://www.fao.org/4/x0490e/x0490e0b.htm ; https://www.fao.org/4/x0490e/x0490e0e.htm |

# Decyzje i braki (luki i niepewności)

| Nr | Temat | Brak albo sprzeczność | Wybór w raporcie |
|---|---|---|---|
| 1 | PVGIS | Interfejs PVGIS odrzucił zapytanie narzędzia. | Global Solar Atlas, typowy rok meteorologiczny i pomiar z roku 2017. |
| 2 | Uzysk zimowy | Global Solar Atlas podaje dla grudnia 23,4 kWh/kWp. Pomiar z roku 2017 dał 11,3 kWh/kWp. | 2 scenariusze: P50 i konserwatywny. Projekt off-grid według scenariusza konserwatywnego. |
| 3 | Serie dni bez słońca | Brak statystyki dla Olsztyna. Brak danych dobowych. | Seria 11 dni z uzyskiem 20 % średniej. Zmienność dobowa jest założeniem. |
| 4 | Zużycie energii | Brak pomiaru zużycia domu. Lista odbiorników jest szacunkiem. | Scenariusz M = 5000 kWh/rok; tryb zimowy 8,0 kWh na dobę. |
| 5 | Dom | Brak powierzchni ogrzewanej, wskaźnika EU, rodzaju grzejników i modelu kotła. | Macierz 120, 160, 200 m² i EU 60, 100, 150. |
| 6 | Sprawność kotła | Producent podaje 90,1 % i 82,0 % bez definicji drugiej wartości. | Sprawność sezonowa 0,78. |
| 7 | Las | Brak wieku, składu i zasobności drzewostanu. Brak przyrostu dla olszy i dla regionu. | Przyrost 6,00; 8,31; 9,94 m³/ha; pozysk 70 % przyrostu. |
| 8 | Gęstość drewna | Brak danych źródłowych dla brzozy, olszy, wierzby i robinii w źródle S29. | Brzoza i olsza z gęstości w źródle S31; wierzba i robinia jako założenie. |
| 9 | Bufory | Brak izolacji, ciśnienia dopuszczalnego i króćców istniejących zbiorników. Brak wartości Q_min kotła. | Strata według granicy klasy C; połączenie szeregowe. |
| 10 | Wężownica schładzająca | Raport nie sprawdził instrukcji kotła. | Zalecenie: zasilacz awaryjny pompy i zapas wody pod ciśnieniem. |
| 11 | Studnia | Brak głębokości, zwierciadła wody, wydajności i wyniku badania wody. | H_geo = 12 m; dobór złoża po badaniu. |
| 12 | Normy zużycia wody | Raport nie odczytał tabel rozporządzenia z 2002-01-14. | Pomiar z Poznania: 110 dm³ na osobę na dobę. |
| 13 | Gleba | Brak pomiaru pojemności wodnej gleby. | Piasek gliniasty: 90 mm/m; piasek luźny: 60 mm/m. |
| 14 | Głębokość przemarzania | Źródła S44, S45, S46 podają różne strefy dla Olsztyna. | Przemarzanie 1,2 m; przykrycie rur 1,6 m. |
| 15 | Woda kempingu | Brak informacji o źródle wody kempingu. | Studnia domowa bez obowiązku badań; kemping do sprawdzenia w PSSE. |
| 16 | Współczynnik 1,23 | Źródła S10 i S11 nie podają zakresu. | Dotyczy tylko wariantów z siecią. |
| 17 | WT 2026 | Stan prawny znany na dzień 2026-09-01. | Magazyn 30 kWh bez formalności. |
| 18 | Dotacje | Źródła S19 i S20 podają różne stawki. Program wymaga przyłączenia do sieci. | Kosztorys bez dotacji. Zakres agenta 1. |
| 19 | Ceny | Źródła S21 i S22 dają różny koszt 1 kWp. Ceny wyposażenia są szacunkiem. | Zakresy „od–do”; oferty wykonawców do zebrania. |
| 20 | Rozporządzenie z 2010-02-15 | Raport zna treść tylko ze streszczenia PIW. Serwis ISAP odrzucił zapytanie. | Normy jako wzorzec; obowiązek kontroli potwierdza koordynator (Dz.U. 2026 poz. 335). |
| 21 | Ciepło kur | Wzór CIGR pochodzi z pamięci autora. | Wynik orientacyjny: 808 W na 100 kur. |
| 22 | Zapasy żywności | Ilości na osobę są szacunkiem roboczym. | Wymiary piwnicy do korekty po raporcie agenta 2. |
| 23 | Powierzchnia pola | Zlecenie podaje pola od 1 ha do 2 ha. Działka 16/1 ma 1,17 ha razem z siedliskiem. | Praca dla pola co najwyżej 0,9 ha. |
| 24 | Pompa na prąd stały | Raport nie odczytał karty pompy. | Zalecenie: pompa z łagodnym rozruchem `[źródło: S63]`. |
| 25 | Pliki obliczeń | Agent 2 nadpisał plik `dane.py` w katalogu wspólnym. | Skrypty agenta 3 leżą w katalogu `calc/agent3/`. Plik agenta 2 pozostał bez zmian. |

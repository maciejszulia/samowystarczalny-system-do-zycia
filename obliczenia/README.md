# Obliczenia

Katalog zawiera skrypty i dane, z których pochodzą liczby projektu. Skrypty są zapisem obliczeń. Żaden skrypt nie pobiera danych z sieci: dane wejściowe leżą w plikach albo w kodzie skryptu.

## Katalogi

| Katalog | Autor obliczeń | Zakres |
|---|---|---|
| `R1/` | agent 1 | Geometria działek w promieniu 500 m, powierzchnie, wysokości i spadki z siatki 305 punktów. |
| `R2/` | agent 2 | Dieta 4 osób, plony i powierzchnie upraw, stado drobiu, plan gruntu. |
| `R3/` | agent 3 | Zasób słoneczny, profil zużycia, bilans fotowoltaiki i magazynu energii, ciepło, woda, magazyn żywności, kurnik, praca, koszty, nawadnianie. |
| `koordynator/` | koordynator | Strefy, spadki, rysunki projektu, synteza przydziału gruntu, wyniki PVGIS, kontrola PK. |
| `koordynator/dsm/` | koordynator | Profil horyzontu stelaża i kontrola położenia Słońca (raport R4). |
| `koordynator/viz3d/` | koordynator | Dane modelu 3D. |

Plik `dzialki_wkt.txt` zawiera geometrię 4 działek gospodarstwa w układzie PL-1992 (EPSG:2180) `[źródło: GUGiK, usługa ULDK]`.

## Skrypty

| Skrypt | Wynik |
|---|---|
| `R1/area.py` | Powierzchnia każdej działki i odległość od punktu adresowego. |
| `R1/elev_an.py` | Wysokości i spadki działek z plików `elev1.txt` i `elev2.txt`. |
| `R1/plot.py` | Szkic działek `parcels.png`. |
| `R2/a_dieta.py` | Normy żywienia i dieta modelowa. |
| `R2/b_plony_powierzchnia.py` | Tabela upraw i powierzchnia na osobę. |
| `R2/c_drob.py` | Skład stada, jaja, mięso, pasza, obornik. |
| `R2/f_plan.py` | Plan dla 4 osób na gruncie gospodarstwa. |
| `R2/zloz.py` | Raport R2 złożony z szablonów `tpl/` i z tabel `out/`. |
| `R3/01_pv_zasob.py` do `R3/10_nawadnianie.py` | 10 kroków obliczeń raportu R3. Skrypty 03, 04 i 08 czytają pliki `wynik_pv.json` i `wynik_profil.json`. |
| `koordynator/parcels.py` | Plik `parcels.json`: geometria 4 działek. |
| `koordynator/nmt.py` | Plik `nmt_pts.json`: wysokości punktów siatki. |
| `koordynator/figs.py` | Rysunek 1 i rysunek 2 projektu oraz siatka wysokości `gz.npy`. |
| `koordynator/zones.py` | Strefy: pliki `zones.json` i `zones_stats.json`. |
| `koordynator/zones2.py`, `koordynator/slopeclass.py` | Powierzchnie stref w klasach spadku. |
| `koordynator/figC.py` | Rysunek 3 projektu i plik `zone_areas.json`. |
| `koordynator/figDE.py` | Rysunek 5 i rysunek 6 projektu oraz plik `praca.json`. |
| `koordynator/synth.py` | Przydział gruntu ornego do grup upraw i pokrycie diety. |
| `koordynator/pvgis_shs.py` | Tabela dni pustych z wyników PVGIS 5.3. |
| `koordynator/pk_check.py` | Kontrola PK: długość zdań i słowa zakazane. |
| `koordynator/dsm/hz_data.py` | Profile horyzontu dla linii stelaża A, B i C. |
| `koordynator/dsm/sun_check.py` | Godziny Słońca nad horyzontem 21 grudnia. |
| `koordynator/viz3d/prep1.py` | Komórki budynków `bld1m.npy` z modelu pokrycia terenu. |
| `koordynator/viz3d/prep2.py` | Pliki modelu 3D: `data.js`, `orto.jpg`, `zones.png`, `plan.png`. |
| `koordynator/viz3d/shot.py` | Zrzuty ekranu modelu 3D w przeglądarce bez okna. |

## Uruchomienie

Skrypty czytają pliki ścieżką względną. Uruchom skrypt z katalogu, w którym skrypt leży.

```sh
cd obliczenia/koordynator && python3 figC.py
```

Rozbicie:

- `cd obliczenia/koordynator`: przechodzi do katalogu skryptu.
- `&&`: uruchamia drugie polecenie tylko po sukcesie pierwszego polecenia.
- `python3 figC.py`: uruchamia skrypt, który rysuje plan stref.

Wymagania: Python 3 oraz pakiety `numpy`, `scipy`, `shapely`, `pyproj`, `matplotlib` i `pillow`. Claude uruchomił skrypty w Pythonie 3.13 `[obserwacja]`. Skrypt `shot.py` wymaga dodatkowo pakietu `playwright` i przeglądarki Chrome.

Skrypt `prep2.py` zapisuje pliki modelu 3D w katalogu `koordynator/viz3d/`. Skopiuj te pliki do katalogu `model-3d/`.

## Kontrola

Claude uruchomił 2026-11-11 każdy skrypt z tabeli w układzie katalogów repozytorium, bez skryptu `shot.py` `[obserwacja]`. Skrypty odtworzyły 8 plików identycznych z plikami repozytorium: `parcels.json`, `zones.json`, `gz.npy`, `zone_areas.json`, raport R2, `data.js`, `zones.png` i `plan.png` `[obserwacja]`.

## Dane obce

| Dane | Dostawca | Pliki |
|---|---|---|
| Geometria działek | GUGiK, usługa ULDK | `dzialki_wkt.txt`, `R1/parcels_raw.txt`, `koordynator/parcels.json` |
| Wysokości terenu, siatka 20 m, 25 m i 50 m | GUGiK, numeryczny model terenu | `R1/elev1.txt`, `R1/elev2.txt`, `koordynator/nmt_pts.json`, `koordynator/gz.npy` |
| Model terenu i wysokość roślin, siatka 1 m, pomiar 2018-03-21 | GUGiK, usługi WCS | `koordynator/viz3d/dtm1m.npy`, `koordynator/viz3d/chm1m.npy` |
| Ortofotomapa z 2025-08-14 | GUGiK | `koordynator/orto_mosaic.png` |
| Symulacja off-grid i uzysk fotowoltaiki | Komisja Europejska, JRC, PVGIS 5.3 | liczby w pliku `koordynator/pvgis_shs.py` |
| Zasób słoneczny | Global Solar Atlas | liczby w pliku `R3/dane.py` |
| Normy klimatu 1991–2020 | IMGW-PIB | liczby w pliku `R3/dane.py` |

Dane obce zachowują warunki dostawcy. Plik `LICENCJE.md` w katalogu głównym opisuje licencje.

# Model 3D gospodarstwa

Model pokazuje teren, ortofotomapę, strefy, pola, drzewa, budynki i obiekty projektu. Suwak godziny ustawia Słońce dla 3 dni: 21 grudnia, 21 marca i 21 czerwca. Model rzuca cień terenu, drzew, budynków i obiektów projektu.

## Pliki

| Plik | Zawartość |
|---|---|
| `index.html` | Strona modelu: panel sterowania i style. |
| `app.js` | Kod sceny: teren, obiekty, Słońce, cień, etykiety. |
| `data.js` | Dane sceny: model terenu w siatce 2 m, drzewa, budynki, strefy, obiekty. |
| `orto.jpg` | Ortofotomapa z 2025-08-14 `[źródło: GUGiK]`. |
| `zones.png` | Obraz stref. |
| `plan.png` | Obraz pól i obiektów. |

Skrypt `obliczenia/koordynator/viz3d/prep2.py` tworzy pliki `data.js`, `orto.jpg`, `zones.png` i `plan.png`.

## Uruchomienie

Przeglądarka Chrome blokuje pliki `orto.jpg`, `zones.png` i `plan.png`, gdy otwierasz plik `index.html` z dysku `[obserwacja: Chrome, 2026-11-11]`. Model pokazuje wtedy teren bez ortofotomapy i bez stref.

Wykonaj każdy krok w tej kolejności:

1. Otwórz terminal w katalogu głównym repozytorium.
2. Uruchom serwer HTTP:

   ```sh
   python3 -m http.server 8000 --directory model-3d
   ```

3. Otwórz w przeglądarce adres `http://localhost:8000`.

Rozbicie:

- `python3 -m http.server`: uruchamia serwer HTTP z biblioteki standardowej Pythona.
- `8000`: numer portu serwera.
- `--directory model-3d`: katalog, który serwer udostępnia.

Strona pobiera z sieci bibliotekę three.js w wersji r128 i czcionkę Barlow. Model wymaga połączenia z internetem.

## Sterowanie

| Działanie | Mysz | Ekran dotykowy |
|---|---|---|
| Obrót | Przeciągnij lewym przyciskiem. | Przeciągnij 1 palcem. |
| Przesunięcie | Przeciągnij prawym przyciskiem. | Przeciągnij 2 palcami. |
| Powiększenie | Obróć kółko. | Rozsuń 2 palce. |
| Odczyt punktu | Kliknij teren. | Dotknij terenu. |

Odczyt punktu podaje współrzędne E i N w układzie PL-1992, wysokość nad poziomem morza i strefę.

## Ograniczenia danych

- Teren, drzewa i budynki pochodzą z pomiaru lotniczego z 2018-03-21 `[źródło: GUGiK, numeryczny model terenu i numeryczny model pokrycia terenu]`.
- Pomiar pochodzi z okresu bez liści i zaniża korony drzew liściastych `[założenie]`.
- Drzewostan strefy S8a jest schematem: wysokość drzew od 11 m do 16 m jest założeniem.
- Model nie pokazuje drzew, które projekt usuwa ze stref S2, S3, S4a i S5.

# -*- coding: utf-8 -*-
"""Dane wejsciowe wspolne dla skryptow agenta 3 (energia, cieplo, woda, magazyny, automatyka).

Punkt pobrania danych slonecznych: 53.7625 N, 20.4667 E (Global Solar Atlas). Gospodarstwo wg korekty zleceniodawcy:
okolice 53.7847 N, 20.4083 E (odleglosc 4.6 km) - roznica pomijalna dla zasobu slonecznego, danych nie pobierano ponownie.
Kazda stala ma zrodlo w komentarzu. "SZACUNEK" = zalozenie wlasne, nie dana zrodlowa.
"""
import math

LAT = 53.7625
LON = 20.4667
MIES = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
DNI = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # srednio 365.25 d

# --- Global Solar Atlas 2 (Solargis / World Bank), punkt 53.7625N 20.4667E, srednie wieloletnie ---
# zrodlo: https://api.globalsolaratlas.info/data/lta?loc=53.7625,20.4667 (pobrano 2026-11-11)
# PVOUT_csi: uzysk instalacji c-Si przy kacie optymalnym 38 st, azymut S [kWh/kWp/mies.]
GSA_PVOUT_38 = [32.71, 53.65, 96.47, 121.11, 139.93, 132.99, 130.76, 125.55, 99.87, 67.61, 30.42, 23.44]
GSA_GHI = [18.38, 35.65, 78.95, 121.29, 161.05, 164.43, 158.81, 136.90, 90.84, 50.34, 20.13, 13.02]  # kWh/m2/mies.
GSA_DIF = [12.43, 21.87, 42.16, 60.54, 74.96, 81.12, 82.71, 68.88, 47.43, 29.60, 14.40, 9.30]       # kWh/m2/mies.
GSA_GTI_38 = [35.22, 58.65, 109.37, 142.80, 169.29, 163.08, 160.92, 153.30, 117.99, 76.66, 33.45, 25.42]  # kWh/m2/mies.
GSA_TEMP = [-2.19, -1.19, 2.25, 7.94, 13.06, 16.88, 18.88, 18.50, 14.13, 8.69, 3.75, -0.38]  # st C
GSA_ROCZNIE = dict(PVOUT=1054.5, GHI=1049.8, DIF=545.4, GTI=1246.14, OPTA=38)

# --- Typowy rok meteorologiczny ISO, stacja 122720 Olsztyn, lata zrodlowe 1971-2000 (Ministerstwo, gov.pl) ---
# zrodlo: https://www.gov.pl/documents/33377/436740/wmo122720iso_stat.txt ; jednostka Wh/m2/mies.
TMY_ITH = [18759, 34446, 58795, 88034, 144266, 129507, 137774, 116430, 73914, 42676, 20953, 17818]
TMY_IDH = [2006, 13373, 19241, 27368, 60416, 41847, 45889, 32491, 21930, 11120, 4566, 261]
TMY_ISH = [16752, 21073, 39553, 60665, 83849, 87659, 91885, 83938, 51984, 31555, 16387, 17557]
TMY_S30 = [21953, 48726, 71642, 96555, 151926, 131930, 141161, 122540, 83240, 52452, 27215, 18288]
TMY_S45 = [23069, 53257, 74973, 97254, 148850, 128680, 137842, 121710, 84834, 55352, 29336, 18455]
TMY_S60 = [23754, 55595, 75891, 95459, 141344, 122746, 131473, 118306, 84190, 56629, 30575, 18562]
TMY_S90 = [23679, 53215, 70403, 85072, 116325, 105259, 112302, 105131, 76511, 54088, 30133, 18566]
TMY_T = [-3.6, -2.9, 2.5, 5.5, 10.9, 15.4, 17.7, 16.5, 12.8, 6.3, 1.9, -0.5]  # srednia roczna 6.9 st C

# --- Normy klimatyczne IMGW 1991-2020, Olsztyn (za: en.wikipedia.org/wiki/Olsztyn, zrodlo tabeli: IMGW) ---
IMGW_T = [-2.0, -1.1, 2.2, 7.9, 12.9, 16.1, 18.3, 17.8, 13.2, 8.0, 3.3, -0.4]   # st C, srednia roczna 8.0
IMGW_OPAD = [42.1, 33.1, 39.4, 37.5, 59.8, 70.1, 88.0, 63.8, 58.5, 57.7, 47.0, 45.4]  # mm, rok 642.4

# --- Pomiar rzeczywisty: instalacja 39.78 kWp, Mysleta (woj. warm.-maz.), dach 30 st, azymut SW ok. 25 st, rok 2017 ---
# zrodlo: Golisz i in. 2020, E3S Web of Conferences 154, 05003 ; [kWh/kWp/mies.]; rocznie 879 kWh/kWp
POMIAR_2017 = {"I": 18.10, "II": 26.14, "XI": 14.83, "XII": 11.31, "ROK": 879.0}

# --- stale fizyczne ---
CP_WODY = 4.19      # kJ/(kg K), woda 40-80 st C
RHO_WODY_65 = 0.980  # kg/dm3 przy ok. 65 st C
G = 9.81            # m/s2
CIEPLO_PAR = 0.68   # kWh/kg wody (LWF Merkblatt 12; = 2.44 MJ/kg)


def deklinacja(n):
    """Deklinacja Slonca [rad] dla dnia roku n (wzor Coopera)."""
    return math.radians(23.45) * math.sin(2 * math.pi * (284 + n) / 365)


DNI_KLEINA = [17, 47, 75, 105, 135, 162, 198, 228, 258, 288, 318, 344]  # reprezentatywny dzien miesiaca (Klein 1977)


def dlugosc_dnia(n, lat=LAT):
    """Dlugosc dnia astronomicznego [h] dla dnia roku n."""
    d = deklinacja(n)
    ws = math.acos(max(-1, min(1, -math.tan(math.radians(lat)) * math.tan(d))))
    return 24 * ws / math.pi

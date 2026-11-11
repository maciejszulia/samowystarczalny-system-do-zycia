# -*- coding: utf-8 -*-
"""01 - Zasob sloneczny i uzyski PV [kWh/kWp] dla Olsztyna-Gutkowa.

PVGIS API bylo niedostepne dla narzedzia (robots_disallowed) -> dane: Global Solar Atlas (Solargis) + TMY ministerialny.
Metoda przeliczenia na inne katy: model izotropowy Liu-Jordana w ujeciu miesiecznym Kleina (1977).
Wzory (kazdy w jednej linii):
  H_T = H_b*R_b + H_d*(1+cos(beta))/2 + H*rho*(1-cos(beta))/2
  R_b = [cos(fi-beta)*cos(delta)*sin(ws') + ws'*sin(fi-beta)*sin(delta)] / [cos(fi)*cos(delta)*sin(ws) + ws*sin(fi)*sin(delta)]
  ws = arccos(-tan(fi)*tan(delta)) ; ws' = min(ws, arccos(-tan(fi-beta)*tan(delta)))
  Y(beta) = Y(38 st) * H_T(beta)/H_T(38 st)   [zalozenie: ten sam wspolczynnik wydajnosci PR w danym miesiacu]
"""
import json
import math
from dane import *

RHO_GRUNT = 0.20  # albedo gruntu bez sniegu (SZACUNEK; snieg 0.5-0.8 zwieksza uzysk stromych paneli)


def Rb(beta_deg, n):
    fi = math.radians(LAT)
    b = math.radians(beta_deg)
    d = deklinacja(n)
    ws = math.acos(-math.tan(fi) * math.tan(d))
    wsp = min(ws, math.acos(max(-1.0, min(1.0, -math.tan(fi - b) * math.tan(d)))))
    licz = math.cos(fi - b) * math.cos(d) * math.sin(wsp) + wsp * math.sin(fi - b) * math.sin(d)
    mian = math.cos(fi) * math.cos(d) * math.sin(ws) + ws * math.sin(fi) * math.sin(d)
    return licz / mian


def HT(beta_deg, m, rho=RHO_GRUNT):
    """Miesieczne napromieniowanie plaszczyzny S o kacie beta [kWh/m2/mies.] z danych GSA (GHI, DIF)."""
    H, Hd = GSA_GHI[m], GSA_DIF[m]
    Hb = H - Hd
    b = math.radians(beta_deg)
    return Hb * Rb(beta_deg, DNI_KLEINA[m]) + Hd * (1 + math.cos(b)) / 2 + H * rho * (1 - math.cos(b)) / 2


def tmy_interp(beta):
    """Miesieczne sumy TMY [Wh/m2] dla kata beta przez interpolacje liniowa miedzy 30/45/60/90 st."""
    wezly = [(30, TMY_S30), (45, TMY_S45), (60, TMY_S60), (90, TMY_S90)]
    for (b0, t0), (b1, t1) in zip(wezly[:-1], wezly[1:]):
        if b0 <= beta <= b1:
            w = (beta - b0) / (b1 - b0)
            return [a + w * (c - a) for a, c in zip(t0, t1)]
    raise ValueError(beta)


print("=== 1. Walidacja modelu transpozycji: H_T(38 st) wlasne vs GTI_opta z GSA [kWh/m2/mies.] ===")
ht38 = [HT(38, m) for m in range(12)]
for m in range(12):
    print(f"{MIES[m]:>4}: model {ht38[m]:7.1f}  GSA {GSA_GTI_38[m]:7.1f}  roznica {100*(ht38[m]/GSA_GTI_38[m]-1):+6.1f}%")
print(f" ROK: model {sum(ht38):7.1f}  GSA {sum(GSA_GTI_38):7.1f}  roznica {100*(sum(ht38)/sum(GSA_GTI_38)-1):+6.1f}%")

print("\n=== 2. Uzysk P50 (srednia wieloletnia GSA) dla katow 35/38/50/65/90 st, azymut S [kWh/kWp/mies.] ===")
katy = [35, 38, 50, 65, 90]
Y50 = {}
for b in katy:
    Y50[b] = [GSA_PVOUT_38[m] * HT(b, m) / ht38[m] for m in range(12)]
print("mies. " + "".join(f"{b:>8} st" for b in katy))
for m in range(12):
    print(f"{MIES[m]:>5} " + "".join(f"{Y50[b][m]:11.1f}" for b in katy))
print("  ROK " + "".join(f"{sum(Y50[b]):11.0f}" for b in katy))
print(" XI-II" + "".join(f"{Y50[b][10]+Y50[b][11]+Y50[b][0]+Y50[b][1]:11.1f}" for b in katy))
assert abs(sum(GSA_PVOUT_38) - GSA_ROCZNIE["PVOUT"]) < 0.5, "suma miesieczna GSA != roczna"

print("\n=== 3. TMY ministerialny 1971-2000 (Olsztyn): sumy roczne [kWh/m2] i stosunki do 30 st ===")
for nazwa, t in [("poziom", TMY_ITH), ("S30", TMY_S30), ("S45", TMY_S45), ("S60", TMY_S60), ("S90", TMY_S90)]:
    print(f"{nazwa:>7}: {sum(t)/1000:7.1f} kWh/m2/rok")
print(f"GHI TMY/GSA = {sum(TMY_ITH)/1000/sum(GSA_GHI):.3f}  (TMY 1971-2000 zaniza promieniowanie wzgledem danych satelitarnych)")
print("Stosunek S60/S30 i S90/S30 wg TMY (miesiace zimowe, dominacja promieniowania rozproszonego):")
for m in [10, 11, 0, 1]:
    print(f"{MIES[m]:>4}: S60/S30 = {TMY_S60[m]/TMY_S30[m]:.3f}  S90/S30 = {TMY_S90[m]/TMY_S30[m]:.3f}  udzial bezposredniego w GHI = {TMY_IDH[m]/TMY_ITH[m]:.2f}")
print("Udzial promieniowania bezposredniego w GHI wg GSA (XI, XII, I, II): " + ", ".join(f"{1-GSA_DIF[m]/GSA_GHI[m]:.2f}" for m in [10, 11, 0, 1]))

print("\n=== 4. Porownanie z pomiarem 2017 (Mysleta, 30 st, SW): stosunek pomiar/GSA(38 st) ===")
for k, m in [("XI", 10), ("XII", 11), ("I", 0), ("II", 1)]:
    print(f"{k:>4}: pomiar {POMIAR_2017[k]:5.1f}  GSA {GSA_PVOUT_38[m]:5.1f}  stosunek {POMIAR_2017[k]/GSA_PVOUT_38[m]:.2f}")
print(f" ROK: pomiar {POMIAR_2017['ROK']:.0f}  GSA {sum(GSA_PVOUT_38):.0f}  stosunek {POMIAR_2017['ROK']/sum(GSA_PVOUT_38):.2f}")

# --- Scenariusz konserwatywny ("zly rok"): wspolczynniki miesieczne przyjete na podstawie pomiaru 2017 (SZACUNEK) ---
F_KONS = [0.50, 0.50, 0.75, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90, 0.75, 0.50, 0.50]
t35 = tmy_interp(35)
Ykons = {}
for b in [35, 65, 90]:
    tb = tmy_interp(b)
    # Y_kons(beta) = f_m * Y50(35 st) * [I_TMY(beta)/I_TMY(35 st)]  (w zlym roku dominuje promieniowanie rozproszone -> stosunki katow z TMY)
    Ykons[b] = [F_KONS[m] * Y50[35][m] * tb[m] / t35[m] for m in range(12)]
print("\n=== 5. Scenariusz konserwatywny [kWh/kWp/mies.] (f_m: XI-II 0.50; III,X 0.75; IV-IX 0.90) ===")
print("mies.     35 st     65 st     90 st")
for m in range(12):
    print(f"{MIES[m]:>5} {Ykons[35][m]:9.1f} {Ykons[65][m]:9.1f} {Ykons[90][m]:9.1f}")
print(f"  ROK {sum(Ykons[35]):9.0f} {sum(Ykons[65]):9.0f} {sum(Ykons[90]):9.0f}")
print(f"  XII dziennie [kWh/kWp/d]: 35 st {Ykons[35][11]/31:.2f}; 65 st {Ykons[65][11]/31:.2f}")

json.dump({"Y50": {str(k): v for k, v in Y50.items()}, "Ykons": {str(k): v for k, v in Ykons.items()}},
          open("wynik_pv.json", "w"), indent=1)
print("\nZapisano wynik_pv.json")

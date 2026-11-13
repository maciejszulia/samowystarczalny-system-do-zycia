#!/usr/bin/env python3
"""Poultry water line L1 (upper tank W1 -> livestock building B1).

Computes the route, the levels, the hydraulics, the trench, the cost and the
order of the deployment operations, and draws the 3 figures of
poultry-water-line.md.

Run from this directory:
    python poultry_water_line.py           # print the numbers, write the figures
    python poultry_water_line.py --check   # also fail if the document quotes other numbers

Inputs (already in the repository): the GUGiK terrain model on a 1 m grid,
the zone polygons and the orthophoto in ../obliczenia/koordynator/.
Requires: numpy, matplotlib, pillow.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "obliczenia" / "koordynator"

# --- terrain grid: PL-1992 origin and size, row 0 = north (same as viz3d/prep2.py) ---
E0, N0, GRID = 592200, 658880, 350
DTM = np.load(SRC / "viz3d" / "dtm1m.npy")


def ground(e, n):
    """Terrain height [m a.s.l.] of the 1 m cell that holds the point (e, n)."""
    row = int(np.clip(GRID - 1 - math.floor(n - N0), 0, GRID - 1))
    col = int(np.clip(math.floor(e - E0), 0, GRID - 1))
    return float(DTM[row, col])


ZONES = json.load(open(SRC / "zones.json", encoding="utf-8"))


def distance_to_ring(e, n, ring):
    """Shortest distance [m] from the point (e, n) to the outline of a polygon."""
    best = math.inf
    for (ax, ay), (bx, by) in zip(ring, ring[1:] + ring[:1]):
        dx, dy = bx - ax, by - ay
        t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((e - ax) * dx + (n - ay) * dy) / (dx * dx + dy * dy)))
        best = min(best, math.hypot(e - ax - t * dx, n - ay - t * dy))
    return best


# --- objects of the project plan (koordynator/figC.py, viz3d/prep2.py) ---
W1 = (592363.0, 659036.0)                              # upper tank
B1 = (592392.0, 659036.0)                              # livestock building
HOUSE = (592285.0, 658959.0)
RUBBLE = (592357.0, 659018.5)                           # rubble heap K
CHM = np.load(SRC / "viz3d" / "chm1m.npy")              # plant height, survey of 2018-03-21
TUNNEL = (592371.75, 659016.5, 592376.25, 659036.5)    # T1: e_min, n_min, e_max, n_max
COMPOST = (592366.0, 659041.0, 592376.0, 659045.5)
AVIARY = (592380.5, 659022.5, 592390.5, 659032.5)
PV_RACK = ((592325.0, 659036.0), (592357.0, 659036.0))

# --- route of pipe L1: one straight west-east run between T1 and the compost ---
P1 = (592365.0, 659038.75)                             # point 1, next to tank W1
P2 = (592392.0, 659038.75)                             # point 2, inside building B1

# --- frost and trench ---
FROST_DEPTH = 1.2          # m, R3 section C8.9 (PN-81/B-03020), assumption of the project
COVER_EXTRA = 0.40         # m above the frost depth, PN-97/B-10725 after Hotlos 2009
PIPE_OD, PIPE_ID = 0.032, 0.026   # m, PE100 SDR11 32 x 3.0 (same pipe as R3)
BEDDING = 0.10             # m of sand under the pipe, assumption
BED_WIDTH = 0.40           # m, bucket width, assumption
WALL_SLOPE_MAX = 0.5       # horizontal per vertical when damp sand sloughs, assumption
SAFE_SLOPE = 1.5           # horizontal per vertical, non-cohesive soil, PN-B-06050:1999
DIGGER_M3_H = (8.0, 15.0)  # m3 per hour, mini excavator in sand, assumption
BACKFILL_SHARE = 0.5       # backfilling takes half of the digging time, assumption
DIGGER_MIN_H = 4.0         # shortest hire, assumption
DIGGER_PLN_H = (140, 190)  # PLN per hour, mini excavator up to 2.5 t with operator, cenauslug.pl 2026

# --- levels in W1 and B1 ---
TANK_OUTLET = 0.05         # m, W1 outlet above the tank bottom, assumption
TANK_DEPTH = 1.5           # m of water in a full W1, assumption
BURIED_COVER = 1.2         # m of soil over a buried W1, R3 section C8.6
FLOOR = 0.20               # m, B1 floor above the terrain, assumption
NIPPLE = 0.40              # m, nipple line above the floor, assumption (adjustable)
COLUMN = 0.20              # m of water over the nipples, Impex/Teagasc 2024
INLET = 0.05               # m, float valve inlet above the W2 water level, assumption
W2_VOLUME = 60.0           # dm3, project section 8
HEAD_GATE = 0.50           # m, smallest measured head that passes operation OP1
CAN = 20.0                 # dm3, one water can carried by hand
HEATER_W_M, HEATED_EXTRA = 10.0, 0.95  # W per m of heating cable (R3) and m of pipe at tank W2, assumption
FLUSH_VOLUMES = 10         # pipe volumes of water for flushing, assumption
SHALLOW = (0.30, 0.40)     # m, width and depth of a hand-dug seasonal trench, assumption
DTM_ERROR = 0.15           # m, height error of one terrain cell, assumption

# --- hydraulics ---
G = 9.81
NU = 1.307e-6              # m2/s, water at 10 degC
ZETA = 10.0                # sum of local loss coefficients, assumption
METER_Q3, METER_DROP = 2.5, 6.42   # m3/h and m of water: a meter of class dP63 loses 0.63 bar at Q3
METER_R = 160              # Q3 / Q1 of the water meter
CD = 0.6                   # discharge coefficient of the float valve nozzle, assumption
Q_TARGET = 1.0             # dm3/min, W2 refills in 60 min
NIPPLES, NIPPLE_FLOW = 10, 0.060   # pieces and dm3/min each (R3: source S37)
PUMP_BAR = (3.0, 4.0)      # bar at the house, R3 section C8.3

# --- demand: R2 dane.py (dm3 per bird per day) and the full flock of project section 8 ---
WATER = {"hen": 0.25, "broiler": 0.35, "duck": 1.0, "goose": 1.5}
HENS, YOUNG, BROILERS, DUCKS, GEESE = 54 + 4, 10, 24, 16, 12
GOATS, GOAT_WATER = 2, (4.0, 10.0)   # R3 section C7, assumption
RESERVE_DAYS = 3           # project section 16

# --- cost of pipe L1, PLN gross 2026: (item, low, high) ---
COIL = 50                  # m, bought coil
PIPE_PLN_M = (5.00, 8.00)  # assumption around 1 offer: 6.29 PLN per m gross, onninen.pl, read 2026-11-13
OTHER_COST = [
    ("warning tape with a metal strip", 30, 80),
    ("casing pipes and insulation of 2 risers", 80, 200),
    ("compression fittings, 2 end caps, valves V1 and V2, strainer", 150, 400),
    ("pressure test pump, 2 days of hire", 100, 200),
    ("levelling instrument, 2 days of hire", 120, 240),
    ("sand for the pipe zone", 0, 300),
]
R3_TANK_AND_PIPE = (4000, 10000)   # R3 cost item "upper tank + PE pipe"
R3_B1_WATER = (300 + 300, 900 + 1100)   # R3 table E2: drinkers + frost protection

# --- operations: id -> (stage, people, hours low, hours high, needs) ---
OPS = {
    "OP1": ("E1", 2, 3, 4, []),
    "OP2": ("E1", 1, 2, 4, ["OP1"]),
    "OP3": ("E3", 1, 2, 3, ["OP1"]),
    "OP4": ("E3", 2, 2, 3, ["OP3"]),
    "OP5": ("E3", 2, None, None, ["OP2", "OP4"]),   # hours follow the excavator
    "OP6": ("E3", 1, 2, 3, ["OP5"]),
    "OP7": ("E6", 1, 6, 10, ["OP6"]),
    "OP8": ("E3", 1, 2, 4, ["OP6"]),
    "OP9": ("E6", 1, 3, 5, ["OP7", "OP8"]),
}
NO_RETURN = "OP5"
GATES = ("OP1", "OP4", "OP6", "OP9")


def profile():
    """Terrain and trench bed every 1 m from point 1 to point 2."""
    length = int(round(P2[0] - P1[0]))
    x = np.arange(length + 1, dtype=float)
    terrain = np.array([ground(P1[0] + d, P1[1]) for d in x])
    depth = math.ceil((FROST_DEPTH + COVER_EXTRA + PIPE_OD + BEDDING) / 0.05) * 0.05
    # the bed never rises towards B1, so no air pocket can form in the pipe
    bed = np.minimum.accumulate(terrain) - depth
    cover = terrain - bed - BEDDING - PIPE_OD
    return x, terrain, bed, cover, depth


def head_loss(q_dm3_min, length):
    """Friction + local + meter loss [m of water] at flow q in pipe L1."""
    q = q_dm3_min / 60000.0
    v = q / (math.pi * PIPE_ID ** 2 / 4)
    re = v * PIPE_ID / NU
    if re <= 0:
        return 0.0
    laminar, blasius = 64 / re, 0.316 / re ** 0.25
    lam = laminar if re < 2300 else blasius if re > 4000 else max(laminar, blasius)
    dynamic = v ** 2 / (2 * G)
    meter = METER_DROP * (q_dm3_min * 0.06 / METER_Q3) ** 2
    return lam * length / PIPE_ID * dynamic + ZETA * dynamic + meter


def nozzle_flow(head, nozzle_mm, length):
    """Flow [dm3/min] through the float valve nozzle under the given head [m]."""
    if head <= 0:
        return 0.0
    area = math.pi * (nozzle_mm / 1000) ** 2 / 4

    def spare(q):   # head left after the pipe and the nozzle
        return head - head_loss(q, length) - (q / 60000.0 / (CD * area)) ** 2 / (2 * G)

    low, high = 0.0, 200.0
    for _ in range(60):
        mid = (low + high) / 2
        low, high = (mid, high) if spare(mid) > 0 else (low, mid)
    return low


def order(ops):
    """Topological order of the operations; fails on a cycle or an unknown name."""
    done, left = [], dict(ops)
    while left:
        ready = [k for k, v in left.items() if all(n in done for n in v[4])]
        assert ready, f"cycle or unknown dependency among {sorted(left)}"
        done += sorted(ready)
        for k in ready:
            del left[k]
    return done


def compute():
    x, terrain, bed, cover, depth = profile()
    r = {"length": float(x[-1]), "depth": depth, "cover_min": float(cover.min()),
         "depth_max": float((terrain - bed).max()), "cover_need": FROST_DEPTH + COVER_EXTRA}
    r["z_w1"], r["z_b1"], r["z_p1"], r["z_p2"] = ground(*W1), ground(*B1), float(terrain[0]), float(terrain[-1])
    r["z_house"] = ground(*HOUSE)
    r["terrain_drop"] = r["z_w1"] - r["z_p2"]
    r["gap_tunnel"] = P1[1] - TUNNEL[3]
    r["gap_compost"] = COMPOST[1] - P1[1]
    r["gap_aviary"] = P1[1] - AVIARY[3]
    r["p1_to_w1"] = math.dist(P1, W1)
    r["slope_pct"] = (bed[0] - bed[-1]) / r["length"] * 100
    r["to_rubble"] = distance_to_ring(*RUBBLE, [list(P1), list(P2)])
    rows = slice(GRID - 1 - math.floor(P1[1] + 2.5 - N0), GRID - math.floor(P1[1] - 2.5 - N0))
    r["plants"] = float(CHM[rows, int(P1[0] - E0):int(P2[0] - E0) + 1].max())

    # levels
    r["inlet_rise"] = FLOOR + NIPPLE + COLUMN + INLET
    r["z_inlet"] = r["z_p2"] + r["inlet_rise"]
    r["z_outlet"] = r["z_w1"] + TANK_OUTLET
    r["head_min"] = r["z_outlet"] - r["z_inlet"]
    r["head_full"] = r["head_min"] + TANK_DEPTH - TANK_OUTLET
    r["head_worst"] = r["head_min"] - 2 * DTM_ERROR
    r["head_buried"] = r["z_w1"] - BURIED_COVER - r["z_inlet"]
    r["bar_min"] = 1000 * G * r["head_min"] / 1e5

    # pipe length: trench + riser at W1 + riser in B1 + 2 m for the bends
    riser_w1 = depth + TANK_OUTLET
    riser_b1 = depth + r["inlet_rise"]
    r["pipe_len"] = math.ceil(r["length"] + riser_w1 + riser_b1 + 2.0)
    r["pipe_volume"] = math.pi * PIPE_ID ** 2 / 4 * r["pipe_len"] * 1000
    r["route_max"] = math.floor(COIL - (riser_w1 + riser_b1 + 2.0))
    r["flush"] = FLUSH_VOLUMES * r["pipe_volume"]
    r["heater_w"] = HEATER_W_M * (FROST_DEPTH + r["inlet_rise"] + HEATED_EXTRA)
    r["to_wood"] = min(distance_to_ring(P1[0] + d, P1[1], ZONES["S8b Zadrzewiony stok 16/1"]) for d in x)

    # hydraulics in summer mode (gravity from an almost empty W1)
    r["loss_target"] = head_loss(Q_TARGET, r["pipe_len"])
    r["loss_tap"] = head_loss(5.0, r["pipe_len"])
    r["q_nipples"] = NIPPLES * NIPPLE_FLOW
    for mm in (3, 5, 6):
        q = nozzle_flow(r["head_min"], mm, r["pipe_len"])
        r[f"q_nozzle{mm}"], r[f"fill_nozzle{mm}"] = q, W2_VOLUME / q
    r["fill_gate5"] = W2_VOLUME / nozzle_flow(HEAD_GATE, 5, r["pipe_len"])
    r["q_meter_start"] = METER_Q3 * 1000 / METER_R            # dm3/h, Q1 of the meter
    # winter mode (pressure from the house): static loss up to the W2 inlet
    lift = r["z_inlet"] - r["z_house"]
    r["lift"] = lift
    r["bar_winter"] = tuple(p - 1000 * G * lift / 1e5 for p in PUMP_BAR)

    # demand and reserve
    poultry_summer = ((HENS + YOUNG) * WATER["hen"] + BROILERS / 2 * WATER["broiler"]
                      + DUCKS / 2 * WATER["duck"] + GEESE * WATER["goose"])
    poultry_winter = (HENS * WATER["hen"], (HENS + YOUNG) * WATER["hen"])
    goats = tuple(GOATS * g for g in GOAT_WATER)
    r["poultry_summer"], r["poultry_winter"], r["goats"] = poultry_summer, poultry_winter, goats
    r["summer"] = (poultry_summer + goats[0], poultry_summer + goats[1])
    r["winter"] = (poultry_winter[0] + goats[0], poultry_winter[1] + goats[1])
    r["q_mean_h"] = poultry_summer / 24
    r["w2_days_summer"] = (W2_VOLUME / r["summer"][1], W2_VOLUME / r["summer"][0])
    r["w2_days_winter"] = (W2_VOLUME / r["winter"][1], W2_VOLUME / r["winter"][0])
    r["w2_need"] = RESERVE_DAYS * r["winter"][1]
    r["ducks_geese"] = DUCKS / 2 * WATER["duck"] + GEESE * WATER["goose"]
    r["cans_summer"] = tuple(math.ceil(v / CAN) for v in r["summer"])
    r["cans_winter"] = tuple(math.ceil(v / CAN) for v in r["winter"])
    r["carry_lift"] = r["z_p2"] - r["z_house"]

    # trench
    depths = terrain - bed
    mean_depth = float(depths.mean())
    r["mean_depth"] = mean_depth
    r["vol_min"] = BED_WIDTH * mean_depth * r["length"]
    r["vol_max"] = (BED_WIDTH + WALL_SLOPE_MAX * mean_depth) * mean_depth * r["length"]
    r["top_width_max"] = BED_WIDTH + 2 * WALL_SLOPE_MAX * mean_depth
    r["top_width_safe"] = BED_WIDTH + 2 * SAFE_SLOPE * mean_depth
    r["vol_safe"] = (BED_WIDTH + SAFE_SLOPE * mean_depth) * mean_depth * r["length"]
    hours = ((1 + BACKFILL_SHARE) * r["vol_min"] / DIGGER_M3_H[1],
             (1 + BACKFILL_SHARE) * r["vol_max"] / DIGGER_M3_H[0])
    r["digger_h"] = (max(DIGGER_MIN_H, math.ceil(hours[0])), max(DIGGER_MIN_H, math.ceil(hours[1])))

    # cost
    r["digger_cost"] = (r["digger_h"][0] * DIGGER_PLN_H[0], r["digger_h"][1] * DIGGER_PLN_H[1])
    r["pipe_cost"] = (round(COIL * PIPE_PLN_M[0]), round(COIL * PIPE_PLN_M[1]))
    r["other_cost"] = (sum(c[1] for c in OTHER_COST), sum(c[2] for c in OTHER_COST))
    r["cost"] = tuple(r["digger_cost"][i] + r["pipe_cost"][i] + r["other_cost"][i] for i in (0, 1))
    r["market_cost"] = (65 * r["length"], 94 * r["length"])     # PLN, trench priced per metre
    r["shallow_vol"] = SHALLOW[0] * SHALLOW[1] * r["length"]
    r["shallow_cost"] = tuple(r["pipe_cost"][i] + OTHER_COST[0][i + 1] + OTHER_COST[2][i + 1] for i in (0, 1))
    r["undo_cost"] = DIGGER_MIN_H * DIGGER_PLN_H[0]

    # work
    work = [0.0, 0.0]
    for name, (_, people, low, high, _) in OPS.items():
        low, high = (r["digger_h"] if low is None else (low, high))
        work[0] += people * low
        work[1] += people * high
    r["work"] = tuple(work)
    r["order"] = order(OPS)
    return r, (x, terrain, bed, cover)


def self_check(r, prof):
    x, terrain, bed, cover = prof
    assert r["length"] == 27.0
    assert abs(r["z_w1"] - 118.19) < 0.01 and abs(r["z_house"] - 107.35) < 0.01   # numbers of the project
    assert np.all(np.diff(bed) <= 1e-9), "the trench bed rises towards B1"
    assert r["cover_min"] >= r["cover_need"], "the cover is smaller than frost depth + 0.40 m"
    assert min(r["gap_tunnel"], r["gap_compost"]) >= 2.0, "the route is too close to T1 or to the compost"
    assert r["head_buried"] < 0 < r["head_worst"] < r["head_min"] < r["head_full"]
    assert head_loss(0, 30) == 0 and head_loss(1, 30) < head_loss(5, 30) < head_loss(5, 60)
    assert r["q_nozzle3"] < r["q_nozzle5"] < r["q_nozzle6"]
    for mm in (3, 5, 6):   # the solver result reproduces the head it was given
        q = r[f"q_nozzle{mm}"] / 60000.0
        area = math.pi * (mm / 1000) ** 2 / 4
        used = head_loss(r[f"q_nozzle{mm}"], r["pipe_len"]) + (q / (CD * area)) ** 2 / (2 * G)
        assert abs(used - r["head_min"]) < 1e-6
    assert abs(r["poultry_summer"] - 47.2) < 0.05          # project section 8: "co najwyzej 47 dm3"
    assert r["w2_days_winter"][0] < RESERVE_DAYS, "W2 already holds the 3-day reserve"
    assert r["vol_min"] < r["vol_max"] < r["vol_safe"]
    assert r["order"][0] == "OP1" and r["order"][-1] == "OP9"
    assert all(r["order"].index(g) < r["order"].index(NO_RETURN) for g in ("OP1", "OP2", "OP4"))
    assert r["pipe_len"] <= COIL and r["length"] <= r["route_max"]
    assert r["fill_gate5"] < 60 < 2 * r["fill_nozzle3"], "the OP1 gate no longer guarantees a 60 min refill"
    assert distance_to_ring(0.5, 0.5, [[0, 0], [1, 0], [1, 1], [0, 1]]) == 0.5
    assert r["shallow_cost"][1] < r["cost"][0], "the seasonal trench is no longer the cheaper way"


def pl(value, digits=2):
    """Number in Polish notation: decimal comma, space as the thousands separator."""
    return f"{value:,.{digits}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def quoted(r):
    """Numbers that the document must quote, already formatted."""
    return {
        "route length": f"{pl(r['length'], 0)} m",
        "terrain at W1": f"{pl(r['z_w1'])} m n.p.m.",
        "terrain at point 2": f"{pl(r['z_p2'])} m n.p.m.",
        "terrain drop": f"{pl(r['terrain_drop'])} m",
        "inlet level": f"{pl(r['z_inlet'])} m n.p.m.",
        "outlet level": f"{pl(r['z_outlet'])} m n.p.m.",
        "head, empty W1": f"{pl(r['head_min'])} m",
        "head, full W1": f"{pl(r['head_full'])} m",
        "head, worst case": f"{pl(r['head_worst'])} m",
        "head, buried W1": f"{pl(r['head_buried'])} m",
        "pressure, empty W1": f"{pl(r['bar_min'], 3)} bar",
        "trench depth": f"{pl(r['depth'])} m",
        "largest depth": f"{pl(r['depth_max'])} m",
        "smallest cover": f"{pl(r['cover_min'])} m",
        "bed slope": f"{pl(r['slope_pct'], 1)}%",
        "gap to T1": f"{pl(r['gap_tunnel'])} m",
        "pipe length": f"{pl(r['pipe_len'], 0)} m",
        "pipe volume": f"{pl(r['pipe_volume'], 1)} dm³",
        "loss at 1 dm3/min": f"{pl(r['loss_target'], 3)} m",
        "loss at 5 dm3/min": f"{pl(r['loss_tap'], 2)} m",
        "fill time, 3 mm": f"{pl(r['fill_nozzle3'], 0)} min",
        "fill time, 5 mm": f"{pl(r['fill_nozzle5'], 0)} min",
        "fill time, 6 mm": f"{pl(r['fill_nozzle6'], 0)} min",
        "meter start": f"{pl(r['q_meter_start'], 1)} dm³/h",
        "mean flow": f"{pl(r['q_mean_h'], 1)} dm³/h",
        "lift from the house": f"{pl(r['lift'])} m",
        "winter pressure": f"od {pl(r['bar_winter'][0], 1)} bar do {pl(r['bar_winter'][1], 1)} bar",
        "summer demand": f"od {pl(r['summer'][0], 1)} dm³ do {pl(r['summer'][1], 1)} dm³",
        "winter demand": f"od {pl(r['winter'][0], 1)} dm³ do {pl(r['winter'][1], 1)} dm³",
        "W2 days, winter": f"od {pl(r['w2_days_winter'][0], 1)} doby do {pl(r['w2_days_winter'][1], 1)} doby",
        "W2 days, summer": f"od {pl(r['w2_days_summer'][0], 1)} doby do {pl(r['w2_days_summer'][1], 1)} doby",
        "W2 needed": f"{pl(r['w2_need'], 0)} dm³",
        "trench volume": f"od {pl(r['vol_min'], 0)} m³ do {pl(r['vol_max'], 0)} m³",
        "safe slope width": f"{pl(r['top_width_safe'], 1)} m",
        "safe slope volume": f"{pl(r['vol_safe'], 0)} m³",
        "excavator hours": f"od {pl(r['digger_h'][0], 0)} h do {pl(r['digger_h'][1], 0)} h",
        "excavator cost": f"od {pl(r['digger_cost'][0], 0)} PLN do {pl(r['digger_cost'][1], 0)} PLN",
        "pipe cost": f"od {pl(r['pipe_cost'][0], 0)} PLN do {pl(r['pipe_cost'][1], 0)} PLN",
        "other cost": f"od {pl(r['other_cost'][0], 0)} PLN do {pl(r['other_cost'][1], 0)} PLN",
        "total cost": f"od {pl(r['cost'][0], 0)} PLN do {pl(r['cost'][1], 0)} PLN",
        "market trench price": f"od {pl(r['market_cost'][0], 0)} PLN do {pl(r['market_cost'][1], 0)} PLN",
        "own work": f"od {pl(r['work'][0], 0)} h do {pl(r['work'][1], 0)} h",
        "longest route": f"{pl(r['route_max'], 0)} m",
        "point 1 to W1": f"{pl(r['p1_to_w1'], 1)} m",
        "distance to the rubble": f"{pl(r['to_rubble'], 1)} m",
        "plants in 2018": f"{pl(r['plants'])} m",
        "fill time at the gate": f"{pl(r['fill_gate5'], 0)} min",
        "flush volume": f"{pl(r['flush'], 0)} dm³",
        "heating cable": f"{pl(r['heater_w'], 0)} W",
        "distance to the wood": f"{pl(r['to_wood'], 1)} m",
        "ducks and geese": f"{pl(r['ducks_geese'], 1)} dm³",
        "poultry, summer": f"{pl(r['poultry_summer'], 1)} dm³",
        "cans, summer": f"od {r['cans_summer'][0]} do {r['cans_summer'][1]} kanistrów",
        "cans, winter": f"{r['cans_winter'][1]} kanistry",
        "carry lift": f"{pl(r['carry_lift'], 1)} m",
        "seasonal trench": f"{pl(r['shallow_vol'], 1)} m³",
        "seasonal cost": f"od {pl(r['shallow_cost'][0], 0)} PLN do {pl(r['shallow_cost'][1], 0)} PLN",
        "undo cost": f"{pl(r['undo_cost'], 0)} PLN",
    }


# ---------------------------------------------------------------- figures
BLUE, RED, EARTH, GREY = "#1f5fa8", "#c0392b", "#8a6d4b", "#555555"
GUGIK = "Źródło danych: GUGiK, geoportal.gov.pl (model terenu w siatce 1 m, pomiar 2018-03-21; ortofotomapa 2025-08-14)."


def titles(fig, ax, finding, drawn, source):
    """Title = the finding, subtitle = what is drawn, footer = the data source."""
    ax.set_title(finding, fontsize=11.5, loc="left", pad=22)
    ax.text(0, 1.012, drawn, transform=ax.transAxes, fontsize=8.8, color=GREY, va="bottom")
    fig.text(0.012, 0.012, source, fontsize=7.8, color=GREY, va="bottom")


def figures(r, prof):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle, Polygon
    from PIL import Image

    x, terrain, bed, cover = prof

    # ---- figure 1: route on the plan
    e_min, e_max, n_min, n_max = 592343, 592411, 659013, 659057
    fig, ax = plt.subplots(figsize=(10.2, 7.0), dpi=140)
    ax.imshow(Image.open(SRC / "orto_mosaic.png"), extent=[E0, E0 + GRID, N0, N0 + GRID], alpha=0.45,
              interpolation="bilinear")
    cells_e = E0 + np.arange(GRID) + 0.5
    cells_n = N0 + GRID - 1 - np.arange(GRID) + 0.5
    contours = ax.contour(cells_e, cells_n, DTM, levels=np.arange(114, 121, 0.5), colors="black",
                          linewidths=0.5, alpha=0.55)
    ax.clabel(contours, fmt=lambda v: f"{v:.1f}".replace(".", ","), fontsize=7, zorder=2)
    ax.text(592357.0, 659023.4, "gruzowisko K", fontsize=8.5, ha="center")
    for key, colour in (("S2 Warzywnik z tunelem", "#2e7d32"), ("S3 Kurnik z wolierą", "#d35400")):
        ax.add_patch(Polygon(ZONES[key], closed=True, fill=False, ec=colour, lw=1.6, ls="--"))
    for (a, b, c, d), name, colour in ((TUNNEL, "tunel T1", "#ffffff"), (COMPOST, "kompost", "#6d4c2f"),
                                       (AVIARY, "woliera", "#f5cba7")):
        ax.add_patch(Rectangle((a, b), c - a, d - b, fc=colour, ec="black", lw=1.0, zorder=3))
        ax.text((a + c) / 2, (b + d) / 2, name, ha="center", va="center", fontsize=8.5, zorder=4,
                rotation=90 if name == "tunel T1" else 0,
                color="white" if name == "kompost" else "black")
    ax.plot(*zip(*PV_RACK), color="navy", lw=5, solid_capstyle="butt")
    ax.text(PV_RACK[1][0] - 6, PV_RACK[1][1] - 2.2, "stelaż PV", fontsize=8.5, color="navy", ha="center")
    ax.add_patch(Circle(W1, 1.0, fc="#aed6f1", ec=BLUE, lw=1.5))
    ax.text(W1[0], W1[1] - 2.6, f"zbiornik W1\n{pl(r['z_w1'])} m n.p.m.", ha="center", va="top", fontsize=8.5)
    ax.add_patch(Rectangle((B1[0] - 2, B1[1] - 3), 4, 6, fc="#fdebd0", ec="black", lw=1.2))
    ax.text(B1[0] + 2.6, B1[1] - 0.5, f"budynek B1\n(obrys schematyczny)\n{pl(r['z_p2'])} m n.p.m.\nw punkcie 2",
            ha="left", va="center", fontsize=8.5)
    ax.plot([P1[0], P2[0]], [P1[1], P2[1]], color=BLUE, lw=3.5, solid_capstyle="butt")
    for point, label, dx in ((P1, "1", -1.6), (P2, "2", 1.6)):
        ax.plot(*point, "o", ms=8, mfc="white", mec=BLUE, mew=2)
        ax.text(point[0] + dx, point[1] + 1.5, label, ha="center", fontsize=10, color=BLUE, weight="bold")
    ax.text((P1[0] + P2[0]) / 2 + 5, P1[1] + 1.0, f"przewód L1: {pl(r['length'], 0)} m", color=BLUE, fontsize=9.5,
            ha="center", weight="bold")
    for n_from, n_to, e in ((TUNNEL[3], P1[1], 592374.0), (P1[1], COMPOST[1], 592371.0)):
        ax.annotate("", xy=(e, n_to), xytext=(e, n_from), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.2))
    ax.text(592378.6, 659035.4, f"odstęp {pl(r['gap_tunnel'])} m\nod tunelu T1\ni od kompostu",
            color=RED, fontsize=8.5, ha="left", va="center")
    ax.plot([e_min + 3, e_min + 13], [n_min + 2.5, n_min + 2.5], color="black", lw=4, solid_capstyle="butt")
    ax.text(e_min + 8, n_min + 3.6, "10 m", ha="center", fontsize=9)
    ax.annotate("N", xy=(e_max - 3, n_max - 2), xytext=(e_max - 3, n_max - 8), ha="center", fontsize=11,
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.8))
    ax.text(e_min + 3, n_max - 2.5, "linia przerywana zielona: strefa S2\nlinia przerywana pomarańczowa: strefa S3\n"
            "warstwice co 0,5 m", fontsize=8, va="top", bbox=dict(fc="white", ec="none", alpha=0.8))
    ax.set_xlim(e_min, e_max); ax.set_ylim(n_min, n_max); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    titles(fig, ax, f"Przewód L1 ma {pl(r['length'], 0)} m i mija tunel T1 oraz kompost w odstępie {pl(r['gap_tunnel'])} m",
           "Plan trasy od punktu 1 do punktu 2. Odstęp liczy się od osi przewodu L1.", GUGIK)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(HERE / "fig1-route.jpg", pil_kwargs={"quality": 88}); plt.close(fig)   # photo background: JPEG is 6 times smaller

    # ---- figure 2: long section with the levels
    fig, ax = plt.subplots(figsize=(10.2, 5.6), dpi=140)
    xs = np.concatenate(([-6.0, -1.4], x, [x[-1] + 6.0]))      # flat ground under tank W1
    ts = np.concatenate(([r["z_w1"], r["z_w1"]], terrain, [terrain[-1]]))
    ax.fill_between(xs, ts, 113.6, color=EARTH, alpha=0.25, lw=0)
    ax.plot(xs, ts, color=EARTH, lw=2)
    ax.plot(xs, ts - FROST_DEPTH, color=GREY, lw=1.1, ls=":")
    ax.text(19.0, float(terrain[8:20].max()) - FROST_DEPTH + 0.08, f"granica przemarzania: {pl(FROST_DEPTH, 1)} m pod terenem",
            fontsize=8.5, color=GREY, ha="right")
    pipe = bed + BEDDING + PIPE_OD / 2
    pipe_x = np.concatenate(([0.0, 0.0], x[1:-1], [x[-1], x[-1]]))
    pipe_z = np.concatenate(([r["z_outlet"], pipe[0]], pipe[1:-1], [pipe[-1], r["z_inlet"]]))
    ax.plot(pipe_x, pipe_z, color=BLUE, lw=2.6, solid_joinstyle="miter")
    ax.plot([-1.4, 0.0], [r["z_outlet"]] * 2, color=BLUE, lw=2.6)
    ax.add_patch(Rectangle((-3.4, r["z_w1"]), 2.0, TANK_DEPTH, fc="#aed6f1", ec=BLUE, lw=1.5))
    ax.text(-2.4, r["z_w1"] + TANK_DEPTH + 0.12, "zbiornik W1", ha="center", fontsize=9)
    ax.add_patch(Rectangle((x[-1] - 1.0, r["z_p2"] + FLOOR), 5.0, 0.06, fc="black", ec="none"))
    ax.add_patch(Rectangle((x[-1] + 0.0, r["z_inlet"] - INLET - 0.35), 0.9, 0.40, fc="#aed6f1", ec=BLUE, lw=1.3))
    ax.text(x[-1] + 1.3, r["z_inlet"] - 0.2, "zbiornik W2", ha="left", va="center", fontsize=9)
    ax.text(x[-1] + 1.3, r["z_p2"] + FLOOR + 0.12, "posadzka B1", ha="left", fontsize=8.5)
    for level, text, ha, xt in ((r["z_outlet"], f"króciec zbiornika W1: {pl(r['z_outlet'])} m n.p.m.", "left", 1.0),
                                (r["z_inlet"], f"wlot zbiornika W2: {pl(r['z_inlet'])} m n.p.m.", "right", x[-1] - 1.0)):
        ax.plot([-6, x[-1] + 6], [level, level], color=RED, lw=0.9, ls="--")
        ax.text(xt, level + 0.07, text, color=RED, fontsize=8.5, ha=ha)
    ax.annotate("", xy=(14.0, r["z_inlet"]), xytext=(14.0, r["z_outlet"]),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
    ax.text(14.5, (r["z_inlet"] + r["z_outlet"]) / 2, f"{pl(r['head_min'])} m", color=RED, fontsize=11, va="center",
            weight="bold")
    ax.text(1.0, float(pipe[:21].min()) - 0.24, f"przewód L1: przykrycie co najmniej {pl(r['cover_min'])} m, spadek {pl(r['slope_pct'], 1)}%",
            color=BLUE, fontsize=8.5, ha="left")
    ax.text(0.2, 114.0, "punkt 1", fontsize=9, color=BLUE); ax.text(x[-1] - 0.2, 114.0, "punkt 2", fontsize=9, color=BLUE, ha="right")
    ax.set_xlim(-6, x[-1] + 6); ax.set_ylim(113.6, 120.4)
    ax.set_xlabel("odległość od punktu 1 [m]"); ax.set_ylabel("wysokość [m n.p.m.]")
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}")
    ax.grid(axis="y", color="black", alpha=0.12)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    titles(fig, ax, f"Króciec zbiornika W1 leży tylko {pl(r['head_min'])} m nad wlotem zbiornika W2",
           "Przekrój wzdłuż przewodu L1. Zbiornik W1 stoi na terenie. Skala pionowa jest powiększona.", GUGIK)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(HERE / "fig2-profile.png"); plt.close(fig)

    # ---- figure 3: operations, lanes = project stages, right-angle edges only
    lanes = {"E1": (2, "Etap E1\nIV kwartał 2026 r."), "E3": (1, "Etap E3\nI kwartał 2027 r."),
             "E6": (0, "Etap E6\nod II kwartału 2027 r.")}
    names = {"OP1": "OP1\npomiar\ni decyzje", "OP2": "OP2\nsieci\ni formalności", "OP3": "OP3\nzakup\ni dostawa",
             "OP4": "OP4\npróba na\npowierzchni", "OP5": "OP5\nwykop\ni zasypka", "OP6": "OP6\npróba po\nzasypaniu",
             "OP7": "OP7\nwęzeł\nw B1", "OP8": "OP8\nwłączenie\nprzy W1", "OP9": "OP9\nodbiór\nkońcowy"}
    column = {"OP1": 0, "OP2": 1, "OP3": 1, "OP4": 2, "OP5": 3, "OP6": 4, "OP8": 5, "OP7": 5, "OP9": 6}
    box_w, box_h, step_x, step_y = 1.5, 1.05, 2.2, 1.9
    centre = {k: (column[k] * step_x, lanes[OPS[k][0]][0] * step_y) for k in OPS}
    fig, ax = plt.subplots(figsize=(11.4, 5.9), dpi=140)
    for stage, (row, label) in lanes.items():
        ax.add_patch(Rectangle((-2.9, row * step_y - 0.86), 17.4, 1.72, fc="#f4f4f4" if row % 2 else "#e9eef5", ec="none"))
        ax.text(-2.75, row * step_y, label, va="center", fontsize=9.5)
    for k, (cx, cy) in centre.items():
        colour = "#f5b7b1" if k == NO_RETURN else "#d6eaf8" if k in GATES else "white"
        ax.add_patch(Rectangle((cx - box_w / 2, cy - box_h / 2), box_w, box_h, fc=colour,
                               ec=RED if k == NO_RETURN else "black", lw=2.2 if k == NO_RETURN else 1.2, zorder=3))
        ax.text(cx, cy, names[k], ha="center", va="center", fontsize=8.8, zorder=4)
    for k, spec in OPS.items():
        for need in spec[4]:
            (x0, y0), (x1, y1) = centre[need], centre[k]
            start, end = (x0 + box_w / 2, y0), (x1 - box_w / 2, y1)
            bend = end[0] - 0.32
            ax.plot([start[0], bend, bend], [start[1], start[1], end[1]], color="black", lw=1.2, zorder=2,
                    solid_joinstyle="miter")
            ax.annotate("", xy=end, xytext=(bend, end[1]), arrowprops=dict(arrowstyle="-|>", color="black", lw=1.2), zorder=2)
    legend_y = -1.45
    for left, colour, edge, text in ((-2.75, "#d6eaf8", "black", "bramka: pomiar decyduje o dalszej pracy"),
                                     (3.2, "#f5b7b1", RED, "punkt bez powrotu: cofnięcie wymaga nowego wykopu"),
                                     (10.9, "white", "black", "operacja bez bramki")):
        ax.add_patch(Rectangle((left, legend_y - 0.16), 0.5, 0.32, fc=colour, ec=edge, lw=1.2))
        ax.text(left + 0.65, legend_y, text, va="center", fontsize=8.8)
    ax.set_xlim(-3.0, 14.6); ax.set_ylim(-1.95, 2 * step_y + 0.95); ax.axis("off")
    titles(fig, ax, "3 bramki stoją przed operacją OP5, bo po zasypaniu rowu poprawka wymaga nowego wykopu",
           "Kolejność 9 operacji w etapach projektu. Strzałka z A do B: operacja B wymaga wyniku operacji A.",
           "Źródło: tabela operacji w sekcji 6. Operacja OP7 czeka na budynek B1. Operacja OP8 czeka na zbiornik W1.")
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(HERE / "fig3-operations.png"); plt.close(fig)


def main():
    r, prof = compute()
    self_check(r, prof)
    numbers = quoted(r)
    for name, text in numbers.items():
        print(f"{name:22s} {text}")
    print(f"{'order':22s} {' '.join(r['order'])}")
    print("self-check passed")
    if "--check" in sys.argv:
        document = (HERE / "poultry-water-line.md").read_text(encoding="utf-8")
        missing = [f"{name}: {text}" for name, text in numbers.items() if text.lower() not in document.lower()]
        if missing:
            sys.exit("the document does not quote:\n  " + "\n  ".join(missing))
        print(f"document quotes all {len(numbers)} numbers")
    else:
        figures(r, prof)
        print("figures written")


if __name__ == "__main__":
    main()

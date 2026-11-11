import sys, math
from shapely.geometry import Polygon, Point
c = Point(592284.78, 658959.28)
rows = []
for line in open('parcels_raw.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    pid, ext, geom = [s.strip() for s in line.split(' # ')]
    rings = []
    for r in geom.split('|R|'):
        pts = [tuple(map(float,p.split())) for p in r.split(';') if p.strip()]
        rings.append(pts)
    poly = Polygon(rings[0], rings[1:])
    ex = list(map(float, ext.split(',')))
    b = poly.bounds
    ok = all(abs(b[i]-ex[i])<0.02 for i in range(4))
    rows.append((pid, poly.area, poly.is_valid, ok, poly.distance(c), len(rings[0])-1, poly))
for pid, a, v, ok, d, nv, poly in sorted(rows, key=lambda r:r[4]):
    print(f"{pid:24s} area={a:10.1f} m2 valid={v} bbox_ok={ok} dist_to_addr={d:6.1f} m  nvert={nv}")

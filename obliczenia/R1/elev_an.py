import numpy as np, math
from shapely.geometry import Polygon, Point
pts={}
for f in ['elev1.txt','elev2.txt']:
    for line in open(''+f):
        for tok in line.strip().split(','):
            if not tok.strip(): continue
            n,e,h=tok.split(); pts[(int(e),int(n))]=float(h)
polys={}
for line in open('parcels_raw.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    pid, ext, geom = [s.strip() for s in line.split(' # ')]
    rings=[[tuple(map(float,p.split())) for p in r.split(';') if p.strip()] for r in geom.split('|R|')]
    polys[pid]=Polygon(rings[0], rings[1:])
print(len(pts),'elevation points')
for pid,poly in polys.items():
    hs=[h for (e,n),h in pts.items() if poly.contains(Point(e,n))]
    if hs: print(f"{pid:24s} n={len(hs):3d} min={min(hs):6.1f} max={max(hs):6.1f} mean={np.mean(hs):6.1f}")
# slope/aspect on 25 m grid for core
def h(e,n): return pts.get((e,n))
print('\nSlope/aspect at 25 m grid nodes inside 16/1 and 24/1 (central differences, 50 m base):')
for pid in ['286201_1.0144.16/1','286201_1.0144.24/1','286201_1.0143.22/1','286201_1.0143.22/2','286201_1.0144.14']:
    poly=polys[pid]; res=[]
    for (e,n),hh in pts.items():
        if not poly.contains(Point(e,n)): continue
        a,b,c,d=h(e+25,n),h(e-25,n),h(e,n+25),h(e,n-25)
        if None in (a,b,c,d): continue
        dzdx=(a-b)/50; dzdy=(c-d)/50
        slope=math.hypot(dzdx,dzdy)
        asp=(math.degrees(math.atan2(-dzdx,-dzdy))+360)%360  # downslope direction azimuth
        res.append((e,n,hh,slope*100,math.degrees(math.atan(slope)),asp))
    print(pid)
    for r in sorted(res,key=lambda r:(-r[1],r[0])):
        print(f"   E{r[0]} N{r[1]} h={r[2]:6.1f} slope={r[3]:5.1f}% ({r[4]:4.1f} deg) downslope azimuth={r[5]:5.0f}")
    if res:
        print(f"   mean slope {np.mean([r[3] for r in res]):.1f}%  max {max(r[3] for r in res):.1f}%")

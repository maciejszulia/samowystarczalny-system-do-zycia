import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
c = Point(592284.78, 658959.28)
fig, ax = plt.subplots(figsize=(11,11))
out=[]
for line in open('parcels_raw.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    pid, ext, geom = [s.strip() for s in line.split(' # ')]
    rings=[[tuple(map(float,p.split())) for p in r.split(';') if p.strip()] for r in geom.split('|R|')]
    poly=Polygon(rings[0], rings[1:])
    x,y=poly.exterior.xy
    ax.plot(x,y,lw=0.8)
    for r in poly.interiors:
        xi,yi=r.xy; ax.plot(xi,yi,lw=0.6,ls=':')
    rp=poly.representative_point()
    lab=pid.split('.')[1].lstrip('0')+'-'+pid.split('.')[2]
    ax.text(rp.x,rp.y,lab,fontsize=7,ha='center')
    out.append((pid, round(rp.x), round(rp.y)))
circ=c.buffer(500); x,y=circ.exterior.xy; ax.plot(x,y,'k--',lw=0.8)
ax.plot(c.x,c.y,'r*',ms=12)
ax.set_xlim(591700,592900); ax.set_ylim(658350,659650); ax.set_aspect('equal'); ax.grid(True,lw=0.3)
fig.savefig('parcels.png',dpi=90,bbox_inches='tight')
for o in out: print(o)

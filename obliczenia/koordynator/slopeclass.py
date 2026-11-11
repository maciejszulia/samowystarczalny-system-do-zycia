import json, numpy as np
from shapely.geometry import Polygon, Point
Z=json.load(open('zones.json'))
gz=np.load('gz.npy'); E0,E1,N0,N1=592200,592550,658880,659230
xs=np.arange(E0,E1+1,2.5); ys=np.arange(N0,N1+1,2.5)
dzdy,dzdx=np.gradient(gz,2.5,2.5); slope=np.hypot(dzdx,dzdy)*100
cell=2.5*2.5
for name in ['S2 Warzywnik z tunelem','S3 Kurnik z wolierą','S4 Pole A','S5 Pole B','S6 Sad z pasieką','S7 Pastwisko i łąka','S9 Pole kempingowe','S1 Siedlisko']:
    pg=Polygon(Z[name]) if not isinstance(Z[name][0][0],list) else None
    if pg is None: 
        from shapely.ops import unary_union
        pg=unary_union([Polygon(c) for c in Z[name]])
    c={'<6':0,'6-10':0,'10-15':0,'15-20':0,'>20':0}
    for j,y in enumerate(ys):
        for i,x in enumerate(xs):
            if pg.contains(Point(x,y)):
                s=slope[j,i]
                k='<6' if s<6 else '6-10' if s<10 else '10-15' if s<15 else '15-20' if s<20 else '>20'
                c[k]+=cell
    print(f"{name:26s} area {pg.area:6.0f}  "+"  ".join(f"{k}%: {v:5.0f}" for k,v in c.items()))

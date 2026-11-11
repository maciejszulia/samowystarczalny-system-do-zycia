import json, numpy as np
from shapely.geometry import Polygon, Point, MultiPolygon, box
from shapely.ops import unary_union
Z=json.load(open('zones.json'))
def P(n):
    c=Z[n]; return Polygon(c) if not isinstance(c[0][0],list) else unary_union([Polygon(x) for x in c])
gz=np.load('gz.npy'); E0,E1,N0,N1=592200,592550,658880,659230
xs=np.arange(E0,E1+1,2.5); ys=np.arange(N0,N1+1,2.5)
dzdy,dzdx=np.gradient(gz,2.5,2.5); slope=np.hypot(dzdx,dzdy)*100
S4=P('S4 Pole A')
steep=[];gentle=[]
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        if S4.contains(Point(x,y)):
            (steep if slope[j,i]>=15 else gentle).append((x,y))
import statistics as st
print('steep n',len(steep),'centroid',st.mean(p[0] for p in steep),st.mean(p[1] for p in steep))
print('gentle n',len(gentle),'centroid',st.mean(p[0] for p in gentle),st.mean(p[1] for p in gentle))
# print a coarse map of S4: rows N desc, cols E asc; S=steep, g=gentle
for y in ys[::-2]:
    row=''
    for x in xs[::2]:
        if S4.contains(Point(x,y)):
            j=int((y-N0)/2.5); i=int((x-E0)/2.5)
            row+='S' if slope[j,i]>=15 else 'g'
        else: row+=' '
    if row.strip(): print(int(y), row[20:110])
print('xs start for print', xs[::2][20], 'step 5 m')

import json, math, numpy as np
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
P=json.load(open('parcels.json'))
PG={k:Polygon(v) for k,v in P.items()}
# --- digitised land-cover / zone polygons (EPSG:2180), from GUGiK orthophoto mosaic
A1=Polygon([(592250.9,658979.9),(592252.7,658986.5),(592264.9,658993.1),(592270,659003),(592287,658994),(592315,658989),(592345,658982),(592304.5,658947.0),(592283.0,658928.5)])
A3=Polygon([(592289,659040),(592295.3,659052.1),(592309.8,659061.3),(592442.3,659065.6),(592420,659047),(592330,659046),(592300,659044)])
A1=A1.intersection(PG['16/1']); A3=A3.intersection(PG['16/1'])
A2=PG['16/1'].difference(A1).difference(A3)
# sub-zones on A2
S2=Polygon([(592318,659012),(592322,659044),(592330,659046),(592378,659046.5),(592378,659016)]).intersection(A2)      # warzywnik + tunel
S3=Polygon([(592378,659016),(592378,659046.5),(592420,659047),(592432,659057),(592410,659030)]).intersection(A2)     # kurnik + woliera + wybieg staly
S4=A2.difference(S2).difference(S3)                                                                                    # pole A
# 24/1
B2=Polygon([(592384,658989),(592443.7,659053.3),(592489,659005),(592445,658996.5)]).intersection(PG['24/1'])          # pole B (ugor)
Bw=Polygon([(592295.9,658928.1),(592317.2,658931.0),(592356.1,658924.8),(592372,658931),(592362,658985),(592319.9,658948.5)]).intersection(PG['24/1']) # naroznik zach. z budynkami
B1=PG['24/1'].difference(B2).difference(Bw)                                                                            # pole kempingowe + pas przy drodze
# 16/3
C1=Polygon([(592383.8,659073.6),(592454.3,659075.9),(592505.9,659120.3),(592471.3,659153.6),(592456.7,659133.7),(592433.3,659113.3),(592404.2,659095.8),(592383.8,659090.0)]).intersection(PG['16/3'])
split=Polygon([(592447,659060),(592447,659200),(592520,659200),(592520,659060)])
S6=C1.intersection(split)            # sad + pasieka (gorna czesc laki)
S7=C1.difference(split)              # pastwisko + laka kosna (dolna czesc)
C2=PG['16/3'].difference(C1)         # drzewostan
Z={'S1 Siedlisko':A1,'S2 Warzywnik z tunelem':S2,'S3 Kurnik z wolierą':S3,'S4 Pole A':S4,'S5 Pole B':B2,
   'S6 Sad z pasieką':S6,'S7 Pastwisko i łąka':S7,'S8a Drzewostan 16/3':C2,'S8b Zadrzewiony stok 16/1':A3,
   'S9 Pole kempingowe':B1,'S10 Budynki kempingu':Bw,'Droga 19/3':PG['19/3']}
gz=np.load('gz.npy'); E0,E1,N0,N1=592200,592550,658880,659230
xs=np.arange(E0,E1+1,2.5); ys=np.arange(N0,N1+1,2.5)
dzdy,dzdx=np.gradient(gz,2.5,2.5)
slope=np.hypot(dzdx,dzdy)*100
asp=(np.degrees(np.arctan2(-dzdx,-dzdy)))%360
def card(a): return ['N','NE','E','SE','S','SW','W','NW'][int(((a+22.5)%360)//45)]
out={}
tot=0
for name,pg in Z.items():
    hs=[];sl=[];ac={}
    minx,miny,maxx,maxy=pg.bounds
    for j,y in enumerate(ys):
        if y<miny or y>maxy: continue
        for i,x in enumerate(xs):
            if x<minx or x>maxx: continue
            if pg.contains(Point(x,y)) and not np.isnan(gz[j,i]):
                hs.append(gz[j,i]); sl.append(slope[j,i])
                if slope[j,i]>3: ac[card(asp[j,i])]=ac.get(card(asp[j,i]),0)+1
    top=sorted(ac.items(),key=lambda t:-t[1])[:2]
    n=sum(ac.values()) or 1
    out[name]=dict(area=pg.area,hmin=min(hs),hmax=max(hs),hmean=sum(hs)/len(hs),slope=sum(sl)/len(sl),smax=max(sl),asp=[(k,round(100*v/n)) for k,v in top])
    tot+=pg.area
    print(f"{name:28s} {pg.area:7.0f} m2  h {min(hs):5.1f}-{max(hs):5.1f}  slope mean {sum(sl)/len(sl):4.1f}% max {max(sl):4.1f}%  {out[name]['asp']}")
print('sum',round(tot), 'parcels',round(sum(p.area for p in PG.values())))
# parcel stats
for k,pg in PG.items():
    hs=[];sl=[]
    for j,y in enumerate(ys):
        for i,x in enumerate(xs):
            if pg.contains(Point(x,y)) and not np.isnan(gz[j,i]): hs.append(gz[j,i]); sl.append(slope[j,i])
    print('parcel',k,round(pg.area),f"h {min(hs):.1f}-{max(hs):.1f} mean slope {sum(sl)/len(sl):.1f}% max {max(sl):.1f}%")
json.dump({k:list(v.exterior.coords) if v.geom_type=='Polygon' else [list(g.exterior.coords) for g in v.geoms] for k,v in Z.items()},open('zones.json','w'))
json.dump({k:{kk:(vv if not isinstance(vv,float) else round(vv,2)) for kk,vv in v.items()} for k,v in out.items()},open('zones_stats.json','w'),ensure_ascii=False,indent=1)

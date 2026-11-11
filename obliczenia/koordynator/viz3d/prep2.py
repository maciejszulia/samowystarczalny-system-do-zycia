import numpy as np, json, base64, math, random
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from shapely.geometry import Polygon, Point, box, LineString, MultiPolygon
from shapely.ops import unary_union
random.seed(7); np.random.seed(7)
E0,N0,W=592200,658880,350
dtm=np.load('dtm1m.npy'); chm=np.load('chm1m.npy'); bld=np.load('bld1m.npy')
def gh(E,N):   # ground height at PL-1992 point (1 m grid, row 0 = north)
    r=int(np.clip(W-1-math.floor(N-N0),0,W-1)); c=int(np.clip(math.floor(E-E0),0,W-1)); return float(dtm[r,c])
# ---------- zones
Z=json.load(open('../zones.json'))
def P(n):
    c=Z[n]; g=Polygon(c) if not isinstance(c[0][0],list) else unary_union([Polygon(x) for x in c])
    return g.buffer(0)
S4=P('S4 Pole A')
west=Polygon([(592200,659100),(592308,659100),(592308,659045),(592310,659012),(592327,659008),(592345,658982),(592345,658900),(592200,658900)])
zones={
 'S1':('Siedlisko',P('S1 Siedlisko'),'#b0b0b0'),
 'S2':('Warzywnik, tunel T1, pole P1, stelaż',P('S2 Warzywnik z tunelem'),'#66c266'),
 'S3':('Budynek inwentarski B1, woliera, wybieg',P('S3 Kurnik z wolierą'),'#ff7f50'),
 'S4a':('Pole P2',S4.difference(west).buffer(0),'#f2d15c'),
 'S4b':('Sad tarasowy i jagodnik',S4.intersection(west).buffer(0),'#c77dd9'),
 'S5':('Pola P3, P4, P5',P('S5 Pole B'),'#e8b339'),
 'S6':('Łąka kośna z pasieką U1',P('S6 Sad z pasieką'),'#9fd8a0'),
 'S7':('Pastwisko kóz',P('S7 Pastwisko i łąka'),'#7fc8c0'),
 'S8a':('Drzewostan opałowy',P('S8a Drzewostan 16/3'),'#2f6b3a'),
 'S8b':('Zadrzewiony stok północny',P('S8b Zadrzewiony stok 16/1'),'#3f8a4c'),
 'S9':('Pole kempingowe',P('S9 Pole kempingowe'),'#6fa8dc'),
 'S10':('Budynki kempingu',P('S10 Budynki kempingu'),'#9ab7d9'),
 'D':('Droga',P('Droga 19/3'),'#d9d9d9'),
}
def parts(g,amin=6):
    gs=[g] if g.geom_type=='Polygon' else [q for q in getattr(g,'geoms',[]) if q.geom_type=='Polygon']
    return [q for q in gs if q.area>=amin]
# S8a as parcel 16/3 minus S6,S7 (clean)
import re
from shapely import wkt
txt=open('../../dzialki_wkt.txt').read()
parc={}
for line in txt.splitlines():
    m=re.match(r'(\S+)\|SRID=2180;(POLYGON.*)',line.strip())
    if m: parc[m.group(1).split('.')[-1]]=wkt.loads(m.group(2))
print('parcels',{k:round(v.area) for k,v in parc.items()})
zones['S8a']=('Drzewostan opałowy',parc['16/3'].difference(unary_union([zones['S6'][1],zones['S7'][1]])).buffer(0),'#2f6b3a')
ZJ={}
for k,(nm,g,col) in zones.items():
    ps=parts(g)
    ZJ[k]={'name':nm,'color':col,'area':round(sum(p.area for p in ps)),'rings':[[[round(x-E0,1),round(y-N0,1)] for x,y in p.simplify(0.3).exterior.coords] for p in ps]}
    c=max(ps,key=lambda p:p.area).representative_point(); ZJ[k]['label']=[round(c.x-E0,1),round(c.y-N0,1)]
print({k:v['area'] for k,v in ZJ.items()}, sum(v['area'] for v in ZJ.values()))
# ---------- rasters 0.5 m/px (700 px), row 0 = north
S=2; PX=W*S
def xy(E,N): return ((E-E0)*S,(N0+W-N)*S)
def hexrgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
zim=Image.new('RGBA',(PX,PX),(0,0,0,0)); d=ImageDraw.Draw(zim)
for k,(nm,g,col) in zones.items():
    for p in parts(g):
        d.polygon([xy(x,y) for x,y in p.exterior.coords],fill=hexrgb(col)+(95,))
for k,(nm,g,col) in zones.items():
    for p in parts(g):
        d.line([xy(x,y) for x,y in p.exterior.coords],fill=(35,35,35,205),width=2)
zim.save('zones.png',optimize=True)
# ---------- plan overlay
pim=Image.new('RGBA',(PX,PX),(0,0,0,0)); d=ImageDraw.Draw(pim)
def fill(g,rgba):
    for p in parts(g,1): d.polygon([xy(x,y) for x,y in p.exterior.coords],fill=rgba)
def outline(g,rgba,w=2):
    for p in parts(g,1): d.line([xy(x,y) for x,y in p.exterior.coords],fill=rgba,width=w)
S2=zones['S2'][1]; S4a=zones['S4a'][1]; S5=zones['S5'][1]; S4b=zones['S4b'][1]; S7=zones['S7'][1]; S3=zones['S3'][1]; S6=zones['S6'][1]
service=box(592323,659036.5,592361,659041.5).intersection(S2)
t1=box(592371.75,659016.5,592376.25,659036.5)
mound=Point(592357,659018.5).buffer(5.0)
garden=box(592318,659011,592351,659034.5).intersection(S2).difference(mound.buffer(1))
compost=box(592366,659041,592376,659045.5).intersection(S2)
p1=S2.difference(unary_union([service,t1.buffer(1),mound.buffer(1),garden,compost])).buffer(0)
FIELD={'P1':(214,170,60),'P2':(226,200,90),'P3':(205,150,50),'P4':(232,190,80),'P5':(190,140,60)}
fill(p1,FIELD['P1']+(165,)); fill(S4a,FIELD['P2']+(165,))
# S5 terciles by elevation (contour strips) with 2 m grass buffer
rr=[];
mask5=np.zeros((W,W),bool)
for r in range(W):
    for c in range(W):
        if S5.contains(Point(E0+c+.5,N0+W-1-r+.5)): mask5[r,c]=True
h5=dtm[mask5]; q1,q2=np.quantile(h5,[1/3,2/3]); print('S5 terciles',round(float(q1),2),round(float(q2),2),'area',int(mask5.sum()))
arr=np.zeros((W,W,4),np.uint8)
for name,lo,hi in (('P3',-1e9,q1),('P4',q1,q2),('P5',q2,1e9)):
    m=mask5&(dtm>lo+0.12)&(dtm<=hi-0.12)
    arr[m]=FIELD[name]+(165,)
    rs,cs=np.where(m); print(name,'cells',int(m.sum()),'centroid E,N',round(E0+cs.mean()+.5,1),round(N0+W-1-rs.mean()+.5,1))
strip=Image.fromarray(arr,'RGBA').resize((PX,PX),Image.NEAREST); pim.alpha_composite(strip); d=ImageDraw.Draw(pim)
# garden beds: stripes 1.2 m bed / 0.5 m path, E-W
fill(garden,(96,70,45,200))
y=659012.0
while y<659034.5:
    bed=box(592318,y,592351,y+1.2).intersection(garden)
    if not bed.is_empty: fill(bed,(70,140,60,225))
    y+=1.7
fill(service,(170,165,150,235)); fill(compost,(90,60,35,240))
fill(t1,(245,245,245,120))
# pasture paddocks S7
x=592383.8+15
while x<592447:
    seg=LineString([(x,659060),(x,659130)]).intersection(S7)
    if not seg.is_empty:
        for gline in ([seg] if seg.geom_type=='LineString' else seg.geoms):
            d.line([xy(*p) for p in gline.coords],fill=(255,255,255,220),width=2)
    x+=15
outline(S7,(255,255,255,230),3)
# run fence S3
outline(S3,(120,60,20,255),3)
woliera=box(592380.5,659022.5,592390.5,659032.5).intersection(S3)
fill(woliera,(255,200,150,170)); outline(woliera,(120,60,20,255),2)
# orchard terraces: contour lines every 2 m inside S4b
mask4=np.zeros((W,W),bool)
for r in range(W):
    for c in range(W):
        if S4b.contains(Point(E0+c+.5,N0+W-1-r+.5)): mask4[r,c]=True
sm=ndi.gaussian_filter(dtm,1.5)
terr=np.zeros((W,W),bool); orch=[]
for lev in np.arange(109,118,2.0):
    band=mask4&(np.abs(sm-lev)<0.22)
    terr|=band
    rs,cs=np.where(band)
    pts=sorted(zip(cs,rs))
    last=None
    for c,r in pts:
        if last is None or math.hypot(c-last[0],r-last[1])>=6:
            if all(math.hypot(c-a,r-b)>=5.5 for a,b,_ in orch):
                orch.append((c,r,lev)); last=(c,r)
ta=np.zeros((W,W,4),np.uint8); ta[terr]=(120,80,40,235)
pim.alpha_composite(Image.fromarray(ta,'RGBA').resize((PX,PX),Image.NEAREST))
pim.save('plan.png',optimize=True)
print('orchard trees',len(orch))
# ---------- orthophoto texture
im=Image.open('../orto_mosaic.png').convert('RGB'); im.save('orto.jpg',quality=84,optimize=True,progressive=True)
o=np.asarray(im.resize((W,W),Image.BOX))
# ---------- terrain 2 m
dtm2=dtm.reshape(175,2,175,2).mean(axis=(1,3))
u16=np.round((dtm2-100)*100).astype('<u2')
# ---------- measured trees (tree tops) from CHM 2018
c2=np.where(bld,0,chm); sm2=ndi.gaussian_filter(c2,0.8)
mx=ndi.maximum_filter(sm2,size=5)
tops=(sm2==mx)&(c2>=4.0)
rs,cs=np.where(tops)
trees=[]
for r,c in zip(rs,cs):
    hmax=float(chm[max(0,r-1):r+2,max(0,c-1):c+2].max())
    trees.append((c+.5,W-1-r+.5,hmax))
clear=unary_union([zones[k][1] for k in ('S2','S3','S4a','S5')]).buffer(0.5)
trees=[t for t in trees if not clear.contains(Point(E0+t[0],N0+t[1]))]
print('measured tree tops',len(trees))
# ---------- schematic trees in S8a where measured tops are missing
S8a=zones['S8a'][1]; sch=[]
tx=np.array([[t[0],t[1]] for t in trees]) if trees else np.zeros((0,2))
from scipy.spatial import cKDTree
kd=cKDTree(tx)
minx,miny,maxx,maxy=S8a.bounds
yy=miny
while yy<maxy:
    xx=minx
    while xx<maxx:
        px=xx+random.uniform(-1.6,1.6); py=yy+random.uniform(-1.6,1.6)
        if S8a.contains(Point(px,py)):
            lx,ly=px-E0,py-N0
            if 0<lx<W and 0<ly<W and len(kd.query_ball_point([lx,ly],3.2))==0:
                sch.append((lx,ly,random.uniform(11,16)))
        xx+=5.0
    yy+=5.0
print('schematic trees S8a',len(sch))
def pack_i16(a): return base64.b64encode(np.round(np.array(a)*10).astype('<i2').tobytes()).decode()
# ---------- buildings (1 m cells)
rs,cs=np.where(bld); B=[]
for r,c in zip(rs,cs):
    col=o[r,c]; B.append((c,W-1-r,int(round(chm[r,c]*10)),int(col[0]),int(col[1]),int(col[2])))
bb=base64.b64encode(np.array(B,dtype='<i2').tobytes()).decode()
# ---------- objects
def obj(E,N): return {'x':round(E-E0,1),'y':round(N-N0,1),'h':round(gh(E,N),2)}
pvseg=[]
for i in range(8):
    E=592325+4*i+2; pvseg.append({'x':E-E0,'y':659036-N0,'h':round(gh(E,659036),2)})
objects={
 'pv':{'label':'Stelaż fotowoltaiki 25 kWp','seg':pvseg,'len':32,'tilt':60,'panel':3.0,'edge':0.5},
 'w1':dict(obj(592363,659036),label='W1 zbiornik górny, 1,06 bar'),
 't1':dict(obj(592374,659026.5),label='T1 tunel foliowy 90 m²',len=20,wid=4.5),
 'b1':dict(obj(592392,659036),label='B1 kurnik i koziarnia'),
 'wol':dict(obj(592385.5,659027.5),label='Woliera 100 m²'),
 'm1':dict(obj(592292,659000),label='M1 piwnica ziemna'),
 'u1':dict(obj(592470,659122),label='U1 pasieka, 3 ule'),
 'k':dict(obj(592357,659018.5),label='Gruzowisko 120,2 m n.p.m.',top=round(float(dtm[W-1-(659019-N0),592356-E0]),2)),
 'dom':dict(obj(592285,658959),label='Dom 107,3 m n.p.m.'),
}
labels=[
 {'t':'jezioro Ukiel','x':592455-E0,'y':658905-N0,'h':104.7,'c':'water'},
 {'t':'P1','x':round(p1.representative_point().x-E0,1),'y':round(p1.representative_point().y-N0,1),'c':'field'},
 {'t':'P2','x':round(S4a.representative_point().x-E0,1),'y':round(S4a.representative_point().y-N0,1),'c':'field'},
 {'t':'Warzywnik 811 m²','x':592334-E0,'y':659022-N0,'c':'field'},
 {'t':'Sad','x':592290-E0,'y':659022-N0,'c':'field'},
]
for name,lo,hi in (('P3',-1e9,q1),('P4',q1,q2),('P5',q2,1e9)):
    m=mask5&(dtm>lo)&(dtm<=hi); rs,cs=np.where(m)
    labels.append({'t':name,'x':round(float(cs.mean())+.5,1),'y':round(float(W-1-rs.mean())+.5,1),'c':'field'})
for L in labels:
    if 'h' not in L: L['h']=round(gh(L['x']+E0,L['y']+N0),2)
orchard=[[c+.5,W-1-r+.5,round(float(dtm[r,c]),2)] for c,r,lev in orch]
parcels={k:[[round(x-E0,1),round(y-N0,1)] for x,y in g.exterior.coords] for k,g in parc.items()}
data={'meta':{'E0':E0,'N0':N0,'size':W,'cell':2,'n':175,'base':104.7,'lake':104.7,'lat':53.7875,
              'dtmDate':'2018-03-21','ortoDate':'2025-08-14','made':'2026-11-11'},
      'dtm':base64.b64encode(u16.tobytes()).decode(),
      'trees':pack_i16(trees),'ntrees':len(trees),'sch':pack_i16(sch),'nsch':len(sch),
      'bld':bb,'nbld':len(B),'zones':ZJ,'parcels':parcels,'objects':objects,'labels':labels,'orchard':orchard}
js='window.FARM='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n'
open('data.js','w',encoding='utf-8').write(js)
import os
for f in ('data.js','orto.jpg','zones.png','plan.png'): print(f,os.path.getsize(f))
print('B1 ground',gh(592400,659041),'wol',gh(592388,659029),'pv',[s['h'] for s in pvseg])

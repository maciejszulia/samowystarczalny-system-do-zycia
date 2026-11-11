import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Patch
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union, split
from PIL import Image
Z=json.load(open('zones.json'))
def P(n):
    c=Z[n]; return Polygon(c) if not isinstance(c[0][0],list) else unary_union([Polygon(x) for x in c])
S4=P('S4 Pole A')
west=Polygon([(592200,659100),(592308,659100),(592308,659045),(592310,659012),(592327,659008),(592345,658982),(592345,658900),(592200,658900)])
S4b=S4.intersection(west); S4a=S4.difference(west)
zones=[
 ('S1','Siedlisko',P('S1 Siedlisko'),'#b0b0b0'),
 ('S2','Warzywnik, tunel, pole P1',P('S2 Warzywnik z tunelem'),'#66c266'),
 ('S3','Budynek inwentarski, woliera, wybieg',P('S3 Kurnik z wolierą'),'#ff7f50'),
 ('S4a','Pole P2',S4a,'#f2d15c'),
 ('S4b','Sad tarasowy i jagodnik',S4b,'#c77dd9'),
 ('S5','Pola P3–P5 (pasy wzdłuż warstwic)',P('S5 Pole B'),'#e8b339'),
 ('S6','Łąka kośna z pasieką',P('S6 Sad z pasieką'),'#9fd8a0'),
 ('S7','Pastwisko kóz',P('S7 Pastwisko i łąka'),'#7fc8c0'),
 ('S8a','Drzewostan opałowy',P('S8a Drzewostan 16/3'),'#2f6b3a'),
 ('S8b','Zadrzewiony stok północny',P('S8b Zadrzewiony stok 16/1'),'#3f8a4c'),
 ('S9','Pole kempingowe',P('S9 Pole kempingowe'),'#6fa8dc'),
 ('S10','Budynki kempingu',P('S10 Budynki kempingu'),'#9ab7d9'),
 ('D','Droga (działka 19/3)',P('Droga 19/3'),'#d9d9d9'),
]
areas={c:round(g.area) for c,_,g,_ in zones}
print(areas, sum(areas.values()))
json.dump(areas,open('zone_areas.json','w'))
mos=Image.open('orto_mosaic.png'); E0,E1,N0,N1=592200,592550,658880,659230
gz=np.load('gz.npy'); gx,gy=np.meshgrid(np.arange(E0,E1+1,2.5),np.arange(N0,N1+1,2.5))
fig,ax=plt.subplots(figsize=(10.5,9),dpi=130)
ax.imshow(mos,extent=[E0,E1,N0,N1],alpha=0.55)
cs=ax.contour(gx,gy,gz,levels=np.arange(104,126,2),colors='k',linewidths=0.4,alpha=0.6)
ax.clabel(cs,fmt='%d',fontsize=6)
lab={'S1':(592288,658968),'S2':(592338,659024),'S3':(592407,659027),'S4a':(592352,658999),'S4b':(592298,659012),'S5':(592440,659018),
     'S6':(592470,659112),'S7':(592415,659088),'S8a':(592345,659125),'S8b':(592360,659054),'S9':(592420,658968),'S10':(592335,658945),'D':(592395,659023)}
for c,n,g,col in zones:
    geoms=[g] if g.geom_type=='Polygon' else [q for q in g.geoms if q.geom_type=='Polygon']
    for gg in geoms:
        ax.add_patch(MPoly(list(gg.exterior.coords),closed=True,fc=col,ec='black',lw=1.0,alpha=0.62))
    if c!='D':
        x,y=lab[c]; ax.text(x,y,c,fontsize=10,weight='bold',ha='center',va='center',bbox=dict(facecolor='white',alpha=0.8,pad=1.5,edgecolor='none'))
# obiekty punktowe
objs=[('B1',592392,659036,'s','budynek inwentarski'),('W1',592363,659036,'o','zbiornik górny 118 m n.p.m.'),('M1',592292,659000,'^','piwnica ziemna'),
      ('U1',592470,659122,'D','pasieka'),('T1',592374,659026,'P','tunel foliowy'),('K',592357,659019,'X','gruzowisko 120 m n.p.m. (model terenu)')]
OFF={'B1':(5,5),'W1':(1,5),'M1':(4,4),'U1':(4,4),'T1':(3,-9),'K':(-11,-9)}
for k,x,y,m,_ in objs:
    ax.plot(x,y,marker=m,ms=9,mfc='red',mec='white',mew=1.2,ls='none')
    ax.text(x+OFF[k][0],y+OFF[k][1],k,fontsize=9,color='red',weight='bold',bbox=dict(facecolor='white',alpha=0.75,pad=1,edgecolor='none'))
ax.plot([592325,592357],[659036,659036],color='navy',lw=4,solid_capstyle='butt'); ax.text(592334,659041,'PV',fontsize=9,color='navy',weight='bold',ha='center',bbox=dict(facecolor='white',alpha=0.75,pad=1,edgecolor='none'))
ax.set_xlim(592225,592530); ax.set_ylim(658905,659205); ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
ax.plot([592240,592290],[658915,658915],color='black',lw=4,solid_capstyle='butt'); ax.text(592265,658920,'50 m',ha='center',fontsize=10,weight='bold')
ax.annotate('N',xy=(592515,659195),xytext=(592515,659170),ha='center',fontsize=12,weight='bold',arrowprops=dict(arrowstyle='-|>',color='black',lw=2))
ax.text(592440,658925,'jezioro Ukiel',fontsize=11,style='italic',ha='center')
handles=[Patch(fc=col,ec='black',label=f"{c}  {n}: "+f"{areas[c]:,}".replace(',',' ')+" m²") for c,n,g,col in zones]
import matplotlib.lines as mlines
handles+=[mlines.Line2D([],[],marker=m,color='w',mfc='red',mec='white',ms=9,label=f"{k}  {d}") for k,x,y,m,d in objs]
handles+=[mlines.Line2D([],[],color='navy',lw=4,label='PV  stelaż fotowoltaiki 25 kWp, 32 m')]
ax.legend(handles=handles,loc='center left',bbox_to_anchor=(1.01,0.5),fontsize=8.5,frameon=False,title='Strefy i obiekty',title_fontsize=10)
ax.set_title('Plan stref gospodarstwa (warstwice co 2 m)',fontsize=12)
plt.tight_layout(); plt.savefig('fig_C_strefy.png',bbox_inches='tight'); plt.close()
# fix title of fig B point count

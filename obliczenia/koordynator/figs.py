import json, math, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
from shapely.geometry import Polygon, Point
from PIL import Image
from scipy.interpolate import griddata

P=json.load(open('parcels.json'))
# neighbours from agent 1
NB={}
for line in open('../R1/parcels_raw.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    pid, ext, geom = [s.strip() for s in line.split('#')]
    ring=geom.split('|R|')[0]
    pts=[tuple(map(float,p.split())) for p in ring.split(';') if p.strip()]
    NB[pid.split('.',1)[1]]=pts   # e.g. 0144.16/1
# elevation points
E=[]
for f in ['../R1/elev1.txt','../R1/elev2.txt']:
    for rec in open(f).read().strip().replace('\n',',').split(','):
        rec=rec.strip()
        if not rec: continue
        n,e,h=rec.split(); E.append((float(e),float(n),float(h)))
for e,n,h in json.load(open('nmt_pts.json')): E.append((e,n,h))
E=list({(e,n):h for e,n,h in E}.items())
ex=np.array([k[0] for k,_ in E]); ny=np.array([k[1] for k,_ in E]); hz=np.array([h for _,h in E])
print('elev points',len(E), hz.min(), hz.max())

E0,E1,N0,N1=592200,592550,658880,659230
gx,gy=np.meshgrid(np.arange(E0,E1+1,2.5),np.arange(N0,N1+1,2.5))
gz=griddata((ex,ny),hz,(gx,gy),method='cubic')
np.save('gz.npy',gz)
mos=Image.open('orto_mosaic.png')
MINE={'16/1':'#ffd400','24/1':'#ff8c1a','16/3':'#7CFC00','19/3':'#00e5ff'}

def base(ax,photo=True,alpha=1.0):
    if photo: ax.imshow(mos,extent=[E0,E1,N0,N1],alpha=alpha)
    ax.set_xlim(E0,E1); ax.set_ylim(N0,N1); ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
def scalebar(ax,x=592215,y=658892,L=50,color='white'):
    ax.plot([x,x+L],[y,y],color=color,lw=4,solid_capstyle='butt')
    ax.text(x+L/2,y+5,f'{L} m',color=color,ha='center',fontsize=11,weight='bold')
    ax.annotate('N',xy=(592530,659215),xytext=(592530,659190),color=color,ha='center',fontsize=13,weight='bold',
                arrowprops=dict(arrowstyle='-|>',color=color,lw=2))

# --- Fig A: stan obecny
fig,ax=plt.subplots(figsize=(9,9),dpi=130)
base(ax)
for k,v in NB.items():
    if k.split('.')[1] in P and k.startswith('0144'): continue
    xs=[p[0] for p in v]+[v[0][0]]; ys=[p[1] for p in v]+[v[0][1]]
    ax.plot(xs,ys,color='white',lw=0.6,alpha=0.55)
area={}
for k,v in P.items():
    pg=Polygon(v); area[k]=pg.area
    ax.add_patch(MPoly(v,closed=True,fill=False,ec=MINE[k],lw=2.6))
lab={'16/1':(592312,659012),'24/1':(592432,658985),'16/3':(592345,659120),'19/3':(592392,659030)}
for k,(x,y) in lab.items():
    t=f"{k}\n{area[k]/1e4:.2f} ha".replace('.',',')
    ax.text(x,y,t,color=MINE[k],fontsize=12,weight='bold',ha='center',va='center',
            bbox=dict(facecolor='black',alpha=0.55,pad=3,edgecolor='none'))
ax.text(592440,658915,'jezioro Ukiel',color='white',fontsize=12,style='italic',ha='center')
ax.text(592410,659218,'jezioro Zgniłek (mokradło)',color='white',fontsize=10,style='italic',ha='center')
scalebar(ax)
ax.set_title('Działki gospodarstwa na ortofotomapie (obręb 144, Olsztyn-Gutkowo)',fontsize=12)
plt.tight_layout(); plt.savefig('fig_A_dzialki.png',bbox_inches='tight'); plt.close()

# --- Fig B: rzeźba
fig,ax=plt.subplots(figsize=(9,9),dpi=130)
base(ax,photo=True,alpha=0.35)
lev=np.arange(104,126,1)
cf=ax.contourf(gx,gy,gz,levels=lev,cmap='terrain',alpha=0.55)
cs=ax.contour(gx,gy,gz,levels=np.arange(104,126,2),colors='k',linewidths=0.7)
ax.clabel(cs,fmt='%d',fontsize=8)
for k,v in P.items():
    ax.add_patch(MPoly(v,closed=True,fill=False,ec='black',lw=2.4))
    x,y=lab[k]; ax.text(x,y,k,fontsize=12,weight='bold',ha='center',va='center',bbox=dict(facecolor='white',alpha=0.7,pad=2,edgecolor='none'))
cb=plt.colorbar(cf,ax=ax,fraction=0.035,pad=0.02); cb.set_label('wysokość [m n.p.m.]')
scalebar(ax,color='black')
ax.set_title('Rzeźba terenu: warstwice co 2 m (NMT GUGiK, interpolacja z 413 punktów)',fontsize=12)
plt.tight_layout(); plt.savefig('fig_B_rzezba.png',bbox_inches='tight'); plt.close()
print({k:round(a) for k,a in area.items()})

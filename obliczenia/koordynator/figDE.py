import numpy as np, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pvgis_shs import PV60_HZ as PV60
M=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
DNI=[31,28.25,31,30,31,30,31,31,30,31,30,31]
kwp=25
prod=[kwp*v/d for v,d in zip(PV60,DNI)]            # kWh/dobe
norm=[444,422,472,422,374,381,410,427,391,411,405,441]   # scenariusz M, kWh/mies. (raport energii)
load_n=[v/d for v,d in zip(norm,DNI)]
load=[8.0 if i in (0,1,10,11) else load_n[i] for i in range(12)]
fig,ax=plt.subplots(figsize=(8.6,4.6),dpi=140)
ax.bar(M,prod,color='#f2b134',label='Produkcja 25 kWp, kąt 60° [kWh na dobę]')
ax.plot(M,load,color='#1f4e79',marker='o',lw=2.2,label='Zużycie: tryb zimowy XI–II, tryb normalny III–X [kWh na dobę]')
ax.plot(M,load_n,color='#1f4e79',ls=':',lw=1.5,label='Zużycie w trybie normalnym przez 12 miesięcy')
for i,v in enumerate(prod): ax.text(i,v+1.5,f"{v:.0f}",ha='center',fontsize=8)
ax.set_ylabel('kWh na dobę (średnia miesiąca)'); ax.set_ylim(0,130)
ax.set_title('Fotowoltaika 25 kWp i zużycie energii: średnie dobowe w miesiącach',fontsize=11)
ax.legend(fontsize=8,loc='upper left',frameon=False); ax.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('fig_D_energia.png'); plt.close()
print('prod kWh/d',[round(p,1) for p in prod]); print('rok kWh',round(sum(kwp*v for v in PV60)))
print('load',[round(l,1) for l in load], 'rok',round(sum(l*d for l,d in zip(load,DNI))))

# --- praca w miesiacach [h/tydzien], zakres od-do (tabela nakladow z raportu automatyzacji; rozklad: zalozenie)
seas=[1,2,6,10,14,12,13,14,13,10,4,1]
def dist(lo,hi,w):
    s=sum(w); return [(lo*x/s,hi*x/s) for x in w]
uni=[d for d in DNI]
items=[
 ('uprawy i przetwórstwo',(300+30+120,700+100+250),seas),
 ('kury: kontrola, pasza, ściółka',(61+60,91+100),uni),
 ('ubój drobiu',(13,33),[0,0,0,0,0,25,0,25,0,50,0,0]),
 ('kozy: dój, karmienie',(250,500),[11,10,31,30,31,30,31,31,30,31,30,11]),
 ('przerób mleka',(80,200),[0,0,31,30,31,30,31,31,30,31,30,0]),
 ('pszczoły',(45,100),[0,0,0,15,20,20,15,15,10,5,0,0]),
 ('drewno: ścinka, łupanie',(30,80),[30,30,20,0,0,0,0,0,0,0,10,10]),
 ('kocioł',(45,70),[682,596,552,363,0,0,0,0,0,372,501,632]),
 ('piwnica i zapasy',(15,40),[31,28,31,30,0,0,0,0,0,31,30,31]),
 ('utrzymanie instalacji',(50,90),uni),
]
lo=np.zeros(12); hi=np.zeros(12); rows={}
for n,(a,b),w in items:
    d=dist(a,b,w); rows[n]=d
    lo+=np.array([x[0] for x in d]); hi+=np.array([x[1] for x in d])
wk=[d/7 for d in DNI]
lo_w=lo/np.array(wk); hi_w=hi/np.array(wk)
print('suma rok',round(lo.sum()),round(hi.sum()))
print('h/tydz od',[round(x) for x in lo_w]); print('h/tydz do',[round(x) for x in hi_w])
json.dump({'lo_w':list(map(float,lo_w)),'hi_w':list(map(float,hi_w)),'lo':list(map(float,lo)),'hi':list(map(float,hi))},open('praca.json','w'))
fig,ax=plt.subplots(figsize=(8.6,4.4),dpi=140)
mid=(lo_w+hi_w)/2
ax.bar(M,hi_w-lo_w,bottom=lo_w,color='#8fbf8f',label='Zakres: od wariantu oszczędnego do wariantu pracochłonnego')
ax.plot(M,mid,color='#2f6b3a',marker='o',lw=2,label='Środek zakresu')
for i,(a,b) in enumerate(zip(lo_w,hi_w)): ax.text(i,b+1.2,f"{a:.0f}–{b:.0f}",ha='center',fontsize=8)
ax.set_ylabel('godziny pracy na tydzień (cała rodzina)'); ax.set_ylim(0,75)
ax.set_title('Nakład pracy po automatyzacji: stado domowe, 2 kozy, 3 ule',fontsize=11)
ax.legend(fontsize=8,loc='upper left',frameon=False); ax.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('fig_E_praca.png'); plt.close()

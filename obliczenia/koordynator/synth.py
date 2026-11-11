# Synteza koordynatora: przydzial gruntu wg pomiaru z ortofotomapy i NMT (grunt orny o spadku < 15 %)
import sys; sys.path.insert(0,'../R2')
from dane import *
from b_plony_powierzchnia import powierzchnia
N_OS=4
POLA=1732+1400+2656        # S2 + S4 (czesc o spadku <15 %) + S5 (czesc o spadku <15 %)  [m2]
mn={"warzywnik":1.25,"tunel foliowy":1.20,"okopowe":1.10,"strączkowe":1.10,"zboża":1.10,"oleiste":1.10,"sad i jagodnik":1.0}
pri=["warzywnik","tunel foliowy","okopowe","strączkowe","zboża","oleiste"]
go=powierzchnia(2,0)[1]; gd=powierzchnia(2,1)[1]
kcal_gr={}
for n,gr,kg,pr,z,zz,pl,m2,kcal in powierzchnia(2,0)[0]:
    kcal_gr[gr]=kcal_gr.get(gr,0)+kcal*N_OS
zwierz=N_OS*(66+74+40+37+473+65)
dieta=N_OS*3037
print("POLA",POLA,"m2; dieta",dieta,"kcal/d; zwierzece",zwierz,"kcal/d; sad",round(kcal_gr["sad i jagodnik"]/365))
for idx,nz in ((0,"ostrożny"),(1,"dobry")):
    g=go if idx==0 else gd
    reszta=POLA; kp=0; ka=0
    print("--",nz)
    for gr in pri:
        potrz=N_OS*g[gr]*mn[gr]; prz=min(potrz,reszta); reszta-=prz
        ka+=kcal_gr[gr]; kp+=kcal_gr[gr]*prz/potrz
        print(f"  {gr:14s} potrzeba {potrz:6.0f}  przydzial {prz:6.0f}  pokrycie {100*prz/potrz:4.0f} %  energia grupy {kcal_gr[gr]/365:6.0f} kcal/d")
    sad=kcal_gr["sad i jagodnik"]/365
    print(f"  zostaje {reszta:.0f} m2; uprawy jednoroczne {kp/365:.0f} z {ka/365:.0f} kcal/d = {100*kp/ka:.0f} %")
    print(f"  pokrycie diety: rosliny jednoroczne+sad {100*(kp/365+sad)/dieta:.0f} %; z produktami zwierzecymi {100*(kp/365+sad+zwierz)/dieta:.0f} %")
    # zakupy
    zb_potrz=N_OS*g["zboża"]*mn["zboża"]; 
# zakup ziarna przy ostroznym
potrz={gr:N_OS*go[gr]*mn[gr] for gr in pri}
reszta=POLA-sum(potrz[g] for g in pri[:4])
brak=potrz["zboża"]-max(0,min(potrz["zboża"],reszta))
zboza_kg=N_OS*(10/0.95+58/0.95+28/0.95+8/0.65+8/0.70)
print("ostrozny: brak zboz m2",round(brak),"udzial",round(brak/potrz["zboża"],2),"zakup ziarna kg/rok",round(zboza_kg*brak/potrz["zboża"]), "zboza potrzeba kg",round(zboza_kg))
potrzd={gr:N_OS*gd[gr]*mn[gr] for gr in pri}
resztad=POLA-sum(potrzd[g] for g in pri[:5])
print("dobry: po zbozach zostaje",round(resztad),"m2 na oleiste; potrzeba oleistych",round(potrzd["oleiste"]),"pokrycie",round(100*max(0,resztad)/potrzd["oleiste"]),"%")
print("sad potrzeba ostrozny/dobry m2:",round(N_OS*go["sad i jagodnik"]),round(N_OS*gd["sad i jagodnik"]))

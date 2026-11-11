import math, sys
from hz_data import *
phi=math.radians(53.7875)
def sun(Hdeg,decdeg=-23.44):
    dec=math.radians(decdeg); H=math.radians(Hdeg)
    el=math.asin(math.sin(phi)*math.sin(dec)+math.cos(phi)*math.cos(dec)*math.cos(H))
    az=math.atan2(math.sin(H), math.cos(H)*math.sin(phi)-math.tan(dec)*math.cos(phi))
    return math.degrees(el), 180+math.degrees(az)
def t(Hd): h=12+Hd/15; return f"{int(h):02d}:{int(round((h-int(h))*60)):02d}"
def check(prof,name,col=1,decdeg=-23.44):
    hz={int(r[0]):r[col] for r in prof}
    def hor(az):
        a0=int(az//5*5)%360; a1=(a0+5)%360; f=(az-a0)/5; return hz[a0]*(1-f)+hz[a1]*f
    tot=blk=0; e_tot=e_blk=0; first=last=None; minmargin=99
    for m in range(-12*60*4//4, 12*60*4//4+1):
        Hd=m*0.25; el,az=sun(Hd,decdeg)
        if el<=0: continue
        tot+=1; am=1/max(0.02,math.sin(math.radians(el))); w=math.sin(math.radians(el))*0.7**(am**0.678); e_tot+=w
        if el<hor(az): blk+=1; e_blk+=w
        else:
            if first is None: first=Hd
            last=Hd
        if abs(Hd)<=30: minmargin=min(minmargin, el-hor(az))
    print(f"{name}: sun-up {tot} min, blocked {blk} min, clear {t(first)}–{t(last)}, beam blocked {100*e_blk/e_tot:.1f} %, min margin 10–14 h {minmargin:.1f}°")
if __name__=="__main__":
    for nm,p in (('A 2018',parse(A_clr)),('B 2018',parse(B_clr)),('C 2018',parse(C0)),('C +5 m',parse(C5))):
        check(p,nm+' max'); check(p,nm+' mean',2)
    print(','.join(str(r[1]) for r in parse(C0)))
    print(','.join(str(r[1]) for r in parse(C5)))
    print('S sector max 150-210 C0', max(r[1] for r in parse(C0) if 150<=r[0]<=210), min(r[1] for r in parse(C0) if 150<=r[0]<=210))
    print('N sector C0', min(r[1] for r in parse(C0) if r[0]>=300 or r[0]<=60), max(r[1] for r in parse(C0) if r[0]>=300 or r[0]<=60))

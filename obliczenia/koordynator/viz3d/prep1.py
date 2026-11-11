import numpy as np, json
from PIL import Image
from scipy import ndimage as ndi
dtm=np.load('dtm1m.npy'); chm=np.load('chm1m.npy')
im=Image.open('../orto_mosaic.png').convert('RGB')
o=np.asarray(im.resize((350,350),Image.BOX)).astype(np.float32)
R,G,B=o[...,0],o[...,1],o[...,2]
exg=2*G-R-B; bright=(R+G+B)/3
# roughness of CHM
mean=ndi.uniform_filter(chm,3); sq=ndi.uniform_filter(chm*chm,3); std=np.sqrt(np.maximum(sq-mean*mean,0))
cand=(chm>=2.2)&(chm<=14)&(std<0.9)
cand=ndi.binary_opening(cand,iterations=1)
lab,n=ndi.label(cand)
sizes=ndi.sum(cand,lab,range(1,n+1))
bld=np.zeros_like(cand)
info=[]
for i,s in enumerate(sizes,1):
    if s>=14:
        m=lab==i
        g=float(exg[m].mean()); h=float(chm[m].mean()); sd=float(std[m].mean())
        rr,cc=np.where(m)
        info.append((int(s),round(h,1),round(sd,2),round(g,1),int(cc.mean())+592200,658880+349-int(rr.mean())))
        if sd<0.6: bld|=m
bld=ndi.binary_dilation(bld,iterations=1)&(chm>=2.0)&(chm<=12.5)&(std<1.6)
np.save('bld1m.npy',bld)
print('components>=14 m2:',len(info)); 
for t in sorted(info,key=lambda t:-t[0])[:40]: print(t)
print('building cells',int(bld.sum()))
# preview
big=im.resize((1050,1050))
ov=np.asarray(big).copy()
mask=np.kron(bld,np.ones((3,3),bool))
ov[mask]=(0.4*ov[mask]+0.6*np.array([255,0,0])).astype(np.uint8)
tall=np.kron((chm>=5)&~bld,np.ones((3,3),bool))
ov[tall]=(0.6*ov[tall]+0.4*np.array([255,255,0])).astype(np.uint8)
Image.fromarray(ov).save('preview_class.jpg',quality=80)

import numpy as np
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

gün_sayisi = 28
hemşire_sayisi = 8
populasyon = 30

if gün_sayisi ==7:
    calisma_saati = 40
if gün_sayisi == 28:
    calisma_saati = 160

#%%

nsp_tablo = np.zeros((populasyon, hemşire_sayisi, gün_sayisi+1))

for p in range(0,populasyon):
    for i in range(0,gün_sayisi):
        rnd =np.random.randint(5,hemşire_sayisi)
        atamalar= random.sample(range(0,hemşire_sayisi),rnd)
        for j in range(0,rnd):
            rnd2 = np.random.randint(0,2)
            if rnd2 == 1:
                nsp_tablo[p,atamalar[j],i]=16
            else:
                nsp_tablo[p,atamalar[j],i]=8

#%% gece çalışanlar ertesi gün çalışmasın

def gece_vardiyasi(NSPtablo):
    tablo = NSPtablo.copy()
    for p in range(0,populasyon):
        for i in range(0,hemşire_sayisi):
            for j in range(1,gün_sayisi):
                if tablo[p,i,j-1] == 16:
                    tablo[p,i,j] = 0
    return tablo
#%%toplam çalışma süresi 

def toplam_calisma(nsp_tablo):
    for p in range(0,populasyon):
        for i in range(0,hemşire_sayisi):
            nsp_tablo[p,i,-1] = 0
            calisma_süresi = np.sum(nsp_tablo[p,i].sum())
            nsp_tablo[p,i,-1] = calisma_süresi
    return nsp_tablo

#%%ceza hesapla

def ceza_hesapla(nsp_tablo):
    kd_sabah = 8.45
    kd_akşam = 15.75
    
    ceza_tablo = np.zeros((populasyon,1))
    
    for p in range(0,populasyon):
        ceza = 0
        for i in range(0,hemşire_sayisi):
            if nsp_tablo[p,i,-1] !=calisma_saati:
                ceza = ceza + abs(nsp_tablo[p,i,-1] - calisma_saati)

        for i in range(0,gün_sayisi):
            sabah_calisma = 0
            akşam_calisma = 0
            for j in range(0,hemşire_sayisi):
                if nsp_tablo[p,j,i] == 8:
                    sabah_calisma = sabah_calisma + 1
                if nsp_tablo[p,j,i] == 16:
                    akşam_calisma = akşam_calisma + 2
            
            hastabakim_sabah = sabah_calisma*4.64
            hastabakim_akşam = akşam_calisma*4.64

            ceza_hsb = abs(kd_sabah - hastabakim_sabah)
            ceza_hba = abs(kd_akşam - hastabakim_akşam)

            ceza = ceza + ceza_hsb + ceza_hba


        ceza_tablo[p] = ceza

    return ceza_tablo

#%% doğal seçilim için rulet tekerleği kullanıcak

def doğal_seçilim(nsp_tablo,ceza_tablo):
    o_tablo = 1/ceza_tablo
    obj_toplam = o_tablo.sum()

    for i in range(0,populasyon):
        o_tablo[i] = o_tablo[i]/obj_toplam
    
    cum = np.cumsum(o_tablo)

    for i in range(0,populasyon):
        rs = np.random.rand(populasyon)
        ara_populasyon =nsp_tablo.copy()

    for p in range(0,populasyon):
        idx =len(cum[np.where(cum <= rs[p])])
        ara_populasyon[p] = nsp_tablo[idx]

    return ara_populasyon
#%% iki nokta çaprazlama

def caprazla(ara_populasyon):
    arapop = ara_populasyon.copy()
    cp=0.95
    sirala =np.random.permutation(populasyon)

    for i in range(0,int(populasyon/2)):
        id1= sirala[2*i]
        id2= sirala[2*i+1]

        ata1 = arapop[id1]
        ata2 = arapop[id2]

        if np.random.rand() < cp:
            cpz_noktasi1=np.random.randint(1,gün_sayisi-1)
            cpz_noktasi2=np.random.randint(cpz_noktasi1,gün_sayisi-1)

            ata1[:,cpz_noktasi1:cpz_noktasi2],ata2[:,cpz_noktasi1:cpz_noktasi2] = ata2[:,cpz_noktasi1:cpz_noktasi2].copy(),ata1[:,cpz_noktasi1:cpz_noktasi2].copy()
            
            arapop[id1] = ata1
        arapop[id2] = ata2

    return arapop

#%% mutasyon işlemleri

def mutasyon(ara_populasyon):
    mts_orani = 0.05
    arapop = ara_populasyon.copy()
    rnd = np.random.rand(populasyon,hemşire_sayisi,gün_sayisi)

    for p in range(0,populasyon):
        for i in range(0,hemşire_sayisi):
            for j in range(0,gün_sayisi):
                if rnd[p,i,j] < mts_orani:
                    rs =np.random.randint(0,3)
                    arapop[p,i,j] = 0
                    if rs == 0:
                        arapop[p,i,j] = 0
                    if rs == 1:
                        arapop[p,i,j] = 8
                    else:
                        arapop[p,i,j] = 16

    return arapop


#%%
eniyideger = 1000000
iter=0

iter_max = 100
iter_durum = np.zeros(iter_max)

while iter < iter_max:
    nsp_tablo = gece_vardiyasi(nsp_tablo)
    nsp_tablo = toplam_calisma(nsp_tablo)
    ceza_tablo = ceza_hesapla(nsp_tablo)

    if ceza_tablo.min() < eniyideger:
        eniyideger = ceza_tablo.min()
        eniyicozum = nsp_tablo[ceza_tablo.argmin()]
    

    ara_populasyon = doğal_seçilim(nsp_tablo,ceza_tablo)
    ara_populasyon = caprazla(ara_populasyon)
    nsp_tablo = mutasyon(ara_populasyon)

    iter_durum[iter] = eniyideger

    iter += 1
    
plt.plot(iter_durum)
plt.show()

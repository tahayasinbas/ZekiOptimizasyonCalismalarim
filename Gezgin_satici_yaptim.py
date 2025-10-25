import numpy as np
import random as rd
import matplotlib.pyplot as plt

def Maaliyet_Tablosu_Olustur(Boyut):
    Maliyet_Tablo=np.random.randint(0,100,(Boyut,Boyut))
    for i in range(Boyut):
        for j in range(Boyut):
            if i == j:
                Maliyet_Tablo[i][j] = 0
            else:
                Maliyet_Tablo[i][j] = Maliyet_Tablo[j][i]
    return Maliyet_Tablo
def Rota_Hesapla(Mevcut_Rota,Maliyet_Tablo):
    Rota_Maaliyeti = 0
    for i in range((len(Mevcut_Rota)-1)):
        x,y=Mevcut_Rota[i],Mevcut_Rota[i+1]
        Rota_Maaliyeti+=Maliyet_Tablo[x][y]
    return Rota_Maaliyeti    
    
def Tavlama_Benzetimi(Maliyet_Tablo,Tson,Tilk,Sogutma_Katsayisi):
    Boyut = len(Maliyet_Tablo)
    rota = [*range(Boyut)]
    Mevcut_Rota=rd.sample(rota,Boyut)
    MevcutRotaMaaliyeti=Rota_Hesapla(Mevcut_Rota, Maliyet_Tablo)
    Eniyirota = Mevcut_Rota
    Eniyimaliyet = MevcutRotaMaaliyeti
    Maliyetler = []
    Sicaklik = Tilk
    iterasyon = 0
    while(Sicaklik > Tson):  
        iterasyon+=1
        Yeni_Rota = Mevcut_Rota[:]
        x,y = np.random.randint(0,len(rota),size = 2) 
        Yeni_Rota[x],Yeni_Rota[y] = Yeni_Rota[y],Yeni_Rota[x]
        Yeni_Maaliyet=Rota_Hesapla(Yeni_Rota, Maliyet_Tablo)
        if Yeni_Maaliyet < MevcutRotaMaaliyeti or np.random.rand() < np.exp((Yeni_Maaliyet-MevcutRotaMaaliyeti)/Sicaklik):
            Mevcut_Rota = Yeni_Rota[:]
            MevcutRotaMaaliyeti = Yeni_Maaliyet
            if Eniyimaliyet > MevcutRotaMaaliyeti:
                Eniyirota = Mevcut_Rota
                Eniyimaliyet = MevcutRotaMaaliyeti
                Maliyetler.append(Eniyimaliyet)
            Sicaklik=Sicaklik*Sogutma_Katsayisi
    return Eniyirota,Eniyimaliyet,Maliyetler,iterasyon
def grafikçiz(Maliyetler,iterasyon):
    plt.figure(figsize=(10, 6))  # Daha büyük bir grafik alanı
    plt.plot(Maliyetler, color="b", linestyle="--", marker="o")  # Çizgi stili ve marker ekleniyor
    
    
def main():
        Maliyet_Tablo=Maaliyet_Tablosu_Olustur(10)
        Eniyirota,Eniyimaliyet,Maliyetler,iterasyon=Tavlama_Benzetimi(Maliyet_Tablo, 10, 10000, 0.99)
        print(Eniyirota,Eniyimaliyet,Maliyetler)
        grafikçiz(Maliyetler, iterasyon)
if __name__ == "__main__":
    main()
        
        
    
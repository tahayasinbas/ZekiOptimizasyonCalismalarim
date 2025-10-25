import random as rd
import numpy as np
class Job:
    def __init__(self,Job_id,Isleme_Zamani,Is_Oncelik):
        self.Job_id = Job_id
        self.Isleme_Zamani = Isleme_Zamani
        self.Is_Oncelik = Is_Oncelik
    def __repr__(self):
        return f"Job({self.Job_id}, {self.Isleme_Zamani}, {self.Is_Oncelik})"

def Baslangic_Cozum_Uret(Jobs):
    return rd.sample(Jobs,len(Jobs))
def AgirlikliGecikmeHesapla(Baslangic_Cozum):
    Toplam_Gecikme=0
    Mevcut_Sure=0
    for i in Baslangic_Cozum:
        Mevcut_Sure+=i.Isleme_Zamani
        delay=max(0,Mevcut_Sure-i.Isleme_Zamani)
        Agirlikli_Gecikme = delay * i.Is_Oncelik
        Toplam_Gecikme += Agirlikli_Gecikme
    return Toplam_Gecikme
def Komsu_Cozumler_Uret(Baslangic_Cozum):
    Komsular_Listesi = []
    for j in range(len(Baslangic_Cozum)):
        for i in range(j+1,len(Baslangic_Cozum)):
                Komsu_Cozum = Baslangic_Cozum[:]
                Komsu_Cozum[j],Komsu_Cozum[i]= Komsu_Cozum[i],Komsu_Cozum[j]
                Komsular_Listesi.append(Komsu_Cozum)
    return Komsular_Listesi
                
def Tabu_Algoritmasi(Jobs,Max_Iterasyon,Tabu_Uzunluk):
    Tabu_List = []
    Baslangic_Cozum = Baslangic_Cozum_Uret(Jobs)
    Mevcut_sonuc = AgirlikliGecikmeHesapla(Baslangic_Cozum)    
    Komsular_Listesi=Komsu_Cozumler_Uret(Baslangic_Cozum)
    Eniyicozum = Baslangic_Cozum
    Eniyisonuc = Mevcut_sonuc
    for i in range(Max_Iterasyon):
        Eniyikomsudeger = 100000
        Komsular_Listesi=Komsu_Cozumler_Uret(Eniyicozum)
        for Komsu in Komsular_Listesi:
            Komsu_Sonuc=AgirlikliGecikmeHesapla(Komsu)
            if Komsu_Sonuc < Eniyikomsudeger:
                Eniyikomsucozum = []
                Eniyikomsudeger = Komsu_Sonuc
                Eniyikomsucozum = Komsu
        if Eniyikomsucozum not in Tabu_List and Eniyikomsudeger < Eniyisonuc:
            Eniyicozum = Eniyikomsucozum
            Eniyisonuc =Eniyikomsudeger
            if len(Tabu_List) > Tabu_Uzunluk:
                Tabu_List.pop(0)
                Tabu_List.append(Eniyicozum)
    return Eniyicozum,Eniyisonuc









def main():
    Jobs = [Job(1, 2,3),
            Job(2, 1,3),
            Job(3, 2,1),
            Job(4, 4,4),
            Job(5, 5,5)]
    Max_Iterasyon = 50
    Tabu_Uzunluk = 3
    Eniyicozum,Eniyideger=Tabu_Algoritmasi(Jobs, Max_Iterasyon, Tabu_Uzunluk)
    print(Eniyicozum,Eniyideger)

if __name__ == "__main__":
    main()
        
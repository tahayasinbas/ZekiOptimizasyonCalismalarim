import numpy as np
import random

class job:
    def __init__(self, makine_id, makine_suresi, is_oncelik):
        self.makine_id = makine_id
        self.makine_suresi = makine_suresi
        self.is_oncelik = is_oncelik
    
    def __repr__(self):
        return f"{self.makine_id},{self.makine_suresi},{self.is_oncelik}"

def Baslangic_populasyonu_olustur(job_listesi):
    Job_listeleri = []
    for _ in range(10):       
        # Kopya liste üzerinde shuffle yaparak orijinal listeyi koruyoruz
        temp_list = job_listesi.copy()
        random.shuffle(temp_list)  # numpy.random.shuffle yerine random.shuffle kullan
        Job_listeleri.append(temp_list)
    return Job_listeleri

def Gecikme_puani_hesapla(job_listesi):
    Toplam_makine_suresi = 0
    Gecikme_puani = 0
    for is_emri in job_listesi:
        Toplam_makine_suresi += is_emri.makine_suresi
        delay = max(0, Toplam_makine_suresi - is_emri.makine_suresi)
        Gecikme_puani += delay * is_emri.is_oncelik
    return Gecikme_puani
              
def Uyum_degeri_hesapla(Job_listeleri):
    Toplam_gecikme_puani = 0
    Uyum_degeri = []
    
    # Her bir iş listesi için gecikme puanını hesapla
    for is_listesi in Job_listeleri:
        Gecikme_puani = Gecikme_puani_hesapla(is_listesi)
        # Gecikme puanının tersi alınarak uyum değeri hesaplanır
        Uyum_degeri.append(1 / (Gecikme_puani + 1))  # +1 sıfıra bölünmeyi önler
    
    # Normalize edilmiş uyum değerleri
    Toplam_uyum = sum(Uyum_degeri)
    Kromozom_Uyumluluk = [uyum / Toplam_uyum for uyum in Uyum_degeri]
    
    return Kromozom_Uyumluluk

def Kromozom_sec(Kromozom_Uyumluluk, Job_listeleri):
    # Uyumluluk olasılıklarına göre kromozom seçimi
    Kromozom_secimi = random.choices(
        Job_listeleri, 
        weights=Kromozom_Uyumluluk, 
        k=len(Job_listeleri)
    )
    return Kromozom_secimi

def Kromozom_Caprazlama(Kromozom_secimi):
    # İlk yarı ve ikinci yarıyı değiştirme
    for i in range(len(Kromozom_secimi)):
        if len(Kromozom_secimi[i]) > 5:
            Kromozom_secimi[i][:5], Kromozom_secimi[i][5:] = \
            Kromozom_secimi[i][5:], Kromozom_secimi[i][:5]
    return Kromozom_secimi

def Kromozom_mutasyon(Kromozom_secimi):
    mutasyon_orani = 0.6
    for i in range(len(Kromozom_secimi)):
        if random.random() < mutasyon_orani:
            # Rastgele iki pozisyonu değiştir
            mutation_index1 = random.randint(0, len(Kromozom_secimi[i])-1)
            mutation_index2 = random.randint(0, len(Kromozom_secimi[i])-1)
            Kromozom_secimi[i][mutation_index1], Kromozom_secimi[i][mutation_index2] = \
            Kromozom_secimi[i][mutation_index2], Kromozom_secimi[i][mutation_index1]
    return Kromozom_secimi

def main():
    # İş listesini oluştur
    job_listesi = [
        job(i, random.randint(1,10), random.randint(1,10)) 
        for i in range(10)
    ]
    
    # En iyi sonucu takip etmek için değişkenler
    en_iyi_sonuc = None
    en_dusuk_gecikme = float('inf')
    
    # Genetik algoritma iterasyonları
    for iterasyon in range(100):
        # Başlangıç popülasyonu oluştur
        Job_listeleri = Baslangic_populasyonu_olustur(job_listesi)
        
        # Uyum değerlerini hesapla
        Kromozom_Uyumluluk = Uyum_degeri_hesapla(Job_listeleri)
        
        # Kromozom seçimi
        Kromozom_secimi = Kromozom_sec(Kromozom_Uyumluluk, Job_listeleri)
        
        # Çaprazlama
        Kromozom_secimi = Kromozom_Caprazlama(Kromozom_secimi)
        
        # Mutasyon
        Kromozom_secimi = Kromozom_mutasyon(Kromozom_secimi)
        
        # En iyi sonucu bul
        for is_listesi in Kromozom_secimi:
            gecikme_puani = Gecikme_puani_hesapla(is_listesi)
            if gecikme_puani < en_dusuk_gecikme:
                en_dusuk_gecikme = gecikme_puani
                en_iyi_sonuc = is_listesi
        
        # Her iterasyonda en iyi sonucu yazdır
        print(f"İterasyon {iterasyon + 1}: En düşük gecikme puanı = {en_dusuk_gecikme}")
    
    # Son en iyi sonucu yazdır
    print("\nEn İyi Sonuç:")
    for is_emri in en_iyi_sonuc:
        print(is_emri)
    print(f"En düşük gecikme puanı: {en_dusuk_gecikme}")

# Programı çalıştır
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    

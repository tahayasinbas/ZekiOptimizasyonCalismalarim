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
        temp_list = job_listesi[:]
        np.random.shuffle(temp_list)
        Job_listeleri.append(temp_list)
    return Job_listeleri

def Gecikme_puani_hesapla(job_listesi):
    Toplam_makine_suresi = 0
    Gecikme_puani = 0
    for job in job_listesi:
        Toplam_makine_suresi += job.makine_suresi
        delay = max(0, Toplam_makine_suresi - job.makine_suresi)
        Gecikme_puani += delay * job.is_oncelik
    return Gecikme_puani

def Uyum_degeri_hesapla(Job_listeleri):
    Uyum_degeri = []
    for job_listesi in Job_listeleri:
        gecikme_puani = Gecikme_puani_hesapla(job_listesi)
        if gecikme_puani > 0:
            Uyum_degeri.append(1 / gecikme_puani)
        else:
            Uyum_degeri.append(float('inf'))
    toplam_uyum = sum(Uyum_degeri)
    return [uyum / toplam_uyum for uyum in Uyum_degeri]

def Kromozom_sec(Kromozom_Uyumluluk, Job_listeleri):
    return list(np.random.choice(Job_listeleri, size=len(Job_listeleri), replace=True, p=Kromozom_Uyumluluk))

def Kromozom_Caprazlama(Kromozom_secimi):
    yeni_kromozomlar = []
    for i in range(0, len(Kromozom_secimi), 2):
        if i + 1 < len(Kromozom_secimi):
            parent1 = Kromozom_secimi[i]
            parent2 = Kromozom_secimi[i + 1]
            kesme_noktasi = random.randint(1, len(parent1) - 1)
            child1 = parent1[:kesme_noktasi] + [job for job in parent2 if job not in parent1[:kesme_noktasi]]
            child2 = parent2[:kesme_noktasi] + [job for job in parent1 if job not in parent2[:kesme_noktasi]]
            yeni_kromozomlar.extend([child1, child2])
        else:
            yeni_kromozomlar.append(Kromozom_secimi[i])
    return yeni_kromozomlar

def Kromozom_mutasyon(Kromozom_secimi):
    mutasyon_orani = 0.6
    for kromozom in Kromozom_secimi:
        if random.random() < mutasyon_orani:
            i, j = random.sample(range(len(kromozom)), 2)
            kromozom[i], kromozom[j] = kromozom[j], kromozom[i]
    return Kromozom_secimi

def main():
    # İş listesi oluşturuluyor
    job_listesi = [
        job(
            makine_id=i,
            makine_suresi=random.randint(1, 10),
            is_oncelik=random.randint(1, 10)
        )
        for i in range(10)
    ]

    # Parametreler
    toplam_iterasyon = 100
    mevcut_iterasyon = 0

    # Genetik algoritma döngüsü
    populasyon = Baslangic_populasyonu_olustur(job_listesi)
    while mevcut_iterasyon < toplam_iterasyon:
        mevcut_iterasyon += 1

        # Uyum değerleri hesaplanıyor
        uyum_degerleri = Uyum_degeri_hesapla(populasyon)

        # Kromozomlar seçiliyor
        secilen_kromozomlar = Kromozom_sec(uyum_degerleri, populasyon)

        # Çaprazlama uygulanıyor
        yeni_kromozomlar = Kromozom_Caprazlama(secilen_kromozomlar)

        # Mutasyon uygulanıyor
        mutasyona_ugramis_kromozomlar = Kromozom_mutasyon(yeni_kromozomlar)

        # Mutasyona uğramış kromozomlar değerlendiriliyor ve iyi olanlar popülasyona ekleniyor
        mutasyona_ugramis_uyum_degerleri = Uyum_degeri_hesapla(mutasyona_ugramis_kromozomlar)
        for kromozom, uyum in zip(mutasyona_ugramis_kromozomlar, mutasyona_ugramis_uyum_degerleri):
            if uyum > min(uyum_degerleri):
                populasyon.append(kromozom)

        # Popülasyonu boyut sınırıyla güncelleme
        populasyon = sorted(populasyon, key=Gecikme_puani_hesapla)[:10]

    # Sonuçlar yazdırılıyor
    print("Son popülasyon:")
    for kromozom in populasyon:
        print(kromozom)

# Program çalıştırılıyor
main()

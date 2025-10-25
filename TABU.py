import random
import matplotlib.pyplot as plt
class Job:
    def __init__(self, job_id, isleme_zamani, is_oncelik):
        self.job_id = job_id
        self.isleme_zamani = isleme_zamani
        self.is_oncelik = is_oncelik

    def __repr__(self):
        return f"Job({self.job_id}, {self.isleme_zamani}, {self.is_oncelik})"

def baslangicCozumuUret(Jobs):
    return random.sample(Jobs, len(Jobs))

def agirlikiGecikmeHesapla(is_listesi):
    mevcut_sure = 0
    toplamAgirlikiGecikme = 0

    for job in is_listesi:
        mevcut_sure += job.isleme_zamani
        delay = max(0, (mevcut_sure - job.isleme_zamani))
        agirlikiGecikme = job.is_oncelik * delay
        toplamAgirlikiGecikme += agirlikiGecikme

    return toplamAgirlikiGecikme

def komsuCozumUret(is_listesi):
    komsular = []
    for i in range(len(is_listesi)):
        for j in range(i + 1, len(is_listesi)):
            komsu_cozum = is_listesi[:]
            komsu_cozum[i], komsu_cozum[j] = komsu_cozum[j], komsu_cozum[i]
            komsular.append(komsu_cozum)
            
    return komsular

def tabu_search(Jobs, max_iterasyon, tabu_uzunluk):
    eniyiCozum = baslangicCozumuUret(Jobs)
    eniyiDeger = agirlikiGecikmeHesapla(eniyiCozum)
    tabu_list = []
    mevcut_cozum = eniyiCozum[:]
    eniyiDegerListesi = []
    for iterasyon in range(max_iterasyon):
        komsu_cozumler = komsuCozumUret(mevcut_cozum)
        eniyikomsuCozum = None
        eniyikomsuDeger = float("inf")

        for komsu in komsu_cozumler:
            if komsu not in tabu_list:
                komsuCozumAG = agirlikiGecikmeHesapla(komsu)
                if komsuCozumAG < eniyikomsuDeger:
                    eniyikomsuDeger = komsuCozumAG
                    eniyikomsuCozum = komsu

        if eniyikomsuCozum is not None:
            mevcut_cozum = eniyikomsuCozum
            tabu_list.append(mevcut_cozum)

            if len(tabu_list) > tabu_uzunluk:
                tabu_list.pop(0)

            if eniyikomsuDeger < eniyiDeger:
                eniyiDeger = eniyikomsuDeger
                eniyiCozum = eniyikomsuCozum

        print(f"Iterasyon: {iterasyon + 1}\nEn iyi Değer: {eniyiDeger}\nEn iyi Çözüm: {eniyiCozum}\n")
        eniyiDegerListesi.append(eniyiDeger)
        plt.plot(eniyiDegerListesi)
    return eniyiCozum, eniyiDeger

def main():
    Jobs = [
        Job(job_id=1, isleme_zamani=3, is_oncelik=2),
        Job(job_id=2, isleme_zamani=1, is_oncelik=3),
        Job(job_id=3, isleme_zamani=2, is_oncelik=1),
        Job(job_id=4, isleme_zamani=4, is_oncelik=4),
        Job(job_id=5, isleme_zamani=5, is_oncelik=5),
    ]

    max_iterasyon = 100
    tabu_uzunluk = 5

    eniyiCozum, eniyiDeger = tabu_search(Jobs, max_iterasyon, tabu_uzunluk)
    print("\nSonuç:")
    print(f"En iyi Çözüm: {eniyiCozum}")
    print(f"En iyi Değer: {eniyiDeger}")
    
if __name__ == "__main__":
    main()

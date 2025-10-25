import numpy as np
import random
import matplotlib.pyplot as plt

# Parçacıkları üret
def parcacik_uret(n_parcacik=10, x_min=0, x_max=100, y_min=0, y_max=100):
    X_Listesi = [random.uniform(x_min, x_max) for _ in range(n_parcacik)]
    Y_Listesi = [random.uniform(y_min, y_max) for _ in range(n_parcacik)]
    Cozumler_Kumesi = [*zip(X_Listesi, Y_Listesi)]
    return Cozumler_Kumesi

# Parçacıkların fonksiyon değerlerini hesapla
def parcaciklari_hesapla(Cozumler_Kumesi):
    Sonuclar_Listesi = []
    for x, y in Cozumler_Kumesi:
        Sonuc = x**2 + 2 * y - x * y + y**2  # Fonksiyon
        Sonuclar_Listesi.append(Sonuc)
    CozumlerKumesiCevaplar = [*zip(Cozumler_Kumesi, Sonuclar_Listesi)]
    return CozumlerKumesiCevaplar

# Global ve kişisel en iyi konumları bul
def Konumlari_Bul(CozumlerKumesiCevaplar):
    P_Best = CozumlerKumesiCevaplar[:]  # Başlangıçta P_Best parçacıkların kendisi
    G_Best = min(CozumlerKumesiCevaplar, key=lambda x: x[1])  # En küçük fonksiyon değerine sahip olan
    return G_Best, P_Best

# Hızları hesapla
def Hizlari_Hesapla(Cozumler_Kumesi, Hiz_Listesi, P_Best, G_Best, C1, C2, W):
    Yeni_Hiz_Listesi = []
    for i, (x, y) in enumerate(Cozumler_Kumesi):
        P_x, P_y = P_Best[i][0]
        G_x, G_y = G_Best[0]

        # Hız güncelleme formülü
        Vx = (W * Hiz_Listesi[i][0] +
              C1 * random.random() * (P_x - x) +
              C2 * random.random() * (G_x - x))
        Vy = (W * Hiz_Listesi[i][1] +
              C1 * random.random() * (P_y - y) +
              C2 * random.random() * (G_y - y))

        Yeni_Hiz_Listesi.append((Vx, Vy))
    return Yeni_Hiz_Listesi

# Konumları hızlara göre güncelle
def Konumlari_Guncelle(Cozumler_Kumesi, Hiz_Listesi):
    Yeni_Konumlar = []
    for i, (x, y) in enumerate(Cozumler_Kumesi):
        Vx, Vy = Hiz_Listesi[i]
        Yeni_Konumlar.append((x + Vx, y + Vy))
    return Yeni_Konumlar

# PSO algoritmasının ana fonksiyonu
def main():
    # Parametreler
    n_parcacik = 20
    n_iterasyon = 100
    C1, C2 = 2, 2
    W = 0.5  # İnertial weight

    # Parçacıkları başlat
    Cozumler_Kumesi = parcacik_uret(n_parcacik)
    Hiz_Listesi = [(0, 0) for _ in range(n_parcacik)]  # Başlangıç hızları sıfır
    CozumlerKumesiCevaplar = parcaciklari_hesapla(Cozumler_Kumesi)
    G_Best, P_Best = Konumlari_Bul(CozumlerKumesiCevaplar)

    # Grafik için ayarlar
    plt.ion()
    fig, ax = plt.subplots()

    for iterasyon in range(n_iterasyon):
        # Hızları hesapla ve konumları güncelle
        Hiz_Listesi = Hizlari_Hesapla(Cozumler_Kumesi, Hiz_Listesi, P_Best, G_Best, C1, C2, W)
        Cozumler_Kumesi = Konumlari_Guncelle(Cozumler_Kumesi, Hiz_Listesi)

        # Yeni fonksiyon değerlerini hesapla
        CozumlerKumesiCevaplar = parcaciklari_hesapla(Cozumler_Kumesi)

        # Kişisel ve global en iyi konumları güncelle
        for i in range(len(P_Best)):
            if CozumlerKumesiCevaplar[i][1] < P_Best[i][1]:
                P_Best[i] = CozumlerKumesiCevaplar[i]
        Yeni_G_Best = min(CozumlerKumesiCevaplar, key=lambda x: x[1])
        if Yeni_G_Best[1] < G_Best[1]:
            G_Best = Yeni_G_Best

        # Grafik çizimi
        ax.clear()
        x_degerleri = [cozum[0][0] for cozum in CozumlerKumesiCevaplar]
        y_degerleri = [cozum[0][1] for cozum in CozumlerKumesiCevaplar]
        ax.scatter(x_degerleri, y_degerleri, c='blue', label='Parçacıklar')
        ax.scatter(G_Best[0][0], G_Best[0][1], c='red', label='En İyi (G_Best)', marker='X')
        ax.set_title(f'İterasyon: {iterasyon+1}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend()
        plt.pause(0.1)  # 100ms bekleme

        print(f"İterasyon {iterasyon+1}: En iyi değer: {G_Best[1]}")

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()

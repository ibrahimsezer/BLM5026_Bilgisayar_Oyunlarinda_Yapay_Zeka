Assignment 1 – Basic TSP on Random Points

## Proje Amacı

Bu ödevin amacı, Gezgin Satıcı Problemi (Traveling Salesperson Problem - TSP) için temel bir grafik soyutlaması yapmak, rastgele bir örnek oluşturmak ve problemin çözümü için En Yakın Komşu (Nearest Neighbor) gibi basit bir sezgiseli uygulamaktır.

### Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki Python kütüphaneleri gereklidir:
```
pip install numpy networkx matplotlib
```

### Çalıştırma

Python script dosyasını (tsp_nearest_neighbor.py) çalıştırın:
```
cd homework_1
python tsp_nearest_neighbor.py
```

Terminal çıktısında tur sırasını ve maliyetini göreceksiniz.

Bir matplotlib penceresinde, rastgele noktalar ve sezgisel ile bulunan tur görselleştirilecektir.

### Uygulanan Yaklaşım ve Kriter Analizi

1. Rastgele Grafik Üretimi

| Kriter            | Açıklama            |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Doğru Grafik      | `networkx.complete_graph` ile tam grafik oluşturulmuştur. Kenar ağırlıkları, noktalar arasındaki Öklid mesafesi ile doğru şekilde atanmıştır.                                       |
| Parametreli       | Grafik boyutu (`NUM_POINTS`) ve koordinat sınırı (`max_coord`) fonksiyon parametreleri aracılığıyla ayarlanabilir.                                                                  |
| Tekrarlanabilirlik| Kodun başlangıcına `numpy.random.seed(42)` eklenerek, rastgele nokta üretimi tekrarlanabilir hale getirilmiş ve her çalıştırmada aynı grafik örneği garanti edilmiştir.              |

1. TSP Sezgiseli: En Yakın Komşu (Nearest Neighbor)

Yaklaşım: Bu, her adımda yerel olarak en iyi kararı (en kısa mesafeyi) vermeye çalışan açgözlü (greedy) bir sezgiseldir.

İşleyiş:

Tur, başlangıç düğümünden (0. düğüm) başlar.

Her adımda, mevcut düğümden henüz ziyaret edilmemiş düğümler arasında en kısa mesafedeki düğüm seçilir.

Tüm düğümler ziyaret edildikten sonra, turu kapatmak için son düğümden başlangıç düğümüne geri dönülür.

Verimlilik: Sezgisel, her düğümde geriye kalan düğümleri taradığı için $O(N^2)$ zaman karmaşıklığına sahiptir ve bu, basit bir sezgisel için verimli kabul edilir.

3. Görselleştirme

matplotlib kullanılarak net bir 2D görsel oluşturulmuştur.

Düğümler: Tüm noktalar mavi noktalarla, başlangıç noktası ise kırmızı yıldızla vurgulanmıştır. Her noktanın etiketi (indeksi) gösterilmiştir.

Tur: Tur, gri çizgilerle, turu kapatan son kenar ise netlik için yeşil renkte çizilmiştir.

Açıklık: Görselin başlığında ve eksen etiketinde kullanılan seed, tur sırası ve hesaplanan toplam maliyet açıkça belirtilmiştir.

### Kenar Sayısı Doğrulaması

Kullanılan $N=15$ düğümlü grafik, bir Tam Grafik (Complete Graph) olduğu için, toplam kenar sayısı ($E$) aşağıdaki formülle hesaplanır:

$$
E = \frac{N \times (N - 1)}{2}
$$

**Hesaplama:**

$N = 15$ için:

$$
E = \frac{15 \times (15 - 1)}{2} = \frac{15 \times 14}{2} = 105
$$

Bu sonuç, kod çıktısında belirtilen **105 kenar** sayısının doğruluğunu teyit etmektedir.

## Sonuçlar

### Seed 16
![Seed 16 TSP Nearest Neighbor Figure](https://github.com/ibrahimsezer/BLM5026_Bilgisayar_Oyunlarinda_Yapay_Zeka/raw/main/homework_1/seed16_tsp_nearest_neighbor_figure.png)

### Seed 42
![Seed 42 TSP Nearest Neighbor Figure](https://github.com/ibrahimsezer/BLM5026_Bilgisayar_Oyunlarinda_Yapay_Zeka/raw/main/homework_1/seed42_tsp_nearest_neighbor_figure.png)

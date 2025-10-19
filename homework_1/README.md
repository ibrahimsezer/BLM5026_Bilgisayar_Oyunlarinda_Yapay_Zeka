Assignment 1 – Basic TSP on Random Points

Proje Amacı

Bu ödevin amacı, Gezgin Satıcı Problemi (Traveling Salesperson Problem - TSP) için temel bir grafik soyutlaması yapmak, rastgele bir örnek oluşturmak ve problemin çözümü için En Yakın Komşu (Nearest Neighbor) gibi basit bir sezgiseli uygulamaktır.

Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki Python kütüphaneleri gereklidir:
```
pip install numpy networkx matplotlib
```

Çalıştırma

Python script dosyasını (tsp_nearest_neighbor.py) çalıştırın:
```
cd homework_1
python tsp_nearest_neighbor.py
```

Terminal çıktısında tur sırasını ve maliyetini göreceksiniz.

Bir matplotlib penceresinde, rastgele noktalar ve sezgisel ile bulunan tur görselleştirilecektir.

Uygulanan Yaklaşım ve Kriter Analizi

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

Açıklık: Görselin başlığında ve eksen etiketinde tur sırası ve hesaplanan toplam maliyet açıkça belirtilmiştir.
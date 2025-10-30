import osmnx as ox
import folium
import networkx as nx
import random
import numpy as np 

SEED = 30102025
random.seed(SEED)
np.random.seed(SEED)

# --- ÖDEV 1'DEN ALINAN ALGORİTMA ---
# Bu fonksiyon, kendisine verilen 'tam' bir grafikte
# en yakın komşu algoritmasını çalıştırır.
def nearest_neighbor_tsp(graph):
    """
    Nearest Neighbor (En Yakın Komşu) sezgiselini uygular.
    (Ödev 1'den direk alınmıştır)
    """
    nodes = list(graph.nodes()) #node'ları bir listeye alıyoruz
    start_node = nodes[0]  #başlangıç node'unu belirliyoruz

    tour = [start_node] #tur listesi oluşturuyoruz
    visited = {start_node} #ziyaret edilen düğümleri tutan kümeyi tanımlıyoruz
    current_node = start_node #şu anki düğümü başlangıç düğümü olarak ayarlıyoruz
    total_cost = 0 #toplam maliyeti tanımlıyoruz

    # Tüm düğümleri ziyaret edene kadar döngü
    while len(visited) < len(nodes):
        min_dist = float('inf') #başlangıçta minimum mesafeyii sonsuz olarak ayarlıyoruz
        next_node = None

        for neighbor in nodes:
            if neighbor not in visited:
                # ÖNEMLİ: Burası 'graph.edges' kullandığı için, 
                # bu fonksiyona vereceğimiz grafiğin 'tam' (complete)
                # ve kenar ağırlıklarının 'weight' olarak ayarlanmış
                # olması GEREKİR.
                dist = graph.edges[current_node, neighbor]['weight'] #mevcut düğümden komşuya olan mesafe
                
                if dist < min_dist: #eğer bu mesafe minimum mesafeden küçükse yer değiştiriyoruz
                    min_dist = dist
                    next_node = neighbor #komşuyu sonraki düğüm olarak seciyoruz
        
        if next_node is not None:
            tour.append(next_node)
            visited.add(next_node)
            total_cost += min_dist
            current_node = next_node
        else:
            # Gidilecek komşu kalmadıysa (normalde olmamalı)
            break

    if len(tour) == len(nodes):
        # Son düğümden başlangıç düğümüne olan mesafeyi ekle
        last_to_first_cost = graph.edges[current_node, start_node]['weight'] 
        tour.append(start_node)
        total_cost += last_to_first_cost
    
    return tour, total_cost



# --- Real Map TSP KODU BAŞLANGICI ---

def solve_real_map_tsp():
    
    # -----------------------------------------------------------------
    # BÖLÜM 1: HARİTA VERİ İŞLEME (osmnx)
    # -----------------------------------------------------------------
    print("Bölüm 1: Harita verisi 'osmnx' ile alınıyor...")
    
    # Birden fazla bölgeyi birleştiriyoruz
    places = ["Nilüfer, Bursa, Turkey", "Osmangazi, Bursa, Turkey"]
    
    # 'drive' ağı (araç yolları) indiriliyor
    G = ox.graph_from_place(places, network_type='drive')
    
    # Mesafe hesaplamaları (metre) için grafiği UTM'ye dönüştür
    G_proj = ox.project_graph(G)
    
    # Görselleştirme (enlem/boylam) için WGS84 formatında bir kopya tut
    G_map = ox.project_graph(G, to_crs='epsg:4326')
    
    print(f"Grafik {G.number_of_nodes()} düğüm ve {G.number_of_edges()} kenar ile alındı.")

    # TSP için 10 adet rastgele durak (düğüm) seç
    NUM_POINTS = 10
    all_nodes = list(G_proj.nodes())
    tsp_nodes = random.sample(all_nodes, NUM_POINTS)
    
    print(f"{NUM_POINTS} adet rastgele durak (düğüm) seçildi.")

    # -----------------------------------------------------------------
    # BÖLÜM 2: SEZGİSEL İLE ENTEGRASYON
    # "Sezgisel yöntemi gerçek harita düğümlerine doğru uygulamak"
    # -----------------------------------------------------------------
    print("Bölüm 2: Gerçek yol mesafeleri hesaplanıyor...")

    # Ödev 1'deki 'nearest_neighbor_tsp' fonksiyonu TAM bir grafik bekler.
    # Bu nedenle, sadece 10 durağımızı içeren YENİ bir tam grafik oluşturacağız.
    # Bu yeni grafiğin kenar ağırlıkları, duraklar arasındaki GERÇEK YOL mesafeleri olacak.
    
    tsp_graph = nx.Graph()
    
    for i, u in enumerate(tsp_nodes):
        for j, v in enumerate(tsp_nodes[i+1:]):
            try:
                # 'G_proj' (büyük harita) üzerinde 'u' ve 'v' arasındaki
                # en kısa yolun mesafesini (metre) hesapla
                length = nx.shortest_path_length(G_proj, source=u, target=v, weight='length')
                
                # Bu mesafeyi 'tsp_graph' (küçük, tam grafiğimiz) üzerine
                # 'weight' olarak ekle.
                tsp_graph.add_edge(u, v, weight=length)
                
            except nx.NetworkXNoPath:
                # İki düğüm arasında yol yoksa (örn. adalar)
                print(f"Uyarı: {u} ve {v} arasında yol bulunamadı.")
                tsp_graph.add_edge(u, v, weight=float('inf'))

    print("Mesafe matrisi (TSP grafiği) oluşturuldu. Ödev 1'deki sezgisel yöntem çalıştırılıyor...")
    
    # Şimdi Ödev 1'den aldığımız fonksiyonu çağırabiliriz.
    # Çünkü 'tsp_graph' tam bir grafiktir ve 'weight' etiketli kenarları vardır.
    tsp_tour_nodes, tour_cost_meters = nearest_neighbor_tsp(tsp_graph)
    
    # -----------------------------------------------------------------
    # BÖLÜM 3: GÖRSELLEŞTİRME (folium)
    # "İnteraktif harita görselleştirmesi"
    # ÇÖZÜM: 'folium.PolyLine' kullanarak rotayı manuel çizme
    # -----------------------------------------------------------------
    print("Bölüm 3: Sonuçlar 'folium' ile interaktif haritaya çizdiriliyor...")

    # Haritanın merkezini ilk durağa ayarla
    start_node_data = G_map.nodes[tsp_tour_nodes[0]]
    map_center = [start_node_data['y'], start_node_data['x']]
    
    m = folium.Map(location=map_center, zoom_start=13, tiles="cartodbdarkmatter")

    # 1. Durakları haritada Kırmızı Noktalar olarak işaretle 
    for node_id in tsp_nodes:
        node_data = G_map.nodes[node_id]
        folium.CircleMarker(
            location=[node_data['y'], node_data['x']],
            radius=5,
            color='red',
            fill=True,
            fill_color='red',
            popup=f"Durak ID: {node_id}"
        ).add_to(m)

    # 2.GERÇEK ROTALARI 'folium.PolyLine' ile çizdir
    
    for i in range(len(tsp_tour_nodes) - 1):
        u = tsp_tour_nodes[i]
        v = tsp_tour_nodes[i+1]
        
        # Rotayı metrik (UTM) grafiği olan 'G_proj' üzerinde hesapla
        # Bu bize [node_id_A, node_id_B, ..., node_id_C] listesini verir
        route_nodes = nx.shortest_path(G_proj, source=u, target=v, weight='length')
        
        # Şimdi bu 'route_nodes' listesini koordinat listesine çevireceğiz
        # folium.PolyLine, [ (lat, lon), (lat, lon), ... ] formatında bir liste bekler
        
        route_coords = []
        for node_id in route_nodes:
            # 'G_map' (enlem/boylam) grafiğinden koordinatları al
            lat = G_map.nodes[node_id]['y']
            lon = G_map.nodes[node_id]['x']
            route_coords.append( (lat, lon) )
            
        # 'folium.PolyLine' fonksiyonunu kullan
        folium.PolyLine(
            locations=route_coords,
            color='cyan',
            weight=3,
            opacity=0.7
        ).add_to(m)

    # Haritayı HTML olarak kaydet
    output_file = "tsp_bursa_map.html"
    m.save(output_file)

    # -----------------------------------------------------------------
    # BÖLÜM 4: DOKÜMANTASYON
    # -----------------------------------------------------------------
    print("\n" + "="*40)
    print("  ÖDEV 2: REAL MAP TSP (GERÇEK HARİTA TSP SONUÇLARI)")
    print("="*40)
    print(f"Harita Verisi: Bursa, {', '.join(places)}")
    print(f"Seçilen Durak Sayısı: {NUM_POINTS}")
    print(f"Kullanılan Sezgisel Yöntem: En Yakın Komşu (Nearest Neighbor)")
    print("-" * 40)
    print(f"Bulunan Tur (Düğüm ID Sırası):\n{tsp_tour_nodes}")
    print(f"Toplam Rota Maliyeti: {tour_cost_meters / 1000:.2f} km")
    print("-" * 40)
    print(f"BAŞARILI: İnteraktif harita '{output_file}' dosyasına kaydedildi.")
    print("Lütfen bu HTML dosyasını açarak sonucu inceleyin.")
    print("="*40)


# Ana fonksiyonu çalıştır
if __name__ == "__main__":
    solve_real_map_tsp()
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Tohum sabiti
SEED = 16 
np.random.seed(SEED)

def generate_tsp_instance(num_points, max_coord=100):
    """
    Rastgele noktalar üretir ve tam grafik oluşturur.
    """
    points = {
        i: (np.random.uniform(0, max_coord), np.random.uniform(0, max_coord)) # rastgele x,y koordinatları
        for i in range(num_points) # verilen num_points sayısı kadar nokta 
    }

    G = nx.complete_graph(num_points)

    for i in range(num_points):
        for j in range(i + 1, num_points):
            dist = np.linalg.norm(np.array(points[i]) - np.array(points[j]))
            G.edges[i, j]['weight'] = dist
            
    return G, points

NUM_POINTS = 15
graph, coordinates = generate_tsp_instance(NUM_POINTS)

print(f"Grafik {graph.number_of_nodes()} düğüm ve {graph.number_of_edges()} kenar içeriyor.")


def nearest_neighbor_tsp(graph):
    """
    Nearest Neighbor (En Yakın Komşu) sezgiselini uygular.
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
            break

    if len(tour) == len(nodes):
        last_to_first_cost = graph.edges[current_node, start_node]['weight'] #son düğümden başlangıç düğümüne olan mesafe hesabi
        tour.append(start_node)
        total_cost += last_to_first_cost
    
    return tour, total_cost

tsp_tour, tour_cost = nearest_neighbor_tsp(graph)


# Terminal sonuçları 
print("-" * 30)
print("TSP Sezgisel Sonuçları:")
print(f"Tur (Düğüm Sırası): {tsp_tour}")
print(f"Tur Maliyeti (Toplam Uzunluk): {tour_cost:.2f}")
print("-" * 30)


def visualize_tsp_tour(coordinates, tour, title="TSP Tour by Nearest Neighbor Heuristic"):
    """
    Noktaları ve bulunan turu görselleştirir.
    """
    plt.figure(figsize=(10, 8))
    
    x_coords = [coord[0] for coord in coordinates.values()]
    y_coords = [coord[1] for coord in coordinates.values()]
    
    plt.scatter(x_coords, y_coords, c='blue', s=100, label='Noktalar')
    
    for i, (x, y) in coordinates.items():
        plt.annotate(str(i), (x + 1, y + 1), fontsize=10)

    start_node = tour[0]
    plt.scatter(coordinates[start_node][0], coordinates[start_node][1], c='red', s=150, marker='*', label='Başlangıç')

    for i in range(len(tour) - 1):
        n1 = tour[i]
        n2 = tour[i+1]
        
        x1, y1 = coordinates[n1]
        x2, y2 = coordinates[n2]
        
        color = 'green' if i == len(tour) - 2 else 'gray'
        linestyle = '-'
        linewidth = 2
        
        plt.plot([x1, x2], [y1, y2], color=color, linestyle=linestyle, linewidth=linewidth, alpha=0.7)

    plt.title(title)
    plt.xlabel(f"X Koordinatı | Seed: {SEED} \n Yol: {tsp_tour} | Toplam uzunluk: {tour_cost:.2f} ") #sonuçları plot ekranında yazdırma
    plt.ylabel("Y Koordinatı")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.show()

# Görselleştirme
visualize_tsp_tour(coordinates, tsp_tour)
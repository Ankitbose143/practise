import heapq

def dijkstra(graph, start):
    pq = [(0, start)]  # Min-heap storing (distance, node)
    print("gr", graph)
    print("pq", pq)
    distances = {node: float('inf') for node in graph}
    print("dis", distances)
    distances[start] = 0

    while pq:
        curr_dist, node = heapq.heappop(pq)
        print("curr_dist12", curr_dist,node, graph[node])
        for neighbor, weight in graph[node]:
            distance = curr_dist + weight
            print("dis12", distances, "-", neighbor,  '+', weight,'--',distances[neighbor])
            print("dis122s3", distances, "-",distance < distances[neighbor], '--',distances[neighbor])
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                print("dis123",  pq, distances, neighbor)
                heapq.heappush(pq, (distance, neighbor))
                print("heapq", heapq, pq)

    return distances

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 5)],
    'C': [('D', 1)],
    'D': []
}

print(dijkstra(graph, 'A'))

import heapq

# Creating a heap
h = [10, 20, 15, 30, 40]
heapq.heapify(h)

# Push a new element (5) and pop the smallest element at the same time
min = heapq.heappushpop(h, 35)

print(min)
print(h)

# heappop() is used to remove the smallest element
heapq.heappop(h)
print("h", h)


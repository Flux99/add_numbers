import heapq
from collections import defaultdict


def dijkstra(graph,start):
    heap = [(0,start)]

    dist = {node: float("inf") for node in graph}

    dist[start] = 0

    while heap:
        curr_dist , node = heapq.heappop(heap)
        if curr_dist > dist[node]:
            continue

        for nei , we in graph[node]:
            temp_dist = curr_dist + we
            if temp_dist < dist[nei]:
                dist[nei] = temp_dist
                heapq.heappush(heap,(temp_dist,nei))
    return dist 
    





graph = {
    'A': [('B', 2), ('C', 4)],
    'B': [('A', 2), ('C', 1), ('D', 7)],
    'C': [('A', 4), ('B', 1), ('E', 3)],
    'D': [('B', 7), ('E', 1)],
    'E': [('C', 3), ('D', 1)]
}

start_node = 'B'
distances = dijkstra(graph, start_node)

print(f"Shortest distances from {start_node}:")
for node in sorted(distances):
    print(f"{node} -> {distances[node]}")

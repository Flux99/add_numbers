import heapq
from collections import defaultdict


def prim(graph,start):
    v = set()
    count= 0
    min_heap = [(0, start)]

    while min_heap:
        cnt, node = heapq.heappop(min_heap)
        if node not in v:
            v.add(node)
            count += cnt
            for nei,wei in graph[node]:
                if nei not in v:
                    heapq.heappush(min_heap,(wei,nei))
    return count

graph = {
    'A': [('B', 1), ('D', 3)],
    'B': [('A', 1), ('D', 4), ('C', 2)],
    'C': [('B', 2), ('D', 5)],
    'D': [('A', 3), ('B', 4), ('C', 5)]
}

print("Prim's MST cost:", prim(graph, 'A'))

    
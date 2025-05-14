from collections import deque


def bfs(graph,start):
    visited = set()
    q = deque([start])
    res = []


    while q:
        node = q.popleft()
        if node not in visited:
            res.append(node)
            visited.add(node)
            for ni in graph[node]:
                if ni not in visited:
                    q.append(ni)
    return res
    


# Example usage
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print("BFS Traversal:", bfs(graph, 'A'))
# BFS Traversal: ['A', 'B', 'C', 'D', 'E', 'F']



from collections import deque


def bfs(graph,start):
    q = deque([start])
    v = set()
    res = []


    while q:
        node = q.popleft()

        if node not in v:
            v.add(node)
            res.append(node)
            for nei in graph[node]:
                q.append(nei)
                
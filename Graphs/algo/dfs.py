from collections import deque


def dfs(graph,start):
    v =set()
    s= [start]

    res = []

    while s:
        node = s.pop()
        if node not in v:
            v.add(node)
            res.append(node)
            for ni in graph[node]:
                if ni not in v:
                    s.append(ni)
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

print("DFS Traversal:", dfs(graph, 'A'))
# DFS Traversal: ['A', 'C', 'F', 'E', 'B', 'D']




from collections import deque


def dfs(graph,start):
    s = [start]
    v = set()
    res = []


    while s:
        node = s.pop()
        if node not in v:
            v.add(node)
            res.append(node)
            for nei in graph[node]:
                s.append(node)

    return res
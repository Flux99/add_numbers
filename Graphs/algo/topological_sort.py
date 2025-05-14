from collections import defaultdict

def build_adjacency_list(vertices, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    return graph

def topological_sort_dfs(vertices, graph):
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)

    for v in range(vertices):
        if v not in visited:
            dfs(v)

    return stack[::-1]

# Example usage
vertices = 6
edges = [
    (5, 0),
    (5, 2),
    (4, 0),
    (4, 1),
    (2, 3),
    (3, 1)
]

# vertices = 4
# edges = [
#     (0, 1),
#     (1, 2),
#     (2, 3),
#     (3, 1)  # This creates a cycle: 1 → 2 → 3 → 1
# ]

graph = build_adjacency_list(vertices, edges)

print("Topological Sort (DFS):", topological_sort_dfs(vertices, graph))




class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        

    def build_adjacency_list(vertices, edges):
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
        return graph

    def topological_sort_dfs(vertices, graph):
        visited = set()
        stack = []

        def dfs(node):
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(node)

        for v in range(vertices):
            if v not in visited:
                dfs(v)

        return stack[::-1]
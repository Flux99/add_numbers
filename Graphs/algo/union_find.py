
n = 10
par = [ i  for i in range(n)]

rank =[1] * n


def find(n):
    if n != par[n]:
        par[n] = find(par[n])
    return par[n]


def union(n1,n2):
    p1, p2 = find(n1), find(n2)
    if p1 == p2: return False

    if rank[p1] > rank[p2]:
        par[p2] = p1
        rank[p1] += rank[p2]
    else:
        par[p1] = p2
        rank[p2] += rank[p1]
    return True


# edges = [[0, 1], [1, 2], [2, 3], [1, 3], [4, 5]]
edges = [[0, 1], [1, 2], [2, 0]]  # This creates a cycle: 0-1-2-0

for n1,n2 in edges:
    if not union(n1,n2):
        print(f"Graph is connected at {n1} & {n2}")


























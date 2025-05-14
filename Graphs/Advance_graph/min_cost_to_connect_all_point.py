class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        N = len(points)
        adj = {i : [] for i in range(N)}
        for i in range(N):
            x1,x2 = points[i]
            for j in range(i+1,N):
                y1,y2 = points[j]
                dist = abs(x1-y1) + abs(x2- y2)
                adj[i].append([dist,j])
                adj[j].append([dist,i])
        cnt = 0
        minH= [[0,0]]
        v = set()

        while len(v) < N:
            count, node = heapq.heappop(minH)
            if node not in v:
                v.add(node)
                cnt += count
                for wei, nei in adj[node]:
                    if nei not in v:
                        heapq.heappush(minH,[wei,nei])
        return cnt


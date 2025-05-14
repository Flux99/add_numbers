import collections
import heapq


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        edges = collections.defaultdict(list)
        for u,v,w in times:
            edges[u].append((v,w))
        minh=[(0,k)]
        v = set()
        cnt = 0


        while minh:
            count , node = heapq.heappop(minh)
            if node in v:
                continue
            v.add(node)
            cnt = max(cnt,count)
            for nei, wei  in edges[node]:
                if nei not in v:
                    heapq.heappush(minh,(wei+count,nei))
        return cnt if len(v) == n else -1 

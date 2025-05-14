import heapq


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        N = len(grid)
        minh = [[grid[0][0],0,0]]
        v = set()
        direction = [[1,0],[0,1],[0,-1],[-1,0]]
        v.add((0,0))
        while minh:
            t , r,c = heapq.heappop(minh)
            if r == N-1 and c == N-1:
                return t
            for dr,dc in direction:
                row, col = dr+r, dc+c
                if row < 0 or row == N or col < 0 or col == N or (row,col) in v : continue
                v.add((row,col))
                heapq.heappush(minh,[max(t,grid[row][col]),row,col])
        
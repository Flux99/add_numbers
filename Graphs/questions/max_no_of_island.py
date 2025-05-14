class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        v = set()
        count =0
        rows , cols = len(grid),len(grid[0])
        def dfs(r,c,v):
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0:
                return 0
            if (r,v) in v:
                return 0
            v.add((r,c))
            side = 1
            side += dfs(r+1,c,v)
            side += dfs(r-1,c,v)
            side += dfs(r,c+1,v)
            side += dfs(r,c-1,v)
            return side
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    count = max(count,dfs(r,c,v))
        return count

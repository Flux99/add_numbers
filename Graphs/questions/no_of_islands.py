class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        

        rows, cols = len(grid),len(grid[0])
        v= set()
        def dfs(r,c,v):
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == "0": return False

            if (r,c) in v: return False
            v.add((r,c))
            dfs(r+1,c,v)
            dfs(r-1,c,v)
            dfs(r,c+1,v)
            dfs(r,c-1,v)
            return True
        
        count = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    if dfs(r,c,v):
                        count+=1
        return count
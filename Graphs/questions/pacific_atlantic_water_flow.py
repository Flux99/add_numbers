class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        ROWS, COLS = len(heights),len(heights[0])

        pac = set()
        atl = set()
        def dfs(r,c,v,prev):
            if (0 > r or r == ROWS or 0 > c or c== COLS or (r,c) in v): return 
            if heights[r][c] < prev: return
            v.add((r,c))
            dfs(r+1,c,v,heights[r][c])
            dfs(r-1,c,v,heights[r][c])
            dfs(r,c+1,v,heights[r][c])
            dfs(r,c-1,v,heights[r][c])
        
        for c in range(COLS):
            dfs(0,c,pac,heights[0][c])
            dfs(ROWS-1,c,atl,heights[ROWS-1][c])
        
        for r in range(ROWS):
            dfs(r,0,pac,heights[r][0])
            dfs(r,COLS-1,atl,heights[r][COLS-1])

        res = []
        for m in range(ROWS):
            for n in range(COLS):
                if (m,n) in pac and (m,n) in atl:
                    res.append([m,n])
        return res

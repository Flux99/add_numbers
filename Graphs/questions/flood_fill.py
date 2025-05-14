def floodFill_DFS(image, sr, sc, newColor):
    if image[sr][sc] == newColor:
        return image
    og_color = image[sr][sc]

    rows, cols = len(image)-1, len(image[0])-1
    def dfs(r,c):
        if 0 <=r <= rows and 0 <= c <= cols and image[r][c] == og_color:
            image[r][c] = newColor
            dfs(r+1,c)
            dfs(r-1,c)
            dfs(r,c+1)
            dfs(r,c-1)
    dfs(sr,sc)
    return image



image = [[1,1,1],[1,1,0],[1,0,1]]
sr = 1
sc = 1
newColor = 2

print(f"floodFill_DFS:{floodFill_DFS(image,1,1,2)}")
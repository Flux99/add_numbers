from collections import deque
class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """


        rows , cols = len(rooms), len(rooms[0])
        v = set()
        q = deque([])
        def dfs(r,c):
            if r < 0 or r >= rows or c < 0 or c >= cols or rooms[r][c] == -1: return
            if (r,c) in v: return
            v.add((r,c))
            q.append([r,c])

        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    v.add((r,c))
                    q.append([r,c])



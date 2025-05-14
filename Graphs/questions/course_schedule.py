class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        premap = {i:[] for i in range(numCourses)}
        for crs,pre in prerequisites:
            premap[crs].append(pre)

        v = set()

        def dfs(crs):
            if crs in v:
                return False
            if premap[crs] == []:
                return True
            
            v.add(crs)
            for cr in premap[crs]:
                if not dfs(cr): return False
            v.remove(crs)
            premap[crs]= []
            return True
        
        for nei in range(numCourses):
            if not dfs(nei): return False
        return True
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        prereq = {c:[] for c in range(numCourses)}
        for crs, pre in prerequisites:
            prereq[crs].append(pre)
        
        v , cy = set(),set()
        res = []
        def dfs(crs):
            if crs in cy:
                return False
            if crs in v:
                return True
            
            cy.add(crs)
            for pre in prereq[crs]:
                if not dfs(pre): return False
            cy.remove(crs)
            v.add(crs)
            res.append(crs)
            return True
        
        for cr in range(numCourses):
            if not dfs(cr): return []
        return res

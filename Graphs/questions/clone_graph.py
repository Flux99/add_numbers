from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        oldtonew = {}


        def dfs(node):
            if node in oldtonew: return oldtonew[node]
            newnode = Node(node.val)
            oldtonew[node] = newnode
            for ni in node.neighbors:
                oldtonew[node].neighbors.append(dfs(ni))
            return newnode
        if node:
            return dfs(node)
        else: return None
#Do a set of the elements and if a number is already present in the set, remove it and move the left pointer
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:

        if len(s) == 0:
            return 0

        memory = set()
        max_length, l = 0, 0

        for r in range(0, len(s)):
            while s[r] in memory:
                memory.remove(s[l])
                l += 1

            memory.add(s[r])
            max_length = max(max_length, r - l + 1)

        return max_length




class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        res=0
        l=0
        charSet = set()

        for r in range(len(s)):
            while s[r] in charSet:
                charSet.remove(s[l])
                l+=1
            charSet.add(s[r])
            res= max(res,r-l+1)
        return res





















class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        res = 0
        l= 0
        mem = set()

        for r in range(len(s)):
            while s[r] in mem:
                mem.remove(s[l])
                l+=1
            mem.add(s[r])
            res = max(res,r-l+1)
        return res

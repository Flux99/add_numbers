# use a sorting function to find the anagrams and add them to a dictionnary where the key is the sorted anagram and the val is the non sorted anagram.

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        dict_anagrams = {}
        for i in strs:
            t = ''.join(sorted(i))

            if t in dict_anagrams:
                dict_anagrams[t].append(i)

            else:
                dict_anagrams[t] = [i]

        return list(dict_anagrams.values())

class TimeMap:

    def __init__(self):
        self.store={}


    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = []
        self.store[key].append([value, timestamp])


    def get(self, key: str, timestamp: int) -> str:
        values= self.store.get(key,[])
        l,r = 0, len(values)-1
        res = ""

        while l <= r:
            m= (l+r)//2
            if values[m][1] <= timestamp:
                res= values[m][0]
                l=m+1
            else:
                r=m-1
        return res




# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)


from collections import OrderedDict


class TimeMap:

    def __init__(self):
        self.arr = {}


    def set(self, key: str, value: str, timestamp: int) -> None:
            if key not in self.arr:
                self.arr[key] = []
            self.arr[key].append((timestamp,value))


    def get(self, key: str, timestamp: int) -> str:
        values = self.arr.get(key,[])
        l,r = 0,len(values)-1
        res = ""
        while l <=r:
            m = (l+r)//2
            if values[m][0] <= timestamp:
                res = values[m][1]
                l = m+1
            else:
                r = m-1
        return res




# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)





class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l,r = 0, len(nums)-1


        while l <=r:
            m = (l+r)//2
            if nums[m] == target:
                return m

            if nums[l] <= nums[m]:
                    if nums[l] > target or target > nums[m]:
                        l = m+1
                    else:
                        r = m -1
            else:
                if nums[m] > target or target > nums[r]:
                    r = m-1
                else:
                    l = m+1
        return -1





















class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        res = len(piles)

        l, r = 1, max(piles)

        while l <= r:

            m = (l + r) // 2

            total_time = 0
            print(m, l, r)
            for pile in piles:
                total_time += (((pile - 1)//m) + 1)

            if total_time <= h:
                res = m
                r = m - 1
            else:
                l = m + 1

        return res

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:

        res = len(piles)
        l,r = 0, max(piles)

        while l <=r:
            m = (l+r)//2

            time_taken= 0
            for i in piles:
                time_taken += (((i-1)//m) +1)

            if time_taken <=h:
                res = m
                r = m-1
            else:
                l = m+1
        return res

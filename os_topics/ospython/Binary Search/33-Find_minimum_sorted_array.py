

# Basic binary search where we converge to the point of disrependcy.
# when l == r, we know that we reached the end goal.
class Solution:
    def findMin(self, nums: List[int]) -> int:

        l, r = 0, len(nums) - 1

        while l < r:
            m = (l + r) // 2
            if nums[m] > nums[r]:
                l = m + 1
            else:
                r = m
        return nums[l]

    def findMax(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1

        while l < r:
            m = (l + r) // 2
            # If the middle element is greater than the rightmost element,
            # the max must be on the left side (including middle).
            if nums[m] > nums[r]:
                l = m + 1
            else:
                r = m  # max could be nums[m], so don't exclude it
        return nums[l]  # at the end of the loop, l will point to the maximum

    # def findMax(self, nums: List[int]) -> int:
    #
    #     l, r = 0, len(nums) - 1
    #
    #     while l < r:
    #         m = (l + r) // 2
    #         if nums[m] > nums[r]:
    #             r = m
    #         else:
    #             l = m + 1
    #     return nums[r]



#Using the 2 pointer methodology:
# 1- init pointers
# 2 - update the value of the pointers depending on their value
# 3 - Update the value of k only when nums[l] > nums[r] since we want to know
#4 - where the rotation is happening and hence,when the breakage point is
def findMin(self, nums: List[int]) -> int:
    l, r = 0, len(nums) - 1
    k = 0

    while l < r:
        if nums[l] > nums[r]:
            k = r
            r -= 1
        else:
            l += 1

    return nums[k]

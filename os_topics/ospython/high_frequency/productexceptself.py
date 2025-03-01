class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1]* len(nums)
        first_pass = 1
        for i in range(len(nums)):
            res[i] = first_pass
            first_pass *= nums[i]


        second_pass = 1

        for j in range(len(nums)-1,-1,-1):
            res[j] *= second_pass
            second_pass *= nums[j]
        return res























class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1]* len(nums)

        first_pass = 1
        for i in range(len(nums)):
            res[i] = first_pass
            first_pass *= nums[i]

        second_pass = 1

        for j in range(len(nums)-1,-1,-1):
            res[j] *= second_pass
            second_pass *= nums[j]
        return res

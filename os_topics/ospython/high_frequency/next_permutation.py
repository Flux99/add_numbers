class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        ind1,ind2= -1,-1
        print(ind1,ind2)
        for i in range(len(nums)-2,-1,-1):
            if nums[i] < nums[i+1]:
                ind1= i
                break
        if ind1 == -1:
            #nums.reverse()
            nums =  self.reversearr(nums)
            return
        for j in range(len(nums)-1,ind1,-1):
            if nums[j] > nums[ind1]:
                ind2 = j
                break
        nums[ind1],nums[ind2] = nums[ind2],nums[ind1]

        nums[ind1+1:] = self.reversearr(nums[ind1+1:]) # reversed(nums[ind1+1:])

    def reversearr(self,nums:List[int])-> List[int]:

        l , r= 0, len(nums)-1

        while l < r:

            nums[l],nums[r] =nums[r],nums[l]
            l+=1
            r-=1
        return nums

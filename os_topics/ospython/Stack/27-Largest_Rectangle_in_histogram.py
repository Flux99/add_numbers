# Focuses on the principle of prolongation.

# in this case, we can extend heights until a point. B0nder@1313
# if the next height is inferior to the previous one, that means that we can extend the "Contained" rectangle within it.

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        maxArea = 0
        stack = [] # pair: (index, height)

        for i, h in enumerate(heights):
            start = i
            while stack and stack[-1][1] > h:
                index, height = stack.pop()
                maxArea = max(maxArea, height * (i - index))
                start = index
            stack.append((start, h))

        for i, h in stack:
            maxArea = max(maxArea, h * (len(heights) - i))
        return maxArea


# class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        leftmax,rightmax, res =[0] * len(heights), [0] * len(heights),[0] * len(heights)
        stack=[]

        for i in range(len(heights)):
            while stack and heights[stack[-1]] >= heights[i]:
                stack.pop()
            if len(stack) == 0:
                leftmax[i]=0
            else:
                leftmax[i]=stack[-1]+1
            stack.append(i)
        while len(stack) is not 0:
            stack.pop()

        for i in range(len(heights)-1,-1,-1):
            print(i)
            while stack and heights[stack[-1]] >= heights[i]:
                stack.pop()
            if len(stack) == 0:
                rightmax[i]=len(heights)-1
            else:
                rightmax[i]=stack[-1]-1
            stack.append(i)

        maxarea = 0
        for i in range(len(heights)):
            maxarea = max(maxarea,heights[i] *(rightmax[i]-leftmax[i]+1))
        return maxarea























def reverseStack(self,s:List[int]):

# use the key as the closure point to check the validity of the parenthesis.
# If the entry is not there, we just ad it to the stack. At each iteration, we pop the stack and check if the
from collections import deque
class Solution:
    def isValid(self, s: str) -> bool:
        print("full string",s)
        stack = deque()
        Map = {"}": "{", ")":"(", "]":"["}

        for item in s:
            if item not in Map:
                stack.append(item)
                continue
            elif not stack or stack[-1] != Map[item]:
                print("item",item)
                return False
            stack.pop()
        return not stack
    

if __name__ == "__main__":

    print(Solution().isValid("()"))
    print(Solution().isValid("()[]{}"))
    print(Solution().isValid("(]"))
    print(Solution().isValid("([)]"))
    print(Solution().isValid("{[]}"))
    print(Solution().isValid("]"))
    print(Solution().isValid("["))
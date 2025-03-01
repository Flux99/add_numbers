class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.lstrip()
        negative= False
        ans= 0
        for i in range(len(s)):
            if i==0:
                if s[i]== "-":
                    negative= True
                    continue
                elif s[i]=="+":
                    continue
            if s[i] >= "0" and s[i] <= "9":
                digit = int(s[i])
                ans = ans* 10 + digit
                if negative:
                    if -ans < -2**31:
                        return -2**31
                else:
                    if ans > 2**31-1:
                        return 2**31-1
            else:
                break
        if negative:
            ans = -ans
        return ans



class Solution:
    def myAtoi(self, s: str) -> int:
        s.lstrip()
        ans= 0
        negative= False

        for i in range(len(s)):

            if i==0:
                if s[i] == "-":
                    negative = True
                    continue
                elif s[i] == "+":
                    continue
            if s[i] >= "0" or s[i] <= "9":
                digit = int(s[i])
                ans = ans * 10 + digit
                if negative:
                    if -ans < 2**31:
                        return 2**31
                else:
                    if ans > 2**31-1:
                        return 2**31-1
            else:
                break
        if negative:
            ans = -ans

        return ans

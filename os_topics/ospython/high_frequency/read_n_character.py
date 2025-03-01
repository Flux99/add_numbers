class Solution:
    def read(self, buf, n):
        """
        :type buf: Destination buffer (List[str])
        :type n: Number of characters to read (int)
        :rtype: The number of actual characters read (int)
        """
        buf4 = [""]* 4
        read_char = 4
        copy_char = 0

        while copy_char < n and read_char == 4:
            read_char = read4(buf4)

            for i in range(read_char):
                if copy_char == n:
                    return copy_char
                buf[copy_char] = buf4[i]
                copy_char+=1
        return copy_char

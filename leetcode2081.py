"""
2081. Sum of k-Mirror Numbers

Hard

A k-mirror number is a positive integer without leading zeros that reads the same both forward and backward in base-10 as well as in base-k.

For example, 9 is a 2-mirror number. The representation of 9 in base-10 and base-2 are 9 and 1001 respectively, which read the same both forward and backward.
On the contrary, 4 is not a 2-mirror number. The representation of 4 in base-2 is 100, which does not read the same both forward and backward.

Given the base k and the number n, return the sum of the n smallest k-mirror numbers.

Example 1:
    Input: k = 2, n = 5
    Output: 25
    Explanation:
        The 5 smallest 2-mirror numbers and their representations in base-2 are:
          base-10    base-2
            1          1
            3          11
            5          101
            7          111
            9          1001
        Their sum = 1 + 3 + 5 + 7 + 9 = 25.

Example 2:
    Input: k = 3, n = 7
    Output: 499
    Explanation:
        The 7 smallest 3-mirror numbers and their representations in base-3 are:
          base-10    base-3
            1          1
            2          2
            4          11
            8          22
            121        11111
            151        12121
            212        21212
        Their sum = 1 + 2 + 4 + 8 + 121 + 151 + 212 = 499.

Example 3:
    Input: k = 7, n = 17
    Output: 20379000
    Explanation:
        The 17 smallest 7-mirror numbers are:
        1, 2, 3, 4, 5, 6, 8, 121, 171, 242, 292, 16561, 65656, 2137312, 4602064, 6597956, 6958596

Constraints:
- 2 <= k <= 9
- 1 <= n <= 30
"""

class Solution:
    def createPalindrome(self, num: int, odd: bool) -> int:
        x = num
        if odd:
            x //= 10
        while x > 0:
            num = num * 10 + x % 10
            x //= 10
        return num

    def isPalindrome(self, num: int, base: int) -> bool:
        digits = []
        while num > 0:
            digits.append(num % base)
            num //= base
        return digits == digits[::-1]

    def kMirror(self, k: int, n: int) -> int:
        total = 0
        length = 1
        while n > 0:
            for i in range(length, length * 10):
                if n <= 0:
                    break
                p = self.createPalindrome(i, True)
                if self.isPalindrome(p, k):
                    total += p
                    n -= 1
            for i in range(length, length * 10):
                if n <= 0:
                    break
                p = self.createPalindrome(i, False)
                if self.isPalindrome(p, k):
                    total += p
                    n -= 1
            length *= 10
        return total

# Test cases
if __name__ == "__main__":
    sol = Solution()
    print(sol.kMirror(2, 5))  # Output: 25
    print(sol.kMirror(3, 7))  # Output: 499
    print(sol.kMirror(7, 17)) # Output: 20379000

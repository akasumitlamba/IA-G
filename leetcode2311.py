"""
2311. Longest Binary Subsequence Less Than or Equal to K

Medium

You are given a binary string s and a positive integer k.
Return the length of the longest subsequence of s that makes up a binary number less than or equal to k.

Note:
- The subsequence can contain leading zeroes.
- The empty string is considered to be equal to 0.
- A subsequence is a string that can be derived from another string by deleting some or no characters without changing the order of the remaining characters.

Example 1:
    Input: s = "1001010", k = 5
    Output: 5
    Explanation:
    The longest subsequence of s that makes up a binary number less than or equal to 5 is "00010" (decimal 2).
    Other examples: "00100" (4), "00101" (5), all length 5.

Example 2:
    Input: s = "00101001", k = 1
    Output: 6
    Explanation:
    "000001" is the longest subsequence making a binary number ≤ 1, length 6.

Constraints:
- 1 <= s.length <= 1000
- s[i] is either '0' or '1'
- 1 <= k <= 10^9
"""

class Solution:
    def longestSubsequence(self, s: str, k: int) -> int:
        n = len(s)
        zeros = s.count('0')
        ones = 0
        value = 0
        power = 1

        # Traverse from right to left (LSB to MSB)
        for i in range(n - 1, -1, -1):
            if s[i] == '1':
                if value + power > k:
                    continue
                value += power
                ones += 1
            power <<= 1
            if power > k:
                break

        return zeros + ones

# Test cases
if __name__ == "__main__":
    sol = Solution()
    print(sol.longestSubsequence("1001010", 5))     # Output: 5
    print(sol.longestSubsequence("00101001", 1))    # Output: 6

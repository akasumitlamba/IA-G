"""
2273. Find Resultant Array After Removing Anagrams

Easy

You are given a 0-indexed string array words, where words[i] consists of lowercase English letters.
In one operation, select any index i such that 0 < i < words.length and words[i - 1] and words[i] are anagrams, and delete words[i] from words. Keep performing this operation as long as you can select an index that satisfies the conditions.

Return words after performing all operations. Selecting the indices for each operation in any order will lead to the same result.

An Anagram is a word formed by rearranging the letters of another, using all the original letters exactly once.

Example 1:
    Input: words = ["abba","baba","bbaa","cd","cd"]
    Output: ["abba","cd"]

Example 2:
    Input: words = ["a","b","c","d","e"]
    Output: ["a","b","c","d","e"]

Constraints:
- 1 <= words.length <= 100
- 1 <= words[i].length <= 10
- words[i] consists of lowercase English letters.
"""

from typing import List

class Solution:
    def removeAnagrams(self, words: List[str]) -> List[str]:
        def freq(s):
            ans = 0
            for c in s:
                i = ord(c) - 97
                ans += (1 << 4 * i)
            return ans
        ans = [words[0]]
        f0 = freq(words[0])
        for r in range(1, len(words)):
            x = freq(words[r])
            if f0 != x:
                ans.append(words[r])
                f0 = x
        return ans

if __name__ == "__main__":
    sol = Solution()
    print(sol.removeAnagrams(["abba","baba","bbaa","cd","cd"])) # Output: ["abba", "cd"]
    print(sol.removeAnagrams(["a","b","c","d","e"]))            # Output: ['a', 'b', 'c', 'd', 'e']

"""
2200. Find All K-Distant Indices in an Array

Easy

You are given a 0-indexed integer array nums and two integers key and k. A k-distant index is an index i of nums for which there exists at least one index j such that |i - j| <= k and nums[j] == key.

Return a list of all k-distant indices sorted in increasing order.

Example 1:
    Input: nums = [3,4,9,1,3,9,5], key = 9, k = 1
    Output: [1,2,3,4,5,6]
    Explanation:
        Here, nums[2] == key and nums[5] == key.
        - For index 0, |0 - 2| > k and |0 - 5| > k, so there is no j where |0 - j| <= k and nums[j] == key. Thus, 0 is not a k-distant index.
        - For index 1, |1 - 2| <= k and nums[2] == key, so 1 is a k-distant index.
        - Indices 2,3,4,5,6 also satisfy the condition similarly.

Example 2:
    Input: nums = [2,2,2,2,2], key = 2, k = 2
    Output: [0,1,2,3,4]
    Explanation:
        Every index has a nearby index with nums[j] == key within distance k, so all are included.

Constraints:
- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 1000
- key is an integer from the array nums
- 1 <= k <= nums.length
"""

from typing import List

class Solution:
    def findKDistantIndices(self, nums: List[int], key: int, k: int) -> List[int]:
        n = len(nums)
        ans = []
        j = 0
        for i, x in enumerate(nums):
            if x == key:
                up = min(n - 1, i + k)
                j = max(j, i - k)
                while j <= up:
                    ans.append(j)
                    j += 1
        return ans

# Test cases
if __name__ == "__main__":
    sol = Solution()
    print(sol.findKDistantIndices([3,4,9,1,3,9,5], 9, 1))  # Output: [1,2,3,4,5,6]
    print(sol.findKDistantIndices([2,2,2,2,2], 2, 2))     # Output: [0,1,2,3,4]

"""
2040. Kth Smallest Product of Two Sorted Arrays

Hard

Given two sorted 0-indexed integer arrays nums1 and nums2 as well as an integer k, return the kth (1-based) smallest product of nums1[i] * nums2[j] where 0 <= i < nums1.length and 0 <= j < nums2.length.

Example 1:
    Input: nums1 = [2,5], nums2 = [3,4], k = 2
    Output: 8
    Explanation:
        The 2 smallest products are:
        - nums1[0] * nums2[0] = 2 * 3 = 6
        - nums1[0] * nums2[1] = 2 * 4 = 8
        The 2nd smallest product is 8.

Example 2:
    Input: nums1 = [-4,-2,0,3], nums2 = [2,4], k = 6
    Output: 0
    Explanation:
        The 6 smallest products are:
        - (-4)*4 = -16
        - (-4)*2 = -8
        - (-2)*4 = -8
        - (-2)*2 = -4
        - 0*2 = 0
        - 0*4 = 0
        The 6th smallest product is 0.

Example 3:
    Input: nums1 = [-2,-1,0,1,2], nums2 = [-3,-1,2,4,5], k = 3
    Output: -6
    Explanation:
        The 3 smallest products are:
        - (-2)*5 = -10
        - (-2)*4 = -8
        - 2*(-3) = -6
        The 3rd smallest product is -6.

Constraints:
- 1 <= nums1.length, nums2.length <= 5 * 10^4
- -10^5 <= nums1[i], nums2[j] <= 10^5
- 1 <= k <= nums1.length * nums2.length
- nums1 and nums2 are sorted.
"""

from typing import List
import bisect

class Solution:
    def kthSmallestProduct(self, nums1: List[int], nums2: List[int], k: int) -> int:
        nums1.sort()
        nums2.sort()

        def count_pairs(x: int) -> int:
            count = 0
            for a in nums1:
                if a > 0:
                    # a * b <= x => b <= x // a
                    count += bisect.bisect_right(nums2, x // a)
                elif a < 0:
                    # a * b <= x => b >= ceil(x / a)
                    target = x // a
                    if x % a != 0:
                        target += 1
                    count += len(nums2) - bisect.bisect_left(nums2, target)
                else:  # a == 0
                    if x >= 0:
                        count += len(nums2)  # zero * anything <= x
                    # else no contribution
            return count

        low, high = -10**10, 10**10
        while low < high:
            mid = (low + high) // 2
            if count_pairs(mid) < k:
                low = mid + 1
            else:
                high = mid
        return low

# Test cases
if __name__ == "__main__":
    sol = Solution()
    print(sol.kthSmallestProduct([2,5], [3,4], 2))          # Output: 8
    print(sol.kthSmallestProduct([-4,-2,0,3], [2,4], 6))    # Output: 0
    print(sol.kthSmallestProduct([-2,-1,0,1,2], [-3,-1,2,4,5], 3))  # Output: -6

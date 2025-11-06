"""
3289. The Two Sneaky Numbers of Digitville

Problem (short):
A list `nums` contains integers from 0 to n-1, but two numbers each appear twice (so the array length is n+2).
Return the two repeated numbers in any order.

Examples:
 - nums = [0,1,1,0] -> [0,1]
 - nums = [0,3,2,1,3,2] -> [2,3]
 - nums = [7,1,5,4,3,4,6,0,9,5,8,2] -> [4,5]

Constraints:
 - 2 <= n <= 100
 - nums.length == n + 2
 - 0 <= nums[i] < n
 - Exactly two elements are repeated (each repeated once)

This file contains a clear, commented Python solution and a few alternative approaches described.
"""

from typing import List
from collections import Counter


class Solution:
    def getSneakyNumbers(self, nums: List[int]) -> List[int]:
        """
        Simple O(n) time, O(n) space approach using a boolean seen array.

        Steps:
          1. Compute the original n (the range of values) as len(nums) - 2.
          2. Create a boolean list `seen` of length n initialized to False.
          3. Iterate through nums:
               - If seen[num] is True, it's a duplicate -> append to result.
               - Otherwise mark seen[num] = True.
          4. Return the list of duplicates (will contain exactly two values).

        This is straightforward, fast, and uses very small extra memory (O(n)).
        """
        n = len(nums) - 2  # original n (values lie in range [0, n-1])
        seen = [False] * n
        res: List[int] = []

        for num in nums:
            if seen[num]:
                res.append(num)
            else:
                seen[num] = True

        return res


# --- Alternative approaches (not implemented as primary) ---
# 1) Counter: use collections.Counter(nums) and collect keys with count == 2.
#    Pros: concise; Cons: slightly more overhead.
#
# 2) Mathematical/XOR trick: for two duplicates, you can use sums and sums of squares
#    to set up two equations and solve for the two repeated values. Works in O(n)
#    time and O(1) extra space but requires care with integer arithmetic and
#    potential overflow in other languages (not an issue in Python for the given constraints).
#
# 3) Sorting: sort the array and scan for adjacent equal elements. O(n log n) time,
#    O(1) additional space if sorting in-place.


if __name__ == '__main__':
    s = Solution()

    # Example 1
    nums = [0, 1, 1, 0]
    print('Example 1 ->', s.getSneakyNumbers(nums))  # -> [0, 1]

    # Example 2
    nums = [0, 3, 2, 1, 3, 2]
    print('Example 2 ->', s.getSneakyNumbers(nums))  # -> [2, 3]

    # Example 3
    nums = [7,1,5,4,3,4,6,0,9,5,8,2]
    print('Example 3 ->', s.getSneakyNumbers(nums))  # -> [4, 5]

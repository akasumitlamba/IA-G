"""
LeetCode Problem: 1488. Avoid Flood in The City
Medium

Your country has an infinite number of lakes. Initially, all the lakes are empty,
but when it rains over the nth lake, the nth lake becomes full of water.
If it rains over a lake that is full of water, there will be a flood.
Your goal is to avoid floods in any lake.

Given an integer array rains where:
- rains[i] > 0 means there will be rains over the rains[i] lake.
- rains[i] == 0 means there are no rains this day and you can choose one lake this day and dry it.

Return an array ans where:
- ans.length == rains.length
- ans[i] == -1 if rains[i] > 0.
- ans[i] is the lake you choose to dry in the ith day if rains[i] == 0.

If there are multiple valid answers return any of them. If it is impossible to avoid flood return an empty array.

Notice that if you chose to dry a full lake, it becomes empty,
but if you chose to dry an empty lake, nothing changes.

Example 1:
Input: rains = [1,2,3,4]
Output: [-1,-1,-1,-1]

Example 2:
Input: rains = [1,2,0,0,2,1]
Output: [-1,-1,2,1,-1,-1]

Example 3:
Input: rains = [1,2,0,1,2]
Output: []

Constraints:
1 <= rains.length <= 10^5
0 <= rains[i] <= 10^9
"""

from bisect import bisect_right
from typing import List
from sortedcontainers import SortedList

class Solution:
    def avoidFlood(self, rains: List[int]) -> List[int]:
        res = [-1] * len(rains)
        full = {}  # lake -> last day it was full
        dry = SortedList()  # days when we can dry lakes
        
        for i, lake in enumerate(rains):
            if lake == 0:
                dry.add(i)
                res[i] = 1  # default dry lake if no pressing need
            else:
                if lake in full:
                    # Find the earliest dry day after last full day of this lake
                    j = dry.bisect_right(full[lake])
                    if j == len(dry):
                        # No dry day to prevent flood
                        return []
                    # Dry this lake on the found dry day
                    res[dry[j]] = lake
                    dry.pop(j)
                full[lake] = i
        
        return res

# Example usage:
if __name__ == "__main__":
    sol = Solution()
    print(sol.avoidFlood([1,2,3,4]))            # Output: [-1, -1, -1, -1]
    print(sol.avoidFlood([1,2,0,0,2,1]))        # Output: [-1, -1, 2, 1, -1, -1]
    print(sol.avoidFlood([1,2,0,1,2]))          # Output: []

"""
407. Trapping Rain Water II

Hard

Given an m x n integer matrix heightMap representing the height of each unit cell in a 2D elevation map, return the volume of water it can trap after raining.

Example 1:
    Input: heightMap = [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]
    Output: 4
    Explanation: After the rain, water is trapped between the blocks.
    We have two small ponds 1 and 3 units trapped.
    The total volume of water trapped is 4.

Example 2:
    Input: heightMap = [[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3],[3,3,3,3,3]]
    Output: 10

Constraints:
- m == heightMap.length
- n == heightMap[i].length
- 1 <= m, n <= 200
- 0 <= heightMap[i][j] <= 2 * 10^4
"""

from typing import List
from heapq import heappop, heappush, heapify

class Solution:
    def trapRainWater(self, height: List[List[int]]) -> int:
        dir = (0, 1, 0, -1, 0)
        m, n = len(height), len(height[0])
        if m <= 2 or n <= 2:
            return 0

        boundary = []
        # Add boundary cells to the heap and mark as visited (-1)
        for i in range(m):
            boundary.append((height[i][0], i, 0))
            boundary.append((height[i][-1], i, n - 1))
            height[i][0] = height[i][-1] = -1

        for j in range(1, n - 1):
            boundary.append((height[0][j], 0, j))
            boundary.append((height[-1][j], m - 1, j))
            height[0][j] = height[-1][j] = -1

        heapify(boundary)
        ans, water_level = 0, 0

        while boundary:
            h, i, j = heappop(boundary)
            water_level = max(water_level, h)
            for a in range(4):
                i0, j0 = i + dir[a], j + dir[a + 1]
                # Check bounds and visited
                if i0 < 0 or i0 >= m or j0 < 0 or j0 >= n or height[i0][j0] == -1:
                    continue
                currH = height[i0][j0]
                if currH < water_level:
                    ans += water_level - currH
                height[i0][j0] = -1  # Mark as visited
                heappush(boundary, (currH, i0, j0))
        return ans

# Test cases
if __name__ == "__main__":
    sol = Solution()
    print(sol.trapRainWater([[1,4,3,1,3,2],
                            [3,2,1,3,2,4],
                            [2,3,3,2,3,1]]))  # Output: 4

    print(sol.trapRainWater([[3,3,3,3,3],
                            [3,2,2,2,3],
                            [3,2,1,2,3],
                            [3,2,2,2,3],
                            [3,3,3,3,3]]))    # Output: 10

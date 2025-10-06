"""
LeetCode Problem: 778. Swim in Rising Water
Hard

You are given an n x n integer matrix grid where each value grid[i][j] represents the elevation at that point (i, j).
It starts raining, and water gradually rises over time.
At time t, the water level is t, meaning any cell with elevation less than equal to t is submerged or reachable.
You can swim from a square to another 4-directionally adjacent square if and only if the elevation of both squares individually are at most t.
You can swim infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.
Return the minimum time until you can reach the bottom right square (n - 1, n - 1) if you start at the top left square (0, 0).

Example 1:
Input: grid = [[0,2],[1,3]]
Output: 3

Example 2:
Input: grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
Output: 16

Constraints:
n == grid.length
n == grid[i].length
1 <= n <= 50
0 <= grid[i][j] < n^2
Each value grid[i][j] is unique.
"""

from typing import List

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        
        def possible(mid):
            seen = set()
            def dfs(r, c):
                if r == m-1 and c == n-1:
                    return True
                seen.add((r, c))
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen:
                        if grid[nr][nc] <= mid:
                            if dfs(nr, nc):
                                return True
                return False
            return grid[0][0] <= mid and dfs(0, 0)
        
        def binary_search():
            lo, hi = grid[0][0], max(max(row) for row in grid)
            while lo < hi:
                mid = (lo + hi) // 2
                if possible(mid):
                    hi = mid
                else:
                    lo = mid + 1
            return lo
        
        return binary_search()

# Example usage:
if __name__ == "__main__":
    sol = Solution()
    print(sol.swimInWater([[0,2],[1,3]]))  # Output: 3
    print(sol.swimInWater([[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]))  # Output: 16

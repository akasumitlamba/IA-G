# LeetCode Problem: 3443. Maximum Manhattan Distance After K Changes
# Medium
# 
# You are given a string s consisting of the characters 'N', 'S', 'E', and 'W',
# where s[i] indicates movements in an infinite grid:
# 'N': Move north by 1 unit.
# 'S': Move south by 1 unit.
# 'E': Move east by 1 unit.
# 'W': Move west by 1 unit.
#
# Initially, you are at the origin (0, 0). You can change at most k characters to any of the four directions.
# Find the maximum Manhattan distance from the origin that can be achieved at any time while performing the movements in order.
# The Manhattan Distance between two cells (xi, yi) and (xj, yj) is |xi - xj| + |yi - yj|.
#
# Example:
# Input: s = "NWSE", k = 1
# Output: 3
#
# Explanation:
# Change s[2] from 'S' to 'N'. Then the string becomes "NWNE".
# Movement and Manhattan distances at each step:
# s[0] = 'N' => (0, 1), Distance = 1
# s[1] = 'W' => (-1, 1), Distance = 2
# s[2] = 'N' => (-1, 2), Distance = 3
# s[3] = 'E' => (0, 2), Distance = 2
# Maximum distance = 3

class Solution:
    def maxDistance(self, s: str, k: int) -> int:
        res = 0
        for diag in [{"N", "E"}, {"N", "W"}, {"S", "E"}, {"S", "W"}]:
            kk, dist = k, 0
            for ch in s:
                if ch in diag or kk:
                    dist += 1
                    kk -= ch not in diag
                else:
                    dist -= 1
                res = max(res, dist)
        return res

# Example usage:
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxDistance("NWSE", 1))  # Output: 3
    print(sol.maxDistance("NSWWEW", 3))  # Output: 6

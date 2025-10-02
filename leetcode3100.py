"""
3100. Water Bottles II

Medium

You are given two integers numBottles and numExchange.
- numBottles represents the number of full water bottles that you initially have.
- In one operation, you can perform one of the following operations:
    1. Drink any number of full water bottles, turning them into empty bottles.
    2. Exchange numExchange empty bottles for one full water bottle. Then, increase numExchange by one.
Note that you cannot exchange multiple batches of empty bottles for the same value of numExchange.

Return the maximum number of water bottles you can drink.

Example 1:
    Input: numBottles = 13, numExchange = 6
    Output: 15

Example 2:
    Input: numBottles = 10, numExchange = 3
    Output: 13

Constraints:
- 1 <= numBottles <= 100
- 1 <= numExchange <= 100
"""

class Solution:
    def maxBottlesDrunk(self, numBottles: int, numExchange: int) -> int:
        bottleDrunk = numBottles
        emptyBottles = numBottles

        while emptyBottles >= numExchange:
            emptyBottles -= numExchange
            numExchange += 1
            bottleDrunk += 1
            emptyBottles += 1
        return bottleDrunk

# Test cases
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxBottlesDrunk(13, 6))   # Output: 15
    print(sol.maxBottlesDrunk(10, 3))   # Output: 13

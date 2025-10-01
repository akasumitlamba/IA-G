"""
1518. Water Bottles

Difficulty: Easy

There are `numBottles` water bottles that are initially full of water. You can exchange `numExchange` empty water bottles from the market with one full water bottle.

Drinking a full water bottle turns it into an empty bottle.

Given two integers, `numBottles` and `numExchange`, return the maximum number of water bottles you can drink.

---

Example 1:

    Input: numBottles = 9, numExchange = 3
    Output: 13
    Explanation: You can exchange 3 empty bottles to get 1 full water bottle.
    Number of water bottles you can drink: 9 + 3 + 1 = 13.

Example 2:

    Input: numBottles = 15, numExchange = 4
    Output: 19
    Explanation: You can exchange 4 empty bottles to get 1 full water bottle.
    Number of water bottles you can drink: 15 + 3 + 1 = 19.

---

Constraints:

- 1 <= numBottles <= 100
- 2 <= numExchange <= 100
"""

class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        return numBottles + (numBottles-1)//(numExchange-1)

# Test cases
if __name__ == '__main__':
    sol = Solution()
    print(sol.numWaterBottles(9, 3))    # Output: 13
    print(sol.numWaterBottles(15, 4))   # Output: 19

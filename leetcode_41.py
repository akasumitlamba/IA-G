# 41. First Missing Positive

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        nums_length = len(nums)
        # initialize the cursor
        i = 0

        # phase 1: sort the numbers with cyclic sort
        # move the cursor through the list
        while i < nums_length:
            # has minus 1 because the numbers start from 1 not 0
            val_at_i = nums[i] - 1

            # does the value belong in the range of the list?
            # if it doesn't, we get an out of bounds error
            # when we try to access nums[val_at_i] later
            belongs_in_range = 0 <= val_at_i < nums_length

            if belongs_in_range and nums[i] != nums[val_at_i]:
                nums[i], nums[val_at_i] = nums[val_at_i], nums[i]
            else:
                i += 1

        # phase 2: find the first missing positive integer
        for x in range(nums_length):
            # has plus 1 because the numbers start from 1 not 0
            if x + 1 != nums[x]:
                return x + 1

        # if all numbers are in the correct spot,
        # the first missing positive integer is the
        # length of the list + 1
        return nums_length + 1

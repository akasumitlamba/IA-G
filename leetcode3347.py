# 3347. Maximum Frequency of an Element After Performing Operations II
# Solved
# Hard
# Topics
# premium lock icon
# Companies
# Hint
# You are given an integer array nums and two integers k and numOperations.

# You must perform an operation numOperations times on nums, where in each operation you:

# Select an index i that was not selected in any previous operations.
# Add an integer in the range [-k, k] to nums[i].
# Return the maximum possible frequency of any element in nums after performing the operations.

 

# Example 1:

# Input: nums = [1,4,5], k = 1, numOperations = 2

# Output: 2

# Explanation:

# We can achieve a maximum frequency of two by:

# Adding 0 to nums[1], after which nums becomes [1, 4, 5].
# Adding -1 to nums[2], after which nums becomes [1, 4, 4].
# Example 2:

# Input: nums = [5,11,20,20], k = 5, numOperations = 1

# Output: 2

# Explanation:

# We can achieve a maximum frequency of two by:

# Adding 0 to nums[1].
 

# Constraints:

# 1 <= nums.length <= 105
# 1 <= nums[i] <= 109
# 0 <= k <= 109
# 0 <= numOperations <= nums.length

class Solution:
    
    def maxFrequency(self, nums: List[int], k: int, numOperations: int) -> int:
        nums.sort()
        # this part implements yesterday's solution to deal with in-array target values
        arrayValMaxFreq = self.maxFrequencyOfArrayVal(nums, k , numOperations) 

        #sliding window solution assuming every element requires an operation:
        left = 0 
        otherValMaxFreq = 0
        for right in range(len(nums)):
            # we adjust the starting point until the sorted subarray is valid
            while nums[right] > nums[left] + 2*k:
                left += 1
            #recording current window length
            otherValMaxFreq = max(otherValMaxFreq, right - left + 1)
            #if the length exceeds the number of operations, we have reached the longest possible window
            if otherValMaxFreq >= numOperations:
                otherValMaxFreq = numOperations
                break
            
        return max(arrayValMaxFreq, otherValMaxFreq)


    # this is the solution from yesterday's problem, used to solve for the values present in the original array
    def maxFrequencyOfArrayVal(self, nums, k, numOperations):
        # NB: nums is already sorted
        count = Counter(nums)

        maxFreq = 0
        # we enumerate the values existing in the original array and deal with them
        for val in count.keys():
            left = bisect_left(nums, val - k)
            right = bisect_right(nums, val + k) - 1
            freq = min(right - left + 1, numOperations + count[val])
            maxFreq = max(maxFreq, freq)

        return maxFreq

        

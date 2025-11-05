"""
Problem 3321: Find X-Sum of All K-Long Subarrays II

You are given an array nums of n integers and two integers k and x.

The x-sum of an array is calculated by the following procedure:
1. Count the occurrences of all elements in the array.
2. Keep only the occurrences of the top x most frequent elements. 
   If two elements have the same number of occurrences, the element 
   with the bigger value is considered more frequent.
3. Calculate the sum of the resulting array.

Note that if an array has less than x distinct elements, its x-sum 
is the sum of the array.

Return an integer array answer of length n - k + 1 where answer[i] 
is the x-sum of the subarray nums[i..i + k - 1].

Example 1:
Input: nums = [1,1,2,2,3,4,2,3], k = 6, x = 2
Output: [6,10,12]

Example 2:
Input: nums = [3,8,7,8,7,5], k = 2, x = 2
Output: [11,15,15,15,12]
"""

from sortedcontainers import SortedSet

def findXSum(nums, k, x):
    """
    Solution using Sliding Window with two SortedSets.
    
    Approach:
    - Maintain two sorted sets: 'top' (x most frequent elements) and 'rest' (others)
    - Use a frequency map to track element occurrences
    - When sliding the window, update frequencies and rebalance the sets
    - Keep track of the sum of elements in the 'top' set
    
    Time Complexity: O(n * k * log k) where n is array length
    Space Complexity: O(k) for storing frequencies and sets
    """
    
    n = len(nums)
    ans = []
    freq = {}
    top = SortedSet()  # Top x frequent elements, sorted by (frequency, value)
    rest = SortedSet()  # Other elements
    top_sum = 0
    
    def balance():
        """Maintain invariant: top contains exactly x most frequent elements"""
        nonlocal top_sum
        
        # If top has more than x elements, move the smallest to rest
        while len(top) > x:
            freq_val, num = top.pop(0)
            top_sum -= freq_val * num
            rest.add((freq_val, num))
        
        # If top has less than x elements and rest is not empty, 
        # move the largest from rest to top
        while len(top) < x and rest:
            freq_val, num = rest.pop()
            top_sum += freq_val * num
            top.add((freq_val, num))
    
    def add(num):
        """Add num to the window"""
        nonlocal top_sum
        
        if num not in freq:
            freq[num] = 0
        
        # Remove old frequency entry if it exists
        if freq[num] > 0:
            old = (freq[num], num)
            if old in top:
                top.remove(old)
                top_sum -= old * old
            else:
                rest.remove(old)
        
        # Add new frequency entry
        freq[num] += 1
        new = (freq[num], num)
        rest.add(new)
        balance()
    
    def remove(num):
        """Remove num from the window"""
        nonlocal top_sum
        
        old = (freq[num], num)
        
        # Remove from top or rest
        if old in top:
            top.remove(old)
            top_sum -= old * old
        else:
            rest.remove(old)
        
        # Update frequency
        freq[num] -= 1
        if freq[num] > 0:
            rest.add((freq[num], num))
        else:
            del freq[num]
        
        balance()
    
    # Build initial window
    for i in range(k):
        add(nums[i])
    ans.append(top_sum)
    
    # Slide the window
    for i in range(k, n):
        remove(nums[i - k])
        add(nums[i])
        ans.append(top_sum)
    
    return ans


# Test cases
if __name__ == "__main__":
    # Test case 1
    nums1 = [1, 1, 2, 2, 3, 4, 2, 3]
    k1 = 6
    x1 = 2
    print(f"Test 1: {findXSum(nums1, k1, x1)}")  # Expected: [6, 10, 12]
    
    # Test case 2
    nums2 = [3, 8, 7, 8, 7, 5]
    k2 = 2
    x2 = 2
    print(f"Test 2: {findXSum(nums2, k2, x2)}")  # Expected: [11, 15, 15, 15, 12]

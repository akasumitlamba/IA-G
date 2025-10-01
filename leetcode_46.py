# 46. Permutations

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []

        def permute_rec(nums, current_index, result):
            if current_index == len(nums) - 1:
                result.append(nums.copy())
                return

            for index in range(current_index, len(nums)):
                nums[current_index], nums[index] = nums[index], nums[current_index]
                permute_rec(nums, current_index + 1, result)
                nums[current_index], nums[index] = nums[index], nums[current_index]

        permute_rec(nums, 0, result)
        return result

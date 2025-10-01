class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        factorials = [1] * n
        for i in range(1, n):
            factorials[i] = factorials[i-1] * i
    
        k -= 1
        numbers = list(range(1, n + 1))
        permutation = []

        for i in range(n, 0, -1):
            index = k // factorials[i - 1]
            k %= factorials[i - 1]
            permutation.append(numbers[index])
            numbers.pop(index)
    
        return ''.join(map(str, permutation))

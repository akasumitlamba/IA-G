# 44. Wildcard Matching
class Solution:
    def isMatch(self, st: str, pattern: str) -> bool:
        s, p, mat, star_idx = 0, 0, 0, -1

        while s < len(st):
            if p < len(pattern) and (pattern[p] == '?' or pattern[p] == st[s]):
                s += 1
                p += 1
            elif p < len(pattern) and pattern[p] == '*':
                star_idx = p
                mat = s
                p += 1
            elif star_idx != -1:
                p = star_idx + 1
                mat += 1
                s = mat
            else:
                return False

        while p < len(pattern) and pattern[p] == '*':
            p += 1

        return p == len(pattern)

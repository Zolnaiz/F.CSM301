"""LeetCode 28. Find the Index of the First Occurrence in a String —
https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/

Built-in хайлт (str.find, in, index) ашиглахгүй.
"""


class Solution:
    """Кнут–Моррис–Праттын (KMP) арга: Θ(n + m) хугацаа, Θ(m) санах ой."""

    def strStr(self, haystack: str, needle: str) -> int:
        m = len(needle)
        if m == 0:
            return 0
        # fail[i] — needle[:i+1]-ийн өөртэйгөө давхцах хамгийн урт жинхэнэ угтвар-дагаврын урт.
        fail = [0] * m
        k = 0
        for i in range(1, m):
            while k > 0 and needle[i] != needle[k]:
                k = fail[k - 1]
            if needle[i] == needle[k]:
                k += 1
            fail[i] = k
        # haystack-ийг нэг удаа гүйнэ: тааралгүй бол needle-ийн заагчийг fail-ээр ухраана.
        k = 0
        for i, ch in enumerate(haystack):
            while k > 0 and ch != needle[k]:
                k = fail[k - 1]
            if ch == needle[k]:
                k += 1
                if k == m:
                    return i - m + 1
        return -1


class SolutionNaive:
    """Харьцуулах зорилготой энгийн арга: байрлал бүрээс тэмдэгт тэмдэгтээр. O(n·m), Θ(1) санах ой."""

    def strStr(self, haystack: str, needle: str) -> int:
        n, m = len(haystack), len(needle)
        for start in range(n - m + 1):
            j = 0
            while j < m and haystack[start + j] == needle[j]:
                j += 1
            if j == m:
                return start
        return -1

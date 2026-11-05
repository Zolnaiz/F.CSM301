"""LeetCode 72. Edit Distance — https://leetcode.com/problems/edit-distance/"""


class Solution:
    """dist[i][j]: word1[:i]-г word2[:j] болгох хамгийн цөөн засвар.

    Тэмдэгт ижил бол dist[i−1][j−1], эс бөгөөс 1 + min(солих dist[i−1][j−1],
    устгах dist[i−1][j], оруулах dist[i][j−1]). Хүснэгтийг мөр мөрөөр бөглөх тул хоёр мөр
    хадгална: хугацаа Θ(mn), санах ой Θ(n).
    """

    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        prev = list(range(n + 1))  # word1 хоосон: j удаа оруулна
        for i in range(1, m + 1):
            curr = [i] + [0] * n  # word2 хоосон: i удаа устгана
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    curr[j] = prev[j - 1]
                else:
                    curr[j] = 1 + min(prev[j - 1], prev[j], curr[j - 1])
            prev = curr
        return prev[n]

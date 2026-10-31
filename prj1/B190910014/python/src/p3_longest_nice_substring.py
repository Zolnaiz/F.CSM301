"""LeetCode 1763. Longest Nice Substring — https://leetcode.com/problems/longest-nice-substring/"""


class Solution:
    """Хэсэгчлэх арга: «муу» үсгүүдээр (эсрэг томын хэлбэр нь мөрөнд байхгүй) хуваана.

    Муу үсгийг агуулсан дэд мөр сайхан байж чадахгүй. Тиймээс бүх муу үсгээр нэг дор
    хуваахад хэсэг бүрээс дор хаяж нэг үсгийн төрөл бүрмөсөн алга болно. Иймд гүн ≤ 52,
    түвшин бүр Θ(n) — нийт Θ(|Σ|·n) = Θ(n) (|Σ| = 52 тогтмол).
    """

    def longestNiceSubstring(self, s: str) -> str:
        if len(s) < 2:
            return ""
        present = set(s)
        best = ""
        start = 0
        split = False
        for i, ch in enumerate(s):
            if ch.swapcase() not in present:  # муу үсэг
                split = True
                part = self.longestNiceSubstring(s[start:i])
                if len(part) > len(best):  # тэнцүү бол эхнийхийг үлдээнэ
                    best = part
                start = i + 1
        if not split:
            return s  # муу үсэггүй — бүхэлдээ сайхан
        part = self.longestNiceSubstring(s[start:])
        return part if len(part) > len(best) else best

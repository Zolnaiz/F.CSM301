"""Codeforces 158B — Taxi. https://codeforces.com/problemset/problem/158/B

Бүлэг бүр 1–4 хүнтэй, нэг бүлэг нэг таксинд (4 суудал) багтах ёстой. Хомхойлох арга:
4-ийн бүлэг бүр тусдаа такси; 3-ын бүлэг бүрд 1-ийн нэг бүлгийг хавсаргана; 2-ын бүлгүүдийг
хосоор нь; үлдсэн 2-ын бүлэгт 1-ийн хоёр бүлэг; үлдсэн 1-ийн бүлгүүдийг 4-өөр нь. Θ(n).
"""
import sys


def taxis(groups: list[int]) -> int:
    c = [0] * 5
    for g in groups:
        c[g] += 1
    total = c[4] + c[3]
    ones = max(0, c[1] - c[3])  # 3 + 1 = 4
    total += c[2] // 2
    if c[2] % 2:
        total += 1
        ones = max(0, ones - 2)  # 2 + 1 + 1 = 4
    return total + (ones + 3) // 4


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    print(taxis([int(x) for x in data[1:1 + n]]))


if __name__ == "__main__":
    main()

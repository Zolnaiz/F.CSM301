"""Codeforces 189A — Cut Ribbon — https://codeforces.com/problemset/problem/189/A

n урттай туузыг a, b, c урттай хэсгүүдэд үлдэгдэлгүй хуваахад хэсгийн тоог хамгийн их болгоно.
best[i] = max(best[i − a], best[i − b], best[i − c]) + 1, best[0] = 0, хүрэхгүй бол −∞.
Хугацаа Θ(n), санах ой Θ(n). Ган савааны бодлоготой ижил бүтэцтэй (зөвхөн 3 урт).
"""
import sys


def max_pieces(n: int, lengths: tuple[int, ...]) -> int:
    best = [-1] * (n + 1)  # −1: энэ уртыг бүрдүүлэх боломжгүй
    best[0] = 0
    for i in range(1, n + 1):
        for x in lengths:
            if x <= i and best[i - x] >= 0 and best[i - x] + 1 > best[i]:
                best[i] = best[i - x] + 1
    return best[n]


def main() -> None:
    n, a, b, c = map(int, sys.stdin.read().split())
    print(max_pieces(n, (a, b, c)))


if __name__ == "__main__":
    main()

def _merge_count(seq: list[int], p: int, q: int, r: int) -> int:
    """seq[p..q], seq[q+1..r]-г нэгтгэж, хоёр хэсгийн хоорондох урвуу хосыг тоолно."""
    left = seq[p : q + 1]
    right = seq[q + 1 : r + 1]
    n_left, n_right = len(left), len(right)
    i = j = 0
    k = p
    inversions = 0
    while i < n_left and j < n_right:
        if left[i] <= right[j]:
            seq[k] = left[i]
            i += 1
        else:
            # left[i..] бүгд right[j]-ээс их тул бүгд right[j]-тэй урвуу хос.
            seq[k] = right[j]
            inversions += n_left - i
            j += 1
        k += 1
    seq[k : k + n_left - i] = left[i:]
    k += n_left - i
    seq[k : k + n_right - j] = right[j:]
    return inversions


def _sort_and_count(seq: list[int], p: int, r: int) -> int:
    if p >= r:
        return 0
    q = (p + r) // 2
    inversions = _sort_and_count(seq, p, q)
    inversions += _sort_and_count(seq, q + 1, r)
    return inversions + _merge_count(seq, p, q, r)


def ranking_distance(a: list[int], b: list[int]) -> int:
    """Хоёр эрэмбийн хоорондох зайг буцаана.

    B-ийн ном бүрийг A дахь байрлалаар нь сольвол A-тай зөрсөн {x, y} хос
    бүр шинэ дараалалд урвуу хос болно. Тиймээс зөрөө нь урвуу хосын тоо.
    """
    if len(a) != len(b):
        raise ValueError("A ба B ижил урттай байх ёстой")
    position = [0] * (len(a) + 1)
    for i, book in enumerate(a):
        position[book] = i
    seq = [position[book] for book in b]
    return _sort_and_count(seq, 0, len(seq) - 1)

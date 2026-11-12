"""Хаффманы код (B төвшин): бага утгын дараалал (heapq)-аар мод байгуулж, код үүсгэнэ."""
import heapq
from itertools import count


def huffman_build(freq: dict[str, int]) -> dict[str, str]:
    """Тэмдэгт → код. Хамгийн бага давтамжтай хоёр зангилааг дахин дахин нэгтгэнэ.

    Навч нь тэмдэгт (str), дотоод зангилаа нь (зүүн, баруун) хос. Ижил давтамжтай үед
    heapq зангилааг өөр хооронд нь харьцуулахгүйн тулд дарааллын дугаар (tie) нэмнэ.
    σ ялгаатай тэмдэгтэд Θ(σ lg σ). Ганц тэмдэгттэй үед код нь "0".
    """
    if not freq:
        return {}
    if len(freq) == 1:
        return {next(iter(freq)): "0"}
    tie = count()
    heap = [(f, next(tie), sym) for sym, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, next(tie), (left, right)))
    codes: dict[str, str] = {}
    stack = [(heap[0][2], "")]
    while stack:  # зүүн тийш 0, баруун тийш 1
        node, code = stack.pop()
        if isinstance(node, tuple):
            stack.append((node[0], code + "0"))
            stack.append((node[1], code + "1"))
        else:
            codes[node] = code
    return codes


def huffman_encode(text: str, codes: dict[str, str]) -> str:
    """Тэмдэгт бүрийг кодоор нь солино. Θ(гаралтын битийн тоо)."""
    return "".join(codes[ch] for ch in text)


def huffman_decode(bits: str, codes: dict[str, str]) -> str:
    """Битийг нэг нэгээр нь уншиж, угтвар нь код болмогц тэмдэгтийг гаргана.

    Угтваргүй код тул тайлалт нэг утгатай. Бит бүрд мөр нэмэх, толь хайх үйлдэл хийнэ.
    """
    reverse = {c: s for s, c in codes.items()}
    out: list[str] = []
    current = ""
    for b in bits:
        current += b
        sym = reverse.get(current)
        if sym is not None:
            out.append(sym)
            current = ""
    if current:
        raise ValueError("битийн мөр бүтэн кодоор төгсөөгүй")
    return "".join(out)

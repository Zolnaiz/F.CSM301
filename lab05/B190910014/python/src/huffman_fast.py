"""Хаффманы код — сайжруулсан тайлалт (A төвшин).

Анхны huffman_decode бит бүрд мөр нэмж, толь хайдаг. Энд кодын модыг төлөвт автомат гэж
үзэж, (төлөв, 8 бит) → (гарах тэмдэгтүүд, шинэ төлөв) хүснэгтийг урьдчилан байгуулна.
Төлөв нь модны дотоод зангилаа (σ − 1 ширхэг) тул хүснэгт (σ − 1)·256 нүдтэй. Хүснэгтийг
4 битийн (16 нүдтэй) хүснэгт хоёроос нийлүүлж байгуулдаг тул бит бүрээр алхахаас ≈ 8 дахин
хурдан. Тайлахдаа 8 бит тутамд ганц хүснэгт хайлт хийнэ (Хаффманы кодын дундаж урт ≈ 4.7
бит тул нэг хайлтаар ≈ 1.7 тэмдэгт гарна).
"""
from src.huffman import huffman_build, huffman_encode

__all__ = ["huffman_build", "huffman_encode", "huffman_decode_fast", "Decoder"]


class Decoder:
    def __init__(self, codes: dict[str, str]) -> None:
        # 1. Кодуудаас мод сэргээнэ: children[зангилаа] = [0-хүүхэд, 1-хүүхэд], навч → тэмдэгт.
        children = [[-1, -1]]
        leaf: dict[int, str] = {}
        for sym, code in codes.items():
            node = 0
            for ch in code:
                b = ch == "1"
                if node in leaf:
                    raise ValueError("код угтваргүй биш")
                if children[node][b] == -1:
                    children.append([-1, -1])
                    children[node][b] = len(children) - 1
                node = children[node][b]
            if node in leaf or children[node] != [-1, -1]:
                raise ValueError("код угтваргүй биш")
            leaf[node] = sym
        self.children, self.leaf = children, leaf
        self.internal = [v for v in range(len(children)) if v not in leaf]
        index = {v: i for i, v in enumerate(self.internal)}

        # 2. 4 битийн хүснэгт: nib[төлөв][0…15] = (гарах мөр, төгсөх зангилаа эсвэл −1).
        nib = {v: [self._walk(v, x, 4) for x in range(16)] for v in self.internal}
        # 3. 8 битийн хүснэгт = дээд 4 бит, дараа нь доод 4 бит.
        self.table: list[list[tuple[str, int]]] = []
        for v in self.internal:
            row: list[tuple[str, int]] = []
            for out1, mid in nib[v]:
                if mid == -1:
                    row.extend([("", -1)] * 16)
                    continue
                for out2, end in nib[mid]:
                    row.append((out1 + out2, index[end] if end != -1 else -1))
            self.table.append(row)

    def _walk(self, v: int, value: int, width: int) -> tuple[str, int]:
        node, out = v, []
        for shift in range(width - 1, -1, -1):
            node = self.children[node][(value >> shift) & 1]
            if node == -1:  # энэ замаар код байхгүй (ганц тэмдэгттэй мод)
                return "".join(out), -1
            if node in self.leaf:
                out.append(self.leaf[node])
                node = 0
        return "".join(out), node

    def decode(self, bits: str) -> str:
        out: list[str] = []
        table, state = self.table, 0
        full = len(bits) - len(bits) % 8
        for pos in range(0, full, 8):
            piece, state = table[state][int(bits[pos:pos + 8], 2)]
            if state == -1:
                raise ValueError("буруу бит")
            out.append(piece)
        node = self.internal[state]  # үлдсэн < 8 битийг модоор нэг нэгээр
        for ch in bits[full:]:
            node = self.children[node][ch == "1"]
            if node == -1:
                raise ValueError("буруу бит")
            if node in self.leaf:
                out.append(self.leaf[node])
                node = 0
        if node != 0:
            raise ValueError("битийн мөр бүтэн кодоор төгсөөгүй")
        return "".join(out)


def huffman_decode_fast(bits: str, codes: dict[str, str]) -> str:
    if not bits:
        return ""
    if len(codes) == 1:  # ганц тэмдэгт: код "0"
        (sym, code), = codes.items()
        if bits.strip(code):
            raise ValueError("буруу бит")
        return sym * (len(bits) // len(code))
    return Decoder(codes).decode(bits)

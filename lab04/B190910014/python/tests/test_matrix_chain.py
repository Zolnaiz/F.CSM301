import re

from src.matrix_chain import matrix_chain_order
from tests.tsv import ints, rows

CASES = rows("matrix_chain_01.tsv")

TOKEN = re.compile(r"A(\d+)|[()]")


def _eval_cost(parens: str, p: list[int]) -> int:
    pos = 0

    def parse():
        nonlocal pos
        m = TOKEN.match(parens, pos)
        assert m, f"буруу тэмдэгт: {parens!r}, байрлал {pos}"
        if m.group(1) is not None:
            i = int(m.group(1))
            pos = m.end()
            return p[i - 1], p[i], 0
        assert parens[pos] == "(", parens
        pos += 1
        r1, c1, cost1 = parse()
        r2, c2, cost2 = parse()
        assert pos < len(parens) and parens[pos] == ")", parens
        pos += 1
        assert c1 == r2, f"хэмжээс таарахгүй: {parens!r}"
        return r1, c2, cost1 + cost2 + r1 * c1 * c2

    _, _, cost = parse()
    assert pos == len(parens), f"ашиглагдаагүй тэмдэгт үлдсэн: {parens!r}"
    return cost


def test_order_is_a_valid_optimal_parenthesization():
    for r in CASES:
        p = ints(r["p"])
        min_mults, parens = matrix_chain_order(p)
        assert min_mults == int(r["min_mults"]), r["id"]
        assert _eval_cost(parens, p) == int(r["min_mults"]), r["id"]

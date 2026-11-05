"""A түвшин: сайжруулсан diff (Myers) ба матрицын цуваа (энгийн дахин дуудалт)."""
import random

import pytest

from src.lcs import lcs_length
from src.lcs_diff_myers import lcs_diff_myers
from src.matrix_chain import matrix_chain_order
from src.matrix_chain_recursive import recursive_matrix_chain
from tests.tsv import SHARED, ints, rows, strs


def _split(lines: list[str]) -> tuple[list[str], list[str], int]:
    a, b, common = [], [], 0
    for line in lines:
        sym, text = line[0], line[1:]
        if sym == " ":
            a.append(text)
            b.append(text)
            common += 1
        elif sym == "-":
            a.append(text)
        elif sym == "+":
            b.append(text)
        else:
            raise AssertionError(line)
    return a, b, common


@pytest.mark.parametrize("r", rows("diff_01.tsv"), ids=lambda r: r["id"])
def test_myers_diff_01(r):
    a_in, b_in = strs(r["A"]), strs(r["B"])
    a_out, b_out, common = _split(lcs_diff_myers(a_in, b_in))
    assert (a_out, b_out, common) == (a_in, b_in, int(r["common"]))


def test_myers_real_document():
    before = (SHARED / "before.txt").read_text(encoding="utf-8").splitlines()
    after = (SHARED / "after.txt").read_text(encoding="utf-8").splitlines()
    assert _split(lcs_diff_myers(before, after)) == (before, after, 6)


def test_myers_common_equals_lcs_random():
    rng = random.Random(4)
    for _ in range(2000):
        a = [rng.choice("abcde") for _ in range(rng.randint(0, 12))]
        b = [rng.choice("abcde") for _ in range(rng.randint(0, 12))]
        a_out, b_out, common = _split(lcs_diff_myers(a, b))
        assert (a_out, b_out) == (a, b)
        assert common == lcs_length("".join(a), "".join(b))


@pytest.mark.parametrize("r", rows("matrix_chain_01.tsv"), ids=lambda r: r["id"])
def test_recursive_chain_matches(r):
    p = ints(r["p"])
    cost, calls = recursive_matrix_chain(p)
    assert cost == int(r["min_mults"]) == matrix_chain_order(p)[0]
    assert calls == 3 ** (len(p) - 2)  # C(n) = 1 + 2·ΣC(k) = 3^(n−1)

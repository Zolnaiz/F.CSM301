import math

import pytest

from src.binary_search import binary_search
from tests.tsv import ints, rows

CASES = rows("binary_search_01.tsv")


@pytest.mark.parametrize("r", CASES, ids=[r["id"] for r in CASES])
def test_index(r):
    idx, _ = binary_search(ints(r["A"]), int(r["x"]))
    assert idx == int(r["index0"])


@pytest.mark.parametrize("r", CASES, ids=[r["id"] for r in CASES])
def test_call_count(r):
    _, calls = binary_search(ints(r["A"]), int(r["x"]))
    assert calls == int(r["calls"])


@pytest.mark.parametrize("r", CASES, ids=[r["id"] for r in CASES])
def test_call_count_within_bound(r):
    n = int(r["n"])
    _, calls = binary_search(ints(r["A"]), int(r["x"]))
    assert calls <= math.floor(math.log2(n)) + 2

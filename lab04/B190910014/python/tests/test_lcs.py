from src.lcs import lcs_length
from tests.tsv import rows

CASES = rows("lcs_01.tsv")


def test_length():
    for r in CASES:
        assert lcs_length(r["X"], r["Y"]) == int(r["length"]), r["id"]

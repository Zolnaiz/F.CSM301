from src.knapsack import fractional_knapsack
from tests.tsv import ints, rows

CASES = rows("knapsack_01.tsv")


def test_fractional_value_to_two_decimals():
    for r in CASES:
        got = fractional_knapsack(ints(r["w"]), ints(r["v"]), int(r["W"]))
        assert f"{got:.2f}" == r["fractional"], r["id"]

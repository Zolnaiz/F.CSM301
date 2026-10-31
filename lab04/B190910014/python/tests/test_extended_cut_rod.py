from src.extended_cut_rod import extended_bottom_up_cut_rod
from tests.tsv import ints, rows

CASES = rows("rod_cuts_01.tsv")


def test_cuts_are_a_valid_optimal_partition():
    for r in CASES:
        p = ints(r["p"])
        n = int(r["n"])
        revenue, cuts = extended_bottom_up_cut_rod(p)
        assert all(1 <= c <= n for c in cuts), r["id"]
        assert sum(cuts) == n, r["id"]
        assert sum(p[c - 1] for c in cuts) == int(r["expected_revenue"]), r["id"]
        assert revenue == int(r["expected_revenue"]), r["id"]

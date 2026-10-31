from src.cut_rod import bottom_up_cut_rod
from tests.tsv import ints, rows

CASES = rows("rod_01.tsv")


def test_revenue_and_loop_count():
    for r in CASES:
        revenue, loop_count = bottom_up_cut_rod(ints(r["p"]))
        assert revenue == int(r["expected_revenue"]), r["id"]
        assert loop_count == int(r["expected_loop_count"]), r["id"]


def test_inner_loop_count_matches_n_n_plus_1_over_2():
    for n in (1, 2, 3, 5, 10):
        _, loop_count = bottom_up_cut_rod([1] * n)
        assert loop_count == n * (n + 1) // 2

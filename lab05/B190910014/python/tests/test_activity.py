from src.activity import activity_select
from tests.tsv import ints, rows

CASES = rows("activity_01.tsv")


def test_selects_maximum_compatible_set():
    for r in CASES:
        s, f = ints(r["s"]), ints(r["f"])
        n = int(r["n"])
        chosen = activity_select(s, f)
        assert all(1 <= i <= n for i in chosen), r["id"]
        assert len(set(chosen)) == len(chosen), r["id"]
        for a in chosen:
            for b in chosen:
                if a < b:
                    assert s[a - 1] >= f[b - 1] or s[b - 1] >= f[a - 1], (r["id"], a, b)
        assert len(chosen) == int(r["expected_count"]), r["id"]

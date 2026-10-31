from src.lcs_diff import lcs_diff
from tests.tsv import SHARED, rows, strs

CASES = rows("diff_01.tsv")


def _split(diff_lines: list[str]) -> tuple[list[str], list[str], int]:
    a, b, common = [], [], 0
    for line in diff_lines:
        assert line, "хоосон мөр буцаасан байж болохгүй"
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
            raise AssertionError(f"мэдэгдэхгүй тэмдэгт: {line!r}")
    return a, b, common


def test_reconstructs_both_sides_and_common_count():
    for r in CASES:
        a_in, b_in = strs(r["A"]), strs(r["B"])
        a_out, b_out, common = _split(lcs_diff(a_in, b_in))
        assert a_out == a_in, r["id"]
        assert b_out == b_in, r["id"]
        assert common == int(r["common"]), r["id"]


def test_real_document_revision():
    before = (SHARED / "before.txt").read_text(encoding="utf-8").splitlines()
    after = (SHARED / "after.txt").read_text(encoding="utf-8").splitlines()
    a_out, b_out, common = _split(lcs_diff(before, after))
    assert a_out == before
    assert b_out == after
    assert common == 6

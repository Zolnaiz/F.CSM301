import csv
from pathlib import Path

import pytest

from fibonacci import fibonacci, fibonacci_recursive

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "test_data"
DATA = DATA_DIR / "fibonacci.tsv"


def load_cases(path: Path):
    with path.open(encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)  # толгойг алгасна
        return [(int(row[0]), int(row[1])) for row in reader if row]


def load_invalid(path: Path):
    with path.open(encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        return [int(row[0]) for row in reader if row]


CASES = load_cases(DATA)
MY_CASES = load_cases(DATA_DIR / "fibonacci_my.tsv")
INVALID = load_invalid(DATA_DIR / "fibonacci_invalid.tsv")


@pytest.mark.parametrize(
    "n,expected", CASES, ids=[f"n={n}" for n, _ in CASES]
)
@pytest.mark.timeout(5)
def test_fibonacci(n, expected):
    assert fibonacci(n) == expected


# (a) алхам: дахин дуудах хувилбар n = 0..10 тохиолдлыг давна.
@pytest.mark.parametrize(
    "n,expected",
    [c for c in CASES if c[0] <= 10],
    ids=[f"n={n}" for n, _ in CASES if n <= 10],
)
@pytest.mark.timeout(5)
def test_fibonacci_recursive_small(n, expected):
    assert fibonacci_recursive(n) == expected


# (c) алхам: n < 0 үед ValueError шидэнэ.
@pytest.mark.parametrize("n", INVALID, ids=[f"n={n}" for n in INVALID])
def test_fibonacci_invalid(n):
    with pytest.raises(ValueError):
        fibonacci(n)


# (d) алхам: хуулбар файлд n = 46, 47 нэмсэн.
@pytest.mark.parametrize(
    "n,expected", MY_CASES, ids=[f"n={n}" for n, _ in MY_CASES]
)
@pytest.mark.timeout(5)
def test_fibonacci_my(n, expected):
    assert fibonacci(n) == expected

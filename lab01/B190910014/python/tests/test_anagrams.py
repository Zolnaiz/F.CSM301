import csv
from pathlib import Path

import pytest

from anagrams import find_anagrams

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "test_data"


def split_words(field: str):
    """'eat,tea' -> ['eat', 'tea']. Хоосон талбар -> []."""
    return field.split(",") if field else []


def split_groups(field: str):
    """'eat,tea;tan,nat' -> [['eat','tea'], ['tan','nat']]."""
    return [split_words(g) for g in field.split(";")] if field else []


def load_cases(name: str):
    with (DATA_DIR / name).open(encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        return [
            (split_words(row[0]), split_groups(row[1]))
            for row in reader
            if row
        ]


def normalize(groups):
    return sorted(sorted(g) for g in groups)


@pytest.mark.parametrize("words,expected", load_cases("anagrams_01.tsv"))
def test_examples(words, expected):
    assert normalize(find_anagrams(words)) == normalize(expected)


@pytest.mark.parametrize("words,expected", load_cases("anagrams_my.tsv"))
def test_my_cases(words, expected):
    assert normalize(find_anagrams(words)) == normalize(expected)

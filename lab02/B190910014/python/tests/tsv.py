from __future__ import annotations

import csv
from pathlib import Path

STUDENT_DIR = Path(__file__).resolve().parents[2]
LAB_DIR = Path(__file__).resolve().parents[3]

SHARED = LAB_DIR / "test_data"
MINE = STUDENT_DIR / "test_data"
OUT = STUDENT_DIR / "out"


def rows(name: str) -> list[dict[str, str]]:
    path = SHARED / name
    if not path.exists():
        path = MINE / name
    if not path.exists():
        raise FileNotFoundError(
            f"{name} олдсонгүй ({SHARED} эсвэл {MINE}). "
            f"lab02/<Student-ID>/python/ дотроос ажиллуулж байна уу?"
        )
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def ints(s: str) -> list[int]:
    """'1,2,3' -> [1, 2, 3];  '' -> []"""
    s = s.strip()
    return [int(x) for x in s.split(",")] if s else []


def write_results(language: str, header: list[str], data: list[list]) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"results_{language}.tsv"
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("\t".join(header) + "\n")
        for r in data:
            f.write("\t".join(str(v) for v in r) + "\n")
    return path

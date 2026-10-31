"""out/results_*.tsv → prj1_report.md доторх <!-- BEGIN:x --> ... <!-- END:x --> хүснэгтүүд.

Ажиллуулах: python make_tables.py
"""
import csv
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out"
REPORT = HERE / "prj1_report.md"
CATALAN = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796]


def load(lang: str) -> dict:
    data = {}
    with (OUT / f"results_{lang}.tsv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            key = (r["problem"], r["variant"], r["case"], int(r["n"]))
            mem = float(r.get("peak_kb") or r.get("alloc_kb"))
            data[key] = (float(r["time_ms"]), mem, r["extra"])
    return data


def ms(x: float) -> str:
    return f"{x:.3f}" if x < 10 else f"{x:.1f}" if x < 1000 else f"{x:,.0f}"


def kb(x: float) -> str:
    return f"{x:,.1f}" if x < 1000 else f"{x:,.0f}"


def tables(py: dict, jv: dict) -> dict[str, str]:
    t = {}

    rows = ["| n | Python, ms | Java, ms | Python t / (n lg n), нс | Python санах ой, KB | Java санах ой, KB |",
            "| -: | -: | -: | -: | -: | -: |"]
    for n in (10**3, 10**4, 10**5, 10**6):
        p, j = py[("p1", "dc", "random", n)], jv[("p1", "dc", "random", n)]
        rows.append(f"| {n:,} | {ms(p[0])} | {ms(j[0])} | {p[0] * 1e6 / (n * math.log2(n)):.0f} "
                    f"| {kb(p[1])} | {kb(j[1])} |")
    t["p1"] = "\n".join(rows)

    rows = ["| n | Python, ms | Java, ms | Python санах ой, KB | Java санах ой, KB | Java, байт/зангилаа |",
            "| -: | -: | -: | -: | -: | -: |"]
    for n in (10**3, 10**4, 10**5, 10**6):
        p, j = py[("p2", "basic", "sorted", n)], jv[("p2", "basic", "sorted", n)]
        rows.append(f"| {n:,} | {ms(p[0])} | {ms(j[0])} | {kb(p[1])} | {kb(j[1])} | {j[1] * 1024 / n:.0f} |")
    t["p2"] = "\n".join(rows)

    rows = ["| n | Оролт | Python, ms | Java, ms | Python t / n, нс | Java t / n, нс | Python санах ой, KB "
            "| Java санах ой, KB |",
            "| -: | --- | -: | -: | -: | -: | -: | -: |"]
    for n in (10**2, 10**3, 10**4, 10**5):
        for case in ("nice", "split"):
            p, j = py[("p3", "dc", case, n)], jv[("p3", "dc", case, n)]
            rows.append(f"| {n:,} | {case} | {ms(p[0])} | {ms(j[0])} | {p[0] * 1e6 / n:.0f} | {j[0] * 1e6 / n:.0f} "
                        f"| {kb(p[1])} | {kb(j[1])} |")
    t["p3"] = "\n".join(rows)

    rows = ["| k | Хариу (Каталан) | Дуудалт: анхны | Дуудалт: сайжруулсан | Python анхны, ms | Python сайжр., ms "
            "| Java анхны, ms | Java сайжр., ms | Python анхны / сайжр. |",
            "| -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
    for k in range(2, 11):
        pb, pi = py[("p4", "basic", "random", k)], py[("p4", "improved", "random", k)]
        jb, ji = jv[("p4", "basic", "random", k)], jv[("p4", "improved", "random", k)]
        cb, ci = pb[2].split("=")[1], pi[2].split("=")[1]
        rows.append(f"| {k} | {CATALAN[k]:,} | {int(cb):,} | {ci} | {ms(pb[0])} | {ms(pi[0])} | {ms(jb[0])} "
                    f"| {ms(ji[0])} | {pb[0] / pi[0]:.1f}× |")
    t["p4_time"] = "\n".join(rows)

    rows = ["| k | Python анхны, KB | Python сайжр., KB | Java анхны, KB | Java сайжр., KB |",
            "| -: | -: | -: | -: | -: |"]
    for k in range(2, 11):
        rows.append(f"| {k} | {kb(py[('p4', 'basic', 'random', k)][1])} | {kb(py[('p4', 'improved', 'random', k)][1])} "
                    f"| {kb(jv[('p4', 'basic', 'random', k)][1])} | {kb(jv[('p4', 'improved', 'random', k)][1])} |")
    t["p4_mem"] = "\n".join(rows)

    for case in ("random", "chain"):
        rows = ["| n | Python анхны, ms | Python сайжр., ms | Java анхны, ms | Java сайжр., ms "
                "| Python анхны, KB | Python сайжр., KB | Java анхны, KB | Java сайжр., KB |",
                "| -: | -: | -: | -: | -: | -: | -: | -: | -: |"]
        for n in (500, 1000, 2000, 4000):
            pb, pi = py[("p5", "basic", case, n)], py[("p5", "improved", case, n)]
            jb, ji = jv[("p5", "basic", case, n)], jv[("p5", "improved", case, n)]
            rows.append(f"| {n:,} | {ms(pb[0])} | {ms(pi[0])} | {ms(jb[0])} | {ms(ji[0])} "
                        f"| {kb(pb[1])} | {kb(pi[1])} | {kb(jb[1])} | {kb(ji[1])} |")
        t[f"p5_{case}"] = "\n".join(rows)
    return t


def main() -> None:
    generated = tables(load("python"), load("java"))
    text = REPORT.read_text(encoding="utf-8")
    for name, table in generated.items():
        pattern = re.compile(rf"(<!-- BEGIN:{name} -->).*?(<!-- END:{name} -->)", re.S)
        text, count = pattern.subn(lambda m: m.group(1) + "\n" + table + "\n" + m.group(2), text)
        if count == 0:
            print(f"анхааруулга: {name} тэмдэг олдсонгүй")
    REPORT.write_text(text, encoding="utf-8")
    print(f"-> {REPORT}")


if __name__ == "__main__":
    main()

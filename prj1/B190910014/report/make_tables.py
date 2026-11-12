"""out/results_*.tsv → prj1_report.tex доторх «% BEGIN:x» … «% END:x» хүснэгтүүд.

Ажиллуулах: python3 make_tables.py && ./build.sh
"""
import csv
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out"
REPORT = HERE / "prj1_report.tex"
CATALAN = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796]


def load(lang: str) -> dict:
    data = {}
    with (OUT / f"results_{lang}.tsv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            key = (r["problem"], r["variant"], r["case"], int(r["n"]))
            mem = float(r.get("peak_kb") or r.get("alloc_kb"))
            data[key] = (float(r["time_ms"]), mem, r["extra"])
    return data


def num(x: float, fmt: str) -> str:
    """Мянгатын тусгаарлагч нь нарийн зай (\\,)."""
    return format(x, fmt).replace(",", r"\,")


def ms(x: float) -> str:
    return num(x, ".3f") if x < 10 else num(x, ".1f") if x < 1000 else num(x, ",.0f")


def kb(x: float) -> str:
    return num(x, ",.1f") if x < 1000 else num(x, ",.0f")


def latex(headers: list[str], align: str, rows: list[list[str]],
          groups: list[tuple[str, int]] | None = None) -> str:
    """Толгойн «\\n» нь нүдэн доторх мөр таслал. groups: дээд мөрийн (нэр, хэдэн багана) бүлгүүд."""
    cols = len(align)
    out = [r"\begin{center}", r"\scriptsize" if cols >= 8 else r"\footnotesize" if cols >= 5 else r"\small"]
    if cols >= 8:
        out.append(r"\setlength{\tabcolsep}{4pt}")
    out += [r"\begin{tabular}{" + align + "}", r"\toprule"]
    if groups:
        top, rules, col = [], [], 1
        for label, span in groups:
            top.append(r"\multicolumn{" + str(span) + "}{c}{" + (r"\textbf{" + label + "}" if label else "") + "}")
            if label:
                rules.append(r"\cmidrule(lr){" + f"{col}-{col + span - 1}" + "}")
            col += span
        out += [" & ".join(top) + r" \\", " ".join(rules)]
    cells = []
    for h, a in zip(headers, align):
        lines = h.split("\n")
        cells.append(r"\textbf{" + h + "}" if len(lines) == 1 else
                     r"\textbf{\begin{tabular}[b]{@{}" + a + "@{}}" + r" \\ ".join(lines) + r"\end{tabular}}")
    out += [" & ".join(cells) + r" \\", r"\midrule"]
    out += [" & ".join(r) + r" \\" for r in rows]
    out += [r"\bottomrule", r"\end{tabular}", r"\end{center}"]
    return "\n".join(out)


def tables(py: dict, jv: dict) -> dict[str, str]:
    t = {}

    rows = []
    for n in (10**3, 10**4, 10**5, 10**6):
        p, j = py[("p1", "dc", "random", n)], jv[("p1", "dc", "random", n)]
        rows.append([num(n, ","), ms(p[0]), ms(j[0]), f"{p[0] * 1e6 / (n * math.log2(n)):.0f}", kb(p[1]), kb(j[1])])
    t["p1"] = latex(["n", "Python,\nms", "Java,\nms", "Python\nt/(n lg n), нс", "Python санах\nой, KB",
                     "Java санах\nой, KB"], "rrrrrr", rows)

    rows = []
    for n in (10**3, 10**4, 10**5, 10**6):
        p, j = py[("p2", "basic", "sorted", n)], jv[("p2", "basic", "sorted", n)]
        rows.append([num(n, ","), ms(p[0]), ms(j[0]), kb(p[1]), kb(j[1]), f"{j[1] * 1024 / n:.0f}"])
    t["p2"] = latex(["n", "Python,\nms", "Java,\nms", "Python санах\nой, KB", "Java санах\nой, KB",
                     "Java, байт/\nзангилаа"], "rrrrrr", rows)

    rows = []
    for n in (10**2, 10**3, 10**4, 10**5):
        for case in ("nice", "split"):
            p, j = py[("p3", "dc", case, n)], jv[("p3", "dc", case, n)]
            rows.append([num(n, ","), case, ms(p[0]), ms(j[0]), f"{p[0] * 1e6 / n:.0f}", f"{j[0] * 1e6 / n:.0f}",
                         kb(p[1]), kb(j[1])])
    t["p3"] = latex(["n", "Оролт", "Python,\nms", "Java,\nms", "Python\nt/n, нс", "Java\nt/n, нс",
                     "Python санах\nой, KB", "Java санах\nой, KB"], "rlrrrrrr", rows)

    rows = []
    for k in range(2, 11):
        pb, pi = py[("p4", "basic", "random", k)], py[("p4", "improved", "random", k)]
        jb, ji = jv[("p4", "basic", "random", k)], jv[("p4", "improved", "random", k)]
        cb, ci = int(pb[2].split("=")[1]), int(pi[2].split("=")[1])
        rows.append([str(k), num(CATALAN[k], ","), num(cb, ","), str(ci), ms(pb[0]), ms(pi[0]), ms(jb[0]), ms(ji[0]),
                     f"{pb[0] / pi[0]:.1f}×"])
    pair = ["анхны", "сайжруулсан"]
    t["p4_time"] = latex(["k", "Хариу\n(Каталан)", *pair, *pair, *pair, "Python-д\nхурдсалт"], "rrrrrrrrr", rows,
                         [("", 2), ("Дуудалтын тоо", 2), ("Python, ms", 2), ("Java, ms", 2), ("", 1)])

    rows = [[str(k), kb(py[("p4", "basic", "random", k)][1]), kb(py[("p4", "improved", "random", k)][1]),
             kb(jv[("p4", "basic", "random", k)][1]), kb(jv[("p4", "improved", "random", k)][1])]
            for k in range(2, 11)]
    t["p4_mem"] = latex(["k", *pair, *pair], "rrrrr", rows, [("", 1), ("Python, KB", 2), ("Java, KB", 2)])

    for case in ("random", "chain"):
        rows = []
        for n in (500, 1000, 2000, 4000):
            pb, pi = py[("p5", "basic", case, n)], py[("p5", "improved", case, n)]
            jb, ji = jv[("p5", "basic", case, n)], jv[("p5", "improved", case, n)]
            rows.append([num(n, ","), ms(pb[0]), ms(pi[0]), ms(jb[0]), ms(ji[0]),
                         kb(pb[1]), kb(pi[1]), kb(jb[1]), kb(ji[1])])
        t[f"p5_{case}"] = latex(["n", *pair * 4], "rrrrrrrrr", rows,
                                [("", 1), ("Python, ms", 2), ("Java, ms", 2), ("Python, KB", 2), ("Java, KB", 2)])
    return t


def main() -> None:
    generated = tables(load("python"), load("java"))
    text = REPORT.read_text(encoding="utf-8")
    for name, table in generated.items():
        pattern = re.compile(rf"(% BEGIN:{name}\n).*?(% END:{name})", re.S)
        text, count = pattern.subn(lambda m: m.group(1) + table + "\n" + m.group(2), text)
        if count == 0:
            print(f"анхааруулга: {name} тэмдэг олдсонгүй")
    REPORT.write_text(text, encoding="utf-8")
    print(f"-> {REPORT}")


if __name__ == "__main__":
    main()

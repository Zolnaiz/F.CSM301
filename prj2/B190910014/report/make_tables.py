"""../out/results_*.tsv → prj2_report.tex доторх «% BEGIN:x» … «% END:x» хүснэгтүүд.

Ажиллуулах: python3 make_tables.py && ./build.sh
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out"
REPORT = HERE / "prj2_report.tex"


def load(lang: str) -> dict:
    data = {}
    with (OUT / f"results_{lang}.tsv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            mem = float(r.get("peak_kb") or r.get("alloc_kb"))
            data[(r["problem"], r["variant"], r["case"], int(r["n"]))] = (float(r["time_ms"]), mem, r["extra"])
    return data


def num(x: float, fmt: str) -> str:
    return format(x, fmt).replace(",", r"\,")


def ms(x: float) -> str:
    return num(x, ".4f") if x < 0.1 else num(x, ".3f") if x < 10 else num(x, ".1f") if x < 1000 else num(x, ",.0f")


def kb(x: float) -> str:
    return num(x, ",.1f") if x < 1000 else num(x, ",.0f")


def extra(e: str, key: str) -> str:
    return dict(p.split("=") for p in e.split(";"))[key]


def latex(headers, align, rows, groups=None) -> str:
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
    pair = ["KMP", "энгийн"]
    rows = []
    for case in ("worst", "random"):
        for n in (10**3, 10**4, 10**5):
            k = [d[("p1", v, case, n)] for d in (py, jv) for v in ("kmp", "naive")]
            rows.append([num(n, ","), {"worst": "муу", "random": "санамсаргүй"}[case],
                         ms(k[0][0]), ms(k[1][0]), ms(k[2][0]), ms(k[3][0]), kb(k[0][1]), kb(k[2][1])])
    t["p1"] = latex(["n", "Оролт", *pair, *pair, "Python\nKMP", "Java\nKMP"], "rlrrrrrr", rows,
                    [("", 2), ("Python, ms", 2), ("Java, ms", 2), ("Санах ой, KB", 2)])

    rows = []
    for side in (50, 200, 1000):
        n = side * side
        p, j = py[("p2", "bfs", "full", n)], jv[("p2", "bfs", "full", n)]
        rows.append([f"{side}×{side}", num(n, ","), ms(p[0]), ms(j[0]), f"{p[0] * 1e6 / n:.0f}",
                     f"{j[0] * 1e6 / n:.1f}", kb(p[1]), kb(j[1])])
    t["p2"] = latex(["Зураг", "Нүд", "Python,\nms", "Java,\nms", "Python\nнс/нүд", "Java\nнс/нүд",
                     "Python\nоргил, KB", "Java\nхуваарилсан, KB"], "lrrrrrrr", rows)

    rows = []
    for n in (10**4, 10**5, 10**6):
        p, j = py[("p3", "greedy", "random", n)], jv[("p3", "greedy", "random", n)]
        rows.append([num(n, ","), p[2], ms(p[0]), ms(j[0]), kb(p[1]), kb(j[1])])
    t["p3"] = latex(["n = m", "Хариу", "Python,\nms", "Java,\nms", "Python\nоргил, KB", "Java\nхуваарилсан, KB"],
                    "rrrrrr", rows)

    rows = []
    for n in (10**3, 10**4, 10**5):
        pg, jg = py[("p4", "greedy", "random", n)], jv[("p4", "greedy", "random", n)]
        pd, jd = py.get(("p4", "dp", "random", n)), jv.get(("p4", "dp", "random", n))
        steps = extra((pd or jd)[2], "steps") if (pd or jd) else "—"
        rows.append([num(n, ","), extra(pg[2], "jumps"), num(int(steps), ",") if steps != "—" else "—",
                     ms(pd[0]) if pd else "—", ms(pg[0]), ms(jd[0]) if jd else "—", ms(jg[0]),
                     kb(pd[1]) if pd else "—", kb(pg[1])])
    t["p4"] = latex(["n", "Үсрэлт", "ДП-гийн\nалхам", "ДП", "хомхойлох", "ДП", "хомхойлох", "ДП", "хомхойлох"],
                    "rrrrrrrrr", rows, [("", 3), ("Python, ms", 2), ("Java, ms", 2), ("Python, KB", 2)])

    rows = []
    names = {"far": "«5555», түгжээгүй", "example": "LeetCode жишээ 1", "random": "500 санамсаргүй түгжээ",
             "blocked": "зорилгыг бүсэлсэн"}
    for case in ("far", "example", "random", "blocked"):
        # Санамсаргүй түгжээний тоо хэл бүрд өөр (санамсаргүй тоо үүсгэгч өөр) тул n-ийг тус тусад нь олно.
        n_py = next(k[3] for k in py if k[:3] == ("p5", "bfs", case))
        n_jv = next(k[3] for k in jv if k[:3] == ("p5", "bfs", case))
        pb, pi = py[("p5", "bfs", case, n_py)], py[("p5", "bidir", case, n_py)]
        jb, ji = jv[("p5", "bfs", case, n_jv)], jv[("p5", "bidir", case, n_jv)]
        rows.append([names[case], extra(pb[2], "answer"), num(int(extra(pb[2], "expanded")), ","),
                     num(int(extra(pi[2], "expanded")), ","), ms(pb[0]), ms(pi[0]), ms(jb[0]), ms(ji[0]),
                     kb(pb[1]), kb(pi[1])])
    t["p5"] = latex(["Тохиолдол", "Хариу", "BFS", "хоёр тал", "BFS", "хоёр тал", "BFS", "хоёр тал", "BFS", "хоёр тал"],
                    "lrrrrrrrrr", rows,
                    [("", 2), ("Тэлсэн төлөв", 2), ("Python, ms", 2), ("Java, ms", 2), ("Python, KB", 2)])
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

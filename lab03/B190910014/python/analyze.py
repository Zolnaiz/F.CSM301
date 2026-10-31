"""5-р даалгаврын хэмжилтийн шинжилгээ: налуу, огтлолцлын цэг, хэлний харьцаа, график.

Ажиллуулах: python3 analyze.py   (matplotlib хэрэгтэй)
Оролт: ../out/results_python.tsv, ../out/results_java.tsv
Гаралт: ../docs/benchmark_loglog.png болон тайланд орох хүснэгтүүд
"""
import csv
import math
from pathlib import Path

STUDENT_DIR = Path(__file__).resolve().parent.parent
OUT = STUDENT_DIR / "out"
DOCS = STUDENT_DIR / "docs"
ALGS = ["matrix_multiply", "matrix_multiply_recursive", "strassen", "strassen_cutoff64"]
THEORY = {"matrix_multiply": 3.0, "matrix_multiply_recursive": 3.0,
          "strassen": math.log2(7), "strassen_cutoff64": math.log2(7)}


def load(lang: str) -> dict[str, dict[int, float]]:
    data: dict[str, dict[int, float]] = {a: {} for a in ALGS}
    path = OUT / f"results_{lang}.tsv"
    if not path.exists():
        return data
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            data[r["algorithm"]][int(r["n"])] = float(r["time_ms"])
    return data


def fit(points: dict[int, float]) -> tuple[float, float]:
    """n-ийн хамгийн их 3 цэгээр log2 t = s·log2 n + c шугаман регресс. (s, c)."""
    ns = sorted(points)[-3:]
    xs = [math.log2(n) for n in ns]
    ys = [math.log2(points[n]) for n in ns]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    s = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return s, my - s * mx


def crossover(data: dict[str, dict[int, float]], fast: str, slow: str, min_n: int = 1) -> str:
    common = sorted(n for n in set(data[fast]) & set(data[slow]) if n >= min_n)
    for n in common:
        if data[fast][n] < data[slow][n] and all(data[fast][m] < data[slow][m] for m in common if m > n):
            return f"n₀ = {n} (хэмжсэн)"
    # Онолын илтгэгчээр: t_fast = C_f·n^lg7, t_slow = C_s·n^3 гэж хамгийн их n-ээр C-г олно.
    n = max(common)
    ratio = data[fast][n] / data[slow][n]
    n0 = n * ratio ** (1 / (THEORY[slow] - THEORY[fast]))
    s1, c1 = fit(data[fast])
    s2, c2 = fit(data[slow])
    by_fit = (f"регрессээр n₀ ≈ {2 ** ((c1 - c2) / (s2 - s1)):.2e}" if s2 > s1
              else "регрессээр огтлолцохгүй (налуу нь бага биш)")
    return (f"хэмжсэн мужид олдсонгүй; n={n} үед {ratio:.1f} дахин удаан → "
            f"онолын илтгэгчээр n₀ ≈ {n0:.2e}; {by_fit}")


def main() -> None:
    langs = {lang: load(lang) for lang in ("python", "java")}

    print("## (c) log–log налуу (n-ийн хамгийн их 3 цэг)\n")
    print("| Хэл | Алгоритм | n (3 цэг) | Налуу | Онол |")
    print("| --- | --- | --- | ---: | ---: |")
    for lang, data in langs.items():
        for alg in ALGS:
            if len(data[alg]) >= 3:
                s, _ = fit(data[alg])
                ns = ", ".join(str(n) for n in sorted(data[alg])[-3:])
                print(f"| {lang} | {alg} | {ns} | {s:.3f} | {THEORY[alg]:.3f} |")

    print("\n## (e) Штрассен хурдан болох цэг\n")
    for lang, data in langs.items():
        # cutoff64 хувилбар n ≤ 64 үед давталттай аргатай яг ижил тул n > 64-өөс харьцуулна.
        for alg, min_n in (("strassen", 1), ("strassen_cutoff64", 128)):
            if data[alg]:
                print(f"- {lang}, {alg}: < дахин дуудах: "
                      f"{crossover(data, alg, 'matrix_multiply_recursive', min_n)}; "
                      f"< давталттай: {crossover(data, alg, 'matrix_multiply', min_n)}")

    print("\n## (f) matrix_multiply: Python / Java хугацааны харьцаа\n")
    py, jv = langs["python"]["matrix_multiply"], langs["java"]["matrix_multiply"]
    print("| n | Python, ms | Java, ms | Харьцаа |")
    print("| ---: | ---: | ---: | ---: |")
    for n in sorted(set(py) & set(jv)):
        ratio = f"{py[n] / jv[n]:.1f}" if jv[n] > 0 else "—"
        print(f"| {n} | {py[n]:.3f} | {jv[n]:.3f} | {ratio} |")

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib олдсонгүй — график зурсангүй")
        return
    DOCS.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5.5))
    styles = {"python": "-", "java": "--"}
    for lang, data in langs.items():
        for alg in ALGS:
            pts = {n: t for n, t in data[alg].items() if t > 0}  # log шкалд 0-ийг зурахгүй
            if pts:
                ns = sorted(pts)
                ax.plot(ns, [pts[n] for n in ns], styles[lang], marker="o", label=f"{lang}: {alg}")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=10)
    ax.set_xlabel("n (матрицын хэмжээ)")
    ax.set_ylabel("хугацаа, ms")
    ax.set_title("Матриц үржүүлэх — log–log")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    path = DOCS / "benchmark_loglog.png"
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    print(f"\n  -> {path}")


if __name__ == "__main__":
    main()

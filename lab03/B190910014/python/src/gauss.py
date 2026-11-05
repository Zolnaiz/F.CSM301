from operator import mul


def gauss_solve(a: list[list[float]], b: list[float]) -> tuple[list[float], int]:
    """Гауссын арга (мөрийн хувиргалтгүй). Шийд x ба *, /, +, - үйлдлийн тоог буцаана."""
    n = len(a)
    if len(b) != n or any(len(row) != n for row in a):
        raise ValueError("A нь n×n, b нь n урттай байх ёстой")
    m = [[float(v) for v in row] for row in a]  # оролтыг өөрчлөхгүйн тулд хуулна
    v = [float(x) for x in b]
    ops = 0

    # Шууд явц: k-р баганын доорх гишүүдийг тэглэнэ.
    for k in range(n - 1):
        if m[k][k] == 0:
            raise ValueError("хувиргалтын гишүүн тэг боллоо")
        for i in range(k + 1, n):
            factor = m[i][k] / m[k][k]
            ops += 1
            for j in range(k, n):
                m[i][j] = m[i][j] - factor * m[k][j]
                ops += 2
            v[i] = v[i] - factor * v[k]
            ops += 2

    # Буцах орлуулга: доороос дээш x-ийг олно.
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = 0.0
        for j in range(i + 1, n):
            s = s + m[i][j] * x[j]
            ops += 2
        x[i] = (v[i] - s) / m[i][i]
        ops += 2
    return x, ops


def gauss_ops(n: int) -> int:
    """gauss_solve-ийн үйлдлийн тоо: (4n³ + 15n² − 7n) / 6 ≈ ⅔n³."""
    return (4 * n**3 + 15 * n**2 - 7 * n) // 6


def gauss_solve_fast(a: list[list[float]], b: list[float]) -> tuple[list[float], int]:
    """Сайжруулсан Гаусс (A түвшин). Хариу gauss_solve-тэй ижил.

    1. k-р баганыг тэглэх үйлдлийг тооцоолохгүй — мэдээж 0 тул шууд 0 гэж онооно:
       мөр бүрд j = k+1..n−1 л шинэчилнэ (үйлдэл (4n³+15n²−7n)/6 → (4n³+9n²−n)/6).
    2. Мөрийг нэг дор (zip, жагсаалтын хураангуй) шинэчилж, тайлбарлагчийн давталтын зардлыг бууруулна.
    3. Тэргүүлэх мөрийн сүүлийг k бүрд нэг удаа хуулж, мөр бүрд дахин зүсэхгүй.
    """
    n = len(a)
    if len(b) != n or any(len(row) != n for row in a):
        raise ValueError("A нь n×n, b нь n урттай байх ёстой")
    m = [[float(v) for v in row] for row in a]
    v = [float(x) for x in b]
    ops = 0
    for k in range(n - 1):
        pivot = m[k][k]
        if pivot == 0:
            raise ValueError("хувиргалтын гишүүн тэг боллоо")
        tail = m[k][k + 1:]
        vk = v[k]
        for i in range(k + 1, n):
            row = m[i]
            factor = row[k] / pivot
            row[k] = 0.0
            row[k + 1:] = [x - factor * y for x, y in zip(row[k + 1:], tail)]
            v[i] -= factor * vk
        rows = n - 1 - k
        ops += rows * (1 + 2 * rows + 2)  # хуваах + (n−k−1) үржүүлэх/хасах + b
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        row = m[i]
        s = sum(row[j] * x[j] for j in range(i + 1, n))
        x[i] = (v[i] - s) / row[i]
        ops += 2 * (n - 1 - i) + 2
    return x, ops


def gauss_fast_ops(n: int) -> int:
    """gauss_solve_fast-ийн үйлдлийн тоо: (4n³ + 9n² − n) / 6 (анхныхаас n(n−1)-ээр бага)."""
    return (4 * n**3 + 9 * n**2 - n) // 6


def jacobi_solve(a: list[list[float]], b: list[float], tol: float = 1e-12,
                 max_iter: int = 1000) -> tuple[list[float], int, int]:
    """Якобийн давталтын арга (A түвшин, Гауссын «илүү энгийн» өрсөлдөгч). (x, ops, давталт).

    x⁽ᵗ⁺¹⁾ᵢ = (bᵢ − Σⱼ≠ᵢ aᵢⱼ x⁽ᵗ⁾ⱼ) / aᵢᵢ. A мөр бүрээрээ хатуу диагональ давамгай бол ямар ч
    анхны x-ээс нийлнэ (‖D⁻¹(L+U)‖∞ < 1). Нэг давталт нь мөр бүрд Σ-г 0-ээс хуримтлуулах 2(n−1),
    хасах ба хуваах 2 буюу нийт 2n² үйлдэл — 3-р бодлогын матриц–вектор үржүүлэлттэй ижил.
    max|Δx| ≤ tol·max(1, max|x|) болоход зогсоно (харьцуулалтыг үйлдэлд тооцохгүй).
    """
    n = len(a)
    if len(b) != n or any(len(row) != n for row in a):
        raise ValueError("A нь n×n, b нь n урттай байх ёстой")
    m = [[float(v) for v in row] for row in a]
    for i, row in enumerate(m):
        if abs(row[i]) <= sum(abs(v) for v in row) - abs(row[i]):
            raise ValueError("Якобийн арга хатуу диагональ давамгай матриц шаардана")
    if n == 0:
        return [], 0, 0
    v = [float(x) for x in b]
    x = [0.0] * n
    for it in range(1, max_iter + 1):
        new = [(vi - (sum(map(mul, row, x)) - row[i] * x[i])) / row[i]
               for i, (row, vi) in enumerate(zip(m, v))]
        delta = max(abs(p - q) for p, q in zip(new, x))
        x = new
        if delta <= tol * max(1.0, max(abs(t) for t in x)):
            return x, it * 2 * n * n, it
    raise ValueError(f"Якобийн давталт {max_iter} алхамд нийлсэнгүй")

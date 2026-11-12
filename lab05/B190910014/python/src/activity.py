def activity_select(s: list[int], f: list[int]) -> list[int]:
    """Ажиллагааг түүвэрлэх: хамгийн эрт дуусахыг сонгох хомхойлох арга.

    Ажиллагааг дуусах хугацаагаар эрэмбэлээд (Θ(n lg n)), өмнө сонгосны дуусах хугацаанаас
    хойш (s ≥ f) эхэлсэн эхний ажиллагааг сонгоно (Θ(n)). Интервалыг [s, f) гэж үзнэ.
    Сонгосон ажиллагааны 1-ээс эхэлсэн дугаарыг сонгосон дарааллаар буцаана.
    """
    if len(s) != len(f):
        raise ValueError("s, f ижил урттай байх ёстой")
    order = sorted(range(len(s)), key=lambda i: f[i])
    chosen: list[int] = []
    last_finish = None
    for i in order:
        if last_finish is None or s[i] >= last_finish:
            chosen.append(i + 1)
            last_finish = f[i]
    return chosen


def shortest_first(s: list[int], f: list[int]) -> list[int]:
    """Шинжилгээ (б), (в): хамгийн богино ажиллагааг сонгох (оновчгүй) дүрэм."""
    order = sorted(range(len(s)), key=lambda i: f[i] - s[i])
    chosen: list[int] = []
    for i in order:
        if all(s[i] >= f[j - 1] or s[j - 1] >= f[i] for j in chosen):
            chosen.append(i + 1)
    return chosen

# F.CSM301 — Алгоритмын зохиомж ба шинжилгээ (2026 намар)

Оюутан: **B190910014** · Хэл: **Python, Java**

Хичээлийн лабораторийн болон бие даалтын ажлуудын хувийн хуулбар. Ажлыг багшийн
[GitLab сан](https://gitlab.com/batmunkh.d/f.csm301-2627) уруу merge request-ээр илгээдэг.
Энэ сан нь зөвхөн хадгалах зориулалттай.

| Ажил | Сэдэв | Тайлан | MR | Төлөв |
| ---- | ----- | ------ | -- | ----- |
| [Лаб 1](lab01/B190910014) | Орчин бэлтгэх, Фибоначчи, анаграмм | [lab01_report.md](lab01/B190910014/lab01_report.md) | [!61](https://gitlab.com/batmunkh.d/f.csm301-2627/-/merge_requests/61) | ✅ merged |
| [Лаб 2](lab02/B190910014) | Эрэмбэлэлт, хоёртын хайлт, дарааллын зөрөө | [lab02_report.md](lab02/B190910014/lab02_report.md) | [!60](https://gitlab.com/batmunkh.d/f.csm301-2627/-/merge_requests/60) | ✅ merged |
| [Лаб 3](lab03/B190910014) | Ерөнхий арга, матриц үржүүлэх, Штрассен, Гаусс | [lab03_report.md](lab03/B190910014/lab03_report.md) | [!146](https://gitlab.com/batmunkh.d/f.csm301-2627/-/merge_requests/146) | ⏳ хүлээгдэж буй |
| [Лаб 4](lab04/B190910014) | Динамик программчлал: ган саваа, матрицын цуваа, LCS, diff | [lab04_report.md](lab04/B190910014/lab04_report.md) | [!154](https://gitlab.com/batmunkh.d/f.csm301-2627/-/merge_requests/154) | ⏳ хүлээгдэж буй |
| [Лаб 5](lab05/B190910014) | Хомхойлох алгоритм: ажиллагаа, үүргэвч, мөнгө, Хаффман, оновчтой кэш | [lab05_report.md](lab05/B190910014/lab05_report.md) | [!186](https://gitlab.com/batmunkh.d/f.csm301-2627/-/merge_requests/186) | ⏳ хүлээгдэж буй |
| [Бие даалт 1](prj1/B190910014) | Хэсэгчлэх ба дахин дуудах арга, A түвшин (5 бодлого + 2 сайжруулалт) | [prj1_report.pdf](prj1/B190910014/report/prj1_report.pdf) | [!153](https://gitlab.com/batmunkh.d/f.csm301-2627/-/merge_requests/153) | ⏳ хүлээгдэж буй |

Шалгуулах бэлтгэл: [шалгуулах_бэлтгэл.md](шалгуулах_бэлтгэл.md)

## Бүтэц

```text
labNN/B190910014/
├── labNN_report.md     тайлан
├── python/             src/, tests/ (pytest)
├── java/               src/main, src/test (Maven, JUnit 5)
├── test_data/          өөрөө зохиосон өгөгдөл
└── online/             LeetCode / Codeforces бодолт, solutions.md
```

## Ажиллуулах

```bash
cd lab03/B190910014/python && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/pytest -v
cd lab03/B190910014/java && mvn test
```

Шалгалтын нийтлэг өгөгдөл (`labNN/test_data/`) болон генераторууд (`labNN/tools/`) багшийн санд
байдаг. Тестийг ажиллуулахдаа хичээлийн сангийн хуулбар дотроос ажиллуулна.

## Шинэчлэх

```bash
./sync.sh    # ../f.csm301-2627 сангаас өөрийн хавтсуудыг дахин хуулна
git add -A && git commit -m "Шинэчлэх" && git push
```

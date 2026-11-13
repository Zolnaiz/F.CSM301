# Бие даалт 2 — B190910014

Графын хайлт, мөрийн хайлт ба хомхойлох алгоритм, **A төвшин** (Python, Java).
Тайлан: [report/prj2_report.pdf](report/prj2_report.pdf) (pdfLaTeX эх: [report/prj2_report.tex](report/prj2_report.tex)).

| № | Бодлого | Python | Java |
| - | ------- | ------ | ---- |
| 1 | LeetCode 28 Find the Index of the First Occurrence in a String (KMP) | `p1_str_str.py` | `StrStr.java` |
| 2 | LeetCode 733 Flood Fill (BFS) | `p2_flood_fill.py` | `FloodFill.java` |
| 3 | LeetCode 455 Assign Cookies (хомхойлох) | `p3_assign_cookies.py` | `AssignCookies.java` |
| 4 | LeetCode 45 Jump Game II (ДП → хомхойлох) | `p4_jump_game.py`, `…_improved.py` | `JumpGame.java`, `…Improved.java` |
| 5 | LeetCode 752 Open the Lock (BFS → хоёр талын BFS) | `p5_open_lock.py`, `…_improved.py` | `OpenLock.java`, `…Improved.java` |

```bash
# Тест
cd python && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/pytest -v
cd java && mvn test

# Хэмжилт → out/results_<lang>.tsv
cd python && python3 bench.py
cd java && javac -d build src/main/java/com/prj2/*.java && java -Xss64m -cp build com.prj2.Bench

# Тайлан: хүснэгт шинэчлэх, PDF үүсгэх (pdfLaTeX: texlive-latex-extra, texlive-lang-cyrillic)
cd report && python3 make_tables.py && ./build.sh
```

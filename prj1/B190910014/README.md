# Бие даалт 1 — B190910014

Хэсэгчлэх ба дахин дуудах арга, **A түвшин** (Python, Java).
Тайлан: [report/prj1_report.pdf](report/prj1_report.pdf) ([Markdown эх](report/prj1_report.md)).

| № | Бодлого | Python | Java |
| - | ------- | ------ | ---- |
| 1 | LeetCode 169 Majority Element | `p1_majority_element.py` | `MajorityElement.java` |
| 2 | LeetCode 108 Convert Sorted Array to BST | `p2_sorted_array_to_bst.py` | `SortedArrayToBst.java` |
| 3 | LeetCode 1763 Longest Nice Substring | `p3_longest_nice_substring.py` | `LongestNiceSubstring.java` |
| 4 | LeetCode 241 Different Ways to Add Parentheses | `p4_different_ways.py`, `…_improved.py` | `DifferentWays.java`, `…Improved.java` |
| 5 | LeetCode 105 Construct Binary Tree from Preorder and Inorder | `p5_build_tree.py`, `…_improved.py` | `BuildTree.java`, `…Improved.java` |

```bash
# Тест
cd python && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/pytest -v
cd java && mvn test

# Хэмжилт → out/results_<lang>.tsv
cd python && python3 bench.py
cd java && javac -d build src/main/java/com/prj1/*.java && java -Xss64m -cp build com.prj1.Bench

# Тайлан: хүснэгт шинэчлэх, PDF үүсгэх (pip install markdown, Chrome/Edge)
cd report && python make_tables.py && python build_pdf.py
```

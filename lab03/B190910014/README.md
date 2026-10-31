# Лаб 3 — B190910014

Хэл: Python, Java. Тайлан: [lab03_report.md](lab03_report.md).
Онлайн бодлого: [online/solutions.md](online/solutions.md).

```bash
# Шалгалт
cd python && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/pytest -v
cd java && mvn test

# Хэмжилт (lab03/B190910014 хавтаснаас)
python3 ../tools/gen_lab03.py B190910014       # test_data/personal_<n>.tsv, n = 2..512
cd python && python3 bench.py                   # -> out/results_python.tsv
cd java && javac -d build src/main/java/com/lab03/*.java && java -cp build com.lab03.Bench
python3 python/analyze.py                       # налуу, n₀, график (matplotlib)
bash env_info.sh                                # орчны мэдээлэл
```

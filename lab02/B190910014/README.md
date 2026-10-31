# Лаб 2 — B190910014

Хэл: Python, Java. Тайлан: [lab02_report.md](lab02_report.md).
Онлайн бодлого: [online/solutions.md](online/solutions.md).

```bash
# Хувийн оролт үүсгэх (5-р даалгаврын хэмжилтэд)
cd lab02/B190910014
python3 ../tools/gen_lab02.py B190910014

# Python
cd python
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest -v
.venv/bin/python experiments.py   # 4(b), 4(c) хүснэгт

# Java
cd java
mvn test
```

Хэмжилтийн үр дүн `out/results_<хэл>.tsv` файлд бичигдэнэ.

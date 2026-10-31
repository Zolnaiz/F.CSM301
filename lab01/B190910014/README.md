# Лаб 1 — B190910014

Хэл: Python, Java. Тайлан: [lab01_report.md](lab01_report.md).

```bash
# Python
cd python
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest -v

# Java
cd java
mvn test
```

Шалгалтын өгөгдөл `test_data/` хавтсанд:

- `fibonacci.tsv`, `fibonacci_invalid.tsv`, `anagrams_01.tsv` — багшийн өгсөн, өөрчлөөгүй
- `fibonacci_my.tsv` — `fibonacci.tsv`-ийн хуулбар, n = 46, 47 нэмсэн
- `anagrams_my.tsv` — өөрөө зохиосон анаграммын тохиолдлууд

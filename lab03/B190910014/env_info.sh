#!/usr/bin/env bash
# Хэмжилт хийсэн орчны мэдээлэл (тайланд хавсаргана).
uname -a
lscpu | grep -E 'Model name|^CPU\(s\)|Thread|Core|Socket|L1d|L2|L3'
free -h | head -2
python3 --version
java -version 2>&1

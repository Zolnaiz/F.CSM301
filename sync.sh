#!/usr/bin/env bash
# Хичээлийн сангаас (../f.csm301-2627) өөрийн ажлыг энэ хавтас руу хуулна.
# Тухайн нэртэй салбар байвал түүнээс, үгүй бол upstream/main-ээс авна.
# Зөвхөн git-д commit хийгдсэн файл хуулагдана (out/, personal_*.tsv, build/ орохгүй).
set -e
cd "$(dirname "$0")"
R=../f.csm301-2627
ID=B190910014

for d in lab01 lab02 lab03 lab04 lab05 lab06 prj1 prj2; do
  if git -C "$R" rev-parse --verify -q "refs/heads/$d" >/dev/null; then
    ref=$d
  else
    ref=upstream/main
  fi
  if git -C "$R" cat-file -e "$ref:$d/$ID" 2>/dev/null; then
    rm -rf "${d:?}/$ID"
    git -C "$R" archive "$ref" "$d/$ID" | tar -x
    echo "$d/$ID <- $ref"
  fi
done

cp ../шалгуулах_бэлтгэл.md .

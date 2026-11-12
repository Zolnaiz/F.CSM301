#!/usr/bin/env bash
# prj1_report.tex → prj1_report.pdf (зөвхөн pdfLaTeX). Гарчиг, холбоосын тулд 2 удаа хөрвүүлнэ.
# Шаардлага (Ubuntu): texlive-latex-extra texlive-lang-cyrillic
set -e
cd "$(dirname "$0")"
mkdir -p build
for _ in 1 2; do
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build prj1_report.tex > build/pdflatex.out \
    || { tail -30 build/pdflatex.out; exit 1; }
done
cp build/prj1_report.pdf .
echo "-> prj1_report.pdf"

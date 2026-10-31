"""prj1_report.md → prj1_report.html → prj1_report.pdf (Chrome/Edge headless).

Ажиллуулах: python build_pdf.py   (pip install markdown)
"""
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
SRC = HERE / "prj1_report.md"
HTML = HERE / "prj1_report.html"
PDF = HERE / "prj1_report.pdf"

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: 'Segoe UI', 'Noto Sans', Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #111; }
h1 { font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 4px; }
h2 { font-size: 14pt; margin-top: 22px; border-bottom: 1px solid #999; padding-bottom: 2px; page-break-after: avoid; }
h3 { font-size: 11.5pt; margin-top: 14px; page-break-after: avoid; }
table { border-collapse: collapse; margin: 8px 0; font-size: 9.5pt; page-break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 3px 7px; }
th { background: #eee; }
td { text-align: right; } td:first-child, td:nth-child(2) { text-align: left; }
code { font-family: Consolas, 'DejaVu Sans Mono', monospace; font-size: 9pt; background: #f4f4f4; padding: 0 2px; }
pre { background: #f6f6f6; border: 1px solid #ddd; padding: 8px; font-size: 8.8pt; line-height: 1.3;
      white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
.title { text-align: center; margin-top: 30mm; }
.title h1 { border: none; font-size: 22pt; }
.pagebreak { page-break-after: always; }
"""


def browser() -> str:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        shutil.which("chromium") or "", shutil.which("google-chrome") or "",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    sys.exit("Chrome/Edge олдсонгүй")


def main() -> None:
    body = markdown.markdown(SRC.read_text(encoding="utf-8"),
                             extensions=["tables", "fenced_code", "md_in_html"])
    HTML.write_text(f"<!doctype html><html lang='mn'><head><meta charset='utf-8'>"
                    f"<title>Бие даалт 1 — B190910014</title><style>{CSS}</style></head>"
                    f"<body>{body}</body></html>", encoding="utf-8")
    subprocess.run([browser(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={PDF}", HTML.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"-> {PDF}")


if __name__ == "__main__":
    main()

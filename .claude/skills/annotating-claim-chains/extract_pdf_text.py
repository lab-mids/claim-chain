"""Extract the text of a PDF page by page, for reading before annotation.

Usage: python -I extract_pdf_text.py paper.pdf > paper.txt
Requires pypdf (pip install pypdf). Figures are not extracted; only their captions appear.
"""
import sys

import pypdf

reader = pypdf.PdfReader(sys.argv[1])
for i, page in enumerate(reader.pages, start=1):
    print(f"=== PAGE {i} ===")
    print(page.extract_text() or "")

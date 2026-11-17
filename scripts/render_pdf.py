"""Render PDF booking ANEX (ban scan, khong co lop chu) thanh PNG tung trang de doc bang mat.
Chay: python -I -X utf8 render_pdf.py "<file.pdf>" "<thu_muc_ra>" [zoom=2.2]
Can: pip install pymupdf
"""
import sys, os
import fitz  # pymupdf

pdf, outdir = sys.argv[1], sys.argv[2]
zoom = float(sys.argv[3]) if len(sys.argv) > 3 else 2.2
os.makedirs(outdir, exist_ok=True)
doc = fitz.open(pdf)
for i, page in enumerate(doc, 1):
    p = os.path.join(outdir, 'trang_%02d.png' % i)
    page.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(p)
    print(p)
print('so trang:', len(doc))

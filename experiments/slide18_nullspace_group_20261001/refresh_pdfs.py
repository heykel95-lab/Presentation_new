from pathlib import Path
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
original = PdfReader(HERE / 'archive/Thesis_Defense_gg0_v3.pdf')
rendered = PdfReader(HERE / 'native_export.pdf')
assert len(original.pages) == len(rendered.pages) == 31
full = PdfWriter()
for index, page in enumerate(original.pages):
    full.add_page(rendered.pages[index] if index == 18 else page)
if original.metadata:
    full.add_metadata({str(k): str(v) for k, v in original.metadata.items() if v is not None})
full.write(HERE / 'Thesis_Defense_gg0_v3.pdf')
supplement = PdfWriter()
for page in full.pages[26:]:
    supplement.add_page(page)
supplement.write(HERE / 'Supplementary_slides.pdf')
print('Replaced physical page 19 and retained the other 30 original pages.')

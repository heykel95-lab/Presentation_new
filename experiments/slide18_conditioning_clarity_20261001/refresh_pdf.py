from pathlib import Path
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
original = PdfReader(HERE / 'archive/Thesis_Defense_gg0_v3.pdf')
native = PdfReader(HERE / 'native_export.pdf')
assert len(original.pages) == 31 and len(native.pages) == 1
output = PdfWriter()
for index, page in enumerate(original.pages):
    output.add_page(native.pages[0] if index == 18 else page)
if original.metadata:
    output.add_metadata({str(k): str(v) for k, v in original.metadata.items() if v is not None})
output.write(HERE / 'Thesis_Defense_gg0_v3.pdf')
print('Replaced physical page 19; all other pages retained.')

from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import ContentStream

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
original = PdfReader(HERE / 'archive/Thesis_Defense_gg0_v3.pdf')
native = PdfReader(HERE / 'native_export.pdf')
assert len(original.pages) == 31 and len(native.pages) == 2
modified = {}
for i, figure in enumerate(['force_plausibility', 'moment_plausibility']):
    page = native.pages[i]
    objects = page['/Resources']['/XObject']
    chart_names = [name for name, ref in objects.items()
                   if ref.get_object().get('/Subtype') == '/Image'
                   and ref.get_object().get('/Width', 0) > 1000]
    assert len(chart_names) == 1
    stream = ContentStream(page.get_contents(), native)
    removed = 0
    kept = []
    for operands, operator in stream.operations:
        if operator == b'Do' and operands[0] == chart_names[0]:
            removed += 1
        else:
            kept.append((operands, operator))
    assert removed == 1
    stream.operations = kept
    page.replace_contents(stream)
    del objects[chart_names[0]]
    vector = PdfReader(FINAL / 'figures_and_images' / (figure + '.pdf'))
    source = vector.pages[0]
    width, height = 650, 269.6105511811024
    transform = Transformation().scale(width / float(source.mediabox.width), height / float(source.mediabox.height)).translate(155, 540 - 89 - height)
    page.merge_transformed_page(source, transform)
    modified[12 + i] = page

full = PdfWriter()
for index, page in enumerate(original.pages):
    full.add_page(modified.get(index, page))
if original.metadata:
    full.add_metadata({str(k): str(v) for k, v in original.metadata.items() if v is not None})
full.write(HERE / 'Thesis_Defense_gg0_v3.pdf')
supplement = PdfWriter()
for page in full.pages[26:]:
    supplement.add_page(page)
supplement.write(HERE / 'Supplementary_slides.pdf')
print('Refreshed both pages with original vector charts; other 29 pages retained.')

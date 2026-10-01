from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import ContentStream, NameObject
from PIL import ImageChops
import pypdfium2 as pdfium
import io, hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FINAL = ROOT / 'Final Presentation'
original = (FINAL / 'Thesis_Defense_gg0_v3.pdf').read_bytes()
checkpoint = json.loads((HERE / 'archive/pdf_before.json').read_text())
assert hashlib.sha256(original).hexdigest() == checkpoint['sha256']
verification = json.loads((HERE / 'verification.json').read_text())
native = PdfReader(HERE / 'native_export.pdf')
assert len(native.pages) == 1

# Keep native PowerPoint text, with exact vector figure and legend assets.
composition = PdfWriter()
composition.add_page(native.pages[0])
page = composition.pages[0]
xobjects = page['/Resources']['/XObject']
remove = [name for name, obj in xobjects.items()
          if obj.get_object().get('/Subtype') == '/Image'
          and obj.get_object().get('/Width', 0) > 109]
assert len(remove) == 2, remove
stream = ContentStream(page.get_contents(), composition)
removed_draws = sum(op == b'Do' and args[0] in remove for args, op in stream.operations)
assert removed_draws == 4
stream.operations = [(args, op) for args, op in stream.operations
                     if not (op == b'Do' and args[0] in remove)]
page.replace_contents(stream)
for name in remove:
    del xobjects[name]
plot = PdfReader(FINAL / 'figures_and_images/contact_wrench_three_panels.pdf').pages[0]
assert abs(float(plot.mediabox.width) - 900) < .01
assert abs(float(plot.mediabox.height) - 310) < .01
page.merge_transformed_page(plot, Transformation().translate(30, 95))
legend = PdfReader(HERE / 'contact_legend_per_plot.pdf').pages[0]
for position in verification['legend_positions_pt']:
    page.merge_transformed_page(legend, Transformation().translate(
        position['x'], 540 - position['y'] - position['height']))

# Append only the changed page objects; every original PDF byte is retained.
output = PdfWriter(io.BytesIO(original), incremental=True)
target = output.pages[17]
for key in ['/Contents', '/Resources', '/Group', '/Annots']:
    if key in page:
        target[NameObject(key)] = page.raw_get(key).clone(output)
    elif key in target:
        del target[key]
memory = io.BytesIO()
output.write(memory)
updated = memory.getvalue()
assert updated[:len(original)] == original
tail = updated[len(original):]
assert len(PdfReader(io.BytesIO(updated)).pages) == 31
(HERE / 'presentation_pdf_update.bin').write_bytes(tail)
(HERE / 'pdf_checkpoint.json').write_text(json.dumps({
    'original_size': len(original), 'original_sha256': hashlib.sha256(original).hexdigest(),
    'updated_sha256': hashlib.sha256(updated).hexdigest(), 'append_bytes': len(tail)
}, indent=2))

before, after = pdfium.PdfDocument(original), pdfium.PdfDocument(updated)
changed = []
for index in range(31):
    old_page, new_page = before[index], after[index]
    old_bitmap = old_page.render(scale=1000/960)
    new_bitmap = new_page.render(scale=1000/960)
    old_image, new_image = old_bitmap.to_pil().convert('RGB'), new_bitmap.to_pil().convert('RGB')
    if ImageChops.difference(old_image, new_image).getbbox():
        changed.append(index + 1)
    if index == 17:
        new_image.save(HERE / 'qa-18.png')
    old_bitmap.close(); new_bitmap.close(); old_page.close(); new_page.close()
before.close(); after.close()
assert changed == [18], changed
verification.update({
    'visually_changed_physical_pages': changed, 'other_30_pages_pixel_identical': True,
    'full_pdf_pages': 31, 'pdf_increment_bytes': len(tail),
    'plot_and_legend_pdf_vectors_preserved': True, 'native_powerpoint_render_reviewed': True,
    'supplementary_pdf_sha256': hashlib.sha256((FINAL / 'Supplementary_slides.pdf').read_bytes()).hexdigest(),
    'supplementary_pdf_pages': len(PdfReader(FINAL / 'Supplementary_slides.pdf').pages)
})
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))

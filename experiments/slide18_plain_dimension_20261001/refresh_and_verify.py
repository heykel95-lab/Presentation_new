from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, RectangleObject
from PIL import ImageChops
import pypdfium2 as pdfium
import pdfplumber
import hashlib, json, io

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FINAL = ROOT / 'Final Presentation'
ARCHIVE = HERE / 'archive'
original_bytes = (FINAL / 'Thesis_Defense_gg0_v3.pdf').read_bytes()
original_hash = hashlib.sha256(original_bytes).hexdigest()
native = PdfReader(HERE / 'native_export.pdf')
assert len(native.pages) == 1

# Store the exact original PDF as a lossless binary delta against the retained
# immutable base, so no full-size copy is needed on the almost-full drive.
base_path = ROOT / 'experiments/slide17_proportions_20261001/archive/Thesis_Defense_gg0_v3.pdf'
base = base_path.read_bytes()
operations, literal = [], bytearray()
for start in range(0, len(original_bytes), 8192):
    block = original_bytes[start:start+8192]
    found = base.find(block)
    if found >= 0:
        kind, offset = 'copy', found
    else:
        kind, offset = 'data', len(literal)
        literal.extend(block)
    if operations and operations[-1][0] == kind and operations[-1][1] + operations[-1][2] == offset:
        operations[-1][2] += len(block)
    else:
        operations.append([kind, offset, len(block)])
metadata = {'base': str(base_path.relative_to(ROOT)), 'base_sha256': hashlib.sha256(base).hexdigest(),
            'original_sha256': original_hash, 'original_size': len(original_bytes), 'operations': operations}
delta_path = ARCHIVE / 'Thesis_Defense_gg0_v3.pdf.delta.zip'
with ZipFile(delta_path, 'w', ZIP_DEFLATED) as archive:
    archive.writestr('manifest.json', json.dumps(metadata))
    archive.writestr('literal.bin', literal)
with ZipFile(delta_path) as archive:
    stored = json.loads(archive.read('manifest.json'))
    payload = archive.read('literal.bin')
reconstructed = b''.join((base if kind == 'copy' else payload)[offset:offset+length]
                         for kind, offset, length in stored['operations'])
assert hashlib.sha256(reconstructed).hexdigest() == original_hash
original_link = (ARCHIVE / 'Thesis_Defense_gg0_v3.pdf').resolve()
assert original_link.is_relative_to(ARCHIVE.resolve())
if original_link.exists():
    original_link.unlink()
(ARCHIVE / 'ARCHIVE_STORAGE.txt').write_text(
    'Exact original PDF retained as a verified binary delta. Keep the shared base in its manifest. '
    'Restore with experiments/slide18_conditioning_clarity_20261001/restore_pdf_archive.py.\n')

# An incremental PDF update preserves every original byte and adds only the
# replacement page objects. This avoids writing another 18 MB temporary PDF.
output = PdfWriter(io.BytesIO(original_bytes), incremental=True)
page = output.pages[18]
source_page = native.pages[0]
for key in ['/Contents', '/Resources', '/Group', '/Annots']:
    if key in source_page:
        page[NameObject(key)] = source_page.raw_get(key).clone(output)
    elif key in page:
        del page[key]
memory = io.BytesIO()
output.write(memory)
updated_bytes = memory.getvalue()
assert updated_bytes[:len(original_bytes)] == original_bytes
updated = PdfReader(io.BytesIO(updated_bytes))
assert len(updated.pages) == 31
text = updated.pages[18].extract_text()
assert 'Null space dimension' in text and 'ker' not in text
tail = updated_bytes[len(original_bytes):]
(HERE / 'presentation_pdf_update.bin').write_bytes(tail)
(HERE / 'pdf_checkpoint.json').write_text(json.dumps({
    'original_size': len(original_bytes), 'original_sha256': original_hash,
    'updated_sha256': hashlib.sha256(updated_bytes).hexdigest(), 'append_bytes': len(tail),
}, indent=2))

# Render all 31 old/new pages with the same renderer without writing duplicate
# PNGs. Every unchanged page must remain pixel identical.
before_pdf, after_pdf = pdfium.PdfDocument(original_bytes), pdfium.PdfDocument(updated_bytes)
changed = []
for index in range(31):
    old_page, new_page = before_pdf[index], after_pdf[index]
    old_bitmap, new_bitmap = old_page.render(scale=1000/960), new_page.render(scale=1000/960)
    old_image, new_image = old_bitmap.to_pil().convert('RGB'), new_bitmap.to_pil().convert('RGB')
    if ImageChops.difference(old_image, new_image).getbbox():
        changed.append(index + 1)
    if index == 18:
        new_image.save(HERE / 'qa-19.png')
    old_bitmap.close(); new_bitmap.close(); old_page.close(); new_page.close()
before_pdf.close(); after_pdf.close()
assert changed == [19], changed

# Crop the exact native equation for matching vector/raster source assets.
with pdfplumber.open(HERE / 'native_export.pdf') as pdf:
    chars = pdf.pages[0].crop((70, 215, 540, 255)).chars
    left, top = min(c['x0'] for c in chars) - 3, min(c['top'] for c in chars) - 3
    right, bottom = max(c['x1'] for c in chars) + 3, max(c['bottom'] for c in chars) + 3
equation = PdfWriter()
equation.add_page(native.pages[0])
equation.pages[0].mediabox = RectangleObject((left, 540-bottom, right, 540-top))
equation.pages[0].cropbox = equation.pages[0].mediabox
equation.write(HERE / 'null_controller_dimension.pdf')
verification = json.loads((HERE / 'verification.json').read_text())
verification.update({'visually_changed_physical_pages': changed, 'other_30_pages_pixel_identical': True,
                     'full_pdf_pages': 31, 'pdf_increment_bytes': len(tail),
                     'original_pdf_archived_losslessly': True, 'equation_asset_crop_pt': [left, top, right, bottom]})
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))

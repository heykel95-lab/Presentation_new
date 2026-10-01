from pathlib import Path
from zipfile import ZipFile
from PIL import Image, ImageChops
from pypdf import PdfReader
import hashlib, json, shutil

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
BASELINE = HERE.parent / 'slide21_hold_disturbance_20261001'
changed_pages = []
bounding_boxes = {}
for page in range(1, 32):
    with Image.open(BASELINE / f'qa-{page:02}.png') as old, Image.open(HERE / f'qa-{page:02}.png') as new:
        assert old.size == new.size
        box = ImageChops.difference(old.convert('RGB'), new.convert('RGB')).getbbox()
        if box:
            changed_pages.append(page)
            bounding_boxes[page] = box
assert changed_pages == [19], changed_pages
with Image.open(BASELINE / 'qa-19.png') as old, Image.open(HERE / 'qa-19.png') as new:
    difference = ImageChops.difference(old.convert('RGB'), new.convert('RGB'))
    assert difference.crop((0, 220, 1000, 520)).getbbox() is None
    footer_difference = difference.crop((0, 520, 1000, 563)).getbbox()
    assert footer_difference == (21, 3, 63, 25), footer_difference

before = json.loads((HERE / 'archive/package_hashes_before.json').read_text())
with ZipFile(FINAL / 'Thesis_Defense_gg0_v3.pptx') as deck:
    assert set(deck.namelist()) == set(before)
    changed_parts = [n for n in deck.namelist()
                     if hashlib.sha256(deck.read(n)).hexdigest() != before[n]]
    assert changed_parts == ['ppt/slides/slide10.xml']
assert len(PdfReader(HERE / 'Thesis_Defense_gg0_v3.pdf').pages) == 31
assert len(PdfReader(HERE / 'Supplementary_slides.pdf').pages) == 5

for name in ['Thesis_Defense_gg0_v3.pdf', 'Supplementary_slides.pdf']:
    shutil.copy2(HERE / name, FINAL / name)

verification = json.loads((HERE / 'verification.json').read_text())
verification.update({
    'visually_changed_physical_pages': changed_pages,
    'change_bounds_at_1000px': bounding_boxes,
    'other_30_pages_pixel_identical': True,
    'equations_and_lower_torque_sections_pixel_identical': True,
    'native_pdf_export_footer_logo_rasterization_only': 'The unchanged HM logo re-rasterized within x=21..63, y=523..545 at 1000px; its PowerPoint package source is unchanged.',
    'pdf_pages': 31, 'supplementary_pages': 5,
    'native_render_visually_checked': True,
    'active_deliverables_updated': True,
})
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
readme = FINAL / 'README.txt'
entry = ("2026-10-01: Null-space controller (footer 18 / physical slide 19) now combines "
         "the two upper sections under Redundancy and null-space motion, with one bullet "
         "linking the full-rank redundant direction to coordinated joint motion that "
         "preserves instantaneous EE motion. Removed Primary Cartesian task. Both native "
         "equations and the damping/conditioning sections are unchanged. Updated both "
         "presentation PDFs; the other 30 pages, all notes, speaking files and media are "
         "preserved. See ../experiments/slide18_nullspace_group_20261001/verification.json.\n\n")
readme.write_text(entry + readme.read_text(encoding='utf-8'), encoding='utf-8')
print(json.dumps(verification, indent=2))

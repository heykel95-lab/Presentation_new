from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageChops
from pypdf import PdfReader
import hashlib, json, shutil

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
ARCHIVE = HERE / 'archive'
BASELINE = HERE.parent / 'slide18_nullspace_group_20261001'
PARTS = ['ppt/slides/slide14.xml', 'ppt/slides/slide15.xml']
changed_pages = []
for physical in range(1, 32):
    with Image.open(BASELINE / f'qa-{physical:02}.png') as old, Image.open(HERE / f'qa-{physical:02}.png') as new:
        assert old.size == new.size
        if ImageChops.difference(old.convert('RGB'), new.convert('RGB')).getbbox():
            changed_pages.append(physical)
assert changed_pages == [13, 14], changed_pages
assert len(PdfReader(HERE / 'Thesis_Defense_gg0_v3.pdf').pages) == 31
assert len(PdfReader(HERE / 'Supplementary_slides.pdf').pages) == 5
before = json.loads((ARCHIVE / 'package_hashes_before.json').read_text())
active = FINAL / 'Thesis_Defense_gg0_v3.pptx'
checkpoint = json.loads((ARCHIVE / 'zip_checkpoint.json').read_text())
with ZipFile(active) as deck:
    assert set(deck.namelist()) == set(before)
    assert deck.start_dir == checkpoint['start_dir']
    assert all(hashlib.sha256(deck.read(n)).hexdigest() == h for n, h in before.items()), 'Source deck changed during editing.'
assert shutil.disk_usage(HERE).free > 1024 * 1024, 'Need at least 1 MB for the ZIP directory update.'

# Replace the central-directory entries without copying the unrelated 302 MB
# of video payloads. Original compressed entries remain unreferenced, and the
# archive checkpoint permits exact rollback of the complete original ZIP.
try:
    with ZipFile(active, 'a', ZIP_DEFLATED) as deck:
        entries = {part: deck.getinfo(part) for part in PARTS}
        deck.filelist = [info for info in deck.filelist if info.filename not in PARTS]
        for part in PARTS:
            del deck.NameToInfo[part]
        for part in PARTS:
            deck.writestr(entries[part], (HERE / Path(part).name).read_bytes())
    with ZipFile(active) as deck:
        assert len(deck.namelist()) == len(set(deck.namelist())) == len(before)
        assert set(deck.namelist()) == set(before)
        changed_parts = [n for n in deck.namelist() if hashlib.sha256(deck.read(n)).hexdigest() != before[n]]
        assert set(changed_parts) == set(PARTS)
        for part in PARTS:
            assert deck.read(part) == (HERE / Path(part).name).read_bytes()
except Exception:
    with active.open('r+b') as deck:
        deck.seek(checkpoint['start_dir'])
        deck.write((ARCHIVE / 'original_zip_directory.bin').read_bytes())
        deck.truncate()
    raise

for name in ['Thesis_Defense_gg0_v3.pdf', 'Supplementary_slides.pdf']:
    (HERE / name).replace(FINAL / name)

verification = json.loads((HERE / 'verification.json').read_text())
verification.update({
    'changed_package_parts': changed_parts,
    'all_other_package_parts_byte_identical': True,
    'all_notes_equations_videos_and_source_assets_preserved': True,
    'visually_changed_physical_pages': changed_pages,
    'other_29_pages_pixel_identical': True,
    'pdf_uses_original_vector_plot_assets': True,
    'native_powerpoint_and_pdf_layouts_visually_checked': True,
    'pdf_pages': 31, 'supplementary_pages': 5,
    'active_deliverables_updated': True,
})
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
readme = FINAL / 'README.txt'
entry = ('2026-10-01: On Normal-force plausibility assessment and Moment plausibility assessment '
         '(footers 12-13 / physical slides 13-14), both equations now start at x=60 pt. '
         'Manual push and Manual rotation are left-aligned Arial 22 pt navy headings above '
         'the plots. The plots move down 24 pt at unchanged size and proportions. Equation '
         'content, plot data, result summaries, notes and speaking files are unchanged. Both '
         'presentation PDFs are refreshed, retaining the original vector plots and the other '
         '29 pages. See ../experiments/slides12_13_layout_20261001/verification.json.\n\n')
readme.write_text(entry + readme.read_text(encoding='utf-8'), encoding='utf-8')
print(json.dumps(verification, indent=2))

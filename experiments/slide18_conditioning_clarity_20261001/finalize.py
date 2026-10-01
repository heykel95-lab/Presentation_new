from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageChops
from pypdf import PdfReader
import hashlib, json, shutil

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
ARCHIVE = HERE / 'archive'
BASELINE = HERE.parent / 'slides12_13_layout_20261001'
PART = 'ppt/slides/slide10.xml'
changed_pages = []
for physical in range(1, 32):
    with Image.open(BASELINE / f'qa-{physical:02}.png') as old, Image.open(HERE / f'qa-{physical:02}.png') as new:
        assert old.size == new.size
        if ImageChops.difference(old.convert('RGB'), new.convert('RGB')).getbbox():
            changed_pages.append(physical)
assert changed_pages == [19], changed_pages
assert len(PdfReader(HERE / 'Thesis_Defense_gg0_v3.pdf').pages) == 31
supplementary = FINAL / 'Supplementary_slides.pdf'
supplementary_hash = hashlib.sha256(supplementary.read_bytes()).hexdigest()
assert len(PdfReader(supplementary).pages) == 5
before = json.loads((ARCHIVE / 'package_hashes_before.json').read_text())
active = FINAL / 'Thesis_Defense_gg0_v3.pptx'
checkpoint = json.loads((ARCHIVE / 'zip_checkpoint.json').read_text())
with ZipFile(active) as deck:
    assert set(deck.namelist()) == set(before)
    assert deck.start_dir == checkpoint['start_dir']
    assert all(hashlib.sha256(deck.read(n)).hexdigest() == h for n, h in before.items()), 'Source deck changed during editing.'
assert shutil.disk_usage(HERE).free > 1024 * 1024
try:
    with ZipFile(active, 'a', ZIP_DEFLATED) as deck:
        entry = deck.getinfo(PART)
        deck.filelist = [info for info in deck.filelist if info.filename != PART]
        del deck.NameToInfo[PART]
        deck.writestr(entry, (HERE / 'slide10.xml').read_bytes())
    with ZipFile(active) as deck:
        assert len(deck.namelist()) == len(set(deck.namelist())) == len(before)
        assert set(deck.namelist()) == set(before)
        changed_parts = [n for n in deck.namelist() if hashlib.sha256(deck.read(n)).hexdigest() != before[n]]
        assert changed_parts == [PART]
        assert deck.read(PART) == (HERE / 'slide10.xml').read_bytes()
except Exception:
    with active.open('r+b') as deck:
        deck.seek(checkpoint['start_dir'])
        deck.write((ARCHIVE / 'original_zip_directory.bin').read_bytes())
        deck.truncate()
    raise
(HERE / 'Thesis_Defense_gg0_v3.pdf').replace(FINAL / 'Thesis_Defense_gg0_v3.pdf')
assert hashlib.sha256(supplementary.read_bytes()).hexdigest() == supplementary_hash

verification = json.loads((HERE / 'verification.json').read_text())
verification.update({
    'changed_package_parts': changed_parts,
    'all_other_package_parts_byte_identical': True,
    'visually_changed_physical_pages': changed_pages,
    'other_30_pages_pixel_identical': True,
    'native_powerpoint_and_pdf_layouts_visually_checked': True,
    'pdf_pages': 31, 'supplementary_pages': 5,
    'supplementary_pdf_unchanged_and_current': True,
    'active_deliverables_updated': True,
})
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
readme = FINAL / 'README.txt'
entry = ('2026-10-01: Null-space controller (footer 18 / physical slide 19) now explains '
         'conditioning with two short bullets: it adjusts joint posture in the null space '
         'and seeks postures away from singularities, where the EE loses a motion direction. '
         'The term Conditioning torque is retained for consistency with the results; it is '
         'not described as joint-position reference tracking. Only this text box changed. '
         'Updated the full presentation PDF; all other 30 pages, equations, notes, media, '
         'speaking files and the five-page supplementary PDF are unchanged. See '
         '../experiments/slide18_conditioning_clarity_20261001/verification.json.\n\n')
readme.write_text(entry + readme.read_text(encoding='utf-8'), encoding='utf-8')
for folder in ['slides12_13_layout_20261001', 'slide18_nullspace_group_20261001', 'slide21_hold_disturbance_20261001']:
    archive = HERE.parent / folder / 'archive'
    explanation = ('The original full PDF is retained losslessly as Thesis_Defense_gg0_v3.pdf.delta.zip.\n'
                   'Its manifest records the original size, SHA256, and shared base path. All original '
                   'bytes were reconstructed and verified before replacing the redundant full copy.\n'
                   'Shared base (keep): experiments/slide17_proportions_20261001/archive/Thesis_Defense_gg0_v3.pdf\n'
                   'Restore from the workspace with:\npython experiments/slide18_conditioning_clarity_20261001/restore_pdf_archive.py '
                   + str((archive / 'Thesis_Defense_gg0_v3.pdf.delta.zip').relative_to(HERE.parents[1])) + '\n'
                   'Unchanged supplementary PDF bytes are retained in Final Presentation/Supplementary_slides.pdf.\n')
    (archive / 'ARCHIVE_STORAGE.txt').write_text(explanation, encoding='utf-8')
print(json.dumps(verification, indent=2))

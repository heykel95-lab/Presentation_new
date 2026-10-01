from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from pypdf import PdfReader
import hashlib, json, os

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
PART='ppt/slides/slide13.xml'
deck_path=FINAL/'Thesis_Defense_gg0_v3.pptx'
pdf_path=FINAL/'Thesis_Defense_gg0_v3.pdf'
before=json.loads((ARCHIVE/'package_hashes_before.json').read_text())
zip_checkpoint=json.loads((ARCHIVE/'zip_checkpoint.json').read_text())
pdf_checkpoint=json.loads((HERE/'pdf_checkpoint.json').read_text())
verification=json.loads((HERE/'verification.json').read_text())
assert verification['other_30_pages_pixel_identical']
with ZipFile(deck_path) as deck:
    assert set(deck.namelist())==set(before)
    assert deck.start_dir==zip_checkpoint['start_dir']
    assert all(hashlib.sha256(deck.read(n)).hexdigest()==h for n,h in before.items())
assert pdf_path.stat().st_size==pdf_checkpoint['original_size']
assert hashlib.sha256(pdf_path.read_bytes()).hexdigest()==pdf_checkpoint['original_sha256']
try:
    with ZipFile(deck_path,'a',ZIP_DEFLATED) as deck:
        entry=deck.getinfo(PART)
        deck.filelist=[info for info in deck.filelist if info.filename!=PART]
        del deck.NameToInfo[PART]
        deck.writestr(entry,(HERE/'slide13.xml').read_bytes())
    with ZipFile(deck_path) as deck:
        assert len(deck.namelist())==len(set(deck.namelist()))==len(before)
        changed=[n for n,h in before.items() if hashlib.sha256(deck.read(n)).hexdigest()!=h]
        assert changed==[PART]
    with pdf_path.open('ab') as pdf:
        pdf.write((HERE/'presentation_pdf_update.bin').read_bytes())
        pdf.flush();os.fsync(pdf.fileno())
    assert hashlib.sha256(pdf_path.read_bytes()).hexdigest()==pdf_checkpoint['updated_sha256']
    assert len(PdfReader(pdf_path).pages)==31
except Exception:
    with deck_path.open('r+b') as deck:
        deck.seek(zip_checkpoint['start_dir'])
        deck.write((ARCHIVE/'original_zip_directory.bin').read_bytes());deck.truncate()
    with pdf_path.open('r+b') as pdf:pdf.truncate(pdf_checkpoint['original_size'])
    raise
assert hashlib.sha256((FINAL/'Supplementary_slides.pdf').read_bytes()).hexdigest()==verification['supplementary_pdf_sha256']
readme=FINAL/'README.txt'
entry=('2026-10-01: On Null-space experiment (footer 21 / physical slide 22), '
       'swapped the damping and conditioning bullet positions. Conditioning is now top-right '
       'and damping bottom-left. Their complete text, parameters, fonts and bullet styling '
       'are unchanged. Updated PowerPoint and the full PDF; the other 30 pages, speaking '
       'material and supplementary PDF are unchanged. '
       'See ../experiments/slide21_swap_settings_20261001/verification.json.\n\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
agents=ROOT/'AGENTS.md'
contents=agents.read_text(encoding='utf-8')
old='Keep the lower settings row at y = 435 pt to allow room for that label.\n'
new=('Keep the lower settings row at y = 435 pt to allow room for that label.\n'
     'At the user request, conditioning is top-right at (510, 365) pt and\n'
     'damping is bottom-left at (60, 435) pt; the baseline and combined\n'
     'conditions retain their positions. See\n'
     'experiments/slide21_swap_settings_20261001/verification.json.\n')
assert old in contents
agents.write_text(contents.replace(old,new,1),encoding='utf-8')
verification.update({'changed_package_parts':changed,'all_other_package_parts_byte_identical':True,
    'native_and_pdf_renders_visually_checked':True,'supplementary_pdf_unchanged_and_current':True,
    'active_deliverables_updated':True})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Installed the bullet-position swap in PowerPoint and PDF.')

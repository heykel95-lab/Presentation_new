from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,os

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
DECK=FINAL/'Thesis_Defense_gg0_v3.pptx'
PDF=FINAL/'Thesis_Defense_gg0_v3.pdf'
PART='ppt/slides/slide10.xml'
before=json.loads((ARCHIVE/'package_hashes_before.json').read_text())
zip_checkpoint=json.loads((ARCHIVE/'zip_checkpoint.json').read_text())
pdf_checkpoint=json.loads((HERE/'pdf_checkpoint.json').read_text())
verification=json.loads((HERE/'verification.json').read_text())
assert verification['other_30_pages_pixel_identical']
with ZipFile(DECK) as deck:
    assert deck.start_dir==zip_checkpoint['start_dir']
    assert set(deck.namelist())==set(before)
    assert all(hashlib.sha256(deck.read(n)).hexdigest()==h for n,h in before.items())
assert hashlib.sha256(PDF.read_bytes()).hexdigest()==pdf_checkpoint['original_sha256']
try:
    with ZipFile(DECK,'a',ZIP_DEFLATED) as deck:
        entry=deck.getinfo(PART)
        deck.filelist=[info for info in deck.filelist if info.filename!=PART]
        del deck.NameToInfo[PART]
        deck.writestr(entry,(HERE/'slide10.xml').read_bytes())
    with ZipFile(DECK) as deck:
        assert len(deck.namelist())==len(set(deck.namelist()))==len(before)
        changed=[n for n,h in before.items() if hashlib.sha256(deck.read(n)).hexdigest()!=h]
        assert changed==[PART]
    with PDF.open('ab') as file:
        file.write((HERE/'presentation_pdf_update.bin').read_bytes());file.flush();os.fsync(file.fileno())
    assert hashlib.sha256(PDF.read_bytes()).hexdigest()==pdf_checkpoint['updated_sha256']
except Exception:
    with DECK.open('r+b') as file:
        file.seek(zip_checkpoint['start_dir']);file.write((ARCHIVE/'original_zip_directory.bin').read_bytes());file.truncate()
    with PDF.open('r+b') as file:file.truncate(pdf_checkpoint['original_size'])
    raise
assert hashlib.sha256((FINAL/'Supplementary_slides.pdf').read_bytes()).hexdigest()==verification['supplementary_pdf_sha256']
for name,digest in verification['speaking_file_hashes'].items():assert hashlib.sha256((FINAL/name).read_bytes()).hexdigest()==digest
readme=FINAL/'README.txt'
entry=('2026-10-01: Added the editable label Null-space condition: before the unchanged '
       'J(q) qdot_null = 0 equation on Null-space controller (footer 18 / physical slide 19). '
       'The label matches the adjacent dimension text in regular black Cambria Math, 22 pt. '
       'The equation is moved right to x=741 pt; all native math content, other slide elements, '
       'notes and speaking files are preserved. The full PDF is updated; its other 30 pages '
       'and the supplementary PDF are unchanged. '
       'See ../experiments/slide18_nullspace_condition_label_20261001/verification.json.\n\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
agents=ROOT/'AGENTS.md'
contents=agents.read_text(encoding='utf-8')
heading='# Thesis and presentation workspace\n'
assert contents.startswith(heading)
rule=('\n## Null-space condition label (2026-10-01)\n\n'
      'On Null-space controller (footer 18 / physical slide 19), retain the\n'
      'editable label Null-space condition: before J(q) qdot_null = 0. The\n'
      'label is regular black Cambria Math, 22 pt, matching the adjacent\n'
      'dimension label. Its box starts at (530, 218) pt, with width 205 pt;\n'
      'the unchanged native equation starts at (741, 218) pt. The label is\n'
      'separate from the equation asset. Preserve all equation contents and\n'
      'the revised speaking material. See\n'
      'experiments/slide18_nullspace_condition_label_20261001/verification.json.\n')
agents.write_text(heading+rule+contents[len(heading):],encoding='utf-8')
verification.update({'changed_package_parts':changed,'all_other_package_parts_byte_identical':True,
    'native_render_visually_checked':True,'speaking_files_unchanged':True,
    'supplementary_pdf_unchanged':True,'installed':True})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Saved the Null-space condition label in PowerPoint and PDF.')

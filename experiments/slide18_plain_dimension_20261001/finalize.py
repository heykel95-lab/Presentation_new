from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from pypdf import PdfReader
import hashlib, json, shutil, os

HERE = Path(__file__).resolve().parent
FINAL = HERE.parents[1] / 'Final Presentation'
ASSETS = FINAL / 'figures_and_images'
ARCHIVE = HERE / 'archive'
PART = 'ppt/slides/slide10.xml'
deck_path = FINAL / 'Thesis_Defense_gg0_v3.pptx'
pdf_path = FINAL / 'Thesis_Defense_gg0_v3.pdf'
before = json.loads((ARCHIVE / 'package_hashes_before.json').read_text())
zip_checkpoint = json.loads((ARCHIVE / 'zip_checkpoint.json').read_text())
pdf_checkpoint = json.loads((HERE / 'pdf_checkpoint.json').read_text())
with ZipFile(deck_path) as deck:
    assert set(deck.namelist()) == set(before)
    assert deck.start_dir == zip_checkpoint['start_dir']
    assert all(hashlib.sha256(deck.read(n)).hexdigest() == h for n, h in before.items())
assert pdf_path.stat().st_size == pdf_checkpoint['original_size']
assert hashlib.sha256(pdf_path.read_bytes()).hexdigest() == pdf_checkpoint['original_sha256']
assert shutil.disk_usage(HERE).free > 1024 * 1024
try:
    with ZipFile(deck_path, 'a', ZIP_DEFLATED) as deck:
        entry = deck.getinfo(PART)
        deck.filelist = [info for info in deck.filelist if info.filename != PART]
        del deck.NameToInfo[PART]
        deck.writestr(entry, (HERE / 'slide10.xml').read_bytes())
    with ZipFile(deck_path) as deck:
        assert len(deck.namelist()) == len(set(deck.namelist())) == len(before)
        changed = [n for n in deck.namelist() if hashlib.sha256(deck.read(n)).hexdigest() != before[n]]
        assert changed == [PART]
    with pdf_path.open('ab') as pdf:
        pdf.write((HERE / 'presentation_pdf_update.bin').read_bytes())
        pdf.flush()
        os.fsync(pdf.fileno())
    assert hashlib.sha256(pdf_path.read_bytes()).hexdigest() == pdf_checkpoint['updated_sha256']
    assert len(PdfReader(pdf_path).pages) == 31
except Exception:
    with deck_path.open('r+b') as deck:
        deck.seek(zip_checkpoint['start_dir'])
        deck.write((ARCHIVE / 'original_zip_directory.bin').read_bytes())
        deck.truncate()
    with pdf_path.open('r+b') as pdf:
        pdf.truncate(pdf_checkpoint['original_size'])
    raise

for name in ['native_equations.json', 'null_controller_dimension.pdf',
             'null_controller_dimension.png', 'null_controller_dimension.svg']:
    shutil.copy2(HERE / name, ASSETS / name)
shutil.copy2(HERE / 'null_controller_dimension.tex', ASSETS / 'sources/null_controller_dimension.tex')
verification = json.loads((HERE / 'verification.json').read_text())
verification.update({'changed_package_parts': changed, 'all_other_package_parts_byte_identical': True,
                     'native_equation_and_sources_synchronized': True,
                     'native_and_pdf_renders_visually_checked': True,
                     'supplementary_pdf_unchanged_and_current': True, 'active_deliverables_updated': True})
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
readme = FINAL / 'README.txt'
entry = ('2026-10-01: Null-space controller (footer 18 / physical slide 19) now writes '
         'Null space dimension = 7 - 6 = 1 in place of dim(ker J). The full-Jacobian-rank '
         'qualification remains above. The equation stays native/editable in 22 pt regular '
         'Cambria Math, with an upright plain-language label. Its LaTeX source, alternative '
         'description, catalog and PDF/PNG/SVG assets agree. The full PDF is refreshed; '
         'the other 30 pages, other equations, notes, media and speaking files are unchanged. '
         'See ../experiments/slide18_plain_dimension_20261001/verification.json.\n\n')
readme.write_text(entry + readme.read_text(encoding='utf-8'), encoding='utf-8')
print(json.dumps(verification, indent=2))

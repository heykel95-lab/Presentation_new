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
entry=('2026-10-01: On Null-space controller (footer 18 / physical 19), conditioning now '
       'explicitly seeks a larger minimum singular value sigma_min of J, moving away from singularities. '
       'This matches the minimum-singular-value quantity used in the results plot. '
       'All other content, equations, notes and speech are unchanged. The full PDF is updated; '
       'the supplementary PDF is unchanged. See ../experiments/slide18_singular_value_20261001/verification.json.\n\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
agents=ROOT/'AGENTS.md';contents=agents.read_text(encoding='utf-8');heading='# Thesis and presentation workspace\n'
assert contents.startswith(heading)
rule=('\n## Conditioning and minimum singular value (2026-10-01)\n\n'
      'On Null-space controller (footer 18 / physical slide 19), the second\n'
      'conditioning bullet reads: Seeks a larger minimum singular value sigma_min\n'
      'of J, moving away from singularities. Display sigma_min with a native\n'
      'Greek sigma and subscript min, matching the metric in the conditioning\n'
      'plot. Retain the first posture-adjustment bullet and all native equations.\n'
      'Speaking files and notes remain unchanged. See\n'
      'experiments/slide18_singular_value_20261001/verification.json.\n')
agents.write_text(heading+rule+contents[len(heading):],encoding='utf-8')
verification.update({'changed_package_parts':changed,'all_other_package_parts_byte_identical':True,
    'native_render_visually_checked':True,'speaking_files_unchanged':True,
    'supplementary_pdf_unchanged':True,'installed':True})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Saved the minimum singular value explanation in PowerPoint and PDF.')

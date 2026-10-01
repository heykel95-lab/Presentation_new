from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from pypdf import PdfReader
import hashlib, json, os

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
PARTS=['ppt/slides/slide36.xml','ppt/slides/slide37.xml','ppt/slides/slide13.xml']
deck_path=FINAL/'Thesis_Defense_gg0_v3.pptx'
pdf_path=FINAL/'Thesis_Defense_gg0_v3.pdf'
before=json.loads((ARCHIVE/'package_hashes_before.json').read_text())
zip_checkpoint=json.loads((ARCHIVE/'zip_checkpoint.json').read_text())
pdf_checkpoint=json.loads((HERE/'pdf_checkpoint.json').read_text())
verification=json.loads((HERE/'verification.json').read_text(encoding='utf-8'))
assert verification['other_28_pages_pixel_identical']
with ZipFile(deck_path) as deck:
    assert set(deck.namelist())==set(before)
    assert deck.start_dir==zip_checkpoint['start_dir']
    assert all(hashlib.sha256(deck.read(n)).hexdigest()==h for n,h in before.items())
assert pdf_path.stat().st_size==pdf_checkpoint['original_size']
assert hashlib.sha256(pdf_path.read_bytes()).hexdigest()==pdf_checkpoint['original_sha256']
try:
    with ZipFile(deck_path,'a',ZIP_DEFLATED) as deck:
        entries={name:deck.getinfo(name) for name in PARTS}
        deck.filelist=[info for info in deck.filelist if info.filename not in entries]
        for name in entries: del deck.NameToInfo[name]
        for name in PARTS: deck.writestr(entries[name],(HERE/Path(name).name).read_bytes())
    with ZipFile(deck_path) as deck:
        assert len(deck.namelist())==len(set(deck.namelist()))==len(before)
        changed=[n for n,h in before.items() if hashlib.sha256(deck.read(n)).hexdigest()!=h]
        assert set(changed)==set(PARTS)
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
entry=('2026-10-01: Disturbance demonstration captions now identify the settings supplied by the user: '
       'Without null-space control → Damping only (footer 19 / physical slide 20) and Conditioning only '
       '(footer 20 / physical slide 21). On Null-space experiment (footer 21 / physical slide 22), '
       'the baseline reads Disturbance without null-space control torque as one two-line bullet; '
       'the lower settings row is moved down for spacing. The recordings, 23 s split, audio, posters, '
       'playback, numerical settings, equations and speaking material are unchanged. The full PDF '
       'is updated and its other 28 pages are pixel-identical. The five-page supplementary PDF is '
       'unchanged. See ../experiments/disturbance_labels_20261001/verification.json.\n\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
agents=ROOT/'AGENTS.md'
contents=agents.read_text(encoding='utf-8')
heading='# Thesis and presentation workspace\n'
assert contents.startswith(heading)
rule=('\n## Disturbance video and baseline labels (2026-10-01)\n\n'
      'The user identified the first disturbance clip as the sequence without\n'
      'null-space control followed by damping, and the second as conditioning\n'
      'only. The captions are Without null-space control → Damping only on\n'
      'footer 19 / physical slide 20 and Conditioning only on footer 20 /\n'
      'physical slide 21. This replaces the earlier generic Part 1 / Part 2\n'
      'caption requirement. Do not infer numerical controller gains. Preserve\n'
      'the exact clips, 23 s split, audio, posters, dimensions and playback.\n\n'
      'On Null-space experiment (footer 21 / physical slide 22), the baseline\n'
      'condition is Disturbance without null-space control torque, as one\n'
      'two-line bullet. All four conditions include the commanded disturbance.\n'
      'Keep the lower settings row at y = 435 pt to allow room for that label.\n'
      'Equations, parameter values, speaking files and notes remain unchanged.\n'
      'See experiments/disturbance_labels_20261001/verification.json.\n')
agents.write_text(heading+rule+contents[len(heading):],encoding='utf-8')
verification.update({'changed_package_parts':changed,'all_other_package_parts_byte_identical':True,
    'native_and_pdf_renders_visually_checked':True,'supplementary_pdf_unchanged_and_current':True,
    'active_deliverables_updated':True})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Updated PowerPoint and full PDF; only the three intended slide parts changed.')

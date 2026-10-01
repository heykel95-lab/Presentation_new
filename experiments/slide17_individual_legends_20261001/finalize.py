from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from pypdf import PdfReader
import hashlib, json, shutil, os

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FINAL = ROOT / 'Final Presentation'
ASSETS = FINAL / 'figures_and_images'
ARCHIVE = HERE / 'archive'
PART = 'ppt/slides/slide20.xml'
RELS = 'ppt/slides/_rels/slide20.xml.rels'
MEDIA = 'ppt/media/contact_legend_per_plot.png'
deck_path = FINAL / 'Thesis_Defense_gg0_v3.pptx'
pdf_path = FINAL / 'Thesis_Defense_gg0_v3.pdf'
before = json.loads((ARCHIVE / 'package_hashes_before.json').read_text())
zip_checkpoint = json.loads((ARCHIVE / 'zip_checkpoint.json').read_text())
pdf_checkpoint = json.loads((HERE / 'pdf_checkpoint.json').read_text())
verification = json.loads((HERE / 'verification.json').read_text())
assert verification['other_30_pages_pixel_identical']
assert verification['plot_and_legend_pdf_vectors_preserved']
with ZipFile(deck_path) as deck:
    assert set(deck.namelist()) == set(before)
    assert deck.start_dir == zip_checkpoint['start_dir']
    assert all(hashlib.sha256(deck.read(n)).hexdigest() == h for n, h in before.items())
assert pdf_path.stat().st_size == pdf_checkpoint['original_size']
assert hashlib.sha256(pdf_path.read_bytes()).hexdigest() == pdf_checkpoint['original_sha256']

# Publish the small new source assets before touching the active documents.
for extension in ['pdf', 'png', 'svg']:
    name = 'contact_legend_per_plot.' + extension
    shutil.copy2(HERE / name, ASSETS / name)
shutil.copy2(HERE / 'contact_legend_per_plot.tex', ASSETS / 'sources/contact_legend_per_plot.tex')
try:
    # Replace the ZIP directory references, retaining all untouched entries.
    with ZipFile(deck_path, 'a', ZIP_DEFLATED) as deck:
        entries = {name: deck.getinfo(name) for name in [PART, RELS]}
        deck.filelist = [info for info in deck.filelist if info.filename not in entries]
        for name in entries:
            del deck.NameToInfo[name]
        deck.writestr(entries[PART], (HERE / 'slide20.xml').read_bytes())
        deck.writestr(entries[RELS], (HERE / 'slide20.xml.rels').read_bytes())
        deck.writestr(MEDIA, (HERE / 'contact_legend_per_plot.png').read_bytes())
    with ZipFile(deck_path) as deck:
        assert len(deck.namelist()) == len(set(deck.namelist())) == len(before) + 1
        assert set(deck.namelist()) == set(before) | {MEDIA}
        changed = [name for name, digest in before.items()
                   if hashlib.sha256(deck.read(name)).hexdigest() != digest]
        assert set(changed) == {PART, RELS}, changed
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

assert hashlib.sha256((FINAL / 'Supplementary_slides.pdf').read_bytes()).hexdigest() == verification['supplementary_pdf_sha256']
manifest_path = ASSETS / 'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
assert not any(item['asset'] == 'contact_legend_per_plot' for item in manifest)
manifest.append({
    'asset': 'contact_legend_per_plot', 'source': 'sources/contact_legend_per_plot.tex',
    'changes': '2026-10-01: On footer 17 / physical slide 18, three identical compact legends replace the single shared key. Each is centred below its data panel and contains the original black -40 mm, red TCP, and blue +40 mm labels. Original legend typography and plot geometry/data are preserved.',
    'positions_pt': verification['legend_positions_pt'],
    'verification': 'experiments/slide17_individual_legends_20261001/verification.json'
})
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
readme = FINAL / 'README.txt'
entry = ('2026-10-01: On Angular error and interaction wrench (footer 17 / physical slide 18), '
         'each plot now has its own centred three-row legend showing all three conditions: '
         'black -40 mm, red TCP, and blue +40 mm. Original labels, colours and typography '
         'are retained. Plot proportions, positions, data and headings are unchanged. '
         'Updated the embedded legend, source PDF/PNG/SVG/TeX assets and full presentation '
         'PDF, preserving vector plots. All other 30 PDF pages and all other PowerPoint '
         'parts are unchanged. The supplementary PDF and speaking material are unchanged. '
         'See ../experiments/slide17_individual_legends_20261001/verification.json.\n\n')
readme.write_text(entry + readme.read_text(encoding='utf-8'), encoding='utf-8')
agents = ROOT / 'AGENTS.md'
old = ('The 900 x 310 pt figure box is at (30, 135) pt. The three headings start at\n'
       '107 pt vertically. The shared legend is centred at x = 480 pt, with its top\n'
       'at 425 pt. This replaces the earlier near-square contact-panel proportions\n')
new = ('The 900 x 310 pt figure box is at (30, 135) pt. The three headings start at\n'
       '107 pt vertically. Each plot has a three-row legend containing all three\n'
       'conditions: black -40 mm, red TCP, and blue +40 mm. Centre these legends\n'
       'at x = 206, 506 and 806 pt, with top y = 398 pt and natural size\n'
       '126.382 x 60.159 pt. Use contact_legend_per_plot assets; the previous\n'
       'shared horizontal legend is retained only as an unused source asset.\n'
       'See experiments/slide17_individual_legends_20261001/verification.json.\n'
       'This replaces the earlier near-square contact-panel proportions\n')
contents = agents.read_text(encoding='utf-8')
assert old in contents
agents.write_text(contents.replace(old, new, 1), encoding='utf-8')
verification.update({
    'changed_existing_package_parts': changed, 'added_package_parts': [MEDIA],
    'all_other_package_parts_byte_identical': True,
    'legend_source_assets_synchronized': True,
    'native_and_pdf_renders_visually_checked': True,
    'supplementary_pdf_unchanged_and_current': True, 'active_deliverables_updated': True
})
(HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))

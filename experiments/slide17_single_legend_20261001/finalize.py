from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json, os

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
DECK=FINAL/'Thesis_Defense_gg0_v3.pptx'
PDF=FINAL/'Thesis_Defense_gg0_v3.pdf'
PART='ppt/slides/slide20.xml'
before=json.loads((ARCHIVE/'package_hashes_before.json').read_text())
zip_checkpoint=json.loads((ARCHIVE/'zip_checkpoint.json').read_text())
pdf_checkpoint=json.loads((HERE/'pdf_checkpoint.json').read_text())
verification=json.loads((HERE/'verification.json').read_text())
assert verification['only_removed_legend_areas_differ']
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
        deck.writestr(entry,(HERE/'slide20.xml').read_bytes())
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
for name,digest in verification['speaking_file_hashes'].items():
    assert hashlib.sha256((FINAL/name).read_bytes()).hexdigest()==digest
manifest_path=FINAL/'figures_and_images/manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
item=next(item for item in manifest if item['asset']=='contact_legend_per_plot')
item['positions_pt']=[p for p in item['positions_pt'] if p['plot']=='normal force']
item['changes']='2026-10-01: At the user request, retain only the existing middle three-row legend on footer 17 / physical slide 18. Remove its left and right duplicates. The retained key, plots, data, typography and all asset bytes are unchanged.'
item['verification']='experiments/slide17_single_legend_20261001/verification.json'
manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
readme=FINAL/'README.txt'
entry=('2026-10-01: On Angular error and interaction wrench (footer 17 / physical slide 18), '
       'removed the left and right legend duplicates and retained only the existing middle legend. '
       'Its labels, size and position are unchanged. Updated PowerPoint and the full PDF; all '
       'other PDF pixels, notes, speaking files and supplementary slides are unchanged. '
       'See ../experiments/slide17_single_legend_20261001/verification.json.\n\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
agents=ROOT/'AGENTS.md'
contents=agents.read_text(encoding='utf-8')
old=('107 pt vertically. Each plot has a three-row legend containing all three\n'
     'conditions: black -40 mm, red TCP, and blue +40 mm. Centre these legends\n'
     'at x = 206, 506 and 806 pt, with top y = 398 pt and natural size\n'
     '126.382 x 60.159 pt. Use contact_legend_per_plot assets; the previous\n'
     'shared horizontal legend is retained only as an unused source asset.\n'
     'See experiments/slide17_individual_legends_20261001/verification.json.\n')
new=('107 pt vertically. Keep only the existing middle three-row legend, with\n'
     'black -40 mm, red TCP, and blue +40 mm labels. Its centre is x = 506 pt,\n'
     'its top is y = 398 pt, and its natural size is 126.382 x 60.159 pt.\n'
     'The left and right legend copies were removed at the user request.\n'
     'Use the unchanged contact_legend_per_plot assets. This supersedes the\n'
     'three-legend layout; do not restore the duplicates. See\n'
     'experiments/slide17_single_legend_20261001/verification.json.\n')
assert old in contents
agents.write_text(contents.replace(old,new,1),encoding='utf-8')
verification.update({'changed_package_parts':changed,'all_other_package_parts_byte_identical':True,
    'final_slide_visually_checked':True,'speaking_files_unchanged':True,
    'supplementary_pdf_unchanged':True,'installed':True})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Saved slide 17 with only the middle legend in PowerPoint and PDF.')

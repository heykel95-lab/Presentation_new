from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from xml.etree import ElementTree as E
import json,hashlib,os,re,shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FINAL=ROOT/'Final Presentation'
ARCHIVE=HERE/'archive'
DECK=FINAL/'Thesis_Defense_gg0_v3.pptx'
before=json.loads((ARCHIVE/'package_hashes_before.json').read_text())
zip_checkpoint=json.loads((ARCHIVE/'zip_checkpoint.json').read_text())
verification=json.loads((HERE/'verification.json').read_text())
assert verification['presentation_other_pages_pixel_identical'] and verification['supplementary_other_pages_pixel_identical']
updates={f'ppt/slides/{name}':(HERE/name).read_bytes() for name in ['slide5.xml','slide8.xml','slide10.xml','slide25.xml']}
updates.update({'ppt/media/image5.png':(HERE/'cartesian_pose_position.png').read_bytes(),
                'ppt/media/image6.png':(HERE/'cartesian_pose_orientation.png').read_bytes()})
with ZipFile(DECK) as deck:
    assert deck.start_dir==zip_checkpoint['start_dir']
    assert set(deck.namelist())==set(before)
    assert all(hashlib.sha256(deck.read(n)).hexdigest()==h for n,h in before.items())
    ns={'m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
    for part,data in updates.items():
        if part.endswith('.xml'):
            old_math=[E.tostring(n) for n in E.fromstring(deck.read(part)).findall('.//m:oMath',ns)]
            new_math=[E.tostring(n) for n in E.fromstring(data).findall('.//m:oMath',ns)]
            assert old_math==new_math
    assert E.fromstring(updates['ppt/slides/slide25.xml']).get('show')=='0'
pdfs=[]
for prefix,name in [('presentation','Thesis_Defense_gg0_v3.pdf'),('supplementary','Supplementary_slides.pdf')]:
    checkpoint=json.loads((HERE/f'{prefix}_checkpoint.json').read_text())
    path=FINAL/name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==checkpoint['original_sha256']
    pdfs.append((prefix,path,checkpoint))
try:
    with ZipFile(DECK,'a',ZIP_DEFLATED) as deck:
        for part,data in updates.items():
            entry=deck.getinfo(part)
            deck.filelist=[info for info in deck.filelist if info.filename!=part]
            del deck.NameToInfo[part]
            deck.writestr(entry,data)
    with ZipFile(DECK) as deck:
        assert len(deck.namelist())==len(set(deck.namelist()))==len(before)
        changed=[n for n,h in before.items() if hashlib.sha256(deck.read(n)).hexdigest()!=h]
        assert set(changed)==set(updates)
        for name in deck.namelist():
            if re.fullmatch(r'ppt/(slides|slideMasters|slideLayouts)/[^/]+\.xml',name):
                for text in E.fromstring(deck.read(name)).iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
                    assert not re.search(r'(?<![\w(])EE(?![\w)])',text.text or ''),(name,text.text)
    for prefix,path,checkpoint in pdfs:
        with path.open('ab') as f:
            f.write((HERE/f'{prefix}_pdf_update.bin').read_bytes());f.flush();os.fsync(f.fileno())
        assert hashlib.sha256(path.read_bytes()).hexdigest()==checkpoint['updated_sha256']
except Exception:
    with DECK.open('r+b') as f:
        f.seek(zip_checkpoint['start_dir']);f.write((ARCHIVE/'original_zip_directory.bin').read_bytes());f.truncate()
    for _,path,checkpoint in pdfs:
        with path.open('r+b') as f:f.truncate(checkpoint['original_size'])
    raise
for name,digest in verification['speaking_file_hashes'].items():assert hashlib.sha256((FINAL/name).read_bytes()).hexdigest()==digest
assets=FINAL/'figures_and_images'
for name in ['cartesian_pose_position','cartesian_pose_orientation']:
    shutil.copy2(HERE/f'{name}.tex',assets/'sources'/f'{name}.tex')
    for ext in ['pdf','png','svg']:shutil.copy2(HERE/f'{name}.{ext}',assets/f'{name}.{ext}')
manifest=assets/'manifest.json'
shutil.copy2(manifest,ARCHIVE/'manifest.json')
entries=json.loads(manifest.read_text(encoding='utf-8'))
for entry in entries:
    if entry.get('asset') in ['cartesian_pose_position','cartesian_pose_orientation']:
        entry['changes']=entry.get('changes','')+' 2026-10-01: standalone diagram label EE is now (EE), preserving geometry and typography.'
manifest.write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(HERE/'presentation_checkpoint.json',HERE/'pdf_checkpoint.json')
readme=FINAL/'README.txt'
entry=('2026-10-01: Parenthesized standalone EE labels throughout visible slide text and the two '
       'Cartesian pose diagrams: seven labels on physical slides 5, 10, 19 and B2/28. '
       'Mathematical EE subscripts, all native equation contents, notes and speech are unchanged. '
       'The pose takeaway row is slightly wider and its equation shifts right to prevent wrapping. '
       'Updated PPTX, both PDFs and the two diagram sources/PDF/PNG/SVG assets. '
       'See ../experiments/ee_parentheses_20261001/verification.json.\n\n')
readme.write_text(entry+readme.read_text(encoding='utf-8'),encoding='utf-8')
agents=ROOT/'AGENTS.md';contents=agents.read_text(encoding='utf-8');heading='# Thesis and presentation workspace\n'
assert contents.startswith(heading)
rule=('\n## Parenthesized end-effector labels (2026-10-01)\n\n'
      'Write standalone EE in slide prose and diagram labels as (EE), including\n'
      'hidden backups. Keep mathematical EE subscripts unchanged. The two pose\n'
      'diagram sources and their PDF/PNG/SVG assets match the embedded figures.\n'
      'On Cartesian pose, the takeaway textbox is 630 pt wide and the unchanged\n'
      'native equation starts at x=715 pt, so the bottom row stays on one line.\n'
      'Preserve the revised speech and notes. See\n'
      'experiments/ee_parentheses_20261001/verification.json.\n')
agents.write_text(heading+rule+contents[len(heading):],encoding='utf-8')
verification.update({'changed_package_parts':changed,'all_other_package_parts_byte_identical':True,
    'native_render_visually_checked':True,'speaking_files_unchanged':True,
    'all_visible_prose_EE_parenthesized':True,'native_equation_contents_unchanged':True,
    'backup_hidden_flag_preserved':True,'installed':True})
(HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print('Saved all seven (EE) labels in PowerPoint and both PDFs. All other package parts and speaking files are unchanged.')
